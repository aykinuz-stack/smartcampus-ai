"""
Egitim Koclugu Modulu - Ultra Premium UI
=========================================
Ogrenci koclugu, haftalik plan, hedef belirleme, motivasyon takibi,
performans analizi, zaman yonetimi ve veli raporlama.
"""

from __future__ import annotations

import json
import os
import streamlit as st
from datetime import datetime, date, timedelta
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("egitim_koclugu")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("egitim_koclugu",
        "1:1 bireysel kocluk, SMART hedef, motivasyon, deneme analizi",
        [("1:1", "Kocluk"), ("SMART", "Hedef"), ("VARK", "Analiz")])
except Exception:
    pass
from utils.shared_data import load_shared_students, get_student_display_options, get_sinif_sube_listesi

from models.egitim_koclugu import (
    get_ek_store, EKDataStore,
    KoclukOgrenci, KoclukGorusme, HedefKaydi, HaftalikPlan,
    MotivasyonKaydi, DenemeAnaliz, VeliRapor, KoclukAyar,
    CalismaTakvim, Odev, CanliDers, SoruKutusu, OnlineTest,
    KOCLUK_ALANLARI, HEDEF_DURUMLARI, HEDEF_ONCELIKLERI,
    GORUSME_TURLERI, GORUSME_DURUMLARI,
    RENK_BANDI, HAFTA_GUNLERI, DERS_LISTESI, SAAT_DILIMLERI,
    ETKINLIK_TURLERI, get_renk_bandi,
    ODEV_DURUMLARI, CANLI_DERS_TURLERI, CANLI_DERS_PLATFORMLARI,
    SORU_DURUMLARI, SORU_ONCELIKLERI,
)


# ============================================================
# KONSOLİDE VERİ YÜKLEME — AT/OD/YD ENTEGRASYONU
# ============================================================

def _g_safe(obj, key, default=""):
    """Güvenli attr/dict getter."""
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)


def _load_consolidated_deneme(store: EKDataStore, ogr_id: str) -> list[dict]:
    """Konsolide deneme/sınav verileri — EK + OD + AT + YD modüllerinden."""
    # 1) EK'nın kendi deneme verileri
    ek_data = store.get_by_ogrenci("deneme_analizleri", ogr_id) if ogr_id else []

    # 2) OD modülünden sınav sonuçları
    try:
        from models.olcme_degerlendirme import DataStore as ODStore
        od = ODStore()
        od_results = od.get_results(student_id=ogr_id)
        exams_map = {}
        try:
            for ex in od.get_exams():
                eid = _g_safe(ex, "id")
                if eid:
                    exams_map[eid] = ex
        except Exception:
            pass
        for r in od_results:
            exam = exams_map.get(_g_safe(r, "exam_id"), {})
            ek_data.append({
                "id": _g_safe(r, "id", ""),
                "ogrenci_id": ogr_id,
                "ogrenci_adi": _g_safe(r, "student_name", ""),
                "sinav_adi": _g_safe(exam, "name", "OD Sınavı"),
                "sinav_turu": _g_safe(exam, "exam_type", "yazili"),
                "tarih": str(_g_safe(r, "graded_at", "")),
                "toplam_soru": int(_g_safe(r, "total_questions", 0) or 0),
                "dogru": int(_g_safe(r, "correct_count", 0) or 0),
                "yanlis": int(_g_safe(r, "wrong_count", 0) or 0),
                "bos": int(_g_safe(r, "empty_count", 0) or 0),
                "net": float(_g_safe(r, "net_score", 0) or 0),
                "puan": float(_g_safe(r, "score", 0) or 0),
                "siralama": "",
                "ders_detaylari": _g_safe(r, "subject_breakdown", {}) or {},
                "notlar": "",
                "_kaynak": "OD",
            })
    except Exception:
        pass

    # 3) AT modülünden KYT sonuçları (kazanım yoklama — D/Y bazlı)
    try:
        from models.akademik_takip import get_akademik_store
        at = get_akademik_store()
        kyt_list = at.get_kyt_cevaplar(student_id=ogr_id) or []
        if kyt_list:
            from collections import defaultdict
            kyt_by_ders = defaultdict(lambda: {"dogru": 0, "yanlis": 0, "toplam": 0})
            for k in kyt_list:
                ders = getattr(k, "ders", "Genel")
                kyt_by_ders[ders]["toplam"] += 1
                if getattr(k, "dogru_mu", False):
                    kyt_by_ders[ders]["dogru"] += 1
                else:
                    kyt_by_ders[ders]["yanlis"] += 1
            toplam_d = sum(v["dogru"] for v in kyt_by_ders.values())
            toplam_y = sum(v["yanlis"] for v in kyt_by_ders.values())
            toplam_s = toplam_d + toplam_y
            puan_val = (toplam_d / toplam_s * 100) if toplam_s else 0
            ders_det = {}
            for ders_nm, vals in kyt_by_ders.items():
                ders_det[ders_nm] = {
                    "dogru": vals["dogru"],
                    "yanlis": vals["yanlis"],
                    "bos": 0,
                    "net": vals["dogru"] - vals["yanlis"] * 0.25,
                }
            ek_data.append({
                "id": f"kyt_{ogr_id}",
                "ogrenci_id": ogr_id,
                "sinav_adi": "Kazanım Yoklama Testi (KYT)",
                "sinav_turu": "kyt",
                "tarih": str(date.today()),
                "toplam_soru": toplam_s,
                "dogru": toplam_d,
                "yanlis": toplam_y,
                "bos": 0,
                "net": toplam_d - toplam_y * 0.25,
                "puan": puan_val,
                "siralama": "",
                "ders_detaylari": ders_det,
                "notlar": f"{len(kyt_list)} KYT sorusu",
                "_kaynak": "AT_KYT",
            })
    except Exception:
        pass

    # 4) YD modülünden yabancı dil sınavları
    try:
        from models.yd_assessment import YdAssessmentStore
        yd = YdAssessmentStore()
        yd_results = yd.get_results(student_id=ogr_id) or []
        for r in yd_results:
            score = float(getattr(r, "score", 0) or 0)
            if score <= 0:
                continue
            _unit_num = getattr(r, "unit", 0) or 0
            _unit_theme = getattr(r, "unit_theme", "") or ""
            _unit_info = f" | Ünite {_unit_num}: {_unit_theme}" if _unit_num > 0 else ""
            ek_data.append({
                "id": getattr(r, "id", ""),
                "ogrenci_id": ogr_id,
                "ogrenci_adi": getattr(r, "student_name", ""),
                "sinav_adi": f"YD: {getattr(r, 'exam_name', 'Sınav')}",
                "sinav_turu": f"yd_{getattr(r, 'exam_category', 'quiz')}",
                "tarih": str(getattr(r, "graded_at", "")),
                "toplam_soru": int(getattr(r, "total_questions", 0) or 0),
                "dogru": int(getattr(r, "correct_count", 0) or 0),
                "yanlis": int(getattr(r, "wrong_count", 0) or 0),
                "bos": int(getattr(r, "empty_count", 0) or 0),
                "net": float(getattr(r, "correct_count", 0) or 0) - float(getattr(r, "wrong_count", 0) or 0) * 0.25,
                "puan": score,
                "siralama": "",
                "ders_detaylari": getattr(r, "skill_breakdown", {}) or {},
                "notlar": f"Seviye: {getattr(r, 'level', '')}{_unit_info}",
                "_kaynak": "YD",
            })
    except Exception:
        pass

    return ek_data


def _load_consolidated_online(store: EKDataStore, ogr_id: str) -> list[dict]:
    """Konsolide online test verileri — EK + OD (online sınavlar)."""
    # 1) EK'nın kendi online test verileri
    ek_data = store.get_by_ogrenci("online_testler", ogr_id) if ogr_id else []

    # 2) OD modülünden online sınavlar
    try:
        from models.olcme_degerlendirme import DataStore as ODStore
        od = ODStore()
        od_results = od.get_results(student_id=ogr_id)
        exams_map = {}
        try:
            for ex in od.get_exams():
                eid = _g_safe(ex, "id")
                if eid:
                    exams_map[eid] = ex
        except Exception:
            pass
        for r in od_results:
            exam = exams_map.get(_g_safe(r, "exam_id"), {})
            is_online = _g_safe(exam, "online_sinav", False)
            if not is_online:
                continue
            ek_data.append({
                "id": _g_safe(r, "id", ""),
                "ogrenci_id": ogr_id,
                "ogrenci_adi": _g_safe(r, "student_name", ""),
                "test_adi": _g_safe(exam, "name", "OD Online Sınav"),
                "ders": _g_safe(exam, "subject", "—"),
                "konu": "",
                "tarih": str(_g_safe(r, "graded_at", "")),
                "sure_dk": int(_g_safe(exam, "duration_minutes", 0) or 0),
                "toplam_soru": int(_g_safe(r, "total_questions", 0) or 0),
                "dogru": int(_g_safe(r, "correct_count", 0) or 0),
                "yanlis": int(_g_safe(r, "wrong_count", 0) or 0),
                "bos": int(_g_safe(r, "empty_count", 0) or 0),
                "net": float(_g_safe(r, "net_score", 0) or 0),
                "puan": float(_g_safe(r, "score", 0) or 0),
                "durum": "tamamlandi",
                "notlar": "",
                "_kaynak": "OD",
            })
    except Exception:
        pass

    return ek_data


def _load_all_deneme_list(store: EKDataStore) -> list[dict]:
    """Dashboard için tüm deneme kayıtları — EK + OD (tüm öğrenciler)."""
    ek_data = store.load_list("deneme_analizleri")

    try:
        from models.olcme_degerlendirme import DataStore as ODStore
        od = ODStore()
        all_results = od.get_results()
        exams_map = {}
        try:
            for ex in od.get_exams():
                eid = _g_safe(ex, "id")
                if eid:
                    exams_map[eid] = ex
        except Exception:
            pass
        for r in all_results:
            exam = exams_map.get(_g_safe(r, "exam_id"), {})
            ek_data.append({
                "id": _g_safe(r, "id", ""),
                "ogrenci_id": _g_safe(r, "student_id", ""),
                "sinav_adi": _g_safe(exam, "name", "OD Sınavı"),
                "sinav_turu": _g_safe(exam, "exam_type", "yazili"),
                "tarih": str(_g_safe(r, "graded_at", "")),
                "dogru": int(_g_safe(r, "correct_count", 0) or 0),
                "yanlis": int(_g_safe(r, "wrong_count", 0) or 0),
                "bos": int(_g_safe(r, "empty_count", 0) or 0),
                "net": float(_g_safe(r, "net_score", 0) or 0),
                "puan": float(_g_safe(r, "score", 0) or 0),
                "_kaynak": "OD",
            })
    except Exception:
        pass

    return ek_data


# ============================================================
# CSS INJECTION - ULTRA PREMIUM
# ============================================================

def _inject_ek_css():
    """Ultra premium Egitim Koclugu CSS."""
    if st.session_state.get("_ek_css_injected"):
        return
    st.session_state["_ek_css_injected"] = True
    inject_common_css("ek")
    st.markdown("""<style>
    :root {
        --ek-primary: #6366f1;
        --ek-primary-dark: #4f46e5;
        --ek-secondary: #8b5cf6;
        --ek-accent: #a78bfa;
        --ek-success: #10b981;
        --ek-warning: #f59e0b;
        --ek-danger: #ef4444;
        --ek-info: #06b6d4;
        --ek-gold: #d4a017;
        --ek-rose: #f43f5e;
    }

    /* ── PREMIUM CARD ── */
    .ek-card {
        background: linear-gradient(145deg, #ffffff 0%, #fafbff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 16px rgba(99,102,241,0.06), 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .ek-card:hover {
        box-shadow: 0 8px 30px rgba(99,102,241,0.12), 0 2px 8px rgba(0,0,0,0.06);
        transform: translateY(-2px);
        border-color: #c7d2fe;
    }

    /* ── GLASS CARD ── */
    .ek-glass {
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(249,250,251,0.9));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(99,102,241,0.12);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 8px 32px rgba(99,102,241,0.08);
    }

    /* ── STAT DIAMOND CARDS ── */
    .ek-diamond-row {
        display: flex; gap: 12px; margin: 16px 0; flex-wrap: wrap;
    }
    .ek-diamond-card {
        flex: 1; min-width: 140px;
        background: linear-gradient(145deg, #ffffff, #f8faff);
        border: 1px solid #e0e7ff;
        border-radius: 16px;
        padding: 18px 14px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .ek-diamond-card::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, var(--ek-primary), var(--ek-secondary), var(--ek-accent));
    }
    .ek-diamond-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(99,102,241,0.15);
    }
    .ek-diamond-icon { font-size: 1.8rem; margin-bottom: 6px; }
    .ek-diamond-value {
        font-size: 1.6rem; font-weight: 800;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .ek-diamond-label {
        font-size: 0.72rem; color: #64748b; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;
    }

    /* ── COACHING WHEEL ── 9 daire — responsive grid */
    .ek-wheel-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
        gap: 14px;
        padding: 20px 10px;
        max-width: 920px;
        margin: 0 auto;
    }
    @media (min-width: 768px) {
        .ek-wheel-container {
            grid-template-columns: repeat(9, 1fr);
            gap: 10px;
        }
    }
    .ek-wheel-item {
        aspect-ratio: 1;
        border-radius: 50%;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        color: white; font-weight: 700;
        text-align: center; padding: 8px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        cursor: default;
        min-height: 90px;
        position: relative;
    }
    .ek-wheel-item::before {
        content: '';
        position: absolute; inset: 0;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.25), transparent 50%);
        pointer-events: none;
    }
    .ek-wheel-item:hover {
        transform: scale(1.08) rotate(-3deg);
        box-shadow: 0 14px 36px rgba(0,0,0,0.35);
    }
    .ek-wheel-icon {
        font-size: 1.8rem;
        line-height: 1;
        margin-bottom: 4px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
    .ek-wheel-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        line-height: 1.1;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }

    /* ── PROGRESS BAR ── */
    .ek-progress-container {
        background: #1A2035; border-radius: 10px; height: 10px;
        overflow: hidden; margin: 6px 0;
    }
    .ek-progress-bar {
        height: 100%; border-radius: 10px;
        background: linear-gradient(90deg, var(--ek-primary), var(--ek-secondary));
        transition: width 0.5s ease;
    }

    /* ── BADGE ── */
    .ek-badge {
        display: inline-flex; align-items: center; gap: 4px;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.72rem; font-weight: 700;
    }

    /* ── TIMELINE ── */
    .ek-timeline { position: relative; padding-left: 28px; }
    .ek-timeline::before {
        content: ''; position: absolute; left: 10px; top: 0; bottom: 0;
        width: 2px; background: linear-gradient(180deg, #6366f1, #a78bfa, #e2e8f0);
    }
    .ek-timeline-item {
        position: relative; margin-bottom: 16px;
        background: white; border: 1px solid #e2e8f0;
        border-radius: 12px; padding: 14px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .ek-timeline-item::before {
        content: ''; position: absolute; left: -23px; top: 18px;
        width: 10px; height: 10px; border-radius: 50%;
        background: #6366f1; border: 2px solid white;
        box-shadow: 0 0 0 2px #6366f1;
    }

    /* ── HAFTALIK PLAN GRID ── */
    .ek-plan-grid {
        display: grid;
        grid-template-columns: 90px repeat(7, 1fr);
        gap: 2px; margin: 12px 0;
        font-size: 0.75rem;
    }
    .ek-plan-header {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white; padding: 10px 6px;
        text-align: center; font-weight: 700;
        border-radius: 6px;
    }
    .ek-plan-saat {
        background: #1A2035; padding: 8px 6px;
        text-align: center; font-weight: 600; color: #475569;
        border-radius: 6px;
    }
    .ek-plan-cell {
        background: white; border: 1px solid #e2e8f0;
        padding: 6px; border-radius: 6px;
        min-height: 36px; cursor: pointer;
        transition: all 0.2s ease;
    }
    .ek-plan-cell:hover { background: #f0f0ff; border-color: #c7d2fe; }
    .ek-plan-cell.filled {
        background: linear-gradient(135deg, #eef2ff, #e0e7ff);
        border-color: #a5b4fc;
    }
    .ek-plan-cell .ders-tag {
        background: linear-gradient(135deg, #6366f1, #818cf8);
        color: white; padding: 2px 6px; border-radius: 4px;
        font-size: 0.65rem; font-weight: 600;
        display: inline-block;
    }

    /* ── RADAR/SPIDER CHART PLACEHOLDER ── */
    .ek-radar-grid {
        display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 10px; margin: 12px 0;
    }
    .ek-radar-item {
        background: #111827; border: 1px solid #e2e8f0;
        border-radius: 12px; padding: 14px;
        text-align: center;
    }
    .ek-radar-score {
        font-size: 1.8rem; font-weight: 800;
        margin: 6px 0;
    }
    .ek-radar-label {
        font-size: 0.78rem; color: #64748b; font-weight: 600;
    }

    /* ── SECTION DIVIDER ── */
    .ek-divider {
        height: 1px; margin: 20px 0;
        background: linear-gradient(90deg, transparent, #c7d2fe, transparent);
    }

    /* ── MOTIVASYON METER ── */
    .ek-meter {
        display: flex; align-items: center; gap: 8px; margin: 6px 0;
    }
    .ek-meter-label {
        width: 120px; font-size: 0.8rem; font-weight: 600; color: #475569;
    }
    .ek-meter-bar-bg {
        flex: 1; height: 12px; background: #1A2035;
        border-radius: 6px; overflow: hidden;
    }
    .ek-meter-bar-fill {
        height: 100%; border-radius: 6px;
        transition: width 0.5s ease;
    }
    .ek-meter-value {
        width: 30px; font-size: 0.8rem; font-weight: 700; color: #334155;
        text-align: right;
    }
    </style>""", unsafe_allow_html=True)


# ============================================================
# YARDIMCI UI FONKSIYONLARI
# ============================================================

def _diamond_stats(stats: list):
    """Ultra premium diamond stat kartlari. stats: [(icon, value, label, color), ...]"""
    html = '<div class="ek-diamond-row">'
    for icon, value, label, color in stats:
        html += f'''
        <div class="ek-diamond-card">
            <div class="ek-diamond-icon">{icon}</div>
            <div class="ek-diamond-value" style="background:linear-gradient(135deg,{color},{color}cc);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent">{value}</div>
            <div class="ek-diamond-label">{label}</div>
        </div>'''
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def _coaching_wheel():
    """Kocluk cemberi - 9 alan (canonical renklerle)."""
    items = [
        ("Mutluluk",        "#DB2777", "😊"),   # pink.600
        ("Farkindalik",     "#7C3AED", "🔍"),   # violet.600
        ("Hedef",           "#4F46E5", "🎯"),   # indigo.600
        ("Motivasyon",      "#D97706", "🔥"),   # amber.600
        ("Ozguven",         "#059669", "💪"),   # emerald.600
        ("Iletisim",        "#0891B2", "💬"),   # cyan.600
        ("Performans",      "#DC2626", "📊"),   # red.600
        ("Zaman Yonetimi",  "#0284C7", "⏰"),   # sky.600
        ("Basari",          "#B45309", "🏆"),   # amber.700 (altın)
    ]
    # HTML'i TEK SATIRDA olusturulmali — markdown parser indent'leri code block olarak algiliyor
    items_html = "".join(
        f'<div class="ek-wheel-item" style="background:linear-gradient(135deg,{color},{color}dd)">'
        f'<div class="ek-wheel-icon">{icon}</div>'
        f'<div class="ek-wheel-label">{label}</div>'
        f'</div>'
        for label, color, icon in items
    )
    st.markdown(f'<div class="ek-wheel-container">{items_html}</div>', unsafe_allow_html=True)


def _progress_bar(value: float, max_val: float = 100):
    """Gradient progress bar."""
    pct = min(100, max(0, (value / max_val * 100) if max_val > 0 else 0))
    color = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 40 else "#ef4444"
    st.markdown(f'''
    <div class="ek-progress-container">
        <div class="ek-progress-bar" style="width:{pct}%;background:linear-gradient(90deg,{color},{color}cc)"></div>
    </div>''', unsafe_allow_html=True)


def _badge(text: str, color: str):
    """Renkli badge."""
    bg = f"{color}18"
    return f'<span class="ek-badge" style="background:{bg};color:{color}">{text}</span>'


def _renk_bandi_badge(puan: float) -> str:
    """Puana gore renk bandi badge'i."""
    band = get_renk_bandi(puan)
    return _badge(f"{band['label']} ({puan:.0f})", band["color"])


def _meter_row(label: str, value: int, max_val: int = 5):
    """Motivasyon meter satiri."""
    pct = (value / max_val * 100) if max_val > 0 else 0
    colors = {1: "#ef4444", 2: "#f97316", 3: "#eab308", 4: "#22c55e", 5: "#10b981"}
    color = colors.get(value, "#6366f1")
    return f'''
    <div class="ek-meter">
        <div class="ek-meter-label">{label}</div>
        <div class="ek-meter-bar-bg">
            <div class="ek-meter-bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{color},{color}bb)"></div>
        </div>
        <div class="ek-meter-value">{value}/{max_val}</div>
    </div>'''


# ============================================================
# SEKME 1: DASHBOARD
# ============================================================

def _render_dashboard(store: EKDataStore):
    """Ana dashboard - genel bakis."""
    ogrenciler = store.load_list("ogrenciler")
    gorusmeler = store.load_list("gorusmeler")
    hedefler = store.load_list("hedefler")
    planlar = store.load_list("haftalik_planlar")
    motivasyonlar = store.load_list("motivasyon")
    denemeler = _load_all_deneme_list(store)

    aktif_ogrenci = [o for o in ogrenciler if o.get("durum") == "Aktif"]
    planli_gorusme = [g for g in gorusmeler if g.get("durum") == "Planli"]
    devam_hedef = [h for h in hedefler if h.get("durum") == "Devam Ediyor"]
    tamamlanan_hedef = [h for h in hedefler if h.get("durum") == "Tamamlandi"]

    # Diamond stats
    _diamond_stats([
        ("👥", str(len(aktif_ogrenci)), "Aktif Ogrenci", "#6366f1"),
        ("📅", str(len(planli_gorusme)), "Planli Gorusme", "#06b6d4"),
        ("🎯", str(len(devam_hedef)), "Aktif Hedef", "#f59e0b"),
        ("✅", str(len(tamamlanan_hedef)), "Tamamlanan Hedef", "#10b981"),
        ("📊", str(len(denemeler)), "Deneme Analizi", "#8b5cf6"),
        ("📋", str(len(planlar)), "Haftalik Plan", "#3b82f6"),
    ])

    st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)

    # Coaching Wheel
    st.markdown("""
    <div class="ek-glass">
        <div style="text-align:center;margin-bottom:8px">
            <span style="font-size:1.1rem;font-weight:800;
                background:linear-gradient(135deg,#4f46e5,#7c3aed);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                Kocluk Alanlari
            </span>
            <div style="font-size:0.78rem;color:#64748b;margin-top:2px">
                9 temel alan ile butunsel ogrenci gelisimi
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    _coaching_wheel()

    col1, col2 = st.columns(2)

    with col1:
        styled_section("Yaklasan Gorusmeler", "#6366f1")
        bugun = date.today().isoformat()
        yaklasan = sorted(
            [g for g in planli_gorusme if g.get("tarih", "") >= bugun],
            key=lambda x: x.get("tarih", "")
        )[:5]
        if not yaklasan:
            styled_info_banner("Planli gorusme bulunmuyor.", "info", "📅")
        else:
            html = '<div class="ek-timeline">'
            for g in yaklasan:
                html += f'''
                <div class="ek-timeline-item">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div>
                            <div style="font-weight:700;color:#94A3B8;font-size:0.88rem">{g.get("ogrenci_adi","")}</div>
                            <div style="font-size:0.75rem;color:#64748b">{g.get("konu","")}</div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-weight:600;color:#6366f1;font-size:0.8rem">{g.get("tarih","")}</div>
                            <div style="font-size:0.72rem;color:#94a3b8">{g.get("saat","")}</div>
                        </div>
                    </div>
                </div>'''
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

    with col2:
        styled_section("Hedef Ilerleme Ozeti", "#10b981")
        if not devam_hedef:
            styled_info_banner("Aktif hedef bulunmuyor.", "info", "🎯")
        else:
            for h in devam_hedef[:5]:
                pct = h.get("ilerleme_yuzdesi", 0)
                st.markdown(f'''
                <div class="ek-card" style="padding:14px 16px">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                        <span style="font-weight:700;font-size:0.85rem;color:#94A3B8">{h.get("baslik","")}</span>
                        <span style="font-weight:700;color:#6366f1;font-size:0.85rem">%{pct}</span>
                    </div>
                    <div style="font-size:0.72rem;color:#64748b;margin-bottom:6px">{h.get("ogrenci_adi","")}</div>
                </div>''', unsafe_allow_html=True)
                _progress_bar(pct)

    # Son deneme sonuclari
    if denemeler:
        st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
        styled_section("Son Deneme Sonuclari", "#8b5cf6")
        son_denemeler = sorted(denemeler, key=lambda x: x.get("tarih", ""), reverse=True)[:5]
        cols = st.columns(len(son_denemeler)) if son_denemeler else []
        for col, d in zip(cols, son_denemeler):
            band = get_renk_bandi(d.get("puan", 0))
            band_badge_html = _renk_bandi_badge(d.get("puan", 0))
            # f-string'i tek satıra dök — indent'ler markdown tarafından code block olarak algılanmasın
            _card_html = (
                f'<div class="ek-card" style="text-align:center;border-top:3px solid {band["color"]}">'
                f'<div style="font-weight:700;font-size:0.82rem;color:#94A3B8;margin-bottom:4px">{d.get("ogrenci_adi","")}</div>'
                f'<div style="font-size:0.72rem;color:#64748b;margin-bottom:8px">{d.get("sinav_adi","")}</div>'
                f'<div style="font-size:1.5rem;font-weight:800;color:{band["color"]}">{d.get("net",0)}</div>'
                f'<div style="font-size:0.7rem;color:#94a3b8">Net</div>'
                f'<div style="margin-top:4px">{band_badge_html}</div>'
                f'<div style="margin-top:6px">{_badge(band["label"], band["color"])}</div>'
                f'</div>'
            )
            col.markdown(_card_html, unsafe_allow_html=True)


# ============================================================
# SEKME 2: OGRENCI YONETIMI
# ============================================================

def _render_ogrenci_yonetimi(store: EKDataStore):
    """Kocluk ogrenci kayit ve yonetimi."""
    styled_section("Ogrenci Kocluk Yonetimi", "#6366f1")

    sub1, sub2 = st.tabs(["📋 Ogrenci Listesi", "➕ Yeni Kayit"])

    with sub1:
        ogrenciler = store.load_list("ogrenciler")
        if not ogrenciler:
            styled_info_banner("Henuz kocluk ogrencisi eklenmemis. 'Yeni Kayit' sekmesinden ekleyebilirsiniz.", "info", "👥")
        else:
            # Filtreler
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                f_sinif = st.selectbox("Sinif Filtresi", ["Tumu"] + sorted(set(o.get("sinif","") for o in ogrenciler if o.get("sinif"))), key="ek_f_sinif")
            with fc2:
                f_durum = st.selectbox("Durum Filtresi", ["Tumu", "Aktif", "Pasif", "Mezun"], key="ek_f_durum")
            with fc3:
                f_arama = st.text_input("Ara (ad/soyad)", key="ek_f_arama")

            filtered = ogrenciler
            if f_sinif != "Tumu":
                filtered = [o for o in filtered if o.get("sinif") == f_sinif]
            if f_durum != "Tumu":
                filtered = [o for o in filtered if o.get("durum") == f_durum]
            if f_arama:
                q = f_arama.lower()
                filtered = [o for o in filtered if q in o.get("ad","").lower() or q in o.get("soyad","").lower()]

            st.markdown(f"**{len(filtered)}** ogrenci listeleniyor")

            for o in filtered:
                mv = o.get("motivasyon_seviyesi", 3)
                mv_colors = {1:"#ef4444", 2:"#f97316", 3:"#eab308", 4:"#22c55e", 5:"#10b981"}
                mv_color = mv_colors.get(mv, "#6366f1")
                durum_color = "#10b981" if o.get("durum") == "Aktif" else "#94a3b8"
                guclu = ", ".join(o.get("guclu_dersler", [])[:3]) or "-"
                zayif = ", ".join(o.get("zayif_dersler", [])[:3]) or "-"

                st.markdown(f'''
                <div class="ek-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                            <div style="font-size:1rem;font-weight:800;color:#94A3B8">
                                {o.get("ad","")} {o.get("soyad","")}
                            </div>
                            <div style="font-size:0.78rem;color:#64748b;margin-top:2px">
                                {o.get("sinif","")}/{o.get("sube","")} - No: {o.get("numara","")}
                                &nbsp;|&nbsp; Koc: {o.get("koc_adi","Atanmadi")}
                            </div>
                        </div>
                        <div style="text-align:right">
                            {_badge(o.get("durum","Aktif"), durum_color)}
                            <div style="margin-top:6px;font-size:0.72rem;color:#94a3b8">
                                Motivasyon: <span style="color:{mv_color};font-weight:700">{mv}/5</span>
                            </div>
                        </div>
                    </div>
                    <div style="display:flex;gap:20px;margin-top:10px;font-size:0.78rem">
                        <div><span style="color:#10b981;font-weight:600">Guclu:</span> {guclu}</div>
                        <div><span style="color:#ef4444;font-weight:600">Zayif:</span> {zayif}</div>
                        <div><span style="color:#6366f1;font-weight:600">Hedef:</span> {o.get("hedef_sinav","") or "-"}</div>
                    </div>
                </div>''', unsafe_allow_html=True)

                # Detay/Sil butonlari
                bc1, bc2, bc3 = st.columns([3, 1, 1])
                with bc2:
                    if st.button("✏️ Duzenle", key=f"ek_edit_{o['id']}", use_container_width=True):
                        st.session_state["_ek_edit_ogr"] = o["id"]
                        st.rerun()
                with bc3:
                    if st.button("🗑️ Sil", key=f"ek_del_{o['id']}", use_container_width=True):
                        store.delete_item("ogrenciler", o["id"])
                        st.success("Ogrenci silindi.")
                        st.rerun()

            # Duzenleme modu
            edit_id = st.session_state.get("_ek_edit_ogr")
            if edit_id:
                ogr = store.get_item("ogrenciler", edit_id)
                if ogr:
                    st.markdown("---")
                    styled_section(f"Duzenle: {ogr.get('ad','')} {ogr.get('soyad','')}", "#f59e0b")
                    with st.form(f"ek_edit_form_{edit_id}"):
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            e_ad = st.text_input("Ad", ogr.get("ad",""))

                            e_sinif = st.text_input("Sinif", ogr.get("sinif",""))

                            e_koc = st.text_input("Koc Adi", ogr.get("koc_adi",""))

                            e_hedef = st.text_input("Hedef Sinav", ogr.get("hedef_sinav",""))

                        with ec2:
                            e_soyad = st.text_input("Soyad", ogr.get("soyad",""))

                            e_sube = st.text_input("Sube", ogr.get("sube",""))

                            e_numara = st.text_input("Numara", ogr.get("numara",""))

                            e_durum = st.selectbox("Durum", ["Aktif","Pasif","Mezun"], index=["Aktif","Pasif","Mezun"].index(ogr.get("durum","Aktif")) if ogr.get("durum","Aktif") in ["Aktif","Pasif","Mezun"] else 0)

                        e_motivasyon = st.slider("Motivasyon Seviyesi", 1, 5, ogr.get("motivasyon_seviyesi",3))

                        e_guclu = st.multiselect("Guclu Dersler", DERS_LISTESI, default=ogr.get("guclu_dersler",[]))

                        e_zayif = st.multiselect("Zayif Dersler", DERS_LISTESI, default=ogr.get("zayif_dersler",[]))

                        e_not = st.text_area("Notlar", ogr.get("notlar",""))

                        if st.form_submit_button("Guncelle", type="primary", use_container_width=True):
                            store.update_item("ogrenciler", edit_id, {
                                "ad": e_ad, "soyad": e_soyad, "sinif": e_sinif, "sube": e_sube,
                                "numara": e_numara, "koc_adi": e_koc, "durum": e_durum,
                                "hedef_sinav": e_hedef, "motivasyon_seviyesi": e_motivasyon,
                                "guclu_dersler": e_guclu, "zayif_dersler": e_zayif, "notlar": e_not,
                            })
                            st.session_state.pop("_ek_edit_ogr", None)
                            st.success("Ogrenci guncellendi!")
                            st.rerun()

    with sub2:
        styled_info_banner(
            "Ogrenci ve veli bilgileri Kurumsal Organizasyon > Iletisim > Sinif Listeleri'nden otomatik yuklenir.",
            "info", "🏢"
        )

        # Sinif listesinden ogrenci sec
        sinif_sube = get_sinif_sube_listesi()
        siniflar = sinif_sube.get("siniflar", [])
        subeler = sinif_sube.get("subeler", [])

        fc1, fc2 = st.columns(2)
        with fc1:
            f_sinif = st.selectbox("Sinif", ["Tumu"] + siniflar, key="ek_ns_sinif")
        with fc2:
            f_sube = st.selectbox("Sube", ["Tumu"] + subeler, key="ek_ns_sube")

        # Shared data'dan ogrenci listesini al
        sinif_f = None if f_sinif == "Tumu" else f_sinif
        sube_f = None if f_sube == "Tumu" else f_sube
        ogr_secenekler = get_student_display_options(sinif_filter=sinif_f, sube_filter=sube_f, include_empty=True)

        # Zaten eklenmis ogrenci ID'lerini bul (duplikasyon engeli)
        mevcut_ids = {o.get("ogrenci_id","") for o in store.load_list("ogrenciler")}

        sec_label = st.selectbox("Ogrenci Sec (Sinif Listesinden)", list(ogr_secenekler.keys()), key="ek_ns_ogr")

        if sec_label and sec_label != "-- Secim yapin --":
            sec_ogr = ogr_secenekler[sec_label]
            ogr_id = sec_ogr.get("id", "")

            if ogr_id in mevcut_ids:
                styled_info_banner("Bu ogrenci zaten kocluk programina ekli.", "warning", "⚠️")
            else:
                # Ogrenci bilgilerini goster
                st.markdown(f'''
                <div class="ek-glass">
                    <div style="display:flex;align-items:center;gap:16px">
                        <div style="width:50px;height:50px;border-radius:50%;
                            background:linear-gradient(135deg,#6366f1,#8b5cf6);
                            display:flex;align-items:center;justify-content:center;
                            font-size:1.2rem;color:white;font-weight:800">
                            {sec_ogr.get("ad","X")[0]}{sec_ogr.get("soyad","X")[0]}
                        </div>
                        <div>
                            <div style="font-size:1rem;font-weight:800;color:#94A3B8">
                                {sec_ogr.get("ad","")} {sec_ogr.get("soyad","")}
                            </div>
                            <div style="font-size:0.82rem;color:#64748b">
                                Sinif: {sec_ogr.get("sinif","")}/{sec_ogr.get("sube","")}
                                &nbsp;|&nbsp; No: {sec_ogr.get("numara","")}
                                &nbsp;|&nbsp; Veli: {sec_ogr.get("veli_adi","") or sec_ogr.get("anne_adi","") or "-"}
                                &nbsp;|&nbsp; Tel: {sec_ogr.get("veli_telefon","") or sec_ogr.get("anne_telefon","") or "-"}
                            </div>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

                # Kocluk bilgileri formu
                with st.form("ek_yeni_ogrenci", clear_on_submit=True):
                    st.markdown("##### Kocluk Bilgileri")
                    c1, c2 = st.columns(2)
                    with c1:
                        n_koc = st.text_input("Koc Adi")

                        n_hedef_sinav = st.text_input("Hedef Sinav (LGS/TYT/AYT)")
                    with c2:
                        n_hedef_puan = st.text_input("Hedef Puan")
                        n_hedef_sira = st.text_input("Hedef Siralama")
                    n_motivasyon = st.slider("Motivasyon Seviyesi", 1, 5, 3, key="ek_n_motiv")
                    n_guclu = st.multiselect("Guclu Dersler", DERS_LISTESI, key="ek_n_guclu")
                    n_zayif = st.multiselect("Zayif Dersler", DERS_LISTESI, key="ek_n_zayif")
                    n_not = st.text_area("Notlar")


                    if st.form_submit_button("Kocluk Programina Ekle", type="primary", use_container_width=True):
                        # Veli bilgisini belirle (fallback sirasi: veli_adi > anne > baba)
                        veli_adi = sec_ogr.get("veli_adi", "")
                        if not veli_adi:
                            anne = f"{sec_ogr.get('anne_adi','')} {sec_ogr.get('anne_soyadi','')}".strip()
                            baba = f"{sec_ogr.get('baba_adi','')} {sec_ogr.get('baba_soyadi','')}".strip()
                            veli_adi = anne or baba
                        veli_tel = sec_ogr.get("veli_telefon","") or sec_ogr.get("anne_telefon","") or sec_ogr.get("baba_telefon","")

                        yeni = KoclukOgrenci(
                            ogrenci_id=ogr_id,
                            ad=sec_ogr.get("ad",""),
                            soyad=sec_ogr.get("soyad",""),
                            sinif=str(sec_ogr.get("sinif","")),
                            sube=sec_ogr.get("sube",""),
                            numara=sec_ogr.get("numara",""),
                            koc_adi=n_koc,
                            hedef_sinav=n_hedef_sinav,
                            hedef_puan=n_hedef_puan,
                            hedef_sira=n_hedef_sira,
                            motivasyon_seviyesi=n_motivasyon,
                            guclu_dersler=n_guclu,
                            zayif_dersler=n_zayif,
                            veli_adi=veli_adi,
                            veli_telefon=veli_tel,
                            notlar=n_not,
                        )
                        store.add_item("ogrenciler", yeni.to_dict())
                        st.success(f"{sec_ogr.get('ad','')} {sec_ogr.get('soyad','')} kocluk programina eklendi!")
                        st.rerun()


# ============================================================
# SEKME 3: GORUSME YONETIMI
# ============================================================

def _render_gorusme_yonetimi(store: EKDataStore):
    """Koc-ogrenci gorusme planlama ve takibi."""
    styled_section("Gorusme Yonetimi", "#06b6d4")

    sub1, sub2 = st.tabs(["📋 Gorusme Takibi", "➕ Yeni Gorusme"])

    with sub1:
        gorusmeler = store.load_list("gorusmeler")
        if not gorusmeler:
            styled_info_banner("Henuz gorusme kaydi yok. 'Yeni Gorusme' sekmesinden olusturabilirsiniz.", "info", "📅")
        else:
            fc1, fc2 = st.columns(2)
            with fc1:
                f_durum = st.selectbox("Durum", ["Tumu"] + GORUSME_DURUMLARI, key="ek_g_durum")
            with fc2:
                f_alan = st.selectbox("Kocluk Alani", ["Tumu"] + KOCLUK_ALANLARI, key="ek_g_alan")

            filtered = gorusmeler
            if f_durum != "Tumu":
                filtered = [g for g in filtered if g.get("durum") == f_durum]
            if f_alan != "Tumu":
                filtered = [g for g in filtered if g.get("kocluk_alani") == f_alan]

            filtered = sorted(filtered, key=lambda x: x.get("tarih", ""), reverse=True)

            durum_colors = {"Planli":"#3b82f6", "Tamamlandi":"#10b981", "Iptal":"#ef4444", "Ertelendi":"#f59e0b"}

            for g in filtered:
                dc = durum_colors.get(g.get("durum",""), "#94a3b8")
                st.markdown(f'''
                <div class="ek-card" style="border-left:4px solid {dc}">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                            <div style="font-weight:700;font-size:0.92rem;color:#94A3B8">
                                {g.get("ogrenci_adi","")}
                            </div>
                            <div style="font-size:0.78rem;color:#64748b;margin-top:2px">
                                {g.get("konu","Belirtilmemis")} &nbsp;|&nbsp;
                                {g.get("kocluk_alani","Genel")} &nbsp;|&nbsp;
                                {g.get("turu","")} &nbsp;|&nbsp; {g.get("sure_dk",45)} dk
                            </div>
                        </div>
                        <div style="text-align:right">
                            {_badge(g.get("durum",""), dc)}
                            <div style="font-size:0.78rem;color:#6366f1;font-weight:600;margin-top:6px">
                                {g.get("tarih","")} - {g.get("saat","")}
                            </div>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

                # Gorusme notlarini goster / durum guncelle
                with st.expander(f"Detay: {g.get('ogrenci_adi','')} - {g.get('tarih','')}", expanded=False):
                    if g.get("gorusme_notlari"):
                        st.markdown(f"**Gorusme Notlari:** {g['gorusme_notlari']}")
                    if g.get("eylem_plani"):
                        st.markdown(f"**Eylem Plani:** {g['eylem_plani']}")
                    if g.get("sonraki_gorusme"):
                        st.markdown(f"**Sonraki Gorusme:** {g['sonraki_gorusme']}")

                    dc1, dc2, dc3 = st.columns(3)
                    with dc1:
                        yeni_durum = st.selectbox("Durum Guncelle", GORUSME_DURUMLARI,
                            index=GORUSME_DURUMLARI.index(g.get("durum","Planli")) if g.get("durum","Planli") in GORUSME_DURUMLARI else 0,
                            key=f"ek_gd_{g['id']}")
                    with dc2:
                        yeni_not = st.text_area("Gorusme Notu Ekle", g.get("gorusme_notlari",""), key=f"ek_gn_{g['id']}")
                    with dc3:
                        yeni_eylem = st.text_area("Eylem Plani", g.get("eylem_plani",""), key=f"ek_ge_{g['id']}")

                    if st.button("Guncelle", key=f"ek_gu_{g['id']}", type="primary", use_container_width=True):
                        store.update_item("gorusmeler", g["id"], {
                            "durum": yeni_durum,
                            "gorusme_notlari": yeni_not,
                            "eylem_plani": yeni_eylem,
                        })
                        st.success("Gorusme guncellendi!")
                        st.rerun()

    with sub2:
        ogrenciler = store.load_list("ogrenciler")
        ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

        with st.form("ek_yeni_gorusme", clear_on_submit=True):
            st.markdown("##### Yeni Gorusme Planla")
            c1, c2 = st.columns(2)
            with c1:
                g_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts.keys()), key="ek_ng_ogr")
                g_tarih = st.date_input("Tarih *", value=date.today(), key="ek_ng_tarih")
                g_tur = st.selectbox("Gorusme Turu", GORUSME_TURLERI, key="ek_ng_tur")
                g_alan = st.selectbox("Kocluk Alani", KOCLUK_ALANLARI, key="ek_ng_alan")
            with c2:
                g_koc = st.text_input("Koc Adi", key="ek_ng_koc")
                g_saat = st.selectbox("Saat", ["09:00","09:30","10:00","10:30","11:00","11:30","12:00","13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30","17:00"], key="ek_ng_saat")
                g_sure = st.number_input("Sure (dk)", min_value=15, max_value=120, value=45, step=15, key="ek_ng_sure")
            g_konu = st.text_input("Konu", key="ek_ng_konu")
            g_not = st.text_area("Notlar", key="ek_ng_not")

            if st.form_submit_button("Gorusme Olustur", type="primary", use_container_width=True):
                if g_ogr == "Seciniz":
                    st.error("Lutfen bir ogrenci seciniz.")
                else:
                    yeni = KoclukGorusme(
                        ogrenci_id=ogr_opts[g_ogr],
                        ogrenci_adi=g_ogr,
                        koc_adi=g_koc,
                        tarih=g_tarih.isoformat(),
                        saat=g_saat,
                        sure_dk=g_sure,
                        turu=g_tur,
                        kocluk_alani=g_alan,
                        konu=g_konu,
                        gorusme_notlari=g_not,
                    )
                    store.add_item("gorusmeler", yeni.to_dict())
                    st.success("Gorusme basariyla olusturuldu!")
                    st.rerun()


# ============================================================
# SEKME 4: HEDEF YONETIMI
# ============================================================

def _render_hedef_yonetimi(store: EKDataStore):
    """Ogrenci hedef belirleme ve takibi."""
    styled_section("Hedef Belirleme & Takip", "#f59e0b")

    sub1, sub2 = st.tabs(["🎯 Hedef Takibi", "➕ Yeni Hedef"])

    with sub1:
        hedefler = store.load_list("hedefler")
        if not hedefler:
            styled_info_banner("Henuz hedef tanimlanmamis.", "info", "🎯")
        else:
            fc1, fc2 = st.columns(2)
            with fc1:
                f_durum = st.selectbox("Durum", ["Tumu"] + HEDEF_DURUMLARI, key="ek_h_durum")
            with fc2:
                f_onc = st.selectbox("Oncelik", ["Tumu"] + HEDEF_ONCELIKLERI, key="ek_h_onc")

            filtered = hedefler
            if f_durum != "Tumu":
                filtered = [h for h in filtered if h.get("durum") == f_durum]
            if f_onc != "Tumu":
                filtered = [h for h in filtered if h.get("oncelik") == f_onc]

            oncelik_colors = {"Dusuk":"#94a3b8", "Orta":"#3b82f6", "Yuksek":"#f59e0b", "Kritik":"#ef4444"}
            durum_colors = {"Beklemede":"#94a3b8", "Devam Ediyor":"#3b82f6", "Tamamlandi":"#10b981", "Iptal":"#ef4444"}

            for h in filtered:
                oc = oncelik_colors.get(h.get("oncelik",""), "#94a3b8")
                dc = durum_colors.get(h.get("durum",""), "#94a3b8")
                pct = h.get("ilerleme_yuzdesi", 0)

                st.markdown(f'''
                <div class="ek-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                            <div style="font-weight:800;font-size:0.95rem;color:#94A3B8">{h.get("baslik","")}</div>
                            <div style="font-size:0.78rem;color:#64748b;margin-top:2px">{h.get("ogrenci_adi","")}</div>
                            <div style="font-size:0.75rem;color:#94a3b8;margin-top:2px">
                                {h.get("kategori","")} &nbsp;|&nbsp; {h.get("baslangic_tarihi","")} - {h.get("bitis_tarihi","Belirtilmemis")}
                            </div>
                        </div>
                        <div style="text-align:right">
                            {_badge(h.get("oncelik",""), oc)}
                            <div style="margin-top:4px">{_badge(h.get("durum",""), dc)}</div>
                        </div>
                    </div>
                    <div style="margin-top:10px">
                        <div style="display:flex;justify-content:space-between;font-size:0.78rem;margin-bottom:4px">
                            <span style="color:#64748b">Ilerleme</span>
                            <span style="font-weight:700;color:#6366f1">%{pct}</span>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)
                _progress_bar(pct)

                with st.expander(f"Guncelle: {h.get('baslik','')}", expanded=False):
                    uc1, uc2, uc3 = st.columns(3)
                    with uc1:
                        u_durum = st.selectbox("Durum", HEDEF_DURUMLARI,
                            index=HEDEF_DURUMLARI.index(h.get("durum","Beklemede")) if h.get("durum") in HEDEF_DURUMLARI else 0,
                            key=f"ek_hd_{h['id']}")
                    with uc2:
                        u_ilerleme = st.slider("Ilerleme %", 0, 100, pct, key=f"ek_hi_{h['id']}")
                    with uc3:
                        u_not = st.text_area("Not", h.get("notlar",""), key=f"ek_hn_{h['id']}")
                    if st.button("Guncelle", key=f"ek_hu_{h['id']}", type="primary"):
                        store.update_item("hedefler", h["id"], {
                            "durum": u_durum, "ilerleme_yuzdesi": u_ilerleme, "notlar": u_not,
                        })
                        st.success("Hedef guncellendi!")
                        st.rerun()

    with sub2:
        ogrenciler = store.load_list("ogrenciler")
        ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

        with st.form("ek_yeni_hedef", clear_on_submit=True):
            st.markdown("##### Yeni Hedef Tanimla")
            c1, c2 = st.columns(2)
            with c1:
                h_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts.keys()), key="ek_nh_ogr")
                h_baslik = st.text_input("Hedef Basligi *", key="ek_nh_baslik")
                h_kategori = st.selectbox("Kategori", KOCLUK_ALANLARI, key="ek_nh_kat")
            with c2:
                h_oncelik = st.selectbox("Oncelik", HEDEF_ONCELIKLERI, index=1, key="ek_nh_onc")
                h_baslangic = st.date_input("Baslangic", value=date.today(), key="ek_nh_bas")
                h_bitis = st.date_input("Bitis", value=date.today()+timedelta(days=30), key="ek_nh_bit")
            h_aciklama = st.text_area("Aciklama", key="ek_nh_ack")

            if st.form_submit_button("Hedef Olustur", type="primary", use_container_width=True):
                if h_ogr == "Seciniz" or not h_baslik:
                    st.error("Ogrenci ve hedef basligi zorunludur.")
                else:
                    yeni = HedefKaydi(
                        ogrenci_id=ogr_opts[h_ogr], ogrenci_adi=h_ogr,
                        baslik=h_baslik, aciklama=h_aciklama, kategori=h_kategori,
                        oncelik=h_oncelik, baslangic_tarihi=h_baslangic.isoformat(),
                        bitis_tarihi=h_bitis.isoformat(),
                    )
                    store.add_item("hedefler", yeni.to_dict())
                    st.success("Hedef basariyla olusturuldu!")
                    st.rerun()


# ============================================================
# SEKME 5: HAFTALIK PLAN
# ============================================================

def _render_haftalik_plan(store: EKDataStore):
    """Haftalik calisma plani olusturma ve takibi."""
    styled_section("Haftalik Calisma Plani", "#3b82f6")

    sub1, sub2 = st.tabs(["📅 Plan Goruntule", "➕ Yeni Plan"])

    with sub1:
        ogrenciler = store.load_list("ogrenciler")
        ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

        if not ogr_opts:
            styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
            return

        sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_hp_ogr")
        ogr_id = ogr_opts.get(sec_ogr, "")
        planlar = store.get_by_ogrenci("haftalik_planlar", ogr_id) if ogr_id else []

        if not planlar:
            styled_info_banner(f"{sec_ogr} icin plan bulunmuyor.", "info", "📅")
        else:
            for plan in sorted(planlar, key=lambda x: x.get("hafta_baslangic",""), reverse=True):
                tamamlanma = 0
                etkinlikler = plan.get("etkinlikler", [])
                if etkinlikler:
                    tamamlanan = sum(1 for e in etkinlikler if e.get("tamamlandi"))
                    tamamlanma = round((tamamlanan / len(etkinlikler)) * 100, 1)

                st.markdown(f'''
                <div class="ek-glass">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
                        <div>
                            <div style="font-weight:800;font-size:1rem;color:#94A3B8">
                                Hafta: {plan.get("hafta_baslangic","")} - {plan.get("hafta_bitis","")}
                            </div>
                            <div style="font-size:0.78rem;color:#64748b">
                                {len(etkinlikler)} etkinlik &nbsp;|&nbsp; Tamamlanma: %{tamamlanma}
                            </div>
                        </div>
                        <div style="font-size:1.5rem;font-weight:800;color:#6366f1">%{tamamlanma}</div>
                    </div>
                </div>''', unsafe_allow_html=True)
                _progress_bar(tamamlanma)

                # Plan tablosu
                if etkinlikler:
                    # Gunlere gore grupla
                    gun_map = {g: [] for g in HAFTA_GUNLERI}
                    for e in etkinlikler:
                        gun = e.get("gun", "")
                        if gun in gun_map:
                            gun_map[gun].append(e)

                    for gun in HAFTA_GUNLERI:
                        items = gun_map[gun]
                        if not items:
                            continue
                        st.markdown(f"**{gun}**")
                        for e in items:
                            check = "✅" if e.get("tamamlandi") else "⬜"
                            st.markdown(f'''
                            <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;
                                background:#111827;border-radius:8px;margin-bottom:4px;font-size:0.82rem">
                                <span>{check}</span>
                                <span style="font-weight:600;color:#6366f1;min-width:60px">{e.get("saat","")}</span>
                                <span class="ek-badge" style="background:#eef2ff;color:#4f46e5">{e.get("ders","")}</span>
                                <span style="color:#475569">{e.get("konu","")}</span>
                                <span style="color:#94a3b8;margin-left:auto">{e.get("sure_dk",60)} dk</span>
                            </div>''', unsafe_allow_html=True)

                    # Etkinlik tamamlama
                    with st.expander("Etkinlik Tamamla / Guncelle"):
                        for i, e in enumerate(etkinlikler):
                            ck = st.checkbox(
                                f"{e.get('gun','')} {e.get('saat','')} - {e.get('ders','')} {e.get('konu','')}",
                                value=e.get("tamamlandi", False),
                                key=f"ek_pet_{plan['id']}_{i}"
                            )
                            etkinlikler[i]["tamamlandi"] = ck

                        if st.button("Plani Guncelle", key=f"ek_pu_{plan['id']}", type="primary"):
                            store.update_item("haftalik_planlar", plan["id"], {"etkinlikler": etkinlikler})
                            st.success("Plan guncellendi!")
                            st.rerun()

    with sub2:
        ogrenciler = store.load_list("ogrenciler")
        ogr_opts2 = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

        st.markdown("##### Yeni Haftalik Plan Olustur")

        p_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts2.keys()), key="ek_np_ogr")
        pc1, pc2 = st.columns(2)
        with pc1:
            p_bas = st.date_input("Hafta Baslangic", value=date.today(), key="ek_np_bas")
        with pc2:
            p_bit = st.date_input("Hafta Bitis", value=date.today()+timedelta(days=6), key="ek_np_bit")

        st.markdown("---")
        st.markdown("**Etkinlik Ekle**")

        if "ek_plan_etkinlikler" not in st.session_state:
            st.session_state["ek_plan_etkinlikler"] = []

        ec1, ec2, ec3, ec4 = st.columns(4)
        with ec1:
            e_gun = st.selectbox("Gun", HAFTA_GUNLERI, key="ek_ne_gun")
        with ec2:
            e_saat = st.selectbox("Saat", SAAT_DILIMLERI, key="ek_ne_saat")
        with ec3:
            e_ders = st.selectbox("Ders", DERS_LISTESI, key="ek_ne_ders")
        with ec4:
            e_tur = st.selectbox("Etkinlik Turu", ETKINLIK_TURLERI, key="ek_ne_tur")

        ec5, ec6 = st.columns(2)
        with ec5:
            e_konu = st.text_input("Konu", key="ek_ne_konu")
        with ec6:
            e_sure = st.number_input("Sure (dk)", min_value=15, max_value=180, value=60, step=15, key="ek_ne_sure")

        if st.button("Etkinlik Ekle", key="ek_ne_ekle"):
            st.session_state["ek_plan_etkinlikler"].append({
                "gun": e_gun, "saat": e_saat, "ders": e_ders,
                "etkinlik_turu": e_tur, "konu": e_konu,
                "sure_dk": e_sure, "tamamlandi": False,
            })
            st.rerun()

        # Eklenmis etkinlikleri goster
        etk_list = st.session_state.get("ek_plan_etkinlikler", [])
        if etk_list:
            st.markdown(f"**{len(etk_list)} etkinlik eklendi:**")
            for i, e in enumerate(etk_list):
                st.markdown(f'''
                <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;
                    background:#f0f0ff;border-radius:8px;margin-bottom:4px;font-size:0.82rem">
                    <span style="font-weight:600;color:#6366f1">{e["gun"]}</span>
                    <span>{e["saat"]}</span>
                    <span class="ek-badge" style="background:#eef2ff;color:#4f46e5">{e["ders"]}</span>
                    <span>{e["konu"]}</span>
                    <span style="color:#94a3b8;margin-left:auto">{e["sure_dk"]} dk</span>
                </div>''', unsafe_allow_html=True)

        if st.button("Plani Kaydet", type="primary", use_container_width=True, key="ek_np_kaydet"):
            if p_ogr == "Seciniz":
                st.error("Lutfen bir ogrenci seciniz.")
            elif not etk_list:
                st.error("En az bir etkinlik ekleyiniz.")
            else:
                toplam_saat = sum(e.get("sure_dk", 60) for e in etk_list) / 60
                yeni = HaftalikPlan(
                    ogrenci_id=ogr_opts2[p_ogr], ogrenci_adi=p_ogr,
                    hafta_baslangic=p_bas.isoformat(), hafta_bitis=p_bit.isoformat(),
                    etkinlikler=etk_list, toplam_saat=round(toplam_saat, 1),
                )
                store.add_item("haftalik_planlar", yeni.to_dict())
                st.session_state["ek_plan_etkinlikler"] = []
                st.success("Haftalik plan olusturuldu!")
                st.rerun()


# ============================================================
# SEKME 6: MOTIVASYON & OZGUVEN TAKIBI
# ============================================================

def _render_motivasyon_takibi(store: EKDataStore):
    """Motivasyon, ozguven, stres takibi."""
    styled_section("Motivasyon & Ozguven Takibi", "#ec4899")

    sub1, sub2 = st.tabs(["📊 Takip Paneli", "➕ Yeni Kayit"])

    with sub1:
        ogrenciler = store.load_list("ogrenciler")
        ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

        if not ogr_opts:
            styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
            return

        sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_mt_ogr")
        ogr_id = ogr_opts.get(sec_ogr, "")
        kayitlar = store.get_by_ogrenci("motivasyon", ogr_id) if ogr_id else []
        kayitlar = sorted(kayitlar, key=lambda x: x.get("tarih",""), reverse=True)

        if not kayitlar:
            styled_info_banner(f"{sec_ogr} icin motivasyon kaydi bulunmuyor.", "info", "📊")
        else:
            # Son kayit detay
            son = kayitlar[0]
            st.markdown(f'''
            <div class="ek-glass">
                <div style="text-align:center;margin-bottom:16px">
                    <div style="font-weight:800;font-size:1rem;color:#94A3B8">Son Degerlendirme: {son.get("tarih","")}</div>
                    <div style="font-size:0.78rem;color:#64748b;margin-top:2px">Genel Ortalama</div>
                    <div style="font-size:2rem;font-weight:900;
                        background:linear-gradient(135deg,#ec4899,#8b5cf6);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                        {MotivasyonKaydi.from_dict(son).ortalama_puan}/5
                    </div>
                </div>
            </div>''', unsafe_allow_html=True)

            # Meter bars
            html = ""
            html += _meter_row("Motivasyon", son.get("motivasyon_puani",3))
            html += _meter_row("Ozguven", son.get("ozguven_puani",3))
            html += _meter_row("Stres", son.get("stres_puani",3))
            html += _meter_row("Enerji", son.get("enerji_puani",3))
            html += _meter_row("Odaklanma", son.get("odaklanma_puani",3))
            html += _meter_row("Mutluluk", son.get("mutluluk_puani",3))
            st.markdown(html, unsafe_allow_html=True)

            # Tarihsel grafik
            if len(kayitlar) > 1:
                st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
                styled_section("Tarihsel Gelisim", "#8b5cf6")
                import pandas as pd
                df = pd.DataFrame([{
                    "Tarih": k.get("tarih",""),
                    "Motivasyon": k.get("motivasyon_puani",3),
                    "Ozguven": k.get("ozguven_puani",3),
                    "Enerji": k.get("enerji_puani",3),
                    "Odaklanma": k.get("odaklanma_puani",3),
                    "Mutluluk": k.get("mutluluk_puani",3),
                } for k in reversed(kayitlar)])
                st.line_chart(df.set_index("Tarih"), height=300)

    with sub2:
        ogrenciler = store.load_list("ogrenciler")
        ogr_opts2 = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

        with st.form("ek_yeni_motivasyon", clear_on_submit=True):
            st.markdown("##### Motivasyon Degerlendirme")
            m_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts2.keys()), key="ek_nm_ogr")
            m_tarih = st.date_input("Tarih", value=date.today(), key="ek_nm_tarih")
            st.markdown("---")
            mc1, mc2 = st.columns(2)
            with mc1:
                m_motiv = st.slider("Motivasyon", 1, 5, 3, key="ek_nm_motiv")
                m_ozguv = st.slider("Ozguven", 1, 5, 3, key="ek_nm_ozguv")
                m_stres = st.slider("Stres Yonetimi", 1, 5, 3, key="ek_nm_stres")
            with mc2:
                m_enerji = st.slider("Enerji", 1, 5, 3, key="ek_nm_enerji")
                m_odak = st.slider("Odaklanma", 1, 5, 3, key="ek_nm_odak")
                m_mutlu = st.slider("Mutluluk", 1, 5, 3, key="ek_nm_mutlu")
            m_not = st.text_area("Notlar / Gozlemler", key="ek_nm_not")

            if st.form_submit_button("Kaydet", type="primary", use_container_width=True):
                if m_ogr == "Seciniz":
                    st.error("Lutfen bir ogrenci seciniz.")
                else:
                    yeni = MotivasyonKaydi(
                        ogrenci_id=ogr_opts2[m_ogr], ogrenci_adi=m_ogr,
                        tarih=m_tarih.isoformat(),
                        motivasyon_puani=m_motiv, ozguven_puani=m_ozguv,
                        stres_puani=m_stres, enerji_puani=m_enerji,
                        odaklanma_puani=m_odak, mutluluk_puani=m_mutlu,
                        notlar=m_not,
                    )
                    store.add_item("motivasyon", yeni.to_dict())
                    st.success("Motivasyon kaydi eklendi!")
                    st.rerun()


# ============================================================
# SEKME 7: DENEME ANALIZI
# ============================================================

def _render_deneme_analizi(store: EKDataStore):
    """Deneme sinavi analiz ve takibi."""
    styled_section("Deneme Analiz & Takip", "#8b5cf6")

    sub1, sub2 = st.tabs(["📊 Analiz Paneli", "➕ Yeni Deneme Kaydi"])

    with sub1:
        ogrenciler = store.load_list("ogrenciler")
        ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

        if not ogr_opts:
            styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
            return

        sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_da_ogr")
        ogr_id = ogr_opts.get(sec_ogr, "")
        denemeler = _load_consolidated_deneme(store, ogr_id)
        denemeler = sorted(denemeler, key=lambda x: x.get("tarih",""), reverse=True)

        if not denemeler:
            styled_info_banner(f"{sec_ogr} icin deneme sonucu bulunmuyor.", "info", "📊")
        else:
            # Genel istatistikler
            son = denemeler[0]
            ort_net = sum(d.get("net",0) for d in denemeler) / len(denemeler) if denemeler else 0
            max_net = max(d.get("net",0) for d in denemeler)
            min_net = min(d.get("net",0) for d in denemeler)

            _diamond_stats([
                ("📝", str(len(denemeler)), "Toplam Deneme", "#6366f1"),
                ("📊", f"{ort_net:.1f}", "Ortalama Net", "#3b82f6"),
                ("🔝", f"{max_net:.1f}", "En Yuksek Net", "#10b981"),
                ("📉", f"{min_net:.1f}", "En Dusuk Net", "#ef4444"),
            ])

            # Deneme listesi
            for d in denemeler:
                band = get_renk_bandi(d.get("puan", 0))
                st.markdown(f'''
                <div class="ek-card" style="border-left:4px solid {band["color"]}">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div>
                            <div style="font-weight:700;font-size:0.9rem;color:#94A3B8">{d.get("sinav_adi","")}</div>
                            <div style="font-size:0.75rem;color:#64748b;margin-top:2px">
                                {d.get("sinav_turu","")} &nbsp;|&nbsp; {d.get("tarih","")}
                            </div>
                            <div style="font-size:0.78rem;margin-top:6px">
                                <span style="color:#10b981;font-weight:600">D: {d.get("dogru",0)}</span> &nbsp;
                                <span style="color:#ef4444;font-weight:600">Y: {d.get("yanlis",0)}</span> &nbsp;
                                <span style="color:#94a3b8;font-weight:600">B: {d.get("bos",0)}</span>
                            </div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-size:1.6rem;font-weight:800;color:{band['color']}">{d.get("net",0)}</div>
                            <div style="font-size:0.7rem;color:#94a3b8">Net</div>
                            <div style="margin-top:4px">{_badge(band["label"], band["color"])}</div>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

                # Ders detaylari
                ders_det = d.get("ders_detaylari", [])
                if ders_det:
                    with st.expander(f"Ders Detaylari - {d.get('sinav_adi','')}", expanded=False):
                        for dd in ders_det:
                            cols = st.columns([2,1,1,1,1])
                            cols[0].markdown(f"**{dd.get('ders','')}**")
                            cols[1].markdown(f"D: {dd.get('dogru',0)}")
                            cols[2].markdown(f"Y: {dd.get('yanlis',0)}")
                            cols[3].markdown(f"B: {dd.get('bos',0)}")
                            cols[4].markdown(f"Net: **{dd.get('net',0)}**")

            # Net trend grafigi
            if len(denemeler) > 1:
                st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
                styled_section("Net Trend Grafigi", "#6366f1")
                import pandas as pd
                df = pd.DataFrame([{
                    "Tarih": d.get("tarih",""),
                    "Net": d.get("net", 0),
                    "Puan": d.get("puan", 0),
                } for d in reversed(denemeler)])
                st.line_chart(df.set_index("Tarih"), height=300)

    with sub2:
        ogrenciler = store.load_list("ogrenciler")
        ogr_opts2 = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

        with st.form("ek_yeni_deneme", clear_on_submit=True):
            st.markdown("##### Yeni Deneme Sonucu Kaydet")
            c1, c2 = st.columns(2)
            with c1:
                d_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts2.keys()), key="ek_nd_ogr")
                d_sinav = st.text_input("Sinav Adi *", key="ek_nd_sinav")
                d_tur = st.selectbox("Sinav Turu", ["TYT","AYT","LGS","Okul Denemesi","Ozel Kurum","Diger"], key="ek_nd_tur")
            with c2:
                d_tarih = st.date_input("Tarih", value=date.today(), key="ek_nd_tarih")
                d_toplam = st.number_input("Toplam Soru", min_value=1, value=120, key="ek_nd_toplam")
                d_siralama = st.number_input("Siralama", min_value=0, value=0, key="ek_nd_sira")

            dc1, dc2, dc3 = st.columns(3)
            with dc1:
                d_dogru = st.number_input("Dogru", min_value=0, value=0, key="ek_nd_dogru")
            with dc2:
                d_yanlis = st.number_input("Yanlis", min_value=0, value=0, key="ek_nd_yanlis")
            with dc3:
                d_bos = st.number_input("Bos", min_value=0, value=0, key="ek_nd_bos")

            d_net = d_dogru - (d_yanlis / 4) if d_yanlis > 0 else float(d_dogru)
            d_puan = (d_net / d_toplam * 100) if d_toplam > 0 else 0
            st.markdown(f"**Hesaplanan Net:** {d_net:.2f} &nbsp;|&nbsp; **Tahmini Puan:** {d_puan:.1f}")

            # Ders bazli detay
            st.markdown("---")
            st.markdown("**Ders Bazli Detay (Opsiyonel)**")
            ders_sayisi = st.number_input("Kac ders detayi gireceksiniz?", min_value=0, max_value=10, value=0, key="ek_nd_ders_sayi")

            ders_detaylari = []
            for i in range(ders_sayisi):
                ddc = st.columns(5)
                with ddc[0]:
                    dd_ders = st.selectbox(f"Ders {i+1}", DERS_LISTESI, key=f"ek_ndd_{i}")
                with ddc[1]:
                    dd_d = st.number_input(f"D", min_value=0, value=0, key=f"ek_nddd_{i}")
                with ddc[2]:
                    dd_y = st.number_input(f"Y", min_value=0, value=0, key=f"ek_nddy_{i}")
                with ddc[3]:
                    dd_b = st.number_input(f"B", min_value=0, value=0, key=f"ek_nddb_{i}")
                with ddc[4]:
                    dd_net = dd_d - (dd_y / 4)
                    st.markdown(f"<br>Net: **{dd_net:.1f}**", unsafe_allow_html=True)
                ders_detaylari.append({"ders": dd_ders, "dogru": dd_d, "yanlis": dd_y, "bos": dd_b, "net": round(dd_net,2)})

            d_not = st.text_area("Notlar", key="ek_nd_not")

            if st.form_submit_button("Kaydet", type="primary", use_container_width=True):
                if d_ogr == "Seciniz" or not d_sinav:
                    st.error("Ogrenci ve sinav adi zorunludur.")
                else:
                    yeni = DenemeAnaliz(
                        ogrenci_id=ogr_opts2[d_ogr], ogrenci_adi=d_ogr,
                        sinav_adi=d_sinav, sinav_turu=d_tur, tarih=d_tarih.isoformat(),
                        toplam_soru=d_toplam, dogru=d_dogru, yanlis=d_yanlis, bos=d_bos,
                        net=round(d_net, 2), puan=round(d_puan, 1),
                        siralama=d_siralama, ders_detaylari=ders_detaylari if ders_sayisi > 0 else [],
                        notlar=d_not,
                    )
                    store.add_item("deneme_analizleri", yeni.to_dict())
                    st.success("Deneme sonucu kaydedildi!")
                    st.rerun()


# ============================================================
# SEKME 8: VELI RAPORLARI
# ============================================================

def _render_veli_raporlari(store: EKDataStore):
    """Veliler icin analiz ve rapor."""
    styled_section("Veli Raporlari & Analiz", "#0d9488")

    sub1, sub2 = st.tabs(["📋 Rapor Gecmisi", "➕ Yeni Rapor"])

    with sub1:
        raporlar = store.load_list("veli_raporlari")
        if not raporlar:
            styled_info_banner("Henuz veli raporu olusturulmamis.", "info", "📋")
        else:
            raporlar = sorted(raporlar, key=lambda x: x.get("tarih",""), reverse=True)
            for r in raporlar:
                st.markdown(f'''
                <div class="ek-card" style="border-left:4px solid #0d9488">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                            <div style="font-weight:700;font-size:0.92rem;color:#94A3B8">
                                {r.get("ogrenci_adi","")}
                            </div>
                            <div style="font-size:0.78rem;color:#64748b;margin-top:2px">
                                Veli: {r.get("veli_adi","")} &nbsp;|&nbsp;
                                Donem: {r.get("donem","")} &nbsp;|&nbsp;
                                Tarih: {r.get("tarih","")}
                            </div>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

                with st.expander(f"Rapor Detayi - {r.get('ogrenci_adi','')} ({r.get('tarih','')})", expanded=False):
                    if r.get("genel_durum"):
                        st.markdown(f"**Genel Durum:** {r['genel_durum']}")
                    if r.get("akademik_ozet"):
                        st.markdown(f"**Akademik Ozet:** {r['akademik_ozet']}")
                    if r.get("motivasyon_ozet"):
                        st.markdown(f"**Motivasyon Ozeti:** {r['motivasyon_ozet']}")
                    if r.get("hedef_ilerleme"):
                        st.markdown(f"**Hedef Ilerleme:** {r['hedef_ilerleme']}")
                    if r.get("oneriler"):
                        st.markdown(f"**Oneriler:** {r['oneriler']}")
                    if r.get("koc_notu"):
                        st.markdown(f"**Koc Notu:** {r['koc_notu']}")

    with sub2:
        ogrenciler = store.load_list("ogrenciler")
        ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o for o in ogrenciler}

        # Shared data'dan veli bilgilerini hazirla
        shared_students = load_shared_students()
        shared_map = {}
        for s in shared_students:
            sid = s.get("id", "")
            if sid:
                shared_map[sid] = s

        with st.form("ek_yeni_vrapor", clear_on_submit=True):
            st.markdown("##### Yeni Veli Raporu Olustur")
            r_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts.keys()), key="ek_vr_ogr")

            # Secilen ogrencinin veli bilgisini otomatik getir
            default_veli = ""
            if r_ogr != "Seciniz" and r_ogr in ogr_opts:
                ogr_data = ogr_opts[r_ogr]
                # Oncelikle kocluk kaydindaki veli_adi
                default_veli = ogr_data.get("veli_adi", "")
                # Yoksa shared data'dan bul
                if not default_veli:
                    s_ogr_id = ogr_data.get("ogrenci_id", "")
                    if s_ogr_id and s_ogr_id in shared_map:
                        shared = shared_map[s_ogr_id]
                        default_veli = shared.get("veli_adi", "")
                        if not default_veli:
                            anne = f"{shared.get('anne_adi','')} {shared.get('anne_soyadi','')}".strip()
                            baba = f"{shared.get('baba_adi','')} {shared.get('baba_soyadi','')}".strip()
                            default_veli = anne or baba

            rc1, rc2 = st.columns(2)
            with rc1:
                r_donem = st.selectbox("Donem", ["1. Donem","2. Donem","Yillik","Ara Rapor"], key="ek_vr_donem")
                r_tarih = st.date_input("Tarih", value=date.today(), key="ek_vr_tarih")
            with rc2:
                r_veli = st.text_input("Veli Adi (Sinif Listesinden otomatik)", value=default_veli, key="ek_vr_veli")

            r_genel = st.text_area("Genel Durum Degerlendirmesi", key="ek_vr_genel")
            r_akad = st.text_area("Akademik Ozet", key="ek_vr_akad")
            r_motiv = st.text_area("Motivasyon Ozeti", key="ek_vr_motiv")
            r_hedef = st.text_area("Hedef Ilerleme Durumu", key="ek_vr_hedef")
            r_oner = st.text_area("Oneriler", key="ek_vr_oner")
            r_koc = st.text_area("Koc Notu", key="ek_vr_koc")

            if st.form_submit_button("Rapor Olustur", type="primary", use_container_width=True):
                if r_ogr == "Seciniz":
                    st.error("Lutfen bir ogrenci seciniz.")
                else:
                    ogr_data = ogr_opts[r_ogr]
                    veli_adi = r_veli or ogr_data.get("veli_adi", "")
                    yeni = VeliRapor(
                        ogrenci_id=ogr_data["id"], ogrenci_adi=r_ogr,
                        veli_adi=veli_adi, tarih=r_tarih.isoformat(),
                        donem=r_donem, genel_durum=r_genel,
                        akademik_ozet=r_akad, motivasyon_ozet=r_motiv,
                        hedef_ilerleme=r_hedef, oneriler=r_oner, koc_notu=r_koc,
                    )
                    store.add_item("veli_raporlari", yeni.to_dict())
                    st.success("Veli raporu olusturuldu!")
                    st.rerun()


# ============================================================
# SEKME 9: DURUM ANALIZI
# ============================================================

def _render_durum_analizi(store: EKDataStore):
    """Ogrenci genel durum analizi - 360 derece bakis."""
    styled_section("360° Durum Analizi", "#7c3aed")

    ogrenciler = store.load_list("ogrenciler")
    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o for o in ogrenciler}

    if not ogr_opts:
        styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
        return

    sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_duan_ogr")
    ogr = ogr_opts.get(sec_ogr)
    if not ogr:
        return

    ogr_id = ogr["id"]

    # Verileri topla
    gorusmeler = store.get_by_ogrenci("gorusmeler", ogr_id)
    hedefler = store.get_by_ogrenci("hedefler", ogr_id)
    planlar = store.get_by_ogrenci("haftalik_planlar", ogr_id)
    motivasyonlar = store.get_by_ogrenci("motivasyon", ogr_id)
    denemeler = _load_consolidated_deneme(store, ogr_id)

    tamamlanan_hedef = [h for h in hedefler if h.get("durum") == "Tamamlandi"]
    devam_hedef = [h for h in hedefler if h.get("durum") == "Devam Ediyor"]
    tamamlanan_gorusme = [g for g in gorusmeler if g.get("durum") == "Tamamlandi"]

    # Profil karti
    mv = ogr.get("motivasyon_seviyesi", 3)
    st.markdown(f'''
    <div class="ek-glass">
        <div style="display:flex;align-items:center;gap:20px">
            <div style="width:70px;height:70px;border-radius:50%;
                background:linear-gradient(135deg,#6366f1,#8b5cf6);
                display:flex;align-items:center;justify-content:center;
                font-size:1.8rem;color:white;font-weight:800">
                {ogr.get("ad","X")[0]}{ogr.get("soyad","X")[0]}
            </div>
            <div>
                <div style="font-size:1.2rem;font-weight:800;color:#94A3B8">
                    {ogr.get("ad","")} {ogr.get("soyad","")}
                </div>
                <div style="font-size:0.85rem;color:#64748b">
                    {ogr.get("sinif","")}/{ogr.get("sube","")} &nbsp;|&nbsp;
                    Koc: {ogr.get("koc_adi","Atanmadi")} &nbsp;|&nbsp;
                    Hedef: {ogr.get("hedef_sinav","Belirtilmemis")}
                </div>
            </div>
        </div>
    </div>''', unsafe_allow_html=True)

    # Genel istatistikler
    _diamond_stats([
        ("📅", str(len(tamamlanan_gorusme)), "Gorusme", "#06b6d4"),
        ("🎯", str(len(tamamlanan_hedef)), "Tamamlanan Hedef", "#10b981"),
        ("📊", str(len(denemeler)), "Deneme", "#8b5cf6"),
        ("🔥", f"{mv}/5", "Motivasyon", "#f59e0b"),
    ])

    # 6 Alan Radar
    col1, col2 = st.columns(2)

    with col1:
        styled_section("Kocluk Degerlendirmesi", "#6366f1")
        if motivasyonlar:
            son_m = sorted(motivasyonlar, key=lambda x: x.get("tarih",""), reverse=True)[0]
            areas = [
                ("Motivasyon", son_m.get("motivasyon_puani",3), "#ec4899"),
                ("Ozguven", son_m.get("ozguven_puani",3), "#8b5cf6"),
                ("Stres Yonetimi", son_m.get("stres_puani",3), "#f59e0b"),
                ("Enerji", son_m.get("enerji_puani",3), "#10b981"),
                ("Odaklanma", son_m.get("odaklanma_puani",3), "#3b82f6"),
                ("Mutluluk", son_m.get("mutluluk_puani",3), "#06b6d4"),
            ]
            html = '<div class="ek-radar-grid">'
            for label, score, color in areas:
                pct = score / 5 * 100
                html += f'''
                <div class="ek-radar-item">
                    <div class="ek-radar-label">{label}</div>
                    <div class="ek-radar-score" style="color:{color}">{score}/5</div>
                    <div class="ek-progress-container">
                        <div class="ek-progress-bar" style="width:{pct}%;background:{color}"></div>
                    </div>
                </div>'''
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)
        else:
            styled_info_banner("Motivasyon kaydi yok.", "info", "📊")

    with col2:
        styled_section("Deneme Net Trend", "#8b5cf6")
        if denemeler:
            son_denemeler = sorted(denemeler, key=lambda x: x.get("tarih",""))
            if len(son_denemeler) > 1:
                import pandas as pd
                df = pd.DataFrame([{"Tarih": d.get("tarih",""), "Net": d.get("net",0)} for d in son_denemeler])
                st.line_chart(df.set_index("Tarih"), height=250)
            else:
                d = son_denemeler[0]
                band = get_renk_bandi(d.get("puan", 0))
                st.markdown(f'''
                <div style="text-align:center;padding:20px">
                    <div style="font-size:2rem;font-weight:800;color:{band['color']}">{d.get("net",0)}</div>
                    <div style="font-size:0.85rem;color:#64748b">Son Deneme Neti</div>
                    <div style="margin-top:8px">{_badge(band['label'], band['color'])}</div>
                </div>''', unsafe_allow_html=True)
        else:
            styled_info_banner("Deneme sonucu yok.", "info", "📊")

    # Guclu/Zayif dersler
    st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    with dc1:
        styled_section("Guclu Dersler", "#10b981")
        guclu = ogr.get("guclu_dersler", [])
        if guclu:
            for d in guclu:
                st.markdown(f'<span class="ek-badge" style="background:#f0fdf4;color:#10b981;margin:2px">✅ {d}</span>', unsafe_allow_html=True)
        else:
            st.markdown("*Belirtilmemis*")
    with dc2:
        styled_section("Gelistirilecek Dersler", "#ef4444")
        zayif = ogr.get("zayif_dersler", [])
        if zayif:
            for d in zayif:
                st.markdown(f'<span class="ek-badge" style="background:#fef2f2;color:#ef4444;margin:2px">⚠️ {d}</span>', unsafe_allow_html=True)
        else:
            st.markdown("*Belirtilmemis*")


# ============================================================
# SEKME 10: ZAMAN YONETIMI
# ============================================================

def _render_zaman_yonetimi(store: EKDataStore):
    """Zaman yonetimi ve calisma verimliligi."""
    styled_section("Zaman Yonetimi & Verimlilik", "#3b82f6")

    ogrenciler = store.load_list("ogrenciler")
    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

    if not ogr_opts:
        styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
        return

    sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_zy_ogr")
    ogr_id = ogr_opts.get(sec_ogr, "")
    planlar = store.get_by_ogrenci("haftalik_planlar", ogr_id) if ogr_id else []

    if not planlar:
        styled_info_banner(f"{sec_ogr} icin plan verisi bulunmuyor. Haftalik Plan sekmesinden plan olusturun.", "info", "📅")
        return

    # Genel calisma istatistikleri
    toplam_etkinlik = sum(len(p.get("etkinlikler", [])) for p in planlar)
    tamamlanan = sum(sum(1 for e in p.get("etkinlikler", []) if e.get("tamamlandi")) for p in planlar)
    toplam_saat = sum(sum(e.get("sure_dk", 60) for e in p.get("etkinlikler", [])) for p in planlar) / 60
    tamamlanan_saat = sum(sum(e.get("sure_dk", 60) for e in p.get("etkinlikler", []) if e.get("tamamlandi")) for p in planlar) / 60

    _diamond_stats([
        ("📋", str(len(planlar)), "Toplam Plan", "#6366f1"),
        ("📝", str(toplam_etkinlik), "Toplam Etkinlik", "#3b82f6"),
        ("✅", str(tamamlanan), "Tamamlanan", "#10b981"),
        ("⏰", f"{toplam_saat:.0f}s", "Toplam Saat", "#f59e0b"),
    ])

    oran = (tamamlanan / toplam_etkinlik * 100) if toplam_etkinlik > 0 else 0
    st.markdown(f'''
    <div class="ek-glass" style="text-align:center">
        <div style="font-size:0.85rem;color:#64748b">Genel Tamamlanma Orani</div>
        <div style="font-size:2.5rem;font-weight:900;
            background:linear-gradient(135deg,#3b82f6,#6366f1);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent">
            %{oran:.1f}
        </div>
    </div>''', unsafe_allow_html=True)
    _progress_bar(oran)

    # Ders bazli analiz
    styled_section("Ders Bazli Calisma Suresi", "#8b5cf6")
    ders_saat = {}
    for p in planlar:
        for e in p.get("etkinlikler", []):
            ders = e.get("ders", "Diger")
            ders_saat[ders] = ders_saat.get(ders, 0) + e.get("sure_dk", 60)

    if ders_saat:
        sorted_dersler = sorted(ders_saat.items(), key=lambda x: x[1], reverse=True)
        max_dk = sorted_dersler[0][1] if sorted_dersler else 1
        for ders, dk in sorted_dersler:
            saat = dk / 60
            pct = (dk / max_dk) * 100
            st.markdown(f'''
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                <div style="width:100px;font-size:0.82rem;font-weight:600;color:#334155">{ders}</div>
                <div style="flex:1">
                    <div class="ek-progress-container">
                        <div class="ek-progress-bar" style="width:{pct}%"></div>
                    </div>
                </div>
                <div style="width:60px;text-align:right;font-size:0.82rem;font-weight:700;color:#6366f1">
                    {saat:.1f}s
                </div>
            </div>''', unsafe_allow_html=True)

    # Gun bazli analiz
    styled_section("Gun Bazli Calisma Dagilimi", "#06b6d4")
    gun_saat = {g: 0 for g in HAFTA_GUNLERI}
    for p in planlar:
        for e in p.get("etkinlikler", []):
            gun = e.get("gun", "")
            if gun in gun_saat:
                gun_saat[gun] += e.get("sure_dk", 60)

    max_gun = max(gun_saat.values()) if gun_saat else 1
    cols = st.columns(7)
    for i, (gun, dk) in enumerate(gun_saat.items()):
        saat = dk / 60
        pct = (dk / max_gun * 100) if max_gun > 0 else 0
        color = "#10b981" if pct >= 60 else "#f59e0b" if pct >= 30 else "#ef4444"
        cols[i].markdown(f'''
        <div style="text-align:center">
            <div style="font-size:0.72rem;font-weight:600;color:#64748b;margin-bottom:4px">{gun[:3]}</div>
            <div style="background:#1A2035;border-radius:6px;height:80px;display:flex;align-items:flex-end;overflow:hidden">
                <div style="width:100%;height:{pct}%;background:linear-gradient(180deg,{color},{color}bb);
                    border-radius:6px;transition:height 0.5s ease"></div>
            </div>
            <div style="font-size:0.78rem;font-weight:700;color:#334155;margin-top:4px">{saat:.1f}s</div>
        </div>''', unsafe_allow_html=True)


# ============================================================
# AI YARDIMCI FONKSIYONLAR
# ============================================================

def _ensure_env() -> None:
    """OPENAI_API_KEY'i .env dosyasindan yukle."""
    if os.environ.get("OPENAI_API_KEY"):
        return
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    val = val.strip().strip("\"'")
                    os.environ[key.strip()] = val


def _get_ai_client():
    """OpenAI client dondur."""
    _ensure_env()
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def _ai_kocluk_analizi(client, ogr: dict, gorusmeler: list, hedefler: list,
                        motivasyonlar: list, denemeler: list, planlar: list) -> dict | None:
    """AI ile kapsamli kocluk analizi."""
    # Verileri ozetle
    ogr_ozet = f"Ad: {ogr.get('ad','')} {ogr.get('soyad','')}, Sinif: {ogr.get('sinif','')}/{ogr.get('sube','')}"
    ogr_ozet += f", Hedef Sinav: {ogr.get('hedef_sinav','Belirtilmemis')}, Hedef Puan: {ogr.get('hedef_puan','Belirtilmemis')}"
    ogr_ozet += f", Guclu Dersler: {', '.join(ogr.get('guclu_dersler',[])) or 'Yok'}"
    ogr_ozet += f", Zayif Dersler: {', '.join(ogr.get('zayif_dersler',[])) or 'Yok'}"
    ogr_ozet += f", Motivasyon Seviyesi: {ogr.get('motivasyon_seviyesi',3)}/5"

    # Gorusme ozeti
    tam_gorusme = [g for g in gorusmeler if g.get("durum") == "Tamamlandi"]
    gorusme_ozet = f"Toplam {len(tam_gorusme)} gorusme tamamlandi."
    if tam_gorusme:
        son_g = sorted(tam_gorusme, key=lambda x: x.get("tarih",""), reverse=True)[:3]
        for g in son_g:
            gorusme_ozet += f"\n- {g.get('tarih','')}: {g.get('konu','')} ({g.get('kocluk_alani','')})"
            if g.get("gorusme_notlari"):
                gorusme_ozet += f" Not: {g['gorusme_notlari'][:100]}"

    # Hedef ozeti
    devam_hedefler = [h for h in hedefler if h.get("durum") == "Devam Ediyor"]
    tam_hedefler = [h for h in hedefler if h.get("durum") == "Tamamlandi"]
    hedef_ozet = f"Devam eden: {len(devam_hedefler)}, Tamamlanan: {len(tam_hedefler)}"
    for h in devam_hedefler:
        hedef_ozet += f"\n- {h.get('baslik','')}: %{h.get('ilerleme_yuzdesi',0)} ({h.get('kategori','')})"

    # Motivasyon ozeti
    motiv_ozet = "Kayit yok"
    if motivasyonlar:
        son_motiv = sorted(motivasyonlar, key=lambda x: x.get("tarih",""), reverse=True)[:5]
        motiv_ozet = ""
        for m in son_motiv:
            motiv_ozet += f"\n- {m.get('tarih','')}: Motivasyon:{m.get('motivasyon_puani',3)} Ozguven:{m.get('ozguven_puani',3)} "
            motiv_ozet += f"Stres:{m.get('stres_puani',3)} Enerji:{m.get('enerji_puani',3)} "
            motiv_ozet += f"Odaklanma:{m.get('odaklanma_puani',3)} Mutluluk:{m.get('mutluluk_puani',3)}"

    # Deneme ozeti
    deneme_ozet = "Deneme sonucu yok"
    if denemeler:
        son_den = sorted(denemeler, key=lambda x: x.get("tarih",""), reverse=True)[:5]
        ort_net = sum(d.get("net",0) for d in denemeler) / len(denemeler)
        deneme_ozet = f"Toplam {len(denemeler)} deneme. Ortalama Net: {ort_net:.1f}"
        for d in son_den:
            deneme_ozet += f"\n- {d.get('tarih','')}: {d.get('sinav_adi','')} - Net: {d.get('net',0)} Puan: {d.get('puan',0)}"
            ders_det = d.get("ders_detaylari", [])
            if ders_det:
                for dd in ders_det:
                    deneme_ozet += f" [{dd.get('ders','')}: D{dd.get('dogru',0)}/Y{dd.get('yanlis',0)}/Net{dd.get('net',0)}]"

    # Plan ozeti
    plan_ozet = "Plan verisi yok"
    if planlar:
        toplam_etkinlik = sum(len(p.get("etkinlikler", [])) for p in planlar)
        tamamlanan = sum(sum(1 for e in p.get("etkinlikler", []) if e.get("tamamlandi")) for p in planlar)
        oran = (tamamlanan / toplam_etkinlik * 100) if toplam_etkinlik > 0 else 0
        ders_saat = {}
        for p in planlar:
            for e in p.get("etkinlikler", []):
                d = e.get("ders", "Diger")
                ders_saat[d] = ders_saat.get(d, 0) + e.get("sure_dk", 60)
        plan_ozet = f"{len(planlar)} haftalik plan, {toplam_etkinlik} etkinlik, Tamamlanma: %{oran:.0f}"
        plan_ozet += f"\nDers dagilimi: " + ", ".join(f"{d}:{dk//60}s" for d, dk in sorted(ders_saat.items(), key=lambda x: -x[1])[:6])

    prompt = f"""Sen deneyimli bir egitim kocu ve ogretmensin. Asagidaki ogrenci verilerini analiz ederek
kapsamli bir kocluk degerlendirmesi yap.

=== OGRENCI PROFILI ===
{ogr_ozet}

=== GORUSME GECMISI ===
{gorusme_ozet}

=== HEDEFLER ===
{hedef_ozet}

=== MOTIVASYON TAKIBI (Son 5 Kayit, 1-5 arasi puan) ===
{motiv_ozet}

=== DENEME SONUCLARI ===
{deneme_ozet}

=== CALISMA PLANI ===
{plan_ozet}

Asagidaki JSON formatinda detayli analiz yap. Turkce yaz, somut ve uygulanabilir oneriler ver:

{{
    "genel_degerlendirme": "3-5 cumlelik genel durum ozeti",
    "akademik_analiz": {{
        "guclu_yonler": ["somut guclu yon 1", "somut guclu yon 2", "somut guclu yon 3"],
        "gelistirme_alanlari": ["somut alan 1", "somut alan 2", "somut alan 3"],
        "akademik_puan": 75
    }},
    "motivasyon_analiz": {{
        "genel_durum": "motivasyon durumu aciklamasi",
        "risk_alanlari": ["risk 1", "risk 2"],
        "guclu_alanlar": ["guclu 1", "guclu 2"],
        "motivasyon_puan": 70
    }},
    "calisma_verimi": {{
        "degerlendirme": "calisma duzenine dair analiz",
        "iyilestirme_onerileri": ["oneri 1", "oneri 2", "oneri 3"],
        "verimlilik_puan": 65
    }},
    "hedef_ilerleme": {{
        "degerlendirme": "hedeflere yaklasim analizi",
        "oneriler": ["oneri 1", "oneri 2"],
        "ilerleme_puan": 60
    }},
    "haftalik_eylem_plani": [
        "Pazartesi-Cuma: somut eylem 1",
        "somut eylem 2",
        "somut eylem 3",
        "somut eylem 4",
        "Hafta sonu: somut eylem 5"
    ],
    "koc_onerileri": [
        "Kisa vadeli (1-2 hafta): somut oneri",
        "Orta vadeli (1 ay): somut oneri",
        "Uzun vadeli (3 ay): somut oneri"
    ],
    "veli_mesaji": "Veliye iletilecek 2-3 cumlelik ozet ve oneri",
    "genel_puan": 68,
    "emoji_durum": "bir emoji ile ogrencinin durumunu ozetle",
    "baslik_durum": "Gelistirilebilir / Iyi / Cok Iyi / Mukemmel gibi tek kelime"
}}

KURALLAR:
- Sadece JSON dondur, baska bir sey yazma
- Puanlar 0-100 arasi olsun
- Oneriler somut, olculebilir ve uygulanabilir olsun
- Pozitif ve motivasyonu artirici bir dil kullan
- Veri yoksa mantikli varsayimlar yap"""

    try:
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": __import__('utils.ai_rules', fromlist=['inject_rules']).inject_rules(
                    "Sen Turkiye'nin en iyi egitim kocusun. 20 yillik deneyimli bir uzmansin. Sadece JSON formatinda cevap ver.", short=True)},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
        )
        content = response.choices[0].message.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except Exception as e:
        return {"error": f"AI analiz hatasi: {str(e)[:200]}"}


def _ai_haftalik_plan_onerisi(client, ogr: dict, denemeler: list, motivasyonlar: list) -> dict | None:
    """AI ile kisisellesitirilmis haftalik calisma plani onerisi."""
    ogr_ozet = f"Sinif: {ogr.get('sinif','')}, Hedef: {ogr.get('hedef_sinav','')}"
    ogr_ozet += f", Guclu: {', '.join(ogr.get('guclu_dersler',[])) or 'Yok'}"
    ogr_ozet += f", Zayif: {', '.join(ogr.get('zayif_dersler',[])) or 'Yok'}"

    deneme_ozet = ""
    if denemeler:
        son = sorted(denemeler, key=lambda x: x.get("tarih",""), reverse=True)[0]
        deneme_ozet = f"Son deneme: Net {son.get('net',0)}, Puan {son.get('puan',0)}"
        for dd in son.get("ders_detaylari", []):
            deneme_ozet += f", {dd.get('ders','')}: Net {dd.get('net',0)}"

    mv = ogr.get("motivasyon_seviyesi", 3)

    prompt = f"""Asagidaki ogrenci icin kisisellestirilmis bir haftalik calisma plani olustur.

OGRENCI: {ogr_ozet}
DENEME: {deneme_ozet or 'Veri yok'}
MOTIVASYON: {mv}/5

Asagidaki JSON formatinda haftalik plan olustur:

{{
    "plan_aciklama": "Bu planin mantigi hakkinda 2-3 cumle",
    "gunluk_toplam_saat": 5,
    "plan": [
        {{"gun": "Pazartesi", "etkinlikler": [
            {{"saat": "15:00-16:00", "ders": "Matematik", "etkinlik": "Konu calismasi", "konu": "Turev", "oncelik": "Yuksek"}},
            {{"saat": "16:15-17:15", "ders": "Fizik", "etkinlik": "Soru cozumu", "konu": "Kuvvet", "oncelik": "Orta"}}
        ]}},
        {{"gun": "Sali", "etkinlikler": [...]}},
        {{"gun": "Carsamba", "etkinlikler": [...]}},
        {{"gun": "Persembe", "etkinlikler": [...]}},
        {{"gun": "Cuma", "etkinlikler": [...]}},
        {{"gun": "Cumartesi", "etkinlikler": [...]}},
        {{"gun": "Pazar", "etkinlikler": [...]}}
    ],
    "onemli_notlar": ["not 1", "not 2", "not 3"]
}}

KURALLAR:
- Zayif derslere daha fazla zaman ayir
- Hafta ici gunluk 4-6 saat, hafta sonu 3-5 saat
- Teneffus araları koy (her 60 dk'da 15 dk)
- Motivasyon dusukse daha kisa ve yogun seanslar planla
- Sadece JSON dondur"""

    try:
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "Sen uzman bir egitim planlama kocusun. Sadece JSON formatinda cevap ver."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500,
            temperature=0.7,
        )
        content = response.choices[0].message.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except Exception as e:
        return {"error": f"AI plan hatasi: {str(e)[:200]}"}


def _ai_motivasyon_mesaji(client, ogr: dict, motivasyonlar: list) -> str:
    """AI ile kisisellesitirilmis motivasyon mesaji."""
    mv = ogr.get("motivasyon_seviyesi", 3)
    ad = ogr.get("ad", "Ogrenci")
    hedef = ogr.get("hedef_sinav", "")

    motiv_trend = ""
    if motivasyonlar:
        son = sorted(motivasyonlar, key=lambda x: x.get("tarih",""), reverse=True)[:3]
        for m in son:
            motiv_trend += f"Tarih:{m.get('tarih','')}, Mot:{m.get('motivasyon_puani',3)}, Ozg:{m.get('ozguven_puani',3)}, "
            motiv_trend += f"Enr:{m.get('enerji_puani',3)}, Odk:{m.get('odaklanma_puani',3)}\n"

    prompt = f"""Ogrenci: {ad}, Sinif: {ogr.get('sinif','')}, Hedef: {hedef or 'Belirtilmemis'}
Motivasyon: {mv}/5
Son motivasyon kayitlari: {motiv_trend or 'Veri yok'}

Bu ogrenci icin kisisellestirilmis, samimi, motive edici ve ilham verici bir mesaj yaz.
- 3-5 paragraf olsun
- Ogrencinin adini kullan
- Hedeflerine atifta bulun
- Somut tavsiyeler ver
- Pozitif ve guclendirici bir ton kullan
- Emojiler kullanabilirsin"""

    try:
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "Sen ilham verici bir egitim kocu ve motivasyon uzmanisin. Turkce yaz."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Motivasyon mesaji olusturulamadi: {str(e)[:200]}"


def _ai_veli_raporu_olustur(client, ogr: dict, gorusmeler: list, hedefler: list,
                             motivasyonlar: list, denemeler: list) -> dict | None:
    """AI ile otomatik veli raporu olustur."""
    ogr_ozet = f"{ogr.get('ad','')} {ogr.get('soyad','')}, {ogr.get('sinif','')}/{ogr.get('sube','')}"

    deneme_ozet = "Veri yok"
    if denemeler:
        son = sorted(denemeler, key=lambda x: x.get("tarih",""), reverse=True)[:3]
        nets = [d.get("net",0) for d in son]
        deneme_ozet = f"Son {len(son)} deneme netleri: {', '.join(str(n) for n in nets)}"

    motiv_ozet = "Veri yok"
    if motivasyonlar:
        son = sorted(motivasyonlar, key=lambda x: x.get("tarih",""), reverse=True)[0]
        motiv_ozet = f"Mot:{son.get('motivasyon_puani',3)} Ozg:{son.get('ozguven_puani',3)} Enr:{son.get('enerji_puani',3)} Odk:{son.get('odaklanma_puani',3)}"

    hedef_ozet = "Hedef yok"
    devam = [h for h in hedefler if h.get("durum") == "Devam Ediyor"]
    if devam:
        hedef_ozet = ", ".join(f"{h.get('baslik','')}: %{h.get('ilerleme_yuzdesi',0)}" for h in devam[:3])

    prompt = f"""Ogrenci: {ogr_ozet}
Guclu dersler: {', '.join(ogr.get('guclu_dersler',[])) or 'Yok'}
Zayif dersler: {', '.join(ogr.get('zayif_dersler',[])) or 'Yok'}
Deneme: {deneme_ozet}
Motivasyon: {motiv_ozet}
Hedefler: {hedef_ozet}
Gorusme sayisi: {len([g for g in gorusmeler if g.get('durum')=='Tamamlandi'])}

Bu ogrenci icin veliye sunulacak profesyonel bir rapor olustur. JSON formatinda:

{{
    "genel_durum": "3-4 cumlelik genel durum degerlendirmesi",
    "akademik_ozet": "Akademik performans ozeti, deneme sonuclari, guclu/zayif alanlar",
    "motivasyon_ozet": "Motivasyon ve psikososyal durum degerlendirmesi",
    "hedef_ilerleme": "Hedeflere yonelik ilerleme durumu",
    "oneriler": "Velinin evde yapabilecegi 3-4 somut oneri",
    "koc_notu": "Kocun veliye ozel mesaji"
}}

KURALLAR:
- Profesyonel ve saygili bir dil kullan
- Pozitif yonleri one cikar, gelistirme alanlarini yapici sekilde ifade et
- Velinin anlayabilecegi bir dil kullan, teknik terimlerden kacin
- Sadece JSON dondur"""

    try:
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "Sen profesyonel bir egitim kocusun. Veli raporlarini titiz ve yapici yazarsin. Sadece JSON formatinda cevap ver."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
        )
        content = response.choices[0].message.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except Exception as e:
        return {"error": f"Rapor hatasi: {str(e)[:200]}"}


# ============================================================
# SEKME 11: CALISMA TAKVIMI
# ============================================================

def _render_calisma_takvimi(store: EKDataStore):
    """Calisma takvimi - takvim gorunumlu etkinlik yonetimi."""
    styled_section("Calisma Takvimi", "#06b6d4")

    ogrenciler = store.load_list("ogrenciler")
    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}
    if not ogr_opts:
        styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
        return

    sub1, sub2 = st.tabs(["📅 Takvim", "➕ Etkinlik Ekle"])

    with sub1:
        sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_ct_ogr")
        ogr_id = ogr_opts.get(sec_ogr, "")

        # Hafta secimi
        bugun = date.today()
        hafta_bas = bugun - timedelta(days=bugun.weekday())
        hc1, hc2, hc3 = st.columns([1,2,1])
        with hc1:
            if st.button("◀ Onceki", key="ek_ct_prev", use_container_width=True):
                st.session_state["_ek_ct_offset"] = st.session_state.get("_ek_ct_offset", 0) - 7
                st.rerun()
        with hc3:
            if st.button("Sonraki ▶", key="ek_ct_next", use_container_width=True):
                st.session_state["_ek_ct_offset"] = st.session_state.get("_ek_ct_offset", 0) + 7
                st.rerun()
        offset = st.session_state.get("_ek_ct_offset", 0)
        hafta_bas = hafta_bas + timedelta(days=offset)
        hafta_bit = hafta_bas + timedelta(days=6)
        with hc2:
            st.markdown(f"<div style='text-align:center;font-weight:700;font-size:0.95rem;padding:8px'>{hafta_bas.strftime('%d.%m')} - {hafta_bit.strftime('%d.%m.%Y')}</div>", unsafe_allow_html=True)

        # Haftanin etkinliklerini getir
        tum_etkinlikler = store.get_by_ogrenci("calisma_takvim", ogr_id)
        hafta_etkinlik = [
            e for e in tum_etkinlikler
            if hafta_bas.isoformat() <= e.get("tarih","") <= hafta_bit.isoformat()
        ]

        # Gunlere gore grid
        cols = st.columns(7)
        for i in range(7):
            gun_tarih = hafta_bas + timedelta(days=i)
            gun_str = gun_tarih.isoformat()
            gun_adi = HAFTA_GUNLERI[i][:3]
            gun_etkinlik = sorted([e for e in hafta_etkinlik if e.get("tarih") == gun_str],
                                   key=lambda x: x.get("saat_baslangic",""))

            is_bugun = gun_tarih == bugun
            border = "border:2px solid #6366f1" if is_bugun else "border:1px solid #e2e8f0"

            with cols[i]:
                st.markdown(f'''
                <div style="text-align:center;{border};border-radius:10px;padding:8px;min-height:200px;
                    background:{'#eef2ff' if is_bugun else '#fafbff'}">
                    <div style="font-weight:700;font-size:0.78rem;color:{'#6366f1' if is_bugun else '#64748b'}">{gun_adi}</div>
                    <div style="font-size:0.72rem;color:#94a3b8;margin-bottom:8px">{gun_tarih.strftime('%d.%m')}</div>
                </div>''', unsafe_allow_html=True)

                for e in gun_etkinlik:
                    check = "✅" if e.get("tamamlandi") else "⬜"
                    st.markdown(f'''
                    <div style="background:{'#f0fdf4' if e.get('tamamlandi') else '#111827'};border:1px solid #e2e8f0;
                        border-radius:6px;padding:4px 6px;margin-bottom:3px;font-size:0.7rem">
                        {check} <span style="color:#6366f1;font-weight:600">{e.get("saat_baslangic","")}</span>
                        <br><span style="font-weight:600">{e.get("ders","")}</span>
                        <br><span style="color:#64748b">{e.get("konu","")[:20]}</span>
                    </div>''', unsafe_allow_html=True)

                if not gun_etkinlik:
                    st.caption("Bos")

        # Tamamlanma takibi
        if hafta_etkinlik:
            tamamlanan = sum(1 for e in hafta_etkinlik if e.get("tamamlandi"))
            oran = (tamamlanan / len(hafta_etkinlik) * 100) if hafta_etkinlik else 0
            st.markdown(f"**Haftalik Tamamlanma:** {tamamlanan}/{len(hafta_etkinlik)} (%{oran:.0f})")
            _progress_bar(oran)

            with st.expander("Etkinlikleri Tamamla"):
                for e in sorted(hafta_etkinlik, key=lambda x: (x.get("tarih",""), x.get("saat_baslangic",""))):
                    ck = st.checkbox(
                        f"{e.get('tarih','')} {e.get('saat_baslangic','')} - {e.get('ders','')} {e.get('konu','')}",
                        value=e.get("tamamlandi", False), key=f"ek_ct_ck_{e['id']}")
                    if ck != e.get("tamamlandi", False):
                        store.update_item("calisma_takvim", e["id"], {"tamamlandi": ck})
                        st.rerun()

    with sub2:
        sec_ogr2 = st.selectbox("Ogrenci", list(ogr_opts.keys()), key="ek_ct_ogr2")
        with st.form("ek_yeni_takvim", clear_on_submit=True):
            st.markdown("##### Yeni Takvim Etkinligi")
            tc1, tc2 = st.columns(2)
            with tc1:
                t_tarih = st.date_input("Tarih", value=date.today(), key="ek_ct_tarih")
                t_ders = st.selectbox("Ders", DERS_LISTESI, key="ek_ct_ders")
                t_tur = st.selectbox("Etkinlik Turu", ETKINLIK_TURLERI, key="ek_ct_tur")
            with tc2:
                t_saat_bas = st.selectbox("Baslangic", SAAT_DILIMLERI, key="ek_ct_sbas")
                t_saat_bit = st.selectbox("Bitis", SAAT_DILIMLERI, index=1, key="ek_ct_sbit")
                t_tekrar = st.selectbox("Tekrar", ["Tek Sefer","Her Hafta","Her Gun"], key="ek_ct_tekrar")
            t_konu = st.text_input("Konu", key="ek_ct_konu")
            t_not = st.text_area("Not", key="ek_ct_not")

            if st.form_submit_button("Ekle", type="primary", use_container_width=True):
                tarihler = [t_tarih]
                if t_tekrar == "Her Hafta":
                    for w in range(1, 12):
                        tarihler.append(t_tarih + timedelta(weeks=w))
                elif t_tekrar == "Her Gun":
                    for d in range(1, 30):
                        tarihler.append(t_tarih + timedelta(days=d))
                for t in tarihler:
                    yeni = CalismaTakvim(
                        ogrenci_id=ogr_opts[sec_ogr2], ogrenci_adi=sec_ogr2,
                        tarih=t.isoformat(), saat_baslangic=t_saat_bas.split("-")[0],
                        saat_bitis=t_saat_bit.split("-")[1] if "-" in t_saat_bit else t_saat_bit,
                        ders=t_ders, konu=t_konu, etkinlik_turu=t_tur,
                        tekrar=t_tekrar, notlar=t_not,
                    )
                    store.add_item("calisma_takvim", yeni.to_dict())
                st.success(f"{len(tarihler)} etkinlik eklendi!")
                st.rerun()


# ============================================================
# SEKME 12: ODEV MODULU
# ============================================================

def _render_odev_modulu(store: EKDataStore):
    """Odev verme ve takip."""
    styled_section("Odev Yonetimi", "#f59e0b")

    ogrenciler = store.load_list("ogrenciler")
    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

    sub1, sub2 = st.tabs(["📋 Odev Takibi", "➕ Yeni Odev"])

    with sub1:
        if not ogr_opts:
            styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
            return

        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            f_ogr = st.selectbox("Ogrenci", ["Tumu"] + list(ogr_opts.keys()), key="ek_od_fogr")
        with fc2:
            f_durum = st.selectbox("Durum", ["Tumu"] + ODEV_DURUMLARI, key="ek_od_fdurum")
        with fc3:
            f_ders = st.selectbox("Ders", ["Tumu"] + DERS_LISTESI, key="ek_od_fders")

        odevler = store.load_list("odevler")
        if f_ogr != "Tumu":
            odevler = [o for o in odevler if o.get("ogrenci_id") == ogr_opts.get(f_ogr)]
        if f_durum != "Tumu":
            odevler = [o for o in odevler if o.get("durum") == f_durum]
        if f_ders != "Tumu":
            odevler = [o for o in odevler if o.get("ders") == f_ders]
        odevler = sorted(odevler, key=lambda x: x.get("teslim_tarihi",""), reverse=True)

        # Istatistikler
        toplam = len(odevler)
        teslim = sum(1 for o in odevler if o.get("teslim_edildi"))
        geciken = sum(1 for o in odevler if o.get("durum") == "Gecikti")
        _diamond_stats([
            ("📝", str(toplam), "Toplam Odev", "#6366f1"),
            ("✅", str(teslim), "Teslim Edilen", "#10b981"),
            ("⚠️", str(geciken), "Geciken", "#ef4444"),
            ("📊", f"%{(teslim/toplam*100):.0f}" if toplam > 0 else "%0", "Teslim Orani", "#3b82f6"),
        ])

        if not odevler:
            styled_info_banner("Odev bulunamadi.", "info", "📝")
        else:
            for o in odevler:
                durum_colors = {"Beklemede":"#94a3b8","Devam Ediyor":"#3b82f6","Teslim Edildi":"#10b981","Gecikti":"#ef4444","Iptal":"#64748b"}
                dc = durum_colors.get(o.get("durum",""), "#94a3b8")
                bugun = date.today().isoformat()
                gecikme = o.get("teslim_tarihi","") < bugun and o.get("durum") not in ("Teslim Edildi","Iptal")

                st.markdown(f'''
                <div class="ek-card" style="border-left:4px solid {dc}{';;background:#fef2f2' if gecikme else ''}">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                            <div style="font-weight:700;font-size:0.9rem;color:#94A3B8">{o.get("ders","")} - {o.get("konu","")}</div>
                            <div style="font-size:0.78rem;color:#64748b;margin-top:2px">
                                {o.get("ogrenci_adi","")} &nbsp;|&nbsp; Teslim: {o.get("teslim_tarihi","")}
                            </div>
                            <div style="font-size:0.75rem;color:#94a3b8;margin-top:4px">{o.get("aciklama","")[:100]}</div>
                        </div>
                        <div style="text-align:right">
                            {_badge(o.get("durum",""), dc)}
                            {f'<div style="margin-top:4px">{_badge("GECİKTİ!", "#ef4444")}</div>' if gecikme else ""}
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

                with st.expander(f"Guncelle: {o.get('ders','')} - {o.get('konu','')}", expanded=False):
                    uc1, uc2 = st.columns(2)
                    with uc1:
                        u_durum = st.selectbox("Durum", ODEV_DURUMLARI,
                            index=ODEV_DURUMLARI.index(o.get("durum","Beklemede")) if o.get("durum") in ODEV_DURUMLARI else 0,
                            key=f"ek_od_d_{o['id']}")
                    with uc2:
                        u_puan = st.number_input("Puan", 0.0, 100.0, o.get("puan",0.0), key=f"ek_od_p_{o['id']}")
                    u_not = st.text_area("Not", o.get("teslim_notu",""), key=f"ek_od_n_{o['id']}")
                    if st.button("Guncelle", key=f"ek_od_u_{o['id']}", type="primary"):
                        updates = {"durum": u_durum, "puan": u_puan, "teslim_notu": u_not}
                        if u_durum == "Teslim Edildi":
                            updates["teslim_edildi"] = True
                        store.update_item("odevler", o["id"], updates)
                        st.success("Odev guncellendi!")
                        st.rerun()

    with sub2:
        with st.form("ek_yeni_odev", clear_on_submit=True):
            st.markdown("##### Yeni Odev Ver")
            oc1, oc2 = st.columns(2)
            with oc1:
                o_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts.keys()), key="ek_no_ogr")
                o_ders = st.selectbox("Ders *", DERS_LISTESI, key="ek_no_ders")
                o_verilis = st.date_input("Verilis Tarihi", value=date.today(), key="ek_no_ver")
            with oc2:
                o_konu = st.text_input("Konu *", key="ek_no_konu")
                o_oncelik = st.selectbox("Oncelik", HEDEF_ONCELIKLERI, index=1, key="ek_no_onc")
                o_teslim = st.date_input("Teslim Tarihi", value=date.today()+timedelta(days=7), key="ek_no_tes")
            o_aciklama = st.text_area("Aciklama", key="ek_no_ack")

            if st.form_submit_button("Odev Ver", type="primary", use_container_width=True):
                if o_ogr == "Seciniz" or not o_konu:
                    st.error("Ogrenci ve konu zorunludur.")
                else:
                    yeni = Odev(
                        ogrenci_id=ogr_opts[o_ogr], ogrenci_adi=o_ogr,
                        ders=o_ders, konu=o_konu, aciklama=o_aciklama,
                        verilis_tarihi=o_verilis.isoformat(), teslim_tarihi=o_teslim.isoformat(),
                        oncelik=o_oncelik,
                    )
                    store.add_item("odevler", yeni.to_dict())
                    st.success("Odev olusturuldu!")
                    st.rerun()


# ============================================================
# SEKME 13: CANLI DERS & ONLINE ETUT
# ============================================================

def _render_canli_ders(store: EKDataStore):
    """Canli ders ve online etut yonetimi."""
    styled_section("Canli Ders & Online Etut", "#8b5cf6")

    ogrenciler = store.load_list("ogrenciler")
    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

    sub1, sub2 = st.tabs(["📋 Ders Takibi", "➕ Yeni Ders/Etut"])

    with sub1:
        dersler = store.load_list("canli_dersler")
        dersler = sorted(dersler, key=lambda x: (x.get("tarih",""), x.get("saat","")), reverse=True)

        # Istatistikler
        planli = sum(1 for d in dersler if d.get("durum") == "Planli")
        tamamlanan = sum(1 for d in dersler if d.get("durum") == "Tamamlandi")
        katilim = sum(1 for d in dersler if d.get("katilim"))

        _diamond_stats([
            ("📅", str(planli), "Planli", "#3b82f6"),
            ("✅", str(tamamlanan), "Tamamlanan", "#10b981"),
            ("👤", str(katilim), "Katilim", "#6366f1"),
            ("📊", f"%{(katilim/len(dersler)*100):.0f}" if dersler else "%0", "Katilim Orani", "#f59e0b"),
        ])

        if not dersler:
            styled_info_banner("Henuz ders/etut kaydi yok.", "info", "📅")
        else:
            for d in dersler:
                durum_colors = {"Planli":"#3b82f6","Tamamlandi":"#10b981","Iptal":"#ef4444","Ertelendi":"#f59e0b"}
                dc = durum_colors.get(d.get("durum",""), "#94a3b8")
                tur_colors = {"Canli Ders":"#6366f1","Online Etut":"#06b6d4","Soru Cozum Seansi":"#f59e0b","Birebir Ders":"#10b981"}
                tc = tur_colors.get(d.get("tur",""), "#94a3b8")

                st.markdown(f'''
                <div class="ek-card" style="border-left:4px solid {tc}">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                            <div style="font-weight:700;font-size:0.9rem;color:#94A3B8">
                                {d.get("ders","")} - {d.get("konu","")}
                            </div>
                            <div style="font-size:0.78rem;color:#64748b;margin-top:2px">
                                {d.get("ogrenci_adi","")} &nbsp;|&nbsp; {d.get("ogretmen","")} &nbsp;|&nbsp;
                                {d.get("platform","")} &nbsp;|&nbsp; {d.get("sure_dk",60)} dk
                            </div>
                        </div>
                        <div style="text-align:right">
                            {_badge(d.get("tur",""), tc)}
                            <div style="margin-top:4px">{_badge(d.get("durum",""), dc)}</div>
                            <div style="font-size:0.78rem;color:#6366f1;font-weight:600;margin-top:4px">
                                {d.get("tarih","")} {d.get("saat","")}
                            </div>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

                with st.expander(f"Guncelle: {d.get('tarih','')} {d.get('ders','')}", expanded=False):
                    uc1, uc2, uc3 = st.columns(3)
                    with uc1:
                        u_durum = st.selectbox("Durum", ["Planli","Tamamlandi","Iptal","Ertelendi"],
                            index=["Planli","Tamamlandi","Iptal","Ertelendi"].index(d.get("durum","Planli")) if d.get("durum") in ["Planli","Tamamlandi","Iptal","Ertelendi"] else 0,
                            key=f"ek_cd_d_{d['id']}")
                    with uc2:
                        u_katilim = st.checkbox("Katildi", d.get("katilim", False), key=f"ek_cd_k_{d['id']}")
                    with uc3:
                        if st.button("Guncelle", key=f"ek_cd_u_{d['id']}", type="primary"):
                            store.update_item("canli_dersler", d["id"], {"durum": u_durum, "katilim": u_katilim})
                            st.success("Guncellendi!")
                            st.rerun()

    with sub2:
        with st.form("ek_yeni_canli", clear_on_submit=True):
            st.markdown("##### Yeni Canli Ders / Online Etut")
            cc1, cc2 = st.columns(2)
            with cc1:
                c_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts.keys()), key="ek_nc_ogr")
                c_ders = st.selectbox("Ders", DERS_LISTESI, key="ek_nc_ders")
                c_tarih = st.date_input("Tarih", value=date.today(), key="ek_nc_tarih")
                c_tur = st.selectbox("Tur", CANLI_DERS_TURLERI, key="ek_nc_tur")
            with cc2:
                c_konu = st.text_input("Konu", key="ek_nc_konu")
                c_ogretmen = st.text_input("Ogretmen", key="ek_nc_ogrt")
                c_saat = st.selectbox("Saat", ["09:00","10:00","11:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00"], key="ek_nc_saat")
                c_platform = st.selectbox("Platform", CANLI_DERS_PLATFORMLARI, key="ek_nc_plat")
            c_sure = st.number_input("Sure (dk)", 15, 180, 60, 15, key="ek_nc_sure")
            c_link = st.text_input("Toplanti Linki", key="ek_nc_link")

            if st.form_submit_button("Ders Olustur", type="primary", use_container_width=True):
                if c_ogr == "Seciniz":
                    st.error("Lutfen ogrenci seciniz.")
                else:
                    yeni = CanliDers(
                        ogrenci_id=ogr_opts[c_ogr], ogrenci_adi=c_ogr,
                        ders=c_ders, konu=c_konu, tarih=c_tarih.isoformat(),
                        saat=c_saat, sure_dk=c_sure, tur=c_tur,
                        platform=c_platform, link=c_link, ogretmen=c_ogretmen,
                    )
                    store.add_item("canli_dersler", yeni.to_dict())
                    st.success("Ders olusturuldu!")
                    st.rerun()


# ============================================================
# SEKME 14: SORU KUTUSU
# ============================================================

def _render_soru_kutusu(store: EKDataStore):
    """Ogrenci soru kutusu - soru sor/cevapla."""
    styled_section("Soru Kutum", "#ec4899")

    ogrenciler = store.load_list("ogrenciler")
    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

    sub1, sub2 = st.tabs(["📋 Sorular", "➕ Yeni Soru"])

    with sub1:
        sorular = store.load_list("soru_kutusu")

        # Istatistikler
        bekleyen = sum(1 for s in sorular if s.get("durum") == "Cevap Bekliyor")
        cevaplanan = sum(1 for s in sorular if s.get("durum") == "Cevaplandi")

        _diamond_stats([
            ("❓", str(len(sorular)), "Toplam Soru", "#6366f1"),
            ("⏳", str(bekleyen), "Cevap Bekliyor", "#f59e0b"),
            ("✅", str(cevaplanan), "Cevaplandi", "#10b981"),
            ("📊", f"%{(cevaplanan/len(sorular)*100):.0f}" if sorular else "%0", "Cevap Orani", "#3b82f6"),
        ])

        fc1, fc2 = st.columns(2)
        with fc1:
            f_durum = st.selectbox("Durum", ["Tumu"] + SORU_DURUMLARI, key="ek_sk_fd")
        with fc2:
            f_ders = st.selectbox("Ders", ["Tumu"] + DERS_LISTESI, key="ek_sk_fders")

        filtered = sorular
        if f_durum != "Tumu":
            filtered = [s for s in filtered if s.get("durum") == f_durum]
        if f_ders != "Tumu":
            filtered = [s for s in filtered if s.get("ders") == f_ders]
        filtered = sorted(filtered, key=lambda x: x.get("tarih",""), reverse=True)

        if not filtered:
            styled_info_banner("Soru bulunmuyor.", "info", "❓")
        else:
            for s in filtered:
                durum_colors = {"Cevap Bekliyor":"#f59e0b","Cevaplandi":"#10b981","Beklemede":"#94a3b8"}
                dc = durum_colors.get(s.get("durum",""), "#94a3b8")
                onc_colors = {"Dusuk":"#94a3b8","Normal":"#3b82f6","Acil":"#ef4444"}
                oc = onc_colors.get(s.get("oncelik",""), "#94a3b8")

                st.markdown(f'''
                <div class="ek-card" style="border-left:4px solid {dc}">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div style="flex:1">
                            <div style="font-weight:700;font-size:0.88rem;color:#94A3B8">
                                {s.get("ders","")} - {s.get("konu","")}
                            </div>
                            <div style="font-size:0.78rem;color:#64748b;margin-top:2px">
                                {s.get("ogrenci_adi","")} &nbsp;|&nbsp; {s.get("tarih","")}
                            </div>
                            <div style="font-size:0.85rem;color:#334155;margin-top:8px;background:#111827;
                                padding:10px;border-radius:8px;border-left:3px solid #e2e8f0">
                                {s.get("soru_metni","")}
                            </div>
                        </div>
                        <div style="text-align:right;margin-left:12px">
                            {_badge(s.get("durum",""), dc)}
                            <div style="margin-top:4px">{_badge(s.get("oncelik",""), oc)}</div>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

                if s.get("durum") == "Cevaplandi" and s.get("cevap"):
                    st.markdown(f'''
                    <div style="margin-left:20px;padding:10px 14px;background:#f0fdf4;border-radius:8px;
                        border-left:3px solid #10b981;font-size:0.85rem;margin-bottom:12px">
                        <span style="font-weight:600;color:#10b981">Cevap ({s.get("cevaplayan","")}):</span><br>
                        {s.get("cevap","")}
                    </div>''', unsafe_allow_html=True)

                if s.get("durum") != "Cevaplandi":
                    with st.expander(f"Cevapla: {s.get('ders','')} - {s.get('konu','')}", expanded=False):
                        cevap = st.text_area("Cevabiniz", key=f"ek_sk_c_{s['id']}")
                        cevaplayan = st.text_input("Cevaplayan", key=f"ek_sk_cv_{s['id']}")
                        if st.button("Cevapla", key=f"ek_sk_u_{s['id']}", type="primary"):
                            store.update_item("soru_kutusu", s["id"], {
                                "durum": "Cevaplandi", "cevap": cevap,
                                "cevaplayan": cevaplayan, "cevap_tarihi": date.today().isoformat(),
                            })
                            st.success("Soru cevaplandi!")
                            st.rerun()

    with sub2:
        with st.form("ek_yeni_soru", clear_on_submit=True):
            st.markdown("##### Yeni Soru Sor")
            sc1, sc2 = st.columns(2)
            with sc1:
                s_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts.keys()), key="ek_ns_ogr2")
                s_ders = st.selectbox("Ders *", DERS_LISTESI, key="ek_ns_ders")
            with sc2:
                s_konu = st.text_input("Konu", key="ek_ns_konu")
                s_oncelik = st.selectbox("Oncelik", SORU_ONCELIKLERI, index=1, key="ek_ns_onc")
            s_soru = st.text_area("Soru Metni *", height=120, key="ek_ns_soru")

            if st.form_submit_button("Soru Gonder", type="primary", use_container_width=True):
                if s_ogr == "Seciniz" or not s_soru:
                    st.error("Ogrenci ve soru metni zorunludur.")
                else:
                    yeni = SoruKutusu(
                        ogrenci_id=ogr_opts[s_ogr], ogrenci_adi=s_ogr,
                        ders=s_ders, konu=s_konu, soru_metni=s_soru, oncelik=s_oncelik,
                    )
                    store.add_item("soru_kutusu", yeni.to_dict())
                    st.success("Soru kaydedildi!")
                    st.rerun()


# ============================================================
# SEKME 15: ONLINE TEST DENEME
# ============================================================

def _render_online_test(store: EKDataStore):
    """Online test ve deneme sinavi takibi."""
    styled_section("Online Test & Deneme Modulu", "#3b82f6")

    ogrenciler = store.load_list("ogrenciler")
    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

    sub1, sub2 = st.tabs(["📊 Test Sonuclari", "➕ Yeni Test Kaydi"])

    with sub1:
        if not ogr_opts:
            styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
            return

        sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_ot_ogr")
        ogr_id = ogr_opts.get(sec_ogr, "")
        testler = _load_consolidated_online(store, ogr_id)
        testler = sorted(testler, key=lambda x: x.get("tarih",""), reverse=True)

        if not testler:
            styled_info_banner("Test sonucu bulunmuyor.", "info", "📊")
        else:
            ort_puan = sum(t.get("puan",0) for t in testler) / len(testler)
            ort_net = sum(t.get("net",0) for t in testler) / len(testler)
            _diamond_stats([
                ("📝", str(len(testler)), "Toplam Test", "#6366f1"),
                ("📊", f"{ort_net:.1f}", "Ort. Net", "#3b82f6"),
                ("🎯", f"{ort_puan:.0f}", "Ort. Puan", "#10b981"),
                ("🔝", f"{max(t.get('puan',0) for t in testler):.0f}", "En Yuksek", "#f59e0b"),
            ])

            # Ders bazli analiz
            ders_map = {}
            for t in testler:
                d = t.get("ders", "Genel")
                if d not in ders_map:
                    ders_map[d] = {"toplam":0, "dogru":0, "yanlis":0, "net":0, "sayi":0}
                ders_map[d]["toplam"] += t.get("toplam_soru",0)
                ders_map[d]["dogru"] += t.get("dogru",0)
                ders_map[d]["yanlis"] += t.get("yanlis",0)
                ders_map[d]["net"] += t.get("net",0)
                ders_map[d]["sayi"] += 1

            if ders_map:
                styled_section("Ders Bazli Performans", "#8b5cf6")
                for ders, data in sorted(ders_map.items(), key=lambda x: -x[1]["net"]):
                    ort = data["net"] / data["sayi"] if data["sayi"] > 0 else 0
                    basari = (data["dogru"] / data["toplam"] * 100) if data["toplam"] > 0 else 0
                    color = "#10b981" if basari >= 70 else "#f59e0b" if basari >= 50 else "#ef4444"
                    st.markdown(f'''
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                        <div style="width:100px;font-weight:600;font-size:0.82rem;color:#334155">{ders}</div>
                        <div style="flex:1">
                            <div class="ek-progress-container">
                                <div class="ek-progress-bar" style="width:{basari}%;background:{color}"></div>
                            </div>
                        </div>
                        <div style="font-size:0.82rem;font-weight:700;color:{color}">{basari:.0f}%</div>
                        <div style="font-size:0.75rem;color:#64748b">({data["sayi"]} test, Ort:{ort:.1f} net)</div>
                    </div>''', unsafe_allow_html=True)

            # Test listesi
            styled_section("Test Gecmisi", "#6366f1")
            for t in testler:
                band = get_renk_bandi(t.get("puan", 0))
                st.markdown(f'''
                <div class="ek-card" style="border-left:4px solid {band["color"]}">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div>
                            <div style="font-weight:700;font-size:0.88rem;color:#94A3B8">{t.get("test_adi","")}</div>
                            <div style="font-size:0.75rem;color:#64748b;margin-top:2px">
                                {t.get("ders","")} - {t.get("konu","")} &nbsp;|&nbsp; {t.get("tarih","")} &nbsp;|&nbsp; {t.get("sure_dk",0)} dk
                            </div>
                            <div style="font-size:0.78rem;margin-top:6px">
                                <span style="color:#10b981;font-weight:600">D:{t.get("dogru",0)}</span>
                                <span style="color:#ef4444;font-weight:600;margin-left:8px">Y:{t.get("yanlis",0)}</span>
                                <span style="color:#94a3b8;font-weight:600;margin-left:8px">B:{t.get("bos",0)}</span>
                            </div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-size:1.4rem;font-weight:800;color:{band['color']}">{t.get("net",0)}</div>
                            <div style="font-size:0.7rem;color:#94a3b8">Net</div>
                            <div style="margin-top:4px">{_badge(band['label'], band['color'])}</div>
                        </div>
                    </div>
                </div>''', unsafe_allow_html=True)

    with sub2:
        with st.form("ek_yeni_test", clear_on_submit=True):
            st.markdown("##### Yeni Test Sonucu Kaydet")
            tc1, tc2 = st.columns(2)
            with tc1:
                t_ogr = st.selectbox("Ogrenci *", ["Seciniz"] + list(ogr_opts.keys()), key="ek_nt_ogr")
                t_ad = st.text_input("Test Adi *", key="ek_nt_ad")
                t_ders = st.selectbox("Ders", DERS_LISTESI, key="ek_nt_ders")
            with tc2:
                t_tarih = st.date_input("Tarih", value=date.today(), key="ek_nt_tarih")
                t_konu = st.text_input("Konu", key="ek_nt_konu")
                t_sure = st.number_input("Sure (dk)", 5, 180, 40, 5, key="ek_nt_sure")
            t_toplam = st.number_input("Toplam Soru", 1, 200, 20, key="ek_nt_toplam")
            tc3, tc4, tc5 = st.columns(3)
            with tc3:
                t_dogru = st.number_input("Dogru", 0, 200, 0, key="ek_nt_dogru")
            with tc4:
                t_yanlis = st.number_input("Yanlis", 0, 200, 0, key="ek_nt_yanlis")
            with tc5:
                t_bos = st.number_input("Bos", 0, 200, 0, key="ek_nt_bos")
            t_net = t_dogru - (t_yanlis / 4) if t_yanlis > 0 else float(t_dogru)
            t_puan = (t_net / t_toplam * 100) if t_toplam > 0 else 0
            st.markdown(f"**Net:** {t_net:.2f} &nbsp;|&nbsp; **Puan:** {t_puan:.1f}")

            if st.form_submit_button("Kaydet", type="primary", use_container_width=True):
                if t_ogr == "Seciniz" or not t_ad:
                    st.error("Ogrenci ve test adi zorunludur.")
                else:
                    yeni = OnlineTest(
                        ogrenci_id=ogr_opts[t_ogr], ogrenci_adi=t_ogr,
                        test_adi=t_ad, ders=t_ders, konu=t_konu,
                        tarih=t_tarih.isoformat(), sure_dk=t_sure,
                        toplam_soru=t_toplam, dogru=t_dogru, yanlis=t_yanlis, bos=t_bos,
                        net=round(t_net, 2), puan=round(t_puan, 1),
                    )
                    store.add_item("online_testler", yeni.to_dict())
                    st.success("Test sonucu kaydedildi!")
                    st.rerun()


# ============================================================
# SEKME 16: KONU & SORU ANALIZLERI
# ============================================================

def _render_konu_soru_analizi(store: EKDataStore):
    """Konu ve soru bazli analiz."""
    styled_section("Konu & Soru Analizleri", "#0d9488")

    ogrenciler = store.load_list("ogrenciler")
    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o["id"] for o in ogrenciler}

    if not ogr_opts:
        styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
        return

    sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_ksa_ogr")
    ogr_id = ogr_opts.get(sec_ogr, "")

    an_tabs = st.tabs(["📚 Konu Analizi", "❓ Soru Analizi"])

    with an_tabs[0]:
        # Deneme ve test verilerinden konu bazli analiz
        denemeler = _load_consolidated_deneme(store, ogr_id)
        testler = _load_consolidated_online(store, ogr_id)

        # Ders bazli konu performansi
        ders_konu = {}
        for t in testler:
            ders = t.get("ders","Genel")
            konu = t.get("konu","Genel")
            key = f"{ders} > {konu}" if konu else ders
            if key not in ders_konu:
                ders_konu[key] = {"dogru":0, "yanlis":0, "bos":0, "toplam":0, "test_sayi":0}
            ders_konu[key]["dogru"] += t.get("dogru",0)
            ders_konu[key]["yanlis"] += t.get("yanlis",0)
            ders_konu[key]["bos"] += t.get("bos",0)
            ders_konu[key]["toplam"] += t.get("toplam_soru",0)
            ders_konu[key]["test_sayi"] += 1

        # Deneme ders detaylarindan da ekle
        for d in denemeler:
            for dd in d.get("ders_detaylari", []):
                ders = dd.get("ders","Genel")
                if ders not in ders_konu:
                    ders_konu[ders] = {"dogru":0, "yanlis":0, "bos":0, "toplam":0, "test_sayi":0}
                ders_konu[ders]["dogru"] += dd.get("dogru",0)
                ders_konu[ders]["yanlis"] += dd.get("yanlis",0)
                ders_konu[ders]["bos"] += dd.get("bos",0)
                ders_konu[ders]["toplam"] += dd.get("dogru",0) + dd.get("yanlis",0) + dd.get("bos",0)
                ders_konu[ders]["test_sayi"] += 1

        if not ders_konu:
            styled_info_banner("Konu analizi icin test/deneme verisi gereklidir.", "info", "📚")
        else:
            # Basari sirasina gore sirala
            sorted_konular = sorted(ders_konu.items(), key=lambda x: (x[1]["dogru"]/x[1]["toplam"]*100 if x[1]["toplam"]>0 else 0))

            # En zayif konular
            styled_section("En Zayif Konular (Oncelikli Calisma)", "#ef4444")
            for konu, data in sorted_konular[:5]:
                basari = (data["dogru"] / data["toplam"] * 100) if data["toplam"] > 0 else 0
                color = "#ef4444" if basari < 50 else "#f59e0b" if basari < 70 else "#10b981"
                st.markdown(f'''
                <div class="ek-card" style="border-left:4px solid {color}">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div>
                            <div style="font-weight:700;font-size:0.88rem;color:#94A3B8">{konu}</div>
                            <div style="font-size:0.75rem;color:#64748b">
                                D:{data["dogru"]} Y:{data["yanlis"]} B:{data["bos"]} ({data["test_sayi"]} test)
                            </div>
                        </div>
                        <div style="font-size:1.4rem;font-weight:800;color:{color}">%{basari:.0f}</div>
                    </div>
                </div>''', unsafe_allow_html=True)
                _progress_bar(basari)

            # En guclu konular
            styled_section("En Guclu Konular", "#10b981")
            for konu, data in reversed(sorted_konular[-5:]):
                basari = (data["dogru"] / data["toplam"] * 100) if data["toplam"] > 0 else 0
                color = "#10b981" if basari >= 70 else "#f59e0b"
                st.markdown(f'''
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
                    <div style="width:180px;font-weight:600;font-size:0.82rem;color:#334155">{konu}</div>
                    <div style="flex:1">
                        <div class="ek-progress-container">
                            <div class="ek-progress-bar" style="width:{basari}%;background:{color}"></div>
                        </div>
                    </div>
                    <div style="font-size:0.82rem;font-weight:700;color:{color}">%{basari:.0f}</div>
                </div>''', unsafe_allow_html=True)

    with an_tabs[1]:
        # Soru kutusu analizi
        sorular = store.get_by_ogrenci("soru_kutusu", ogr_id)
        if not sorular:
            styled_info_banner("Soru kutusu verisi bulunmuyor.", "info", "❓")
        else:
            # Ders bazli soru dagilimi
            ders_soru = {}
            for s in sorular:
                d = s.get("ders","Diger")
                ders_soru[d] = ders_soru.get(d, 0) + 1

            styled_section("Ders Bazli Soru Dagilimi", "#6366f1")
            sorted_ders = sorted(ders_soru.items(), key=lambda x: -x[1])
            max_s = sorted_ders[0][1] if sorted_ders else 1
            for ders, sayi in sorted_ders:
                pct = (sayi / max_s * 100)
                st.markdown(f'''
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
                    <div style="width:100px;font-weight:600;font-size:0.82rem;color:#334155">{ders}</div>
                    <div style="flex:1">
                        <div class="ek-progress-container">
                            <div class="ek-progress-bar" style="width:{pct}%"></div>
                        </div>
                    </div>
                    <div style="font-size:0.82rem;font-weight:700;color:#6366f1">{sayi} soru</div>
                </div>''', unsafe_allow_html=True)

            # Cevap bekleyen sorular
            bekleyen = [s for s in sorular if s.get("durum") == "Cevap Bekliyor"]
            if bekleyen:
                styled_section(f"Cevap Bekleyen ({len(bekleyen)} soru)", "#f59e0b")
                for s in bekleyen:
                    st.markdown(f'''
                    <div class="ek-card" style="border-left:3px solid #f59e0b">
                        <div style="font-weight:600;font-size:0.85rem">{s.get("ders","")} - {s.get("konu","")}</div>
                        <div style="font-size:0.82rem;color:#475569;margin-top:4px">{s.get("soru_metni","")[:150]}</div>
                        <div style="font-size:0.72rem;color:#94a3b8;margin-top:4px">{s.get("tarih","")}</div>
                    </div>''', unsafe_allow_html=True)


# ============================================================
# SEKME 17: AI KOCLUK ANALIZI
# ============================================================

def _render_ai_analiz(store: EKDataStore):
    """AI destekli kapsamli kocluk analizi."""
    styled_section("AI Kocluk Analizi & Degerlendirme", "#7c3aed")

    client = _get_ai_client()
    if not client:
        styled_info_banner("OpenAI API anahtari bulunamadi. Lutfen .env dosyasinda OPENAI_API_KEY tanimlayin.", "error", "🔑")
        return

    ogrenciler = store.load_list("ogrenciler")
    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')}": o for o in ogrenciler}

    if not ogr_opts:
        styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
        return

    sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_ai_ogr")
    ogr = ogr_opts.get(sec_ogr)
    if not ogr:
        return

    ogr_id = ogr["id"]

    # AI Analiz Alt Sekmeleri
    ai_tabs = st.tabs([
        "🧠 Kapsamli Kocluk Analizi",
        "📅 AI Haftalik Plan",
        "🔥 Motivasyon Mesaji",
        "📋 AI Veli Raporu",
    ])

    # === 1. KAPSAMLI KOCLUK ANALIZI ===
    with ai_tabs[0]:
        st.markdown(f'''
        <div class="ek-glass">
            <div style="text-align:center">
                <div style="font-size:1.1rem;font-weight:800;
                    background:linear-gradient(135deg,#7c3aed,#6366f1);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                    AI Destekli 360° Kocluk Analizi
                </div>
                <div style="font-size:0.78rem;color:#64748b;margin-top:4px">
                    Tum verileri analiz ederek kapsamli bir degerlendirme raporu olusturur
                </div>
            </div>
        </div>''', unsafe_allow_html=True)

        if st.button("🧠 AI Analizi Baslat", key="ek_ai_start", type="primary", use_container_width=True):
            gorusmeler = store.get_by_ogrenci("gorusmeler", ogr_id)
            hedefler = store.get_by_ogrenci("hedefler", ogr_id)
            planlar = store.get_by_ogrenci("haftalik_planlar", ogr_id)
            motivasyonlar = store.get_by_ogrenci("motivasyon", ogr_id)
            denemeler = _load_consolidated_deneme(store, ogr_id)

            with st.spinner("AI analiz yapiyor... Tum veriler inceleniyor..."):
                result = _ai_kocluk_analizi(client, ogr, gorusmeler, hedefler, motivasyonlar, denemeler, planlar)

            if not result:
                st.error("AI analizi tamamlanamadi.")
            elif result.get("error"):
                st.error(result["error"])
            else:
                st.session_state["_ek_ai_result"] = result
                st.session_state["_ek_ai_ogr_name"] = sec_ogr

        # Sonuclari goster
        result = st.session_state.get("_ek_ai_result")
        ai_name = st.session_state.get("_ek_ai_ogr_name", "")
        if result and not result.get("error") and ai_name == sec_ogr:
            # Genel durum header
            genel_puan = result.get("genel_puan", 0)
            band = get_renk_bandi(genel_puan)
            emoji = result.get("emoji_durum", "📊")
            baslik = result.get("baslik_durum", "")

            st.markdown(f'''
            <div class="ek-glass" style="border-top:4px solid {band["color"]}">
                <div style="display:flex;align-items:center;justify-content:space-between">
                    <div>
                        <div style="font-size:2rem;margin-bottom:4px">{emoji}</div>
                        <div style="font-size:1.1rem;font-weight:800;color:#94A3B8">{sec_ogr}</div>
                        <div style="font-size:0.85rem;color:#64748b;margin-top:4px">{result.get("genel_degerlendirme","")}</div>
                    </div>
                    <div style="text-align:center">
                        <div style="font-size:2.8rem;font-weight:900;color:{band["color"]}">{genel_puan}</div>
                        <div style="font-size:0.78rem;font-weight:700;color:{band["color"]}">{baslik}</div>
                    </div>
                </div>
            </div>''', unsafe_allow_html=True)

            # 4 Puan Karti
            akad = result.get("akademik_analiz", {})
            motiv = result.get("motivasyon_analiz", {})
            verim = result.get("calisma_verimi", {})
            hedef_il = result.get("hedef_ilerleme", {})

            _diamond_stats([
                ("📚", str(akad.get("akademik_puan", 0)), "Akademik", "#6366f1"),
                ("🔥", str(motiv.get("motivasyon_puan", 0)), "Motivasyon", "#ec4899"),
                ("⏰", str(verim.get("verimlilik_puan", 0)), "Verimlilik", "#3b82f6"),
                ("🎯", str(hedef_il.get("ilerleme_puan", 0)), "Hedef Ilerleme", "#10b981"),
            ])

            st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)

            # Akademik Analiz
            col1, col2 = st.columns(2)
            with col1:
                styled_section("Guclu Yonler", "#10b981")
                for item in akad.get("guclu_yonler", []):
                    st.markdown(f'<div style="padding:6px 12px;background:#f0fdf4;border-radius:8px;margin-bottom:4px;font-size:0.85rem;border-left:3px solid #10b981">✅ {item}</div>', unsafe_allow_html=True)

            with col2:
                styled_section("Gelistirme Alanlari", "#f59e0b")
                for item in akad.get("gelistirme_alanlari", []):
                    st.markdown(f'<div style="padding:6px 12px;background:#fffbeb;border-radius:8px;margin-bottom:4px;font-size:0.85rem;border-left:3px solid #f59e0b">⚠️ {item}</div>', unsafe_allow_html=True)

            # Motivasyon Analiz
            st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
            styled_section("Motivasyon Degerlendirmesi", "#ec4899")
            st.markdown(f'<div class="ek-card">{motiv.get("genel_durum","")}</div>', unsafe_allow_html=True)

            mc1, mc2 = st.columns(2)
            with mc1:
                for item in motiv.get("guclu_alanlar", []):
                    st.markdown(f"- 💪 {item}")
            with mc2:
                for item in motiv.get("risk_alanlari", []):
                    st.markdown(f"- ⚠️ {item}")

            # Calisma Verimi
            st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
            styled_section("Calisma Verimi & Iyilestirme", "#3b82f6")
            st.markdown(f'<div class="ek-card">{verim.get("degerlendirme","")}</div>', unsafe_allow_html=True)
            for i, item in enumerate(verim.get("iyilestirme_onerileri", []), 1):
                st.markdown(f'<div style="padding:8px 14px;background:#eff6ff;border-radius:8px;margin-bottom:4px;font-size:0.85rem;border-left:3px solid #3b82f6">📌 {i}. {item}</div>', unsafe_allow_html=True)

            # Haftalik Eylem Plani
            st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
            styled_section("Haftalik Eylem Plani", "#6366f1")
            for item in result.get("haftalik_eylem_plani", []):
                st.markdown(f'<div style="padding:8px 14px;background:#eef2ff;border-radius:8px;margin-bottom:4px;font-size:0.85rem;border-left:3px solid #6366f1">📋 {item}</div>', unsafe_allow_html=True)

            # Koc Onerileri
            st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
            styled_section("Koc Onerileri (Kisa-Orta-Uzun Vade)", "#d4a017")
            for item in result.get("koc_onerileri", []):
                st.markdown(f'<div style="padding:10px 16px;background:linear-gradient(135deg,#fffbeb,#fef3c7);border-radius:10px;margin-bottom:6px;font-size:0.88rem;border-left:4px solid #d4a017;font-weight:500">🏆 {item}</div>', unsafe_allow_html=True)

            # Veli Mesaji
            st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
            styled_section("Veliye Mesaj", "#0d9488")
            st.markdown(f'''
            <div class="ek-glass" style="border-left:4px solid #0d9488">
                <div style="font-size:0.88rem;color:#334155;line-height:1.6">
                    👨‍👩‍👧 {result.get("veli_mesaji","")}
                </div>
            </div>''', unsafe_allow_html=True)

    # === 2. AI HAFTALIK PLAN ===
    with ai_tabs[1]:
        st.markdown(f'''
        <div class="ek-glass">
            <div style="text-align:center">
                <div style="font-size:1.1rem;font-weight:800;
                    background:linear-gradient(135deg,#3b82f6,#06b6d4);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                    AI Kisisellestirilmis Haftalik Plan
                </div>
                <div style="font-size:0.78rem;color:#64748b;margin-top:4px">
                    Deneme sonuclari ve zayif alanlara gore optimize edilmis calisma programi
                </div>
            </div>
        </div>''', unsafe_allow_html=True)

        if st.button("📅 AI Plan Olustur", key="ek_ai_plan", type="primary", use_container_width=True):
            denemeler = _load_consolidated_deneme(store, ogr_id)
            motivasyonlar = store.get_by_ogrenci("motivasyon", ogr_id)

            with st.spinner("AI kisisellestirilmis plan olusturuyor..."):
                plan_result = _ai_haftalik_plan_onerisi(client, ogr, denemeler, motivasyonlar)

            if plan_result and not plan_result.get("error"):
                st.session_state["_ek_ai_plan"] = plan_result
                st.session_state["_ek_ai_plan_ogr"] = sec_ogr
            elif plan_result and plan_result.get("error"):
                st.error(plan_result["error"])

        plan_result = st.session_state.get("_ek_ai_plan")
        plan_ogr = st.session_state.get("_ek_ai_plan_ogr", "")
        if plan_result and not plan_result.get("error") and plan_ogr == sec_ogr:
            st.markdown(f'<div class="ek-card"><strong>Plan Aciklama:</strong> {plan_result.get("plan_aciklama","")}</div>', unsafe_allow_html=True)

            for gun_data in plan_result.get("plan", []):
                gun = gun_data.get("gun", "")
                etkinlikler = gun_data.get("etkinlikler", [])
                st.markdown(f'''
                <div style="background:linear-gradient(135deg,#4f46e5,#6366f1);color:white;
                    padding:8px 16px;border-radius:8px;margin-top:12px;margin-bottom:6px;
                    font-weight:700;font-size:0.88rem">
                    📅 {gun}
                </div>''', unsafe_allow_html=True)

                for e in etkinlikler:
                    onc_color = {"Yuksek":"#ef4444","Orta":"#f59e0b","Dusuk":"#10b981"}.get(e.get("oncelik","Orta"),"#94a3b8")
                    st.markdown(f'''
                    <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;
                        background:white;border:1px solid #e2e8f0;border-radius:8px;
                        margin-bottom:4px;font-size:0.82rem">
                        <span style="font-weight:600;color:#6366f1;min-width:90px">{e.get("saat","")}</span>
                        <span class="ek-badge" style="background:#eef2ff;color:#4f46e5">{e.get("ders","")}</span>
                        <span style="color:#475569">{e.get("etkinlik","")} - {e.get("konu","")}</span>
                        <span style="margin-left:auto">{_badge(e.get("oncelik",""), onc_color)}</span>
                    </div>''', unsafe_allow_html=True)

            # Onemli notlar
            notlar = plan_result.get("onemli_notlar", [])
            if notlar:
                st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
                styled_section("Onemli Notlar", "#f59e0b")
                for n in notlar:
                    st.markdown(f'<div style="padding:6px 12px;background:#fffbeb;border-radius:8px;margin-bottom:4px;font-size:0.85rem;border-left:3px solid #f59e0b">📝 {n}</div>', unsafe_allow_html=True)

            # Plani kaydetme butonu
            st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
            if st.button("💾 Bu Plani Haftalik Plana Kaydet", key="ek_ai_plan_kaydet", type="secondary", use_container_width=True):
                etkinlik_list = []
                for gun_data in plan_result.get("plan", []):
                    gun = gun_data.get("gun", "")
                    for e in gun_data.get("etkinlikler", []):
                        saat = e.get("saat", "").split("-")[0] if "-" in e.get("saat","") else e.get("saat","")
                        etkinlik_list.append({
                            "gun": gun, "saat": saat, "ders": e.get("ders",""),
                            "etkinlik_turu": e.get("etkinlik","Ders Calismasi"),
                            "konu": e.get("konu",""), "sure_dk": 60, "tamamlandi": False,
                        })
                bugun = date.today()
                yeni_plan = HaftalikPlan(
                    ogrenci_id=ogr_id, ogrenci_adi=sec_ogr,
                    hafta_baslangic=bugun.isoformat(),
                    hafta_bitis=(bugun + timedelta(days=6)).isoformat(),
                    etkinlikler=etkinlik_list,
                    toplam_saat=len(etkinlik_list),
                )
                store.add_item("haftalik_planlar", yeni_plan.to_dict())
                st.success("AI plani haftalik planlara kaydedildi!")

    # === 3. MOTIVASYON MESAJI ===
    with ai_tabs[2]:
        st.markdown(f'''
        <div class="ek-glass">
            <div style="text-align:center">
                <div style="font-size:1.1rem;font-weight:800;
                    background:linear-gradient(135deg,#f59e0b,#ef4444);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                    Kisisellestirilmis Motivasyon Mesaji
                </div>
                <div style="font-size:0.78rem;color:#64748b;margin-top:4px">
                    Ogrenciye ozel ilham verici ve motive edici mesaj olusturur
                </div>
            </div>
        </div>''', unsafe_allow_html=True)

        if st.button("🔥 Motivasyon Mesaji Olustur", key="ek_ai_motiv", type="primary", use_container_width=True):
            motivasyonlar = store.get_by_ogrenci("motivasyon", ogr_id)
            with st.spinner("AI motivasyon mesaji olusturuyor..."):
                mesaj = _ai_motivasyon_mesaji(client, ogr, motivasyonlar)
            st.session_state["_ek_ai_motiv_msg"] = mesaj
            st.session_state["_ek_ai_motiv_ogr"] = sec_ogr

        motiv_msg = st.session_state.get("_ek_ai_motiv_msg", "")
        motiv_ogr = st.session_state.get("_ek_ai_motiv_ogr", "")
        if motiv_msg and motiv_ogr == sec_ogr:
            st.markdown(f'''
            <div class="ek-glass" style="border: 2px solid #f59e0b;
                background:linear-gradient(145deg,#fffbeb,#fef3c7,#fff)">
                <div style="font-size:0.92rem;color:#334155;line-height:1.8;white-space:pre-wrap">
                    {motiv_msg}
                </div>
            </div>''', unsafe_allow_html=True)

    # === 4. AI VELI RAPORU ===
    with ai_tabs[3]:
        st.markdown(f'''
        <div class="ek-glass">
            <div style="text-align:center">
                <div style="font-size:1.1rem;font-weight:800;
                    background:linear-gradient(135deg,#0d9488,#10b981);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                    AI Destekli Veli Raporu
                </div>
                <div style="font-size:0.78rem;color:#64748b;margin-top:4px">
                    Tum verileri analiz ederek profesyonel veli raporu olusturur
                </div>
            </div>
        </div>''', unsafe_allow_html=True)

        vc1, vc2 = st.columns(2)
        with vc1:
            vr_donem = st.selectbox("Donem", ["1. Donem","2. Donem","Yillik","Ara Rapor"], key="ek_ai_vr_donem")
        with vc2:
            vr_veli = st.text_input("Veli Adi", ogr.get("veli_adi",""), key="ek_ai_vr_veli")

        if st.button("📋 AI Veli Raporu Olustur", key="ek_ai_vr_start", type="primary", use_container_width=True):
            gorusmeler = store.get_by_ogrenci("gorusmeler", ogr_id)
            hedefler = store.get_by_ogrenci("hedefler", ogr_id)
            motivasyonlar = store.get_by_ogrenci("motivasyon", ogr_id)
            denemeler = _load_consolidated_deneme(store, ogr_id)

            with st.spinner("AI veli raporu olusturuyor..."):
                vr_result = _ai_veli_raporu_olustur(client, ogr, gorusmeler, hedefler, motivasyonlar, denemeler)

            if vr_result and not vr_result.get("error"):
                st.session_state["_ek_ai_vr"] = vr_result
                st.session_state["_ek_ai_vr_ogr"] = sec_ogr
            elif vr_result and vr_result.get("error"):
                st.error(vr_result["error"])

        vr_result = st.session_state.get("_ek_ai_vr")
        vr_name = st.session_state.get("_ek_ai_vr_ogr", "")
        if vr_result and not vr_result.get("error") and vr_name == sec_ogr:
            # Rapor onizleme
            st.markdown(f'''
            <div class="ek-glass" style="border:2px solid #0d9488">
                <div style="text-align:center;margin-bottom:16px">
                    <div style="font-size:1.1rem;font-weight:800;color:#0d9488">Veli Raporu - {sec_ogr}</div>
                    <div style="font-size:0.78rem;color:#64748b">Donem: {vr_donem} | Tarih: {date.today().isoformat()}</div>
                </div>
            </div>''', unsafe_allow_html=True)

            sections = [
                ("Genel Durum", vr_result.get("genel_durum",""), "#94A3B8", "📊"),
                ("Akademik Ozet", vr_result.get("akademik_ozet",""), "#6366f1", "📚"),
                ("Motivasyon Durumu", vr_result.get("motivasyon_ozet",""), "#ec4899", "🔥"),
                ("Hedef Ilerleme", vr_result.get("hedef_ilerleme",""), "#f59e0b", "🎯"),
                ("Oneriler", vr_result.get("oneriler",""), "#10b981", "💡"),
                ("Koc Notu", vr_result.get("koc_notu",""), "#0d9488", "📝"),
            ]
            for title, content, color, icon in sections:
                if content:
                    st.markdown(f'''
                    <div class="ek-card" style="border-left:4px solid {color}">
                        <div style="font-weight:700;font-size:0.88rem;color:{color};margin-bottom:6px">{icon} {title}</div>
                        <div style="font-size:0.85rem;color:#334155;line-height:1.6">{content}</div>
                    </div>''', unsafe_allow_html=True)

            # Kaydetme butonu
            st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
            if st.button("💾 Raporu Veli Raporlarina Kaydet", key="ek_ai_vr_kaydet", type="secondary", use_container_width=True):
                yeni_rapor = VeliRapor(
                    ogrenci_id=ogr_id, ogrenci_adi=sec_ogr,
                    veli_adi=vr_veli or ogr.get("veli_adi",""),
                    tarih=date.today().isoformat(), donem=vr_donem,
                    genel_durum=vr_result.get("genel_durum",""),
                    akademik_ozet=vr_result.get("akademik_ozet",""),
                    motivasyon_ozet=vr_result.get("motivasyon_ozet",""),
                    hedef_ilerleme=vr_result.get("hedef_ilerleme",""),
                    oneriler=vr_result.get("oneriler",""),
                    koc_notu=vr_result.get("koc_notu",""),
                )
                store.add_item("veli_raporlari", yeni_rapor.to_dict())
                st.success("AI raporu veli raporlarina kaydedildi!")


# ============================================================
# SEKME 12: AYARLAR
# ============================================================

def _render_ayarlar(store: EKDataStore):
    """Modul ayarlari."""
    styled_section("Modul Ayarlari", "#64748b")

    ayarlar_list = store.load_list("ek_ayarlar")
    ayar = ayarlar_list[0] if ayarlar_list else KoclukAyar().to_dict()

    with st.form("ek_ayarlar_form"):
        c1, c2 = st.columns(2)
        with c1:
            a_sure = st.number_input("Gorusme Suresi (dk)", min_value=15, max_value=120,
                value=ayar.get("gorusme_suresi_dk", 45), step=15, key="ek_a_sure")
            a_haftalik = st.number_input("Haftalik Gorusme Sayisi", min_value=1, max_value=5,
                value=ayar.get("haftalik_gorusme", 1), key="ek_a_haftalik")
        with c2:
            a_rapor = st.selectbox("Veli Rapor Sikligi", ["Haftalik","Aylik","Donemlik"],
                index=["Haftalik","Aylik","Donemlik"].index(ayar.get("veli_rapor_sikligi","Aylik")) if ayar.get("veli_rapor_sikligi","Aylik") in ["Haftalik","Aylik","Donemlik"] else 1,
                key="ek_a_rapor")
            a_hatirlatma = st.checkbox("Otomatik Hatirlatma", value=ayar.get("otomatik_hatirlatma", True), key="ek_a_hatirlatma")
        a_motivasyon = st.checkbox("Motivasyon Takibi Aktif", value=ayar.get("motivasyon_takip", True), key="ek_a_motivasyon")

        if st.form_submit_button("Ayarlari Kaydet", type="primary", use_container_width=True):
            yeni_ayar = KoclukAyar(
                gorusme_suresi_dk=a_sure, haftalik_gorusme=a_haftalik,
                motivasyon_takip=a_motivasyon, veli_rapor_sikligi=a_rapor,
                otomatik_hatirlatma=a_hatirlatma,
            ).to_dict()
            if ayarlar_list:
                store.update_item("ek_ayarlar", ayar.get("id","ek_ayar_01"), yeni_ayar)
            else:
                store.add_item("ek_ayarlar", yeni_ayar)
            st.success("Ayarlar kaydedildi!")
            st.rerun()


# ============================================================
# SEKME: OGRENCI OLCME SON DURUM (KAPSAMLI AI DESTEKLI)
# ============================================================

def _olcme_pdf_rapor(ogr: dict, denemeler: list, ders_ozet: dict,
                      genel_stats: dict, ai_yorum: str | None) -> bytes | None:
    """Ultra Premium Diamond Olcme Son Durum PDF v2 - Full page, zero white space."""
    try:
        import io, math
        from utils.shared_data import ensure_turkish_pdf_fonts
        font_name, font_bold = ensure_turkish_pdf_fonts()
        from reportlab.pdfgen import canvas as pdf_canvas
        from reportlab.lib import colors as rl_colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm, mm
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics.charts.piecharts import Pie
        from reportlab.graphics.charts.barcharts import VerticalBarChart
        from reportlab.graphics import renderPDF
    except Exception:
        return None

    buffer = io.BytesIO()
    pw, ph = A4
    c = pdf_canvas.Canvas(buffer, pagesize=A4)

    # ── RENK PALETI ──
    NAVY = rl_colors.HexColor("#0f2744")
    GOLD = rl_colors.HexColor("#C8952E")
    GOLD_BG = rl_colors.HexColor("#FFF8E1")
    ZEBRA_GOLD = rl_colors.HexColor("#FFFBF0")
    INDIGO = rl_colors.HexColor("#4f46e5")
    DARK = rl_colors.HexColor("#94A3B8")
    GRAY = rl_colors.HexColor("#64748b")
    WHITE = rl_colors.white
    GREEN_C = rl_colors.HexColor("#10b981")
    RED_C = rl_colors.HexColor("#ef4444")
    BLUE_C = rl_colors.HexColor("#3b82f6")
    ORANGE_C = rl_colors.HexColor("#f97316")
    PURPLE_C = rl_colors.HexColor("#8b5cf6")
    CYAN_C = rl_colors.HexColor("#06b6d4")
    ROSE_C = rl_colors.HexColor("#f43f5e")

    ML = 1.4 * cm
    MR = 1.4 * cm
    MT = 1.2 * cm
    MB = 1.3 * cm
    UW = pw - ML - MR
    page_num = [0]

    # ── YARDIMCI FONKSİYONLAR ──
    def _gold_line(y, thick=2.5, thin=0.5, gap=3):
        c.setStrokeColor(GOLD)
        c.setLineWidth(thick)
        c.line(ML, y, pw - MR, y)
        c.setStrokeColor(NAVY)
        c.setLineWidth(thin)
        c.line(ML, y - gap, pw - MR, y - gap)

    def _section_header(y, title, icon="\u25c6"):
        c.setFillColor(NAVY)
        c.rect(ML, y - 18, UW, 22, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.2)
        c.line(ML, y + 4, ML + UW * 0.25, y + 4)
        c.line(ML + UW * 0.75, y + 4, ML + UW, y + 4)
        c.setFillColor(WHITE)
        c.setFont(font_bold, 9.5)
        c.drawString(ML + 8, y - 13, f"{icon}  {title}")
        c.setFillColor(GOLD)
        c.setFont(font_bold, 6.5)
        c.drawRightString(pw - MR - 8, y - 13, "\u25c6 SmartCampus AI \u25c6")
        return y - 26

    def _dm(x, y, s=3):
        """Diamond accent."""
        c.saveState()
        c.setFillColor(GOLD)
        c.translate(x, y)
        c.rotate(45)
        c.rect(-s / 2, -s / 2, s, s, fill=1, stroke=0)
        c.restoreState()

    def _progress_rect(x, y, w, h, pct, fg_color, bg_color=rl_colors.HexColor("#e2e8f0")):
        """Horizontal progress bar."""
        c.setFillColor(bg_color)
        c.roundRect(x, y, w, h, h / 2, fill=1, stroke=0)
        fill_w = max(h, w * min(pct, 100) / 100)
        c.setFillColor(fg_color)
        c.roundRect(x, y, fill_w, h, h / 2, fill=1, stroke=0)

    def _score_gauge(cx, cy, radius, score, max_score, label, color):
        """Circular score gauge."""
        import math as _m
        # Outer ring background
        c.setStrokeColor(rl_colors.HexColor("#e2e8f0"))
        c.setLineWidth(6)
        c.circle(cx, cy, radius, stroke=1, fill=0)
        # Score arc
        pct = min(score / max_score, 1.0) if max_score > 0 else 0
        if pct > 0:
            c.setStrokeColor(color)
            c.setLineWidth(6)
            start_angle = 90
            extent = -pct * 360
            p = c.beginPath()
            p.arc(cx - radius, cy - radius, cx + radius, cy + radius, start_angle, extent)
            c.drawPath(p, stroke=1, fill=0)
        # Inner circle
        c.setFillColor(WHITE)
        c.circle(cx, cy, radius - 8, stroke=0, fill=1)
        # Score text
        c.setFont(font_bold, 14)
        c.setFillColor(color)
        c.drawCentredString(cx, cy + 2, f"{score:.0f}")
        # Label
        c.setFont(font_name, 6)
        c.setFillColor(GRAY)
        c.drawCentredString(cx, cy - 10, label)

    def _draw_hf(pg):
        _gold_line(ph - MT)
        c.setFont(font_bold, 7)
        c.setFillColor(NAVY)
        c.drawString(ML, ph - MT + 6, "OGRENCI OLCME SON DURUM RAPORU")
        c.setFillColor(GOLD)
        c.drawRightString(pw - MR, ph - MT + 6, f"Sayfa {pg}")
        for dx in range(3):
            _dm(pw / 2 - 8 + dx * 8, ph - MT + 9, 2)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.5)
        c.line(ML, MB - 4, pw - MR, MB - 4)
        c.setStrokeColor(NAVY)
        c.setLineWidth(0.4)
        c.line(ML, MB - 7, pw - MR, MB - 7)
        c.setFont(font_name, 6)
        c.setFillColor(GRAY)
        c.drawString(ML, MB - 16, f"SmartCampus AI  \u25c6  Egitim Koclugu  \u25c6  {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        c.setFillColor(NAVY)
        c.drawRightString(pw - MR, MB - 16, "\u25c6 \u25c6 \u25c6  Gizli  \u25c6 \u25c6 \u25c6")

    def _watermark():
        c.saveState()
        c.setFillColor(rl_colors.HexColor("#f4f4fa"))
        c.setFont(font_bold, 48)
        c.translate(pw / 2, ph / 2)
        c.rotate(35)
        c.drawCentredString(0, 0, "SmartCampus AI")
        c.restoreState()

    def _new_page():
        c.showPage()
        page_num[0] += 1
        _watermark()
        _draw_hf(page_num[0])

    def _wrap(text, font, size, max_w):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            test = f"{cur} {w}".strip()
            if c.stringWidth(test, font, size) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines or [""]

    gs = genel_stats
    ort_puan = gs.get("ort_puan", 0)
    band_info = get_renk_bandi(ort_puan)

    # ════════════════════════════════════════
    #         SAYFA 1: ULTRA KAPAK
    # ════════════════════════════════════════
    page_num[0] = 1
    _watermark()

    # Outer double frame
    c.setStrokeColor(GOLD)
    c.setLineWidth(3)
    c.rect(ML - 8, MB - 8, UW + 16, ph - MT - MB + 16, fill=0, stroke=1)
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.7)
    c.rect(ML - 4, MB - 4, UW + 8, ph - MT - MB + 8, fill=0, stroke=1)

    y = ph - 2.5 * cm
    # Top diamond ornament row
    for dx in range(9):
        _dm(ML + UW * 0.1 + dx * UW * 0.1, y + 6, 4.5)
    _gold_line(y, thick=3, thin=0.8, gap=4)
    y -= 1 * cm

    c.setFillColor(NAVY)
    c.setFont(font_bold, 9)
    c.drawCentredString(pw / 2, y, "T.C.")
    y -= 14
    c.setFont(font_bold, 13)
    c.drawCentredString(pw / 2, y, "SMARTCAMPUS AI EGITIM PLATFORMU")
    y -= 12
    c.setFont(font_name, 8)
    c.setFillColor(GOLD)
    c.drawCentredString(pw / 2, y, "\u25c6  \u25c6  \u25c6  \u25c6  \u25c6")
    y -= 1 * cm

    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5)
    c.line(ML + 2.5 * cm, y, pw - MR - 2.5 * cm, y)
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.6)
    c.line(ML + 2.5 * cm, y - 3.5, pw - MR - 2.5 * cm, y - 3.5)
    y -= 1.5 * cm

    c.setFillColor(NAVY)
    c.setFont(font_bold, 26)
    c.drawCentredString(pw / 2, y, "OLCME SON DURUM RAPORU")
    y -= 20
    c.setFont(font_bold, 13)
    c.setFillColor(GOLD)
    c.drawCentredString(pw / 2, y, "Kapsamli Akademik Performans Analizi")
    y -= 12
    c.setFont(font_name, 9)
    c.setFillColor(GRAY)
    c.drawCentredString(pw / 2, y, "AI Destekli  \u25c6  Veri Odakli  \u25c6  Profesyonel")
    y -= 1 * cm

    # ── PERFORMANS GAUGE CLUSTER ──
    gauge_y = y - 2.2 * cm
    gauge_r = 28
    gauges = [
        (pw / 2 - 3.8 * cm, gauge_y, gs.get("ort_net", 0), 120, "ORT NET", INDIGO),
        (pw / 2 - 1.2 * cm, gauge_y, ort_puan, 100, "ORT PUAN", rl_colors.HexColor(band_info["color"])),
        (pw / 2 + 1.4 * cm, gauge_y, gs.get("max_net", 0), 120, "MAX NET", GREEN_C),
        (pw / 2 + 4 * cm, gauge_y, float(gs.get("toplam", 0)), 50, "SINAV", PURPLE_C),
    ]
    # Gauge background panel
    panel_w = 10 * cm
    c.setFillColor(rl_colors.HexColor("#FAFBFF"))
    c.setStrokeColor(rl_colors.HexColor("#E0E7FF"))
    c.setLineWidth(0.8)
    c.roundRect(pw / 2 - panel_w / 2, gauge_y - gauge_r - 18, panel_w, gauge_r * 2 + 30, 10, fill=1, stroke=1)
    for gx, gy, gval, gmax, glbl, gcol in gauges:
        _score_gauge(gx, gy, gauge_r, gval, gmax, glbl, gcol)
    y = gauge_y - gauge_r - 28

    # ── OGRENCI BILGI KUTUSU ──
    y -= 0.4 * cm
    box_h = 3.6 * cm
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.8)
    c.setFillColor(rl_colors.HexColor("#FEFCF3"))
    c.roundRect(ML + 0.5 * cm, y - box_h, UW - 1 * cm, box_h, 8, fill=1, stroke=1)
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.4)
    c.roundRect(ML + 0.5 * cm + 3, y - box_h + 3, UW - 1 * cm - 6, box_h - 6, 6, fill=0, stroke=1)

    bx = ML + 1.2 * cm
    by = y - 16
    c.setFillColor(NAVY)
    c.setFont(font_bold, 9.5)
    c.drawString(bx, by, "OGRENCI BILGILERI")
    _dm(bx + c.stringWidth("OGRENCI BILGILERI", font_bold, 9.5) + 8, by + 4, 3)
    by -= 4
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(bx, by, bx + UW - 3 * cm, by)
    by -= 14

    half = UW / 2 - 0.5 * cm
    info_pairs = [
        ("Ogrenci:", f"{ogr.get('ad','')} {ogr.get('soyad','')}",
         "Sinif / Sube:", f"{ogr.get('sinif','')}/{ogr.get('sube','')}"),
        ("Hedef Sinav:", ogr.get("hedef_sinav", "-"),
         "Hedef Puan:", ogr.get("hedef_puan", "-")),
        ("Koc:", ogr.get("koc_adi", "-"),
         "Rapor Tarihi:", datetime.now().strftime("%d.%m.%Y")),
    ]
    for lab1, val1, lab2, val2 in info_pairs:
        c.setFont(font_bold, 8)
        c.setFillColor(NAVY)
        c.drawString(bx, by, lab1)
        c.setFont(font_name, 8)
        c.setFillColor(DARK)
        c.drawString(bx + 62, by, val1)
        c.setFont(font_bold, 8)
        c.setFillColor(NAVY)
        c.drawString(bx + half, by, lab2)
        c.setFont(font_name, 8)
        c.setFillColor(DARK)
        c.drawString(bx + half + 62, by, val2)
        by -= 14

    by -= 2
    c.setFont(font_bold, 7.5)
    c.setFillColor(GREEN_C)
    c.drawString(bx, by, "Guclu: ")
    c.setFont(font_name, 7.5)
    c.drawString(bx + 34, by, (", ".join(ogr.get("guclu_dersler", [])) or "-")[:42])
    c.setFont(font_bold, 7.5)
    c.setFillColor(RED_C)
    c.drawString(bx + half, by, "Zayif: ")
    c.setFont(font_name, 7.5)
    c.drawString(bx + half + 30, by, (", ".join(ogr.get("zayif_dersler", [])) or "-")[:42])

    # Bottom ornament
    bot_y = MB + 1.5 * cm
    for dx in range(9):
        _dm(ML + UW * 0.1 + dx * UW * 0.1, bot_y, 4.5)
    _gold_line(bot_y - 10, thick=3, thin=0.8, gap=4)
    c.setFont(font_name, 6.5)
    c.setFillColor(GRAY)
    c.drawCentredString(pw / 2, MB + 0.3 * cm,
                        f"Bu rapor SmartCampus AI tarafindan otomatik olarak olusturulmustur  \u25c6  {datetime.now().strftime('%d.%m.%Y %H:%M')}")

    # ════════════════════════════════════════
    #   SAYFA 2: STATS + PIE + BAR (COMPACT)
    # ════════════════════════════════════════
    _new_page()
    y = ph - MT - 20

    # ── STAT CARDS ──
    y = _section_header(y, "GENEL ISTATISTIKLER")
    y -= 2

    stat_items = [
        ("Toplam Sinav", str(gs.get("toplam", 0)), INDIGO),
        ("Ort. Net", f"{gs.get('ort_net', 0):.1f}", BLUE_C),
        ("Max Net", f"{gs.get('max_net', 0):.1f}", GREEN_C),
        ("Min Net", f"{gs.get('min_net', 0):.1f}", RED_C),
        ("Ort. Puan", f"{ort_puan:.1f}", GOLD),
        ("Son Sira", str(gs.get("son_siralama", "-")), PURPLE_C),
    ]
    card_w = (UW - 5 * 4) / 6
    for i, (label, val, color) in enumerate(stat_items):
        cx = ML + i * (card_w + 4)
        c.setFillColor(rl_colors.HexColor("#FAFBFF"))
        c.setStrokeColor(rl_colors.HexColor("#E0E7FF"))
        c.setLineWidth(0.5)
        c.roundRect(cx, y - 42, card_w, 42, 5, fill=1, stroke=1)
        c.setFillColor(color)
        c.rect(cx, y, card_w, 2, fill=1, stroke=0)
        c.setFont(font_bold, 13)
        c.setFillColor(color)
        c.drawCentredString(cx + card_w / 2, y - 20, val)
        c.setFont(font_name, 5.5)
        c.setFillColor(GRAY)
        c.drawCentredString(cx + card_w / 2, y - 34, label.upper())
    y -= 52

    # ── PIE: D/Y/B (left) + BAR: Net Trend (right) ──
    td = sum(d.get("dogru", 0) for d in denemeler)
    ty = sum(d.get("yanlis", 0) for d in denemeler)
    tb = sum(d.get("bos", 0) for d in denemeler)
    ta = td + ty + tb or 1

    half_w = UW / 2 - 4

    # Left: Pie
    y = _section_header(y, "CEVAP DAGILIMI")
    y -= 2
    drawing = Drawing(half_w, 150)
    pie = Pie()
    pie.x = half_w / 2 - 60
    pie.y = 5
    pie.width = 120
    pie.height = 120
    pie.data = [td, ty, tb]
    pie.labels = [f"Dogru: {td} (%{td * 100 // ta})", f"Yanlis: {ty} (%{ty * 100 // ta})", f"Bos: {tb} (%{tb * 100 // ta})"]
    pie.slices.strokeWidth = 1
    pie.slices.strokeColor = WHITE
    pie.slices[0].fillColor = GREEN_C
    pie.slices[1].fillColor = RED_C
    pie.slices[2].fillColor = rl_colors.HexColor("#94a3b8")
    pie.slices.fontName = font_name
    pie.slices.fontSize = 7
    pie.sideLabels = True
    pie.sideLabelsOffset = 0.08
    drawing.add(pie)
    renderPDF.draw(drawing, c, ML, y - 155)

    # Right side: D/Y/B progress bars + summary
    rx = ML + half_w + 12
    ry = y - 10
    c.setFont(font_bold, 8)
    c.setFillColor(NAVY)
    c.drawString(rx, ry, "DETAY OZET")
    _dm(rx + c.stringWidth("DETAY OZET", font_bold, 8) + 6, ry + 3, 2)
    ry -= 18

    for lbl, cnt, color in [("Dogru", td, GREEN_C), ("Yanlis", ty, RED_C), ("Bos", tb, rl_colors.HexColor("#94a3b8"))]:
        c.setFont(font_name, 7.5)
        c.setFillColor(DARK)
        c.drawString(rx, ry, f"{lbl}:")
        c.setFont(font_bold, 8)
        c.setFillColor(color)
        c.drawString(rx + 40, ry, str(cnt))
        c.setFont(font_name, 7)
        c.setFillColor(GRAY)
        c.drawString(rx + 65, ry, f"(%{cnt * 100 // ta})")
        _progress_rect(rx + 90, ry - 1, half_w - 100, 8, cnt * 100 / ta, color)
        ry -= 18

    # Dogru/Yanlis orani
    ry -= 8
    dy_oran = td / (td + ty) * 100 if (td + ty) > 0 else 0
    c.setFont(font_bold, 8)
    c.setFillColor(NAVY)
    c.drawString(rx, ry, "Basari Orani:")
    c.setFont(font_bold, 12)
    c.setFillColor(GREEN_C if dy_oran >= 70 else ORANGE_C if dy_oran >= 50 else RED_C)
    c.drawString(rx + 68, ry - 2, f"%{dy_oran:.1f}")
    ry -= 18

    # Net ortalaması bar
    c.setFont(font_name, 7.5)
    c.setFillColor(DARK)
    c.drawString(rx, ry, "Ort Net:")
    c.setFont(font_bold, 9)
    c.setFillColor(INDIGO)
    c.drawString(rx + 40, ry, f"{gs.get('ort_net', 0):.1f}")
    _progress_rect(rx + 75, ry - 1, half_w - 85, 8, gs.get("ort_net", 0) * 100 / 120, INDIGO)
    ry -= 18
    c.setFont(font_name, 7.5)
    c.setFillColor(DARK)
    c.drawString(rx, ry, "Ort Puan:")
    c.setFont(font_bold, 9)
    c.setFillColor(GOLD)
    c.drawString(rx + 46, ry, f"{ort_puan:.1f}")
    _progress_rect(rx + 80, ry - 1, half_w - 90, 8, ort_puan, GOLD)

    y -= 165

    # ── NET TREND BAR CHART ──
    sirali = sorted(denemeler, key=lambda x: x.get("tarih", ""))
    if len(sirali) >= 2:
        y = _section_header(y, "NET TREND GRAFIGI")
        y -= 2
        drawing2 = Drawing(UW, 140)
        bc = VerticalBarChart()
        bc.x = 40
        bc.y = 18
        bc.width = UW - 70
        bc.height = 105
        bc.data = [[d.get("net", 0) for d in sirali]]
        bc.categoryAxis.categoryNames = [
            f"{d.get('sinav_adi','')[:8]} ({d.get('tarih','')[-5:]})" for d in sirali
        ]
        bc.categoryAxis.labels.fontName = font_name
        bc.categoryAxis.labels.fontSize = 6
        bc.categoryAxis.labels.angle = 25
        bc.valueAxis.valueMin = 0
        bc.valueAxis.labels.fontName = font_name
        bc.valueAxis.labels.fontSize = 6
        bc.valueAxis.gridStrokeColor = rl_colors.HexColor("#e2e8f0")
        bc.valueAxis.gridStrokeWidth = 0.3
        bc.valueAxis.visibleGrid = True
        bc.bars[0].fillColor = INDIGO
        bc.bars[0].strokeColor = NAVY
        bc.bars[0].strokeWidth = 0.3
        bc.barWidth = max(8, min(30, int((UW - 90) / max(len(sirali), 1))))
        drawing2.add(bc)
        renderPDF.draw(drawing2, c, ML, y - 145)
        y -= 155

    # ── PUAN TREND (overlay) ──
    if len(sirali) >= 2:
        y = _section_header(y, "PUAN & SIRALAMA TREND")
        y -= 2
        drawing_p = Drawing(UW, 130)
        bc_p = VerticalBarChart()
        bc_p.x = 40
        bc_p.y = 18
        bc_p.width = UW - 70
        bc_p.height = 95
        bc_p.data = [
            [d.get("puan", 0) for d in sirali],
        ]
        bc_p.categoryAxis.categoryNames = [d.get("tarih", "")[-5:] for d in sirali]
        bc_p.categoryAxis.labels.fontName = font_name
        bc_p.categoryAxis.labels.fontSize = 6
        bc_p.valueAxis.valueMin = 0
        bc_p.valueAxis.labels.fontName = font_name
        bc_p.valueAxis.labels.fontSize = 6
        bc_p.valueAxis.gridStrokeColor = rl_colors.HexColor("#e2e8f0")
        bc_p.valueAxis.gridStrokeWidth = 0.3
        bc_p.valueAxis.visibleGrid = True
        bc_p.bars[0].fillColor = ROSE_C
        bc_p.bars[0].strokeColor = None
        bc_p.barWidth = max(8, min(30, int((UW - 90) / max(len(sirali), 1))))
        drawing_p.add(bc_p)
        renderPDF.draw(drawing_p, c, ML, y - 135)
        y -= 145

    # ════════════════════════════════════════
    #   SAYFA 3: DERS BAZLI ANALIZ
    # ════════════════════════════════════════
    if ders_ozet:
        _new_page()
        y = ph - MT - 20

        # ── DERS PIE ──
        y = _section_header(y, "DERS BAZLI NET DAGILIMI")
        y -= 2
        ders_list = list(ders_ozet.keys())
        ders_netler = [ders_ozet[d]["ort_net"] for d in ders_list]
        dc = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6",
              "#06b6d4", "#ec4899", "#3b82f6", "#f97316", "#14b8a6",
              "#a855f7", "#64748b", "#d946ef", "#0ea5e9", "#84cc16",
              "#e11d48", "#7c3aed", "#0d9488"]

        drawing3 = Drawing(half_w + 20, 150)
        pie2 = Pie()
        pie2.x = 10
        pie2.y = 5
        pie2.width = 130
        pie2.height = 130
        pie2.data = [max(0.1, n) for n in ders_netler]
        pie2.labels = [f"{d}: {n:.1f}" for d, n in zip(ders_list, ders_netler)]
        pie2.slices.strokeWidth = 1
        pie2.slices.strokeColor = WHITE
        for i in range(len(ders_list)):
            pie2.slices[i].fillColor = rl_colors.HexColor(dc[i % len(dc)])
        pie2.slices.fontName = font_name
        pie2.slices.fontSize = 7
        pie2.sideLabels = True
        pie2.sideLabelsOffset = 0.06
        drawing3.add(pie2)
        renderPDF.draw(drawing3, c, ML, y - 155)

        # Right: ders progress bars
        rx2 = ML + half_w + 20
        ry2 = y - 12
        max_net_all = max((info["ort_net"] for info in ders_ozet.values()), default=1) or 1
        c.setFont(font_bold, 8.5)
        c.setFillColor(NAVY)
        c.drawString(rx2, ry2, "DERS PERFORMANS BARLARI")
        _dm(rx2 + c.stringWidth("DERS PERFORMANS BARLARI", font_bold, 8.5) + 6, ry2 + 3, 2)
        ry2 -= 6
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.5)
        c.line(rx2, ry2, rx2 + half_w - 28, ry2)
        ry2 -= 14
        for di, (ders, info) in enumerate(sorted(ders_ozet.items(), key=lambda x: -x[1]["ort_net"])):
            d_color = rl_colors.HexColor(dc[di % len(dc)])
            c.setFont(font_bold, 7)
            c.setFillColor(DARK)
            c.drawString(rx2, ry2, ders[:14])
            c.setFont(font_bold, 8)
            c.setFillColor(d_color)
            c.drawRightString(rx2 + half_w - 30, ry2, f"{info['ort_net']:.1f}")
            _progress_rect(rx2, ry2 - 10, half_w - 30, 7, info["ort_net"] * 100 / max_net_all, d_color)
            ry2 -= 26
        y -= 160

        # ── DERS BAR CHART ──
        if len(ders_ozet) >= 2:
            y = _section_header(y, "DERS KARSILASTIRMA (ORT. NET vs MAX NET)")
            y -= 2
            dls = sorted(ders_ozet.items(), key=lambda x: -x[1]["ort_net"])
            drawing4 = Drawing(UW, 140)
            bc2 = VerticalBarChart()
            bc2.x = 40
            bc2.y = 18
            bc2.width = UW - 70
            bc2.height = 105
            bc2.data = [
                [info["ort_net"] for _, info in dls],
                [info["max_net"] for _, info in dls],
            ]
            bc2.categoryAxis.categoryNames = [d[:12] for d, _ in dls]
            bc2.categoryAxis.labels.fontName = font_name
            bc2.categoryAxis.labels.fontSize = 6.5
            bc2.categoryAxis.labels.angle = 25
            bc2.valueAxis.valueMin = 0
            bc2.valueAxis.labels.fontName = font_name
            bc2.valueAxis.labels.fontSize = 6
            bc2.valueAxis.gridStrokeColor = rl_colors.HexColor("#e2e8f0")
            bc2.valueAxis.gridStrokeWidth = 0.3
            bc2.valueAxis.visibleGrid = True
            bc2.bars[0].fillColor = INDIGO
            bc2.bars[0].strokeColor = None
            bc2.bars[1].fillColor = GREEN_C
            bc2.bars[1].strokeColor = None
            bc2.barWidth = max(6, min(20, int((UW - 100) / max(len(dls) * 2, 1))))
            drawing4.add(bc2)
            renderPDF.draw(drawing4, c, ML, y - 145)
            # Legend
            c.setFont(font_name, 6)
            c.setFillColor(INDIGO)
            c.rect(ML + UW - 100, y - 148, 8, 8, fill=1, stroke=0)
            c.setFillColor(DARK)
            c.drawString(ML + UW - 90, y - 147, "Ort Net")
            c.setFillColor(GREEN_C)
            c.rect(ML + UW - 55, y - 148, 8, 8, fill=1, stroke=0)
            c.setFillColor(DARK)
            c.drawString(ML + UW - 45, y - 147, "Max Net")
            y -= 160

        # ── DERS PERFORMANS TABLOSU ──
        y = _section_header(y, "DERS BAZLI PERFORMANS DETAY TABLOSU")
        y -= 2
        row_h = 15
        t_cols = [ML, ML + 3 * cm, ML + 4.4 * cm, ML + 5.8 * cm, ML + 7.2 * cm, ML + 8.8 * cm, ML + 10.4 * cm, ML + 12 * cm]
        t_labels = ["DERS", "SINAV", "ORT D", "ORT Y", "ORT NET", "MAX NET", "BASARI%", "DURUM"]
        c.setFillColor(NAVY)
        c.rect(ML, y - row_h, UW, row_h, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.8)
        c.line(ML, y, ML + UW, y)
        c.line(ML, y - row_h, ML + UW, y - row_h)
        c.setFont(font_bold, 6.5)
        c.setFillColor(GOLD)
        for ci, lbl in enumerate(t_labels):
            c.drawString(t_cols[ci] + 3, y - 11, lbl)
        y -= row_h

        for ri, (ders, info) in enumerate(sorted(ders_ozet.items(), key=lambda x: -x[1]["ort_net"])):
            bg = ZEBRA_GOLD if ri % 2 == 0 else WHITE
            c.setFillColor(bg)
            c.rect(ML, y - row_h, UW, row_h, fill=1, stroke=0)
            c.setStrokeColor(rl_colors.HexColor("#e2e8f0"))
            c.setLineWidth(0.2)
            c.line(ML, y - row_h, ML + UW, y - row_h)

            basari = info["ort_dogru"] / (info["ort_dogru"] + info["ort_yanlis"]) * 100 if (info["ort_dogru"] + info["ort_yanlis"]) > 0 else 0
            durum = "Mukemmel" if info["ort_net"] >= 15 else "Iyi" if info["ort_net"] >= 10 else "Gelistir" if info["ort_net"] >= 5 else "Kritik"
            d_c = GREEN_C if info["ort_net"] >= 15 else BLUE_C if info["ort_net"] >= 10 else ORANGE_C if info["ort_net"] >= 5 else RED_C

            c.setFont(font_bold, 7)
            c.setFillColor(DARK)
            c.drawString(ML + 3, y - 11, ders[:16])
            vals = [str(info["sinav_sayisi"]), f"{info['ort_dogru']:.1f}",
                    f"{info['ort_yanlis']:.1f}", f"{info['ort_net']:.1f}",
                    f"{info['max_net']:.1f}", f"%{basari:.0f}"]
            c.setFont(font_name, 7)
            for vi, v in enumerate(vals):
                c.setFillColor(DARK)
                c.drawCentredString((t_cols[vi + 1] + (t_cols[vi + 2] if vi + 2 < len(t_cols) else ML + UW)) / 2, y - 11, v)
            dw = c.stringWidth(durum, font_bold, 6) + 8
            c.setFillColor(d_c)
            c.roundRect(t_cols[7] + 3, y - 13, dw, 11, 3, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont(font_bold, 5.5)
            c.drawString(t_cols[7] + 7, y - 10, durum)
            y -= row_h
        c.setStrokeColor(GOLD)
        c.setLineWidth(1)
        c.line(ML, y, ML + UW, y)

    # ════════════════════════════════════════
    #   SAYFA 4: TUM SINAV TABLOSU
    # ════════════════════════════════════════
    _new_page()
    y = ph - MT - 20
    y = _section_header(y, "TUM SINAV SONUCLARI DETAY TABLOSU")
    y -= 2

    sc = [ML]
    sw = [0.6 * cm, 1.6 * cm, 3.8 * cm, 1.4 * cm, 0.9 * cm, 0.9 * cm, 0.9 * cm, 1.3 * cm, 1.3 * cm, 1 * cm, 1.5 * cm]
    for w in sw[:-1]:
        sc.append(sc[-1] + w)
    sl = ["#", "TARIH", "SINAV ADI", "TUR", "D", "Y", "B", "NET", "PUAN", "SIRA", "BAND"]
    row_h = 14

    def _draw_sinav_header(yy):
        c.setFillColor(NAVY)
        c.rect(ML, yy - row_h, UW, row_h, fill=1, stroke=0)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1)
        c.line(ML, yy, ML + UW, yy)
        c.line(ML, yy - row_h, ML + UW, yy - row_h)
        c.setFont(font_bold, 6)
        c.setFillColor(GOLD)
        for ci, lbl in enumerate(sl):
            c.drawString(sc[ci] + 2, yy - 10, lbl)
        return yy - row_h

    y = _draw_sinav_header(y)

    sirali_den = sorted(denemeler, key=lambda x: x.get("tarih", ""), reverse=True)
    for ri, d in enumerate(sirali_den):
        if y - row_h < MB + 12:
            _new_page()
            y = ph - MT - 20
            y = _section_header(y, "TUM SINAV SONUCLARI (DEVAM)")
            y -= 2
            y = _draw_sinav_header(y)

        bg = ZEBRA_GOLD if ri % 2 == 0 else WHITE
        c.setFillColor(bg)
        c.rect(ML, y - row_h, UW, row_h, fill=1, stroke=0)
        c.setStrokeColor(rl_colors.HexColor("#e2e8f0"))
        c.setLineWidth(0.2)
        c.line(ML, y - row_h, ML + UW, y - row_h)
        if ri % 5 == 0:
            c.setFillColor(GOLD)
            c.rect(ML, y - row_h, 2, row_h, fill=1, stroke=0)

        puan_v = d.get("puan", 0)
        bnd = get_renk_bandi(puan_v)
        net_v = d.get("net", 0)
        nc = GREEN_C if net_v >= 60 else BLUE_C if net_v >= 40 else ORANGE_C if net_v >= 20 else RED_C

        rv = [
            (str(ri + 1), font_name, 6, GRAY),
            (d.get("tarih", "")[:10], font_name, 6, DARK),
            (d.get("sinav_adi", "")[:24], font_bold, 6.5, DARK),
            (d.get("sinav_turu", "")[:10], font_name, 5.5, GRAY),
            (str(d.get("dogru", 0)), font_bold, 6.5, GREEN_C),
            (str(d.get("yanlis", 0)), font_bold, 6.5, RED_C),
            (str(d.get("bos", 0)), font_name, 6.5, GRAY),
            (f"{net_v:.1f}", font_bold, 7.5, nc),
            (f"{puan_v:.1f}", font_bold, 6.5, NAVY),
            (str(d.get("siralama", "-")), font_name, 6.5, DARK),
        ]
        for ci, (txt, fn, fs, fc) in enumerate(rv):
            c.setFont(fn, fs)
            c.setFillColor(fc)
            c.drawString(sc[ci] + 2, y - 10, txt)

        bl = bnd["label"]
        bc_c = rl_colors.HexColor(bnd["color"])
        bw_t = c.stringWidth(bl, font_bold, 5.5) + 7
        c.setFillColor(bc_c)
        c.roundRect(sc[10] + 1, y - 12, bw_t, 10, 3, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(font_bold, 5)
        c.drawString(sc[10] + 4, y - 9.5, bl)
        y -= row_h

    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(ML, y, ML + UW, y)

    # Band distribution
    y -= 16
    c.setFont(font_bold, 7.5)
    c.setFillColor(NAVY)
    c.drawString(ML, y, "RENK BANDI DAGILIMI:")
    _dm(ML + c.stringWidth("RENK BANDI DAGILIMI:", font_bold, 7.5) + 6, y + 3, 2)
    y -= 12
    bc_map = {}
    for d in denemeler:
        b = get_renk_bandi(d.get("puan", 0))
        bc_map[b["label"]] = bc_map.get(b["label"], 0) + 1
    bx_c = ML
    for lbl, cnt in sorted(bc_map.items(), key=lambda x: -x[1]):
        b_i = None
        for bn in RENK_BANDI.values():
            if bn["label"] == lbl:
                b_i = bn
                break
        if not b_i:
            continue
        txt = f"{lbl}: {cnt}"
        tw = c.stringWidth(txt, font_bold, 7) + 12
        c.setFillColor(rl_colors.HexColor(b_i["color"]))
        c.roundRect(bx_c, y - 1, tw, 12, 3, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(font_bold, 6.5)
        c.drawString(bx_c + 6, y + 1, txt)
        bx_c += tw + 6

    # ════════════════════════════════════════
    #   SAYFA 5+: AI DEGERLENDIRME
    # ════════════════════════════════════════
    if ai_yorum:
        _new_page()
        y = ph - MT - 20
        y = _section_header(y, "AI DESTEKLI KAPSAMLI DEGERLENDIRME")
        y -= 6

        intro_h = 26
        c.setFillColor(rl_colors.HexColor("#F0EDFF"))
        c.setStrokeColor(INDIGO)
        c.setLineWidth(0.8)
        c.roundRect(ML, y - intro_h, UW, intro_h, 5, fill=1, stroke=1)
        c.setFont(font_bold, 7.5)
        c.setFillColor(INDIGO)
        c.drawString(ML + 8, y - 10, "Bu analiz SmartCampus AI tarafindan GPT-4o-mini modeli ile olusturulmustur.")
        c.setFont(font_name, 6.5)
        c.setFillColor(GRAY)
        c.drawString(ML + 8, y - 21, "Veriye dayali, kisisellestirilmis, uygulanabilir onerilere sahip profesyonel degerlendirme raporu.")
        y -= intro_h + 8

        for raw_line in ai_yorum.split("\n"):
            line = raw_line.strip()
            if y < MB + 28:
                _new_page()
                y = ph - MT - 20
                y = _section_header(y, "AI DEGERLENDIRME (DEVAM)")
                y -= 6

            if not line:
                y -= 4
                continue
            if line.startswith("##"):
                title = line.replace("##", "").strip()
                y -= 6
                c.setFillColor(INDIGO)
                c.rect(ML, y - 15, UW, 17, fill=1, stroke=0)
                c.setStrokeColor(GOLD)
                c.setLineWidth(0.6)
                c.line(ML, y + 2, ML + UW * 0.18, y + 2)
                c.line(ML + UW * 0.82, y + 2, ML + UW, y + 2)
                c.setFillColor(WHITE)
                c.setFont(font_bold, 8.5)
                c.drawString(ML + 8, y - 11, title.upper())
                _dm(ML + UW - 10, y - 6, 2)
                y -= 22
            elif line.startswith("**") and line.endswith("**"):
                c.setFont(font_bold, 8)
                c.setFillColor(NAVY)
                c.drawString(ML + 4, y, line.strip("* "))
                y -= 12
            elif line.startswith("- ") or line.startswith("* "):
                bullet = line[2:].strip()
                lines = _wrap(bullet, font_name, 8, UW - 18)
                _dm(ML + 5, y + 2.5, 1.8)
                for ln in lines:
                    if y < MB + 20:
                        _new_page()
                        y = ph - MT - 20
                        y = _section_header(y, "AI DEGERLENDIRME (DEVAM)")
                        y -= 6
                    c.setFont(font_name, 8)
                    c.setFillColor(DARK)
                    c.drawString(ML + 14, y, ln)
                    y -= 11.5
            else:
                lines = _wrap(line, font_name, 8, UW - 6)
                for ln in lines:
                    if y < MB + 20:
                        _new_page()
                        y = ph - MT - 20
                        y = _section_header(y, "AI DEGERLENDIRME (DEVAM)")
                        y -= 6
                    c.setFont(font_name, 8)
                    c.setFillColor(DARK)
                    c.drawString(ML + 4, y, ln)
                    y -= 11.5

    # ════════════════════════════════════════
    #         KAPANIŞ
    # ════════════════════════════════════════
    if y > MB + 3.5 * cm:
        y -= 1 * cm
    else:
        _new_page()
        y = ph - MT - 22

    _gold_line(y, thick=2, thin=0.5)
    y -= 1 * cm
    c.setFont(font_bold, 10)
    c.setFillColor(NAVY)
    c.drawCentredString(pw / 2, y, "Bu rapor SmartCampus AI Egitim Koclugu modulu tarafindan")
    y -= 14
    c.drawCentredString(pw / 2, y, "otomatik olarak olusturulmustur.")
    y -= 18
    c.setFont(font_name, 8)
    c.setFillColor(GOLD)
    c.drawCentredString(pw / 2, y, "\u25c6  \u25c6  \u25c6  \u25c6  \u25c6")
    y -= 14
    c.setFont(font_name, 7.5)
    c.setFillColor(GRAY)
    c.drawCentredString(pw / 2, y, f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}  |  Ogrenci: {ogr.get('ad','')} {ogr.get('soyad','')}")

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def _ai_olcme_son_durum(client, ogr: dict, denemeler: list,
                         ders_ozet: dict, genel_stats: dict,
                         motivasyonlar: list, hedefler: list) -> str | None:
    """AI ile kapsamli olcme son durum degerlendirmesi."""
    ogr_bilgi = (f"Ogrenci: {ogr.get('ad','')} {ogr.get('soyad','')}, "
                 f"Sinif: {ogr.get('sinif','')}/{ogr.get('sube','')}, "
                 f"Hedef Sinav: {ogr.get('hedef_sinav','Belirtilmemis')}, "
                 f"Hedef Puan: {ogr.get('hedef_puan','Belirtilmemis')}, "
                 f"Guclu: {', '.join(ogr.get('guclu_dersler',[])) or 'Yok'}, "
                 f"Zayif: {', '.join(ogr.get('zayif_dersler',[])) or 'Yok'}")

    deneme_bilgi = f"Toplam {genel_stats.get('toplam',0)} sinav. "
    deneme_bilgi += f"Ort Net: {genel_stats.get('ort_net',0):.1f}, "
    deneme_bilgi += f"Max Net: {genel_stats.get('max_net',0):.1f}, "
    deneme_bilgi += f"Min Net: {genel_stats.get('min_net',0):.1f}\n"

    sirali = sorted(denemeler, key=lambda x: x.get("tarih", ""), reverse=True)
    for d in sirali[:8]:
        deneme_bilgi += (f"\n- {d.get('tarih','')}: {d.get('sinav_adi','')} "
                         f"D:{d.get('dogru',0)} Y:{d.get('yanlis',0)} B:{d.get('bos',0)} "
                         f"Net:{d.get('net',0)} Puan:{d.get('puan',0)}")
        for dd in d.get("ders_detaylari", []):
            deneme_bilgi += f" [{dd.get('ders','')}: D{dd.get('dogru',0)}/Y{dd.get('yanlis',0)}/Net{dd.get('net',0)}]"

    ders_bilgi = ""
    for ders, info in sorted(ders_ozet.items(), key=lambda x: -x[1]["ort_net"]):
        ders_bilgi += (f"\n- {ders}: {info['sinav_sayisi']} sinav, "
                       f"Ort Net: {info['ort_net']:.1f}, Max: {info['max_net']:.1f}")

    motiv_bilgi = "Motivasyon kaydi yok"
    if motivasyonlar:
        son_m = sorted(motivasyonlar, key=lambda x: x.get("tarih", ""), reverse=True)[:3]
        motiv_bilgi = ""
        for m in son_m:
            motiv_bilgi += (f"\n- {m.get('tarih','')}: Mot:{m.get('motivasyon_puani',3)} "
                            f"Ozg:{m.get('ozguven_puani',3)} Str:{m.get('stres_puani',3)} "
                            f"Enr:{m.get('enerji_puani',3)} Odk:{m.get('odaklanma_puani',3)}")

    hedef_bilgi = ""
    for h in hedefler[:5]:
        hedef_bilgi += f"\n- {h.get('baslik','')}: %{h.get('ilerleme_yuzdesi',0)} ({h.get('durum','')})"

    prompt = f"""Sen cok deneyimli bir egitim kocu ve olcme degerlendirme uzmanisin.
Asagidaki verileri analiz ederek KAPSAMLI ve PROFESYONEL bir olcme son durum raporu olustur.

=== OGRENCI ===
{ogr_bilgi}

=== SINAV SONUCLARI ===
{deneme_bilgi}

=== DERS BAZLI PERFORMANS ===
{ders_bilgi}

=== MOTIVASYON DURUMU ===
{motiv_bilgi}

=== HEDEFLER ===
{hedef_bilgi}

Asagidaki basliklarda detayli analiz yap (Turkce, somut, uygulanabilir):

## GENEL PERFORMANS DEGERLENDIRMESI
(3-5 cumle genel bakis, trend analizi, guclu/zayif noktalar)

## DERS BAZLI ANALIZ
(Her ders icin 1-2 cumle: performans durumu, trend, oneri)

## NET TREND ANALIZI
(Yukselen/dusen trend, son sinavlardaki degisim, sebep analizi)

## GUCLU YONLER
(En az 3 somut guclu yon)

## GELISTIRILMESI GEREKEN ALANLAR
(En az 3 somut gelistirme alani + kisa strateji)

## HEDEF UYUMLULUK ANALIZI
(Mevcut performans vs hedefler, yetisir mi, ne yapmali)

## HAFTALIK EYLEM PLANI
(7 gunluk somut plan onerisi: kac soru, hangi ders, kac saat)

## MOTIVASYON VE PSİKOLOJIK DESTEK
(Motivasyon durumu analizi, onerilir yaklasim)

## VELI ICIN OZET
(Veliye iletilebilecek 3-5 cumlelik kisa ozet)
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": __import__('utils.ai_rules', fromlist=['inject_rules']).inject_rules(
                    "Sen Turkiye'nin en basarili egitim kocu ve olcme degerlendirme uzmanisin. Detayli, profesyonel ve uygulanabilir analizler yapiyorsun.")},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=3000,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"AI analiz olusturulamadi: {str(e)}"


def _render_yd_degerlendirme_ek(store: EKDataStore):
    """Yabanci Dil Degerlendirmesi — Kocluk perspektifinden Quiz + CEFR analizi."""
    styled_section("Ogrenci Yabanci Dil Degerlendirmesi", "#4338ca")

    ogrenciler = store.load_list("ogrenciler")
    if not ogrenciler:
        styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
        return

    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')} ({o.get('sinif','')}/{o.get('sube','')})": o
                for o in ogrenciler}
    sel_label = st.selectbox("Ogrenci:", list(ogr_opts.keys()), key="ek_yd_ogr_sel")
    if not sel_label:
        return
    ogr = ogr_opts[sel_label]
    ogr_id = ogr.get("ogrenci_id", ogr.get("id", ""))
    sinif_int = int(ogr.get("sinif", 0) or 0)

    # Veri yukle
    yd_results = []
    try:
        from models.yd_assessment import YdAssessmentStore
        yd_store = YdAssessmentStore()
        yd_results = yd_store.get_results(student_id=ogr_id)
    except Exception:
        pass

    cefr_placement = []
    try:
        from models.cefr_exam import CEFRPlacementStore, GRADE_TO_CEFR, CEFR_ORDER, CEFR_LEVELS
        _cp = CEFRPlacementStore()
        cefr_placement = _cp.get_student_results(ogr_id)
    except Exception:
        pass

    cefr_mock = []
    try:
        from models.cefr_exam import CEFRExamStore
        _ce = CEFRExamStore()
        cefr_mock = _ce.get_student_results(ogr_id, grade=sinif_int)
    except Exception:
        pass

    if not yd_results and not cefr_placement and not cefr_mock:
        styled_info_banner("Bu ogrenci icin yabanci dil verisi bulunamadi.", "info", "🌍")
        return

    # Ozet kartlari
    yd_puanlar = [float(getattr(d, "score", 0)) for d in yd_results if getattr(d, "score", 0) and float(getattr(d, "score", 0)) > 0]
    quiz_results = [d for d in yd_results if getattr(d, "exam_category", "") == "quiz"]
    quiz_puanlar = [float(getattr(d, "score", 0)) for d in quiz_results if getattr(d, "score", 0) and float(getattr(d, "score", 0)) > 0]
    quiz_avg = sum(quiz_puanlar) / len(quiz_puanlar) if quiz_puanlar else 0

    target_cefr = GRADE_TO_CEFR.get(sinif_int, "A2") if sinif_int else "—"
    placed = cefr_placement[-1].placed_cefr if cefr_placement else "—"
    mock_level = cefr_mock[-1].achieved_cefr if cefr_mock else "—"

    # Stat row
    st.markdown(
        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0;">'
        + "".join(
            f'<div style="flex:1;min-width:100px;background:linear-gradient(135deg,#0f172a,#1e293b);'
            f'border-radius:10px;padding:10px;text-align:center;border:1px solid {c}30;">'
            f'<div style="font-size:.7rem;color:#94a3b8;">{l}</div>'
            f'<div style="font-size:1.1rem;font-weight:800;color:{c};">{v}</div></div>'
            for l, v, c in [
                ("Quiz Ort.", f"{quiz_avg:.0f}" if quiz_puanlar else "—", "#d97706"),
                ("Quiz Sayisi", str(len(quiz_results)), "#7c3aed"),
                ("CEFR Tespit", placed, "#8b5cf6"),
                ("Mock Exam", mock_level, "#6d28d9"),
                ("Hedef", target_cefr, "#059669"),
                ("Toplam Sinav", str(len(yd_results)), "#2563eb"),
            ]
        )
        + '</div>',
        unsafe_allow_html=True,
    )

    # Beceri analizi
    agg_skills: dict[str, dict] = {}
    for d in yd_results:
        sb = getattr(d, "skill_breakdown", {}) or {}
        for sk, data in sb.items():
            if sk not in agg_skills:
                agg_skills[sk] = {"correct": 0, "total": 0}
            if isinstance(data, dict):
                agg_skills[sk]["correct"] += data.get("correct", 0)
                agg_skills[sk]["total"] += data.get("total", 0)

    if agg_skills:
        st.markdown("**Beceri Analizi:**")
        sk_labels = {"vocabulary": "Kelime", "grammar": "Dilbilgisi", "reading": "Okuma",
                     "listening": "Dinleme", "other": "Diger"}
        for sk, data in agg_skills.items():
            pct = (data["correct"] / data["total"] * 100) if data["total"] else 0
            clr = "#22c55e" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;padding:3px 0;">'
                f'<span style="min-width:70px;font-size:.82rem;color:#cbd5e1;">{sk_labels.get(sk, sk)}</span>'
                f'<div style="flex:1;background:rgba(99,102,241,.08);border-radius:4px;height:14px;overflow:hidden;">'
                f'<div style="width:{pct}%;height:100%;background:{clr};border-radius:4px;"></div></div>'
                f'<span style="color:{clr};font-weight:700;font-size:.82rem;">%{pct:.0f}</span></div>',
                unsafe_allow_html=True,
            )

    # Kocluk tavsiyeleri
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:10px;'
        'padding:12px 16px;border:1px solid rgba(139,92,246,.2);">'
        '<h5 style="margin:0 0 8px;color:#a78bfa;">🧠 Koçluk Tavsiyeleri</h5>',
        unsafe_allow_html=True,
    )
    tvs = []
    if quiz_avg > 0 and quiz_avg < 50:
        tvs.append("📚 Quiz ortalaması düşük — haftalık ünite tekrar programı oluşturun")
        tvs.append("🔄 SRS (Aralıklı Tekrar) kelime çalışmasını günlük rutine ekleyin")
    elif quiz_avg > 0 and quiz_avg < 70:
        tvs.append("📝 Quiz performansı geliştirilmeli — zayıf ünitelere odaklanın")

    if placed != "—" and target_cefr != "—":
        try:
            if CEFR_ORDER.index(placed) < CEFR_ORDER.index(target_cefr):
                tvs.append(f"🌐 CEFR seviyesi ({placed}) hedefin ({target_cefr}) altında — yoğunlaştırılmış dil programı")
        except Exception:
            pass

    weak = [sk for sk, d in agg_skills.items() if d["total"] > 0 and (d["correct"] / d["total"] * 100) < 50]
    if weak:
        sk_labels2 = {"vocabulary": "kelime", "grammar": "dilbilgisi", "reading": "okuma", "listening": "dinleme"}
        tvs.append(f"🎯 Zayıf alanlar: {', '.join(sk_labels2.get(s, s) for s in weak)} — bireysel çalışma planı")

    if not cefr_mock:
        tvs.append("🏆 Cambridge formatında Mock Exam uygulatarak gerçek sınav deneyimi kazandırın")
    if not cefr_placement:
        tvs.append("📋 CEFR Seviye Tespiti yapılmalı — doğru seviyede içerik sunulabilmesi için")

    if not tvs:
        tvs.append("✅ Yabancı dil performansı iyi — mevcut seviyeyi koruyucu aktiviteler sürdürülmeli")

    for t in tvs:
        st.markdown(f'<div style="padding:3px 0;font-size:.85rem;color:#e2e8f0;">{t}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Aile Bilgi Formu — Koçluk Perspektifi ──
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_EK
        _abf_list = _CML_EK.load_aile_bilgi_formlari()
        _ogr_abf = [f for f in _abf_list if f.get("ogrenci_id") == ogr_id]
        if _ogr_abf:
            st.markdown("---")
            st.markdown(
                '<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:10px;'
                'padding:12px 16px;border:1px solid rgba(13,148,136,.2);">'
                '<h5 style="margin:0 0 8px;color:#2dd4bf;">📋 Aile Bilgi Formu — Koçluk Değerlendirmesi</h5>',
                unsafe_allow_html=True,
            )
            abf = _ogr_abf[-1]
            _risk_flags = []
            if abf.get("anne_birlikte_bosanmis") in ("Boşanmış", "Ayrı") or abf.get("baba_birlikte_bosanmis") in ("Boşanmış", "Ayrı"):
                _risk_flags.append(("⚠️ Aile boşanmış/ayrı", "#f59e0b", "Duygusal destek + stabil rutin oluşturma"))
            if abf.get("anne_sag_olu") == "Ölü" or abf.get("baba_sag_olu") == "Ölü":
                _risk_flags.append(("💔 Ebeveyn kaybı", "#ef4444", "Yas süreci takibi + rehberlik yönlendirme"))
            if abf.get("etkisindeki_olay"):
                _risk_flags.append((f"⚠️ Travma: {abf['etkisindeki_olay']}", "#ef4444", "Psikososyal destek planı"))
            if abf.get("bagimllik_durumu"):
                _risk_flags.append((f"🚫 Ailede bağımlılık: {abf['bagimllik_durumu']}", "#f97316", "Koruyucu faktörler güçlendirme"))
            if abf.get("kiminle_nerede_yasiyor") not in ("Aile", "", None):
                _risk_flags.append((f"🏠 Aile dışı yaşam: {abf['kiminle_nerede_yasiyor']}", "#f59e0b", "Aidiyet duygusu güçlendirme"))
            if abf.get("ders_calisma_alani") == "Hayır":
                _risk_flags.append(("📚 Evde çalışma alanı yok", "#3b82f6", "Okul etüt programına yönlendirme"))
            if abf.get("okula_tutum") and any(k in str(abf["okula_tutum"]).lower() for k in ("olumsuz", "ilgisiz", "isteksiz")):
                _risk_flags.append(("📖 Okula karşı olumsuz tutum", "#f97316", "Motivasyon artırıcı etkinlikler"))

            if _risk_flags:
                for flag, clr, oneri in _risk_flags:
                    st.markdown(
                        f'<div style="background:{clr}08;border-left:3px solid {clr};'
                        f'border-radius:0 6px 6px 0;padding:6px 12px;margin:3px 0;">'
                        f'<span style="font-weight:700;color:{clr};font-size:.82rem;">{flag}</span>'
                        f'<span style="color:#94a3b8;font-size:.75rem;margin-left:8px;">→ {oneri}</span></div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown('<div style="color:#22c55e;font-size:.85rem;">✅ Kritik aile risk faktörü tespit edilmedi</div>', unsafe_allow_html=True)

            # Sosyo-ekonomik özet
            _se_items = []
            if abf.get("ortalama_gelir"): _se_items.append(f"Gelir: {abf['ortalama_gelir']}")
            if abf.get("ev_sahipligi"): _se_items.append(f"Ev: {abf['ev_sahipligi']}")
            if abf.get("kurum_yardimi"): _se_items.append(f"Yardım: {abf['kurum_yardimi']}")
            if _se_items:
                st.markdown(f'<div style="color:#94a3b8;font-size:.78rem;margin-top:4px;">Sosyo-ekonomik: {" | ".join(_se_items)}</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        pass

    # ── MEB Dijital Formlar — Koçluk Perspektifi ──
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_MEB_EK
        _meb_all = _CML_MEB_EK.load_all_meb_forms()
        # Öğrenci bazlı formları filtrele
        _ogr_meb: dict[str, list] = {}
        for sk, forms in _meb_all.items():
            for f in forms:
                if f.get("ogrenci_id") == ogr_id:
                    _ogr_meb.setdefault(sk, []).append(f)
        if _ogr_meb:
            st.markdown("---")
            st.markdown(
                '<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:10px;'
                'padding:12px 16px;border:1px solid rgba(59,130,246,.2);">'
                '<h5 style="margin:0 0 8px;color:#60a5fa;">📄 MEB Dijital Formlar — Koçluk Değerlendirmesi</h5>',
                unsafe_allow_html=True,
            )
            from models.meb_formlar import MEB_FORM_SCHEMAS
            _meb_flags = []
            for sk, forms in _ogr_meb.items():
                # Şema adını bul
                schema = next((s for s in MEB_FORM_SCHEMAS.values() if s["store_key"] == sk), None)
                form_title = schema["title"] if schema else sk
                form_icon = schema.get("icon", "📄") if schema else "📄"
                st.markdown(f'<div style="color:#94a3b8;font-size:.78rem;margin:3px 0;">'
                            f'{form_icon} <b>{form_title}</b>: {len(forms)} kayıt</div>', unsafe_allow_html=True)
                # Koçluk perspektifli risk tespiti
                for f in forms:
                    if sk == "dehb_gozlem_formlari" and "yönlendirme" in str(f.get("yonlendirme_onerisi", "")).lower():
                        _meb_flags.append(("🧠 DEHB şüphesi — yönlendirme önerilmiş", "#ef4444",
                                           "Bireysel çalışma planı + kısa aralıklı görev verme + hareket molası"))
                    if sk == "ozel_ogrenme_guclugu_formlari" and "yönlendirme" in str(f.get("yonlendirme_onerisi", "")).lower():
                        _meb_flags.append(("📖 ÖÖG şüphesi — yönlendirme önerilmiş", "#ef4444",
                                           "Çok duyusal öğretim + fazladan süre + görsel destek materyalleri"))
                    if sk == "disiplin_gorusme_formlari":
                        _meb_flags.append(("⚖️ Disiplin olayı kaydı", "#f59e0b",
                                           "Öfke yönetimi + problem çözme becerileri + mentorluk"))
                    if sk == "psikolojik_yonlendirme_formlari":
                        sev = f.get("belirti_siddeti", "")
                        if sev in ("Şiddetli", "Çok Şiddetli / Acil"):
                            _meb_flags.append(("🚨 Psikolojik destek — ACİL", "#ef4444",
                                               "Acil uzman yönlendirme + günlük check-in + güvenli alan sağlama"))
                        else:
                            _meb_flags.append(("🧭 Psikolojik destek yönlendirmesi", "#f59e0b",
                                               "Düzenli görüşme + sosyal destek ağı güçlendirme"))
                    if sk == "ev_ziyareti_formlari" and "acil" in str(f.get("takip_gerekliligi", "")).lower():
                        _meb_flags.append(("🏡 Ev ziyareti — acil takip", "#ef4444",
                                           "Sosyal destek + okul kaynaklarına yönlendirme + veli işbirliği"))
            if _meb_flags:
                st.markdown('<div style="margin-top:6px;">', unsafe_allow_html=True)
                for flag, clr, tavsiye in _meb_flags:
                    st.markdown(f'<div style="background:{clr}08;border-left:3px solid {clr};'
                                f'padding:6px 10px;border-radius:0 6px 6px 0;margin:3px 0;">'
                                f'<span style="color:{clr};font-weight:700;font-size:.82rem;">{flag}</span>'
                                f'<div style="color:#94a3b8;font-size:.75rem;">Koçluk: {tavsiye}</div></div>',
                                unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        pass

    # ── AI MEB Form Değerlendirme — Koçluk ──
    try:
        from views.meb_formlar import render_ai_ogrenci_panel
        render_ai_ogrenci_panel(None, ogr_id, "")
    except Exception:
        pass

    # ── Rehberlik Test & Envanter — Koçluk Perspektifi ──
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_RT3
        _rt_otr = _CML_RT3.load_rehberlik_test_oturumlari()
        _rt_cvp = _CML_RT3.load_rehberlik_test_cevaplari()
        _rt_tst = _CML_RT3.load_rehberlik_testler()
        _ogr_otr = [o for o in _rt_otr if o.get("ogrenci_id") == ogr_id]
        if _ogr_otr:
            st.markdown("---")
            st.markdown(
                '<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:10px;'
                'padding:12px 16px;border:1px solid rgba(139,92,246,.2);">'
                '<h5 style="margin:0 0 8px;color:#a78bfa;">📝 Rehberlik Test Sonuçları</h5>',
                unsafe_allow_html=True,
            )
            _tst_map = {t.get("id", ""): t for t in _rt_tst}
            for o in _ogr_otr:
                test = _tst_map.get(o.get("test_id", ""), {})
                durum = o.get("durum", "-")
                d_clr = "#22c55e" if durum == "TAMAMLANDI" else "#f59e0b"
                # Ortalama puan
                _c = [c for c in _rt_cvp if c.get("oturum_id") == o.get("id")]
                _p = [float(c.get("puan", 0)) for c in _c if c.get("puan")]
                _avg = sum(_p) / len(_p) if _p else 0
                _p_text = f" — Ort: {_avg:.1f}" if _p else ""
                st.markdown(
                    f'<div style="background:{d_clr}08;border-left:3px solid {d_clr};'
                    f'padding:6px 10px;border-radius:0 6px 6px 0;margin:3px 0;">'
                    f'<span style="color:{d_clr};font-weight:700;font-size:.82rem;">'
                    f'{test.get("test_adi", "-")} ({durum}){_p_text}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception:
        pass


def _render_olcme_son_durum(store: EKDataStore):
    """Kapsamli AI destekli ogrenci olcme son durum ekrani."""
    styled_section("Ogrenci Olcme Son Durum", "#4f46e5")

    ogrenciler = store.load_list("ogrenciler")
    if not ogrenciler:
        styled_info_banner("Oncelikle ogrenci ekleyin.", "warning", "👥")
        return

    ogr_opts = {f"{o.get('ad','')} {o.get('soyad','')} ({o.get('sinif','')}/{o.get('sube','')})": o
                for o in ogrenciler}

    fc1, fc2 = st.columns([3, 1])
    with fc1:
        sec_ogr = st.selectbox("Ogrenci Sec", list(ogr_opts.keys()), key="ek_osd_ogr")
    ogr = ogr_opts.get(sec_ogr)
    if not ogr:
        return

    ogr_id = ogr["id"]

    # Tum verileri yukle
    denemeler = _load_consolidated_deneme(store, ogr_id)
    denemeler = sorted(denemeler, key=lambda x: x.get("tarih", ""), reverse=True)
    motivasyonlar = store.get_by_ogrenci("motivasyon", ogr_id)
    hedefler = store.get_by_ogrenci("hedefler", ogr_id)
    gorusmeler = store.get_by_ogrenci("gorusmeler", ogr_id)
    planlar = store.get_by_ogrenci("haftalik_planlar", ogr_id)

    if not denemeler:
        styled_info_banner(f"{sec_ogr} icin henuz deneme sonucu kaydi bulunmuyor. Once 'Deneme Analizi' sekmesinden sinav kaydi ekleyin.", "info", "📊")
        return

    # ── GENEL ISTATISTIKLER HESAPLA ──
    toplam = len(denemeler)
    ort_net = sum(d.get("net", 0) for d in denemeler) / toplam
    max_net = max(d.get("net", 0) for d in denemeler)
    min_net = min(d.get("net", 0) for d in denemeler)
    ort_puan = sum(d.get("puan", 0) for d in denemeler) / toplam
    son_siralama = denemeler[0].get("siralama", 0) if denemeler else 0
    toplam_dogru = sum(d.get("dogru", 0) for d in denemeler)
    toplam_yanlis = sum(d.get("yanlis", 0) for d in denemeler)
    toplam_bos = sum(d.get("bos", 0) for d in denemeler)
    toplam_all = toplam_dogru + toplam_yanlis + toplam_bos or 1

    genel_stats = {
        "toplam": toplam, "ort_net": ort_net, "max_net": max_net,
        "min_net": min_net, "ort_puan": ort_puan, "son_siralama": son_siralama,
    }

    # Ders bazli ozet
    ders_ozet = {}
    for d in denemeler:
        for dd in d.get("ders_detaylari", []):
            ders = dd.get("ders", "")
            if not ders:
                continue
            if ders not in ders_ozet:
                ders_ozet[ders] = {"dogru_toplam": 0, "yanlis_toplam": 0, "net_toplam": 0,
                                    "max_net": 0, "sinav_sayisi": 0}
            info = ders_ozet[ders]
            info["dogru_toplam"] += dd.get("dogru", 0)
            info["yanlis_toplam"] += dd.get("yanlis", 0)
            info["net_toplam"] += dd.get("net", 0)
            info["max_net"] = max(info["max_net"], dd.get("net", 0))
            info["sinav_sayisi"] += 1
    for ders, info in ders_ozet.items():
        s = info["sinav_sayisi"] or 1
        info["ort_dogru"] = info["dogru_toplam"] / s
        info["ort_yanlis"] = info["yanlis_toplam"] / s
        info["ort_net"] = info["net_toplam"] / s

    # ── PROFIL KARTI ──
    band = get_renk_bandi(ort_puan)
    st.markdown(f'''
    <div class="ek-glass" style="border-left:5px solid {band["color"]}">
        <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap">
            <div style="width:70px;height:70px;border-radius:50%;
                background:linear-gradient(135deg,#4f46e5,#7c3aed);
                display:flex;align-items:center;justify-content:center;
                font-size:1.8rem;color:white;font-weight:800;flex-shrink:0">
                {ogr.get("ad","X")[0]}{ogr.get("soyad","X")[0]}
            </div>
            <div style="flex:1">
                <div style="font-size:1.3rem;font-weight:800;color:#94A3B8">
                    {ogr.get("ad","")} {ogr.get("soyad","")}
                    <span style="font-size:0.8rem;color:#64748b;font-weight:500;margin-left:12px">
                        {ogr.get("sinif","")}/{ogr.get("sube","")}
                    </span>
                </div>
                <div style="font-size:0.85rem;color:#64748b;margin-top:4px">
                    Koc: {ogr.get("koc_adi","Atanmadi")} &nbsp;|&nbsp;
                    Hedef: {ogr.get("hedef_sinav","-")} &nbsp;|&nbsp;
                    Hedef Puan: {ogr.get("hedef_puan","-")}
                </div>
            </div>
            <div style="text-align:center;padding:8px 20px;border-radius:16px;
                background:{band["bg"]};border:2px solid {band["color"]}">
                <div style="font-size:1.8rem;font-weight:800;color:{band["color"]}">{ort_puan:.1f}</div>
                <div style="font-size:0.72rem;color:{band["color"]};font-weight:700">{band["label"]}</div>
            </div>
        </div>
    </div>''', unsafe_allow_html=True)

    # ── DIAMOND STATS ──
    _diamond_stats([
        ("📝", str(toplam), "Toplam Sinav", "#6366f1"),
        ("📊", f"{ort_net:.1f}", "Ortalama Net", "#3b82f6"),
        ("🔝", f"{max_net:.1f}", "En Yuksek Net", "#10b981"),
        ("📉", f"{min_net:.1f}", "En Dusuk Net", "#ef4444"),
        ("🏆", f"{ort_puan:.1f}", "Ort. Puan", "#f59e0b"),
        ("🏅", str(son_siralama or "-"), "Son Siralama", "#8b5cf6"),
    ])

    st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)

    # ── GRAFIKLER ──
    import pandas as pd

    g1, g2 = st.columns(2)

    with g1:
        styled_section("Cevap Dagilimi (Pasta Grafik)", "#10b981")
        pie_df = pd.DataFrame({
            "Kategori": ["Dogru", "Yanlis", "Bos"],
            "Adet": [toplam_dogru, toplam_yanlis, toplam_bos],
        })
        import plotly.express as px
        fig_pie = px.pie(
            pie_df, names="Kategori", values="Adet",
            color="Kategori",
            color_discrete_map={"Dogru": "#10b981", "Yanlis": "#ef4444", "Bos": "#94a3b8"},
            hole=0.4,
        )
        fig_pie.update_traces(
            textposition="inside", textinfo="percent+label+value",
            textfont_size=12,
            marker=dict(line=dict(color="white", width=2)),
        )
        fig_pie.update_layout(
            height=350, showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, x=0.5, xanchor="center"),
            margin=dict(t=20, b=40, l=20, r=20),
            font=dict(family="sans-serif"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with g2:
        styled_section("Net Trend (Sutun Grafik)", "#6366f1")
        sirali = sorted(denemeler, key=lambda x: x.get("tarih", ""))
        trend_df = pd.DataFrame([{
            "Sinav": f"{d.get('sinav_adi','')[:12]}\n({d.get('tarih','')[-5:]})",
            "Net": d.get("net", 0),
        } for d in sirali])
        fig_bar = px.bar(
            trend_df, x="Sinav", y="Net",
            color="Net",
            color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
        )
        fig_bar.update_layout(
            height=350,
            xaxis_title="", yaxis_title="Net",
            margin=dict(t=20, b=60, l=40, r=20),
            coloraxis_showscale=False,
            font=dict(family="sans-serif"),
        )
        fig_bar.update_traces(
            marker_line_color="white", marker_line_width=1,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── DERS BAZLI ANALIZ ──
    if ders_ozet:
        st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)

        g3, g4 = st.columns(2)

        with g3:
            styled_section("Ders Bazli Net Dagilimi (Pasta)", "#8b5cf6")
            ders_pie_df = pd.DataFrame([{
                "Ders": ders,
                "Ort Net": max(0.1, info["ort_net"]),
            } for ders, info in ders_ozet.items()])
            fig_dpie = px.pie(
                ders_pie_df, names="Ders", values="Ort Net",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.35,
            )
            fig_dpie.update_traces(
                textposition="inside", textinfo="percent+label",
                textfont_size=10,
                marker=dict(line=dict(color="white", width=2)),
            )
            fig_dpie.update_layout(
                height=350, showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, x=0.5, xanchor="center"),
                margin=dict(t=20, b=50, l=20, r=20),
            )
            st.plotly_chart(fig_dpie, use_container_width=True)

        with g4:
            styled_section("Ders Karsilastirma (Sutun)", "#f59e0b")
            ders_bar_df = pd.DataFrame([{
                "Ders": ders,
                "Ort Net": info["ort_net"],
                "Max Net": info["max_net"],
            } for ders, info in sorted(ders_ozet.items(), key=lambda x: -x[1]["ort_net"])])
            fig_dbar = px.bar(
                ders_bar_df, x="Ders", y=["Ort Net", "Max Net"],
                barmode="group",
                color_discrete_map={"Ort Net": "#6366f1", "Max Net": "#10b981"},
            )
            fig_dbar.update_layout(
                height=350,
                xaxis_title="", yaxis_title="Net",
                margin=dict(t=20, b=60, l=40, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, x=0.5, xanchor="center"),
            )
            st.plotly_chart(fig_dbar, use_container_width=True)

        # Ders detay tablosu
        styled_section("Ders Bazli Performans Tablosu", "#06b6d4")
        ders_tablo_html = '''<table style="width:100%;border-collapse:collapse;font-size:0.82rem;border-radius:12px;overflow:hidden">
        <thead><tr style="background:linear-gradient(135deg,#4f46e5,#6366f1);color:white">
            <th style="padding:10px 12px;text-align:left">Ders</th>
            <th style="padding:10px 8px;text-align:center">Sinav</th>
            <th style="padding:10px 8px;text-align:center">Ort D</th>
            <th style="padding:10px 8px;text-align:center">Ort Y</th>
            <th style="padding:10px 8px;text-align:center">Ort Net</th>
            <th style="padding:10px 8px;text-align:center">Max Net</th>
            <th style="padding:10px 8px;text-align:center">Durum</th>
        </tr></thead><tbody>'''
        for i, (ders, info) in enumerate(sorted(ders_ozet.items(), key=lambda x: -x[1]["ort_net"])):
            bg = "#111827" if i % 2 == 0 else "white"
            durum_renk = "#10b981" if info["ort_net"] >= 15 else "#3b82f6" if info["ort_net"] >= 10 else "#f59e0b" if info["ort_net"] >= 5 else "#ef4444"
            durum_text = "Mukemmel" if info["ort_net"] >= 15 else "Iyi" if info["ort_net"] >= 10 else "Gelistir" if info["ort_net"] >= 5 else "Kritik"
            ders_tablo_html += f'''<tr style="background:{bg}">
                <td style="padding:8px 12px;font-weight:600">{ders}</td>
                <td style="padding:8px;text-align:center">{info["sinav_sayisi"]}</td>
                <td style="padding:8px;text-align:center;color:#10b981;font-weight:600">{info["ort_dogru"]:.1f}</td>
                <td style="padding:8px;text-align:center;color:#ef4444;font-weight:600">{info["ort_yanlis"]:.1f}</td>
                <td style="padding:8px;text-align:center;font-weight:800;color:#4f46e5">{info["ort_net"]:.1f}</td>
                <td style="padding:8px;text-align:center;font-weight:600">{info["max_net"]:.1f}</td>
                <td style="padding:8px;text-align:center">
                    <span style="background:{durum_renk}18;color:{durum_renk};padding:3px 10px;border-radius:12px;font-weight:700;font-size:0.72rem">{durum_text}</span>
                </td>
            </tr>'''
        ders_tablo_html += '</tbody></table>'
        st.markdown(ders_tablo_html, unsafe_allow_html=True)

    # ── TUM SINAVLAR TABLOSU ──
    st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
    styled_section("Tum Sinav Sonuclari", "#94A3B8")
    sinav_html = '''<table style="width:100%;border-collapse:collapse;font-size:0.8rem;border-radius:12px;overflow:hidden">
    <thead><tr style="background:linear-gradient(135deg,#94A3B8,#334155);color:white">
        <th style="padding:10px 8px;text-align:center">#</th>
        <th style="padding:10px 12px;text-align:left">Tarih</th>
        <th style="padding:10px 12px;text-align:left">Sinav Adi</th>
        <th style="padding:10px 8px;text-align:center">Tur</th>
        <th style="padding:10px 8px;text-align:center;color:#10b981">D</th>
        <th style="padding:10px 8px;text-align:center;color:#ef4444">Y</th>
        <th style="padding:10px 8px;text-align:center;color:#94a3b8">B</th>
        <th style="padding:10px 8px;text-align:center;font-weight:800">Net</th>
        <th style="padding:10px 8px;text-align:center">Puan</th>
        <th style="padding:10px 8px;text-align:center">Sira</th>
        <th style="padding:10px 8px;text-align:center">Band</th>
    </tr></thead><tbody>'''
    for i, d in enumerate(denemeler):
        bg = "#111827" if i % 2 == 0 else "white"
        b = get_renk_bandi(d.get("puan", 0))
        sinav_html += f'''<tr style="background:{bg}">
            <td style="padding:6px 8px;text-align:center;color:#94a3b8">{i+1}</td>
            <td style="padding:6px 12px;font-weight:500">{d.get("tarih","")[:10]}</td>
            <td style="padding:6px 12px;font-weight:600">{d.get("sinav_adi","")}</td>
            <td style="padding:6px 8px;text-align:center;font-size:0.72rem">{d.get("sinav_turu","")}</td>
            <td style="padding:6px 8px;text-align:center;color:#10b981;font-weight:700">{d.get("dogru",0)}</td>
            <td style="padding:6px 8px;text-align:center;color:#ef4444;font-weight:700">{d.get("yanlis",0)}</td>
            <td style="padding:6px 8px;text-align:center;color:#94a3b8">{d.get("bos",0)}</td>
            <td style="padding:6px 8px;text-align:center;font-weight:800;font-size:0.95rem;color:{b["color"]}">{d.get("net",0):.1f}</td>
            <td style="padding:6px 8px;text-align:center;font-weight:600">{d.get("puan",0):.1f}</td>
            <td style="padding:6px 8px;text-align:center">{d.get("siralama","-")}</td>
            <td style="padding:6px 8px;text-align:center">
                <span style="background:{b["bg"]};color:{b["color"]};padding:2px 8px;border-radius:10px;font-weight:700;font-size:0.68rem">{b["label"]}</span>
            </td>
        </tr>'''
    sinav_html += '</tbody></table>'
    st.markdown(sinav_html, unsafe_allow_html=True)

    # ── PUAN TREND (Line Chart) ──
    if len(denemeler) >= 2:
        st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
        styled_section("Puan & Net Trend Grafigi", "#ec4899")
        sirali2 = sorted(denemeler, key=lambda x: x.get("tarih", ""))
        trend2_df = pd.DataFrame([{
            "Tarih": d.get("tarih", "")[:10],
            "Net": d.get("net", 0),
            "Puan": d.get("puan", 0),
        } for d in sirali2])
        fig_line = px.line(
            trend2_df, x="Tarih", y=["Net", "Puan"],
            markers=True,
            color_discrete_map={"Net": "#6366f1", "Puan": "#ec4899"},
        )
        fig_line.update_layout(
            height=300,
            xaxis_title="", yaxis_title="Deger",
            margin=dict(t=20, b=40, l=40, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, x=0.5, xanchor="center"),
        )
        fig_line.update_traces(line_width=3, marker_size=8)
        st.plotly_chart(fig_line, use_container_width=True)

    # ── DOGRU/YANLIS/BOS BAR (Her sinav) ──
    if len(denemeler) >= 2:
        styled_section("Sinav Bazli Dogru/Yanlis/Bos Dagilimi", "#f97316")
        sirali3 = sorted(denemeler, key=lambda x: x.get("tarih", ""))
        dyb_df = pd.DataFrame([{
            "Sinav": f"{d.get('sinav_adi','')[:10]} ({d.get('tarih','')[-5:]})",
            "Dogru": d.get("dogru", 0),
            "Yanlis": d.get("yanlis", 0),
            "Bos": d.get("bos", 0),
        } for d in sirali3])
        fig_stack = px.bar(
            dyb_df, x="Sinav", y=["Dogru", "Yanlis", "Bos"],
            barmode="stack",
            color_discrete_map={"Dogru": "#10b981", "Yanlis": "#ef4444", "Bos": "#94a3b8"},
        )
        fig_stack.update_layout(
            height=320,
            xaxis_title="", yaxis_title="Soru Sayisi",
            margin=dict(t=20, b=80, l=40, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig_stack, use_container_width=True)

    # ── AI DESTEKLI DEGERLENDIRME ──
    st.markdown('<div class="ek-divider"></div>', unsafe_allow_html=True)
    styled_section("AI Destekli Kapsamli Degerlendirme", "#7c3aed")

    ai_key = f"ek_osd_ai_{ogr_id}"
    ai_pdf_key = f"ek_osd_pdf_{ogr_id}"

    ac1, ac2 = st.columns([3, 1])
    with ac1:
        if st.button("🧠 AI ile Kapsamli Analiz Olustur", type="primary",
                      use_container_width=True, key="ek_osd_ai_btn"):
            client = _get_ai_client()
            if not client:
                st.error("OpenAI API anahtari bulunamadi. Ayarlar sekmesinden veya .env dosyasindan yapilandiriniz.")
            else:
                with st.spinner("AI kapsamli olcme analizi olusturuyor... (Bu islem 15-30 saniye surebilir)"):
                    result = _ai_olcme_son_durum(
                        client, ogr, denemeler, ders_ozet,
                        genel_stats, motivasyonlar, hedefler,
                    )
                    if result:
                        st.session_state[ai_key] = result

    with ac2:
        if st.button("📄 PDF Rapor Olustur", type="secondary",
                      use_container_width=True, key="ek_osd_pdf_btn"):
            with st.spinner("PDF rapor olusturuluyor..."):
                ai_text = st.session_state.get(ai_key)
                pdf_bytes = _olcme_pdf_rapor(ogr, denemeler, ders_ozet, genel_stats, ai_text)
                if pdf_bytes:
                    st.session_state[ai_pdf_key] = pdf_bytes
                    st.success("PDF hazir! Asagidan indirin.")
                else:
                    st.error("PDF olusturulamadi. ReportLab yuklü oldugundan emin olun.")

    # AI sonucu goster
    if st.session_state.get(ai_key):
        ai_text = st.session_state[ai_key]
        st.markdown(f'''
        <div class="ek-glass" style="border-left:4px solid #7c3aed">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">
                <span style="font-size:1.3rem">🧠</span>
                <span style="font-size:1rem;font-weight:800;
                    background:linear-gradient(135deg,#7c3aed,#4f46e5);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                    AI Kapsamli Olcme Degerlendirmesi
                </span>
            </div>
        </div>''', unsafe_allow_html=True)

        # Parse ve goruntule
        sections = ai_text.split("##")
        for sec in sections:
            sec = sec.strip()
            if not sec:
                continue
            lines = sec.split("\n", 1)
            title = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else ""

            section_icons = {
                "GENEL": "📊", "DERS": "📚", "NET": "📈", "GUCLU": "💪",
                "GELISTIR": "🔧", "HEDEF": "🎯", "HAFTALIK": "📋",
                "MOTIVASYON": "🔥", "VELI": "👨‍👩‍👧", "TREND": "📈",
                "EYLEM": "📋", "PSIKOL": "❤️",
            }
            icon = "📌"
            for key, ico in section_icons.items():
                if key in title.upper():
                    icon = ico
                    break

            st.markdown(f'''
            <div class="ek-card" style="border-top:3px solid #7c3aed">
                <div style="font-weight:800;font-size:0.95rem;color:#4f46e5;margin-bottom:8px">
                    {icon} {title}
                </div>
                <div style="font-size:0.85rem;color:#334155;line-height:1.7;white-space:pre-wrap">{body}</div>
            </div>''', unsafe_allow_html=True)

    # PDF indirme butonu
    if st.session_state.get(ai_pdf_key):
        ogr_ad = f"{ogr.get('ad','')}_{ogr.get('soyad','')}"
        tarih_str = datetime.now().strftime("%Y%m%d")
        st.download_button(
            label="📥 Olcme Son Durum PDF Raporunu Indir",
            data=st.session_state[ai_pdf_key],
            file_name=f"Olcme_Son_Durum_{ogr_ad}_{tarih_str}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="ek_osd_dl_btn",
        )


# ============================================================
# 🧠 YAPAY ZEKA ERKEN UYARI SİSTEMİ
# ============================================================

def _render_ai_erken_uyari(store: EKDataStore):
    """AI destekli otomatik erken uyarı sistemi — sayfa açılınca çalışır."""
    styled_section("Yapay Zeka Erken Uyarı Sistemi", "#dc2626")

    # ── Üst açıklama banner ──
    st.markdown('''
    <div style="background:linear-gradient(135deg,#fef2f2,#fee2e2);border:1px solid #fca5a5;
        border-radius:12px;padding:16px 20px;margin-bottom:16px;border-left:4px solid #dc2626">
        <div style="font-size:0.95rem;font-weight:700;color:#991b1b;margin-bottom:6px">
            🧠 Otomatik Veri Toplama & AI Analiz Motoru
        </div>
        <div style="font-size:0.82rem;color:#7f1d1d;line-height:1.5">
            Bu sistem tüm SmartCampusAI modüllerinden (Akademik Takip, Ölçme Değerlendirme,
            Eğitim Koçluğu, Yabancı Dil) verileri otomatik toplar, risk analizi yapar ve
            GPT destekli kişiselleştirilmiş müdahale önerileri üretir.
        </div>
    </div>''', unsafe_allow_html=True)

    # ── AT EarlyWarningEngine yükle ──
    engine = None
    at_store = None
    try:
        from models.akademik_takip import get_akademik_store, EarlyWarningEngine
        at_store = get_akademik_store()
        engine = EarlyWarningEngine(at_store)
    except Exception:
        styled_info_banner(
            "Akademik Takip modülü yüklenemedi. Erken uyarı sistemi bu modüle bağlıdır.",
            "error", "⚠️"
        )
        return

    # ── Öğrenci listesi ──
    ek_ogrenciler = store.load_list("ogrenciler")
    if not ek_ogrenciler:
        styled_info_banner("Koçluk öğrencisi bulunamadı. Önce 'Koçluk Yönetimi' sekmesinden öğrenci ekleyin.", "warning", "👥")
        return

    # ── OTOMATİK TARAMA — sayfa açılınca çalışır ──
    cache_key = "_ek_ai_ew_cache"
    cache_ts_key = "_ek_ai_ew_ts"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Her 5 dk'da bir yeniden tara (veya ilk açılışta)
    cached = st.session_state.get(cache_key)
    cached_ts = st.session_state.get(cache_ts_key, "")
    should_scan = not cached or cached_ts != now_str[:15]  # 5 dk gruplama

    if should_scan:
        with st.spinner("🔍 Tüm öğrenciler taranıyor... Veriler toplanıyor..."):
            scan_results = []
            for ogr in ek_ogrenciler:
                ogr_id = ogr.get("id", "")
                ad = ogr.get("ad", "")
                soyad = ogr.get("soyad", "")
                sinif = ogr.get("sinif", "")
                sube = ogr.get("sube", "")

                # EarlyWarningEngine ile risk hesapla
                risk = engine.calculate_composite_risk(ogr_id)

                # EK verilerini topla
                denemeler = _load_consolidated_deneme(store, ogr_id)
                online_testler = _load_consolidated_online(store, ogr_id)
                gorusmeler = store.get_by_ogrenci("gorusmeler", ogr_id)
                hedefler = store.get_by_ogrenci("hedefler", ogr_id)
                motivasyonlar = store.get_by_ogrenci("motivasyon", ogr_id)

                # Deneme ortalaması
                deneme_puanlar = [d.get("puan", 0) for d in denemeler if d.get("puan", 0) > 0]
                deneme_ort = sum(deneme_puanlar) / len(deneme_puanlar) if deneme_puanlar else 0

                # Motivasyon trendi
                son_motiv = sorted(motivasyonlar, key=lambda x: x.get("tarih", ""), reverse=True)[:3] if motivasyonlar else []
                motiv_avg = sum(m.get("seviye", 3) for m in son_motiv) / len(son_motiv) if son_motiv else 3

                # Aktif hedefler
                aktif_hedef = sum(1 for h in hedefler if h.get("durum") == "Devam Ediyor")
                tamamlanan_hedef = sum(1 for h in hedefler if h.get("durum") == "Tamamlandi")

                # Görüşme sıklığı
                son_30gun = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                yakin_gorusme = sum(1 for g in gorusmeler if g.get("tarih", "") >= son_30gun)

                scan_results.append({
                    "ogr_id": ogr_id,
                    "ad": ad,
                    "soyad": soyad,
                    "sinif": sinif,
                    "sube": sube,
                    "risk_score": risk["score"],
                    "severity": risk["severity"],
                    "factors": risk["factors"],
                    "details": risk["details"],
                    "deneme_sayisi": len(denemeler),
                    "deneme_ort": round(deneme_ort, 1),
                    "online_test_sayisi": len(online_testler),
                    "motiv_avg": round(motiv_avg, 1),
                    "aktif_hedef": aktif_hedef,
                    "tamamlanan_hedef": tamamlanan_hedef,
                    "gorusme_30gun": yakin_gorusme,
                    "gorusme_toplam": len(gorusmeler),
                })

            scan_results.sort(key=lambda x: x["risk_score"], reverse=True)
            st.session_state[cache_key] = scan_results
            st.session_state[cache_ts_key] = now_str[:15]

    results = st.session_state.get(cache_key, [])

    # ── DASHBOARD HEADER ──
    toplam = len(results)
    kritik = sum(1 for r in results if r["severity"] == "critical")
    yuksek = sum(1 for r in results if r["severity"] == "high")
    orta = sum(1 for r in results if r["severity"] == "medium")
    dusuk = sum(1 for r in results if r["severity"] == "low")
    risksiz = toplam - kritik - yuksek - orta - dusuk

    _diamond_stats([
        ("🚨", str(kritik), "Kritik Risk", "#dc2626"),
        ("⚠️", str(yuksek), "Yüksek Risk", "#ea580c"),
        ("📊", str(orta), "Orta Risk", "#d97706"),
        ("✅", str(risksiz), "Risksiz", "#16a34a"),
    ])

    # Son tarama bilgisi
    st.markdown(f'''
    <div style="text-align:center;font-size:0.75rem;color:#94a3b8;margin:8px 0 16px">
        Son tarama: {datetime.now().strftime("%d.%m.%Y %H:%M")} | {toplam} öğrenci tarandı |
        Veri kaynakları: AT + OD + EK + YD
    </div>''', unsafe_allow_html=True)

    # ── YENİDEN TARA butonu ──
    if st.button("🔄 Yeniden Tara", key="ek_ew_rescan", use_container_width=True):
        st.session_state.pop(cache_key, None)
        st.session_state.pop(cache_ts_key, None)
        st.rerun()

    # ── ALT SEKMELER ──
    ew_tabs = st.tabs([
        "  🚨 Risk Haritası  ",
        "  🧠 AI Analiz & Öneriler  ",
        "  📋 Detaylı Rapor  ",
        "  📊 Öğrenci Detay & PDF  ",
    ])

    # ═══════════════════════════════════════════
    # TAB 1: RİSK HARİTASI
    # ═══════════════════════════════════════════
    with ew_tabs[0]:
        styled_section("Öğrenci Risk Haritası", "#dc2626")

        if not results:
            styled_info_banner("Tarama sonucu bulunamadı.", "info", "📊")
        else:
            riskli = [r for r in results if r["severity"]]
            if not riskli:
                st.markdown('''
                <div style="text-align:center;padding:40px 20px;background:linear-gradient(135deg,#f0fdf4,#dcfce7);
                    border-radius:16px;border:2px solid #86efac">
                    <div style="font-size:3rem;margin-bottom:12px">✅</div>
                    <div style="font-size:1.2rem;font-weight:700;color:#166534">Tüm Öğrenciler Güvende</div>
                    <div style="font-size:0.85rem;color:#15803d;margin-top:8px">
                        Hiçbir öğrencide risk tespit edilmedi. Harika gidiyorsunuz!
                    </div>
                </div>''', unsafe_allow_html=True)
            else:
                # Severity renkler
                sev_colors = {
                    "critical": ("#dc2626", "#fef2f2", "🚨 KRİTİK"),
                    "high": ("#ea580c", "#fff7ed", "⚠️ YÜKSEK"),
                    "medium": ("#d97706", "#fffbeb", "📊 ORTA"),
                    "low": ("#65a30d", "#f7fee7", "📋 DÜŞÜK"),
                }

                for r in riskli:
                    sev = r["severity"]
                    color, bg, label = sev_colors.get(sev, ("#6b7280", "#0F1420", "—"))
                    factors = r.get("factors", {})

                    # Faktör barları
                    factor_bars = ""
                    factor_labels = {
                        "attendance": ("Devamsızlık", "#ef4444"),
                        "grade": ("Not Düşüşü", "#f59e0b"),
                        "homework": ("Ödev Teslim", "#3b82f6"),
                        "exam": ("Sınav Trendi", "#8b5cf6"),
                    }
                    for fkey, (flabel, fcolor) in factor_labels.items():
                        val = factors.get(fkey, 0)
                        if val > 0:
                            factor_bars += f'''
                            <div style="display:flex;align-items:center;gap:8px;margin-top:4px">
                                <div style="font-size:0.72rem;color:#64748b;width:85px">{flabel}</div>
                                <div style="flex:1;background:#e2e8f0;border-radius:4px;height:8px;overflow:hidden">
                                    <div style="width:{min(val, 100)}%;height:100%;background:{fcolor};border-radius:4px"></div>
                                </div>
                                <div style="font-size:0.72rem;color:{fcolor};font-weight:700;width:32px;text-align:right">{val:.0f}</div>
                            </div>'''

                    st.markdown(f'''
                    <div style="background:{bg};border:1px solid {color}33;border-radius:12px;padding:14px 18px;
                        margin-bottom:10px;border-left:5px solid {color}">
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <div>
                                <span style="font-size:0.95rem;font-weight:700;color:#94A3B8">
                                    {r["ad"]} {r["soyad"]}
                                </span>
                                <span style="font-size:0.78rem;color:#64748b;margin-left:8px">
                                    {r["sinif"]}/{r["sube"]}
                                </span>
                            </div>
                            <div style="display:flex;align-items:center;gap:10px">
                                <span style="font-size:0.75rem;font-weight:700;color:{color};
                                    background:{color}15;padding:3px 10px;border-radius:6px">{label}</span>
                                <span style="font-size:1.4rem;font-weight:900;color:{color}">{r["risk_score"]:.0f}</span>
                            </div>
                        </div>
                        <div style="font-size:0.78rem;color:#475569;margin-top:6px">{r["details"]}</div>
                        <div style="margin-top:8px">{factor_bars}</div>
                        <div style="display:flex;gap:12px;margin-top:8px;flex-wrap:wrap">
                            <span style="font-size:0.72rem;color:#64748b">📝 {r["deneme_sayisi"]} sınav (ort: {r["deneme_ort"]})</span>
                            <span style="font-size:0.72rem;color:#64748b">💻 {r["online_test_sayisi"]} online test</span>
                            <span style="font-size:0.72rem;color:#64748b">🔥 Motivasyon: {r["motiv_avg"]}/5</span>
                            <span style="font-size:0.72rem;color:#64748b">🎯 {r["aktif_hedef"]} aktif hedef</span>
                            <span style="font-size:0.72rem;color:#64748b">💬 {r["gorusme_30gun"]} görüşme (30 gün)</span>
                        </div>
                    </div>''', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # TAB 2: AI ANALİZ & ÖNERİLER
    # ═══════════════════════════════════════════
    with ew_tabs[1]:
        styled_section("AI Destekli Risk Analizi & Müdahale Önerileri", "#7c3aed")

        riskli = [r for r in results if r["risk_score"] >= 30]
        if not riskli:
            styled_info_banner("Yüksek riskli öğrenci yok — AI analiz gerekmiyor.", "success", "✅")
        else:
            client = _get_ai_client()
            if not client:
                styled_info_banner(
                    "OpenAI API anahtarı bulunamadı. AI analiz için .env dosyasında OPENAI_API_KEY tanımlayın.",
                    "error", "🔑"
                )
            else:
                ai_cache_key = "_ek_ai_ew_analysis"
                ai_cache_ts = "_ek_ai_ew_analysis_ts"
                cached_analysis = st.session_state.get(ai_cache_key)
                cached_analysis_ts = st.session_state.get(ai_cache_ts, "")

                # Otomatik AI analiz (5 dk cache)
                should_analyze = not cached_analysis or cached_analysis_ts != now_str[:15]

                if should_analyze:
                    with st.spinner("🧠 AI risk analizi yapılıyor... Kişiselleştirilmiş öneriler üretiliyor..."):
                        # Riskli öğrenci özeti hazırla
                        ogrenci_ozetleri = []
                        for r in riskli[:10]:  # max 10 öğrenci
                            f = r.get("factors", {})
                            ozet = (
                                f"- {r['ad']} {r['soyad']} ({r['sinif']}/{r['sube']}): "
                                f"Risk={r['risk_score']:.0f}, Seviye={r['severity']}, "
                                f"Devamsızlık={f.get('attendance',0):.0f}, Not={f.get('grade',0):.0f}, "
                                f"Ödev={f.get('homework',0):.0f}, Sınav={f.get('exam',0):.0f}, "
                                f"Deneme Ort={r['deneme_ort']}, Motivasyon={r['motiv_avg']}/5, "
                                f"30 Gün Görüşme={r['gorusme_30gun']}, "
                                f"Detay: {r['details']}"
                            )
                            ogrenci_ozetleri.append(ozet)

                        prompt = f"""Sen bir eğitim koçluğu uzmanısın. Aşağıdaki öğrencilerin risk verilerini analiz et.

ÖĞRENCİ RİSK VERİLERİ:
{chr(10).join(ogrenci_ozetleri)}

Risk faktörleri: devamsızlık (0-100), not düşüşü (0-100), ödev teslim (0-100), sınav trendi (0-100)
Bileşik risk: %30 devamsızlık + %25 not + %20 ödev + %25 sınav

Her öğrenci için şunları üret:
1. 2-3 cümlelik durum değerlendirmesi
2. En acil müdahale önerisi (1 cümle)
3. Haftalık eylem planı (3 madde)
4. Veliye iletilecek mesaj (2 cümle)

Ayrıca genel sınıf için:
- Ortak risk pattern'leri
- Toplu müdahale önerileri (3 madde)

Yanıtı JSON formatında ver:
{{
    "ogrenciler": [
        {{
            "ad_soyad": "...",
            "durum_degerlendirme": "...",
            "acil_mudahale": "...",
            "haftalik_eylem": ["...", "...", "..."],
            "veli_mesaji": "..."
        }}
    ],
    "genel_analiz": {{
        "ortak_patternler": "...",
        "toplu_mudahale": ["...", "...", "..."]
    }}
}}"""

                        try:
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": __import__('utils.ai_rules', fromlist=['inject_rules']).inject_rules(
                                        "Sen deneyimli bir egitim kocu ve rehberlik uzmanisin. Turkce yanit ver. JSON formatinda yanit ver.", short=True)},
                                    {"role": "user", "content": prompt},
                                ],
                                temperature=0.7,
                                max_tokens=3000,
                                response_format={"type": "json_object"},
                            )
                            import json as _json
                            ai_result = _json.loads(response.choices[0].message.content)
                            st.session_state[ai_cache_key] = ai_result
                            st.session_state[ai_cache_ts] = now_str[:15]
                        except Exception as e:
                            st.session_state[ai_cache_key] = {"error": str(e)}
                            st.session_state[ai_cache_ts] = now_str[:15]

                # Sonuçları göster
                ai_data = st.session_state.get(ai_cache_key, {})

                if ai_data.get("error"):
                    styled_info_banner(f"AI analiz hatası: {ai_data['error']}", "error", "⚠️")
                elif ai_data:
                    # Genel analiz
                    genel = ai_data.get("genel_analiz", {})
                    if genel:
                        st.markdown(f'''
                        <div style="background:linear-gradient(135deg,#eef2ff,#e0e7ff);border:1px solid #a5b4fc;
                            border-radius:12px;padding:16px 20px;margin-bottom:16px;border-left:4px solid #6366f1">
                            <div style="font-size:0.88rem;font-weight:700;color:#3730a3;margin-bottom:8px">
                                📊 Genel Sınıf Analizi
                            </div>
                            <div style="font-size:0.82rem;color:#4338ca;line-height:1.6;margin-bottom:10px">
                                {genel.get("ortak_patternler", "")}
                            </div>
                        </div>''', unsafe_allow_html=True)

                        for i, oneri in enumerate(genel.get("toplu_mudahale", []), 1):
                            st.markdown(
                                f'<div style="padding:8px 14px;background:#f5f3ff;border-radius:8px;margin-bottom:4px;'
                                f'font-size:0.82rem;border-left:3px solid #7c3aed">📌 {i}. {oneri}</div>',
                                unsafe_allow_html=True,
                            )

                    st.markdown('<hr style="border:none;border-top:1px solid #e2e8f0;margin:16px 0">', unsafe_allow_html=True)

                    # Öğrenci bazlı AI analiz
                    for ogr_ai in ai_data.get("ogrenciler", []):
                        ad_soyad = ogr_ai.get("ad_soyad", "—")
                        # Eşleşen risk verisini bul
                        match = next((r for r in riskli if f"{r['ad']} {r['soyad']}" == ad_soyad), None)
                        sev_color = "#dc2626" if match and match.get("severity") == "critical" else (
                            "#ea580c" if match and match.get("severity") == "high" else "#d97706"
                        )

                        st.markdown(f'''
                        <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;
                            margin-bottom:12px;border-left:5px solid {sev_color};box-shadow:0 2px 8px rgba(0,0,0,0.04)">
                            <div style="font-size:0.95rem;font-weight:700;color:#94A3B8;margin-bottom:8px">
                                🎯 {ad_soyad}
                                {f'<span style="font-size:0.75rem;color:{sev_color};margin-left:8px">Risk: {match["risk_score"]:.0f}</span>' if match else ''}
                            </div>
                            <div style="font-size:0.82rem;color:#475569;line-height:1.6;margin-bottom:10px;
                                background:#111827;padding:10px 14px;border-radius:8px">
                                💬 {ogr_ai.get("durum_degerlendirme", "")}
                            </div>
                            <div style="font-size:0.82rem;color:#dc2626;font-weight:600;margin-bottom:8px;
                                background:#fef2f2;padding:8px 14px;border-radius:8px">
                                🚨 Acil: {ogr_ai.get("acil_mudahale", "")}
                            </div>
                        </div>''', unsafe_allow_html=True)

                        # Haftalık eylem
                        for j, eylem in enumerate(ogr_ai.get("haftalik_eylem", []), 1):
                            st.markdown(
                                f'<div style="padding:6px 14px;background:#f0fdf4;border-radius:6px;margin-bottom:3px;'
                                f'font-size:0.8rem;border-left:3px solid #10b981;margin-left:20px">📋 {j}. {eylem}</div>',
                                unsafe_allow_html=True,
                            )

                        # Veli mesajı
                        veli_msg = ogr_ai.get("veli_mesaji", "")
                        if veli_msg:
                            st.markdown(
                                f'<div style="padding:8px 14px;background:#fffbeb;border-radius:8px;margin:6px 0 4px 20px;'
                                f'font-size:0.8rem;border-left:3px solid #d97706">👨‍👩‍👧 Veli: {veli_msg}</div>',
                                unsafe_allow_html=True,
                            )

                # Yeniden analiz butonu
                if st.button("🧠 AI Analizi Yenile", key="ek_ew_ai_refresh"):
                    st.session_state.pop(ai_cache_key, None)
                    st.session_state.pop(ai_cache_ts, None)
                    st.rerun()

    # ═══════════════════════════════════════════
    # TAB 3: DETAYLI RAPOR
    # ═══════════════════════════════════════════
    with ew_tabs[2]:
        styled_section("Erken Uyarı Detaylı Rapor", "#0d9488")

        if not results:
            styled_info_banner("Tarama sonucu bulunamadı.", "info", "📊")
        else:
            # Filtre
            fc1, fc2 = st.columns([1, 1])
            with fc1:
                filtre_sev = st.selectbox("Risk Seviyesi", ["Tümü", "Kritik", "Yüksek", "Orta", "Düşük", "Risksiz"],
                                          key="ek_ew_filtre_sev")
            with fc2:
                filtre_siralama = st.selectbox("Sıralama", ["Risk (Yüksek→Düşük)", "Risk (Düşük→Yüksek)", "İsim (A→Z)"],
                                               key="ek_ew_filtre_sira")

            # Filtre uygula
            filtered = results[:]
            sev_map = {"Kritik": "critical", "Yüksek": "high", "Orta": "medium", "Düşük": "low", "Risksiz": None}
            if filtre_sev != "Tümü":
                target_sev = sev_map.get(filtre_sev)
                if filtre_sev == "Risksiz":
                    filtered = [r for r in filtered if not r["severity"]]
                else:
                    filtered = [r for r in filtered if r["severity"] == target_sev]

            if filtre_siralama == "Risk (Düşük→Yüksek)":
                filtered.sort(key=lambda x: x["risk_score"])
            elif filtre_siralama == "İsim (A→Z)":
                filtered.sort(key=lambda x: f"{x['ad']} {x['soyad']}")

            st.markdown(f'<div style="font-size:0.78rem;color:#64748b;margin-bottom:10px">'
                        f'Gösterilen: {len(filtered)} / {len(results)} öğrenci</div>',
                        unsafe_allow_html=True)

            # Tablo
            if filtered:
                sev_badges = {
                    "critical": '<span style="background:#dc2626;color:white;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:700">KRİTİK</span>',
                    "high": '<span style="background:#ea580c;color:white;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:700">YÜKSEK</span>',
                    "medium": '<span style="background:#d97706;color:white;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:700">ORTA</span>',
                    "low": '<span style="background:#65a30d;color:white;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:700">DÜŞÜK</span>',
                    None: '<span style="background:#16a34a;color:white;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:700">✅</span>',
                    "": '<span style="background:#16a34a;color:white;padding:2px 8px;border-radius:4px;font-size:0.72rem;font-weight:700">✅</span>',
                }

                rows_html = ""
                for i, r in enumerate(filtered):
                    f = r.get("factors", {})
                    bg = "#fff" if i % 2 == 0 else "#111827"
                    badge = sev_badges.get(r["severity"], sev_badges[""])
                    rows_html += f'''
                    <tr style="background:{bg}">
                        <td style="padding:8px 12px;font-size:0.82rem;font-weight:600">{r["ad"]} {r["soyad"]}</td>
                        <td style="padding:8px;font-size:0.8rem;text-align:center">{r["sinif"]}/{r["sube"]}</td>
                        <td style="padding:8px;text-align:center">{badge}</td>
                        <td style="padding:8px;font-size:0.85rem;font-weight:700;text-align:center;color:{"#dc2626" if r["risk_score"]>=60 else "#d97706" if r["risk_score"]>=30 else "#16a34a"}">{r["risk_score"]:.0f}</td>
                        <td style="padding:8px;font-size:0.78rem;text-align:center">{f.get("attendance",0):.0f}</td>
                        <td style="padding:8px;font-size:0.78rem;text-align:center">{f.get("grade",0):.0f}</td>
                        <td style="padding:8px;font-size:0.78rem;text-align:center">{f.get("homework",0):.0f}</td>
                        <td style="padding:8px;font-size:0.78rem;text-align:center">{f.get("exam",0):.0f}</td>
                        <td style="padding:8px;font-size:0.78rem;text-align:center">{r["deneme_ort"]}</td>
                        <td style="padding:8px;font-size:0.78rem;text-align:center">{r["motiv_avg"]}/5</td>
                    </tr>'''

                st.markdown(f'''
                <div style="overflow-x:auto;border-radius:12px;border:1px solid #e2e8f0">
                    <table style="width:100%;border-collapse:collapse">
                        <thead>
                            <tr style="background:linear-gradient(135deg,#0B0F19,#94A3B8);color:white">
                                <th style="padding:10px 12px;font-size:0.78rem;text-align:left">Öğrenci</th>
                                <th style="padding:10px 8px;font-size:0.78rem;text-align:center">Sınıf</th>
                                <th style="padding:10px 8px;font-size:0.78rem;text-align:center">Seviye</th>
                                <th style="padding:10px 8px;font-size:0.78rem;text-align:center">Risk</th>
                                <th style="padding:10px 8px;font-size:0.78rem;text-align:center">Devam.</th>
                                <th style="padding:10px 8px;font-size:0.78rem;text-align:center">Not</th>
                                <th style="padding:10px 8px;font-size:0.78rem;text-align:center">Ödev</th>
                                <th style="padding:10px 8px;font-size:0.78rem;text-align:center">Sınav</th>
                                <th style="padding:10px 8px;font-size:0.78rem;text-align:center">Ort.</th>
                                <th style="padding:10px 8px;font-size:0.78rem;text-align:center">Motiv.</th>
                            </tr>
                        </thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                </div>''', unsafe_allow_html=True)

                # CSV İndir
                csv_lines = ["Öğrenci;Sınıf;Risk Skoru;Seviye;Devamsızlık;Not;Ödev;Sınav;Deneme Ort;Motivasyon"]
                for r in filtered:
                    f = r.get("factors", {})
                    csv_lines.append(
                        f"{r['ad']} {r['soyad']};{r['sinif']}/{r['sube']};{r['risk_score']:.1f};"
                        f"{r['severity'] or 'risksiz'};{f.get('attendance',0):.0f};{f.get('grade',0):.0f};"
                        f"{f.get('homework',0):.0f};{f.get('exam',0):.0f};{r['deneme_ort']};{r['motiv_avg']}"
                    )
                csv_data = "\n".join(csv_lines)
                st.download_button(
                    "📥 CSV Rapor İndir",
                    data=csv_data,
                    file_name=f"erken_uyari_rapor_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="ek_ew_csv_dl",
                )

    # ═══════════════════════════════════════════
    # TAB 4: ÖĞRENCİ DETAY & PDF RAPOR
    # ═══════════════════════════════════════════
    with ew_tabs[3]:
        styled_section("Öğrenci Detay Analizi & PDF Rapor", "#4f46e5")

        if not results:
            styled_info_banner("Tarama sonucu bulunamadı.", "info", "📊")
        else:
            # ── Öğrenci seçimi ──
            ogr_opts = {f"{r['ad']} {r['soyad']} ({r['sinif']}/{r['sube']}) — Risk: {r['risk_score']:.0f}": r
                        for r in results}
            sec_ogr_key = st.selectbox("Öğrenci Seçin", list(ogr_opts.keys()), key="ek_ew_ogr_detay")
            sel = ogr_opts.get(sec_ogr_key)

            if sel:
                ogr_id = sel["ogr_id"]
                ad_soyad = f"{sel['ad']} {sel['soyad']}"
                factors = sel.get("factors", {})

                # Detay verilerini yükle
                denemeler = _load_consolidated_deneme(store, ogr_id)
                denemeler = sorted(denemeler, key=lambda x: x.get("tarih", ""))
                online_testler = _load_consolidated_online(store, ogr_id)
                gorusmeler = store.get_by_ogrenci("gorusmeler", ogr_id)
                hedefler = store.get_by_ogrenci("hedefler", ogr_id)
                motivasyonlar = store.get_by_ogrenci("motivasyon", ogr_id)
                motivasyonlar = sorted(motivasyonlar, key=lambda x: x.get("tarih", ""))

                # ── Üst risk kartı ──
                sev_map = {"critical": ("KRİTİK", "#dc2626"), "high": ("YÜKSEK", "#ea580c"),
                           "medium": ("ORTA", "#d97706"), "low": ("DÜŞÜK", "#65a30d")}
                sev_label, sev_color = sev_map.get(sel["severity"], ("RİSKSİZ", "#16a34a"))

                st.markdown(f'''
                <div style="background:linear-gradient(135deg,{sev_color}08,{sev_color}15);border:2px solid {sev_color}44;
                    border-radius:14px;padding:18px 24px;margin-bottom:16px">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div>
                            <div style="font-size:1.3rem;font-weight:800;color:#94A3B8">{ad_soyad}</div>
                            <div style="font-size:0.85rem;color:#64748b;margin-top:4px">
                                Sınıf: {sel["sinif"]}/{sel["sube"]} | {sel["deneme_sayisi"]} sınav |
                                {sel["gorusme_toplam"]} görüşme | Motivasyon: {sel["motiv_avg"]}/5
                            </div>
                        </div>
                        <div style="text-align:center">
                            <div style="font-size:2.8rem;font-weight:900;color:{sev_color}">{sel["risk_score"]:.0f}</div>
                            <div style="font-size:0.78rem;font-weight:700;color:{sev_color}">{sev_label}</div>
                        </div>
                    </div>
                    <div style="font-size:0.82rem;color:#475569;margin-top:8px">{sel["details"]}</div>
                </div>''', unsafe_allow_html=True)

                # ══════════════════════════════════════
                # PLOTLY GRAFİKLER (EKRANDA)
                # ══════════════════════════════════════
                try:
                    import plotly.graph_objects as go
                    from utils.chart_utils import sc_pie, sc_bar, SC_CHART_CFG, SC_COLORS
                    has_plotly = True
                except ImportError:
                    has_plotly = False

                if has_plotly:
                    g_col1, g_col2 = st.columns(2)

                    # ── 1) PASTA: Risk Faktörleri Dağılımı ──
                    with g_col1:
                        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#94A3B8;margin-bottom:8px">'
                                    '🥧 Risk Faktörleri Dağılımı</div>', unsafe_allow_html=True)
                        f_labels = ["Devamsızlık", "Not Düşüşü", "Ödev Teslim", "Sınav Trendi"]
                        f_values = [
                            factors.get("attendance", 0),
                            factors.get("grade", 0),
                            factors.get("homework", 0),
                            factors.get("exam", 0),
                        ]
                        f_colors = ["#ef4444", "#f59e0b", "#3b82f6", "#8b5cf6"]
                        # Sıfır değerleri filtrele
                        pie_labels, pie_values, pie_colors = [], [], []
                        for lb, vl, cl in zip(f_labels, f_values, f_colors):
                            if vl > 0:
                                pie_labels.append(lb)
                                pie_values.append(vl)
                                pie_colors.append(cl)

                        if pie_values:
                            fig_pie = go.Figure(data=[go.Pie(
                                labels=pie_labels, values=pie_values,
                                marker=dict(colors=pie_colors),
                                textinfo="label+percent",
                            )])
                            sc_pie(fig_pie, height=280,
                                   center_text=f"<b>{sel['risk_score']:.0f}</b><br><span style='font-size:10px;color:#64748b'>Risk</span>")
                            st.plotly_chart(fig_pie, use_container_width=True, config=SC_CHART_CFG)
                        else:
                            styled_info_banner("Risk faktörü tespit edilmedi.", "success", "✅")

                    # ── 2) SÜTUN: Faktör Skorları ──
                    with g_col2:
                        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#94A3B8;margin-bottom:8px">'
                                    '📊 Risk Faktör Skorları</div>', unsafe_allow_html=True)
                        fig_bar = go.Figure(data=[go.Bar(
                            x=f_labels, y=f_values,
                            marker_color=f_colors,
                            text=[f"{v:.0f}" for v in f_values],
                            textposition="outside",
                        )])
                        sc_bar(fig_bar, height=280)
                        fig_bar.update_layout(yaxis_range=[0, max(f_values + [10]) * 1.2])
                        st.plotly_chart(fig_bar, use_container_width=True, config=SC_CHART_CFG)

                    # ── 3) SÜTUN: Deneme/Sınav Puan Trendi ──
                    if denemeler:
                        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#94A3B8;margin:12px 0 8px">'
                                    '📈 Sınav Puan Trendi</div>', unsafe_allow_html=True)
                        sinav_labels = []
                        sinav_puanlar = []
                        sinav_colors = []
                        for d in denemeler[-15:]:  # son 15 sınav
                            ad_kisa = d.get("sinav_adi", d.get("test_adi", "Sınav"))
                            if len(ad_kisa) > 18:
                                ad_kisa = ad_kisa[:16] + ".."
                            tarih = d.get("tarih", "")
                            if tarih and len(tarih) >= 10:
                                ad_kisa = f"{tarih[5:10]} {ad_kisa}"
                            sinav_labels.append(ad_kisa)
                            puan = d.get("puan", 0)
                            sinav_puanlar.append(puan)
                            sinav_colors.append("#dc2626" if puan < 50 else "#d97706" if puan < 70 else "#16a34a")

                        fig_trend = go.Figure()
                        fig_trend.add_trace(go.Bar(
                            x=sinav_labels, y=sinav_puanlar,
                            marker_color=sinav_colors,
                            text=[f"{p:.0f}" for p in sinav_puanlar],
                            textposition="outside",
                        ))
                        # Ortalama çizgisi
                        if sinav_puanlar:
                            ort = sum(sinav_puanlar) / len(sinav_puanlar)
                            fig_trend.add_hline(y=ort, line_dash="dash", line_color="#6366f1",
                                                annotation_text=f"Ort: {ort:.1f}", annotation_position="top left")
                        sc_bar(fig_trend, height=300)
                        fig_trend.update_layout(
                            yaxis_range=[0, max(sinav_puanlar + [10]) * 1.2],
                            xaxis_tickangle=-45,
                            margin=dict(b=80),
                        )
                        st.plotly_chart(fig_trend, use_container_width=True, config=SC_CHART_CFG)

                    # ── 4) Motivasyon Trendi (çizgi) ──
                    if motivasyonlar:
                        g2_col1, g2_col2 = st.columns(2)
                        with g2_col1:
                            st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#94A3B8;margin-bottom:8px">'
                                        '🔥 Motivasyon Trendi</div>', unsafe_allow_html=True)
                            m_tarihler = [m.get("tarih", "?") for m in motivasyonlar[-12:]]
                            m_seviyeler = [m.get("seviye", 3) for m in motivasyonlar[-12:]]
                            fig_motiv = go.Figure()
                            fig_motiv.add_trace(go.Scatter(
                                x=m_tarihler, y=m_seviyeler,
                                mode="lines+markers+text",
                                text=[str(s) for s in m_seviyeler],
                                textposition="top center",
                                line=dict(color="#ec4899", width=3),
                                marker=dict(size=10, color="#ec4899"),
                                fill="tozeroy",
                                fillcolor="rgba(236,72,153,0.1)",
                            ))
                            fig_motiv.update_layout(
                                height=240, yaxis_range=[0, 5.5],
                                margin=dict(t=10, b=30, l=30, r=10),
                                yaxis_title="Seviye (1-5)",
                            )
                            st.plotly_chart(fig_motiv, use_container_width=True, config=SC_CHART_CFG)

                        # ── 5) PASTA: Hedef Durumu ──
                        with g2_col2:
                            st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#94A3B8;margin-bottom:8px">'
                                        '🎯 Hedef Durumu</div>', unsafe_allow_html=True)
                            if hedefler:
                                h_devam = sum(1 for h in hedefler if h.get("durum") == "Devam Ediyor")
                                h_tamam = sum(1 for h in hedefler if h.get("durum") == "Tamamlandi")
                                h_iptal = sum(1 for h in hedefler if h.get("durum") not in ("Devam Ediyor", "Tamamlandi"))
                                h_labels = ["Devam Eden", "Tamamlanan", "Diğer"]
                                h_vals = [h_devam, h_tamam, h_iptal]
                                h_cols = ["#3b82f6", "#10b981", "#94a3b8"]
                                # Sıfır filtrele
                                hl, hv, hc = [], [], []
                                for a, b, c in zip(h_labels, h_vals, h_cols):
                                    if b > 0:
                                        hl.append(a)
                                        hv.append(b)
                                        hc.append(c)
                                if hv:
                                    fig_h = go.Figure(data=[go.Pie(labels=hl, values=hv, marker=dict(colors=hc))])
                                    sc_pie(fig_h, height=240,
                                           center_text=f"<b>{len(hedefler)}</b><br><span style='font-size:10px;color:#64748b'>Hedef</span>")
                                    st.plotly_chart(fig_h, use_container_width=True, config=SC_CHART_CFG)
                                else:
                                    styled_info_banner("Hedef kaydı yok.", "info", "🎯")
                            else:
                                styled_info_banner("Hedef kaydı yok.", "info", "🎯")

                # ══════════════════════════════════════
                # PDF RAPOR ÜRETİMİ
                # ══════════════════════════════════════
                st.markdown('<hr style="border:none;border-top:2px solid #e2e8f0;margin:20px 0">', unsafe_allow_html=True)

                pdf_key = f"_ek_ew_pdf_{ogr_id}"
                if st.button("📄 PDF Rapor Oluştur", key="ek_ew_pdf_btn", type="primary", use_container_width=True):
                    with st.spinner("PDF rapor oluşturuluyor (grafiklerle)..."):
                        try:
                            import pandas as pd
                            from utils.report_utils import ReportPDFGenerator

                            pdf = ReportPDFGenerator(
                                title=f"Erken Uyarı Raporu — {ad_soyad}",
                                subtitle=f"Sınıf: {sel['sinif']}/{sel['sube']} | Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                            )
                            pdf.add_header()

                            # 1) Risk Özet Metrikleri
                            pdf.add_section("Risk Özeti", "#dc2626")
                            pdf.add_metrics([
                                ("Risk Skoru", f"{sel['risk_score']:.0f}", sev_color),
                                ("Seviye", sev_label, sev_color),
                                ("Sınav Sayısı", str(sel["deneme_sayisi"]), "#3b82f6"),
                                ("Deneme Ort.", str(sel["deneme_ort"]), "#6366f1"),
                                ("Motivasyon", f"{sel['motiv_avg']}/5", "#ec4899"),
                            ])
                            pdf.add_spacer(0.3)
                            pdf.add_text(f"Detay: {sel['details']}")

                            # 2) Risk Faktörleri Bar Chart
                            pdf.add_section("Risk Faktörleri", "#4f46e5")
                            factor_data = {
                                "Devamsızlık": factors.get("attendance", 0),
                                "Not Düşüşü": factors.get("grade", 0),
                                "Ödev Teslim": factors.get("homework", 0),
                                "Sınav Trendi": factors.get("exam", 0),
                            }
                            pdf.add_bar_chart(factor_data, "Risk Faktör Skorları (0-100)", "#4f46e5")

                            # 3) Risk Faktörleri Pasta
                            pie_data = {k: v for k, v in factor_data.items() if v > 0}
                            if pie_data:
                                pdf.add_donut_chart(pie_data, "Risk Dağılımı",
                                                    ["#ef4444", "#f59e0b", "#3b82f6", "#8b5cf6"][:len(pie_data)])

                            # 4) Sınav Puan Trendi
                            if denemeler:
                                pdf.add_section("Sınav Puan Trendi", "#d97706")
                                sinav_chart_data = {}
                                for d in denemeler[-12:]:
                                    lbl = d.get("sinav_adi", d.get("test_adi", "Sınav"))
                                    if len(lbl) > 15:
                                        lbl = lbl[:13] + ".."
                                    tarih = d.get("tarih", "")
                                    if tarih and len(tarih) >= 10:
                                        lbl = f"{tarih[5:10]}"
                                    sinav_chart_data[lbl] = d.get("puan", 0)
                                pdf.add_bar_chart(sinav_chart_data, "Son Sınav Puanları", "#d97706")

                                # Sınav tablo
                                sinav_rows = []
                                for d in denemeler[-12:]:
                                    sinav_rows.append({
                                        "Sınav": d.get("sinav_adi", d.get("test_adi", "—"))[:25],
                                        "Tarih": d.get("tarih", "—")[:10],
                                        "Puan": f"{d.get('puan', 0):.0f}",
                                        "Doğru": str(d.get("dogru", 0)),
                                        "Yanlış": str(d.get("yanlis", 0)),
                                        "Net": f"{d.get('net', 0):.1f}",
                                        "Kaynak": d.get("_kaynak", "EK"),
                                    })
                                df_sinav = pd.DataFrame(sinav_rows)
                                pdf.add_table(df_sinav, header_color="#d97706")

                            # 5) Motivasyon Trendi
                            if motivasyonlar:
                                pdf.add_section("Motivasyon Trendi", "#ec4899")
                                m_chart = {}
                                for m in motivasyonlar[-10:]:
                                    tarih = m.get("tarih", "?")
                                    if len(tarih) >= 10:
                                        tarih = tarih[:10]
                                    m_chart[tarih] = m.get("seviye", 3)
                                pdf.add_bar_chart(m_chart, "Motivasyon Seviyesi (1-5)", "#ec4899")

                            # 6) Hedef Durumu
                            if hedefler:
                                pdf.add_section("Hedef Durumu", "#10b981")
                                h_devam = sum(1 for h in hedefler if h.get("durum") == "Devam Ediyor")
                                h_tamam = sum(1 for h in hedefler if h.get("durum") == "Tamamlandi")
                                h_diger = len(hedefler) - h_devam - h_tamam
                                hedef_pie = {}
                                if h_devam:
                                    hedef_pie["Devam Eden"] = h_devam
                                if h_tamam:
                                    hedef_pie["Tamamlanan"] = h_tamam
                                if h_diger:
                                    hedef_pie["Diğer"] = h_diger
                                if hedef_pie:
                                    pdf.add_donut_chart(hedef_pie, "Hedef Dağılımı",
                                                        ["#3b82f6", "#10b981", "#94a3b8"][:len(hedef_pie)])
                                pdf.add_metrics([
                                    ("Aktif", str(h_devam), "#3b82f6"),
                                    ("Tamamlanan", str(h_tamam), "#10b981"),
                                    ("Toplam", str(len(hedefler)), "#6366f1"),
                                ])

                            # 7) Görüşme Özeti
                            if gorusmeler:
                                pdf.add_section("Görüşme Özeti", "#0d9488")
                                tam = sum(1 for g in gorusmeler if g.get("durum") == "Tamamlandi")
                                plan = len(gorusmeler) - tam
                                pdf.add_metrics([
                                    ("Tamamlanan", str(tam), "#0d9488"),
                                    ("Planlanan", str(plan), "#3b82f6"),
                                    ("Son 30 Gün", str(sel["gorusme_30gun"]), "#6366f1"),
                                ])

                            # 8) AI Önerileri (varsa cache'de)
                            ai_data = st.session_state.get("_ek_ai_ew_analysis", {})
                            if ai_data and not ai_data.get("error"):
                                ogr_ai_list = ai_data.get("ogrenciler", [])
                                match_ai = next((o for o in ogr_ai_list if o.get("ad_soyad") == ad_soyad), None)
                                if match_ai:
                                    pdf.add_section("AI Değerlendirme & Öneriler", "#7c3aed")
                                    pdf.add_text(f"Durum: {match_ai.get('durum_degerlendirme', '')}")
                                    pdf.add_text(f"Acil Müdahale: {match_ai.get('acil_mudahale', '')}")
                                    for ey in match_ai.get("haftalik_eylem", []):
                                        pdf.add_text(f"• {ey}")
                                    pdf.add_spacer(0.3)
                                    pdf.add_text(f"Veli Mesajı: {match_ai.get('veli_mesaji', '')}")

                            pdf_bytes = pdf.generate()
                            st.session_state[pdf_key] = pdf_bytes
                        except Exception as e:
                            st.error(f"PDF oluşturma hatası: {e}")

                # PDF indirme
                if st.session_state.get(pdf_key):
                    tarih_str = datetime.now().strftime("%Y%m%d")
                    st.download_button(
                        "📥 Erken Uyarı PDF Raporunu İndir",
                        data=st.session_state[pdf_key],
                        file_name=f"Erken_Uyari_{sel['ad']}_{sel['soyad']}_{tarih_str}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="ek_ew_pdf_dl",
                    )


# ============================================================
# ANA RENDER FONKSIYONU
# ============================================================

def render_egitim_koclugu():
    """Egitim Koclugu modulu ana giris noktasi - 6 gruplu modern tasarim."""
    _inject_ek_css()

    styled_header(
        "Egitim Koclugu",
        "Butunsel ogrenci koclugu, hedef belirleme, motivasyon takibi ve performans analizi",
        icon="🏅"
    )

    store = get_ek_store()

    try:
        from utils.smarti_helper import render_smarti_welcome, render_smarti_chat
        render_smarti_welcome("egitim_koclugu")
        has_smarti = True
    except ImportError:
        has_smarti = False

    # ==================== 9 ANA GRUP ====================
    grp_names = [
        "  📊 Dashboard  ",
        "  👥 Kocluk Yonetimi  ",
        "  📅 Planlama & Odev  ",
        "  📈 Sinav & Analiz  ",
        "  🧠 AI & Raporlar  ",
        "  ⚙️ Araclar & Ayarlar  ",
        "  🏆 Koc Karnesi  ",
        "  🎯 Net Tahmin  ",
        "  🎮 Gamifiye  ",
        "  🧠 Sinav Kaygisi  ",
        "  🤝 Akran Kocluk  ",
        "  🔄 Kocluk Dongusu  ",
        "  🌐 Ekosistem Endeks  ",
        "  🤖 AI Koc  ",
        "  📖 Bilgi Bankasi  ",
    ]
    if has_smarti:
        grp_names.append("  🤖 Smarti  ")

    grps = st.tabs(grp_names)

    # ── GRUP 1: DASHBOARD ──
    with grps[0]:
        _render_dashboard(store)

    # ── GRUP 2: KOCLUK YONETIMI ──
    with grps[1]:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#4f46e5,#7c3aed);color:white;"
            "padding:10px 16px;border-radius:10px;margin-bottom:12px;font-size:0.85rem;"
            "font-weight:600'>👥 Kocluk Yonetimi — Ogrenci, gorusme, hedef ve motivasyon takibi</div>",
            unsafe_allow_html=True,
        )
        ky_t1, ky_t2, ky_t3, ky_t4 = st.tabs([
            "  👥 Ogrenci Yonetimi  ",
            "  📅 Gorusme Yonetimi  ",
            "  🎯 Hedef Yonetimi  ",
            "  🔥 Motivasyon Takibi  ",
        ])
        with ky_t1:
            _render_ogrenci_yonetimi(store)
        with ky_t2:
            _render_gorusme_yonetimi(store)
        with ky_t3:
            _render_hedef_yonetimi(store)
        with ky_t4:
            _render_motivasyon_takibi(store)

    # ── GRUP 3: PLANLAMA & ODEV ──
    with grps[2]:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#059669,#10b981);color:white;"
            "padding:10px 16px;border-radius:10px;margin-bottom:12px;font-size:0.85rem;"
            "font-weight:600'>📅 Planlama & Odev — Haftalik plan, calisma takvimi, zaman yonetimi ve odev takibi</div>",
            unsafe_allow_html=True,
        )
        pl_t1, pl_t2, pl_t3, pl_t4 = st.tabs([
            "  📋 Haftalik Plan  ",
            "  📆 Calisma Takvimi  ",
            "  ⏰ Zaman Yonetimi  ",
            "  📝 Odev Takibi  ",
        ])
        with pl_t1:
            _render_haftalik_plan(store)
        with pl_t2:
            _render_calisma_takvimi(store)
        with pl_t3:
            _render_zaman_yonetimi(store)
        with pl_t4:
            _render_odev_modulu(store)

    # ── GRUP 4: SINAV & ANALIZ ──
    with grps[3]:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#d97706,#f59e0b);color:white;"
            "padding:10px 16px;border-radius:10px;margin-bottom:12px;font-size:0.85rem;"
            "font-weight:600'>📈 Sinav & Analiz — Deneme analizi, online test, konu analizi ve olcme degerlendirme</div>",
            unsafe_allow_html=True,
        )
        sa_t1, sa_t2, sa_t3, sa_t4, sa_t5, sa_t6 = st.tabs([
            "  📈 Deneme Analizi  ",
            "  📝 Online Test  ",
            "  📊 Konu & Soru Analizi  ",
            "  🔍 Durum Analizi  ",
            "  📋 Olcme Son Durum  ",
            "  🌍 Yabancı Dil  ",
        ])
        with sa_t1:
            _render_deneme_analizi(store)
        with sa_t2:
            _render_online_test(store)
        with sa_t3:
            _render_konu_soru_analizi(store)
        with sa_t4:
            _render_durum_analizi(store)
        with sa_t5:
            _render_olcme_son_durum(store)
        with sa_t6:
            _render_yd_degerlendirme_ek(store)

    # ── GRUP 5: AI & RAPORLAR ──
    with grps[4]:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#7c3aed,#a78bfa);color:white;"
            "padding:10px 16px;border-radius:10px;margin-bottom:12px;font-size:0.85rem;"
            "font-weight:600'>🧠 AI & Raporlar — AI erken uyarı, koçluk analizi ve veli raporları</div>",
            unsafe_allow_html=True,
        )
        ai_t1, ai_t2, ai_t3 = st.tabs([
            "  🚨 AI Erken Uyarı  ",
            "  🧠 AI Kocluk Analizi  ",
            "  👨‍👩‍👧 Veli Raporlari  ",
        ])
        with ai_t1:
            _render_ai_erken_uyari(store)
        with ai_t2:
            _render_ai_analiz(store)
        with ai_t3:
            _render_veli_raporlari(store)

    # ── GRUP 6: ARACLAR & AYARLAR ──
    with grps[5]:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#475569,#64748b);color:white;"
            "padding:10px 16px;border-radius:10px;margin-bottom:12px;font-size:0.85rem;"
            "font-weight:600'>⚙️ Araclar & Ayarlar — Canli ders, soru kutusu ve modul ayarlari</div>",
            unsafe_allow_html=True,
        )
        ay_t1, ay_t2, ay_t3 = st.tabs([
            "  🎥 Canli Ders & Etut  ",
            "  💬 Soru Kutusu  ",
            "  ⚙️ Ayarlar  ",
        ])
        with ay_t1:
            _render_canli_ders(store)
        with ay_t2:
            _render_soru_kutusu(store)
        with ay_t3:
            _render_ayarlar(store)

    # ── GRUP 7: KOÇ KARNESİ ──
    with grps[6]:
        try:
            from views._ek_yeni_ozellikler import render_koc_karnesi
            render_koc_karnesi(store)
        except Exception as _e:
            st.error(f"Koc Karnesi yuklenemedi: {_e}")

    # ── GRUP 8: NET TAHMİN ──
    with grps[7]:
        try:
            from views._ek_yeni_ozellikler import render_net_tahmin
            render_net_tahmin(store)
        except Exception as _e:
            st.error(f"Net Tahmin yuklenemedi: {_e}")

    # ── GRUP 9: GAMİFİYE ──
    with grps[8]:
        try:
            from views._ek_yeni_ozellikler import render_gamifiye_kocluk
            render_gamifiye_kocluk(store)
        except Exception as _e:
            st.error(f"Gamifiye yuklenemedi: {_e}")

    # ── GRUP 10: SINAV KAYGISI ──
    with grps[9]:
        try:
            from views._ek_super_features import render_sinav_kaygisi
            render_sinav_kaygisi(store)
        except Exception as _e:
            st.error(f"Sinav Kaygisi yuklenemedi: {_e}")

    # ── GRUP 11: AKRAN KOÇLUK ──
    with grps[10]:
        try:
            from views._ek_super_features import render_akran_kocluk
            render_akran_kocluk(store)
        except Exception as _e:
            st.error(f"Akran Kocluk yuklenemedi: {_e}")

    # ── GRUP 12: KOÇLUK DÖNGÜSÜ ──
    with grps[11]:
        try:
            from views._ek_super_features import render_kocluk_dongusu
            render_kocluk_dongusu(store)
        except Exception as _e:
            st.error(f"Kocluk Dongusu yuklenemedi: {_e}")

    # ── GRUP 13: EKOSİSTEM ENDEKSİ ──
    with grps[12]:
        try:
            from views._ek_final_features import render_ekosistem_endeksi
            render_ekosistem_endeksi(store)
        except Exception as _e:
            st.error(f"Ekosistem Endeksi yuklenemedi: {_e}")

    # ── GRUP 14: AI DİJİTAL KOÇ ──
    with grps[13]:
        try:
            from views._ek_final_features import render_ai_dijital_koc
            render_ai_dijital_koc(store)
        except Exception as _e:
            st.error(f"AI Koc yuklenemedi: {_e}")

    # ── GRUP 15: BİLGİ BANKASI ──
    with grps[14]:
        try:
            from views._ek_final_features import render_bilgi_bankasi
            render_bilgi_bankasi(store)
        except Exception as _e:
            st.error(f"Bilgi Bankasi yuklenemedi: {_e}")

    # ── SMARTI ──
    if has_smarti and len(grps) > 15:
        with grps[15]:
            render_smarti_chat("egitim_koclugu", {
                "modul": "Egitim Koclugu",
                "ogrenci_sayisi": store.count("ogrenciler"),
                "gorusme_sayisi": store.count("gorusmeler"),
                "hedef_sayisi": store.count("hedefler"),
            })
