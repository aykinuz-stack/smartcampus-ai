"""
YD-01 Yabanci Dil Modulu - Streamlit UI
========================================
Kurumsal dil ogretim platformu — CEFR uyumlu.
Preschool/Grade 1-4 mufredat, interaktif aktiviteler,
gunluk plan, sinav, odev, dijital kaynaklar.
"""

from __future__ import annotations

import json
_json = json
import os
from datetime import datetime, timedelta

import streamlit as st

# Agir importlar yd_content.py ve yd_tools.py'a tasindi (lazy import)
# Sadece ana dosyada gereken importlar:
from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("yabanci_dil")
except Exception:
    pass
from utils.tenant import get_tenant_dir
from views.yd_core import (
    _CLR_BLUE, _CLR_DARK, _CLR_GREEN, _CLR_ORANGE, _CLR_PURPLE, _CLR_RED, _CLR_TEAL, _CLR_CYAN,
    _comp_rendered_keys,
    _get_academic_year_str, _get_sinif_sube_options, _yd_sinif_to_level,
    _get_eng_store, _get_eng_student_id,
)

import logging as _logging
_logger = _logging.getLogger("yabanci_dil")

# Centralized data paths
_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "english")
_WP_PATH = os.path.join(_DATA_DIR, "weekly_plans.json")
_YP_PATH = os.path.join(_DATA_DIR, "year_plans.json")

def _data_path(filename: str) -> str:
    """Return full path for a file in data/english/."""
    return os.path.join(_DATA_DIR, filename)

# Cached data loader
_DATA_CACHE: dict = {}

def _load_json_cached(filename: str, force: bool = False) -> dict | list:
    """Load JSON file with session-level caching."""
    cache_key = f"_yd_cache_{filename}"
    if not force and cache_key in st.session_state:
        return st.session_state[cache_key]
    path = _data_path(filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = _json.load(f)
            st.session_state[cache_key] = data
            return data
        except (_json.JSONDecodeError, OSError) as e:
            _logger.warning("Failed to load %s: %s", filename, e)
            return {}
    return {}

def _save_json_cached(filename: str, data) -> bool:
    """Save JSON and update cache."""
    path = _data_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            _json.dump(data, f, ensure_ascii=False, indent=2)
        cache_key = f"_yd_cache_{filename}"
        st.session_state[cache_key] = data
        return True
    except OSError as e:
        _logger.error("Failed to save %s: %s", filename, e)
        return False

def _validate_grade(grade_str: str) -> str:
    """Validate and sanitize grade input."""
    valid = {"preschool", "grade1", "grade2", "grade3", "grade4",
             "grade5", "grade6", "grade7", "grade8",
             "grade9", "grade10", "grade11", "grade12",
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"}
    return grade_str if grade_str in valid else "grade5"

def _validate_week(week: int) -> int:
    """Validate week number is within bounds."""
    return max(1, min(36, int(week)))

def _sanitize_html(text: str) -> str:
    """Basic HTML sanitization for user-generated content."""
    if not isinstance(text, str):
        return str(text)
    return text.replace("<script", "&lt;script").replace("</script", "&lt;/script").replace("javascript:", "")


# ══════════════════════════════════════════════════════════════════════════════
# RENK PALETİ
# ══════════════════════════════════════════════════════════════════════════════

_CLR_BLUE = "#4472C4"
_CLR_DARK = "#0B0F19"
_CLR_GREEN = "#70AD47"
_CLR_ORANGE = "#ED7D31"
_CLR_PURPLE = "#7c3aed"
_CLR_RED = "#dc2626"
_CLR_TEAL = "#2563eb"
_CLR_CYAN = "#0891b2"


# ══════════════════════════════════════════════════════════════════════════════
# CSS İNJECTION — PREMIUM+++
# ══════════════════════════════════════════════════════════════════════════════

def _inject_yd_css():
    """Enterprise Ultra Premium Diamond CSS — OD/AT modulleriyle ayni tasarim dili."""
    inject_common_css("yd")
    if st.session_state.get("_yd_css_injected"):
        return
    st.session_state["_yd_css_injected"] = True
    st.markdown("""<style>
    /* font: sistem fontu kullaniliyor */
    :root {
        --dk-primary: #6366F1;
        --dk-primary-dark: #A5B4FC;
        --dk-primary-light: #6366F1;
        --dk-success: #10b981;
        --dk-warning: #f59e0b;
        --dk-danger: #ef4444;
        --dk-purple: #8b5cf6;
        --dk-teal: #0d9488;
        --dk-dark: #0B0F19;
        --dk-gray-50: #131825;
        --dk-gray-100: #1A2035;
        --dk-gray-200: rgba(212,175,55,0.2);
        --dk-gray-500: #94A3B8;
        --dk-gray-800: #E2E8F0;
    }

    /* Radio ve checkbox label'lari koyu temada okunur yap */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] p,
    div[data-testid="stRadio"] span,
    div[data-testid="stCheckbox"] label,
    div[role="radiogroup"] label {
        color: #E2E8F0 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    /* Selectbox ve label'lar da okunur olsun */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] p {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }

    /* ===== 3. SEVIYE TABS ===== */
    div[data-testid="stTabs"] div[data-testid="stTabs"] div[data-testid="stTabs"] > div[role="tablist"] {
        background: linear-gradient(135deg, #0B0F19 0%, #1A2035 100%);
        border: 1px solid rgba(212,175,55,0.15);
        border-radius: 8px; padding: 3px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
    }
    div[data-testid="stTabs"] div[data-testid="stTabs"] div[data-testid="stTabs"] > div[role="tablist"] > button {
        color: #94A3B8 !important; font-size: 0.75rem !important;
        font-weight: 500 !important; padding: 6px 12px !important;
    }
    div[data-testid="stTabs"] div[data-testid="stTabs"] div[data-testid="stTabs"] > div[role="tablist"] > button[aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1, #6366F1) !important;
        color: #0B0F19 !important;
        box-shadow: 0 2px 6px rgba(212,175,55,0.3) !important;
    }
    div[data-testid="stTabs"] div[data-testid="stTabs"] div[data-testid="stTabs"] > div[role="tablist"] > button:hover {
        background: rgba(212,175,55,0.1) !important; color: #6366F1 !important;
    }

    /* ===== METRIC CARDS ===== */
    div[data-testid="stMetric"] {
        background: #131825; border: 1px solid rgba(212,175,55,0.2); border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease; border-left: 4px solid #6366F1;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px); box-shadow: 0 8px 20px rgba(212,175,55,0.15);
    }
    div[data-testid="stMetric"] label {
        color: #94A3B8 !important; font-size: 0.75rem !important;
        font-weight: 600 !important; text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #6366F1 !important; font-weight: 800 !important; font-size: 1.5rem !important;
    }

    /* ===== BUTTONS — tum butonlar gold tema ===== */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #A5B4FC 0%, #6366F1 100%) !important;
        color: #0B0F19 !important;
        border: none !important; border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(212,175,55,0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        box-shadow: 0 6px 20px rgba(212,175,55,0.4) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="stBaseButton-secondary"],
    .stButton > button:not([kind]) {
        background: #131825 !important; color: #6366F1 !important;
        border-radius: 10px !important; border: 1.5px solid rgba(212,175,55,0.3) !important;
        font-weight: 600 !important; transition: all 0.2s ease !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button[data-testid="stBaseButton-secondary"]:hover,
    .stButton > button:not([kind]):hover {
        border-color: #6366F1 !important; background: rgba(212,175,55,0.1) !important;
        color: #6366F1 !important;
    }
    /* Streamlit global primaryColor override */
    :root { --primary-color: #6366F1 !important; }

    /* ===== EXPANDERS ===== */
    details[data-testid="stExpander"] {
        border: 1px solid rgba(212,175,55,0.2) !important; border-radius: 12px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.15) !important; overflow: hidden;
        background: #131825 !important;
    }
    details[data-testid="stExpander"] summary {
        font-weight: 600 !important; padding: 12px 16px !important;
        color: #E2E8F0 !important;
    }

    /* ===== INPUTS ===== */
    div[data-baseweb="select"] > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important; border-color: rgba(212,175,55,0.2) !important;
        background: #131825 !important; color: #E2E8F0 !important;
        transition: all 0.2s ease !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(212,175,55,0.15) !important;
    }

    /* ===== DATA TABLES ===== */
    .stDataFrame {
        border-radius: 12px !important; overflow: hidden !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
    }

    /* ===== DOWNLOAD BUTTON ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #A5B4FC 0%, #6366F1 100%) !important;
        color: #0B0F19 !important; border: none !important; border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(212,175,55,0.25) !important;
    }
    .stDownloadButton > button:hover {
        box-shadow: 0 6px 18px rgba(212,175,55,0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* ===== DIVIDERS ===== */
    hr {
        border: none !important; height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, rgba(212,175,55,0.3) 50%, transparent 100%) !important;
        margin: 1rem 0 !important;
    }

    /* ===== ALERTS & RADIO ===== */
    .stAlert { border-radius: 10px !important; }
    .stRadio > div { gap: 0.5rem; }
    .stRadio > div > label { border-radius: 10px !important; padding: 6px 12px !important; }

    /* ===== GLOBAL LABEL & TEXT VISIBILITY (koyu arka plan uyumu) ===== */
    /* Radio — baslik etiketi ("Secim:" vb.) */
    div[data-testid="stRadio"] > label,
    div[data-testid="stRadio"] > label p,
    div[data-testid="stRadio"] > label span,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    /* Radio — tum secenekler */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label *,
    div[data-testid="stRadio"] [role="radiogroup"] label,
    div[data-testid="stRadio"] [role="radiogroup"] label * {
        color: #c0c0d8 !important;
        font-weight: 600 !important;
    }
    /* Radio — secili secenek (gold vurgu) */
    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stRadio"] label[data-checked="true"] *,
    div[data-testid="stRadio"] [aria-checked="true"],
    div[data-testid="stRadio"] [aria-checked="true"] *,
    div[data-testid="stRadio"] input[type="radio"]:checked ~ div,
    div[data-testid="stRadio"] input[type="radio"]:checked ~ div *,
    div[data-testid="stRadio"] input[type="radio"]:checked + label,
    div[data-testid="stRadio"] input[type="radio"]:checked + label * {
        color: #6366F1 !important;
        font-weight: 700 !important;
    }
    /* Selectbox / text input / number input etiketleri */
    div[data-testid="stSelectbox"] > label,
    div[data-testid="stSelectbox"] > label p,
    div[data-testid="stTextInput"] > label,
    div[data-testid="stTextInput"] > label p,
    div[data-testid="stNumberInput"] > label,
    div[data-testid="stNumberInput"] > label p,
    div[data-testid="stMultiSelect"] > label,
    div[data-testid="stMultiSelect"] > label p,
    div[data-testid="stDateInput"] > label,
    div[data-testid="stDateInput"] > label p,
    div[data-testid="stTextArea"] > label,
    div[data-testid="stTextArea"] > label p {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    /* Alert / info / warning / success mesaj metinleri */
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span {
        color: #E2E8F0 !important;
    }
    /* Checkbox etiketleri */
    div[data-testid="stCheckbox"] label span,
    div[data-testid="stCheckbox"] label p {
        color: #E2E8F0 !important;
    }
    /* Slider etiketleri */
    div[data-testid="stSlider"] > label,
    div[data-testid="stSlider"] > label p {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    /* Genel paragraf ve baslik renkleri (koyu arka plan icin) */
    .stMarkdown p, .stMarkdown li {
        color: #E2E8F0;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #6366F1 !important;
    }
    </style>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# UI YARDIMCI BİLEŞENLER
# ══════════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════════
# UI YARDIMCI BİLEŞENLER
# ══════════════════════════════════════════════════════════════════════════════

def _render_grade_flipbook(grade: str):
    """Sinif bazli flipbook okuma kitaplari bilesenini render eder."""
    _GRADE_LABELS = {
        "preschool": "Pre-A1", "1": "A1.1", "2": "A1.2",
        "3": "A1.3", "4": "A1+", "5": "A2.1",
        "6": "A2.2", "7": "A2.3", "8": "A2.4",
    }
    label = _GRADE_LABELS.get(grade, "A1")
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,rgba(201,168,76,.10),rgba(201,168,76,.03));'
        'border:1px solid rgba(201,168,76,.2);border-radius:12px;padding:14px 18px;margin-bottom:8px">'
        '<span style="font-size:1.1rem;font-weight:700;color:#6366F1">'
        '\U0001f4d6 Okuma Kitaplar\u0131 \u2014 Flipbook</span>'
        f'<span style="font-size:.75rem;color:#888;margin-left:10px">'
        f'CEFR {label} seviye hikayeler | Sesli dinleme + T\u00fcrk\u00e7e \u00e7eviri</span></div>',
        unsafe_allow_html=True,
    )
    from views.kdg_engine import build_flipbook_html
    st.components.v1.html(build_flipbook_html(grade), height=700, scrolling=True)


def _render_grade_resources(grade: str):
    """Sinif bazli dis kaynak okuma platformlarini render eder."""
    _GRADE_LABELS = {
        "preschool": "Pre-A1", "1": "A1.1", "2": "A1.2",
        "3": "A1.3", "4": "A1+", "5": "A2.1",
        "6": "A2.2", "7": "A2.3", "8": "A2.4",
    }
    label = _GRADE_LABELS.get(grade, "A1")
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,rgba(201,168,76,.10),rgba(201,168,76,.03));'
        'border:1px solid rgba(201,168,76,.2);border-radius:12px;padding:14px 18px;margin-bottom:8px">'
        '<span style="font-size:1.1rem;font-weight:700;color:#6366F1">'
        '\U0001f310 D\u0131\u015f Kaynaklar \u2014 Online Okuma Platformlar\u0131</span>'
        f'<span style="font-size:.75rem;color:#888;margin-left:10px">'
        f'CEFR {label} seviye | StoryWeaver, British Council, Oxford Owl ve daha fazlas\u0131</span></div>',
        unsafe_allow_html=True,
    )
    from views.kdg_engine import build_reading_resources_html
    st.components.v1.html(build_reading_resources_html(grade), height=750, scrolling=True)


# ══════════════════════════════════════════════════════════════════════════════
# YABANCI DİL İÇERİĞİ
# ══════════════════════════════════════════════════════════════════════════════

def _build_vocab_html(username="misafir"):
    """Ingilizce Kelime Quiz oyunu — Premium Ultra Diamond Edition + Kullanici Bazli Ilerleme."""
    _u = username.replace("'", "")
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>"
        "*{margin:0;padding:0;box-sizing:border-box;}"
        "body{background:#010012;overflow:hidden;font-family:'Segoe UI',Arial,sans-serif;}"
        "#wrap{position:relative;width:820px;margin:0 auto;"
        "background:linear-gradient(135deg,rgba(8,4,30,0.98),rgba(3,3,20,0.99));"
        "border:2px solid rgba(140,90,255,0.5);border-radius:20px;"
        "box-shadow:0 0 60px rgba(120,60,255,0.35),0 0 120px rgba(80,40,200,0.15),"
        "inset 0 0 60px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,255,255,0.05);overflow:hidden;}"
        "@keyframes borderPulse{0%,100%{border-color:rgba(140,90,255,0.5);box-shadow:0 0 60px rgba(120,60,255,0.35),0 0 120px rgba(80,40,200,0.15)}"
        "50%{border-color:rgba(100,200,255,0.5);box-shadow:0 0 60px rgba(60,150,255,0.35),0 0 120px rgba(40,100,200,0.15)}}"
        "#wrap{animation:borderPulse 6s ease-in-out infinite;}"
        "#topbar{background:linear-gradient(180deg,rgba(12,8,45,0.97),rgba(6,4,30,0.95));"
        "padding:12px 24px;display:flex;align-items:center;justify-content:space-between;"
        "border-bottom:1px solid rgba(140,100,255,0.25);min-height:64px;"
        "backdrop-filter:blur(10px);}"
        "#topbar .level-badge{background:linear-gradient(135deg,#7c4dff,#448aff,#00e5ff);"
        "padding:8px 22px;border-radius:24px;color:#fff;font-weight:800;font-size:16px;"
        "text-shadow:0 0 15px rgba(100,180,255,0.7);letter-spacing:1px;"
        "box-shadow:0 0 20px rgba(100,150,255,0.4),inset 0 1px 0 rgba(255,255,255,0.2);}"
        "#topbar .score-box{color:#e8d5ff;font-size:16px;font-weight:700;"
        "text-shadow:0 0 10px rgba(180,140,255,0.5);}"
        "#topbar .streak-box{color:#ffab40;font-size:18px;font-weight:800;"
        "text-shadow:0 0 15px rgba(255,170,50,0.6);min-width:60px;text-align:center;}"
        "#progress-bar{height:6px;background:rgba(255,255,255,0.08);display:none;"
        "border-bottom:1px solid rgba(140,100,255,0.15);}"
        "#progress-fill{height:100%;width:0%;background:linear-gradient(90deg,#7c4dff,#448aff,#00e5ff);"
        "transition:width 0.5s ease;box-shadow:0 0 15px rgba(100,150,255,0.5);}"
        "canvas{display:block;}"
        "</style></head><body>"
        "<div id='wrap'>"
        "<div id='topbar' style='display:none;'>"
        "<span class='level-badge' id='lvlBadge'>A1</span>"
        "<span class='score-box' id='scoreBox'>Skor: 0</span>"
        "<span class='streak-box' id='streakBox'></span>"
        "<span class='score-box' id='progressText'>0/100</span>"
        "</div>"
        "<div id='progress-bar' style='display:none;'><div id='progress-fill'></div></div>"
        "<canvas id='c' width='820' height='640'></canvas>"
        "</div>"
        "<script>"
        "if(!CanvasRenderingContext2D.prototype.roundRect){"
        "CanvasRenderingContext2D.prototype.roundRect=function(x,y,w,h,r){"
        "if(typeof r==='number')r={tl:r,tr:r,br:r,bl:r};"
        "this.beginPath();this.moveTo(x+r.tl,y);"
        "this.lineTo(x+w-r.tr,y);this.quadraticCurveTo(x+w,y,x+w,y+r.tr);"
        "this.lineTo(x+w,y+h-r.br);this.quadraticCurveTo(x+w,y+h,x+w-r.br,y+h);"
        "this.lineTo(x+r.bl,y+h);this.quadraticCurveTo(x,y+h,x,y+h-r.bl);"
        "this.lineTo(x,y+r.tl);this.quadraticCurveTo(x,y,x+r.tl,y);"
        "this.closePath();return this;};}"
        "var W=820,H=640;"
        "var canvas=document.getElementById('c');"
        "var ctx=canvas.getContext('2d');"
        "var topbar=document.getElementById('topbar');"
        "var progBar=document.getElementById('progress-bar');"
        "var progFill=document.getElementById('progress-fill');"
        "var lvlBadge=document.getElementById('lvlBadge');"
        "var scoreBox=document.getElementById('scoreBox');"
        "var streakBox=document.getElementById('streakBox');"
        "var progressText=document.getElementById('progressText');"
        "var USERNAME='" + _u + "';"
        "var LS_KEY='vocab_game_'+USERNAME;"
        "var LEVELS=['A1','A2','B1','B2','C1','C2'];"
        "var LEVEL_COLORS={A1:'#69f0ae',A2:'#40c4ff',B1:'#ffab40',B2:'#ff6e40',C1:'#ff5252',C2:'#e040fb'};"
        "var LEVEL_GRADIENTS={A1:['#69f0ae','#00e676'],A2:['#40c4ff','#448aff'],B1:['#ffab40','#ff9100'],B2:['#ff6e40','#ff3d00'],C1:['#ff5252','#d50000'],C2:['#e040fb','#aa00ff']};"
        "var LEVEL_LABELS={A1:'Beginner',A2:'Elementary',B1:'Intermediate',B2:'Upper-Int.',C1:'Advanced',C2:'Mastery'};"
        "var LEVEL_SIZE={A1:202,A2:202,B1:298,B2:286,C1:263,C2:272};"
        "var WORDS={A1:[{t:'ev',e:'house'},{t:'okul',e:'school'},{t:'kitap',e:'book'},{t:'su',e:'water'},{t:'araba',e:'car'},{t:'kedi',e:'cat'},{t:'köpek',e:'dog'},{t:'anne',e:'mother'},{t:'baba',e:'father'},{t:'kardeş',e:'sibling'},{t:'arkadaş',e:'friend'},{t:'öğretmen',e:'teacher'},{t:'öğrenci',e:'student'},{t:'doktor',e:'doctor'},{t:'yemek',e:'food'},{t:'ekmek',e:'bread'},{t:'süt',e:'milk'},{t:'çay',e:'tea'},{t:'kahve',e:'coffee'},{t:'meyve',e:'fruit'},{t:'elma',e:'apple'},{t:'portakal',e:'orange'},{t:'muz',e:'banana'},{t:'masa',e:'table'},{t:'sandalye',e:'chair'},{t:'yatak',e:'bed'},{t:'kapı',e:'door'},{t:'pencere',e:'window'},{t:'güneş',e:'sun'},{t:'ay',e:'moon'},{t:'yıldız',e:'star'},{t:'deniz',e:'sea'},{t:'dağ',e:'mountain'},{t:'nehir',e:'river'},{t:'ağaç',e:'tree'},{t:'çiçek',e:'flower'},{t:'renk',e:'color'},{t:'kırmızı',e:'red'},{t:'mavi',e:'blue'},{t:'yeşil',e:'green'},{t:'sarı',e:'yellow'},{t:'beyaz',e:'white'},{t:'siyah',e:'black'},{t:'büyük',e:'big'},{t:'küçük',e:'small'},{t:'sıcak',e:'hot'},{t:'soğuk',e:'cold'},{t:'güzel',e:'beautiful'},{t:'çirkin',e:'ugly'},{t:'iyi',e:'good'},{t:'kötü',e:'bad'},{t:'hızlı',e:'fast'},{t:'yavaş',e:'slow'},{t:'yeni',e:'new'},{t:'eski',e:'old'},{t:'genç',e:'young'},{t:'uzun',e:'tall'},{t:'kısa',e:'short'},{t:'göz',e:'eye'},{t:'kulak',e:'ear'},{t:'burun',e:'nose'},{t:'ağız',e:'mouth'},{t:'el',e:'hand'},{t:'ayak',e:'foot'},{t:'baş',e:'head'},{t:'kalp',e:'heart'},{t:'saat',e:'clock'},{t:'gün',e:'day'},{t:'gece',e:'night'},{t:'sabah',e:'morning'},{t:'akşam',e:'evening'},{t:'hafta',e:'week'},{t:'ay',e:'month'},{t:'yıl',e:'year'},{t:'para',e:'money'},{t:'iş',e:'work'},{t:'oyun',e:'game'},{t:'müzik',e:'music'},{t:'film',e:'movie'},{t:'resim',e:'picture'},{t:'kalem',e:'pen'},{t:'defter',e:'notebook'},{t:'silgi',e:'eraser'},{t:'cetvel',e:'ruler'},{t:'çanta',e:'bag'},{t:'ayakkabı',e:'shoe'},{t:'gömlek',e:'shirt'},{t:'pantolon',e:'pants'},{t:'şapka',e:'hat'},{t:'yağmur',e:'rain'},{t:'kar',e:'snow'},{t:'bulut',e:'cloud'},{t:'rüzgar',e:'wind'},{t:'toprak',e:'soil'},{t:'ateş',e:'fire'},{t:'hava',e:'air'},{t:'sokak',e:'street'},{t:'şehir',e:'city'},{t:'ülke',e:'country'},{t:'dünya',e:'world'},{t:'bir',e:'one'},{t:'iki',e:'two'},{t:'üç',e:'three'},{t:'dört',e:'four'},{t:'beş',e:'five'},{t:'altı',e:'six'},{t:'yedi',e:'seven'},{t:'sekiz',e:'eight'},{t:'dokuz',e:'nine'},{t:'on',e:'ten'},{t:'sıfır',e:'zero'},{t:'yüz',e:'hundred'},{t:'bin',e:'thousand'},{t:'parmak',e:'finger'},{t:'diş',e:'tooth'},{t:'saç',e:'hair'},{t:'boyun',e:'neck'},{t:'omuz',e:'shoulder'},{t:'diz',e:'knee'},{t:'karın',e:'stomach'},{t:'sırt',e:'back'},{t:'kan',e:'blood'},{t:'kemik',e:'bone'},{t:'deri',e:'skin'},{t:'abla',e:'elder sister'},{t:'abi',e:'elder brother'},{t:'oğul',e:'son'},{t:'kız',e:'daughter'},{t:'torun',e:'grandchild'},{t:'eş',e:'spouse'},{t:'koca',e:'husband'},{t:'karı',e:'wife'},{t:'bebek',e:'baby'},{t:'komşular',e:'neighbors'},{t:'tavşan',e:'rabbit'},{t:'fare',e:'mouse'},{t:'ayı',e:'bear'},{t:'aslan',e:'lion'},{t:'fil',e:'elephant'},{t:'maymun',e:'monkey'},{t:'yılan',e:'snake'},{t:'kaplumbağa',e:'turtle'},{t:'kurbağa',e:'frog'},{t:'çilek',e:'strawberry'},{t:'üzüm',e:'grape'},{t:'karpuz',e:'watermelon'},{t:'armut',e:'pear'},{t:'kiraz',e:'cherry'},{t:'şeftali',e:'peach'},{t:'limon',e:'lemon'},{t:'havuç',e:'carrot'},{t:'marul',e:'lettuce'},{t:'fasulye',e:'bean'},{t:'nohut',e:'chickpea'},{t:'bal',e:'honey'},{t:'şeker',e:'sugar'},{t:'tuz',e:'salt'},{t:'baharat',e:'spice'},{t:'tabak',e:'plate'},{t:'bardak',e:'glass'},{t:'kaşık',e:'spoon'},{t:'çatal',e:'fork'},{t:'bıçak',e:'knife'},{t:'tencere',e:'pot'},{t:'tava',e:'pan'},{t:'buzdolabı',e:'refrigerator'},{t:'fırın',e:'oven'},{t:'çamaşır',e:'laundry'},{t:'havlu',e:'towel'},{t:'sabun',e:'soap'},{t:'ayna',e:'mirror'},{t:'merdiven',e:'stairs'},{t:'duvar',e:'wall'},{t:'tavan',e:'ceiling'},{t:'zemin',e:'floor'},{t:'bahçe',e:'garden'},{t:'çim',e:'grass'},{t:'taş',e:'stone'},{t:'kum',e:'sand'},{t:'dalga',e:'wave'},{t:'gökyüzü',e:'sky'},{t:'gökkuşağı',e:'rainbow'},{t:'gelmek',e:'to come'},{t:'gitmek',e:'to go'},{t:'yemek',e:'to eat'},{t:'içmek',e:'to drink'},{t:'uyumak',e:'to sleep'},{t:'kalkmak',e:'to get up'},{t:'yürümek',e:'to walk'},{t:'koşmak',e:'to run'},{t:'okumak',e:'to read'},{t:'yazmak',e:'to write'},{t:'konuşmak',e:'to speak'},{t:'dinlemek',e:'to listen'},{t:'görmek',e:'to see'},{t:'duymak',e:'to hear'},{t:'bilmek',e:'to know'},{t:'istemek',e:'to want'},{t:'sevmek',e:'to love'},{t:'gülmek',e:'to laugh'},{t:'ağlamak',e:'to cry'},{t:'beklemek',e:'to wait'}],A2:[{t:'mutfak',e:'kitchen'},{t:'banyo',e:'bathroom'},{t:'salon',e:'living room'},{t:'bahçe',e:'garden'},{t:'market',e:'grocery store'},{t:'hastane',e:'hospital'},{t:'eczane',e:'pharmacy'},{t:'kütüphane',e:'library'},{t:'havaalanı',e:'airport'},{t:'istasyon',e:'station'},{t:'otel',e:'hotel'},{t:'restoran',e:'restaurant'},{t:'sinema',e:'cinema'},{t:'müze',e:'museum'},{t:'park',e:'park'},{t:'plaj',e:'beach'},{t:'tatil',e:'holiday'},{t:'seyahat',e:'travel'},{t:'bilet',e:'ticket'},{t:'pasaport',e:'passport'},{t:'bavul',e:'suitcase'},{t:'harita',e:'map'},{t:'adres',e:'address'},{t:'telefon',e:'telephone'},{t:'bilgisayar',e:'computer'},{t:'internet',e:'internet'},{t:'mesaj',e:'message'},{t:'mektup',e:'letter'},{t:'gazete',e:'newspaper'},{t:'dergi',e:'magazine'},{t:'haber',e:'news'},{t:'program',e:'program'},{t:'alışveriş',e:'shopping'},{t:'fiyat',e:'price'},{t:'indirim',e:'discount'},{t:'kasa',e:'cashier'},{t:'komşu',e:'neighbor'},{t:'misafir',e:'guest'},{t:'davet',e:'invitation'},{t:'hediye',e:'gift'},{t:'doğum günü',e:'birthday'},{t:'düğün',e:'wedding'},{t:'aile',e:'family'},{t:'çocuk',e:'child'},{t:'bebek',e:'baby'},{t:'dede',e:'grandfather'},{t:'nine',e:'grandmother'},{t:'amca',e:'uncle'},{t:'teyze',e:'aunt'},{t:'kuzen',e:'cousin'},{t:'meslek',e:'profession'},{t:'mühendis',e:'engineer'},{t:'avukat',e:'lawyer'},{t:'hemşire',e:'nurse'},{t:'aşçı',e:'cook'},{t:'şoför',e:'driver'},{t:'polis',e:'police'},{t:'itfaiye',e:'firefighter'},{t:'sanatçı',e:'artist'},{t:'sporcu',e:'athlete'},{t:'futbol',e:'football'},{t:'basketbol',e:'basketball'},{t:'yüzmek',e:'swimming'},{t:'kosmak',e:'running'},{t:'bisiklet',e:'bicycle'},{t:'otobüs',e:'bus'},{t:'tren',e:'train'},{t:'uçak',e:'airplane'},{t:'gemi',e:'ship'},{t:'trafik',e:'traffic'},{t:'kavşak',e:'intersection'},{t:'köprü',e:'bridge'},{t:'orman',e:'forest'},{t:'göl',e:'lake'},{t:'ada',e:'island'},{t:'çiftlik',e:'farm'},{t:'hayvan',e:'animal'},{t:'kuş',e:'bird'},{t:'balık',e:'fish'},{t:'at',e:'horse'},{t:'tavuk',e:'chicken'},{t:'inek',e:'cow'},{t:'koyun',e:'sheep'},{t:'domates',e:'tomato'},{t:'patates',e:'potato'},{t:'soğan',e:'onion'},{t:'biber',e:'pepper'},{t:'peynir',e:'cheese'},{t:'tereyağı',e:'butter'},{t:'yumurta',e:'egg'},{t:'pirinç',e:'rice'},{t:'makarna',e:'pasta'},{t:'çorba',e:'soup'},{t:'salata',e:'salad'},{t:'tatlı',e:'dessert'},{t:'dondurma',e:'ice cream'},{t:'sıcaklık',e:'temperature'},{t:'mevsim',e:'season'},{t:'ilkbahar',e:'spring'},{t:'yaz',e:'summer'},{t:'sonbahar',e:'autumn'},{t:'kış',e:'winter'},{t:'sis',e:'fog'},{t:'fırtına',e:'storm'},{t:'deprem',e:'earthquake'},{t:'sel',e:'flood'},{t:'yangın',e:'fire disaster'},{t:'kaza',e:'accident'},{t:'ambulans',e:'ambulance'},{t:'reçete',e:'prescription'},{t:'iğne',e:'needle'},{t:'ateş',e:'fever'},{t:'baş ağrısı',e:'headache'},{t:'grip',e:'flu'},{t:'öksürük',e:'cough'},{t:'alerji',e:'allergy'},{t:'diyet',e:'diet'},{t:'egzersiz',e:'exercise'},{t:'spor salonu',e:'gym'},{t:'stadyum',e:'stadium'},{t:'voleybol',e:'volleyball'},{t:'tenis',e:'tennis'},{t:'buz pateni',e:'ice skating'},{t:'kayak',e:'skiing'},{t:'kamp',e:'camping'},{t:'piknik',e:'picnic'},{t:'yürüyüş',e:'hiking'},{t:'fotoğraf',e:'photograph'},{t:'kamera',e:'camera'},{t:'video',e:'video'},{t:'şarkı',e:'song'},{t:'dans',e:'dance'},{t:'tiyatro',e:'theater'},{t:'konser',e:'concert'},{t:'sergi',e:'exhibition'},{t:'heykel',e:'sculpture'},{t:'roman',e:'novel'},{t:'şiir',e:'poem'},{t:'masal',e:'fairy tale'},{t:'çizgi film',e:'cartoon'},{t:'belgesel',e:'documentary'},{t:'dizi',e:'TV series'},{t:'reklam',e:'advertisement'},{t:'radyo',e:'radio'},{t:'mikrofon',e:'microphone'},{t:'hoparlör',e:'speaker'},{t:'kulaklık',e:'headphones'},{t:'ekran',e:'screen'},{t:'klavye',e:'keyboard'},{t:'yazıcı',e:'printer'},{t:'dosya',e:'file'},{t:'şifre',e:'password'},{t:'e-posta',e:'email'},{t:'web sitesi',e:'website'},{t:'uygulama',e:'app'},{t:'güncelleme',e:'update'},{t:'cüzdan',e:'wallet'},{t:'kredi kartı',e:'credit card'},{t:'banka',e:'bank'},{t:'hesap',e:'account'},{t:'borç',e:'debt'},{t:'kira',e:'rent'},{t:'fatura',e:'bill'},{t:'maaş',e:'salary'},{t:'garson',e:'waiter'},{t:'berber',e:'barber'},{t:'terzi',e:'tailor'},{t:'çilingir',e:'locksmith'},{t:'tesisatçı',e:'plumber'},{t:'elektrikçi',e:'electrician'},{t:'mimar',e:'architect'},{t:'pilot',e:'pilot'},{t:'kaptan',e:'captain'},{t:'asker',e:'soldier'},{t:'gazeteci',e:'journalist'},{t:'çevirmen',e:'translator'},{t:'otopark',e:'parking lot'},{t:'benzin',e:'gasoline'},{t:'lastik',e:'tire'},{t:'motor',e:'engine'},{t:'direksiyon',e:'steering wheel'},{t:'emniyet kemeri',e:'seat belt'},{t:'plaka',e:'license plate'},{t:'yön',e:'direction'},{t:'kuzey',e:'north'},{t:'güney',e:'south'},{t:'doğu',e:'east'},{t:'batı',e:'west'},{t:'hayal',e:'imagination'},{t:'şans',e:'luck'},{t:'hata',e:'mistake'},{t:'özür',e:'apology'},{t:'teşekkür',e:'thanks'},{t:'tebrikler',e:'congratulations'},{t:'hoşgeldiniz',e:'welcome'},{t:'görüşürüz',e:'see you'},{t:'lütfen',e:'please'},{t:'tabii',e:'of course'},{t:'belki',e:'maybe'},{t:'hemen',e:'immediately'},{t:'genellikle',e:'usually'},{t:'bazen',e:'sometimes'}],B1:[{t:'deneyim',e:'experience'},{t:'başarı',e:'success'},{t:'çevre',e:'environment'},{t:'toplum',e:'society'},{t:'eğitim',e:'education'},{t:'üniversite',e:'university'},{t:'mezuniyet',e:'graduation'},{t:'diploma',e:'diploma'},{t:'kariyer',e:'career'},{t:'maaş',e:'salary'},{t:'şirket',e:'company'},{t:'toplantı',e:'meeting'},{t:'proje',e:'project'},{t:'rapor',e:'report'},{t:'sunum',e:'presentation'},{t:'görüşme',e:'interview'},{t:'başvuru',e:'application'},{t:'özgeçmiş',e:'resume'},{t:'yetenek',e:'ability'},{t:'sorumluluk',e:'responsibility'},{t:'geliştirmek',e:'to develop'},{t:'araştırmak',e:'to research'},{t:'keşfetmek',e:'to discover'},{t:'iletişim',e:'communication'},{t:'tartışma',e:'discussion'},{t:'öneri',e:'suggestion'},{t:'şikayet',e:'complaint'},{t:'çözüm',e:'solution'},{t:'sorun',e:'problem'},{t:'fayda',e:'benefit'},{t:'avantaj',e:'advantage'},{t:'dezavantaj',e:'disadvantage'},{t:'karşılaştırma',e:'comparison'},{t:'fark',e:'difference'},{t:'benzerlik',e:'similarity'},{t:'örnek',e:'example'},{t:'sonuç',e:'result'},{t:'neden',e:'reason'},{t:'amaç',e:'purpose'},{t:'hedef',e:'goal'},{t:'plan',e:'plan'},{t:'strateji',e:'strategy'},{t:'yöntem',e:'method'},{t:'süreç',e:'process'},{t:'etki',e:'effect'},{t:'değişim',e:'change'},{t:'gelişim',e:'development'},{t:'ilerleme',e:'progress'},{t:'teknoloji',e:'technology'},{t:'bilim',e:'science'},{t:'matematik',e:'mathematics'},{t:'tarih',e:'history'},{t:'coğrafya',e:'geography'},{t:'edebiyat',e:'literature'},{t:'felsefe',e:'philosophy'},{t:'psikoloji',e:'psychology'},{t:'ekonomi',e:'economy'},{t:'politika',e:'politics'},{t:'hükümet',e:'government'},{t:'demokrasi',e:'democracy'},{t:'özgürlük',e:'freedom'},{t:'adalet',e:'justice'},{t:'eşitlik',e:'equality'},{t:'barış',e:'peace'},{t:'savaş',e:'war'},{t:'güvenlik',e:'security'},{t:'sağlık',e:'health'},{t:'hastalık',e:'disease'},{t:'tedavi',e:'treatment'},{t:'ilaç',e:'medicine'},{t:'ameliyat',e:'surgery'},{t:'bakım',e:'care'},{t:'kirlilik',e:'pollution'},{t:'geri dönüşüm',e:'recycling'},{t:'enerji',e:'energy'},{t:'doğal',e:'natural'},{t:'iklim',e:'climate'},{t:'kuraklık',e:'drought'},{t:'sel',e:'flood'},{t:'deprem',e:'earthquake'},{t:'kültür',e:'culture'},{t:'gelenek',e:'tradition'},{t:'festival',e:'festival'},{t:'tören',e:'ceremony'},{t:'inanç',e:'belief'},{t:'değer',e:'value'},{t:'saygı',e:'respect'},{t:'güven',e:'trust'},{t:'mutluluk',e:'happiness'},{t:'üzüntü',e:'sadness'},{t:'korku',e:'fear'},{t:'öfke',e:'anger'},{t:'heyecan',e:'excitement'},{t:'merak',e:'curiosity'},{t:'umut',e:'hope'},{t:'hayal',e:'dream'},{t:'anlık',e:'instant'},{t:'sürekli',e:'continuous'},{t:'geçici',e:'temporary'},{t:'kalıcı',e:'permanent'},{t:'karmaşık',e:'complex'},{t:'basit',e:'simple'},{t:'önemli',e:'important'},{t:'gerekli',e:'necessary'},{t:'zorunlu',e:'mandatory'},{t:'gönüllü',e:'voluntary'},{t:'resmi',e:'official'},{t:'özel',e:'private'},{t:'kamusal',e:'public'},{t:'yasal',e:'legal'},{t:'yasadışı',e:'illegal'},{t:'adil',e:'fair'},{t:'haksız',e:'unfair'},{t:'dürüst',e:'honest'},{t:'yalancı',e:'liar'},{t:'sadık',e:'loyal'},{t:'cesur',e:'brave'},{t:'korkak',e:'coward'},{t:'kibirli',e:'arrogant'},{t:'alçakgönüllü',e:'humble'},{t:'sabır',e:'patience'},{t:'hoşgörülü',e:'tolerant'},{t:'kindar',e:'resentful'},{t:'minnettar',e:'grateful'},{t:'şefkat',e:'compassion'},{t:'merhamet',e:'mercy'},{t:'vicdan',e:'conscience'},{t:'ahlak',e:'morality'},{t:'namus',e:'honor'},{t:'onur',e:'dignity'},{t:'utanç',e:'shame'},{t:'pişman',e:'regretful'},{t:'kıskançlık',e:'jealousy'},{t:'haset',e:'envy'},{t:'hırs',e:'ambition'},{t:'tutku',e:'passion'},{t:'özlem',e:'longing'},{t:'huzur',e:'serenity'},{t:'kaygı',e:'anxiety'},{t:'stres',e:'stress'},{t:'depresyon',e:'depression'},{t:'terapi',e:'therapy'},{t:'danışma',e:'counseling'},{t:'destek',e:'support'},{t:'bağımlılık',e:'addiction'},{t:'alışkanlık',e:'habit'},{t:'disiplin',e:'discipline'},{t:'motivasyon',e:'motivation'},{t:'özgüven',e:'self-confidence'},{t:'benlik',e:'self'},{t:'kimlik',e:'identity'},{t:'kişilik',e:'personality'},{t:'karakter',e:'character'},{t:'davranış',e:'behavior'},{t:'tutum',e:'attitude'},{t:'bakış açısı',e:'viewpoint'},{t:'görüş',e:'opinion'},{t:'yargı',e:'judgment'},{t:'önyargı',e:'bias'},{t:'eleştiri',e:'critique'},{t:'analiz',e:'analysis'},{t:'sentez',e:'synthesis'},{t:'özetlemek',e:'to summarize'},{t:'açıklamak',e:'to explain'},{t:'tanımlamak',e:'to define'},{t:'sınıflandırmak',e:'to classify'},{t:'kanıtlamak',e:'to prove'},{t:'varsaymak',e:'to assume'},{t:'sonuçlandırmak',e:'to conclude'},{t:'önermek',e:'to propose'},{t:'uygulamak',e:'to implement'},{t:'denetlemek',e:'to supervise'},{t:'yönetmek',e:'to manage'},{t:'koordine etmek',e:'to coordinate'},{t:'işbirliği',e:'cooperation'},{t:'rekabet',e:'competition'},{t:'çevirmek',e:'to translate'},{t:'uyarlamak',e:'to adapt'},{t:'değiştirmek',e:'to modify'},{t:'iyileştirmek',e:'to improve'},{t:'onarmak',e:'to repair'},{t:'yenilemek',e:'to renew'},{t:'tasarlamak',e:'to design'},{t:'üretmek',e:'to produce'},{t:'tüketmek',e:'to consume'},{t:'dağıtmak',e:'to distribute'},{t:'toplamak',e:'to collect'},{t:'depolamak',e:'to store'},{t:'ihracat',e:'export'},{t:'ithalat',e:'import'},{t:'ticaret',e:'trade'},{t:'sanayi',e:'industry'},{t:'tarım',e:'agriculture'},{t:'hasat',e:'harvest'},{t:'ekin',e:'crop'},{t:'gübre',e:'fertilizer'},{t:'sulama',e:'irrigation'},{t:'çiftçi',e:'farmer'},{t:'balıkçı',e:'fisherman'},{t:'madenci',e:'miner'},{t:'fabrika',e:'factory'},{t:'atık',e:'waste'},{t:'geri kazanım',e:'recovery'},{t:'sürdürülebilirlik',e:'sustainability'},{t:'yenilenebilir',e:'renewable'},{t:'fosil',e:'fossil'},{t:'karbon',e:'carbon'},{t:'sera etkisi',e:'greenhouse effect'},{t:'küresel ısınma',e:'global warming'},{t:'ozon',e:'ozone'},{t:'biyoçeşitlilik',e:'biodiversity'},{t:'habitat',e:'habitat'},{t:'ekoloji',e:'ecology'},{t:'tükenme',e:'depletion'},{t:'koruma',e:'protection'},{t:'yaşam alanı',e:'living space'},{t:'nesil',e:'generation'},{t:'miras',e:'heritage'},{t:'antik',e:'ancient'},{t:'çağ',e:'era'},{t:'dönem',e:'period'},{t:'yüzyıl',e:'century'},{t:'medeniyet',e:'civilization'},{t:'imparatorluk',e:'empire'},{t:'krallık',e:'kingdom'},{t:'cumhuriyet',e:'republic'},{t:'anayasa',e:'constitution'},{t:'parlamento',e:'parliament'},{t:'bakanlık',e:'ministry'},{t:'vali',e:'governor'},{t:'belediye',e:'municipality'},{t:'vatandaş',e:'citizen'},{t:'göçmen',e:'immigrant'},{t:'mülteci',e:'refugee'},{t:'sınır',e:'border'},{t:'vize',e:'visa'},{t:'gümrük',e:'customs'},{t:'elçilik',e:'embassy'},{t:'konsolosluk',e:'consulate'},{t:'birleşme',e:'merger'},{t:'satın alma',e:'acquisition'},{t:'ortaklık',e:'partnership'},{t:'hisse',e:'share'},{t:'borsa',e:'stock exchange'},{t:'piyasa',e:'market'},{t:'arz',e:'supply'},{t:'talep',e:'demand'},{t:'tedarik',e:'procurement'},{t:'lojistik',e:'logistics'},{t:'depo',e:'warehouse'},{t:'nakliye',e:'shipping'},{t:'sigorta',e:'insurance'},{t:'emeklilik',e:'retirement'},{t:'tasarruf',e:'savings'},{t:'harcama',e:'spending'},{t:'gelir',e:'income'},{t:'gider',e:'expense'},{t:'kâr',e:'profit'},{t:'zarar',e:'loss'},{t:'performans',e:'performance'},{t:'verimlilik',e:'productivity'},{t:'kalite',e:'quality'},{t:'standart',e:'standard'},{t:'sertifika',e:'certificate'},{t:'patent',e:'patent'},{t:'telif hakkı',e:'copyright'},{t:'marka',e:'brand'},{t:'reklam',e:'advertising'},{t:'pazarlama',e:'marketing'},{t:'müşteri',e:'customer'},{t:'tüketici',e:'consumer'},{t:'anket',e:'survey'},{t:'istatistik',e:'statistics'},{t:'grafik',e:'graph'},{t:'tablo',e:'chart'},{t:'veri',e:'data'},{t:'bilgi',e:'information'},{t:'belge',e:'document'},{t:'arsiv',e:'archive'},{t:'yazılım',e:'software'},{t:'donanım',e:'hardware'},{t:'ağ',e:'network'},{t:'sunucu',e:'server'},{t:'veritabanı',e:'database'},{t:'algoritma',e:'algorithm'},{t:'programlama',e:'programming'},{t:'kodlama',e:'coding'},{t:'robot',e:'robot'},{t:'yapay zeka',e:'artificial intelligence'},{t:'sanal gerçeklik',e:'virtual reality'},{t:'drone',e:'drone'},{t:'uydu',e:'satellite'},{t:'uzay',e:'space'},{t:'gezegen',e:'planet'},{t:'galaksi',e:'galaxy'},{t:'atmosfer',e:'atmosphere'},{t:'yerçekim',e:'gravity'},{t:'magnetics',e:'magnetism'}],B2:[{t:'varsayım',e:'assumption'},{t:'küresel',e:'global'},{t:'yerel',e:'local'},{t:'bölgesel',e:'regional'},{t:'uluslararası',e:'international'},{t:'diplomasi',e:'diplomacy'},{t:'antlaşma',e:'treaty'},{t:'yaptırım',e:'sanction'},{t:'muhalefet',e:'opposition'},{t:'koalisyon',e:'coalition'},{t:'reform',e:'reform'},{t:'devrim',e:'revolution'},{t:'ideoloji',e:'ideology'},{t:'propaganda',e:'propaganda'},{t:'bürokrasi',e:'bureaucracy'},{t:'yolsuzluk',e:'corruption'},{t:'hesap verebilirlik',e:'accountability'},{t:'şeffaflık',e:'transparency'},{t:'oy',e:'vote'},{t:'seçim',e:'election'},{t:'enflasyon',e:'inflation'},{t:'durgunluk',e:'recession'},{t:'büyüme',e:'growth'},{t:'yatırım',e:'investment'},{t:'girişimci',e:'entrepreneur'},{t:'rekabet',e:'competition'},{t:'tekel',e:'monopoly'},{t:'arz',e:'supply'},{t:'talep',e:'demand'},{t:'ihracat',e:'export'},{t:'ithalat',e:'import'},{t:'borç',e:'debt'},{t:'faiz',e:'interest'},{t:'vergi',e:'tax'},{t:'bütçe',e:'budget'},{t:'kaynak',e:'resource'},{t:'verimlilik',e:'efficiency'},{t:'sürdürülebilir',e:'sustainable'},{t:'yenilenebilir',e:'renewable'},{t:'emisyon',e:'emission'},{t:'ekosistem',e:'ecosystem'},{t:'biyolojik çeşitlilik',e:'biodiversity'},{t:'koruma',e:'conservation'},{t:'nesli tükenmiş',e:'extinct'},{t:'yapay zeka',e:'artificial intelligence'},{t:'algoritma',e:'algorithm'},{t:'veri tabani',e:'database'},{t:'siber güvenlik',e:'cybersecurity'},{t:'bulut bilişim',e:'cloud computing'},{t:'otomasyon',e:'automation'},{t:'robotik',e:'robotics'},{t:'biyoteknoloji',e:'biotechnology'},{t:'nanoteknoloji',e:'nanotechnology'},{t:'gen',e:'gene'},{t:'mutasyon',e:'mutation'},{t:'evrim',e:'evolution'},{t:'hipotez',e:'hypothesis'},{t:'deney',e:'experiment'},{t:'gozlem',e:'observation'},{t:'analiz',e:'analysis'},{t:'sentez',e:'synthesis'},{t:'değerlendirme',e:'evaluation'},{t:'eleştiri',e:'criticism'},{t:'yorum',e:'interpretation'},{t:'bakış açısı',e:'perspective'},{t:'önyargı',e:'prejudice'},{t:'ayrımcılık',e:'discrimination'},{t:'stereotip',e:'stereotype'},{t:'empati',e:'empathy'},{t:'farkındalık',e:'awareness'},{t:'ikilem',e:'dilemma'},{t:'paradoks',e:'paradox'},{t:'ironi',e:'irony'},{t:'metafor',e:'metaphor'},{t:'alegori',e:'allegory'},{t:'anlatım',e:'narrative'},{t:'retorik',e:'rhetoric'},{t:'arguman',e:'argument'},{t:'kanıt',e:'evidence'},{t:'çıkarım',e:'inference'},{t:'tümevarım',e:'induction'},{t:'tümdengelim',e:'deduction'},{t:'mantık',e:'logic'},{t:'özerklik',e:'autonomy'},{t:'hiyerarşi',e:'hierarchy'},{t:'dinamik',e:'dynamic'},{t:'etkileşim',e:'interaction'},{t:'entegrasyon',e:'integration'},{t:'uyum',e:'adaptation'},{t:'dönüşüm',e:'transformation'},{t:'yenilik',e:'innovation'},{t:'vizyon',e:'vision'},{t:'motivasyon',e:'motivation'},{t:'liderlik',e:'leadership'},{t:'işbirliği',e:'collaboration'},{t:'müdahale',e:'intervention'},{t:'önlem',e:'precaution'},{t:'risk',e:'risk'},{t:'belirsizlik',e:'uncertainty'},{t:'karar',e:'decision'},{t:'uzlaşma',e:'consensus'},{t:'olasılık',e:'probability'},{t:'istatistiksel',e:'statistical'},{t:'korelasyon',e:'correlation'},{t:'regresyon',e:'regression'},{t:'sapma',e:'deviation'},{t:'değişkenlik',e:'variability'},{t:'örneklem',e:'sampling'},{t:'gözlemsel',e:'observational'},{t:'deneysel',e:'experimental'},{t:'kontrol grubu',e:'control group'},{t:'plasebo',e:'placebo'},{t:'etik kurul',e:'ethics board'},{t:'gizlilik',e:'confidentiality'},{t:'onam',e:'consent'},{t:'katılımcı',e:'participant'},{t:'bulgular',e:'findings'},{t:'literatür',e:'literature'},{t:'atıf',e:'citation'},{t:'hakemli',e:'peer-reviewed'},{t:'yayınlamak',e:'to publish'},{t:'bildiri',e:'proceedings'},{t:'tez',e:'thesis'},{t:'disertasyon',e:'dissertation'},{t:'derleme',e:'review article'},{t:'metodoloji',e:'methodology'},{t:'kalitatif',e:'qualitative'},{t:'kantitatif',e:'quantitative'},{t:'sınırlılık',e:'limitation'},{t:'genellenebilirlik',e:'generalizability'},{t:'tekrarlanabilirlik',e:'replicability'},{t:'geçerlik',e:'validity'},{t:'güvenilirlik',e:'reliability'},{t:'ölçüt',e:'criterion'},{t:'gösterge',e:'indicator'},{t:'ölçek',e:'scale'},{t:'değerlendirici',e:'assessor'},{t:'kapsamlılık',e:'comprehensiveness'},{t:'tutarlılık',e:'consistency'},{t:'nesnellik',e:'objectivity'},{t:'öznellik',e:'subjectivity'},{t:'tarafsızlık',e:'impartiality'},{t:'çatışma',e:'conflict'},{t:'arabuluculuk',e:'mediation'},{t:'tahkim',e:'arbitration'},{t:'müzakere',e:'negotiation'},{t:'uzlaşı',e:'compromise'},{t:'ittifak',e:'alliance'},{t:'ambargo',e:'embargo'},{t:'saldırganlık',e:'aggression'},{t:'caydırıcılık',e:'deterrence'},{t:'savunma',e:'defense'},{t:'stratejik',e:'strategic'},{t:'taktik',e:'tactical'},{t:'operasyonel',e:'operational'},{t:'istihbarat',e:'intelligence'},{t:'gözetleme',e:'surveillance'},{t:'propaganda',e:'propaganda'},{t:'sansür',e:'censorship'},{t:'basın özgürlüğü',e:'press freedom'},{t:'ifade özgürlüğü',e:'freedom of speech'},{t:'sivil toplum',e:'civil society'},{t:'lobi',e:'lobby'},{t:'kamuoyu',e:'public opinion'},{t:'referandum',e:'referendum'},{t:'meşruiyet',e:'legitimacy'},{t:'egemenlik',e:'sovereignty'},{t:'ozerklik',e:'autonomy'},{t:'özyönetim',e:'self-governance'},{t:'ademimerkeziyet',e:'decentralization'},{t:'oligarşi',e:'oligarchy'},{t:'plutokrasi',e:'plutocracy'},{t:'meritokrasi',e:'meritocracy'},{t:'otokrasi',e:'autocracy'},{t:'teokrasi',e:'theocracy'},{t:'kleptokrasi',e:'kleptocracy'},{t:'popülizm',e:'populism'},{t:'milliyetçilik',e:'nationalism'},{t:'kozmopolitanizm',e:'cosmopolitanism'},{t:'çok kültürlülük',e:'multiculturalism'},{t:'asimilasyon',e:'assimilation'},{t:'entegrasyon',e:'integration'},{t:'diaspora',e:'diaspora'},{t:'soykırım',e:'genocide'},{t:'etnik temizlik',e:'ethnic cleansing'},{t:'insan hakları',e:'human rights'},{t:'sözleşme',e:'convention'},{t:'protokol',e:'protocol'},{t:'deflasyon',e:'deflation'},{t:'hiperenflasyon',e:'hyperinflation'},{t:'devalüasyon',e:'devaluation'},{t:'kur',e:'exchange rate'},{t:'döviz',e:'foreign currency'},{t:'likidite',e:'liquidity'},{t:'teminat',e:'collateral'},{t:'iflas',e:'bankruptcy'},{t:'konkordato',e:'concordat'},{t:'özelleştirme',e:'privatization'},{t:'devletleştirme',e:'nationalization'},{t:'subvansiyon',e:'subsidy'},{t:'korumacı',e:'protectionist'},{t:'serbest ticaret',e:'free trade'},{t:'gümrük tarifeleri',e:'tariffs'},{t:'kota',e:'quota'},{t:'damping',e:'dumping'},{t:'kartel',e:'cartel'},{t:'holding',e:'holding'},{t:'konsorsiyum',e:'consortium'},{t:'franchisor',e:'franchise'},{t:'fikri mülkiyet',e:'intellectual property'},{t:'lisans',e:'license'},{t:'royalti',e:'royalty'},{t:'risk yönetimi',e:'risk management'},{t:'fizibilite',e:'feasibility'},{t:'maliyet',e:'cost'},{t:'amortisman',e:'depreciation'},{t:'envanter',e:'inventory'},{t:'audit',e:'audit'},{t:'muhasebecilik',e:'accounting'},{t:'aktuarya',e:'actuarial'},{t:'portföy',e:'portfolio'},{t:'diversifikasyon',e:'diversification'},{t:'hedge',e:'hedge'},{t:'türev',e:'derivative'},{t:'opsiyon',e:'option'},{t:'vadeli işlem',e:'futures'},{t:'spekülasyon',e:'speculation'},{t:'balon',e:'bubble'},{t:'çöküş',e:'crash'},{t:'toparlanma',e:'recovery'},{t:'döngüsel',e:'cyclical'},{t:'yapısal',e:'structural'},{t:'konjonktürel',e:'conjunctural'},{t:'makro',e:'macro'},{t:'mikro',e:'micro'},{t:'mezo',e:'meso'},{t:'epidemi',e:'epidemic'},{t:'pandemi',e:'pandemic'},{t:'karantina',e:'quarantine'},{t:'aşı',e:'vaccine'},{t:'antikor',e:'antibody'},{t:'bağışıklık',e:'immunity'},{t:'genom',e:'genome'},{t:'biyometri',e:'biometrics'},{t:'teletibb',e:'telemedicine'},{t:'nanopartikul',e:'nanoparticle'},{t:'protez',e:'prosthesis'},{t:'implant',e:'implant'},{t:'rehabilitasyon',e:'rehabilitation'},{t:'ergonomi',e:'ergonomics'},{t:'fizyoterapi',e:'physiotherapy'},{t:'nöroloji',e:'neurology'},{t:'onkoloji',e:'oncology'},{t:'kardiyoloji',e:'cardiology'},{t:'ortopedi',e:'orthopedics'},{t:'dermatoloji',e:'dermatology'},{t:'psikiyatri',e:'psychiatry'},{t:'radyoloji',e:'radiology'},{t:'anestezi',e:'anesthesia'},{t:'genetik',e:'genetics'},{t:'biyo etik',e:'bioethics'},{t:'klinik deney',e:'clinical trial'},{t:'farmasi',e:'pharmacy'},{t:'toksin',e:'toxin'},{t:'antioksidan',e:'antioxidant'},{t:'metabolizma',e:'metabolism'},{t:'enzim',e:'enzyme'},{t:'hormon',e:'hormone'},{t:'sinaps',e:'synapse'},{t:'nöron',e:'neuron'},{t:'dopamin',e:'dopamine'},{t:'serotonin',e:'serotonin'},{t:'bilişim',e:'informatics'},{t:'blokzincir',e:'blockchain'},{t:'kuantum bilgisayar',e:'quantum computer'},{t:'makine öğrenimi',e:'machine learning'},{t:'derin öğrenme',e:'deep learning'},{t:'sinir ağı',e:'neural network'},{t:'doğal dil işleme',e:'natural language processing'},{t:'bilgisayarlı görü',e:'computer vision'},{t:'otonom',e:'autonomous'},{t:'robot etiği',e:'robot ethics'},{t:'siber fiziksel',e:'cyber-physical'},{t:'nesnelerin interneti',e:'internet of things'},{t:'büyük veri',e:'big data'},{t:'veri madenciliği',e:'data mining'}],C1:[{t:'epistemoloji',e:'epistemology'},{t:'ontoloji',e:'ontology'},{t:'metafizik',e:'metaphysics'},{t:'determinizm',e:'determinism'},{t:'ampirizm',e:'empiricism'},{t:'rasyonalizm',e:'rationalism'},{t:'pragmatizm',e:'pragmatism'},{t:'nihilizm',e:'nihilism'},{t:'varoluşçuluk',e:'existentialism'},{t:'fenomenoloji',e:'phenomenology'},{t:'hermeneutik',e:'hermeneutics'},{t:'semiyotik',e:'semiotics'},{t:'söylev',e:'discourse'},{t:'paradigma',e:'paradigm'},{t:'bağlamsal',e:'contextual'},{t:'ölçeklendirmek',e:'to scale'},{t:'kavramsallaştırma',e:'conceptualization'},{t:'somutlaştırmak',e:'to concretize'},{t:'soyutlama',e:'abstraction'},{t:'genelleme',e:'generalization'},{t:'ayrıntılı',e:'elaborate'},{t:'kapsamlı',e:'comprehensive'},{t:'sistematik',e:'systematic'},{t:'ampirik',e:'empirical'},{t:'nitel',e:'qualitative'},{t:'nicel',e:'quantitative'},{t:'korelasyon',e:'correlation'},{t:'nedensellik',e:'causality'},{t:'değişken',e:'variable'},{t:'örneklem',e:'sample'},{t:'populasyon',e:'population'},{t:'istatistik',e:'statistics'},{t:'standart sapma',e:'standard deviation'},{t:'ortalama',e:'mean'},{t:'medyan',e:'median'},{t:'regresyon',e:'regression'},{t:'olasılık',e:'probability'},{t:'dağılım',e:'distribution'},{t:'güvenilirlik',e:'reliability'},{t:'geçerlilik',e:'validity'},{t:'olgubilim',e:'phenomenography'},{t:'sosyoloji',e:'sociology'},{t:'antropoloji',e:'anthropology'},{t:'arkeoloji',e:'archaeology'},{t:'dilbilim',e:'linguistics'},{t:'morfoloji',e:'morphology'},{t:'sentaks',e:'syntax'},{t:'semantik',e:'semantics'},{t:'pragmatik',e:'pragmatics'},{t:'fonoloji',e:'phonology'},{t:'etnografya',e:'ethnography'},{t:'demografi',e:'demography'},{t:'jeopolitik',e:'geopolitics'},{t:'hegemonya',e:'hegemony'},{t:'emperyalizm',e:'imperialism'},{t:'kolonyalizm',e:'colonialism'},{t:'milliyetçilik',e:'nationalism'},{t:'federalizm',e:'federalism'},{t:'totalitarizm',e:'totalitarianism'},{t:'otoritarizm',e:'authoritarianism'},{t:'liberalizm',e:'liberalism'},{t:'sosyalizm',e:'socialism'},{t:'kapitalizm',e:'capitalism'},{t:'merkantilizm',e:'mercantilism'},{t:'fizyokrasi',e:'physiocracy'},{t:'makroekonomi',e:'macroeconomics'},{t:'mikroekonomi',e:'microeconomics'},{t:'maliye',e:'public finance'},{t:'likidite',e:'liquidity'},{t:'devalüasyon',e:'devaluation'},{t:'stagflasyon',e:'stagflation'},{t:'oligopol',e:'oligopoly'},{t:'dışsallık',e:'externality'},{t:'marjinal',e:'marginal'},{t:'elastikiyet',e:'elasticity'},{t:'fayda',e:'utility'},{t:'optimizasyon',e:'optimization'},{t:'stokastik',e:'stochastic'},{t:'asimptotik',e:'asymptotic'},{t:'homojen',e:'homogeneous'},{t:'heterojen',e:'heterogeneous'},{t:'izomorfizm',e:'isomorphism'},{t:'topoloji',e:'topology'},{t:'diferansiyel',e:'differential'},{t:'integral',e:'integral'},{t:'matris',e:'matrix'},{t:'vektor',e:'vector'},{t:'skaler',e:'scalar'},{t:'tensor',e:'tensor'},{t:'kuantum',e:'quantum'},{t:'relativite',e:'relativity'},{t:'termodinamik',e:'thermodynamics'},{t:'entropi',e:'entropy'},{t:'katalizor',e:'catalyst'},{t:'polimer',e:'polymer'},{t:'sentez',e:'synthesis'},{t:'hidroliz',e:'hydrolysis'},{t:'oksidasyon',e:'oxidation'},{t:'indirgenme',e:'reduction'},{t:'elektroliz',e:'electrolysis'},{t:'izotop',e:'isotope'},{t:'toplumsal cinsiyet',e:'gender'},{t:'soybilim',e:'genealogy'},{t:'etimoloji',e:'etymology'},{t:'mitoloji',e:'mythology'},{t:'kozmogoni',e:'cosmogony'},{t:'eskatoloji',e:'eschatology'},{t:'teogoni',e:'theogony'},{t:'ikonografi',e:'iconography'},{t:'paleografi',e:'paleography'},{t:'epigrafi',e:'epigraphy'},{t:'filoloji',e:'philology'},{t:'leksikografi',e:'lexicography'},{t:'terminoloji',e:'terminology'},{t:'neolojizm',e:'neologism'},{t:'arkaizm',e:'archaism'},{t:'diyakronik',e:'diachronic'},{t:'senkronik',e:'synchronic'},{t:'tipoloji',e:'typology'},{t:'sınıflandırma',e:'taxonomy'},{t:'sistematik',e:'systematics'},{t:'nomenklatur',e:'nomenclature'},{t:'filogenetik',e:'phylogenetics'},{t:'filogeni',e:'phylogeny'},{t:'ontogeni',e:'ontogeny'},{t:'homoloji',e:'homology'},{t:'analoji',e:'analogy'},{t:'konverjans',e:'convergence'},{t:'diverjans',e:'divergence'},{t:'adaptasyon',e:'adaptation'},{t:'seleksiyon',e:'selection'},{t:'mutasyon oranı',e:'mutation rate'},{t:'genetik sürüklenme',e:'genetic drift'},{t:'gen akışı',e:'gene flow'},{t:'ekolojik niş',e:'ecological niche'},{t:'biyom',e:'biome'},{t:'sukcesyon',e:'succession'},{t:'simbiyoz',e:'symbiosis'},{t:'parazitizm',e:'parasitism'},{t:'mutualizm',e:'mutualism'},{t:'kommensalizm',e:'commensalism'},{t:'avcılık',e:'predation'},{t:'rekabet dışlaması',e:'competitive exclusion'},{t:'biyojeokimya',e:'biogeochemistry'},{t:'azot döngüsü',e:'nitrogen cycle'},{t:'karbon döngüsü',e:'carbon cycle'},{t:'fotosentez',e:'photosynthesis'},{t:'kemosentez',e:'chemosynthesis'},{t:'anabolizma',e:'anabolism'},{t:'katabolizma',e:'catabolism'},{t:'glikoliz',e:'glycolysis'},{t:'mitokondri',e:'mitochondria'},{t:'kloroplast',e:'chloroplast'},{t:'ribozom',e:'ribosome'},{t:'endoplazmik retikulum',e:'endoplasmic reticulum'},{t:'golgi aygıtı',e:'golgi apparatus'},{t:'lizozom',e:'lysosome'},{t:'vakuol',e:'vacuole'},{t:'sitoplazma',e:'cytoplasm'},{t:'hücre zarı',e:'cell membrane'},{t:'çekirdek',e:'nucleus'},{t:'kromozom',e:'chromosome'},{t:'DNA',e:'DNA'},{t:'RNA',e:'RNA'},{t:'transkripsiyon',e:'transcription'},{t:'translasyon',e:'translation'},{t:'replikasyon',e:'replication'},{t:'rekombinasyon',e:'recombination'},{t:'klonlama',e:'cloning'},{t:'transgenics',e:'transgenics'},{t:'proteomiks',e:'proteomics'},{t:'metabolomiks',e:'metabolomics'},{t:'genomiks',e:'genomics'},{t:'biyoinformatik',e:'bioinformatics'},{t:'sistem biyolojisi',e:'systems biology'},{t:'sentetik biyoloji',e:'synthetic biology'},{t:'CRISPR',e:'CRISPR'},{t:'fermentasyon',e:'fermentation'},{t:'distilasyon',e:'distillation'},{t:'kristalizasyon',e:'crystallization'},{t:'kromatografi',e:'chromatography'},{t:'spektroskopi',e:'spectroscopy'},{t:'titrasyon',e:'titration'},{t:'molarite',e:'molarity'},{t:'molar kütle',e:'molar mass'},{t:'avogadro sayısı',e:'Avogadro number'},{t:'periyodik tablo',e:'periodic table'},{t:'elektron',e:'electron'},{t:'proton',e:'proton'},{t:'notron',e:'neutron'},{t:'atom numarası',e:'atomic number'},{t:'kütle numarası',e:'mass number'},{t:'iyonizasyon',e:'ionization'},{t:'elektronegatiflik',e:'electronegativity'},{t:'kovalent bağ',e:'covalent bond'},{t:'iyonik bağ',e:'ionic bond'},{t:'metalik bağ',e:'metallic bond'},{t:'van der Waals',e:'van der Waals'},{t:'hidrojen bağı',e:'hydrogen bond'},{t:'kristal kafes',e:'crystal lattice'},{t:'amorf',e:'amorphous'},{t:'alaşım',e:'alloy'},{t:'korozyon',e:'corrosion'},{t:'galvanizleme',e:'galvanizing'},{t:'elektrokaplama',e:'electroplating'},{t:'süperiletkenlik',e:'superconductivity'},{t:'yarıiletken',e:'semiconductor'},{t:'diyot',e:'diode'},{t:'transistör',e:'transistor'},{t:'entegre devre',e:'integrated circuit'},{t:'kuantum tünelleme',e:'quantum tunneling'},{t:'dalga fonksiyonu',e:'wave function'},{t:'belirsizlik ilkesi',e:'uncertainty principle'},{t:'Schrödinger denklemi',e:'Schrodinger equation'},{t:'ozel relativite',e:'special relativity'},{t:'genel relativite',e:'general relativity'},{t:'uzay-zaman',e:'spacetime'},{t:'kara delik',e:'black hole'},{t:'nötrino',e:'neutrino'},{t:'bozon',e:'boson'},{t:'fermiyon',e:'fermion'},{t:'kuark',e:'quark'},{t:'lepton',e:'lepton'},{t:'hadron',e:'hadron'},{t:'antimadde',e:'antimatter'},{t:'karanlık madde',e:'dark matter'},{t:'karanlık enerji',e:'dark energy'},{t:'kozmik mikrodalga',e:'cosmic microwave'},{t:'büyük patlama',e:'big bang'},{t:'kozmik enflasyon',e:'cosmic inflation'},{t:'sicim teorisi',e:'string theory'},{t:'çoklu evren',e:'multiverse'},{t:'paralel evren',e:'parallel universe'},{t:'boyut',e:'dimension'},{t:'tekilleştirme',e:'unification'},{t:'birleşik alan teorisi',e:'unified field theory'},{t:'standart model',e:'standard model'},{t:'süpersimetri',e:'supersymmetry'},{t:'Higgs bozonu',e:'Higgs boson'},{t:'kuvvetli kuvvet',e:'strong force'},{t:'zayif kuvvet',e:'weak force'},{t:'elektromanyetik',e:'electromagnetic'},{t:'graviton',e:'graviton'},{t:'gravitasyonel dalga',e:'gravitational wave'},{t:'pulsar',e:'pulsar'},{t:'kuazar',e:'quasar'},{t:'süpernova',e:'supernova'},{t:'beyaz cüce',e:'white dwarf'},{t:'nötron yıldızı',e:'neutron star'},{t:'protoyıldız',e:'protostar'},{t:'yıldızlararası',e:'interstellar'},{t:'galaksilerarası',e:'intergalactic'},{t:'ekzogezegen',e:'exoplanet'},{t:'astrobiyoloji',e:'astrobiology'},{t:'termodinamik yasalari',e:'laws of thermodynamics'},{t:'entalpi',e:'enthalpy'},{t:'serbest enerji',e:'free energy'},{t:'ısı kapasitesi',e:'heat capacity'},{t:'adyabatik',e:'adiabatic'},{t:'izotermik',e:'isothermal'},{t:'izobarik',e:'isobaric'},{t:'izokhorik',e:'isochoric'},{t:'karnot döngüsü',e:'Carnot cycle'}],C2:[{t:'aporetik',e:'aporetic'},{t:'diyalektik',e:'dialectic'},{t:'teleoloji',e:'teleology'},{t:'deontoloji',e:'deontology'},{t:'faydacılık',e:'utilitarianism'},{t:'erdem etiği',e:'virtue ethics'},{t:'solipsizm',e:'solipsism'},{t:'dualizm',e:'dualism'},{t:'monizm',e:'monism'},{t:'panteizm',e:'pantheism'},{t:'agnostisizm',e:'agnosticism'},{t:'skeptisizm',e:'skepticism'},{t:'pozitivizm',e:'positivism'},{t:'yapısalcılık',e:'structuralism'},{t:'postyapısalcılık',e:'post-structuralism'},{t:'yapısöküm',e:'deconstruction'},{t:'postmodernizm',e:'postmodernism'},{t:'modernizm',e:'modernism'},{t:'avangard',e:'avant-garde'},{t:'eklektisizm',e:'eclecticism'},{t:'senkretizm',e:'syncretism'},{t:'reduksiyonizm',e:'reductionism'},{t:'holizm',e:'holism'},{t:'emergentizm',e:'emergentism'},{t:'epifenomenalizm',e:'epiphenomenalism'},{t:'işlevselcilik',e:'functionalism'},{t:'davranışçılık',e:'behaviorism'},{t:'bilişsel',e:'cognitive'},{t:'nostalji',e:'nostalgia'},{t:'melankoli',e:'melancholy'},{t:'eufori',e:'euphoria'},{t:'katarsis',e:'catharsis'},{t:'subliminal',e:'subliminal'},{t:'arketip',e:'archetype'},{t:'alegori',e:'allegory'},{t:'aforizma',e:'aphorism'},{t:'oksimoron',e:'oxymoron'},{t:'pleonazm',e:'pleonasm'},{t:'anakronizm',e:'anachronism'},{t:'dogmatizm',e:'dogmatism'},{t:'relativizm',e:'relativism'},{t:'subjektivizm',e:'subjectivism'},{t:'objektivizm',e:'objectivism'},{t:'materyalizm',e:'materialism'},{t:'idealizm',e:'idealism'},{t:'transsendentalizm',e:'transcendentalism'},{t:'immanentizm',e:'immanentism'},{t:'animizm',e:'animism'},{t:'totemizm',e:'totemism'},{t:'fetişizm',e:'fetishism'},{t:'ikonoklazm',e:'iconoclasm'},{t:'hedonizm',e:'hedonism'},{t:'asketizm',e:'asceticism'},{t:'stoacılık',e:'stoicism'},{t:'epikürcülük',e:'epicureanism'},{t:'sinizm',e:'cynicism'},{t:'sofistlik',e:'sophistry'},{t:'pedagoji',e:'pedagogy'},{t:'andragoji',e:'andragogy'},{t:'heuristik',e:'heuristic'},{t:'didaktik',e:'didactic'},{t:'polemik',e:'polemic'},{t:'retorik',e:'rhetoric'},{t:'filoloji',e:'philology'},{t:'leksikografi',e:'lexicography'},{t:'etimoloji',e:'etymology'},{t:'paleografi',e:'paleography'},{t:'epigrafi',e:'epigraphy'},{t:'nümismatik',e:'numismatics'},{t:'filateli',e:'philately'},{t:'heraldik',e:'heraldry'},{t:'genealoji',e:'genealogy'},{t:'kozmoloji',e:'cosmology'},{t:'astrofizik',e:'astrophysics'},{t:'jeomorfoloji',e:'geomorphology'},{t:'okyanusbilim',e:'oceanography'},{t:'meteoroloji',e:'meteorology'},{t:'sismoloji',e:'seismology'},{t:'vulkanoloji',e:'volcanology'},{t:'paleontoloji',e:'paleontology'},{t:'taksonomi',e:'taxonomy'},{t:'sitoloji',e:'cytology'},{t:'histoloji',e:'histology'},{t:'patoloji',e:'pathology'},{t:'farmakoloji',e:'pharmacology'},{t:'toksikoloji',e:'toxicology'},{t:'epidemiyoloji',e:'epidemiology'},{t:'immunoloji',e:'immunology'},{t:'viroloji',e:'virology'},{t:'mikrobiyoloji',e:'microbiology'},{t:'biyoinformatik',e:'bioinformatics'},{t:'proteomik',e:'proteomics'},{t:'genomik',e:'genomics'},{t:'epigenetik',e:'epigenetics'},{t:'norobilim',e:'neuroscience'},{t:'psikofizik',e:'psychophysics'},{t:'psikolinguistik',e:'psycholinguistics'},{t:'sosyolinguistik',e:'sociolinguistics'},{t:'kriptografi',e:'cryptography'},{t:'steganografi',e:'steganography'},{t:'logosantrizm',e:'logocentrism'},{t:'fonosantrizm',e:'phonocentrism'},{t:'fallosantrizm',e:'phallocentrism'},{t:'etnosantrizm',e:'ethnocentrism'},{t:'antroposantrizm',e:'anthropocentrism'},{t:'biyosantrizm',e:'biocentrism'},{t:'ekosantrizm',e:'ecocentrism'},{t:'teknosantrizm',e:'technocentrism'},{t:'heliyosantrizm',e:'heliocentrism'},{t:'jeosantrizm',e:'geocentrism'},{t:'fenomenalizm',e:'phenomenalism'},{t:'enstrumentalizm',e:'instrumentalism'},{t:'konvansiyonalizm',e:'conventionalism'},{t:'fideizm',e:'fideism'},{t:'voluntarizm',e:'voluntarism'},{t:'fatalizm',e:'fatalism'},{t:'indeterminizm',e:'indeterminism'},{t:'kompatibilizm',e:'compatibilism'},{t:'inkompatibilizm',e:'incompatibilism'},{t:'libertaryenizm',e:'libertarianism'},{t:'kommunitarizm',e:'communitarianism'},{t:'kozmopolitizm',e:'cosmopolitanism'},{t:'anarsizm',e:'anarchism'},{t:'sendikalizm',e:'syndicalism'},{t:'mutualzim',e:'mutualism'},{t:'korporatizm',e:'corporatism'},{t:'teknokrasi',e:'technocracy'},{t:'epistokrasi',e:'epistocracy'},{t:'postkolonyalizm',e:'postcolonialism'},{t:'oryantalizm',e:'orientalism'},{t:'oksidentalizm',e:'occidentalism'},{t:'neoklasizm',e:'neoclassicism'},{t:'romantizm',e:'romanticism'},{t:'natüralizm',e:'naturalism'},{t:'realizm',e:'realism'},{t:'sembolizm',e:'symbolism'},{t:'ekspresyonizm',e:'expressionism'},{t:'empresyonizm',e:'impressionism'},{t:'fovizm',e:'fauvism'},{t:'kübizm',e:'cubism'},{t:'futurizm',e:'futurism'},{t:'dadaizm',e:'dadaism'},{t:'sürrealizm',e:'surrealism'},{t:'minimalizm',e:'minimalism'},{t:'konceptualizm',e:'conceptualism'},{t:'performativite',e:'performativity'},{t:'intertekstüellik',e:'intertextuality'},{t:'metatekstüellik',e:'metatextuality'},{t:'palimpsest',e:'palimpsest'},{t:'pastis',e:'pastiche'},{t:'parodi',e:'parody'},{t:'grotesk',e:'grotesque'},{t:'absurt',e:'absurd'},{t:'tragikomik',e:'tragicomic'},{t:'pikareski',e:'picaresque'},{t:'bildungsroman',e:'bildungsroman'},{t:'epistolar',e:'epistolary'},{t:'hagiografi',e:'hagiography'},{t:'prosopografi',e:'prosopography'},{t:'historiografi',e:'historiography'},{t:'fenomenografi',e:'phenomenography'},{t:'etnometodoloji',e:'ethnomethodology'},{t:'sembolik etkileşimcilik',e:'symbolic interactionism'},{t:'rasyonel seçim',e:'rational choice'},{t:'oyun teorisi',e:'game theory'},{t:'kaos teorisi',e:'chaos theory'},{t:'karmaşıklık teorisi',e:'complexity theory'},{t:'sistem teorisi',e:'systems theory'},{t:'bilgi teorisi',e:'information theory'},{t:'iletişim teorisi',e:'communication theory'},{t:'çiftbeslemeli',e:'double hermeneutic'},{t:'düşünümsellik',e:'reflexivity'},{t:'özyinesellik',e:'recursivity'},{t:'otoreferansiyellik',e:'self-referentiality'},{t:'metabilişsellik',e:'metacognition'},{t:'fenomenolojik',e:'phenomenological'},{t:'transandantal',e:'transcendental'},{t:'immanent',e:'immanent'},{t:'apriori',e:'a priori'},{t:'aposteriori',e:'a posteriori'},{t:'analitik',e:'analytic'},{t:'sentetik',e:'synthetic'},{t:'tautoloji',e:'tautology'},{t:'antinomi',e:'antinomy'},{t:'apori',e:'aporia'},{t:'paradoks',e:'paradox'},{t:'sillogizm',e:'syllogism'},{t:'entimem',e:'enthymeme'},{t:'sofizm',e:'sophism'},{t:'eristic',e:'eristic'},{t:'diyalektik',e:'dialectics'},{t:'maieutik',e:'maieutic'},{t:'sokratik yöntem',e:'Socratic method'},{t:'elenktik',e:'elenctic'},{t:'aporetik',e:'aporetic'},{t:'prolegomena',e:'prolegomena'},{t:'propedeutik',e:'propaedeutic'},{t:'prolegomenon',e:'prolegomenon'},{t:'aksiomatik',e:'axiomatic'},{t:'aksiyoloji',e:'axiology'},{t:'deontik',e:'deontic'},{t:'normatif',e:'normative'},{t:'deskriptif',e:'descriptive'},{t:'preskriptif',e:'prescriptive'},{t:'süpererogasyon',e:'supererogation'},{t:'akresia',e:'akrasia'},{t:'eudaimonia',e:'eudaimonia'},{t:'ataraxia',e:'ataraxia'},{t:'apatheia',e:'apatheia'},{t:'phronesis',e:'phronesis'},{t:'praxis',e:'praxis'},{t:'poiesis',e:'poiesis'},{t:'tekne',e:'techne'},{t:'episteme',e:'episteme'},{t:'doxa',e:'doxa'},{t:'aletheia',e:'aletheia'},{t:'hermeneutik cember',e:'hermeneutic circle'},{t:'anlam ufku',e:'horizon of meaning'},{t:'onanlam',e:'pre-understanding'},{t:'yaşam dünyası',e:'lifeworld'},{t:'dasein',e:'dasein'},{t:'varoluşsal',e:'existential'},{t:'olgusallık',e:'facticity'},{t:'fırlatılmışlık',e:'thrownness'},{t:'özantılık',e:'authenticity'},{t:'kötü niyet',e:'bad faith'},{t:'bulanti',e:'nausea'},{t:'absürtlük',e:'absurdity'},{t:'sisifüsçü',e:'Sisyphean'},{t:'Prometeuscu',e:'Promethean'},{t:'Dionysoscu',e:'Dionysian'},{t:'Apolloncu',e:'Apollonian'},{t:'Faustcu',e:'Faustian'},{t:'Makyavelist',e:'Machiavellian'},{t:'Kafkaesk',e:'Kafkaesque'},{t:'Orwellci',e:'Orwellian'},{t:'Nietzscheci',e:'Nietzschean'},{t:'Kartezyen',e:'Cartesian'},{t:'Kantci',e:'Kantian'},{t:'Hegelci',e:'Hegelian'},{t:'Marksist',e:'Marxist'},{t:'Freudyen',e:'Freudian'},{t:'Jungci',e:'Jungian'},{t:'Lacanci',e:'Lacanian'},{t:'Foucaultcu',e:'Foucauldian'},{t:'Derridacı',e:'Derridean'},{t:'Deleuzecu',e:'Deleuzian'},{t:'Habermasci',e:'Habermasian'},{t:'Wittgensteinci',e:'Wittgensteinian'},{t:'Heideggerci',e:'Heideggerian'},{t:'Husserlci',e:'Husserlian'},{t:'Gadamerci',e:'Gadamerian'},{t:'biyosemiyotik',e:'biosemiotics'},{t:'zoosemiyotik',e:'zoosemiotics'},{t:'endosemiyotik',e:'endosemiotics'},{t:'fitosemiyotik',e:'phytosemiotics'},{t:'semiyosfer',e:'semiosphere'},{t:'logoosfer',e:'logosphere'},{t:'noofer',e:'noosphere'},{t:'biyosfer',e:'biosphere'},{t:'teknosfer',e:'technosphere'},{t:'antroposen',e:'Anthropocene'},{t:'holoseen',e:'Holocene'},{t:'pleistosen',e:'Pleistocene'},{t:'miosen',e:'Miocene'},{t:'paleozoik',e:'Paleozoic'},{t:'mezozoik',e:'Mesozoic'},{t:'senozoik',e:'Cenozoic'},{t:'prekambriyen',e:'Precambrian'},{t:'kambriyen patlaması',e:'Cambrian explosion'},{t:'buzul çağı',e:'ice age'},{t:'pangea',e:'Pangaea'}]};"
        "var FINAL_TEST_COUNT=50;"
        "var FINAL_TEST_PASS=35;"
        "/* === PARTICLE SYSTEM === */"
        "var stars=[];var shootingStars=[];var particles=[];var orbs=[];"
        "for(var i=0;i<70;i++){stars.push({x:Math.random()*W,y:Math.random()*H,"
        "r:Math.random()*1.8+0.3,sp:Math.random()*0.4+0.08,ph:Math.random()*Math.PI*2,"
        "twinkle:Math.random()*0.5+0.5,"
        "col:['#ffffff','#c8e6ff','#ffe4b5','#e0c0ff','#a0ffff'][Math.floor(Math.random()*5)]});}"
        "var nebulas=[];"
        "for(var i=0;i<6;i++){nebulas.push({x:Math.random()*W,y:Math.random()*H,"
        "r:Math.random()*160+100,phase:Math.random()*Math.PI*2,drift:Math.random()*0.2+0.05,"
        "col:['rgba(120,60,220,0.045)','rgba(30,100,220,0.035)','rgba(220,50,120,0.03)',"
        "'rgba(50,180,220,0.035)','rgba(255,150,50,0.02)','rgba(100,255,150,0.025)'][i]});}"
        "for(var i=0;i<4;i++){orbs.push({x:Math.random()*W,y:Math.random()*H,"
        "r:Math.random()*3+2,vx:Math.random()*0.3-0.15,vy:Math.random()*0.3-0.15,"
        "col:['rgba(120,80,255,0.6)','rgba(0,229,255,0.5)','rgba(255,170,50,0.4)','rgba(255,80,180,0.5)'][i],trail:[]});}"
        "/* === GAME STATE === */"
        "var state='menu';var currentLevel=0;var words=[];var wordIdx=0;var options=[];"
        "var score=0;var streak=0;var bestStreak=0;var correct=0;var wrong=0;"
        "var timer=0;var maxTime=10;var selectedOpt=-1;var showResult=0;"
        "var resultCorrect=false;var correctOptIdx=-1;var confetti=[];var hoverOpt=-1;"
        "var animT=0;var scorePopups=[];var shakeTimer=0;var pulseTimer=0;"
        "var cardFloat=0;var menuFloat=0;"
        "/* final test vars */"
        "var ftWords=[];var ftIdx=0;var ftCorrect=0;var ftWrong=0;var ftScore=0;"
        "var ftOptions=[];var ftSelected=-1;var ftShowResult=0;var ftResultCorrect=false;"
        "var ftCorrectOptIdx=-1;var ftTimer=0;var ftStreak=0;"
        "/* === PROGRESS SYSTEM === */"
        "var progress={levels:{}};"
        "function initProgress(){LEVELS.forEach(function(ln){"
        "if(!progress.levels[ln])progress.levels[ln]={answered:[],score:0,testPassed:false};});}"
        "function migrateProgress(raw){"
        "if(!raw)return{levels:{}};"
        "if(raw.levels)return raw;"
        "var np={levels:{}};LEVELS.forEach(function(ln){"
        "var c=(raw[ln])||0;var ans=[];"
        "for(var i=0;i<Math.min(c,LEVEL_SIZE[ln]);i++)ans.push(i);"
        "np.levels[ln]={answered:ans,score:0,testPassed:false};});"
        "return np;}"
        "try{var saved=localStorage.getItem(LS_KEY);"
        "if(saved)progress=migrateProgress(JSON.parse(saved));}catch(e){}"
        "initProgress();"
        "function saveProg(){try{localStorage.setItem(LS_KEY,JSON.stringify(progress));}catch(e){}}"
        "function getAnswered(lvl){var ln=LEVELS[lvl];return progress.levels[ln].answered;}"
        "function getLevelDone(lvl){return getAnswered(lvl).length;}"
        "function isTestPassed(lvl){var ln=LEVELS[lvl];return progress.levels[ln].testPassed;}"
        "function isAllAnswered(lvl){return getLevelDone(lvl)>=LEVEL_SIZE[LEVELS[lvl]];}"
        "function isLevelUnlocked(lvl){if(lvl===0)return true;"
        "return isTestPassed(lvl-1);}"
        "function getLevelStatus(lvl){var done=getLevelDone(lvl);var total=LEVEL_SIZE[LEVELS[lvl]];"
        "if(isTestPassed(lvl))return'done';"
        "if(done>=total)return'test_ready';"
        "if(done>0)return'in_progress';"
        "return'not_started';}"
        "/* === CORE FUNCTIONS === */"
        "function shuffle(a){for(var i=a.length-1;i>0;i--){"
        "var j=Math.floor(Math.random()*(i+1));var tmp=a[i];a[i]=a[j];a[j]=tmp;}return a;}"
        "function startLevel(lvl){currentLevel=lvl;var ln=LEVELS[lvl];"
        "var answered=getAnswered(lvl);"
        "var unanswered=[];for(var i=0;i<WORDS[ln].length;i++){"
        "if(answered.indexOf(i)<0)unanswered.push(i);}"
        "if(unanswered.length===0){showFinalTestIntro();return;}"
        "words=shuffle(unanswered);wordIdx=0;"
        "score=progress.levels[ln].score;streak=0;bestStreak=0;correct=0;wrong=0;"
        "nextWord();state='play';topbar.style.display='flex';progBar.style.display='block';"
        "lvlBadge.textContent=ln;lvlBadge.style.background='linear-gradient(135deg,'+LEVEL_GRADIENTS[ln][0]+','+LEVEL_GRADIENTS[ln][1]+')';"
        "updateHUD();}"
        "function nextWord(){if(wordIdx>=words.length){"
        "if(isAllAnswered(currentLevel)){showFinalTestIntro();return;}"
        "var ln=LEVELS[currentLevel];var answered=getAnswered(currentLevel);"
        "var un=[];for(var i=0;i<WORDS[ln].length;i++){if(answered.indexOf(i)<0)un.push(i);}"
        "if(un.length===0){showFinalTestIntro();return;}"
        "words=shuffle(un);wordIdx=0;}"
        "var wi=words[wordIdx];var ln=LEVELS[currentLevel];var w=WORDS[ln][wi];"
        "var pool=[];for(var i=0;i<WORDS[ln].length;i++){if(i!==wi)pool.push(WORDS[ln][i]);}"
        "pool=shuffle(pool);var wrongs=pool.slice(0,3);"
        "options=[{text:w.e,correct:true,idx:wi}];"
        "for(var i=0;i<3;i++)options.push({text:wrongs[i].e,correct:false,idx:-1});"
        "options=shuffle(options);correctOptIdx=-1;"
        "for(var i=0;i<4;i++)if(options[i].correct)correctOptIdx=i;"
        "timer=maxTime;selectedOpt=-1;showResult=0;cardFloat=0;}"
        "function selectOption(idx){if(showResult>0||selectedOpt>=0)return;"
        "if(state!=='play'&&state!=='final_test')return;"
        "selectedOpt=idx;"
        "if(state==='play'){handlePlayAnswer(idx);}"
        "else if(state==='final_test'){handleFinalTestAnswer(idx);}}"
        "function handlePlayAnswer(idx){"
        "resultCorrect=options[idx].correct;showResult=2.0;"
        "if(resultCorrect){correct++;streak++;"
        "if(streak>bestStreak)bestStreak=streak;"
        "var mult=streak>=10?3:streak>=5?2:streak>=3?1.5:1;"
        "var pts=Math.round((100+Math.round(timer*5))*mult);"
        "score+=pts;var ln=LEVELS[currentLevel];"
        "var wi=options[idx].idx;var ans=progress.levels[ln].answered;"
        "if(ans.indexOf(wi)<0){ans.push(wi);}"
        "progress.levels[ln].score=score;saveProg();"
        "scorePopups.push({text:'+'+pts,x:410,y:280,life:1.5,col:'#69f0ae'});pulseTimer=0.5;"
        "for(var i=0;i<8;i++){confetti.push({x:410,y:320,vx:(Math.random()-0.5)*8,"
        "vy:-Math.random()*10-3,r:Math.random()*4+2,col:['#69f0ae','#40c4ff','#ffab40','#e040fb','#ff5252','#00e5ff'][Math.floor(Math.random()*6)],"
        "life:1.5,shape:Math.floor(Math.random()*3)});}}"
        "else{wrong++;streak=0;shakeTimer=0.4;}"
        "updateHUD();}"
        "/* === FINAL TEST === */"
        "function showFinalTestIntro(){state='final_test_intro';"
        "topbar.style.display='none';progBar.style.display='none';}"
        "function startFinalTest(){var ln=LEVELS[currentLevel];"
        "var pool=[];for(var i=0;i<WORDS[ln].length;i++)pool.push(i);"
        "ftWords=shuffle(pool).slice(0,FINAL_TEST_COUNT);"
        "ftIdx=0;ftCorrect=0;ftWrong=0;ftScore=0;ftStreak=0;"
        "state='final_test';topbar.style.display='flex';progBar.style.display='block';"
        "lvlBadge.textContent=LEVELS[currentLevel]+' TEST';"
        "lvlBadge.style.background='linear-gradient(135deg,#ffd700,#ff8f00)';"
        "loadFinalTestQuestion();updateFinalTestHUD();}"
        "function loadFinalTestQuestion(){"
        "if(ftIdx>=FINAL_TEST_COUNT){showFinalTestResult();return;}"
        "var wi=ftWords[ftIdx];var ln=LEVELS[currentLevel];var w=WORDS[ln][wi];"
        "var pool=[];for(var i=0;i<WORDS[ln].length;i++){if(i!==wi)pool.push(WORDS[ln][i]);}"
        "pool=shuffle(pool);var wrongs=pool.slice(0,3);"
        "options=[{text:w.e,correct:true,idx:wi}];"
        "for(var i=0;i<3;i++)options.push({text:wrongs[i].e,correct:false,idx:-1});"
        "options=shuffle(options);correctOptIdx=-1;"
        "for(var i=0;i<4;i++)if(options[i].correct)correctOptIdx=i;"
        "ftTimer=maxTime;selectedOpt=-1;ftShowResult=0;showResult=0;cardFloat=0;}"
        "function handleFinalTestAnswer(idx){"
        "resultCorrect=options[idx].correct;showResult=1.8;"
        "if(resultCorrect){ftCorrect++;ftStreak++;"
        "var mult=ftStreak>=10?3:ftStreak>=5?2:ftStreak>=3?1.5:1;"
        "var pts=Math.round((100+Math.round(ftTimer*5))*mult);ftScore+=pts;"
        "scorePopups.push({text:'+'+pts,x:410,y:280,life:1.5,col:'#ffd700'});pulseTimer=0.5;"
        "for(var i=0;i<5;i++){confetti.push({x:410,y:320,vx:(Math.random()-0.5)*6,"
        "vy:-Math.random()*8-2,r:Math.random()*3+2,"
        "col:['#ffd700','#ff8f00','#ffab40','#fff176'][Math.floor(Math.random()*4)],"
        "life:1.2,shape:Math.floor(Math.random()*3)});}}"
        "else{ftWrong++;ftStreak=0;shakeTimer=0.4;}"
        "updateFinalTestHUD();}"
        "function showFinalTestResult(){"
        "state='final_result';topbar.style.display='none';progBar.style.display='none';"
        "if(ftCorrect>=FINAL_TEST_PASS){"
        "var ln=LEVELS[currentLevel];progress.levels[ln].testPassed=true;saveProg();"
        "for(var i=0;i<50;i++){confetti.push({x:Math.random()*W,y:Math.random()*H*0.3,"
        "vx:(Math.random()-0.5)*10,vy:-Math.random()*12-5,r:Math.random()*5+2,"
        "col:['#ffd700','#69f0ae','#40c4ff','#e040fb','#ff5252','#00e5ff'][Math.floor(Math.random()*6)],"
        "life:3,shape:Math.floor(Math.random()*3)});}"
        "}}"
        "function updateHUD(){scoreBox.textContent='Skor: '+score;"
        "streakBox.textContent=streak>1?'\\uD83D\\uDD25 x'+streak:'';"
        "var ln=LEVELS[currentLevel];var done=getAnswered(currentLevel).length;"
        "var total=LEVEL_SIZE[ln];var kalan=total-done;"
        "progressText.textContent=done+'/'+total+' \u2022 '+kalan+' kaldi';"
        "progFill.style.width=Math.round(done*100/total)+'%';}"
        "function updateFinalTestHUD(){scoreBox.textContent='Skor: '+ftScore;"
        "streakBox.textContent=ftStreak>1?'\\uD83D\\uDD25 x'+ftStreak:'';"
        "progressText.textContent=(ftIdx+1)+'/'+FINAL_TEST_COUNT;"
        "progFill.style.width=Math.round((ftIdx+1)*100/FINAL_TEST_COUNT)+'%';}"
        "/* === AUDIO === */"
        "var audioCtx=null;function getAudio(){if(!audioCtx)try{audioCtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}return audioCtx;}"
        "function playSound(freq,dur,type){if(!window._uc){if(!window._ucL){window._ucL=1;document.addEventListener('click',function(){window._uc=1});document.addEventListener('touchstart',function(){window._uc=1})}return;}var a=getAudio();if(!a)return;var o=a.createOscillator();var g=a.createGain();"
        "o.connect(g);g.connect(a.destination);o.type=type||'sine';o.frequency.value=freq;"
        "g.gain.setValueAtTime(0.15,a.currentTime);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+dur);"
        "o.start();o.stop(a.currentTime+dur);}"
        "function playLevelUpSound(){var a=getAudio();if(!a)return;"
        "[523,659,784,1047].forEach(function(f,i){setTimeout(function(){playSound(f,0.3,'sine');},i*150);});}"
        "/* === MOUSE/TOUCH === */"
        "function getMousePos(e){var r=canvas.getBoundingClientRect();"
        "var cx=e.clientX||((e.touches&&e.touches[0])?e.touches[0].clientX:0);"
        "var cy=e.clientY||((e.touches&&e.touches[0])?e.touches[0].clientY:0);"
        "return{x:(cx-r.left)*(W/r.width),y:(cy-r.top)*(H/r.height)};}"
        "canvas.addEventListener('mousemove',function(e){var p=getMousePos(e);hoverOpt=-1;"
        "if(state==='play'||state==='final_test'){"
        "var bw=340,bh=52,gap=12,sx=(W-bw*2-gap)/2,sy=430;"
        "for(var i=0;i<4;i++){var col=i%2;var row=Math.floor(i/2);"
        "var bx=sx+col*(bw+gap);var by=sy+row*(bh+gap);"
        "if(p.x>=bx&&p.x<=bx+bw&&p.y>=by&&p.y<=by+bh){hoverOpt=i;break;}}}"
        "if(state==='menu'){"
        "for(var i=0;i<6;i++){var col=i%3;var row=Math.floor(i/3);"
        "var cx2=90+col*230;var cy2=175+row*195;"
        "if(p.x>=cx2&&p.x<=cx2+200&&p.y>=cy2&&p.y<=cy2+170){hoverOpt=100+i;break;}}}});"
        "canvas.addEventListener('click',function(e){var p=getMousePos(e);"
        "if(state==='menu'){for(var i=0;i<6;i++){var col=i%3;var row=Math.floor(i/3);"
        "var cx2=90+col*230;var cy2=175+row*195;"
        "if(p.x>=cx2&&p.x<=cx2+200&&p.y>=cy2&&p.y<=cy2+170){"
        "if(isLevelUnlocked(i)){var st2=getLevelStatus(i);"
        "if(st2==='test_ready'){currentLevel=i;showFinalTestIntro();}"
        "else if(st2!=='done'){startLevel(i);}"
        "else{startLevel(i);}}"
        "playSound(600,0.1);break;}}}"
        "if(state==='play'||state==='final_test'){"
        "var bw=340,bh=52,gap=12,sx=(W-bw*2-gap)/2,sy=430;"
        "for(var i=0;i<4;i++){var col=i%2;var row=Math.floor(i/2);"
        "var bx=sx+col*(bw+gap);var by=sy+row*(bh+gap);"
        "if(p.x>=bx&&p.x<=bx+bw&&p.y>=by&&p.y<=by+bh){selectOption(i);playSound(440,0.1);break;}}}"
        "if(state==='final_test_intro'){"
        "if(p.x>=260&&p.x<=560&&p.y>=400&&p.y<=460){startFinalTest();playSound(600,0.15);}}"
        "if(state==='final_result'){"
        "if(ftCorrect>=FINAL_TEST_PASS){"
        "if(p.x>=260&&p.x<=560&&p.y>=430&&p.y<=490){"
        "if(currentLevel<5){currentLevel++;startLevel(currentLevel);}"
        "else{state='menu';topbar.style.display='none';progBar.style.display='none';}"
        "playSound(600,0.15);}}"
        "else{if(p.x>=210&&p.x<=410&&p.y>=430&&p.y<=490){startFinalTest();playSound(600,0.15);}"
        "if(p.x>=420&&p.x<=620&&p.y>=430&&p.y<=490){state='menu';topbar.style.display='none';progBar.style.display='none';playSound(400,0.1);}}}"
        "if(state==='levelup'){"
        "if(p.x>=260&&p.x<=560&&p.y>=430&&p.y<=490){"
        "state='menu';topbar.style.display='none';progBar.style.display='none';}}"
        "if(state==='play'||state==='final_test'){"
        "if(p.x>=15&&p.x<=80&&p.y>=610&&p.y<=638){"
        "state='menu';topbar.style.display='none';progBar.style.display='none';"
        "playSound(300,0.1);}}});"
        "canvas.addEventListener('touchstart',function(e){e.preventDefault();"
        "var touch=e.touches[0];canvas.dispatchEvent(new MouseEvent('click',{clientX:touch.clientX,clientY:touch.clientY}));});"
        "/* === DRAW FUNCTIONS === */"
        "function drawBg(){ctx.fillStyle='#010012';ctx.fillRect(0,0,W,H);"
        "for(var i=0;i<nebulas.length;i++){var n=nebulas[i];"
        "n.phase+=n.drift*0.01;n.x+=Math.sin(n.phase)*0.3;n.y+=Math.cos(n.phase*0.7)*0.2;"
        "var ng=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r);"
        "ng.addColorStop(0,n.col);ng.addColorStop(1,'rgba(0,0,0,0)');"
        "ctx.fillStyle=ng;ctx.fillRect(n.x-n.r,n.y-n.r,n.r*2,n.r*2);}"
        "for(var i=0;i<stars.length;i++){var s=stars[i];"
        "s.ph+=s.sp*0.02;var alpha=0.4+0.6*Math.abs(Math.sin(s.ph))*s.twinkle;"
        "ctx.globalAlpha=alpha;ctx.fillStyle=s.col;"
        "ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();"
        "ctx.globalAlpha=alpha*0.3;ctx.beginPath();ctx.arc(s.x,s.y,s.r*3,0,Math.PI*2);ctx.fill();}"
        "ctx.globalAlpha=1.0;}"
        "function drawMenu(){ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';"
        "menuFloat+=0.02;var titleY=60+Math.sin(menuFloat)*4;"
        "ctx.font='bold 40px Segoe UI';"
        "var tg=ctx.createLinearGradient(250,titleY-20,550,titleY+20);"
        "tg.addColorStop(0,'#e040fb');tg.addColorStop(0.5,'#7c4dff');tg.addColorStop(1,'#00e5ff');"
        "ctx.fillStyle=tg;ctx.shadowColor='rgba(120,80,255,0.8)';ctx.shadowBlur=30;"
        "ctx.fillText('English Vocabulary',410,titleY);"
        "ctx.shadowBlur=0;ctx.font='14px Segoe UI';ctx.fillStyle='rgba(180,170,220,0.5)';"
        "ctx.fillText('Kullanici: '+USERNAME+' \u2022 Seviye sec \u2022 Kelimeleri ogren',410,titleY+55);"
        "ctx.font='bold 18px Segoe UI';ctx.fillStyle='rgba(200,180,255,0.8)';"
        "ctx.fillText('Premium Ultra Diamond',410,titleY+30);"
        "for(var i=0;i<6;i++){var col=i%3;var row=Math.floor(i/3);"
        "var cx2=90+col*230;var cy2=175+row*195;"
        "var ln=LEVELS[i];var unlocked=isLevelUnlocked(i);"
        "var st2=getLevelStatus(i);var done=getLevelDone(i);var total=LEVEL_SIZE[ln];"
        "ctx.globalAlpha=unlocked?1:0.35;"
        "ctx.save();ctx.beginPath();ctx.roundRect(cx2,cy2,200,170,14);ctx.clip();"
        "var cg=ctx.createLinearGradient(cx2,cy2,cx2+200,cy2+170);"
        "cg.addColorStop(0,'rgba(20,15,60,0.9)');cg.addColorStop(1,'rgba(10,8,40,0.95)');"
        "ctx.fillStyle=cg;ctx.fillRect(cx2,cy2,200,170);"
        "ctx.restore();"
        "ctx.strokeStyle=unlocked?LEVEL_COLORS[ln]:'rgba(100,100,120,0.3)';"
        "ctx.lineWidth=unlocked?2:1;ctx.beginPath();ctx.roundRect(cx2,cy2,200,170,14);ctx.stroke();"
        "if(st2==='done'){ctx.strokeStyle='rgba(105,240,174,0.6)';ctx.lineWidth=2;"
        "ctx.beginPath();ctx.roundRect(cx2,cy2,200,170,14);ctx.stroke();}"
        "ctx.textAlign='center';ctx.textBaseline='middle';"
        "ctx.font='bold 32px Segoe UI';ctx.fillStyle=unlocked?LEVEL_COLORS[ln]:'#555';"
        "ctx.fillText(ln,cx2+100,cy2+40);"
        "ctx.font='13px Segoe UI';ctx.fillStyle=unlocked?'rgba(200,200,220,0.8)':'#444';"
        "ctx.fillText(LEVEL_LABELS[ln],cx2+100,cy2+65);"
        "if(!unlocked){ctx.font='28px Segoe UI';ctx.fillStyle='#555';ctx.fillText('\\uD83D\\uDD12',cx2+100,cy2+100);}"
        "else{"
        "var pct=Math.round(done*100/total);"
        "ctx.fillStyle='rgba(255,255,255,0.08)';ctx.beginPath();ctx.roundRect(cx2+20,cy2+85,160,10,5);ctx.fill();"
        "if(pct>0){ctx.fillStyle=LEVEL_COLORS[ln];ctx.beginPath();ctx.roundRect(cx2+20,cy2+85,Math.max(5,160*pct/100),10,5);ctx.fill();}"
        "ctx.font='12px Segoe UI';ctx.fillStyle='rgba(200,200,220,0.7)';"
        "ctx.fillText(done+'/'+total+' kelime',cx2+100,cy2+110);"
        "ctx.font='bold 13px Segoe UI';"
        "if(st2==='done'){ctx.fillStyle='#69f0ae';ctx.fillText('\u2713 Tamamlandi',cx2+100,cy2+135);}"
        "else if(st2==='test_ready'){ctx.fillStyle='#ffd700';ctx.fillText('\\uD83C\\uDFC6 Test Bekliyor',cx2+100,cy2+135);}"
        "else if(st2==='in_progress'){ctx.fillStyle='#40c4ff';ctx.fillText('Devam Ediyor',cx2+100,cy2+135);}"
        "else{ctx.fillStyle='rgba(180,180,200,0.5)';ctx.fillText('Baslamadi',cx2+100,cy2+135);}}"
        "ctx.font='11px Segoe UI';ctx.fillStyle='rgba(180,180,200,0.3)';"
        "ctx.fillText(total+' kelime',cx2+100,cy2+155);}"
        "ctx.globalAlpha=1;ctx.restore();}"
        "function drawCurrentWord(){var ln=LEVELS[currentLevel];var wi;"
        "if(state==='final_test'){wi=ftWords[ftIdx];}else{wi=words[wordIdx];}"
        "var w=WORDS[ln][wi];"
        "cardFloat+=0.03;var fy=Math.sin(cardFloat)*3;"
        "var cx2=W/2;var cy2=300+fy;"
        "if(shakeTimer>0){cx2+=Math.sin(shakeTimer*40)*8;}"
        "ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';"
        "var cg=ctx.createLinearGradient(cx2-180,cy2-50,cx2+180,cy2+50);"
        "cg.addColorStop(0,'rgba(30,20,80,0.95)');cg.addColorStop(1,'rgba(15,10,50,0.95)');"
        "ctx.fillStyle=cg;ctx.beginPath();ctx.roundRect(cx2-180,cy2-50,360,100,16);ctx.fill();"
        "var gc=LEVEL_COLORS[LEVELS[currentLevel]];"
        "ctx.strokeStyle=gc;ctx.lineWidth=2;"
        "ctx.shadowColor=gc;ctx.shadowBlur=20;"
        "ctx.beginPath();ctx.roundRect(cx2-180,cy2-50,360,100,16);ctx.stroke();"
        "ctx.shadowBlur=0;"
        "ctx.font='bold 34px Segoe UI';ctx.fillStyle='#fff';ctx.fillText(w.t,cx2,cy2);"
        "ctx.restore();}"
        "function drawOptions(){var bw=340,bh=52,gap=12;"
        "var sx=(W-bw*2-gap)/2,sy=430;"
        "for(var i=0;i<4;i++){var col=i%2;var row=Math.floor(i/2);"
        "var bx=sx+col*(bw+gap);var by=sy+row*(bh+gap);"
        "ctx.save();"
        "var isHover=hoverOpt===i;var isSel=selectedOpt===i;"
        "var bg;if(showResult>0&&isSel&&resultCorrect){bg='rgba(40,180,100,0.5)';}"
        "else if(showResult>0&&isSel&&!resultCorrect){bg='rgba(220,50,50,0.5)';}"
        "else if(showResult>0&&options[i].correct){bg='rgba(40,180,100,0.3)';}"
        "else if(isHover){bg='rgba(100,80,200,0.4)';}"
        "else{bg='rgba(25,18,60,0.85)';}"
        "ctx.fillStyle=bg;ctx.beginPath();ctx.roundRect(bx,by,bw,bh,12);ctx.fill();"
        "var sc=showResult>0&&options[i].correct?'#69f0ae':"
        "showResult>0&&isSel&&!resultCorrect?'#ff5252':"
        "isHover?'rgba(140,100,255,0.8)':'rgba(120,100,180,0.3)';"
        "ctx.strokeStyle=sc;ctx.lineWidth=showResult>0&&options[i].correct?2:1;"
        "ctx.beginPath();ctx.roundRect(bx,by,bw,bh,12);ctx.stroke();"
        "ctx.textAlign='center';ctx.textBaseline='middle';"
        "ctx.font='bold 18px Segoe UI';"
        "ctx.fillStyle=showResult>0&&options[i].correct?'#69f0ae':'#e0d8f0';"
        "ctx.fillText(options[i].text,bx+bw/2,by+bh/2);"
        "ctx.restore();}}"
        "function drawTimer(){var t=state==='final_test'?ftTimer:timer;"
        "var pct=t/maxTime;var x=W/2;var y=230;"
        "ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';"
        "ctx.beginPath();ctx.arc(x,y,22,0,Math.PI*2);"
        "ctx.fillStyle='rgba(20,15,50,0.8)';ctx.fill();"
        "ctx.strokeStyle='rgba(100,80,180,0.3)';ctx.lineWidth=3;"
        "ctx.beginPath();ctx.arc(x,y,22,-Math.PI/2,-Math.PI/2+Math.PI*2*pct);"
        "ctx.strokeStyle=pct>0.5?'#69f0ae':pct>0.25?'#ffab40':'#ff5252';"
        "ctx.stroke();"
        "ctx.font='bold 16px Segoe UI';ctx.fillStyle='#fff';"
        "ctx.fillText(Math.ceil(t),x,y);ctx.restore();}"
        "function drawBack(){ctx.save();ctx.textAlign='left';ctx.textBaseline='middle';"
        "ctx.font='13px Segoe UI';ctx.fillStyle='rgba(180,170,220,0.4)';"
        "ctx.fillText('\u2190 Menu',20,625);ctx.restore();}"
        "function drawPlay(dt){"
        "if(showResult>0){showResult-=dt;if(showResult<=0){"
        "if(state==='play'){wordIdx++;nextWord();}"
        "else if(state==='final_test'){ftIdx++;loadFinalTestQuestion();}}}"
        "else{if(state==='final_test'){ftTimer-=dt;}else{timer-=dt;}"
        "var curT=state==='final_test'?ftTimer:timer;"
        "if(curT<=0&&selectedOpt<0){if(state==='final_test')ftTimer=0;else timer=0;selectedOpt=-2;"
        "showResult=2;resultCorrect=false;"
        "if(state==='play'){wrong++;streak=0;shakeTimer=0.4;updateHUD();}"
        "else if(state==='final_test'){ftWrong++;ftStreak=0;shakeTimer=0.4;updateFinalTestHUD();}}}"
        "if(shakeTimer>0)shakeTimer-=dt;"
        "drawCurrentWord();drawTimer();drawOptions();drawBack();}"
        "function drawFinalTestIntro(){ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';"
        "menuFloat+=0.02;var cy=H/2-30+Math.sin(menuFloat)*3;"
        "ctx.font='bold 42px Segoe UI';"
        "var tg=ctx.createLinearGradient(200,cy-30,620,cy+30);"
        "tg.addColorStop(0,'#ffd700');tg.addColorStop(0.5,'#ff8f00');tg.addColorStop(1,'#ffd700');"
        "ctx.fillStyle=tg;ctx.shadowColor='rgba(255,200,0,0.6)';ctx.shadowBlur=30;"
        "ctx.fillText('\\uD83C\\uDFC6 Bitirme Testi',410,cy-40);"
        "ctx.shadowBlur=0;ctx.font='bold 24px Segoe UI';ctx.fillStyle='#fff';"
        "ctx.fillText(LEVELS[currentLevel]+' Seviyesi',410,cy+10);"
        "ctx.font='16px Segoe UI';ctx.fillStyle='rgba(220,210,255,0.7)';"
        "ctx.fillText('Tum kelimeleri ogrendin! Simdi '+FINAL_TEST_COUNT+' soruluk testi gec.',410,cy+50);"
        "ctx.fillText(FINAL_TEST_PASS+'/'+FINAL_TEST_COUNT+' dogru yaparsan sonraki seviye acilir.',410,cy+75);"
        "ctx.fillStyle='rgba(255,200,100,0.6)';ctx.font='14px Segoe UI';"
        "ctx.fillText('Test tek seferde cozulmeli - cikarsaniz baslamaniz gerekir!',410,cy+105);"
        "ctx.fillStyle='rgba(255,215,0,0.9)';ctx.beginPath();ctx.roundRect(260,cy+130,300,50,14);ctx.fill();"
        "ctx.fillStyle='#1a1a2e';ctx.font='bold 20px Segoe UI';ctx.fillText('Teste Basla',410,cy+155);"
        "drawBack();ctx.restore();}"
        "function drawFinalResult(){ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';"
        "var passed=ftCorrect>=FINAL_TEST_PASS;var cy=H/2-60;"
        "ctx.font='bold 48px Segoe UI';"
        "if(passed){var tg=ctx.createLinearGradient(200,cy-30,620,cy+30);"
        "tg.addColorStop(0,'#69f0ae');tg.addColorStop(1,'#00e5ff');"
        "ctx.fillStyle=tg;ctx.shadowColor='rgba(100,240,170,0.6)';ctx.shadowBlur=30;"
        "ctx.fillText('\\uD83C\\uDF89 BASARILI!',410,cy);}"
        "else{ctx.fillStyle='#ff5252';ctx.shadowColor='rgba(255,80,80,0.5)';ctx.shadowBlur=20;"
        "ctx.fillText('Basarisiz',410,cy);}"
        "ctx.shadowBlur=0;ctx.font='bold 28px Segoe UI';ctx.fillStyle='#fff';"
        "ctx.fillText(ftCorrect+'/'+FINAL_TEST_COUNT+' Dogru',410,cy+60);"
        "ctx.font='18px Segoe UI';ctx.fillStyle='rgba(220,210,255,0.7)';"
        "ctx.fillText('Skor: '+ftScore,410,cy+95);"
        "if(passed){ctx.font='16px Segoe UI';ctx.fillStyle='#69f0ae';"
        "if(currentLevel<5){ctx.fillText(LEVELS[currentLevel+1]+' seviyesi acildi!',410,cy+130);}"
        "else{ctx.fillText('Tum seviyeler tamamlandi!',410,cy+130);}"
        "ctx.fillStyle='rgba(100,240,170,0.9)';ctx.beginPath();ctx.roundRect(260,cy+160,300,50,14);ctx.fill();"
        "ctx.fillStyle='#1a1a2e';ctx.font='bold 18px Segoe UI';"
        "ctx.fillText(currentLevel<5?'Sonraki Seviye':'Ana Menu',410,cy+185);}"
        "else{ctx.font='16px Segoe UI';ctx.fillStyle='rgba(255,200,100,0.7)';"
        "ctx.fillText(FINAL_TEST_PASS+' dogru gerekli. Tekrar deneyebilirsin!',410,cy+130);"
        "ctx.fillStyle='rgba(255,215,0,0.85)';ctx.beginPath();ctx.roundRect(210,cy+160,190,50,12);ctx.fill();"
        "ctx.fillStyle='#1a1a2e';ctx.font='bold 16px Segoe UI';ctx.fillText('Tekrar Dene',305,cy+185);"
        "ctx.fillStyle='rgba(150,140,200,0.5)';ctx.beginPath();ctx.roundRect(420,cy+160,190,50,12);ctx.fill();"
        "ctx.fillStyle='#fff';ctx.fillText('Ana Menu',515,cy+185);}"
        "ctx.restore();}"
        "function drawConfetti(dt){for(var i=confetti.length-1;i>=0;i--){"
        "var c=confetti[i];c.x+=c.vx;c.y+=c.vy;c.vy+=15*dt;c.life-=dt;"
        "if(c.life<=0){confetti.splice(i,1);continue;}"
        "ctx.globalAlpha=Math.min(1,c.life);ctx.fillStyle=c.col;"
        "if(c.shape===0){ctx.fillRect(c.x-c.r,c.y-c.r,c.r*2,c.r*2);}"
        "else if(c.shape===1){ctx.beginPath();ctx.arc(c.x,c.y,c.r,0,Math.PI*2);ctx.fill();}"
        "else{ctx.beginPath();ctx.moveTo(c.x,c.y-c.r);ctx.lineTo(c.x+c.r,c.y+c.r);ctx.lineTo(c.x-c.r,c.y+c.r);ctx.closePath();ctx.fill();}}"
        "ctx.globalAlpha=1;}"
        "function drawParticles(dt){for(var i=0;i<orbs.length;i++){var o=orbs[i];"
        "o.x+=o.vx;o.y+=o.vy;"
        "if(o.x<0||o.x>W)o.vx*=-1;if(o.y<0||o.y>H)o.vy*=-1;"
        "o.trail.push({x:o.x,y:o.y});if(o.trail.length>20)o.trail.shift();"
        "for(var j=0;j<o.trail.length;j++){var t=o.trail[j];var a=j/o.trail.length*0.3;"
        "ctx.globalAlpha=a;ctx.fillStyle=o.col;ctx.beginPath();ctx.arc(t.x,t.y,o.r*0.5,0,Math.PI*2);ctx.fill();}"
        "ctx.globalAlpha=0.8;ctx.fillStyle=o.col;ctx.beginPath();ctx.arc(o.x,o.y,o.r,0,Math.PI*2);ctx.fill();"
        "ctx.globalAlpha=1;}"
        "for(var i=scorePopups.length-1;i>=0;i--){var sp=scorePopups[i];"
        "sp.y-=40*dt;sp.life-=dt;if(sp.life<=0){scorePopups.splice(i,1);continue;}"
        "ctx.globalAlpha=Math.min(1,sp.life*2);ctx.fillStyle=sp.col;"
        "ctx.font='bold 22px Segoe UI';ctx.textAlign='center';"
        "ctx.fillText(sp.text,sp.x,sp.y);ctx.globalAlpha=1;}}"
        "/* === MAIN LOOP === */"
        "var lastTime=0;function frame(ts){var dt=(ts-lastTime)/1000;if(dt>0.1)dt=0.1;lastTime=ts;"
        "try{animT+=dt;drawBg();"
        "if(state==='menu')drawMenu();"
        "else if(state==='play')drawPlay(dt);"
        "else if(state==='final_test')drawPlay(dt);"
        "else if(state==='final_test_intro')drawFinalTestIntro();"
        "else if(state==='final_result')drawFinalResult();"
        "else if(state==='levelup')drawFinalResult();"
        "drawConfetti(dt);drawParticles(dt);"
        "}catch(err){ctx.fillStyle='#ff0';ctx.font='16px monospace';"
        "ctx.fillText('Error: '+err.message,20,30);}"
        "requestAnimationFrame(frame);}"
        "requestAnimationFrame(frame);"
        "</script></body></html>"
    )

def _render_kazanim_pdf_view():
    """Kazanim PDF Hizli Indirme — bagimsiz view."""
    from utils.ui_common import styled_section
    styled_section("Kazanim PDF Hizli Indirme", "#e11d48")

    _kz_levels = [
        ("preschool", "Okul Oncesi", "Pre-A1", "#0ea5e9"),
        ("1", "1. Sinif", "Pre-A1", "#ef4444"),
        ("2", "2. Sinif", "Pre-A1", "#ef4444"),
        ("3", "3. Sinif", "A1", "#f97316"),
        ("4", "4. Sinif", "A1", "#f97316"),
        ("5", "5. Sinif", "A2", "#eab308"),
        ("6", "6. Sinif", "A2", "#eab308"),
        ("7", "7. Sinif", "B1", "#22c55e"),
        ("8", "8. Sinif", "B1", "#22c55e"),
        ("9", "9. Sinif", "B1", "#3b82f6"),
        ("10", "10. Sinif", "B1+", "#6366f1"),
        ("11", "11. Sinif", "B2", "#8b5cf6"),
        ("12", "12. Sinif", "B2+", "#a855f7"),
    ]

    _c1, _c2, _c3 = st.columns(3)
    with _c1:
        _grade_idx = st.selectbox(
            "Kademe", range(len(_kz_levels)),
            format_func=lambda i: f"{_kz_levels[i][1]} ({_kz_levels[i][2]})",
            key="kzpdf_grade",
        )
    with _c2:
        _scope = st.selectbox(
            "Kapsam", ["Tum Yil (Yillik)", "Unite Secimi"],
            key="kzpdf_scope",
        )
    _lk, _ln, _lc, _lcol = _kz_levels[_grade_idx]

    _unit_sel = None
    _unit_list = []
    if _scope == "Unite Secimi":
        try:
            if "_yd_kzpdf_wp" not in st.session_state:
                with open(_WP_PATH, "r", encoding="utf-8") as _f:
                    st.session_state["_yd_kzpdf_wp"] = _json.load(_f)
            _wp = st.session_state["_yd_kzpdf_wp"]
            _weeks = _wp.get(_lk, [])
            _seen = {}
            for _w in _weeks:
                _u = _w.get("unit", _w.get("week", 0))
                if _u not in _seen:
                    _seen[_u] = _w.get("unit_theme", _w.get("theme", ""))
            _unit_list = [(k, v) for k, v in sorted(_seen.items())]
            if _unit_list:
                with _c2:
                    _unit_sel = st.selectbox(
                        "Unite", range(len(_unit_list)),
                        format_func=lambda i: f"Unite {_unit_list[i][0]}: {_unit_list[i][1]}",
                        key="kzpdf_unit",
                    )
        except Exception:
            pass

    with _c3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("\U0001F4E5 PDF Indir", key="kzpdf_btn", use_container_width=True, type="primary"):
            try:
                if "_yd_kzpdf_wp" not in st.session_state:
                    with open(_WP_PATH, "r", encoding="utf-8") as _f:
                        st.session_state["_yd_kzpdf_wp"] = _json.load(_f)
                _wp2 = st.session_state["_yd_kzpdf_wp"]
                _all_wks = [w for w in _wp2.get(_lk, []) if w.get("outcomes")]
                if _scope == "Unite Secimi" and _unit_sel is not None and _unit_list:
                    _target_u = _unit_list[_unit_sel][0]
                    _all_wks = [w for w in _all_wks if w.get("unit", w.get("week", 0)) == _target_u]

                from views.yd_tools import _generate_kazanim_pdf
                _pbytes = _generate_kazanim_pdf(_ln, _lc, _lcol, _all_wks)
                _slabel = "yillik" if _scope != "Unite Secimi" else f"unite{_unit_list[_unit_sel][0]}"
                st.download_button(
                    "\U0001F4BE PDF Indir",
                    data=_pbytes,
                    file_name=f"kazanimlar_{_lk}_{_slabel}.pdf",
                    mime="application/pdf",
                    key="kzpdf_dl",
                )
            except Exception as _err:
                st.error(f"PDF olusturma hatasi: {_err}")


def _render_yd_dashboard():
    """Yabanci Dil Dashboard — genel bakis, istatistikler, hizli erisim."""
    from datetime import datetime, date as _date_cls
    _yil = _get_academic_year_str()
    _ss = _get_sinif_sube_options()
    _sinif_count = len(set(s for s, _ in _ss))
    _sube_count = len(_ss)

    # Ogrenci sayisi
    try:
        from utils.shared_data import load_shared_students
        _students = load_shared_students()
        _stu_count = len(_students)
    except Exception:
        _students = []
        _stu_count = 0

    # Ogretmen sayisi
    try:
        from utils.shared_data import get_ik_employee_names
        _teachers = get_ik_employee_names()
        _teacher_count = len(_teachers) if _teachers else 0
    except Exception:
        _teacher_count = 0

    # Kurum bilgisi
    try:
        from utils.report_utils import get_institution_info
        _info = get_institution_info()
        _kurum = _info.get("name", "")
    except Exception:
        _kurum = ""

    # Haftalik plan verisi
    _wp_path = _WP_PATH
    _has_plans = os.path.exists(_wp_path)
    _plan_grades = 0
    if _has_plans:
        try:
            with open(_wp_path, "r", encoding="utf-8") as _f:
                _wpd = _json.load(_f)
            _plan_grades = sum(1 for k in _wpd if _wpd.get(k))
        except Exception as _exc:
            _logger.debug('Suppressed: %s', _exc)

    # Akademik hafta
    _today = _date_cls.today()
    _acad_start = _date_cls(_today.year if _today.month >= 9 else _today.year - 1, 9, 11)
    _week_num = max(1, (_today - _acad_start).days // 7 + 1)
    if _week_num > 36:
        _week_num = 36

    _day_map = {0: "Pazartesi", 1: "Sali", 2: "Carsamba", 3: "Persembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
    _today_str = _today.strftime("%d.%m.%Y")
    _today_day = _day_map.get(_today.weekday(), "")

    # ── HEADER (Dark navy + gold tema) ──
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#131825 0%,#1A2035 50%,#232B3E 100%);'
        f'border-radius:16px;padding:24px 28px;margin-bottom:16px;'
        f'border:1px solid rgba(212,175,55,0.15);'
        f'box-shadow:0 8px 32px rgba(0,0,0,.3);">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">'
        f'<div>'
        f'<div style="font-size:1.4rem;font-weight:900;color:#6366F1;letter-spacing:.3px;">'
        f'🌍 Yabancı Dil Modülü</div>'
        f'<div style="font-size:.88rem;color:#94A3B8;margin-top:4px;">'
        f'CEFR Uyumlu Kurumsal Dil Öğretim Platformu</div>'
        + (f'<div style="font-size:.78rem;color:#c0c0d8;margin-top:2px;opacity:.8;">{_kurum}</div>' if _kurum else '')
        + f'</div>'
        f'<div style="text-align:right;">'
        f'<div style="font-size:1.5rem;font-weight:900;color:#6366F1;">{_yil}</div>'
        f'<div style="font-size:.78rem;color:#94A3B8;">{_today_str} | {_today_day}</div>'
        f'<span style="background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.2);border-radius:8px;padding:3px 10px;'
        f'font-size:.75rem;color:#6366F1;font-weight:600;">Hafta {_week_num}/36</span>'
        f'</div></div>'
        # Istatistik satirlari — header icinde kompakt
        f'<div style="display:flex;gap:8px;margin-top:14px;flex-wrap:wrap;">'
        f'<span style="background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.15);border-radius:8px;padding:4px 12px;'
        f'font-size:.75rem;color:#6366F1;font-weight:600;">'
        f'\U0001F4DA {_sinif_count} Sinif | {_sube_count} Sube</span>'
        f'<span style="background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.15);border-radius:8px;padding:4px 12px;'
        f'font-size:.75rem;color:#6366F1;font-weight:600;">'
        f'\U0001F393 {_stu_count} Ogrenci | {_teacher_count} Ogretmen</span>'
        f'<span style="background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.15);border-radius:8px;padding:4px 12px;'
        f'font-size:.75rem;color:#6366F1;font-weight:600;">'
        f'\U0001F4CB {_plan_grades} Plan | {_plan_grades * 360} Saat</span>'
        f'<span style="background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.15);border-radius:8px;padding:4px 12px;'
        f'font-size:.75rem;color:#6366F1;font-weight:600;">'
        f'\U0001F3AF CEFR A1 \u2192 A2</span>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # ── DERS MODELI + CEFR (Tek Satir — dark navy + gold tema) ──
    st.markdown(
        '<div style="display:flex;gap:12px;margin-bottom:12px;flex-wrap:wrap;">'
        # Ders modeli
        '<div style="flex:1;min-width:300px;background:linear-gradient(135deg,#131825,#1A2035);'
        'border:1px solid rgba(212,175,55,0.15);border-radius:12px;padding:12px 16px;">'
        '<div style="font-size:12px;font-weight:700;color:#6366F1;margin-bottom:8px;">'
        '\U0001F4D6 10 Saatlik Haftalik Ders Modeli</div>'
        '<div style="display:flex;gap:8px;">'
        '<div style="flex:1;background:linear-gradient(135deg,#A5B4FC,#6366F1);'
        'color:#0B0F19;border-radius:8px;padding:8px 6px;text-align:center;">'
        '<div style="font-size:18px;font-weight:800;">4</div>'
        '<div style="font-size:9px;font-weight:700;color:#0B0F19;">MAIN COURSE</div></div>'
        '<div style="flex:1;background:linear-gradient(135deg,#6366F1,#6366F1);'
        'color:#0B0F19;border-radius:8px;padding:8px 6px;text-align:center;">'
        '<div style="font-size:18px;font-weight:800;">4</div>'
        '<div style="font-size:9px;font-weight:700;color:#0B0F19;">SKILLS LAB</div></div>'
        '<div style="flex:1;background:linear-gradient(135deg,#6366F1,#E8C975);'
        'color:#0B0F19;border-radius:8px;padding:8px 6px;text-align:center;">'
        '<div style="font-size:18px;font-weight:800;">2</div>'
        '<div style="font-size:9px;font-weight:700;color:#0B0F19;">NATIVE SPEAKER</div></div>'
        '</div></div>'
        # CEFR haritasi
        '<div style="flex:1;min-width:300px;background:linear-gradient(135deg,#131825,#1A2035);'
        'border:1px solid rgba(212,175,55,0.15);border-radius:12px;padding:12px 16px;">'
        '<div style="font-size:12px;font-weight:700;color:#6366F1;margin-bottom:8px;">'
        '\U0001F3AF CEFR Seviye Haritasi</div>'
        '<div style="display:flex;gap:4px;flex-wrap:wrap;">'
        + ''.join(
            f'<div style="flex:1;min-width:55px;background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);'
            f'border-radius:6px;padding:4px 3px;text-align:center;">'
            f'<div style="font-size:8px;color:#94A3B8;">{s}</div>'
            f'<div style="font-size:12px;font-weight:800;color:#6366F1;">{lvl}</div></div>'
            for s, lvl, c in [
                ("1.", "A1.1", "#6366F1"), ("2.", "A1.2", "#6366F1"),
                ("3.", "A1.3", "#6366F1"), ("4.", "A1+", "#6366F1"),
                ("5.", "A2.1", "#6366F1"), ("6.", "A2.2", "#6366F1"),
                ("7.", "A2.3", "#6366F1"), ("8.", "A2.4", "#6366F1"),
            ]
        )
        + '</div></div></div>',
        unsafe_allow_html=True,
    )

    # ── HIZLI ERISIM (Kompakt Grid — dark navy + gold tema) ──
    _qlinks = [
        ("\U0001F4CB Yillik Plan", "36 hafta"),
        ("\u23F1 10 Saat Plan", "Haftalik detay"),
        ("\U0001F4C4 Plan PDF", "B5 baski"),
        ("\U0001F4D5 Etkinlik PDF", "Diamond Ed."),
        ("\U0001F3AF Kazanim PDF", "Unite/Yillik"),
        ("\U0001F4DD Sinav", "Olustur & analiz"),
        ("\U0001F310 Kaynaklar", "Dijital"),
    ]
    st.markdown(
        '<div style="background:linear-gradient(135deg,#131825,#1A2035);'
        'border:1px solid rgba(212,175,55,0.15);border-radius:12px;'
        'padding:10px 14px;margin-bottom:12px;">'
        '<div style="font-size:11px;font-weight:700;color:#6366F1;margin-bottom:6px;">'
        '\u26A1 Hizli Erisim</div>'
        '<div style="display:flex;gap:6px;flex-wrap:wrap;">'
        + ''.join(
            f'<div style="background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:8px;'
            f'padding:6px 10px;flex:1;min-width:100px;">'
            f'<div style="font-size:11px;font-weight:700;color:#6366F1;">{t}</div>'
            f'<div style="font-size:9px;color:#94A3B8;">{d}</div></div>'
            for t, d in _qlinks
        )
        + '</div></div>',
        unsafe_allow_html=True,
    )

    # ── PLATFORM BİLGİSİ ──
    st.markdown(
        f'<div style="margin-top:12px;text-align:center;padding:8px;'
        f'background:#131825;border:1px solid rgba(212,175,55,0.15);border-radius:8px;">'
        f'<span style="font-size:10px;color:#94A3B8;">'
        f'SmartCampus AI &mdash; Yabanci Dil Modulu | '
        f'{_plan_grades} sinif x 36 hafta x 10 saat = {_plan_grades * 360} toplam ders saati'
        f'</span></div>',
        unsafe_allow_html=True,
    )


def _generate_daily_plan_full_pdf(grade_key: str) -> bytes | None:
    """36 hafta x 5 gün = 180 günlük detaylı interaktif ders planı PDF.
    Her gün kendi sayfasında. Days verisinden ana açıklama + detailed plan adımları birleşik."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as rl
        from reportlab.lib.units import cm
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from utils.shared_data import ensure_turkish_pdf_fonts
        from views.yd_tools import _generate_detailed_daily_plan
        from views.yd_content import _CURRICULUM
        import io

        fn, fb = ensure_turkish_pdf_fonts()
        if fn == "Helvetica":
            fn, fb = "Helvetica", "Helvetica-Bold"

        curriculum = _CURRICULUM.get(grade_key, [])
        if not curriculum:
            return None

        grade_num = int(grade_key.replace("grade", "")) if "grade" in grade_key else 0

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=1*cm, bottomMargin=0.8*cm,
                                leftMargin=1.2*cm, rightMargin=1.2*cm)

        # Stiller
        title_s = ParagraphStyle("T", fontName=fb, fontSize=13, alignment=TA_CENTER, spaceAfter=4,
                                  textColor=rl.HexColor("#1e293b"))
        sub_s = ParagraphStyle("S", fontName=fn, fontSize=8.5, alignment=TA_CENTER, spaceAfter=6,
                                textColor=rl.HexColor("#64748b"))
        h2_s = ParagraphStyle("H2", fontName=fb, fontSize=10, spaceAfter=3,
                               textColor=rl.HexColor("#4338CA"))
        cell_s = ParagraphStyle("C", fontName=fn, fontSize=7.5, leading=9.5,
                                 textColor=rl.HexColor("#1e293b"))
        cell_b = ParagraphStyle("CB", fontName=fb, fontSize=7.5, leading=9.5,
                                 textColor=rl.HexColor("#4338CA"))
        small_s = ParagraphStyle("SM", fontName=fn, fontSize=7, leading=9,
                                  textColor=rl.HexColor("#475569"))

        day_names = {"mon": "Pazartesi", "tue": "Sali", "wed": "Carsamba", "thu": "Persembe", "fri": "Cuma"}
        day_keys = ["mon", "tue", "wed", "thu", "fri"]

        elements = []

        # Kapak
        elements.append(Spacer(1, 4*cm))
        elements.append(Paragraph(f"Detayli Interaktif Gunluk Ders Plani", title_s))
        elements.append(Spacer(1, 0.5*cm))
        elements.append(Paragraph(f"{grade_num}. Sinif — 36 Hafta x 5 Gun = 180 Ders Gunu", sub_s))
        elements.append(Paragraph("1. Ders (40dk) + 2. Ders (40dk) — Etkinlik adimlarıyla", sub_s))
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("4+4+2 Modeli: Ana Ders + Beceri Lab + Native Speaker", small_s))
        elements.append(PageBreak())

        day_count = 0
        for week_data in curriculum:
            week_num = week_data.get("week", 0)
            theme = week_data.get("theme", "")
            theme_tr = week_data.get("theme_tr", "")
            vocab = week_data.get("vocab", [])
            structure = week_data.get("structure", "")
            assessment = week_data.get("assessment", "")

            for dk in day_keys:
                # Detaylı plan üret
                plan = _generate_detailed_daily_plan(grade_key, week_data, dk)
                if not plan:
                    continue

                day_name = day_names.get(dk, dk)
                day_count += 1

                # ── Sayfa başlığı ──
                elements.append(Paragraph(
                    f"Hafta {week_num} / {day_name} — {theme} ({theme_tr})",
                    title_s,
                ))
                elements.append(Paragraph(
                    f"{grade_num}. Sinif | Gun {day_count} | Yapi: {structure[:70]}{'...' if len(structure) > 70 else ''}",
                    sub_s,
                ))

                # Kelimeler
                if vocab:
                    vt = ", ".join(vocab[:10])
                    if len(vocab) > 10:
                        vt += f" (+{len(vocab)-10})"
                    elements.append(Paragraph(f"Kelimeler: {vt}", small_s))
                elements.append(Spacer(1, 0.2*cm))

                # Days + skills + linked_content + assessment
                days = week_data.get("days", {})
                day_lessons_text = days.get(dk, [])
                skills = week_data.get("skills", {})
                linked = week_data.get("linked_content", {})
                songs = linked.get("songs", [])
                games = linked.get("games", [])
                dialogues = linked.get("dialogues", [])
                grammar_topics = linked.get("grammar", [])

                # ── 1. DERS (40dk) ──
                lesson_1 = plan.get("lesson_1", [])
                ders1_text = day_lessons_text[0] if len(day_lessons_text) > 0 else ""

                elements.append(Paragraph("1. Ders — Ana Ders (40 dk)", h2_s))
                if ders1_text:
                    elements.append(Paragraph(str(ders1_text), cell_s))
                    elements.append(Spacer(1, 0.15*cm))

                if lesson_1:
                    t1_data = [[
                        Paragraph("Dk", cell_b),
                        Paragraph("Adim", cell_b),
                        Paragraph("Etkinlik Detayi", cell_b),
                    ]]
                    for act in lesson_1:
                        title_text = str(act.get("title", "")).strip()
                        t1_data.append([
                            Paragraph(f"{act.get('min', '')}dk", cell_s),
                            Paragraph(f"{act.get('step', '')}", cell_b),
                            Paragraph(title_text, cell_s),
                        ])

                    t1 = Table(t1_data, colWidths=[1.3*cm, 2.5*cm, 14*cm], repeatRows=1)
                    t1.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), rl.HexColor("#EEF2FF")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), rl.HexColor("#3730A3")),
                        ("GRID", (0, 0), (-1, -1), 0.4, rl.HexColor("#CBD5E1")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [rl.white, rl.HexColor("#F8FAFC")]),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ]))
                    elements.append(t1)
                elements.append(Spacer(1, 0.3*cm))

                # ── 2. DERS (40dk) ──
                lesson_2 = plan.get("lesson_2", [])
                ders2_text = day_lessons_text[1] if len(day_lessons_text) > 1 else ""

                elements.append(Paragraph("2. Ders — Beceri Lab / Native Speaker (40 dk)", h2_s))
                if ders2_text:
                    elements.append(Paragraph(str(ders2_text), cell_s))
                    elements.append(Spacer(1, 0.15*cm))

                if lesson_2:
                    t2_data = [[
                        Paragraph("Dk", cell_b),
                        Paragraph("Adim", cell_b),
                        Paragraph("Etkinlik Detayi", cell_b),
                    ]]
                    for act in lesson_2:
                        title_text = str(act.get("title", "")).strip()
                        t2_data.append([
                            Paragraph(f"{act.get('min', '')}dk", cell_s),
                            Paragraph(f"{act.get('step', '')}", cell_b),
                            Paragraph(title_text, cell_s),
                        ])

                    t2 = Table(t2_data, colWidths=[1.3*cm, 2.5*cm, 14*cm], repeatRows=1)
                    t2.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), rl.HexColor("#F0FDF4")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), rl.HexColor("#166534")),
                        ("GRID", (0, 0), (-1, -1), 0.4, rl.HexColor("#CBD5E1")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [rl.white, rl.HexColor("#F0FDF4")]),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ]))
                    elements.append(t2)

                # ── Beceriler ──
                if skills:
                    elements.append(Spacer(1, 0.2*cm))
                    skill_rows = [[Paragraph("Beceri", cell_b), Paragraph("Hedef", cell_b)]]
                    for sk, sv in skills.items():
                        sk_tr = {"listening": "Dinleme", "speaking": "Konusma", "reading": "Okuma", "writing": "Yazma"}.get(sk, sk)
                        skill_rows.append([Paragraph(sk_tr, cell_b), Paragraph(str(sv), cell_s)])
                    st_tbl = Table(skill_rows, colWidths=[2.5*cm, 15.3*cm], repeatRows=1)
                    st_tbl.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), rl.HexColor("#FEF3C7")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), rl.HexColor("#92400E")),
                        ("GRID", (0, 0), (-1, -1), 0.3, rl.HexColor("#E5E7EB")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("TOPPADDING", (0, 0), (-1, -1), 2),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ]))
                    elements.append(st_tbl)

                # ── Materyaller (linked_content) ──
                _mat_parts = []
                if songs:
                    _mat_parts.append(f"Sarki: {', '.join(songs[:2])}")
                if dialogues:
                    _mat_parts.append(f"Diyalog: {', '.join(dialogues[:2])}")
                if games:
                    _mat_parts.append(f"Oyun: {', '.join(games[:2])}")
                if grammar_topics:
                    _mat_parts.append(f"Gramer: {', '.join(grammar_topics[:2])}")
                if _mat_parts:
                    elements.append(Spacer(1, 0.1*cm))
                    elements.append(Paragraph("Materyaller: " + " | ".join(_mat_parts), small_s))

                # Cuma değerlendirme
                if dk == "fri" and assessment:
                    elements.append(Spacer(1, 0.2*cm))
                    elements.append(Paragraph(f"Haftalik Degerlendirme: {assessment}", small_s))

                elements.append(PageBreak())

        # Son sayfa
        elements.append(Spacer(1, 4*cm))
        elements.append(Paragraph("Plan Tamamlandi", title_s))
        elements.append(Paragraph(f"{grade_num}. Sinif — {day_count} ders gunu", sub_s))

        doc.build(elements)
        return buf.getvalue()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None


def _render_main_course_book():
    """Main Course Book — tüm kademeler için interaktif flipbook ders kitabı."""
    styled_header("📘 Main Course Book", "İnteraktif Sesli Ders Kitabı — Tüm Kademeler")

    _grade_map = {
        "Okul Öncesi — Early Steps": 0,
        "1. Sınıf — Bright Start 1": 1,
        "2. Sınıf — Bright Start 2": 2,
        "3. Sınıf — Bright Start 3": 3,
        "4. Sınıf — Bright Start 4": 4,
        "5. Sınıf — Next Level 5": 5,
        "6. Sınıf — Next Level 6": 6,
        "7. Sınıf — Next Level 7": 7,
        "8. Sınıf — Next Level 8": 8,
        "9. Sınıf — English Core 9": 9,
        "10. Sınıf — English Core 10": 10,
        "11. Sınıf — English Core 11": 11,
        "12. Sınıf — English Core 12": 12,
    }

    _sel = st.selectbox("📚 Sınıf / Kitap Seçin", list(_grade_map.keys()), key="mc_grade_select")
    _grade = _grade_map[_sel]

    try:
        from views.textbook_grade5 import build_coursebook_flipbook_html

        # Müfredat yükle
        _cur = None
        if _grade == 0:
            from views.curriculum_okul_oncesi import CURRICULUM_PRESCHOOL
            _cur = CURRICULUM_PRESCHOOL
        elif _grade in (1, 2, 3, 4):
            from views.curriculum_ilkokul import (
                CURRICULUM_GRADE1, CURRICULUM_GRADE2, CURRICULUM_GRADE3, CURRICULUM_GRADE4)
            _cur = {1: CURRICULUM_GRADE1, 2: CURRICULUM_GRADE2,
                    3: CURRICULUM_GRADE3, 4: CURRICULUM_GRADE4}[_grade]
        elif _grade in (5, 6, 7, 8):
            from views.curriculum_ortaokul import (
                CURRICULUM_GRADE5, CURRICULUM_GRADE6, CURRICULUM_GRADE7, CURRICULUM_GRADE8)
            _cur = {5: CURRICULUM_GRADE5, 6: CURRICULUM_GRADE6,
                    7: CURRICULUM_GRADE7, 8: CURRICULUM_GRADE8}[_grade]
        elif _grade in (9, 10, 11, 12):
            from views.curriculum_lise import (
                CURRICULUM_GRADE9, CURRICULUM_GRADE10, CURRICULUM_GRADE11, CURRICULUM_GRADE12)
            _cur = {9: CURRICULUM_GRADE9, 10: CURRICULUM_GRADE10,
                    11: CURRICULUM_GRADE11, 12: CURRICULUM_GRADE12}[_grade]

        if _cur:
            from views.coursebook_engine import build_anime_coursebook
            _html = build_anime_coursebook(_grade, _cur, mode="student")
            st.components.v1.html(_html, height=750, scrolling=True)

            # PDF export
            if st.button("📄 PDF Olarak İndir", key="mc_pdf_export", type="secondary", use_container_width=True):
                with st.spinner("PDF oluşturuluyor..."):
                    from views.coursebook_engine import build_anime_coursebook_pdf
                    _pdf = build_anime_coursebook_pdf(_grade, _cur)
                if _pdf:
                    st.download_button(
                        "⬇️ Main Course Book PDF İndir",
                        data=_pdf,
                        file_name=f"main_course_grade{_grade}.pdf",
                        mime="application/pdf",
                        key="mc_pdf_dl",
                    )
                else:
                    st.error("PDF oluşturulamadı.")
        else:
            st.info("Bu sınıf seviyesi için müfredat verisi bulunamadı.")
    except Exception as _e:
        st.error(f"Ders kitabı yüklenirken hata: {_e}")


def _render_yabanci_dil():
    """Yabanci Dil sekmesi — alt sekmeler ile dil oyunlari."""
    _comp_rendered_keys.clear()  # Reset duplicate guard for this render cycle
    # Stop ALL lingering audio: speechSynthesis + AudioContext + HTML5 audio/video
    st.components.v1.html(
        "<script>"
        "(function(){"
        "function killAudio(w){"
        "  try{w.speechSynthesis.cancel()}catch(e){}"
        "  try{var aa=w.document.querySelectorAll('audio,video');"
        "  aa.forEach(function(a){try{a.pause();a.currentTime=0;a.src='';}catch(e){}});}catch(e){}"
        "}"
        "function killCtx(w){"
        "  var names=['AC','audioCtx','_aC','ac','actx','audioContext'];"
        "  names.forEach(function(n){try{if(w[n]&&w[n].state!=='closed'){w[n].close()}}catch(e){}});"
        "}"
        "killAudio(window);"
        "killCtx(window);"
        "try{killAudio(window.parent);killCtx(window.parent)}catch(e){}"
        "try{"
        "  var iframes=window.parent.document.querySelectorAll('iframe');"
        "  iframes.forEach(function(f){"
        "    try{"
        "      killAudio(f.contentWindow);"
        "      killCtx(f.contentWindow);"
        "    }catch(e){}"
        "  });"
        "}catch(e){}"
        # Continuously kill for 3 seconds to catch delayed audio
        "var _killCount=0;"
        "var _killInterval=setInterval(function(){"
        "  _killCount++;"
        "  try{window.parent.speechSynthesis.cancel()}catch(e){}"
        "  try{"
        "    window.parent.document.querySelectorAll('iframe').forEach(function(f){"
        "      try{f.contentWindow.speechSynthesis.cancel()}catch(e){}"
        "      try{var aa=f.contentWindow.document.querySelectorAll('audio,video');"
        "        aa.forEach(function(a){try{a.pause();a.src=''}catch(e){}});}catch(e){}"
        "    });"
        "  }catch(e){}"
        "  if(_killCount>=6)clearInterval(_killInterval);"
        "},500);"
        "})();"
        "</script>",
        height=0,
    )
    # Ana ekranda dashboard kendi header'ini gosteriyor, styled_header sadece kademe gorunumlerinde
    if st.session_state.get("yd_view", "ana") != "ana":
        styled_header("🌍 Yabancı Dil", "Kurumsal Dil Öğretim Platformu — CEFR Uyumlu")

    # ── QR Kod Yonlendirme Handler ──
    _qr_modul = st.query_params.get("modul", "")
    _qr_aksiyon = st.query_params.get("aksiyon", "")
    _qr_sinif = st.query_params.get("sinif", "")
    _qr_unite = st.query_params.get("unite", "")
    _qr_sekme = st.query_params.get("sekme", "")
    if _qr_modul == "yabanci_dil" and _qr_aksiyon and _qr_sinif:
        _qr_grade = int(_qr_sinif) if _qr_sinif.isdigit() else 0
        # Kademeyi belirle
        if 5 <= _qr_grade <= 8:
            st.session_state["yd_view"] = "secondary"
        elif 9 <= _qr_grade <= 12:
            st.session_state["yd_view"] = "high"
        elif 1 <= _qr_grade <= 4:
            st.session_state["yd_view"] = "primary"
        # QR bilgilerini session'a kaydet (sekme icinde kullanilacak)
        st.session_state["_qr_target"] = {
            "grade": str(_qr_grade),
            "action": _qr_aksiyon,
            "unit": _qr_unite,
            "tab_index": int(_qr_sekme) if _qr_sekme.isdigit() else None,
        }
        # Query params temizle
        for k in ["modul", "aksiyon", "sinif", "unite", "sekme"]:
            if k in st.query_params:
                del st.query_params[k]
        # Bilgilendirme
        _aksiyon_labels = {
            "listening": "Dinleme Etkinlikleri",
            "speaking": "Konusma Etkinlikleri",
            "reading": "Okuma Etkinlikleri",
            "writing": "Yazma Etkinlikleri",
            "grammar": "Dilbilgisi Etkinlikleri",
            "vocabulary": "Kelime Etkinlikleri",
            "pronunciation": "Telaffuz",
            "kitaplar": "Dijital Kitaplar (Flipbook)",
            "kaynaklar": "Dis Kaynaklar",
            "interactive": "Interaktif Oyunlar",
            "coursebook": "Ders Kitabi",
            "song": "Sarki / Tekerleme",
        }
        _lbl = _aksiyon_labels.get(_qr_aksiyon, _qr_aksiyon.title())
        st.toast(f"QR: {_qr_grade}. Sinif — {_lbl} (Unite {_qr_unite})")
        st.rerun()

    # ── Global Filtreler (Eğitim-Öğretim Yılı / Sınıf / Şube) ──
    _gcol1, _gcol2, _gcol3 = st.columns([1.2, 0.8, 0.8])
    with _gcol1:
        _yil = _get_academic_year_str()
        _prev_yil = f"{int(_yil[:4]) - 1}-{int(_yil[:4])}"
        _yil_opts = [_prev_yil, _yil]
        st.selectbox(
            "\U0001F4C5 Egitim-Ogretim Yili:",
            _yil_opts, index=1, key="yd_egitim_yili",
        )
    with _gcol2:
        _ss_all = _get_sinif_sube_options()
        _sinif_set = sorted(set(s for s, _ in _ss_all))
        _sinif_opts = [None] + _sinif_set
        st.selectbox(
            "\U0001F3EB Sinif:",
            _sinif_opts,
            format_func=lambda x: "\u2014 Genel \u2014" if x is None else f"{x}. Sinif",
            key="yd_sinif",
        )
    with _gcol3:
        _sel_sinif = st.session_state.get("yd_sinif")
        if _sel_sinif is not None:
            _sube_set = sorted(set(sb for s, sb in _ss_all if s == _sel_sinif))
            _sube_opts = [None] + _sube_set
        else:
            _sube_opts = [None]
        st.selectbox(
            "\U0001F4CB Sube:",
            _sube_opts,
            format_func=lambda x: "\u2014 Tumu \u2014" if x is None else x,
            key="yd_sube",
        )
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ── SESSION STATE TABANLI NAVİGASYON (Performans icin sadece secili view render edilir) ──
    if "yd_view" not in st.session_state:
        st.session_state["yd_view"] = "ana"

    _yd_view = st.session_state["yd_view"]

    # ── "Ana Ekrana Don" butonu (kademe/arac gorunumlerinde) ──
    # Veli rolü — geri dönüş yok, sadece Okuma Kütüphanesi
    from utils.auth import AuthManager as _AuthMgr
    _is_veli_yd = _AuthMgr.get_current_user().get("role") == "Veli"
    if _yd_view != "ana" and not _is_veli_yd:
        _bk1, _bk2 = st.columns([0.18, 0.82])
        with _bk1:
            if st.button("\u2B05 Ana Ekrana Don", key="yd_back_main", type="secondary"):
                st.session_state["yd_view"] = "ana"
                st.rerun()
        with _bk2:
            _view_labels = {
                "preschool": "\U0001F392 Okul Oncesi",
                "primary": "\U0001F4D5 Ilkokul (1-4)",
                "secondary": "\U0001F4D7 Ortaokul (5-8)",
                "high": "\U0001F4D8 Lise (9-12)",
                "vocab": "\U0001F1EC\U0001F1E7 Ingilizce Kelime",
                "plan": "\U0001F4CB Plan & Etkinlik Olusturma",
                "plan_pdf": "\U0001F4C4 Ders Plani PDF",
                "activity_pdf": "\U0001F3AF Etkinlik Kitabi PDF",
                "odev": "\U0001F4DD Odev",
                "sinav": "\U0001F4CA Sinav/Degerlendirme",
                "olcme36": "\U0001F4DD 36 Hafta Olcme Degerlendirme",
                "yd_quiz": "\U0001F3AF Unite Quiz Sistemi",
                "ibook": "\U0001F4D6 Interaktif Etkinlik Kitabi",
                "dijital": "\U0001F4DA Dijital Kaynaklar",
                "srs": "\U0001F504 SRS Kelime Tekrar",
                "ai_conv": "\U0001F916 AI Konusma",
                "reading": "\U0001F4D6 Okuma Kutuphanesi",
                "temelden": "\U0001F680 Temelden Baslama",
                "mufredatli": "\U0001F4D0 Ingilizce Mufredatli",
                "kazanimlar": "\U0001F3AF Kazanimlar",
                "kazanim_pdf": "\U0001F3AF Kazanim PDF Hizli Indirme",
                "cefr_placement": "\U0001F4CB CEFR Seviye Tespit Sinavi",
                "games": "\U0001F9E9 Games & Puzzles",
                "spotlight": "\U0001F4D6 Spotlight Reading",
                "lesson_pdf": "\U0001F4C4 Ders Isleme Motoru PDF",
            }
            _vl = _view_labels.get(_yd_view, _yd_view)
            st.markdown(
                f'<div style="padding:6px 0;font-size:1.05rem;font-weight:700;color:#6366F1;">{_vl}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # ANA EKRAN — Kademe Secim + Arac Kisayollari
    # ══════════════════════════════════════════════════════════════════
    if _yd_view == "ana":
        _render_yd_dashboard()

        # ── DERS İŞLEME MOTORU ──
        st.markdown(
            '<div style="background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#312e81 100%);padding:16px 20px;'
            'border-radius:14px;margin:18px 0 10px 0;border:1.5px solid rgba(99,102,241,0.3);">'
            '<div style="font-size:1.1rem;font-weight:700;color:#818cf8;">'
            '\U0001F393 Ders Isleme Motoru</div>'
            '<div style="font-size:.82rem;color:#a5b4fc;margin-top:3px;">'
            'Plan + 4 Kitap + Etkilesimli Alistirma — Ogretmen dersi isler, ogrenci doldurur</div></div>',
            unsafe_allow_html=True,
        )
        _ld_cols_top = st.columns(5)
        with _ld_cols_top[0]:
            if st.button("\U0001F393 Ders Isleme Motorunu Ac", key="yd_open_lesson_delivery_top",
                          use_container_width=True, type="primary"):
                st.session_state["yd_view"] = "lesson"
                st.rerun()
        with _ld_cols_top[1]:
            if st.button("\U0001F4C4 Ders Isleme Motoru PDF", key="yd_open_lesson_pdf_top",
                          use_container_width=True, type="secondary"):
                st.session_state["yd_view"] = "lesson_pdf"
                st.rerun()
        with _ld_cols_top[2]:
            if st.button("\U0001F4CB CEFR Seviye Tespit", key="yd_open_cefr_placement_top",
                          use_container_width=True, type="primary"):
                st.session_state["yd_view"] = "cefr_placement"
                st.rerun()
        with _ld_cols_top[3]:
            if st.button("\U0001F3C6 CEFR Mock Exam", key="yd_open_cefr_exam_top",
                          use_container_width=True, type="secondary"):
                st.session_state["yd_view"] = "cefr_exam"
                st.rerun()
        with _ld_cols_top[4]:
            if st.button("\U0001F680 Akilli Ogrenme Merkezi", key="yd_open_adaptive_top",
                          use_container_width=True, type="secondary"):
                st.session_state["yd_view"] = "adaptive_hub"
                st.rerun()

        # ── UNITE QUIZ & OLCME KISAYOLLARI ──
        st.markdown(
            '<div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 50%,#4338ca 100%);padding:16px 20px;'
            'border-radius:14px;margin:16px 0 10px 0;border:1.5px solid rgba(129,140,248,0.3);">'
            '<div style="font-size:1.1rem;font-weight:700;color:#a5b4fc;">'
            '\U0001F3AF Unite Quiz & Olcme Degerlendirme</div>'
            '<div style="font-size:.82rem;color:#c7d2fe;margin-top:3px;">'
            'Unite bazli quiz olustur | 36 hafta olcme | Sinav sonuclari & karne</div></div>',
            unsafe_allow_html=True,
        )
        _qz_cols = st.columns(3)
        with _qz_cols[0]:
            if st.button("\U0001F3AF Unite Quiz Sistemi", key="yd_open_quiz_main",
                          use_container_width=True, type="primary"):
                st.session_state["yd_view"] = "yd_quiz"
                st.rerun()
        with _qz_cols[1]:
            if st.button("\U0001F4DD 36 Hafta Olcme Degerlendirme", key="yd_open_olcme36_main",
                          use_container_width=True, type="secondary"):
                st.session_state["yd_view"] = "olcme36"
                st.rerun()
        with _qz_cols[2]:
            if st.button("\U0001F4CA Sinav / Degerlendirme", key="yd_open_sinav_main",
                          use_container_width=True, type="secondary"):
                st.session_state["yd_view"] = "sinav"
                st.rerun()

        # ── KADEME SECİM KARTLARI ──
        st.markdown(
            '<div style="background:linear-gradient(135deg,#131825 0%,#1A2035 50%,#232B3E 100%);padding:18px 22px;'
            'border-radius:14px;margin:16px 0 12px 0;border:1px solid rgba(212,175,55,0.15);">'
            '<div style="font-size:1.1rem;font-weight:800;color:#6366F1;letter-spacing:.3px;">'
            '\U0001F393 Kademe Secimi</div>'
            '<div style="font-size:.82rem;color:#94A3B8;margin-top:2px;">'
            'Ders icerigine erismek icin kademe seciniz</div></div>',
            unsafe_allow_html=True,
        )
        _kd_cols = st.columns(6)
        _kd_items = [
            ("preschool", "\U0001F392", "Okul Oncesi", "5-6 Yas | Pre-A1"),
            ("primary", "\U0001F4D5", "Ilkokul (1-4)", "A1 \u2014 A1.2 | MEB"),
            ("secondary", "\U0001F4D7", "Ortaokul (5-8)", "A2.1 \u2014 A2.4 | MEB"),
            ("high", "\U0001F4D8", "Lise (9-12)", "B1.1 \u2014 B1.4 | MEB"),
            ("temelden", "\U0001F680", "Temelden Baslama", "5-6. Sinif Yogun | A1\u2192B1.2"),
            ("mufredatli", "\U0001F4D0", "Ingilizce Mufredatli", "1-12. Sinif | Pre-A1\u2192B2"),
        ]
        for _ki, _kd in enumerate(_kd_items):
            with _kd_cols[_ki]:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#131825,#1A2035);'
                    f'border:2px solid rgba(212,175,55,0.2);border-radius:14px;padding:20px 16px;text-align:center;'
                    f'min-height:140px;display:flex;flex-direction:column;justify-content:center;">'
                    f'<div style="font-size:2.2rem;margin-bottom:6px;">{_kd[1]}</div>'
                    f'<div style="font-size:1rem;font-weight:800;color:#6366F1;margin-bottom:4px;">{_kd[2]}</div>'
                    f'<div style="font-size:.75rem;color:#94A3B8;">{_kd[3]}</div></div>',
                    unsafe_allow_html=True,
                )
                if st.button(f"\U0001F4CD {_kd[2]}", key=f"yd_go_{_kd[0]}", use_container_width=True, type="primary"):
                    st.session_state["yd_view"] = _kd[0]
                    st.rerun()

        # ── ARAC KISAYOLLARI (tıkla aç/kapa) ──
        with st.expander("\U0001F6E0 Araclar & Kaynaklar — Tum kademeler icin ortak araclar", expanded=False):
            _tool_items = [
                ("vocab", "\U0001F1EC\U0001F1E7", "Ingilizce Kelime", "#7c3aed"),
                ("odev", "\U0001F4DD", "Odev", "#ea580c"),
                ("sinav", "\U0001F4CA", "Sinav/Degerlendirme", "#0d9488"),
                ("olcme36", "\U0001F4DD", "36 Hafta Olcme", "#be123c"),
                ("yd_quiz", "\U0001F3AF", "Unite Quiz", "#7c3aed"),
                ("srs", "\U0001F504", "SRS Kelime Tekrar", "#2563eb"),
                ("ai_conv", "\U0001F916", "AI Konusma", "#9333ea"),
                ("reading", "\U0001F4D6", "Okuma Kutuphanesi", "#059669"),
                ("kazanimlar", "\U0001F3AF", "Kazanimlar", "#d946ef"),
                ("kazanim_pdf", "\U0001F3AF", "Kazanim PDF Hizli Indirme", "#e11d48"),
                ("games", "\U0001F9E9", "Games & Puzzles", "#f59e0b"),
                ("yd_cockpit", "\U0001F4CA", "Dil Cockpit", "#2563eb"),
                ("yd_konusma", "\U0001F5E3", "AI Konusma", "#10b981"),
                ("yd_cefr_yol", "\U0001F3C6", "CEFR Yol Haritasi", "#8b5cf6"),
            ]
            _t_rows = [_tool_items[i:i+4] for i in range(0, len(_tool_items), 4)]
            for _trow in _t_rows:
                _tcols = st.columns(4)
                for _ti, _tc in enumerate(_trow):
                    with _tcols[_ti]:
                        if st.button(f"{_tc[1]} {_tc[2]}", key=f"yd_tool_{_tc[0]}", use_container_width=True):
                            st.session_state["yd_view"] = _tc[0]
                            st.rerun()

        # ── MODÜL DERS KİTAPLARI (tıkla aç/kapa) ──
        with st.expander("\U0001F4DA Modul Ders Kitaplari — Basili kitaplar, okuma kaynaklari ve kelime calismalari", expanded=False):
            _book_items = [
                ("main_course", "\U0001F4D8", "Main Course Book", "#1d4ed8"),
                ("basili_kitap", "\U0001F4D5", "English Workbook", "#b45309"),
                ("read_book", "\U0001F4D6", "Read Book", "#0369a1"),
                ("vocabulary", "\U0001F4DD", "Vocabulary", "#16a34a"),
            ]
            _bk_cols = st.columns(4)
            for _bi, _bk in enumerate(_book_items):
                with _bk_cols[_bi]:
                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,#131825,#1A2035);'
                        f'border:2px solid {_bk[3]}40;border-radius:14px;padding:20px 16px;text-align:center;'
                        f'min-height:100px;display:flex;flex-direction:column;justify-content:center;">'
                        f'<div style="font-size:2rem;margin-bottom:6px;">{_bk[1]}</div>'
                        f'<div style="font-size:0.95rem;font-weight:700;color:{_bk[3]};">{_bk[2]}</div></div>',
                        unsafe_allow_html=True,
                    )
                    if st.button(f"\U0001F4CD {_bk[2]}", key=f"yd_book_{_bk[0]}", use_container_width=True, type="primary"):
                        st.session_state["yd_view"] = _bk[0]
                        st.rerun()

        # ── PDF KİTAP ÜRETİCİ (tıkla aç/kapa) ──
        with st.expander("\U0001F4C4 PDF Kitap Uretici — Sinif Bazli | Unite uyumlu, baski hazir PDF kitaplar", expanded=False):
            _pdf_grade_sel = st.selectbox("Sinif Secin", [
                "Okul Oncesi", "1. Sinif", "2. Sinif", "3. Sinif", "4. Sinif",
                "5. Sinif", "6. Sinif", "7. Sinif", "8. Sinif",
                "9. Sinif", "10. Sinif", "11. Sinif", "12. Sinif",
            ], key="yd_pdf_book_grade")
            _pdf_grade_map = {"Okul Oncesi": (0, "preschool"), "1. Sinif": (1, "grade1"),
                "2. Sinif": (2, "grade2"), "3. Sinif": (3, "grade3"), "4. Sinif": (4, "grade4"),
                "5. Sinif": (5, "grade5"), "6. Sinif": (6, "grade6"), "7. Sinif": (7, "grade7"),
                "8. Sinif": (8, "grade8"), "9. Sinif": (9, "grade9"), "10. Sinif": (10, "grade10"),
                "11. Sinif": (11, "grade11"), "12. Sinif": (12, "grade12")}
            _pg_num, _pg_key = _pdf_grade_map[_pdf_grade_sel]

            _pb_cols = st.columns(4)
            _pdf_books = [
                ("basic_main", "\U0001F4D8", "Basic Main Course"),
                ("workbook", "\U0001F4D5", "English Workbook"),
                ("reading", "\U0001F4D6", "Read Book"),
                ("vocab_book", "\U0001F4DD", "Vocabulary"),
            ]
            # Eski session cache temizle (yeni premium engine ile uyumsuz)
            for _pb in _pdf_books:
                _old_key = f"_yd_pdfbook_{_pb[0]}_{_pg_key}"
                _old_data = st.session_state.get(_old_key)
                if _old_data and len(_old_data) < 200_000:
                    del st.session_state[_old_key]

            for _pbi, _pb in enumerate(_pdf_books):
                with _pb_cols[_pbi]:
                    if st.button(f"{_pb[1]} {_pb[2]}", key=f"yd_pdfbook_{_pb[0]}_{_pg_key}", use_container_width=True):
                        with st.spinner(f"{_pdf_grade_sel} — {_pb[2]} PDF olusturuluyor... (200+ sayfa, biraz bekleyin)"):
                            try:
                                from views.book_pdf_engine import (
                                    generate_basic_main_course_pdf, generate_workbook_pdf,
                                    generate_reading_book_pdf, generate_vocabulary_book_pdf,
                                )
                                from views.yd_content import _CURRICULUM
                                _cur = _CURRICULUM.get(_pg_key, [])
                                if _pb[0] == "basic_main":
                                    _pdf = generate_basic_main_course_pdf(_pg_num, _cur)
                                elif _pb[0] == "workbook":
                                    _pdf = generate_workbook_pdf(_pg_num, _cur)
                                elif _pb[0] == "reading":
                                    _pdf = generate_reading_book_pdf(_pg_num, _cur)
                                else:
                                    _pdf = generate_vocabulary_book_pdf(_pg_num, _cur)
                                if _pdf:
                                    st.session_state[f"_yd_pdfbook_{_pb[0]}_{_pg_key}"] = _pdf
                                    _page_count = len(_pdf) // 2500
                                    st.success(f"PDF hazır — {len(_pdf)//1024} KB (~{_page_count} sayfa)")
                                else:
                                    st.error("PDF oluşturulamadı.")
                            except Exception as _pbe:
                                import traceback
                                traceback.print_exc()
                                st.error(f"Hata: {_pbe}")

            # İndirme butonları
            for _pb in _pdf_books:
                _pd = st.session_state.get(f"_yd_pdfbook_{_pb[0]}_{_pg_key}")
                if _pd:
                    st.download_button(
                        f"\u2B07 {_pdf_grade_sel} — {_pb[2]} PDF Indir ({len(_pd)//1024} KB)",
                        data=_pd,
                        file_name=f"{_pb[0]}_{_pg_key}.pdf",
                        mime="application/pdf",
                        key=f"yd_dl_pdfbook_{_pb[0]}_{_pg_key}",
                        use_container_width=True,
                    )

        # ── PLAN KİTAPLARI (tıkla aç/kapa) ──
        with st.expander("\U0001F4CB Plan Kitaplari — Ders planlari ve etkinlik kitaplari olusturma araclari", expanded=False):
            _plan_items = [
                ("ibook", "\U0001F4D6", "Interaktif Etkinlik Kitabi", "#e11d48"),
                ("plan", "\U0001F4CB", "Plan & Etkinlik Olusturma", "#0891b2"),
                ("plan_pdf", "\U0001F4C4", "Ders Plani PDF", "#6366f1"),
                ("activity_pdf", "\U0001F3AF", "Etkinlik Kitabi PDF", "#dc2626"),
            ]
            _pk_cols = st.columns(4)
            for _pi, _pk in enumerate(_plan_items):
                with _pk_cols[_pi]:
                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,#131825,#1A2035);'
                        f'border:2px solid {_pk[3]}40;border-radius:14px;padding:20px 16px;text-align:center;'
                        f'min-height:100px;display:flex;flex-direction:column;justify-content:center;">'
                        f'<div style="font-size:2rem;margin-bottom:6px;">{_pk[1]}</div>'
                        f'<div style="font-size:0.85rem;font-weight:700;color:{_pk[3]};">{_pk[2]}</div>'
                        f'<div style="font-size:0.65rem;color:#94A3B8;margin-top:4px;">#{_pi+1} olusturulan</div></div>',
                        unsafe_allow_html=True,
                    )
                    if st.button(f"\U0001F4CD {_pk[2]}", key=f"yd_plan_{_pk[0]}", use_container_width=True, type="primary"):
                        st.session_state["yd_view"] = _pk[0]
                        st.rerun()

        # ── SON PLANLAR — 36 Haftalık Full PDF (tıkla aç/kapa) ──
        with st.expander("\U0001F4C4 Son Planlar — 36 Haftalik Full PDF | 4+4+2 modeli — Sinif bazli tam yillik plan", expanded=False):
            _plan_grades = {
                "Okul Oncesi": ("preschool", "Pre-A1"),
                "1. Sinif — Bright Start 1": ("grade1", "A1"),
                "2. Sinif — Bright Start 2": ("grade2", "A1"),
                "3. Sinif — Bright Start 3": ("grade3", "A1"),
                "4. Sinif — Bright Start 4": ("grade4", "A1.2"),
                "5. Sinif — Next Level 5": ("grade5", "A2.1"),
                "6. Sinif — Next Level 6": ("grade6", "A2.2"),
                "7. Sinif — Next Level 7": ("grade7", "A2.3"),
                "8. Sinif — Next Level 8": ("grade8", "A2.4"),
                "9. Sinif — English Core 9": ("grade9", "B1.1"),
                "10. Sinif — English Core 10": ("grade10", "B1.2"),
                "11. Sinif — English Core 11": ("grade11", "B1.3"),
                "12. Sinif — English Core 12": ("grade12", "B1.4"),
            }

            _sp_cols = st.columns(4)
            for _si, (_slabel, (_skey, _scefr)) in enumerate(_plan_grades.items()):
                with _sp_cols[_si % 4]:
                    if st.button(f"\U0001F4E5 {_slabel}", key=f"yd_fullplan_{_skey}", use_container_width=True):
                        with st.spinner(f"{_slabel} — 36 haftalik PDF olusturuluyor..."):
                            try:
                                from views._gen_weekly_plan_pdf import generate_weekly_plan_pdf
                                _pdf_bytes = generate_weekly_plan_pdf(_skey, 1, 36)
                                st.session_state[f"_yd_fullplan_pdf_{_skey}"] = _pdf_bytes
                                st.session_state[f"_yd_fullplan_label_{_skey}"] = _slabel
                            except Exception as _pe:
                                st.error(f"PDF olusturulamadi: {_pe}")

            # Üretilen PDF'leri göster
            for _skey in [v[0] for v in _plan_grades.values()]:
                _pdf_data = st.session_state.get(f"_yd_fullplan_pdf_{_skey}")
                if _pdf_data:
                    _pdf_label = st.session_state.get(f"_yd_fullplan_label_{_skey}", _skey)
                    st.download_button(
                        f"\u2B07 {_pdf_label} — 36 Hafta PDF Indir",
                        data=_pdf_data,
                        file_name=f"yillik_plan_{_skey}_36hafta.pdf",
                        mime="application/pdf",
                        key=f"yd_dl_fullplan_{_skey}",
                        use_container_width=True,
                    )

        # ── SON GÜNLÜK PLAN — Detaylı İnteraktif Ders Planı (tıkla aç/kapa) ──
        with st.expander("\U0001F4CB Detayli Interaktif Ders Plani (40+40 dk) — 36 hafta x 5 gun = 180 gun", expanded=False):
            _dg_grades = {
                "Okul Oncesi": "preschool",
                "1. Sinif": "grade1",
                "2. Sinif": "grade2",
                "3. Sinif": "grade3",
                "4. Sinif": "grade4",
                "5. Sinif": "grade5",
                "6. Sinif": "grade6",
                "7. Sinif": "grade7",
                "8. Sinif": "grade8",
                "9. Sinif": "grade9",
                "10. Sinif": "grade10",
                "11. Sinif": "grade11",
                "12. Sinif": "grade12",
            }

            _dg_cols = st.columns(4)
            for _di, (_dlabel, _dkey) in enumerate(_dg_grades.items()):
                with _dg_cols[_di % 4]:
                    if st.button(f"\U0001F4E5 {_dlabel}", key=f"yd_dailyplan_{_dkey}", use_container_width=True):
                        with st.spinner(f"{_dlabel} — 180 gunluk detayli plan PDF olusturuluyor..."):
                            try:
                                _dp_bytes = _generate_daily_plan_full_pdf(_dkey)
                                if _dp_bytes:
                                    st.session_state[f"_yd_dailyplan_pdf_{_dkey}"] = _dp_bytes
                                    st.session_state[f"_yd_dailyplan_label_{_dkey}"] = _dlabel
                                else:
                                    st.error("PDF olusturulamadi — mufredat verisi bulunamadi.")
                            except Exception as _dpe:
                                st.error(f"PDF olusturulamadi: {_dpe}")

            for _dkey in _dg_grades.values():
                _dp_data = st.session_state.get(f"_yd_dailyplan_pdf_{_dkey}")
                if _dp_data:
                    _dp_label = st.session_state.get(f"_yd_dailyplan_label_{_dkey}", _dkey)
                    st.download_button(
                        f"\u2B07 {_dp_label} — 180 Gun Detayli Plan PDF Indir",
                        data=_dp_data,
                        file_name=f"detayli_gunluk_plan_{_dkey}_36hafta.pdf",
                        mime="application/pdf",
                        key=f"yd_dl_dailyplan_{_dkey}",
                        use_container_width=True,
                    )

    # ══════════════════════════════════════════════════════════════════
    # KADEME GORUNUMLERI — Sadece secili kademe/arac render edilir
    # ══════════════════════════════════════════════════════════════════
    elif _yd_view == "lesson":
        from views.lesson_delivery import render_lesson_delivery
        render_lesson_delivery()

    elif _yd_view == "lesson_pdf":
        from views.lesson_delivery_pdf import render_lesson_pdf_tab
        render_lesson_pdf_tab()

    elif _yd_view == "cefr_exam":
        from views.cefr_exam_ui import render_cefr_exam
        render_cefr_exam()

    elif _yd_view == "cefr_placement":
        from views.cefr_placement_ui import render_cefr_placement
        render_cefr_placement()

    elif _yd_view == "adaptive_hub":
        from views.adaptive_gamified_ui import render_adaptive_gamified
        render_adaptive_gamified()

    elif _yd_view == "preschool":
        from views.yd_content import _render_preschool_view
        _render_preschool_view()

    elif _yd_view == "primary":
        from views.yd_content import _render_primary_view
        _render_primary_view()

    elif _yd_view == "secondary":
        from views.yd_tools import _render_ortaokul_english
        _render_ortaokul_english()
    elif _yd_view == "high":
        from views.yd_tools import _render_lise_english
        _render_lise_english()
    elif _yd_view == "vocab":
        from views.yd_tools import _render_vocab_game
        _render_vocab_game()
    elif _yd_view == "plan":
        from views.yd_tools import _render_plan_etkinlik_olusturma_tab
        _render_plan_etkinlik_olusturma_tab()
    elif _yd_view == "plan_pdf":
        from views.yd_tools import _render_plan_pdf_tab
        _render_plan_pdf_tab()
    elif _yd_view == "activity_pdf":
        from views.yd_tools import _render_activity_pdf_tab
        _render_activity_pdf_tab()
    elif _yd_view == "odev":
        from views.yd_tools import _render_odev_tab
        _render_odev_tab()
    elif _yd_view == "sinav":
        from views.yd_tools import _render_sinav_degerlendirme_tab
        _render_sinav_degerlendirme_tab()
    elif _yd_view == "olcme36":
        from views.yd_tools import _render_olcme_36_hafta_tab
        _render_olcme_36_hafta_tab()
    elif _yd_view == "yd_quiz":
        from views.yd_tools import _render_yd_quiz_tab
        _render_yd_quiz_tab()
    elif _yd_view == "dijital":
        from views.yd_tools import _render_dijital_kaynaklar_tab
        _render_dijital_kaynaklar_tab()
    elif _yd_view == "srs":
        from views.yd_tools import _render_srs_kelime_tab
        _render_srs_kelime_tab()
    elif _yd_view == "ai_conv":
        from views.yd_tools import _render_ai_conversation
        _render_ai_conversation()
    elif _yd_view == "reading":
        # Okuma Kütüphanesi — Spotlight Reading dahil
        _reading_mode = st.radio("", ["📖 Okuma Kaynakları", "📚 Spotlight Reading"], horizontal=True, key="yd_reading_mode")
        if _reading_mode.startswith("📖"):
            from views.yd_tools import _render_reading_library
            _render_reading_library()
        else:
            from views.yd_tools import _render_spotlight_reading_tab
            _render_spotlight_reading_tab()
    elif _yd_view == "main_course":
        _render_main_course_book()
    elif _yd_view == "temelden":
        from views.yd_tools import _render_temelden_baslama
        _render_temelden_baslama()
    elif _yd_view == "mufredatli":
        from views.yd_tools import _render_ingilizce_mufredatli
        _render_ingilizce_mufredatli()
    elif _yd_view == "kazanimlar":
        from views.yd_tools import _render_kazanimlar_tab
        _render_kazanimlar_tab()
    elif _yd_view == "kazanim_pdf":
        _render_kazanim_pdf_view()
    elif _yd_view == "ibook":
        from views.yd_tools import _render_interactive_book_tab
        _render_interactive_book_tab()
    elif _yd_view == "basili_kitap":
        from views.yd_tools import _render_basili_kitap_tab
        _render_basili_kitap_tab()
    elif _yd_view == "read_book":
        from views.yd_tools import _render_read_book_tab
        _render_read_book_tab()
    elif _yd_view == "vocabulary":
        from views.yd_tools import _render_vocabulary_tab
        _render_vocabulary_tab()
    elif _yd_view == "games":
        from views.yd_tools import _render_games_puzzles_tab
        _render_games_puzzles_tab()
    elif _yd_view == "spotlight":
        from views.yd_tools import _render_spotlight_reading_tab
        _render_spotlight_reading_tab()
    elif _yd_view == "yd_cockpit":
        try:
            from views._yd_super_features import render_yd_cockpit
            render_yd_cockpit()
        except Exception as _e:
            st.error(f"Cockpit yuklenemedi: {_e}")
    elif _yd_view == "yd_konusma":
        try:
            from views._yd_super_features import render_yd_konusma_partneri
            render_yd_konusma_partneri()
        except Exception as _e:
            st.error(f"Konusma Partneri yuklenemedi: {_e}")
    elif _yd_view == "yd_cefr_yol":
        try:
            from views._yd_super_features import render_yd_cefr_yol_haritasi
            render_yd_cefr_yol_haritasi()
        except Exception as _e:
            st.error(f"CEFR Yol Haritasi yuklenemedi: {_e}")


# ── Ilerleme Takibi: yd_core.py'dan import edildi ──
# _get_eng_store, _get_eng_student_id, _eng_* fonksiyonlari yd_core'dan gelir


# ── Veli Paneli Ingilizce Sekmesi — public wrapper ──────────────────────────

def _render_veli_etkinlik_section(sinif, sube):
    """Veli Yabanci Dil sekmesinde gunun etkinlik PDF'ini goster + arsiv."""
    from views.yd_tools import _load_eng_gunluk_ozet
    from datetime import date as _date_cls
    _today = _date_cls.today()

    st.markdown(
        '<div style="background:linear-gradient(135deg,#1e3a5f,#2563eb);color:#fff;'
        'padding:12px 16px;border-radius:12px;margin-bottom:10px;text-align:center;">'
        '<h4 style="margin:0;font-size:16px;">\U0001F4C4 Gunun Etkinlik Calisma Kagidi</h4>'
        '<p style="margin:3px 0 0;font-size:11px;opacity:0.85;">'
        'Ogretmenin isledigiplana ait etkinlik PDF</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    _sel_date = st.date_input(
        "\U0001F4C5 Tarih:", value=_today, key="veli_etk_tarih")
    _tarih_str = _sel_date.strftime("%Y-%m-%d")

    ozet = _load_eng_gunluk_ozet(_tarih_str, sinif, sube or "")

    if ozet and ozet.get("etkinlik_pdf_path"):
        pdf_path = ozet["etkinlik_pdf_path"]
        if os.path.exists(pdf_path):
            _tema = ozet.get("theme_tr", "")
            _vocab = ", ".join(ozet.get("vocab", [])[:6])
            st.markdown(
                f'<div style="background:#eff6ff;padding:10px 14px;'
                f'border-radius:10px;margin:8px 0;border:1px solid #93c5fd;">'
                f'<b style="color:#1e40af;">\U0001F3AF Tema:</b> {_tema} &nbsp;|&nbsp; '
                f'<b style="color:#1e40af;">\U0001F4DA Kelimeler:</b> {_vocab}'
                f'</div>',
                unsafe_allow_html=True,
            )
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "\U0001F4E5 Etkinlik PDF Indir",
                    data=f.read(),
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    key=f"veli_etk_dl_{_tarih_str}",
                    use_container_width=True,
                )
            if ozet.get("ogretmen_notu"):
                st.info(f"\U0001F4DD Ogretmen Notu: {ozet['ogretmen_notu']}")
        else:
            st.info("Etkinlik PDF dosyasi bulunamadi.")
    elif ozet and ozet.get("islendi"):
        st.info(f"{_tarih_str} icin plan islendi ancak etkinlik PDF olusturulmamis.")
    else:
        _gun_adi = _sel_date.strftime("%d.%m.%Y")
        st.info(f"{_gun_adi} icin henuz islenmis plan bulunmuyor.")

    st.divider()


def _render_veli_ek_gonderiler(sinif, sube):
    """Veli Yabanci Dil sekmesinde ogretmenin gonderdigi ek materyaller."""
    from views.yd_tools import _load_eng_ek_gonderiler
    st.markdown(
        '<div style="background:linear-gradient(135deg,#0d9488,#14b8a6);color:#fff;'
        'padding:12px 16px;border-radius:12px;margin-bottom:10px;text-align:center;">'
        '<h4 style="margin:0;font-size:16px;">📎 Ek Gonderiler</h4>'
        '<p style="margin:3px 0 0;font-size:11px;opacity:0.85;">'
        'Ogretmenin gonderdigi ek materyaller (dosya ve linkler)</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    all_records = _load_eng_ek_gonderiler()
    filtered = [
        r for r in all_records
        if r.get("sinif") == sinif
        and (not sube or r.get("sube") == sube)
    ]

    if not filtered:
        st.info("Henuz ek gonderi bulunmamaktadir.")
        st.divider()
        return

    # En yeniden eskiye sirala, son 20
    filtered.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    filtered = filtered[:20]

    for idx, rec in enumerate(filtered):
        tarih_raw = rec.get("tarih", rec.get("created_at", "")[:10])
        dosyalar = rec.get("dosyalar", [])
        link = rec.get("link", "")

        dosya_count = len(dosyalar)
        parts = []
        if dosya_count:
            parts.append(f"{dosya_count} dosya")
        if link:
            parts.append("1 link")
        summary = " + ".join(parts) if parts else ""

        with st.expander(f"📅 {tarih_raw} — {summary}", expanded=(idx == 0)):
            # Dosyalar
            for di, d in enumerate(dosyalar):
                d_path = d.get("dosya_yolu", "")
                d_name = d.get("dosya_adi", "dosya")
                d_tur = d.get("tur", "")
                icon = "📄"
                if d_tur in ("jpg", "jpeg", "png", "gif"):
                    icon = "🖼️"
                elif d_tur in ("mp4", "mp3"):
                    icon = "🎬"
                elif d_tur == "pdf":
                    icon = "📕"

                if d_path and os.path.exists(d_path):
                    try:
                        with open(d_path, "rb") as f:
                            st.download_button(
                                f"{icon} {d_name}",
                                data=f.read(),
                                file_name=d_name,
                                mime="application/octet-stream",
                                key=f"veli_ek_dl_{rec.get('id', idx)}_{di}",
                                use_container_width=True,
                            )
                    except Exception:
                        st.text(f"{icon} {d_name} (dosya okunamadi)")
                else:
                    st.text(f"{icon} {d_name} (dosya bulunamadi)")

            # Link
            if link:
                st.link_button(
                    f"🔗 {link[:60]}{'...' if len(link) > 60 else ''}",
                    url=link,
                    use_container_width=True,
                )

    st.divider()


def _render_veli_cefr_placement(sinif, sube):
    """Veli/Ogrenci panelinde CEFR Seviye Tespit sonuclari."""
    try:
        from models.cefr_exam import CEFRPlacementStore, CEFR_LEVELS, CEFR_ORDER

        store = CEFRPlacementStore()
        # Ogrenci ID session'dan
        student_id = st.session_state.get("student_id", "")
        if not student_id:
            return

        results = store.get_student_results(student_id)
        if not results:
            return

        with st.expander("📋 CEFR Seviye Tespit Sonuclari", expanded=True):
            # En son sonuclari donemlere gore grupla
            basi = [r for r in results if r.period == "sene_basi"]
            sonu = [r for r in results if r.period == "sene_sonu"]
            last_basi = max(basi, key=lambda r: r.submitted_at) if basi else None
            last_sonu = max(sonu, key=lambda r: r.submitted_at) if sonu else None

            cols = st.columns(2)

            for i, (label, r) in enumerate([("Sene Basi", last_basi), ("Sene Sonu", last_sonu)]):
                with cols[i]:
                    if r:
                        ci = CEFR_LEVELS.get(r.placed_cefr, {})
                        color = ci.get("color", "#6366f1")
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
                        padding:16px;text-align:center;border:2px solid {color}40;">
                        <div style="color:#94a3b8;font-size:.8rem;margin-bottom:6px;">{label} {r.academic_year}</div>
                        <div style="display:inline-block;border-radius:20px;padding:8px 20px;
                        font-weight:700;font-size:1.3rem;color:#fff;background:{color};">{r.placed_cefr}</div>
                        <div style="color:#c7d2fe;font-size:1rem;font-weight:700;margin-top:8px;">
                        %{r.percentage}</div>
                        <div style="color:#64748b;font-size:.75rem;margin-top:4px;">
                        L:{r.listening_score:.0f} | R:{r.reading_score:.0f} |
                        G:{r.use_of_english_score:.0f} | W:{r.writing_score:.0f}</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background:#131825;border-radius:14px;padding:16px;
                        text-align:center;border:1px dashed #334155;">
                        <div style="color:#94a3b8;font-size:.8rem;">{label}</div>
                        <div style="color:#475569;margin-top:8px;">Henuz sinav yok</div>
                        </div>""", unsafe_allow_html=True)

            # Karsilastirma — eger her ikisi de varsa
            if last_basi and last_sonu:
                delta = round(last_sonu.percentage - last_basi.percentage, 1)
                arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "→")
                delta_cls = "color:#10b981" if delta > 0 else ("color:#ef4444" if delta < 0 else "color:#94a3b8")
                basi_idx = CEFR_ORDER.index(last_basi.placed_cefr) if last_basi.placed_cefr in CEFR_ORDER else 0
                sonu_idx = CEFR_ORDER.index(last_sonu.placed_cefr) if last_sonu.placed_cefr in CEFR_ORDER else 0
                level_change = sonu_idx - basi_idx
                level_text = f"+{level_change} seviye" if level_change > 0 else (f"{level_change} seviye" if level_change < 0 else "Ayni seviye")

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#131825,#1a2035);border-radius:10px;
                padding:12px;text-align:center;margin-top:8px;border:1px solid rgba(99,102,241,.15);">
                <span style="font-weight:700;{delta_cls};font-size:1.1rem;">
                {arrow} {delta:+.1f}% | {level_text}
                </span>
                <span style="color:#64748b;font-size:.8rem;margin-left:8px;">
                {last_basi.placed_cefr} → {last_sonu.placed_cefr}</span>
                </div>""", unsafe_allow_html=True)
    except Exception:
        pass


def _render_veli_cefr_mock_results(sinif, sube):
    """Veli/Ogrenci panelinde CEFR Mock Exam sonuclari."""
    try:
        from models.cefr_exam import CEFRExamStore, CEFRResult, CEFR_LEVELS, GRADE_TO_CEFR

        store = CEFRExamStore()
        student_id = st.session_state.get("student_id", "")
        if not student_id:
            return

        sinif_int = int(sinif) if sinif else 0
        results = store.get_student_results(student_id, grade=sinif_int)
        if not results:
            return

        with st.expander("\U0001F3C6 CEFR Mock Exam Sonuclari", expanded=True):
            st.markdown(
                '<div style="background:linear-gradient(135deg,#312e81,#6d28d9);color:#fff;'
                'padding:14px 18px;border-radius:12px;margin-bottom:10px;text-align:center;">'
                '<h4 style="margin:0;font-size:16px;">CEFR Mock Exam Sonuclari</h4>'
                '<p style="margin:3px 0 0;font-size:12px;opacity:.85;">'
                'Cambridge formatinda sinav performansi</p></div>',
                unsafe_allow_html=True,
            )

            # Son sonuc
            latest = max(results, key=lambda r: r.submitted_at)
            target_cefr = GRADE_TO_CEFR.get(sinif_int, "A2")
            achieved = latest.achieved_cefr or latest.cefr
            ci = CEFR_LEVELS.get(achieved, {})
            color = ci.get("color", "#7c3aed")

            # Seviye karti
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
            padding:18px;text-align:center;border:2px solid {color}40;margin-bottom:10px;">
            <div style="color:#94a3b8;font-size:.8rem;">Tespit Edilen Seviye</div>
            <div style="display:inline-block;border-radius:20px;padding:8px 24px;
            font-weight:800;font-size:1.5rem;color:#fff;background:{color};margin:8px 0;">
            {achieved}</div>
            <div style="color:#c7d2fe;font-size:1.1rem;font-weight:700;">%{latest.percentage:.0f}</div>
            <div style="color:#64748b;font-size:.78rem;margin-top:6px;">
            Hedef: {target_cefr} | Sonraki: {latest.next_cefr or "-"}</div>
            </div>""", unsafe_allow_html=True)

            # Beceri kirilimi
            skills = [
                ("Listening", latest.listening_score, latest.listening_max),
                ("Reading", latest.reading_score, latest.reading_max),
                ("Writing", latest.writing_score, latest.writing_max),
                ("Speaking", latest.speaking_score, latest.speaking_max),
            ]
            sk_cols = st.columns(4)
            for i, (sk_name, sk_score, sk_max) in enumerate(skills):
                pct = round(sk_score / sk_max * 100) if sk_max > 0 else 0
                sk_clr = "#22c55e" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
                with sk_cols[i]:
                    st.markdown(f"""
                    <div style="background:#131825;border-radius:10px;padding:10px;text-align:center;
                    border:1px solid {sk_clr}30;">
                    <div style="font-size:.75rem;color:#94a3b8;">{sk_name}</div>
                    <div style="font-size:1.1rem;font-weight:700;color:{sk_clr};">%{pct}</div>
                    <div style="background:rgba(99,102,241,.1);border-radius:4px;height:6px;margin-top:4px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{sk_clr};border-radius:4px;"></div>
                    </div></div>""", unsafe_allow_html=True)

            # Skill breakdown
            if latest.skill_breakdown:
                st.markdown("**Detay Beceri Analizi:**")
                sk_labels = {"vocabulary": "Kelime", "grammar": "Dilbilgisi",
                             "comprehension": "Anlama", "inference": "Cikarim"}
                for sk, val in latest.skill_breakdown.items():
                    v = float(val) if val else 0
                    c = "#22c55e" if v >= 70 else "#f59e0b" if v >= 50 else "#ef4444"
                    st.markdown(
                        f'<div style="display:flex;justify-content:space-between;padding:3px 0;">'
                        f'<span style="color:#cbd5e1;font-size:.85rem;">{sk_labels.get(sk, sk.title())}</span>'
                        f'<span style="color:{c};font-weight:700;font-size:.85rem;">%{v:.0f}</span></div>',
                        unsafe_allow_html=True,
                    )

            # Gecmis sinavlar (birden fazla varsa)
            if len(results) > 1:
                st.markdown("---")
                st.markdown("**Gecmis Sinavlar:**")
                for r in sorted(results, key=lambda x: x.submitted_at, reverse=True):
                    ach = r.achieved_cefr or r.cefr
                    rc = CEFR_LEVELS.get(ach, {}).get("color", "#64748b")
                    st.markdown(
                        f'<div style="background:#0f172a;border-left:3px solid {rc};'
                        f'padding:6px 12px;border-radius:4px;margin:3px 0;font-size:.82rem;">'
                        f'<b style="color:{rc};">{ach}</b> — %{r.percentage:.0f} | '
                        f'L:{r.listening_score:.0f} R:{r.reading_score:.0f} '
                        f'W:{r.writing_score:.0f} S:{r.speaking_score:.0f} | '
                        f'{r.submitted_at[:10]}</div>',
                        unsafe_allow_html=True,
                    )
    except Exception:
        pass


def _render_veli_ilerleme_raporu(sinif, sube):
    """Veli ekraninda Yabanci Dil ilerleme raporu — placement, speaking, writing ozeti."""
    import os as _os

    # Veri yukle
    _pt_data = []
    _pt_path = _os.path.join("data", "english", "placement_tests.json")
    if _os.path.exists(_pt_path):
        try:
            with open(_pt_path, "r", encoding="utf-8") as f:
                _pt_data = json.load(f)
        except Exception as _exc:
            _logger.debug('Suppressed: %s', _exc)

    _spk_data = []
    _spk_path = _os.path.join("data", "english", "speaking_records.json")
    if _os.path.exists(_spk_path):
        try:
            with open(_spk_path, "r", encoding="utf-8") as f:
                _spk_data = json.load(f)
        except Exception as _exc:
            _logger.debug('Suppressed: %s', _exc)

    _wr_data = []
    _wr_path = _os.path.join("data", "english", "writing_records.json")
    if _os.path.exists(_wr_path):
        try:
            with open(_wr_path, "r", encoding="utf-8") as f:
                _wr_data = json.load(f)
        except Exception as _exc:
            _logger.debug('Suppressed: %s', _exc)

    # Sinif/sube filtrele
    if sinif:
        _pt_data = [r for r in _pt_data if r.get("sinif") == sinif]
        _spk_data = [r for r in _spk_data if r.get("sinif") == sinif]
        _wr_data = [r for r in _wr_data if r.get("sinif") == sinif]
        if sube:
            _pt_data = [r for r in _pt_data if r.get("sube") == sube]
            _spk_data = [r for r in _spk_data if r.get("sube") == sube]
            _wr_data = [r for r in _wr_data if r.get("sube") == sube]

    # Hicbir veri yoksa gosterme
    if not _pt_data and not _spk_data and not _wr_data:
        return

    st.markdown(
        '<div style="background:linear-gradient(135deg,#1e3a5f,#2563eb);color:#fff;'
        'padding:14px 18px;border-radius:12px;margin-bottom:12px;">'
        '<div style="font-size:1.1rem;font-weight:700;">📈 Yabanci Dil Ilerleme Raporu</div>'
        '<div style="font-size:0.82rem;opacity:.8;">Seviye, konusma ve yazma becerilerinin ozeti</div>'
        '</div>', unsafe_allow_html=True,
    )

    # Placement sonucu
    if _pt_data:
        latest_pt = sorted(_pt_data, key=lambda x: x.get("created_at", ""), reverse=True)[0]
        cefr = latest_pt.get("final_cefr", latest_pt.get("assigned_cefr", "—"))
        score = latest_pt.get("total_score", 0)
        sl = latest_pt.get("score_by_level", {})
        cefr_color = {"A1": "#22c55e", "A2": "#3b82f6", "B1": "#f59e0b", "B2": "#ef4444"}.get(cefr, "#6b7280")

        st.markdown(
            f'<div style="background:{cefr_color}10;border:1px solid {cefr_color}33;'
            f'border-radius:10px;padding:12px 16px;margin-bottom:10px;">'
            f'<div style="font-size:0.85rem;font-weight:600;">🎯 Seviye Belirleme Sonucu</div>'
            f'<div style="display:flex;gap:16px;align-items:center;margin-top:6px;">'
            f'<div style="font-size:2rem;font-weight:800;color:{cefr_color};">{cefr}</div>'
            f'<div style="font-size:0.85rem;color:#6b7280;">'
            f'Genel: {score}% | A1: {sl.get("A1", 0)}% | A2: {sl.get("A2", 0)}% | '
            f'B1: {sl.get("B1", 0)}% | B2: {sl.get("B2", 0)}%</div>'
            f'</div></div>', unsafe_allow_html=True,
        )

    # Speaking ozeti
    if _spk_data:
        latest_spk = sorted(_spk_data, key=lambda x: x.get("created_at", ""), reverse=True)[:3]
        avg_pct = round(sum(r.get("percentage", 0) for r in latest_spk) / len(latest_spk), 1)
        spk_color = "#22c55e" if avg_pct >= 70 else ("#f59e0b" if avg_pct >= 50 else "#ef4444")

        st.markdown(
            f'<div style="background:{spk_color}10;border:1px solid {spk_color}33;'
            f'border-radius:10px;padding:12px 16px;margin-bottom:10px;">'
            f'<div style="font-size:0.85rem;font-weight:600;">🗣️ Konusma Becerisi (son {len(latest_spk)} kayit)</div>'
            f'<div style="font-size:1.5rem;font-weight:700;color:{spk_color};margin-top:4px;">{avg_pct}%</div>'
            f'<div style="font-size:0.8rem;color:#6b7280;">', unsafe_allow_html=True,
        )
        for r in latest_spk:
            st.markdown(
                f'<span style="font-size:0.8rem;">📌 {r.get("task_title", "Gorev")} — {r.get("percentage", 0)}% '
                f'({r.get("cefr_speaking_level", "")}) | {r.get("created_at", "")[:10]}</span><br>',
                unsafe_allow_html=True,
            )
        st.markdown('</div></div>', unsafe_allow_html=True)

    # Writing ozeti
    if _wr_data:
        latest_wr = sorted(_wr_data, key=lambda x: x.get("created_at", ""), reverse=True)[:3]
        avg_pct_w = round(sum(r.get("percentage", 0) for r in latest_wr) / len(latest_wr), 1)
        wr_color = "#22c55e" if avg_pct_w >= 70 else ("#f59e0b" if avg_pct_w >= 50 else "#ef4444")

        st.markdown(
            f'<div style="background:{wr_color}10;border:1px solid {wr_color}33;'
            f'border-radius:10px;padding:12px 16px;margin-bottom:10px;">'
            f'<div style="font-size:0.85rem;font-weight:600;">✍️ Yazma Becerisi (son {len(latest_wr)} kayit)</div>'
            f'<div style="font-size:1.5rem;font-weight:700;color:{wr_color};margin-top:4px;">{avg_pct_w}%</div>'
            f'<div style="font-size:0.8rem;color:#6b7280;">', unsafe_allow_html=True,
        )
        for r in latest_wr:
            st.markdown(
                f'<span style="font-size:0.8rem;">📝 {r.get("task_title", "Gorev")} — {r.get("percentage", 0)}% '
                f'({r.get("word_count", 0)} kelime) | {r.get("created_at", "")[:10]}</span><br>',
                unsafe_allow_html=True,
            )
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.divider()


def _render_veli_yd_ozet(sinif, sube):
    """Veli ekraninda Yabanci Dil islenen konular ozeti."""
    from views.yd_tools import _load_eng_gunluk_ozet
    from datetime import date as _vd, timedelta as _vtd

    st.markdown(
        '<div style="background:linear-gradient(135deg,#059669,#10b981);color:#fff;'
        'padding:12px 16px;border-radius:12px;margin-bottom:10px;text-align:center;">'
        '<h4 style="margin:0;font-size:16px;">Yabanci Dil Ozeti</h4>'
        '<p style="margin:3px 0 0;font-size:11px;opacity:0.85;">'
        'Ogretmenin isledigi konularin ozeti</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    _today = _vd.today()
    # Son 7 gunun ozetlerini goster
    _ozetler = []
    for _d in range(7):
        _t = _today - _vtd(days=_d)
        _oz = _load_eng_gunluk_ozet(_t.isoformat(), sinif, sube or "")
        if _oz and _oz.get("islendi"):
            _oz["_display_date"] = _t.strftime("%d.%m.%Y")
            _oz["_day_name"] = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"][_t.weekday()]
            _ozetler.append(_oz)

    if not _ozetler:
        st.info("Son 7 gunde islenmis ders bulunmuyor.")
    else:
        for oz in _ozetler:
            _islenen = oz.get("islenen_dersler", [])
            _pct = oz.get("pct", 0)
            _pct_clr = "#059669" if _pct == 100 else ("#f59e0b" if _pct >= 50 else "#ef4444")
            _vocab = ", ".join(oz.get("vocab", [])[:6])
            _ders_list = " | ".join([d.get("focus", "") for d in _islenen[:4]])

            st.markdown(
                f'<div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:10px;'
                f'padding:10px 14px;margin-bottom:8px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-weight:700;color:#059669;font-size:.82rem;">'
                f'{oz["_day_name"]} — {oz["_display_date"]}</span>'
                f'<span style="font-weight:800;color:{_pct_clr};font-size:.82rem;">%{_pct}</span>'
                f'</div>'
                f'<div style="font-weight:600;color:#94A3B8;font-size:.78rem;margin-top:4px;">'
                f'Hafta {oz.get("hafta", "")}: {oz.get("theme_tr", "")}</div>'
                f'<div style="font-size:.7rem;color:#475569;margin-top:3px;">'
                f'Islenen: {_ders_list}</div>'
                + (f'<div style="font-size:.68rem;color:#94a3b8;margin-top:2px;">'
                   f'Kelimeler: {_vocab}</div>' if _vocab else '')
                + f'</div>',
                unsafe_allow_html=True,
            )

    st.divider()


def _render_veli_dijital_odev(sinif, sube):
    """Veli/ogrenci ekraninda dijital etkinlikler — kitapta olmayan, evde tekrar edilecek aktiviteler."""
    from views.yd_content import _CURRICULUM
    from views.yd_tools import _generate_detailed_daily_plan, _DIGITAL_ONLY_BTNS, _BTN_LABELS_TR
    from datetime import date as _d_dij, timedelta as _td_dij

    _today = _d_dij.today()
    _day_keys = ["mon", "tue", "wed", "thu", "fri"]
    _dow = min(_today.weekday(), 4)
    _day_key = _day_keys[_dow]

    # Sinif seviyesini belirle
    _sinif_int = 0
    try:
        _sinif_int = int(str(sinif).replace(". Sinif", "").replace("Okul Oncesi", "0").strip())
    except Exception:
        return

    _level = f"grade{_sinif_int}" if _sinif_int > 0 else "preschool"
    _curriculum = _CURRICULUM.get(_level, [])
    if not _curriculum:
        return

    # Bugunku haftayi bul
    _yr = _today.year if _today.month >= 9 else _today.year - 1
    _sep1 = _d_dij(_yr, 9, 1)
    _dtm = (7 - _sep1.weekday()) % 7
    _fm = _sep1 + _td_dij(days=_dtm) if _sep1.weekday() != 0 else _sep1
    _acad = _fm + _td_dij(weeks=1)
    _diff = (_today - _acad).days
    _wk = max(1, min((_diff // 7 + 1 if _diff >= 0 else 1), len(_curriculum)))

    _week_data = None
    for w in _curriculum:
        if w["week"] == _wk:
            _week_data = w
            break
    if not _week_data:
        return

    _plan = _generate_detailed_daily_plan(_level, _week_data, _day_key)
    if not _plan:
        return

    # Dijital aktiviteleri topla
    _digital_acts = []
    for act in _plan.get("lesson_1", []) + _plan.get("lesson_2", []):
        _bt = act.get("btn_type")
        if _bt and _bt in _DIGITAL_ONLY_BTNS:
            _label = _BTN_LABELS_TR.get(_bt, _bt)
            _digital_acts.append({"btn_type": _bt, "label": _label, "title": act["title"]})

    if not _digital_acts:
        return

    _gun_tr = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"][_dow]
    _theme = _week_data.get("theme_tr", _week_data.get("theme", ""))

    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed,#a855f7);color:#fff;'
        'padding:14px 18px;border-radius:12px;margin-bottom:12px;">'
        '<div style="font-size:1.1rem;font-weight:700;">'
        '\U0001F4BB Evde Tekrar Edilecek Dijital Etkinlikler</div>'
        '<div style="font-size:0.82rem;opacity:.8;">'
        'Kitapta olmayan interaktif calismalar — modulden acarak tekrar edin</div>'
        '</div>', unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="font-size:.78rem;color:#6b7280;margin-bottom:8px;">'
        f'{_gun_tr} — Hafta {_wk}: {_theme}</div>',
        unsafe_allow_html=True,
    )

    for da in _digital_acts:
        st.markdown(
            f'<div style="background:#faf5ff;border:2px solid #c4b5fd;border-radius:10px;'
            f'padding:10px 14px;margin-bottom:8px;display:flex;align-items:center;gap:10px;">'
            f'<div style="font-size:1.4rem;">\U0001F4BB</div>'
            f'<div>'
            f'<div style="font-weight:700;color:#7c3aed;font-size:.85rem;">{da["label"]}</div>'
            f'<div style="font-size:.73rem;color:#475569;">{da["title"]}</div>'
            f'<div style="font-size:.65rem;color:#a855f7;margin-top:3px;">'
            f'\U0001F449 Yabanci Dil modulunden {da["label"]} sekmesini acin</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    st.divider()


def _generate_hw_quiz(hw_item: dict, week_data: dict, level: str) -> list:
    """Odev tipine gore otomatik quiz sorulari uretir.

    Her soru: {"q": str, "choices": [str], "answer": int, "explanation": str}
    """
    import random as _rng
    hw_type = hw_item.get("type", "")
    vocab = week_data.get("vocab", [])
    theme = week_data.get("theme", "")
    theme_tr = week_data.get("theme_tr", "")
    grammar = week_data.get("grammar_focus", "")
    questions = []

    if hw_type == "vocabulary" and vocab:
        # Kelime-anlam eslestirme sorulari
        _tr_map = {
            "hello": "merhaba", "goodbye": "hosca kal", "cat": "kedi", "dog": "kopek",
            "bird": "kus", "fish": "balik", "red": "kirmizi", "blue": "mavi",
            "green": "yesil", "yellow": "sari", "big": "buyuk", "small": "kucuk",
            "happy": "mutlu", "sad": "uzgun", "water": "su", "milk": "sut",
            "apple": "elma", "book": "kitap", "school": "okul", "house": "ev",
            "mother": "anne", "father": "baba", "friend": "arkadas", "teacher": "ogretmen",
            "one": "bir", "two": "iki", "three": "uc", "four": "dort", "five": "bes",
            "sun": "gunes", "moon": "ay", "star": "yildiz", "tree": "agac",
            "car": "araba", "bus": "otobus", "food": "yiyecek", "ball": "top",
        }
        _pool = [w for w in vocab if w.lower() in _tr_map]
        if len(_pool) < 3:
            _pool = vocab[:6]

        for w in _pool[:5]:
            w_low = w.lower()
            correct_tr = _tr_map.get(w_low, f"{w} (anlami)")
            distractors = [v for k, v in _tr_map.items() if k != w_low]
            _rng.shuffle(distractors)
            choices = [correct_tr] + distractors[:3]
            _rng.shuffle(choices)
            questions.append({
                "q": f"'{w}' kelimesinin Turkce anlami nedir?",
                "choices": choices,
                "answer": choices.index(correct_tr),
                "explanation": f"'{w}' = '{correct_tr}'",
            })

    elif hw_type == "grammar" and grammar:
        # Gramer bosluk doldurma
        _grammar_qs = {
            "am / is / are": [
                {"q": "I ___ a student.", "choices": ["am", "is", "are", "be"], "answer": 0,
                 "explanation": "I + am"},
                {"q": "She ___ happy.", "choices": ["am", "is", "are", "be"], "answer": 1,
                 "explanation": "She + is"},
                {"q": "They ___ friends.", "choices": ["am", "is", "are", "be"], "answer": 2,
                 "explanation": "They + are"},
                {"q": "He ___ a teacher.", "choices": ["am", "is", "are", "be"], "answer": 1,
                 "explanation": "He + is"},
                {"q": "We ___ students.", "choices": ["am", "is", "are", "be"], "answer": 2,
                 "explanation": "We + are"},
            ],
            "have / has": [
                {"q": "I ___ a cat.", "choices": ["have", "has", "had", "having"], "answer": 0,
                 "explanation": "I + have"},
                {"q": "She ___ a dog.", "choices": ["have", "has", "had", "having"], "answer": 1,
                 "explanation": "She + has"},
                {"q": "They ___ two cars.", "choices": ["have", "has", "had", "having"], "answer": 0,
                 "explanation": "They + have"},
            ],
            "can / can't": [
                {"q": "I ___ swim.", "choices": ["can", "can't", "cans", "canning"], "answer": 0,
                 "explanation": "can + fiil"},
                {"q": "She ___ fly. (X)", "choices": ["can", "can't", "cans", "does"], "answer": 1,
                 "explanation": "olumsuz: can't"},
            ],
        }
        # En yakin eslesen gramer konusu bul
        for gk, gqs in _grammar_qs.items():
            if gk.lower() in grammar.lower() or grammar.lower() in gk.lower():
                questions = gqs[:5]
                break
        if not questions:
            # Varsayilan am/is/are
            questions = _grammar_qs.get("am / is / are", [])[:5]

    elif hw_type == "listening":
        # Dinleme - cumle tamamlama
        questions = [
            {"q": f"'{theme}' konusunda dinleme yapildi. Dinledigini anladigini goster: "
                  f"Bu unite hangi konuyla ilgili?",
             "choices": [theme_tr, "Matematik", "Spor", "Muzik"],
             "answer": 0, "explanation": f"Bu unitenin konusu: {theme_tr}"},
            {"q": f"Bu haftanin kelimelerinden biri hangisidir?",
             "choices": ([vocab[0]] if vocab else ["kelime"]) +
                        ["television", "computer", "airplane"],
             "answer": 0,
             "explanation": f"Bu haftanin kelimeleri: {', '.join(vocab[:4])}"},
        ]

    elif hw_type == "reading":
        questions = [
            {"q": f"'{theme}' konusundaki okuma parcasinin ana fikri nedir?",
             "choices": [f"{theme_tr} hakkinda bilgi", "Yemek tarifleri",
                        "Uzay yolculugu", "Tarih dersi"],
             "answer": 0, "explanation": f"Parcanin konusu: {theme_tr}"},
        ]

    elif hw_type == "functional":
        questions = [
            {"q": "Birine 'Nasilsin?' diye sormak icin ne dersiniz?",
             "choices": ["How are you?", "Where are you?",
                        "What are you?", "Who are you?"],
             "answer": 0, "explanation": "How are you? = Nasilsin?"},
            {"q": "Birinden bir sey rica ederken ne dersiniz?",
             "choices": ["Can I have...?", "I don't want...",
                        "Go away!", "No thanks."],
             "answer": 0, "explanation": "Can I have...? = Alabilir miyim?"},
        ]

    elif hw_type == "pronunciation":
        questions = [
            {"q": f"Bu haftanin kelimelerinden '{vocab[0] if vocab else 'hello'}' "
                  f"kac heceden olusur?",
             "choices": ["1", "2", "3", "4"],
             "answer": 1 if vocab and len(vocab[0]) > 4 else 0,
             "explanation": "Kelimenin hece sayisini belirlemek icin sesli harflere bak."},
        ]

    elif hw_type in ("coursebook", "destek_kitap", "library"):
        # Genel icerik sorusu
        questions = [
            {"q": f"Bu haftanin konusu '{theme_tr}'. "
                  f"Asagidakilerden hangisi bu konuyla ilgilidir?",
             "choices": ([vocab[0] if vocab else theme_tr] +
                        ["penguin", "volcano", "algebra"]),
             "answer": 0,
             "explanation": f"Bu haftanin konusu: {theme_tr}, kelimeler: {', '.join(vocab[:3])}"},
        ]

    # En az 1, en fazla 5 soru
    return questions[:5]


def _get_hw_teslim_key(odev_id: str, student_key: str) -> str:
    """Odev teslim durumunu session + dosyada takip icin key uret."""
    return f"yd_hw_teslim_{odev_id}_{student_key}"


def _load_yd_hw_submissions() -> list:
    """YD odev teslim kayitlarini yukle."""
    _path = os.path.join(get_tenant_dir(), "dijital_kutuphane", "yd_hw_submissions.json")
    if os.path.exists(_path):
        try:
            with open(_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def _save_yd_hw_submission(submission: dict):
    """YD odev teslim kaydini kaydet."""
    _path = os.path.join(get_tenant_dir(), "dijital_kutuphane", "yd_hw_submissions.json")
    os.makedirs(os.path.dirname(_path), exist_ok=True)
    records = _load_yd_hw_submissions()
    # Upsert by odev_id + student_key
    _key = (submission.get("odev_id"), submission.get("student_key"))
    found = False
    for i, r in enumerate(records):
        if (r.get("odev_id"), r.get("student_key")) == _key:
            records[i] = submission
            found = True
            break
    if not found:
        records.append(submission)
    with open(_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def _render_veli_yd_odevler(sinif, sube):
    """Veli/ogrenci ekraninda Yabanci Dil odevleri — quiz coz + geri gonder + sonuc gor."""
    from views.yd_content import _CURRICULUM
    from views.yd_tools import _get_akademik_store, _load_yd_odevler
    from datetime import date as _vd2

    st.markdown(
        '<div style="background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;'
        'padding:14px 18px;border-radius:12px;margin-bottom:12px;text-align:center;">'
        '<h4 style="margin:0;font-size:17px;">\U0001F4DA Yabanci Dil Odevleri</h4>'
        '<p style="margin:3px 0 0;font-size:11px;opacity:0.85;">'
        'Odevini coz, geri gonder — sistem otomatik degerlendirir</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Student key for submission tracking
    _auth = st.session_state.get("auth_user", {})
    _student_key = _auth.get("username", f"stu_{sinif}_{sube}")

    # Odevleri yukle (akademik store + legacy)
    _odevler_ak = []
    try:
        _ak_store = _get_akademik_store()
        _odevler_ak = _ak_store.get_odevler(sinif=sinif, sube=sube, ders="Ingilizce", durum="aktif")
    except Exception:
        pass

    _all_legacy = _load_yd_odevler()
    _today = _vd2.today()

    # Legacy odevleri de ekle
    _legacy_filtered = [
        o for o in _all_legacy
        if str(o.get("sinif", "")) == str(sinif)
        and (not sube or o.get("sube", "") == sube or o.get("sube", "") == "")
    ]

    # Teslim kayitlarini yukle
    _submissions = _load_yd_hw_submissions()
    _sub_map = {}
    for s in _submissions:
        _sub_map[(s.get("odev_id"), s.get("student_key"))] = s

    # AkademikDataStore teslimleri de kontrol et
    _ak_teslim_map = {}
    try:
        _ak_teslimleri = _ak_store.get_odev_teslimleri(student_id=_student_key)
        for t in _ak_teslimleri:
            _ak_teslim_map[t.odev_id] = t
    except Exception:
        pass

    # ── Hafta ve level belirle ──
    _level = _yd_sinif_to_level(sinif)
    _cur = _CURRICULUM.get(_level, []) if _level else []

    # ── Istatistikler ──
    _total_ak = len(_odevler_ak)
    _total_legacy = len(_legacy_filtered)
    _total = _total_ak + _total_legacy
    _completed = sum(1 for s in _submissions if s.get("student_key") == _student_key)
    _completed += sum(1 for t in _ak_teslim_map.values() if t.durum == "teslim_edildi")
    _pending = max(0, _total - _completed)

    st.markdown(
        f'<div style="display:flex;gap:8px;margin-bottom:12px;">'
        f'<div style="flex:1;background:#eff6ff;border:1px solid #93c5fd;'
        f'border-radius:8px;padding:8px;text-align:center;">'
        f'<div style="font-size:20px;font-weight:800;color:#1e40af;">{_total}</div>'
        f'<div style="font-size:10px;color:#64748b;">Toplam</div></div>'
        f'<div style="flex:1;background:#fef3c7;border:1px solid #fcd34d;'
        f'border-radius:8px;padding:8px;text-align:center;">'
        f'<div style="font-size:20px;font-weight:800;color:#d97706;">{_pending}</div>'
        f'<div style="font-size:10px;color:#64748b;">Bekleyen</div></div>'
        f'<div style="flex:1;background:#d1fae5;border:1px solid #6ee7b7;'
        f'border-radius:8px;padding:8px;text-align:center;">'
        f'<div style="font-size:20px;font-weight:800;color:#059669;">{_completed}</div>'
        f'<div style="font-size:10px;color:#64748b;">Tamamlanan</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if not _odevler_ak and not _legacy_filtered:
        st.info("Henuz yabanci dil odevi bulunmuyor.")
        st.divider()
        return

    # ══════════════════════════════════════════════════════════════
    # AKADEMİK STORE ÖDEVLERİ (Yeni sistem — haftalik odevler)
    # ══════════════════════════════════════════════════════════════
    for odev in _odevler_ak:
        _ak_teslim = _ak_teslim_map.get(odev.id)
        _is_done = _ak_teslim and _ak_teslim.durum == "teslim_edildi"
        _gecikti = bool(odev.son_teslim_tarihi and odev.son_teslim_tarihi < _today.isoformat())

        if _is_done:
            _icon = "\u2705"
            _border = "#22c55e"
            _bg = "#f0fdf4"
            _status = f"Teslim Edildi | Puan: {_ak_teslim.puan:.0f}/100"
        elif _gecikti:
            _icon = "\U0001F534"
            _border = "#ef4444"
            _bg = "#fef2f2"
            _status = "Gecikti!"
        else:
            _icon = "\u23F3"
            _border = "#3b82f6"
            _bg = "#eff6ff"
            _status = f"Son Teslim: {odev.son_teslim_tarihi or '-'}"

        with st.expander(f"{_icon} {odev.baslik} — {_status}", expanded=not _is_done,
        ):
            if _is_done:
                # Sonuc goster
                _puan = _ak_teslim.puan or 0
                _renk = "#22c55e" if _puan >= 70 else "#f59e0b" if _puan >= 50 else "#ef4444"
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{_renk}15,{_renk}08);'
                    f'border:2px solid {_renk};border-radius:14px;'
                    f'padding:20px;text-align:center;">'
                    f'<div style="font-size:2.5rem;font-weight:900;color:{_renk};">'
                    f'{_puan:.0f}</div>'
                    f'<div style="color:{_renk};font-weight:700;">/ 100 Puan</div>'
                    f'<div style="margin-top:8px;font-size:.8rem;color:#475569;">'
                    f'Teslim: {_ak_teslim.teslim_tarihi}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if _ak_teslim.ogretmen_notu:
                    st.info(f"\U0001F4AC Ogretmen Notu: {_ak_teslim.ogretmen_notu}")
            else:
                st.markdown(f"**{odev.baslik}**")
                if odev.aciklama:
                    st.markdown(f"<div style='font-size:12px;color:#475569;'>"
                               f"{odev.aciklama}</div>", unsafe_allow_html=True)

                # Odev iceriginden quiz uret
                _hw_meta = _parse_odev_to_hw_items(odev)
                _render_hw_quiz_and_submit(
                    odev_id=odev.id,
                    hw_items=_hw_meta,
                    level=_level,
                    student_key=_student_key,
                    store_mode="akademik",
                )

    # ══════════════════════════════════════════════════════════════
    # LEGACY ÖDEVLERİ (yd_odevler.json)
    # ══════════════════════════════════════════════════════════════
    for o in _legacy_filtered:
        _odev_id = o.get("id", f"leg_{o.get('hafta', 0)}_{o.get('tip', '')}")
        _sub = _sub_map.get((_odev_id, _student_key))
        _is_done = _sub and _sub.get("durum") == "teslim_edildi"

        try:
            _st_date = _vd2.fromisoformat(o.get("son_teslim", "2099-01-01"))
            _gecikti = _st_date < _today
        except Exception:
            _gecikti = False

        if _is_done:
            _icon = "\u2705"
            _status = f"Teslim Edildi | Puan: {_sub.get('puan', 0):.0f}/100"
        elif _gecikti:
            _icon = "\U0001F534"
            _status = "Gecikti!"
        else:
            _icon = "\u23F3"
            _status = f"Son Teslim: {o.get('son_teslim', '-')}"

        with st.expander(f"{_icon} {o.get('baslik', 'Odev')} — {_status}",
            expanded=not _is_done,
        ):
            if _is_done:
                _puan = _sub.get("puan", 0)
                _renk = "#22c55e" if _puan >= 70 else "#f59e0b" if _puan >= 50 else "#ef4444"
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{_renk}15,{_renk}08);'
                    f'border:2px solid {_renk};border-radius:14px;'
                    f'padding:20px;text-align:center;">'
                    f'<div style="font-size:2.5rem;font-weight:900;color:{_renk};">'
                    f'{_puan:.0f}</div>'
                    f'<div style="color:{_renk};font-weight:700;">/ 100 Puan</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f"<div style='font-size:12px;color:#475569;'>"
                           f"{o.get('aciklama', '')}</div>", unsafe_allow_html=True)

                # Legacy odevden quiz uret
                _week_num = o.get("hafta", 1)
                _wk_data = _cur[_week_num - 1] if _cur and _week_num <= len(_cur) else {}
                _hw_item = {
                    "type": o.get("tip", "vocabulary"),
                    "title": o.get("baslik", ""),
                    "source": o.get("interaktif_sekme", ""),
                }
                _render_hw_quiz_and_submit(
                    odev_id=_odev_id,
                    hw_items=[_hw_item],
                    level=_level,
                    student_key=_student_key,
                    store_mode="legacy",
                    week_data=_wk_data,
                )

    st.divider()


def _parse_odev_to_hw_items(odev) -> list:
    """Akademik Odev aciklamasindan odev tiplerini cikar."""
    items = []
    if not odev.aciklama:
        return [{"type": "vocabulary", "title": odev.baslik, "source": "Vocabulary"}]
    text = odev.aciklama.lower()
    _type_hints = [
        ("vocabulary", ["kelime", "vocab"]),
        ("grammar", ["gramer", "grammar", "structure"]),
        ("listening", ["dinleme", "listening"]),
        ("speaking", ["konusma", "speaking"]),
        ("reading", ["okuma", "reading"]),
        ("writing", ["yazma", "writing"]),
        ("functional", ["iletisim", "functional", "diyalog"]),
        ("pronunciation", ["telaffuz", "pronunciation"]),
        ("coursebook", ["coursebook", "ders kitabi"]),
        ("destek_kitap", ["practice", "words & sounds", "reading adv", "performance"]),
    ]
    for hw_type, keywords in _type_hints:
        if any(kw in text for kw in keywords):
            items.append({"type": hw_type, "title": odev.baslik, "source": hw_type})
    if not items:
        items.append({"type": "vocabulary", "title": odev.baslik, "source": "General"})
    return items


def _render_hw_quiz_and_submit(odev_id: str, hw_items: list, level: str,
                                student_key: str, store_mode: str = "legacy",
                                week_data: dict = None):
    """Odev icin quiz goster, cevapla, Geri Gonder butonu ile otomatik degerlendir."""
    from views.yd_content import _CURRICULUM, _curriculum_auto_week
    from views.yd_tools import _get_akademik_store
    from datetime import datetime as _dt_q

    # Hafta verisini bul
    if week_data is None:
        # Akademik odev icin guncel haftayi bul
        _cur = _CURRICULUM.get(level, [])
        _auto_wk = _curriculum_auto_week()
        week_data = _cur[_auto_wk - 1] if _cur and _auto_wk <= len(_cur) else {}

    # Tum odev tiplerinden sorulari topla
    _all_qs = []
    for hw in hw_items:
        qs = _generate_hw_quiz(hw, week_data, level or "grade5")
        _all_qs.extend(qs)

    if not _all_qs:
        st.info("Bu odev icin otomatik degerlendirme mevcut degil.")
        return

    # Quiz anahtari (use _get_hw_teslim_key for tracking)
    _teslim_key = _get_hw_teslim_key(odev_id, student_key)
    _quiz_key = f"yd_quiz_{odev_id}_{student_key}"
    if _quiz_key not in st.session_state:
        st.session_state[_quiz_key] = _all_qs

    _qs = st.session_state[_quiz_key]

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0ea5e915,#0ea5e908);'
        f'border:1px solid #0ea5e930;border-radius:10px;padding:10px 14px;margin:8px 0;">'
        f'<div style="font-weight:700;color:#0369a1;font-size:.9rem;">'
        f'\U0001F4DD Odev Quizi \u2014 {len(_qs)} Soru</div>'
        f'<div style="font-size:.75rem;color:#64748b;margin-top:2px;">'
        f'Sorulari cevapla ve "Geri Gonder" butonuna bas. '
        f'Sistem otomatik degerlendirecek.</div></div>',
        unsafe_allow_html=True,
    )

    _answers = {}
    for i, q in enumerate(_qs):
        st.markdown(f"**{i + 1}.** {q['q']}")
        _sel = st.radio(
            f"q_{i}",
            q["choices"],
            key=f"yd_q_{odev_id}_{i}",
            index=None,
            label_visibility="collapsed",
        )
        if _sel is not None:
            _answers[i] = q["choices"].index(_sel)
        st.markdown("")

    _answered = len(_answers)
    _btn_label = (
        f"\U0001F4E4 Geri Gonder & Degerlendir"
        if _answered == len(_qs)
        else f"\U0001F4E4 Geri Gonder ({_answered}/{len(_qs)} cevaplanmis)"
    )

    if st.button(_btn_label, key=f"yd_submit_{odev_id}",
                 type="primary", use_container_width=True):
        if _answered == 0:
            st.warning("Lutfen en az bir soruyu cevaplayin.")
            return

        # Otomatik degerlendirme
        _correct = sum(1 for i, q in enumerate(_qs) if _answers.get(i) == q["answer"])
        _wrong = _answered - _correct
        _empty = len(_qs) - _answered
        _puan = round((_correct / len(_qs)) * 100) if _qs else 0

        # Sonuc kaydet
        _now = _dt_q.now().isoformat()
        _submission = {
            "odev_id": odev_id,
            "student_key": student_key,
            "puan": _puan,
            "dogru": _correct,
            "yanlis": _wrong,
            "bos": _empty,
            "toplam": len(_qs),
            "durum": "teslim_edildi",
            "teslim_tarihi": _now,
            "cevaplar": {str(k): v for k, v in _answers.items()},
        }
        _save_yd_hw_submission(_submission)

        # Akademik store'a da kaydet
        if store_mode == "akademik":
            try:
                _ak_store = _get_akademik_store()
                _teslimleri = _ak_store.get_odev_teslimleri(odev_id=odev_id, student_id=student_key)
                _teslim = _teslimleri[0] if _teslimleri else None
                if _teslim is None:
                    from models.akademik_takip import OdevTeslim
                    _teslim = OdevTeslim(
                        odev_id=odev_id,
                        student_id=student_key,
                        student_adi=st.session_state.get("ad_soyad", student_key),
                    )
                _teslim.durum = "teslim_edildi"
                _teslim.puan = float(_puan)
                _teslim.teslim_tarihi = _now[:10]
                _teslim.teslim_metni = (
                    f"Otomatik Degerlendirme: {_correct}/{len(_qs)} dogru, "
                    f"Puan: {_puan}/100"
                )
                _ak_store.save_odev_teslim(_teslim)
            except Exception as _e:
                _logger.debug("AK store save failed: %s", _e)

        # Sonuc goster
        _renk = "#22c55e" if _puan >= 70 else "#f59e0b" if _puan >= 50 else "#ef4444"
        st.markdown(
            f'<div style="background:linear-gradient(135deg,{_renk}15,{_renk}08);'
            f'border:2px solid {_renk};border-radius:14px;'
            f'padding:24px;text-align:center;margin-top:12px;">'
            f'<div style="font-size:2.5rem;font-weight:900;color:{_renk};">{_puan}</div>'
            f'<div style="color:{_renk};font-weight:700;font-size:1.1rem;">/ 100 Puan</div>'
            f'<div style="margin-top:10px;color:#475569;font-size:0.88rem;">'
            f'\u2705 {_correct} Dogru &nbsp;&nbsp;'
            f'\u274C {_wrong} Yanlis &nbsp;&nbsp;'
            f'\u2B1C {_empty} Bos</div></div>',
            unsafe_allow_html=True,
        )

        # Detayli geri bildirim — her sorunun aciklamasi
        st.markdown(
            '<div style="font-weight:700;font-size:13px;color:#1e40af;margin:12px 0 6px;">'
            '\U0001F4CB Detayli Geri Bildirim</div>',
            unsafe_allow_html=True,
        )
        for i, q in enumerate(_qs):
            _user_ans = _answers.get(i)
            _is_correct = _user_ans == q["answer"]
            _ic = "\u2705" if _is_correct else "\u274C"
            _user_text = q["choices"][_user_ans] if _user_ans is not None else "Bos"
            _correct_text = q["choices"][q["answer"]]
            _bg_fb = "#f0fdf4" if _is_correct else "#fef2f2"
            _bd_fb = "#86efac" if _is_correct else "#fca5a5"
            st.markdown(
                f'<div style="background:{_bg_fb};border:1px solid {_bd_fb};'
                f'border-radius:8px;padding:8px 12px;margin-bottom:4px;">'
                f'<div style="font-weight:600;font-size:12px;">{_ic} S{i+1}: {q["q"]}</div>'
                f'<div style="font-size:11px;color:#475569;margin-top:2px;">'
                f'Senin cevabin: <b>{_user_text}</b>'
                + (f' | Dogru cevap: <b>{_correct_text}</b>' if not _is_correct else '')
                + f'</div>'
                f'<div style="font-size:10px;color:#64748b;margin-top:2px;">'
                f'\U0001F4A1 {q.get("explanation", "")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.success("\U0001F389 Odev teslim edildi ve degerlendirildi!")
        # Quiz temizle
        st.session_state.pop(_quiz_key, None)
        st.rerun()


def _render_veli_ders_oynatici(sinif, sube):
    """Veli ekraninda islenen konunun premium ders anlatim oynaticisi."""
    from views.yd_tools import _load_eng_gunluk_ozet, _render_lesson_player
    from datetime import date as _vd3

    # Bugunun ozet verisinden hafta ve level bilgisi al
    _today = _vd3.today()
    _oz = _load_eng_gunluk_ozet(_today.isoformat(), sinif, sube or "")

    # Son 3 gun icinde islenmis ders ara
    if not _oz or not _oz.get("islendi"):
        from datetime import timedelta as _vtd3
        for _d in range(1, 4):
            _t = _today - _vtd3(days=_d)
            _oz = _load_eng_gunluk_ozet(_t.isoformat(), sinif, sube or "")
            if _oz and _oz.get("islendi"):
                break
        else:
            _oz = None

    if not _oz:
        return

    _hafta = _oz.get("hafta")
    _level = _yd_sinif_to_level(sinif)
    if not _hafta or not _level:
        return

    st.markdown(
        '<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;'
        'padding:12px 16px;border-radius:12px;margin-bottom:10px;text-align:center;">'
        '<h4 style="margin:0;font-size:16px;">Premium Ders Anlatimi</h4>'
        '<p style="margin:3px 0 0;font-size:11px;opacity:0.85;">'
        f'Hafta {_hafta}: {_oz.get("theme_tr", "")} — Interaktif sesli ders</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    _render_lesson_player(_level, _hafta, height=480)
    st.divider()


def _render_veli_ders_isleme_mesajlari(sinif, sube):
    """Veli panelinde Ders Isleme Motoru'ndan gelen ders ozetleri."""
    from models.lesson_delivery import LessonDeliveryStore

    store = LessonDeliveryStore()
    _sinif_int = int(sinif) if sinif else 0
    sessions = store.get_completed_sessions(sinif=_sinif_int, sube=sube or "", limit=10)

    if not sessions:
        return

    st.markdown(
        '<div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);color:#fff;'
        'padding:14px 18px;border-radius:12px;margin-bottom:10px;text-align:center;'
        'border:1.5px solid rgba(99,102,241,.25);">'
        '<h4 style="margin:0;font-size:16px;color:#c7d2fe;">'
        '\U0001F393 Ders Isleme Motoru Mesajlari</h4>'
        '<p style="margin:3px 0 0;font-size:11px;color:#818cf8;">'
        'Ogretmeninizin isledigitkonular ve ders ozetleri</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    _PHASE_LABELS = {
        "L1_warmup": "Isinma", "L1_vocabulary": "Kelime",
        "L1_grammar": "Dilbilgisi", "L1_listening": "Dinleme & Konusma",
        "L2_reading": "Okuma", "L2_writing": "Yazma",
        "L2_song": "Sarki & Kultur", "L2_exercises": "Alistirma",
        "L2_review": "Tekrar",
    }

    for s in sessions:
        theme = s.get("theme", "")
        theme_tr = s.get("theme_tr", "")
        week = s.get("week", 0)
        unit_num = s.get("unit_num", 0)
        vocab = s.get("vocab", [])
        structure = s.get("structure", "")
        teacher = s.get("teacher_name", "Ogretmen")
        ended = s.get("ended_at", "")
        phases = s.get("completed_phases", [])
        total = 9
        done = len(phases)
        pct = round(done / total * 100) if total else 0
        pct_color = "#22c55e" if pct >= 80 else "#f59e0b" if pct >= 50 else "#ef4444"

        # Tarih formatla
        date_disp = ended[:10] if ended else ""
        time_disp = ended[11:16] if len(ended) > 16 else ""

        # Tamamlanan faz isimleri
        phase_names = [_PHASE_LABELS.get(p, p) for p in phases]
        phase_str = ", ".join(phase_names) if phase_names else "—"

        # Kelime listesi
        vocab_str = ", ".join(vocab[:8]) if vocab else "—"

        with st.expander(f"\U0001F4D8 Hafta {week} / Unite {unit_num}: {theme} ({theme_tr}) — {date_disp}",
            expanded=False,
        ):
            st.markdown(
                f'<div style="background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.15);'
                f'border-radius:12px;padding:14px 18px;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'
                f'<div><span style="color:#c7d2fe;font-weight:700;font-size:1rem;">'
                f'\U0001F4D8 Unit {unit_num}: {theme}</span>'
                f'<br><span style="color:#94a3b8;font-size:.82rem;">{theme_tr}</span></div>'
                f'<div style="text-align:right;">'
                f'<div style="color:{pct_color};font-size:1.3rem;font-weight:800;">%{pct}</div>'
                f'<div style="color:#64748b;font-size:.72rem;">{done}/{total} faz</div></div></div>'
                f'<div style="font-size:.85rem;color:#cbd5e1;margin-bottom:6px;">'
                f'\U0001F468\u200D\U0001F3EB <b>Ogretmen:</b> {_sanitize_html(teacher)} &nbsp;|&nbsp; '
                f'\U0001F4C5 {date_disp} {time_disp}</div>'
                f'<div style="font-size:.85rem;color:#cbd5e1;margin-bottom:6px;">'
                f'\U0001F4DA <b>Kelimeler:</b> {_sanitize_html(vocab_str)}</div>'
                f'<div style="font-size:.85rem;color:#cbd5e1;margin-bottom:6px;">'
                f'\U0001F4DD <b>Dilbilgisi:</b> {_sanitize_html(structure[:120]) if structure else "—"}</div>'
                f'<div style="font-size:.85rem;color:#cbd5e1;">'
                f'\u2705 <b>Islenen fazlar:</b> {_sanitize_html(phase_str)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Ev calismasi onerileri
            if vocab:
                st.markdown(
                    '<div style="background:rgba(34,197,94,.06);border-left:4px solid #22c55e;'
                    'border-radius:0 8px 8px 0;padding:10px 14px;margin-top:8px;">'
                    '<div style="color:#22c55e;font-weight:700;font-size:.88rem;">'
                    '\U0001F3E0 Evde Yapilabilecekler</div>'
                    '<ul style="color:#94a3b8;font-size:.82rem;margin:6px 0 0 0;padding-left:18px;">'
                    '<li>Yeni kelimeleri sesli tekrarlasin</li>'
                    '<li>Her kelimeyle bir cumle kursun</li>'
                    '<li>Ders kitabindaki metni tekrar okusun</li>'
                    '</ul></div>',
                    unsafe_allow_html=True,
                )

    st.divider()


def render_veli_english_tab(sinif, sube=None):
    """Veli paneli icin Ingilizce ogrenme sekmesi."""
    from views.yd_content import _CURRICULUM, _render_preschool_english
    from views.yd_tools import _render_veli_yd_sinavlar, _render_veli_yd_quizler
    from views.curriculum_ortaokul import (
        CURRICULUM_GRADE5, CURRICULUM_GRADE6,
        CURRICULUM_GRADE7, CURRICULUM_GRADE8,
    )
    level = _yd_sinif_to_level(sinif)
    if level is None:
        st.info("Bu sinif seviyesi icin Ingilizce icerik bulunmamaktadir.")
        return

    # Veli Ilerleme Raporu (TIER 1.5)
    _render_veli_ilerleme_raporu(sinif, sube)

    # 📋 CEFR Seviye Tespit Sonuclari
    _render_veli_cefr_placement(sinif, sube)

    # 🏆 CEFR Mock Exam Sonuclari
    _render_veli_cefr_mock_results(sinif, sube)

    # Yabanci Dil Islenen Konular Ozeti (yeni)
    _render_veli_yd_ozet(sinif, sube)

    # Premium Ders Anlatimi — bugunun islenen konusu
    _render_veli_ders_oynatici(sinif, sube)

    # 🎓 Ders Isleme Motoru Mesajlari
    _render_veli_ders_isleme_mesajlari(sinif, sube)

    # Dijital Etkinlikler — evde tekrar (kitapta olmayan)
    _render_veli_dijital_odev(sinif, sube)

    # Yabanci Dil Odevleri (yeni)
    _render_veli_yd_odevler(sinif, sube)

    # Yabanci Dil Sinavlari (36 hafta olcme)
    _render_veli_yd_sinavlar(sinif, sube)

    # Unite Quizleri (unite bazli quiz sonuclari + aktif quizler)
    _render_veli_yd_quizler(sinif, sube)

    # ── Ders Kitabi (Flip Book) ──
    _veli_grade = int(sinif) if sinif else 5
    if 5 <= _veli_grade <= 8:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#0B0F19,#1e3a5f);color:#fff;'
            'padding:12px 16px;border-radius:12px;margin-bottom:10px;text-align:center;">'
            '<h4 style="margin:0;font-size:16px;">English Coursebook — Sesli Ders Kitabı</h4>'
            '<p style="margin:3px 0 0;font-size:11px;opacity:0.85;">'
            'Interaktif flip book | Sesli okuma | Kelime telaffuzu</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        with st.expander("Ders Kitabini Ac (Flip Book)", expanded=False):
            try:
                from views.textbook_grade5 import build_coursebook_flipbook_html as _vfb_fn
                _veli_cur = None
                if _veli_grade == 0:
                    from views.curriculum_okul_oncesi import CURRICULUM_PRESCHOOL as _veli_cur
                elif _veli_grade in (1, 2, 3, 4):
                    from views.curriculum_ilkokul import (
                        CURRICULUM_GRADE1, CURRICULUM_GRADE2, CURRICULUM_GRADE3, CURRICULUM_GRADE4)
                    _veli_cur = {1: CURRICULUM_GRADE1, 2: CURRICULUM_GRADE2,
                                 3: CURRICULUM_GRADE3, 4: CURRICULUM_GRADE4}[_veli_grade]
                elif _veli_grade in (5, 6, 7, 8):
                    _veli_cur = {5: CURRICULUM_GRADE5, 6: CURRICULUM_GRADE6,
                                 7: CURRICULUM_GRADE7, 8: CURRICULUM_GRADE8}[_veli_grade]
                elif _veli_grade in (9, 10, 11, 12):
                    from views.curriculum_lise import (
                        CURRICULUM_GRADE9, CURRICULUM_GRADE10, CURRICULUM_GRADE11, CURRICULUM_GRADE12)
                    _veli_cur = {9: CURRICULUM_GRADE9, 10: CURRICULUM_GRADE10,
                                 11: CURRICULUM_GRADE11, 12: CURRICULUM_GRADE12}[_veli_grade]
                if _veli_cur:
                    _vfb_html = _vfb_fn(_veli_grade, _veli_cur, mode="parent")
                    st.components.v1.html(_vfb_html, height=700, scrolling=True)
                else:
                    st.info("Bu sinif seviyesi icin ders kitabi henuz hazir degil.")
            except Exception as _vfb_err:
                st.warning(f"Ders kitabi yuklenemedi: {_vfb_err}")
        st.divider()

    # Gunun Etkinligi Bolumu
    _render_veli_etkinlik_section(sinif, sube)

    # Ek Gonderiler Bolumu
    _render_veli_ek_gonderiler(sinif, sube)

    # Interaktif Ogrenme Sekmeleri
    key_prefix = f"veli_{level}"

    _render_preschool_english(
        key_prefix=key_prefix,
        etkinlik_level=None,         # Etkinlik kitabi gizli
        curriculum_level=None,       # Haftalik plan gizli
        writing_level=level,         # Yazma acik
        grammar_level=None,          # Dilbilgisi gizli
        phonics_level=level,         # Sesler acik
        listening_level=level,       # Dinleme acik
    )


# ══════════════════════════════════════════════════════════════════════════════
# OKUL ÖNCESİ BECERİ SEKMELERİ (5-6 Yaş — Okuma Yazma Bilmiyor)
# 36 Hafta × 10 Saat = 360 Saat | %100 Görsel + İşitsel + Kinestetik
# ══════════════════════════════════════════════════════════════════════════════



def render_yabanci_dil():
    """YD-01 modulu ana giris noktasi."""
    _inject_yd_css()

    # Smarti AI welcome
    try:
        from utils.smarti_helper import render_smarti_welcome
        render_smarti_welcome("yabanci_dil")
    except Exception:
        pass

    # Veli rolü — sadece Okuma Kütüphanesi'ne erişim
    from utils.auth import AuthManager
    _yd_user = AuthManager.get_current_user()
    if _yd_user.get("role") == "Veli":
        styled_header("📖 Okuma Kütüphanesi", "Çocuğunuzla birlikte İngilizce okuma kaynakları")
        # Direkt Okuma Kütüphanesi view'ını render et
        st.session_state["yd_view"] = "reading"
        _render_yabanci_dil()
        return

    _render_yabanci_dil()
