"""
Matematik Köyü (Math Village) — Streamlit UI
==============================================
Emsalsiz, bağımsız olimpik matematik modülü: oyunlar, olimpiyat, konu bankası,
bulmacalar, yarışmalar, formül kütüphanesi ve ilerleme takibi.
"""
from __future__ import annotations

import hashlib
import json
import random
import time
import streamlit as st
from datetime import datetime, date, timedelta

from utils.ui_common import inject_common_css, styled_header, styled_section, _render_html
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("steam_merkezi")
except Exception:
    pass
from models.matematik_dunyasi import (
    get_store,
    MatematikDataStore,
    MathProblem,
    OlympiadQuestion,
    GameSession,
    DailyChallenge,
    Competition,
    StudentMathProfile,
    PuzzleRecord,
    MathProblemGenerator,
    SpeedGameEngine,
    NumberPyramidEngine,
    SudokuEngine,
    ProgressTracker,
    LeaderboardManager,
    DailyChallengeManager,
    PuzzleGenerator,
    ZekaEgzersizGenerator,
    EglenceliMatematikGenerator,
    DikkatProfili,
    OlimpiyatSoruGenerator,
    get_gunluk_ipucu,
    MathCategory,
    MathDifficulty,
    GameType,
    OlympiadLevel,
    OlympiadSource,
    SINIF_KONULARI,
    SINIF_OYUN_ONERILERI,
    OYUN_BILGILERI,
    BASARIM_TANIMLARI,
    FORMUL_KATEGORILERI,
    XP_SEVIYELERI,
    UNLU_MATEMATIKÇILER,
    ORNEK_OLIMPIYAT_SORULARI,
    ORNEK_BULMACALAR,
    MATEMATIK_TARIHI,
)


# ══════════════════════════════════════════════════════════════════════════════
# YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════════════════════════════════════

def _mat_css():
    """Matematik Dünyası özel CSS."""
    _render_html("""
    <style>
    /* ═══ MATEMATİK KÖYÜ (MATH VILLAGE) ULTRA PREMIUM CSS ═══ */
    .mat-hero {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 20px; padding: 32px; margin-bottom: 24px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
        position: relative; overflow: hidden;
    }
    .mat-hero::before {
        content: ''; position: absolute; top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(99,102,241,0.05) 0%, transparent 60%);
        animation: mat-pulse 8s ease-in-out infinite;
    }
    @keyframes mat-pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .mat-hero h1 {
        color: #e0e7ff !important; font-size: 2rem !important; margin: 0 !important;
        position: relative; z-index: 1;
    }
    .mat-hero p { color: #a5b4fc !important; position: relative; z-index: 1; margin: 8px 0 0 !important; }

    .mat-stat-card {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border-radius: 16px; padding: 20px; text-align: center;
        border: 1px solid rgba(99, 102, 241, 0.2);
        transition: all 0.3s ease;
    }
    .mat-stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(99,102,241,0.2); }
    .mat-stat-value {
        font-size: 2.2rem; font-weight: 800; color: #818cf8 !important;
        line-height: 1; margin-bottom: 4px;
    }
    .mat-stat-label { font-size: 0.8rem; color: #a5b4fc !important; text-transform: uppercase; letter-spacing: 1px; }
    .mat-stat-icon { font-size: 1.6rem; margin-bottom: 8px; }

    .mat-game-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border-radius: 16px; padding: 20px; cursor: pointer;
        border: 1px solid rgba(99, 102, 241, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: 160px; position: relative; overflow: hidden;
    }
    .mat-game-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.25);
        border-color: rgba(99, 102, 241, 0.5);
    }
    .mat-game-card .game-icon { font-size: 2.5rem; margin-bottom: 8px; }
    .mat-game-card .game-title {
        font-size: 1.1rem; font-weight: 700; color: #e0e7ff !important; margin-bottom: 6px;
    }
    .mat-game-card .game-desc { font-size: 0.8rem; color: #94a3b8 !important; line-height: 1.4; }
    .mat-game-card .game-badge {
        position: absolute; top: 12px; right: 12px;
        background: rgba(99, 102, 241, 0.2); border-radius: 20px;
        padding: 2px 10px; font-size: 0.7rem; color: #818cf8 !important;
    }

    .mat-formula-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 14px; padding: 18px; margin-bottom: 12px;
        border-left: 4px solid #6366f1;
        transition: all 0.2s ease;
    }
    .mat-formula-card:hover { background: linear-gradient(135deg, #1e293b, #334155); }
    .mat-formula-card .formula-name { font-weight: 700; color: #e0e7ff !important; font-size: 0.95rem; }
    .mat-formula-card .formula-expr {
        font-family: 'Cambria Math', 'Times New Roman', serif;
        font-size: 1.2rem; color: #818cf8 !important; margin: 8px 0;
        padding: 10px 14px; background: rgba(99, 102, 241, 0.08);
        border-radius: 8px; text-align: center;
    }
    .mat-formula-card .formula-desc { font-size: 0.8rem; color: #94a3b8 !important; }
    .mat-formula-card .formula-grade {
        font-size: 0.7rem; color: #6366f1 !important;
        background: rgba(99, 102, 241, 0.1); border-radius: 12px;
        padding: 2px 8px; display: inline-block; margin-top: 6px;
    }

    .mat-achievement {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 14px; padding: 14px 18px; margin-bottom: 8px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        display: flex; align-items: center; gap: 14px;
    }
    .mat-achievement.earned { border-color: #eab308; background: linear-gradient(135deg, #1a1a2e, #2d2506); }
    .mat-achievement .ach-icon { font-size: 2rem; }
    .mat-achievement .ach-name { font-weight: 700; color: #e0e7ff !important; font-size: 0.95rem; }
    .mat-achievement .ach-desc { font-size: 0.8rem; color: #94a3b8 !important; }
    .mat-achievement .ach-xp { color: #eab308 !important; font-weight: 700; font-size: 0.85rem; }

    .mat-level-bar {
        background: #1e1b4b; border-radius: 12px; height: 16px;
        overflow: hidden; position: relative;
    }
    .mat-level-fill {
        height: 100%; border-radius: 12px;
        background: linear-gradient(90deg, #4f46e5, #818cf8, #a78bfa);
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .mat-level-fill::after {
        content: ''; position: absolute; top: 0; left: 0;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: mat-shimmer 2s infinite;
    }
    @keyframes mat-shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .mat-leaderboard-row {
        display: flex; align-items: center; gap: 12px;
        padding: 10px 16px; border-radius: 10px; margin-bottom: 6px;
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border: 1px solid rgba(99, 102, 241, 0.1);
    }
    .mat-leaderboard-row.top-3 {
        border-color: #eab308; background: linear-gradient(135deg, #1a1a2e, #2d2506);
    }
    .mat-rank { font-size: 1.2rem; font-weight: 800; color: #818cf8 !important; min-width: 36px; }
    .mat-rank.gold { color: #fbbf24 !important; }
    .mat-rank.silver { color: #94a3b8 !important; }
    .mat-rank.bronze { color: #b45309 !important; }

    .mat-olympiad-card {
        background: linear-gradient(135deg, #1a0a2e, #2d1b69);
        border-radius: 16px; padding: 22px; margin-bottom: 14px;
        border: 1px solid rgba(168, 85, 247, 0.25);
        position: relative;
    }
    .mat-olympiad-card::before {
        content: '🏅'; position: absolute; top: 14px; right: 16px; font-size: 1.5rem; opacity: 0.3;
    }
    .mat-olympiad-source {
        font-size: 0.75rem; color: #c084fc !important;
        background: rgba(168, 85, 247, 0.15); border-radius: 12px;
        padding: 3px 10px; display: inline-block; margin-bottom: 8px;
    }
    .mat-olympiad-title { font-weight: 700; color: #e9d5ff !important; font-size: 1rem; margin-bottom: 8px; }
    .mat-olympiad-body { color: #c4b5fd !important; font-size: 0.9rem; line-height: 1.6; }

    .mat-puzzle-card {
        background: linear-gradient(135deg, #0a1628, #1e3a5f);
        border-radius: 16px; padding: 20px; margin-bottom: 12px;
        border: 1px solid rgba(6, 182, 212, 0.25);
    }
    .mat-puzzle-card .puzzle-type {
        font-size: 0.75rem; color: #22d3ee !important;
        background: rgba(6, 182, 212, 0.15); border-radius: 12px;
        padding: 3px 10px; display: inline-block; margin-bottom: 8px;
    }

    .mat-daily-challenge {
        background: linear-gradient(135deg, #1a0a0a, #3d1c1c);
        border-radius: 20px; padding: 28px; margin-bottom: 20px;
        border: 2px solid rgba(239, 68, 68, 0.3);
        position: relative; overflow: hidden;
    }
    .mat-daily-challenge::before {
        content: '🌟'; position: absolute; top: -10px; right: -10px;
        font-size: 4rem; opacity: 0.1;
    }

    .mat-competition-card {
        background: linear-gradient(135deg, #0c1a0c, #1a3d1a);
        border-radius: 16px; padding: 22px; margin-bottom: 14px;
        border: 1px solid rgba(34, 197, 94, 0.25);
    }

    .mat-game-area {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 20px; padding: 30px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin: 16px 0;
    }
    .mat-game-question {
        font-size: 2.5rem; font-weight: 800; color: #e0e7ff !important;
        text-align: center; margin: 20px 0;
    }
    .mat-game-timer {
        font-size: 1.5rem; font-weight: 700; color: #f59e0b !important;
        text-align: center;
    }
    .mat-game-score {
        font-size: 1.2rem; font-weight: 700; color: #10b981 !important;
        text-align: center;
    }

    .mat-pyramid-cell {
        display: inline-flex; align-items: center; justify-content: center;
        width: 50px; height: 40px; margin: 2px;
        background: #1e293b; border: 2px solid #4f46e5;
        border-radius: 8px; font-weight: 700; color: #e0e7ff !important;
        font-size: 1rem;
    }
    .mat-pyramid-cell.hidden { border-style: dashed; color: #475569 !important; }
    .mat-pyramid-row { text-align: center; margin: 4px 0; }

    .mat-topic-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 14px; padding: 16px; margin-bottom: 10px;
        border: 1px solid rgba(99, 102, 241, 0.15);
        cursor: pointer; transition: all 0.2s ease;
    }
    .mat-topic-card:hover {
        border-color: #6366f1; transform: translateX(4px);
    }

    .mat-streak-fire { animation: mat-fire 0.5s ease-in-out infinite alternate; }
    @keyframes mat-fire {
        from { transform: scale(1); }
        to { transform: scale(1.1); }
    }
    </style>
    """)


def _difficulty_badge(diff: str) -> str:
    colors = {
        "kolay": "#10b981", "orta": "#f59e0b",
        "zor": "#ef4444", "olimpiyat": "#8b5cf6", "uzman": "#ec4899"
    }
    labels = {
        "kolay": "Kolay", "orta": "Orta",
        "zor": "Zor", "olimpiyat": "Olimpiyat", "uzman": "Uzman"
    }
    c = colors.get(diff, "#6366f1")
    l = labels.get(diff, diff)
    return f'<span style="background:{c}22;color:{c};padding:2px 10px;border-radius:12px;font-size:0.75rem;font-weight:600">{l}</span>'


def _xp_badge(xp: int) -> str:
    return f'<span style="color:#eab308;font-weight:700;font-size:0.85rem">⭐ {xp} XP</span>'


def _rank_display(rank: int) -> str:
    if rank == 1:
        return "🥇"
    elif rank == 2:
        return "🥈"
    elif rank == 3:
        return "🥉"
    return f"#{rank}"


# ══════════════════════════════════════════════════════════════════════════════
# ANA RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render_matematik_dunyasi():
    """Ana giriş noktası — app.py'den çağrılır."""
    inject_common_css("mat")
    _mat_css()
    styled_header("Matematik Köyü (Math Village)", "🏘️")
    # XP bar gecici olarak devre disi
    # from utils.gamification_ui import render_xp_bar
    # render_xp_bar()

    store = get_store()

    # -- Tab Gruplama (21 tab -> 3 grup) --
    _GRP_44830 = {
        "📋 Grup A": [("🏠 Köy Meydanı", 0), ("🎮 Oyun Parkı", 1), ("🏆 Olimpiyat Arenası", 2), ("📐 Bilgi Evi", 3), ("🧩 Bulmaca Kulesi", 4), ("🏅 Turnuva Sahası", 5), ("📊 Gelişim Bahçesi", 6)],
        "📊 Grup B": [("📖 Formül Kütüphanesi", 7), ("📚 Matematik Sözlüğü", 8), ("🎨 Eğlenceli Matematik", 9), ("🔮 3D Geometri Lab", 10), ("🔐 Sayıların Sırrı", 11), ("🧠 Zeka Geliştirme", 12), ("🎯 DGS Dikkat Geliştirme", 13)],
        "🔧 Grup C": [("📝 LGS/YKS Soru Bankasi", 14), ("⚡ Carpim Yarisi", 15), ("🍕 Kesir Lab", 16), ("🎬 Adim Adim Cozum", 17), ("🏃 Gunluk Maraton", 18), ("📊 Ogrenci Raporu", 19), ("🤖 Smarti", 20)],
    }
    _sg_44830 = st.radio("", list(_GRP_44830.keys()), horizontal=True, label_visibility="collapsed", key="rg_44830")
    _gt_44830 = _GRP_44830[_sg_44830]
    _aktif_idx_44830 = set(t[1] for t in _gt_44830)
    _tab_names_44830 = [t[0] for t in _gt_44830]
    tabs = st.tabs(_tab_names_44830)
    _tab_real_44830 = {idx: t for idx, t in zip((t[1] for t in _gt_44830), tabs)}

    if 0 in _aktif_idx_44830:
      with _tab_real_44830[0]:
        _render_dashboard(store)
    if 1 in _aktif_idx_44830:
      with _tab_real_44830[1]:
        _render_oyunlar(store)
    if 2 in _aktif_idx_44830:
      with _tab_real_44830[2]:
        _render_olimpiyat(store)
    if 3 in _aktif_idx_44830:
      with _tab_real_44830[3]:
        _render_konu_bankasi(store)
    if 4 in _aktif_idx_44830:
      with _tab_real_44830[4]:
        _render_bulmacalar(store)
    if 5 in _aktif_idx_44830:
      with _tab_real_44830[5]:
        _render_yarisma(store)
    if 6 in _aktif_idx_44830:
      with _tab_real_44830[6]:
        _render_ilerleme(store)
    if 7 in _aktif_idx_44830:
      with _tab_real_44830[7]:
        _render_formuller(store)
    if 8 in _aktif_idx_44830:
      with _tab_real_44830[8]:
        _render_matematik_sozlugu()
    if 9 in _aktif_idx_44830:
      with _tab_real_44830[9]:
        _render_eglenceli_matematik(store)
    if 10 in _aktif_idx_44830:
      with _tab_real_44830[10]:
        _render_3d_geometri_lab(store)
    if 11 in _aktif_idx_44830:
      with _tab_real_44830[11]:
        _render_sayilarin_sirri()
    if 12 in _aktif_idx_44830:
      with _tab_real_44830[12]:
        _render_zeka_gelistirme(store)
    if 13 in _aktif_idx_44830:
      with _tab_real_44830[13]:
        _render_dgs_dikkat(store)
    if 14 in _aktif_idx_44830:
      with _tab_real_44830[14]:
        _render_lgs_yks_soru_bankasi()
    if 15 in _aktif_idx_44830:
      with _tab_real_44830[15]:
        _render_carpim_yarisi()
    if 16 in _aktif_idx_44830:
      with _tab_real_44830[16]:
        _render_kesir_lab()
    if 17 in _aktif_idx_44830:
      with _tab_real_44830[17]:
        _render_adim_adim_cozum()
    if 18 in _aktif_idx_44830:
      with _tab_real_44830[18]:
        _render_gunluk_maraton()
    if 19 in _aktif_idx_44830:
      with _tab_real_44830[19]:
        from views.modul_rapor_ui import render_ogretmen_rapor
        render_ogretmen_rapor(modul_filter="matematik", key_prefix="mr_mat")

    if 20 in _aktif_idx_44830:
      with _tab_real_44830[20]:
        try:
            from views.ai_destek import render_smarti_chat
            render_smarti_chat(modul="matematik_dunyasi")
        except Exception:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
                'padding:20px;border-radius:12px;text-align:center;margin:20px 0">'
                '<h3 style="margin:0">🤖 Smarti AI</h3>'
                '<p style="margin:8px 0 0;opacity:.85">Smarti AI asistanı bu modülde aktif. '
                'Sorularınızı yazın, AI destekli yanıtlar alın.</p></div>',
                unsafe_allow_html=True)
            user_q = st.text_area("Smarti'ye sorunuzu yazın:", key="smarti_q_matematik_dunyasi")
            if st.button("Gönder", key="smarti_send_matematik_dunyasi"):
                if user_q.strip():
                    try:
                        from openai import OpenAI
                        import os
                        api_key = os.environ.get("OPENAI_API_KEY", "")
                        if api_key:
                            client = OpenAI(api_key=api_key)
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen SmartCampus AI'nin Smarti asistanısın. matematik_dunyasi modülü hakkında Türkçe yardım et."},
                                    {"role": "user", "content": user_q}
                                ],
                                temperature=0.7, max_tokens=500)
                            st.markdown(resp.choices[0].message.content)
                        else:
                            st.warning("API anahtarı tanımlı değil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 1) DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def _render_dashboard(store: MatematikDataStore):
    """Ana panel — istatistikler, günlük meydan okuma, liderlik."""

    # Hero banner
    _render_html("""
    <div class="mat-hero">
        <h1>🏘️ Matematik Köyü'ne Hoş Geldiniz! <span style="font-size:0.6em;opacity:0.7">(Math Village)</span></h1>
        <p>Olimpik düzeyde eğitim, interaktif oyunlar, dünya çapında yarışma soruları — matematiğin kalbi burada atıyor!</p>
    </div>
    """)

    # Günlük İpucu
    ipucu = get_gunluk_ipucu()
    tip_renk = {"bilgi": "#3b82f6", "formul": "#10b981", "numara": "#f59e0b"}.get(ipucu.get("tip", ""), "#6366f1")
    _render_html(f"""
    <div style="background:linear-gradient(135deg,{tip_renk}15,{tip_renk}08);border-radius:16px;padding:16px 20px;
                 margin-bottom:16px;border:1px solid {tip_renk}30;display:flex;align-items:center;gap:16px">
        <div style="font-size:2.2rem;min-width:40px">{ipucu.get('ikon','💡')}</div>
        <div>
            <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem;margin-bottom:2px">
                💡 Günün Matematik İpucu — {ipucu.get('baslik','')}
            </div>
            <div style="color:#94a3b8 !important;font-size:0.83rem;line-height:1.5">{ipucu.get('icerik','')}</div>
        </div>
    </div>
    """)

    stats = store.get_dashboard_stats()

    # İstatistik kartları
    cols = st.columns(6)
    stat_items = [
        ("📚", str(stats["total_problems"]), "Problem"),
        ("🏆", str(stats["total_olympiad"]), "Olimpiyat"),
        ("🎮", str(stats["total_games"]), "Oyun"),
        ("🧩", str(stats["total_puzzles"]), "Bulmaca"),
        ("👥", str(stats["total_profiles"]), "Öğrenci"),
        ("🎯", f"%{stats['overall_accuracy']:.0f}", "Doğruluk"),
    ]
    for col, (icon, val, label) in zip(cols, stat_items):
        with col:
            _render_html(f"""
            <div class="mat-stat-card">
                <div class="mat-stat-icon">{icon}</div>
                <div class="mat-stat-value">{val}</div>
                <div class="mat-stat-label">{label}</div>
            </div>
            """)

    st.markdown("---")

    # Günlük Meydan Okuma
    col1, col2 = st.columns([3, 2])
    with col1:
        styled_section("🌟 Günün Sorusu", "#ef4444")

        grade_sel = st.selectbox("Sınıf seç", list(SINIF_KONULARI.keys()),
                                 key="mat_dash_grade", index=4)

        dcm = DailyChallengeManager(store)
        challenge = dcm.get_or_create_today(grade_sel)

        if challenge:
            _render_html(f"""
            <div class="mat-daily-challenge">
                <div style="font-weight:700;color:#fca5a5 !important;font-size:1.1rem;margin-bottom:12px;position:relative;z-index:1">
                    {challenge.get('title', 'Günün Sorusu')}
                </div>
                <div style="color:#e0e7ff !important;font-size:1rem;line-height:1.6;position:relative;z-index:1">
                    {challenge.get('body', '')}
                </div>
                <div style="margin-top:12px;position:relative;z-index:1">
                    {_xp_badge(challenge.get('xp_reward', 25))}
                    {_difficulty_badge(challenge.get('difficulty', 'orta'))}
                </div>
            </div>
            """)

            with st.expander("💡 Cevabını Kontrol Et"):
                user_answer = st.text_input("Cevabın:", key="mat_daily_answer")
                if st.button("Kontrol Et", key="mat_daily_check"):
                    correct_ans = str(challenge.get("answer", "")).strip()
                    if user_answer.strip() == correct_ans:
                        st.success("🎉 Tebrikler! Doğru cevap!")
                        st.balloons()
                    else:
                        st.error(f"❌ Yanlış! Doğru cevap: **{correct_ans}**")
        else:
            st.info("Bugün için meydan okuma oluşturulamadı.")

    with col2:
        styled_section("🏆 Liderlik Tablosu", "#eab308")
        lb = LeaderboardManager(store)
        leaders = lb.get_leaderboard(limit=5)
        if leaders:
            for entry in leaders:
                rank_icon = _rank_display(entry["rank"])
                _render_html(f"""
                <div class="mat-leaderboard-row {'top-3' if entry['rank'] <= 3 else ''}">
                    <div class="mat-rank {'gold' if entry['rank']==1 else 'silver' if entry['rank']==2 else 'bronze' if entry['rank']==3 else ''}">{rank_icon}</div>
                    <div style="flex:1">
                        <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{entry['student_name'] or 'Öğrenci'}</div>
                        <div style="font-size:0.75rem;color:#94a3b8 !important">{entry['grade']}. sınıf • Seviye {entry['level']}</div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-weight:700;color:#eab308 !important;font-size:0.9rem">{entry['xp']} XP</div>
                        <div style="font-size:0.7rem;color:#94a3b8 !important">{entry['solved']} çözüm</div>
                    </div>
                </div>
                """)
        else:
            st.info("Henüz liderlik tablosu verisi yok. İlk çözen sen ol!")

    # Haftalık yıldızlar
    styled_section("⭐ Bu Haftanın Yıldızları", "#f59e0b")
    stars = lb.get_weekly_stars(limit=5)
    if stars:
        cols = st.columns(min(len(stars), 5))
        for col, s in zip(cols, stars):
            with col:
                _render_html(f"""
                <div class="mat-stat-card" style="border-color:rgba(234,179,8,0.3)">
                    <div class="mat-stat-icon">⭐</div>
                    <div style="font-weight:700;color:#e0e7ff !important">{s['student_name']}</div>
                    <div style="color:#eab308 !important;font-weight:700">{s['weekly_xp']} XP</div>
                    <div style="font-size:0.75rem;color:#94a3b8 !important">{s['weekly_solved']} çözüm</div>
                </div>
                """)
    else:
        st.info("Bu hafta henüz aktif öğrenci yok.")

    # ── Matematikçiler Sokağı ──
    st.markdown("---")
    styled_section("🏛️ Matematikçiler Sokağı — Portre Galerisi", "#8b5cf6")
    st.caption("Matematik Köyü'nün sokakları ünlü matematikçilerin adını taşır! Kartlara tıklayarak detaylı biyografileri oku.")

    # 4'lü grid, rastgele 4 matematikçi göster (portreli)
    import random as _rnd
    showcased = _rnd.sample(UNLU_MATEMATIKÇILER, min(4, len(UNLU_MATEMATIKÇILER)))
    cols = st.columns(4)
    for col, m in zip(cols, showcased):
        img_html = f'<img src="{m["portre_url"]}" style="width:70px;height:70px;border-radius:50%;object-fit:cover;border:3px solid #6366f1;margin-bottom:8px" onerror="this.style.display=\'none\'">' if m.get("portre_url") else f'<div style="font-size:2.5rem;margin-bottom:8px">{m["ikon"]}</div>'
        with col:
            _render_html(f"""
            <div class="mat-stat-card" style="text-align:center;padding:16px;min-height:240px;border-color:rgba(139,92,246,0.3)">
                {img_html}
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{m['ad']}</div>
                <div style="font-size:0.68rem;color:#a5b4fc !important;margin-bottom:2px">{m['yaşam']} • {m.get('ulke','')}</div>
                <div style="font-size:0.7rem;color:#c084fc !important;margin-bottom:6px">{m['unvan']}</div>
                <div style="font-size:0.7rem;color:#94a3b8 !important;line-height:1.3;font-style:italic">"{m['sozu'][:70]}{'...' if len(m['sozu'])>70 else ''}"</div>
            </div>
            """)

    # Her matematikçi için detaylı biyografi paneli
    with st.expander("📜 Tüm Matematikçilerin Portreleri & Hayat Hikayeleri", expanded=False):
        for idx, m in enumerate(UNLU_MATEMATIKÇILER):
            # Portre kartı — büyük detaylı versiyon
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#1a0a2e,#2d1b69);border-radius:20px;padding:28px;margin-bottom:20px;
                         border:1px solid rgba(168,85,247,0.3);position:relative;overflow:hidden">
                <!-- Dekoratif arka plan ikonu -->
                <div style="position:absolute;top:-20px;right:-20px;font-size:8rem;opacity:0.05;z-index:0">{m['ikon']}</div>

                <!-- Üst kısım: Portre bilgileri -->
                <div style="display:flex;gap:24px;position:relative;z-index:1;margin-bottom:20px">
                    <!-- Sol: Portre resmi -->
                    <div style="min-width:120px;text-align:center">
                        {'<img src="' + m.get("portre_url","") + '" style="width:100px;height:100px;border-radius:50%;object-fit:cover;border:3px solid #8b5cf6;margin-bottom:8px" onerror="this.outerHTML=\'<div style=font-size:4rem>' + m["ikon"] + '</div>\'">' if m.get("portre_url") else '<div style="font-size:4rem;margin-bottom:8px;background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:50%;width:100px;height:100px;display:flex;align-items:center;justify-content:center;margin:0 auto">' + m["ikon"] + '</div>'}
                        <div style="font-size:0.7rem;color:#c084fc !important;
                                     background:rgba(168,85,247,0.15);border-radius:12px;
                                     padding:3px 10px;display:inline-block;margin-top:4px">{m.get('ulke','')}</div>
                    </div>
                    <!-- Sağ: İsim, unvan, portre açıklaması -->
                    <div style="flex:1">
                        <div style="font-size:1.3rem;font-weight:800;color:#e9d5ff !important;margin-bottom:4px">{m['ad']}</div>
                        <div style="font-size:0.85rem;color:#c084fc !important;margin-bottom:4px">{m['unvan']} • {m['yaşam']}</div>
                        <div style="font-size:0.8rem;color:#94a3b8 !important;margin-bottom:8px"><b>Alanlar:</b> {m['alan']}</div>
                        <div style="font-size:0.8rem;color:#a5b4fc !important;font-style:italic;line-height:1.5;
                                     background:rgba(99,102,241,0.08);border-radius:10px;padding:10px 14px;
                                     border-left:3px solid #6366f1">
                            🖼️ <b>Portre:</b> {m.get('portre','')}
                        </div>
                    </div>
                </div>

                <!-- Ünlü sözü -->
                <div style="background:rgba(234,179,8,0.08);border-radius:12px;padding:14px 18px;margin-bottom:16px;
                             border-left:3px solid #eab308;position:relative;z-index:1">
                    <div style="font-size:0.85rem;color:#fde68a !important;font-style:italic;line-height:1.5">
                        💬 "{m['sozu']}"
                    </div>
                </div>

                <!-- Teorem -->
                <div style="background:rgba(99,102,241,0.1);border-radius:12px;padding:12px 18px;margin-bottom:16px;
                             position:relative;z-index:1;text-align:center">
                    <div style="font-size:0.75rem;color:#94a3b8 !important;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">En Ünlü Teoremi</div>
                    <div style="font-size:1rem;font-weight:700;color:#818cf8 !important;
                                 font-family:'Cambria Math','Times New Roman',serif">{m.get('teorem','')}</div>
                </div>
            </div>
            """)

            # Biyografi (Streamlit markdown ile — daha okunabilir)
            st.markdown(f"#### 📖 {m['ad']} — Hayat Hikayesi")
            st.markdown(m.get("biyografi", ""))

            # İlginç bilgi
            if m.get("ilginc_bilgi"):
                st.info(f"💡 **İlginç Bilgi:** {m['ilginc_bilgi']}")

            st.markdown("---")

    # ── Matematik Tarihi Yolculuğu ──
    styled_section("📜 Matematik Tarihi Yolculuğu", "#f59e0b")
    for i, donem in enumerate(MATEMATIK_TARIHI):
        _render_html(f"""
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:8px;padding:12px 18px;
                     background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:12px;
                     border-left:4px solid {'#eab308' if i%2==0 else '#6366f1'}">
            <div style="font-size:2rem;min-width:40px;text-align:center">{donem['ikon']}</div>
            <div>
                <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{donem['donem']} <span style="color:#94a3b8 !important;font-weight:400;font-size:0.8rem">({donem['yil']})</span></div>
                <div style="font-size:0.8rem;color:#94a3b8 !important">{donem['olay']}</div>
            </div>
        </div>
        """)


    # ── Haftalık Çalışma Takvimi ──
    st.markdown("---")
    styled_section("📅 Bu Hafta Ne Çalışmalıyım?", "#06b6d4")
    from datetime import datetime
    gun_adi = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"]
    gunluk_plan = [
        ("🔢 Aritmetik + 🎮 Hızlı Hesap", "15 dk"),
        ("📐 Geometri + 🔮 3D Lab", "15 dk"),
        ("🧩 Bulmaca + 🧠 Zeka Egzersizi", "15 dk"),
        ("🏆 Olimpiyat Soruları", "20 dk"),
        ("🎯 DGS Dikkat Egzersizi", "15 dk"),
        ("🎨 Eğlenceli Matematik + 🎮 Oyunlar", "20 dk"),
        ("📊 İlerleme Kontrolü + 📖 Formül Tekrar", "10 dk"),
    ]
    bugun = datetime.now().weekday()
    cols = st.columns(7)
    for i, col in enumerate(cols):
        with col:
            aktif = i == bugun
            plan, sure = gunluk_plan[i]
            _render_html(f"""
            <div style="background:{'linear-gradient(135deg,#1e0a3a,#4c1d95)' if aktif else '#0f172a'};
                         border-radius:12px;padding:10px 8px;text-align:center;min-height:120px;
                         border:{'2px solid #8b5cf6' if aktif else '1px solid rgba(99,102,241,0.1)'};
                         {'box-shadow:0 0 12px rgba(139,92,246,0.2)' if aktif else ''}">
                <div style="font-weight:{'800' if aktif else '600'};color:{'#e9d5ff' if aktif else '#64748b'} !important;font-size:0.7rem;margin-bottom:4px">
                    {'📌 ' if aktif else ''}{gun_adi[i][:3]}
                </div>
                <div style="font-size:0.65rem;color:{'#c4b5fd' if aktif else '#475569'} !important;line-height:1.4">{plan}</div>
                <div style="font-size:0.6rem;color:{'#a78bfa' if aktif else '#374151'} !important;margin-top:4px">⏱️ {sure}</div>
            </div>
            """)

    # ── AI Matematik Koçu ──
    st.markdown("---")
    styled_section("🤖 AI Matematik Koçu", "#ec4899")
    _render_html("""
    <div style="background:linear-gradient(135deg,#831843,#be185d);border-radius:16px;padding:18px;
                 border:2px solid rgba(236,72,153,0.4);display:flex;align-items:center;gap:16px">
        <div style="font-size:2.5rem" class="mat-grow">🤖</div>
        <div>
            <div style="font-weight:700;color:#e0e7ff !important;font-size:0.95rem">Matematik hakkında her şeyi sor!</div>
            <div style="color:#fce7f3 !important;font-size:0.8rem">Formül, kavram, çözüm yolu — AI Koç sana yardım etmeye hazır.</div>
        </div>
    </div>
    """)
    koç_soru = st.text_input("🤖 Matematik sorunuzu yazın:", key="mat_koc_soru",
                              placeholder="Ör: Pisagor teoremi nedir? 2. derece denklem nasıl çözülür?")
    if koç_soru:
        # Basit anahtar kelime bazlı cevaplama (AI API olmadan)
        soru_lower = koç_soru.lower()
        cevap = None
        if any(k in soru_lower for k in ["pisagor", "pythagoras", "hipotenüs"]):
            cevap = "**Pisagor Teoremi:** Dik üçgende a² + b² = c² (c = hipotenüs). Örnek: 3² + 4² = 9 + 16 = 25 = 5². Kenarlar 3, 4, 5."
        elif any(k in soru_lower for k in ["2. derece", "ikinci derece", "diskriminant", "delta"]):
            cevap = "**2. Derece Denklem:** ax²+bx+c=0 → x = (-b ± √Δ) / 2a, Δ = b²-4ac. Δ>0: 2 kök, Δ=0: 1 kök, Δ<0: kök yok."
        elif any(k in soru_lower for k in ["alan", "dikdörtgen", "kare alan"]):
            cevap = "**Alan Formülleri:** Kare=a², Dikdörtgen=a×b, Üçgen=½×t×h, Daire=πr², Paralelkenar=t×h, Yamuk=½(a+c)×h"
        elif any(k in soru_lower for k in ["türev", "derivat"]):
            cevap = "**Türev:** f'(x) = lim[Δx→0] (f(x+Δx)-f(x))/Δx. Kurallar: (xⁿ)'=nxⁿ⁻¹, (sinx)'=cosx, (eˣ)'=eˣ, (lnx)'=1/x"
        elif any(k in soru_lower for k in ["integral"]):
            cevap = "**İntegral:** Türevin tersi. ∫xⁿdx = xⁿ⁺¹/(n+1)+C. ∫sinx dx=-cosx+C. Belirli: ∫[a,b]f(x)dx = F(b)-F(a)"
        elif any(k in soru_lower for k in ["olasılık", "olasilik"]):
            cevap = "**Olasılık:** P(A) = n(A)/n(S). Tümleyen: P(A')=1-P(A). Birleşim: P(A∪B)=P(A)+P(B)-P(A∩B)"
        elif any(k in soru_lower for k in ["fibonacci"]):
            cevap = "**Fibonacci:** 1,1,2,3,5,8,13,21,34,55... Her terim önceki ikisinin toplamı. Doğada her yerde: ayçiçeği, deniz kabuğu, çam kozalağı."
        elif any(k in soru_lower for k in ["pi", "π", "daire"]):
            cevap = "**π (Pi):** ≈ 3.14159... Daire çevresi=2πr, alanı=πr². Sonsuz ve tekrarsız. 14 Mart = Pi Günü!"
        elif any(k in soru_lower for k in ["logaritma", "log"]):
            cevap = "**Logaritma:** logₐb=c demek aᶜ=b demek. Kurallar: log(ab)=loga+logb, log(a/b)=loga-logb, log(aⁿ)=n·loga"
        elif any(k in soru_lower for k in ["kombinasyon", "permütasyon", "permutasyon"]):
            cevap = "**Permütasyon (sıralı):** P(n,r)=n!/(n-r)!. **Kombinasyon (sırasız):** C(n,r)=n!/(r!(n-r)!). Ör: C(5,2)=10"
        else:
            cevap = f"🤖 Bu konuda **Formül Kütüphanesi** veya **Matematik Sözlüğü** sekmelerinde detaylı bilgi bulabilirsin! Ayrıca **Sayıların Sırrı** sekmesi de ilginç bilgilerle dolu."

        _render_html(f"""
        <div style="background:#0f172a;border-radius:14px;padding:16px;margin-top:8px;
                     border-left:4px solid #ec4899;border:1px solid rgba(236,72,153,0.15)">
            <div style="font-size:0.85rem;color:#e0e7ff !important;line-height:1.6">{cevap}</div>
        </div>
        """)


# ══════════════════════════════════════════════════════════════════════════════
# 2) OYUNLAR
# ══════════════════════════════════════════════════════════════════════════════

def _render_oyunlar(store: MatematikDataStore):
    """Matematik oyunları."""
    styled_section("🎮 Matematik Oyunları", "#6366f1")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:16px;padding:20px;margin-bottom:20px;border:1px solid rgba(99,102,241,0.3)">
        <div style="font-weight:700;color:#e0e7ff !important;font-size:1.1rem;margin-bottom:6px">🕹️ Oyna, Öğren, Eğlen!</div>
        <div style="color:#a5b4fc !important;font-size:0.9rem">14 farklı matematik oyunu ile becerilerini geliştir. Her sınıf düzeyi için özel oyunlar!</div>
    </div>
    """)

    grade_filter = st.selectbox("Sınıf Düzeyi", ["Tümü"] + list(SINIF_KONULARI.keys()),
                                key="mat_game_grade")

    sub_tabs = st.tabs([
        "🎯 Oyun Seç", "⚡ Hızlı Hesap", "🔺 Sayı Piramidi", "🧩 Sudoku",
        "⚔️ Çarpım Savaşı", "🎯 Tahmin Oyunu", "🃏 Hafıza Kartları",
        "🍕 Kesir Pizzası", "⚖️ Denklem Dengesi", "🔢 Sayı Bulmaca",
        "📐 Geometri", "💡 Açık Uçlu",
    ])

    with sub_tabs[0]:
        _render_oyun_sec(store, grade_filter)
    with sub_tabs[1]:
        _render_hizli_hesap(store)
    with sub_tabs[2]:
        _render_sayi_piramidi(store)
    with sub_tabs[3]:
        _render_sudoku(store)
    with sub_tabs[4]:
        _render_carpim_savasi(store)
    with sub_tabs[5]:
        _render_tahmin_oyunu(store)
    with sub_tabs[6]:
        _render_hafiza_kartlari(store)
    with sub_tabs[7]:
        _render_kesir_pizzasi(store)
    with sub_tabs[8]:
        _render_denklem_dengesi(store)
    with sub_tabs[9]:
        _render_sayi_bulmaca(store)
    with sub_tabs[10]:
        _render_geometri_macerasi(store)
    with sub_tabs[11]:
        _render_acik_uclu(store)


def _render_oyun_sec(store: MatematikDataStore, grade_filter: str):
    """Oyun seçim ekranı."""
    games = OYUN_BILGILERI.items()

    if grade_filter != "Tümü":
        g = int(grade_filter) if grade_filter.isdigit() else 5
        games = [(k, v) for k, v in games if v["min_sinif"] <= g <= v["max_sinif"]]
    else:
        games = list(games)

    # 3 sütunlu grid — tıklanabilir oyun kartları
    for i in range(0, len(games), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(games):
                key, info = games[i + j]
                with col:
                    _render_html(f"""
                    <div class="mat-game-card">
                        <div class="game-badge">Sınıf {info['min_sinif']}-{info['max_sinif']}</div>
                        <div class="game-icon">{info['ikon']}</div>
                        <div class="game-title">{info['ad'].split(' ', 1)[1] if ' ' in info['ad'] else info['ad']}</div>
                        <div class="game-desc">{info['aciklama']}</div>
                    </div>
                    """)
                    if st.button(f"▶️ {info['ad']}", key=f"play_{key}", use_container_width=True):
                        st.session_state["mat_aktif_oyun"] = key
                        st.rerun()

    # Seçilen oyun açılsın
    if "mat_aktif_oyun" in st.session_state:
        aktif = st.session_state["mat_aktif_oyun"]
        info = OYUN_BILGILERI.get(aktif, {})
        st.markdown("---")
        styled_section(f"{info.get('ad', aktif)} — Oyna!", info.get("renk", "#6366f1"))

        # Oyun türüne göre yönlendir
        if aktif == "hizli_hesap":
            st.info("⬆️ **Hızlı Hesap** sekmesine geç!")
        elif aktif == "sayi_piramidi":
            st.info("⬆️ **Sayı Piramidi** sekmesine geç!")
        elif aktif == "sudoku":
            st.info("⬆️ **Sudoku** sekmesine geç!")
        elif aktif == "carpim_savaslari":
            st.info("⬆️ **Çarpım Savaşı** sekmesine geç!")
        elif aktif == "tahmin_oyunu":
            st.info("⬆️ **Tahmin Oyunu** sekmesine geç!")
        elif aktif == "hafiza_kartlari":
            st.info("⬆️ **Hafıza Kartları** sekmesine geç!")
        else:
            # Diğer oyunlar için mini oyun alanı
            _render_mini_oyun(aktif, store)

    # Sınıf bazlı öneri
    if grade_filter != "Tümü" and grade_filter in SINIF_OYUN_ONERILERI:
        st.markdown("---")
        styled_section(f"⭐ {grade_filter}. Sınıf İçin Önerilen Oyunlar", "#f59e0b")
        recommended = SINIF_OYUN_ONERILERI[grade_filter]
        cols = st.columns(min(len(recommended), 5))
        for col, game_key in zip(cols, recommended):
            info = OYUN_BILGILERI.get(game_key, {})
            if info:
                with col:
                    _render_html(f"""
                    <div class="mat-stat-card" style="border-color:{info['renk']}33">
                        <div style="font-size:2rem">{info['ikon']}</div>
                        <div style="font-weight:600;color:#e0e7ff !important;font-size:0.85rem">{info['ad'].split(' ',1)[1] if ' ' in info['ad'] else info['ad']}</div>
                    </div>
                    """)


def _render_hizli_hesap(store: MatematikDataStore):
    """Hızlı hesap oyunu — süre limiti + doğru/yanlış takibi."""
    styled_section("⚡ Hızlı Hesap", "#f59e0b")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        grade = st.selectbox("Sınıf", list(SINIF_KONULARI.keys()), key="mat_hh_grade", index=2)
    with col2:
        diff = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="mat_hh_diff", index=1)
    with col3:
        q_count = st.selectbox("Soru Sayısı", [5, 10, 15, 20], key="mat_hh_count", index=1)
    with col4:
        sure_limit = st.selectbox("Süre Limiti", [30, 60, 90, 120, 180, 0], key="mat_hh_sure",
                                   format_func=lambda x: f"{x} sn" if x > 0 else "Sınırsız", index=2)

    state_key = "mat_hh_state"
    # Eski state uyumluluğu — eksik anahtarları tamamla
    _defaults = {"active": False, "questions": [], "current": 0, "score": 0,
                 "correct": 0, "wrong": 0, "start_time": None, "sure_limit": 0, "son_cevap": None}
    if state_key not in st.session_state:
        st.session_state[state_key] = dict(_defaults)
    else:
        for k, v in _defaults.items():
            if k not in st.session_state[state_key]:
                st.session_state[state_key][k] = v

    state = st.session_state[state_key]

    if not state.get("active", False):
        if st.button("🚀 Oyunu Başlat!", key="mat_hh_start", type="primary"):
            engine = SpeedGameEngine(grade, diff)
            questions = [engine.generate_question() for _ in range(q_count)]
            st.session_state[state_key] = {
                "active": True, "questions": questions, "current": 0,
                "score": 0, "correct": 0, "wrong": 0, "start_time": time.time(),
                "sure_limit": sure_limit, "son_cevap": None,
            }
            st.rerun()
    else:
        # Süre kontrolü
        elapsed = round(time.time() - state.get("start_time", time.time()), 1) if state.get("start_time") else 0
        sl = state.get("sure_limit", 0)
        sure_bitti = sl > 0 and elapsed >= sl
        cur = state.get("current", 0)
        questions = state.get("questions", [])

        if cur < len(questions) and not sure_bitti:
            q = questions[cur]
            progress = cur / len(questions) if questions else 0
            kalan = max(0, sl - elapsed) if sl > 0 else None

            # Son cevap geri bildirimi
            sc = state.get("son_cevap")
            if sc == "dogru":
                _render_html('<div style="text-align:center;color:#10b981 !important;font-weight:700;font-size:1.1rem;margin-bottom:8px">✅ Doğru!</div>')
            elif sc == "yanlis":
                _render_html(f'<div style="text-align:center;color:#ef4444 !important;font-weight:700;font-size:1.1rem;margin-bottom:8px">❌ Yanlış! Doğrusu: {state.get("son_dogru","")}</div>')

            _render_html(f"""
            <div class="mat-game-area">
                <div style="display:flex;justify-content:space-between;margin-bottom:16px">
                    <div class="mat-game-score">✅ {state.get('correct',0)} ❌ {state.get('wrong',0)}</div>
                    <div style="color:#94a3b8 !important">Soru {cur+1}/{len(questions)}</div>
                    {f'<div style="color:{"#ef4444" if kalan and kalan<15 else "#f59e0b"} !important;font-weight:700;font-size:1.2rem">⏱️ {kalan:.0f}s</div>' if kalan is not None else ''}
                </div>
                <div class="mat-game-question">{q['question']}</div>
            </div>
            """)

            st.progress(progress)

            cols = st.columns(4)
            for idx, opt in enumerate(q["options"]):
                with cols[idx]:
                    if st.button(str(opt), key=f"mat_hh_opt_{cur}_{idx}",
                                 use_container_width=True):
                        if opt == q["answer"]:
                            state["correct"] = state.get("correct", 0) + 1
                            state["score"] = state.get("score", 0) + {"kolay": 5, "orta": 10, "zor": 20}.get(diff, 10)
                            state["son_cevap"] = "dogru"
                        else:
                            state["wrong"] = state.get("wrong", 0) + 1
                            state["son_cevap"] = "yanlis"
                            state["son_dogru"] = str(q["answer"])
                        state["current"] = cur + 1
                        st.rerun()
        else:
            # Oyun bitti (sorular tükendi veya süre doldu)
            elapsed = round(time.time() - state.get("start_time", time.time()), 1) if state.get("start_time") else 0
            total_answered = state.get("correct", 0) + state.get("wrong", 0)
            accuracy = (state.get("correct", 0) / total_answered * 100) if total_answered > 0 else 0

            bitis_neden = "⏱️ Süre Doldu!" if sure_bitti else "🏁 Tüm Sorular Bitti!"

            _render_html(f"""
            <div class="mat-game-area" style="text-align:center">
                <div style="font-size:1rem;color:#94a3b8 !important;margin-bottom:8px">{bitis_neden}</div>
                <div style="font-size:3rem;margin-bottom:12px">{'🏆' if accuracy >= 80 else '👏' if accuracy >= 60 else '💪'}</div>
                <div style="font-size:1.5rem;font-weight:800;color:#e0e7ff !important;margin-bottom:16px">Oyun Bitti!</div>
                <div style="display:flex;justify-content:center;gap:30px;flex-wrap:wrap">
                    <div><div class="mat-stat-value" style="color:#10b981 !important">{state.get('correct',0)}</div><div class="mat-stat-label">Doğru</div></div>
                    <div><div class="mat-stat-value" style="color:#ef4444 !important">{state.get('wrong',0)}</div><div class="mat-stat-label">Yanlış</div></div>
                    <div><div class="mat-stat-value" style="color:#f59e0b !important">%{accuracy:.0f}</div><div class="mat-stat-label">Başarı</div></div>
                    <div><div class="mat-stat-value" style="color:#6366f1 !important">{elapsed}s</div><div class="mat-stat-label">Süre</div></div>
                    <div><div class="mat-stat-value" style="color:#eab308 !important">{state.get('score',0)}</div><div class="mat-stat-label">XP</div></div>
                </div>
            </div>
            """)

            # Sonucu kaydet
            session = GameSession(
                game_type="hizli_hesap",
                grade=grade,
                difficulty=diff,
                score=state.get("score", 0),
                correct_answers=state.get("correct", 0),
                total_questions=len(state.get("questions", [])),
                time_spent_sec=int(elapsed),
                xp_earned=state.get("score", 0),
            )
            store.add_game_session(session)

            if st.button("🔄 Tekrar Oyna", key="mat_hh_restart"):
                del st.session_state[state_key]
                st.rerun()


def _render_sayi_piramidi(store: MatematikDataStore):
    """Sayı piramidi oyunu."""
    styled_section("🔺 Sayı Piramidi", "#a855f7")

    st.info("Alt satırdaki sayıları kullanarak piramidi tamamla! Yan yana iki sayının toplamı üstlerindeki sayıyı verir.")

    col1, col2 = st.columns(2)
    with col1:
        rows = st.selectbox("Satır Sayısı", [3, 4, 5], key="mat_pyr_rows", index=1)
    with col2:
        max_base = st.selectbox("Maks Taban Değeri", [10, 20, 50], key="mat_pyr_max", index=0)

    pyr_key = "mat_pyr_state"

    if st.button("🔺 Yeni Piramit Oluştur", key="mat_pyr_new"):
        st.session_state[pyr_key] = NumberPyramidEngine.generate(rows, max_base)

    if pyr_key in st.session_state:
        pyr = st.session_state[pyr_key]
        solution = pyr["solution"]
        pyramid = pyr["pyramid"]

        # Piramidi göster (üstten alta)
        for r_idx in range(len(solution) - 1, -1, -1):
            row = solution[r_idx]
            display_row = pyramid[r_idx]

            html_cells = ""
            for c_idx, val in enumerate(display_row):
                if val is None:
                    html_cells += f'<span class="mat-pyramid-cell hidden">?</span>'
                else:
                    html_cells += f'<span class="mat-pyramid-cell">{val}</span>'

            _render_html(f'<div class="mat-pyramid-row">{html_cells}</div>')

        with st.expander("👁️ Çözümü Göster"):
            for r_idx in range(len(solution) - 1, -1, -1):
                row = solution[r_idx]
                html_cells = ""
                for val in row:
                    html_cells += f'<span class="mat-pyramid-cell">{val}</span>'
                _render_html(f'<div class="mat-pyramid-row">{html_cells}</div>')


def _render_sudoku(store: MatematikDataStore):
    """Sudoku oyunu — gerçek tablolu, sınırsız üretim."""
    import streamlit.components.v1 as components
    styled_section("🧩 Sudoku", "#6366f1")

    col1, col2 = st.columns(2)
    with col1:
        size = st.selectbox("Boyut", [4, 9], key="mat_sdk_size",
                            format_func=lambda x: f"{x}×{x}")
    with col2:
        if size == 4:
            blanks = st.selectbox("Zorluk", [4, 6, 8], key="mat_sdk_blanks",
                                   format_func=lambda x: {4:"Kolay (4 boş)",6:"Orta (6 boş)",8:"Zor (8 boş)"}[x])
        else:
            blanks = st.selectbox("Zorluk", [25, 35, 45, 55], key="mat_sdk_blanks9",
                                   format_func=lambda x: {25:"Kolay",35:"Orta",45:"Zor",55:"Uzman"}.get(x,str(x)))

    sdk_key = "mat_sdk_state"

    if st.button("🧩 Yeni Sudoku Üret!", key="mat_sdk_new", type="primary"):
        st.session_state[sdk_key] = SudokuEngine.generate(size, blanks)

    if sdk_key in st.session_state:
        sdk = st.session_state[sdk_key]
        puzzle = sdk["puzzle"]
        solution = sdk["solution"]
        sz = sdk["size"]
        box = 2 if sz == 4 else 3

        st.write(f"**{sz}×{sz} Sudoku** — Her satır, sütun ve {box}×{box} blokta 1-{sz} arası rakamlar birer kez bulunmalı.")

        # HTML Tablo ile gerçek Sudoku grid
        cell_size = 48 if sz == 9 else 64
        font_size = "1.2rem" if sz == 9 else "1.5rem"

        table_html = f"""
        <table style="border-collapse:collapse;margin:12px auto;background:#0f172a">
        """
        for r in range(sz):
            table_html += "<tr>"
            for c in range(sz):
                val = puzzle[r][c]
                sol_val = solution[r][c]

                # Kalın kenar: kutu sınırları
                border_top = "3px solid #6366f1" if r % box == 0 else "1px solid #334155"
                border_left = "3px solid #6366f1" if c % box == 0 else "1px solid #334155"
                border_right = "3px solid #6366f1" if c == sz - 1 else ""
                border_bottom = "3px solid #6366f1" if r == sz - 1 else ""

                style = (f"width:{cell_size}px;height:{cell_size}px;text-align:center;"
                         f"font-size:{font_size};font-weight:700;font-family:'Courier New',monospace;"
                         f"border-top:{border_top};border-left:{border_left};")
                if border_right:
                    style += f"border-right:{border_right};"
                if border_bottom:
                    style += f"border-bottom:{border_bottom};"

                if val != 0:
                    style += "color:#e0e7ff;background:#1e1b4b;"
                    table_html += f'<td style="{style}">{val}</td>'
                else:
                    style += "color:#64748b;background:#0f172a;"
                    table_html += f'<td style="{style}"></td>'
            table_html += "</tr>"
        table_html += "</table>"

        _render_html(table_html)

        # Streamlit input grid — cevap girişi
        with st.expander("✏️ Cevaplarını Gir", expanded=True):
            for r in range(sz):
                cols = st.columns(sz)
                for c in range(sz):
                    with cols[c]:
                        if puzzle[r][c] == 0:
                            st.text_input(f"R{r+1}C{c+1}", key=f"mat_sdk_{r}_{c}",
                                          placeholder="?", label_visibility="collapsed", max_chars=1)
                        else:
                            st.markdown(f"<div style='text-align:center;font-weight:700;color:#818cf8;padding:6px'>{puzzle[r][c]}</div>",
                                        unsafe_allow_html=True)

            if st.button("✅ Cevapları Kontrol Et!", key="mat_sdk_check", type="primary"):
                dogru = 0
                yanlis = 0
                bos = 0
                for r in range(sz):
                    for c in range(sz):
                        if puzzle[r][c] == 0:
                            user_val = st.session_state.get(f"mat_sdk_{r}_{c}", "")
                            if user_val and user_val.isdigit():
                                if int(user_val) == solution[r][c]:
                                    dogru += 1
                                else:
                                    yanlis += 1
                            else:
                                bos += 1
                toplam = dogru + yanlis
                if yanlis == 0 and bos == 0:
                    st.success(f"🎉 MÜKEMMEL! Tüm hücreler doğru! ({dogru}/{dogru})")
                    st.balloons()
                elif yanlis == 0 and bos > 0:
                    st.info(f"✅ Girdiğin {dogru} hücre doğru! {bos} hücre daha kaldı.")
                else:
                    st.warning(f"✅ {dogru} doğru, ❌ {yanlis} yanlış, ⬜ {bos} boş")

        with st.expander("👁️ Çözümü Göster"):
            # Çözüm tablosu
            sol_html = '<table style="border-collapse:collapse;margin:8px auto;background:#052e16">'
            for r in range(sz):
                sol_html += "<tr>"
                for c in range(sz):
                    bt = "2px solid #10b981" if r % box == 0 else "1px solid #1e4d3a"
                    bl = "2px solid #10b981" if c % box == 0 else "1px solid #1e4d3a"
                    br = "2px solid #10b981" if c == sz-1 else ""
                    bb = "2px solid #10b981" if r == sz-1 else ""
                    s = f"width:36px;height:36px;text-align:center;font-size:1rem;font-weight:700;color:#86efac;border-top:{bt};border-left:{bl};"
                    if br: s += f"border-right:{br};"
                    if bb: s += f"border-bottom:{bb};"
                    sol_html += f'<td style="{s}">{solution[r][c]}</td>'
                sol_html += "</tr>"
            sol_html += "</table>"
            _render_html(sol_html)


def _render_carpim_savasi(store: MatematikDataStore):
    """Çarpım tablosu hız oyunu — süre + doğru/yanlış takibi."""
    import random as _r, time
    styled_section("⚔️ Çarpım Savaşı", "#dc2626")

    col1, col2, col3 = st.columns(3)
    with col1:
        tablo = st.selectbox("Çarpım Tablosu", list(range(2, 13)), key="mat_cs_tablo", index=1)
    with col2:
        soru_s = st.selectbox("Soru Sayısı", [5, 10, 15, 20], key="mat_cs_adet", index=1)
    with col3:
        cs_sure = st.selectbox("Süre Limiti", [30, 60, 90, 0], key="mat_cs_sure",
                                format_func=lambda x: f"{x} sn" if x > 0 else "Sınırsız", index=1)

    sk = "mat_cs_state"
    if sk not in st.session_state:
        st.session_state[sk] = {"active": False}

    state = st.session_state[sk]

    if not state.get("active"):
        if st.button("⚔️ Savaşı Başlat!", key="mat_cs_start", type="primary"):
            sorular = []
            for _ in range(soru_s):
                b = _r.randint(1, 12)
                sorular.append({"a": tablo, "b": b, "cevap": tablo * b})
            st.session_state[sk] = {
                "active": True, "sorular": sorular, "current": 0,
                "dogru": 0, "yanlis": 0, "start": time.time(),
                "sure_limit": cs_sure, "son_cevap": None,
            }
            st.rerun()
    else:
        elapsed = round(time.time() - state.get("start", time.time()), 1) if state.get("start") else 0
        sl = state.get("sure_limit", 0)
        sure_bitti = sl > 0 and elapsed >= sl
        cur = state.get("current", 0)
        sorular_list = state.get("sorular", [])
        d = state.get("dogru", 0)
        y = state.get("yanlis", 0)

        if cur < len(sorular_list) and not sure_bitti:
            s = sorular_list[cur]
            progress = cur / len(sorular_list) if sorular_list else 0
            kalan = max(0, sl - elapsed) if sl > 0 else None

            sc = state.get("son_cevap")
            if sc == "dogru":
                _render_html('<div style="text-align:center;color:#10b981 !important;font-weight:700;margin-bottom:6px">✅ Doğru!</div>')
            elif sc == "yanlis":
                _render_html(f'<div style="text-align:center;color:#ef4444 !important;font-weight:700;margin-bottom:6px">❌ Yanlış! Doğrusu: {state.get("son_dogru","")}</div>')

            st.progress(progress, text=f"Soru {cur+1}/{len(sorular_list)} • ✅{d} ❌{y}")

            _render_html(f"""
            <div style="background:#0f172a;border-radius:20px;padding:32px;text-align:center;margin:12px 0;
                         border:2px solid rgba(220,38,38,0.3)">
                {f'<div style="color:{"#ef4444" if kalan and kalan<10 else "#f59e0b"} !important;font-weight:700;font-size:1.3rem;margin-bottom:12px">⏱️ {kalan:.0f}s</div>' if kalan is not None else ''}
                <div style="font-size:3.5rem;font-weight:900;color:#e0e7ff !important">
                    {s['a']} × {s['b']} = ?
                </div>
            </div>
            """)

            secenekler = {s["cevap"]}
            while len(secenekler) < 4:
                wrong = s["cevap"] + _r.choice([-2,-1,1,2,3]) * _r.randint(1,3)
                if wrong > 0 and wrong != s["cevap"]:
                    secenekler.add(wrong)
            secenekler = sorted(list(secenekler))

            cols = st.columns(4)
            for idx, opt in enumerate(secenekler):
                with cols[idx]:
                    if st.button(str(opt), key=f"mat_cs_opt_{cur}_{idx}", use_container_width=True):
                        if opt == s["cevap"]:
                            state["dogru"] = d + 1
                            state["son_cevap"] = "dogru"
                        else:
                            state["yanlis"] = y + 1
                            state["son_cevap"] = "yanlis"
                            state["son_dogru"] = str(s["cevap"])
                        state["current"] = cur + 1
                        st.rerun()
        else:
            toplam = d + y
            oran = (d / toplam * 100) if toplam > 0 else 0
            bitis = "⏱️ Süre Doldu!" if sure_bitti else "🏁 Bitti!"

            _render_html(f"""
            <div style="background:#0f172a;border-radius:20px;padding:32px;text-align:center;margin:16px 0;
                         border:2px solid rgba(16,185,129,0.3)">
                <div style="font-size:0.9rem;color:#94a3b8 !important;margin-bottom:8px">{bitis}</div>
                <div style="font-size:3rem;margin-bottom:12px">{'🏆' if oran>=80 else '👏' if oran>=50 else '💪'}</div>
                <div style="font-size:1.5rem;font-weight:800;color:#e0e7ff !important;margin-bottom:12px">Savaş Bitti!</div>
                <div style="display:flex;justify-content:center;gap:24px;flex-wrap:wrap">
                    <div><div style="font-size:2rem;font-weight:900;color:#10b981 !important">{d}</div><div style="font-size:0.75rem;color:#94a3b8 !important">Doğru</div></div>
                    <div><div style="font-size:2rem;font-weight:900;color:#ef4444 !important">{y}</div><div style="font-size:0.75rem;color:#94a3b8 !important">Yanlış</div></div>
                    <div><div style="font-size:2rem;font-weight:900;color:#f59e0b !important">%{oran:.0f}</div><div style="font-size:0.75rem;color:#94a3b8 !important">Başarı</div></div>
                    <div><div style="font-size:2rem;font-weight:900;color:#6366f1 !important">{elapsed:.1f}s</div><div style="font-size:0.75rem;color:#94a3b8 !important">Süre</div></div>
                </div>
            </div>
            """)
            if st.button("🔄 Tekrar Savaş!", key="mat_cs_reset"):
                del st.session_state[sk]
                st.rerun()


def _render_tahmin_oyunu(store: MatematikDataStore):
    """Sayı tahmin oyunu — bilgisayar sayı tutuyor, sen bul!"""
    import random as _r
    styled_section("🎯 Tahmin Oyunu", "#059669")

    col1, col2 = st.columns(2)
    with col1:
        aralik = st.selectbox("Aralık", [
            (1, 20, "1-20 (Kolay)"), (1, 50, "1-50 (Orta)"),
            (1, 100, "1-100 (Zor)"), (1, 500, "1-500 (Uzman)"),
        ], key="mat_to_aralik", format_func=lambda x: x[2])
    with col2:
        max_deneme = st.selectbox("Max Deneme", [5, 7, 10, 15], key="mat_to_deneme", index=1)

    sk = "mat_to_state"

    if st.button("🎯 Yeni Oyun!", key="mat_to_start", type="primary"):
        hedef = _r.randint(aralik[0], aralik[1])
        st.session_state[sk] = {
            "hedef": hedef, "denemeler": [], "max": max_deneme,
            "bitti": False, "aralik": (aralik[0], aralik[1]),
        }

    if sk in st.session_state:
        state = st.session_state[sk]

        if not state["bitti"]:
            kalan = state["max"] - len(state["denemeler"])
            _render_html(f"""
            <div style="background:#0f172a;border-radius:16px;padding:20px;text-align:center;margin:12px 0;
                         border:1px solid rgba(5,150,105,0.3)">
                <div style="font-size:1rem;color:#86efac !important;margin-bottom:8px">
                    {state['aralik'][0]}-{state['aralik'][1]} arası bir sayı tuttum! 🤔
                </div>
                <div style="font-size:0.9rem;color:#f59e0b !important">Kalan deneme: {kalan}</div>
            </div>
            """)

            # Önceki denemeler
            for d in state["denemeler"]:
                yön = "⬆️ Daha büyük!" if d < state["hedef"] else "⬇️ Daha küçük!"
                st.markdown(f"- Tahmin: **{d}** → {yön}")

            tahmin = st.number_input("Tahminin:", min_value=state["aralik"][0],
                                      max_value=state["aralik"][1], step=1, key=f"mat_to_inp_{len(state['denemeler'])}")

            if st.button("🔍 Tahmin Et!", key=f"mat_to_guess_{len(state['denemeler'])}"):
                state["denemeler"].append(int(tahmin))

                if int(tahmin) == state["hedef"]:
                    state["bitti"] = True
                    st.success(f"🎉 BİLDİN! Sayı **{state['hedef']}** — {len(state['denemeler'])} denemede!")
                    st.balloons()
                elif len(state["denemeler"]) >= state["max"]:
                    state["bitti"] = True
                    st.error(f"😢 Denemen bitti! Sayı **{state['hedef']}** idi.")
                else:
                    st.rerun()


def _render_hafiza_kartlari(store: MatematikDataStore):
    """Hafıza kartları — eşleşen çiftleri bul."""
    import random as _r
    styled_section("🃏 Hafıza Kartları", "#ec4899")

    boyut = st.selectbox("Kart Sayısı", [
        (3, "6 kart (3 çift) — Kolay"), (4, "8 kart (4 çift) — Orta"),
        (5, "10 kart (5 çift) — Zor"), (6, "12 kart (6 çift) — Uzman"),
    ], key="mat_hk_boyut", format_func=lambda x: x[1])

    cift_sayisi = boyut[0]
    emojiler = ["🐶","🐱","🐰","🦊","🐻","🐼","🐸","🦁","🐯","🐵","🦋","🐝"]

    sk = "mat_hk_state"

    if st.button("🃏 Yeni Oyun!", key="mat_hk_start", type="primary"):
        secilen = emojiler[:cift_sayisi]
        kartlar = secilen * 2
        _r.shuffle(kartlar)
        st.session_state[sk] = {
            "kartlar": kartlar, "acik": [False] * len(kartlar),
            "eslesen": [False] * len(kartlar),
            "ilk_secim": None, "hamle": 0, "eslesen_cift": 0,
            "toplam_cift": cift_sayisi,
        }

    if sk in st.session_state:
        state = st.session_state[sk]
        kartlar = state["kartlar"]

        st.markdown(f"**Hamle:** {state['hamle']} | **Eşleşen:** {state['eslesen_cift']}/{state['toplam_cift']}")

        # Kart grid — 4 sütun
        sutun = 4
        for row in range(0, len(kartlar), sutun):
            cols = st.columns(sutun)
            for col_idx, col in enumerate(cols):
                idx = row + col_idx
                if idx < len(kartlar):
                    with col:
                        if state["eslesen"][idx]:
                            # Eşleşen kart — göster
                            _render_html(f"""
                            <div style="background:#065f46;border-radius:12px;padding:16px;text-align:center;
                                         margin-bottom:8px;font-size:2rem;border:2px solid #10b981">
                                {kartlar[idx]}
                            </div>
                            """)
                        elif state["acik"][idx]:
                            # Açık kart — göster
                            _render_html(f"""
                            <div style="background:#1e1b4b;border-radius:12px;padding:16px;text-align:center;
                                         margin-bottom:8px;font-size:2rem;border:2px solid #6366f1">
                                {kartlar[idx]}
                            </div>
                            """)
                        else:
                            # Kapalı kart — buton
                            if st.button("❓", key=f"mat_hk_card_{idx}", use_container_width=True):
                                if state["ilk_secim"] is None:
                                    # İlk kartı aç
                                    state["acik"][idx] = True
                                    state["ilk_secim"] = idx
                                    st.rerun()
                                else:
                                    # İkinci kartı aç — eşleşme kontrolü
                                    ilk = state["ilk_secim"]
                                    state["acik"][idx] = True
                                    state["hamle"] += 1

                                    if kartlar[ilk] == kartlar[idx]:
                                        # Eşleşti!
                                        state["eslesen"][ilk] = True
                                        state["eslesen"][idx] = True
                                        state["eslesen_cift"] += 1
                                        state["ilk_secim"] = None

                                        if state["eslesen_cift"] >= state["toplam_cift"]:
                                            st.success(f"🎉 Tebrikler! {state['hamle']} hamlede tamamladın!")
                                            st.balloons()
                                    else:
                                        # Eşleşmedi — kapat
                                        state["acik"][ilk] = False
                                        state["acik"][idx] = False
                                        state["ilk_secim"] = None

                                    st.rerun()


def _render_kesir_pizzasi(store: MatematikDataStore):
    """Kesir pizzası oyunu — sınırsız soru üretimi."""
    import random as _r
    styled_section("🍕 Kesir Pizzası", "#ef4444")

    sk = "mat_kp_state"
    if sk not in st.session_state:
        st.session_state[sk] = {"skor": 0, "toplam": 0}

    skor = st.session_state[sk]

    if st.button("🍕 Yeni Pizza!", key="mat_kp_new", type="primary"):
        payda = _r.choice([2, 3, 4, 5, 6, 8])
        pay = _r.randint(1, payda - 1)
        st.session_state["mat_kp_soru"] = {"pay": pay, "payda": payda}

    if "mat_kp_soru" in st.session_state:
        s = st.session_state["mat_kp_soru"]
        pay, payda = s["pay"], s["payda"]
        pizza_dolu = "🍕" * pay
        pizza_bos = "⬜" * (payda - pay)

        _render_html(f"""
        <div style="background:#0f172a;border-radius:20px;padding:28px;text-align:center;margin:12px 0;
                     border:2px solid rgba(239,68,68,0.3)">
            <div style="font-size:1rem;color:#94a3b8 !important;margin-bottom:12px">Pizza {payda} dilime bölündü. Kaç dilim yenildi?</div>
            <div style="font-size:2.5rem;letter-spacing:4px;margin-bottom:12px">{pizza_dolu}{pizza_bos}</div>
            <div style="font-size:1.5rem;font-weight:800;color:#e0e7ff !important">❓ / {payda} = ?</div>
        </div>
        """)

        ans = st.number_input("Yenilen dilim sayısı:", 0, payda, 0, key="mat_kp_ans")
        if st.button("✅ Kontrol Et", key="mat_kp_chk"):
            skor["toplam"] += 1
            if int(ans) == pay:
                skor["skor"] += 1
                st.success(f"🎉 Doğru! {pay}/{payda} pizza yenildi!")
            else:
                st.error(f"❌ Yanlış! Doğru cevap: {pay}/{payda}")

    if skor["toplam"] > 0:
        st.markdown(f"**Skor:** ✅ {skor['skor']}/{skor['toplam']}")


def _render_denklem_dengesi(store: MatematikDataStore):
    """Denklem dengesi oyunu — sınırsız."""
    import random as _r
    styled_section("⚖️ Denklem Dengesi", "#10b981")

    zorluk = st.selectbox("Zorluk", ["Kolay (ax=b)", "Orta (ax+b=c)", "Zor (ax+b=cx+d)"],
                           key="mat_dd_zor")

    sk = "mat_dd_state"
    if sk not in st.session_state:
        st.session_state[sk] = {"skor": 0, "toplam": 0}

    if st.button("⚖️ Yeni Denklem!", key="mat_dd_new", type="primary"):
        if "Kolay" in zorluk:
            x = _r.randint(1, 10)
            a = _r.randint(2, 9)
            b = a * x
            denklem = f"{a}x = {b}"
        elif "Orta" in zorluk:
            x = _r.randint(1, 15)
            a = _r.randint(2, 8)
            b = _r.randint(1, 20)
            c = a * x + b
            denklem = f"{a}x + {b} = {c}"
        else:
            x = _r.randint(1, 10)
            a = _r.randint(2, 6)
            c = _r.randint(1, a - 1) if a > 1 else 1
            b = _r.randint(1, 15)
            d = a * x + b - c * x
            denklem = f"{a}x + {b} = {c}x + {d}"

        st.session_state["mat_dd_soru"] = {"denklem": denklem, "cevap": x}

    if "mat_dd_soru" in st.session_state:
        s = st.session_state["mat_dd_soru"]
        _render_html(f"""
        <div style="background:#0f172a;border-radius:20px;padding:32px;text-align:center;margin:12px 0;
                     border:2px solid rgba(16,185,129,0.3)">
            <div style="font-size:2rem;margin-bottom:12px">⚖️</div>
            <div style="font-size:2.5rem;font-weight:900;color:#e0e7ff !important;
                         font-family:'Cambria Math','Times New Roman',serif">{s['denklem']}</div>
            <div style="font-size:1.2rem;color:#94a3b8 !important;margin-top:12px">x = ?</div>
        </div>
        """)

        ans = st.number_input("x değeri:", -100, 100, 0, key="mat_dd_ans")
        if st.button("✅ Kontrol Et", key="mat_dd_chk"):
            st.session_state[sk]["toplam"] += 1
            if int(ans) == s["cevap"]:
                st.session_state[sk]["skor"] += 1
                st.success(f"🎉 Doğru! x = {s['cevap']}")
            else:
                st.error(f"❌ Yanlış! x = {s['cevap']}")

    skor = st.session_state[sk]
    if skor["toplam"] > 0:
        st.markdown(f"**Skor:** ✅ {skor['skor']}/{skor['toplam']}")


def _render_sayi_bulmaca(store: MatematikDataStore):
    """Sayı bulmaca oyunu — ipuçlarıyla sayıyı bul."""
    import random as _r
    styled_section("🔢 Sayı Bulmaca", "#3b82f6")

    aralik = st.selectbox("Aralık", [(1,50,"1-50"),(1,100,"1-100"),(1,200,"1-200")],
                           key="mat_sb_aralik", format_func=lambda x: x[2])

    sk = "mat_sb_state"

    if st.button("🔢 Yeni Bulmaca!", key="mat_sb_new", type="primary"):
        hedef = _r.randint(aralik[0], aralik[1])
        rak_toplam = sum(int(d) for d in str(hedef))
        ipuclari = [
            f"{'Çift' if hedef % 2 == 0 else 'Tek'} sayı",
            f"Rakamları toplamı: {rak_toplam}",
        ]
        if hedef > aralik[1] // 2:
            ipuclari.append(f"{aralik[1]//2}'den büyük")
        else:
            ipuclari.append(f"{aralik[1]//2}'den küçük veya eşit")
        if hedef % 3 == 0:
            ipuclari.append("3'e tam bölünür")
        if hedef % 5 == 0:
            ipuclari.append("5'e tam bölünür")

        st.session_state[sk] = {"hedef": hedef, "ipuclari": ipuclari, "denemeler": [], "bitti": False}

    if sk in st.session_state:
        state = st.session_state[sk]
        if not state.get("bitti", False):
            st.markdown("**İpuçları:**")
            for ip in state.get("ipuclari", []):
                st.markdown(f"- {ip}")

            for d in state.get("denemeler", []):
                yon = "⬆️ Daha büyük!" if d < state["hedef"] else "⬇️ Daha küçük!"
                st.markdown(f"- Tahmin: **{d}** → {yon}")

            tahmin = st.number_input("Tahminin:", aralik[0], aralik[1], aralik[1]//2,
                                      key=f"mat_sb_inp_{len(state.get('denemeler',[]))}")
            if st.button("🔍 Tahmin Et!", key=f"mat_sb_guess_{len(state.get('denemeler',[]))}"):
                state.setdefault("denemeler", []).append(int(tahmin))
                if int(tahmin) == state["hedef"]:
                    state["bitti"] = True
                    st.success(f"🎉 BİLDİN! Sayı **{state['hedef']}** — {len(state['denemeler'])} denemede!")
                    st.balloons()
                else:
                    st.rerun()
        else:
            st.success(f"🏆 Tebrikler! {state['hedef']} sayısını {len(state.get('denemeler',[]))} denemede buldun!")
            if st.button("🔄 Yeni Bulmaca", key="mat_sb_reset"):
                del st.session_state[sk]
                st.rerun()


def _render_geometri_macerasi(store: MatematikDataStore):
    """Geometri macerası — şekil tanıma, açı, alan hesaplama."""
    import random as _r
    import math
    styled_section("📐 Geometri Macerası", "#8b5cf6")

    sk = "mat_gm_state"
    if sk not in st.session_state:
        st.session_state[sk] = {"skor": 0, "toplam": 0}

    tip = st.selectbox("Soru Türü", ["Karışık", "Alan Hesapla", "Çevre Hesapla", "Açı Bul"],
                        key="mat_gm_tip")

    if st.button("📐 Yeni Soru!", key="mat_gm_new", type="primary"):
        if tip == "Karışık":
            secim = _r.choice(["alan", "cevre", "aci"])
        elif "Alan" in tip:
            secim = "alan"
        elif "Çevre" in tip:
            secim = "cevre"
        else:
            secim = "aci"

        if secim == "alan":
            sekil = _r.choice(["kare", "dikdortgen", "ucgen", "daire"])
            if sekil == "kare":
                a = _r.randint(2, 20)
                soru = f"⬜ Kenar uzunluğu **{a} cm** olan karenin alanı kaç cm²?"
                cevap = a * a
            elif sekil == "dikdortgen":
                a, b = _r.randint(3, 15), _r.randint(3, 15)
                soru = f"▬ Kenarları **{a} cm** ve **{b} cm** olan dikdörtgenin alanı kaç cm²?"
                cevap = a * b
            elif sekil == "ucgen":
                t, h = _r.randint(4, 20), _r.randint(3, 15)
                cevap = t * h // 2
                soru = f"🔺 Tabanı **{t} cm**, yüksekliği **{h} cm** olan üçgenin alanı kaç cm²?"
            else:
                r = _r.randint(2, 10)
                cevap = round(3.14 * r * r, 1)
                soru = f"⭕ Yarıçapı **{r} cm** olan dairenin alanı kaç cm²? (π=3.14)"
        elif secim == "cevre":
            sekil = _r.choice(["kare", "dikdortgen", "daire"])
            if sekil == "kare":
                a = _r.randint(2, 20)
                soru = f"⬜ Kenar uzunluğu **{a} cm** olan karenin çevresi kaç cm?"
                cevap = 4 * a
            elif sekil == "dikdortgen":
                a, b = _r.randint(3, 15), _r.randint(3, 15)
                soru = f"▬ Kenarları **{a} cm** ve **{b} cm** olan dikdörtgenin çevresi kaç cm?"
                cevap = 2 * (a + b)
            else:
                r = _r.randint(2, 10)
                cevap = round(2 * 3.14 * r, 1)
                soru = f"⭕ Yarıçapı **{r} cm** olan dairenin çevresi kaç cm? (π=3.14)"
        else:
            tip_aci = _r.choice(["ucgen", "dortgen", "tamamlayici"])
            if tip_aci == "ucgen":
                a1 = _r.randint(20, 80)
                a2 = _r.randint(20, 80)
                cevap = 180 - a1 - a2
                soru = f"🔺 Üçgende iki açı **{a1}°** ve **{a2}°**. Üçüncü açı kaç derece?"
            elif tip_aci == "dortgen":
                a1 = _r.randint(50, 120)
                a2 = _r.randint(50, 120)
                a3 = _r.randint(50, 120)
                cevap = 360 - a1 - a2 - a3
                soru = f"⬜ Dörtgende üç açı **{a1}°**, **{a2}°**, **{a3}°**. Dördüncü açı?"
            else:
                a1 = _r.randint(10, 80)
                cevap = 90 - a1
                soru = f"📐 **{a1}°**'nin tamamlayıcı açısı (toplamları 90°) kaç derece?"

        st.session_state["mat_gm_soru"] = {"soru": soru, "cevap": cevap}

    if "mat_gm_soru" in st.session_state:
        s = st.session_state["mat_gm_soru"]
        st.markdown(f"### {s['soru']}")

        ans = st.number_input("Cevabın:", -1000.0, 100000.0, 0.0, step=0.1, key="mat_gm_ans")
        if st.button("✅ Kontrol Et", key="mat_gm_chk"):
            st.session_state[sk]["toplam"] += 1
            # Yuvarlama toleransı
            if abs(float(ans) - float(s["cevap"])) < 0.5:
                st.session_state[sk]["skor"] += 1
                st.success(f"🎉 Doğru! Cevap: {s['cevap']}")
            else:
                st.error(f"❌ Yanlış! Doğru cevap: {s['cevap']}")

    skor = st.session_state[sk]
    if skor["toplam"] > 0:
        st.markdown(f"**Skor:** ✅ {skor['skor']}/{skor['toplam']}")


def _render_acik_uclu(store: MatematikDataStore):
    """Açık uçlu yaratıcı problemler — birden fazla çözüm yolu."""
    import random as _r
    styled_section("💡 Açık Uçlu Meydan Okuma", "#eab308")

    problemler = [
        {"soru": "4 tane 4 kullanarak (ve +, -, ×, ÷, parantez) 0'dan 10'a kadar tüm sayıları yaz.\nÖrnek: 4+4-4-4 = 0, 4÷4+4-4 = 1", "ipucu": "44, 4!, √4 de kullanabilirsin"},
        {"soru": "1'den 9'a kadar tüm rakamları bir kez kullanarak toplamı 100 yapan bir ifade yaz.\nÖrnek: 1+2+3+4+5+6+7+8×9 = ?", "ipucu": "Çarpma ve toplama karıştır"},
        {"soru": "3 kesim ile bir pastayı en fazla kaç parçaya bölebilirsin? Kesimlerin düz olması gerekir.", "ipucu": "Kesimler birbirini kesebilir! Cevap 4'ten fazla!"},
        {"soru": "100'e ulaşmak için 1,2,3,4,5,6,7,8,9 sayılarını sırasıyla kullan. Aralarına +, - koyabilirsin.", "ipucu": "Birden fazla çözüm var! Ör: 1+2+34-5+67-8+9"},
        {"soru": "Bir çiftçinin 17 koyunu var. 9'u hariç hepsi öldü. Kaç koyun kaldı?", "ipucu": "Soruyu dikkatli oku — '9'u hariç HEPSI'"},
        {"soru": "64 takımlı eleme turnuvasında şampiyon belirlemek için toplam kaç maç oynanmalı?", "ipucu": "Her maçta 1 takım elenir..."},
        {"soru": "Bir ip merdivende 10 basamak var. Bir kurbağa her adımda 3 basamak çıkıp 1 basamak kayıyor. Kaç adımda tepeye ulaşır?", "ipucu": "Son adımda kayma olmaz!"},
        {"soru": "1 ile 1000 arasında kaç tane 7 rakamı yazılır?", "ipucu": "Birler, onlar ve yüzler basamağını ayrı ayrı say"},
        {"soru": "Saat 3:15'te akrep ile yelkovan arasındaki açı tam olarak kaç derecedir?", "ipucu": "Akrep de hareket eder! 3:15'te tam 90° değil..."},
        {"soru": "5 kişi birbirleriyle birer kez tokalaşırsa toplam kaç tokalaşma olur? Ya 20 kişi olsaydı?", "ipucu": "Kombinasyon: C(n,2) = n(n-1)/2"},
        {"soru": "Bir tavuk 1.5 günde 1.5 yumurta bırakıyorsa 9 tavuk 9 günde kaç yumurta bırakır?", "ipucu": "Oranı bul: 1 tavuk 1 günde kaç yumurta?"},
        {"soru": "3 kutu var: biri elma, biri portakal, biri karışık. Etiketlerin HEPSİ yanlış. 1 kutudan 1 meyve çekerek tüm kutuları doğru etiketleyebilir misin?", "ipucu": "Karışık etiketli kutudan başla!"},
    ]

    if st.button("💡 Yeni Problem!", key="mat_au_new", type="primary"):
        st.session_state["mat_au_soru"] = _r.choice(problemler)

    if "mat_au_soru" in st.session_state:
        s = st.session_state["mat_au_soru"]
        _render_html(f"""
        <div style="background:#0f172a;border-radius:20px;padding:28px;margin:12px 0;
                     border:2px solid rgba(234,179,8,0.3)">
            <div style="font-size:2rem;margin-bottom:12px;text-align:center" class="mat-grow">💡</div>
            <div style="font-size:1rem;color:#e0e7ff !important;line-height:1.8;white-space:pre-line">{s['soru']}</div>
        </div>
        """)

        with st.expander("💡 İpucu"):
            st.info(s["ipucu"])

        st.text_area("Çözümünü yaz:", key="mat_au_cevap", height=100,
                      placeholder="Çözüm yolunu ve cevabını buraya yaz...")


def _render_mini_oyun(oyun_key: str, store: MatematikDataStore):
    """Oyun Seç ekranından seçilen oyun için mini alan."""
    import random as _r
    info = OYUN_BILGILERI.get(oyun_key, {})

    if oyun_key in ("kesir_pizzasi",):
        styled_section("🍕 Kesir Pizzası", "#ef4444")
        st.info("Pizzayı doğru böl!")
        kesir_pay = _r.randint(1, 7)
        kesir_payda = _r.choice([2, 3, 4, 5, 6, 8])
        if kesir_pay >= kesir_payda:
            kesir_pay = kesir_payda - 1
        pizza = "🍕" * kesir_payda
        _render_html(f"""
        <div style="background:#0f172a;border-radius:16px;padding:24px;text-align:center;margin:12px 0;
                     border:1px solid rgba(239,68,68,0.2)">
            <div style="font-size:2rem;letter-spacing:4px;margin-bottom:12px">{pizza}</div>
            <div style="font-size:1.3rem;color:#e0e7ff !important;font-weight:700">
                Pizzanın {kesir_pay}/{kesir_payda}'{'i' if kesir_payda in (2,3,4,5) else 'ü'} kaç dilim?
            </div>
        </div>
        """)
        ans = st.number_input("Kaç dilim?", 0, 20, 0, key="mat_mo_kesir")
        if st.button("✅ Kontrol", key="mat_mo_kesir_chk"):
            if int(ans) == kesir_pay:
                st.success(f"🎉 Doğru! {kesir_pay}/{kesir_payda} = {kesir_pay} dilim")
            else:
                st.error(f"❌ Doğru cevap: {kesir_pay} dilim")

    elif oyun_key == "denklem_dengesi":
        styled_section("⚖️ Denklem Dengesi", "#10b981")
        x = _r.randint(1, 15)
        a = _r.randint(2, 6)
        b = _r.randint(1, 20)
        sonuc = a * x + b
        st.markdown(f"### ⚖️  {a}x + {b} = {sonuc}")
        st.markdown("**x = ?**")
        ans = st.number_input("x değeri:", -50, 100, 0, key="mat_mo_denk")
        if st.button("✅ Kontrol", key="mat_mo_denk_chk"):
            if int(ans) == x:
                st.success(f"🎉 Doğru! x = {x}")
                st.balloons()
            else:
                st.error(f"❌ x = {x} ({a}×{x}+{b}={sonuc})")

    elif oyun_key == "sayi_labirenti":
        styled_section("🌀 Sayı Labirenti", "#06b6d4")
        lab_key = "mat_lab_state"
        if lab_key not in st.session_state:
            hedef = _r.randint(20, 100)
            baslangic = _r.randint(1, 10)
            st.session_state[lab_key] = {"baslangic": baslangic, "hedef": hedef, "mevcut": baslangic, "adimlar": [], "bitti": False}

        s = st.session_state[lab_key]
        if not s.get("bitti"):
            st.markdown(f"### 🌀 Başlangıç: **{s['baslangic']}** → Hedef: **{s['hedef']}** | Şu an: **{s['mevcut']}**")
            if s.get("adimlar"):
                st.markdown("Adımlar: " + " → ".join(s["adimlar"]))

            col1, col2 = st.columns(2)
            with col1:
                islem = st.selectbox("İşlem", ["+", "-", "×"], key="mat_lab_op")
            with col2:
                deger = st.number_input("Değer", 1, 100, 2, key="mat_lab_val")
            if st.button("▶️ Uygula", key="mat_lab_go"):
                eski = s["mevcut"]
                if islem == "+":
                    s["mevcut"] = eski + deger
                elif islem == "-":
                    s["mevcut"] = max(0, eski - deger)
                else:
                    s["mevcut"] = eski * deger
                s["adimlar"].append(f"{eski}{islem}{deger}={s['mevcut']}")
                if s["mevcut"] == s["hedef"]:
                    s["bitti"] = True
                    st.success(f"🎉 Hedefe ulaştın! {len(s['adimlar'])} adımda!")
                    st.balloons()
                elif s["mevcut"] > s["hedef"] * 2:
                    st.error(f"⚠️ Çok büyük! ({s['mevcut']})")
                else:
                    st.rerun()
        else:
            st.success(f"🏆 {s['baslangic']} → {s['hedef']} = {len(s['adimlar'])} adım!")
            if st.button("🔄 Yeni Labirent", key="mat_lab_reset"):
                del st.session_state[lab_key]
                st.rerun()

    elif oyun_key == "sayi_bulmaca":
        st.info("⬆️ **Sayı Bulmaca** sekmesine geç!")

    else:
        st.info(f"🎮 **{info.get('ad', oyun_key)}** oyunu yakında aktif olacak! Diğer sekmelerdeki oyunları dene.")


# ══════════════════════════════════════════════════════════════════════════════
# 3) OLİMPİYAT MERKEZİ
# ══════════════════════════════════════════════════════════════════════════════

def _render_olimpiyat(store: MatematikDataStore):
    """Olimpiyat merkezi."""
    styled_section("🏆 Matematik Olimpiyat Merkezi", "#8b5cf6")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1a0a2e,#2d1b69);border-radius:16px;padding:20px;margin-bottom:20px;border:1px solid rgba(168,85,247,0.3)">
        <div style="font-weight:700;color:#e9d5ff !important;font-size:1.1rem;margin-bottom:6px">🏅 Olimpiyata Hazırlan!</div>
        <div style="color:#c4b5fd !important;font-size:0.9rem">TÜBİTAK, IMO, Kanguru ve daha fazlası! Olimpiyat seviyesinde sorularla kendini test et.</div>
    </div>
    """)

    sub_tabs = st.tabs(["📋 Soru Bankası", "🤖 Otomatik Üret", "➕ Soru Ekle", "📊 İstatistikler"])

    with sub_tabs[0]:
        _render_olimpiyat_sorulari(store)

    with sub_tabs[1]:
        _render_olimpiyat_oto_uret(store)

    with sub_tabs[2]:
        _render_olimpiyat_ekle(store)

    with sub_tabs[3]:
        _render_olimpiyat_istatistik(store)


def _render_olimpiyat_oto_uret(store: MatematikDataStore):
    """Olimpiyat sorusu otomatik üretimi."""
    styled_section("🤖 Otomatik Olimpiyat Sorusu Üret", "#a855f7")

    col1, col2 = st.columns(2)
    with col1:
        ol_adet = st.selectbox("Adet", [5, 10, 20, 50], key="ol_oto_adet", index=1)
    with col2:
        ol_kaydet = st.checkbox("Veritabanına kaydet", value=True, key="ol_oto_kaydet")

    mevcut = len(store.get_olympiad_questions())
    st.caption(f"Mevcut: {mevcut} olimpiyat sorusu")

    if st.button(f"🚀 {ol_adet} Olimpiyat Sorusu Üret!", key="ol_oto_go", type="primary"):
        sorular = OlimpiyatSoruGenerator.toplu_uret(ol_adet)
        if ol_kaydet:
            for s in sorular:
                q = OlympiadQuestion(
                    title=s["title"], body=s["body"], category=s.get("category", "Sayı Kuramı"),
                    level=s.get("level", "Okul"), source=s.get("source", "AI"),
                    year=s.get("year", 2025), answer=s.get("answer", ""),
                    solution=s.get("solution", ""), hints=s.get("hints", []),
                    grade_range=s.get("grade_range", "9-12"), xp_reward=s.get("xp_reward", 40),
                )
                store.add_olympiad_question(q)
        st.success(f"✅ {len(sorular)} olimpiyat sorusu üretildi{'ve kaydedildi' if ol_kaydet else ''}!")

        for i, s in enumerate(sorular[:5], 1):
            with st.expander(f"#{i} {s['title']}", expanded=False):
                st.markdown(s["body"])
                st.markdown(f"**Cevap:** ||{s['answer']}||")
                st.caption(s.get("solution", ""))
        if len(sorular) > 5:
            st.caption(f"... ve {len(sorular)-5} soru daha")


def _render_olimpiyat_sorulari(store: MatematikDataStore):
    """Olimpiyat soruları listesi."""
    col1, col2, col3 = st.columns(3)
    with col1:
        level_f = st.selectbox("Seviye", ["Tümü"] + [e.value for e in OlympiadLevel],
                               key="mat_ol_level")
    with col2:
        source_f = st.selectbox("Kaynak", ["Tümü"] + [e.value for e in OlympiadSource],
                                key="mat_ol_source")
    with col3:
        cat_f = st.selectbox("Kategori", ["Tümü"] + [e.value for e in MathCategory],
                             key="mat_ol_cat")

    questions = store.get_olympiad_questions(
        level=level_f if level_f != "Tümü" else None,
        source=source_f if source_f != "Tümü" else None,
        category=cat_f if cat_f != "Tümü" else None,
    )

    if not questions:
        st.info("Henüz olimpiyat sorusu eklenmemiş. Hazır örnek soruları yükleyebilirsiniz!")
        if st.button("🚀 Örnek Olimpiyat Sorularını Yükle (6 Soru)", key="mat_ol_seed", type="primary"):
            for oq in ORNEK_OLIMPIYAT_SORULARI:
                q = OlympiadQuestion(
                    title=oq["title"], body=oq["body"],
                    category=oq.get("category", "Sayı Kuramı"),
                    level=oq.get("level", "Okul"),
                    source=oq.get("source", "TÜBİTAK"),
                    year=oq.get("year", 2024),
                    answer=oq.get("answer", ""),
                    solution=oq.get("solution", ""),
                    hints=oq.get("hints", []),
                    grade_range=oq.get("grade_range", "9-12"),
                    xp_reward=oq.get("xp_reward", 50),
                )
                store.add_olympiad_question(q)
            st.success(f"✅ {len(ORNEK_OLIMPIYAT_SORULARI)} olimpiyat sorusu yüklendi!")
            st.rerun()
        return

    for q in questions[:20]:
        source_label = q.get("source", "")
        year = q.get("year", "")
        _render_html(f"""
        <div class="mat-olympiad-card">
            <div class="mat-olympiad-source">{source_label} — {year}</div>
            <div class="mat-olympiad-title">{q.get('title', 'Olimpiyat Sorusu')}</div>
            <div class="mat-olympiad-body">{q.get('body', '')}</div>
            <div style="margin-top:10px">
                {_difficulty_badge(q.get('difficulty', 'olimpiyat'))}
                {_xp_badge(q.get('xp_reward', 50))}
                <span style="color:#94a3b8 !important;font-size:0.8rem;margin-left:12px">
                    {q.get('category', '')} • Tahmini {q.get('estimated_time_min', 30)} dk
                </span>
            </div>
        </div>
        """)

        with st.expander(f"💡 Çözüm — {q.get('title', '')}", expanded=False):
            if q.get("solution"):
                st.markdown(q["solution"])
            if q.get("hints"):
                st.markdown("**İpuçları:**")
                for i, h in enumerate(q["hints"], 1):
                    st.markdown(f"{i}. {h}")


def _render_olimpiyat_ekle(store: MatematikDataStore):
    """Olimpiyat sorusu ekleme formu."""
    styled_section("➕ Yeni Olimpiyat Sorusu", "#a855f7")

    with st.form("mat_ol_form"):
        title = st.text_input("Soru Başlığı", key="matematik__1")

        body = st.text_area("Soru Metni", height=200,
                            placeholder="Markdown desteklidir. LaTeX için $...$ kullanın.", key="matematik__m1")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            source = st.selectbox("Kaynak", [e.value for e in OlympiadSource], key="matematik__3")

        with col2:
            level = st.selectbox("Seviye", [e.value for e in OlympiadLevel], key="matematik__4")

        with col3:
            category = st.selectbox("Kategori", [e.value for e in MathCategory], key="matematik__5")

        with col4:
            year = st.number_input("Yıl", 2000, 2030, 2024, key="matematik__6")


        col1, col2 = st.columns(2)
        with col1:
            round_name = st.text_input("Tur", placeholder="1. Tur, Final, vb.", key="matematik__7")

        with col2:
            est_time = st.number_input("Tahmini Süre (dk)", 5, 120, 30, key="matematik__8")


        answer = st.text_area("Cevap", height=80, key="matematik__9")

        solution = st.text_area("Çözüm (Detaylı)", height=200, key="matematik__10")

        hints = st.text_area("İpuçları (her satıra bir ipucu)", height=100, key="matematik__11")


        submitted = st.form_submit_button("💾 Soruyu Kaydet", type="primary")

        if submitted:
            if not title or not body:
                st.error("Başlık ve soru metni zorunludur!")
            else:
                q = OlympiadQuestion(
                    title=title, body=body,
                    category=category, level=level,
                    source=source, year=year,
                    round_name=round_name,
                    answer=answer, solution=solution,
                    hints=[h.strip() for h in hints.split("\n") if h.strip()],
                    estimated_time_min=est_time,
                    xp_reward=50 if level in ("Okul", "İlçe") else 100,
                )
                store.add_olympiad_question(q)
                st.success(f"✅ Olimpiyat sorusu eklendi: **{title}**")
                st.rerun()


def _render_olimpiyat_istatistik(store: MatematikDataStore):
    """Olimpiyat istatistikleri."""
    questions = store.get_olympiad_questions()

    if not questions:
        st.info("Henüz veri yok.")
        return

    # Kaynak dağılımı
    from collections import Counter
    source_counts = Counter(q.get("source", "Diğer") for q in questions)
    level_counts = Counter(q.get("level", "Bilinmiyor") for q in questions)
    cat_counts = Counter(q.get("category", "Diğer") for q in questions)

    col1, col2, col3 = st.columns(3)
    with col1:
        styled_section("Kaynağa Göre", "#a855f7")
        for src, cnt in source_counts.most_common(10):
            st.markdown(f"**{src}:** {cnt} soru")
    with col2:
        styled_section("Seviyeye Göre", "#6366f1")
        for lvl, cnt in level_counts.most_common():
            st.markdown(f"**{lvl}:** {cnt} soru")
    with col3:
        styled_section("Kategoriye Göre", "#10b981")
        for cat, cnt in cat_counts.most_common(10):
            st.markdown(f"**{cat}:** {cnt} soru")


# ══════════════════════════════════════════════════════════════════════════════
# 4) KONU BANKASI
# ══════════════════════════════════════════════════════════════════════════════

def _render_konu_bankasi(store: MatematikDataStore):
    """Konu bazlı problem bankası."""
    styled_section("📐 Konu Bankası", "#3b82f6")

    sub_tabs = st.tabs(["📚 Konulara Göz At", "➕ Problem Ekle", "🤖 Otomatik Üret"])

    with sub_tabs[0]:
        _render_konu_gozat(store)

    with sub_tabs[1]:
        _render_problem_ekle(store)

    with sub_tabs[2]:
        _render_otomatik_uret(store)


def _render_konu_gozat(store: MatematikDataStore):
    """Konulara göz at."""
    col1, col2, col3 = st.columns(3)
    with col1:
        grade_sel = st.selectbox("Sınıf", ["Tümü"] + list(SINIF_KONULARI.keys()),
                                 key="mat_kb_grade")
    with col2:
        cat_sel = st.selectbox("Kategori", ["Tümü"] + [e.value for e in MathCategory],
                               key="mat_kb_cat")
    with col3:
        diff_sel = st.selectbox("Zorluk", ["Tümü"] + [e.value for e in MathDifficulty],
                                key="mat_kb_diff")

    # Sınıf konularını göster
    if grade_sel != "Tümü" and grade_sel in SINIF_KONULARI:
        styled_section(f"📖 {grade_sel}. Sınıf Konuları", "#3b82f6")
        topics = SINIF_KONULARI[grade_sel]
        cols = st.columns(min(len(topics), 4))
        for i, topic in enumerate(topics):
            with cols[i % len(cols)]:
                _render_html(f"""
                <div class="mat-topic-card">
                    <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">📌 {topic}</div>
                    <div style="font-size:0.75rem;color:#94a3b8 !important;margin-top:4px">{grade_sel}. Sınıf</div>
                </div>
                """)

    st.markdown("---")

    # Problemler
    problems = store.get_problems(
        grade=grade_sel if grade_sel != "Tümü" else None,
        category=cat_sel if cat_sel != "Tümü" else None,
        difficulty=diff_sel if diff_sel != "Tümü" else None,
    )

    st.write(f"**{len(problems)} problem** bulundu")

    if not problems:
        st.info("Bu filtrelere uygun problem bulunamadı. Otomatik üretim veya manuel ekleme yapabilirsiniz.")
        return

    for p in problems[:20]:
        with st.expander(f"{'📌' if p.get('difficulty') == 'zor' else '📝'} {p.get('title', 'Problem')} — {_difficulty_badge(p.get('difficulty', 'orta'))}", expanded=False):
            st.markdown(p.get("body", ""))
            st.markdown(f"**Kategori:** {p.get('category', '')} | **Konu:** {p.get('topic', '')} | **Sınıf:** {p.get('grade', '')}")

            if p.get("hints"):
                st.markdown("**💡 İpuçları:**")
                for h in p["hints"]:
                    st.markdown(f"- {h}")

            if p.get("solution"):
                st.markdown(f"**📝 Çözüm:** {p['solution']}")
            st.markdown(f"**Cevap:** ||{p.get('answer', '')}||")


def _render_problem_ekle(store: MatematikDataStore):
    """Manuel problem ekleme."""
    styled_section("➕ Yeni Problem", "#10b981")

    with st.form("mat_prob_form"):
        title = st.text_input("Başlık", key="matematik__12")

        body = st.text_area("Problem Metni", height=200, key="matematik__m2")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            grade = st.selectbox("Sınıf", list(SINIF_KONULARI.keys()), key="mat_pe_grade")
        with col2:
            category = st.selectbox("Kategori", [e.value for e in MathCategory], key="mat_pe_cat")
        with col3:
            difficulty = st.selectbox("Zorluk", [e.value for e in MathDifficulty], key="mat_pe_diff")
        with col4:
            answer_type = st.selectbox("Cevap Tipi", ["numeric", "multiple_choice", "text", "proof"], key="matematik__13")


        topic = st.text_input("Alt Konu", key="matematik__14")

        answer = st.text_input("Doğru Cevap", key="matematik__15")

        solution = st.text_area("Çözüm Açıklaması", height=150, key="matematik__16")

        hints = st.text_area("İpuçları (satır satır)", height=80, key="matematik__17")


        if answer_type == "multiple_choice":
            options = st.text_input("Şıklar (virgülle ayır)", placeholder="A, B, C, D", key="matematik__18")

        else:
            options = ""

        xp = st.number_input("XP Ödülü", 5, 200, 10, key="matematik__19")


        submitted = st.form_submit_button("💾 Kaydet", type="primary")
        if submitted:
            if not title or not body:
                st.error("Başlık ve metin zorunludur!")
            else:
                p = MathProblem(
                    title=title, body=body,
                    category=category, difficulty=difficulty,
                    grade=grade, topic=topic,
                    answer=answer, answer_type=answer_type,
                    options=[o.strip() for o in options.split(",") if o.strip()] if options else [],
                    solution=solution,
                    hints=[h.strip() for h in hints.split("\n") if h.strip()],
                    xp_reward=xp,
                )
                store.add_problem(p)
                st.success(f"✅ Problem eklendi: **{title}**")
                st.rerun()


def _render_otomatik_uret(store: MatematikDataStore):
    """Otomatik problem üretimi."""
    styled_section("🤖 Otomatik Problem Üretimi", "#f59e0b")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        grade = st.selectbox("Sınıf", list(SINIF_KONULARI.keys()), key="mat_gen_grade", index=4)
    with col2:
        category = st.selectbox("Tür", ["Aritmetik", "Denklem", "Geometri"], key="mat_gen_type")
    with col3:
        difficulty = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="mat_gen_diff", index=1)
    with col4:
        count = st.number_input("Adet", 1, 50, 10, key="mat_gen_count")

    if st.button("🚀 Üret & Kaydet", key="mat_gen_go", type="primary"):
        gen = MathProblemGenerator()
        if category == "Aritmetik":
            problems = gen.generate_arithmetic(grade, difficulty, count)
        elif category == "Denklem":
            problems = gen.generate_equation(grade, difficulty, count)
        else:
            problems = gen.generate_geometry(grade, difficulty, count)

        for p in problems:
            store.add_problem(p)

        st.success(f"✅ {len(problems)} problem üretildi ve kaydedildi!")

        # Üretilenleri göster
        for p in problems[:5]:
            st.markdown(f"- **{p.title}**: {p.body} → Cevap: `{p.answer}`")
        if len(problems) > 5:
            st.caption(f"... ve {len(problems) - 5} problem daha")


# ══════════════════════════════════════════════════════════════════════════════
# 5) BULMACALAR & ZEKA
# ══════════════════════════════════════════════════════════════════════════════

def _render_bulmacalar(store: MatematikDataStore):
    """Bulmacalar ve zeka soruları."""
    styled_section("🧩 Bulmacalar & Zeka Soruları", "#06b6d4")

    _render_html("""
    <div style="background:linear-gradient(135deg,#0a1628,#1e3a5f);border-radius:16px;padding:20px;margin-bottom:20px;border:1px solid rgba(6,182,212,0.3)">
        <div style="font-weight:700;color:#cffafe !important;font-size:1.1rem;margin-bottom:6px">🧠 Beynini Çalıştır!</div>
        <div style="color:#67e8f9 !important;font-size:0.9rem">Mantık bulmacaları, geometrik zeka soruları, sayı dizileri ve daha fazlası.</div>
    </div>
    """)

    sub_tabs = st.tabs(["🧩 Bulmacalar", "🤖 Toplu Üret", "➕ Bulmaca Ekle", "🎲 Rastgele Meydan Okuma"])

    with sub_tabs[0]:
        _render_bulmaca_listesi(store)

    with sub_tabs[1]:
        _render_toplu_bulmaca_uret(store)

    with sub_tabs[2]:
        _render_bulmaca_ekle(store)

    with sub_tabs[3]:
        _render_rastgele_meydan_okuma(store)


def _render_toplu_bulmaca_uret(store: MatematikDataStore):
    """Toplu otomatik bulmaca üretimi — yüzlerce/binlerce bulmaca."""
    styled_section("🤖 Otomatik Bulmaca Üretici", "#8b5cf6")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1e0a3a,#4c1d95);border-radius:20px;padding:22px;margin-bottom:20px;
                 border:2px solid rgba(139,92,246,0.4);text-align:center">
        <div style="font-size:2.5rem;margin-bottom:8px" class="mat-grow">🤖⚡</div>
        <div style="font-weight:700;color:#e9d5ff !important;font-size:1.1rem">Sonsuz Bulmaca Fabrikası!</div>
        <div style="color:#c4b5fd !important;font-size:0.9rem">Bir tıkla yüzlerce benzersiz bulmaca üret — sayı dizisi, mantık, geometri, sözel problem!</div>
    </div>
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        tur = st.selectbox("Bulmaca Türü", [
            ("karisik", "🔀 Karışık (Her Türden)"),
            ("dizi", "🔢 Sayı Dizisi"),
            ("mantik", "🧩 Mantık Bulmacası"),
            ("geometrik", "📐 Geometrik"),
            ("sozel", "📝 Sözel Problem"),
        ], key="btu_tur", format_func=lambda x: x[1])
    with col2:
        zorluk = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="btu_zor", index=1,
                               format_func=lambda x: {"kolay": "🌱 Kolay", "orta": "🌿 Orta", "zor": "🌳 Zor"}[x])
    with col3:
        adet = st.selectbox("Adet", [10, 25, 50, 100, 250, 500, 1000], key="btu_adet", index=2)

    col1, col2 = st.columns([3, 1])
    with col1:
        kaydet = st.checkbox("Oluşturulanları veritabanına kaydet", value=True, key="btu_kaydet")
    with col2:
        mevcut = len(store.get_puzzles())
        _render_html(f"""
        <div style="text-align:center;background:#0f172a;border-radius:10px;padding:8px;
                     border:1px solid rgba(99,102,241,0.15)">
            <div style="font-weight:700;color:#818cf8 !important;font-size:1.3rem">{mevcut}</div>
            <div style="font-size:0.7rem;color:#94a3b8 !important">Mevcut Bulmaca</div>
        </div>
        """)

    if st.button(f"🚀 {adet} Bulmaca Üret!", key="btu_go", type="primary"):
        with st.spinner(f"🤖 {adet} bulmaca üretiliyor..."):
            gen = PuzzleGenerator()
            puzzles = gen.generate_bulk(tur[0], zorluk, adet)

        if kaydet:
            for pz in puzzles:
                store.add_puzzle(pz)

        st.session_state["btu_sonuc"] = puzzles

        # Özet istatistikler
        from collections import Counter
        tip_sayim = Counter(p.puzzle_type for p in puzzles)
        zorluk_sayim = Counter(p.difficulty for p in puzzles)

        _render_html(f"""
        <div style="background:linear-gradient(135deg,#052e16,#065f46);border-radius:16px;padding:20px;margin:16px 0;
                     border:2px solid rgba(16,185,129,0.4);text-align:center">
            <div style="font-size:2rem;margin-bottom:8px">✅</div>
            <div style="font-weight:800;color:#bbf7d0 !important;font-size:1.2rem">{len(puzzles)} Bulmaca Üretildi!</div>
            <div style="color:#86efac !important;font-size:0.9rem;margin-top:8px">
                {'✅ Veritabanına kaydedildi' if kaydet else '📋 Önizleme modu (kaydedilmedi)'}
            </div>
        </div>
        """)

        # Tür dağılımı
        cols = st.columns(len(tip_sayim))
        tip_emojiler = {"dizi": "🔢", "mantik": "🧩", "geometrik": "📐", "sozel": "📝"}
        tip_adlar = {"dizi": "Sayı Dizisi", "mantik": "Mantık", "geometrik": "Geometrik", "sozel": "Sözel"}
        for col, (tip, cnt) in zip(cols, tip_sayim.most_common()):
            with col:
                _render_html(f"""
                <div class="mat-stat-card" style="padding:12px">
                    <div style="font-size:1.5rem">{tip_emojiler.get(tip, '🧩')}</div>
                    <div style="font-weight:700;color:#818cf8 !important;font-size:1.3rem">{cnt}</div>
                    <div style="font-size:0.7rem;color:#94a3b8 !important">{tip_adlar.get(tip, tip)}</div>
                </div>
                """)

    # Üretilenleri göster
    if "btu_sonuc" in st.session_state:
        puzzles = st.session_state["btu_sonuc"]
        styled_section(f"📋 Üretilen Bulmacalar ({len(puzzles)} adet)", "#6366f1")

        # Sayfa sistemi
        sayfa_boyut = 10
        toplam_sayfa = max(1, (len(puzzles) + sayfa_boyut - 1) // sayfa_boyut)
        sayfa = st.selectbox("Sayfa", list(range(1, toplam_sayfa + 1)), key="btu_sayfa",
                              format_func=lambda x: f"Sayfa {x}/{toplam_sayfa}")

        baslangic = (sayfa - 1) * sayfa_boyut
        bitis = min(baslangic + sayfa_boyut, len(puzzles))

        tip_emojiler = {"dizi": "🔢", "mantik": "🧩", "geometrik": "📐", "sozel": "📝"}

        for idx, pz in enumerate(puzzles[baslangic:bitis], start=baslangic + 1):
            tip_emoji = tip_emojiler.get(pz.puzzle_type, "🧩")
            with st.expander(f"{tip_emoji} #{idx} — {pz.title}", expanded=False):
                st.markdown(pz.body)
                st.markdown(f"**Cevap:** ||{pz.answer}||")
                if pz.explanation:
                    st.caption(f"💡 {pz.explanation}")
                st.caption(f"Tür: {pz.puzzle_type} • Zorluk: {pz.difficulty} • Sınıf: {pz.grade_range} • {pz.xp_reward} XP")


def _render_bulmaca_listesi(store: MatematikDataStore):
    """Bulmaca listesi."""
    col1, col2 = st.columns(2)
    with col1:
        p_type = st.selectbox("Bulmaca Türü", ["Tümü", "mantik", "geometrik", "sayisal", "sozel", "dizi"],
                              key="mat_pz_type",
                              format_func=lambda x: {
                                  "Tümü": "Tümü", "mantik": "🧠 Mantık",
                                  "geometrik": "📐 Geometrik", "sayisal": "🔢 Sayısal",
                                  "sozel": "📝 Sözel", "dizi": "🔗 Dizi/Örüntü"
                              }.get(x, x))
    with col2:
        p_diff = st.selectbox("Zorluk", ["Tümü", "kolay", "orta", "zor"],
                              key="mat_pz_diff")

    puzzles = store.get_puzzles(
        puzzle_type=p_type if p_type != "Tümü" else None,
        difficulty=p_diff if p_diff != "Tümü" else None,
    )

    if not puzzles:
        st.info("Henüz bulmaca eklenmemiş. Hazır örnek bulmacaları yükleyebilirsiniz!")
        if st.button("🚀 Örnek Bulmacaları Yükle (7 Bulmaca)", key="mat_pz_seed", type="primary"):
            for pb in ORNEK_BULMACALAR:
                pz = PuzzleRecord(
                    title=pb["title"], body=pb["body"],
                    puzzle_type=pb.get("puzzle_type", "mantik"),
                    difficulty=pb.get("difficulty", "orta"),
                    grade_range=pb.get("grade_range", "5-12"),
                    answer=pb.get("answer", ""),
                    explanation=pb.get("explanation", ""),
                    xp_reward=pb.get("xp_reward", 20),
                )
                store.add_puzzle(pz)
            st.success(f"✅ {len(ORNEK_BULMACALAR)} bulmaca yüklendi!")
            st.rerun()
        return

    for p in puzzles[:20]:
        type_labels = {"mantik": "🧠 Mantık", "geometrik": "📐 Geometrik",
                       "sayisal": "🔢 Sayısal", "sozel": "📝 Sözel", "dizi": "🔗 Dizi"}
        _render_html(f"""
        <div class="mat-puzzle-card">
            <div class="puzzle-type">{type_labels.get(p.get('puzzle_type', ''), '🧩')}</div>
            <div style="font-weight:700;color:#e0e7ff !important;margin-bottom:8px">{p.get('title', 'Bulmaca')}</div>
            <div style="color:#94a3b8 !important;line-height:1.6">{p.get('body', '')}</div>
            <div style="margin-top:10px">
                {_difficulty_badge(p.get('difficulty', 'orta'))} {_xp_badge(p.get('xp_reward', 20))}
            </div>
        </div>
        """)
        with st.expander(f"💡 Cevap & Açıklama", expanded=False):
            st.markdown(f"**Cevap:** {p.get('answer', '')}")
            if p.get("explanation"):
                st.markdown(f"**Açıklama:** {p['explanation']}")


def _render_bulmaca_ekle(store: MatematikDataStore):
    """Bulmaca ekleme formu."""
    styled_section("➕ Yeni Bulmaca", "#06b6d4")

    with st.form("mat_pz_form"):
        title = st.text_input("Başlık", key="matematik__21")

        body = st.text_area("Bulmaca Metni", height=200, key="matematik__22")


        col1, col2, col3 = st.columns(3)
        with col1:
            puzzle_type = st.selectbox("Tür", ["mantik", "geometrik", "sayisal", "sozel", "dizi"],
                                       key="mat_pze_type")
        with col2:
            difficulty = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="mat_pze_diff")
        with col3:
            grade_range = st.text_input("Sınıf Aralığı", value="5-12", key="matematik__23")


        answer = st.text_input("Cevap", key="matematik__24")

        explanation = st.text_area("Açıklama", height=100, key="matematik__25")

        hints = st.text_area("İpuçları (satır satır)", height=80, key="matematik__26")

        xp = st.number_input("XP Ödülü", 5, 100, 20, key="matematik__27")


        submitted = st.form_submit_button("💾 Kaydet", type="primary")
        if submitted:
            if not title or not body:
                st.error("Başlık ve metin zorunludur!")
            else:
                pz = PuzzleRecord(
                    title=title, body=body,
                    puzzle_type=puzzle_type, difficulty=difficulty,
                    grade_range=grade_range, answer=answer,
                    explanation=explanation,
                    hints=[h.strip() for h in hints.split("\n") if h.strip()],
                    xp_reward=xp,
                )
                store.add_puzzle(pz)
                st.success(f"✅ Bulmaca eklendi: **{title}**")
                st.rerun()


def _render_rastgele_meydan_okuma(store: MatematikDataStore):
    """Rastgele bir meydan okuma oluştur."""
    styled_section("🎲 Rastgele Meydan Okuma", "#ef4444")

    difficulty = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="mat_rnd_diff", index=1)

    if st.button("🎲 Meydan Okuma!", key="mat_rnd_go", type="primary"):
        gen = MathProblemGenerator()
        func = random.choice([gen.generate_arithmetic, gen.generate_equation, gen.generate_geometry])
        grade = str(random.randint(5, 10))
        problems = func(grade, difficulty, 1)

        if problems:
            p = problems[0]
            st.session_state["mat_rnd_problem"] = p

    if "mat_rnd_problem" in st.session_state:
        p = st.session_state["mat_rnd_problem"]
        _render_html(f"""
        <div class="mat-daily-challenge">
            <div style="font-weight:700;color:#fca5a5 !important;font-size:1.1rem;margin-bottom:12px;position:relative;z-index:1">
                🎲 {p.title}
            </div>
            <div style="color:#e0e7ff !important;font-size:1.1rem;line-height:1.6;position:relative;z-index:1">
                {p.body}
            </div>
            <div style="margin-top:12px;position:relative;z-index:1">
                {_difficulty_badge(p.difficulty)} {_xp_badge(p.xp_reward)}
            </div>
        </div>
        """)

        user_ans = st.text_input("Cevabın:", key="mat_rnd_ans")
        if st.button("Kontrol Et", key="mat_rnd_check"):
            if user_ans.strip() == str(p.answer).strip():
                st.success("🎉 Harika! Doğru cevap!")
                st.balloons()
            else:
                st.error(f"❌ Yanlış! Doğru cevap: **{p.answer}**")


# ══════════════════════════════════════════════════════════════════════════════
# 6) YARIŞMALAR
# ══════════════════════════════════════════════════════════════════════════════

def _render_yarisma(store: MatematikDataStore):
    """Yarışma ve turnuva yönetimi."""
    styled_section("🏅 Matematik Yarışmaları", "#10b981")

    _render_html("""
    <div style="background:linear-gradient(135deg,#0c1a0c,#1a3d1a);border-radius:16px;padding:20px;margin-bottom:20px;border:1px solid rgba(34,197,94,0.3)">
        <div style="font-weight:700;color:#bbf7d0 !important;font-size:1.1rem;margin-bottom:6px">🏆 Yarış, Kazan, Öğren!</div>
        <div style="color:#86efac !important;font-size:0.9rem">Okul içi matematik yarışmaları düzenle, katıl ve sıralamalarda yüksel!</div>
    </div>
    """)

    sub_tabs = st.tabs(["⚡ Hızlı Yarışma", "📋 Aktif Yarışmalar", "➕ Yarışma Oluştur", "🏆 Geçmiş Yarışmalar"])

    with sub_tabs[0]:
        _render_hizli_yarisma(store)
    with sub_tabs[1]:
        _render_aktif_yarismalar(store)
    with sub_tabs[2]:
        _render_yarisma_olustur(store)
    with sub_tabs[3]:
        _render_gecmis_yarismalar(store)


def _render_hizli_yarisma(store: MatematikDataStore):
    """Hızlı yarışma — anında başlat, otomatik soru üretimli, süreli."""
    import random as _r, time
    styled_section("⚡ Hızlı Yarışma Başlat", "#10b981")

    col1, col2, col3 = st.columns(3)
    with col1:
        yr_sinif = st.selectbox("Sınıf", list(SINIF_KONULARI.keys()), key="yr_sinif", index=4)
    with col2:
        yr_tur = st.selectbox("Tür", ["Karışık", "Aritmetik", "Denklem", "Geometri"], key="yr_tur")
    with col3:
        yr_sure = st.selectbox("Süre", [60, 120, 180, 300], key="yr_sure",
                                format_func=lambda x: f"{x//60} dk")

    yr_key = "yr_state"

    if st.button("🏁 Yarışmayı Başlat!", key="yr_start", type="primary"):
        gen = MathProblemGenerator()
        sorular = []
        for _ in range(50):
            if yr_tur == "Aritmetik":
                ps = gen.generate_arithmetic(yr_sinif, "orta", 1)
            elif yr_tur == "Denklem":
                ps = gen.generate_equation(yr_sinif, "orta", 1)
            elif yr_tur == "Geometri":
                ps = gen.generate_geometry(yr_sinif, "orta", 1)
            else:
                func = _r.choice([gen.generate_arithmetic, gen.generate_equation, gen.generate_geometry])
                ps = func(yr_sinif, "orta", 1)
            if ps:
                p = ps[0]
                sorular.append({"soru": p.body, "cevap": str(p.answer), "xp": p.xp_reward})

        st.session_state[yr_key] = {
            "sorular": sorular, "current": 0, "dogru": 0, "yanlis": 0,
            "start": time.time(), "sure_limit": yr_sure, "bitti": False,
        }
        st.rerun()

    if yr_key in st.session_state:
        state = st.session_state[yr_key]
        elapsed = time.time() - state.get("start", time.time())
        kalan = max(0, state.get("sure_limit", 120) - elapsed)
        cur = state.get("current", 0)
        sorular = state.get("sorular", [])
        d = state.get("dogru", 0)
        y = state.get("yanlis", 0)

        if kalan <= 0 or state.get("bitti"):
            # Yarışma bitti
            toplam = d + y
            oran = (d / toplam * 100) if toplam > 0 else 0
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#052e16,#065f46);border-radius:24px;padding:32px;
                         margin:16px 0;text-align:center;border:2px solid rgba(16,185,129,0.4)">
                <div style="font-size:3rem;margin-bottom:12px">{'🏆' if oran>=80 else '🥈' if oran>=60 else '🥉'}</div>
                <div style="font-size:1.5rem;font-weight:800;color:#bbf7d0 !important">Yarışma Tamamlandı!</div>
                <div style="display:flex;justify-content:center;gap:30px;margin-top:16px;flex-wrap:wrap">
                    <div><div style="font-size:2.2rem;font-weight:900;color:#10b981 !important">{d}</div><div style="font-size:0.75rem;color:#94a3b8 !important">Doğru</div></div>
                    <div><div style="font-size:2.2rem;font-weight:900;color:#ef4444 !important">{y}</div><div style="font-size:0.75rem;color:#94a3b8 !important">Yanlış</div></div>
                    <div><div style="font-size:2.2rem;font-weight:900;color:#f59e0b !important">%{oran:.0f}</div><div style="font-size:0.75rem;color:#94a3b8 !important">Başarı</div></div>
                    <div><div style="font-size:2.2rem;font-weight:900;color:#6366f1 !important">{elapsed:.0f}s</div><div style="font-size:0.75rem;color:#94a3b8 !important">Süre</div></div>
                </div>
            </div>
            """)
            if st.button("🔄 Yeni Yarışma!", key="yr_reset"):
                del st.session_state[yr_key]
                st.rerun()
        elif cur < len(sorular):
            s = sorular[cur]
            _render_html(f"""
            <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="color:#10b981 !important;font-weight:700">✅{d} ❌{y}</span>
                <span style="color:#94a3b8 !important">Soru {cur+1}</span>
                <span style="color:{'#ef4444' if kalan<15 else '#f59e0b'} !important;font-weight:700;font-size:1.2rem">⏱️ {kalan:.0f}s</span>
            </div>
            """)
            st.progress(min(elapsed / state.get("sure_limit", 120), 1.0))
            st.markdown(s["soru"])
            ans = st.text_input("Cevabın:", key=f"yr_ans_{cur}")
            if st.button("✅ Cevapla", key=f"yr_chk_{cur}"):
                if ans.strip() == s["cevap"].strip():
                    state["dogru"] = d + 1
                else:
                    state["yanlis"] = y + 1
                state["current"] = cur + 1
                st.rerun()


def _render_aktif_yarismalar(store: MatematikDataStore):
    """Aktif yarışmalar."""
    competitions = store.get_competitions(status="aktif")

    if not competitions:
        st.info("Şu anda aktif yarışma yok. Yeni bir yarışma oluşturabilirsiniz!")
        return

    for comp in competitions:
        participant_count = len(comp.get("participants", []))
        _render_html(f"""
        <div class="mat-competition-card">
            <div style="font-weight:700;color:#bbf7d0 !important;font-size:1.1rem;margin-bottom:8px">🏆 {comp.get('name', '')}</div>
            <div style="color:#86efac !important;font-size:0.9rem;margin-bottom:12px">{comp.get('description', '')}</div>
            <div style="display:flex;gap:20px;flex-wrap:wrap">
                <span style="color:#94a3b8 !important;font-size:0.85rem">📅 {comp.get('start_date', '')} — {comp.get('end_date', '')}</span>
                <span style="color:#94a3b8 !important;font-size:0.85rem">⏱️ {comp.get('time_limit_min', 60)} dk</span>
                <span style="color:#94a3b8 !important;font-size:0.85rem">👥 {participant_count} katılımcı</span>
                <span style="color:#94a3b8 !important;font-size:0.85rem">🎯 Sınıf: {comp.get('grade_range', '')}</span>
                {_difficulty_badge(comp.get('difficulty', 'orta'))}
            </div>
        </div>
        """)


def _render_yarisma_olustur(store: MatematikDataStore):
    """Yarışma oluşturma formu."""
    styled_section("➕ Yeni Yarışma", "#10b981")

    with st.form("mat_comp_form"):
        name = st.text_input("Yarışma Adı", key="matematik__28")

        description = st.text_area("Açıklama", height=100, key="matematik__29")


        col1, col2, col3 = st.columns(3)
        with col1:
            comp_type = st.selectbox("Tür", ["bireysel", "takim", "sinif"],
                                      format_func=lambda x: {"bireysel": "🧑 Bireysel", "takim": "👥 Takım", "sinif": "🏫 Sınıf"}.get(x, x), key="matematik__m3")
        with col2:
            grade_range = st.text_input("Sınıf Aralığı", value="5-8", key="matematik__m4")
        with col3:
            difficulty = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="mat_comp_diff")

        col1, col2, col3 = st.columns(3)
        with col1:
            time_limit = st.number_input("Süre (dk)", 15, 180, 60, key="matematik__m5")
        with col2:
            start_date = st.date_input("Başlangıç", key="mat_comp_start")
        with col3:
            end_date = st.date_input("Bitiş", key="mat_comp_end")

        prizes = st.text_input("Ödüller (virgülle ayır)", placeholder="🥇 1., 🥈 2., 🥉 3.", key="matematik__31")


        submitted = st.form_submit_button("🏆 Yarışma Oluştur", type="primary")
        if submitted:
            if not name:
                st.error("Yarışma adı zorunludur!")
            else:
                comp = Competition(
                    name=name, description=description,
                    competition_type=comp_type,
                    grade_range=grade_range,
                    difficulty=difficulty,
                    time_limit_min=time_limit,
                    start_date=str(start_date),
                    end_date=str(end_date),
                    status="aktif",
                    prizes=[p.strip() for p in prizes.split(",") if p.strip()],
                )
                store.add_competition(comp)
                st.success(f"✅ Yarışma oluşturuldu: **{name}**")
                st.rerun()


def _render_gecmis_yarismalar(store: MatematikDataStore):
    """Geçmiş yarışmalar."""
    competitions = store.get_competitions(status="tamamlandi")

    if not competitions:
        st.info("Henüz tamamlanmış yarışma yok.")
        return

    for comp in competitions:
        results = comp.get("results", [])
        _render_html(f"""
        <div class="mat-competition-card" style="opacity:0.8">
            <div style="font-weight:700;color:#bbf7d0 !important;font-size:1rem;margin-bottom:6px">✅ {comp.get('name', '')}</div>
            <div style="color:#94a3b8 !important;font-size:0.85rem">{comp.get('start_date', '')} — {comp.get('end_date', '')} • {len(results)} sonuç</div>
        </div>
        """)


# ══════════════════════════════════════════════════════════════════════════════
# 7) İLERLEME TAKİBİ
# ══════════════════════════════════════════════════════════════════════════════

def _render_ilerleme(store: MatematikDataStore):
    """Öğrenci ilerleme takibi."""
    styled_section("📊 İlerleme Takibi", "#8b5cf6")

    sub_tabs = st.tabs(["👤 Profil", "🏆 Başarımlar", "📈 Liderlik Tablosu", "📅 Günlük Log", "📊 Veri Analizi Raporu"])

    with sub_tabs[0]:
        _render_profil(store)

    with sub_tabs[1]:
        _render_basarimlar(store)

    with sub_tabs[2]:
        _render_liderlik(store)

    with sub_tabs[3]:
        _render_gunluk_log(store)

    with sub_tabs[4]:
        _render_veri_analizi(store)


def _render_profil(store: MatematikDataStore):
    """Öğrenci profil özeti — giriş yapan kullanıcıyla otomatik bağlı."""
    profiles = store.get_profiles()

    if not profiles:
        st.info("Henüz öğrenci profili yok. Oyun oynayın veya problem çözün, profiliniz otomatik oluşsun!")
        return

    # Giriş yapan kullanıcıyı otomatik bul
    auth_user = st.session_state.get("auth_user", {})
    current_username = auth_user.get("username", "")

    profile_options = {p.get("student_id", ""): f"{p.get('student_name', 'Bilinmiyor')} ({p.get('grade', '')}. sınıf)"
                       for p in profiles}

    # Otomatik eşleştirme: giriş yapan kullanıcının profilini varsayılan seç
    default_idx = 0
    if current_username:
        for i, pid in enumerate(profile_options.keys()):
            if pid == current_username:
                default_idx = i
                break

    selected_id = st.selectbox("Öğrenci Seç", list(profile_options.keys()),
                                format_func=lambda x: profile_options.get(x, x),
                                key="mat_prof_sel", index=default_idx)

    profile_data = store.get_profile(selected_id)
    if not profile_data:
        return

    profile = StudentMathProfile.from_dict(profile_data)
    level_info = profile.get_level_info()

    # Profil kartı
    current = level_info["current"]
    next_lvl = level_info["next"]
    progress = level_info["progress"]

    _render_html(f"""
    <div class="mat-hero" style="margin-bottom:20px">
        <div style="display:flex;align-items:center;gap:20px;position:relative;z-index:1">
            <div style="font-size:3.5rem">{current['rozet']}</div>
            <div>
                <div style="font-size:1.5rem;font-weight:800;color:#e0e7ff !important">{profile.student_name}</div>
                <div style="color:#a5b4fc !important;font-size:0.9rem">Seviye {current['seviye']} — {current['ad']}</div>
                <div style="color:#eab308 !important;font-weight:700;margin-top:4px">⭐ {profile.total_xp} XP</div>
            </div>
        </div>
        <div style="margin-top:16px;position:relative;z-index:1">
            <div class="mat-level-bar">
                <div class="mat-level-fill" style="width:{progress:.0f}%"></div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:4px;font-size:0.75rem;color:#94a3b8 !important">
                <span>Seviye {current['seviye']}</span>
                <span>{f"Sonraki: {next_lvl['ad']} ({next_lvl['min_xp']} XP)" if next_lvl else "Maksimum Seviye!"}</span>
            </div>
        </div>
    </div>
    """)

    # İstatistik kartları
    cols = st.columns(5)
    stats = [
        ("📚", str(profile.total_problems_solved), "Çözülen"),
        ("✅", f"%{profile.accuracy:.0f}", "Doğruluk"),
        ("🎮", str(profile.total_games_played), "Oyun"),
        ("🔥", str(profile.current_streak), "Seri (Gün)"),
        ("🏅", str(len(profile.achievements)), "Başarım"),
    ]
    for col, (icon, val, label) in zip(cols, stats):
        with col:
            _render_html(f"""
            <div class="mat-stat-card">
                <div class="mat-stat-icon">{icon}</div>
                <div class="mat-stat-value">{val}</div>
                <div class="mat-stat-label">{label}</div>
            </div>
            """)

    # Kategori bazlı istatistikler
    if profile.category_stats:
        st.markdown("---")
        styled_section("📊 Kategori Performansı", "#3b82f6")
        for cat, stats_data in profile.category_stats.items():
            solved = stats_data.get("solved", 0)
            correct = stats_data.get("correct", 0)
            acc = (correct / solved * 100) if solved > 0 else 0
            st.progress(acc / 100, text=f"**{cat}** — {correct}/{solved} doğru (%{acc:.0f})")


def _render_basarimlar(store: MatematikDataStore):
    """Başarım sistemi."""
    styled_section("🏆 Başarımlar", "#eab308")

    # Profil seçimi
    profiles = store.get_profiles()
    earned_ids = set()

    if profiles:
        profile_options = {p.get("student_id", ""): p.get("student_name", "")
                           for p in profiles}
        sel = st.selectbox("Öğrenci", list(profile_options.keys()),
                           format_func=lambda x: profile_options.get(x, x),
                           key="mat_ach_sel")
        prof = store.get_profile(sel)
        if prof:
            earned_ids = set(prof.get("achievements", []))

    kazanilan = len(earned_ids)
    toplam = len(BASARIM_TANIMLARI)
    oran = (kazanilan / toplam * 100) if toplam > 0 else 0

    # İlerleme özet
    _render_html(f"""
    <div style="background:linear-gradient(135deg,#451a03,#78350f);border-radius:16px;padding:18px;margin-bottom:16px;
                 border:2px solid rgba(234,179,8,0.3);text-align:center">
        <div style="font-size:2rem;margin-bottom:6px">🏆</div>
        <div style="font-size:1.5rem;font-weight:900;color:#eab308 !important">{kazanilan}/{toplam}</div>
        <div style="font-size:0.8rem;color:#fcd34d !important">Başarım Kazanıldı (%{oran:.0f})</div>
        <div style="max-width:300px;margin:8px auto;background:#1e1b4b;border-radius:8px;height:10px;overflow:hidden">
            <div style="width:{oran:.0f}%;height:100%;background:linear-gradient(90deg,#eab308,#f59e0b);border-radius:8px"></div>
        </div>
    </div>
    """)

    # Rozet kategorileri
    kategoriler = {"toplam": "📚 Çözüm", "seri": "🔥 Seri", "hiz": "⚡ Hız",
                   "dogruluk": "🎯 Doğruluk", "olimpiyat": "🏅 Olimpiyat",
                   "oyun": "🎮 Oyun", "kesfetme": "🔍 Keşif", "yarismaci": "🏆 Yarışma"}

    for kat_key, kat_ad in kategoriler.items():
        kat_basarimlar = [a for a in BASARIM_TANIMLARI if a.get("tip") == kat_key]
        if not kat_basarimlar:
            continue
        kat_kazanilan = sum(1 for a in kat_basarimlar if a["id"] in earned_ids)
        styled_section(f"{kat_ad} ({kat_kazanilan}/{len(kat_basarimlar)})", "#eab308")

        for ach in kat_basarimlar:
            is_earned = ach["id"] in earned_ids
            rozet_emoji = ach['ad'].split(' ')[0]
            _render_html(f"""
            <div style="background:{'linear-gradient(135deg,#1a1a2e,#2d2506)' if is_earned else '#0f172a'};
                         border-radius:14px;padding:12px 16px;margin-bottom:6px;
                         border:{'2px solid #eab308' if is_earned else '1px solid rgba(99,102,241,0.1)'};
                         display:flex;align-items:center;gap:14px;
                         {'box-shadow:0 0 12px rgba(234,179,8,0.15)' if is_earned else ''}">
                <div style="font-size:2rem;min-width:40px;text-align:center;
                             {'filter:none' if is_earned else 'filter:grayscale(1) opacity(0.4)'}">{rozet_emoji}</div>
                <div style="flex:1">
                    <div style="font-weight:700;color:{'#fde68a' if is_earned else '#64748b'} !important;font-size:0.9rem">
                        {'✅ ' if is_earned else '🔒 '}{ach['ad']}
                    </div>
                    <div style="font-size:0.78rem;color:#94a3b8 !important">{ach['aciklama']}</div>
                </div>
                <div style="text-align:right">
                    <div style="font-weight:700;color:{'#eab308' if is_earned else '#475569'} !important;font-size:0.85rem">+{ach['puan']} XP</div>
                </div>
            </div>
            """)


def _render_liderlik(store: MatematikDataStore):
    """Liderlik tablosu (detaylı)."""
    styled_section("📈 Genel Liderlik Tablosu", "#6366f1")

    col1, col2 = st.columns(2)
    with col1:
        grade_f = st.selectbox("Sınıf Filtresi", ["Tümü"] + list(SINIF_KONULARI.keys()),
                               key="mat_lb_grade")
    with col2:
        metric = st.selectbox("Sıralama Kriteri",
                              ["xp", "accuracy", "streak", "solved"],
                              key="mat_lb_metric",
                              format_func=lambda x: {
                                  "xp": "⭐ XP", "accuracy": "🎯 Doğruluk",
                                  "streak": "🔥 Seri", "solved": "📚 Çözülen"
                              }.get(x, x))

    lb = LeaderboardManager(store)
    leaders = lb.get_leaderboard(
        grade=grade_f if grade_f != "Tümü" else None,
        metric=metric, limit=20,
    )

    if not leaders:
        st.info("Henüz liderlik tablosu verisi yok.")
        return

    for entry in leaders:
        rank_icon = _rank_display(entry["rank"])
        rank_class = "gold" if entry["rank"] == 1 else "silver" if entry["rank"] == 2 else "bronze" if entry["rank"] == 3 else ""

        _render_html(f"""
        <div class="mat-leaderboard-row {'top-3' if entry['rank'] <= 3 else ''}">
            <div class="mat-rank {rank_class}" style="font-size:1.4rem">{rank_icon}</div>
            <div style="flex:1">
                <div style="font-weight:700;color:#e0e7ff !important">{entry['student_name'] or 'Öğrenci'}</div>
                <div style="font-size:0.75rem;color:#94a3b8 !important">{entry['grade']}. sınıf • Seviye {entry['level']} • 🏅 {entry['achievements']} başarım</div>
            </div>
            <div style="text-align:right">
                <div style="font-weight:700;color:#eab308 !important">{entry['xp']} XP</div>
                <div style="font-size:0.75rem;color:#94a3b8 !important">📚 {entry['solved']} • 🎯 %{entry['accuracy']} • 🔥 {entry['streak']} gün</div>
            </div>
        </div>
        """)


def _render_gunluk_log(store: MatematikDataStore):
    """Günlük çalışma logu."""
    styled_section("📅 Günlük Çalışma Logu", "#f59e0b")

    profiles = store.get_profiles()
    if not profiles:
        st.info("Henüz veri yok.")
        return

    profile_options = {p.get("student_id", ""): p.get("student_name", "")
                       for p in profiles}
    sel = st.selectbox("Öğrenci", list(profile_options.keys()),
                       format_func=lambda x: profile_options.get(x, x),
                       key="mat_log_sel")

    prof = store.get_profile(sel)
    if not prof:
        return

    daily_log = prof.get("daily_log", {})
    if not daily_log:
        st.info("Bu öğrenci için günlük log bulunmuyor.")
        return

    # Son 30 günü göster
    sorted_dates = sorted(daily_log.keys(), reverse=True)[:30]

    for date_str in sorted_dates:
        log = daily_log[date_str]
        solved = log.get("solved", 0)
        correct = log.get("correct", 0)
        xp = log.get("xp", 0)
        acc = (correct / solved * 100) if solved > 0 else 0

        _render_html(f"""
        <div class="mat-leaderboard-row">
            <div style="min-width:90px;font-weight:600;color:#a5b4fc !important">{date_str}</div>
            <div style="flex:1;display:flex;gap:20px">
                <span style="color:#e0e7ff !important">📚 {solved} çözüm</span>
                <span style="color:#10b981 !important">✅ {correct} doğru</span>
                <span style="color:#f59e0b !important">🎯 %{acc:.0f}</span>
                <span style="color:#eab308 !important">⭐ {xp} XP</span>
            </div>
        </div>
        """)


# ══════════════════════════════════════════════════════════════════════════════
def _render_veri_analizi(store: MatematikDataStore):
    """Veri analizi raporu — öğretmen/veli görünümü."""
    styled_section("📊 Veri Analizi & Öğretmen Raporu", "#6366f1")

    profiles = store.get_profiles()
    stats = store.get_dashboard_stats()

    if not profiles:
        st.info("Henüz öğrenci verisi yok. Öğrenciler oyun oynayıp problem çözdükçe veriler burada analiz edilecek.")
        return

    # Genel özet
    _render_html(f"""
    <div style="background:linear-gradient(135deg,#1e0a3a,#4c1d95);border-radius:20px;padding:24px;margin-bottom:20px;
                 border:2px solid rgba(99,102,241,0.3);text-align:center">
        <div style="font-size:1.2rem;font-weight:700;color:#e9d5ff !important;margin-bottom:12px">📊 Genel Platform İstatistikleri</div>
        <div style="display:flex;justify-content:center;gap:24px;flex-wrap:wrap">
            <div><div style="font-size:2rem;font-weight:900;color:#818cf8 !important">{stats['total_problems']}</div><div style="font-size:0.7rem;color:#94a3b8 !important">Problem</div></div>
            <div><div style="font-size:2rem;font-weight:900;color:#10b981 !important">{stats['total_solved']}</div><div style="font-size:0.7rem;color:#94a3b8 !important">Çözülen</div></div>
            <div><div style="font-size:2rem;font-weight:900;color:#f59e0b !important">%{stats['overall_accuracy']:.0f}</div><div style="font-size:0.7rem;color:#94a3b8 !important">Doğruluk</div></div>
            <div><div style="font-size:2rem;font-weight:900;color:#ec4899 !important">{stats['total_profiles']}</div><div style="font-size:0.7rem;color:#94a3b8 !important">Öğrenci</div></div>
            <div><div style="font-size:2rem;font-weight:900;color:#06b6d4 !important">{stats['total_games']}</div><div style="font-size:0.7rem;color:#94a3b8 !important">Oyun</div></div>
        </div>
    </div>
    """)

    # Öğrenci bazlı analiz
    styled_section("👤 Öğrenci Bazlı Analiz", "#10b981")
    profile_options = {p.get("student_id", ""): f"{p.get('student_name', '?')} ({p.get('grade', '')}. sınıf)"
                       for p in profiles}
    sel_id = st.selectbox("Öğrenci Seç", list(profile_options.keys()),
                           format_func=lambda x: profile_options.get(x, x), key="va_sel")

    prof = store.get_profile(sel_id)
    if not prof:
        return

    p = StudentMathProfile.from_dict(prof)
    level_info = p.get_level_info()

    col1, col2 = st.columns([2, 1])
    with col1:
        # Kategori performans tablosu
        styled_section("📐 Kategori Performansı", "#3b82f6")
        if p.category_stats:
            for cat, cs in p.category_stats.items():
                solved = cs.get("solved", 0)
                correct = cs.get("correct", 0)
                acc = (correct / solved * 100) if solved > 0 else 0
                bar_renk = "#10b981" if acc >= 70 else "#f59e0b" if acc >= 40 else "#ef4444"
                _render_html(f"""
                <div style="background:#0f172a;border-radius:10px;padding:10px 14px;margin-bottom:4px;
                             border:1px solid rgba(99,102,241,0.08)">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                        <span style="font-weight:600;color:#e0e7ff !important;font-size:0.85rem">{cat}</span>
                        <span style="font-weight:700;color:{bar_renk} !important;font-size:0.85rem">{correct}/{solved} • %{acc:.0f}</span>
                    </div>
                    <div style="background:#1e1b4b;border-radius:6px;height:6px;overflow:hidden">
                        <div style="width:{acc:.0f}%;height:100%;background:{bar_renk};border-radius:6px"></div>
                    </div>
                </div>
                """)
        else:
            st.caption("Henüz kategori verisi yok.")

    with col2:
        # Özet kart
        current = level_info["current"]
        _render_html(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:16px;padding:18px;text-align:center;
                     border:1px solid rgba(99,102,241,0.15)">
            <div style="font-size:2.5rem;margin-bottom:6px">{current['rozet']}</div>
            <div style="font-weight:700;color:#e0e7ff !important;font-size:1rem">{p.student_name}</div>
            <div style="font-size:0.8rem;color:#a5b4fc !important">Seviye {current['seviye']} — {current['ad']}</div>
            <div style="font-size:1.3rem;font-weight:800;color:#eab308 !important;margin:8px 0">{p.total_xp} XP</div>
            <div style="font-size:0.75rem;color:#94a3b8 !important">
                📚 {p.total_problems_solved} çözüm • 🎯 %{p.accuracy:.0f} • 🔥 {p.current_streak} gün seri
            </div>
        </div>
        """)

    # Günlük aktivite grafiği
    if p.daily_log:
        styled_section("📅 Son 14 Gün Aktivite", "#f59e0b")
        sorted_dates = sorted(p.daily_log.keys(), reverse=True)[:14]
        sorted_dates.reverse()

        max_xp = max((p.daily_log[d].get("xp", 0) for d in sorted_dates), default=1)
        grafik_html = '<div style="display:flex;align-items:flex-end;gap:4px;height:120px;padding:8px;background:#0f172a;border-radius:12px;border:1px solid rgba(99,102,241,0.1)">'
        for d in sorted_dates:
            log = p.daily_log[d]
            xp = log.get("xp", 0)
            solved = log.get("solved", 0)
            h = max(4, (xp / max(max_xp, 1)) * 100)
            renk = "#10b981" if xp >= 50 else "#f59e0b" if xp >= 20 else "#ef4444"
            grafik_html += f'''
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%">
                <div style="font-size:0.55rem;color:{renk} !important;margin-bottom:1px">{xp}</div>
                <div style="width:100%;height:{h:.0f}px;background:{renk};border-radius:3px 3px 0 0;min-width:6px" title="{d}: {solved} çözüm, {xp} XP"></div>
                <div style="font-size:0.45rem;color:#64748b !important;margin-top:1px">{d[-5:]}</div>
            </div>'''
        grafik_html += '</div>'
        _render_html(grafik_html)

    # AI Öğretmen Tavsiyesi
    styled_section("🤖 AI Öğretmen Raporu", "#ec4899")
    rapor_maddeler = []

    if p.total_problems_solved == 0:
        rapor_maddeler.append(("📋", "Başlangıç", "Bu öğrenci henüz hiç problem çözmemiş. Matematik Köyü'nü tanıtarak başlayın.", "#94a3b8"))
    else:
        if p.accuracy >= 80:
            rapor_maddeler.append(("🌟", "Üstün Başarı", f"%{p.accuracy:.0f} doğruluk oranı mükemmel. Olimpiyat seviyesinde sorular verilebilir.", "#10b981"))
        elif p.accuracy >= 60:
            rapor_maddeler.append(("👍", "İyi Seviye", f"%{p.accuracy:.0f} doğruluk oranı iyi. Zorluk seviyesi artırılabilir.", "#3b82f6"))
        elif p.accuracy >= 40:
            rapor_maddeler.append(("💪", "Gelişmekte", f"%{p.accuracy:.0f} doğruluk — temel konularda pekiştirme yapılmalı.", "#f59e0b"))
        else:
            rapor_maddeler.append(("🎯", "Destek Gerekli", f"%{p.accuracy:.0f} doğruluk — kolay seviyeden başlayarak güven oluşturulmalı.", "#ef4444"))

        if p.current_streak >= 7:
            rapor_maddeler.append(("🔥", "Süreklilik", f"{p.current_streak} gün üst üste çalışma — motivasyonu çok yüksek!", "#10b981"))
        elif p.current_streak == 0:
            rapor_maddeler.append(("⚠️", "Düzensiz", "Düzenli çalışma alışkanlığı oluşturulmalı. Günde 10 dk hedef koyun.", "#f59e0b"))

        # Zayıf kategori
        if p.category_stats:
            zayif = min(p.category_stats.items(),
                        key=lambda x: (x[1].get("correct", 0) / max(x[1].get("solved", 0), 1)))
            zayif_oran = (zayif[1].get("correct", 0) / max(zayif[1].get("solved", 0), 1)) * 100
            if zayif_oran < 50:
                rapor_maddeler.append(("📐", f"Zayıf Alan: {zayif[0]}", f"Bu konuda %{zayif_oran:.0f} başarı. Ekstra destek ve pratik önerilir.", "#ef4444"))

        rapor_maddeler.append(("📊", "Toplam", f"{p.total_problems_solved} problem çözüldü, {p.total_xp} XP kazanıldı, {len(p.achievements)} başarım.", "#6366f1"))

    for ikon, baslik, mesaj, renk in rapor_maddeler:
        _render_html(f"""
        <div style="background:{renk}08;border-radius:12px;padding:12px 16px;margin-bottom:6px;border-left:4px solid {renk}">
            <div style="display:flex;align-items:flex-start;gap:10px">
                <span style="font-size:1.3rem">{ikon}</span>
                <div>
                    <div style="font-weight:700;color:#e0e7ff !important;font-size:0.85rem">{baslik}</div>
                    <div style="color:#94a3b8 !important;font-size:0.8rem">{mesaj}</div>
                </div>
            </div>
        </div>
        """)

    # PDF Rapor Çıktısı
    st.markdown("---")
    styled_section("📄 PDF Rapor Çıktısı", "#3b82f6")
    rapor_text = f"""MATEMATIK KOYU - OGRENCI ILERLEME RAPORU
{'='*50}
Ogrenci: {p.student_name}
Seviye: {level_info['current']['seviye']} - {level_info['current']['ad']}
XP: {p.total_xp}
Toplam Cozum: {p.total_problems_solved}
Dogruluk: %{p.accuracy:.0f}
Seri: {p.current_streak} gun (en iyi: {p.best_streak})
Basarim: {len(p.achievements)}/{len(BASARIM_TANIMLARI)}
{'='*50}
KATEGORI PERFORMANSI:
"""
    for cat, cs in p.category_stats.items():
        s_count = cs.get("solved", 0)
        c_count = cs.get("correct", 0)
        acc = (c_count / s_count * 100) if s_count > 0 else 0
        rapor_text += f"  {cat}: {c_count}/{s_count} (%{acc:.0f})\n"

    rapor_text += f"\nRapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}"

    st.download_button(
        label="📄 Raporu İndir (TXT)",
        data=rapor_text,
        file_name=f"matematik_rapor_{p.student_name}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        key="mat_pdf_download",
    )


# ══════════════════════════════════════════════════════════════════════════════
# 8) FORMÜL KÜTÜPHANESİ
# ══════════════════════════════════════════════════════════════════════════════

def _render_formuller(store: MatematikDataStore):
    """Formül kütüphanesi."""
    styled_section("📖 Formül Kütüphanesi", "#6366f1")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:16px;padding:20px;margin-bottom:20px;border:1px solid rgba(99,102,241,0.3)">
        <div style="font-weight:700;color:#e0e7ff !important;font-size:1.1rem;margin-bottom:6px">📐 Tüm Formüller Bir Arada</div>
        <div style="color:#a5b4fc !important;font-size:0.9rem">Temel aritmetikten analize kadar — ihtiyacın olan her formül burada!</div>
    </div>
    """)

    # Sınıf filtresi
    grade_filter = st.selectbox("Sınıf Filtresi", ["Tümü"] + list(SINIF_KONULARI.keys()),
                                key="mat_form_grade")

    # Arama
    search = st.text_input("🔍 Formül Ara", key="mat_form_search",
                           placeholder="Pisagor, türev, olasılık...")

    for category, formulas in FORMUL_KATEGORILERI.items():
        filtered = formulas

        # Sınıf filtresi
        if grade_filter != "Tümü":
            g = int(grade_filter) if grade_filter.isdigit() else 5
            filtered = [f for f in filtered if _grade_in_range(g, f.get("sinif", "1-12"))]

        # Arama filtresi
        if search:
            q = search.lower()
            filtered = [f for f in filtered if q in f.get("ad", "").lower()
                        or q in f.get("formul", "").lower()
                        or q in f.get("aciklama", "").lower()]

        if not filtered:
            continue

        styled_section(f"📐 {category}", "#4f46e5")

        for formula in filtered:
            _render_html(f"""
            <div class="mat-formula-card">
                <div class="formula-name">{formula['ad']}</div>
                <div class="formula-expr">{formula['formul']}</div>
                <div class="formula-desc">{formula['aciklama']}</div>
                <div class="formula-grade">📚 {formula.get('sinif', '')}. sınıf</div>
            </div>
            """)


def _grade_in_range(grade: int, range_str: str) -> bool:
    """Sınıfın belirtilen aralıkta olup olmadığını kontrol et."""
    if range_str == "olimpiyat":
        return grade >= 9
    try:
        parts = range_str.split("-")
        if len(parts) == 2:
            return int(parts[0]) <= grade <= int(parts[1])
        return grade == int(parts[0])
    except (ValueError, IndexError):
        return True


# ══════════════════════════════════════════════════════════════════════════════
# 9) EĞLENCELİ MATEMATİK (0-4. Sınıf — Emoji Karakterli)
# ══════════════════════════════════════════════════════════════════════════════

def _render_matematik_sozlugu():
    """Matematik sözlüğü ve kavram haritası."""
    styled_section("📚 Matematik Sözlüğü & Kavram Haritası", "#3b82f6")

    sozluk = {
        "A": [
            ("Açı", "İki ışının ortak başlangıç noktasından oluşan şekil. Derece (°) ile ölçülür.", "5-12"),
            ("Açıortay", "Bir açıyı iki eşit parçaya bölen ışın.", "6-10"),
            ("Alan", "Düzlemsel bir şeklin kapladığı yüzey büyüklüğü. cm², m² ile ölçülür.", "4-12"),
            ("Aritmetik Ortalama", "Verilerin toplamının veri sayısına bölümü: x̄ = Σxᵢ/n", "6-12"),
            ("Asal Sayı", "1 ve kendisinden başka pozitif böleni olmayan 1'den büyük doğal sayı. Ör: 2,3,5,7,11...", "4-12"),
            ("Asimptot", "Bir eğrinin sonsuza giderken yaklaştığı ama asla ulaşamadığı doğru.", "11-12"),
        ],
        "B": [
            ("Binom", "İki terimli cebirsel ifade: (a+b)", "9-12"),
            ("Bölen", "Bir sayıyı kalansız bölen sayı. 12'nin bölenleri: 1,2,3,4,6,12", "3-8"),
            ("Bileşke Fonksiyon", "f∘g(x) = f(g(x)) — bir fonksiyonun çıktısı diğerinin girdisi", "10-12"),
        ],
        "C-Ç": [
            ("Çevre", "Düzlemsel şeklin dış sınırının uzunluğu.", "4-12"),
            ("Çember", "Bir merkeze eşit uzaklıktaki noktaların oluşturduğu eğri.", "5-12"),
            ("Çarpanlara Ayırma", "Bir ifadeyi çarpımlarına bölme. Ör: x²−9 = (x−3)(x+3)", "8-12"),
        ],
        "D": [
            ("Denklem", "Bilinmeyen içeren eşitlik. Ör: 2x+3=7", "6-12"),
            ("Determinant", "Kare matrise atanan sayısal değer. 2×2: ad−bc", "11-12"),
            ("Dik Açı", "90° ölçüsündeki açı. ⊾ sembolü ile gösterilir.", "4-12"),
            ("Diskriminant", "Δ = b²−4ac. İkinci derece denklemin kök sayısını belirler.", "9-12"),
            ("Doğal Sayılar", "0, 1, 2, 3, 4, ... sıfır dahil negatif olmayan tam sayılar (ℕ)", "1-12"),
        ],
        "E": [
            ("EBOB", "En Büyük Ortak Bölen. İki sayının ortak bölenlerinin en büyüğü.", "5-8"),
            ("EKOK", "En Küçük Ortak Kat. İki sayının ortak katlarının en küçüğü.", "5-8"),
            ("Eşitsizlik", "İki ifade arasındaki büyüklük-küçüklük ilişkisi: <, >, ≤, ≥", "7-12"),
            ("Eğim", "Doğrunun dikliğini gösteren oran: m = Δy/Δx", "8-12"),
            ("Euler Sayısı (e)", "e ≈ 2.71828... Doğal logaritmanın tabanı.", "11-12"),
        ],
        "F": [
            ("Faktöriyel", "n! = n×(n−1)×...×2×1. Ör: 5! = 120", "9-12"),
            ("Fibonacci Dizisi", "Her terim önceki ikisinin toplamı: 1,1,2,3,5,8,13,21...", "5-12"),
            ("Fonksiyon", "Her girdiye tek bir çıktı atayan kural: f(x)", "8-12"),
        ],
        "G": [
            ("Geometrik Dizi", "Her terimin öncekinin sabit katı olduğu dizi: a, ar, ar², ar³...", "9-12"),
            ("Grafik", "Fonksiyonun koordinat düzlemindeki görsel temsili.", "8-12"),
        ],
        "H-I-İ": [
            ("Hacim", "Üç boyutlu cismin kapladığı uzay büyüklüğü. cm³, m³, litre", "5-12"),
            ("Hipotenüs", "Dik üçgende 90° açının karşısındaki en uzun kenar.", "8-12"),
            ("İntegral", "Türevin tersi. Eğri altında kalan alanı hesaplar: ∫f(x)dx", "12"),
            ("İrrasyonel Sayı", "Kesir olarak yazılamayan sayı: √2, π, e", "8-12"),
        ],
        "K": [
            ("Kare", "4 kenarı ve 4 açısı eşit dörtgen.", "2-12"),
            ("Karekök", "x² = a ise x = √a. Ör: √25 = 5", "7-12"),
            ("Kesir", "Bir bütünün parçasını ifade eden sayı: a/b", "3-12"),
            ("Kombinasyon", "Sırasız seçim: C(n,r) = n!/(r!(n−r)!)", "10-12"),
            ("Koordinat", "Düzlemde noktanın konumu: (x, y)", "6-12"),
            ("Küme", "Belirli nesnelerin iyi tanımlanmış topluluğu: A = {1,2,3}", "9-12"),
        ],
        "L-M": [
            ("Logaritma", "Üssün tersi: logₐb = c demek aᶜ = b demek", "10-12"),
            ("Limit", "Fonksiyonun bir noktaya yaklaşırken aldığı değer", "11-12"),
            ("Matris", "Sayıların satır ve sütunlar halinde düzenlenmesi", "11-12"),
            ("Medyan", "Sıralı veri setinin ortadaki değeri", "6-12"),
            ("Mod", "Veri setinde en çok tekrar eden değer", "6-12"),
        ],
        "O-Ö": [
            ("Oran", "İki niceliğin bölümü: a:b = a/b", "5-12"),
            ("Orantı", "İki oranın eşitliği: a/b = c/d", "6-12"),
            ("Olasılık", "Bir olayın gerçekleşme şansı: P = istenen/toplam", "8-12"),
            ("Öklid Algoritması", "EBOB bulmak için bölme tekrarlama yöntemi", "6-12"),
        ],
        "P": [
            ("Parabol", "İkinci derece fonksiyonun grafiği: y = ax²+bx+c", "9-12"),
            ("Paralel", "Hiç kesişmeyen iki doğru. ∥ sembolü.", "5-12"),
            ("Permütasyon", "Sıralı dizilim: P(n,r) = n!/(n−r)!", "10-12"),
            ("Pi (π)", "Daire çevresi/çap = 3.14159... Evrensel sabit.", "7-12"),
            ("Polinom", "Değişkenlerin üslü terimlerinin toplamı: ax²+bx+c", "9-12"),
            ("Prizma", "İki eş paralel tabanlı geometrik cisim.", "6-12"),
        ],
        "R-S": [
            ("Rasyonel Sayı", "p/q şeklinde yazılabilen sayı (q≠0): ½, 0.75, −3", "7-12"),
            ("Simetri", "Şeklin bir eksen/nokta etrafında aynı görünmesi", "4-12"),
            ("Standart Sapma", "Verilerin ortalamadan ne kadar saptığının ölçüsü: σ", "10-12"),
        ],
        "T": [
            ("Tam Sayılar", "...−3,−2,−1, 0, 1, 2, 3... (ℤ)", "6-12"),
            ("Teğet", "Eğriyi tek bir noktada kesen doğru.", "10-12"),
            ("Trigonometri", "Üçgenlerdeki açı-kenar ilişkilerini inceleyen dal: sin, cos, tan", "9-12"),
            ("Türev", "Fonksiyonun değişim hızı: f'(x) = lim[Δx→0] Δf/Δx", "12"),
        ],
        "U-Ü-V-Y-Z": [
            ("Üçgen", "3 kenarlı çokgen. İç açıları toplamı 180°.", "3-12"),
            ("Üslü Sayı", "aⁿ = a×a×...×a (n kez)", "6-12"),
            ("Varyans", "Verilerin yayılma ölçüsü: σ² = Σ(xᵢ−x̄)²/n", "10-12"),
            ("Vektör", "Hem büyüklüğü hem yönü olan nicelik.", "11-12"),
            ("Yüzde", "Yüzde birler cinsinden oran: %50 = 50/100 = 0.5", "5-12"),
        ],
    }

    # Arama
    arama = st.text_input("🔍 Kavram Ara", key="mat_sz_ara", placeholder="Ör: Pisagor, türev, kesir...")

    sinif_f = st.selectbox("Sınıf Filtresi", ["Tümü"] + [str(i) for i in range(1, 13)], key="mat_sz_sinif")

    toplam_kavram = sum(len(v) for v in sozluk.values())
    st.caption(f"📚 Toplam {toplam_kavram} kavram")

    for harf, kavramlar in sozluk.items():
        filtered = kavramlar

        if arama:
            q = arama.lower()
            filtered = [k for k in filtered if q in k[0].lower() or q in k[1].lower()]

        if sinif_f != "Tümü":
            g = int(sinif_f)
            def _sinif_uygun(sinif_str, grade):
                try:
                    parts = sinif_str.split("-")
                    return int(parts[0]) <= grade <= int(parts[1]) if len(parts) == 2 else grade == int(parts[0])
                except (ValueError, IndexError):
                    return True
            filtered = [k for k in filtered if _sinif_uygun(k[2], g)]

        if not filtered:
            continue

        styled_section(f"📖 {harf}", "#3b82f6")
        for ad, aciklama, sinif in filtered:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:12px 16px;margin-bottom:6px;
                         border-left:4px solid #3b82f6;border:1px solid rgba(59,130,246,0.1)">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="font-weight:700;color:#e0e7ff !important;font-size:0.95rem">{ad}</span>
                    <span style="font-size:0.65rem;color:#6366f1 !important;background:rgba(99,102,241,0.1);
                                  padding:2px 8px;border-radius:10px">{sinif}. sınıf</span>
                </div>
                <div style="font-size:0.83rem;color:#94a3b8 !important;margin-top:4px;line-height:1.5">{aciklama}</div>
            </div>
            """)


def _render_eglenceli_matematik(store: MatematikDataStore):
    """Küçükler için eğlenceli matematik — emoji animasyonlu, renkli karakterler."""
    styled_section("🎨 Eğlenceli Matematik Dünyası", "#ec4899")

    _render_html("""
    <style>
    @keyframes mat-bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
    @keyframes mat-wiggle { 0%,100%{transform:rotate(0)} 25%{transform:rotate(-8deg)} 75%{transform:rotate(8deg)} }
    @keyframes mat-grow { 0%,100%{transform:scale(1)} 50%{transform:scale(1.15)} }
    @keyframes mat-rainbow { 0%{color:#ef4444} 16%{color:#f97316} 33%{color:#eab308} 50%{color:#10b981} 66%{color:#3b82f6} 83%{color:#8b5cf6} 100%{color:#ef4444} }
    .mat-bounce { animation: mat-bounce 1.5s ease-in-out infinite; display:inline-block; }
    .mat-wiggle { animation: mat-wiggle 1s ease-in-out infinite; display:inline-block; }
    .mat-grow { animation: mat-grow 2s ease-in-out infinite; display:inline-block; }
    .mat-rainbow-text { animation: mat-rainbow 3s linear infinite; }
    .mat-fear-card {
        background: linear-gradient(135deg, #fdf2f8, #fce7f3);
        border-radius: 24px; padding: 24px; margin-bottom: 16px;
        border: 2px solid #f9a8d4; position: relative; overflow: hidden;
    }
    .mat-fear-card .fear-emoji { font-size: 3rem; }
    .mat-courage-card {
        background: linear-gradient(135deg, #0d3320, #065f46);
        border-radius: 20px; padding: 22px; margin-bottom: 14px;
        border: 2px solid rgba(16,185,129,0.4); text-align: center;
    }
    .mat-story-bubble {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border-radius: 20px; padding: 22px; margin-bottom: 16px;
        border: 2px solid rgba(99,102,241,0.3);
        position: relative;
    }
    .mat-story-bubble::after {
        content:''; position:absolute; bottom:-12px; left:60px;
        border-left:12px solid transparent; border-right:12px solid transparent;
        border-top:12px solid #312e81;
    }
    .mat-visual-op {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 20px; padding: 28px; margin: 16px 0;
        border: 2px solid rgba(99,102,241,0.2); text-align: center;
    }
    .mat-shape-math {
        display: inline-flex; align-items: center; justify-content: center;
        gap: 12px; flex-wrap: wrap; font-size: 2rem; padding: 8px;
    }
    </style>
    <div style="background:linear-gradient(135deg,#831843,#be185d,#ec4899);border-radius:24px;padding:28px;margin-bottom:24px;
                 border:2px solid rgba(236,72,153,0.4);text-align:center;position:relative;overflow:hidden">
        <div style="position:absolute;top:10px;left:20px;font-size:2rem" class="mat-bounce">🌈</div>
        <div style="position:absolute;top:10px;right:20px;font-size:2rem" class="mat-grow">⭐</div>
        <div style="position:absolute;bottom:10px;left:40px;font-size:1.5rem" class="mat-wiggle">🎈</div>
        <div style="position:absolute;bottom:10px;right:40px;font-size:1.5rem" class="mat-bounce">🎪</div>
        <h2 style="color:#e0e7ff !important;font-size:1.8rem;margin:0 0 8px !important;position:relative;z-index:1">🎪 Matematik Sirki'ne Hoş Geldin! 🎪</h2>
        <p style="color:#fce7f3 !important;font-size:1rem;margin:0 !important;position:relative;z-index:1">Matematik hiç korkutucu değil! Sayı arkadaşlarınla birlikte eğlenerek öğren!</p>
    </div>
    """)

    sub_tabs = st.tabs([
        "🤖 Sınırsız Üretici",
        "📝 Dört İşlem Çalışma",
        "🦁 Korkma, Gel!",
        "🔢 Sayı Arkadaşları",
        "🎯 Topla-Çıkar",
        "✖️ Çarpma Bahçesi",
        "🎨 Şekil Ülkesi",
        "🔷 Şekillerle İşlem",
        "🧮 Sayma Parkuru",
        "🎵 Ritim & Örüntü",
        "📖 Matematik Masalları",
    ])

    with sub_tabs[0]:
        _render_eglenceli_uretici(store)
    with sub_tabs[1]:
        _render_dort_islem_calisma()
    with sub_tabs[2]:
        _render_korkma_gel()
    with sub_tabs[3]:
        _render_sayi_arkadaslari()
    with sub_tabs[4]:
        _render_topla_cikar_oyunu()
    with sub_tabs[5]:
        _render_carpma_bahcesi()
    with sub_tabs[6]:
        _render_sekil_ulkesi()
    with sub_tabs[7]:
        _render_sekillerle_islem()
    with sub_tabs[8]:
        _render_sayma_parkuru()
    with sub_tabs[9]:
        _render_ritim_oruntu()
    with sub_tabs[10]:
        _render_matematik_masallari()


def _render_eglenceli_uretici(store: MatematikDataStore):
    """Sınırsız eğlenceli matematik sorusu üretici."""
    import random as _r
    styled_section("🤖 Sınırsız Eğlenceli Matematik Üretici", "#ec4899")

    _render_html("""
    <div style="background:linear-gradient(135deg,#831843,#be185d);border-radius:20px;padding:24px;margin-bottom:20px;
                 border:2px solid rgba(236,72,153,0.4);text-align:center">
        <div style="font-size:2.5rem;margin-bottom:8px" class="mat-grow">🤖🎪⚡</div>
        <div style="font-weight:700;color:#e0e7ff !important;font-size:1.2rem">Sınırsız Eğlence Fabrikası!</div>
        <div style="color:#fce7f3 !important;font-size:0.9rem">Toplama, çıkarma, çarpma, bölme, sayma, örüntü, şekil — emojili, renkli, eğlenceli!</div>
    </div>
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        tur = st.selectbox("Soru Türü", [
            ("karisik", "🔀 Karışık (Her Türden)"),
            ("toplama_cikarma", "➕➖ Toplama & Çıkarma"),
            ("carpma_bolme", "✖️➗ Çarpma & Bölme"),
            ("sayma", "🧮 Sayma Soruları"),
            ("oruntu", "🎵 Örüntü Soruları"),
            ("sekil", "🎨 Şekil Soruları"),
        ], key="egl_fab_tur", format_func=lambda x: x[1])
    with col2:
        sinif = st.selectbox("Sınıf", [1, 2, 3, 4, 5, 6], key="egl_fab_sinif", index=2,
                              format_func=lambda x: f"{x}. Sınıf")
    with col3:
        adet = st.selectbox("Adet", [10, 25, 50, 100, 250, 500], key="egl_fab_adet", index=2)

    if st.button(f"🚀 {adet} Soru Üret!", key="egl_fab_go", type="primary"):
        with st.spinner(f"🤖 {adet} eğlenceli soru üretiliyor..."):
            gen = EglenceliMatematikGenerator()
            sorular = gen.toplu_uret(tur[0], sinif, adet)

        st.session_state["egl_fab_sonuc"] = sorular

        # Tür dağılımı
        from collections import Counter
        tip_sayim = Counter(s.get("tip", "?") for s in sorular)
        tip_emojiler = {"toplama": "➕", "cikarma": "➖", "carpma": "✖️", "bolme": "➗",
                        "sayma": "🧮", "oruntu": "🎵", "sekil_kenar": "🎨", "sekil_toplam": "🎨",
                        "sekil_carp": "🎨", "sekil_tani": "🎨"}

        _render_html(f"""
        <div style="background:linear-gradient(135deg,#052e16,#065f46);border-radius:16px;padding:20px;margin:16px 0;
                     border:2px solid rgba(16,185,129,0.4);text-align:center">
            <div style="font-size:2rem;margin-bottom:8px">✅</div>
            <div style="font-weight:800;color:#bbf7d0 !important;font-size:1.2rem">{len(sorular)} Soru Üretildi!</div>
        </div>
        """)

        cols = st.columns(min(len(tip_sayim), 6))
        for col, (tip, cnt) in zip(cols, tip_sayim.most_common(6)):
            with col:
                _render_html(f"""
                <div class="mat-stat-card" style="padding:10px">
                    <div style="font-size:1.3rem">{tip_emojiler.get(tip,'🧮')}</div>
                    <div style="font-weight:700;color:#818cf8 !important;font-size:1.2rem">{cnt}</div>
                    <div style="font-size:0.65rem;color:#94a3b8 !important">{tip}</div>
                </div>
                """)

    # Üretilenleri göster ve çöz
    if "egl_fab_sonuc" in st.session_state:
        sorular = st.session_state["egl_fab_sonuc"]

        # Çözüm modu
        styled_section("🎯 Soru Çöz!", "#f59e0b")

        if "egl_fab_idx" not in st.session_state:
            st.session_state["egl_fab_idx"] = 0
            st.session_state["egl_fab_skor"] = {"dogru": 0, "toplam": 0}

        idx = st.session_state["egl_fab_idx"]
        skor = st.session_state["egl_fab_skor"]

        if idx < len(sorular):
            s = sorular[idx]

            # İlerleme
            progress = idx / len(sorular)
            st.progress(progress, text=f"Soru {idx+1}/{len(sorular)} • ✅ {skor['dogru']}/{skor['toplam']}")

            tip = s.get("tip", "")

            if tip in ("toplama", "cikarma"):
                _render_html(f"""
                <div style="background:#0f172a;border-radius:20px;padding:28px;margin:12px 0;text-align:center;
                             border:1px solid rgba(99,102,241,0.2)">
                    <div style="font-size:1.8rem;margin-bottom:8px;letter-spacing:2px">{s.get('gosterim','')}</div>
                    <div style="font-size:2rem;font-weight:900;color:#e0e7ff !important;margin:8px 0">
                        {s['a']} {'➕' if s['op']=='+' else '➖'} {s['b']} = ❓
                    </div>
                </div>
                """)
                ans = st.number_input("Cevabın:", min_value=-10000, max_value=100000, step=1, value=0, key=f"egl_ans_{idx}")
                if st.button("✅ Kontrol Et", key=f"egl_chk_{idx}", type="primary"):
                    skor["toplam"] += 1
                    if int(ans) == s["cevap"]:
                        skor["dogru"] += 1
                        st.success(f"🎉 Doğru! {s['denklem']}")
                    else:
                        st.error(f"❌ Doğru cevap: {s['cevap']} → {s['denklem']}")
                    st.session_state["egl_fab_idx"] = idx + 1
                    st.rerun()

            elif tip in ("carpma", "bolme"):
                _render_html(f"""
                <div style="background:#0f172a;border-radius:20px;padding:28px;margin:12px 0;text-align:center;
                             border:1px solid rgba(99,102,241,0.2)">
                    <div style="font-size:1.5rem;margin-bottom:8px;letter-spacing:2px">{s.get('gosterim','')[:100]}</div>
                    <div style="font-size:1rem;color:#94a3b8 !important;margin:8px 0">{s.get('soru','')}</div>
                </div>
                """)
                ans = st.number_input("Cevabın:", min_value=0, max_value=100000, step=1, value=0, key=f"egl_ans_{idx}")
                if st.button("✅ Kontrol Et", key=f"egl_chk_{idx}", type="primary"):
                    skor["toplam"] += 1
                    if int(ans) == s["cevap"]:
                        skor["dogru"] += 1
                        st.success(f"🎉 Doğru! {s['denklem']}")
                    else:
                        st.error(f"❌ Doğru cevap: {s['cevap']} → {s['denklem']}")
                    st.session_state["egl_fab_idx"] = idx + 1
                    st.rerun()

            elif tip == "sayma":
                grid_str = "  ".join(s["grid"])
                _render_html(f"""
                <div style="background:#0f172a;border-radius:20px;padding:28px;margin:12px 0;text-align:center;
                             border:1px solid rgba(99,102,241,0.2)">
                    <div style="font-size:0.9rem;color:#94a3b8 !important;margin-bottom:10px">{s['soru']}</div>
                    <div style="font-size:2rem;line-height:2;letter-spacing:6px">{grid_str}</div>
                </div>
                """)
                ans = st.number_input(f"Kaç tane {s['emoji']}?", min_value=0, max_value=50, step=1, value=0, key=f"egl_ans_{idx}")
                if st.button("✅ Kontrol Et", key=f"egl_chk_{idx}", type="primary"):
                    skor["toplam"] += 1
                    if int(ans) == s["cevap"]:
                        skor["dogru"] += 1
                        st.success(f"🎉 Doğru! {s['adet']} tane {s['emoji']}")
                    else:
                        st.error(f"❌ {s['adet']} tane var!")
                    st.session_state["egl_fab_idx"] = idx + 1
                    st.rerun()

            elif tip == "oruntu":
                desen_str = "  ".join(s["desen"])
                _render_html(f"""
                <div style="background:#0f172a;border-radius:20px;padding:28px;margin:12px 0;text-align:center;
                             border:1px solid rgba(99,102,241,0.2)">
                    <div style="font-size:0.85rem;color:#94a3b8 !important;margin-bottom:10px">Sıradaki ne?</div>
                    <div style="font-size:2rem;letter-spacing:8px;margin-bottom:12px">{desen_str}</div>
                    <div style="font-size:2.5rem">❓</div>
                </div>
                """)
                cols = st.columns(4)
                for i, opt in enumerate(s.get("secenekler", [])):
                    with cols[i % 4]:
                        if st.button(str(opt), key=f"egl_opt_{idx}_{i}", use_container_width=True):
                            skor["toplam"] += 1
                            if str(opt) == str(s["cevap"]):
                                skor["dogru"] += 1
                                st.success(f"🎉 Doğru! {s.get('ipucu','')}")
                            else:
                                st.error(f"❌ Doğru: {s['cevap']}")
                            st.session_state["egl_fab_idx"] = idx + 1
                            st.rerun()

            else:  # şekil soruları
                _render_html(f"""
                <div style="background:#0f172a;border-radius:20px;padding:28px;margin:12px 0;text-align:center;
                             border:1px solid rgba(99,102,241,0.2)">
                    <div style="font-size:3rem;margin-bottom:12px">{s.get('emoji','🎨')}</div>
                    <div style="font-size:1.1rem;color:#e0e7ff !important;font-weight:600">{s.get('soru','')}</div>
                </div>
                """)
                ans = st.text_input("Cevabın:", key=f"egl_ans_{idx}")
                if st.button("✅ Kontrol Et", key=f"egl_chk_{idx}", type="primary"):
                    skor["toplam"] += 1
                    if ans.strip().lower() == str(s["cevap"]).lower():
                        skor["dogru"] += 1
                        st.success(f"🎉 Doğru! {s.get('aciklama','')}")
                    else:
                        st.error(f"❌ Doğru cevap: {s['cevap']} — {s.get('aciklama','')}")
                    st.session_state["egl_fab_idx"] = idx + 1
                    st.rerun()
        else:
            # Tüm sorular bitti — sonuç
            oran = (skor["dogru"] / skor["toplam"] * 100) if skor["toplam"] > 0 else 0
            emoji_son = "🏆" if oran >= 90 else "⭐" if oran >= 70 else "👏" if oran >= 50 else "💪"
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#1e0a3a,#4c1d95);border-radius:24px;padding:32px;
                         margin:16px 0;text-align:center;border:2px solid rgba(139,92,246,0.4)">
                <div style="font-size:4rem;margin-bottom:12px">{emoji_son}</div>
                <div style="font-size:1.5rem;font-weight:800;color:#e9d5ff !important">Tamamlandı!</div>
                <div style="display:flex;justify-content:center;gap:40px;margin-top:16px">
                    <div>
                        <div style="font-size:2.2rem;font-weight:900;color:#10b981 !important">{skor['dogru']}/{skor['toplam']}</div>
                        <div style="font-size:0.75rem;color:#94a3b8 !important">Doğru</div>
                    </div>
                    <div>
                        <div style="font-size:2.2rem;font-weight:900;color:#f59e0b !important">%{oran:.0f}</div>
                        <div style="font-size:0.75rem;color:#94a3b8 !important">Başarı</div>
                    </div>
                </div>
            </div>
            """)
            if oran >= 80:
                st.balloons()

            if st.button("🔄 Yeni Set Üret!", key="egl_fab_reset", type="primary"):
                for k in list(st.session_state.keys()):
                    if k.startswith("egl_fab_") or k.startswith("egl_ans_") or k.startswith("egl_chk_") or k.startswith("egl_opt_"):
                        del st.session_state[k]
                st.rerun()


def _render_dort_islem_calisma():
    """Dört işlem çalışma kağıdı — geleneksel defter formatında dikey işlemler."""
    styled_section("📝 Dört İşlem Çalışma Kağıdı", "#3b82f6")

    # Çalışma kağıdı CSS
    _render_html("""
    <style>
    .ck-page {
        background: #0f172a; border-radius: 16px; padding: 20px 24px;
        border: 1px solid rgba(99,102,241,0.15); margin-bottom: 20px;
    }
    .ck-header {
        text-align: center; margin-bottom: 16px;
        border-bottom: 2px solid #ef4444; padding-bottom: 10px;
    }
    .ck-header h3 {
        color: #e0e7ff !important; font-size: 1rem; margin: 0 0 4px !important;
        font-weight: 700;
    }
    .ck-header .ck-sinif {
        background: #6366f1; color: #e0e7ff !important; padding: 2px 12px;
        border-radius: 20px; font-size: 0.7rem; font-weight: 700;
        display: inline-block;
    }
    .ck-grid {
        display: grid; grid-template-columns: repeat(7, 1fr); gap: 16px 20px;
    }
    .ck-grid.ck-3col { grid-template-columns: repeat(3, 1fr); }
    .ck-grid.ck-4col { grid-template-columns: repeat(4, 1fr); }
    /* ── Sade Defter İşlem Stili ── */
    .ck-card { background: transparent; padding: 4px 6px 8px; }
    .ck-num {
        font-family: 'Courier New', monospace; font-size: 1.35rem;
        font-weight: 700; color: #e0e7ff !important;
        text-align: right; line-height: 1.4; letter-spacing: 2px;
    }
    .ck-op-row { display: flex; align-items: baseline; }
    .ck-op {
        font-family: 'Courier New', monospace; font-size: 1.25rem;
        font-weight: 700; color: #ef4444 !important;
        min-width: 20px; text-align: left;
    }
    .ck-op-num {
        flex: 1; text-align: right;
        font-family: 'Courier New', monospace; font-size: 1.35rem;
        font-weight: 700; color: #e0e7ff !important; letter-spacing: 2px;
    }
    .ck-line { border-top: 2px solid #64748b; margin: 1px 0 4px; }
    .ck-answer {
        font-family: 'Courier New', monospace; font-size: 1.35rem;
        font-weight: 700; color: #10b981 !important;
        letter-spacing: 2px; text-align: right; min-height: 1.3em;
    }
    .ck-answer.hidden { color: transparent !important; }
    .ck-dots { min-height: 1.3em; }
    /* Bölme */
    .ck-bolme-box { background: transparent; padding: 4px 6px 8px; }
    .ck-bolme-layout {
        display: flex; align-items: flex-start;
        font-family: 'Courier New', monospace;
        font-size: 1.35rem; font-weight: 700; color: #e0e7ff !important;
    }
    .ck-bolme-left {
        border-right: 2px solid #64748b; border-bottom: 2px solid #64748b;
        padding: 3px 8px 3px 2px; text-align: right; letter-spacing: 2px;
    }
    .ck-bolme-right { padding: 3px 2px 3px 8px; letter-spacing: 2px; }
    .ck-bolme-result {
        padding: 5px 2px 0; text-align: right;
        font-family: 'Courier New', monospace; font-size: 1.35rem;
        font-weight: 700; color: #10b981 !important; letter-spacing: 2px;
    }
    .ck-bolme-kalan {
        font-size: 0.75rem; color: #f59e0b !important;
        margin-top: 2px; text-align: right;
        font-family: 'Courier New', monospace;
    }
    </style>
    """)

    import random as _r

    # Ayarlar
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sinif = st.selectbox("Sınıf", ["1", "2", "3", "4", "5", "6"], key="ck_sinif", index=2)
    with col2:
        islem_turu = st.selectbox("İşlem Türü", [
            "➕ Toplama", "➖ Çıkarma", "✖️ Çarpma", "➗ Bölme", "🔀 Karışık (Dört İşlem)"
        ], key="ck_islem")
    with col3:
        soru_sayisi = st.selectbox("Soru Sayısı", [5, 10, 15, 20], key="ck_adet", index=1)
    with col4:
        cevap_goster = st.checkbox("Cevapları Göster", key="ck_cevap", value=False)

    if st.button("📝 Çalışma Kağıdı Oluştur!", key="ck_olustur", type="primary"):
        grade = int(sinif)
        sorular = []

        for _ in range(soru_sayisi):
            # İşlem türü belirle
            if "Toplama" in islem_turu:
                op = "+"
            elif "Çıkarma" in islem_turu:
                op = "-"
            elif "Çarpma" in islem_turu:
                op = "×"
            elif "Bölme" in islem_turu:
                op = "÷"
            else:
                op = _r.choice(["+", "-", "×", "÷"])

            # Sınıfa göre sayı aralıkları
            if grade <= 1:
                a, b = _r.randint(1, 10), _r.randint(1, 10)
                if op in ("×", "÷"):
                    op = _r.choice(["+", "-"])
            elif grade == 2:
                if op in ("+", "-"):
                    a, b = _r.randint(10, 99), _r.randint(1, 99)
                elif op == "×":
                    a, b = _r.randint(2, 10), _r.randint(2, 10)
                else:
                    b = _r.randint(2, 9)
                    a = b * _r.randint(2, 10)
            elif grade == 3:
                if op in ("+", "-"):
                    a, b = _r.randint(100, 999), _r.randint(100, 999)
                elif op == "×":
                    a, b = _r.randint(100, 999), _r.randint(2, 9)
                else:
                    b = _r.randint(2, 9)
                    a = b * _r.randint(10, 99) + _r.randint(0, b - 1)
            elif grade == 4:
                if op in ("+", "-"):
                    a, b = _r.randint(1000, 9999), _r.randint(100, 9999)
                elif op == "×":
                    a, b = _r.randint(100, 999), _r.randint(2, 9)
                else:
                    b = _r.randint(2, 9)
                    a = b * _r.randint(50, 200) + _r.randint(0, b - 1)
            else:
                if op in ("+", "-"):
                    a, b = _r.randint(10000, 99999), _r.randint(1000, 99999)
                elif op == "×":
                    a, b = _r.randint(100, 9999), _r.randint(10, 99)
                else:
                    b = _r.randint(3, 20)
                    a = b * _r.randint(100, 500) + _r.randint(0, b - 1)

            # Çıkarmada büyük üstte olsun
            if op == "-" and a < b:
                a, b = b, a

            # Cevap hesapla
            if op == "+":
                cevap = a + b
            elif op == "-":
                cevap = a - b
            elif op == "×":
                cevap = a * b
            else:
                cevap = a // b
                kalan = a % b

            sorular.append({"a": a, "b": b, "op": op,
                            "cevap": cevap if op != "÷" else cevap,
                            "kalan": kalan if op == "÷" else 0})

        st.session_state["ck_sorular"] = sorular

    # Soruları göster
    if "ck_sorular" in st.session_state:
        sorular = st.session_state["ck_sorular"]

        # İşlem türüne göre grupla
        toplama = [s for s in sorular if s["op"] == "+"]
        cikarma = [s for s in sorular if s["op"] == "-"]
        carpma = [s for s in sorular if s["op"] == "×"]
        bolme = [s for s in sorular if s["op"] == "÷"]

        # TOPLAMA
        if toplama:
            _render_html(f"""
            <div class="ck-page">
                <div class="ck-header">
                    <span class="ck-sinif">{sinif}. Sınıf</span>
                    <h3>➕ TOPLAMA İŞLEMLERİ</h3>
                </div>
                <div class="ck-grid">
            """)
            for s in toplama:
                ans_display = str(s["cevap"]) if cevap_goster else ""
                _render_html(f"""
                    <div class="ck-card toplama">
                        <div class="ck-num">{s['a']}</div>
                        <div class="ck-op-row">
                            <span class="ck-op">+</span>
                            <span class="ck-op-num">{s['b']}</span>
                        </div>
                        <div class="ck-line"></div>
                        <div class="ck-answer {'hidden' if not cevap_goster else ''}">{ans_display}</div>
                        {'<div class="ck-dots"></div>' if not cevap_goster else ''}
                    </div>
                """)
            _render_html("</div></div>")

        # ÇIKARMA
        if cikarma:
            _render_html(f"""
            <div class="ck-page">
                <div class="ck-header">
                    <span class="ck-sinif">{sinif}. Sınıf</span>
                    <h3>➖ ÇIKARMA İŞLEMLERİ</h3>
                </div>
                <div class="ck-grid">
            """)
            for s in cikarma:
                ans_display = str(s["cevap"]) if cevap_goster else ""
                _render_html(f"""
                    <div class="ck-card cikarma">
                        <div class="ck-num">{s['a']}</div>
                        <div class="ck-op-row">
                            <span class="ck-op">–</span>
                            <span class="ck-op-num">{s['b']}</span>
                        </div>
                        <div class="ck-line"></div>
                        <div class="ck-answer {'hidden' if not cevap_goster else ''}">{ans_display}</div>
                        {'<div class="ck-dots"></div>' if not cevap_goster else ''}
                    </div>
                """)
            _render_html("</div></div>")

        # ÇARPMA
        if carpma:
            _render_html(f"""
            <div class="ck-page">
                <div class="ck-header">
                    <span class="ck-sinif">{sinif}. Sınıf</span>
                    <h3>✖️ ÇARPMA İŞLEMLERİ</h3>
                </div>
                <div class="ck-grid">
            """)
            for s in carpma:
                ans_display = str(s["cevap"]) if cevap_goster else ""
                _render_html(f"""
                    <div class="ck-card carpma">
                        <div class="ck-num">{s['a']}</div>
                        <div class="ck-op-row">
                            <span class="ck-op">×</span>
                            <span class="ck-op-num">{s['b']}</span>
                        </div>
                        <div class="ck-line"></div>
                        <div class="ck-answer {'hidden' if not cevap_goster else ''}">{ans_display}</div>
                        {'<div class="ck-dots"></div>' if not cevap_goster else ''}
                    </div>
                """)
            _render_html("</div></div>")

        # BÖLME
        if bolme:
            _render_html(f"""
            <div class="ck-page">
                <div class="ck-header">
                    <span class="ck-sinif">{sinif}. Sınıf</span>
                    <h3>➗ BÖLME İŞLEMLERİ</h3>
                </div>
                <div class="ck-grid">
            """)
            for s in bolme:
                ans_display = str(s["cevap"]) if cevap_goster else ""
                kalan_display = f'<div class="ck-bolme-kalan">Kalan: {s["kalan"]}</div>' if cevap_goster and s["kalan"] > 0 else ""
                _render_html(f"""
                    <div class="ck-bolme-box">
                        <div class="ck-bolme-layout">
                            <div class="ck-bolme-left">{s['a']}</div>
                            <div class="ck-bolme-right">{s['b']}</div>
                        </div>
                        <div class="ck-bolme-result {'hidden' if not cevap_goster else ''}" style="font-family:'Courier New',monospace;font-size:1.3rem;font-weight:700;color:#388e3c !important;padding:8px 4px 0;text-align:right;min-height:1.4em">
                            {ans_display}
                        </div>
                        {kalan_display}
                        {'<div class="ck-dots"></div>' if not cevap_goster else ''}
                    </div>
                """)
            _render_html("</div></div>")

        # İnteraktif cevaplama
        st.markdown("---")
        styled_section("✏️ Cevaplarını Yaz & Kontrol Et", "#10b981")

        for idx, s in enumerate(sorular):
            if idx % 5 == 0:
                cols = st.columns(5)
            col = cols[idx % 5]
            with col:
                op_label = {"+" : "+", "-": "−", "×": "×", "÷": "÷"}[s["op"]]
                label = f"{s['a']} {op_label} {s['b']}"
                user_ans = st.number_input(
                    label, min_value=-999999, max_value=999999,
                    step=1, value=0, key=f"ck_ans_{idx}",
                    label_visibility="visible",
                )

        if st.button("✅ Cevapları Kontrol Et!", key="ck_kontrol", type="primary"):
            dogru = 0
            yanlis_list = []
            for idx, s in enumerate(sorular):
                user_val = st.session_state.get(f"ck_ans_{idx}", 0)
                if int(user_val) == s["cevap"]:
                    dogru += 1
                else:
                    op_label = {"+" : "+", "-": "−", "×": "×", "÷": "÷"}[s["op"]]
                    yanlis_list.append(f"{s['a']} {op_label} {s['b']} = **{s['cevap']}** (sen: {user_val})")

            toplam = len(sorular)
            oran = (dogru / toplam) * 100 if toplam > 0 else 0

            if oran == 100:
                st.success(f"🎉 MÜKEMMEL! {dogru}/{toplam} — Hepsini doğru yaptın! ⭐⭐⭐")
                st.balloons()
            elif oran >= 80:
                st.success(f"👏 Harika! {dogru}/{toplam} doğru (%{oran:.0f})")
            elif oran >= 50:
                st.warning(f"💪 İyi gidiyorsun! {dogru}/{toplam} doğru (%{oran:.0f})")
            else:
                st.info(f"🌱 Pratik yaparak gelişeceksin! {dogru}/{toplam} doğru (%{oran:.0f})")

            if yanlis_list:
                with st.expander(f"❌ Yanlışların ({len(yanlis_list)} adet)", expanded=True):
                    for y in yanlis_list:
                        st.markdown(f"- {y}")


def _render_korkma_gel():
    """Matematikten korkan çocuklar için cesaret veren, sevdiren bölüm."""
    styled_section("🦁 Hey! Matematik Hiç Korkutucu Değil!", "#ec4899")

    # Cesaret veren açılış
    _render_html("""
    <div style="background:linear-gradient(135deg,#fdf2f8,#fce7f3);border-radius:24px;padding:28px;margin-bottom:20px;
                 border:2px solid #f9a8d4;text-align:center">
        <div style="font-size:4rem;margin-bottom:12px" class="mat-bounce">🤗</div>
        <div style="font-size:1.5rem;font-weight:800;color:#831843 !important;margin-bottom:8px">Matematik Seni Seviyor!</div>
        <div style="font-size:1rem;color:#9d174d !important;line-height:1.8">
            Hata yapmak <span class="mat-wiggle" style="font-size:1.3rem">✨</span> <b>süper güçtür!</b>
            Her yanlış cevap, doğruya bir adım daha yaklaşmaktır. 💪<br>
            Burada kimse sana kızmaz, kimse seninle dalga geçmez.<br>
            <b>Sadece sen, emojiler ve eğlence var!</b> 🎉
        </div>
    </div>
    """)

    # Matematik korkusu karakterleri ve çözümleri
    _render_html("""
    <div class="mat-story-bubble">
        <div style="display:flex;align-items:center;gap:16px">
            <div style="font-size:3.5rem" class="mat-wiggle">😰</div>
            <div>
                <div style="font-weight:700;color:#fca5a5 !important;font-size:1.1rem">Korku Canavarı diyor ki:</div>
                <div style="color:#94a3b8 !important;font-size:0.95rem;font-style:italic">"Matematik çok zor! Asla yapamayacaksın!"</div>
            </div>
        </div>
    </div>
    <div class="mat-courage-card">
        <div style="font-size:3.5rem;margin-bottom:8px" class="mat-grow">🦸‍♀️</div>
        <div style="font-weight:800;color:#bbf7d0 !important;font-size:1.2rem;margin-bottom:6px">Cesaret Kahramanı cevaplıyor:</div>
        <div style="color:#86efac !important;font-size:1rem;line-height:1.8">
            "Dur bakalım! Sen her gün matematik yapıyorsun farkında bile değilsin! 🤔<br>
            <b>🍕 Pizzayı eşit bölerken</b> → Kesir!<br>
            <b>🛒 Markette para sayarken</b> → Toplama!<br>
            <b>🎮 Oyunda puan hesaplarken</b> → Çarpma!<br>
            <b>⏰ Saati okurken</b> → Sayılar!<br>
            Sen zaten bir matematik kahramanısın! 💪✨"
        </div>
    </div>
    """)

    st.markdown("---")

    # Adım adım cesaret basamakları
    styled_section("🪜 Cesaret Basamakları", "#8b5cf6")
    _render_html("""
    <div style="color:#94a3b8 !important;font-size:0.9rem;margin-bottom:12px">Her basamağı tıkla ve matematiğin ne kadar kolay olduğunu gör!</div>
    """)

    basamaklar = [
        {
            "seviye": 1, "ad": "🌱 Tohumcuk", "renk": "#10b981",
            "mesaj": "Sadece say: 1, 2, 3... Parmaklarını kullan!",
            "ornek": "Kaç parmağın var? 🖐️🖐️ = 10 parmak!",
            "emoji_goster": "☝️✌️🤟🖐️",
        },
        {
            "seviye": 2, "ad": "🌿 Filiz", "renk": "#3b82f6",
            "mesaj": "Topla: Elmaları bir araya getir!",
            "ornek": "🍎🍎 + 🍎 = 🍎🍎🍎  →  2 + 1 = 3",
            "emoji_goster": "🍎🍎 ➕ 🍎 = 🍎🍎🍎",
        },
        {
            "seviye": 3, "ad": "🌳 Ağaç", "renk": "#f59e0b",
            "mesaj": "Çıkar: Birkaçını ye, kaç kaldı?",
            "ornek": "🍪🍪🍪🍪🍪 - 🍪🍪 = 🍪🍪🍪  →  5 - 2 = 3",
            "emoji_goster": "🍪🍪🍪🍪🍪 ➖ 🍪🍪 = 🍪🍪🍪",
        },
        {
            "seviye": 4, "ad": "🌸 Çiçek", "renk": "#ec4899",
            "mesaj": "Çarp: Aynı şeyden birkaç tane!",
            "ornek": "3 tabakta 2'şer kurabiye: 🍪🍪 🍪🍪 🍪🍪  →  3 × 2 = 6",
            "emoji_goster": "🍪🍪 | 🍪🍪 | 🍪🍪 = 6 kurabiye!",
        },
        {
            "seviye": 5, "ad": "⭐ Yıldız", "renk": "#6366f1",
            "mesaj": "Böl: Eşit paylaştır!",
            "ornek": "6 çilek 3 arkadaşa: 🍓🍓 | 🍓🍓 | 🍓🍓  →  6 ÷ 3 = 2",
            "emoji_goster": "🍓🍓 | 🍓🍓 | 🍓🍓 → herkes 2 tane!",
        },
    ]

    for b in basamaklar:
        with st.expander(f"{b['ad']} — Seviye {b['seviye']}", expanded=(b['seviye'] <= 2)):
            _render_html(f"""
            <div style="background:linear-gradient(135deg,{b['renk']}15,{b['renk']}08);
                         border-radius:20px;padding:24px;border:2px solid {b['renk']}30">
                <div style="font-weight:700;color:#e0e7ff !important;font-size:1.1rem;margin-bottom:10px">
                    {b['mesaj']}
                </div>
                <div style="font-size:1.8rem;margin:16px 0;text-align:center;letter-spacing:4px">
                    {b['emoji_goster']}
                </div>
                <div style="background:{b['renk']}20;border-radius:12px;padding:12px 16px;
                             text-align:center;font-size:1rem;color:#e0e7ff !important;font-weight:600">
                    {b['ornek']}
                </div>
            </div>
            """)

    st.markdown("---")

    # Motivasyon duvarı
    styled_section("🌟 Motivasyon Duvarı", "#eab308")
    motivasyonlar = [
        ("🧒", "Hata yapmak öğrenmenin en güzel yolu!", "#ef4444"),
        ("🦋", "Bugün zor görünen yarın çok kolay olacak!", "#8b5cf6"),
        ("🚀", "Her gün biraz pratik yap, roket gibi yüksel!", "#3b82f6"),
        ("🌈", "Matematikte tek bir doğru yol yok — kendi yolunu bul!", "#10b981"),
        ("🎯", "Yavaş da olsa doğru yapmak, hızlı ama yanlış yapmaktan iyidir!", "#f59e0b"),
        ("💎", "En parlak elmaslar en çok yontulanlardır — denemekten vazgeçme!", "#ec4899"),
    ]

    for i in range(0, len(motivasyonlar), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(motivasyonlar):
                emoji, mesaj, renk = motivasyonlar[i + j]
                with col:
                    _render_html(f"""
                    <div style="background:linear-gradient(135deg,{renk}10,{renk}05);
                                 border-radius:20px;padding:20px;text-align:center;min-height:140px;
                                 border:2px solid {renk}25;display:flex;flex-direction:column;
                                 align-items:center;justify-content:center">
                        <div style="font-size:2.5rem;margin-bottom:8px" class="mat-bounce">{emoji}</div>
                        <div style="font-size:0.85rem;color:#e0e7ff !important;font-weight:600;line-height:1.5">{mesaj}</div>
                    </div>
                    """)


def _render_sayi_arkadaslari():
    """0-9 sayıları emoji karakterlerle tanıtım."""
    styled_section("🔢 Sayı Arkadaşlarını Tanı!", "#f59e0b")

    sayi_karakterler = [
        {"sayi": 0, "ad": "Sıfır Sihirbazı", "emoji": "🪄", "renk": "#94a3b8",
         "hikaye": "Ben Sıfır! Hiçbir şey yok gibi görünürüm ama aslında çok güçlüyüm! Beni bir sayının sağına koyarsan onu 10 kat büyütürüm! 1 → 10 🤯",
         "ornek": "0 elma = Sepet boş! 🧺"},
        {"sayi": 1, "ad": "Bir Kahraman", "emoji": "🦸", "renk": "#ef4444",
         "hikaye": "Ben Bir! Her şeyin başlangıcıyım. Her sayıyı benimle çarp, kendisi kalır! Ben çarpmanın süper kahramanıyım! 💪",
         "ornek": "1 güneş ☀️ = Tek ve biricik!"},
        {"sayi": 2, "ad": "İkiz Kardeşler", "emoji": "👯", "renk": "#3b82f6",
         "hikaye": "Biz İkiziz! Her şeyin çifti bizde. 2 göz 👀, 2 kulak 👂, 2 el ✋. Çift sayıların ilkiyiz!",
         "ornek": "2 ayak = Yürüyüş zamanı! 🚶"},
        {"sayi": 3, "ad": "Üçgen Prenses", "emoji": "👸", "renk": "#8b5cf6",
         "hikaye": "Ben Üç! Üçgenin köşe sayısıyım 🔺. Masal dünyasında 3 dilek hakkın var! Sihirli sayıyım ✨",
         "ornek": "3 renk 🚦 = Trafik lambası!"},
        {"sayi": 4, "ad": "Dört Mevsim", "emoji": "🍂", "renk": "#10b981",
         "hikaye": "Ben Dört! Kare benim en yakın arkadaşım ⬜. 4 mevsim 🌸☀️🍂❄️, 4 yön 🧭, 4 teker 🚗 — düzeni severim!",
         "ornek": "4 bacak = Masa ayakları! 🪑"},
        {"sayi": 5, "ad": "Beşli Kaptan", "emoji": "🖐️", "renk": "#f97316",
         "hikaye": "Ben Beş! Elindeki parmak sayısı kadarım 🖐️. 10'un yarısıyım. Yıldızların köşe sayısıyım ⭐!",
         "ornek": "5 parmak = High five! ✋"},
        {"sayi": 6, "ad": "Altı Arı", "emoji": "🐝", "renk": "#eab308",
         "hikaye": "Ben Altı! Arıların petek hücresi 6 kenarlıdır 🔯. 2×3=6, 1+2+3=6 — mükemmel sayıyım! Çünkü bölenlerimin (1,2,3) toplamı da benim!",
         "ornek": "6 kenar = Altıgen petek! 🍯"},
        {"sayi": 7, "ad": "Yedi Gökkuşağı", "emoji": "🌈", "renk": "#6366f1",
         "hikaye": "Ben Yedi! Gökkuşağında 7 renk var 🌈. Haftada 7 gün 📅. Dünya harikalarının sayısıyım! Şans getiririm 🍀",
         "ornek": "7 nota = Do Re Mi Fa Sol La Si 🎵"},
        {"sayi": 8, "ad": "Sekiz Ahtapot", "emoji": "🐙", "renk": "#ec4899",
         "hikaye": "Ben Sekiz! Ahtapotun kolu kadarım 🐙. Beni yatırırsan sonsuz olurum ∞! Küpün köşe sayısıyım 🎲",
         "ornek": "8 kol = Ahtapot dansı! 🐙💃"},
        {"sayi": 9, "ad": "Dokuz Gezegen", "emoji": "🪐", "renk": "#14b8a6",
         "hikaye": "Ben Dokuz! Tek basamaklı sayıların en büyüğüyüm 💪. 3×3=9, karenin karesi! Galaksi kaşifiyim 🚀",
         "ornek": "9 gezegen = Güneş sistemi! ☀️🪐"},
    ]

    for s in sayi_karakterler:
        _render_html(f"""
        <div style="background:linear-gradient(135deg,{s['renk']}15,{s['renk']}08);
                     border-radius:20px;padding:20px;margin-bottom:14px;
                     border:2px solid {s['renk']}40;display:flex;align-items:center;gap:20px">
            <div style="min-width:90px;text-align:center">
                <div style="font-size:3.5rem;margin-bottom:4px;animation:mat-fire 1s infinite alternate">{s['emoji']}</div>
                <div style="font-size:2.5rem;font-weight:900;color:{s['renk']} !important">{s['sayi']}</div>
            </div>
            <div style="flex:1">
                <div style="font-weight:800;color:#e0e7ff !important;font-size:1.1rem;margin-bottom:6px">{s['ad']}</div>
                <div style="color:#c4b5fd !important;font-size:0.9rem;line-height:1.6;margin-bottom:8px">{s['hikaye']}</div>
                <div style="background:{s['renk']}15;border-radius:10px;padding:8px 14px;
                             font-size:0.85rem;color:{s['renk']} !important;font-weight:600">{s['ornek']}</div>
            </div>
        </div>
        """)


def _render_topla_cikar_oyunu():
    """Emojili toplama-çıkarma oyunu."""
    styled_section("🎯 Topla & Çıkar!", "#10b981")

    col1, col2 = st.columns(2)
    with col1:
        max_num = st.selectbox("Zorluk", [10, 20, 50, 100], key="mat_tc_max",
                                format_func=lambda x: f"0-{x} arası")
    with col2:
        islem = st.selectbox("İşlem", ["Toplama ➕", "Çıkarma ➖", "Karışık 🔀"], key="mat_tc_islem")

    tc_key = "mat_tc_state"
    if tc_key not in st.session_state:
        st.session_state[tc_key] = {"skor": 0, "toplam": 0}

    emojiler = ["🍎", "🍊", "🍋", "🍇", "🍓", "🍌", "🍑", "🫐", "🥝", "🍒"]

    if st.button("🎲 Yeni Soru!", key="mat_tc_new", type="primary"):
        import random as _r
        if "Toplama" in islem:
            op = "+"
        elif "Çıkarma" in islem:
            op = "-"
        else:
            op = _r.choice(["+", "-"])

        a = _r.randint(1, max_num)
        b = _r.randint(1, max_num if op == "+" else a)
        emoji = _r.choice(emojiler)

        if op == "+":
            cevap = a + b
        else:
            cevap = a - b

        st.session_state["mat_tc_soru"] = {"a": a, "b": b, "op": op, "cevap": cevap, "emoji": emoji}

    if "mat_tc_soru" in st.session_state:
        s = st.session_state["mat_tc_soru"]
        emoji_a = s["emoji"] * min(s["a"], 12)
        emoji_b = s["emoji"] * min(s["b"], 12)
        op_emoji = "➕" if s["op"] == "+" else "➖"

        _render_html(f"""
        <div style="background:linear-gradient(135deg,#064e3b,#065f46);border-radius:20px;padding:28px;
                     margin:16px 0;text-align:center;border:2px solid rgba(16,185,129,0.3)">
            <div style="font-size:1.8rem;margin-bottom:12px;letter-spacing:2px">{emoji_a}</div>
            <div style="font-size:2.5rem;font-weight:900;color:#e0e7ff !important;margin:8px 0">
                {s['a']}  {op_emoji}  {s['b']}  =  ❓
            </div>
            <div style="font-size:1.8rem;margin-top:12px;letter-spacing:2px">{emoji_b}</div>
        </div>
        """)

        cevap_input = st.number_input("Cevabını yaz:", min_value=0, max_value=200,
                                       step=1, key="mat_tc_cevap_input")
        if st.button("✅ Kontrol Et", key="mat_tc_kontrol"):
            st.session_state[tc_key]["toplam"] += 1
            if int(cevap_input) == s["cevap"]:
                st.session_state[tc_key]["skor"] += 1
                st.success(f"🎉 Harikasın! {s['a']} {s['op']} {s['b']} = **{s['cevap']}** ✨")
                st.balloons()
            else:
                st.error(f"😅 Tekrar dene! Doğru cevap: **{s['cevap']}**")

    skor = st.session_state[tc_key]
    if skor["toplam"] > 0:
        _render_html(f"""
        <div class="mat-stat-card" style="margin-top:12px;border-color:rgba(16,185,129,0.3)">
            <div class="mat-stat-icon">🏆</div>
            <div class="mat-stat-value" style="color:#10b981 !important">{skor['skor']}/{skor['toplam']}</div>
            <div class="mat-stat-label">Skor</div>
        </div>
        """)


def _render_carpma_bahcesi():
    """Çarpım tablosu eğlenceli öğretim."""
    styled_section("✖️ Çarpma Bahçesi", "#8b5cf6")

    st.info("🌻 Çarpım tablosunu çiçek bahçesinde öğren!")

    selected = st.selectbox("Hangi sayının çarpım tablosu?",
                             list(range(1, 11)), key="mat_cb_sayi", index=1)

    emojiler = ["🌻", "🌹", "🌸", "🌺", "🌼", "🌷", "💐", "🌿", "🍀", "🪻"]

    _render_html(f"""
    <div style="background:linear-gradient(135deg,#1a0a2e,#2d1b69);border-radius:20px;padding:24px;margin:16px 0;
                 border:2px solid rgba(139,92,246,0.3)">
        <div style="text-align:center;font-size:1.5rem;font-weight:800;color:#e9d5ff !important;margin-bottom:16px">
            {emojiler[selected-1]} {selected} Sayısının Çarpım Bahçesi {emojiler[selected-1]}
        </div>
    """)

    rows_html = ""
    for i in range(1, 11):
        result = selected * i
        flowers = emojiler[selected - 1] * min(i, 10)
        rows_html += f"""
        <div style="display:flex;align-items:center;gap:12px;padding:8px 14px;margin-bottom:4px;
                     background:rgba(139,92,246,0.08);border-radius:10px">
            <div style="min-width:120px;font-weight:700;color:#c4b5fd !important;font-size:1.1rem">
                {selected} × {i} = {result}
            </div>
            <div style="font-size:1rem;letter-spacing:1px">{flowers}</div>
        </div>
        """

    _render_html(rows_html + "</div>")

    # Mini quiz
    st.markdown("---")
    styled_section("🎯 Hızlı Test", "#f59e0b")
    import random as _r
    if "mat_cb_quiz" not in st.session_state:
        b = _r.randint(1, 10)
        st.session_state["mat_cb_quiz"] = {"a": selected, "b": b, "cevap": selected * b}

    q = st.session_state["mat_cb_quiz"]
    st.markdown(f"### {q['a']} × {q['b']} = ?")
    ans = st.number_input("Cevap:", min_value=0, max_value=200, step=1, key="mat_cb_ans")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Kontrol", key="mat_cb_check"):
            if int(ans) == q["cevap"]:
                st.success(f"🎉 Doğru! {q['a']} × {q['b']} = {q['cevap']}")
                st.balloons()
            else:
                st.error(f"❌ Doğru cevap: {q['cevap']}")
    with col2:
        if st.button("🔄 Yeni Soru", key="mat_cb_yeni"):
            b = _r.randint(1, 10)
            st.session_state["mat_cb_quiz"] = {"a": selected, "b": b, "cevap": selected * b}
            st.rerun()


def _render_sekil_ulkesi():
    """Geometrik şekiller tanıtımı — küçük çocuklar için."""
    styled_section("🎨 Şekil Ülkesi", "#f97316")

    sekiller = [
        {"ad": "Daire", "emoji": "⭕", "kenar": "0 (sonsuz!)", "renk": "#ef4444",
         "aciklama": "Yuvarlarım, dönerim! Tekerlek, pizza, güneş — hepsi benim gibi yuvarlak!",
         "gercek": "🍕 Pizza, ⚽ Top, 🎯 Hedef, 🪙 Para, 🕐 Saat"},
        {"ad": "Kare", "emoji": "⬜", "kenar": "4 eşit kenar", "renk": "#3b82f6",
         "aciklama": "Tüm kenarlarım eşit, tüm açılarım 90°! Düzenli ve simetriyim.",
         "gercek": "🪟 Pencere, 🧇 Waffle, 📱 Ekran, 🎲 Zar yüzü, 🏁 Bayrak"},
        {"ad": "Üçgen", "emoji": "🔺", "kenar": "3 kenar", "renk": "#10b981",
         "aciklama": "En az kenarlı çokgenim! Piramitlerin yüzüyüm, çatıların şekliyim.",
         "gercek": "🔺 Trafik işareti, 🏔️ Dağ, 🎄 Çam ağacı, 🍕 Pizza dilimi, ⛺ Çadır"},
        {"ad": "Dikdörtgen", "emoji": "▬", "kenar": "4 kenar (2'şer eşit)", "renk": "#8b5cf6",
         "aciklama": "Kare'nin uzun kardeşiyim! Kapılar, kitaplar, ekranlar — ben her yerdeyim.",
         "gercek": "📚 Kitap, 🚪 Kapı, 📺 TV, 💳 Kart, 🛏️ Yatak"},
        {"ad": "Yıldız", "emoji": "⭐", "kenar": "5 veya 6 köşe", "renk": "#eab308",
         "aciklama": "Gökyüzünde parlarım! 5 köşeli olanım en meşhur.",
         "gercek": "⭐ Gökyüzü, 🏅 Madalya, 🎄 Ağaç tepesi, ⚜️ Logo"},
        {"ad": "Kalp", "emoji": "❤️", "kenar": "Eğri kenar", "renk": "#ec4899",
         "aciklama": "Sevginin şekliyim! Simetriğim — ortadan ikiye bölünürüm.",
         "gercek": "❤️ Sevgi, 🎴 Kart, 🍫 Çikolata, 💌 Mektup"},
    ]

    for i in range(0, len(sekiller), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(sekiller):
                s = sekiller[i + j]
                with col:
                    _render_html(f"""
                    <div style="background:linear-gradient(135deg,{s['renk']}15,{s['renk']}08);
                                 border-radius:20px;padding:20px;margin-bottom:14px;text-align:center;
                                 border:2px solid {s['renk']}30;min-height:280px">
                        <div style="font-size:4rem;margin-bottom:8px;animation:mat-fire 1.5s infinite alternate">{s['emoji']}</div>
                        <div style="font-weight:800;color:#e0e7ff !important;font-size:1.2rem;margin-bottom:4px">{s['ad']}</div>
                        <div style="font-size:0.75rem;color:{s['renk']} !important;margin-bottom:8px">📏 {s['kenar']}</div>
                        <div style="font-size:0.8rem;color:#94a3b8 !important;line-height:1.5;margin-bottom:10px">{s['aciklama']}</div>
                        <div style="font-size:0.8rem;color:#c4b5fd !important;background:rgba(0,0,0,0.2);border-radius:10px;padding:8px">
                            <b>Gerçek hayat:</b> {s['gercek']}
                        </div>
                    </div>
                    """)


def _render_sayma_parkuru():
    """İnteraktif sayma parkuru."""
    styled_section("🧮 Sayma Parkuru", "#06b6d4")

    st.info("🎈 Emojileri say! Her soruda kaç tane olduğunu bul.")

    import random as _r
    emojiler = ["🎈", "🦋", "🐞", "🌟", "🍎", "🐠", "🦊", "🐸"]

    if st.button("🎲 Yeni Sayma Sorusu!", key="mat_sp_new", type="primary"):
        emoji = _r.choice(emojiler)
        count = _r.randint(3, 15)
        st.session_state["mat_sp_soru"] = {"emoji": emoji, "count": count}

    if "mat_sp_soru" in st.session_state:
        s = st.session_state["mat_sp_soru"]
        display = (s["emoji"] + " ") * s["count"]
        _render_html(f"""
        <div style="background:linear-gradient(135deg,#0a1628,#1e3a5f);border-radius:20px;padding:28px;
                     margin:16px 0;text-align:center;border:2px solid rgba(6,182,212,0.3)">
            <div style="font-size:1.2rem;color:#67e8f9 !important;margin-bottom:12px">Kaç tane {s['emoji']} var?</div>
            <div style="font-size:2rem;line-height:2;letter-spacing:4px">{display}</div>
        </div>
        """)

        ans = st.number_input("Kaç tane?", min_value=0, max_value=50, step=1, key="mat_sp_ans")
        if st.button("✅ Kontrol Et", key="mat_sp_check"):
            if int(ans) == s["count"]:
                st.success(f"🎉 Süper! {s['count']} tane {s['emoji']} var! Harikasın! ⭐")
                st.balloons()
            else:
                st.error(f"😅 Tekrar say! Doğru cevap: **{s['count']}**")


def _render_ritim_oruntu():
    """Örüntü (pattern) tanıma — küçükler için."""
    styled_section("🎵 Ritim & Örüntü", "#a855f7")

    st.info("🎶 Deseni bul ve sıradakini tahmin et!")

    import random as _r
    oruntuler = [
        {"desen": "🔴🔵🔴🔵🔴🔵", "sonraki": "🔴🔵", "ipucu": "Kırmızı-Mavi tekrarı"},
        {"desen": "⭐⭐🌙⭐⭐🌙⭐⭐", "sonraki": "🌙", "ipucu": "2 yıldız, 1 ay"},
        {"desen": "🐱🐶🐱🐶🐱", "sonraki": "🐶", "ipucu": "Kedi-köpek sırası"},
        {"desen": "🌸🌸🌻🌸🌸🌻🌸🌸", "sonraki": "🌻", "ipucu": "2 pembe çiçek, 1 sarı"},
        {"desen": "👏👏👏✋👏👏👏", "sonraki": "✋", "ipucu": "3 alkış, 1 dur"},
        {"desen": "1️⃣2️⃣3️⃣1️⃣2️⃣3️⃣1️⃣2️⃣", "sonraki": "3️⃣", "ipucu": "1-2-3 tekrarı"},
        {"desen": "🔺🔺🔻🔺🔺🔻🔺🔺", "sonraki": "🔻", "ipucu": "2 yukarı, 1 aşağı"},
        {"desen": "🍎🍊🍋🍎🍊🍋🍎🍊", "sonraki": "🍋", "ipucu": "Elma-portakal-limon"},
    ]

    if "mat_ort_idx" not in st.session_state:
        st.session_state["mat_ort_idx"] = _r.randint(0, len(oruntuler) - 1)

    ort = oruntuler[st.session_state["mat_ort_idx"]]

    _render_html(f"""
    <div style="background:linear-gradient(135deg,#1a0a2e,#2d1b69);border-radius:20px;padding:28px;
                 margin:16px 0;text-align:center;border:2px solid rgba(168,85,247,0.3)">
        <div style="font-size:1rem;color:#c084fc !important;margin-bottom:12px">Sıradaki ne olmalı?</div>
        <div style="font-size:2.5rem;letter-spacing:6px;margin-bottom:12px">{ort['desen']}</div>
        <div style="font-size:2rem;color:#e0e7ff !important">❓</div>
    </div>
    """)

    with st.expander("💡 İpucu"):
        st.markdown(f"**Desen:** {ort['ipucu']}")

    with st.expander("👁️ Cevabı Göster"):
        _render_html(f"""
        <div style="text-align:center;font-size:2.5rem;margin:12px 0">{ort['desen']}<span style="background:#4f46e5;border-radius:12px;padding:4px 12px">{ort['sonraki']}</span></div>
        """)
        st.success(f"Doğru cevap: **{ort['sonraki']}**")

    if st.button("🔄 Yeni Örüntü", key="mat_ort_yeni"):
        st.session_state["mat_ort_idx"] = _r.randint(0, len(oruntuler) - 1)
        st.rerun()


def _render_sekillerle_islem():
    """Şekillerle görsel aritmetik — korkuyu yenmek için."""
    styled_section("🔷 Şekillerle İşlem Yap!", "#6366f1")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:20px;padding:22px;margin-bottom:20px;
                 border:2px solid rgba(99,102,241,0.3);text-align:center">
        <div style="font-size:2rem;margin-bottom:8px" class="mat-wiggle">🔷</div>
        <div style="font-weight:700;color:#e0e7ff !important;font-size:1.1rem">Sayıları unutalım! Şekillerle hesaplayalım!</div>
        <div style="color:#a5b4fc !important;font-size:0.9rem">Şekilleri say, grupla ve sonucu bul!</div>
    </div>
    """)

    # Görsel toplama örnekleri
    islemler = [
        {
            "baslik": "Toplama: Şekilleri Birleştir!",
            "sol": "🔴🔴🔴",
            "islem": "➕",
            "sag": "🔴🔴",
            "sonuc": "🔴🔴🔴🔴🔴",
            "aciklama": "3 kırmızı top + 2 kırmızı top = 5 kırmızı top",
            "denklem": "3 + 2 = 5",
            "renk": "#10b981",
        },
        {
            "baslik": "Çıkarma: Bazılarını Kaldır!",
            "sol": "⭐⭐⭐⭐⭐⭐",
            "islem": "➖",
            "sag": "⭐⭐",
            "sonuc": "⭐⭐⭐⭐",
            "aciklama": "6 yıldız var, 2 tanesini aldık, 4 kaldı!",
            "denklem": "6 - 2 = 4",
            "renk": "#ef4444",
        },
        {
            "baslik": "Çarpma: Gruplar Oluştur!",
            "sol": "🟦🟦🟦",
            "islem": "×",
            "sag": "3 grup",
            "sonuc": "🟦🟦🟦 | 🟦🟦🟦 | 🟦🟦🟦",
            "aciklama": "3 tane 3'lü grup = 9 kare!",
            "denklem": "3 × 3 = 9",
            "renk": "#8b5cf6",
        },
        {
            "baslik": "Bölme: Eşit Paylaştır!",
            "sol": "🍬🍬🍬🍬🍬🍬🍬🍬",
            "islem": "÷",
            "sag": "4 çocuk",
            "sonuc": "🍬🍬 | 🍬🍬 | 🍬🍬 | 🍬🍬",
            "aciklama": "8 şeker 4 çocuğa = herkes 2 şeker alır!",
            "denklem": "8 ÷ 4 = 2",
            "renk": "#f59e0b",
        },
    ]

    for isl in islemler:
        _render_html(f"""
        <div class="mat-visual-op" style="border-color:{isl['renk']}40">
            <div style="font-weight:700;color:{isl['renk']} !important;font-size:1rem;margin-bottom:14px">{isl['baslik']}</div>
            <div class="mat-shape-math">
                <span>{isl['sol']}</span>
                <span style="font-size:2.5rem;color:{isl['renk']} !important" class="mat-bounce">{isl['islem']}</span>
                <span>{isl['sag']}</span>
                <span style="font-size:2.5rem;color:#e0e7ff !important">=</span>
                <span style="font-size:1.2rem">{isl['sonuc']}</span>
            </div>
            <div style="margin-top:12px;font-size:0.9rem;color:#94a3b8 !important">{isl['aciklama']}</div>
            <div style="margin-top:8px;background:{isl['renk']}20;border-radius:12px;padding:8px 16px;
                         display:inline-block;font-size:1.3rem;font-weight:800;color:{isl['renk']} !important">{isl['denklem']}</div>
        </div>
        """)

    st.markdown("---")

    # İnteraktif şekil işlemi
    styled_section("🎯 Şimdi Sen Dene!", "#ec4899")

    import random as _r
    sekil_emojileri = [
        ("🔴", "top"), ("🟡", "top"), ("🔵", "top"),
        ("⭐", "yıldız"), ("🌸", "çiçek"), ("🦋", "kelebek"),
        ("🐟", "balık"), ("🎈", "balon"), ("💎", "elmas"),
    ]

    if st.button("🎲 Yeni Şekil Sorusu!", key="mat_si_new", type="primary"):
        emoji, ad = _r.choice(sekil_emojileri)
        op = _r.choice(["+", "-"])
        a = _r.randint(1, 8)
        b = _r.randint(1, a if op == "-" else 8)
        cevap = a + b if op == "+" else a - b
        st.session_state["mat_si_soru"] = {
            "emoji": emoji, "ad": ad, "op": op, "a": a, "b": b, "cevap": cevap
        }

    if "mat_si_soru" in st.session_state:
        s = st.session_state["mat_si_soru"]
        sol = s["emoji"] * s["a"]
        sag = s["emoji"] * s["b"]
        op_emoji = "➕" if s["op"] == "+" else "➖"

        _render_html(f"""
        <div class="mat-visual-op" style="border-color:#ec489940">
            <div style="font-size:0.9rem;color:#94a3b8 !important;margin-bottom:10px">Kaç {s['ad']} oluyor?</div>
            <div style="font-size:2rem;margin:12px 0;letter-spacing:4px">{sol}</div>
            <div style="font-size:2.5rem;color:#ec4899 !important" class="mat-bounce">{op_emoji}</div>
            <div style="font-size:2rem;margin:12px 0;letter-spacing:4px">{sag}</div>
            <div style="font-size:2.5rem;color:#e0e7ff !important;margin-top:8px">= ❓</div>
        </div>
        """)

        ans = st.number_input(f"Kaç {s['ad']} kaldı?", min_value=0, max_value=20,
                               step=1, key="mat_si_ans")
        if st.button("✅ Kontrol Et!", key="mat_si_check"):
            if int(ans) == s["cevap"]:
                sonuc_goster = s["emoji"] * s["cevap"]
                st.success(f"🎉 SÜPER! {s['a']} {s['op']} {s['b']} = **{s['cevap']}** {s['ad']}!")
                _render_html(f'<div style="text-align:center;font-size:2rem;margin:12px 0">{sonuc_goster}</div>')
                st.balloons()
            else:
                st.error(f"😊 Tekrar dene! İpucu: {s['emoji']} şekillerini tek tek say!")


def _render_matematik_masallari():
    """Matematikle ilgili kısa masallar ve hikayeler."""
    styled_section("📖 Matematik Masalları", "#f59e0b")

    _render_html("""
    <div style="background:linear-gradient(135deg,#451a03,#78350f);border-radius:20px;padding:22px;margin-bottom:20px;
                 border:2px solid rgba(245,158,11,0.3);text-align:center">
        <div style="font-size:2rem;margin-bottom:8px" class="mat-grow">📖</div>
        <div style="font-weight:700;color:#fde68a !important;font-size:1.1rem">Uyumadan Önce Bir Matematik Masalı!</div>
        <div style="color:#fcd34d !important;font-size:0.9rem">Matematiğin aslında ne kadar eğlenceli olduğunu masallarla öğren.</div>
    </div>
    """)

    masallar = [
        {
            "baslik": "🐻 Ayıcık ve Bal Kavanozu",
            "ikon": "🍯",
            "hikaye": (
                "Bir zamanlar ormanda küçük bir ayıcık yaşarmış. Ayıcığın 5 tane bal kavanozu varmış. 🍯🍯🍯🍯🍯\n\n"
                "Bir gün arkadaşı tavşancık gelmiş: *'Ayıcık, bana 2 kavanoz bal verir misin?'* 🐰\n\n"
                "Ayıcık düşünmüş: *'5 kavanozum var, 2 tane verirsem...'* 🤔\n\n"
                "Parmaklarını saymış: 🍯🍯🍯~~🍯🍯~~ → **3 kavanoz kalır!**\n\n"
                "Ertesi gün arıcık 4 kavanoz daha getirmiş! 🐝🍯🍯🍯🍯\n\n"
                "Ayıcık sevinçle toplamış: *'3 + 4 = 7 kavanozum oldu!'* 🎉\n\n"
                "**Öğrendiğimiz:** Çıkarma = paylaşmak 💕, Toplama = biriktirmek 🌟"
            ),
            "soru": "Ayıcığın sonunda kaç kavanozu oldu?",
            "cevap": "7",
            "renk": "#f59e0b",
        },
        {
            "baslik": "🦊 Tilkinin Pizza Partisi",
            "ikon": "🍕",
            "hikaye": (
                "Tilki, 3 arkadaşını pizza partisine davet etmiş: 🦊🐰🦔🐿️\n\n"
                "Annesi 2 tane pizza yapmış. Her pizza 4 dilim! 🍕🍕\n\n"
                "Tilki düşünmüş: *'2 pizza × 4 dilim = 8 dilim var!'* 🤔\n\n"
                "🍕🍕🍕🍕 🍕🍕🍕🍕 = **8 dilim**\n\n"
                "4 arkadaş var: *'8 ÷ 4 = herkes 2 dilim yer!'* 🎉\n\n"
                "🦊: 🍕🍕 | 🐰: 🍕🍕 | 🦔: 🍕🍕 | 🐿️: 🍕🍕\n\n"
                "Herkes mutlu olmuş! 💕\n\n"
                "**Öğrendiğimiz:** Çarpma = toplam bulmak, Bölme = eşit paylaşmak!"
            ),
            "soru": "Her arkadaş kaç dilim pizza yedi?",
            "cevap": "2",
            "renk": "#ef4444",
        },
        {
            "baslik": "🌻 Bahçıvan Kız ve Çiçekler",
            "ikon": "🌸",
            "hikaye": (
                "Küçük Elif bahçesine çiçek ekmeyi çok severmiş. 🌱\n\n"
                "Pazartesi 3 tohum ekmiş: 🌱🌱🌱\n"
                "Salı 3 tohum daha ekmiş: 🌱🌱🌱\n"
                "Çarşamba 3 tohum daha ekmiş: 🌱🌱🌱\n\n"
                "*'Her gün 3 tohum, 3 gün boyunca... Bu bir çarpma!'* 💡\n\n"
                "**3 × 3 = 9 tohum!** 🌱🌱🌱🌱🌱🌱🌱🌱🌱\n\n"
                "Bir hafta sonra hepsi çiçek olmuş! 🌸🌸🌸🌸🌸🌸🌸🌸🌸\n\n"
                "Elif 3 demet yapmak istemiş: 9 ÷ 3 = **her demette 3 çiçek!**\n\n"
                "💐💐💐 → Annesine, babasına ve öğretmenine birer demet! 💕\n\n"
                "**Öğrendiğimiz:** Çarpma = aynı sayıyı tekrar etme, Bölme = gruplara ayırma!"
            ),
            "soru": "Elif toplam kaç tohum ekti?",
            "cevap": "9",
            "renk": "#ec4899",
        },
        {
            "baslik": "🚂 Tren ve Sayı İstasyonları",
            "ikon": "🚂",
            "hikaye": (
                "Sayı Treni yola çıkmış! 🚂💨\n\n"
                "**1. İstasyon:** 2 yolcu bindi. 🧑🧑 (Toplam: 2)\n"
                "**2. İstasyon:** 3 yolcu daha bindi. 🧑🧑🧑 (Toplam: 2+3 = 5)\n"
                "**3. İstasyon:** 1 yolcu indi. 👋 (Toplam: 5-1 = 4)\n"
                "**4. İstasyon:** 4 yolcu bindi! 🧑🧑🧑🧑 (Toplam: 4+4 = 8)\n"
                "**Son İstasyon:** Herkes indi! 👋👋👋👋👋👋👋👋\n\n"
                "Makinist gülmüş: *'Bugün toplam 8 yolcum oldu!'* 🚂✨\n\n"
                "**Öğrendiğimiz:** Binmek = toplama ➕, inmek = çıkarma ➖!"
            ),
            "soru": "Son istasyonda kaç yolcu indi?",
            "cevap": "8",
            "renk": "#3b82f6",
        },
        {
            "baslik": "🏰 Şekiller Krallığı",
            "ikon": "👑",
            "hikaye": (
                "Şekiller Krallığı'nda her şeklin özel bir görevi varmış:\n\n"
                "**🔺 Üçgen** en güçlüsüymüş — 3 kenarlı, çatıları tutarmış: 🏠\n"
                "**⬜ Kare** en düzenlisiymiş — 4 eşit kenar, pencereleri yaparmış: 🪟\n"
                "**⭕ Daire** en neşelisiymiş — köşesi yok, tekerlekleri döndürürmüş: 🛞\n"
                "**▬ Dikdörtgen** en uzunuymuş — kapıları korurmuş: 🚪\n\n"
                "Bir gün kötü Karmaşa Canavarı gelmiş! 👾\n"
                "*'Hepinizi karıştıracağım!'* demiş.\n\n"
                "Ama şekiller birleşince... 🏰 bir kale yapmışlar!\n"
                "Kare duvarları, üçgen çatıyı, daire kuleleri, dikdörtgen kapıyı!\n\n"
                "Canavar kaçmış! 👾💨\n\n"
                "**Öğrendiğimiz:** Her şeklin özel gücü vardır — birlikte güçlüyüz! 💪"
            ),
            "soru": "Üçgenin kaç kenarı var?",
            "cevap": "3",
            "renk": "#8b5cf6",
        },
    ]

    for masal in masallar:
        with st.expander(f"{masal['baslik']}", expanded=False):
            _render_html(f"""
            <div style="background:linear-gradient(135deg,{masal['renk']}10,{masal['renk']}05);
                         border-radius:20px;padding:24px;border:2px solid {masal['renk']}25">
                <div style="text-align:center;font-size:3rem;margin-bottom:12px" class="mat-grow">{masal['ikon']}</div>
            </div>
            """)
            st.markdown(masal["hikaye"])

            st.markdown("---")
            st.markdown(f"**🎯 Masal Sorusu:** {masal['soru']}")
            ans = st.text_input("Cevabın:", key=f"mat_masal_{masal['baslik'][:10]}")
            if ans:
                if ans.strip() == masal["cevap"]:
                    st.success("🎉 Aferin! Masalı çok iyi dinlemişsin! ⭐⭐⭐")
                else:
                    st.info(f"🤔 Masalı tekrar oku! Doğru cevap: **{masal['cevap']}**")


# ══════════════════════════════════════════════════════════════════════════════
# 10) 3D GEOMETRİ LABORATUVARI
# ══════════════════════════════════════════════════════════════════════════════

def _render_3d_geometri_lab(store: MatematikDataStore):
    """3D interaktif geometri laboratuvarı — detaylı bilgi kartlarıyla."""
    styled_section("🔮 3D Geometri Laboratuvarı", "#6366f1")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:16px;padding:20px;margin-bottom:20px;
                 border:1px solid rgba(99,102,241,0.3)">
        <div style="font-weight:700;color:#e0e7ff !important;font-size:1.1rem;margin-bottom:6px">🔮 3 Boyutlu Geometri Dünyası</div>
        <div style="color:#a5b4fc !important;font-size:0.9rem">Cisimleri döndür, incele, öğren! Mouse ile sürükleyerek döndür, scroll ile yakınlaş.</div>
    </div>
    """)

    # Cisim seçimi
    cisim = st.selectbox("Cisim Seç", [
        "Küp (Cube)", "Dikdörtgenler Prizması", "Üçgen Prizma",
        "Silindir (Cylinder)", "Koni (Cone)", "Küre (Sphere)",
        "Altıgen Prizma", "Piramit (Pyramid)", "Oktahedron",
        "Tetrahedron", "İkosahedron", "Dodekahedron",
        "Kesik Koni", "Yarım Küre", "Elipsoid",
        "Üçgen Piramit", "Beşgen Prizma", "Torus",
        "Paralel Yüzlü", "Kesik Piramit",
        "Sekizgen Prizma", "Çift Koni", "Kapsül",
        "Yıldız Prizması", "Altıgen Piramit", "Kesik Oktahedron",
        "Çan Yüzeyi", "Helisel Silindir", "Paraboloid", "Hiperboloid",
    ], key="mat_3d_cisim")

    # Her cisim için DETAYLI bilgi kartı
    cisim_bilgi = {
        "Küp (Cube)": {
            "yuzey": "6 kare yüz", "koşe": "8 köşe", "ayrıt": "12 ayrıt",
            "hacim": "V = a³", "alan": "A = 6a²", "cevre": "Toplam ayrıt = 12a",
            "kosegen": "Yüz köşegeni = a√2, Cisim köşegeni = a√3",
            "emoji": "🎲", "renk": "#818cf8",
            "tanim": "Tüm kenarları eşit, tüm açıları 90° olan düzgün altı yüzlü (heksahedron).",
            "ozellikler": [
                "Tüm 6 yüzü birbirine eş karelerdir",
                "Her köşede 3 ayrıt birleşir",
                "Euler formülü: K-A+Y = 8-12+6 = 2 ✓",
                "3 tane simetri düzlemi vardır (toplam 9)",
                "Cisim köşegeninin uzunluğu: d = a√3",
            ],
            "gercek_hayat": "🎲 Zar, 📦 Kargo kutusu, 🧊 Buz küpü, 🏗️ Rubik küpü, 🧱 Yapı taşı",
            "hesaplama_ornek": "a = 5 cm → Hacim = 125 cm³, Alan = 150 cm², Köşegen = 8.66 cm",
            "euler": "K=8, A=12, Y=6 → 8-12+6=2 ✓",
            "sinif": "5-8. Sınıf",
        },
        "Dikdörtgenler Prizması": {
            "yuzey": "6 dikdörtgen yüz", "koşe": "8 köşe", "ayrıt": "12 ayrıt",
            "hacim": "V = a·b·c", "alan": "A = 2(ab+bc+ac)", "cevre": "Toplam ayrıt = 4(a+b+c)",
            "kosegen": "Cisim köşegeni = √(a²+b²+c²)",
            "emoji": "📦", "renk": "#f59e0b",
            "tanim": "Karşılıklı yüzleri eş dikdörtgenlerden oluşan prizma. Küpün genelleştirilmiş hali.",
            "ozellikler": [
                "Karşılıklı 3 çift yüz birbirine eştir",
                "Tüm açıları 90°'dir",
                "Herhangi bir yüzü taban kabul edilebilir",
                "Cisim köşegeni: d = √(a²+b²+c²)",
                "En çok kullanılan geometrik cisimdir",
            ],
            "gercek_hayat": "📦 Kutu, 📚 Kitap, 🧱 Tuğla, 🏠 Oda, 📱 Telefon, 🚪 Kapı",
            "hesaplama_ornek": "a=3, b=4, c=5 cm → V=60 cm³, A=94 cm², Köşegen=7.07 cm",
            "euler": "K=8, A=12, Y=6 → 8-12+6=2 ✓",
            "sinif": "5-8. Sınıf",
        },
        "Üçgen Prizma": {
            "yuzey": "2 üçgen + 3 dikdörtgen", "koşe": "6 köşe", "ayrıt": "9 ayrıt",
            "hacim": "V = (½·t·h_üçgen)·H", "alan": "t·h_üçgen + (a+b+c)·H",
            "cevre": "2(a+b+c) + 3H", "kosegen": "Yüz köşegenleri dikdörtgenlerde",
            "emoji": "🔺", "renk": "#10b981",
            "tanim": "İki tabanı eş üçgen, yanal yüzleri dikdörtgen olan prizma.",
            "ozellikler": [
                "2 taban yüzü eş üçgenlerdir",
                "3 yanal yüzü dikdörtgendir",
                "Toblerone çikolata şekli!",
                "Optik prizmalar ışığı renklerine ayırır",
                "Euler: 6-9+5=2 ✓",
            ],
            "gercek_hayat": "🍫 Toblerone, 🔺 Çatı yapısı, 🌈 Optik prizma, ⛺ Çadır",
            "hesaplama_ornek": "Eşkenar üçgen taban (a=6 cm), H=10 cm → V=155.9 cm³",
            "euler": "K=6, A=9, Y=5 → 6-9+5=2 ✓",
            "sinif": "6-9. Sınıf",
        },
        "Silindir (Cylinder)": {
            "yuzey": "2 daire + 1 yanal yüzey", "koşe": "0 köşe", "ayrıt": "2 daire kenarı",
            "hacim": "V = πr²h", "alan": "A = 2πr² + 2πrh = 2πr(r+h)",
            "cevre": "Taban çevresi = 2πr", "kosegen": "—",
            "emoji": "🥫", "renk": "#06b6d4",
            "tanim": "Bir dikdörtgenin bir kenarı etrafında döndürülmesiyle oluşan cisim. İki tabanı eş dairelerdir.",
            "ozellikler": [
                "Köşesi ve ayrıtı yoktur (eğri yüzeylidir)",
                "Yanal yüzeyi açılınca dikdörtgen olur",
                "Yanal yüzey alanı = 2πrh (dikdörtgen)",
                "Sonsuz simetri ekseni vardır",
                "Hacmi = Taban alanı × Yükseklik",
            ],
            "gercek_hayat": "🥫 Konserve, 🧻 Tuvalet kağıdı rulosu, 🪵 Tomruk, 🕯️ Mum, 🏛️ Sütun",
            "hesaplama_ornek": "r=3 cm, h=10 cm → V=282.7 cm³, A=245.0 cm²",
            "euler": "Euler formülü düz yüzeyler için geçerlidir, silindir eğri yüzeylidir",
            "sinif": "7-10. Sınıf",
        },
        "Koni (Cone)": {
            "yuzey": "1 daire + 1 yanal", "koşe": "1 (tepe noktası)", "ayrıt": "1 daire kenarı",
            "hacim": "V = ⅓πr²h", "alan": "A = πr² + πrl",
            "cevre": "Taban çevresi = 2πr", "kosegen": "Ana doğru (l) = √(r²+h²)",
            "emoji": "🍦", "renk": "#f97316",
            "tanim": "Bir dik üçgenin hipotenüs etrafında döndürülmesiyle oluşan cisim. Hacmi eş tabanlı silindirin ⅓'üdür.",
            "ozellikler": [
                "Tek bir tepe noktası (köşe) vardır",
                "Hacmi = aynı taban ve yükseklikteki silindirin ⅓'ü",
                "Ana doğru (l) = √(r²+h²) — Pisagor!",
                "Yanal yüzeyi açılınca daire dilimi olur",
                "3 koni = 1 silindir (aynı r ve h ile)",
            ],
            "gercek_hayat": "🍦 Dondurma külahı, 🎄 Çam ağacı, 🏔️ Volkan, 🎉 Parti şapkası, 📢 Megafon",
            "hesaplama_ornek": "r=4 cm, h=6 cm → l=7.21 cm, V=100.5 cm³, A=141.0 cm²",
            "euler": "Euler formülü düz yüzeyler için geçerlidir",
            "sinif": "8-10. Sınıf",
        },
        "Küre (Sphere)": {
            "yuzey": "1 eğri yüzey", "koşe": "0", "ayrıt": "0",
            "hacim": "V = ⁴⁄₃πr³", "alan": "A = 4πr²",
            "cevre": "Büyük daire çevresi = 2πr", "kosegen": "Çap = 2r",
            "emoji": "🏀", "renk": "#8b5cf6",
            "tanim": "Bir merkeze eşit uzaklıktaki tüm noktaların oluşturduğu cisim. Doğanın en mükemmel şekli.",
            "ozellikler": [
                "Köşesi, ayrıtı ve düz yüzeyi yoktur",
                "Aynı hacmi kaplayan cisimler arasında en küçük yüzey alanına sahiptir",
                "Sonsuz simetri ekseni vardır",
                "Her kesiti dairedir",
                "Yüzey alanı = aynı çaplı 4 dairenin alanı toplamı!",
                "Arşimet keşfi: Küre hacmi = onu çevreleyen silindirin ⅔'ü",
            ],
            "gercek_hayat": "🏀 Top, 🌍 Dünya, 🫧 Sabun köpüğü, 🔮 Kristal küre, 🍊 Portakal",
            "hesaplama_ornek": "r=5 cm → V=523.6 cm³, A=314.2 cm²",
            "euler": "Euler formülü düz yüzeyler için geçerlidir",
            "sinif": "8-11. Sınıf",
        },
        "Altıgen Prizma": {
            "yuzey": "2 altıgen + 6 dikdörtgen", "koşe": "12 köşe", "ayrıt": "18 ayrıt",
            "hacim": "V = (3√3/2)a²·h", "alan": "A = 3√3a² + 6ah",
            "cevre": "Taban çevresi = 6a", "kosegen": "Yüz köşegenleri",
            "emoji": "🔷", "renk": "#06b6d4",
            "tanim": "İki tabanı düzgün altıgen, yanal yüzleri dikdörtgen olan prizma.",
            "ozellikler": [
                "Tabanları 6 eş eşkenar üçgene bölünebilir",
                "Arıların bal peteği altıgen prizma şeklindedir",
                "6 simetri ekseni vardır",
                "Kalem genellikle altıgen prizma şeklindedir",
                "Euler: 12-18+8=2 ✓",
            ],
            "gercek_hayat": "🐝 Bal peteği, ✏️ Kalem, 🔩 Somun (vida), 🪨 Bazalt sütunları",
            "hesaplama_ornek": "a=3 cm, h=8 cm → V=187.1 cm³, A=190.7 cm²",
            "euler": "K=12, A=18, Y=8 → 12-18+8=2 ✓",
            "sinif": "7-10. Sınıf",
        },
        "Piramit (Pyramid)": {
            "yuzey": "1 kare + 4 üçgen", "koşe": "5 köşe", "ayrıt": "8 ayrıt",
            "hacim": "V = ⅓·a²·h", "alan": "A = a² + 2al",
            "cevre": "Taban çevresi = 4a", "kosegen": "Yanal ayrıt, apothem",
            "emoji": "🔺", "renk": "#f97316",
            "tanim": "Tabanı çokgen, yanal yüzleri üçgen olan ve bir tepe noktasında birleşen cisim.",
            "ozellikler": [
                "Hacmi = aynı taban ve yükseklikteki prizmanın ⅓'ü",
                "Mısır piramitleri kare tabanlı piramittir",
                "Yanal yüzey alanı = ½ × çevre × apothem",
                "Tepe noktası tabanın merkezinin tam üstündeyse 'dik piramit'tir",
                "Euler: 5-8+5=2 ✓",
            ],
            "gercek_hayat": "🏛️ Mısır piramitleri, 🔺 Çatı, 🧀 Peynir dilimi, 🎪 Çadır tepesi",
            "hesaplama_ornek": "a=6 cm, h=8 cm → V=96 cm³, apothem=√(h²+(a/2)²)=8.54 cm",
            "euler": "K=5, A=8, Y=5 → 5-8+5=2 ✓",
            "sinif": "7-10. Sınıf",
        },
        "Oktahedron": {
            "yuzey": "8 eşkenar üçgen", "koşe": "6 köşe", "ayrıt": "12 ayrıt",
            "hacim": "V = (√2/3)a³", "alan": "A = 2√3·a²",
            "cevre": "—", "kosegen": "Uzun köşegen = a√2",
            "emoji": "💎", "renk": "#ec4899",
            "tanim": "8 eşkenar üçgen yüzeyden oluşan düzgün çokyüzlü. İki piramidi tabandan birleştirin!",
            "ozellikler": [
                "5 Platonik cisimden biridir",
                "Her köşede 4 yüz birleşir",
                "İki kare tabanlı piramidi tabandan yapıştırınca olur",
                "Küpün dualidir (köşe↔yüz)",
                "Elmas kristali oktahedron şeklindedir",
                "Euler: 6-12+8=2 ✓",
            ],
            "gercek_hayat": "💎 Elmas kristali, 🎲 D8 zar (rol yapma oyunları), ✡️ Yıldız şekli",
            "hesaplama_ornek": "a=4 cm → V=30.17 cm³, A=55.43 cm²",
            "euler": "K=6, A=12, Y=8 → 6-12+8=2 ✓",
            "sinif": "9-12. Sınıf",
        },
        "Tetrahedron": {
            "yuzey": "4 eşkenar üçgen", "koşe": "4 köşe", "ayrıt": "6 ayrıt",
            "hacim": "V = (√2/12)a³", "alan": "A = √3·a²",
            "cevre": "Toplam ayrıt = 6a", "kosegen": "—",
            "emoji": "🔺", "renk": "#ef4444",
            "tanim": "4 eşkenar üçgen yüzeyden oluşan en basit Platonik cisim. Ateş elementini temsil eder.",
            "ozellikler": [
                "En az yüzeye sahip Platonik cisim (4 yüz)",
                "Her köşede 3 yüz birleşir",
                "Kendinin duali — tetrahedronun duali yine tetrahedron!",
                "Metan (CH₄) molekülü tetrahedron şeklinde",
                "Euler: 4-6+4=2 ✓",
            ],
            "gercek_hayat": "🧪 Metan molekülü, 🎲 D4 zar, 🔺 Üçgen piramit, 🏗️ Uzay kafes yapılar",
            "hesaplama_ornek": "a=6 cm → V=25.46 cm³, A=62.35 cm²",
            "euler": "K=4, A=6, Y=4 → 4-6+4=2 ✓",
            "sinif": "9-12. Sınıf",
        },
        "İkosahedron": {
            "yuzey": "20 eşkenar üçgen", "koşe": "12 köşe", "ayrıt": "30 ayrıt",
            "hacim": "V = (5(3+√5)/12)a³", "alan": "A = 5√3·a²",
            "cevre": "—", "kosegen": "—",
            "emoji": "⚽", "renk": "#10b981",
            "tanim": "20 eşkenar üçgen yüzeyden oluşan Platonik cisim. Küreye en yakın düzgün çokyüzlü.",
            "ozellikler": [
                "En çok yüzeye sahip Platonik cisim (20 yüz)",
                "Her köşede 5 üçgen birleşir",
                "Futbol topunun temel yapısı (kesilmiş ikosahedron)",
                "Virüs kapsülleri ikosahedron şeklinde",
                "Euler: 12-30+20=2 ✓",
            ],
            "gercek_hayat": "⚽ Futbol topu yapısı, 🦠 Virüs kapsülü, 🎲 D20 zar, 🌐 Jeodesik kubbe",
            "hesaplama_ornek": "a=4 cm → V=349.1 cm³, A=138.6 cm²",
            "euler": "K=12, A=30, Y=20 → 12-30+20=2 ✓",
            "sinif": "10-12. Sınıf",
        },
        "Dodekahedron": {
            "yuzey": "12 düzgün beşgen", "koşe": "20 köşe", "ayrıt": "30 ayrıt",
            "hacim": "V = (15+7√5)/4·a³", "alan": "A = 3√(25+10√5)·a²",
            "cevre": "—", "kosegen": "—",
            "emoji": "🔮", "renk": "#8b5cf6",
            "tanim": "12 düzgün beşgen yüzeyden oluşan Platonik cisim. Evreni temsil eder.",
            "ozellikler": [
                "Her köşede 3 beşgen birleşir",
                "Platon'a göre evreni temsil eden cisim",
                "Altın oran (φ) ile doğrudan ilişkili",
                "Euler: 20-30+12=2 ✓",
            ],
            "gercek_hayat": "🔮 Dekoratif obje, 🎲 D12 zar, 🌌 Evren modeli (Platon)",
            "hesaplama_ornek": "a=3 cm → V=187.7 cm³, A=185.8 cm²",
            "euler": "K=20, A=30, Y=12 → 20-30+12=2 ✓",
            "sinif": "10-12. Sınıf",
        },
        "Kesik Koni": {
            "yuzey": "2 daire + yanal", "koşe": "0", "ayrıt": "2 daire",
            "hacim": "V = ⅓πh(R²+Rr+r²)", "alan": "A = π(R²+r²+l(R+r))",
            "cevre": "Üst çevre=2πr, Alt çevre=2πR", "kosegen": "Ana doğru l=√(h²+(R-r)²)",
            "emoji": "🪣", "renk": "#f97316",
            "tanim": "Koninin tepe kısmının bir düzlemle kesilmesiyle oluşan cisim. Kova, saksı şekli.",
            "ozellikler": [
                "İki farklı yarıçaplı daire tabanı var (R ve r)",
                "R=r olursa silindir olur, r=0 olursa koni olur",
                "Günlük hayatta en çok karşılaşılan cisimlerden",
                "Ana doğru: l = √(h² + (R-r)²)",
            ],
            "gercek_hayat": "🪣 Kova, 🪴 Saksı, 🥤 Bardak, 🎩 Fötr şapka, 🚀 Roket burnu",
            "hesaplama_ornek": "R=5, r=3, h=8 cm → V=412.3 cm³",
            "euler": "Eğri yüzeylidir — Euler düz yüzeyler için geçerlidir",
            "sinif": "9-11. Sınıf",
        },
        "Yarım Küre": {
            "yuzey": "1 yarı küre + 1 daire", "koşe": "0", "ayrıt": "1 daire",
            "hacim": "V = ⅔πr³", "alan": "A = 3πr²",
            "cevre": "Taban çevresi = 2πr", "kosegen": "Çap = 2r",
            "emoji": "🥣", "renk": "#06b6d4",
            "tanim": "Kürenin tam ortadan ikiye bölünmesiyle oluşan cisim.",
            "ozellikler": [
                "Hacmi = kürenin yarısı = ⅔πr³",
                "Yüzey alanı = 2πr² (eğri) + πr² (düz taban) = 3πr²",
                "Kubbe mimarisinin temel şekli",
                "Kase, kâse şeklindeki nesneler",
            ],
            "gercek_hayat": "🥣 Kase, 🏛️ Kubbe, 🪖 Kask, 🌍 Dünya'nın yarısı, 🍦 Dondurma topağı",
            "hesaplama_ornek": "r=6 cm → V=452.4 cm³, A=339.3 cm²",
            "euler": "Eğri yüzeylidir",
            "sinif": "8-11. Sınıf",
        },
        "Elipsoid": {
            "yuzey": "1 eğri yüzey", "koşe": "0", "ayrıt": "0",
            "hacim": "V = ⁴⁄₃π·a·b·c", "alan": "A ≈ yaklaşık formül",
            "cevre": "—", "kosegen": "3 yarıçap: a, b, c",
            "emoji": "🏈", "renk": "#eab308",
            "tanim": "Kürenin 3 farklı yarıçapla gerilmesiyle oluşan cisim. Amerikan futbol topu şekli.",
            "ozellikler": [
                "3 yarıçap: a (x), b (y), c (z)",
                "a=b=c olursa küre olur",
                "Dünya tam bir küre değil, hafif basık elipsoiddir",
                "Gezegenler ve galaksiler elipsoid şeklinde",
            ],
            "gercek_hayat": "🏈 Amerikan futbol topu, 🌍 Dünya (basık), 🥚 Yumurta, 🪐 Gezegenler",
            "hesaplama_ornek": "a=5, b=4, c=3 cm → V=251.3 cm³",
            "euler": "Eğri yüzeylidir",
            "sinif": "10-12. Sınıf",
        },
        "Üçgen Piramit": {
            "yuzey": "1 üçgen + 3 üçgen", "koşe": "4 köşe", "ayrıt": "6 ayrıt",
            "hacim": "V = ⅓·(taban alanı)·h", "alan": "Taban + 3 yanal üçgen",
            "cevre": "Taban çevresi = 3a", "kosegen": "—",
            "emoji": "⛰️", "renk": "#10b981",
            "tanim": "Tabanı üçgen olan piramit. Tüm yüzleri üçgendir (tetrahedron'un genel hali).",
            "ozellikler": [
                "4 yüzünün hepsi üçgendir",
                "Taban eşkenar üçgen ise ve yanal yüzler eşit ise = tetrahedron",
                "En az yüzlü piramit",
                "Euler: 4-6+4=2 ✓",
            ],
            "gercek_hayat": "⛰️ Dağ tepesi, 🏗️ Çatı yapısı, 🔺 Üçgen piramit bulmaca",
            "hesaplama_ornek": "Eşkenar üçgen taban a=8, h=10 → V=92.4 cm³",
            "euler": "K=4, A=6, Y=4 → 4-6+4=2 ✓",
            "sinif": "7-10. Sınıf",
        },
        "Beşgen Prizma": {
            "yuzey": "2 beşgen + 5 dikdörtgen", "koşe": "10 köşe", "ayrıt": "15 ayrıt",
            "hacim": "V = (taban alanı)·h", "alan": "2·beşgen + 5·dikdörtgen",
            "cevre": "Taban çevresi = 5a", "kosegen": "Yüz köşegenleri",
            "emoji": "⬠", "renk": "#3b82f6",
            "tanim": "İki tabanı düzgün beşgen, yanal yüzleri dikdörtgen olan prizma.",
            "ozellikler": [
                "Pentagon (beşgen) tabanlı prizma",
                "ABD Savunma Bakanlığı binası Pentagon bu şekilde",
                "Euler: 10-15+7=2 ✓",
                "Düzgün beşgen alan = (5a²/4)·√(5+2√5)/√5",
            ],
            "gercek_hayat": "🏛️ Pentagon binası, ✏️ Bazı kalemler, 🪴 Saksı tasarımları",
            "hesaplama_ornek": "a=4, h=10 cm → V=275.3 cm³",
            "euler": "K=10, A=15, Y=7 → 10-15+7=2 ✓",
            "sinif": "8-11. Sınıf",
        },
        "Torus": {
            "yuzey": "1 eğri yüzey", "koşe": "0", "ayrıt": "0",
            "hacim": "V = 2π²Rr²", "alan": "A = 4π²Rr",
            "cevre": "—", "kosegen": "R=büyük yarıçap, r=küçük yarıçap",
            "emoji": "🍩", "renk": "#ec4899",
            "tanim": "Bir dairenin bir eksen etrafında döndürülmesiyle oluşan halka (simit) şekli.",
            "ozellikler": [
                "R = merkez eksen ile daire merkezi arası mesafe",
                "r = döndürülen dairenin yarıçapı",
                "Topolojide tek delikli yüzey (genus 1)",
                "Euler karakteristiği = 0 (küre=2, torus=0)",
                "Manyetik plazma kapları (tokamak) torus şeklinde",
            ],
            "gercek_hayat": "🍩 Donut/Simit, 🛟 Can simidi, 🪐 Satürn halkası, ⚛️ Tokamak reaktör",
            "hesaplama_ornek": "R=8, r=3 cm → V=1421.2 cm³, A=947.5 cm²",
            "euler": "Euler karakteristiği = 0 (delikli yüzey)",
            "sinif": "10-12. Sınıf",
        },
        "Paralel Yüzlü": {
            "yuzey": "6 paralelkenar", "koşe": "8 köşe", "ayrıt": "12 ayrıt",
            "hacim": "V = taban alanı × h", "alan": "2(S₁+S₂+S₃)",
            "cevre": "4(a+b+c)", "kosegen": "Cisim köşegeni",
            "emoji": "📐", "renk": "#f59e0b",
            "tanim": "Karşılıklı yüzleri paralel ve eş olan altı yüzlü cisim. Dikdörtgenler prizmasının eğik hali.",
            "ozellikler": [
                "Karşılıklı 3 çift yüz paralel ve eştir",
                "Köşegenler birbirini ortalar",
                "Tüm açılar 90° ise = dikdörtgenler prizması",
                "Kristal yapılarda sık görülür",
                "Euler: 8-12+6=2 ✓",
            ],
            "gercek_hayat": "💎 Kristal yapılar, 📦 Eğik kutu, 🧱 Eğik tuğla",
            "hesaplama_ornek": "Taban 5×4 cm, h=6 cm → V=120 cm³",
            "euler": "K=8, A=12, Y=6 → 8-12+6=2 ✓",
            "sinif": "9-11. Sınıf",
        },
        "Kesik Piramit": {
            "yuzey": "2 kare + 4 yamuk", "koşe": "8 köşe", "ayrıt": "12 ayrıt",
            "hacim": "V = ⅓h(S₁+S₂+√(S₁S₂))", "alan": "S₁+S₂+yanal",
            "cevre": "Alt 4a + Üst 4b", "kosegen": "Yanal ayrıtlar",
            "emoji": "🏛️", "renk": "#6366f1",
            "tanim": "Piramidin tepe kısmının bir düzlemle kesilmesiyle oluşan cisim. Maya piramitleri bu şekildedir.",
            "ozellikler": [
                "İki farklı boyutta kare tabanı var",
                "Alt taban büyük (a), üst taban küçük (b)",
                "b=0 olursa tam piramit, a=b olursa prizma olur",
                "Yanal yüzler ikizkenar yamuktur",
                "Euler: 8-12+6=2 ✓",
            ],
            "gercek_hayat": "🏛️ Maya/Aztek piramitleri, 🪴 Saksı, 🏗️ Bina temeli, 🎂 Düğün pastası katları",
            "hesaplama_ornek": "a=10, b=4, h=8 cm → V=362.7 cm³",
            "euler": "K=8, A=12, Y=6 → 8-12+6=2 ✓",
            "sinif": "9-11. Sınıf",
        },
        "Sekizgen Prizma": {
            "yuzey": "2 sekizgen + 8 dikdörtgen", "koşe": "16 köşe", "ayrıt": "24 ayrıt",
            "hacim": "V = 2(1+√2)a²·h", "alan": "4(1+√2)a² + 8ah",
            "cevre": "Taban çevresi = 8a", "kosegen": "Yüz köşegenleri",
            "emoji": "🛑", "renk": "#ef4444",
            "tanim": "İki tabanı düzgün sekizgen, yanal yüzleri dikdörtgen olan prizma. Dur işareti şekli.",
            "ozellikler": [
                "8 kenarlı düzgün çokgen tabanlı",
                "Trafik dur işareti (STOP) sekizgen şeklinde",
                "Euler: 16-24+10=2 ✓",
                "Silindire en yakın prizma",
            ],
            "gercek_hayat": "🛑 STOP tabelası, 🏛️ Vaftiz havuzu, ⌚ Bazı saat kasaları",
            "hesaplama_ornek": "a=3, h=10 cm → V=434.5 cm³",
            "euler": "K=16, A=24, Y=10 → 16-24+10=2 ✓",
            "sinif": "8-11. Sınıf",
        },
        "Çift Koni": {
            "yuzey": "2 yanal yüzey", "koşe": "2 (tepe noktaları)", "ayrıt": "1 orta daire",
            "hacim": "V = ⅔πr²h", "alan": "A = 2πrl",
            "cevre": "Orta daire = 2πr", "kosegen": "l = √(r²+(h/2)²)",
            "emoji": "💠", "renk": "#06b6d4",
            "tanim": "İki koniyi tabanlarından birleştirerek oluşan cisim. Elmas şekli.",
            "ozellikler": [
                "İki koninin tabanlarının birleşmesiyle oluşur",
                "Hacim = 2 × tek koni = ⅔πr²h",
                "Elmas kristali ve uçurtma şekli",
                "Optik lenslerde kullanılır",
            ],
            "gercek_hayat": "💎 Elmas kesimi, 🪁 Uçurtma, 🔷 Dekoratif objeler, 🏏 Kriket topu şekli",
            "hesaplama_ornek": "r=4, h=12 cm → V=201.1 cm³",
            "euler": "Eğri yüzeylidir",
            "sinif": "9-11. Sınıf",
        },
        "Kapsül": {
            "yuzey": "1 silindir + 2 yarım küre", "koşe": "0", "ayrıt": "0",
            "hacim": "V = πr²h + ⁴⁄₃πr³", "alan": "A = 2πrh + 4πr²",
            "cevre": "—", "kosegen": "Toplam boy = h + 2r",
            "emoji": "💊", "renk": "#10b981",
            "tanim": "Silindirin iki ucuna yarım küre eklenmesiyle oluşan cisim. İlaç kapsülü şekli.",
            "ozellikler": [
                "Silindir + 2 yarım küre = silindir + 1 tam küre",
                "Basınç kapları bu şekilde (en güçlü yapı)",
                "Uzay kapsülleri bu formu kullanır",
                "Roket burunları kapsül şeklinde",
            ],
            "gercek_hayat": "💊 İlaç kapsülü, 🚀 Uzay kapsülü, ⛽ LPG tüpü, 🏊 Denizaltı",
            "hesaplama_ornek": "r=3, h=10 cm → V=396.0 cm³",
            "euler": "Eğri yüzeylidir",
            "sinif": "9-12. Sınıf",
        },
        "Yıldız Prizması": {
            "yuzey": "2 yıldız + 10 dikdörtgen", "koşe": "20 köşe", "ayrıt": "30 ayrıt",
            "hacim": "V ≈ özel hesap", "alan": "2·yıldız + 10·dikdörtgen",
            "cevre": "10 kenar", "kosegen": "—",
            "emoji": "⭐", "renk": "#eab308",
            "tanim": "İki tabanı 5 köşeli yıldız olan prizma. Dekoratif şekil.",
            "ozellikler": [
                "Tabanları beş köşeli yıldız (pentagram)",
                "10 yanal dikdörtgen yüzü var",
                "Noel süsleri ve dekoratif objelerde kullanılır",
                "5 dış + 5 iç köşe = 10 köşe/taban",
            ],
            "gercek_hayat": "⭐ Yıldız şeker kutusu, 🎄 Noel süsü, 🏅 Madalya şekli",
            "hesaplama_ornek": "Özel geometrik hesap gerekir",
            "euler": "K=20, A=30, Y=12 → 20-30+12=2 ✓",
            "sinif": "9-12. Sınıf",
        },
        "Altıgen Piramit": {
            "yuzey": "1 altıgen + 6 üçgen", "koşe": "7 köşe", "ayrıt": "12 ayrıt",
            "hacim": "V = ⅓·(3√3/2)a²·h", "alan": "Alt + 6 yanal üçgen",
            "cevre": "Taban çevresi = 6a", "kosegen": "Yanal ayrıt",
            "emoji": "🔷", "renk": "#8b5cf6",
            "tanim": "Tabanı düzgün altıgen, yanal yüzleri üçgen olan piramit.",
            "ozellikler": [
                "6 yanal üçgen yüzü + 1 altıgen taban",
                "Arı kovanı + piramit birleşimi",
                "Euler: 7-12+7=2 ✓",
                "Kristal yapılarda görülür",
            ],
            "gercek_hayat": "💎 Kristal uçları, 🏗️ Mimari detaylar, 🔷 Geometrik tasarım",
            "hesaplama_ornek": "a=4, h=9 cm → V=124.7 cm³",
            "euler": "K=7, A=12, Y=7 → 7-12+7=2 ✓",
            "sinif": "8-11. Sınıf",
        },
        "Kesik Oktahedron": {
            "yuzey": "8 altıgen + 6 kare", "koşe": "24 köşe", "ayrıt": "36 ayrıt",
            "hacim": "V = 8√2·a³", "alan": "A = (6+12√3)a²",
            "cevre": "—", "kosegen": "—",
            "emoji": "⬡", "renk": "#f97316",
            "tanim": "Oktahedronun köşelerinin kesilmesiyle oluşan Arşimet cismi. Uzay doldurabilen nadir cisimlerden.",
            "ozellikler": [
                "14 yüz: 8 altıgen + 6 kare",
                "Arşimet cisimlerinden biri",
                "Uzayı tek başına doldurabilir (tessellation)!",
                "Euler: 24-36+14=2 ✓",
            ],
            "gercek_hayat": "🧊 Kristal yapılar, 🏗️ Uzay kafes sistemleri, ⚛️ Moleküler yapılar",
            "hesaplama_ornek": "a=3 cm → V=305.5 cm³, A=222.5 cm²",
            "euler": "K=24, A=36, Y=14 → 24-36+14=2 ✓",
            "sinif": "10-12. Sınıf",
        },
        "Çan Yüzeyi": {
            "yuzey": "1 eğri yüzey + 1 daire", "koşe": "0", "ayrıt": "1 daire",
            "hacim": "V ≈ ⅔πr²h", "alan": "A ≈ eğri yüzey hesabı",
            "cevre": "Taban çevresi = 2πr", "kosegen": "—",
            "emoji": "🔔", "renk": "#eab308",
            "tanim": "Çan şeklinde eğri yüzey. Gauss eğrisi (normal dağılım) 3D'ye döndürüldüğünde oluşur.",
            "ozellikler": [
                "Gauss eğrisinin rotasyonel hali",
                "İstatistikte normal dağılım çanı",
                "Akustik tasarımda önemli",
                "Simetri ekseni etrafında dönel",
            ],
            "gercek_hayat": "🔔 Çan, 📊 Gauss eğrisi 3D, 🎺 Trompet ağzı, 🪂 Paraşüt",
            "hesaplama_ornek": "Yaklaşık hesap — şekle bağlı",
            "euler": "Eğri yüzeylidir",
            "sinif": "10-12. Sınıf",
        },
        "Helisel Silindir": {
            "yuzey": "Sarmal yüzey", "koşe": "0", "ayrıt": "0",
            "hacim": "V = πr²·L (silindir hacmi)", "alan": "Sarmal yüzey alanı",
            "cevre": "—", "kosegen": "Sarmal adımı (pitch)",
            "emoji": "🧬", "renk": "#ec4899",
            "tanim": "Silindir yüzeyinde sarmal (helis) çizen yapı. DNA çift sarmalı bu şekilde.",
            "ozellikler": [
                "Helis: sabit yarıçapla yükselen sarmal eğri",
                "DNA çift sarmalı helisel yapıdadır",
                "Vida dişleri helis şeklinde",
                "Parametrik: x=r·cos(t), y=r·sin(t), z=c·t",
            ],
            "gercek_hayat": "🧬 DNA sarmalı, 🔩 Vida, 🌀 Yay, 🎡 Helezon merdiven, 🍭 Lolipop",
            "hesaplama_ornek": "r=2, pitch=3, tur=5 → yükseklik=15 cm",
            "euler": "Eğri yüzeylidir",
            "sinif": "11-12. Sınıf",
        },
        "Paraboloid": {
            "yuzey": "1 eğri yüzey", "koşe": "0", "ayrıt": "0",
            "hacim": "V = ½πr²h", "alan": "A = özel integral",
            "cevre": "Ağız çevresi = 2πr", "kosegen": "Odak noktası",
            "emoji": "📡", "renk": "#3b82f6",
            "tanim": "Parabolün bir eksen etrafında döndürülmesiyle oluşan yüzey. Uydu anteni şekli.",
            "ozellikler": [
                "z = x² + y² denklemiyle tanımlanır",
                "Paralel ışınları odak noktasına toplar",
                "Uydu antenleri ve teleskop aynaları paraboloid",
                "Hacmi = aynı r ve h'li koninin 1.5 katı",
            ],
            "gercek_hayat": "📡 Çanak anten, 🔭 Teleskop aynası, 🏟️ Olimpiyat meşalesi, 🔦 Far reflektörü",
            "hesaplama_ornek": "r=5, h=8 cm → V=314.2 cm³",
            "euler": "Eğri yüzeylidir",
            "sinif": "11-12. Sınıf",
        },
        "Hiperboloid": {
            "yuzey": "1 eğri yüzey", "koşe": "0", "ayrıt": "0",
            "hacim": "V = özel integral", "alan": "A = özel integral",
            "cevre": "—", "kosegen": "—",
            "emoji": "🗼", "renk": "#f59e0b",
            "tanim": "Hiperbolün bir eksen etrafında döndürülmesiyle oluşan yüzey. Soğutma kulesi şekli.",
            "ozellikler": [
                "x²/a² + y²/b² - z²/c² = 1 denklemi",
                "Tek parçalı (kuleler) ve çift parçalı türleri var",
                "Düz çizgilerden oluşan eğri yüzey (çifte regle yüzey)!",
                "Nükleer santral soğutma kuleleri bu şekilde",
                "En az malzemeyle en güçlü yapı",
            ],
            "gercek_hayat": "🗼 Soğutma kulesi, 🏗️ Kobe Port Tower, 🌀 Çöp sepeti şekli, 🪑 Tabure bacağı",
            "hesaplama_ornek": "Parametrelere bağlı — özel hesap",
            "euler": "Eğri yüzeylidir",
            "sinif": "11-12. Sınıf",
        },
    }

    bilgi = cisim_bilgi.get(cisim, {})

    # 3D Canvas — interaktif cisim (önce göster)
    _render_3d_canvas(cisim)

    if bilgi:
        # Üst özet kartları
        cols = st.columns(6)
        info_items = [
            (bilgi["emoji"], cisim.split(" (")[0], "Cisim"),
            ("📐", bilgi["yuzey"], "Yüzey"),
            ("📍", bilgi["koşe"], "Köşe"),
            ("📏", bilgi["ayrıt"], "Ayrıt"),
            ("📦", bilgi["hacim"], "Hacim Formülü"),
            ("🔲", bilgi["alan"], "Yüzey Alanı"),
        ]
        for col, (icon, val, label) in zip(cols, info_items):
            with col:
                _render_html(f"""
                <div class="mat-stat-card" style="padding:12px;min-height:90px;border-color:{bilgi['renk']}30">
                    <div style="font-size:1.2rem">{icon}</div>
                    <div style="font-weight:700;color:{bilgi['renk']} !important;font-size:0.78rem">{val}</div>
                    <div class="mat-stat-label" style="font-size:0.65rem">{label}</div>
                </div>
                """)

        # DETAYLI BİLGİ KARTI
        with st.expander(f"📋 {cisim} — Detaylı Bilgi Kartı", expanded=True):
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#0f0524,#1a0a3e);border-radius:20px;padding:24px;
                         border:2px solid {bilgi['renk']}30;position:relative;overflow:hidden">
                <div style="position:absolute;top:-30px;right:-30px;font-size:8rem;opacity:0.04">{bilgi['emoji']}</div>

                <!-- Tanım -->
                <div style="position:relative;z-index:1;margin-bottom:20px">
                    <div style="font-size:1.3rem;font-weight:800;color:#e0e7ff !important;margin-bottom:8px">
                        {bilgi['emoji']} {cisim}
                    </div>
                    <div style="font-size:0.9rem;color:#c4b5fd !important;line-height:1.6;
                                 background:rgba(99,102,241,0.08);border-radius:12px;padding:14px;
                                 border-left:4px solid {bilgi['renk']}">
                        {bilgi['tanim']}
                    </div>
                </div>

                <!-- Formüller Grid -->
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:20px;position:relative;z-index:1">
                    <div style="background:rgba(99,102,241,0.08);border-radius:12px;padding:14px;text-align:center;
                                 border:1px solid rgba(99,102,241,0.15)">
                        <div style="font-size:0.7rem;color:#94a3b8 !important;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Hacim</div>
                        <div style="font-size:1.1rem;font-weight:700;color:{bilgi['renk']} !important;
                                     font-family:'Cambria Math','Times New Roman',serif">{bilgi['hacim']}</div>
                    </div>
                    <div style="background:rgba(99,102,241,0.08);border-radius:12px;padding:14px;text-align:center;
                                 border:1px solid rgba(99,102,241,0.15)">
                        <div style="font-size:0.7rem;color:#94a3b8 !important;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Yüzey Alanı</div>
                        <div style="font-size:1.1rem;font-weight:700;color:{bilgi['renk']} !important;
                                     font-family:'Cambria Math','Times New Roman',serif">{bilgi['alan']}</div>
                    </div>
                    <div style="background:rgba(99,102,241,0.08);border-radius:12px;padding:14px;text-align:center;
                                 border:1px solid rgba(99,102,241,0.15)">
                        <div style="font-size:0.7rem;color:#94a3b8 !important;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Köşegen</div>
                        <div style="font-size:0.9rem;font-weight:700;color:{bilgi['renk']} !important;
                                     font-family:'Cambria Math','Times New Roman',serif">{bilgi['kosegen']}</div>
                    </div>
                </div>

                <!-- Euler Formülü -->
                <div style="background:rgba(234,179,8,0.08);border-radius:12px;padding:12px 16px;margin-bottom:16px;
                             text-align:center;border:1px dashed rgba(234,179,8,0.2);position:relative;z-index:1">
                    <div style="font-size:0.7rem;color:#fde68a !important;margin-bottom:4px">⚡ Euler Formülü (K - A + Y = 2)</div>
                    <div style="font-size:0.9rem;font-weight:700;color:#eab308 !important">{bilgi['euler']}</div>
                </div>
            </div>
            """)

            # Özellikler
            st.markdown(f"**📌 Temel Özellikler:**")
            for oz in bilgi["ozellikler"]:
                st.markdown(f"- {oz}")

            # Hesaplama örneği
            st.markdown("---")
            _render_html(f"""
            <div style="background:rgba(16,185,129,0.08);border-radius:12px;padding:14px;
                         border:1px solid rgba(16,185,129,0.2);margin-bottom:12px">
                <div style="font-weight:700;color:#10b981 !important;font-size:0.85rem;margin-bottom:6px">🧮 Hesaplama Örneği</div>
                <div style="color:#86efac !important;font-size:0.9rem;font-family:'Courier New',monospace">{bilgi['hesaplama_ornek']}</div>
            </div>
            """)

            # Gerçek hayat
            _render_html(f"""
            <div style="background:rgba(99,102,241,0.08);border-radius:12px;padding:14px;
                         border:1px solid rgba(99,102,241,0.2)">
                <div style="font-weight:700;color:#818cf8 !important;font-size:0.85rem;margin-bottom:6px">🌍 Gerçek Hayatta Nerede?</div>
                <div style="color:#a5b4fc !important;font-size:0.95rem">{bilgi['gercek_hayat']}</div>
            </div>
            """)

            st.caption(f"📚 Sınıf Düzeyi: {bilgi['sinif']}")

        # İnteraktif hesaplayıcı
        with st.expander(f"🧮 {cisim} Hesaplayıcı — Kendi Değerlerini Gir!", expanded=False):
            _render_cisim_hesaplayici(cisim, bilgi)


def _render_cisim_hesaplayici(cisim: str, bilgi: dict):
    """Cisim ölçülerini gir, hacim/alan/köşegen otomatik hesapla."""
    import math

    cisim_key = cisim.split(" (")[0]

    if cisim_key in ("Küp", "Oktahedron"):
        a = st.number_input("Kenar uzunluğu (a) cm:", 0.1, 1000.0, 5.0, key=f"3d_calc_{cisim_key}_a")
        if cisim_key == "Küp":
            hacim = a ** 3
            alan = 6 * a ** 2
            kosegen_yuz = a * math.sqrt(2)
            kosegen_cisim = a * math.sqrt(3)
            st.markdown(f"**Hacim:** {hacim:.2f} cm³")
            st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")
            st.markdown(f"**Yüz Köşegeni:** {kosegen_yuz:.2f} cm")
            st.markdown(f"**Cisim Köşegeni:** {kosegen_cisim:.2f} cm")
            st.markdown(f"**Toplam Ayrıt Uzunluğu:** {12*a:.2f} cm")
        else:
            hacim = (math.sqrt(2) / 3) * a ** 3
            alan = 2 * math.sqrt(3) * a ** 2
            st.markdown(f"**Hacim:** {hacim:.2f} cm³")
            st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")

    elif cisim_key == "Dikdörtgenler Prizması":
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("a (cm):", 0.1, 1000.0, 3.0, key="3d_calc_dp_a")
        with col2:
            b = st.number_input("b (cm):", 0.1, 1000.0, 4.0, key="3d_calc_dp_b")
        with col3:
            c = st.number_input("c (cm):", 0.1, 1000.0, 5.0, key="3d_calc_dp_c")
        hacim = a * b * c
        alan = 2 * (a*b + b*c + a*c)
        kosegen = math.sqrt(a**2 + b**2 + c**2)
        st.markdown(f"**Hacim:** {hacim:.2f} cm³")
        st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")
        st.markdown(f"**Cisim Köşegeni:** {kosegen:.2f} cm")

    elif cisim_key in ("Silindir", "Koni"):
        col1, col2 = st.columns(2)
        with col1:
            r = st.number_input("Yarıçap (r) cm:", 0.1, 500.0, 4.0, key=f"3d_calc_{cisim_key}_r")
        with col2:
            h = st.number_input("Yükseklik (h) cm:", 0.1, 500.0, 6.0, key=f"3d_calc_{cisim_key}_h")
        if cisim_key == "Silindir":
            hacim = math.pi * r**2 * h
            alan = 2 * math.pi * r * (r + h)
            st.markdown(f"**Hacim:** {hacim:.2f} cm³")
            st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")
            st.markdown(f"**Taban Çevresi:** {2*math.pi*r:.2f} cm")
            st.markdown(f"**Taban Alanı:** {math.pi*r**2:.2f} cm²")
        else:
            l = math.sqrt(r**2 + h**2)
            hacim = (1/3) * math.pi * r**2 * h
            alan = math.pi * r * (r + l)
            st.markdown(f"**Hacim:** {hacim:.2f} cm³")
            st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")
            st.markdown(f"**Ana Doğru (l):** {l:.2f} cm")
            st.markdown(f"**Taban Çevresi:** {2*math.pi*r:.2f} cm")

    elif cisim_key == "Küre":
        r = st.number_input("Yarıçap (r) cm:", 0.1, 500.0, 5.0, key="3d_calc_kure_r")
        hacim = (4/3) * math.pi * r**3
        alan = 4 * math.pi * r**2
        st.markdown(f"**Hacim:** {hacim:.2f} cm³")
        st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")
        st.markdown(f"**Çap:** {2*r:.2f} cm")
        st.markdown(f"**Büyük Daire Çevresi:** {2*math.pi*r:.2f} cm")
        st.markdown(f"**Büyük Daire Alanı:** {math.pi*r**2:.2f} cm²")

    elif cisim_key == "Piramit":
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("Taban kenarı (a) cm:", 0.1, 500.0, 6.0, key="3d_calc_pir_a")
        with col2:
            h = st.number_input("Yükseklik (h) cm:", 0.1, 500.0, 8.0, key="3d_calc_pir_h")
        apothem = math.sqrt(h**2 + (a/2)**2)
        hacim = (1/3) * a**2 * h
        yanal = 2 * a * apothem
        alan = a**2 + yanal
        st.markdown(f"**Hacim:** {hacim:.2f} cm³")
        st.markdown(f"**Taban Alanı:** {a**2:.2f} cm²")
        st.markdown(f"**Yanal Yüzey Alanı:** {yanal:.2f} cm²")
        st.markdown(f"**Toplam Yüzey Alanı:** {alan:.2f} cm²")
        st.markdown(f"**Apothem:** {apothem:.2f} cm")

    elif cisim_key == "Altıgen Prizma":
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("Taban kenarı (a) cm:", 0.1, 500.0, 3.0, key="3d_calc_alt_a")
        with col2:
            h = st.number_input("Yükseklik (h) cm:", 0.1, 500.0, 8.0, key="3d_calc_alt_h")
        hacim = (3 * math.sqrt(3) / 2) * a**2 * h
        alan = 3 * math.sqrt(3) * a**2 + 6 * a * h
        st.markdown(f"**Hacim:** {hacim:.2f} cm³")
        st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")
        st.markdown(f"**Taban Alanı:** {(3*math.sqrt(3)/2)*a**2:.2f} cm²")
        st.markdown(f"**Taban Çevresi:** {6*a:.2f} cm")

    elif cisim_key == "Kesik Koni":
        col1, col2, col3 = st.columns(3)
        with col1:
            R = st.number_input("Büyük yarıçap (R) cm:", 0.1, 500.0, 5.0, key="3d_calc_kk_R")
        with col2:
            r = st.number_input("Küçük yarıçap (r) cm:", 0.1, 500.0, 3.0, key="3d_calc_kk_r")
        with col3:
            h = st.number_input("Yükseklik (h) cm:", 0.1, 500.0, 8.0, key="3d_calc_kk_h")
        l = math.sqrt(h**2 + (R - r)**2)
        hacim = (1/3) * math.pi * h * (R**2 + R*r + r**2)
        alan = math.pi * (R**2 + r**2 + l*(R + r))
        st.markdown(f"**Hacim:** {hacim:.2f} cm³")
        st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")
        st.markdown(f"**Ana Doğru (l):** {l:.2f} cm")

    elif cisim_key == "Yarım Küre":
        r = st.number_input("Yarıçap (r) cm:", 0.1, 500.0, 6.0, key="3d_calc_yk_r")
        hacim = (2/3) * math.pi * r**3
        alan = 3 * math.pi * r**2
        st.markdown(f"**Hacim:** {hacim:.2f} cm³")
        st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")

    elif cisim_key == "Elipsoid":
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("a (cm):", 0.1, 500.0, 5.0, key="3d_calc_el_a")
        with col2:
            b = st.number_input("b (cm):", 0.1, 500.0, 4.0, key="3d_calc_el_b")
        with col3:
            c = st.number_input("c (cm):", 0.1, 500.0, 3.0, key="3d_calc_el_c")
        hacim = (4/3) * math.pi * a * b * c
        st.markdown(f"**Hacim:** {hacim:.2f} cm³")

    elif cisim_key == "Torus":
        col1, col2 = st.columns(2)
        with col1:
            R = st.number_input("Büyük yarıçap (R) cm:", 0.1, 500.0, 8.0, key="3d_calc_tor_R")
        with col2:
            r = st.number_input("Küçük yarıçap (r) cm:", 0.1, 500.0, 3.0, key="3d_calc_tor_r")
        hacim = 2 * math.pi**2 * R * r**2
        alan = 4 * math.pi**2 * R * r
        st.markdown(f"**Hacim:** {hacim:.2f} cm³")
        st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")

    elif cisim_key == "Kesik Piramit":
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("Alt kenar (a) cm:", 0.1, 500.0, 10.0, key="3d_calc_kp_a")
        with col2:
            b = st.number_input("Üst kenar (b) cm:", 0.1, 500.0, 4.0, key="3d_calc_kp_b")
        with col3:
            h = st.number_input("Yükseklik (h) cm:", 0.1, 500.0, 8.0, key="3d_calc_kp_h")
        S1 = a**2
        S2 = b**2
        hacim = (1/3) * h * (S1 + S2 + math.sqrt(S1 * S2))
        st.markdown(f"**Hacim:** {hacim:.2f} cm³")
        st.markdown(f"**Alt Taban Alanı:** {S1:.2f} cm²")
        st.markdown(f"**Üst Taban Alanı:** {S2:.2f} cm²")

    else:  # Üçgen Prizma, Tetrahedron, vb.
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("Kenar (a) cm:", 0.1, 500.0, 6.0, key="3d_calc_gen_a")
        with col2:
            h = st.number_input("Yükseklik (h) cm:", 0.1, 500.0, 10.0, key="3d_calc_gen_h")
        if cisim_key == "Tetrahedron":
            hacim = (math.sqrt(2) / 12) * a**3
            alan = math.sqrt(3) * a**2
            st.markdown(f"**Hacim:** {hacim:.2f} cm³")
            st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")
        elif cisim_key in ("İkosahedron",):
            hacim = (5 * (3 + math.sqrt(5)) / 12) * a**3
            alan = 5 * math.sqrt(3) * a**2
            st.markdown(f"**Hacim:** {hacim:.2f} cm³")
            st.markdown(f"**Yüzey Alanı:** {alan:.2f} cm²")
        else:
            taban_alan = (math.sqrt(3) / 4) * a**2
            hacim = taban_alan * h
            alan = 2 * taban_alan + 3 * a * h
            st.markdown(f"**Hacim:** {hacim:.2f} cm³")
            st.markdown(f"**Taban Alanı:** {taban_alan:.2f} cm²")
            st.markdown(f"**Toplam Yüzey Alanı:** {alan:.2f} cm²")


def _render_3d_canvas(cisim: str):
    """3D canvas render — JavaScript ile interaktif döndürme."""
    import streamlit.components.v1 as components

    # Cisim tipi belirleme
    cisim_key = cisim.split(" (")[0].lower().replace("ü", "u").replace("ö", "o").replace("ş", "s").replace("ı", "i").replace("ç", "c")

    # Cisim modelleri için JS vertex/edge tanımları
    models_js = """
    const models = {
        kup: {
            vertices: [[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],
            edges: [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],
            faces: [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[0,3,7,4],[1,2,6,5]],
            color: '#818cf8', name: 'Küp'
        },
        dikdortgenler: {
            vertices: [[-1.5,-1,-0.7],[1.5,-1,-0.7],[1.5,1,-0.7],[-1.5,1,-0.7],[-1.5,-1,0.7],[1.5,-1,0.7],[1.5,1,0.7],[-1.5,1,0.7]],
            edges: [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],
            faces: [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[0,3,7,4],[1,2,6,5]],
            color: '#f59e0b', name: 'Dikdörtgenler Prizması'
        },
        ucgen: {
            vertices: [[0,-1,-1.2],[1,-1,0.6],[-1,-1,0.6],[0,1,-1.2],[1,1,0.6],[-1,1,0.6]],
            edges: [[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[0,3],[1,4],[2,5]],
            faces: [[0,1,2],[3,4,5],[0,1,4,3],[1,2,5,4],[0,2,5,3]],
            color: '#10b981', name: 'Üçgen Prizma'
        },
        piramit: {
            vertices: [[-1,-1,-1],[1,-1,-1],[1,-1,1],[-1,-1,1],[0,1.2,0]],
            edges: [[0,1],[1,2],[2,3],[3,0],[0,4],[1,4],[2,4],[3,4]],
            faces: [[0,1,2,3],[0,1,4],[1,2,4],[2,3,4],[3,0,4]],
            color: '#f97316', name: 'Piramit'
        },
        oktahedron: {
            vertices: [[0,1.2,0],[0,-1.2,0],[1.2,0,0],[-1.2,0,0],[0,0,1.2],[0,0,-1.2]],
            edges: [[0,2],[0,3],[0,4],[0,5],[1,2],[1,3],[1,4],[1,5],[2,4],[4,3],[3,5],[5,2]],
            faces: [[0,2,4],[0,4,3],[0,3,5],[0,5,2],[1,2,4],[1,4,3],[1,3,5],[1,5,2]],
            color: '#ec4899', name: 'Oktahedron'
        },
        altigen: {
            vertices: (function(){
                let v=[];
                for(let i=0;i<6;i++){
                    let a=Math.PI/3*i;
                    v.push([Math.cos(a),-1,Math.sin(a)]);
                }
                for(let i=0;i<6;i++){
                    let a=Math.PI/3*i;
                    v.push([Math.cos(a),1,Math.sin(a)]);
                }
                return v;
            })(),
            edges: (function(){
                let e=[];
                for(let i=0;i<6;i++){e.push([i,(i+1)%6]); e.push([i+6,(i+1)%6+6]); e.push([i,i+6]);}
                return e;
            })(),
            faces: [],
            color: '#06b6d4', name: 'Altıgen Prizma'
        },
        tetrahedron: {
            vertices: [[0,1.2,0],[1.1,-0.4,-0.65],[-1.1,-0.4,-0.65],[0,-0.4,1.3]],
            edges: [[0,1],[0,2],[0,3],[1,2],[2,3],[3,1]],
            faces: [[0,1,2],[0,2,3],[0,3,1],[1,2,3]],
            color: '#ef4444', name: 'Tetrahedron'
        },
        ikosahedron: {
            vertices: (function(){
                let v=[], phi=(1+Math.sqrt(5))/2, s=1;
                [[-1,phi,0],[1,phi,0],[-1,-phi,0],[1,-phi,0],
                 [0,-1,phi],[0,1,phi],[0,-1,-phi],[0,1,-phi],
                 [phi,0,-1],[phi,0,1],[-phi,0,-1],[-phi,0,1]].forEach(p=>v.push([p[0]*s,p[1]*s,p[2]*s]));
                return v;
            })(),
            edges: [[0,1],[0,5],[0,7],[0,10],[0,11],[1,5],[1,7],[1,8],[1,9],[2,3],[2,4],[2,6],[2,10],[2,11],
                    [3,4],[3,6],[3,8],[3,9],[4,5],[4,9],[4,11],[5,9],[5,11],[6,7],[6,8],[6,10],[7,8],[7,10],
                    [8,9],[10,11]],
            faces: [], color: '#10b981', name: 'İkosahedron'
        },
        dodekahedron: {
            vertices: (function(){
                let v=[], phi=(1+Math.sqrt(5))/2, ip=1/phi;
                [[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1],
                 [0,phi,ip],[0,phi,-ip],[0,-phi,ip],[0,-phi,-ip],
                 [ip,0,phi],[-ip,0,phi],[ip,0,-phi],[-ip,0,-phi],
                 [phi,ip,0],[phi,-ip,0],[-phi,ip,0],[-phi,-ip,0]].forEach(p=>v.push(p));
                return v;
            })(),
            edges: [[0,8],[0,12],[0,16],[1,9],[1,14],[1,16],[2,10],[2,12],[2,17],[3,11],[3,14],[3,17],
                    [4,8],[4,13],[4,18],[5,9],[5,15],[5,18],[6,10],[6,13],[6,19],[7,11],[7,15],[7,19],
                    [8,9],[10,11],[12,13],[14,15],[16,17],[18,19]],
            faces: [], color: '#8b5cf6', name: 'Dodekahedron'
        },
        ucgen_piramit: {
            vertices: [[0,-1,-0.8],[1,-1,0.6],[-1,-1,0.6],[0,1.2,0]],
            edges: [[0,1],[1,2],[2,0],[0,3],[1,3],[2,3]],
            faces: [[0,1,2],[0,1,3],[1,2,3],[0,2,3]],
            color: '#10b981', name: 'Üçgen Piramit'
        },
        besgen: {
            vertices: (function(){
                let v=[];
                for(let i=0;i<5;i++){let a=Math.PI*2/5*i; v.push([Math.cos(a),-1,Math.sin(a)]);}
                for(let i=0;i<5;i++){let a=Math.PI*2/5*i; v.push([Math.cos(a),1,Math.sin(a)]);}
                return v;
            })(),
            edges: (function(){
                let e=[];
                for(let i=0;i<5;i++){e.push([i,(i+1)%5]); e.push([i+5,(i+1)%5+5]); e.push([i,i+5]);}
                return e;
            })(),
            faces: [], color: '#3b82f6', name: 'Beşgen Prizma'
        },
        paralel: {
            vertices: [[-1,-1,-0.8],[1.2,-1,-0.8],[1.2,1,-0.8],[-1,1,-0.8],
                       [-0.6,-1,0.8],[1.6,-1,0.8],[1.6,1,0.8],[-0.6,1,0.8]],
            edges: [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],
            faces: [], color: '#f59e0b', name: 'Paralel Yüzlü'
        },
        kesik_piramit: {
            vertices: [[-1.2,-1,-1.2],[1.2,-1,-1.2],[1.2,-1,1.2],[-1.2,-1,1.2],
                       [-0.6,1,-0.6],[0.6,1,-0.6],[0.6,1,0.6],[-0.6,1,0.6]],
            edges: [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]],
            faces: [], color: '#6366f1', name: 'Kesik Piramit'
        },
        sekizgen: {
            vertices: (function(){
                let v=[];
                for(let i=0;i<8;i++){let a=Math.PI/4*i; v.push([Math.cos(a),-1,Math.sin(a)]);}
                for(let i=0;i<8;i++){let a=Math.PI/4*i; v.push([Math.cos(a),1,Math.sin(a)]);}
                return v;
            })(),
            edges: (function(){
                let e=[];
                for(let i=0;i<8;i++){e.push([i,(i+1)%8]); e.push([i+8,(i+1)%8+8]); e.push([i,i+8]);}
                return e;
            })(),
            faces: [], color: '#ef4444', name: 'Sekizgen Prizma'
        },
        yildiz: {
            vertices: (function(){
                let v=[];
                for(let i=0;i<10;i++){
                    let a=Math.PI*2/10*i, r=i%2==0?1.2:0.5;
                    v.push([r*Math.cos(a),-0.8,r*Math.sin(a)]);
                }
                for(let i=0;i<10;i++){
                    let a=Math.PI*2/10*i, r=i%2==0?1.2:0.5;
                    v.push([r*Math.cos(a),0.8,r*Math.sin(a)]);
                }
                return v;
            })(),
            edges: (function(){
                let e=[];
                for(let i=0;i<10;i++){e.push([i,(i+1)%10]); e.push([i+10,(i+1)%10+10]); e.push([i,i+10]);}
                return e;
            })(),
            faces: [], color: '#eab308', name: 'Yıldız Prizması'
        },
        altigen_piramit: {
            vertices: (function(){
                let v=[];
                for(let i=0;i<6;i++){let a=Math.PI/3*i; v.push([Math.cos(a),-0.8,Math.sin(a)]);}
                v.push([0,1.2,0]);
                return v;
            })(),
            edges: (function(){
                let e=[];
                for(let i=0;i<6;i++){e.push([i,(i+1)%6]); e.push([i,6]);}
                return e;
            })(),
            faces: [], color: '#8b5cf6', name: 'Altıgen Piramit'
        },
        kesik_oktahedron: {
            vertices: [[0,1.4,0.7],[0,1.4,-0.7],[0.7,1.4,0],[-0.7,1.4,0],
                        [0,-1.4,0.7],[0,-1.4,-0.7],[0.7,-1.4,0],[-0.7,-1.4,0],
                        [1.4,0,0.7],[1.4,0,-0.7],[-1.4,0,0.7],[-1.4,0,-0.7],
                        [0.7,0,1.4],[-0.7,0,1.4],[0.7,0,-1.4],[-0.7,0,-1.4],
                        [0,0.7,1.4],[0,-0.7,1.4],[0,0.7,-1.4],[0,-0.7,-1.4],
                        [1.4,0.7,0],[1.4,-0.7,0],[-1.4,0.7,0],[-1.4,-0.7,0]],
            edges: [[0,2],[0,3],[0,16],[1,2],[1,3],[1,18],[2,20],[3,22],[4,6],[4,7],[4,17],
                    [5,6],[5,7],[5,19],[6,21],[7,23],[8,12],[8,20],[8,21],[9,14],[9,20],[9,21],
                    [10,13],[10,22],[10,23],[11,15],[11,22],[11,23],[12,16],[12,17],[13,16],[13,17],
                    [14,18],[14,19],[15,18],[15,19]],
            faces: [], color: '#f97316', name: 'Kesik Oktahedron'
        }
    };
    """

    html_code = f"""
    <canvas id="mat3d" width="600" height="420" style="background:#0B0F19;border-radius:16px;border:1px solid #1e293b;cursor:grab;display:block;margin:0 auto"></canvas>
    <script>
    (function(){{
        {models_js}

        const c=document.getElementById('mat3d'), ctx=c.getContext('2d');
        let rotX=0.5, rotY=0.5, zoom=120, dragging=false, lx=0, ly=0;
        const cKey = '{cisim_key}';

        // Cisim seçimi
        let model = models[cKey] || null;
        const isCurved = ['silindir','koni','kure','kesik koni','yarim kure','elipsoid','torus','kapsul','cift koni','can','helisel','paraboloid','hiperboloid'].some(k => cKey.includes(k));

        function project(x,y,z){{
            let cosX=Math.cos(rotX),sinX=Math.sin(rotX),cosY=Math.cos(rotY),sinY=Math.sin(rotY);
            let y1=y*cosX-z*sinX, z1=y*sinX+z*cosX;
            let x1=x*cosY+z1*sinY; z1=-x*sinY+z1*cosY;
            let scale=zoom/(z1+5);
            return [c.width/2+x1*scale, c.height/2-y1*scale, z1];
        }}

        function drawLine(x1,y1,z1,x2,y2,z2,color,w){{
            let p1=project(x1,y1,z1), p2=project(x2,y2,z2);
            ctx.beginPath(); ctx.moveTo(p1[0],p1[1]); ctx.lineTo(p2[0],p2[1]);
            ctx.strokeStyle=color; ctx.lineWidth=w||2; ctx.stroke();
        }}

        function drawPoint(x,y,z,r,color,label){{
            let p=project(x,y,z);
            ctx.beginPath(); ctx.arc(p[0],p[1],r||4,0,Math.PI*2);
            ctx.fillStyle=color; ctx.fill();
            if(label){{ctx.fillStyle='#e0e7ff';ctx.font='11px Inter,sans-serif';ctx.fillText(label,p[0]+8,p[1]-6);}}
        }}

        function drawSphere(radius,color,segments){{
            segments=segments||20;
            for(let i=0;i<segments;i++){{
                let lat=Math.PI*i/segments-Math.PI/2;
                let lat2=Math.PI*(i+1)/segments-Math.PI/2;
                for(let j=0;j<segments;j++){{
                    let lon=2*Math.PI*j/segments;
                    let lon2=2*Math.PI*(j+1)/segments;
                    let x1=radius*Math.cos(lat)*Math.cos(lon), y1=radius*Math.sin(lat), z1=radius*Math.cos(lat)*Math.sin(lon);
                    let x2=radius*Math.cos(lat)*Math.cos(lon2), y2=radius*Math.sin(lat), z2=radius*Math.cos(lat)*Math.sin(lon2);
                    let x3=radius*Math.cos(lat2)*Math.cos(lon), y3=radius*Math.sin(lat2), z3=radius*Math.cos(lat2)*Math.sin(lon);
                    drawLine(x1,y1,z1,x2,y2,z2,color,0.5);
                    drawLine(x1,y1,z1,x3,y3,z3,color,0.5);
                }}
            }}
        }}

        function drawCylinder(radius,height,color,segments){{
            segments=segments||20;
            let h2=height/2;
            for(let i=0;i<segments;i++){{
                let a1=2*Math.PI*i/segments, a2=2*Math.PI*(i+1)/segments;
                let x1=radius*Math.cos(a1),z1=radius*Math.sin(a1);
                let x2=radius*Math.cos(a2),z2=radius*Math.sin(a2);
                drawLine(x1,-h2,z1,x2,-h2,z2,color,1);
                drawLine(x1,h2,z1,x2,h2,z2,color,1);
                drawLine(x1,-h2,z1,x1,h2,z1,color,0.5);
            }}
        }}

        function drawCone(radius,height,color,segments){{
            segments=segments||20;
            let h2=height/2;
            for(let i=0;i<segments;i++){{
                let a1=2*Math.PI*i/segments, a2=2*Math.PI*(i+1)/segments;
                let x1=radius*Math.cos(a1),z1=radius*Math.sin(a1);
                let x2=radius*Math.cos(a2),z2=radius*Math.sin(a2);
                drawLine(x1,-h2,z1,x2,-h2,z2,color,1);
                drawLine(x1,-h2,z1,0,h2,0,color,0.5);
            }}
        }}

        function draw(){{
            ctx.clearRect(0,0,c.width,c.height);
            ctx.fillStyle='#0B0F19'; ctx.fillRect(0,0,c.width,c.height);

            // Başlık
            ctx.fillStyle='#94a3b8'; ctx.font='14px Inter,sans-serif'; ctx.textAlign='center';
            ctx.fillText('Mouse ile döndür • Scroll ile yakınlaş',c.width/2,c.height-12);

            if(isCurved){{
                if(cKey.includes('kesik koni')){{
                    // Kesik koni: 2 farklı yarıçaplı daire + yanal çizgiler
                    let R=1.3, r=0.7, h2=1.2, seg=24;
                    for(let i=0;i<seg;i++){{
                        let a1=2*Math.PI*i/seg, a2=2*Math.PI*(i+1)/seg;
                        drawLine(R*Math.cos(a1),-h2,R*Math.sin(a1),R*Math.cos(a2),-h2,R*Math.sin(a2),'#f97316',1);
                        drawLine(r*Math.cos(a1),h2,r*Math.sin(a1),r*Math.cos(a2),h2,r*Math.sin(a2),'#f97316',1);
                        drawLine(R*Math.cos(a1),-h2,R*Math.sin(a1),r*Math.cos(a1),h2,r*Math.sin(a1),'#f97316',0.5);
                    }}
                }}
                else if(cKey.includes('yarim kure')){{
                    // Yarım küre
                    let r=1.5, seg=16;
                    for(let i=0;i<=seg/2;i++){{
                        let lat=Math.PI*i/seg;
                        for(let j=0;j<seg;j++){{
                            let lon=2*Math.PI*j/seg, lon2=2*Math.PI*(j+1)/seg;
                            let x1=r*Math.sin(lat)*Math.cos(lon),y1=r*Math.cos(lat),z1=r*Math.sin(lat)*Math.sin(lon);
                            let x2=r*Math.sin(lat)*Math.cos(lon2),y2=r*Math.cos(lat),z2=r*Math.sin(lat)*Math.sin(lon2);
                            drawLine(x1,y1,z1,x2,y2,z2,'#06b6d4',0.5);
                        }}
                    }}
                    // Taban dairesi
                    for(let j=0;j<seg;j++){{
                        let a1=2*Math.PI*j/seg, a2=2*Math.PI*(j+1)/seg;
                        drawLine(r*Math.cos(a1),0,r*Math.sin(a1),r*Math.cos(a2),0,r*Math.sin(a2),'#06b6d4',1);
                    }}
                }}
                else if(cKey.includes('elipsoid')){{
                    // Elipsoid: 3 farklı yarıçap
                    let a=1.8, b=1.2, cc=0.9, seg=16;
                    for(let i=0;i<seg;i++){{
                        let lat=Math.PI*i/seg-Math.PI/2, lat2=Math.PI*(i+1)/seg-Math.PI/2;
                        for(let j=0;j<seg;j++){{
                            let lon=2*Math.PI*j/seg, lon2=2*Math.PI*(j+1)/seg;
                            let x1=a*Math.cos(lat)*Math.cos(lon),y1=b*Math.sin(lat),z1=cc*Math.cos(lat)*Math.sin(lon);
                            let x2=a*Math.cos(lat)*Math.cos(lon2),y2=b*Math.sin(lat),z2=cc*Math.cos(lat)*Math.sin(lon2);
                            drawLine(x1,y1,z1,x2,y2,z2,'#eab308',0.4);
                        }}
                    }}
                }}
                else if(cKey.includes('torus')){{
                    // Torus
                    let R=1.2, r=0.5, seg=24, tubeSeg=12;
                    for(let i=0;i<seg;i++){{
                        let a1=2*Math.PI*i/seg, a2=2*Math.PI*(i+1)/seg;
                        for(let j=0;j<tubeSeg;j++){{
                            let b1=2*Math.PI*j/tubeSeg, b2=2*Math.PI*(j+1)/tubeSeg;
                            let x1=(R+r*Math.cos(b1))*Math.cos(a1),y1=r*Math.sin(b1),z1=(R+r*Math.cos(b1))*Math.sin(a1);
                            let x2=(R+r*Math.cos(b2))*Math.cos(a1),y2=r*Math.sin(b2),z2=(R+r*Math.cos(b2))*Math.sin(a1);
                            let x3=(R+r*Math.cos(b1))*Math.cos(a2),y3=r*Math.sin(b1),z3=(R+r*Math.cos(b1))*Math.sin(a2);
                            drawLine(x1,y1,z1,x2,y2,z2,'#ec4899',0.4);
                            drawLine(x1,y1,z1,x3,y3,z3,'#ec4899',0.4);
                        }}
                    }}
                }}
                else if(cKey.includes('kapsul')){{
                    drawCylinder(0.8,2,'#10b981',20);
                    let seg=16,r=0.8;
                    for(let i=0;i<=seg/2;i++){{let lat=Math.PI*i/seg;
                        for(let j=0;j<seg;j++){{let lon=2*Math.PI*j/seg,lon2=2*Math.PI*(j+1)/seg;
                            drawLine(r*Math.sin(lat)*Math.cos(lon),1+r*Math.cos(lat),r*Math.sin(lat)*Math.sin(lon),
                                     r*Math.sin(lat)*Math.cos(lon2),1+r*Math.cos(lat),r*Math.sin(lat)*Math.sin(lon2),'#10b981',0.4);
                            drawLine(r*Math.sin(lat)*Math.cos(lon),-1-r*Math.cos(lat),r*Math.sin(lat)*Math.sin(lon),
                                     r*Math.sin(lat)*Math.cos(lon2),-1-r*Math.cos(lat),r*Math.sin(lat)*Math.sin(lon2),'#10b981',0.4);
                    }}}}
                }}
                else if(cKey.includes('cift koni')){{
                    drawCone(1.2,1.5,'#06b6d4',24);
                    // Alt koni (ters)
                    let seg=24,r=1.2,h=1.5;
                    for(let i=0;i<seg;i++){{
                        let a1=2*Math.PI*i/seg;
                        let x1=r*Math.cos(a1),z1=r*Math.sin(a1);
                        drawLine(x1,0,z1,0,-h,0,'#06b6d4',0.5);
                    }}
                }}
                else if(cKey.includes('can')){{
                    let seg=20;
                    for(let i=0;i<seg;i++){{
                        let t1=i/seg*Math.PI,t2=(i+1)/seg*Math.PI;
                        let r1=1.5*Math.sin(t1),y1=1.5*Math.cos(t1)-0.5;
                        let r2=1.5*Math.sin(t2),y2=1.5*Math.cos(t2)-0.5;
                        for(let j=0;j<seg;j++){{
                            let a=2*Math.PI*j/seg,a2=2*Math.PI*(j+1)/seg;
                            drawLine(r1*Math.cos(a),y1,r1*Math.sin(a),r2*Math.cos(a),y2,r2*Math.sin(a),'#eab308',0.3);
                            drawLine(r1*Math.cos(a),y1,r1*Math.sin(a),r1*Math.cos(a2),y1,r1*Math.sin(a2),'#eab308',0.3);
                    }}}}
                }}
                else if(cKey.includes('helisel')){{
                    drawCylinder(1,2.4,'#ec489966',16);
                    let turns=3,pts=100,r=1;
                    for(let i=0;i<pts;i++){{
                        let t1=i/pts*turns*2*Math.PI,t2=(i+1)/pts*turns*2*Math.PI;
                        let y1=-1.2+i/pts*2.4,y2=-1.2+(i+1)/pts*2.4;
                        drawLine(r*Math.cos(t1),y1,r*Math.sin(t1),r*Math.cos(t2),y2,r*Math.sin(t2),'#ec4899',2);
                    }}
                }}
                else if(cKey.includes('paraboloid')){{
                    let seg=20;
                    for(let i=0;i<seg;i++){{
                        let t=i/seg, r1=1.5*Math.sqrt(t), y1=-1.2+t*2.4;
                        let t2=(i+1)/seg, r2=1.5*Math.sqrt(t2), y2=-1.2+t2*2.4;
                        for(let j=0;j<seg;j++){{
                            let a=2*Math.PI*j/seg,a2=2*Math.PI*(j+1)/seg;
                            drawLine(r1*Math.cos(a),y1,r1*Math.sin(a),r2*Math.cos(a),y2,r2*Math.sin(a),'#3b82f6',0.4);
                            drawLine(r1*Math.cos(a),y1,r1*Math.sin(a),r1*Math.cos(a2),y1,r1*Math.sin(a2),'#3b82f6',0.3);
                    }}}}
                }}
                else if(cKey.includes('hiperboloid')){{
                    let seg=20;
                    for(let i=0;i<seg;i++){{
                        let t=-1+2*i/seg, r1=0.6*Math.sqrt(1+t*t*3);
                        let t2=-1+2*(i+1)/seg, r2=0.6*Math.sqrt(1+t2*t2*3);
                        let y1=t*1.5, y2=t2*1.5;
                        for(let j=0;j<seg;j++){{
                            let a=2*Math.PI*j/seg,a2=2*Math.PI*(j+1)/seg;
                            drawLine(r1*Math.cos(a),y1,r1*Math.sin(a),r2*Math.cos(a),y2,r2*Math.sin(a),'#f59e0b',0.4);
                            drawLine(r1*Math.cos(a),y1,r1*Math.sin(a),r1*Math.cos(a2),y1,r1*Math.sin(a2),'#f59e0b',0.3);
                    }}}}
                }}
                else if(cKey.includes('silindir')){{ drawCylinder(1.2,2.4,'#06b6d4',24); }}
                else if(cKey.includes('koni')){{ drawCone(1.2,2.4,'#f59e0b',24); }}
                else if(cKey.includes('kure')){{ drawSphere(1.5,'#8b5cf6',16); }}
            }} else if(model){{
                // Kenarları çiz
                for(let e of model.edges){{
                    let v1=model.vertices[e[0]], v2=model.vertices[e[1]];
                    drawLine(v1[0],v1[1],v1[2],v2[0],v2[1],v2[2],model.color,2);
                }}
                // Köşeleri çiz
                for(let i=0;i<model.vertices.length;i++){{
                    let v=model.vertices[i];
                    drawPoint(v[0],v[1],v[2],5,model.color, String.fromCharCode(65+i));
                }}
            }}

            // Cisim adı
            ctx.fillStyle=model?model.color:'#818cf8'; ctx.font='bold 16px Inter,sans-serif';
            ctx.fillText(model?model.name:'{cisim.split(" (")[0]}',c.width/2,24);
        }}

        // Mouse etkileşimi
        c.addEventListener('mousedown',e=>{{dragging=true;lx=e.clientX;ly=e.clientY;c.style.cursor='grabbing';}});
        c.addEventListener('mousemove',e=>{{
            if(!dragging)return;
            rotY+=(e.clientX-lx)*0.01; rotX+=(e.clientY-ly)*0.01;
            lx=e.clientX; ly=e.clientY; draw();
        }});
        c.addEventListener('mouseup',()=>{{dragging=false;c.style.cursor='grab';}});
        c.addEventListener('mouseleave',()=>{{dragging=false;c.style.cursor='grab';}});
        c.addEventListener('wheel',e=>{{zoom=Math.max(40,Math.min(300,zoom-e.deltaY*0.2));draw();e.preventDefault();}},{{passive:false}});

        // Touch desteği (mobil)
        c.addEventListener('touchstart',e=>{{dragging=true;lx=e.touches[0].clientX;ly=e.touches[0].clientY;}});
        c.addEventListener('touchmove',e=>{{
            if(!dragging)return;
            rotY+=(e.touches[0].clientX-lx)*0.01; rotX+=(e.touches[0].clientY-ly)*0.01;
            lx=e.touches[0].clientX; ly=e.touches[0].clientY; draw(); e.preventDefault();
        }},{{passive:false}});
        c.addEventListener('touchend',()=>{{dragging=false;}});

        draw();
    }})();
    </script>
    """

    components.html(html_code, height=450)


# ══════════════════════════════════════════════════════════════════════════════
# 11) SAYILARIN SIRRI
# ══════════════════════════════════════════════════════════════════════════════

def _render_sayilarin_sirri():
    """Sayıların büyüleyici sırları — ultra premium içerik."""
    styled_section("🔐 Sayıların Sırrı", "#a855f7")

    # Büyüleyici giriş
    _render_html("""
    <style>
    .sir-hero {
        background: linear-gradient(135deg, #0c0024 0%, #1a0a3e 30%, #2d1b69 60%, #4c1d95 100%);
        border-radius: 24px; padding: 36px; margin-bottom: 28px;
        border: 2px solid rgba(168,85,247,0.4);
        text-align: center; position: relative; overflow: hidden;
    }
    .sir-hero::before {
        content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 20% 50%, rgba(168,85,247,0.08) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(236,72,153,0.06) 0%, transparent 40%),
                    radial-gradient(circle at 50% 80%, rgba(99,102,241,0.06) 0%, transparent 40%);
    }
    .sir-card {
        background: linear-gradient(145deg, #0f0524, #1a0a3e);
        border-radius: 20px; padding: 24px; margin-bottom: 18px;
        border: 1px solid rgba(168,85,247,0.2);
        position: relative; overflow: hidden;
        transition: all 0.3s ease;
    }
    .sir-card:hover {
        border-color: rgba(168,85,247,0.5);
        box-shadow: 0 8px 32px rgba(168,85,247,0.15);
        transform: translateY(-2px);
    }
    .sir-card .sir-number {
        font-size: 3rem; font-weight: 900;
        background: linear-gradient(135deg, #c084fc, #818cf8, #f0abfc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; line-height: 1;
    }
    .sir-card .sir-title {
        font-weight: 800; color: #e9d5ff !important;
        font-size: 1.1rem; margin: 8px 0 6px;
    }
    .sir-card .sir-body {
        color: #c4b5fd !important; font-size: 0.88rem; line-height: 1.7;
    }
    .sir-badge {
        display: inline-block; padding: 3px 12px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 700; margin-right: 6px;
    }
    .sir-mystery {
        background: linear-gradient(135deg, #1a0a2e, #0f0524);
        border: 2px solid rgba(236,72,153,0.3);
        border-radius: 20px; padding: 24px; margin-bottom: 18px;
        position: relative;
    }
    .sir-mystery::after {
        content: '🔮'; position: absolute; top: 12px; right: 16px;
        font-size: 2rem; opacity: 0.15;
    }
    .sir-calc {
        background: rgba(99,102,241,0.08); border-radius: 14px;
        padding: 16px; margin: 12px 0; text-align: center;
        font-family: 'Cambria Math','Times New Roman',serif;
        font-size: 1.15rem; color: #818cf8 !important;
        border: 1px dashed rgba(99,102,241,0.2);
    }
    .sir-wow {
        background: linear-gradient(135deg, #451a03, #78350f);
        border: 2px solid rgba(245,158,11,0.4);
        border-radius: 16px; padding: 14px 20px; margin: 12px 0;
        text-align: center;
    }
    .sir-wow .wow-text {
        font-weight: 800; font-size: 1rem;
        color: #fde68a !important;
    }
    </style>

    <div class="sir-hero">
        <div style="position:relative;z-index:1">
            <div style="font-size:3.5rem;margin-bottom:12px" class="mat-grow">🔐</div>
            <h2 style="color:#e9d5ff !important;font-size:1.8rem;margin:0 0 10px !important">Sayıların Sırrı</h2>
            <p style="color:#c4b5fd !important;font-size:1rem;margin:0 !important;max-width:600px;display:inline-block">
                Her sayının bir hikayesi, bir sırrı, bir büyüsü var. Binlerce yıldır
                matematikçileri büyüleyen, şaşırtan ve hayrete düşüren sayıların
                gizemli dünyasına hoş geldiniz!
            </p>
        </div>
    </div>
    """)

    sub_tabs = st.tabs([
        "✨ Efsanevi Sayılar",
        "🌀 Büyülü Sabitler",
        "🎩 Sayı Sihirbazlığı",
        "🔍 Gizli Örüntüler",
        "💀 Lanetli & Şanslı",
        "🧬 Doğadaki Sayılar",
        "🤯 İnanılmaz Gerçekler",
        "🌀 Paradokslar",
        "❓ Çözülmemiş Problemler",
        "💡 Günlük Hayatta Sayılar",
    ])

    with sub_tabs[0]:
        _render_efsanevi_sayilar()
    with sub_tabs[1]:
        _render_buyulu_sabitler()
    with sub_tabs[2]:
        _render_sayi_sihirbazligi()
    with sub_tabs[3]:
        _render_gizli_oruntuler()
    with sub_tabs[4]:
        _render_lanetli_sansli()
    with sub_tabs[5]:
        _render_dogadaki_sayilar()
    with sub_tabs[6]:
        _render_inanilmaz_gercekler()
    with sub_tabs[7]:
        _render_paradokslar()
    with sub_tabs[8]:
        _render_cozulmemis()
    with sub_tabs[9]:
        _render_gunluk_hayat_sayilar()


# ── 11a) Efsanevi Sayılar ───────────────────────────────────────────────────

def _render_efsanevi_sayilar():
    """Özel sayılar ve hikayeleri."""
    styled_section("✨ Efsanevi Sayılar", "#c084fc")

    sayilar = [
        {
            "sayi": "0",
            "baslik": "Sıfır — Hiçlik mi, Her Şey mi?",
            "emoji": "🕳️",
            "badge_renk": "#94a3b8", "badge": "Devrimci",
            "icerik": (
                "Sıfır, insanlığın bulması **en uzun süren** sayıdır. Romalılar onsuz yaşadı, "
                "Yunanlılar varlığını reddetti! Hint matematikçi **Brahmagupta** (628) sıfırı ilk "
                "kez bir sayı olarak tanımladı.\n\n"
                "**Neden devrimci?**\n"
                "- Sıfır olmadan onluk sistem çalışmaz: 10, 100, 1000 yazamazdık!\n"
                "- Sıfıra bölmek **yasaktır** — bilgisayarları bile çökertir! (÷0 = 💥)\n"
                "- 0! = 1 (sıfırın faktöriyeli birdir — neden? Boş kümeyi sıralamanın 1 yolu var!)\n"
                "- Sıfır ne pozitif ne negatif — sayı doğrusunun tam ortasında, tarafsız hakem gibi!"
            ),
        },
        {
            "sayi": "1",
            "baslik": "Bir — Evrenin Başlangıcı",
            "emoji": "☝️",
            "badge_renk": "#ef4444", "badge": "Temel Taşı",
            "icerik": (
                "1, çarpmanın **kimlik elemanıdır**: herhangi bir sayıyı 1 ile çarp, "
                "kendisi kalır. Ama 1'in en büyük sırrı: **asal değildir!**\n\n"
                "**Neden 1 asal değil?**\n"
                "Eğer 1 asal olsaydı, aritmetiğin temel teoremi çökerdi! "
                "Her sayı *tek bir şekilde* asal çarpanlarına ayrılır (6 = 2×3). "
                "Ama 1 asal olsaydı: 6 = 1×2×3 = 1×1×2×3 = ... sonsuz farklı yazım olurdu!\n\n"
                "**1'in süper güçleri:**\n"
                "- 1^n = 1 (1'in herhangi bir kuvveti 1'dir)\n"
                "- 1/1 = 1, 11/11 = 1, 111/111 = 1 ... sonsuza kadar!\n"
                "- Herhangi bir sayının 0. kuvveti 1'dir: 999⁰ = 1"
            ),
        },
        {
            "sayi": "7",
            "baslik": "Yedi — Evrenin Sihirli Sayısı",
            "emoji": "🌈",
            "badge_renk": "#6366f1", "badge": "Gizemli",
            "icerik": (
                "7, hemen her kültürde **kutsal ve şanslı** kabul edilen tek sayıdır.\n\n"
                "**Doğada 7:**\n"
                "🌈 7 gökkuşağı rengi • 🎵 7 nota • 📅 7 gün • 🌍 7 kıta • "
                "7 deniz • ✨ 7 dünya harikası\n\n"
                "**Matematiksel sırrı:**\n"
                "- 1/7 = 0.142857142857... — bu 6 rakam sonsuza kadar tekrar eder!\n"
                "- Ve bu 6 rakam (142857) bir **siklik sayıdır** — çarpımları büyüleyici:\n"
                "  - 142857 × 2 = 285714 (aynı rakamlar, farklı sıra!)\n"
                "  - 142857 × 3 = 428571 ✨\n"
                "  - 142857 × 7 = 999999 🤯\n\n"
                "**Psikolojik sır:** İnsanlardan 1-10 arası rastgele sayı söylemeleri istendiğinde "
                "en çok söylenen sayı **7**'dir!"
            ),
        },
        {
            "sayi": "12",
            "baslik": "On İki — Medeniyetin Sayısı",
            "emoji": "🕐",
            "badge_renk": "#f59e0b", "badge": "Medeniyet",
            "icerik": (
                "12, insanlık tarihinde 10'dan bile önemli bir sayıydı. Babiller 12'yi "
                "temel alarak **60'lık sistemi** kurdu — bu yüzden bugün hâlâ 1 saat = "
                "60 dakika, 1 dakika = 60 saniye!\n\n"
                "**12'nin üstünlüğü:** 12, küçük sayılar arasında **en çok böleni olan** sayıdır:\n"
                "- 12 = 1, 2, 3, 4, 6, 12 ile bölünür (6 bölen!)\n"
                "- 10 = 1, 2, 5, 10 ile bölünür (sadece 4 bölen)\n"
                "- Bu yüzden 12'li düzen (düzine) ticarette daha pratiktir: 12 yumurta "
                "2'ye, 3'e, 4'e, 6'ya eşit bölünür!\n\n"
                "**Hayatımızda 12:**\n"
                "🕐 12 saat • 📅 12 ay • 🔢 12 burç • 🎵 12 nota (kromatik) • "
                "👥 12 havari • 🍳 1 düzine = 12"
            ),
        },
        {
            "sayi": "13",
            "baslik": "On Üç — Uğursuz mu, Şanslı mı?",
            "emoji": "🖤",
            "badge_renk": "#1f2937", "badge": "Tartışmalı",
            "icerik": (
                "13 korkusu o kadar yaygın ki adı bile var: **Triskaidekafobi**!\n\n"
                "**Neden korkuyorlar?**\n"
                "- Birçok binada 13. kat yoktur (12'den 14'e atlanır!)\n"
                "- %80 yüksek bina 13. katı atlar\n"
                "- Cuma 13 korkusu: **Paraskevidekatrifobi** (evet, gerçek bir kelime!)\n"
                "- Formula 1'de 13 numaralı araç kullanılmaz\n\n"
                "**Ama matematiksel olarak:**\n"
                "- 13 bir **asal sayıdır** — sadece kendisi ve 1'e bölünür, güçlüdür!\n"
                "- 13 bir **mutlu sayıdır**: 1² + 3² = 10, 1² + 0² = 1 ✓\n"
                "- Fibonacci dizisinde 13 vardır: 1,1,2,3,5,8,**13**,21...\n\n"
                "**Şanslı 13:** Çin'de 13 şanslı kabul edilir. Taylor Swift'in şanslı sayısı 13'tür!"
            ),
        },
        {
            "sayi": "42",
            "baslik": "42 — Hayatın, Evrenin ve Her Şeyin Cevabı",
            "emoji": "🌌",
            "badge_renk": "#3b82f6", "badge": "Efsane",
            "icerik": (
                "Douglas Adams'ın **'Otostopçunun Galaksi Rehberi'** adlı romanında, süper "
                "bilgisayar Deep Thought'a 'hayatın, evrenin ve her şeyin nihai sorusunun "
                "cevabı nedir?' diye sorarlar. 7.5 milyon yıl düşündükten sonra cevap verir:\n\n"
                "**42.**\n\n"
                "**Matematiksel ilginçlikleri:**\n"
                "- 42 = 2 × 3 × 7 (ardışık 3 asal sayının çarpımı)\n"
                "- 42, ilk 6 çift sayının ortalamasıdır: (2+4+6+8+10+12)/6... hayır aslında değil 😄 ama popüler bir efsanedir!\n"
                "- 2019'da matematikçiler, **42'nin 3 küpün toplamı** olarak yazılabileceğini "
                "kanıtladı: 42 = (-80538738812075974)³ + 80435758145817515³ + 12602123297335631³ 🤯\n"
                "- Bu çözümü bulmak 1.3 milyon saat bilgisayar zamanı aldı!\n\n"
                "- Gökkuşağının oluşum açısı: **42°**"
            ),
        },
        {
            "sayi": "1729",
            "baslik": "1729 — Hardy-Ramanujan Taksi Sayısı",
            "emoji": "🚕",
            "badge_renk": "#eab308", "badge": "Efsanevi",
            "icerik": (
                "Matematikçi G.H. Hardy, hastanede yatan Ramanujan'ı ziyaret eder:\n\n"
                "*'Taksimin numarası 1729'du, oldukça sıkıcı bir sayı.'*\n\n"
                "Ramanujan hemen cevaplar: *'Hayır Hardy! Çok ilginç bir sayı! "
                "İki küpün toplamı olarak **iki farklı şekilde** yazılabilen en küçük sayıdır!'*\n\n"
                "**1729 = 1³ + 12³ = 9³ + 10³** 🤯\n\n"
                "1729 = 1 + 1728 = 729 + 1000\n\n"
                "Bu hikaye, Ramanujan'ın **sayılarla kişisel ilişkisinin** en güzel örneğidir. "
                "O, her sayıyı bir arkadaş gibi tanıyordu.\n\n"
                "Bu tür sayılara artık **'taksi sayısı'** denir. Sonraki taksi sayısı "
                "**87539319**'dur (ancak 2 farklı yolla değil, 3 farklı yolla yazılır)."
            ),
        },
        {
            "sayi": "6174",
            "baslik": "6174 — Kaprekar'ın Büyülü Sabiti",
            "emoji": "🎩",
            "badge_renk": "#ec4899", "badge": "Sihirli",
            "icerik": (
                "Hint matematikçi D.R. Kaprekar 1949'da inanılmaz bir keşif yaptı:\n\n"
                "**Herhangi bir 4 basamaklı sayıyı al** (tüm rakamları aynı olmasın):\n"
                "1. Rakamları büyükten küçüğe sırala → büyük sayı\n"
                "2. Rakamları küçükten büyüğe sırala → küçük sayı\n"
                "3. Büyükten küçüğü çıkar\n"
                "4. Tekrarla — **en fazla 7 adımda mutlaka 6174'e ulaşırsın!**\n\n"
                "**Örnek: 3524**\n"
                "- 5432 - 2345 = 3087\n"
                "- 8730 - 0378 = 8352\n"
                "- 8532 - 2358 = **6174** ✨ (3 adımda!)\n\n"
                "Ve 6174'e ulaşınca: 7641 - 1467 = **6174** → Sonsuza kadar 6174!\n\n"
                "Bu neden çalışır? **Tam olarak kimse bilmiyor!** 🔮 "
                "Matematiksel bir kara delik gibi — tüm sayıları kendine çeker."
            ),
        },
        {
            "sayi": "153",
            "baslik": "153 — Narsist Sayı",
            "emoji": "🪞",
            "badge_renk": "#f97316", "badge": "Kendine Hayran",
            "icerik": (
                "153 bir **narsist sayıdır** (Armstrong sayısı): her basamağının küplerinin "
                "toplamı kendisine eşittir!\n\n"
                "**1³ + 5³ + 3³ = 1 + 125 + 27 = 153** ✨\n\n"
                "Diğer 3 basamaklı narsist sayılar:\n"
                "- **370** = 3³+7³+0³ = 27+343+0 = 370\n"
                "- **371** = 3³+7³+1³ = 27+343+1 = 371\n"
                "- **407** = 4³+0³+7³ = 64+0+343 = 407\n\n"
                "**İncil'deki 153:** Yuhanna İncili'nde İsa'nın mucizevi balık avında "
                "tam **153 balık** yakalanır. Aziz Augustinus bu sayının özel olduğunu "
                "1-17 arası sayıların toplamı (153 = 1+2+...+17) olarak açıkladı.\n\n"
                "4 basamaklı narsist sayı: **1634** = 1⁴+6⁴+3⁴+4⁴ = 1+1296+81+256 = 1634"
            ),
        },
        {
            "sayi": "googol",
            "baslik": "Googol & Googolplex — Sayılamayacak Kadar Büyük",
            "emoji": "🔭",
            "badge_renk": "#06b6d4", "badge": "Devasa",
            "icerik": (
                "1938'de matematikçi Edward Kasner, 9 yaşındaki yeğeni Milton'a "
                "'10 üzeri 100'e ne ad koyalım?' diye sordu. Milton cevapladı: **Googol!**\n\n"
                "**Googol = 10¹⁰⁰** = 1'in arkasına 100 tane sıfır\n\n"
                "Bu sayı, gözlemlenebilir evrendeki tüm atom sayısından (≈10⁸⁰) bile büyüktür!\n\n"
                "**Googolplex = 10^(googol) = 10^(10¹⁰⁰)**\n"
                "Bu sayıyı yazmaya çalışsanız, evrendeki tüm atomları mürekkep yapıp "
                "tüm evreni kağıt yapsanız bile **yetmez!**\n\n"
                "**Google'ın hikayesi:** Larry Page ve Sergey Brin, arama motorlarına "
                "'Googol' adını vermek istediler ama yanlışlıkla **Google** yazarak "
                "tescil ettirdiler! Yazım hatası trilyon dolarlık marka oldu! 🤑"
            ),
        },
    ]

    for s in sayilar:
        _render_html(f"""
        <div class="sir-card">
            <div style="display:flex;gap:20px;align-items:flex-start">
                <div style="min-width:80px;text-align:center">
                    <div style="font-size:2.5rem;margin-bottom:4px" class="mat-grow">{s['emoji']}</div>
                    <div class="sir-number">{s['sayi']}</div>
                </div>
                <div style="flex:1">
                    <div><span class="sir-badge" style="background:{s['badge_renk']}30;color:{s['badge_renk']}">{s['badge']}</span></div>
                    <div class="sir-title">{s['baslik']}</div>
                </div>
            </div>
        </div>
        """)
        with st.expander(f"🔍 {s['baslik']}", expanded=False):
            st.markdown(s["icerik"])


# ── 11b) Büyülü Sabitler ────────────────────────────────────────────────────

def _render_buyulu_sabitler():
    """Pi, e, altın oran ve diğer büyülü sabitler."""
    styled_section("🌀 Evrenin Büyülü Sabitleri", "#6366f1")

    sabitler = [
        {
            "sembol": "π",
            "ad": "Pi (π) — Dairenin Sonsuz Sırrı",
            "deger": "3.14159265358979323846...",
            "emoji": "🥧",
            "renk": "#ef4444",
            "aciklama": (
                "Dairenin çevresinin çapına oranı. **Sonsuz ve tekrarsız** — hiçbir örüntü "
                "yok, hiçbir tekrar yok, sonsuza kadar devam eder!\n\n"
                "**Akıl almaz gerçekler:**\n"
                "- Pi'nin ilk **31.4 trilyon** basamağı hesaplandı (2019)\n"
                "- Pi'nin içinde **her sayı dizisi** bulunabilir: doğum tarihiniz, telefon numaranız, "
                "hatta Shakespeare'in tüm eserleri bile ASCII olarak pi'nin basamaklarında saklıdır! (sonsuz olduğu için)\n"
                "- **14 Mart** (3/14) Dünya Pi Günü olarak kutlanır 🥧\n"
                "- Einstein'ın doğum günü de 14 Mart'tır!\n"
                "- Japonya'da Akira Haraguchi pi'nin **100.000** basamağını ezbere söyledi! 🤯\n"
                "- Antik Mısırlılar pi'yi ≈3.16 olarak biliyordu (MÖ 1650)"
            ),
        },
        {
            "sembol": "e",
            "ad": "Euler Sayısı (e) — Doğanın Büyüme Sabiti",
            "deger": "2.71828182845904523536...",
            "emoji": "📈",
            "renk": "#10b981",
            "aciklama": (
                "Doğal logaritmanın tabanı. Büyüme, çürüme ve bileşik faizin gizli formülü.\n\n"
                "**e nasıl bulundu?**\n"
                "Jacob Bernoulli bileşik faiz problemini çözerken keşfetti:\n"
                "1 TL'yi %100 faizle 1 yıl boyunca yatırırsanız:\n"
                "- Yıllık: 1×(1+1)¹ = 2.00 TL\n"
                "- Aylık: 1×(1+1/12)¹² = 2.61 TL\n"
                "- Günlük: 1×(1+1/365)³⁶⁵ = 2.7146 TL\n"
                "- Sonsuz bölme: **e = 2.71828...** TL!\n\n"
                "**Neden bu kadar önemli?**\n"
                "- Nüfus artışı, radyoaktif bozunum, bakteriler hep e ile büyür\n"
                "- e^(iπ) + 1 = 0 → Euler'in özdeşliği (matematiğin en güzel denklemi)\n"
                "- (d/dx)eˣ = eˣ → Türevi kendisine eşit tek fonksiyon!"
            ),
        },
        {
            "sembol": "φ",
            "ad": "Altın Oran (φ) — Güzelliğin Matematik Formülü",
            "deger": "1.61803398874989484820...",
            "emoji": "🌻",
            "renk": "#eab308",
            "aciklama": (
                "**φ (fi)** = (1+√5)/2 ≈ 1.618... — doğanın en güzel oranı.\n\n"
                "**Nerede bulunur?**\n"
                "- 🌻 **Ayçiçeği**: Çekirdekler φ açısıyla (137.5°) dizilir — böylece "
                "en az boşlukla en çok çekirdek sığar!\n"
                "- 🐚 **Deniz kabuğu**: Nautilus spirali altın oranla büyür\n"
                "- 🌀 **Galaksiler**: Sarmal galaksilerin kolları φ ile kıvrılır\n"
                "- 🏛️ **Parthenon**: Genişlik/yükseklik oranı ≈ φ\n"
                "- 🖼️ **Mona Lisa**: Da Vinci altın oranı bilinçli kullandı\n"
                "- 💳 **Kredi kartı**: En/boy oranı ≈ φ\n\n"
                "**Fibonacci ile ilişkisi:**\n"
                "1, 1, 2, 3, 5, 8, 13, 21, 34, 55...\n"
                "Ardışık terimlerin oranı φ'ye yakınsar:\n"
                "8/5=1.6, 13/8=1.625, 21/13=1.615, 34/21=1.619...\n\n"
                "**Kendi kendinin tersi:** φ - 1 = 1/φ (bunu yapabilen başka pozitif sayı yok!)"
            ),
        },
        {
            "sembol": "i",
            "ad": "Sanal Birim (i) — Var Olmayan Sayı",
            "deger": "i² = -1",
            "emoji": "👻",
            "renk": "#8b5cf6",
            "aciklama": (
                "**i = √(-1)** — hiçbir gerçel sayı kendisiyle çarpılınca negatif vermez. "
                "O yüzden matematikçiler **hayali** bir sayı icat ettiler!\n\n"
                "**Neden gerekli?**\n"
                "x² + 1 = 0 denkleminin gerçek çözümü yoktur. Ama i ile: x = ±i\n\n"
                "**'Hayali' denmesine aldanma:**\n"
                "- Elektrik mühendisliği i olmadan çalışmaz (AC devre analizi)\n"
                "- Kuantum mekaniği i olmadan yazılamaz\n"
                "- Uçak kanatlarının aerodinamiği i ile hesaplanır\n"
                "- Sinyal işleme, Fourier dönüşümü tamamen i üzerine kuruludur\n\n"
                "**Akıl almaz:** i^i (hayali sayının hayali kuvveti) = **0.2079...** "
                "Bu **gerçel bir sayıdır!** Hayali sayının hayali kuvveti gerçek! 🤯\n\n"
                "Euler bunu kanıtladı: i^i = e^(-π/2) ≈ 0.20788..."
            ),
        },
        {
            "sembol": "∞",
            "ad": "Sonsuz (∞) — Sayıların Ötesi",
            "deger": "Tanımsız — bir sayı değil, bir kavram",
            "emoji": "♾️",
            "renk": "#ec4899",
            "aciklama": (
                "Sonsuz bir sayı değildir — bir **kavramdır.** Ama sonsuzun da türleri vardır!\n\n"
                "**Georg Cantor'un çılgın keşfi (1874):**\n"
                "Bazı sonsuzlar diğerlerinden **daha büyüktür!**\n"
                "- Doğal sayılar (1,2,3,...) → ℵ₀ (aleph-sıfır) — sayılabilir sonsuz\n"
                "- Gerçel sayılar (tüm ondalıklar) → daha büyük sonsuz!\n\n"
                "**Cantor bunu nasıl kanıtladı?** Köşegenleştirme argümanı ile: "
                "ne yaparsanız yapın, gerçel sayıları doğal sayılarla eşleştiremezsiniz!\n\n"
                "**Sonsuz sürprizler:**\n"
                "- 0 ile 1 arasındaki sayılar, tüm doğal sayılardan fazladır!\n"
                "- 0 ile 1 arasıyla 0 ile 1000000 arasında aynı miktarda sayı var!\n"
                "- ∞ + 1 = ∞, ∞ × 2 = ∞, ama ∞ - ∞ = ? (tanımsız!)\n"
                "- Hilbert Oteli: Sonsuz odalı dolu otele sonsuz yeni misafir alınabilir!\n\n"
                "Cantor bu keşifler yüzünden meslektaşlarınca dışlandı ve akıl hastanesinde "
                "yaşamının son yıllarını geçirdi. Bugün ise bir dahi olarak anılır."
            ),
        },
    ]

    for s in sabitler:
        _render_html(f"""
        <div class="sir-mystery" style="border-color:{s['renk']}40">
            <div style="display:flex;gap:20px;align-items:center">
                <div style="min-width:80px;text-align:center">
                    <div style="font-size:2rem;margin-bottom:4px" class="mat-grow">{s['emoji']}</div>
                    <div style="font-size:2.8rem;font-weight:900;color:{s['renk']} !important;
                                 font-family:'Cambria Math','Times New Roman',serif">{s['sembol']}</div>
                </div>
                <div style="flex:1">
                    <div style="font-weight:800;color:#e9d5ff !important;font-size:1.05rem;margin-bottom:4px">{s['ad']}</div>
                    <div class="sir-calc">{s['deger']}</div>
                </div>
            </div>
        </div>
        """)
        with st.expander(f"🔍 {s['ad']}", expanded=False):
            st.markdown(s["aciklama"])


# ── 11c) Sayı Sihirbazlığı ──────────────────────────────────────────────────

def _render_sayi_sihirbazligi():
    """İnteraktif sayı sihirbazlığı numaraları."""
    styled_section("🎩 Sayı Sihirbazlığı", "#f59e0b")

    _render_html("""
    <div style="background:linear-gradient(135deg,#451a03,#78350f);border-radius:20px;padding:22px;margin-bottom:20px;
                 border:2px solid rgba(245,158,11,0.4);text-align:center">
        <div style="font-size:2.5rem;margin-bottom:8px" class="mat-wiggle">🎩✨</div>
        <div style="font-weight:700;color:#fde68a !important;font-size:1.1rem">Arkadaşlarını bu numaralarla şaşırt!</div>
        <div style="color:#fcd34d !important;font-size:0.9rem">Her numaranın arkasında matematik var!</div>
    </div>
    """)

    numaralar = [
        {
            "ad": "🔮 Düşündüğün Sayıyı Biliyorum!",
            "adimlar": [
                "1️⃣ Bir sayı düşün (1-10 arası)",
                "2️⃣ 2 ile çarp",
                "3️⃣ 8 ekle",
                "4️⃣ 2'ye böl",
                "5️⃣ İlk düşündüğün sayıyı çıkar",
            ],
            "sonuc": "Sonuç her zaman **4** olur! 🎩✨",
            "aciklama": "Cebir: (2x+8)/2 - x = x+4-x = 4. Başlangıç sayısı ne olursa olsun kaybolur!",
        },
        {
            "ad": "🧙 1089 Sihri",
            "adimlar": [
                "1️⃣ 3 basamaklı bir sayı yaz (ilk ve son rakam farklı olsun, ör: 742)",
                "2️⃣ Rakamlarını ters çevir (247)",
                "3️⃣ Büyükten küçüğü çıkar (742-247 = 495)",
                "4️⃣ Sonucu da ters çevir (594)",
                "5️⃣ 3. ve 4. adımdaki sayıları topla",
            ],
            "sonuc": "Sonuç her zaman **1089** olur! 🤯",
            "aciklama": "Bu 100a+10b+c şeklindeki sayılar için çalışır. Çıkarma sonucu her zaman 99|a-c| olur, tersi ile toplamı 1089!",
        },
        {
            "ad": "⚡ 9'un Parmak Sihri",
            "adimlar": [
                "1️⃣ İki elini aç, parmakları 1'den 10'a kadar say",
                "2️⃣ 9 × N için N. parmağı kapat",
                "3️⃣ Kapanan parmağın solundakiler = onlar basamağı",
                "4️⃣ Sağındakiler = birler basamağı",
            ],
            "sonuc": "Örnek: 9×4 → 4. parmağı kapat → sol:3 sağ:6 → **36** ✨",
            "aciklama": "9 = 10-1 olduğu için her çarpımda toplamı 9 olan iki basamak oluşur: 09,18,27,36,45,54,63,72,81",
        },
        {
            "ad": "🌟 6 ile Çarpma Sihri",
            "adimlar": [
                "1️⃣ Tek bir çift sayı seç (2,4,6,8)",
                "2️⃣ 6 ile çarp",
            ],
            "sonuc": "Sonucun **birler basamağı** her zaman seçtiğin sayı, **onlar basamağı** yarısı olur!",
            "aciklama": "6×2=12 (birler:2, onlar:1=2/2) • 6×4=24 (birler:4, onlar:2=4/2) • 6×6=36 • 6×8=48 ✨",
        },
        {
            "ad": "🎯 11 ile Çarpma Kolaylığı",
            "adimlar": [
                "1️⃣ 2 basamaklı herhangi bir sayı al (ör: 36)",
                "2️⃣ İki rakamı ayır: 3_6",
                "3️⃣ Araya toplamlarını yaz: 3(3+6)6 = 396",
            ],
            "sonuc": "**36 × 11 = 396!** Hızlı hesap! ⚡",
            "aciklama": "Toplam 10'u geçerse elde var: 85×11 → 8(13)5 → 935. Çünkü 11×(10a+b)=100a+10(a+b)+b",
        },
    ]

    for i, n in enumerate(numaralar):
        with st.expander(n["ad"], expanded=(i == 0)):
            for adim in n["adimlar"]:
                st.markdown(f"**{adim}**")

            _render_html(f"""
            <div class="sir-wow">
                <div class="wow-text">✨ {n['sonuc']}</div>
            </div>
            """)

            st.caption(f"💡 **Nasıl çalışır?** {n['aciklama']}")

    # İnteraktif sihirbaz
    st.markdown("---")
    styled_section("🎩 Kendin Dene — Sayı Bilici", "#ec4899")

    st.markdown("**Bir sayı düşün, adımları uygula, ben sonucu bileyim!**")
    col1, col2 = st.columns(2)
    with col1:
        x = st.number_input("Düşündüğün sayı (gizli tutacağım!):", 1, 100, 7, key="mat_sir_x")
    with col2:
        numara = st.selectbox("Numara:", ["Düşündüğünü Bilme (=4)", "1089 Sihri"], key="mat_sir_sel")

    if st.button("🎩 Sihri Göster!", key="mat_sir_go", type="primary"):
        if "Bilme" in numara:
            step1 = x * 2
            step2 = step1 + 8
            step3 = step2 // 2
            step4 = step3 - x
            st.markdown(f"- Sayın: **{x}**")
            st.markdown(f"- ×2 = {step1}")
            st.markdown(f"- +8 = {step2}")
            st.markdown(f"- ÷2 = {step3}")
            st.markdown(f"- -{x} = **{step4}**")
            _render_html(f'<div class="sir-wow"><div class="wow-text">🎩 Sonuç: {step4}! Her zaman 4!</div></div>')
        else:
            if 100 <= x <= 999:
                rev = int(str(x)[::-1])
                diff = abs(x - rev)
                diff_rev = int(str(diff).zfill(3)[::-1])
                total = diff + diff_rev
                st.markdown(f"- Sayın: **{x}**, Tersi: **{rev}**")
                st.markdown(f"- Fark: |{x}-{rev}| = **{diff}**")
                st.markdown(f"- Farkın tersi: **{diff_rev}**")
                st.markdown(f"- Toplam: {diff}+{diff_rev} = **{total}**")
                _render_html(f'<div class="sir-wow"><div class="wow-text">🎩 Sonuç: {total}!</div></div>')
            else:
                st.warning("1089 sihri için 3 basamaklı bir sayı girin (100-999).")


# ── 11d) Gizli Örüntüler ────────────────────────────────────────────────────

def _render_gizli_oruntuler():
    """Sayılardaki gizli örüntüler ve şaşırtıcı eşitlikler."""
    styled_section("🔍 Gizli Örüntüler & Büyüleyici Eşitlikler", "#10b981")

    oruntuler = [
        {
            "baslik": "🔢 1'lerden Piramit",
            "gosterim": (
                "1 × 1 = 1\n"
                "11 × 11 = 121\n"
                "111 × 111 = 12321\n"
                "1111 × 1111 = 1234321\n"
                "11111 × 11111 = 123454321\n"
                "111111 × 111111 = 12345654321\n"
                "1111111 × 1111111 = 1234567654321\n"
                "11111111 × 11111111 = 123456787654321\n"
                "111111111 × 111111111 = **12345678987654321** 🤯"
            ),
            "aciklama": "Mükemmel bir sayı piramidi! Yukarı çık, aşağı in — palindrom oluşur!",
        },
        {
            "baslik": "🔥 8'lerin Büyüsü",
            "gosterim": (
                "1 × 8 + 1 = 9\n"
                "12 × 8 + 2 = 98\n"
                "123 × 8 + 3 = 987\n"
                "1234 × 8 + 4 = 9876\n"
                "12345 × 8 + 5 = 98765\n"
                "123456 × 8 + 6 = 987654\n"
                "1234567 × 8 + 7 = 9876543\n"
                "12345678 × 8 + 8 = 98765432\n"
                "123456789 × 8 + 9 = **987654321** ✨"
            ),
            "aciklama": "Artan sayılar × 8 + son rakam = Azalan sayılar! Evrenin simetrisi!",
        },
        {
            "baslik": "✨ 9'un Sihirli Tablosu",
            "gosterim": (
                "9 × 1 = 09 → 0+9 = 9\n"
                "9 × 2 = 18 → 1+8 = 9\n"
                "9 × 3 = 27 → 2+7 = 9\n"
                "9 × 4 = 36 → 3+6 = 9\n"
                "9 × 5 = 45 → 4+5 = 9\n"
                "9 × 6 = 54 → 5+4 = 9\n"
                "9 × 7 = 63 → 6+3 = 9\n"
                "9 × 8 = 72 → 7+2 = 9\n"
                "9 × 9 = 81 → 8+1 = 9\n"
                "9 × 10 = 90 → 9+0 = **9** 🔄"
            ),
            "aciklama": "9'un katlarının rakamları toplamı HER ZAMAN 9 eder! 9, 10'luk sistemin 'sınır muhafızıdır'.",
        },
        {
            "baslik": "🌟 142857 — Dairesel Sayı",
            "gosterim": (
                "142857 × 1 = 142857\n"
                "142857 × 2 = 285714 (aynı rakamlar döndü!)\n"
                "142857 × 3 = 428571\n"
                "142857 × 4 = 571428\n"
                "142857 × 5 = 714285\n"
                "142857 × 6 = 857142\n"
                "142857 × 7 = **999999** 🤯\n\n"
                "Ve: 142 + 857 = **999**\n"
                "14 + 28 + 57 = **99**"
            ),
            "aciklama": "1/7 = 0.142857142857... Bu 6 rakam sonsuza kadar döner. Çarpımları aynı rakamların döngüsüdür!",
        },
        {
            "baslik": "💎 Karesallerin Sırrı",
            "gosterim": (
                "1 = 1\n"
                "1+3 = 4 = 2²\n"
                "1+3+5 = 9 = 3²\n"
                "1+3+5+7 = 16 = 4²\n"
                "1+3+5+7+9 = 25 = 5²\n"
                "1+3+5+7+9+11 = 36 = 6²\n"
                "...\n"
                "İlk n tek sayının toplamı = **n²** 🎯"
            ),
            "aciklama": "Ardışık tek sayıları topla → mükemmel kare! Pisagor bunu taşlarla gösterirdi: her yeni tek sayı L şeklinde eklenir.",
        },
        {
            "baslik": "🎭 Palindromik Asal Sürprizi",
            "gosterim": (
                "11, 101, 131, 151, 181, 191, 313, 353, 373, 383...\n\n"
                "Tersten de aynı okunan asal sayılar!\n\n"
                "En büyük bilinen: 10^(1888529) - 10^(944264) - 1\n"
                "(1.888.529 basamaklı!)"
            ),
            "aciklama": "Palindromik asallar hem ileriye hem geriye asal kalır. İki yönlü koruma!",
        },
        {
            "baslik": "🌀 Fibonacci Her Yerde",
            "gosterim": (
                "1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...\n\n"
                "Karelerin toplamı:\n"
                "1² + 1² = 1×2\n"
                "1² + 1² + 2² = 2×3\n"
                "1² + 1² + 2² + 3² = 3×5\n"
                "1² + 1² + 2² + 3² + 5² = 5×8\n"
                "→ İlk n Fibonacci'nin kareleri toplamı = Fₙ × Fₙ₊₁ ✨"
            ),
            "aciklama": "Fibonacci kareleri dikdörtgen oluşturur. Bu yüzden doğadaki spiraller Fibonacci ile büyür!",
        },
    ]

    for o in oruntuler:
        with st.expander(o["baslik"], expanded=False):
            st.code(o["gosterim"], language=None)
            st.info(f"💡 **Sırrı:** {o['aciklama']}")


# ── 11e) Lanetli & Şanslı Sayılar ───────────────────────────────────────────

def _render_lanetli_sansli():
    """Kültürlerde lanetli ve şanslı sayılar."""
    styled_section("💀 Lanetli & Şanslı Sayılar", "#ef4444")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1a0a0a,#3d1c1c);border-radius:20px;padding:22px;margin-bottom:20px;
                 border:2px solid rgba(239,68,68,0.3);text-align:center">
        <div style="font-size:1.8rem;margin-bottom:8px">💀 ☘️</div>
        <div style="font-weight:700;color:#fca5a5 !important;font-size:1.1rem">Sayılar kültürleri nasıl şekillendirdi?</div>
        <div style="color:#f87171 !important;font-size:0.9rem">Bazıları uğurlu, bazıları lanetli — ama hepsi birer sayı!</div>
    </div>
    """)

    col1, col2 = st.columns(2)

    with col1:
        styled_section("💀 Korkulan Sayılar", "#ef4444")

        lanetli = [
            ("4️⃣", "4 — Doğu Asya", "🇯🇵🇨🇳🇰🇷",
             "Japonca, Çince ve Korece'de '4' (shi/si) 'ölüm' ile aynı sesli! Hastanelerde 4. kat olmaz, "
             "uçaklarda 4. sıra atlanır. Bu korkunun adı: **Tetrafobi.**"),
            ("1️⃣3️⃣", "13 — Batı Dünyası", "🇺🇸🇬🇧🇪🇺",
             "Son Akşam Yemeği'nde masada 13 kişi vardı. Viking mitolojisinde 13. tanrı kaosu başlattı. "
             "Otellerin %80'inde 13. kat yok!"),
            ("6️⃣6️⃣6️⃣", "666 — Batı", "😈",
             "Vahiy Kitabı'nda 'canavarın sayısı' olarak geçer. Ama tarihçiler bunun aslında Neron "
             "Sezar'ın İbranice isim karşılığı olduğunu düşünür!"),
            ("1️⃣7️⃣", "17 — İtalya", "🇮🇹",
             "Roma rakamıyla XVII, harfleri karıştırılınca VIXI = 'yaşadım' (yani öldüm!) olur. "
             "İtalyan uçaklarında 17. sıra yoktur!"),
            ("🔢", "39 — Afganistan", "🇦🇫",
             "Afganistan'da 39 sayısı büyük utanç kabul edilir. 39 plakalı araba almak neredeyse "
             "imkansızdır!"),
        ]

        for emoji, ad, bayrak, aciklama in lanetli:
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#1f0a0a,#2d1515);border-radius:14px;padding:14px 16px;
                         margin-bottom:10px;border:1px solid rgba(239,68,68,0.2)">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
                    <span style="font-size:1.5rem">{emoji}</span>
                    <span style="font-weight:700;color:#fca5a5 !important;font-size:0.9rem">{ad}</span>
                    <span style="font-size:0.9rem">{bayrak}</span>
                </div>
                <div style="font-size:0.8rem;color:#94a3b8 !important;line-height:1.5">{aciklama}</div>
            </div>
            """)

    with col2:
        styled_section("☘️ Şanslı Sayılar", "#10b981")

        sansli = [
            ("7️⃣", "7 — Dünya Geneli", "🌍",
             "Neredeyse her kültürde şanslı! 7 renk, 7 nota, 7 gün, 7 kıta. "
             "Kumarhanelerde en çok aranan sayı. İnsanların 'rastgele' seçtiği #1 sayı!"),
            ("8️⃣", "8 — Çin", "🇨🇳",
             "Çince'de '8' (ba) 'zenginlik' anlamına gelir. Pekin Olimpiyatları **08/08/08** "
             "tarihinde saat **08:08:08**'de başladı! Bir telefon numarası 8888-8888 "
             "için 270.000$ ödendi!"),
            ("3️⃣", "3 — Evrensel", "✨",
             "3 dilek, 3 deneme, üçüncüsü şans getirir! Hristiyanlıkta Teslis, "
             "masallarda 3 kardeş, 3'lü ritim insanlara doğal gelir."),
            ("9️⃣", "9 — Çin & Japonya", "🇨🇳🇯🇵",
             "Çince'de 'uzun ömür' ile aynı sesli. İmparatorluk sarayında her şey "
             "9 veya 9'un katıydı: Yasak Şehir'de 9.999 oda var!"),
            ("🔢", "108 — Hindistan & Budizm", "🇮🇳",
             "Hinduizm'de 108 kutsal sayıdır. Tespih 108 taneli, yoga 108 selamlama. "
             "Güneş-Dünya mesafesi ≈ 108 × Güneş çapı! Tesadüf mü? 🤔"),
        ]

        for emoji, ad, bayrak, aciklama in sansli:
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#0a1f0a,#152d15);border-radius:14px;padding:14px 16px;
                         margin-bottom:10px;border:1px solid rgba(16,185,129,0.2)">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
                    <span style="font-size:1.5rem">{emoji}</span>
                    <span style="font-weight:700;color:#86efac !important;font-size:0.9rem">{ad}</span>
                    <span style="font-size:0.9rem">{bayrak}</span>
                </div>
                <div style="font-size:0.8rem;color:#94a3b8 !important;line-height:1.5">{aciklama}</div>
            </div>
            """)


# ── 11f) Doğadaki Sayılar ───────────────────────────────────────────────────

def _render_dogadaki_sayilar():
    """Doğanın matematiksel mucizeleri."""
    styled_section("🧬 Doğadaki Matematiksel Mucizeler", "#06b6d4")

    _render_html("""
    <div style="background:linear-gradient(135deg,#0a1628,#1e3a5f);border-radius:20px;padding:22px;margin-bottom:20px;
                 border:2px solid rgba(6,182,212,0.3);text-align:center">
        <div style="font-size:2rem;margin-bottom:8px" class="mat-grow">🌍</div>
        <div style="font-weight:700;color:#cffafe !important;font-size:1.1rem">Doğa Bir Matematikçidir!</div>
        <div style="color:#67e8f9 !important;font-size:0.9rem">Evrenin her köşesinde sayılar gizli — sadece bakmayı bilmek gerek.</div>
    </div>
    """)

    dogadaki = [
        {
            "baslik": "🌻 Fibonacci Spiralleri",
            "emoji": "🌻",
            "icerik": (
                "**Ayçiçeği çekirdekleri** Fibonacci sayılarıyla dizilir:\n"
                "- Saat yönünde 34 spiral, ters yönde 55 spiral (veya 21-34, 55-89)\n"
                "- Bu, çekirdeklerin **en verimli şekilde** paketlenmesini sağlar!\n\n"
                "**Nerede daha var?**\n"
                "- 🍍 Ananas kabuğu: 8, 13, 21 spiral\n"
                "- 🌹 Gül taç yaprakları: Fibonacci sayılarında\n"
                "- 🐚 Nautilus kabuğu: Fibonacci spirali\n"
                "- 🌲 Çam kozalağı: 8 ve 13 spiral"
            ),
        },
        {
            "baslik": "❄️ Kar Taneleri — 6'nın Krallığı",
            "emoji": "❄️",
            "icerik": (
                "Her kar tanesi **6 kolludur** — istisnasız! Neden?\n\n"
                "Su molekülü (H₂O) 120° açıyla bağlanır. Donunca altıgen "
                "kristal yapı oluşur. Trilyon su molekülü bu 6'lı simetriye uyar!\n\n"
                "**Her kar tanesi benzersizdir** — ama hepsi 6 kollu! Bu, "
                "matematiğin doğayı nasıl yönettiğinin en güzel örneğidir.\n\n"
                "**Arı petekleri** de altıgen: 6 kenarlı yapı, en az malzemeyle "
                "en çok alanı kaplar! 🐝"
            ),
        },
        {
            "baslik": "🦎 Hayvanlar ve Matematik",
            "emoji": "🦎",
            "icerik": (
                "- 🐝 **Arılar** en kısa yolu (Gezgin Satıcı Problemi) bilgisayardan önce çözer!\n"
                "- 🐜 **Karıncalar** koloni optimizasyonu yapar — internet yönlendirme algoritmaları karıncalardan esinlenmiştir!\n"
                "- 🦎 **Bukalemun** deri hücreleri fraktal geometriyle renk değiştirir\n"
                "- 🕷️ **Örümcek ağı** logaritmik spiral ve mükemmel geometri\n"
                "- 🐬 **Yunuslar** sonar için Fourier dönüşümü kullanır\n"
                "- 🐦 **Sığırcıklar** murmuration uçuşunda 3 basit kuralla binlercesi koordine olur"
            ),
        },
        {
            "baslik": "🌌 Evrenin Matematik Dili",
            "emoji": "🌌",
            "icerik": (
                "Galileo: *'Evren matematik dilinde yazılmıştır.'*\n\n"
                "- 🪐 **Gezegen yörüngeleri** Kepler'in 3 yasasına uyar\n"
                "- 🌊 **Dalga hareketleri** sinüs ve kosinüs fonksiyonları\n"
                "- ⚛️ **Atom yapısı** kuantum sayılarıyla belirlenir\n"
                "- 🧬 **DNA** çift sarmal — geometrik yapı\n"
                "- 🔭 **Galaksiler** logaritmik spiraller şeklinde\n"
                "- 🌡️ **Radyoaktif bozunum** e sayısıyla üstel azalma\n\n"
                "Fizikçi Eugene Wigner bunu 'matematiğin akıl almaz etkinliği' olarak adlandırdı — "
                "neden soyut matematik bu kadar iyi gerçek dünyayı açıklıyor?"
            ),
        },
        {
            "baslik": "🌿 Fraktallar — Sonsuz Tekrar",
            "emoji": "🥦",
            "icerik": (
                "**Fraktal:** Parçası bütünün küçük kopyası olan yapı.\n\n"
                "- 🥦 **Romanesco brokoli**: Mükemmel fraktal — her çıkıntı, bütünün küçük kopyası!\n"
                "- 🌿 **Eğreltiotu**: Her yaprak, tüm bitkinin minyatürü\n"
                "- ⚡ **Yıldırım**: Dallanma fraktal geometriyle oluşur\n"
                "- 🏔️ **Dağ siluetleri**: Fraktal boyut ≈ 2.3\n"
                "- 🫁 **Akciğer**: 70m² yüzey alanı fraktal dallanma sayesinde\n"
                "- 🩸 **Kan damarları**: Fraktal ağ — en ince kılcal damara kadar\n\n"
                "**Mandelbrot kümesi:** z → z²+c formülünün sonsuz tekrarından "
                "oluşan dünyanın en karmaşık şekli — sonsuz yakınlaştır, hep yeni detay!"
            ),
        },
    ]

    for d in dogadaki:
        with st.expander(f"{d['baslik']}", expanded=False):
            _render_html(f"""
            <div style="text-align:center;font-size:3rem;margin-bottom:12px" class="mat-grow">{d['emoji']}</div>
            """)
            st.markdown(d["icerik"])


# ── 11g) İnanılmaz Gerçekler ────────────────────────────────────────────────

def _render_inanilmaz_gercekler():
    """Akıl almaz matematik gerçekleri."""
    styled_section("🤯 İnanılmaz Matematik Gerçekleri", "#ec4899")

    gercekler = [
        ("🃏", "52 kart destesinin olası sıralaması",
         "52! = 8 × 10⁶⁷ — Bu sayı evrendeki atom sayısından büyük! "
         "Her kart karıştırdığınızda, o sıralama tarihte ilk kez ve muhtemelen son kez oluşuyordur!"),
        ("📄", "Kağıt katlama paradoksu",
         "Bir kağıdı 42 kez katlayabilseydiniz, kalınlığı Ay'a ulaşırdı! (0.1mm × 2⁴² ≈ 440.000 km) "
         "103 kez katlasanız gözlemlenebilir evrenin çapını aşardınız!"),
        ("🎂", "Doğum Günü Paradoksu",
         "23 kişilik bir grupta aynı doğum gününü paylaşan iki kişi olma olasılığı %50'den fazla! "
         "70 kişide bu olasılık %99.9'u geçer! Sezgisel olarak imkansız gibi görünür ama matematik yalan söylemez."),
        ("🐒", "Sonsuz Maymun Teoremi",
         "Sonsuz sayıda maymun, sonsuz süre boyunca rastgele daktilo tuşlarına basarsa, "
         "Shakespeare'in tüm eserlerini yazma olasılığı 1'dir. Sonsuzun gücü!"),
        ("🏀", "Basketbol ve Olasılık",
         "NBA'de 3 sayılık atış oranı ~%35. Ama 'hot hand' yanlışlığı: Üst üste 3 basket atan "
         "oyuncunun 4. atışı daha isabetli olacağı **yanılsamadır** — her atış bağımsızdır!"),
        ("🗺️", "4 Renk Teoremi",
         "Herhangi bir harita yalnızca 4 renkle boyanabilir öyle ki komşu bölgeler farklı renkte olsun. "
         "1852'de soruldu, 1976'da bilgisayar yardımıyla kanıtlandı — tarihte bilgisayar kullanan ilk kanıt!"),
        ("🌐", "Dünya'nın çevresi ve ip",
         "Dünya'nın çevresine sarılı bir ipe 1 metre eklesen, ip yüzeyden ne kadar yükselir? "
         "Sezgi: milimetrik. Gerçek: **16 cm!** (C=2πr, +1m → Δr = 1/(2π) ≈ 0.159m) "
         "Ve bu kürenin büyüklüğünden bağımsız — portakal da olsa Jüpiter de olsa 16 cm!"),
        ("♾️", "0.999... = 1",
         "0.9999... (sonsuz 9) tam olarak 1'e eşittir! İspat: x=0.999..., 10x=9.999..., "
         "10x-x=9, 9x=9, x=1. Veya: 1/3=0.333..., 3×(1/3)=1, 3×0.333...=0.999...=1 ✓"),
        ("📐", "Banach-Tarski Paradoksu",
         "Matematiksel olarak bir küreyi parçalara ayırıp yeniden birleştirerek "
         "**aynı boyutta 2 küre** elde edebilirsiniz! Sonsuzun katkılarıyla 1+1=1 olabilir! "
         "(Fiziksel olarak imkansız ama matematiksel olarak kanıtlanmış!)"),
        ("🔢", "Benford Yasası",
         "Doğadaki sayıların %30'u **1** ile başlar! Nüfus, nehir uzunlukları, borsa fiyatları, "
         "elektrik faturaları... İlk basamak dağılımı eşit değildir. Bu yasa vergi kaçakçılığını "
         "tespit etmek için kullanılır!"),
        ("🧊", "Bir Rubik Küpü",
         "3×3 Rubik küpünün 43.252.003.274.489.856.000 farklı konumu vardır (43 kentilyon!). "
         "Ama her konumdan en fazla **20 hamleyle** çözülebileceği 2010'da kanıtlandı. Buna 'Tanrı'nın Sayısı' denir."),
        ("🎰", "Büyük Sayılar Yasası",
         "Bir madeni parayı 10 kez atarsan 7 yazı gelebilir. Ama 10 milyon kez atarsan "
         "yazı oranı %50.00...'a yakınsayacaktır. Kısa vadede şans, uzun vadede matematik kazanır."),
    ]

    for i, (emoji, baslik, aciklama) in enumerate(gercekler):
        _render_html(f"""
        <div class="sir-card" style="{'border-color:rgba(236,72,153,0.35)' if i%2==0 else ''}">
            <div style="display:flex;gap:16px;align-items:flex-start">
                <div style="font-size:2rem;min-width:40px;text-align:center" class="{'mat-bounce' if i%3==0 else 'mat-grow' if i%3==1 else 'mat-wiggle'}">{emoji}</div>
                <div>
                    <div style="font-weight:700;color:#e9d5ff !important;font-size:0.95rem;margin-bottom:6px">{baslik}</div>
                    <div style="color:#c4b5fd !important;font-size:0.85rem;line-height:1.7">{aciklama}</div>
                </div>
            </div>
        </div>
        """)


def _render_paradokslar():
    """Matematiksel paradokslar — beyin yakıcı çelişkiler."""
    styled_section("🌀 Matematik Paradoksları", "#ec4899")

    _render_html("""
    <div style="background:linear-gradient(135deg,#831843,#be185d);border-radius:20px;padding:22px;margin-bottom:20px;
                 border:2px solid rgba(236,72,153,0.4);text-align:center">
        <div style="font-size:2rem;margin-bottom:8px" class="mat-grow">🌀🤯</div>
        <div style="font-weight:700;color:#e0e7ff !important;font-size:1.1rem">Matematik Bazen Mantığı Yıkar!</div>
        <div style="color:#fce7f3 !important;font-size:0.85rem">Bu paradokslar yüzyıllardır matematikçilerin uykusunu kaçırıyor.</div>
    </div>
    """)

    paradokslar = [
        {
            "ad": "🐢 Zenon'un Paradoksu — Aşil ve Kaplumbağa",
            "aciklama": (
                "Hızlı Aşil yavaş kaplumbağayı asla yakalayamaz! Çünkü Aşil kaplumbağanın olduğu "
                "noktaya geldiğinde kaplumbağa biraz ilerlemiştir. Aşil o noktaya geldiğinde kaplumbağa "
                "yine biraz ilerlemiştir... Sonsuz kez tekrarlanır!\n\n"
                "**Çözüm:** Sonsuz toplamın sonlu olabilmesi! 1/2 + 1/4 + 1/8 + ... = 1. "
                "Sonsuz adım sonlu zamanda tamamlanır. Bu paradoks kalkülüsün doğuşuna katkı sağladı."
            ),
        },
        {
            "ad": "🏨 Hilbert'in Sonsuz Oteli",
            "aciklama": (
                "Sonsuz odalı otel tamamen dolu. Yeni bir misafir geliyor. Yer var mı?\n\n"
                "**EVET!** Herkesi bir sonraki odaya kaydır: 1→2, 2→3, n→n+1. Oda 1 boşalır!\n\n"
                "Peki **sonsuz** yeni misafir gelirse? Herkesi 2n'inci odaya kaydır: 1→2, 2→4, 3→6... "
                "Tüm tek odalar boşalır — sonsuz oda!\n\n"
                "**Sonuç:** ∞ + 1 = ∞, ∞ + ∞ = ∞. Sonsuzluk bir sayı değil, bir kavramdır."
            ),
        },
        {
            "ad": "🃏 Monty Hall Problemi",
            "aciklama": (
                "3 kapı: birinde araba, ikisinde keçi. Bir kapı seçiyorsun. Sunucu keçi olan bir kapıyı açıyor.\n\n"
                "**Kapını değiştirir misin?** Sezgi: fark etmez (50-50). Matematik: **DEĞİŞTİR!**\n\n"
                "İlk seçimde doğru olma olasılığı 1/3. Değiştirince 2/3! Çünkü sunucu bilgisini kullanarak "
                "keçi olan kapıyı açtı — kalan kapıda araba olma olasılığı 2/3'e çıktı.\n\n"
                "Bu problem 1990'da Marilyn vos Savant tarafından açıklandığında 10.000 mektup geldi — "
                "900'ü doktoralı matematikçilerden: 'Yanlışsınız!' Ama haklıydı!"
            ),
        },
        {
            "ad": "📏 Banach-Tarski Paradoksu",
            "aciklama": (
                "Bir küreyi parçalara ayırıp yeniden birleştirerek **tamamen aynı boyutta 2 küre** "
                "elde edebilirsiniz!\n\n"
                "Fiziksel olarak imkansız ama matematiksel olarak **kanıtlanmış**. Seçim aksiyomu "
                "kullanılarak sonsuz parçalama yapılır.\n\n"
                "Bu paradoks, sonsuzluk matematiğinin ne kadar tuhaf olabileceğini gösterir. "
                "1 portakal → 2 portakal... bedava yemek! (Tabii sadece matematikte 😄)"
            ),
        },
        {
            "ad": "💈 Berber Paradoksu (Russell)",
            "aciklama": (
                "Bir köyde tek berber var. Kuralı: 'Kendini tıraş etmeyen herkesi tıraş ederim.'\n\n"
                "**Soru:** Berber kendini tıraş eder mi?\n\n"
                "- Kendini tıraş ederse → kuralına göre kendini tıraş etmemeli (çünkü kendini tıraş edenleri tıraş etmez)\n"
                "- Kendini tıraş etmezse → kuralına göre kendini tıraş etmeli (çünkü kendini tıraş etmeyenleri tıraş eder)\n\n"
                "**ÇELİŞKİ!** Bu paradoks, Russell'ın küme kuramındaki çelişkiyi göstermiş ve "
                "modern mantığın temellerini sarsmıştır."
            ),
        },
        {
            "ad": "🎂 Doğum Günü Paradoksu",
            "aciklama": (
                "Bir odada kaç kişi olmalı ki, en az 2 kişinin aynı doğum günü olma olasılığı %50'yi geçsin?\n\n"
                "Sezgi: 183 kişi (365/2). Gerçek: **23 kişi!** 🤯\n\n"
                "70 kişide olasılık %99.9'u geçer!\n\n"
                "**Neden bu kadar az?** Çünkü her yeni kişi, odadaki TÜM kişilerle karşılaştırılır. "
                "23 kişi = C(23,2) = 253 çift! 253 karşılaştırma çok fazla."
            ),
        },
        {
            "ad": "🔄 0.999... = 1 Paradoksu",
            "aciklama": (
                "0.9999... (sonsuz 9) tam olarak 1'e eşittir. Çoğu insan buna inanmaz!\n\n"
                "**İspat 1:** x = 0.999..., 10x = 9.999..., 10x - x = 9, 9x = 9, x = 1 ✓\n"
                "**İspat 2:** 1/3 = 0.333..., 3 × (1/3) = 1, 3 × 0.333... = 0.999... = 1 ✓\n"
                "**İspat 3:** 1 - 0.999... = 0.000... = 0, fark sıfır → eşitler ✓\n\n"
                "Bu bir paradoks değil, sonsuzluğun doğasının bir sonucu. "
                "İki farklı gösterim, aynı sayı — tıpkı 1/2 = 2/4 gibi."
            ),
        },
        {
            "ad": "🐛 Sorites Paradoksu (Yığın Paradoksu)",
            "aciklama": (
                "1.000.000 kum tanesi bir yığın mıdır? Evet.\n"
                "1 tane çıkarırsak? Hâlâ yığın.\n"
                "1 daha çıkarırsak? Hâlâ yığın.\n"
                "...\n"
                "1 kum tanesi yığın mıdır? **HAYIR.**\n\n"
                "Ama hangi adımda yığın olmaktan çıktı? Kesin bir sınır yok!\n\n"
                "Bu paradoks, matematikteki kesinlik ile günlük dildeki belirsizlik arasındaki "
                "farkı gösterir. Fuzzy mantık bu soruna çözüm arar."
            ),
        },
        {
            "ad": "⚡ Thomson'ın Lambası",
            "aciklama": (
                "Bir lamba: 1 dk sonra aç, 1/2 dk sonra kapa, 1/4 dk sonra aç, 1/8 dk sonra kapa...\n\n"
                "2 dakika sonra (1+1/2+1/4+...=2) lamba açık mı kapalı mı?\n\n"
                "Sonsuz kez açılıp kapanmış — son durumu belirsiz! Bu, süpertask "
                "(sonsuz işlemi sonlu zamanda tamamlama) kavramının çelişkisini gösterir."
            ),
        },
        {
            "ad": "🎯 İki Zarf Problemi",
            "aciklama": (
                "İki zarfta para var. Biri diğerinin 2 katı. Birini açıyorsun: 100 TL.\n\n"
                "Değiştirmeli misin? Diğer zarfta ya 50 ya 200 TL var.\n"
                "Beklenen değer: (50+200)/2 = 125 > 100. Değiştir!\n\n"
                "Ama aynı mantık diğer zarf için de geçerli — sonsuz döngü!\n\n"
                "**Paradoks:** Her iki zarf için de değiştirmek avantajlı görünüyor. "
                "Sorun, koşullu olasılığın yanlış kullanımından kaynaklanır."
            ),
        },
    ]

    for idx, p in enumerate(paradokslar):
        with st.expander(p["ad"], expanded=(idx == 0)):
            st.markdown(p["aciklama"])


def _render_cozulmemis():
    """Matematiğin çözülmemiş büyük problemleri."""
    styled_section("❓ Çözülmemiş Büyük Problemler", "#ef4444")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1a0505,#7f1d1d);border-radius:20px;padding:22px;margin-bottom:20px;
                 border:2px solid rgba(239,68,68,0.4);text-align:center">
        <div style="font-size:2rem;margin-bottom:8px">❓🏆💰</div>
        <div style="font-weight:700;color:#fca5a5 !important;font-size:1.1rem">Bunları Çözersen 1 Milyon Dolar Kazanırsın!</div>
        <div style="color:#fecaca !important;font-size:0.85rem">Clay Matematik Enstitüsü 7 Milenyum Problemi belirledi. Her birinin ödülü 1.000.000$!</div>
    </div>
    """)

    problemler = [
        {
            "ad": "📊 P vs NP Problemi",
            "odul": "1.000.000$", "durum": "Çözülmedi",
            "aciklama": (
                "Hızlı doğrulanabilen her problem hızlı çözülebilir mi?\n\n"
                "**P:** Polinom zamanda çözülebilen problemler (sıralama, arama)\n"
                "**NP:** Polinom zamanda doğrulanabilen problemler (Sudoku çözümü)\n\n"
                "P = NP ise: Tüm şifreler kırılır, protein katlanması çözülür, kanser tedavisi bulunur!\n"
                "P ≠ NP ise: Bazı problemler doğası gereği zordur.\n\n"
                "Bilgisayar biliminin en önemli açık sorusu. Çözen kişi dünyayı değiştirir."
            ),
        },
        {
            "ad": "🔢 Riemann Hipotezi",
            "odul": "1.000.000$", "durum": "Çözülmedi",
            "aciklama": (
                "Riemann zeta fonksiyonunun sıfır olmayan tüm kökleri Re(s) = 1/2 doğrusu üzerinde midir?\n\n"
                "1859'dan beri çözülemiyor! İlk 10 trilyon kökün hepsi doğruyu karşılıyor ama "
                "genel kanıt yok.\n\n"
                "**Neden önemli?** Asal sayıların dağılımını tam olarak belirler. Kriptografi, "
                "fizik ve sayı kuramının temeli."
            ),
        },
        {
            "ad": "🌊 Navier-Stokes Denklemleri",
            "odul": "1.000.000$", "durum": "Çözülmedi",
            "aciklama": (
                "Akışkan hareketini tanımlayan denklemlerin her zaman düzgün çözümü var mıdır?\n\n"
                "Hava durumu tahmini, uçak tasarımı, okyanus akıntıları — hepsi bu denklemlere bağlı. "
                "Ama denklemlerin 3 boyutta her zaman 'güzel' davranıp davranmadığı bilinmiyor.\n\n"
                "Türbülans hâlâ fiziğin en büyük çözülmemiş problemidir."
            ),
        },
        {
            "ad": "🔗 Hodge Konjektürü",
            "odul": "1.000.000$", "durum": "Çözülmedi",
            "aciklama": (
                "Cebirsel geometride belirli kohomoloji sınıflarının cebirsel alt çeşitlemelerle "
                "temsil edilip edilemeyeceği sorusu.\n\n"
                "Çok soyut! Ama temelde şu soruyu sorar: Geometrik şekillerin topolojik özelliklerini "
                "cebirsel olarak tam olarak yakalayabilir miyiz?"
            ),
        },
        {
            "ad": "✅ Poincaré Konjektürü",
            "odul": "1.000.000$ (reddedildi)", "durum": "ÇÖZÜLDÜ! (2003)",
            "aciklama": (
                "Her basit bağlantılı, kapalı 3-manifold bir 3-küreye homeomorf mudur?\n\n"
                "**Grigori Perelman** 2003'te çözdü! Fields Madalyası ve 1 milyon dolar ödülü **reddetti!**\n\n"
                "'Evreni kontrol edebiliyorsam neden 1 milyon dolara ihtiyacım olsun?' dedi ve "
                "münzevi yaşamaya devam etti. 7 Milenyum probleminden çözülen tek problem."
            ),
        },
        {
            "ad": "🔄 Goldbach Konjektürü",
            "odul": "Milenyum problemi değil ama 300 yıllık", "durum": "Çözülmedi",
            "aciklama": (
                "2'den büyük her çift sayı, iki asal sayının toplamı olarak yazılabilir mi?\n\n"
                "4=2+2, 6=3+3, 8=3+5, 10=3+7=5+5, 12=5+7...\n\n"
                "4×10¹⁸'e kadar tüm çift sayılar için doğrulanmış ama genel kanıt yok! "
                "1742'den beri çözülemiyor — ifade etmesi kolay, kanıtlaması imkansız görünüyor."
            ),
        },
        {
            "ad": "👫 İkiz Asal Konjektürü",
            "odul": "Açık problem", "durum": "Kısmen çözüldü",
            "aciklama": (
                "Sonsuz sayıda ikiz asal çifti (farkları 2 olan asallar) var mıdır?\n\n"
                "(3,5), (5,7), (11,13), (17,19), (29,31), (41,43)...\n\n"
                "2013'te Yitang Zhang çığır açtı: farkı 70 milyondan az olan sonsuz asal çifti var! "
                "Sonra James Maynard farkı 600'e indirdi. Ama 2'ye indirmek (ikiz asal) hâlâ kanıtlanmadı."
            ),
        },
        {
            "ad": "🔢 Collatz Konjektürü (3n+1)",
            "odul": "Açık problem", "durum": "Çözülmedi",
            "aciklama": (
                "Herhangi bir pozitif tam sayıyla başla:\n"
                "- Çift ise 2'ye böl\n"
                "- Tek ise 3 ile çarp ve 1 ekle\n"
                "- Tekrarla\n\n"
                "**Her sayı sonunda 1'e ulaşır mı?**\n\n"
                "7 → 22 → 11 → 34 → 17 → 52 → 26 → 13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1 ✓\n\n"
                "10⁶⁸'e kadar tüm sayılar için doğrulanmış ama kanıt yok! "
                "Erdős: 'Matematik bu tür problemlere henüz hazır değil.'"
            ),
        },
    ]

    for idx, p in enumerate(problemler):
        cozuldu = "ÇÖZÜLDÜ" in p["durum"]
        renk = "#10b981" if cozuldu else "#ef4444"
        with st.expander(f"{p['ad']} — {'✅' if cozuldu else '❓'} {p['durum']}", expanded=(idx == 0)):
            _render_html(f"""
            <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="color:{renk} !important;font-weight:700;font-size:0.85rem">💰 {p['odul']}</span>
                <span style="color:{renk} !important;font-weight:700;font-size:0.85rem">{p['durum']}</span>
            </div>
            """)
            st.markdown(p["aciklama"])


def _render_gunluk_hayat_sayilar():
    """Günlük hayatta sayıların gücü."""
    styled_section("💡 Günlük Hayatta Sayıların Gücü", "#f59e0b")

    _render_html("""
    <div style="background:linear-gradient(135deg,#451a03,#78350f);border-radius:20px;padding:22px;margin-bottom:20px;
                 border:2px solid rgba(245,158,11,0.4);text-align:center">
        <div style="font-size:2rem;margin-bottom:8px">💡🌍</div>
        <div style="font-weight:700;color:#fde68a !important;font-size:1.1rem">Matematik Olmadan Bir Gün Geçiremezsin!</div>
        <div style="color:#fcd34d !important;font-size:0.85rem">Farkında olmasan da her an matematik kullanıyorsun.</div>
    </div>
    """)

    konular = [
        {
            "baslik": "🛒 Markette Matematik",
            "ikon": "🛒",
            "icerik": (
                "- **İndirim hesabı:** %30 indirim = fiyat × 0.70\n"
                "- **Birim fiyat karşılaştırma:** 500g = 15 TL vs 750g = 20 TL → hangisi ucuz? (30 TL/kg vs 26.7 TL/kg)\n"
                "- **Bütçe yönetimi:** Aylık gelir − giderler = tasarruf\n"
                "- **KDV hesabı:** Fiyat × 1.20 = KDV dahil fiyat\n"
                "- **Tartıda yuvarlama:** 1.48 kg → 1.5 kg"
            ),
        },
        {
            "baslik": "🍳 Mutfakta Matematik",
            "ikon": "🍳",
            "icerik": (
                "- **Tarif ölçekleme:** 4 kişilik tarif × 1.5 = 6 kişilik\n"
                "- **Oran:** 2 su bardağı un : 1 bardak süt = 2:1 oranı\n"
                "- **Pişirme süresi:** 1 kg et → 40 dk, 2.5 kg et → 100 dk (doğru orantı)\n"
                "- **Kesir:** Pastanın 3/8'i kaç dilim? 8 dilimin 3'ü!\n"
                "- **Dönüşüm:** 1 çay kaşığı = 5 mL, 1 su bardağı = 200 mL"
            ),
        },
        {
            "baslik": "🚗 Trafikte Matematik",
            "ikon": "🚗",
            "icerik": (
                "- **Hız-Zaman-Yol:** 90 km/h × 2 saat = 180 km\n"
                "- **Yakıt hesabı:** 100 km'de 7 litre → 500 km = 35 litre\n"
                "- **Varış süresi:** 300 km ÷ 80 km/h = 3.75 saat = 3 saat 45 dk\n"
                "- **Fren mesafesi:** v² / (2 × sürtünme × g) — hız 2 katına çıkarsa fren 4 kat uzar!\n"
                "- **GPS:** Trigonometri + uydu geometrisi = konum"
            ),
        },
        {
            "baslik": "🏠 Evde Matematik",
            "ikon": "🏠",
            "icerik": (
                "- **Boya hesabı:** Duvar alanı = 2×(uzunluk+genişlik)×yükseklik − kapı/pencere\n"
                "- **Halı seçimi:** 4m × 5m oda = 20 m² halı\n"
                "- **Elektrik faturası:** 100W × 10 saat = 1 kWh × birim fiyat\n"
                "- **Faiz:** 100.000 TL × %2 aylık = 2.000 TL/ay faiz\n"
                "- **İnşaat:** 1 m³ beton = 7 torba çimento + kum + çakıl (oran!)"
            ),
        },
        {
            "baslik": "📱 Teknolojide Matematik",
            "ikon": "📱",
            "icerik": (
                "- **Piksel:** 1920×1080 ekran = 2.073.600 piksel (çarpma!)\n"
                "- **Depolama:** 1 GB = 1024 MB = 1.073.741.824 byte (2'nin kuvvetleri)\n"
                "- **Sıkıştırma:** MP3 dosya 10× küçültülür (Fourier dönüşümü!)\n"
                "- **Şifreleme:** Online bankacılık = asal sayılar + modüler aritmetik\n"
                "- **Yapay Zeka:** Matris çarpımı + istatistik + kalkülüs = ChatGPT!"
            ),
        },
        {
            "baslik": "⚽ Sporda Matematik",
            "ikon": "⚽",
            "icerik": (
                "- **Averaj:** Atılan gol − yenen gol = averaj\n"
                "- **Yüzde:** 20 maçta 14 galibiyet = %70 başarı oranı\n"
                "- **Olasılık:** Penaltı yönü tahmini = 1/3 (sol/orta/sağ)\n"
                "- **Fizik:** Top atış açısı 45° = maksimum mesafe\n"
                "- **İstatistik:** xG (beklenen gol) = her şutun gol olma olasılığı toplamı"
            ),
        },
        {
            "baslik": "🎵 Müzikte Matematik",
            "ikon": "🎵",
            "icerik": (
                "- **Frekans:** La notası = 440 Hz, 1 oktav yukarı = 880 Hz (×2)\n"
                "- **Ritim:** 4/4 ölçü = 4 vuruş, 3/4 = vals ritmi (kesirler!)\n"
                "- **Harmonik:** Akorlar = frekans oranları (4:5:6 = majör akor)\n"
                "- **Pisagor:** Müzik-matematik ilişkisini keşfeden ilk kişi\n"
                "- **Dijital müzik:** Ses dalgası → 44.100 örnek/saniye (sayısallaştırma)"
            ),
        },
        {
            "baslik": "🏥 Tıpta Matematik",
            "ikon": "🏥",
            "icerik": (
                "- **İlaç dozu:** 10 mg/kg × 70 kg = 700 mg (orantı)\n"
                "- **Kalp atışı:** 72 atış/dk = 103.680 atış/gün (çarpma)\n"
                "- **Tomografi:** CT tarama = trigonometri + lineer cebir\n"
                "- **Epidemi:** R₀ = 2 ise her hasta 2 kişiye bulaştırır → üstel büyüme!\n"
                "- **DNA dizilimi:** 3 milyar baz çifti = istatistik + kombinatorik"
            ),
        },
    ]

    for k in konular:
        with st.expander(f"{k['baslik']}", expanded=False):
            _render_html(f'<div style="text-align:center;font-size:3rem;margin-bottom:12px">{k["ikon"]}</div>')
            st.markdown(k["icerik"])


# ══════════════════════════════════════════════════════════════════════════════
# 12) ZEKA GELİŞTİRME — ULTRA PREMİUM
# ══════════════════════════════════════════════════════════════════════════════

def _render_zeka_gelistirme(store: MatematikDataStore):
    """0-6. sınıf zeka geliştirme — ultra premium interaktif içerik."""
    import random as _r
    import streamlit.components.v1 as components

    styled_section("🧠 Zeka Geliştirme Merkezi", "#8b5cf6")

    _render_html("""
    <style>
    @keyframes zk-glow { 0%,100%{box-shadow:0 0 8px #a78bfa40} 50%{box-shadow:0 0 24px #a78bfa80} }
    @keyframes zk-float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
    @keyframes zk-spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
    .zk-hero {
        background: linear-gradient(135deg, #1e0a3a 0%, #3b0764 40%, #6d28d9 100%);
        border-radius: 28px; padding: 36px; margin-bottom: 28px;
        border: 2px solid rgba(167,139,250,0.4);
        text-align: center; position: relative; overflow: hidden;
        animation: zk-glow 4s ease-in-out infinite;
    }
    .zk-hero::before {
        content: '🧠'; position: absolute; top: -30px; right: -30px;
        font-size: 10rem; opacity: 0.04; transform: rotate(-15deg);
    }
    .zk-scene {
        background: linear-gradient(180deg, #0c1222 0%, #1a1a3e 50%, #0f3d0f 100%);
        border-radius: 20px; min-height: 280px; position: relative;
        overflow: hidden; margin-bottom: 20px;
        border: 2px solid rgba(99,102,241,0.2);
    }
    .zk-card {
        background: linear-gradient(145deg, #1a0a2e, #2d1b69);
        border-radius: 18px; padding: 22px; margin-bottom: 14px;
        border: 1px solid rgba(167,139,250,0.2);
        transition: all 0.3s ease;
    }
    .zk-card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(139,92,246,0.2); }
    .zk-emoji-grid {
        display: grid; gap: 6px; padding: 12px;
        background: #0f172a; border-radius: 14px;
        border: 1px solid rgba(99,102,241,0.15);
    }
    .zk-emoji-cell {
        display: flex; align-items: center; justify-content: center;
        font-size: 1.8rem; padding: 8px; border-radius: 10px;
        cursor: pointer; transition: all 0.2s;
        background: rgba(30,27,75,0.6); border: 1px solid rgba(99,102,241,0.1);
    }
    .zk-emoji-cell:hover { background: rgba(99,102,241,0.15); transform: scale(1.1); }
    .zk-progress-ring {
        width: 100px; height: 100px; border-radius: 50%;
        background: conic-gradient(#8b5cf6 var(--pct), #1e1b4b var(--pct));
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto;
    }
    .zk-progress-inner {
        width: 76px; height: 76px; border-radius: 50%;
        background: #0f0a1e; display: flex; align-items: center;
        justify-content: center; font-weight: 800; color: #a78bfa !important;
        font-size: 1.2rem;
    }
    </style>

    <div class="zk-hero">
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:10px" class="mat-grow">🧠✨</div>
            <h2 style="color:#e9d5ff !important;font-size:1.6rem;margin:0 0 8px !important">Zeka Geliştirme Merkezi</h2>
            <p style="color:#c4b5fd !important;font-size:0.95rem;margin:0 !important;max-width:650px;display:inline-block">
                Mantık, görsel algı, hafıza, örüntü tanıma, uzamsal zeka ve problem çözme —
                her gün 15 dakika pratik, zekayı %30 geliştirir! 🚀
            </p>
        </div>
    </div>
    """)

    sub = st.tabs([
        "📊 Zeka Panosu",
        "🤖 Egzersiz Fabrikası",
        "🧪 IQ Ölçüm Testi",
        "🔍 Örüntü Dedektifi",
        "🧩 Mantık Labirenti",
        "🎭 Hafıza Sarayı",
        "🌍 Görsel Zeka",
        "🐾 Hayvan Matematiği",
        "🧮 Matematik Zinciri",
        "🔢 Kayıp Sayı",
        "🎲 Zar Matematiği",
        "⏱️ Hız Testi",
        "🌱 Doğa ile Sayılar",
        "🎪 Zeka Sirki",
    ])

    with sub[0]:
        _zk_pano(store)
    with sub[1]:
        _zk_egzersiz_fabrikasi(store)
    with sub[2]:
        _zk_iq_olcum()
    with sub[3]:
        _zk_oruntu_dedektifi()
    with sub[4]:
        _zk_mantik_labirenti()
    with sub[5]:
        _zk_hafiza_sarayi()
    with sub[6]:
        _zk_gorsel_zeka()
    with sub[7]:
        _zk_hayvan_matemat()
    with sub[8]:
        _zk_matematik_zinciri()
    with sub[9]:
        _zk_kayip_sayi()
    with sub[10]:
        _zk_zar_matemat()
    with sub[11]:
        _zk_hiz_testi()
    with sub[12]:
        _zk_doga_sayilar()
    with sub[13]:
        _zk_zeka_sirki()


# ── 12a) Örüntü Dedektifi ───────────────────────────────────────────────────

def _ai_zeka_tavsiye(modul_detay: list, genel_oran: float, toplam_soru: int, aktif: list) -> list[dict]:
    """AI bazlı kişiselleştirilmiş zeka geliştirme tavsiyeleri üret."""
    tavsiyeler = []

    pasif = [m for m in modul_detay if m["toplam"] == 0]
    zayif = [m for m in aktif if m["oran"] < 50] if aktif else []
    guclu = [m for m in aktif if m["oran"] >= 75] if aktif else []

    # 1. Başlangıç tavsiyesi
    if toplam_soru < 10:
        tavsiyeler.append({
            "ikon": "🚀", "baslik": "İlk Adım — Keşfet!",
            "mesaj": "Henüz yeterli veri yok. En az 3 farklı modülde 10'ar soru çözerek zeka profilini oluştur. Bu sayede AI Koç sana özel program hazırlayabilir.",
            "renk": "#3b82f6",
        })

    # 2. Pasif modüller
    if pasif:
        pasif_str = ", ".join(m["ad"] for m in pasif[:4])
        tavsiyeler.append({
            "ikon": "🎯", "baslik": f"Keşfedilmemiş Alanlar ({len(pasif)} modül)",
            "mesaj": f"Şu modülleri henüz denemedin: **{pasif_str}**. Zeka çok yönlüdür — her alanı deneyerek güçlü ve zayıf yanlarını keşfet!",
            "renk": "#6366f1",
        })

    # 3. Zayıf alanlar için özel tavsiye
    for m in zayif[:2]:
        alan_tavsiyeleri = {
            "🔍 Örüntü": "Günlük hayatta tekrar eden kalıplara dikkat et: müzik ritimleri, duvar kağıdı desenleri, trafik ışıkları. Beynin örüntü tanımayı pratikle geliştirir.",
            "🧩 Mantık": "Her gün 1 mantık bulmacası çöz. 'Eğer-ise' ilişkilerini düşün. Sudoku ve satranç mantıksal düşünmeyi güçlendirir.",
            "🎭 Hafıza": "Ezberleme teknikleri kullan: hikaye yöntemi (emojileri bir hikayeye bağla), mekan yöntemi (emojileri odandaki nesnelere yerleştir). Günde 5 dk pratik yeter!",
            "🌍 Görsel": "Fark bul oyunlarında sistematik tara: sol→sağ, üst→alt. Acele etme, her hücreye 1 saniye bak. Çevrendeki detaylara günlük hayatta dikkat et.",
            "🐾 Hayvan": "Problemleri görselleştir: parmaklarınla say, kağıda çiz. 'Toplam', 'paylaş', 'kalan' gibi anahtar kelimelere odaklan.",
            "🧮 Zincir": "İşlem sırasını takip etmek için her adımı not al. İlk sayıdan başla, adım adım ilerle. Zihinsel hesaplama pratiği yap.",
            "🔢 Kayıp Sayı": "Ters düşünmeyi dene: sonuçtan geriye doğru çalış. 'x + 5 = 12 ise x = 12 - 5' gibi ters işlem yap.",
            "🎲 Zar": "Hızlı toplama için ikili grupla: 3+4=7, sonra +2=9. Çarpım tablosunu pekiştir. Günde 5 dk zihinsel hesap pratiği yap.",
        }
        tavsiye_mesaj = alan_tavsiyeleri.get(m["ad"], f"{m['ad']} alanında daha fazla pratik yap. Günde 10 soru çöz.")
        tavsiyeler.append({
            "ikon": "💪", "baslik": f"Gelişim: {m['ad']} (%{m['oran']:.0f})",
            "mesaj": tavsiye_mesaj,
            "renk": "#f59e0b",
        })

    # 4. Güçlü alanlar için ileri seviye tavsiye
    for m in guclu[:1]:
        tavsiyeler.append({
            "ikon": "🌟", "baslik": f"Harika! {m['ad']} (%{m['oran']:.0f})",
            "mesaj": f"Bu alanda çok iyisin! Zorluk seviyesini 'Zor'a çıkar. Ayrıca bu becerini diğer alanlara transfer etmeyi dene — {m['ad']} yeteneğin diğer modüllerde de sana avantaj sağlar.",
            "renk": "#10b981",
        })

    # 5. Genel seviye tavsiyesi
    if genel_oran >= 80 and toplam_soru >= 50:
        tavsiyeler.append({
            "ikon": "🏆", "baslik": "Üstün Performans!",
            "mesaj": "Zeka puanın çok yüksek! Olimpiyat Arenası'na geç ve gerçek yarışma sorularıyla kendini test et. Ayrıca IQ Ölçüm Testi'ni çözerek detaylı analiz al.",
            "renk": "#eab308",
        })
    elif genel_oran >= 50 and toplam_soru >= 30:
        tavsiyeler.append({
            "ikon": "📈", "baslik": "İstikrarlı Gelişim",
            "mesaj": "Güzel ilerliyorsun! Şimdi zayıf alanlarına odaklan. Araştırmalar, zayıf alanlarda yapılan pratiklerin zeka gelişimine en büyük katkıyı sağladığını gösteriyor.",
            "renk": "#8b5cf6",
        })

    # 6. Pratik sıklığı tavsiyesi
    if toplam_soru >= 20:
        tavsiyeler.append({
            "ikon": "⏰", "baslik": "Günlük Rutin Önerisi",
            "mesaj": "Araştırmalar, günde 15 dakika düzenli zeka egzersizinin IQ'yu 2 yılda ortalama 5-10 puan artırdığını gösteriyor. En etkili zaman: sabah kahvaltıdan sonra veya öğleden sonra 3-4 arası.",
            "renk": "#06b6d4",
        })

    return tavsiyeler[:5]  # En fazla 5 tavsiye göster


def _ai_dikkat_tavsiye(modul_oranlar: dict, genel_oran: float) -> list[dict]:
    """AI bazlı dikkat geliştirme tavsiyeleri."""
    tavsiyeler = []

    zayif_moduller = {k: v for k, v in modul_oranlar.items() if v.get("toplam", 0) > 0 and v.get("oran", 0) < 50}
    guclu_moduller = {k: v for k, v in modul_oranlar.items() if v.get("toplam", 0) > 0 and v.get("oran", 0) >= 70}
    pasif = {k: v for k, v in modul_oranlar.items() if v.get("toplam", 0) == 0}

    dikkat_tavsiyeleri = {
        "farkli_bul": {
            "beceri": "Görsel Tarama",
            "tavsiye": "Sistematik tarama tekniği kullan: sol üstten başla, satır satır ilerle. Acele etme — her hücreye 0.5 saniye bak. Günlük hayatta 'farkı bul' oyunları, gazete bulmacaları ve detaylı resimleri inceleme pratiği yap.",
            "aktivite": "Çevrendeki bir odayı 30 saniye incele, sonra gözlerini kapat ve 5 detay hatırlamaya çalış. Her gün tekrarla.",
        },
        "sayi_avcisi": {
            "beceri": "Sıralı Tarama",
            "tavsiye": "Sayıları ararken bölgelere ayır: sol üst, sağ üst, sol alt, sağ alt. Her bölgede sırayla ara. Periferik görüşünü kullan — doğrudan bakmadan çevredeki sayıları fark etmeye çalış.",
            "aktivite": "Bir kitap sayfasında belirli bir harfi (ör: 'a') sayma egzersizi yap. Süreyi ölç ve her gün kısaltmaya çalış.",
        },
        "stroop": {
            "beceri": "Seçici Dikkat / Ketleme",
            "tavsiye": "Stroop etkisi, otomatik tepkileri bastırma (ketleme) yeteneğini ölçer. Bu beceri, dikkat dağıtıcıları yok saymak için kritiktir. Meditasyon ve nefes egzersizleri ketleme kontrolünü güçlendirir.",
            "aktivite": "Günde 5 dk nefes meditasyonu yap: 4 saniye nefes al, 4 saniye tut, 4 saniye ver. Zihnine gelen düşünceleri yargılamadan gözlemle.",
        },
        "eksik_ne": {
            "beceri": "Çalışma Belleği",
            "tavsiye": "Çalışma belleği, bilgiyi kısa süre tutma ve işleme kapasitesidir. Gruplandırma (chunking) tekniğini kullan: 8 emojiyi 2'li veya 3'lü gruplar halinde ezberle, tek tek değil.",
            "aktivite": "Alışveriş listesini kağıda yazmadan ezberlemeye çalış. Başta 3 madde ile başla, her hafta 1 artır.",
        },
        "sira_takibi": {
            "beceri": "Sıralı Hafıza",
            "tavsiye": "Sıralı hafıza için 'hikaye zinciri' tekniğini kullan: her emojiyi bir hikayeye bağla. Örn: '🔴 kırmızı top 🔵 mavi denize düştü' gibi. Görsel ve duygusal bağlantılar hafızayı güçlendirir.",
            "aktivite": "Telefon numaralarını, plakaları veya kapı şifrelerini ezbere tekrarla. Her gün 1 yeni numara ekle.",
        },
        "hiz_odagi": {
            "beceri": "Tepki Hızı",
            "tavsiye": "Tepki hızı hem dikkat hem de motor koordinasyon gerektirir. Düzenli fiziksel egzersiz (özellikle top oyunları) tepki süresini iyileştirir. Yeterli uyku kritiktir — uykusuz tepki süresi %30 yavaşlar.",
            "aktivite": "Bir arkadaşınla 'el çırpma' oyunu oyna veya online tepki süresi testleri çöz. Hedefe: 300ms altı.",
        },
        "cift_gorev": {
            "beceri": "Bölünmüş Dikkat",
            "tavsiye": "Bölünmüş dikkat en zor dikkat türüdür. Aslında beyin gerçek anlamda iki şeye aynı anda odaklanamaz — hızlı geçiş yapar. Bu geçiş hızını artırmak için çift görev pratiği yap.",
            "aktivite": "Yürürken geriye doğru say (100, 97, 94...) veya müzik dinlerken matematik sorusu çöz. Başta zor ama pratikle gelişir!",
        },
    }

    # Zayıf alanlar için detaylı tavsiye
    for mk, mv in zayif_moduller.items():
        info = dikkat_tavsiyeleri.get(mk, {})
        if info:
            tavsiyeler.append({
                "ikon": "🔬", "baslik": f"Gelişim: {info['beceri']} (%{mv.get('oran',0):.0f})",
                "mesaj": info["tavsiye"],
                "renk": "#f59e0b",
            })
            tavsiyeler.append({
                "ikon": "🏋️", "baslik": f"Günlük Aktivite: {info['beceri']}",
                "mesaj": info["aktivite"],
                "renk": "#8b5cf6",
            })

    # Pasif modüller
    if pasif:
        pasif_str = ", ".join(v.get("beceri", k) for k, v in list(pasif.items())[:3])
        tavsiyeler.append({
            "ikon": "🎯", "baslik": f"Keşfedilmemiş Beceriler ({len(pasif)})",
            "mesaj": f"Şu dikkat becerilerini henüz test etmedin: **{pasif_str}**. Dikkat çok boyutlu bir beceridir — tüm alanları deneyerek tam profil oluştur.",
            "renk": "#6366f1",
        })

    # Güçlü alanlar
    for mk, mv in list(guclu_moduller.items())[:1]:
        info = dikkat_tavsiyeleri.get(mk, {})
        tavsiyeler.append({
            "ikon": "🌟", "baslik": f"Güçlü Alan: {info.get('beceri', mk)} (%{mv.get('oran',0):.0f})",
            "mesaj": f"Bu alanda üstün performans gösteriyorsun! Zorluk seviyesini artır ve süre limitini kısalt. Bu becerini günlük hayatta da aktif kullan.",
            "renk": "#10b981",
        })

    # Genel dikkat tavsiyesi
    if genel_oran >= 70:
        tavsiyeler.append({
            "ikon": "🧠", "baslik": "Bilimsel Gerçek: Dikkat Eğitilebilir!",
            "mesaj": "Nöroplastisite araştırmaları, düzenli dikkat eğitiminin prefrontal korteksi güçlendirdiğini, beyaz madde bağlantılarını artırdığını ve dikkat süresini %40'a kadar iyileştirdiğini göstermektedir. Günde 10-15 dk yeterlidir.",
            "renk": "#06b6d4",
        })
    else:
        tavsiyeler.append({
            "ikon": "💡", "baslik": "Dikkat Geliştirme İpuçları",
            "mesaj": "1) Her gün aynı saatte pratik yap (rutin oluştur) 2) Sessiz ortamda çalış 3) Telefonu kapat 4) 25 dk çalış, 5 dk mola (Pomodoro) 5) Yeterli uyku al (7-9 saat) 6) Düzenli egzersiz yap 7) Su iç — dehidrasyon dikkati %15 azaltır!",
            "renk": "#ef4444",
        })

    return tavsiyeler[:6]


def _zk_pano(store: MatematikDataStore):
    """Profesyonel Zeka Geliştirme Panosu — ilerleme, grafik, analiz."""
    styled_section("📊 Zeka Geliştirme Panosu", "#8b5cf6")

    auth_user = st.session_state.get("auth_user", {})
    user_name = auth_user.get("ad_soyad", auth_user.get("username", "Kullanıcı"))

    # Session state'den tüm zeka modülü skorlarını topla
    zeka_modulleri = [
        ("🔍 Örüntü", "zk_ort_state", "#6366f1"),
        ("🧩 Mantık", "zk_ml_state", "#10b981"),
        ("🎭 Hafıza", "zk_hf_state", "#f59e0b"),  # farklı yapı
        ("🌍 Görsel", "zk_gz_state", "#06b6d4"),
        ("🐾 Hayvan", "zk_hm_state", "#f97316"),
        ("🧮 Zincir", "zk_mz_state", "#6366f1"),
        ("🔢 Kayıp Sayı", "zk_ks_state", "#eab308"),
        ("🎲 Zar", "zk_zr_state", "#ec4899"),
    ]

    toplam_dogru = 0
    toplam_soru = 0
    modul_detay = []

    for ad, sk, renk in zeka_modulleri:
        data = st.session_state.get(sk, {})
        d = data.get("skor", data.get("dogru", 0))
        t = data.get("toplam", 0)
        toplam_dogru += d
        toplam_soru += t
        oran = (d / t * 100) if t > 0 else 0
        modul_detay.append({"ad": ad, "dogru": d, "toplam": t, "oran": oran, "renk": renk})

    genel_oran = (toplam_dogru / toplam_soru * 100) if toplam_soru > 0 else 0
    aktif_modul = sum(1 for m in modul_detay if m["toplam"] > 0)

    # Zeka seviyesi belirleme
    if genel_oran >= 90:
        seviye, sev_emoji, sev_renk = "Üstün Zeka", "🏆", "#eab308"
    elif genel_oran >= 75:
        seviye, sev_emoji, sev_renk = "Yüksek Zeka", "🌟", "#8b5cf6"
    elif genel_oran >= 60:
        seviye, sev_emoji, sev_renk = "İyi Seviye", "⭐", "#3b82f6"
    elif genel_oran >= 40:
        seviye, sev_emoji, sev_renk = "Gelişmekte", "🌿", "#10b981"
    elif toplam_soru > 0:
        seviye, sev_emoji, sev_renk = "Başlangıç", "🌱", "#f59e0b"
    else:
        seviye, sev_emoji, sev_renk = "Henüz Başlanmadı", "❓", "#64748b"

    # Ana puan kartı
    _render_html(f"""
    <div style="background:linear-gradient(135deg,#0c0024,#1e0a3a,{sev_renk}15);border-radius:24px;padding:28px;margin-bottom:20px;
                 border:2px solid {sev_renk}50;text-align:center;position:relative;overflow:hidden">
        <div style="position:absolute;top:-20px;right:-20px;font-size:8rem;opacity:0.03">🧠</div>
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:8px">{sev_emoji}</div>
            <div style="font-size:2.5rem;font-weight:900;color:{sev_renk} !important">
                {'%' + f'{genel_oran:.0f}' if toplam_soru > 0 else '—'}
            </div>
            <div style="font-size:1.2rem;font-weight:700;color:#e0e7ff !important;margin:4px 0">{seviye}</div>
            <div style="font-size:0.85rem;color:#94a3b8 !important">{user_name} • {toplam_dogru}/{toplam_soru} doğru • {aktif_modul}/8 modül aktif</div>

            <div style="max-width:400px;margin:16px auto 0;background:#1e1b4b;border-radius:12px;height:14px;overflow:hidden">
                <div style="width:{genel_oran:.0f}%;height:100%;border-radius:12px;
                             background:linear-gradient(90deg,#ef4444,#f59e0b,#10b981);
                             transition:width 0.8s"></div>
            </div>
        </div>
    </div>
    """)

    # Özet istatistik kartları
    cols = st.columns(4)
    stats = [
        ("🧠", f"{genel_oran:.0f}%" if toplam_soru > 0 else "—", "Zeka Puanı"),
        ("📚", str(toplam_soru), "Toplam Egzersiz"),
        ("✅", str(toplam_dogru), "Doğru Cevap"),
        ("📊", f"{aktif_modul}/8", "Aktif Modül"),
    ]
    for col, (ikon, deger, etiket) in zip(cols, stats):
        with col:
            _render_html(f"""
            <div class="mat-stat-card" style="padding:14px">
                <div style="font-size:1.5rem">{ikon}</div>
                <div style="font-weight:800;color:#818cf8 !important;font-size:1.4rem">{deger}</div>
                <div style="font-size:0.7rem;color:#94a3b8 !important">{etiket}</div>
            </div>
            """)

    # Modül bazlı performans radar
    styled_section("📋 Zeka Alanları Performansı", "#6366f1")

    for m in modul_detay:
        oran = m["oran"]
        durum = "🟢" if oran >= 70 else "🟡" if oran >= 40 else "🔴" if m["toplam"] > 0 else "⚪"
        bar_renk = m["renk"]

        _render_html(f"""
        <div style="background:#0f172a;border-radius:12px;padding:12px 16px;margin-bottom:6px;
                     border-left:4px solid {bar_renk}">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                <span style="font-weight:700;color:#e0e7ff !important;font-size:0.85rem">{durum} {m['ad']}</span>
                <span style="font-weight:700;color:{bar_renk} !important;font-size:0.85rem">
                    {m['dogru']}/{m['toplam']} {'• %' + f"{oran:.0f}" if m['toplam']>0 else ''}
                </span>
            </div>
            <div style="background:#1e1b4b;border-radius:6px;height:8px;overflow:hidden">
                <div style="width:{oran:.0f}%;height:100%;background:{bar_renk};border-radius:6px"></div>
            </div>
        </div>
        """)

    # Güçlü ve zayıf alanlar
    aktif = [m for m in modul_detay if m["toplam"] > 0]
    if len(aktif) >= 2:
        en_guclu = max(aktif, key=lambda x: x["oran"])
        en_zayif = min(aktif, key=lambda x: x["oran"])

        col1, col2 = st.columns(2)
        with col1:
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#052e16,#065f46);border-radius:16px;padding:16px;
                         border:2px solid rgba(16,185,129,0.3);text-align:center">
                <div style="font-size:1.3rem;margin-bottom:4px">💪</div>
                <div style="font-weight:700;color:#bbf7d0 !important;font-size:0.85rem">En Güçlü Alan</div>
                <div style="font-size:1.1rem;font-weight:800;color:#10b981 !important">{en_guclu['ad']} (%{en_guclu['oran']:.0f})</div>
            </div>
            """)
        with col2:
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#451a03,#78350f);border-radius:16px;padding:16px;
                         border:2px solid rgba(245,158,11,0.3);text-align:center">
                <div style="font-size:1.3rem;margin-bottom:4px">🎯</div>
                <div style="font-weight:700;color:#fde68a !important;font-size:0.85rem">Gelişim Alanı</div>
                <div style="font-size:1.1rem;font-weight:800;color:#f59e0b !important">{en_zayif['ad']} (%{en_zayif['oran']:.0f})</div>
            </div>
            """)

    # AI Tavsiye Sistemi
    styled_section("🤖 AI Zeka Koçu Tavsiyeleri", "#ec4899")
    if toplam_soru > 0:
        tavsiyeler = _ai_zeka_tavsiye(modul_detay, genel_oran, toplam_soru, aktif)
        for t in tavsiyeler:
            _render_html(f"""
            <div style="background:linear-gradient(135deg,{t['renk']}08,{t['renk']}04);border-radius:14px;
                         padding:14px 18px;margin-bottom:8px;border-left:4px solid {t['renk']};
                         border:1px solid {t['renk']}20">
                <div style="display:flex;align-items:flex-start;gap:12px">
                    <div style="font-size:1.5rem;min-width:30px">{t['ikon']}</div>
                    <div>
                        <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem;margin-bottom:4px">{t['baslik']}</div>
                        <div style="color:#94a3b8 !important;font-size:0.83rem;line-height:1.5">{t['mesaj']}</div>
                    </div>
                </div>
            </div>
            """)
    else:
        _render_html("""
        <div style="background:#0f172a;border-radius:14px;padding:20px;text-align:center;
                     border:1px solid rgba(99,102,241,0.15)">
            <div style="font-size:2rem;margin-bottom:8px">🤖</div>
            <div style="color:#94a3b8 !important;font-size:0.9rem">
                Henüz veri yok. Egzersiz sekmelerinden başla —<br>
                AI Koç sana özel tavsiyeler üretecek!
            </div>
        </div>
        """)


def _zk_egzersiz_fabrikasi(store: MatematikDataStore):
    """Sonsuz zeka egzersizi üretici — tüm türlerden toplu üretim ve veritabanına kayıt."""
    import random as _r
    styled_section("🤖 Zeka Egzersizi Fabrikası", "#8b5cf6")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1e0a3a,#4c1d95);border-radius:20px;padding:24px;margin-bottom:20px;
                 border:2px solid rgba(139,92,246,0.4);text-align:center">
        <div style="font-size:2.5rem;margin-bottom:8px" class="mat-grow">🤖🧠⚡</div>
        <div style="font-weight:700;color:#e9d5ff !important;font-size:1.2rem">Sonsuz Egzersiz Fabrikası!</div>
        <div style="color:#c4b5fd !important;font-size:0.9rem">Bir tıkla yüzlerce zeka egzersizi üret — örüntü, mantık, hafıza, görsel, hayvan problemi!</div>
    </div>
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        tur = st.selectbox("Egzersiz Türü", [
            ("karisik", "🔀 Karışık (Her Türden)"),
            ("oruntu", "🔍 Örüntü Tanıma"),
            ("mantik", "🧩 Mantık Soruları"),
            ("hafiza", "🎭 Hafıza Egzersizi"),
            ("gorsel", "🌍 Görsel Fark Bulma"),
            ("hayvan", "🐾 Hayvan Problemleri"),
        ], key="zk_fab_tur", format_func=lambda x: x[1])
    with col2:
        zorluk = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="zk_fab_zor", index=1,
                               format_func=lambda x: {"kolay": "🌱 Kolay", "orta": "🌿 Orta", "zor": "🌳 Zor"}[x])
    with col3:
        adet = st.selectbox("Adet", [10, 25, 50, 100, 250, 500], key="zk_fab_adet", index=2)

    if st.button(f"🚀 {adet} Egzersiz Üret!", key="zk_fab_go", type="primary"):
        with st.spinner(f"🤖 {adet} egzersiz üretiliyor..."):
            gen = ZekaEgzersizGenerator()
            egzersizler = gen.toplu_uret(tur[0], zorluk, adet)

        st.session_state["zk_fab_sonuc"] = egzersizler

        _render_html(f"""
        <div style="background:linear-gradient(135deg,#052e16,#065f46);border-radius:16px;padding:20px;margin:16px 0;
                     border:2px solid rgba(16,185,129,0.4);text-align:center">
            <div style="font-size:2rem;margin-bottom:8px">✅</div>
            <div style="font-weight:800;color:#bbf7d0 !important;font-size:1.2rem">{len(egzersizler)} Egzersiz Üretildi!</div>
        </div>
        """)

    # Üretilenleri interaktif göster
    if "zk_fab_sonuc" in st.session_state:
        egzersizler = st.session_state["zk_fab_sonuc"]
        styled_section(f"📋 Üretilen Egzersizler ({len(egzersizler)} adet)", "#6366f1")

        # Sayfa sistemi
        sayfa_boyut = 10
        toplam_sayfa = max(1, (len(egzersizler) + sayfa_boyut - 1) // sayfa_boyut)
        sayfa = st.selectbox("Sayfa", list(range(1, toplam_sayfa + 1)), key="zk_fab_sayfa",
                              format_func=lambda x: f"Sayfa {x}/{toplam_sayfa}")

        baslangic = (sayfa - 1) * sayfa_boyut
        bitis = min(baslangic + sayfa_boyut, len(egzersizler))

        for idx, eg in enumerate(egzersizler[baslangic:bitis], start=baslangic + 1):
            tur_ad = eg.get("tur", "bilinmiyor")
            tur_emojiler = {"oruntu": "🔍", "mantik": "🧩", "hafiza": "🎭", "gorsel": "🌍", "hayvan": "🐾"}
            emoji = tur_emojiler.get(tur_ad, "🧠")

            if "desen" in eg:
                # Örüntü sorusu
                desen = "  ".join(eg.get("desen", []))
                with st.expander(f"{emoji} #{idx} Örüntü — {eg.get('ipucu','')[:40]}", expanded=False):
                    st.markdown(f"**Desen:** {desen}")
                    st.markdown(f"**Cevap:** ||{eg.get('cevap','')}||")
                    st.caption(f"İpucu: {eg.get('ipucu','')}")
            elif "soru" in eg and "secenekler" in eg:
                # Mantık sorusu
                with st.expander(f"{emoji} #{idx} Mantık — {eg.get('tip','')}", expanded=False):
                    st.markdown(eg["soru"])
                    st.markdown(f"**Seçenekler:** {' • '.join(eg.get('secenekler',[]))}")
                    st.markdown(f"**Cevap:** ||{eg.get('cevap','')}||")
                    if eg.get("aciklama"):
                        st.caption(f"💡 {eg['aciklama']}")
            elif "tam_set" in eg:
                # Hafıza sorusu
                with st.expander(f"{emoji} #{idx} Hafıza (Seviye {eg.get('seviye',5)})", expanded=False):
                    st.markdown(f"**Set:** {'  '.join(eg['tam_set'])}")
                    st.markdown(f"**Eksik:** ||{eg.get('eksik','')}||")
            elif "grid" in eg:
                # Görsel fark bulma
                with st.expander(f"{emoji} #{idx} Fark Bul ({eg.get('boyut',5)}x{eg.get('boyut',5)})", expanded=False):
                    st.markdown(f"**Ana emoji:** {eg.get('ana','')} | **Farklı:** {eg.get('farkli','')}")
                    st.markdown(f"**Farklı pozisyonlar:** {eg.get('farkli_poz',[])}")
            elif "sahne" in eg:
                # Hayvan problemi
                with st.expander(f"{emoji} #{idx} Hayvan — {eg.get('soru','')[:40]}", expanded=False):
                    st.markdown(f"**Sahne:** {eg['sahne']}")
                    st.markdown(f"**Soru:** {eg['soru']}")
                    st.markdown(f"**Cevap:** ||{eg.get('cevap','')}|| — {eg.get('islem','')}")

        # Çözme modu
        st.markdown("---")
        styled_section("🎯 Hızlı Çözüm Modu", "#f59e0b")
        st.info("Rastgele bir egzersiz seç ve çöz!")

        if st.button("🎲 Rastgele Egzersiz!", key="zk_fab_rnd", type="primary"):
            st.session_state["zk_fab_aktif"] = _r.choice(egzersizler)

        if "zk_fab_aktif" in st.session_state:
            eg = st.session_state["zk_fab_aktif"]

            if "desen" in eg:
                desen_str = "  ".join(eg["desen"])
                _render_html(f"""
                <div style="background:#0f172a;border-radius:16px;padding:24px;text-align:center;margin:12px 0;
                             border:1px solid rgba(99,102,241,0.2)">
                    <div style="font-size:0.85rem;color:#94a3b8 !important;margin-bottom:10px">Sıradaki ne?</div>
                    <div style="font-size:2rem;letter-spacing:8px;margin-bottom:12px">{desen_str}</div>
                    <div style="font-size:2.5rem">❓</div>
                </div>
                """)
                cols = st.columns(4)
                for i, opt in enumerate(eg.get("secenekler", [])):
                    with cols[i % 4]:
                        if st.button(str(opt), key=f"zk_fab_opt_{i}", use_container_width=True):
                            if str(opt) == str(eg["cevap"]):
                                st.success(f"🎉 Doğru! {eg.get('ipucu','')}")
                                st.balloons()
                            else:
                                st.error(f"❌ Doğru cevap: {eg['cevap']}")

            elif "soru" in eg and "secenekler" in eg:
                st.markdown(f"### {eg['soru']}")
                ans = st.radio("Cevabın:", eg["secenekler"], key="zk_fab_ans", index=None)
                if ans:
                    if ans == eg["cevap"]:
                        st.success(f"🎉 Doğru! {eg.get('aciklama','')}")
                    else:
                        st.error(f"❌ Doğru cevap: {eg['cevap']} — {eg.get('aciklama','')}")

            elif "sahne" in eg:
                _render_html(f'<div style="text-align:center;font-size:2rem;margin:12px 0">{eg["sahne"]}</div>')
                st.markdown(f"**{eg['soru']}**")
                ans = st.text_input("Cevabın:", key="zk_fab_hayvan_ans")
                if ans and ans.strip() == str(eg["cevap"]):
                    st.success(f"🎉 Doğru! {eg['islem']}")
                elif ans:
                    st.error(f"❌ Doğru cevap: {eg['cevap']} — {eg['islem']}")


def _zk_iq_olcum():
    """IQ / Zeka Seviyesi Ölçüm Testi — interaktif, görsel, sonuç analizli."""
    import random as _r
    import time

    styled_section("🧪 Zeka Seviyesi Ölçüm Testi", "#8b5cf6")

    _render_html("""
    <div style="background:linear-gradient(135deg,#1e0a3a,#4c1d95,#7c3aed);border-radius:24px;padding:32px;margin-bottom:24px;
                 border:2px solid rgba(167,139,250,0.5);text-align:center;position:relative;overflow:hidden">
        <div style="position:absolute;top:0;left:0;width:100%;height:100%;
                     background:radial-gradient(circle at 30% 70%,rgba(139,92,246,0.1),transparent 60%);"></div>
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:10px" class="mat-grow">🧪🧠✨</div>
            <h2 style="color:#e9d5ff !important;font-size:1.5rem;margin:0 0 8px !important">Matematiksel Zeka Ölçüm Makinesi</h2>
            <p style="color:#c4b5fd !important;font-size:0.9rem;margin:0 !important">
                20 soruluk kapsamlı test: Mantık, Örüntü, Uzamsal, Sayısal ve Problem Çözme.<br>
                Sonunda detaylı zeka profil analizi al!
            </p>
        </div>
    </div>
    """)

    sinif = st.selectbox("Sınıf Düzeyin:", ["1-2. Sınıf", "3-4. Sınıf", "5-6. Sınıf"], key="iq_sinif", index=1)

    # Sorular havuzu — sınıf bazlı
    if "1-2" in sinif:
        sorular_havuz = [
            # Sayısal Mantık
            {"alan": "Sayısal", "emoji": "🔢", "soru": "2, 4, 6, 8, ? → Sıradaki sayı nedir?", "secenekler": ["9","10","11","12"], "cevap": "10", "puan": 5},
            {"alan": "Sayısal", "emoji": "🔢", "soru": "5 + ? = 12", "secenekler": ["6","7","8","9"], "cevap": "7", "puan": 5},
            {"alan": "Sayısal", "emoji": "🔢", "soru": "🍎🍎🍎 + 🍎🍎 = kaç elma?", "secenekler": ["4","5","6","7"], "cevap": "5", "puan": 5},
            {"alan": "Sayısal", "emoji": "🔢", "soru": "10'dan geriye sayınca 10,9,8,7,?,5 — ? kaçtır?", "secenekler": ["4","6","3","8"], "cevap": "6", "puan": 5},
            # Örüntü
            {"alan": "Örüntü", "emoji": "🔍", "soru": "🔴🔵🔴🔵🔴 → Sıradaki?", "secenekler": ["🔴","🔵","🟡","🟢"], "cevap": "🔵", "puan": 5},
            {"alan": "Örüntü", "emoji": "🔍", "soru": "⬛⬜⬛⬜⬛⬜ → Sıradaki?", "secenekler": ["⬛","⬜","🟥","🟦"], "cevap": "⬛", "puan": 5},
            {"alan": "Örüntü", "emoji": "🔍", "soru": "🌸🌸🌻🌸🌸🌻🌸🌸 → Sıradaki?", "secenekler": ["🌸","🌻","🌹","🌺"], "cevap": "🌻", "puan": 6},
            # Uzamsal
            {"alan": "Uzamsal", "emoji": "📐", "soru": "Üçgenin kaç köşesi vardır?", "secenekler": ["2","3","4","5"], "cevap": "3", "puan": 4},
            {"alan": "Uzamsal", "emoji": "📐", "soru": "Karenin tüm kenarları eşit mi?", "secenekler": ["Evet","Hayır","Bazen","2'si eşit"], "cevap": "Evet", "puan": 4},
            {"alan": "Uzamsal", "emoji": "📐", "soru": "🔺 döndürülürse hangisi olur?", "secenekler": ["🔻","⬜","⬡","⭕"], "cevap": "🔻", "puan": 5},
            # Mantık
            {"alan": "Mantık", "emoji": "🧩", "soru": "Ali Berk'ten büyük, Berk Cem'den büyük. En küçük kim?", "secenekler": ["Ali","Berk","Cem","Bilinmez"], "cevap": "Cem", "puan": 6},
            {"alan": "Mantık", "emoji": "🧩", "soru": "Bütün kediler hayvandır. Pamuk bir kedi. Pamuk hayvan mıdır?", "secenekler": ["Evet","Hayır","Belki","Bilinmez"], "cevap": "Evet", "puan": 5},
            {"alan": "Mantık", "emoji": "🧩", "soru": "🐶 > 🐱 > 🐭 ise en ağır hangisi?", "secenekler": ["🐱","🐶","🐭","Hepsi eşit"], "cevap": "🐶", "puan": 5},
            # Problem Çözme
            {"alan": "Problem", "emoji": "💡", "soru": "Sepette 8 elma var. 3 yedim, 2 aldım. Kaç elma var?", "secenekler": ["5","7","3","10"], "cevap": "7", "puan": 6},
            {"alan": "Problem", "emoji": "💡", "soru": "3 çocuk 6 kurabiyeyi eşit paylaşırsa kişi başı kaç?", "secenekler": ["1","2","3","4"], "cevap": "2", "puan": 5},
            {"alan": "Problem", "emoji": "💡", "soru": "Saat 3'ü gösteriyorsa akrep nereyi gösterir?", "secenekler": ["12","3","6","9"], "cevap": "3", "puan": 5},
            {"alan": "Problem", "emoji": "💡", "soru": "Yarın Çarşamba ise dün hangi gündü?", "secenekler": ["Pazartesi","Salı","Perşembe","Cuma"], "cevap": "Pazartesi", "puan": 6},
            # Hafıza & Dikkat
            {"alan": "Dikkat", "emoji": "👁️", "soru": "🐶🐱🐭🐹🐰 — 5 hayvan var. 3. sıradaki hangisi?", "secenekler": ["🐶","🐱","🐭","🐹"], "cevap": "🐭", "puan": 5},
            {"alan": "Dikkat", "emoji": "👁️", "soru": "🟢🟢🟢🔴🟢🟢🟢🟢🟢 — Kırmızı kaçıncı sırada?", "secenekler": ["3","4","5","6"], "cevap": "4", "puan": 5},
            {"alan": "Dikkat", "emoji": "👁️", "soru": "🌟🌟🌟🌟🌟🌟🌟 — Kaç yıldız var?", "secenekler": ["5","6","7","8"], "cevap": "7", "puan": 4},
        ]
    elif "3-4" in sinif:
        sorular_havuz = [
            {"alan": "Sayısal", "emoji": "🔢", "soru": "3, 6, 12, 24, ? → Sıradaki?", "secenekler": ["36","48","30","42"], "cevap": "48", "puan": 6},
            {"alan": "Sayısal", "emoji": "🔢", "soru": "1, 4, 9, 16, 25, ? → Sıradaki?", "secenekler": ["30","36","49","35"], "cevap": "36", "puan": 7},
            {"alan": "Sayısal", "emoji": "🔢", "soru": "? × 7 = 56", "secenekler": ["7","8","9","6"], "cevap": "8", "puan": 5},
            {"alan": "Sayısal", "emoji": "🔢", "soru": "144 ÷ 12 = ?", "secenekler": ["10","11","12","14"], "cevap": "12", "puan": 5},
            {"alan": "Örüntü", "emoji": "🔍", "soru": "🔺🔻🔺🔺🔻🔻🔺🔺🔺 → Sıradaki?", "secenekler": ["🔻🔻🔻","🔺","🔻🔻","🔺🔺"], "cevap": "🔻🔻🔻", "puan": 7},
            {"alan": "Örüntü", "emoji": "🔍", "soru": "A=1, B=2, C=3... ise F=?", "secenekler": ["4","5","6","7"], "cevap": "6", "puan": 5},
            {"alan": "Örüntü", "emoji": "🔍", "soru": "2,3,5,7,11,? → Sıradaki asal sayı?", "secenekler": ["12","13","14","15"], "cevap": "13", "puan": 7},
            {"alan": "Uzamsal", "emoji": "📐", "soru": "Küpün kaç yüzeyi vardır?", "secenekler": ["4","6","8","12"], "cevap": "6", "puan": 5},
            {"alan": "Uzamsal", "emoji": "📐", "soru": "Bir dikdörtgenin çevresi 20 cm, kısa kenarı 3 cm. Uzun kenar?", "secenekler": ["5","7","10","14"], "cevap": "7", "puan": 6},
            {"alan": "Uzamsal", "emoji": "📐", "soru": "Aynada 'AMBULANCE' nasıl görünür?", "secenekler": ["Ters yazılı","Normal","Ters dönmüş","Baş aşağı"], "cevap": "Ters yazılı", "puan": 6},
            {"alan": "Mantık", "emoji": "🧩", "soru": "Tüm balıklar suda yaşar. Yunus suda yaşar. Yunus balık mıdır?", "secenekler": ["Evet","Hayır","Kesin evet","Kesinlikle belirlenemez"], "cevap": "Kesinlikle belirlenemez", "puan": 8},
            {"alan": "Mantık", "emoji": "🧩", "soru": "5 kedi 5 fareyi 5 dakikada yakalar. 100 kedi 100 fareyi kaç dakikada yakalar?", "secenekler": ["100","5","20","50"], "cevap": "5", "puan": 8},
            {"alan": "Mantık", "emoji": "🧩", "soru": "Bir çiftçinin 17 koyunu var. 9'u hariç hepsi öldü. Kaç koyun kaldı?", "secenekler": ["8","9","0","17"], "cevap": "9", "puan": 7},
            {"alan": "Problem", "emoji": "💡", "soru": "Saat 3:15'te akrep ile yelkovan arasındaki açı nedir?", "secenekler": ["0°","7.5°","90°","45°"], "cevap": "7.5°", "puan": 8},
            {"alan": "Problem", "emoji": "💡", "soru": "Bir tavuk 1.5 günde 1.5 yumurta bırakır. 9 tavuk 9 günde kaç yumurta bırakır?", "secenekler": ["9","27","54","81"], "cevap": "54", "puan": 8},
            {"alan": "Problem", "emoji": "💡", "soru": "0'dan 100'e kadar kaç tane 9 rakamı kullanılır?", "secenekler": ["10","11","19","20"], "cevap": "20", "puan": 8},
            {"alan": "Problem", "emoji": "💡", "soru": "3 arkadaş 30 TL'lik hesabı eşit ödedi. Garson 5 TL iade etti ama 2 TL kendine aldı. Kişi başı 9 TL ödendi (27 TL). 2 TL garsonda. 27+2=29. 1 TL nerede?", "secenekler": ["Soru yanlış kurulmuş","Garsonda","Masada","Kasada"], "cevap": "Soru yanlış kurulmuş", "puan": 9},
            {"alan": "Dikkat", "emoji": "👁️", "soru": "🟥🟧🟨🟩🟦🟪 — Renkleri tersten say: 3. renk hangisi?", "secenekler": ["🟩","🟨","🟧","🟦"], "cevap": "🟩", "puan": 6},
            {"alan": "Dikkat", "emoji": "👁️", "soru": "ABCDEFGHIJ — 4. ve 7. harfler hangileri?", "secenekler": ["C ve F","D ve G","D ve H","E ve G"], "cevap": "D ve G", "puan": 5},
            {"alan": "Dikkat", "emoji": "👁️", "soru": "1234567890 sayısında rakamların toplamı?", "secenekler": ["45","50","55","40"], "cevap": "45", "puan": 6},
        ]
    else:
        sorular_havuz = [
            {"alan": "Sayısal", "emoji": "🔢", "soru": "1,1,2,3,5,8,13,21,? → Fibonacci sıradaki?", "secenekler": ["28","34","32","29"], "cevap": "34", "puan": 6},
            {"alan": "Sayısal", "emoji": "🔢", "soru": "2⁰ + 2¹ + 2² + 2³ = ?", "secenekler": ["15","16","14","12"], "cevap": "15", "puan": 6},
            {"alan": "Sayısal", "emoji": "🔢", "soru": "√144 + √81 = ?", "secenekler": ["21","20","23","19"], "cevap": "21", "puan": 6},
            {"alan": "Sayısal", "emoji": "🔢", "soru": "0.125 hangi kesre eşittir?", "secenekler": ["1/4","1/8","1/5","1/10"], "cevap": "1/8", "puan": 6},
            {"alan": "Örüntü", "emoji": "🔍", "soru": "1,4,9,16,25,36,49,? — Sıradaki tam kare?", "secenekler": ["56","64","72","81"], "cevap": "64", "puan": 6},
            {"alan": "Örüntü", "emoji": "🔍", "soru": "Her terim öncekinin 3 katı -1: 2,5,14,41,? ", "secenekler": ["122","123","124","120"], "cevap": "122", "puan": 8},
            {"alan": "Örüntü", "emoji": "🔍", "soru": "🔴:1, 🟡:2, 🟢:3 ise 🔴🟢🟡🔴 = ?", "secenekler": ["1321","7","4231","1+3+2+1"], "cevap": "7", "puan": 7},
            {"alan": "Uzamsal", "emoji": "📐", "soru": "Bir küpü köşeden köşeye kesen düzlem ne şekil oluşturur?", "secenekler": ["Üçgen","Kare","Altıgen","Daire"], "cevap": "Altıgen", "puan": 9},
            {"alan": "Uzamsal", "emoji": "📐", "soru": "İkizkenar üçgende taban açıları 70° ise tepe açısı?", "secenekler": ["40°","50°","70°","80°"], "cevap": "40°", "puan": 6},
            {"alan": "Uzamsal", "emoji": "📐", "soru": "Silindirin açınımında kaç farklı şekil vardır?", "secenekler": ["2 (daire+dikdörtgen)","3","1","4"], "cevap": "2 (daire+dikdörtgen)", "puan": 7},
            {"alan": "Mantık", "emoji": "🧩", "soru": "A ise B'dir. B ise C'dir. O halde kesinlikle ne söylenebilir?", "secenekler": ["C ise A'dır","A ise C'dir","C ise B'dir","B ise A'dır"], "cevap": "A ise C'dir", "puan": 7},
            {"alan": "Mantık", "emoji": "🧩", "soru": "100 kapılı bir koridorda 1. kişi hepsini açar, 2. kişi 2'nin katlarını kapar, 3. kişi 3'ün katlarını değiştirir... 100. kişiden sonra kaç kapı açıktır?", "secenekler": ["10","50","25","12"], "cevap": "10", "puan": 10},
            {"alan": "Mantık", "emoji": "🧩", "soru": "Bir adada herkes doğrucu veya yalancı. Biri diyor: 'Ben yalancıyım.' Bu kişi kimdir?", "secenekler": ["Yalancı","Doğrucu","İkisi de olamaz","Belirsiz"], "cevap": "İkisi de olamaz", "puan": 9},
            {"alan": "Problem", "emoji": "💡", "soru": "3 kova: 8L, 5L, 3L. 8L dolu. Tam 4L ölçmek mümkün mü?", "secenekler": ["Evet","Hayır","8L ile olmaz","Sadece tahmin"], "cevap": "Evet", "puan": 8},
            {"alan": "Problem", "emoji": "💡", "soru": "Bir salyangoz 3m tırmanıp 2m kayıyor. 10m duvara kaç günde çıkar?", "secenekler": ["10","8","9","7"], "cevap": "8", "puan": 8},
            {"alan": "Problem", "emoji": "💡", "soru": "64 takımlı eleme turnuvasında şampiyon belirlemek için kaç maç oynanır?", "secenekler": ["32","63","64","128"], "cevap": "63", "puan": 7},
            {"alan": "Problem", "emoji": "💡", "soru": "1'den 1000'e kadar kaç kez 1 rakamı yazılır?", "secenekler": ["300","301","299","310"], "cevap": "301", "puan": 9},
            {"alan": "Dikkat", "emoji": "👁️", "soru": "111111111 × 111111111 sonucundaki en büyük rakam?", "secenekler": ["8","9","1","7"], "cevap": "9", "puan": 7},
            {"alan": "Dikkat", "emoji": "👁️", "soru": "Bu cümledeki harfleri say: 'ON İKİ' kaç harftir?", "secenekler": ["4","5","6","7"], "cevap": "5", "puan": 5},
            {"alan": "Dikkat", "emoji": "👁️", "soru": "🔴🔵🟡🔴🔵🟡🔴🔵🟡🔴🔵🟡 — 10. emoji hangisi?", "secenekler": ["🔴","🔵","🟡","🟢"], "cevap": "🔴", "puan": 6},
        ]

    # Test state
    iq_key = "zk_iq_state"

    if iq_key not in st.session_state:
        st.session_state[iq_key] = {"started": False, "answers": {}, "submitted": False}

    state = st.session_state[iq_key]

    if not state["started"]:
        _render_html("""
        <div style="text-align:center;margin:20px 0">
            <div style="font-size:5rem;margin-bottom:16px" class="mat-grow">🧪</div>
            <div style="color:#c4b5fd !important;font-size:0.95rem;max-width:500px;display:inline-block;line-height:1.7">
                <b>20 soru</b> • <b>5 zeka alanı</b> • Sonunda detaylı analiz<br>
                Alanlar: 🔢 Sayısal • 🔍 Örüntü • 📐 Uzamsal • 🧩 Mantık • 💡 Problem Çözme • 👁️ Dikkat
            </div>
        </div>
        """)

        if st.button("🚀 Testi Başlat!", key="iq_start", type="primary"):
            _r.shuffle(sorular_havuz)
            st.session_state[iq_key] = {
                "started": True,
                "sorular": sorular_havuz[:20],
                "answers": {},
                "submitted": False,
                "start_time": time.time(),
            }
            st.rerun()

    elif not state.get("submitted"):
        sorular = state["sorular"]
        st.progress(len(state["answers"]) / len(sorular), text=f"İlerleme: {len(state['answers'])}/{len(sorular)}")

        for idx, s in enumerate(sorular):
            _render_html(f"""
            <div class="zk-card" style="border-left:4px solid {'#10b981' if idx in [int(k) for k in state['answers']] else '#4f46e5'}">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
                    <span style="font-size:1.3rem">{s['emoji']}</span>
                    <span style="font-weight:700;color:#a78bfa !important;font-size:0.8rem">{s['alan']}</span>
                    <span style="color:#94a3b8 !important;font-size:0.75rem">Soru {idx+1}/20 • {s['puan']} puan</span>
                </div>
                <div style="font-weight:600;color:#e0e7ff !important;font-size:0.95rem">{s['soru']}</div>
            </div>
            """)
            ans = st.radio("", s["secenekler"], key=f"iq_q_{idx}", index=None,
                           label_visibility="collapsed", horizontal=True)
            if ans:
                state["answers"][str(idx)] = ans

        if len(state["answers"]) >= 15:
            if st.button("📊 Testi Bitir & Sonuçları Gör!", key="iq_submit", type="primary"):
                state["submitted"] = True
                state["end_time"] = time.time()
                st.rerun()
        else:
            st.info(f"⏳ En az 15 soruyu cevaplamalısın ({len(state['answers'])}/15)")

    else:
        # SONUÇLAR
        sorular = state["sorular"]
        answers = state["answers"]
        elapsed = round(state.get("end_time", time.time()) - state.get("start_time", time.time()), 0)

        # Hesapla
        toplam_puan = 0
        max_puan = 0
        alan_skor = {}
        for idx, s in enumerate(sorular):
            max_puan += s["puan"]
            alan = s["alan"]
            if alan not in alan_skor:
                alan_skor[alan] = {"dogru": 0, "toplam": 0, "puan": 0, "max": 0}
            alan_skor[alan]["toplam"] += 1
            alan_skor[alan]["max"] += s["puan"]

            user_ans = answers.get(str(idx))
            if user_ans and user_ans == s["cevap"]:
                toplam_puan += s["puan"]
                alan_skor[alan]["dogru"] += 1
                alan_skor[alan]["puan"] += s["puan"]

        oran = (toplam_puan / max_puan * 100) if max_puan > 0 else 0

        # IQ eşdeğeri hesapla (basitleştirilmiş — gerçek IQ testleri normatif)
        if oran >= 95:
            iq = 145
            seviye = "Olağanüstü Üstün Zeka"
            emoji_sev = "🏆💎"
            renk = "#eab308"
        elif oran >= 85:
            iq = 130
            seviye = "Üstün Zeka"
            emoji_sev = "🌟🧠"
            renk = "#8b5cf6"
        elif oran >= 70:
            iq = 115
            seviye = "Ortanın Üstü"
            emoji_sev = "⭐📈"
            renk = "#3b82f6"
        elif oran >= 50:
            iq = 100
            seviye = "Ortalama"
            emoji_sev = "👍🎯"
            renk = "#10b981"
        elif oran >= 30:
            iq = 90
            seviye = "Ortanın Altı — Gelişim Alanı"
            emoji_sev = "💪🌱"
            renk = "#f59e0b"
        else:
            iq = 80
            seviye = "Pratik Gerekli"
            emoji_sev = "🌱📚"
            renk = "#94a3b8"

        # Sonuç kartı
        _render_html(f"""
        <div style="background:linear-gradient(135deg,#1e0a3a,#4c1d95);border-radius:28px;padding:36px;margin-bottom:24px;
                     border:2px solid {renk}60;text-align:center;position:relative;overflow:hidden">
            <div style="position:absolute;top:0;left:0;width:100%;height:100%;
                         background:radial-gradient(circle at 50% 50%,{renk}08,transparent 70%)"></div>
            <div style="position:relative;z-index:1">
                <div style="font-size:3rem;margin-bottom:8px">{emoji_sev}</div>
                <div style="font-size:2.5rem;font-weight:900;color:{renk} !important;margin-bottom:4px">IQ ≈ {iq}</div>
                <div style="font-size:1.2rem;font-weight:700;color:#e9d5ff !important;margin-bottom:16px">{seviye}</div>
                <div style="display:flex;justify-content:center;gap:36px;flex-wrap:wrap">
                    <div>
                        <div style="font-size:2rem;font-weight:800;color:#818cf8 !important">{toplam_puan}/{max_puan}</div>
                        <div style="font-size:0.75rem;color:#94a3b8 !important">Puan</div>
                    </div>
                    <div>
                        <div style="font-size:2rem;font-weight:800;color:#10b981 !important">%{oran:.0f}</div>
                        <div style="font-size:0.75rem;color:#94a3b8 !important">Başarı</div>
                    </div>
                    <div>
                        <div style="font-size:2rem;font-weight:800;color:#f59e0b !important">{int(elapsed)}s</div>
                        <div style="font-size:0.75rem;color:#94a3b8 !important">Süre</div>
                    </div>
                    <div>
                        <div style="font-size:2rem;font-weight:800;color:#ec4899 !important">{len(answers)}/20</div>
                        <div style="font-size:0.75rem;color:#94a3b8 !important">Cevaplanan</div>
                    </div>
                </div>
            </div>
        </div>
        """)

        # Alan bazlı analiz
        styled_section("📊 Zeka Alanları Analizi", "#6366f1")

        alan_emojileri = {"Sayısal": "🔢", "Örüntü": "🔍", "Uzamsal": "📐",
                          "Mantık": "🧩", "Problem": "💡", "Dikkat": "👁️"}

        for alan, data in alan_skor.items():
            alan_oran = (data["puan"] / data["max"] * 100) if data["max"] > 0 else 0
            bar_renk = "#10b981" if alan_oran >= 70 else "#f59e0b" if alan_oran >= 40 else "#ef4444"
            emoji_a = alan_emojileri.get(alan, "📊")

            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:14px 18px;margin-bottom:8px;
                         border:1px solid rgba(99,102,241,0.1)">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                    <span style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{emoji_a} {alan}</span>
                    <span style="font-weight:700;color:{bar_renk} !important;font-size:0.9rem">{data['dogru']}/{data['toplam']} doğru • %{alan_oran:.0f}</span>
                </div>
                <div style="background:#1e1b4b;border-radius:8px;height:10px;overflow:hidden">
                    <div style="width:{alan_oran:.0f}%;height:100%;background:linear-gradient(90deg,{bar_renk},{bar_renk}aa);border-radius:8px;transition:width 0.8s"></div>
                </div>
            </div>
            """)

        # Güçlü ve zayıf alanlar
        en_guclu = max(alan_skor.items(), key=lambda x: (x[1]["puan"]/x[1]["max"]*100) if x[1]["max"]>0 else 0)
        en_zayif = min(alan_skor.items(), key=lambda x: (x[1]["puan"]/x[1]["max"]*100) if x[1]["max"]>0 else 0)

        col1, col2 = st.columns(2)
        with col1:
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#052e16,#065f46);border-radius:16px;padding:18px;
                         border:2px solid rgba(16,185,129,0.3);text-align:center">
                <div style="font-size:1.5rem;margin-bottom:6px">💪</div>
                <div style="font-weight:700;color:#bbf7d0 !important;font-size:0.9rem">En Güçlü Alanın</div>
                <div style="font-size:1.3rem;font-weight:800;color:#10b981 !important">{alan_emojileri.get(en_guclu[0],'')} {en_guclu[0]}</div>
            </div>
            """)
        with col2:
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#451a03,#78350f);border-radius:16px;padding:18px;
                         border:2px solid rgba(245,158,11,0.3);text-align:center">
                <div style="font-size:1.5rem;margin-bottom:6px">🎯</div>
                <div style="font-weight:700;color:#fde68a !important;font-size:0.9rem">Gelişim Alanın</div>
                <div style="font-size:1.3rem;font-weight:800;color:#f59e0b !important">{alan_emojileri.get(en_zayif[0],'')} {en_zayif[0]}</div>
            </div>
            """)

        # Tekrar test
        if st.button("🔄 Testi Sıfırla & Tekrar Çöz", key="iq_reset"):
            del st.session_state[iq_key]
            st.rerun()


def _zk_oruntu_dedektifi():
    """Görsel örüntü tanıma — sınırsız üretim modunda."""
    styled_section("🔍 Örüntü Dedektifi", "#6366f1")

    zorluk = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="zk_ort_z",
                           format_func=lambda x: {"kolay":"🌱 Kolay","orta":"🌿 Orta","zor":"🌳 Zor"}[x])

    ort_key = "zk_ort_state"
    if ort_key not in st.session_state:
        st.session_state[ort_key] = {"skor": 0, "toplam": 0}

    if st.button("🔍 Yeni Örüntü Üret!", key="zk_ort_new", type="primary"):
        sorular = ZekaEgzersizGenerator.oruntu_uret(zorluk, 1)
        if sorular:
            st.session_state["zk_ort_soru"] = sorular[0]

    if "zk_ort_soru" in st.session_state:
        s = st.session_state["zk_ort_soru"]
        desen_str = "  ".join(s.get("desen", []))

        _render_html(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:20px;padding:28px;
                     margin:16px 0;text-align:center;border:2px solid rgba(99,102,241,0.25)">
            <div style="font-size:0.85rem;color:#94a3b8 !important;margin-bottom:12px">Sıradaki ne olmalı?</div>
            <div style="font-size:2.2rem;letter-spacing:8px;margin-bottom:16px;line-height:1.8">{desen_str}</div>
            <div style="font-size:3rem;color:#f59e0b !important">❓</div>
        </div>
        """)

        with st.expander("💡 İpucu"):
            st.info(s.get("ipucu", ""))

        secenekler = s.get("secenekler", [])
        cols = st.columns(max(len(secenekler), 1))
        for idx, opt in enumerate(secenekler):
            with cols[idx]:
                if st.button(str(opt), key=f"zk_ort_opt_{idx}", use_container_width=True):
                    st.session_state[ort_key]["toplam"] += 1
                    if str(opt) == str(s.get("cevap", "")):
                        st.session_state[ort_key]["skor"] += 1
                        st.success(f"🎉 Doğru!")
                        st.balloons()
                    else:
                        st.error(f"❌ Doğru cevap: {s.get('cevap','')}")

    skor = st.session_state[ort_key]
    if skor["toplam"] > 0:
        _render_html(f"""
        <div style="text-align:center;margin-top:12px">
            <span style="color:#a78bfa !important;font-weight:700;font-size:1.1rem">
                🏆 Skor: {skor['skor']}/{skor['toplam']}
            </span>
        </div>
        """)


# ── 12b) Mantık Labirenti ────────────────────────────────────────────────────

def _zk_mantik_labirenti():
    """Mantıksal düşünme — sınırsız üretim modunda."""
    styled_section("🧩 Mantık Labirenti", "#10b981")

    zorluk = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="zk_ml_z",
                           format_func=lambda x: {"kolay":"🌱 Kolay","orta":"🌿 Orta","zor":"🌳 Zor"}[x])

    ml_key = "zk_ml_state"
    if ml_key not in st.session_state:
        st.session_state[ml_key] = {"skor": 0, "toplam": 0}

    if st.button("🧩 Yeni Mantık Sorusu Üret!", key="zk_ml_new", type="primary"):
        sorular = ZekaEgzersizGenerator.mantik_uret(zorluk, 1)
        if sorular:
            st.session_state["zk_ml_soru"] = sorular[0]

    if "zk_ml_soru" in st.session_state:
        s = st.session_state["zk_ml_soru"]
        st.markdown(f"### {s.get('soru','')}")

        secenekler = s.get("secenekler", [])
        ans = st.radio("Cevabın:", secenekler, key="zk_ml_ans", index=None)
        if ans is not None:
            st.session_state[ml_key]["toplam"] += 1
            if ans == s.get("cevap"):
                st.session_state[ml_key]["skor"] += 1
                st.success(f"🎉 Doğru! {s.get('aciklama','')}")
            else:
                st.error(f"❌ Doğru cevap: {s.get('cevap','')} — {s.get('aciklama','')}")

    skor = st.session_state[ml_key]
    if skor["toplam"] > 0:
        st.markdown(f"**🏆 Skor:** {skor['skor']}/{skor['toplam']}")


# ── 12c) Hafıza Sarayı ──────────────────────────────────────────────────────

def _zk_hafiza_sarayi():
    """Hafıza geliştirme — emoji ezberleme, sıra hatırlama."""
    import random as _r
    styled_section("🎭 Hafıza Sarayı", "#f59e0b")

    _render_html("""
    <div class="zk-card" style="text-align:center;border-color:rgba(245,158,11,0.3)">
        <div style="font-size:2rem;margin-bottom:8px" class="mat-grow">🏰</div>
        <div style="font-weight:700;color:#fde68a !important;font-size:1rem">Hafızanı Güçlendir!</div>
        <div style="color:#fcd34d !important;font-size:0.85rem">Emojileri ezberle, sonra tekrarla. Her seviyede zorluk artar!</div>
    </div>
    """)

    col1, col2 = st.columns(2)
    with col1:
        seviye = st.selectbox("Seviye", [3, 4, 5, 6, 7, 8], key="zk_hf_sev",
                               format_func=lambda x: f"{'🌱' if x<=4 else '🌿' if x<=6 else '🌳'} {x} emoji")
    with col2:
        sure = st.selectbox("Ezberleme Süresi", [3, 5, 8, 10], key="zk_hf_sure",
                             format_func=lambda x: f"{x} saniye")

    emoji_havuz = ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐸","🐵",
                   "🦁","🐯","🐮","🐷","🐔","🐧","🦋","🐝","🐞","🐙",
                   "🌸","🌻","🌹","🍎","🍊","🍋","🍇","🍓","⭐","🌙",
                   "❤️","💎","🎈","🎯","🚀","⚡","🔥","🌈","🎵","🏀"]

    hf_key = "zk_hf_state"

    if st.button("🧠 Yeni Ezber Başlat!", key="zk_hf_start", type="primary"):
        secilen = _r.sample(emoji_havuz, seviye)
        st.session_state[hf_key] = {
            "emojiler": secilen,
            "goster": True,
            "cevap_bekle": False,
        }

    if hf_key in st.session_state:
        state = st.session_state[hf_key]

        if state.get("goster"):
            emojiler = state["emojiler"]
            emoji_str = "  ".join(emojiler)
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#451a03,#78350f);border-radius:20px;padding:32px;
                         margin:16px 0;text-align:center;border:2px solid rgba(245,158,11,0.4)">
                <div style="font-size:0.9rem;color:#fde68a !important;margin-bottom:12px">🧠 EZBERLE! ({sure} saniye)</div>
                <div style="font-size:2.8rem;letter-spacing:12px;line-height:1.6">{emoji_str}</div>
            </div>
            """)

            if st.button("👁️ Ezberledim! Gizle!", key="zk_hf_hide"):
                st.session_state[hf_key]["goster"] = False
                st.session_state[hf_key]["cevap_bekle"] = True
                st.rerun()

        elif state.get("cevap_bekle"):
            _render_html("""
            <div style="background:linear-gradient(135deg,#1a0a2e,#2d1b69);border-radius:20px;padding:32px;
                         margin:16px 0;text-align:center;border:2px solid rgba(139,92,246,0.3)">
                <div style="font-size:3rem;margin-bottom:12px" class="mat-wiggle">🤔</div>
                <div style="font-size:1.2rem;color:#e9d5ff !important;font-weight:700">Hangi emojileri gördün?</div>
                <div style="font-size:0.85rem;color:#94a3b8 !important;margin-top:6px">Aşağıdan doğru olanları seç!</div>
            </div>
            """)

            # 2 kat emoji göster (yarısı doğru, yarısı yanlış)
            dogru_set = set(state["emojiler"])
            yanlislar = [e for e in emoji_havuz if e not in dogru_set]
            gosterilecek = list(dogru_set) + _r.sample(yanlislar, min(len(yanlislar), seviye))
            _r.shuffle(gosterilecek)

            secimler = st.multiselect("Gördüğün emojileri seç:", gosterilecek,
                                       key="zk_hf_secim",
                                       format_func=lambda x: f"{x}")

            if st.button("✅ Kontrol Et!", key="zk_hf_kontrol"):
                secim_set = set(secimler)
                dogru_bilinen = secim_set & dogru_set
                yanlis_secilen = secim_set - dogru_set
                kacirilan = dogru_set - secim_set

                skor = len(dogru_bilinen) - len(yanlis_secilen)
                maks = len(dogru_set)

                if skor == maks and len(yanlis_secilen) == 0:
                    st.success(f"🎉 MÜKEMMEL! {maks}/{maks} doğru — Hafızan süper! ⭐⭐⭐")
                    st.balloons()
                elif skor > 0:
                    st.warning(f"👏 {len(dogru_bilinen)}/{maks} doğru hatırladın!")
                else:
                    st.info(f"🌱 {len(dogru_bilinen)}/{maks} doğru. Tekrar dene!")

                dogruler = "  ".join(state["emojiler"])
                st.markdown(f"**Doğru sıra:** {dogruler}")


# ── 12d) Görsel Zeka ────────────────────────────────────────────────────────

def _zk_gorsel_zeka():
    """Görsel-uzamsal zeka — sınırsız üretim modunda."""
    styled_section("🌍 Görsel Zeka Atölyesi", "#06b6d4")

    boyut = st.selectbox("Grid Boyutu", [4, 5, 6, 7], key="zk_gz_boy",
                          format_func=lambda x: f"{x}×{x} ({'Kolay' if x<=4 else 'Orta' if x<=5 else 'Zor' if x<=6 else 'Uzman'})")

    gz_key = "zk_gz_state"
    if gz_key not in st.session_state:
        st.session_state[gz_key] = {"skor": 0, "toplam": 0}

    # Fark bulma
    styled_section("🔎 Farklı Olanı Bul!", "#3b82f6")

    if st.button("🔎 Yeni Fark Bul Sorusu Üret!", key="zk_fark_new", type="primary"):
        sorular = ZekaEgzersizGenerator.gorsel_fark_uret(boyut, 1)
        if sorular:
            st.session_state["zk_fark"] = sorular[0]

    if "zk_fark" in st.session_state:
        soru = st.session_state["zk_fark"]
        grid = soru.get("grid", [])
        b = soru.get("boyut", 3)
        farkli_poz = soru.get("farkli_poz", [])

        for row in range(b):
            cols = st.columns(b)
            for col_idx, col in enumerate(cols):
                idx = row * b + col_idx
                if idx < len(grid):
                    with col:
                        bulundu = idx in st.session_state.get("zk_fark_bulunan", [])
                        btn_type = "primary" if bulundu else "secondary"
                        if st.button(grid[idx], key=f"zk_fark_c_{idx}", use_container_width=True, type=btn_type):
                            if idx in farkli_poz:
                                bulunan = st.session_state.get("zk_fark_bulunan", [])
                                if idx not in bulunan:
                                    bulunan.append(idx)
                                    st.session_state["zk_fark_bulunan"] = bulunan
                                    if len(bulunan) >= soru.get("farkli_adet", 1):
                                        st.session_state[gz_key]["skor"] += 1
                                        st.session_state[gz_key]["toplam"] += 1
                                        st.success("🎉 Hepsini buldun!")
                                        st.balloons()
                                    else:
                                        st.success(f"✅ ({len(bulunan)}/{soru.get('farkli_adet',1)})")
                                    st.rerun()
                            else:
                                st.session_state[gz_key]["toplam"] += 1
                                st.error("❌ Bu farklı değil!")

    st.markdown("---")

    # Sayma
    styled_section("🔢 Kaç Tane Var?", "#f59e0b")

    if st.button("🎲 Yeni Sayma Sorusu Üret!", key="zk_say_new", type="primary"):
        import random as _r
        emoji = _r.choice(["🐝","🦋","⭐","🌸","🐟","🎈","🐞","🌻","💎","🦊"])
        karistirici = _r.choice(["🌿","☁️","💧","🍃","🪨","🌊","🍂","❄️"])
        asil = _r.randint(3, 15)
        sahte = _r.randint(2, 10)
        tum = [emoji]*asil + [karistirici]*sahte
        _r.shuffle(tum)
        st.session_state["zk_say"] = {"emoji": emoji, "kar": karistirici, "adet": asil, "grid": tum}

    if "zk_say" in st.session_state:
        s = st.session_state["zk_say"]
        grid_str = "  ".join(s.get("grid", []))
        _render_html(f"""
        <div style="background:#0f172a;border-radius:16px;padding:20px;text-align:center;
                     border:1px solid rgba(245,158,11,0.2);margin:12px 0">
            <div style="font-size:0.85rem;color:#fde68a !important;margin-bottom:10px">Kaç tane {s.get('emoji','')} var?</div>
            <div style="font-size:2rem;line-height:2;letter-spacing:6px">{grid_str}</div>
        </div>
        """)
        cevap = st.number_input(f"Kaç {s.get('emoji','')}?", 0, 30, 0, key="zk_say_ans")
        if st.button("✅ Kontrol", key="zk_say_chk"):
            if int(cevap) == s.get("adet", 0):
                st.success(f"🎉 Doğru! {s.get('adet',0)} tane!")
                st.balloons()
            else:
                st.error(f"❌ {s.get('adet',0)} tane var!")

    skor = st.session_state[gz_key]
    if skor["toplam"] > 0:
        st.markdown(f"**🏆 Skor:** {skor['skor']}/{skor['toplam']}")


# ── 12e) Hayvan Matematiği ───────────────────────────────────────────────────

def _zk_hayvan_matemat():
    """Hayvan figürleri ile matematik — sınırsız üretim modunda."""
    styled_section("🐾 Hayvan Matematiği", "#f97316")

    zorluk = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="zk_hm_z",
                           format_func=lambda x: {"kolay":"🌱 Kolay","orta":"🌿 Orta","zor":"🌳 Zor"}[x])

    hm_key = "zk_hm_state"
    if hm_key not in st.session_state:
        st.session_state[hm_key] = {"skor": 0, "toplam": 0}

    if st.button("🐾 Yeni Hayvan Problemi Üret!", key="zk_hm_new", type="primary"):
        sorular = ZekaEgzersizGenerator.hayvan_problem_uret(zorluk, 1)
        if sorular:
            st.session_state["zk_hm_soru"] = sorular[0]

    if "zk_hm_soru" in st.session_state:
        s = st.session_state["zk_hm_soru"]
        _render_html(f"""
        <div style="background:#0f172a;border-radius:20px;padding:24px;text-align:center;margin:12px 0;
                     border:2px solid rgba(249,115,22,0.3)">
            <div style="font-size:2rem;line-height:1.8;margin-bottom:12px">{s.get('sahne','')}</div>
        </div>
        """)
        st.markdown(f"**{s.get('soru','')}**")

        ans = st.text_input("Cevabın:", key="zk_hm_ans")
        if ans:
            st.session_state[hm_key]["toplam"] += 1
            if ans.strip() == str(s.get("cevap", "")):
                st.session_state[hm_key]["skor"] += 1
                st.success(f"🎉 Doğru! {s.get('islem','')}")
            else:
                st.error(f"❌ Doğru cevap: {s.get('cevap','')} → {s.get('islem','')}")

    skor = st.session_state[hm_key]
    if skor["toplam"] > 0:
        st.markdown(f"**🏆 Skor:** {skor['skor']}/{skor['toplam']}")


# ── 12f) Doğa ile Sayılar ───────────────────────────────────────────────────

def _zk_matematik_zinciri():
    """Matematik zinciri — bir işlemin sonucu diğerinin başlangıcı. Sınırsız."""
    import random as _r
    styled_section("🧮 Matematik Zinciri", "#6366f1")

    st.markdown("**Kurallar:** Bir sayıdan başla, işlemleri sırayla uygula, sonucu bul!")

    zorluk = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="zk_mz_z",
                           format_func=lambda x: {"kolay": "🌱 Kolay (2 adım)", "orta": "🌿 Orta (3 adım)", "zor": "🌳 Zor (4 adım)"}[x])

    mz_key = "zk_mz_state"
    if mz_key not in st.session_state:
        st.session_state[mz_key] = {"skor": 0, "toplam": 0}

    if st.button("🧮 Yeni Zincir Üret!", key="zk_mz_new", type="primary"):
        adim_sayisi = {"kolay": 2, "orta": 3, "zor": 4}[zorluk]
        baslangic = _r.randint(2, 20)
        zincir = [{"sayi": baslangic, "op": "", "deger": 0}]
        sonuc = baslangic

        for _ in range(adim_sayisi):
            op = _r.choice(["+", "-", "×"])
            if op == "+":
                d = _r.randint(1, 15)
                sonuc = sonuc + d
            elif op == "-":
                d = _r.randint(1, min(sonuc - 1, 10)) if sonuc > 2 else 1
                sonuc = sonuc - d
            else:
                d = _r.randint(2, 5)
                sonuc = sonuc * d
            zincir.append({"op": op, "deger": d})

        st.session_state["zk_mz_soru"] = {"baslangic": baslangic, "zincir": zincir, "cevap": sonuc}

    if "zk_mz_soru" in st.session_state:
        s = st.session_state["zk_mz_soru"]
        zincir_str = str(s["baslangic"])
        for adim in s["zincir"][1:]:
            op_goster = {"+" : "➕", "-": "➖", "×": "✖️"}.get(adim["op"], adim["op"])
            zincir_str += f" {op_goster} {adim['deger']}"

        _render_html(f"""
        <div style="background:#0f172a;border-radius:20px;padding:28px;text-align:center;margin:12px 0;
                     border:2px solid rgba(99,102,241,0.3)">
            <div style="font-size:0.85rem;color:#94a3b8 !important;margin-bottom:12px">İşlem zincirini takip et!</div>
            <div style="font-size:2rem;font-weight:800;color:#e0e7ff !important;letter-spacing:4px">
                {zincir_str} = ❓
            </div>
        </div>
        """)

        ans = st.number_input("Sonuç:", min_value=-10000, max_value=100000, step=1, value=0, key="zk_mz_ans")
        if st.button("✅ Kontrol", key="zk_mz_chk"):
            st.session_state[mz_key]["toplam"] += 1
            if int(ans) == s["cevap"]:
                st.session_state[mz_key]["skor"] += 1
                st.success(f"🎉 Doğru! {zincir_str} = {s['cevap']}")
            else:
                st.error(f"❌ Yanlış! Doğru: {s['cevap']}")

    skor = st.session_state[mz_key]
    if skor["toplam"] > 0:
        st.markdown(f"**🏆 Skor:** {skor['skor']}/{skor['toplam']}")


def _zk_kayip_sayi():
    """Kayıp sayı — denklemdeki eksik sayıyı bul. Sınırsız."""
    import random as _r
    styled_section("🔢 Kayıp Sayı", "#f59e0b")

    st.markdown("**İşlemdeki ❓ yerine hangi sayı gelmeli?**")

    zorluk = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="zk_ks_z",
                           format_func=lambda x: {"kolay": "🌱 Kolay", "orta": "🌿 Orta", "zor": "🌳 Zor"}[x])

    ks_key = "zk_ks_state"
    if ks_key not in st.session_state:
        st.session_state[ks_key] = {"skor": 0, "toplam": 0}

    if st.button("🔢 Yeni Kayıp Sayı Üret!", key="zk_ks_new", type="primary"):
        if zorluk == "kolay":
            a = _r.randint(1, 20)
            b = _r.randint(1, 20)
            op = _r.choice(["+", "-"])
            if op == "-" and a < b:
                a, b = b, a
            sonuc = a + b if op == "+" else a - b
            gizli = _r.choice(["a", "b", "sonuc"])
        elif zorluk == "orta":
            a = _r.randint(2, 50)
            b = _r.randint(2, 30)
            op = _r.choice(["+", "-", "×"])
            if op == "-" and a < b:
                a, b = b, a
            sonuc = a + b if op == "+" else a - b if op == "-" else a * b
            gizli = _r.choice(["a", "b", "sonuc"])
        else:
            a = _r.randint(5, 100)
            b = _r.randint(2, 20)
            op = _r.choice(["+", "-", "×", "÷"])
            if op == "÷":
                a = b * _r.randint(2, 15)
                sonuc = a // b
            elif op == "-":
                if a < b:
                    a, b = b, a
                sonuc = a - b
            elif op == "+":
                sonuc = a + b
            else:
                sonuc = a * b
            gizli = _r.choice(["a", "b", "sonuc"])

        if gizli == "a":
            gosterim = f"❓ {op} {b} = {sonuc}"
            cevap = a
        elif gizli == "b":
            gosterim = f"{a} {op} ❓ = {sonuc}"
            cevap = b
        else:
            gosterim = f"{a} {op} {b} = ❓"
            cevap = sonuc

        st.session_state["zk_ks_soru"] = {"gosterim": gosterim, "cevap": cevap, "a": a, "b": b, "op": op, "sonuc": sonuc}

    if "zk_ks_soru" in st.session_state:
        s = st.session_state["zk_ks_soru"]
        _render_html(f"""
        <div style="background:#0f172a;border-radius:20px;padding:32px;text-align:center;margin:12px 0;
                     border:2px solid rgba(245,158,11,0.3)">
            <div style="font-size:2.5rem;font-weight:900;color:#e0e7ff !important;letter-spacing:6px">
                {s['gosterim']}
            </div>
        </div>
        """)

        ans = st.number_input("❓ = ?", min_value=-10000, max_value=100000, step=1, value=0, key="zk_ks_ans")
        if st.button("✅ Kontrol", key="zk_ks_chk"):
            st.session_state[ks_key]["toplam"] += 1
            if int(ans) == s["cevap"]:
                st.session_state[ks_key]["skor"] += 1
                st.success(f"🎉 Doğru! {s['a']} {s['op']} {s['b']} = {s['sonuc']}")
            else:
                st.error(f"❌ Yanlış! ❓ = {s['cevap']} → {s['a']} {s['op']} {s['b']} = {s['sonuc']}")

    skor = st.session_state[ks_key]
    if skor["toplam"] > 0:
        st.markdown(f"**🏆 Skor:** {skor['skor']}/{skor['toplam']}")


def _zk_zar_matemat():
    """Zar matematiği — zar at, işlem yap. Sınırsız."""
    import random as _r
    styled_section("🎲 Zar Matematiği", "#ec4899")

    st.markdown("**Zarları at, işlemi çöz!**")

    zar_sayisi = st.selectbox("Zar Sayısı", [2, 3, 4], key="zk_zr_adet",
                               format_func=lambda x: f"{x} zar")

    zr_key = "zk_zr_state"
    if zr_key not in st.session_state:
        st.session_state[zr_key] = {"skor": 0, "toplam": 0}

    zar_emojileri = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

    if st.button("🎲 Zarları At!", key="zk_zr_new", type="primary"):
        zarlar = [_r.randint(1, 6) for _ in range(zar_sayisi)]
        islem = _r.choice(["toplam", "carpim", "fark", "en_buyuk_en_kucuk"])

        if islem == "toplam":
            cevap = sum(zarlar)
            soru = "Zarların TOPLAMI kaçtır?"
        elif islem == "carpim":
            c = 1
            for z in zarlar:
                c *= z
            cevap = c
            soru = "Zarların ÇARPIMI kaçtır?"
        elif islem == "fark":
            cevap = max(zarlar) - min(zarlar)
            soru = "En BÜYÜK ile en KÜÇÜK zar arasındaki FARK kaçtır?"
        else:
            cevap = max(zarlar) + min(zarlar)
            soru = "En BÜYÜK ve en KÜÇÜK zarın TOPLAMI kaçtır?"

        st.session_state["zk_zr_soru"] = {"zarlar": zarlar, "soru": soru, "cevap": cevap, "islem": islem}

    if "zk_zr_soru" in st.session_state:
        s = st.session_state["zk_zr_soru"]
        zarlar = s.get("zarlar", [])
        zar_goster = "  ".join(zar_emojileri.get(z, str(z)) for z in zarlar)
        zar_sayilar = "  ".join(str(z) for z in zarlar)

        _render_html(f"""
        <div style="background:#0f172a;border-radius:20px;padding:28px;text-align:center;margin:12px 0;
                     border:2px solid rgba(236,72,153,0.3)">
            <div style="font-size:4rem;letter-spacing:16px;margin-bottom:12px">{zar_goster}</div>
            <div style="font-size:1.2rem;color:#94a3b8 !important;margin-bottom:8px">({zar_sayilar})</div>
            <div style="font-size:1.1rem;font-weight:700;color:#e0e7ff !important">{s.get('soru','')}</div>
        </div>
        """)

        ans = st.number_input("Cevabın:", min_value=-100, max_value=10000, step=1, value=0, key="zk_zr_ans")
        if st.button("✅ Kontrol", key="zk_zr_chk"):
            st.session_state[zr_key]["toplam"] += 1
            if int(ans) == s.get("cevap", -1):
                st.session_state[zr_key]["skor"] += 1
                st.success(f"🎉 Doğru! Cevap: {s['cevap']}")
            else:
                st.error(f"❌ Yanlış! Doğru: {s['cevap']}")

    skor = st.session_state[zr_key]
    if skor["toplam"] > 0:
        st.markdown(f"**🏆 Skor:** {skor['skor']}/{skor['toplam']}")


def _zk_hiz_testi():
    """Hız testi — art arda sorular, süre ölçümü. Sınırsız."""
    import random as _r
    import time
    styled_section("⏱️ Hız Testi — 60 Saniye Meydan Okuma", "#ef4444")

    st.markdown("**60 saniyede kaç soru çözebilirsin?**")

    zorluk = st.selectbox("Zorluk", ["kolay", "orta", "zor"], key="zk_ht_z",
                           format_func=lambda x: {"kolay": "🌱 Kolay (+,-)", "orta": "🌿 Orta (+,-,×)", "zor": "🌳 Zor (dört işlem)"}[x])

    ht_key = "zk_ht_state"

    if st.button("⏱️ 60 Saniye Başlat!", key="zk_ht_start", type="primary"):
        st.session_state[ht_key] = {
            "active": True, "start": time.time(), "skor": 0, "yanlis": 0, "soru_no": 0,
        }
        # İlk soruyu üret
        _zk_ht_yeni_soru(zorluk)

    if ht_key in st.session_state and st.session_state[ht_key].get("active"):
        state = st.session_state[ht_key]
        elapsed = time.time() - state.get("start", time.time())
        kalan = max(0, 60 - elapsed)

        if kalan <= 0:
            state["active"] = False
            oran = (state["skor"] / max(state["skor"] + state["yanlis"], 1)) * 100
            _render_html(f"""
            <div style="background:#0f172a;border-radius:20px;padding:32px;text-align:center;margin:12px 0;
                         border:2px solid rgba(16,185,129,0.3)">
                <div style="font-size:3rem;margin-bottom:12px">{'🏆' if oran>=80 else '👏' if oran>=50 else '💪'}</div>
                <div style="font-size:1.5rem;font-weight:800;color:#e0e7ff !important">Süre Doldu!</div>
                <div style="display:flex;justify-content:center;gap:30px;margin-top:16px">
                    <div><div style="font-size:2rem;font-weight:900;color:#10b981 !important">{state['skor']}</div><div style="font-size:0.75rem;color:#94a3b8 !important">Doğru</div></div>
                    <div><div style="font-size:2rem;font-weight:900;color:#ef4444 !important">{state['yanlis']}</div><div style="font-size:0.75rem;color:#94a3b8 !important">Yanlış</div></div>
                    <div><div style="font-size:2rem;font-weight:900;color:#f59e0b !important">%{oran:.0f}</div><div style="font-size:0.75rem;color:#94a3b8 !important">Başarı</div></div>
                </div>
            </div>
            """)
            if st.button("🔄 Tekrar!", key="zk_ht_reset"):
                del st.session_state[ht_key]
                st.rerun()
        else:
            _render_html(f"""
            <div style="text-align:center;margin:8px 0">
                <span style="font-size:1.5rem;font-weight:900;color:{'#ef4444' if kalan<10 else '#f59e0b'} !important">⏱️ {kalan:.0f}s</span>
                <span style="color:#94a3b8 !important;margin-left:16px">✅{state['skor']} ❌{state['yanlis']}</span>
            </div>
            """)

            if "zk_ht_soru" in st.session_state:
                s = st.session_state["zk_ht_soru"]
                _render_html(f"""
                <div style="background:#0f172a;border-radius:20px;padding:24px;text-align:center;margin:8px 0;
                             border:2px solid rgba(239,68,68,0.3)">
                    <div style="font-size:2.5rem;font-weight:900;color:#e0e7ff !important">{s.get('soru','')}</div>
                </div>
                """)

                secenekler = s.get("secenekler", [])
                cols = st.columns(4)
                for idx, opt in enumerate(secenekler):
                    with cols[idx]:
                        if st.button(str(opt), key=f"zk_ht_opt_{state['soru_no']}_{idx}", use_container_width=True):
                            if opt == s.get("cevap"):
                                state["skor"] += 1
                            else:
                                state["yanlis"] += 1
                            state["soru_no"] += 1
                            _zk_ht_yeni_soru(zorluk)
                            st.rerun()


def _zk_ht_yeni_soru(zorluk: str):
    """Hız testi için yeni soru üret."""
    import random as _r
    if zorluk == "kolay":
        a, b = _r.randint(1, 20), _r.randint(1, 20)
        op = _r.choice(["+", "-"])
        if op == "-" and a < b:
            a, b = b, a
    elif zorluk == "orta":
        a, b = _r.randint(2, 30), _r.randint(2, 15)
        op = _r.choice(["+", "-", "×"])
        if op == "-" and a < b:
            a, b = b, a
    else:
        a, b = _r.randint(3, 50), _r.randint(2, 12)
        op = _r.choice(["+", "-", "×", "÷"])
        if op == "÷":
            a = b * _r.randint(2, 10)
        elif op == "-" and a < b:
            a, b = b, a

    if op == "+":
        cevap = a + b
    elif op == "-":
        cevap = a - b
    elif op == "×":
        cevap = a * b
    else:
        cevap = a // b

    secenekler = {cevap}
    while len(secenekler) < 4:
        w = cevap + _r.choice([-3, -2, -1, 1, 2, 3]) * _r.randint(1, 3)
        if w >= 0 and w != cevap:
            secenekler.add(w)
    secenekler = sorted(list(secenekler))

    st.session_state["zk_ht_soru"] = {"soru": f"{a} {op} {b} = ?", "cevap": cevap, "secenekler": secenekler}


def _zk_doga_sayilar():
    """Doğadaki matematik — bitkiler, hayvanlar, mevsimler."""
    styled_section("🌱 Doğa ile Sayılar", "#10b981")

    _render_html("""
    <div class="zk-card" style="text-align:center;border-color:rgba(16,185,129,0.3)">
        <div style="font-size:2rem;margin-bottom:6px" class="mat-grow">🌍🌿</div>
        <div style="font-weight:700;color:#bbf7d0 !important">Doğa Bir Matematik Kitabıdır!</div>
        <div style="color:#86efac !important;font-size:0.85rem">Etrafına bak — sayılar her yerde!</div>
    </div>
    """)

    kartlar = [
        {
            "baslik": "🌻 Ayçiçeği Spiralleri",
            "gorsel": """
            <div style='text-align:center;font-size:1.5rem;line-height:2;margin:12px 0;
                          background:#0f172a;border-radius:16px;padding:20px;border:1px solid rgba(234,179,8,0.2)'>
                <div>🌻</div>
                <div style='font-size:0.9rem;color:#fde68a !important'>Spiral sayıları: <b>1, 1, 2, 3, 5, 8, 13, 21, 34</b></div>
                <div style='font-size:0.85rem;color:#94a3b8 !important'>Saat yönü: 34 spiral • Ters yön: 55 spiral</div>
                <div style='margin-top:8px'>🌻🌻🌻🌻🌻🌻🌻🌻🌻🌻🌻🌻🌻</div>
            </div>""",
            "bilgi": "Ayçiçeği tohumları **Fibonacci spiralleri** şeklinde dizilir. Bu sayede en az boşlukla en çok tohum sığar!",
            "soru": "Fibonacci'de 5'ten sonra gelen sayı nedir? (3+5=?)",
            "cevap": "8",
        },
        {
            "baslik": "❄️ Kar Tanesi Geometrisi",
            "gorsel": """
            <div style='text-align:center;margin:12px 0;background:#0f172a;border-radius:16px;padding:20px;
                          border:1px solid rgba(96,165,250,0.2)'>
                <div style='font-size:3rem'>❄️</div>
                <div style='font-size:2rem;margin:8px 0'>🔷🔷🔷🔷🔷🔷</div>
                <div style='font-size:0.85rem;color:#93c5fd !important'><b>Her kar tanesi 6 kolludur!</b> İstisnasız!</div>
                <div style='font-size:0.8rem;color:#94a3b8 !important'>Altıgen simetri — su molekülünün 120° bağ açısından</div>
            </div>""",
            "bilgi": "Trilyon trilyon kar tanesi arasında **hiçbiri birbirinin aynısı değildir** — ama hepsi 6 kolludur!",
            "soru": "Bir kar tanesinin kaç kolu var?",
            "cevap": "6",
        },
        {
            "baslik": "🐝 Arı Peteği Matematiği",
            "gorsel": """
            <div style='text-align:center;margin:12px 0;background:#0f172a;border-radius:16px;padding:20px;
                          border:1px solid rgba(234,179,8,0.2)'>
                <div style='font-size:2rem;line-height:1.2'>
                    ⬡⬡⬡⬡⬡<br>
                     ⬡⬡⬡⬡⬡<br>
                    ⬡⬡⬡⬡⬡<br>
                </div>
                <div style='font-size:0.85rem;color:#fde68a !important;margin-top:8px'><b>Altıgen petek:</b> En az balmumu ile en çok bal!</div>
                <div style='font-size:1.5rem;margin-top:4px'>🐝🍯</div>
            </div>""",
            "bilgi": "Altıgen, **en az çevre ile en çok alanı** kaplayan şekildir (düzgün döşemede). Arılar bunu milyon yıl önce 'keşfetti'!",
            "soru": "Arı peteğinin her hücresi kaç kenarlı?",
            "cevap": "6",
        },
        {
            "baslik": "🌿 Yaprak Dizilişi (Fillotaksi)",
            "gorsel": """
            <div style='text-align:center;margin:12px 0;background:#0f172a;border-radius:16px;padding:20px;
                          border:1px solid rgba(16,185,129,0.2)'>
                <div style='font-size:2rem'>🌿🍀🌱🌿🍀🌱🌿🍀</div>
                <div style='font-size:0.85rem;color:#86efac !important;margin-top:8px'>
                    Yapraklar gövdede <b>137.5°</b> açıyla dizilir<br>
                    Bu açı = 360° / φ² (Altın oran!)
                </div>
                <div style='font-size:1.5rem;margin-top:8px'>🌻 = φ = 1.618...</div>
            </div>""",
            "bilgi": "Yapraklar bu açıyla dizilir çünkü böylece **her yaprak maksimum güneş ışığı** alır — üstteki alttakini gölgelemez!",
            "soru": "Altın oran (φ) yaklaşık kaçtır? (Bir veya iki ondalık basamak)",
            "cevap": "1.62",
        },
        {
            "baslik": "🐚 Deniz Kabuğu Spirali",
            "gorsel": """
            <div style='text-align:center;margin:12px 0;background:#0f172a;border-radius:16px;padding:20px;
                          border:1px solid rgba(168,85,247,0.2)'>
                <div style='font-size:3rem' class='mat-grow'>🐚</div>
                <div style='font-size:1.5rem;margin:8px 0'>🌀 → 📐 → φ</div>
                <div style='font-size:0.85rem;color:#c4b5fd !important'>
                    Nautilus kabuğu <b>logaritmik spiral</b> şeklinde büyür<br>
                    Her odacık bir öncekinin φ katı büyüklüğünde!
                </div>
            </div>""",
            "bilgi": "Deniz kabuğu büyüdükçe şeklini korur — bu **kendine benzerlik** (fraktal) özelliğidir. Doğanın mükemmel tasarımı!",
            "soru": "Nautilus kabuğunun spiral şekli ne tür bir spiraldir? (l... spiral)",
            "cevap": "logaritmik",
        },
    ]

    for idx, k in enumerate(kartlar):
        with st.expander(k["baslik"], expanded=(idx < 2)):
            _render_html(k["gorsel"])
            st.markdown(k["bilgi"])
            st.markdown("---")
            ans = st.text_input(f"🎯 {k['soru']}", key=f"zk_doga_{idx}")
            if ans:
                if ans.strip().lower().replace(",", ".") in (k["cevap"], k["cevap"].replace(".", ",")):
                    st.success("🎉 Doğru! Doğanın matematik sırlarını çözüyorsun! 🌟")
                else:
                    st.info(f"🤔 Doğru cevap: **{k['cevap']}**")


# ── 12g) Zeka Sirki ─────────────────────────────────────────────────────────

def _zk_zeka_sirki():
    """Karışık zeka soruları — her türden, eğlenceli sahnelerle."""
    import random as _r
    styled_section("🎪 Zeka Sirki — Büyük Gösteri!", "#ec4899")

    _render_html("""
    <div style="background:linear-gradient(135deg,#831843,#be185d);border-radius:24px;padding:28px;margin-bottom:20px;
                 border:2px solid rgba(236,72,153,0.4);text-align:center;position:relative;overflow:hidden">
        <div style="position:absolute;top:8px;left:16px;font-size:1.8rem" class="mat-bounce">🎪</div>
        <div style="position:absolute;top:8px;right:16px;font-size:1.8rem" class="mat-wiggle">🤹</div>
        <div style="position:relative;z-index:1">
            <div style="font-size:2.5rem;margin-bottom:8px">🎪🎭🤹🎩✨</div>
            <div style="font-weight:800;color:#e0e7ff !important;font-size:1.3rem">Büyük Zeka Gösterisi!</div>
            <div style="color:#fce7f3 !important;font-size:0.9rem">Her soru bir gösteri numarası — hepsini çöz, sirkten şampiyon çık!</div>
        </div>
    </div>
    """)

    gosteriler = [
        {
            "ad": "🤹 Jonglör Sorusu",
            "sahne": "🤹 → 🔴🟡🔵🟢🟣",
            "soru": "Jonglör 5 topla oynuyor. Her 3 saniyede bir top düşüyor. Kaç saniye sonra elinde top kalmaz?",
            "cevap": "15",
            "aciklama": "5 top × 3 saniye = 15 saniye",
        },
        {
            "ad": "🎩 Sihirbaz Sorusu",
            "sahne": "🎩 → 🐰🐰🐰 → 🎩 → 🐰🐰🐰🐰🐰🐰",
            "soru": "Sihirbaz şapkadan 3 tavşan çıkardı. Her tavşan 2 tavşan daha doğurursa toplam kaç tavşan olur?",
            "cevap": "9",
            "aciklama": "3 ana + 3×2 yavru = 3+6 = 9",
        },
        {
            "ad": "🎭 Maske Bulmacası",
            "sahne": "😊😊😊😢😊😊😢😢😊😢😢😢",
            "soru": "Yukarıdaki 12 maskede kaç gülen yüz var?",
            "cevap": "6",
            "aciklama": "😊 say: 1,2,3, _,5,6, _, _,9, _, _, _ → 6 gülen yüz",
        },
        {
            "ad": "🏋️ Ağırlık Dengesi",
            "sahne": "⚖️  🐘=🐻🐻🐻  ve  🐻=🐱🐱🐱🐱",
            "soru": "1 fil = 3 ayı, 1 ayı = 4 kedi. 1 fil kaç kediye eşittir?",
            "cevap": "12",
            "aciklama": "1 fil = 3 ayı = 3 × 4 kedi = 12 kedi",
        },
        {
            "ad": "🧊 Buz Kırma",
            "sahne": "🧊🧊🧊🧊🧊🧊🧊🧊 → 🔨",
            "soru": "8 buz parçasını yarıya bölmek istiyoruz. Her kırma 1 parçayı 2'ye böler. Hepsini bölmek için kaç kırma gerekir?",
            "cevap": "8",
            "aciklama": "Her kırma 1 parça ekler: 8→9→...→16 = 8 kırma. VEYA: 8 parçanın her birini 1 kez = 8 kırma.",
        },
        {
            "ad": "🌈 Renk Karışımı",
            "sahne": "🔴+🔵=🟣   🔴+🟡=🟠   🔵+🟡=🟢",
            "soru": "Kırmızı+Mavi=Mor, Kırmızı+Sarı=Turuncu, Mavi+Sarı=Yeşil. 3 ana renkle kaç farklı karışım renk yapılabilir?",
            "cevap": "3",
            "aciklama": "3 ana rengin 2'li kombinasyonları: C(3,2) = 3",
        },
        {
            "ad": "🚂 Tren Vagonu",
            "sahne": "🚂🟦🟥🟨🟩🟦🟥🟨🟩🟦🟥❓",
            "soru": "Tren vagonları: Mavi-Kırmızı-Sarı-Yeşil tekrar ediyor. 12. vagon ne renk?",
            "cevap": "🟨",
            "aciklama": "12 ÷ 4 = 3 (tam bölünür) → 4'lü grubun sonuncusu = Yeşil... Hayır: 4,8,12 → 12. vagon grubun 4. elemanı = Yeşil 🟩. Ancak soru 12. vagonu soruyor: 4n=12 → Yeşil. Veya sayalım: M,K,S,Y,M,K,S,Y,M,K,S,? = Sarı. 11=S, 12=Y. 12. = Yeşil!",
        },
        {
            "ad": "🎂 Pasta Dilimi",
            "sahne": "🎂 → 3 kesim ile max kaç dilim?",
            "soru": "Yuvarlak bir pastayı 3 düz kesimle en fazla kaç parçaya bölebilirsin?",
            "cevap": "7",
            "aciklama": "1 kesim=2, 2 kesim=4, 3 kesim=7 parça (kesimler birbirini kesmeli!) Formül: n(n+1)/2 + 1",
        },
    ]

    _r.shuffle(gosteriler)

    for idx, g in enumerate(gosteriler[:5]):
        with st.expander(g["ad"], expanded=(idx == 0)):
            _render_html(f"""
            <div style="text-align:center;font-size:2rem;margin:12px 0;letter-spacing:4px;
                         background:#0f172a;border-radius:14px;padding:16px;
                         border:1px solid rgba(236,72,153,0.15)">{g['sahne']}</div>
            """)
            st.markdown(f"**{g['soru']}**")

            ans = st.text_input("Cevabın:", key=f"zk_sirk_{idx}")
            if ans:
                if ans.strip() == str(g["cevap"]):
                    st.success(f"🎉 Bravo! {g['aciklama']}")
                    st.balloons()
                else:
                    st.error(f"🤔 Doğru cevap: **{g['cevap']}** — {g['aciklama']}")


# ══════════════════════════════════════════════════════════════════════════════
# 13) DGS — DİKKAT GELİŞTİRME SİSTEMİ
# ══════════════════════════════════════════════════════════════════════════════

def _render_dgs_dikkat(store: MatematikDataStore):
    """DGS — Dikkat Geliştirme Sistemi. Adım adım, seviye seviye dikkat eğitimi."""
    import random as _r
    styled_section("🎯 DGS — Dikkat Geliştirme Sistemi", "#ef4444")

    _render_html("""
    <style>
    .dgs-hero {
        background: linear-gradient(135deg, #1a0505 0%, #7f1d1d 50%, #dc2626 100%);
        border-radius: 24px; padding: 32px; margin-bottom: 24px;
        border: 2px solid rgba(239,68,68,0.5); text-align: center;
        position: relative; overflow: hidden;
    }
    .dgs-hero::before {
        content: ''; position: absolute; inset: 0;
        background: radial-gradient(circle at 70% 30%, rgba(239,68,68,0.1) 0%, transparent 50%);
    }
    .dgs-level-card {
        background: linear-gradient(145deg, #1a0a0a, #2d1515);
        border-radius: 18px; padding: 22px; margin-bottom: 14px;
        border: 1px solid rgba(239,68,68,0.2);
    }
    .dgs-grid { display: grid; gap: 4px; margin: 16px auto; }
    .dgs-cell {
        display: flex; align-items: center; justify-content: center;
        border-radius: 8px; font-weight: 700; cursor: pointer;
        transition: all 0.15s; border: 1px solid rgba(239,68,68,0.1);
    }
    .dgs-timer {
        font-size: 2rem; font-weight: 900; text-align: center;
        font-family: 'Courier New', monospace;
    }
    </style>

    <div class="dgs-hero">
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:10px" class="mat-grow">🎯🧠👁️</div>
            <h2 style="color:#fca5a5 !important;font-size:1.6rem;margin:0 0 8px !important">Dikkat Geliştirme Sistemi</h2>
            <p style="color:#fecaca !important;font-size:0.9rem;margin:0 !important;max-width:600px;display:inline-block">
                Bilimsel araştırmalara dayalı 8 modüllü dikkat eğitim programı.
                Görsel tarama, seçici dikkat, sürdürülebilir dikkat, bölünmüş dikkat
                ve çalışma belleği — her gün 10 dk pratik, dikkat süresini %40 artırır!
            </p>
        </div>
    </div>
    """)

    # Kullanıcı bilgisi
    auth_user = st.session_state.get("auth_user", {})
    dgs_user_id = auth_user.get("username", "misafir")
    dgs_user_name = auth_user.get("ad_soyad", auth_user.get("username", "Misafir"))

    sub = st.tabs([
        "📊 Dikkat Panosu",
        "👁️ Farklı Olanı Bul",
        "🔢 Sayı Avcısı",
        "🎨 Renk Karmaşası",
        "📝 Eksik Olan Ne?",
        "🔀 Sıra Takibi",
        "⏱️ Hız Odağı",
        "🧮 Çift Görev",
    ])

    with sub[0]:
        _dgs_dikkat_panosu(store, dgs_user_id, dgs_user_name)
    with sub[1]:
        _dgs_farkli_bul()
    with sub[2]:
        _dgs_sayi_avcisi()
    with sub[3]:
        _dgs_renk_karmasasi()
    with sub[4]:
        _dgs_eksik_ne()
    with sub[5]:
        _dgs_sira_takibi()
    with sub[6]:
        _dgs_hiz_odagi()
    with sub[7]:
        _dgs_cift_gorev()


# ── 13a) Farklı Olanı Bul ───────────────────────────────────────────────────

def _dgs_farkli_bul():
    """Görsel tarama — grid içinde farklı emojileri bul."""
    import random as _r
    styled_section("👁️ Farklı Olanı Bul — Görsel Tarama", "#ef4444")

    seviye = st.selectbox("Seviye", [
        ("4x4 Kolay", 4, 1), ("5x5 Orta", 5, 1), ("6x6 Zor", 6, 2),
        ("7x7 Uzman", 7, 2), ("8x8 Usta", 8, 3),
    ], key="dgs_fb_sev", format_func=lambda x: x[0])

    boyut, farkli_adet = seviye[1], seviye[2]

    # Benzer emoji çiftleri (dikkat gerektirenler)
    benzer_ciftler = [
        ("😀", "😃"), ("🐶", "🐕"), ("🌻", "🌼"), ("🔵", "🔷"), ("🟢", "🟩"),
        ("⭐", "🌟"), ("🍎", "🍏"), ("🐱", "😺"), ("👋", "🖐️"), ("🔴", "🟠"),
        ("🌸", "🌺"), ("🐟", "🐠"), ("🦊", "🐕"), ("📘", "📗"), ("💙", "💎"),
        ("🎵", "🎶"), ("☀️", "🌞"), ("🏠", "🏡"), ("✏️", "🖊️"), ("🧡", "❤️"),
    ]

    if st.button("🎯 Yeni Bulmaca!", key="dgs_fb_new", type="primary"):
        pair = _r.choice(benzer_ciftler)
        ana, farkli = pair
        total = boyut * boyut
        grid = [ana] * total

        # Rastgele pozisyonlara farklı emojileri yerleştir
        farkli_pozlar = _r.sample(range(total), farkli_adet)
        for p in farkli_pozlar:
            grid[p] = farkli

        st.session_state["dgs_fb"] = {
            "grid": grid, "boyut": boyut, "ana": ana, "farkli": farkli,
            "farkli_poz": farkli_pozlar, "farkli_adet": farkli_adet,
            "bulunan": [],
        }

    if "dgs_fb" in st.session_state:
        s = st.session_state["dgs_fb"]
        b = s["boyut"]

        _render_html(f"""
        <div style="text-align:center;color:#fca5a5 !important;font-size:0.9rem;margin-bottom:8px">
            <b>{s['farkli_adet']}</b> tane farklı {s['farkli']} bul! (Çoğunluk: {s['ana']})
        </div>
        """)

        # Grid göster
        for row in range(b):
            cols = st.columns(b)
            for col_idx, col in enumerate(cols):
                idx = row * b + col_idx
                emoji = s["grid"][idx]
                bulundu = idx in s.get("bulunan", [])
                with col:
                    btn_type = "primary" if bulundu else "secondary"
                    if st.button(emoji, key=f"dgs_fb_{idx}", use_container_width=True, type=btn_type):
                        if idx in s["farkli_poz"] and idx not in s["bulunan"]:
                            s["bulunan"].append(idx)
                            if len(s["bulunan"]) >= s["farkli_adet"]:
                                st.success(f"🎉 Hepsini buldun! {s['farkli_adet']}/{s['farkli_adet']} — Süper dikkat!")
                                st.balloons()
                            else:
                                st.success(f"✅ Buldum! ({len(s['bulunan'])}/{s['farkli_adet']})")
                        elif idx not in s["farkli_poz"]:
                            st.error("❌ Bu farklı değil! Daha dikkatli bak!")


# ── 13b) Sayı Avcısı ────────────────────────────────────────────────────────

def _dgs_sayi_avcisi():
    """Sayıları sırayla bul — seçici dikkat ve tarama hızı."""
    import random as _r
    styled_section("🔢 Sayı Avcısı — Sıralı Tarama", "#f59e0b")

    _render_html("""
    <div class="dgs-level-card" style="text-align:center;border-color:rgba(245,158,11,0.3)">
        <div style="font-size:1.8rem;margin-bottom:6px">🔢🎯</div>
        <div style="font-weight:700;color:#fde68a !important">Sayıları 1'den başlayarak sırayla bul!</div>
        <div style="color:#fcd34d !important;font-size:0.85rem">Ne kadar hızlı bulabilirsin?</div>
    </div>
    """)

    seviye = st.selectbox("Grid Boyutu", [
        ("4x4 (1-16)", 4), ("5x5 (1-25)", 5), ("6x6 (1-36)", 6), ("7x7 (1-49)", 7),
    ], key="dgs_sa_sev", format_func=lambda x: x[0])

    boyut = seviye[1]
    total = boyut * boyut

    if st.button("🎯 Başla!", key="dgs_sa_new", type="primary"):
        sayilar = list(range(1, total + 1))
        _r.shuffle(sayilar)
        import time
        st.session_state["dgs_sa"] = {
            "grid": sayilar, "boyut": boyut, "siradaki": 1,
            "baslangic": time.time(), "tamamlandi": False,
        }

    if "dgs_sa" in st.session_state:
        s = st.session_state["dgs_sa"]
        b = s["boyut"]

        if not s["tamamlandi"]:
            _render_html(f"""
            <div style="text-align:center;margin:8px 0">
                <span style="font-size:1.3rem;font-weight:800;color:#f59e0b !important">
                    Sıradaki: {s['siradaki']}
                </span>
            </div>
            """)

            for row in range(b):
                cols = st.columns(b)
                for col_idx, col in enumerate(cols):
                    idx = row * b + col_idx
                    sayi = s["grid"][idx]
                    bulundu = sayi < s["siradaki"]
                    with col:
                        if bulundu:
                            st.button(f"✅", key=f"dgs_sa_{idx}", disabled=True,
                                      use_container_width=True)
                        else:
                            if st.button(str(sayi), key=f"dgs_sa_{idx}", use_container_width=True):
                                if sayi == s["siradaki"]:
                                    s["siradaki"] += 1
                                    if s["siradaki"] > total:
                                        import time
                                        sure = round(time.time() - s["baslangic"], 1)
                                        s["tamamlandi"] = True
                                        st.success(f"🏆 Tamamlandı! Süre: **{sure} saniye**")
                                        st.balloons()
                                    else:
                                        st.rerun()
                                else:
                                    st.error(f"❌ Sıra {s['siradaki']}! {sayi} değil!")


# ── 13c) Renk Karmaşası (Stroop) ────────────────────────────────────────────

def _dgs_renk_karmasasi():
    """Stroop testi — 3 farklı mod, sınırsız, profesyonel."""
    import random as _r
    styled_section("🎨 Renk Karmaşası — Stroop Testi", "#8b5cf6")

    mod = st.selectbox("Test Modu", [
        "🎨 Klasik Stroop (Rengi söyle)",
        "🔄 Ters Stroop (Kelimeyi oku)",
        "🔢 Sayı Stroop (Kaç tane var?)",
    ], key="dgs_str_mod")

    renkler = [
        ("KIRMIZI", "#ef4444"), ("MAVİ", "#3b82f6"), ("YEŞİL", "#10b981"),
        ("SARI", "#eab308"), ("TURUNCU", "#f97316"), ("MOR", "#8b5cf6"),
    ]

    sk = "dgs_stroop"
    if sk not in st.session_state:
        st.session_state[sk] = {"skor": 0, "toplam": 0}

    if st.button("🎨 Yeni Soru Üret!", key="dgs_str_new", type="primary"):
        if "Klasik" in mod:
            # Klasik: kelime bir renk, yazım başka renk — YAZIM RENGİNİ söyle
            k_idx = _r.randint(0, len(renkler) - 1)
            r_idx = _r.randint(0, len(renkler) - 1)
            while r_idx == k_idx:
                r_idx = _r.randint(0, len(renkler) - 1)
            st.session_state["dgs_str_soru"] = {
                "mod": "klasik",
                "gosterim": renkler[k_idx][0],
                "renk_kodu": renkler[r_idx][1],
                "dogru": renkler[r_idx][0],
                "soru_text": "Bu kelime hangi RENKTE yazılmış?",
            }
        elif "Ters" in mod:
            # Ters: kelime bir renk, yazım başka renk — KELİMEYİ oku
            k_idx = _r.randint(0, len(renkler) - 1)
            r_idx = _r.randint(0, len(renkler) - 1)
            while r_idx == k_idx:
                r_idx = _r.randint(0, len(renkler) - 1)
            st.session_state["dgs_str_soru"] = {
                "mod": "ters",
                "gosterim": renkler[k_idx][0],
                "renk_kodu": renkler[r_idx][1],
                "dogru": renkler[k_idx][0],
                "soru_text": "Yazılan KELİME ne? (Rengine bakma!)",
            }
        else:
            # Sayı Stroop: "3 3 3 3" yazıyor ama kaç tane?
            sayi_kelime = _r.randint(1, 6)
            sayi_adet = _r.randint(2, 5)
            while sayi_adet == sayi_kelime:
                sayi_adet = _r.randint(2, 5)
            gosterim = (str(sayi_kelime) + " ") * sayi_adet
            st.session_state["dgs_str_soru"] = {
                "mod": "sayi",
                "gosterim": gosterim.strip(),
                "renk_kodu": _r.choice(renkler)[1],
                "dogru": str(sayi_adet),
                "soru_text": f"Kaç TANE sayı yazılmış? (Sayının değerini değil ADEDİNİ say!)",
            }

    if "dgs_str_soru" in st.session_state:
        s = st.session_state["dgs_str_soru"]

        _render_html(f"""
        <div style="background:#0f172a;border-radius:20px;padding:40px;text-align:center;margin:16px 0;
                     border:2px solid rgba(99,102,241,0.2)">
            <div style="font-size:0.85rem;color:#94a3b8 !important;margin-bottom:16px">{s.get('soru_text','')}</div>
            <div style="font-size:4rem;font-weight:900;color:{s.get('renk_kodu','#fff')} !important;letter-spacing:8px">
                {s.get('gosterim','')}
            </div>
        </div>
        """)

        if s.get("mod") == "sayi":
            # Sayı modu — sayı şıkları
            secenekler = list(range(1, 7))
            cols = st.columns(6)
            for idx, opt in enumerate(secenekler):
                with cols[idx]:
                    if st.button(str(opt), key=f"dgs_str_s_{idx}", use_container_width=True):
                        st.session_state[sk]["toplam"] += 1
                        if str(opt) == s.get("dogru"):
                            st.session_state[sk]["skor"] += 1
                            st.success(f"✅ Doğru! {s['dogru']} tane var!")
                        else:
                            st.error(f"❌ Yanlış! {s['dogru']} tane var!")
        else:
            # Renk şıkları
            cols = st.columns(3)
            for idx in range(len(renkler)):
                col = cols[idx % 3]
                renk_ad, renk_kod = renkler[idx]
                with col:
                    if st.button(renk_ad, key=f"dgs_str_{idx}", use_container_width=True):
                        st.session_state[sk]["toplam"] += 1
                        if renk_ad == s.get("dogru"):
                            st.session_state[sk]["skor"] += 1
                            st.success(f"✅ Doğru!")
                        else:
                            st.error(f"❌ Yanlış! Doğrusu: {s.get('dogru','')}")

    skor = st.session_state[sk]
    if skor["toplam"] > 0:
        oran = skor["skor"] / skor["toplam"] * 100
        _render_html(f"""
        <div style="text-align:center;margin-top:12px;color:#a78bfa !important;font-weight:700">
            🏆 Skor: {skor['skor']}/{skor['toplam']} (%{oran:.0f})
        </div>
        """)


# ── 13d) Eksik Olan Ne? ─────────────────────────────────────────────────────

def _dgs_eksik_ne():
    """Görsel hafıza — bir set göster, birini gizle, hangisi eksik?"""
    import random as _r
    styled_section("📝 Eksik Olan Ne? — Görsel Hafıza", "#10b981")

    havuz = ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐸","🐵","🦁","🐯",
             "🐮","🐷","🐔","🦋","🐝","🐞","🐙","🦀","🐟","🐬","🦅","🦉",
             "🌸","🌻","🌹","🍎","🍊","🍋","🍇","🍓","⭐","🌙","❤️","💎"]

    adet = st.selectbox("Eleman Sayısı", [5, 7, 9, 12], key="dgs_en_adet",
                         format_func=lambda x: f"{x} eleman ({'Kolay' if x<=5 else 'Orta' if x<=7 else 'Zor' if x<=9 else 'Uzman'})")

    ek = "dgs_eksik"

    if st.button("🧠 Yeni Tur!", key="dgs_en_new", type="primary"):
        secilen = _r.sample(havuz, adet)
        eksik_idx = _r.randint(0, len(secilen) - 1)
        eksik = secilen[eksik_idx]
        gosterilen = [e for i, e in enumerate(secilen) if i != eksik_idx]
        # Yanlış şıklar
        kalanlar = [e for e in havuz if e not in secilen]
        yanlis_secenekler = _r.sample(kalanlar, min(3, len(kalanlar)))
        tum_secenekler = [eksik] + yanlis_secenekler
        _r.shuffle(tum_secenekler)

        st.session_state[ek] = {
            "tam_set": secilen, "gosterilen": gosterilen,
            "eksik": eksik, "secenekler": tum_secenekler,
            "faz": "ezberle",  # ezberle -> cevapla
        }

    if ek in st.session_state:
        s = st.session_state[ek]

        if s["faz"] == "ezberle":
            _render_html(f"""
            <div style="background:#052e16;border-radius:20px;padding:28px;text-align:center;margin:16px 0;
                         border:2px solid rgba(16,185,129,0.3)">
                <div style="font-size:0.9rem;color:#86efac !important;margin-bottom:12px">🧠 Bu {len(s['tam_set'])} emojinin hepsini ezberle!</div>
                <div style="font-size:2.5rem;letter-spacing:12px;line-height:1.8">
                    {"  ".join(s['tam_set'])}
                </div>
            </div>
            """)

            if st.button("👁️ Ezberledim! Birini Gizle!", key="dgs_en_hide"):
                s["faz"] = "cevapla"
                st.rerun()

        elif s["faz"] == "cevapla":
            goster_str = "  ".join(s["gosterilen"])
            _render_html(f"""
            <div style="background:#0f172a;border-radius:20px;padding:28px;text-align:center;margin:16px 0;
                         border:2px solid rgba(239,68,68,0.3)">
                <div style="font-size:0.9rem;color:#fca5a5 !important;margin-bottom:12px">❓ Hangisi eksik?</div>
                <div style="font-size:2.5rem;letter-spacing:12px;line-height:1.8">
                    {goster_str}
                </div>
                <div style="font-size:3rem;color:#ef4444 !important;margin-top:12px" class="mat-wiggle">❓</div>
            </div>
            """)

            cols = st.columns(len(s["secenekler"]))
            for idx, opt in enumerate(s["secenekler"]):
                with cols[idx]:
                    if st.button(opt, key=f"dgs_en_opt_{idx}", use_container_width=True):
                        if opt == s["eksik"]:
                            st.success(f"🎉 Doğru! Eksik olan: {s['eksik']}")
                            st.balloons()
                        else:
                            st.error(f"❌ Yanlış! Eksik olan: {s['eksik']}")


# ── 13e) Sıra Takibi ────────────────────────────────────────────────────────

def _dgs_sira_takibi():
    """Sıralı hafıza — emojiler belli sırayla yanar, aynı sırayı tekrarla."""
    import random as _r
    styled_section("🔀 Sıra Takibi — Sıralı Hafıza", "#06b6d4")

    _render_html("""
    <div class="dgs-level-card" style="text-align:center;border-color:rgba(6,182,212,0.3)">
        <div style="font-size:1.8rem;margin-bottom:6px">🔀👁️</div>
        <div style="font-weight:700;color:#cffafe !important">Emojilerin yanma sırasını ezberle ve tekrarla!</div>
    </div>
    """)

    uzunluk = st.selectbox("Sıra Uzunluğu", [3, 4, 5, 6, 7, 8], key="dgs_st_uz",
                            format_func=lambda x: f"{x} adım ({'Kolay' if x<=4 else 'Orta' if x<=6 else 'Zor'})")

    emojiler = ["🔴", "🔵", "🟡", "🟢", "🟣", "🟠", "⚪", "🟤"]
    gosterim_set = emojiler[:min(uzunluk + 2, 8)]

    sk = "dgs_sira"

    if st.button("🎯 Yeni Sıra!", key="dgs_st_new", type="primary"):
        sira = [_r.choice(gosterim_set) for _ in range(uzunluk)]
        st.session_state[sk] = {
            "sira": sira, "kullanici": [],
            "faz": "goster", "set": gosterim_set,
        }

    if sk in st.session_state:
        s = st.session_state[sk]

        if s["faz"] == "goster":
            sira_str = " → ".join(s["sira"])
            _render_html(f"""
            <div style="background:#0a1628;border-radius:20px;padding:28px;text-align:center;margin:16px 0;
                         border:2px solid rgba(6,182,212,0.3)">
                <div style="font-size:0.9rem;color:#67e8f9 !important;margin-bottom:12px">🧠 Bu sırayı ezberle!</div>
                <div style="font-size:2.5rem;letter-spacing:8px">{sira_str}</div>
            </div>
            """)
            if st.button("✅ Ezberledim!", key="dgs_st_hide"):
                s["faz"] = "cevapla"
                st.rerun()

        elif s["faz"] == "cevapla":
            kalan = uzunluk - len(s["kullanici"])
            _render_html(f"""
            <div style="text-align:center;margin:12px 0">
                <div style="font-size:0.9rem;color:#fca5a5 !important;margin-bottom:8px">
                    Sırayla bas! ({len(s['kullanici'])}/{uzunluk})
                </div>
                <div style="font-size:2rem;letter-spacing:8px;min-height:2.5rem">
                    {' → '.join(s['kullanici']) if s['kullanici'] else '...'}
                </div>
            </div>
            """)

            cols = st.columns(len(s["set"]))
            for idx, emoji in enumerate(s["set"]):
                with cols[idx]:
                    if st.button(emoji, key=f"dgs_st_btn_{idx}", use_container_width=True):
                        s["kullanici"].append(emoji)
                        pos = len(s["kullanici"]) - 1
                        if s["kullanici"][pos] != s["sira"][pos]:
                            st.error(f"❌ Yanlış sıra! Doğrusu: {' → '.join(s['sira'])}")
                            s["faz"] = "bitti"
                        elif len(s["kullanici"]) >= uzunluk:
                            st.success(f"🎉 Mükemmel! {uzunluk} adımı doğru sırayla tekrarladın!")
                            st.balloons()
                            s["faz"] = "bitti"
                        else:
                            st.rerun()


# ── 13f) Hız Odağı ──────────────────────────────────────────────────────────

def _dgs_hiz_odagi():
    """Hızlı tepki — beliren emojiye hızla bas."""
    import random as _r
    import time
    styled_section("⏱️ Hız Odağı — Tepki Süresi", "#f97316")

    _render_html("""
    <div class="dgs-level-card" style="text-align:center;border-color:rgba(249,115,22,0.3)">
        <div style="font-size:1.8rem;margin-bottom:6px">⚡⏱️</div>
        <div style="font-weight:700;color:#fed7aa !important">Hedef emojiyi gördüğünde hemen bas!</div>
        <div style="color:#fdba74 !important;font-size:0.85rem">Ama tuzaklara basma! Sadece hedefi seç!</div>
    </div>
    """)

    hedef_emoji = st.selectbox("Hedef Emoji", ["⭐", "🎯", "💎", "🔴", "🦋"], key="dgs_ho_hedef")

    sk = "dgs_hiz"
    if sk not in st.session_state:
        st.session_state[sk] = {"skor": 0, "yanlis": 0, "toplam": 0}

    tuzaklar = ["🟡", "🟢", "🔵", "🟣", "🟠", "⬛", "🟤", "⚪"]

    if st.button("⚡ Yeni Hedef!", key="dgs_ho_new", type="primary"):
        # %60 hedef, %40 tuzak
        if _r.random() < 0.6:
            gosterilen = hedef_emoji
            dogru = True
        else:
            gosterilen = _r.choice(tuzaklar)
            dogru = False

        st.session_state["dgs_ho_soru"] = {
            "gosterilen": gosterilen, "dogru": dogru,
            "zaman": time.time(),
        }

    if "dgs_ho_soru" in st.session_state:
        s = st.session_state["dgs_ho_soru"]

        _render_html(f"""
        <div style="background:#0f172a;border-radius:24px;padding:40px;text-align:center;margin:16px 0;
                     border:2px solid rgba(249,115,22,0.3)">
            <div style="font-size:0.85rem;color:#94a3b8 !important;margin-bottom:16px">
                Hedef: {hedef_emoji} — Bu hedef mi?
            </div>
            <div style="font-size:6rem;line-height:1" class="mat-grow">{s['gosterilen']}</div>
        </div>
        """)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ HEDEF!", key="dgs_ho_evet", use_container_width=True, type="primary"):
                st.session_state[sk]["toplam"] += 1
                tepki = round(time.time() - s["zaman"], 2)
                if s["dogru"]:
                    st.session_state[sk]["skor"] += 1
                    st.success(f"✅ Doğru! Tepki: {tepki}s")
                else:
                    st.session_state[sk]["yanlis"] += 1
                    st.error(f"❌ Tuzak! Bu {s['gosterilen']}, hedef {hedef_emoji}!")
        with col2:
            if st.button("🚫 TUZAK!", key="dgs_ho_hayir", use_container_width=True):
                st.session_state[sk]["toplam"] += 1
                tepki = round(time.time() - s["zaman"], 2)
                if not s["dogru"]:
                    st.session_state[sk]["skor"] += 1
                    st.success(f"✅ Doğru! Bu tuzaktı. Tepki: {tepki}s")
                else:
                    st.session_state[sk]["yanlis"] += 1
                    st.error("❌ Bu hedefti! Kaçırdın!")

        skor = st.session_state[sk]
        if skor["toplam"] > 0:
            oran = skor["skor"] / skor["toplam"] * 100
            _render_html(f"""
            <div style="text-align:center;margin-top:12px;font-weight:700;color:#f97316 !important">
                🏆 {skor['skor']}/{skor['toplam']} doğru (%{oran:.0f}) • ❌ {skor['yanlis']} yanlış
            </div>
            """)


# ── 13g) Çift Görev ─────────────────────────────────────────────────────────

def _dgs_cift_gorev():
    """Bölünmüş dikkat — aynı anda iki göreve odaklan."""
    import random as _r
    styled_section("🧮 Çift Görev — Bölünmüş Dikkat", "#ec4899")

    _render_html("""
    <div class="dgs-level-card" style="text-align:center;border-color:rgba(236,72,153,0.3)">
        <div style="font-size:1.8rem;margin-bottom:6px">🧮🔀</div>
        <div style="font-weight:700;color:#fce7f3 !important">İki Görevi Aynı Anda Yap!</div>
        <div style="color:#f9a8d4 !important;font-size:0.85rem">Hem işlemi çöz, hem emojinin rengini söyle — bölünmüş dikkat!</div>
    </div>
    """)

    sk = "dgs_cift"
    if sk not in st.session_state:
        st.session_state[sk] = {"skor": 0, "toplam": 0}

    renkler = [("KIRMIZI", "#ef4444"), ("MAVİ", "#3b82f6"), ("YEŞİL", "#10b981"), ("SARI", "#eab308")]

    if st.button("🔀 Yeni Çift Görev!", key="dgs_cg_new", type="primary"):
        # Görev 1: Basit işlem
        a = _r.randint(1, 20)
        b = _r.randint(1, 20)
        op = _r.choice(["+", "-"])
        if op == "-" and a < b:
            a, b = b, a
        cevap_islem = a + b if op == "+" else a - b

        # Görev 2: Renk sorusu
        renk_ad, renk_kod = _r.choice(renkler)
        emoji = _r.choice(["⭐", "🔷", "🔶", "💠", "♦️", "●"])

        st.session_state["dgs_cg_soru"] = {
            "a": a, "b": b, "op": op, "cevap_islem": cevap_islem,
            "renk_ad": renk_ad, "renk_kod": renk_kod, "emoji": emoji,
        }

    if "dgs_cg_soru" in st.session_state:
        s = st.session_state["dgs_cg_soru"]

        col1, col2 = st.columns(2)
        with col1:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:16px;padding:24px;text-align:center;
                         border:2px solid rgba(99,102,241,0.2)">
                <div style="font-size:0.8rem;color:#94a3b8 !important;margin-bottom:8px">📐 Görev 1: İşlemi Çöz</div>
                <div style="font-size:2.5rem;font-weight:900;color:#e0e7ff !important">
                    {s['a']} {s['op']} {s['b']} = ?
                </div>
            </div>
            """)
            ans_islem = st.number_input("İşlem sonucu:", -100, 100, 0, key="dgs_cg_islem")

        with col2:
            _render_html(f"""
            <div style="background:#0f172a;border-radius:16px;padding:24px;text-align:center;
                         border:2px solid rgba(236,72,153,0.2)">
                <div style="font-size:0.8rem;color:#94a3b8 !important;margin-bottom:8px">🎨 Görev 2: Rengi Söyle</div>
                <div style="font-size:4rem;color:{s['renk_kod']} !important">{s['emoji']}</div>
            </div>
            """)
            ans_renk = st.selectbox("Simgenin rengi:", [r[0] for r in renkler], key="dgs_cg_renk")

        if st.button("✅ İkisini de Kontrol Et!", key="dgs_cg_check", type="primary"):
            st.session_state[sk]["toplam"] += 1
            islem_dogru = (int(ans_islem) == s["cevap_islem"])
            renk_dogru = (ans_renk == s["renk_ad"])

            if islem_dogru and renk_dogru:
                st.session_state[sk]["skor"] += 1
                st.success("🎉 İKİSİ DE DOĞRU! Mükemmel bölünmüş dikkat!")
                st.balloons()
            elif islem_dogru:
                st.warning(f"📐 İşlem doğru! Ama renk yanlış — doğrusu: {s['renk_ad']}")
            elif renk_dogru:
                st.warning(f"🎨 Renk doğru! Ama işlem yanlış — doğrusu: {s['cevap_islem']}")
            else:
                st.error(f"❌ İkisi de yanlış! İşlem: {s['cevap_islem']}, Renk: {s['renk_ad']}")

        skor = st.session_state[sk]
        if skor["toplam"] > 0:
            _render_html(f"""
            <div style="text-align:center;margin-top:12px;font-weight:700;color:#ec4899 !important">
                🏆 Çift doğru: {skor['skor']}/{skor['toplam']}
            </div>
            """)


# ── 13h) DGS Raporu ──────────────────────────────────────────────────────────

def _dgs_dikkat_panosu(store: MatematikDataStore, user_id: str, user_name: str):
    """Profesyonel dikkat ölçüm panosu — ilerleme grafikleri ve analiz."""
    styled_section("📊 Dikkat Ölçüm & İlerleme Panosu", "#6366f1")

    # Profili yükle veya session'dan hesapla
    profil_data = store.get_dikkat_profili(user_id)
    profil = DikkatProfili.from_dict(profil_data) if profil_data else None

    # Session state'den anlık skorları da topla
    moduller = [
        ("👁️ Farklı Olanı Bul", "dgs_fb", "farkli_bul", "Görsel Tarama", "#3b82f6"),
        ("🔢 Sayı Avcısı", "dgs_sa", "sayi_avcisi", "Sıralı Tarama", "#10b981"),
        ("🎨 Renk Karmaşası", "dgs_stroop", "stroop", "Seçici Dikkat", "#8b5cf6"),
        ("📝 Eksik Olan Ne?", "dgs_eksik", "eksik_ne", "Görsel Hafıza", "#f59e0b"),
        ("🔀 Sıra Takibi", "dgs_sira", "sira_takibi", "Sıralı Hafıza", "#06b6d4"),
        ("⏱️ Hız Odağı", "dgs_hiz", "hiz_odagi", "Tepki Süresi", "#ef4444"),
        ("🧮 Çift Görev", "dgs_cift", "cift_gorev", "Bölünmüş Dikkat", "#ec4899"),
    ]

    # Session state'den anlık skorları topla
    toplam_dogru = 0
    toplam_soru = 0
    modul_oranlar = {}

    for ad, sk, modul_key, beceri, renk in moduller:
        data = st.session_state.get(sk, {})
        d = data.get("skor", 0)
        t = data.get("toplam", 0)
        toplam_dogru += d
        toplam_soru += t
        modul_oranlar[modul_key] = {"dogru": d, "toplam": t, "ad": ad, "beceri": beceri, "renk": renk,
                                      "oran": (d / t * 100) if t > 0 else 0}

    genel_oran = (toplam_dogru / toplam_soru * 100) if toplam_soru > 0 else 0

    # Kaydet butonu
    if toplam_soru > 0:
        if st.button("💾 Bu Oturumu Kaydet (İlerleme Takibi)", key="dgs_kaydet", type="primary"):
            for mk, mv in modul_oranlar.items():
                if mv["toplam"] > 0:
                    store.kaydet_dikkat_sonuc(user_id, user_name, mk, mv["dogru"], mv["toplam"])
            st.success("✅ Dikkat profili kaydedildi!")
            profil_data = store.get_dikkat_profili(user_id)
            profil = DikkatProfili.from_dict(profil_data) if profil_data else None

    # ── Dikkat Puanı Kartı ──
    if genel_oran >= 85:
        seviye, sev_emoji, sev_renk = "Üstün Dikkat", "🏆", "#eab308"
    elif genel_oran >= 70:
        seviye, sev_emoji, sev_renk = "İyi Dikkat", "⭐", "#10b981"
    elif genel_oran >= 50:
        seviye, sev_emoji, sev_renk = "Ortalama Dikkat", "👍", "#3b82f6"
    elif genel_oran >= 30:
        seviye, sev_emoji, sev_renk = "Gelişmekte", "🌿", "#f59e0b"
    elif toplam_soru > 0:
        seviye, sev_emoji, sev_renk = "Başlangıç", "🌱", "#94a3b8"
    else:
        seviye, sev_emoji, sev_renk = "Henüz Ölçülmedi", "❓", "#64748b"

    _render_html(f"""
    <div style="background:linear-gradient(135deg,#0c0024,#1e0a3a,{sev_renk}20);border-radius:24px;padding:28px;margin-bottom:20px;
                 border:2px solid {sev_renk}60;text-align:center;position:relative;overflow:hidden">
        <div style="position:relative;z-index:1">
            <div style="font-size:3rem;margin-bottom:8px">{sev_emoji}</div>
            <div style="font-size:2.5rem;font-weight:900;color:{sev_renk} !important">
                {'%' + f'{genel_oran:.0f}' if toplam_soru > 0 else '—'}
            </div>
            <div style="font-size:1.2rem;font-weight:700;color:#e0e7ff !important;margin:4px 0">{seviye}</div>
            <div style="font-size:0.85rem;color:#94a3b8 !important">{user_name} • {toplam_dogru}/{toplam_soru} doğru</div>

            <!-- Dikkat barı -->
            <div style="max-width:400px;margin:16px auto 0;background:#1e1b4b;border-radius:12px;height:14px;overflow:hidden">
                <div style="width:{genel_oran:.0f}%;height:100%;border-radius:12px;
                             background:linear-gradient(90deg,#ef4444,#f59e0b,#10b981);
                             transition:width 0.8s"></div>
            </div>
            <div style="display:flex;justify-content:space-between;max-width:400px;margin:4px auto;font-size:0.65rem;color:#64748b !important">
                <span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span>
            </div>
        </div>
    </div>
    """)

    # ── Modül Detayları ──
    styled_section("📋 Modül Bazlı Performans", "#8b5cf6")

    for mk, mv in modul_oranlar.items():
        oran = mv["oran"]
        durum = "🟢" if oran >= 70 else "🟡" if oran >= 40 else "🔴" if mv["toplam"] > 0 else "⚪"

        _render_html(f"""
        <div style="background:#0f172a;border-radius:12px;padding:14px 18px;margin-bottom:8px;
                     border-left:4px solid {mv['renk']};border:1px solid rgba(99,102,241,0.1)">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                <span style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem">{durum} {mv['ad']}</span>
                <span style="font-size:0.75rem;color:#94a3b8 !important;background:#1e1b4b;padding:2px 8px;border-radius:10px">{mv['beceri']}</span>
                <span style="font-weight:700;color:{mv['renk']} !important;font-size:0.9rem">{mv['dogru']}/{mv['toplam']} • %{oran:.0f}</span>
            </div>
            <div style="background:#1e1b4b;border-radius:8px;height:10px;overflow:hidden">
                <div style="width:{oran:.0f}%;height:100%;background:{mv['renk']};border-radius:8px;transition:width 0.5s"></div>
            </div>
        </div>
        """)

    # ── Geçmiş İlerleme Grafiği ──
    if profil and profil.puan_gecmisi and len(profil.puan_gecmisi) > 1:
        styled_section("📈 Dikkat Puanı İlerleme Grafiği", "#10b981")

        tarihler = [p.get("tarih", "") for p in profil.puan_gecmisi[-30:]]
        puanlar = [p.get("puan", 0) for p in profil.puan_gecmisi[-30:]]

        # Basit HTML çubuk grafik
        max_puan = max(puanlar) if puanlar else 100
        grafik_html = '<div style="display:flex;align-items:flex-end;gap:4px;height:150px;padding:10px;background:#0f172a;border-radius:12px;border:1px solid rgba(99,102,241,0.1)">'
        for i, (t, p) in enumerate(zip(tarihler, puanlar)):
            h = max(4, (p / max(max_puan, 1)) * 130)
            renk = "#10b981" if p >= 70 else "#f59e0b" if p >= 40 else "#ef4444"
            grafik_html += f'''
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%">
                <div style="font-size:0.6rem;color:{renk} !important;margin-bottom:2px">{p:.0f}</div>
                <div style="width:100%;height:{h:.0f}px;background:{renk};border-radius:4px 4px 0 0;min-width:8px"></div>
                <div style="font-size:0.5rem;color:#64748b !important;margin-top:2px;transform:rotate(-45deg);white-space:nowrap">{t[-5:]}</div>
            </div>'''
        grafik_html += '</div>'
        _render_html(grafik_html)

        # Trend analizi
        if len(puanlar) >= 3:
            son_3 = puanlar[-3:]
            ilk_3 = puanlar[:3]
            trend = sum(son_3) / 3 - sum(ilk_3) / 3
            if trend > 5:
                _render_html('<div style="text-align:center;color:#10b981 !important;font-weight:700;margin-top:8px">📈 Dikkat puanın ARTIŞTA! Harika gidiyorsun!</div>')
            elif trend < -5:
                _render_html('<div style="text-align:center;color:#ef4444 !important;font-weight:700;margin-top:8px">📉 Dikkat puanın düşüşte. Daha fazla pratik yap!</div>')
            else:
                _render_html('<div style="text-align:center;color:#f59e0b !important;font-weight:700;margin-top:8px">📊 Dikkat puanın stabil. Düzenli pratikle yüksel!</div>')

    # ── Geçmiş Profil İstatistikleri ──
    if profil:
        styled_section("🏅 Genel İstatistikler", "#eab308")
        cols = st.columns(5)
        stats = [
            ("🧠", f"{profil.dikkat_puani:.0f}", "Dikkat Puanı"),
            ("📚", str(profil.toplam_egzersiz), "Toplam Egzersiz"),
            ("✅", str(profil.toplam_dogru), "Toplam Doğru"),
            ("🔥", str(profil.seri_gun), f"Seri ({profil.en_iyi_seri} en iyi)"),
            ("⏱️", f"{profil.toplam_sure_sn // 60}dk", "Toplam Süre"),
        ]
        for col, (ikon, deger, etiket) in zip(cols, stats):
            with col:
                _render_html(f"""
                <div class="mat-stat-card" style="padding:12px">
                    <div style="font-size:1.3rem">{ikon}</div>
                    <div style="font-weight:800;color:#818cf8 !important;font-size:1.3rem">{deger}</div>
                    <div style="font-size:0.65rem;color:#94a3b8 !important">{etiket}</div>
                </div>
                """)

    # AI Dikkat Koçu Tavsiyeleri
    if toplam_soru > 0:
        styled_section("🤖 AI Dikkat Koçu Tavsiyeleri", "#ec4899")
        tavsiyeler = _ai_dikkat_tavsiye(modul_oranlar, genel_oran)
        for t in tavsiyeler:
            _render_html(f"""
            <div style="background:linear-gradient(135deg,{t['renk']}08,{t['renk']}04);border-radius:14px;
                         padding:14px 18px;margin-bottom:8px;border-left:4px solid {t['renk']};
                         border:1px solid {t['renk']}20">
                <div style="display:flex;align-items:flex-start;gap:12px">
                    <div style="font-size:1.5rem;min-width:30px">{t['ikon']}</div>
                    <div>
                        <div style="font-weight:700;color:#e0e7ff !important;font-size:0.9rem;margin-bottom:4px">{t['baslik']}</div>
                        <div style="color:#94a3b8 !important;font-size:0.83rem;line-height:1.5">{t['mesaj']}</div>
                    </div>
                </div>
            </div>
            """)

    elif toplam_soru == 0:
        st.info("Henüz hiçbir DGS modülünü denemediniz. Yukarıdaki sekmelerden başlayın!")


# ══════════════════════════════════════════════════════════════════════════════
# CARPIM YARISI (Multiplication Speed Race)
# ══════════════════════════════════════════════════════════════════════════════

def _render_carpim_yarisi():
    """Carpim tablosu hiz yarisi — interaktif carpma oyunu."""
    styled_section("Carpim Tablosu Hiz Yarisi", "#f59e0b")

    _render_html("""
    <div class="mat-hero" style="background:linear-gradient(135deg,#78350f 0%,#b45309 50%,#d97706 100%);padding:20px;margin-bottom:16px">
        <h1 style="font-size:1.5rem !important">&#9889; Carpim Tablosu Hiz Yarisi</h1>
        <p>Carpim tablosunu ne kadar hizli biliyorsun? Zamana karsi yaris!</p>
    </div>
    """)

    # --- Session state baslat ---
    if "mat_cy_active" not in st.session_state:
        st.session_state["mat_cy_active"] = False
    if "mat_cy_questions" not in st.session_state:
        st.session_state["mat_cy_questions"] = []
    if "mat_cy_current" not in st.session_state:
        st.session_state["mat_cy_current"] = 0
    if "mat_cy_correct" not in st.session_state:
        st.session_state["mat_cy_correct"] = 0
    if "mat_cy_wrong" not in st.session_state:
        st.session_state["mat_cy_wrong"] = 0
    if "mat_cy_start_time" not in st.session_state:
        st.session_state["mat_cy_start_time"] = None
    if "mat_cy_end_time" not in st.session_state:
        st.session_state["mat_cy_end_time"] = None
    if "mat_cy_streak" not in st.session_state:
        st.session_state["mat_cy_streak"] = 0
    if "mat_cy_best_streak" not in st.session_state:
        st.session_state["mat_cy_best_streak"] = 0
    if "mat_cy_personal_best" not in st.session_state:
        st.session_state["mat_cy_personal_best"] = {}
    if "mat_cy_leaderboard" not in st.session_state:
        st.session_state["mat_cy_leaderboard"] = []
    if "mat_cy_last_feedback" not in st.session_state:
        st.session_state["mat_cy_last_feedback"] = None
    if "mat_cy_answers_log" not in st.session_state:
        st.session_state["mat_cy_answers_log"] = []

    def _generate_questions(table_choice, difficulty, count=20):
        """Soru listesi olustur."""
        questions = []
        for _ in range(count):
            if difficulty == "Kolay":
                if table_choice == "Karisik":
                    a = random.randint(2, 9)
                else:
                    a = table_choice
                b = random.randint(2, 9)
            elif difficulty == "Orta":
                if table_choice == "Karisik":
                    a = random.randint(2, 12)
                else:
                    a = table_choice
                b = random.randint(10, 99)
            else:  # Zor
                if table_choice == "Karisik":
                    a = random.randint(2, 12)
                else:
                    a = table_choice
                b = random.randint(100, 999)
            questions.append({"a": a, "b": b, "answer": a * b})
        return questions

    # --- Yaris ayarlari ---
    if not st.session_state["mat_cy_active"] and st.session_state["mat_cy_end_time"] is None:
        col1, col2, col3 = st.columns(3)
        with col1:
            table_options = ["Karisik"] + list(range(2, 13))
            table_choice = st.selectbox(
                "Carpim Tablosu",
                table_options,
                key="mat_cy_table_select",
                help="Belirli bir tabloyu sec veya Karisik modda calis"
            )
        with col2:
            difficulty = st.selectbox(
                "Zorluk",
                ["Kolay", "Orta", "Zor"],
                key="mat_cy_difficulty_select",
                help="Kolay: tek hane | Orta: cift hane | Zor: uc hane"
            )
        with col3:
            q_count = st.selectbox(
                "Soru Sayisi",
                [10, 20, 30, 50],
                index=1,
                key="mat_cy_count_select"
            )

        # Zorluk aciklamasi
        diff_info = {
            "Kolay": ("2-9 arasi tek haneli sayilar", "#22c55e"),
            "Orta": ("10-99 arasi cift haneli sayilar", "#f59e0b"),
            "Zor": ("100-999 arasi uc haneli sayilar", "#ef4444"),
        }
        info_text, info_color = diff_info[difficulty]
        _render_html(f"""
        <div style="background:{info_color}15;border-radius:12px;padding:12px 16px;margin:8px 0 16px;
                     border-left:4px solid {info_color}">
            <span style="color:#e0e7ff !important;font-size:0.85rem">
                <strong>{difficulty}:</strong> {info_text}
            </span>
        </div>
        """)

        # Personal best goster
        pb_key = f"{table_choice}_{difficulty}_{q_count}"
        if pb_key in st.session_state["mat_cy_personal_best"]:
            pb = st.session_state["mat_cy_personal_best"][pb_key]
            _render_html(f"""
            <div class="mat-stat-card" style="padding:14px;margin-bottom:16px;
                         background:linear-gradient(135deg,#064e3b,#065f46)">
                <div style="color:#6ee7b7 !important;font-size:0.8rem;margin-bottom:4px">
                    &#127942; Kisisel Rekor ({table_choice} | {difficulty} | {q_count} soru)
                </div>
                <div style="color:#ecfdf5 !important;font-size:1.3rem;font-weight:800">
                    {pb['time']:.1f}s - %{pb['accuracy']:.0f} dogruluk
                </div>
            </div>
            """)

        if st.button("&#9889; Yarisi Baslat!", key="mat_cy_start_btn", use_container_width=True):
            t_val = table_choice if table_choice != "Karisik" else "Karisik"
            st.session_state["mat_cy_questions"] = _generate_questions(
                t_val if t_val == "Karisik" else int(t_val), difficulty, q_count
            )
            st.session_state["mat_cy_active"] = True
            st.session_state["mat_cy_current"] = 0
            st.session_state["mat_cy_correct"] = 0
            st.session_state["mat_cy_wrong"] = 0
            st.session_state["mat_cy_start_time"] = time.time()
            st.session_state["mat_cy_end_time"] = None
            st.session_state["mat_cy_streak"] = 0
            st.session_state["mat_cy_best_streak"] = 0
            st.session_state["mat_cy_last_feedback"] = None
            st.session_state["mat_cy_answers_log"] = []
            st.session_state["mat_cy_settings"] = {
                "table": table_choice, "difficulty": difficulty, "count": q_count
            }
            st.rerun()

    # --- Aktif yaris ---
    elif st.session_state["mat_cy_active"]:
        questions = st.session_state["mat_cy_questions"]
        idx = st.session_state["mat_cy_current"]
        total = len(questions)
        elapsed = time.time() - st.session_state["mat_cy_start_time"]

        # Ust bilgi cubugu
        progress = idx / total
        correct = st.session_state["mat_cy_correct"]
        wrong = st.session_state["mat_cy_wrong"]
        streak = st.session_state["mat_cy_streak"]

        _render_html(f"""
        <div style="display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap">
            <div class="mat-stat-card" style="flex:1;min-width:80px;padding:10px">
                <div style="font-size:0.7rem;color:#94a3b8 !important">Soru</div>
                <div style="font-size:1.2rem;font-weight:800;color:#818cf8 !important">{idx + 1}/{total}</div>
            </div>
            <div class="mat-stat-card" style="flex:1;min-width:80px;padding:10px">
                <div style="font-size:0.7rem;color:#94a3b8 !important">Sure</div>
                <div style="font-size:1.2rem;font-weight:800;color:#f59e0b !important">{elapsed:.1f}s</div>
            </div>
            <div class="mat-stat-card" style="flex:1;min-width:80px;padding:10px">
                <div style="font-size:0.7rem;color:#94a3b8 !important">Dogru</div>
                <div style="font-size:1.2rem;font-weight:800;color:#22c55e !important">{correct}</div>
            </div>
            <div class="mat-stat-card" style="flex:1;min-width:80px;padding:10px">
                <div style="font-size:0.7rem;color:#94a3b8 !important">Yanlis</div>
                <div style="font-size:1.2rem;font-weight:800;color:#ef4444 !important">{wrong}</div>
            </div>
            <div class="mat-stat-card" style="flex:1;min-width:80px;padding:10px;
                         background:linear-gradient(135deg,#7c2d12,#9a3412)">
                <div style="font-size:0.7rem;color:#fed7aa !important">Seri</div>
                <div style="font-size:1.2rem;font-weight:800;color:#fb923c !important">&#128293; {streak}</div>
            </div>
        </div>
        """)

        # Progress bar
        _render_html(f"""
        <div style="background:#1e1b4b;border-radius:8px;height:8px;margin-bottom:16px;overflow:hidden">
            <div style="background:linear-gradient(90deg,#818cf8,#6366f1);height:100%;width:{progress * 100:.1f}%;
                         border-radius:8px;transition:width 0.3s ease"></div>
        </div>
        """)

        # Son cevap feedback
        fb = st.session_state["mat_cy_last_feedback"]
        if fb is not None:
            if fb["correct"]:
                _render_html(f"""
                <div style="background:#052e1615;border:2px solid #22c55e40;border-radius:14px;padding:12px 16px;
                             margin-bottom:12px;text-align:center">
                    <span style="font-size:1.3rem">&#9989;</span>
                    <span style="color:#22c55e !important;font-weight:700;font-size:1rem;margin-left:8px">
                        Dogru! {fb['a']} x {fb['b']} = {fb['answer']}
                    </span>
                </div>
                """)
            else:
                _render_html(f"""
                <div style="background:#450a0a15;border:2px solid #ef444440;border-radius:14px;padding:12px 16px;
                             margin-bottom:12px;text-align:center">
                    <span style="font-size:1.3rem">&#10060;</span>
                    <span style="color:#ef4444 !important;font-weight:700;font-size:1rem;margin-left:8px">
                        Yanlis! {fb['a']} x {fb['b']} = {fb['answer']} (senin cevabin: {fb['given']})
                    </span>
                </div>
                """)

        if idx < total:
            q = questions[idx]
            # Soru gosterimi
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#312e81,#3730a3);border-radius:20px;
                         padding:32px;text-align:center;margin-bottom:16px;
                         border:2px solid rgba(129,140,248,0.3)">
                <div style="font-size:2.8rem;font-weight:900;color:#e0e7ff !important;letter-spacing:4px">
                    {q['a']} &#215; {q['b']} = ?
                </div>
            </div>
            """)

            col_input, col_btn = st.columns([3, 1])
            with col_input:
                user_answer = st.text_input(
                    "Cevabin",
                    key=f"mat_cy_input_{idx}",
                    placeholder="Sonucu yaz...",
                    label_visibility="collapsed"
                )
            with col_btn:
                submit = st.button("Gonder ➜", key=f"mat_cy_submit_{idx}", use_container_width=True)

            if submit and user_answer.strip():
                try:
                    given = int(user_answer.strip())
                except ValueError:
                    st.warning("Lutfen gecerli bir sayi girin!")
                    return

                is_correct = (given == q["answer"])
                st.session_state["mat_cy_answers_log"].append({
                    "a": q["a"], "b": q["b"], "answer": q["answer"],
                    "given": given, "correct": is_correct
                })

                if is_correct:
                    st.session_state["mat_cy_correct"] += 1
                    st.session_state["mat_cy_streak"] += 1
                    if st.session_state["mat_cy_streak"] > st.session_state["mat_cy_best_streak"]:
                        st.session_state["mat_cy_best_streak"] = st.session_state["mat_cy_streak"]
                else:
                    st.session_state["mat_cy_wrong"] += 1
                    st.session_state["mat_cy_streak"] = 0

                st.session_state["mat_cy_last_feedback"] = {
                    "correct": is_correct, "a": q["a"], "b": q["b"],
                    "answer": q["answer"], "given": given
                }
                st.session_state["mat_cy_current"] += 1

                # Son soru mu?
                if st.session_state["mat_cy_current"] >= total:
                    st.session_state["mat_cy_active"] = False
                    st.session_state["mat_cy_end_time"] = time.time()

                st.rerun()

        # Yarisi birak butonu
        if st.button("&#9898; Yarisi Birak", key="mat_cy_cancel_btn"):
            st.session_state["mat_cy_active"] = False
            st.session_state["mat_cy_end_time"] = None
            st.session_state["mat_cy_last_feedback"] = None
            st.rerun()

    # --- Sonuc ekrani ---
    elif st.session_state["mat_cy_end_time"] is not None:
        total_time = st.session_state["mat_cy_end_time"] - st.session_state["mat_cy_start_time"]
        correct = st.session_state["mat_cy_correct"]
        wrong = st.session_state["mat_cy_wrong"]
        total = len(st.session_state["mat_cy_questions"])
        accuracy = (correct / total * 100) if total > 0 else 0
        best_streak = st.session_state["mat_cy_best_streak"]
        avg_time = total_time / total if total > 0 else 0

        # Performans degerlendirmesi
        if accuracy >= 95 and avg_time < 3:
            perf_emoji, perf_text, perf_color = "&#127775;", "Muhtesem! Isik hizinda!", "#f59e0b"
        elif accuracy >= 85:
            perf_emoji, perf_text, perf_color = "&#128640;", "Harika performans!", "#22c55e"
        elif accuracy >= 70:
            perf_emoji, perf_text, perf_color = "&#128170;", "Iyi gidiyorsun!", "#3b82f6"
        else:
            perf_emoji, perf_text, perf_color = "&#128218;", "Biraz daha pratik gerekiyor", "#f59e0b"

        _render_html(f"""
        <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:20px;
                     padding:28px;text-align:center;margin-bottom:20px;
                     border:2px solid {perf_color}40">
            <div style="font-size:3rem;margin-bottom:8px">{perf_emoji}</div>
            <div style="font-size:1.4rem;font-weight:800;color:{perf_color} !important;margin-bottom:4px">
                {perf_text}
            </div>
            <div style="font-size:0.85rem;color:#94a3b8 !important">Yaris Tamamlandi!</div>
        </div>
        """)

        cols = st.columns(5)
        result_stats = [
            ("&#9201;", f"{total_time:.1f}s", "Toplam Sure"),
            ("&#9989;", str(correct), "Dogru"),
            ("&#10060;", str(wrong), "Yanlis"),
            ("&#127919;", f"%{accuracy:.0f}", "Dogruluk"),
            ("&#128293;", str(best_streak), "En Iyi Seri"),
        ]
        for col, (icon, val, label) in zip(cols, result_stats):
            with col:
                _render_html(f"""
                <div class="mat-stat-card" style="padding:12px">
                    <div style="font-size:1.2rem">{icon}</div>
                    <div style="font-size:1.2rem;font-weight:800;color:#818cf8 !important">{val}</div>
                    <div style="font-size:0.65rem;color:#94a3b8 !important">{label}</div>
                </div>
                """)

        # Ortalama sure
        _render_html(f"""
        <div style="background:#1e1b4b;border-radius:14px;padding:14px;text-align:center;margin:12px 0;
                     border:1px solid rgba(129,140,248,0.2)">
            <span style="color:#94a3b8 !important;font-size:0.85rem">Soru basina ortalama: </span>
            <span style="color:#818cf8 !important;font-weight:800;font-size:1.1rem">{avg_time:.2f}s</span>
        </div>
        """)

        # Personal best guncelle
        settings = st.session_state.get("mat_cy_settings", {})
        pb_key = f"{settings.get('table', '')}_{settings.get('difficulty', '')}_{settings.get('count', '')}"
        current_pb = st.session_state["mat_cy_personal_best"].get(pb_key)
        is_new_record = False
        if current_pb is None or (accuracy >= current_pb["accuracy"] and total_time < current_pb["time"]):
            st.session_state["mat_cy_personal_best"][pb_key] = {
                "time": total_time, "accuracy": accuracy,
                "correct": correct, "total": total
            }
            is_new_record = current_pb is not None

        if is_new_record:
            _render_html("""
            <div style="background:linear-gradient(135deg,#854d0e,#a16207);border-radius:14px;
                         padding:14px;text-align:center;margin:12px 0;
                         border:2px solid #eab30840">
                <span style="font-size:1.3rem">&#127942;</span>
                <span style="color:#fef3c7 !important;font-weight:800;font-size:1rem;margin-left:8px">
                    YENI KISISEL REKOR!
                </span>
            </div>
            """)

        # Leaderboard guncelle
        st.session_state["mat_cy_leaderboard"].append({
            "time": total_time, "accuracy": accuracy, "correct": correct,
            "total": total, "difficulty": settings.get("difficulty", ""),
            "table": settings.get("table", ""), "timestamp": datetime.now().isoformat()
        })
        st.session_state["mat_cy_leaderboard"].sort(
            key=lambda x: (-x["accuracy"], x["time"])
        )
        st.session_state["mat_cy_leaderboard"] = st.session_state["mat_cy_leaderboard"][:20]

        # Yanlis cevaplar tablosu
        wrong_answers = [a for a in st.session_state["mat_cy_answers_log"] if not a["correct"]]
        if wrong_answers:
            styled_section("Yanlis Cevaplarin", "#ef4444")
            for wa in wrong_answers:
                _render_html(f"""
                <div style="background:#450a0a15;border-radius:10px;padding:10px 14px;margin-bottom:6px;
                             border-left:3px solid #ef4444;display:flex;justify-content:space-between;align-items:center">
                    <span style="color:#fca5a5 !important;font-size:0.9rem">
                        {wa['a']} x {wa['b']} = <strong>{wa['answer']}</strong>
                    </span>
                    <span style="color:#94a3b8 !important;font-size:0.8rem">
                        Senin cevabin: {wa['given']}
                    </span>
                </div>
                """)

        # Leaderboard
        if st.session_state["mat_cy_leaderboard"]:
            styled_section("Skor Tablosu", "#a855f7")
            for i, entry in enumerate(st.session_state["mat_cy_leaderboard"][:10]):
                rank_icon = ["&#129351;", "&#129352;", "&#129353;"][i] if i < 3 else f"#{i+1}"
                _render_html(f"""
                <div style="background:{'linear-gradient(135deg,#1e1b4b,#312e81)' if i < 3 else '#1e1b4b'};
                             border-radius:10px;padding:10px 14px;margin-bottom:4px;
                             border:1px solid rgba(168,85,247,{0.3 if i < 3 else 0.1});
                             display:flex;justify-content:space-between;align-items:center">
                    <span style="color:#e0e7ff !important;font-size:0.9rem">
                        {rank_icon} &nbsp; {entry['difficulty']} | Tablo: {entry['table']}
                    </span>
                    <span style="color:#a5b4fc !important;font-size:0.85rem">
                        {entry['time']:.1f}s | %{entry['accuracy']:.0f} | {entry['correct']}/{entry['total']}
                    </span>
                </div>
                """)

        # Tekrar oyna butonu
        if st.button("&#9889; Tekrar Oyna!", key="mat_cy_replay_btn", use_container_width=True):
            st.session_state["mat_cy_active"] = False
            st.session_state["mat_cy_end_time"] = None
            st.session_state["mat_cy_current"] = 0
            st.session_state["mat_cy_last_feedback"] = None
            st.session_state["mat_cy_answers_log"] = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# KESIR LAB (Fraction Visualization)
# ══════════════════════════════════════════════════════════════════════════════

def _render_kesir_lab():
    """Kesir gorsellestime laboratuvari."""
    styled_section("Kesir Laboratuvari", "#ec4899")

    _render_html("""
    <div class="mat-hero" style="background:linear-gradient(135deg,#831843 0%,#be185d 50%,#ec4899 100%);padding:20px;margin-bottom:16px">
        <h1 style="font-size:1.5rem !important">&#127829; Kesir Laboratuvari</h1>
        <p>Kesirleri gorsellerle ogren, topla ve oyun oyna!</p>
    </div>
    """)

    sub_tabs = st.tabs(["&#127829; Kesir Goster", "&#10133; Kesir Toplama", "&#127922; Kesir Oyunu"])

    # ═══ Sub-tab A: Kesir Goster ═══
    with sub_tabs[0]:
        _render_kesir_goster()

    # ═══ Sub-tab B: Kesir Toplama ═══
    with sub_tabs[1]:
        _render_kesir_toplama()

    # ═══ Sub-tab C: Kesir Oyunu ═══
    with sub_tabs[2]:
        _render_kesir_oyunu()


def _gcd(a: int, b: int) -> int:
    """En buyuk ortak bolen."""
    while b:
        a, b = b, a % b
    return a


def _simplify(pay: int, payda: int):
    """Kesri sadeler, (pay, payda) doner."""
    if payda == 0:
        return pay, 1
    g = _gcd(abs(pay), abs(payda))
    return pay // g, payda // g


def _pizza_css(pay: int, payda: int, size: int = 160, label: str = ""):
    """CSS conic-gradient ile pizza/pie chart HTML olustur."""
    if payda == 0:
        payda = 1
    fraction = min(pay / payda, 1.0)
    degrees = fraction * 360
    # Renk
    fill_color = "#818cf8"
    bg_color = "#1e1b4b"
    border_color = "#6366f1"

    label_html = f'<div style="color:#94a3b8 !important;font-size:0.75rem;margin-top:6px">{label}</div>' if label else ""

    return f"""
    <div style="text-align:center;display:inline-block;margin:8px">
        <div style="width:{size}px;height:{size}px;border-radius:50%;
                     background:conic-gradient({fill_color} 0deg, {fill_color} {degrees:.1f}deg,
                     {bg_color} {degrees:.1f}deg, {bg_color} 360deg);
                     border:3px solid {border_color};margin:0 auto;
                     box-shadow:0 4px 15px rgba(99,102,241,0.2)">
        </div>
        <div style="color:#e0e7ff !important;font-weight:800;font-size:1.1rem;margin-top:8px">{pay}/{payda}</div>
        {label_html}
    </div>
    """


def _bar_css(pay: int, payda: int, width: int = 200, height: int = 30):
    """CSS linear-gradient ile bar chart HTML olustur."""
    if payda == 0:
        payda = 1
    fraction = min(pay / payda, 1.0)
    pct = fraction * 100

    return f"""
    <div style="text-align:center;margin:8px 0">
        <div style="width:{width}px;height:{height}px;background:#1e1b4b;border-radius:8px;
                     overflow:hidden;border:1px solid #6366f140;margin:0 auto;position:relative">
            <div style="width:{pct:.1f}%;height:100%;background:linear-gradient(90deg,#818cf8,#6366f1);
                         border-radius:8px;transition:width 0.5s ease"></div>
            <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                         color:#e0e7ff !important;font-size:0.75rem;font-weight:700">{pay}/{payda}</div>
        </div>
    </div>
    """


def _render_kesir_goster():
    """Kesir Goster alt sekmesi."""
    styled_section("Kesir Gorsellesir", "#818cf8")

    col1, col2 = st.columns(2)
    with col1:
        pay = st.slider("Pay (Ust sayi)", 0, 24, 3, key="mat_kl_pay")
    with col2:
        payda = st.slider("Payda (Alt sayi)", 1, 12, 4, key="mat_kl_payda")

    # Gorsel: Pizza + Bar
    col_pizza, col_bar = st.columns(2)
    with col_pizza:
        _render_html(f"""
        <div style="background:#0f0c2990;border-radius:16px;padding:20px;text-align:center;
                     border:1px solid rgba(129,140,248,0.2)">
            <div style="color:#a5b4fc !important;font-size:0.8rem;margin-bottom:8px;font-weight:600">PIZZA GOSTERIM</div>
            {_pizza_css(min(pay, payda), payda, 160)}
        </div>
        """)
    with col_bar:
        _render_html(f"""
        <div style="background:#0f0c2990;border-radius:16px;padding:20px;text-align:center;
                     border:1px solid rgba(129,140,248,0.2)">
            <div style="color:#a5b4fc !important;font-size:0.8rem;margin-bottom:12px;font-weight:600">CUBUK GOSTERIM</div>
            {_bar_css(min(pay, payda * 2), payda, 240, 36)}
            <div style="margin-top:12px">
        """)

        # Dilimler gosterimi (parcali bar)
        slices_html = ""
        for i in range(payda):
            filled = i < pay
            color = "#818cf8" if filled else "#1e1b4b"
            border = "#6366f140"
            slices_html += f'<div style="display:inline-block;width:{min(28, 200 // payda)}px;height:28px;background:{color};border:1px solid {border};margin:1px;border-radius:3px"></div>'

        _render_html(f"""
            <div style="margin-top:4px">{slices_html}</div>
            </div>
        </div>
        """)

    # Bilgi kartlari
    decimal_val = pay / payda if payda > 0 else 0
    percentage = decimal_val * 100
    tam = pay // payda
    kalan_pay = pay % payda
    s_pay, s_payda = _simplify(pay, payda)
    mixed_str = f"{tam} tam {kalan_pay}/{payda}" if tam > 0 and kalan_pay > 0 else (f"{tam}" if kalan_pay == 0 and tam > 0 else f"{pay}/{payda}")

    info_items = [
        ("&#128290;", f"{pay}/{payda}", "Kesir"),
        ("&#128178;", f"{decimal_val:.4f}", "Ondalik"),
        ("%", f"%{percentage:.1f}", "Yuzde"),
        ("&#128256;", f"{s_pay}/{s_payda}", "Sadeles"),
        ("&#127856;", mixed_str, "Bileik Sayi"),
    ]
    cols = st.columns(5)
    for col, (icon, val, label) in zip(cols, info_items):
        with col:
            _render_html(f"""
            <div class="mat-stat-card" style="padding:10px">
                <div style="font-size:1rem">{icon}</div>
                <div style="font-size:0.95rem;font-weight:800;color:#818cf8 !important">{val}</div>
                <div style="font-size:0.6rem;color:#94a3b8 !important">{label}</div>
            </div>
            """)


def _render_kesir_toplama():
    """Kesir Toplama alt sekmesi."""
    styled_section("Kesir Toplama", "#22c55e")

    _render_html("""
    <div style="background:#052e1615;border-radius:12px;padding:12px 16px;margin-bottom:16px;
                 border-left:4px solid #22c55e">
        <span style="color:#86efac !important;font-size:0.85rem">
            Iki kesri toplayalim! Sonucu gorsel olarak inceleyin.
        </span>
    </div>
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pay1 = st.number_input("Pay 1", min_value=0, max_value=24, value=1, key="mat_kt_pay1")
    with col2:
        payda1 = st.number_input("Payda 1", min_value=1, max_value=12, value=3, key="mat_kt_payda1")
    with col3:
        pay2 = st.number_input("Pay 2", min_value=0, max_value=24, value=1, key="mat_kt_pay2")
    with col4:
        payda2 = st.number_input("Payda 2", min_value=1, max_value=12, value=4, key="mat_kt_payda2")

    # Hesaplama
    ortak_payda = payda1 * payda2 // _gcd(payda1, payda2)  # EKOK
    yeni_pay1 = pay1 * (ortak_payda // payda1)
    yeni_pay2 = pay2 * (ortak_payda // payda2)
    sonuc_pay = yeni_pay1 + yeni_pay2
    sonuc_payda = ortak_payda
    s_pay, s_payda = _simplify(sonuc_pay, sonuc_payda)

    # Gorsel: 3 pizza
    _render_html(f"""
    <div style="background:#0f0c2990;border-radius:16px;padding:20px;text-align:center;margin:16px 0;
                 border:1px solid rgba(129,140,248,0.2);display:flex;justify-content:center;align-items:center;
                 flex-wrap:wrap;gap:12px">
        {_pizza_css(min(pay1, payda1), payda1, 120, f"{pay1}/{payda1}")}
        <div style="font-size:2rem;color:#818cf8 !important;font-weight:900;padding:0 8px">+</div>
        {_pizza_css(min(pay2, payda2), payda2, 120, f"{pay2}/{payda2}")}
        <div style="font-size:2rem;color:#818cf8 !important;font-weight:900;padding:0 8px">=</div>
        {_pizza_css(min(s_pay, s_payda), s_payda, 140, f"{s_pay}/{s_payda}")}
    </div>
    """)

    # Adim adim cozum
    styled_section("Adim Adim Cozum", "#f59e0b")

    steps = [
        ("1. Paydalar esitlenir", f"EKOK({payda1}, {payda2}) = {ortak_payda}"),
        ("2. Paylar genisletilir", f"{pay1}/{payda1} = {yeni_pay1}/{ortak_payda} &nbsp;&nbsp; {pay2}/{payda2} = {yeni_pay2}/{ortak_payda}"),
        ("3. Paylar toplanir", f"{yeni_pay1}/{ortak_payda} + {yeni_pay2}/{ortak_payda} = {sonuc_pay}/{sonuc_payda}"),
    ]
    if (sonuc_pay, sonuc_payda) != (s_pay, s_payda):
        steps.append(("4. Sadelesirir", f"{sonuc_pay}/{sonuc_payda} = {s_pay}/{s_payda}"))

    for i, (step_title, step_detail) in enumerate(steps):
        step_color = ["#818cf8", "#a855f7", "#22c55e", "#f59e0b"][i % 4]
        _render_html(f"""
        <div style="background:linear-gradient(135deg,{step_color}08,{step_color}04);
                     border-radius:12px;padding:12px 16px;margin-bottom:8px;
                     border-left:4px solid {step_color}">
            <div style="color:#e0e7ff !important;font-weight:700;font-size:0.85rem">{step_title}</div>
            <div style="color:#a5b4fc !important;font-size:1rem;font-weight:600;margin-top:4px">{step_detail}</div>
        </div>
        """)

    # Sonuc karti
    decimal_result = s_pay / s_payda if s_payda > 0 else 0
    _render_html(f"""
    <div style="background:linear-gradient(135deg,#064e3b,#065f46);border-radius:16px;
                 padding:18px;text-align:center;margin-top:16px;border:2px solid #22c55e40">
        <div style="color:#6ee7b7 !important;font-size:0.8rem;margin-bottom:6px">SONUC</div>
        <div style="color:#ecfdf5 !important;font-size:1.8rem;font-weight:900">
            {s_pay}/{s_payda}
        </div>
        <div style="color:#86efac !important;font-size:0.85rem;margin-top:4px">
            = {decimal_result:.4f} &nbsp; = &nbsp; %{decimal_result * 100:.1f}
        </div>
    </div>
    """)


def _render_kesir_oyunu():
    """Kesir Oyunu alt sekmesi — pizza gorselden kesri tahmin et."""
    styled_section("Kesir Tahmin Oyunu", "#f59e0b")

    # Session state
    if "mat_ko_active" not in st.session_state:
        st.session_state["mat_ko_active"] = False
    if "mat_ko_questions" not in st.session_state:
        st.session_state["mat_ko_questions"] = []
    if "mat_ko_current" not in st.session_state:
        st.session_state["mat_ko_current"] = 0
    if "mat_ko_score" not in st.session_state:
        st.session_state["mat_ko_score"] = 0
    if "mat_ko_start_time" not in st.session_state:
        st.session_state["mat_ko_start_time"] = None
    if "mat_ko_end_time" not in st.session_state:
        st.session_state["mat_ko_end_time"] = None
    if "mat_ko_feedback" not in st.session_state:
        st.session_state["mat_ko_feedback"] = None
    if "mat_ko_total_q" not in st.session_state:
        st.session_state["mat_ko_total_q"] = 10

    def _generate_fraction_questions(count=10):
        """Kesir tahmin sorulari olustur."""
        questions = []
        for _ in range(count):
            payda = random.randint(2, 10)
            pay = random.randint(1, payda)
            correct = (pay, payda)

            # 3 yanlis secenek olustur
            options = [correct]
            attempts = 0
            while len(options) < 4 and attempts < 50:
                w_payda = random.randint(2, 10)
                w_pay = random.randint(1, w_payda)
                candidate = (w_pay, w_payda)
                # Farkli deger olmali
                if candidate not in options and (w_pay / w_payda) != (pay / payda):
                    options.append(candidate)
                attempts += 1
            # Yeterli secenek bulunamadiysa tamamla
            while len(options) < 4:
                fp = random.randint(1, 8)
                fd = random.randint(2, 10)
                if (fp, fd) not in options:
                    options.append((fp, fd))

            random.shuffle(options)
            correct_idx = options.index(correct)
            questions.append({
                "pay": pay, "payda": payda,
                "options": options, "correct_idx": correct_idx
            })
        return questions

    # --- Baslangic ekrani ---
    if not st.session_state["mat_ko_active"] and st.session_state["mat_ko_end_time"] is None:
        _render_html("""
        <div style="background:#0f0c2990;border-radius:16px;padding:20px;text-align:center;margin-bottom:16px;
                     border:1px solid rgba(245,158,11,0.2)">
            <div style="font-size:2.5rem;margin-bottom:8px">&#127829;</div>
            <div style="color:#e0e7ff !important;font-size:1.1rem;font-weight:700;margin-bottom:4px">
                Pizza Kesir Oyunu
            </div>
            <div style="color:#94a3b8 !important;font-size:0.85rem">
                Pizza gorseline bakip hangi kesri gosterdigini tahmin et!
            </div>
        </div>
        """)

        q_count = st.selectbox("Soru sayisi", [5, 10, 15, 20], index=1, key="mat_ko_qcount")

        if st.button("&#127922; Oyunu Baslat!", key="mat_ko_start_btn", use_container_width=True):
            st.session_state["mat_ko_questions"] = _generate_fraction_questions(q_count)
            st.session_state["mat_ko_active"] = True
            st.session_state["mat_ko_current"] = 0
            st.session_state["mat_ko_score"] = 0
            st.session_state["mat_ko_start_time"] = time.time()
            st.session_state["mat_ko_end_time"] = None
            st.session_state["mat_ko_feedback"] = None
            st.session_state["mat_ko_total_q"] = q_count
            st.rerun()

    # --- Aktif oyun ---
    elif st.session_state["mat_ko_active"]:
        questions = st.session_state["mat_ko_questions"]
        idx = st.session_state["mat_ko_current"]
        total = len(questions)
        elapsed = time.time() - st.session_state["mat_ko_start_time"]
        score = st.session_state["mat_ko_score"]

        # Ust bar
        _render_html(f"""
        <div style="display:flex;gap:12px;margin-bottom:12px">
            <div class="mat-stat-card" style="flex:1;padding:8px">
                <div style="font-size:0.65rem;color:#94a3b8 !important">Soru</div>
                <div style="font-size:1.1rem;font-weight:800;color:#818cf8 !important">{idx + 1}/{total}</div>
            </div>
            <div class="mat-stat-card" style="flex:1;padding:8px">
                <div style="font-size:0.65rem;color:#94a3b8 !important">Puan</div>
                <div style="font-size:1.1rem;font-weight:800;color:#22c55e !important">{score}</div>
            </div>
            <div class="mat-stat-card" style="flex:1;padding:8px">
                <div style="font-size:0.65rem;color:#94a3b8 !important">Sure</div>
                <div style="font-size:1.1rem;font-weight:800;color:#f59e0b !important">{elapsed:.0f}s</div>
            </div>
        </div>
        """)

        # Feedback
        fb = st.session_state["mat_ko_feedback"]
        if fb is not None:
            if fb["correct"]:
                _render_html(f"""
                <div style="background:#052e1615;border:2px solid #22c55e40;border-radius:12px;
                             padding:10px;text-align:center;margin-bottom:12px">
                    <span style="color:#22c55e !important;font-weight:700">&#9989; Dogru! {fb['pay']}/{fb['payda']}</span>
                </div>
                """)
            else:
                _render_html(f"""
                <div style="background:#450a0a15;border:2px solid #ef444440;border-radius:12px;
                             padding:10px;text-align:center;margin-bottom:12px">
                    <span style="color:#ef4444 !important;font-weight:700">&#10060; Yanlis! Dogru cevap: {fb['pay']}/{fb['payda']}</span>
                </div>
                """)

        if idx < total:
            q = questions[idx]

            # Pizza gorseli
            _render_html(f"""
            <div style="background:linear-gradient(135deg,#312e81,#3730a3);border-radius:20px;
                         padding:24px;text-align:center;margin-bottom:16px;
                         border:2px solid rgba(129,140,248,0.3)">
                <div style="color:#a5b4fc !important;font-size:0.8rem;margin-bottom:8px">Bu pizza hangi kesri gosteriyor?</div>
                {_pizza_css(q['pay'], q['payda'], 180)}
            </div>
            """)

            # 4 secenek butonu
            opt_cols = st.columns(4)
            for i, (opt_pay, opt_payda) in enumerate(q["options"]):
                with opt_cols[i]:
                    btn_label = f"{opt_pay}/{opt_payda}"
                    if st.button(btn_label, key=f"mat_ko_opt_{idx}_{i}", use_container_width=True):
                        is_correct = (i == q["correct_idx"])
                        if is_correct:
                            st.session_state["mat_ko_score"] += 1

                        st.session_state["mat_ko_feedback"] = {
                            "correct": is_correct,
                            "pay": q["pay"], "payda": q["payda"]
                        }
                        st.session_state["mat_ko_current"] += 1

                        if st.session_state["mat_ko_current"] >= total:
                            st.session_state["mat_ko_active"] = False
                            st.session_state["mat_ko_end_time"] = time.time()

                        st.rerun()

    # --- Sonuc ekrani ---
    elif st.session_state["mat_ko_end_time"] is not None:
        total_time = st.session_state["mat_ko_end_time"] - st.session_state["mat_ko_start_time"]
        score = st.session_state["mat_ko_score"]
        total = st.session_state["mat_ko_total_q"]
        accuracy = (score / total * 100) if total > 0 else 0

        if accuracy >= 90:
            perf_emoji, perf_text = "&#127775;", "Kesir Ustasi!"
        elif accuracy >= 70:
            perf_emoji, perf_text = "&#128640;", "Harika!"
        elif accuracy >= 50:
            perf_emoji, perf_text = "&#128170;", "Iyi gidiyor!"
        else:
            perf_emoji, perf_text = "&#128218;", "Biraz daha pratik!"

        _render_html(f"""
        <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:20px;
                     padding:28px;text-align:center;margin-bottom:20px;
                     border:2px solid #f59e0b40">
            <div style="font-size:3rem;margin-bottom:8px">{perf_emoji}</div>
            <div style="font-size:1.4rem;font-weight:800;color:#f59e0b !important;margin-bottom:4px">{perf_text}</div>
            <div style="font-size:0.85rem;color:#94a3b8 !important">Oyun Tamamlandi!</div>
        </div>
        """)

        cols = st.columns(3)
        result_stats = [
            ("&#9989;", f"{score}/{total}", "Dogru"),
            ("&#127919;", f"%{accuracy:.0f}", "Dogruluk"),
            ("&#9201;", f"{total_time:.1f}s", "Sure"),
        ]
        for col, (icon, val, label) in zip(cols, result_stats):
            with col:
                _render_html(f"""
                <div class="mat-stat-card" style="padding:12px">
                    <div style="font-size:1.2rem">{icon}</div>
                    <div style="font-size:1.2rem;font-weight:800;color:#818cf8 !important">{val}</div>
                    <div style="font-size:0.65rem;color:#94a3b8 !important">{label}</div>
                </div>
                """)

        if st.button("&#127922; Tekrar Oyna!", key="mat_ko_replay_btn", use_container_width=True):
            st.session_state["mat_ko_active"] = False
            st.session_state["mat_ko_end_time"] = None
            st.session_state["mat_ko_current"] = 0
            st.session_state["mat_ko_score"] = 0
            st.session_state["mat_ko_feedback"] = None
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# 15) LGS / YKS SORU BANKASI
# ══════════════════════════════════════════════════════════════════════════════

def _lgs_sorulari():
    """500 LGS Matematik sorusu (8. Sinif) - 10 konu x 50 soru."""
    try:
        from data.lgs_sorulari import LGS_SORU_HAVUZU
        return LGS_SORU_HAVUZU
    except ImportError:
        pass
    return [
        # --- Carpanlar ve Katlar (5) ---
        {"soru": "36 ve 48 sayilarinin EBOB'u kactir?", "secenekler": ["A) 6", "B) 12", "C) 18", "D) 24"], "cevap": 1, "konu": "Carpanlar-Katlar", "aciklama": "36 = 2^2 x 3^2, 48 = 2^4 x 3. EBOB = 2^2 x 3 = 12."},
        {"soru": "12, 18 ve 24 sayilarinin EKOK'u kactir?", "secenekler": ["A) 36", "B) 48", "C) 72", "D) 96"], "cevap": 2, "konu": "Carpanlar-Katlar", "aciklama": "12=2^2x3, 18=2x3^2, 24=2^3x3. EKOK=2^3x3^2=72."},
        {"soru": "Bir sayinin hem 6'nin hem 8'in kati olabilmesi icin en kucuk pozitif deger kactir?", "secenekler": ["A) 12", "B) 24", "C) 36", "D) 48"], "cevap": 1, "konu": "Carpanlar-Katlar", "aciklama": "EKOK(6,8) = 24. En kucuk ortak kat 24'tur."},
        {"soru": "120 sayisinin pozitif bolen sayisi kactir?", "secenekler": ["A) 12", "B) 14", "C) 16", "D) 18"], "cevap": 2, "konu": "Carpanlar-Katlar", "aciklama": "120=2^3x3x5. Bolen sayisi=(3+1)(1+1)(1+1)=16."},
        {"soru": "Ardisik uc dogal sayinin toplami 75 ise en buyugu kactir?", "secenekler": ["A) 24", "B) 25", "C) 26", "D) 27"], "cevap": 2, "konu": "Carpanlar-Katlar", "aciklama": "n-1+n+n+1=3n=75, n=25. En buyuk: 26."},
        # --- Uslu Sayilar (5) ---
        {"soru": "2^8 ifadesinin degeri kactir?", "secenekler": ["A) 64", "B) 128", "C) 256", "D) 512"], "cevap": 2, "konu": "Uslu Sayilar", "aciklama": "2^8 = 256."},
        {"soru": "3^4 + 3^4 + 3^4 ifadesi asagidakilerden hangisine esittir?", "secenekler": ["A) 3^5", "B) 3^12", "C) 9^4", "D) 3^8"], "cevap": 0, "konu": "Uslu Sayilar", "aciklama": "3^4+3^4+3^4 = 3 x 3^4 = 3^5."},
        {"soru": "5^3 x 5^2 isleminin sonucu kactir?", "secenekler": ["A) 5^5", "B) 5^6", "C) 25^5", "D) 5^10"], "cevap": 0, "konu": "Uslu Sayilar", "aciklama": "Ayni tabanli uslulerin carpiminda usler toplanir: 5^(3+2)=5^5=3125."},
        {"soru": "(2^3)^2 ifadesinin sonucu kactir?", "secenekler": ["A) 32", "B) 64", "C) 128", "D) 256"], "cevap": 1, "konu": "Uslu Sayilar", "aciklama": "(2^3)^2 = 2^6 = 64."},
        {"soru": "(-2)^5 + (-2)^4 isleminin sonucu kactir?", "secenekler": ["A) -48", "B) -16", "C) 0", "D) 16"], "cevap": 1, "konu": "Uslu Sayilar", "aciklama": "(-2)^5=-32, (-2)^4=16. -32+16=-16."},
        # --- Karekok (5) ---
        {"soru": "Karekok(144) kactir?", "secenekler": ["A) 11", "B) 12", "C) 13", "D) 14"], "cevap": 1, "konu": "Karekok", "aciklama": "12 x 12 = 144, dolayisiyla Karekok(144) = 12."},
        {"soru": "Karekok(50) ifadesi asagidakilerden hangisine esittir?", "secenekler": ["A) 5.Karekok(2)", "B) 2.Karekok(5)", "C) 10.Karekok(5)", "D) 25.Karekok(2)"], "cevap": 0, "konu": "Karekok", "aciklama": "Karekok(50)=Karekok(25x2)=5.Karekok(2)."},
        {"soru": "Karekok(3) x Karekok(12) isleminin sonucu kactir?", "secenekler": ["A) 4", "B) 6", "C) Karekok(15)", "D) 36"], "cevap": 1, "konu": "Karekok", "aciklama": "Karekok(3)xKarekok(12)=Karekok(36)=6."},
        {"soru": "Karekok(72) - Karekok(32) ifadesinin sadelesilmis hali nedir?", "secenekler": ["A) Karekok(2)", "B) 2.Karekok(2)", "C) Karekok(40)", "D) 4.Karekok(2)"], "cevap": 1, "konu": "Karekok", "aciklama": "Karekok(72)=6.Karekok(2), Karekok(32)=4.Karekok(2). 6.Karekok(2)-4.Karekok(2)=2.Karekok(2)."},
        {"soru": "2.Karekok(5) ile 3.Karekok(5) sayilarinin toplami kactir?", "secenekler": ["A) 5.Karekok(5)", "B) 6.Karekok(5)", "C) 5.Karekok(10)", "D) Karekok(30)"], "cevap": 0, "konu": "Karekok", "aciklama": "2.Karekok(5)+3.Karekok(5)=5.Karekok(5)."},
        # --- Cebirsel Ifadeler (5) ---
        {"soru": "(x+3)(x-3) ifadesinin acilimi nedir?", "secenekler": ["A) x^2 - 9", "B) x^2 + 9", "C) x^2 - 6x + 9", "D) x^2 + 6x - 9"], "cevap": 0, "konu": "Cebirsel Ifadeler", "aciklama": "(x+3)(x-3) = x^2 - 9 (iki kare farki)."},
        {"soru": "2x + 3 = 11 denkleminde x kactir?", "secenekler": ["A) 3", "B) 4", "C) 5", "D) 6"], "cevap": 1, "konu": "Cebirsel Ifadeler", "aciklama": "2x=11-3=8, x=4."},
        {"soru": "(a+b)^2 aciliminda orta terim nedir?", "secenekler": ["A) ab", "B) 2ab", "C) a^2 + b^2", "D) (ab)^2"], "cevap": 1, "konu": "Cebirsel Ifadeler", "aciklama": "(a+b)^2 = a^2 + 2ab + b^2. Orta terim 2ab'dir."},
        {"soru": "3(2x - 4) + 5 = 17 ise x kactir?", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 5"], "cevap": 2, "konu": "Cebirsel Ifadeler", "aciklama": "6x-12+5=17, 6x-7=17, 6x=24, x=4."},
        {"soru": "x^2 - 5x + 6 ifadesinin carpanlara ayrilmis hali nedir?", "secenekler": ["A) (x-1)(x-6)", "B) (x-2)(x-3)", "C) (x+2)(x+3)", "D) (x-1)(x+6)"], "cevap": 1, "konu": "Cebirsel Ifadeler", "aciklama": "Carpimi 6, toplami -5 olan sayilar: -2 ve -3. (x-2)(x-3)."},
        # --- Esitsizlikler (5) ---
        {"soru": "3x - 5 > 10 esitsizliginin cozum kumesi nedir?", "secenekler": ["A) x > 3", "B) x > 5", "C) x > 7", "D) x < 5"], "cevap": 1, "konu": "Esitsizlikler", "aciklama": "3x > 15, x > 5."},
        {"soru": "-2x + 8 >= 0 esitsizliginde x'in alabilecegi en buyuk tam sayi kactir?", "secenekler": ["A) 3", "B) 4", "C) 5", "D) 6"], "cevap": 1, "konu": "Esitsizlikler", "aciklama": "-2x >= -8, x <= 4. En buyuk tam sayi: 4."},
        {"soru": "x + 3 < 2x - 1 esitsizliginin cozumu nedir?", "secenekler": ["A) x > 4", "B) x > 2", "C) x < 4", "D) x < 2"], "cevap": 0, "konu": "Esitsizlikler", "aciklama": "3+1 < 2x-x, 4 < x, yani x > 4."},
        {"soru": "5 - x < 3 esitsizligini saglayan en kucuk tam sayi kactir?", "secenekler": ["A) 1", "B) 2", "C) 3", "D) 4"], "cevap": 2, "konu": "Esitsizlikler", "aciklama": "-x < -2, x > 2. En kucuk tam sayi: 3."},
        {"soru": "2(x-1) <= x+5 esitsizliginin cozum kumesi nedir?", "secenekler": ["A) x <= 5", "B) x <= 7", "C) x >= 7", "D) x <= 3"], "cevap": 1, "konu": "Esitsizlikler", "aciklama": "2x-2 <= x+5, x <= 7."},
        # --- Olasilik (5) ---
        {"soru": "Bir zarla atista 3'ten buyuk sayi gelme olasiligi kactir?", "secenekler": ["A) 1/6", "B) 1/3", "C) 1/2", "D) 2/3"], "cevap": 2, "konu": "Olasilik", "aciklama": "4,5,6 yani 3 sayi. P=3/6=1/2."},
        {"soru": "Bir torba icinde 4 kirmizi, 3 mavi, 2 yesil bilye vardir. Rastgele secilen bilyenin mavi olma olasiligi kactir?", "secenekler": ["A) 1/9", "B) 2/9", "C) 1/3", "D) 4/9"], "cevap": 2, "konu": "Olasilik", "aciklama": "Toplam=9, Mavi=3. P=3/9=1/3."},
        {"soru": "Iki zar atildiginda toplamin 7 gelme olasiligi kactir?", "secenekler": ["A) 1/12", "B) 1/6", "C) 5/36", "D) 7/36"], "cevap": 1, "konu": "Olasilik", "aciklama": "Toplami 7 yapan ikililer: (1,6)(2,5)(3,4)(4,3)(5,2)(6,1)=6 ihtimal. P=6/36=1/6."},
        {"soru": "Bir madeni para 3 kez atildiginda en az bir yazi gelme olasiligi kactir?", "secenekler": ["A) 3/8", "B) 1/2", "C) 5/8", "D) 7/8"], "cevap": 3, "konu": "Olasilik", "aciklama": "Hic yazi gelmeme: (1/2)^3=1/8. En az bir yazi=1-1/8=7/8."},
        {"soru": "52 kartlik bir desteden cekilen kartin kupa ya da kiz olma olasiligi kactir?", "secenekler": ["A) 4/13", "B) 15/52", "C) 16/52", "D) 17/52"], "cevap": 2, "konu": "Olasilik", "aciklama": "Kupa:13, Kiz:4, Kupa kizi:1. P=(13+4-1)/52=16/52=4/13."},
        # --- Denklemler (5) ---
        {"soru": "2x + 3y = 12 ve x - y = 1 denklem sisteminde x kactir?", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 5"], "cevap": 1, "konu": "Denklemler", "aciklama": "x=y+1. 2(y+1)+3y=12, 5y+2=12, y=2, x=3."},
        {"soru": "x^2 - 7x + 12 = 0 denkleminin kokleri toplami kactir?", "secenekler": ["A) 5", "B) 7", "C) 12", "D) -7"], "cevap": 1, "konu": "Denklemler", "aciklama": "Vieta: kokler toplami = -(-7)/1 = 7."},
        {"soru": "3/(x-2) = 6 denkleminde x kactir?", "secenekler": ["A) 5/2", "B) 3", "C) 7/2", "D) 4"], "cevap": 0, "konu": "Denklemler", "aciklama": "3=6(x-2), 3=6x-12, 15=6x, x=5/2."},
        {"soru": "|2x - 6| = 10 denkleminin cozum kumesindeki elemanlarin toplami kactir?", "secenekler": ["A) 4", "B) 6", "C) 8", "D) 10"], "cevap": 1, "konu": "Denklemler", "aciklama": "2x-6=10 => x=8 veya 2x-6=-10 => x=-2. Toplam=8+(-2)=6."},
        {"soru": "Bir sayinin 3 kati ile 5'in farkinin yarisi 7'dir. Bu sayi kactir?", "secenekler": ["A) 17/3", "B) 19/3", "C) 7", "D) 23/3"], "cevap": 1, "konu": "Denklemler", "aciklama": "(3x-5)/2=7, 3x-5=14, 3x=19, x=19/3."},
        # --- Ucgenler (5) ---
        {"soru": "Bir ucgenin iki kenari 5 cm ve 8 cm ise ucuncu kenar asagidakilerden hangisi olamaz?", "secenekler": ["A) 4 cm", "B) 7 cm", "C) 12 cm", "D) 14 cm"], "cevap": 3, "konu": "Ucgenler", "aciklama": "Ucgen esitsizligi: |5-8| < c < 5+8, yani 3 < c < 13. 14 > 13 oldugundan olamaz."},
        {"soru": "Dik ucgende dik kenarlar 6 cm ve 8 cm ise hipotenus kac cm'dir?", "secenekler": ["A) 9", "B) 10", "C) 11", "D) 12"], "cevap": 1, "konu": "Ucgenler", "aciklama": "Pisagor: c^2=6^2+8^2=36+64=100, c=10."},
        {"soru": "Bir ikizkenar ucgenin tabanindaki acilarin her biri 65 derece ise tepe acisi kac derecedir?", "secenekler": ["A) 40", "B) 50", "C) 55", "D) 60"], "cevap": 1, "konu": "Ucgenler", "aciklama": "Ic acilar toplami=180. 180-65-65=50."},
        {"soru": "Kenar uzunluklari 3, 4, 5 olan ucgenin alani kac birim karedir?", "secenekler": ["A) 5", "B) 6", "C) 7.5", "D) 10"], "cevap": 1, "konu": "Ucgenler", "aciklama": "3-4-5 dik ucgendir. Alan=(3x4)/2=6."},
        {"soru": "Bir ucgenin dis acisi 120 derece ise karsi iki ic acinin toplami kac derecedir?", "secenekler": ["A) 60", "B) 90", "C) 120", "D) 150"], "cevap": 2, "konu": "Ucgenler", "aciklama": "Dis aci teoremi: Bir dis aci, karsi iki ic acinin toplamina esittir. 120 derece."},
        # --- Donusum Geometrisi (5) ---
        {"soru": "A(2,3) noktasinin x-eksenine gore simetrik noktasi nedir?", "secenekler": ["A) (-2,3)", "B) (2,-3)", "C) (-2,-3)", "D) (3,2)"], "cevap": 1, "konu": "Donusum Geometrisi", "aciklama": "x-eksenine gore simetride y isareti degisir: (2,-3)."},
        {"soru": "B(4,-1) noktasinin orijine gore simetrik noktasi nedir?", "secenekler": ["A) (-4,1)", "B) (4,1)", "C) (-4,-1)", "D) (1,-4)"], "cevap": 0, "konu": "Donusum Geometrisi", "aciklama": "Orijine gore simetride her iki isaret degisir: (-4,1)."},
        {"soru": "Bir nokta saga 3, yukari 5 birim otelemelenir. (1,2) noktasinin yeni yeri neresidir?", "secenekler": ["A) (4,7)", "B) (3,5)", "C) (4,5)", "D) (3,7)"], "cevap": 0, "konu": "Donusum Geometrisi", "aciklama": "(1+3, 2+5) = (4,7)."},
        {"soru": "y = x dogrusuna gore (3,1) noktasinin simetrik noktasi nedir?", "secenekler": ["A) (1,3)", "B) (3,-1)", "C) (-3,1)", "D) (-1,-3)"], "cevap": 0, "konu": "Donusum Geometrisi", "aciklama": "y=x dogrusuna gore simetride x ve y yer degistirir: (1,3)."},
        {"soru": "Orijin etrafinda 90 derece saat yonunun tersine donus ile (2,0) nereye gider?", "secenekler": ["A) (0,2)", "B) (0,-2)", "C) (-2,0)", "D) (2,2)"], "cevap": 0, "konu": "Donusum Geometrisi", "aciklama": "90 derece CCW: (x,y)->(-y,x). (2,0)->(0,2)."},
        # --- Veri Analizi (5) ---
        {"soru": "5, 8, 3, 12, 7 sayilarinin aritmetik ortalamasi kactir?", "secenekler": ["A) 6", "B) 7", "C) 8", "D) 9"], "cevap": 1, "konu": "Veri Analizi", "aciklama": "(5+8+3+12+7)/5=35/5=7."},
        {"soru": "2, 5, 5, 7, 8, 9, 11 veri setinin medyani kactir?", "secenekler": ["A) 5", "B) 7", "C) 8", "D) 9"], "cevap": 1, "konu": "Veri Analizi", "aciklama": "7 veri siralandi, ortadaki (4.) deger: 7."},
        {"soru": "3, 3, 5, 7, 3, 8, 9 veri setinin modu kactir?", "secenekler": ["A) 3", "B) 5", "C) 7", "D) 8"], "cevap": 0, "konu": "Veri Analizi", "aciklama": "En cok tekrar eden sayi 3'tur (3 kez)."},
        {"soru": "1, 4, 7, 10, 13 veri setinin acikligi (degisim araligi) kactir?", "secenekler": ["A) 9", "B) 10", "C) 12", "D) 13"], "cevap": 2, "konu": "Veri Analizi", "aciklama": "Aciklik = en buyuk - en kucuk = 13 - 1 = 12."},
        {"soru": "Bir sinifta 10 ogrenci not almis, ortalama 72'dir. 75 alan bir ogrenci eklenirse yeni ortalama yaklasik kactir?", "secenekler": ["A) 72.1", "B) 72.3", "C) 72.5", "D) 73.0"], "cevap": 1, "konu": "Veri Analizi", "aciklama": "Toplam=720+75=795. Yeni ortalama=795/11=72.27... yaklasik 72.3."},
    ]


def _tyt_sorulari():
    """500 TYT Matematik sorusu (9-12. Sinif)."""
    try:
        from data.tyt_sorulari import TYT_SORU_HAVUZU
        return TYT_SORU_HAVUZU
    except ImportError:
        pass
    return [
        # --- Temel Kavramlar (4) ---
        {"soru": "A = {1,2,3,4,5} kumesinin eleman sayisi kactir?", "secenekler": ["A) 3", "B) 4", "C) 5", "D) 6"], "cevap": 2, "konu": "Temel Kavramlar", "aciklama": "A kumesinde 5 eleman vardir: s(A)=5."},
        {"soru": "(-3)^2 + (-2)^3 isleminin sonucu kactir?", "secenekler": ["A) 1", "B) 5", "C) 17", "D) -1"], "cevap": 0, "konu": "Temel Kavramlar", "aciklama": "9 + (-8) = 1."},
        {"soru": "0.125 sayisinin kesir karsiligi nedir?", "secenekler": ["A) 1/4", "B) 1/8", "C) 1/5", "D) 3/8"], "cevap": 1, "konu": "Temel Kavramlar", "aciklama": "0.125 = 125/1000 = 1/8."},
        {"soru": "Dort ardisik cift sayinin toplami 60 ise en buyugu kactir?", "secenekler": ["A) 16", "B) 18", "C) 20", "D) 22"], "cevap": 1, "konu": "Temel Kavramlar", "aciklama": "n+(n+2)+(n+4)+(n+6)=4n+12=60, n=12. En buyuk=12+6=18."},
        # --- Sayi Basamaklari (3) ---
        {"soru": "3a5 uc basamakli sayisi 9 ile bolunebiliyorsa a kactir?", "secenekler": ["A) 0", "B) 1", "C) 4", "D) 7"], "cevap": 1, "konu": "Sayi Basamaklari", "aciklama": "3+a+5=8+a, 9'a bolunmesi icin 8+a=9, a=1."},
        {"soru": "Bir uc basamakli sayinin yuzler basamagi 4, onlar basamagi 0, birler basamagi 7 ise sayi kactir?", "secenekler": ["A) 470", "B) 407", "C) 704", "D) 740"], "cevap": 1, "konu": "Sayi Basamaklari", "aciklama": "Yuzler:4, Onlar:0, Birler:7 => 407."},
        {"soru": "ab + ba = 132 ise a + b kactir?", "secenekler": ["A) 10", "B) 11", "C) 12", "D) 13"], "cevap": 2, "konu": "Sayi Basamaklari", "aciklama": "10a+b+10b+a=11(a+b)=132, a+b=12."},
        # --- Bolme ve Bolunebilme (3) ---
        {"soru": "372 sayisi 4 ile bolundugunde kalan kactir?", "secenekler": ["A) 0", "B) 1", "C) 2", "D) 3"], "cevap": 0, "konu": "Bolme-Bolunebilme", "aciklama": "Son iki basamak 72, 72/4=18 (tam boluniyor). Kalan 0."},
        {"soru": "Bir sayi 7'ye bolundugunde 5 kaliyor. Bu sayi 5 arttirilirsa 7'ye bolumunden kalan kactir?", "secenekler": ["A) 0", "B) 1", "C) 3", "D) 5"], "cevap": 2, "konu": "Bolme-Bolunebilme", "aciklama": "Sayi=7k+5. Sayi+5=7k+10=7k+7+3=7(k+1)+3. Kalan=3."},
        {"soru": "252 sayisinin asal carpanlarinin toplami kactir?", "secenekler": ["A) 9", "B) 12", "C) 14", "D) 16"], "cevap": 1, "konu": "Bolme-Bolunebilme", "aciklama": "252=2^2 x 3^2 x 7. Asal carpanlar: 2,3,7. Toplam=12."},
        # --- EBOB-EKOK (3) ---
        {"soru": "EBOB(48,60) kactir?", "secenekler": ["A) 6", "B) 8", "C) 12", "D) 24"], "cevap": 2, "konu": "EBOB-EKOK", "aciklama": "48=2^4x3, 60=2^2x3x5. EBOB=2^2x3=12."},
        {"soru": "EKOK(15,20) kactir?", "secenekler": ["A) 30", "B) 60", "C) 120", "D) 300"], "cevap": 1, "konu": "EBOB-EKOK", "aciklama": "15=3x5, 20=2^2x5. EKOK=2^2x3x5=60."},
        {"soru": "Iki sayinin EBOB'u 6, EKOK'u 180 ve sayilardan biri 36 ise digeri kactir?", "secenekler": ["A) 24", "B) 30", "C) 36", "D) 42"], "cevap": 1, "konu": "EBOB-EKOK", "aciklama": "EBOB x EKOK = a x b. 6 x 180 = 36 x b, b = 30."},
        # --- Rasyonel Sayilar (3) ---
        {"soru": "2/3 + 3/4 isleminin sonucu kactir?", "secenekler": ["A) 5/7", "B) 5/12", "C) 17/12", "D) 11/12"], "cevap": 2, "konu": "Rasyonel Sayilar", "aciklama": "8/12 + 9/12 = 17/12."},
        {"soru": "(5/6) / (10/3) isleminin sonucu kactir?", "secenekler": ["A) 1/4", "B) 1/2", "C) 25/18", "D) 50/18"], "cevap": 0, "konu": "Rasyonel Sayilar", "aciklama": "(5/6) x (3/10) = 15/60 = 1/4."},
        {"soru": "0.3333... (3 tekrarli) sayisi hangi kesre esittir?", "secenekler": ["A) 1/3", "B) 3/10", "C) 33/100", "D) 3/9"], "cevap": 0, "konu": "Rasyonel Sayilar", "aciklama": "0.333... = 1/3."},
        # --- Mutlak Deger (3) ---
        {"soru": "|3 - 8| + |(-2) - 3| isleminin sonucu kactir?", "secenekler": ["A) 5", "B) 8", "C) 10", "D) 13"], "cevap": 2, "konu": "Mutlak Deger", "aciklama": "|-5| + |-5| = 5 + 5 = 10."},
        {"soru": "|2x - 4| = 0 denkleminde x kactir?", "secenekler": ["A) 0", "B) 1", "C) 2", "D) 4"], "cevap": 2, "konu": "Mutlak Deger", "aciklama": "2x-4=0, x=2."},
        {"soru": "|x+1| + |x-3| ifadesinin minimum degeri kactir?", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 5"], "cevap": 2, "konu": "Mutlak Deger", "aciklama": "Iki mutlak degerin toplami icin min deger iki nokta arasindaki uzaklik: |-1-3|=4."},
        # --- Uslu-Koklu (3) ---
        {"soru": "Karekok(27) x Karekok(3) isleminin sonucu kactir?", "secenekler": ["A) 3", "B) 9", "C) 27", "D) 81"], "cevap": 1, "konu": "Uslu-Koklu", "aciklama": "Karekok(27x3) = Karekok(81) = 9."},
        {"soru": "4^(3/2) ifadesinin degeri kactir?", "secenekler": ["A) 6", "B) 8", "C) 12", "D) 16"], "cevap": 1, "konu": "Uslu-Koklu", "aciklama": "4^(3/2) = (4^(1/2))^3 = 2^3 = 8."},
        {"soru": "9^(-1/2) ifadesinin degeri kactir?", "secenekler": ["A) -3", "B) 1/3", "C) -1/3", "D) 3"], "cevap": 1, "konu": "Uslu-Koklu", "aciklama": "9^(-1/2) = 1/Karekok(9) = 1/3."},
        # --- Polinomlar (3) ---
        {"soru": "P(x) = 2x^3 - x + 5 ise P(1) kactir?", "secenekler": ["A) 4", "B) 6", "C) 8", "D) 10"], "cevap": 1, "konu": "Polinomlar", "aciklama": "P(1) = 2(1) - 1 + 5 = 6."},
        {"soru": "P(x) = x^2 + 3x + k polinomunda P(2) = 14 ise k kactir?", "secenekler": ["A) 1", "B) 2", "C) 3", "D) 4"], "cevap": 3, "konu": "Polinomlar", "aciklama": "P(2)=4+6+k=10+k=14, k=4."},
        {"soru": "(x^2-1)/(x-1) ifadesi x != 1 icin neye esittir?", "secenekler": ["A) x-1", "B) x+1", "C) x^2+1", "D) 1"], "cevap": 1, "konu": "Polinomlar", "aciklama": "x^2-1 = (x-1)(x+1). Bolerek x+1 elde edilir."},
        # --- 1. Dereceden Denklemler (3) ---
        {"soru": "4(x - 3) = 2(x + 1) denkleminde x kactir?", "secenekler": ["A) 5", "B) 6", "C) 7", "D) 8"], "cevap": 2, "konu": "1.Dereceden Denklemler", "aciklama": "4x-12=2x+2, 2x=14, x=7."},
        {"soru": "(x+2)/3 = (x-1)/2 denkleminde x kactir?", "secenekler": ["A) 5", "B) 7", "C) 9", "D) 11"], "cevap": 1, "konu": "1.Dereceden Denklemler", "aciklama": "2(x+2)=3(x-1), 2x+4=3x-3, x=7."},
        {"soru": "Bir sayinin 2/3'u 18'e esittir. Sayi kactir?", "secenekler": ["A) 12", "B) 24", "C) 27", "D) 36"], "cevap": 2, "konu": "1.Dereceden Denklemler", "aciklama": "(2/3)x=18, x=18x(3/2)=27."},
        # --- Oran-Oranti (3) ---
        {"soru": "a/b = 3/5 ve a + b = 40 ise a kactir?", "secenekler": ["A) 12", "B) 15", "C) 18", "D) 20"], "cevap": 1, "konu": "Oran-Oranti", "aciklama": "a=3k, b=5k. 3k+5k=8k=40, k=5. a=15."},
        {"soru": "Bir isi A 6 gunde, B 12 gunde bitiriyorsa birlikte kac gunde bitirirler?", "secenekler": ["A) 3", "B) 4", "C) 5", "D) 6"], "cevap": 1, "konu": "Oran-Oranti", "aciklama": "1/6 + 1/12 = 3/12 = 1/4. Birlikte 4 gun."},
        {"soru": "120 km yolu 80 km/h ile giden bir arac kac dakikada varir?", "secenekler": ["A) 80", "B) 90", "C) 100", "D) 120"], "cevap": 1, "konu": "Oran-Oranti", "aciklama": "120/80 = 1.5 saat = 90 dakika."},
        # --- Problemler (3) ---
        {"soru": "Ali'nin yasi Ayse'nin yasinin 3 katidir. 4 yil sonra yaslarinin toplami 48 olacaktir. Ali'nin su anki yasi kactir?", "secenekler": ["A) 24", "B) 27", "C) 30", "D) 33"], "cevap": 2, "konu": "Problemler", "aciklama": "Ali=3x, Ayse=x. (3x+4)+(x+4)=48, 4x+8=48, 4x=40, x=10. Ali=30."},
        {"soru": "Bir sinifta 30 ogrenci vardir. Kizlarin sayisi erkeklerin 2 katidir. Kac kiz vardir?", "secenekler": ["A) 10", "B) 15", "C) 20", "D) 25"], "cevap": 2, "konu": "Problemler", "aciklama": "k=2e, k+e=30, 3e=30, e=10, k=20."},
        {"soru": "Bir urunun fiyati once %20 artti, sonra %10 indi. Toplam degisim yuzdesi kactir?", "secenekler": ["A) %8", "B) %10", "C) %12", "D) %15"], "cevap": 0, "konu": "Problemler", "aciklama": "100 -> 120 -> 108. Toplam artis: %8."},
        # --- Kumeler (3) ---
        {"soru": "s(A)=15, s(B)=10, s(A kesisim B)=4 ise s(A birlesim B) kactir?", "secenekler": ["A) 17", "B) 19", "C) 21", "D) 25"], "cevap": 2, "konu": "Kumeler", "aciklama": "s(AUB)=s(A)+s(B)-s(AnB)=15+10-4=21."},
        {"soru": "A = {x: x < 5, x dogal sayi} kumesinin alt kume sayisi kactir?", "secenekler": ["A) 16", "B) 32", "C) 64", "D) 128"], "cevap": 1, "konu": "Kumeler", "aciklama": "A={0,1,2,3,4}, 5 eleman. Alt kume sayisi=2^5=32."},
        {"soru": "A'nin tumleyeni B ise A birlesim B neye esittir?", "secenekler": ["A) Bos kume", "B) A", "C) B", "D) Evrensel kume"], "cevap": 3, "konu": "Kumeler", "aciklama": "Bir kumenin tumleyeni ile birlesimi evrensel kumeyi verir."},
        # --- Ek sorular (toplam 40'a tamamlama) ---
        {"soru": "Bir havuz A muslugu ile 8 saatte, B muslugu ile 12 saatte doluyor. Iki musluk birlikte acilirsa havuz kac saatte dolar?", "secenekler": ["A) 4", "B) 4.8", "C) 5", "D) 6"], "cevap": 1, "konu": "Problemler", "aciklama": "1/8+1/12=5/24. Birlikte 24/5=4.8 saat."},
        {"soru": "3^(x+1) = 81 ise x kactir?", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 5"], "cevap": 1, "konu": "Uslu-Koklu", "aciklama": "81=3^4. 3^(x+1)=3^4, x+1=4, x=3."},
        {"soru": "A={1,2,3}, B={2,3,4,5} ise A kesisim B'nin eleman sayisi kactir?", "secenekler": ["A) 1", "B) 2", "C) 3", "D) 4"], "cevap": 1, "konu": "Kumeler", "aciklama": "A kesisim B = {2,3}. Eleman sayisi=2."},
    ]


def _ayt_sorulari():
    """500 AYT Matematik sorusu (11-12. Sinif)."""
    try:
        from data.ayt_sorulari import AYT_SORU_HAVUZU
        return AYT_SORU_HAVUZU
    except ImportError:
        pass
    return [
        # --- Fonksiyonlar (4) ---
        {"soru": "f(x) = 2x + 1 ve g(x) = x^2 ise (fog)(2) kactir?", "secenekler": ["A) 7", "B) 9", "C) 10", "D) 25"], "cevap": 1, "konu": "Fonksiyonlar", "aciklama": "g(2)=4, f(g(2))=f(4)=2(4)+1=9."},
        {"soru": "f(x) = (x-1)/(x+2) fonksiyonunun tanimli olmadigi x degeri kactir?", "secenekler": ["A) -2", "B) -1", "C) 1", "D) 2"], "cevap": 0, "konu": "Fonksiyonlar", "aciklama": "Payda sifir olamaz: x+2=0, x=-2."},
        {"soru": "f(x) = 3x - 5 fonksiyonunun tersi f^(-1)(x) nedir?", "secenekler": ["A) (x+5)/3", "B) (x-5)/3", "C) 3x+5", "D) (5-x)/3"], "cevap": 0, "konu": "Fonksiyonlar", "aciklama": "y=3x-5, x=(y+5)/3. f^(-1)(x)=(x+5)/3."},
        {"soru": "f(x) = x^2 - 4x + 3 fonksiyonunun koklerinin carpimi kactir?", "secenekler": ["A) -3", "B) 1", "C) 3", "D) 4"], "cevap": 2, "konu": "Fonksiyonlar", "aciklama": "Vieta: kokler carpimi = c/a = 3/1 = 3."},
        # --- Logaritma (4) ---
        {"soru": "log2(32) kactir?", "secenekler": ["A) 3", "B) 4", "C) 5", "D) 6"], "cevap": 2, "konu": "Logaritma", "aciklama": "2^5 = 32, dolayisiyla log2(32) = 5."},
        {"soru": "log(1000) kactir? (taban 10)", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 10"], "cevap": 1, "konu": "Logaritma", "aciklama": "10^3 = 1000, log(1000) = 3."},
        {"soru": "log3(1/9) kactir?", "secenekler": ["A) -3", "B) -2", "C) 2", "D) 3"], "cevap": 1, "konu": "Logaritma", "aciklama": "3^(-2) = 1/9, log3(1/9) = -2."},
        {"soru": "log2(x) = 3 ise x kactir?", "secenekler": ["A) 6", "B) 8", "C) 9", "D) 12"], "cevap": 1, "konu": "Logaritma", "aciklama": "x = 2^3 = 8."},
        # --- Trigonometri (4) ---
        {"soru": "sin(30) + cos(60) kactir?", "secenekler": ["A) 0", "B) 1/2", "C) 1", "D) Karekok(3)/2"], "cevap": 2, "konu": "Trigonometri", "aciklama": "sin30=1/2, cos60=1/2. 1/2+1/2=1."},
        {"soru": "sin^2(x) + cos^2(x) ifadesi neye esittir?", "secenekler": ["A) 0", "B) 1", "C) 2", "D) sin(2x)"], "cevap": 1, "konu": "Trigonometri", "aciklama": "Temel trigonometrik ozdeslik: sin^2(x)+cos^2(x)=1."},
        {"soru": "tan(45) kactir?", "secenekler": ["A) 0", "B) 1/2", "C) 1", "D) Karekok(2)"], "cevap": 2, "konu": "Trigonometri", "aciklama": "tan45 = sin45/cos45 = 1."},
        {"soru": "sin(150) kactir?", "secenekler": ["A) -1/2", "B) 1/2", "C) Karekok(3)/2", "D) -Karekok(3)/2"], "cevap": 1, "konu": "Trigonometri", "aciklama": "sin(150)=sin(180-30)=sin30=1/2."},
        # --- Karmasik Sayilar (4) ---
        {"soru": "i^2 kactir? (i: sanal birim)", "secenekler": ["A) 1", "B) -1", "C) i", "D) -i"], "cevap": 1, "konu": "Karmasik Sayilar", "aciklama": "Tanimdan: i^2 = -1."},
        {"soru": "(3+2i) + (1-5i) isleminin sonucu nedir?", "secenekler": ["A) 4+3i", "B) 4-3i", "C) 2+7i", "D) 2-3i"], "cevap": 1, "konu": "Karmasik Sayilar", "aciklama": "(3+1) + (2-5)i = 4 - 3i."},
        {"soru": "i^(2024) kactir?", "secenekler": ["A) 1", "B) -1", "C) i", "D) -i"], "cevap": 0, "konu": "Karmasik Sayilar", "aciklama": "2024/4=506, kalan 0. i^(4k)=1."},
        {"soru": "|3+4i| kactir?", "secenekler": ["A) 3", "B) 4", "C) 5", "D) 7"], "cevap": 2, "konu": "Karmasik Sayilar", "aciklama": "|3+4i| = Karekok(9+16) = Karekok(25) = 5."},
        # --- Limit (4) ---
        {"soru": "lim(x->2) (x^2-4)/(x-2) kactir?", "secenekler": ["A) 0", "B) 2", "C) 4", "D) Tanimsiz"], "cevap": 2, "konu": "Limit", "aciklama": "(x^2-4)/(x-2) = (x-2)(x+2)/(x-2) = x+2. Limit: 2+2=4."},
        {"soru": "lim(x->0) sin(x)/x kactir?", "secenekler": ["A) 0", "B) 1", "C) Sonsuz", "D) -1"], "cevap": 1, "konu": "Limit", "aciklama": "Temel limit: lim(x->0) sin(x)/x = 1."},
        {"soru": "lim(x->sonsuz) (3x+1)/(x-2) kactir?", "secenekler": ["A) 1", "B) 3", "C) Sonsuz", "D) 0"], "cevap": 1, "konu": "Limit", "aciklama": "En yuksek dereceli terimlerin orani: 3x/x = 3."},
        {"soru": "lim(x->1) (x^3-1)/(x-1) kactir?", "secenekler": ["A) 1", "B) 2", "C) 3", "D) Tanimsiz"], "cevap": 2, "konu": "Limit", "aciklama": "x^3-1=(x-1)(x^2+x+1). Sadeleserek: x^2+x+1, x=1 icin 3."},
        # --- Turev (4) ---
        {"soru": "f(x) = 3x^4 fonksiyonunun turevi nedir?", "secenekler": ["A) 3x^3", "B) 12x^3", "C) 12x^4", "D) 4x^3"], "cevap": 1, "konu": "Turev", "aciklama": "f'(x) = 4.3x^3 = 12x^3."},
        {"soru": "f(x) = x^2 - 6x + 5 fonksiyonunun minimum yaptigi x degeri kactir?", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 5"], "cevap": 1, "konu": "Turev", "aciklama": "f'(x)=2x-6=0, x=3."},
        {"soru": "f(x) = sin(x) ise f'(x) nedir?", "secenekler": ["A) -sin(x)", "B) cos(x)", "C) -cos(x)", "D) tan(x)"], "cevap": 1, "konu": "Turev", "aciklama": "(sin(x))' = cos(x)."},
        {"soru": "f(x) = e^(2x) fonksiyonunun turevi nedir?", "secenekler": ["A) e^(2x)", "B) 2e^(2x)", "C) 2e^x", "D) e^(x+2)"], "cevap": 1, "konu": "Turev", "aciklama": "Zincir kurali: f'(x) = 2.e^(2x)."},
        # --- Integral (4) ---
        {"soru": "integral(2x dx) nedir?", "secenekler": ["A) x^2 + C", "B) 2x^2 + C", "C) x + C", "D) x^2/2 + C"], "cevap": 0, "konu": "Integral", "aciklama": "integral(2x dx) = 2.(x^2/2) + C = x^2 + C."},
        {"soru": "integral(0,1)(x^2 dx) kactir?", "secenekler": ["A) 1/4", "B) 1/3", "C) 1/2", "D) 1"], "cevap": 1, "konu": "Integral", "aciklama": "[x^3/3] 0'dan 1'e = 1/3 - 0 = 1/3."},
        {"soru": "integral(cos(x) dx) nedir?", "secenekler": ["A) sin(x) + C", "B) -sin(x) + C", "C) cos(x) + C", "D) tan(x) + C"], "cevap": 0, "konu": "Integral", "aciklama": "integral(cos(x) dx) = sin(x) + C."},
        {"soru": "integral(1,e)(1/x dx) kactir?", "secenekler": ["A) 0", "B) 1", "C) e", "D) 1/e"], "cevap": 1, "konu": "Integral", "aciklama": "[ln|x|] 1'den e'ye = ln(e) - ln(1) = 1 - 0 = 1."},
        # --- Diziler (4) ---
        {"soru": "2, 5, 8, 11, ... aritmetik dizisinin 10. terimi kactir?", "secenekler": ["A) 26", "B) 29", "C) 32", "D) 35"], "cevap": 1, "konu": "Diziler", "aciklama": "a_n = a_1 + (n-1)d = 2 + 9(3) = 29."},
        {"soru": "3, 6, 12, 24, ... geometrik dizisinin 6. terimi kactir?", "secenekler": ["A) 48", "B) 64", "C) 96", "D) 192"], "cevap": 2, "konu": "Diziler", "aciklama": "a_n = a_1.r^(n-1) = 3.2^5 = 96."},
        {"soru": "1+2+3+...+100 toplami kactir?", "secenekler": ["A) 4950", "B) 5000", "C) 5050", "D) 5100"], "cevap": 2, "konu": "Diziler", "aciklama": "n(n+1)/2 = 100(101)/2 = 5050."},
        {"soru": "Bir aritmetik dizide a1=5, a5=17 ise ortak fark d kactir?", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 5"], "cevap": 1, "konu": "Diziler", "aciklama": "a5=a1+4d, 17=5+4d, d=3."},
        # --- Matrisler (4) ---
        {"soru": "A=[1 2; 3 4] matrisinin determinanti kactir?", "secenekler": ["A) -2", "B) -1", "C) 2", "D) 10"], "cevap": 0, "konu": "Matrisler", "aciklama": "det(A) = 1.4 - 2.3 = 4 - 6 = -2."},
        {"soru": "2x2 birim matrisin determinanti kactir?", "secenekler": ["A) 0", "B) 1", "C) 2", "D) 4"], "cevap": 1, "konu": "Matrisler", "aciklama": "I=[1 0; 0 1], det(I)=1.1-0.0=1."},
        {"soru": "A=[2 0; 0 3] matrisinin tersi nedir?", "secenekler": ["A) [1/2 0; 0 1/3]", "B) [3 0; 0 2]", "C) [2 0; 0 3]", "D) [-2 0; 0 -3]"], "cevap": 0, "konu": "Matrisler", "aciklama": "Kosegensel matrisin tersi: kosegen elemanlarin tersi alinir."},
        {"soru": "A=[1 2; 3 4], B=[5 6; 7 8] ise A+B'nin (1,1) elemani kactir?", "secenekler": ["A) 4", "B) 6", "C) 8", "D) 10"], "cevap": 1, "konu": "Matrisler", "aciklama": "(A+B)(1,1) = 1+5 = 6."},
        # --- Konikler (4) ---
        {"soru": "x^2 + y^2 = 25 cemberinin yaricapi kactir?", "secenekler": ["A) 3", "B) 4", "C) 5", "D) 25"], "cevap": 2, "konu": "Konikler", "aciklama": "r^2=25, r=5."},
        {"soru": "Merkezi (2,3) ve yaricapi 4 olan cemberin denklemi nedir?", "secenekler": ["A) (x-2)^2+(y-3)^2=4", "B) (x-2)^2+(y-3)^2=16", "C) (x+2)^2+(y+3)^2=16", "D) x^2+y^2=16"], "cevap": 1, "konu": "Konikler", "aciklama": "(x-a)^2+(y-b)^2=r^2 => (x-2)^2+(y-3)^2=16."},
        {"soru": "x^2/9 + y^2/4 = 1 elipsinde a kactir?", "secenekler": ["A) 2", "B) 3", "C) 4", "D) 9"], "cevap": 1, "konu": "Konikler", "aciklama": "a^2=9, a=3 (buyuk yaricap)."},
        {"soru": "y = x^2 parabolunun tepe noktasi nerededir?", "secenekler": ["A) (0,0)", "B) (1,0)", "C) (0,1)", "D) (1,1)"], "cevap": 0, "konu": "Konikler", "aciklama": "y=x^2 standart parabol, tepe noktasi orijinde: (0,0)."},
    ]


def _matematik_format_html(text):
    """Soru metni icin HTML matematik gosterimi."""
    import re
    # Karekok: kok45, kok(45), sqrt(45), sqrt45 -> √ gorseli
    def _kok_html(icerik):
        return (f'<span style="display:inline-block;vertical-align:middle;margin:0 2px">'
                f'<span style="font-size:1.1em;color:#a5b4fc">√</span>'
                f'<span style="border-top:2px solid #a5b4fc;padding:0 3px;color:#e0e7ff">{icerik}</span></span>')
    text = re.sub(r'kok\(([^)]+)\)', lambda m: _kok_html(m.group(1)), text)
    text = re.sub(r'kok(\d+)', lambda m: _kok_html(m.group(1)), text)
    text = re.sub(r'sqrt\(([^)]+)\)', lambda m: _kok_html(m.group(1)), text)
    text = re.sub(r'sqrt(\d+)', lambda m: _kok_html(m.group(1)), text)
    # Kesir: a/b -> HTML kesir
    def _kesir(m):
        pay, payda = m.group(1), m.group(2)
        return (f'<span style="display:inline-block;text-align:center;vertical-align:middle;'
                f'font-size:0.85em;line-height:1.1;margin:0 2px">'
                f'<span style="display:block;border-bottom:2px solid #a5b4fc;padding:1px 4px;color:#e0e7ff">{pay}</span>'
                f'<span style="display:block;padding:1px 4px;color:#e0e7ff">{payda}</span></span>')
    text = re.sub(r'(\d+)/(\d+)', _kesir, text)
    # Uslu: x^2 -> x²
    sup_map = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','n':'ⁿ'}
    def _ust(m):
        return m.group(1) + ''.join(sup_map.get(c, c) for c in m.group(2))
    text = re.sub(r'(\w)\^(\d+|n)', _ust, text)
    # Pi -> π
    text = re.sub(r'\bpi\b', 'π', text)
    # Ozel isimler
    text = text.replace('kesisim', '∩').replace('birlesim', '∪').replace('>=', '≥').replace('<=', '≤').replace('!=', '≠')
    return text


def _matematik_format_text(text):
    """Sik metni icin Unicode kesir (st.radio icin — HTML olmaz)."""
    import re
    sup_map = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','n':'ⁿ'}
    def _ust(m):
        return m.group(1) + ''.join(sup_map.get(c, c) for c in m.group(2))
    text = re.sub(r'(\w)\^(\d+|n)', _ust, text)
    text = re.sub(r'sqrt\(([^)]+)\)', r'√\1', text)
    return text


def _kume_gorsel(soru_text):
    """Soru metninde kume ifadesi varsa Venn diyagrami HTML'i dondur."""
    import re
    m = re.search(r'A\s*=\s*\{([^}]+)\}.*?B\s*=\s*\{([^}]+)\}', soru_text)
    if not m:
        return ""
    a_items = set(x.strip() for x in m.group(1).split(','))
    b_items = set(x.strip() for x in m.group(2).split(','))
    only_a = a_items - b_items
    both = a_items & b_items
    only_b = b_items - a_items
    oa = ", ".join(sorted(only_a)) if only_a else ""
    ob = ", ".join(sorted(both)) if both else ""
    oc = ", ".join(sorted(only_b)) if only_b else ""
    return f"""
    <div style="display:flex;justify-content:center;margin:12px 0">
      <div style="position:relative;width:320px;height:180px">
        <div style="position:absolute;left:30px;top:20px;width:170px;height:140px;
            border-radius:50%;border:3px solid #6366f1;background:rgba(99,102,241,0.1);
            display:flex;align-items:center;padding-left:20px">
            <span style="color:#a5b4fc;font-size:0.85rem;font-weight:700">{oa}</span>
        </div>
        <div style="position:absolute;right:30px;top:20px;width:170px;height:140px;
            border-radius:50%;border:3px solid #f59e0b;background:rgba(245,158,11,0.1);
            display:flex;align-items:center;justify-content:flex-end;padding-right:20px">
            <span style="color:#fcd34d;font-size:0.85rem;font-weight:700">{oc}</span>
        </div>
        <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
            z-index:2;text-align:center">
            <span style="color:#10b981;font-size:0.9rem;font-weight:800">{ob}</span>
        </div>
        <div style="position:absolute;left:55px;top:2px;color:#818cf8;font-weight:800;font-size:0.9rem">A</div>
        <div style="position:absolute;right:55px;top:2px;color:#f59e0b;font-weight:800;font-size:0.9rem">B</div>
      </div>
    </div>"""


def _soru_gorseli(soru_text, konu=""):
    """Soru konusuna gore gorsel HTML uret. Bos string donerse gorsel yok."""
    import re
    txt = soru_text.lower()
    konu_lower = konu.lower() if konu else ""

    # ── 1. Kumeler ──────────────────────────────────────────────
    venn = _kume_gorsel(soru_text)
    if venn:
        return venn

    # ── 2. Geometri / Ucgenler ──────────────────────────────────
    if any(k in txt for k in ["ucgen", "üçgen", "kenar", "aci", "açı", "hipoten"]) or any(k in konu_lower for k in ["geometri", "ucgen", "üçgen"]):
        # Ucgen tipini belirle
        if any(k in txt for k in ["dik ucgen", "dik üçgen", "hipotenüs", "hipotenus", "90°", "90 derece"]):
            # Dik ucgen (SVG)
            return """
    <div style="display:flex;justify-content:center;margin:12px 0">
      <svg width="200" height="180" viewBox="0 0 200 180">
        <polygon points="30,150 170,150 30,30" fill="rgba(99,102,241,0.1)" stroke="#6366f1" stroke-width="2.5"/>
        <rect x="30" y="130" width="20" height="20" fill="none" stroke="#f59e0b" stroke-width="1.5"/>
        <text x="18" y="95" fill="#a5b4fc" font-size="11" font-weight="700">a</text>
        <text x="95" y="168" fill="#a5b4fc" font-size="11" font-weight="700">b</text>
        <text x="105" y="82" fill="#10b981" font-size="11" font-weight="700">c</text>
        <text x="10" y="160" fill="#f59e0b" font-size="10" font-weight="600">90°</text>
        <text x="75" y="20" fill="#94a3b8" font-size="10">Dik Ucgen</text>
      </svg>
    </div>"""
        elif any(k in txt for k in ["eskenar", "eşkenar"]):
            # Eskenar ucgen
            return """
    <div style="display:flex;justify-content:center;margin:12px 0">
      <svg width="200" height="180" viewBox="0 0 200 180">
        <polygon points="100,20 30,160 170,160" fill="rgba(16,185,129,0.1)" stroke="#10b981" stroke-width="2.5"/>
        <text x="55" y="100" fill="#a5b4fc" font-size="11" font-weight="700" transform="rotate(-60,55,100)">a</text>
        <text x="95" y="168" fill="#a5b4fc" font-size="11" font-weight="700">a</text>
        <text x="140" y="100" fill="#a5b4fc" font-size="11" font-weight="700" transform="rotate(60,140,100)">a</text>
        <text x="90" y="40" fill="#f59e0b" font-size="10" font-weight="600">60°</text>
        <text x="35" y="157" fill="#f59e0b" font-size="10" font-weight="600">60°</text>
        <text x="145" y="157" fill="#f59e0b" font-size="10" font-weight="600">60°</text>
        <text x="60" y="14" fill="#94a3b8" font-size="10">Eskenar Ucgen</text>
      </svg>
    </div>"""
        elif any(k in txt for k in ["ikizkenar", "ikiz kenar"]):
            # Ikizkenar ucgen
            return """
    <div style="display:flex;justify-content:center;margin:12px 0">
      <svg width="200" height="180" viewBox="0 0 200 180">
        <polygon points="100,20 40,160 160,160" fill="rgba(245,158,11,0.1)" stroke="#f59e0b" stroke-width="2.5"/>
        <text x="60" y="95" fill="#a5b4fc" font-size="11" font-weight="700" transform="rotate(-62,60,95)">a</text>
        <text x="95" y="168" fill="#10b981" font-size="11" font-weight="700">b</text>
        <text x="138" y="95" fill="#a5b4fc" font-size="11" font-weight="700" transform="rotate(62,138,95)">a</text>
        <text x="55" y="14" fill="#94a3b8" font-size="10">Ikizkenar Ucgen</text>
      </svg>
    </div>"""
        else:
            # Genel ucgen
            return """
    <div style="display:flex;justify-content:center;margin:12px 0">
      <svg width="220" height="170" viewBox="0 0 220 170">
        <polygon points="110,15 20,150 190,150" fill="rgba(99,102,241,0.08)" stroke="#6366f1" stroke-width="2.5"/>
        <text x="55" y="88" fill="#a5b4fc" font-size="11" font-weight="700">a</text>
        <text x="100" y="165" fill="#10b981" font-size="11" font-weight="700">b</text>
        <text x="157" y="88" fill="#f59e0b" font-size="11" font-weight="700">c</text>
        <text x="100" y="40" fill="#94a3b8" font-size="10" text-anchor="middle">A</text>
        <text x="13" y="160" fill="#94a3b8" font-size="10">B</text>
        <text x="193" y="160" fill="#94a3b8" font-size="10">C</text>
      </svg>
    </div>"""

    # ── 3. Denklemler ───────────────────────────────────────────
    eq_match = re.search(r'([0-9x]+\s*[+\-*/]\s*[0-9x]+\s*=\s*[0-9x]+)', soru_text)
    if eq_match or any(k in konu_lower for k in ["denklem", "esitlik"]):
        eq_display = eq_match.group(1).strip() if eq_match else ""
        if eq_display:
            # Sayi dogrusu + denklem kutusu
            # Cozumu bulmaya calis (basit x + a = b)
            sol_match = re.search(r'x\s*[+]\s*(\d+)\s*=\s*(\d+)', eq_display)
            sol_marker = ""
            if sol_match:
                a_val = int(sol_match.group(1))
                b_val = int(sol_match.group(2))
                x_val = b_val - a_val
                # Sayi dogrusunda konum (0-10 arasi normalize)
                pos_pct = min(max(x_val * 10, 5), 95)
                sol_marker = f"""
            <div style="position:relative;height:40px;margin-top:8px">
              <div style="position:absolute;left:{pos_pct}%;top:18px;transform:translateX(-50%);
                  width:12px;height:12px;background:#10b981;border-radius:50%"></div>
              <div style="position:absolute;left:{pos_pct}%;top:2px;transform:translateX(-50%);
                  color:#10b981;font-size:0.75rem;font-weight:700">x={x_val}</div>
            </div>"""
            else:
                sol_match2 = re.search(r'x\s*[-]\s*(\d+)\s*=\s*(\d+)', eq_display)
                if sol_match2:
                    a_val = int(sol_match2.group(1))
                    b_val = int(sol_match2.group(2))
                    x_val = b_val + a_val
                    pos_pct = min(max(x_val * 10, 5), 95)
                    sol_marker = f"""
            <div style="position:relative;height:40px;margin-top:8px">
              <div style="position:absolute;left:{pos_pct}%;top:18px;transform:translateX(-50%);
                  width:12px;height:12px;background:#10b981;border-radius:50%"></div>
              <div style="position:absolute;left:{pos_pct}%;top:2px;transform:translateX(-50%);
                  color:#10b981;font-size:0.75rem;font-weight:700">x={x_val}</div>
            </div>"""
            # Sayi dogrusu tiklari
            ticks = ""
            for i in range(11):
                lp = i * 10
                ticks += f'<div style="position:absolute;left:{lp}%;top:0;width:1px;height:8px;background:#475569"></div>'
                ticks += f'<div style="position:absolute;left:{lp}%;top:10px;transform:translateX(-50%);color:#64748b;font-size:0.6rem">{i}</div>'
            return f"""
    <div style="display:flex;flex-direction:column;align-items:center;margin:12px 0">
      <div style="background:linear-gradient(135deg,#312e81,#1e1b4b);border-radius:10px;padding:12px 20px;
          border:1.5px solid #4338ca;margin-bottom:10px">
        <span style="color:#e0e7ff;font-size:1.3rem;font-weight:800;letter-spacing:1px">{eq_display}</span>
      </div>
      <div style="position:relative;width:280px;height:30px;margin-top:4px">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#475569,#6366f1,#475569)"></div>
        <div style="position:absolute;right:-6px;top:-4px;width:0;height:0;border-left:8px solid #6366f1;
            border-top:5px solid transparent;border-bottom:5px solid transparent"></div>
        {ticks}
      </div>
      {sol_marker}
    </div>"""

    # ── 4. Koordinat / Grafik ───────────────────────────────────
    if any(k in txt for k in ["koordinat", "grafik", "graf", "dogru denklemi", "doğru denklemi", "(x,y)", "x ekseni", "y ekseni"]) or any(k in konu_lower for k in ["koordinat", "grafik", "analitik"]):
        # Koordinatlari bul
        coords = re.findall(r'\((\-?\d+)\s*,\s*(\-?\d+)\)', soru_text)
        points_svg = ""
        if coords:
            for cx, cy in coords[:5]:  # max 5 nokta
                px = 100 + int(cx) * 20
                py = 100 - int(cy) * 20
                px = max(10, min(190, px))
                py = max(10, min(190, py))
                points_svg += f'<circle cx="{px}" cy="{py}" r="5" fill="#f59e0b"/>'
                points_svg += f'<text x="{px+7}" y="{py-5}" fill="#fcd34d" font-size="9" font-weight="600">({cx},{cy})</text>'
        return f"""
    <div style="display:flex;justify-content:center;margin:12px 0">
      <svg width="200" height="200" viewBox="0 0 200 200">
        <rect width="200" height="200" fill="#0f172a" rx="8"/>
        <line x1="10" y1="100" x2="190" y2="100" stroke="#334155" stroke-width="1.5"/>
        <line x1="100" y1="10" x2="100" y2="190" stroke="#334155" stroke-width="1.5"/>
        <polygon points="190,100 183,96 183,104" fill="#6366f1"/>
        <polygon points="100,10 96,17 104,17" fill="#6366f1"/>
        <text x="192" y="105" fill="#94a3b8" font-size="10">x</text>
        <text x="104" y="16" fill="#94a3b8" font-size="10">y</text>
        <line x1="80" y1="98" x2="80" y2="102" stroke="#475569" stroke-width="1"/>
        <line x1="60" y1="98" x2="60" y2="102" stroke="#475569" stroke-width="1"/>
        <line x1="120" y1="98" x2="120" y2="102" stroke="#475569" stroke-width="1"/>
        <line x1="140" y1="98" x2="140" y2="102" stroke="#475569" stroke-width="1"/>
        <line x1="98" y1="80" x2="102" y2="80" stroke="#475569" stroke-width="1"/>
        <line x1="98" y1="60" x2="102" y2="60" stroke="#475569" stroke-width="1"/>
        <line x1="98" y1="120" x2="102" y2="120" stroke="#475569" stroke-width="1"/>
        <line x1="98" y1="140" x2="102" y2="140" stroke="#475569" stroke-width="1"/>
        <text x="76" y="114" fill="#64748b" font-size="8">-1</text>
        <text x="56" y="114" fill="#64748b" font-size="8">-2</text>
        <text x="118" y="114" fill="#64748b" font-size="8">1</text>
        <text x="138" y="114" fill="#64748b" font-size="8">2</text>
        <text x="104" y="84" fill="#64748b" font-size="8">1</text>
        <text x="104" y="64" fill="#64748b" font-size="8">2</text>
        <text x="104" y="124" fill="#64748b" font-size="8">-1</text>
        <text x="104" y="144" fill="#64748b" font-size="8">-2</text>
        {points_svg}
      </svg>
    </div>"""

    # ── 5. Olasilik ─────────────────────────────────────────────
    if any(k in txt for k in ["olasilik", "olasılık", "olasılığ", "olasiligi"]) or "olasilik" in konu_lower or "olasılık" in konu_lower:
        # Zar
        if any(k in txt for k in ["zar", "zarın", "zarin"]):
            # 6 yuzlu zar gorseli
            dots_map = {
                1: [(25,25)],
                2: [(12,12),(38,38)],
                3: [(12,12),(25,25),(38,38)],
                4: [(12,12),(38,12),(12,38),(38,38)],
                5: [(12,12),(38,12),(25,25),(12,38),(38,38)],
                6: [(12,12),(38,12),(12,25),(38,25),(12,38),(38,38)],
            }
            dice_html = ""
            for face in range(1, 7):
                dots = "".join(f'<div style="position:absolute;left:{dx}px;top:{dy}px;width:7px;height:7px;background:#e2e8f0;border-radius:50%"></div>' for dx, dy in dots_map[face])
                dice_html += f"""
            <div style="position:relative;width:50px;height:50px;background:#1e293b;border:2px solid #6366f1;
                border-radius:8px;margin:3px">{dots}</div>"""
            return f"""
    <div style="display:flex;justify-content:center;margin:12px 0">
      <div style="display:flex;flex-wrap:wrap;max-width:180px;justify-content:center">{dice_html}</div>
    </div>"""
        # Yazi-tura
        if any(k in txt for k in ["yazi", "yazı", "tura", "bozuk para", "madeni"]):
            return """
    <div style="display:flex;justify-content:center;gap:16px;margin:12px 0">
      <div style="width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#f59e0b,#d97706);
          display:flex;align-items:center;justify-content:center;border:2px solid #fcd34d">
        <span style="color:#1e293b;font-weight:800;font-size:0.85rem">YAZI</span>
      </div>
      <div style="width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#4338ca);
          display:flex;align-items:center;justify-content:center;border:2px solid #a5b4fc">
        <span style="color:#e0e7ff;font-weight:800;font-size:0.85rem">TURA</span>
      </div>
    </div>"""
        # Kart
        if any(k in txt for k in ["kart", "iskambil", "deste"]):
            suits = [
                ("\u2660", "#e2e8f0"),
                ("\u2665", "#ef4444"),
                ("\u2666", "#ef4444"),
                ("\u2663", "#e2e8f0"),
            ]
            cards_html = ""
            for sym, clr in suits:
                cards_html += f"""
            <div style="width:40px;height:56px;background:#1e293b;border:1.5px solid #475569;border-radius:6px;
                display:flex;align-items:center;justify-content:center;margin:2px">
              <span style="color:{clr};font-size:1.3rem">{sym}</span>
            </div>"""
            return f"""
    <div style="display:flex;justify-content:center;margin:12px 0">
      <div style="display:flex;gap:4px">{cards_html}</div>
    </div>"""
        # Genel olasilik ikonu
        return ""

    # ── 6. Veri Analizi ─────────────────────────────────────────
    if any(k in txt for k in ["veri", "ortalama", "medyan", "mod ", "grafig", "tablo", "frekans"]) or any(k in konu_lower for k in ["veri", "istatistik"]):
        nums = re.findall(r'\b(\d{1,3})\b', soru_text)
        nums = [int(n) for n in nums if 1 <= int(n) <= 200]
        if len(nums) >= 3:
            vals = nums[:8]  # max 8 bar
            mx = max(vals) if vals else 1
            bars_html = ""
            colors = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899", "#14b8a6"]
            for i, v in enumerate(vals):
                h = max(int(120 * v / mx), 8)
                c = colors[i % len(colors)]
                bars_html += f"""
            <div style="display:flex;flex-direction:column;align-items:center;gap:2px">
              <span style="color:#94a3b8;font-size:0.65rem">{v}</span>
              <div style="width:22px;height:{h}px;background:linear-gradient(180deg,{c},{c}88);
                  border-radius:4px 4px 0 0"></div>
            </div>"""
            return f"""
    <div style="display:flex;justify-content:center;margin:12px 0">
      <div style="display:flex;align-items:flex-end;gap:6px;padding:8px 12px;
          background:#0f172a;border-radius:10px;border:1px solid #1e293b">
        {bars_html}
      </div>
    </div>"""

    # ── 7. Uslu Sayilar / Karekok ───────────────────────────────
    if any(k in txt for k in ["uslu", "üslü", "kuvvet", "karekok", "karekök", "küp kök", "kup kok"]) or any(k in konu_lower for k in ["uslu", "üslü", "karekok", "karekök", "kuvvet"]):
        # Ust ifadelerini bul
        power_match = re.search(r'(\d+)\s*\^\s*(\d+)', soru_text)
        sqrt_match = re.search(r'(?:sqrt|karekök|karekok)\s*\(?(\d+)\)?', txt)
        display_parts = []
        if power_match:
            base = power_match.group(1)
            exp = power_match.group(2)
            display_parts.append(f'<span style="font-size:1.8rem;color:#e0e7ff;font-weight:800">{base}<sup style="font-size:1rem;color:#f59e0b">{exp}</sup></span>')
        if sqrt_match:
            radicand = sqrt_match.group(1)
            display_parts.append(f"""
            <span style="display:inline-block;font-size:1.6rem;color:#e0e7ff;font-weight:800">
              <span style="color:#10b981;font-size:1.4rem">\u221A</span><span style="border-top:2px solid #10b981;padding:0 4px">{radicand}</span>
            </span>""")
        if not display_parts:
            # Genel uslu sayi gosterimi
            all_powers = re.findall(r'(\d+)\^(\d+)', soru_text)
            for b, e in all_powers[:3]:
                display_parts.append(f'<span style="font-size:1.6rem;color:#e0e7ff;font-weight:800;margin:0 8px">{b}<sup style="font-size:0.9rem;color:#f59e0b">{e}</sup></span>')
        if display_parts:
            content = " ".join(display_parts)
            return f"""
    <div style="display:flex;justify-content:center;margin:12px 0">
      <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:12px;padding:14px 24px;
          border:1.5px solid #4338ca;display:flex;align-items:center;gap:12px">
        {content}
      </div>
    </div>"""

    # ── 8. Carpanlar-Katlar ─────────────────────────────────────
    if any(k in txt for k in ["carpan", "çarpan", "asal carpan", "asal çarpan", "carpanlara ayir", "çarpanlara ayır", "katlar", "kat "]) or any(k in konu_lower for k in ["carpan", "çarpan", "katlar"]):
        # Bir sayi bul ve carpan agaci goster
        num_match = re.search(r'\b(\d{2,4})\b', soru_text)
        if num_match:
            n = int(num_match.group(1))
            if 2 <= n <= 9999:
                # Asal carpanlara ayir
                factors = []
                temp = n
                d = 2
                while d * d <= temp and len(factors) < 6:
                    while temp % d == 0:
                        factors.append(d)
                        temp = temp // d
                    d += 1
                if temp > 1:
                    factors.append(temp)
                if factors:
                    tree_rows = ""
                    current = n
                    for i, f in enumerate(factors):
                        indent = i * 18
                        next_val = current // f
                        tree_rows += f"""
              <div style="display:flex;align-items:center;margin-left:{indent}px;margin-bottom:2px">
                <span style="color:#e0e7ff;font-weight:700;font-size:0.85rem;min-width:40px">{current}</span>
                <span style="color:#475569;margin:0 6px">|</span>
                <span style="color:#f59e0b;font-weight:800;font-size:0.85rem">{f}</span>
              </div>"""
                        current = next_val
                    tree_rows += f"""
              <div style="display:flex;align-items:center;margin-left:{len(factors)*18}px">
                <span style="color:#10b981;font-weight:800;font-size:0.85rem">1</span>
              </div>"""
                    factor_str = " x ".join(str(f) for f in factors)
                    return f"""
    <div style="display:flex;justify-content:center;margin:12px 0">
      <div style="background:#0f172a;border-radius:10px;padding:10px 16px;border:1px solid #1e293b">
        <div style="color:#94a3b8;font-size:0.7rem;margin-bottom:6px;text-align:center">Carpan Agaci</div>
        {tree_rows}
        <div style="text-align:center;margin-top:6px;padding-top:6px;border-top:1px solid #1e293b">
          <span style="color:#a5b4fc;font-size:0.8rem;font-weight:600">{n} = {factor_str}</span>
        </div>
      </div>
    </div>"""

    # ── 9. Oran-Oranti ──────────────────────────────────────────
    if any(k in txt for k in ["oran", "orant", "orantı"]) or any(k in konu_lower for k in ["oran", "orantı", "orant"]):
        ratio_match = re.search(r'(\d+)\s*[:/]\s*(\d+)', soru_text)
        if ratio_match:
            a = int(ratio_match.group(1))
            b = int(ratio_match.group(2))
            total = a + b
            if total > 0:
                pct_a = round(100 * a / total)
                pct_b = 100 - pct_a
                return f"""
    <div style="display:flex;justify-content:center;margin:12px 0">
      <div style="width:280px">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px">
          <span style="color:#a5b4fc;font-size:0.75rem;font-weight:700">{a}</span>
          <span style="color:#fcd34d;font-size:0.75rem;font-weight:700">{b}</span>
        </div>
        <div style="display:flex;height:28px;border-radius:8px;overflow:hidden;border:1.5px solid #334155">
          <div style="width:{pct_a}%;background:linear-gradient(135deg,#6366f1,#818cf8);
              display:flex;align-items:center;justify-content:center">
            <span style="color:#fff;font-size:0.7rem;font-weight:700">{a}</span>
          </div>
          <div style="width:{pct_b}%;background:linear-gradient(135deg,#f59e0b,#fbbf24);
              display:flex;align-items:center;justify-content:center">
            <span style="color:#1e293b;font-size:0.7rem;font-weight:700">{b}</span>
          </div>
        </div>
        <div style="text-align:center;margin-top:4px">
          <span style="color:#94a3b8;font-size:0.7rem">Oran: {a} : {b}</span>
        </div>
      </div>
    </div>"""

    # ── 10. EBOB-EKOK ───────────────────────────────────────────
    if any(k in txt for k in ["ebob", "ekok"]) or any(k in konu_lower for k in ["ebob", "ekok"]):
        nums_found = re.findall(r'\b(\d{2,4})\b', soru_text)
        nums_found = [int(n) for n in nums_found if 2 <= int(n) <= 9999]
        if len(nums_found) >= 2:
            a, b = nums_found[0], nums_found[1]
            # Asal carpanlari bul
            def _prime_factors(n):
                fs = {}
                d = 2
                while d * d <= n:
                    while n % d == 0:
                        fs[d] = fs.get(d, 0) + 1
                        n //= d
                    d += 1
                if n > 1:
                    fs[n] = fs.get(n, 0) + 1
                return fs
            fa = _prime_factors(a)
            fb = _prime_factors(b)
            all_primes = sorted(set(list(fa.keys()) + list(fb.keys())))
            only_a_parts = []
            common_parts = []
            only_b_parts = []
            for p in all_primes:
                ca = fa.get(p, 0)
                cb = fb.get(p, 0)
                common = min(ca, cb)
                if common > 0:
                    common_parts.append(f"{p}^{common}" if common > 1 else str(p))
                diff_a = ca - common
                diff_b = cb - common
                if diff_a > 0:
                    only_a_parts.append(f"{p}^{diff_a}" if diff_a > 1 else str(p))
                if diff_b > 0:
                    only_b_parts.append(f"{p}^{diff_b}" if diff_b > 1 else str(p))
            oa_txt = ", ".join(only_a_parts) if only_a_parts else "-"
            cm_txt = ", ".join(common_parts) if common_parts else "-"
            ob_txt = ", ".join(only_b_parts) if only_b_parts else "-"
            return f"""
    <div style="display:flex;justify-content:center;margin:12px 0">
      <div style="position:relative;width:320px;height:160px">
        <div style="position:absolute;left:20px;top:15px;width:160px;height:130px;
            border-radius:50%;border:2.5px solid #6366f1;background:rgba(99,102,241,0.08);
            display:flex;align-items:center;padding-left:16px">
          <span style="color:#a5b4fc;font-size:0.8rem;font-weight:700">{oa_txt}</span>
        </div>
        <div style="position:absolute;right:20px;top:15px;width:160px;height:130px;
            border-radius:50%;border:2.5px solid #f59e0b;background:rgba(245,158,11,0.08);
            display:flex;align-items:center;justify-content:flex-end;padding-right:16px">
          <span style="color:#fcd34d;font-size:0.8rem;font-weight:700">{ob_txt}</span>
        </div>
        <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2;text-align:center">
          <span style="color:#10b981;font-size:0.85rem;font-weight:800">{cm_txt}</span>
        </div>
        <div style="position:absolute;left:50px;top:0;color:#818cf8;font-weight:800;font-size:0.8rem">{a}</div>
        <div style="position:absolute;right:50px;top:0;color:#f59e0b;font-weight:800;font-size:0.8rem">{b}</div>
        <div style="position:absolute;left:50%;bottom:0;transform:translateX(-50%);
            color:#94a3b8;font-size:0.7rem">EBOB = ortak | EKOK = hepsi</div>
      </div>
    </div>"""

    # Gorsel uretilecek konu bulunamadi
    return ""


def _quiz_sinav_motoru(sorular, sinav_turu, prefix):
    """Ortak sinav arayuzu - LGS/TYT/AYT icin kullanilir.

    Args:
        sorular: Soru listesi (dict)
        sinav_turu: "LGS" / "TYT" / "AYT"
        prefix: session_state key prefix (benzersizlik icin)
    """
    sk = f"mk_sb_{prefix}"  # session key prefix

    # --- Konu listesi ---
    konular = sorted(set(s["konu"] for s in sorular))

    # --- Baslatma / Sifirlama ---
    if f"{sk}_aktif" not in st.session_state:
        st.session_state[f"{sk}_aktif"] = False
        st.session_state[f"{sk}_bitti"] = False
        st.session_state[f"{sk}_siralama"] = list(range(len(sorular)))
        st.session_state[f"{sk}_cevaplar"] = {}
        st.session_state[f"{sk}_baslangic"] = None

    # --- Kontroller ---
    col_f1, col_f2, col_f3 = st.columns([2, 2, 2])
    with col_f1:
        secili_konu = st.selectbox(
            "Konu Filtresi",
            ["Tumu"] + konular,
            key=f"{sk}_konu_filtre",
        )
    with col_f2:
        gosterim = st.radio(
            "Gorunum",
            ["5erli Goster", "Tek Tek Goster", "Tumu Goster"],
            key=f"{sk}_gosterim",
            horizontal=True,
        )
    with col_f3:
        if st.button("Yeni Sinav Baslat", key=f"{sk}_baslat_btn", use_container_width=True):
            sira = list(range(len(sorular)))
            random.shuffle(sira)
            st.session_state[f"{sk}_siralama"] = sira
            st.session_state[f"{sk}_cevaplar"] = {}
            st.session_state[f"{sk}_aktif"] = True
            st.session_state[f"{sk}_bitti"] = False
            st.session_state[f"{sk}_baslangic"] = time.time()
            st.session_state[f"{sk}_sayfa"] = 0
            st.rerun()

    if not st.session_state[f"{sk}_aktif"] and not st.session_state[f"{sk}_bitti"]:
        st.info(f"{sinav_turu} Matematik sinavina baslamak icin 'Yeni Sinav Baslat' tusuna basin.")
        return

    # --- Timer ---
    if st.session_state[f"{sk}_baslangic"] and not st.session_state[f"{sk}_bitti"]:
        gecen = int(time.time() - st.session_state[f"{sk}_baslangic"])
        dk = gecen // 60
        sn = gecen % 60
        st.markdown(f"**Gecen Sure:** {dk:02d}:{sn:02d}")

    # --- Sorulari filtrele ve sirala ---
    sira = st.session_state[f"{sk}_siralama"]
    filtre_sorular = []
    for idx in sira:
        s = sorular[idx]
        if secili_konu == "Tumu" or s["konu"] == secili_konu:
            filtre_sorular.append((idx, s))

    if not filtre_sorular:
        st.warning("Secilen konuda soru bulunamadi.")
        return

    # --- Sinav devam ediyor ---
    if st.session_state[f"{sk}_aktif"] and not st.session_state[f"{sk}_bitti"]:
        if gosterim == "5erli Goster":
            # 5'erli sayfalama
            if f"{sk}_5sayfa" not in st.session_state:
                st.session_state[f"{sk}_5sayfa"] = 0
            sayfa5 = st.session_state[f"{sk}_5sayfa"]
            toplam_sayfa = (len(filtre_sorular) + 4) // 5
            baslangic = sayfa5 * 5
            bitis = min(baslangic + 5, len(filtre_sorular))

            st.markdown(f"**Sayfa {sayfa5+1}/{toplam_sayfa}** — Soru {baslangic+1}-{bitis} / {len(filtre_sorular)}")

            for q_num, (idx, s) in enumerate(filtre_sorular[baslangic:bitis], baslangic + 1):
                soru_html = _matematik_format_html(s['soru'])
                gorsel = _soru_gorseli(s['soru'], s.get('konu', ''))
                _render_html(f"""
                <div style="background:#0f172a;border-radius:12px;padding:14px 18px;margin:10px 0;border-left:4px solid #6366f1">
                    <div style="color:#94a3b8;font-size:0.7rem;margin-bottom:4px">Soru {q_num} — {s['konu']}</div>
                    <div style="color:#e2e8f0;font-size:1rem;line-height:1.8">{soru_html}</div>
                    {gorsel}
                </div>
                """)
                # Format math notation in options for radio display
                formatted_secenekler = [_matematik_format_text(opt) for opt in s["secenekler"]]
                secim = st.radio(
                    f"Cevabiniz (S{q_num})",
                    formatted_secenekler,
                    index=None,
                    key=f"{sk}_q_{idx}",
                )
                if secim is not None:
                    sec_idx = s["secenekler"].index(secim)
                    st.session_state[f"{sk}_cevaplar"][idx] = sec_idx

            # Sayfa navigasyonu
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if sayfa5 > 0:
                    if st.button("Onceki 5", key=f"{sk}_5prev"):
                        st.session_state[f"{sk}_5sayfa"] = sayfa5 - 1
                        st.rerun()
            with nav2:
                st.markdown(f"<div style='text-align:center;color:#94a3b8;font-size:0.8rem'>{baslangic+1}-{bitis} / {len(filtre_sorular)}</div>", unsafe_allow_html=True)
            with nav3:
                if bitis < len(filtre_sorular):
                    if st.button("Sonraki 5", key=f"{sk}_5next"):
                        st.session_state[f"{sk}_5sayfa"] = sayfa5 + 1
                        st.rerun()

        elif gosterim == "Tumu Goster":
            for q_num, (idx, s) in enumerate(filtre_sorular, 1):
                soru_html = _matematik_format_html(s['soru'])
                gorsel = _soru_gorseli(s['soru'], s.get('konu', ''))
                _render_html(f"""
                <div style="background:#0f172a;border-radius:12px;padding:14px 18px;margin:10px 0;border-left:4px solid #6366f1">
                    <div style="color:#94a3b8;font-size:0.7rem;margin-bottom:4px">Soru {q_num} — {s['konu']}</div>
                    <div style="color:#e2e8f0;font-size:1rem;line-height:1.8">{soru_html}</div>
                    {gorsel}
                </div>
                """)
                fmt_secenekler = [_matematik_format_html(sec) for sec in s["secenekler"]]
                # Format math notation in options for radio display
                formatted_secenekler = [_matematik_format_text(opt) for opt in s["secenekler"]]
                secim = st.radio(
                    f"Cevabiniz (S{q_num})",
                    formatted_secenekler,
                    index=None,
                    key=f"{sk}_q_{idx}",
                )
                if secim is not None:
                    sec_idx = s["secenekler"].index(secim)
                    st.session_state[f"{sk}_cevaplar"][idx] = sec_idx
        else:
            # Tek tek gosterim
            if f"{sk}_sayfa" not in st.session_state:
                st.session_state[f"{sk}_sayfa"] = 0
            sayfa = st.session_state[f"{sk}_sayfa"]
            if sayfa >= len(filtre_sorular):
                sayfa = len(filtre_sorular) - 1
                st.session_state[f"{sk}_sayfa"] = sayfa

            idx, s = filtre_sorular[sayfa]
            soru_html = _matematik_format_html(s['soru'])
            gorsel = _soru_gorseli(s['soru'], s.get('konu', ''))
            _render_html(f"""
            <div style="background:#0f172a;border-radius:12px;padding:14px 18px;margin:10px 0;border-left:4px solid #6366f1">
                <div style="color:#94a3b8;font-size:0.7rem;margin-bottom:4px">Soru {sayfa+1}/{len(filtre_sorular)} — {s['konu']}</div>
                <div style="color:#e2e8f0;font-size:1rem;line-height:1.8">{soru_html}</div>
                {gorsel}
            </div>
            """)
            prev_ans = st.session_state[f"{sk}_cevaplar"].get(idx)
            secim = st.radio(
                "Cevabiniz",
                s["secenekler"],
                index=prev_ans if prev_ans is not None else None,
                key=f"{sk}_q_{idx}",
                format_func=lambda x: _matematik_format_html(x),
            )
            if secim is not None:
                sec_idx = s["secenekler"].index(secim)
                st.session_state[f"{sk}_cevaplar"][idx] = sec_idx

            nav_c1, nav_c2, nav_c3 = st.columns([1, 2, 1])
            with nav_c1:
                if sayfa > 0:
                    if st.button("Onceki", key=f"{sk}_prev"):
                        st.session_state[f"{sk}_sayfa"] = sayfa - 1
                        st.rerun()
            with nav_c3:
                if sayfa < len(filtre_sorular) - 1:
                    if st.button("Sonraki", key=f"{sk}_next"):
                        st.session_state[f"{sk}_sayfa"] = sayfa + 1
                        st.rerun()
            with nav_c2:
                cevaplanan = sum(1 for i2, _ in filtre_sorular if i2 in st.session_state[f"{sk}_cevaplar"])
                st.markdown(f"Cevaplanan: {cevaplanan}/{len(filtre_sorular)}")

        st.markdown("---")
        if st.button("Sinavi Bitir", key=f"{sk}_bitir_btn", type="primary", use_container_width=True):
            st.session_state[f"{sk}_aktif"] = False
            st.session_state[f"{sk}_bitti"] = True
            st.rerun()

    # --- Sonuclar ---
    if st.session_state[f"{sk}_bitti"]:
        gecen = 0
        if st.session_state[f"{sk}_baslangic"]:
            gecen = int(time.time() - st.session_state[f"{sk}_baslangic"])
        dk = gecen // 60
        sn = gecen % 60

        cevaplar = st.session_state[f"{sk}_cevaplar"]
        dogru = 0
        yanlis = 0
        bos = 0
        konu_dogru = {}
        konu_toplam = {}
        yanlis_sorular = []

        for idx, s in enumerate(sorular):
            kn = s["konu"]
            konu_toplam[kn] = konu_toplam.get(kn, 0) + 1
            if idx in cevaplar:
                if cevaplar[idx] == s["cevap"]:
                    dogru += 1
                    konu_dogru[kn] = konu_dogru.get(kn, 0) + 1
                else:
                    yanlis += 1
                    yanlis_sorular.append((idx, s, cevaplar[idx]))
            else:
                bos += 1

        toplam = len(sorular)
        puan = round(100 * dogru / toplam, 1) if toplam > 0 else 0

        styled_section(f"{sinav_turu} Sinav Sonuclari", "#6366f1")

        rc1, rc2, rc3, rc4 = st.columns(4)
        rc1.metric("Puan", f"{puan}/100")
        rc2.metric("Dogru", str(dogru))
        rc3.metric("Yanlis", str(yanlis))
        rc4.metric("Bos", str(bos))

        st.markdown(f"**Sure:** {dk:02d}:{sn:02d}")

        # --- Sonuc gorseli ---
        _render_html(f"""
        <div style="display:flex;gap:16px;justify-content:center;margin:16px 0">
            <div style="background:#10b981;color:#fff;padding:12px 24px;border-radius:12px;font-weight:700">
                Dogru: {dogru}
            </div>
            <div style="background:#ef4444;color:#fff;padding:12px 24px;border-radius:12px;font-weight:700">
                Yanlis: {yanlis}
            </div>
            <div style="background:#6b7280;color:#fff;padding:12px 24px;border-radius:12px;font-weight:700">
                Bos: {bos}
            </div>
        </div>
        """)

        # --- Konu bazli analiz ---
        styled_section("Konu Bazli Analiz", "#8b5cf6")
        for kn in sorted(konu_toplam.keys()):
            kt = konu_toplam[kn]
            kd = konu_dogru.get(kn, 0)
            oran = round(100 * kd / kt, 1) if kt > 0 else 0
            if oran >= 70:
                renk = "#10b981"
                durum = "Basarili"
            elif oran >= 50:
                renk = "#f59e0b"
                durum = "Orta"
            else:
                renk = "#ef4444"
                durum = "Gelistirilmeli"
            _render_html(f"""
            <div style="background:linear-gradient(135deg,{renk}15,{renk}08);border-radius:12px;
                         padding:12px 16px;margin-bottom:8px;border-left:4px solid {renk};
                         border:1px solid {renk}30">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="font-weight:700;color:#e0e7ff !important">{kn}</span>
                    <span style="color:{renk} !important;font-weight:700">{kd}/{kt} (%{oran}) - {durum}</span>
                </div>
            </div>
            """)

        # --- Yanlis cevap inceleme ---
        if yanlis_sorular:
            styled_section("Yanlis Cevaplarin Incelenmesi", "#ef4444")
            for idx, s, verilen in yanlis_sorular:
                dogru_sec = s["secenekler"][s["cevap"]]
                verilen_sec = s["secenekler"][verilen]
                st.markdown(f"""
**Soru:** {s['soru']}
- Sizin cevabin: {verilen_sec}
- Dogru cevap: {dogru_sec}
- **Aciklama:** {s['aciklama']}
---""")

        # --- TXT rapor indirme ---
        rapor_satirlari = []
        rapor_satirlari.append(f"{sinav_turu} MATEMATIK SINAV SONUCU")
        rapor_satirlari.append(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        rapor_satirlari.append(f"Sure: {dk:02d}:{sn:02d}")
        rapor_satirlari.append(f"Puan: {puan}/100")
        rapor_satirlari.append(f"Dogru: {dogru} | Yanlis: {yanlis} | Bos: {bos}")
        rapor_satirlari.append("")
        rapor_satirlari.append("KONU BAZLI ANALIZ")
        rapor_satirlari.append("-" * 40)
        for kn in sorted(konu_toplam.keys()):
            kt = konu_toplam[kn]
            kd = konu_dogru.get(kn, 0)
            oran = round(100 * kd / kt, 1) if kt > 0 else 0
            rapor_satirlari.append(f"  {kn}: {kd}/{kt} (%{oran})")
        rapor_satirlari.append("")
        if yanlis_sorular:
            rapor_satirlari.append("YANLIS CEVAPLAR")
            rapor_satirlari.append("-" * 40)
            for idx, s, verilen in yanlis_sorular:
                rapor_satirlari.append(f"  Soru: {s['soru']}")
                rapor_satirlari.append(f"  Verilen: {s['secenekler'][verilen]}")
                rapor_satirlari.append(f"  Dogru: {s['secenekler'][s['cevap']]}")
                rapor_satirlari.append(f"  Aciklama: {s['aciklama']}")
                rapor_satirlari.append("")

        rapor_txt = "\n".join(rapor_satirlari)
        st.download_button(
            label="PDF Indir",
            data=rapor_txt.encode("utf-8"),
            file_name=f"{sinav_turu}_sinav_sonucu_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            key=f"{sk}_pdf_indir",
        )


def _render_lgs_yks_soru_bankasi():
    """LGS/YKS Soru Bankasi ana fonksiyonu."""
    styled_section("LGS/YKS Soru Bankasi", "#6366f1")
    _render_html("""
    <div style="background:linear-gradient(135deg,#312e81,#4338ca);border-radius:16px;
                 padding:20px 24px;margin-bottom:20px;border:1px solid rgba(99,102,241,0.3)">
        <h3 style="color:#e0e7ff !important;margin:0 0 8px 0">LGS / YKS Matematik Soru Bankasi</h3>
        <p style="color:#a5b4fc !important;margin:0;font-size:0.9rem">
            LGS (8. Sinif), TYT (9-12. Sinif) ve AYT (11-12. Sinif) seviyesinde
            matematik sorulari ile kendinizi test edin.
        </p>
    </div>
    """)

    sub_tabs = st.tabs([
        "LGS Matematik (8. Sinif)",
        "TYT Matematik (9-12. Sinif)",
        "AYT Matematik (11-12. Sinif)",
    ])

    with sub_tabs[0]:
        st.markdown("**LGS Matematik - 50 Soru (10 Konu x 5 Soru)**")
        _quiz_sinav_motoru(_lgs_sorulari(), "LGS", "lgs")

    with sub_tabs[1]:
        st.markdown("**TYT Matematik - 40 Soru (12 Konu)**")
        _quiz_sinav_motoru(_tyt_sorulari(), "TYT", "tyt")

    with sub_tabs[2]:
        st.markdown("**AYT Matematik - 40 Soru (10 Konu)**")
        _quiz_sinav_motoru(_ayt_sorulari(), "AYT", "ayt")


# ══════════════════════════════════════════════════════════════════════════════
# ADIM ADIM COZUM ANIMASYONU
# ══════════════════════════════════════════════════════════════════════════════

_ADIM_ADIM_PROBLEMLER = [
    # --- Denklem Cozme (4) ---
    {
        "baslik": "Birinci Dereceden Denklem",
        "konu": "Denklem",
        "soru": "2x + 6 = 14 denklemini cozunuz.",
        "adimlar": [
            "Denklem: 2x + 6 = 14",
            "Adim 1: Her iki taraftan 6 cikar -> 2x + 6 - 6 = 14 - 6",
            "Adim 2: Sadelelestir -> 2x = 8",
            "Adim 3: Her iki tarafi 2'ye bol -> 2x / 2 = 8 / 2",
            "Adim 4: Sonuc -> x = 4",
        ],
        "sonuc": "x = 4",
    },
    {
        "baslik": "Iki Bilinmeyenli Denklem",
        "konu": "Denklem",
        "soru": "x + y = 10 ve x - y = 4 denklem sistemini cozunuz.",
        "adimlar": [
            "Denklem 1: x + y = 10  |  Denklem 2: x - y = 4",
            "Adim 1: Iki denklemi topla -> (x+y) + (x-y) = 10 + 4",
            "Adim 2: Sadelelestir -> 2x = 14",
            "Adim 3: x = 7 bulduk",
            "Adim 4: x = 7 degerini Denklem 1'e yaz -> 7 + y = 10",
            "Adim 5: y = 3 bulduk",
        ],
        "sonuc": "x = 7, y = 3",
    },
    {
        "baslik": "Ikinci Derece Denklem",
        "konu": "Denklem",
        "soru": "x^2 - 5x + 6 = 0 denklemini cozunuz.",
        "adimlar": [
            "Denklem: x^2 - 5x + 6 = 0",
            "Adim 1: Carpanlara ayir. Carpimi 6, toplami -5 veren iki sayi bul",
            "Adim 2: -2 ve -3 sayilari: (-2) x (-3) = 6, (-2) + (-3) = -5",
            "Adim 3: (x - 2)(x - 3) = 0 yazilir",
            "Adim 4: x - 2 = 0 -> x = 2  veya  x - 3 = 0 -> x = 3",
        ],
        "sonuc": "x = 2 veya x = 3",
    },
    {
        "baslik": "Kesirli Denklem",
        "konu": "Denklem",
        "soru": "(3x - 1) / 2 = 7 denklemini cozunuz.",
        "adimlar": [
            "Denklem: (3x - 1) / 2 = 7",
            "Adim 1: Iki tarafı 2 ile carp -> 3x - 1 = 14",
            "Adim 2: Her iki tarafa 1 ekle -> 3x = 15",
            "Adim 3: Her iki tarafi 3'e bol -> x = 5",
        ],
        "sonuc": "x = 5",
    },
    # --- Geometri (4) ---
    {
        "baslik": "Ucgen Alan Hesabi",
        "konu": "Geometri",
        "soru": "Tabani 10 cm, yuksekligi 6 cm olan ucgenin alanini bulunuz.",
        "adimlar": [
            "Ucgen alan formulunu hatirlayalim: A = (taban x yukseklik) / 2",
            "Adim 1: Degerleri yaz -> A = (10 x 6) / 2",
            "Adim 2: Carpimi hesapla -> A = 60 / 2",
            "Adim 3: Bolmeyi yap -> A = 30 cm^2",
        ],
        "sonuc": "Alan = 30 cm^2",
    },
    {
        "baslik": "Pisagor Teoremi",
        "konu": "Geometri",
        "soru": "Dik ucgende a=3, b=4 ise hipotenüs c kactir?",
        "adimlar": [
            "Pisagor Teoremi: a^2 + b^2 = c^2",
            "Adim 1: Degerleri yaz -> 3^2 + 4^2 = c^2",
            "Adim 2: Kare al -> 9 + 16 = c^2",
            "Adim 3: Topla -> 25 = c^2",
            "Adim 4: Karekok al -> c = 5",
        ],
        "sonuc": "c = 5",
    },
    {
        "baslik": "Daire Cevresi",
        "konu": "Geometri",
        "soru": "Yaricapi 7 cm olan dairenin cevresini bulunuz (pi=22/7).",
        "adimlar": [
            "Daire cevre formulu: C = 2 x pi x r",
            "Adim 1: Degerleri yaz -> C = 2 x (22/7) x 7",
            "Adim 2: 7'leri sadelelestir -> C = 2 x 22",
            "Adim 3: Carp -> C = 44 cm",
        ],
        "sonuc": "Cevre = 44 cm",
    },
    {
        "baslik": "Dikdortgen Kosegen",
        "konu": "Geometri",
        "soru": "6 cm ve 8 cm kenarli dikdortgenin kosegen uzunlugu kactir?",
        "adimlar": [
            "Dikdortgen kosegeni bir dik ucgenin hipotenusu olusturur",
            "Adim 1: Pisagor uygula -> d^2 = 6^2 + 8^2",
            "Adim 2: d^2 = 36 + 64 = 100",
            "Adim 3: d = Karekok(100) = 10 cm",
        ],
        "sonuc": "Kosegen = 10 cm",
    },
    # --- Kesir (4) ---
    {
        "baslik": "Kesir Toplama",
        "konu": "Kesir",
        "soru": "2/3 + 1/4 islemini yapiniz.",
        "adimlar": [
            "Paydalar farkli: 3 ve 4. Ortak payda bul",
            "Adim 1: EKOK(3, 4) = 12. Ortak payda 12",
            "Adim 2: 2/3 = (2x4)/(3x4) = 8/12",
            "Adim 3: 1/4 = (1x3)/(4x3) = 3/12",
            "Adim 4: 8/12 + 3/12 = 11/12",
        ],
        "sonuc": "2/3 + 1/4 = 11/12",
    },
    {
        "baslik": "Kesir Carpma",
        "konu": "Kesir",
        "soru": "3/5 x 10/9 islemini yapiniz.",
        "adimlar": [
            "Kesirlerde carpma: Pay x Pay / Payda x Payda",
            "Adim 1: (3 x 10) / (5 x 9) = 30 / 45",
            "Adim 2: EBOB(30, 45) = 15 ile sadelelestir",
            "Adim 3: 30/45 = 2/3",
        ],
        "sonuc": "3/5 x 10/9 = 2/3",
    },
    {
        "baslik": "Bilesik Kesir",
        "konu": "Kesir",
        "soru": "1 + 1/(1 + 1/2) ifadesini hesaplayiniz.",
        "adimlar": [
            "Ic icten disa dogru coz",
            "Adim 1: Ilk olarak 1/2'yi hesapla: 1/2",
            "Adim 2: 1 + 1/2 = 3/2",
            "Adim 3: 1 / (3/2) = 2/3",
            "Adim 4: 1 + 2/3 = 5/3",
        ],
        "sonuc": "Sonuc = 5/3",
    },
    {
        "baslik": "Kesir Bolme",
        "konu": "Kesir",
        "soru": "4/7 : 2/3 islemini yapiniz.",
        "adimlar": [
            "Kesir bolme: Birinci kesri, ikincinin tersi ile carp",
            "Adim 1: 4/7 : 2/3 = 4/7 x 3/2",
            "Adim 2: (4 x 3) / (7 x 2) = 12/14",
            "Adim 3: EBOB(12,14)=2 ile sadelelestir -> 6/7",
        ],
        "sonuc": "4/7 : 2/3 = 6/7",
    },
    # --- Uslu Sayilar (4) ---
    {
        "baslik": "Us Kurallari - Carpma",
        "konu": "Uslu Sayilar",
        "soru": "2^3 x 2^5 islemini hesaplayiniz.",
        "adimlar": [
            "Kural: Ayni tabanli uslulerin carpiminda usler toplanir",
            "Adim 1: 2^3 x 2^5 = 2^(3+5)",
            "Adim 2: 2^8 = 256",
        ],
        "sonuc": "2^3 x 2^5 = 256",
    },
    {
        "baslik": "Us Kurallari - Bolme",
        "konu": "Uslu Sayilar",
        "soru": "5^7 / 5^4 islemini hesaplayiniz.",
        "adimlar": [
            "Kural: Ayni tabanli uslulerin bolumunde usler cikarilir",
            "Adim 1: 5^7 / 5^4 = 5^(7-4)",
            "Adim 2: 5^3 = 125",
        ],
        "sonuc": "5^7 / 5^4 = 125",
    },
    {
        "baslik": "Usun Usu",
        "konu": "Uslu Sayilar",
        "soru": "(3^2)^3 islemini hesaplayiniz.",
        "adimlar": [
            "Kural: Usun usu -> usler carpilir",
            "Adim 1: (3^2)^3 = 3^(2x3)",
            "Adim 2: 3^6 hesapla: 3^3 = 27, 3^6 = 27 x 27",
            "Adim 3: 27 x 27 = 729",
        ],
        "sonuc": "(3^2)^3 = 729",
    },
    {
        "baslik": "Negatif Us",
        "konu": "Uslu Sayilar",
        "soru": "4^(-2) degerini hesaplayiniz.",
        "adimlar": [
            "Kural: a^(-n) = 1 / a^n",
            "Adim 1: 4^(-2) = 1 / 4^2",
            "Adim 2: 4^2 = 16",
            "Adim 3: 1/16",
        ],
        "sonuc": "4^(-2) = 1/16",
    },
    # --- Olasilik (4) ---
    {
        "baslik": "Zar Olasiligi",
        "konu": "Olasilik",
        "soru": "Bir zar atildiginda 3'ten buyuk sayi gelme olasiligi nedir?",
        "adimlar": [
            "Ornek uzay: {1, 2, 3, 4, 5, 6} -> 6 eleman",
            "Adim 1: 3'ten buyuk sayilar: {4, 5, 6} -> 3 eleman",
            "Adim 2: P = istenen / toplam = 3/6",
            "Adim 3: Sadelelestir -> 1/2",
        ],
        "sonuc": "P(X > 3) = 1/2",
    },
    {
        "baslik": "Kart Olasiligi",
        "konu": "Olasilik",
        "soru": "52 kartlik desteden 1 kart cekildiginde kupa gelme olasiligi nedir?",
        "adimlar": [
            "Toplam kart: 52. 4 tur var: kupa, karo, sinek, maca",
            "Adim 1: Her turden 13 kart var",
            "Adim 2: Kupa sayisi = 13",
            "Adim 3: P = 13/52 = 1/4",
        ],
        "sonuc": "P(Kupa) = 1/4",
    },
    {
        "baslik": "Iki Zar Toplami",
        "konu": "Olasilik",
        "soru": "Iki zar atildiginda toplamin 7 gelme olasiligi nedir?",
        "adimlar": [
            "Ornek uzay: 6 x 6 = 36 farkli sonuc",
            "Adim 1: Toplami 7 yapan ciftler: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1)",
            "Adim 2: 6 uygun sonuc var",
            "Adim 3: P = 6/36 = 1/6",
        ],
        "sonuc": "P(Toplam=7) = 1/6",
    },
    {
        "baslik": "Torba Olasiligi",
        "konu": "Olasilik",
        "soru": "Bir torbada 5 kirmizi, 3 mavi, 2 yesil bilye var. Mavi bilye cekme olasiligi nedir?",
        "adimlar": [
            "Toplam bilye: 5 + 3 + 2 = 10",
            "Adim 1: Mavi bilye sayisi = 3",
            "Adim 2: P = 3/10",
            "Adim 3: Yuzdesi: %30",
        ],
        "sonuc": "P(Mavi) = 3/10 = %30",
    },
]


def _render_adim_adim_cozum():
    """Adim Adim Cozum Animasyonu - 20 problem, adimlari tek tek goster."""
    styled_section("Adim Adim Cozum Animasyonu", "#6366f1")

    _render_html("""
    <div style="background:linear-gradient(135deg,#312e81,#4338ca);border-radius:16px;
                 padding:20px 24px;margin-bottom:20px;border:1px solid rgba(99,102,241,0.3)">
        <h3 style="color:#e0e7ff !important;margin:0 0 8px 0">Adim Adim Cozum</h3>
        <p style="color:#a5b4fc !important;margin:0;font-size:0.9rem">
            Matematik problemlerini adim adim animasyonlu olarak cozmeyi ogrenin.
            Her adimi tek tek gorun, cozmelerini izleyin!
        </p>
    </div>
    """)

    # Session state init
    if "mat_adim_idx" not in st.session_state:
        st.session_state["mat_adim_idx"] = 0
    if "mat_adim_step" not in st.session_state:
        st.session_state["mat_adim_step"] = 0

    # Problem selector
    problem_labels = [f"{i+1}. [{p['konu']}] {p['baslik']}" for i, p in enumerate(_ADIM_ADIM_PROBLEMLER)]
    col1, col2, col3 = st.columns([4, 1, 1])

    with col1:
        selected = st.selectbox(
            "Problem secin:",
            options=list(range(len(_ADIM_ADIM_PROBLEMLER))),
            format_func=lambda i: problem_labels[i],
            index=st.session_state["mat_adim_idx"],
            key="mat_adim_select",
        )
        if selected != st.session_state["mat_adim_idx"]:
            st.session_state["mat_adim_idx"] = selected
            st.session_state["mat_adim_step"] = 0
            st.rerun()

    with col2:
        if st.button("Rastgele Problem", key="mat_adim_random"):
            st.session_state["mat_adim_idx"] = random.randint(0, len(_ADIM_ADIM_PROBLEMLER) - 1)
            st.session_state["mat_adim_step"] = 0
            st.rerun()

    with col3:
        if st.button("Sifirla", key="mat_adim_reset"):
            st.session_state["mat_adim_step"] = 0
            st.rerun()

    prob = _ADIM_ADIM_PROBLEMLER[st.session_state["mat_adim_idx"]]
    total_steps = len(prob["adimlar"])
    current_step = st.session_state["mat_adim_step"]

    # Problem card
    _render_html(f"""
    <div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:14px;
                padding:20px 24px;margin:16px 0;border:1px solid rgba(99,102,241,0.3)">
        <div style="font-size:0.75rem;color:#818cf8;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px">
            {prob['konu']}
        </div>
        <div style="font-size:1.2rem;font-weight:700;color:#e0e7ff;margin-bottom:8px">
            {prob['baslik']}
        </div>
        <div style="font-size:1.05rem;color:#c7d2fe;background:rgba(99,102,241,0.1);
                    border-radius:10px;padding:14px 18px;border-left:4px solid #818cf8">
            {prob['soru']}
        </div>
    </div>
    """)

    # Step counter
    if current_step < total_steps:
        _render_html(f"""
        <div style="text-align:center;margin:10px 0;font-size:0.9rem;color:#a5b4fc">
            Adim {current_step}/{total_steps}
        </div>
        """)
    else:
        _render_html(f"""
        <div style="text-align:center;margin:10px 0;font-size:0.9rem;color:#34d399">
            Tum adimlar tamamlandi! ({total_steps}/{total_steps})
        </div>
        """)

    # Render visible steps with fade-in animation
    for i in range(min(current_step, total_steps)):
        step_text = prob["adimlar"][i]
        delay = 0 if i < current_step - 1 else 0.3
        _render_html(f"""
        <style>
            @keyframes mat_fadeIn_{st.session_state['mat_adim_idx']}_{i} {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        <div style="background:rgba(99,102,241,0.08);border-radius:10px;padding:12px 18px;
                    margin:8px 0;border-left:3px solid #6366f1;
                    animation: mat_fadeIn_{st.session_state['mat_adim_idx']}_{i} 0.5s ease {delay}s both">
            <span style="color:#818cf8;font-weight:600;font-size:0.85rem">#{i+1}</span>
            <span style="color:#e0e7ff;margin-left:10px">{step_text}</span>
        </div>
        """)

    # Sonuc card (after all steps)
    if current_step >= total_steps:
        _render_html(f"""
        <div style="background:rgba(16,185,129,0.1);border-radius:14px;padding:18px 24px;
                    margin:16px 0;border:2px solid #10b981">
            <div style="color:#34d399;font-weight:700;font-size:1.1rem;margin-bottom:4px">
                Sonuc
            </div>
            <div style="color:#a7f3d0;font-size:1.15rem;font-weight:600">
                {prob['sonuc']}
            </div>
        </div>
        """)

    # Sonraki Adim button
    if current_step < total_steps:
        if st.button(f"Sonraki Adim ({current_step + 1}/{total_steps})", key="mat_adim_next",
                     type="primary"):
            st.session_state["mat_adim_step"] = current_step + 1
            st.rerun()

    # Konu filtresi
    st.markdown("---")
    st.markdown("**Konulara Gore Problemler:**")
    konular = sorted(set(p["konu"] for p in _ADIM_ADIM_PROBLEMLER))
    for konu in konular:
        prob_list = [(i, p) for i, p in enumerate(_ADIM_ADIM_PROBLEMLER) if p["konu"] == konu]
        with st.expander(f"{konu} ({len(prob_list)} problem)"):
            for idx, p in prob_list:
                if st.button(f"{p['baslik']}", key=f"mat_adim_goto_{idx}"):
                    st.session_state["mat_adim_idx"] = idx
                    st.session_state["mat_adim_step"] = 0
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# GUNLUK MATEMATIK MARATONU
# ══════════════════════════════════════════════════════════════════════════════

def _maraton_soru_havuzu(zorluk: str):
    """Zorluk seviyesine gore soru havuzu getir."""
    if zorluk == "LGS (8.Sinif)":
        try:
            from data.lgs_sorulari import LGS_SORU_HAVUZU
            return LGS_SORU_HAVUZU
        except ImportError:
            return _lgs_sorulari()
    elif zorluk == "TYT (Lise)":
        try:
            from data.tyt_sorulari import TYT_SORU_HAVUZU
            return TYT_SORU_HAVUZU
        except ImportError:
            return _tyt_sorulari()
    else:
        try:
            from data.ayt_sorulari import AYT_SORU_HAVUZU
            return AYT_SORU_HAVUZU
        except ImportError:
            return _ayt_sorulari()


def _maraton_gunluk_sorular(zorluk: str, tarih: date):
    """Tarihe ve zorluga gore deterministik 5 soru sec."""
    havuz = _maraton_soru_havuzu(zorluk)
    if not havuz:
        return []
    seed_str = f"{tarih.isoformat()}_{zorluk}"
    seed_val = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**31)
    rng = random.Random(seed_val)
    count = min(5, len(havuz))
    return rng.sample(havuz, count)


def _render_gunluk_maraton():
    """Gunluk Matematik Maratonu - her gun 5 yeni soru."""
    styled_section("Gunluk Matematik Maratonu", "#6366f1")

    _render_html("""
    <div style="background:linear-gradient(135deg,#312e81,#4338ca);border-radius:16px;
                 padding:20px 24px;margin-bottom:20px;border:1px solid rgba(99,102,241,0.3)">
        <h3 style="color:#e0e7ff !important;margin:0 0 8px 0">Gunluk Maraton</h3>
        <p style="color:#a5b4fc !important;margin:0;font-size:0.9rem">
            Her gun 5 yeni soru! Ayni gun herkes ayni sorulari cozer.
            Zorluk seviyeni sec ve maratona katil!
        </p>
    </div>
    """)

    bugun = date.today()

    # Session state init
    if "mat_maraton_history" not in st.session_state:
        st.session_state["mat_maraton_history"] = {}  # {date_str: {zorluk: skor}}
    if "mat_maraton_answers" not in st.session_state:
        st.session_state["mat_maraton_answers"] = {}
    if "mat_maraton_submitted" not in st.session_state:
        st.session_state["mat_maraton_submitted"] = False
    if "mat_maraton_leaderboard" not in st.session_state:
        st.session_state["mat_maraton_leaderboard"] = {}  # {date_str: [(isim, skor, zorluk)]}

    # Timer: countdown to midnight
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day, 23, 59, 59)
    remaining = midnight - now
    hours_left = remaining.seconds // 3600
    mins_left = (remaining.seconds % 3600) // 60
    secs_left = remaining.seconds % 60

    _render_html(f"""
    <div style="text-align:center;margin-bottom:16px">
        <span style="color:#a5b4fc;font-size:0.85rem">Bugunun maratonu biter:</span>
        <span style="color:#818cf8;font-size:1.3rem;font-weight:700;margin-left:8px;
                     font-family:monospace">
            {hours_left:02d}:{mins_left:02d}:{secs_left:02d}
        </span>
    </div>
    """)

    # Streak counter
    streak = 0
    check_date = bugun - timedelta(days=1)
    while check_date.isoformat() in st.session_state["mat_maraton_history"]:
        streak += 1
        check_date -= timedelta(days=1)
    if bugun.isoformat() in st.session_state["mat_maraton_history"]:
        streak += 1

    if streak > 0:
        _render_html(f"""
        <div style="background:rgba(251,191,36,0.1);border-radius:12px;padding:12px 18px;
                    margin-bottom:16px;border:1px solid rgba(251,191,36,0.3);text-align:center">
            <span style="font-size:1.5rem">&#128293;</span>
            <span style="color:#fbbf24;font-weight:700;font-size:1.1rem;margin-left:8px">
                {streak} gun ust uste katildin!
            </span>
        </div>
        """)

    # Calendar view (last 30 days)
    st.markdown("**Son 30 Gun Takvimi:**")
    cal_days = []
    for i in range(29, -1, -1):
        d = bugun - timedelta(days=i)
        completed = d.isoformat() in st.session_state["mat_maraton_history"]
        is_today = d == bugun
        cal_days.append((d, completed, is_today))

    # Render calendar as a grid (6 rows x 5 cols)
    cal_html_items = []
    for d, completed, is_today in cal_days:
        bg = "#10b981" if completed else ("rgba(99,102,241,0.2)" if is_today else "rgba(99,102,241,0.05)")
        border = "2px solid #818cf8" if is_today else "1px solid rgba(99,102,241,0.1)"
        color = "#fff" if completed else ("#c7d2fe" if is_today else "#6b7280")
        cal_html_items.append(
            f'<div style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:36px;height:36px;border-radius:8px;margin:2px;background:{bg};'
            f'border:{border};font-size:0.75rem;font-weight:600;color:{color}">'
            f'{d.day}</div>'
        )
    _render_html(
        '<div style="display:flex;flex-wrap:wrap;gap:2px;margin-bottom:16px">'
        + "".join(cal_html_items)
        + "</div>"
    )

    # Difficulty selector
    zorluk = st.selectbox(
        "Zorluk Seviyesi:",
        ["LGS (8.Sinif)", "TYT (Lise)", "AYT (Ileri)"],
        key="mat_maraton_zorluk",
    )

    # Check if already submitted today for this difficulty
    bugun_str = bugun.isoformat()
    already_done = (
        bugun_str in st.session_state["mat_maraton_history"]
        and zorluk in st.session_state["mat_maraton_history"][bugun_str]
    )

    if already_done:
        skor = st.session_state["mat_maraton_history"][bugun_str][zorluk]
        _render_html(f"""
        <div style="background:rgba(16,185,129,0.1);border-radius:14px;padding:20px 24px;
                    margin:16px 0;border:2px solid #10b981;text-align:center">
            <div style="color:#34d399;font-weight:700;font-size:1.3rem;margin-bottom:8px">
                Bugunun Maratonunu Tamamladin!
            </div>
            <div style="color:#a7f3d0;font-size:1.1rem">
                {zorluk} - Skorun: {skor}/5
            </div>
        </div>
        """)
    else:
        # Get today's questions
        sorular = _maraton_gunluk_sorular(zorluk, bugun)
        if not sorular:
            st.warning("Bu zorluk seviyesi icin soru bulunamadi.")
            return

        st.markdown(f"**Bugunun {zorluk} Sorulari (5 Soru):**")

        # Render questions
        for i, s in enumerate(sorular):
            _render_html(f"""
            <div style="background:rgba(99,102,241,0.06);border-radius:12px;padding:14px 18px;
                        margin:12px 0 4px 0;border-left:3px solid #6366f1">
                <span style="color:#818cf8;font-weight:700">Soru {i+1}:</span>
                <span style="color:#e0e7ff;margin-left:8px">{s['soru']}</span>
            </div>
            """)
            secenekler = s.get("secenekler", [])
            answer_key = f"mat_maraton_ans_{i}"
            st.radio(
                f"Cevabin (Soru {i+1}):",
                options=list(range(len(secenekler))),
                format_func=lambda x, opts=secenekler: opts[x] if x < len(opts) else "",
                key=answer_key,
                label_visibility="collapsed",
            )

        # Submit button
        if st.button("Maratonu Bitir", key="mat_maraton_submit", type="primary"):
            skor = 0
            for i, s in enumerate(sorular):
                answer_key = f"mat_maraton_ans_{i}"
                user_ans = st.session_state.get(answer_key, -1)
                if user_ans == s.get("cevap", -1):
                    skor += 1

            # Save to history
            if bugun_str not in st.session_state["mat_maraton_history"]:
                st.session_state["mat_maraton_history"][bugun_str] = {}
            st.session_state["mat_maraton_history"][bugun_str][zorluk] = skor

            # Add to leaderboard
            if bugun_str not in st.session_state["mat_maraton_leaderboard"]:
                st.session_state["mat_maraton_leaderboard"][bugun_str] = []
            st.session_state["mat_maraton_leaderboard"][bugun_str].append(
                ("Sen", skor, zorluk)
            )

            st.rerun()

    # Leaderboard
    st.markdown("---")
    st.markdown("**Gunluk Liderlik Tablosu:**")
    if bugun_str in st.session_state["mat_maraton_leaderboard"]:
        entries = st.session_state["mat_maraton_leaderboard"][bugun_str]
        entries_sorted = sorted(entries, key=lambda x: -x[1])
        lb_rows = ""
        for rank, (isim, skor, zrlk) in enumerate(entries_sorted, 1):
            medal = ""
            if rank == 1:
                medal = "&#129351; "
            elif rank == 2:
                medal = "&#129352; "
            elif rank == 3:
                medal = "&#129353; "
            color = "#fbbf24" if rank <= 3 else "#a5b4fc"
            lb_rows += f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:8px 14px;background:rgba(99,102,241,0.06);
                        border-radius:8px;margin:4px 0">
                <span style="color:{color};font-weight:600">{medal}{rank}. {isim}</span>
                <span style="color:#818cf8;font-weight:700">{skor}/5</span>
                <span style="color:#6b7280;font-size:0.8rem">{zrlk}</span>
            </div>
            """
        _render_html(f"""
        <div style="background:rgba(30,27,75,0.5);border-radius:14px;padding:14px;
                    border:1px solid rgba(99,102,241,0.2)">
            {lb_rows}
        </div>
        """)
    else:
        st.info("Bugun henuz kimse maratonu tamamlamadi. Ilk sen ol!")

    # Past results
    past_dates = sorted(
        [d for d in st.session_state["mat_maraton_history"].keys() if d != bugun_str],
        reverse=True,
    )
    if past_dates:
        with st.expander("Gecmis Sonuclar"):
            for d_str in past_dates[:10]:
                results = st.session_state["mat_maraton_history"][d_str]
                parts = ", ".join([f"{z}: {s}/5" for z, s in results.items()])
                st.markdown(f"**{d_str}:** {parts}")
