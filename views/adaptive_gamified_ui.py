"""
SmartCampusAI — Adaptive Learning + Gamification + Speaking Assessment UI
==========================================================================
Yabancı Dil modülü için entegre öğrenme ekranı.
3 ana sekme: 🧠 Adaptif Öğrenme | 🏆 Gamification | 🗣️ Speaking Assessment
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("default")
except Exception:
    pass
from models.cefr_exam import GRADE_TO_CEFR


# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════

def _inject_css():
    st.markdown("""<style>
    .adp-hero{background:linear-gradient(135deg,#0f172a,#1e1b4b,#312e81);
    border-radius:16px;padding:22px 24px;margin-bottom:14px;border:1.5px solid rgba(99,102,241,.25);}
    .adp-hero h2{margin:0;color:#c7d2fe;font-size:1.25rem;}
    .adp-hero .sub{color:#818cf8;font-size:.85rem;margin-top:3px;}
    .adp-card{background:linear-gradient(135deg,#131825,#1a2035);border-radius:14px;
    padding:18px 20px;margin:8px 0;border:1px solid rgba(99,102,241,.12);}
    .adp-stat{text-align:center;padding:12px;}
    .adp-stat .num{font-size:1.6rem;font-weight:800;color:#818cf8;}
    .adp-stat .lbl{font-size:.75rem;color:#64748b;margin-top:2px;}
    .xp-bar{background:rgba(99,102,241,.12);border-radius:8px;height:22px;overflow:hidden;margin:6px 0;}
    .xp-fill{height:100%;border-radius:8px;background:linear-gradient(90deg,#6366F1,#818cf8);
    transition:width .4s;}
    .badge-card{background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:12px;
    padding:14px;text-align:center;border:1px solid rgba(139,92,246,.2);min-height:100px;}
    .badge-card .icon{font-size:2rem;}
    .badge-card .name{font-size:.82rem;font-weight:700;color:#c7d2fe;margin-top:4px;}
    .badge-card .desc{font-size:.7rem;color:#64748b;margin-top:2px;}
    .lb-row{display:flex;align-items:center;gap:12px;padding:8px 14px;border-radius:10px;margin:3px 0;}
    .lb-row:nth-child(1){background:linear-gradient(90deg,rgba(234,179,8,.12),transparent);}
    .lb-row:nth-child(2){background:linear-gradient(90deg,rgba(148,163,184,.1),transparent);}
    .lb-row:nth-child(3){background:linear-gradient(90deg,rgba(180,83,9,.1),transparent);}
    .lb-rank{font-size:1.1rem;font-weight:800;width:32px;color:#f59e0b;}
    .lb-name{flex:1;color:#c7d2fe;font-weight:600;font-size:.88rem;}
    .lb-val{color:#818cf8;font-weight:700;font-size:.9rem;}
    .speak-record{background:linear-gradient(135deg,#7c3aed20,#6366F120);border:2px dashed #7c3aed40;
    border-radius:16px;padding:30px;text-align:center;margin:12px 0;}
    .speak-score{display:inline-block;background:linear-gradient(135deg,#6366F1,#8B5CF6);
    border-radius:50%;width:80px;height:80px;line-height:80px;font-size:1.5rem;
    font-weight:800;color:#fff;text-align:center;}
    .crit-row{display:flex;align-items:center;gap:10px;margin:6px 0;}
    .crit-icon{font-size:1.2rem;width:28px;}
    .crit-name{width:160px;color:#94A3B8;font-size:.82rem;}
    .crit-bar{flex:1;background:rgba(99,102,241,.1);border-radius:6px;height:16px;overflow:hidden;}
    .crit-fill{height:100%;border-radius:6px;transition:width .3s;}
    .crit-val{width:40px;text-align:right;color:#c7d2fe;font-weight:700;font-size:.85rem;}
    </style>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. ADAPTİF ÖĞRENME SEKMESİ
# ═══════════════════════════════════════════════════════════════════════════════

def _render_adaptive_tab(student_id: str, student_name: str, grade: int):
    """Adaptif öğrenme ana ekranı."""
    from models.adaptive_learning import (
        AdaptiveLearningStore, LearningPlanGenerator,
        ELOCalculator, SKILL_AREAS, CEFR_ELO_BANDS,
    )

    store = AdaptiveLearningStore()
    cefr = GRADE_TO_CEFR.get(grade, "A2")

    profile = store.get_or_create_profile(student_id, student_name, grade, cefr)
    profile.check_daily_reset()
    profile.update_weak_strong()
    detected_cefr = profile.get_cefr_from_elo()

    # ── Hero ──
    st.markdown(f"""<div class="adp-hero">
    <h2>🧠 Adaptif Öğrenme — {student_name or 'Öğrenci'}</h2>
    <div class="sub">Kişiselleştirilmiş öğrenme yolculuğun · CEFR {detected_cefr} · ELO {profile.overall_elo:.0f}</div>
    </div>""", unsafe_allow_html=True)

    # ── Üst istatistikler ──
    cols = st.columns(5)
    stats_data = [
        (f"{profile.overall_elo:.0f}", "Genel ELO", "#6366F1"),
        (detected_cefr, "CEFR Seviye", "#10B981"),
        (f"{profile.total_questions_answered}", "Toplam Soru", "#f59e0b"),
        (f"%{round(profile.total_correct / max(profile.total_questions_answered, 1) * 100)}", "Doğruluk", "#EC4899"),
        (f"{profile.daily_completed}/{profile.daily_goal}", "Günlük Hedef", "#06B6D4"),
    ]
    for i, (val, lbl, clr) in enumerate(stats_data):
        with cols[i]:
            st.markdown(f"""<div class="adp-stat">
            <div class="num" style="color:{clr};">{val}</div>
            <div class="lbl">{lbl}</div></div>""", unsafe_allow_html=True)

    sub_tabs = st.tabs(["📊 Beceri Haritası", "🔄 SRS Tekrar", "📅 Öğrenme Planı", "📈 İlerleme"])

    # ── Beceri Haritası ──
    with sub_tabs[0]:
        st.markdown("#### 🎯 Beceri ELO Haritası")
        skill_icons = {"listening": "🎧", "reading": "📖", "writing": "✍️",
                       "speaking": "🗣️", "vocabulary": "📚", "grammar": "📝", "pronunciation": "🔊"}
        skill_colors = {"listening": "#6366F1", "reading": "#10B981", "writing": "#f59e0b",
                        "speaking": "#EC4899", "vocabulary": "#06B6D4", "grammar": "#8B5CF6",
                        "pronunciation": "#3B82F6"}

        for skill in SKILL_AREAS:
            elo = profile.skill_elos.get(skill, 1000)
            max_elo = 2400
            pct = min(100, round(elo / max_elo * 100, 1))
            icon = skill_icons.get(skill, "📊")
            clr = skill_colors.get(skill, "#6366F1")
            is_weak = skill in profile.weak_areas
            is_strong = skill in profile.strong_areas
            tag = " 🔴 Zayıf" if is_weak else (" 🟢 Güçlü" if is_strong else "")

            st.markdown(f"""<div class="crit-row">
            <div class="crit-icon">{icon}</div>
            <div class="crit-name">{skill.title()}{tag}</div>
            <div class="crit-bar"><div class="crit-fill" style="width:{pct}%;background:{clr};"></div></div>
            <div class="crit-val">{elo:.0f}</div>
            </div>""", unsafe_allow_html=True)

        if profile.weak_areas:
            st.info(f"🎯 Odak alanların: **{', '.join(s.title() for s in profile.weak_areas)}** — Bu alanlara daha fazla soru yönlendirilecek.")

    # ── SRS Tekrar ──
    with sub_tabs[1]:
        due_cards = store.get_due_cards(student_id, limit=20)
        st.markdown(f"#### 🔄 Bugün Tekrar Edilecek Kartlar ({len(due_cards)})")

        if not due_cards:
            st.success("🎉 Bugün tekrar edilecek kart yok! Harika iş çıkardın.")
        else:
            for idx, card in enumerate(due_cards):
                with st.expander(f"📝 {card.item_key} ({card.item_type})", expanded=(idx == 0)):
                    data = card.item_data
                    if card.item_type == "vocabulary":
                        st.markdown(f"**Kelime:** {data.get('word', card.item_key)}")
                        st.markdown(f"**Tanım:** {data.get('definition', '-')}")
                        st.markdown(f"**Örnek:** _{data.get('example', '-')}_")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"Tekrar #{card.total_reviews} · Seri: {card.streak}")
                    with col2:
                        st.caption(f"Kolaylık: {card.easiness:.2f} · Aralık: {card.interval} gün")

                    # Kalite seçimi
                    quality = st.select_slider(
                        "Ne kadar hatırladın?",
                        options=[0, 1, 2, 3, 4, 5],
                        value=3,
                        format_func=lambda x: ["Hiç 😰", "Çok Zor 😓", "Zor 😐", "İdare eder 🙂", "İyi 😊", "Mükemmel 🌟"][x],
                        key=f"srs_q_{card.id}",
                    )
                    if st.button("✅ Kaydet", key=f"srs_save_{card.id}"):
                        card.update_sm2(quality)
                        store.save_card(card)
                        st.success(f"Sonraki tekrar: {card.next_review} ({card.interval} gün sonra)")
                        st.rerun()

    # ── Öğrenme Planı ──
    with sub_tabs[2]:
        plan = LearningPlanGenerator.generate_daily_plan(profile)
        st.markdown(f"#### 📅 Günlük Plan — {plan['date']}")
        st.markdown(f"**CEFR:** {plan['cefr_level']} · **Hedef:** {plan['daily_goal']} soru")

        for task in plan["tasks"]:
            st.markdown(f"""<div class="adp-card">
            <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:1.5rem;">{task['icon']}</span>
            <div>
            <div style="color:#c7d2fe;font-weight:700;font-size:.95rem;">{task['title']}</div>
            <div style="color:#64748b;font-size:.8rem;">{task['description']}</div>
            </div>
            <div style="margin-left:auto;color:#818cf8;font-weight:700;">{task.get('estimated_questions', 0)} soru</div>
            </div></div>""", unsafe_allow_html=True)

        st.markdown("---")
        weekly = LearningPlanGenerator.generate_weekly_plan(profile)
        st.markdown("#### 📆 Haftalık Plan")
        _skill_icons_map = {"listening": "🎧", "reading": "📖", "vocabulary": "📚",
                            "grammar": "📝", "writing": "✍️", "speaking": "🗣️", "review": "🔄"}
        w_cols = st.columns(7)
        for i, day in enumerate(weekly["days"]):
            with w_cols[i]:
                weak_tag = "🔴" if day["is_weak_area"] else ""
                _day_icon = _skill_icons_map.get(day["focus_skill"], "📊")
                st.markdown(f"""<div style="text-align:center;background:rgba(99,102,241,.06);
                border-radius:10px;padding:10px 4px;font-size:.78rem;">
                <div style="font-weight:700;color:#c7d2fe;">{day['day'][:3]}</div>
                <div style="color:#818cf8;font-size:1.1rem;margin:4px 0;">{_day_icon}</div>
                <div style="color:#64748b;">{day['focus_skill'].title()}</div>
                <div style="color:#f59e0b;font-size:.7rem;">{weak_tag} {day['question_count']}q</div>
                </div>""", unsafe_allow_html=True)

    # ── İlerleme ──
    with sub_tabs[3]:
        sessions_stats = store.get_student_stats(student_id)
        st.markdown("#### 📈 Öğrenme İlerlemesi")
        p_cols = st.columns(4)
        progress_items = [
            (str(sessions_stats.get("total_sessions", 0)), "Toplam Oturum", "#6366F1"),
            (str(sessions_stats.get("total_questions", 0)), "Çözülen Soru", "#10B981"),
            (f"%{sessions_stats.get('avg_accuracy', 0)}", "Ort. Doğruluk", "#f59e0b"),
            (f"{sessions_stats.get('total_elo_change', 0):+.0f}", "ELO Değişim", "#EC4899"),
        ]
        for i, (val, lbl, clr) in enumerate(progress_items):
            with p_cols[i]:
                st.markdown(f"""<div class="adp-stat">
                <div class="num" style="color:{clr};">{val}</div>
                <div class="lbl">{lbl}</div></div>""", unsafe_allow_html=True)

        all_cards = store.get_student_cards(student_id)
        if all_cards:
            mastered = sum(1 for c in all_cards if c.repetitions >= 5)
            learning = sum(1 for c in all_cards if 1 <= c.repetitions < 5)
            new_cards = sum(1 for c in all_cards if c.repetitions == 0)
            st.markdown("#### 📚 SRS Kart Durumu")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("🟢 Öğrenildi", mastered)
            with c2:
                st.metric("🟡 Öğreniliyor", learning)
            with c3:
                st.metric("🔴 Yeni", new_cards)


# ═══════════════════════════════════════════════════════════════════════════════
# 2. GAMİFİCATİON SEKMESİ
# ═══════════════════════════════════════════════════════════════════════════════

def _render_gamification_tab(student_id: str, student_name: str, grade: int, sube: str):
    """Gamification ekranı."""
    from models.gamification import (
        GamificationStore, GamificationEngine, BadgeChecker,
        BADGE_DEFINITIONS, LEVEL_THRESHOLDS, XP_REWARDS,
    )

    store = GamificationStore()
    profile = store.get_or_create(student_id, student_name, grade, sube)
    profile.check_weekly_reset()
    streak_info = profile.check_streak()
    store.save(profile)

    # ── Hero + Level ──
    xp_pct = min(100, round(profile.total_xp / max(profile.total_xp + profile.xp_to_next_level, 1) * 100))
    st.markdown(f"""<div class="adp-hero">
    <div style="display:flex;align-items:center;gap:16px;">
    <div style="font-size:2.5rem;">{profile.level_icon}</div>
    <div style="flex:1;">
    <h2>Level {profile.level} — {profile.level_name}</h2>
    <div class="sub">{student_name or 'Öğrenci'} · {profile.total_xp} XP</div>
    <div class="xp-bar"><div class="xp-fill" style="width:{xp_pct}%;"></div></div>
    <div style="color:#64748b;font-size:.72rem;">{profile.xp_to_next_level} XP sonraki seviyeye</div>
    </div>
    <div style="text-align:center;">
    <div style="font-size:2rem;">🔥</div>
    <div style="color:#f59e0b;font-weight:800;font-size:1.2rem;">{profile.streak_days}</div>
    <div style="color:#64748b;font-size:.7rem;">gün seri</div>
    </div>
    </div></div>""", unsafe_allow_html=True)

    sub_tabs = st.tabs(["🏅 Rozetler", "🏆 Liderlik Tablosu", "📊 İstatistikler"])

    # ── Rozetler ──
    with sub_tabs[0]:
        earned_ids = {b["badge_id"] for b in profile.badges_earned}
        st.markdown(f"#### 🏅 Rozetler ({len(earned_ids)}/{len(BADGE_DEFINITIONS)})")

        categories = {}
        for bid, bdef in BADGE_DEFINITIONS.items():
            cat = bdef.get("category", "other")
            categories.setdefault(cat, []).append((bid, bdef))

        cat_names = {"streak": "🔥 Seri", "questions": "❓ Sorular", "accuracy": "🎯 Doğruluk",
                     "cefr": "📈 CEFR Seviye", "skill": "💪 Beceriler", "special": "⭐ Özel"}

        for cat, badges in categories.items():
            st.markdown(f"**{cat_names.get(cat, cat.title())}**")
            b_cols = st.columns(min(5, len(badges)))
            for i, (bid, bdef) in enumerate(badges):
                earned = bid in earned_ids
                with b_cols[i % len(b_cols)]:
                    opacity = "1" if earned else "0.3"
                    check = "✅" if earned else "🔒"
                    st.markdown(f"""<div class="badge-card" style="opacity:{opacity};">
                    <div class="icon">{bdef['icon']}</div>
                    <div class="name">{check} {bdef['name']}</div>
                    <div class="desc">{bdef['desc']}</div>
                    <div style="color:#818cf8;font-size:.7rem;margin-top:4px;">+{bdef.get('xp',0)} XP</div>
                    </div>""", unsafe_allow_html=True)

    # ── Liderlik Tablosu ──
    with sub_tabs[1]:
        sort_opts = {"Haftalık XP": "weekly_xp", "Toplam XP": "total_xp",
                     "Seri": "streak", "Doğruluk": "accuracy", "Seviye": "level"}
        sort_sel = st.selectbox("Sıralama", list(sort_opts.keys()), key="gam_lb_sort")
        sort_by = sort_opts[sort_sel]

        lb = store.get_leaderboard(grade, sube, sort_by)
        if not lb:
            st.info("Henüz liderlik tablosunda kimse yok.")
        else:
            medals = {1: "🥇", 2: "🥈", 3: "🥉"}
            for entry in lb[:20]:
                medal = medals.get(entry["rank"], f"#{entry['rank']}")
                is_me = entry["student_id"] == student_id
                bg = "rgba(99,102,241,.08)" if is_me else "transparent"
                me_tag = " ← Sen" if is_me else ""
                val = entry.get(sort_by, 0)
                if sort_by == "accuracy":
                    val = f"%{val}"
                st.markdown(f"""<div class="lb-row" style="background:{bg};">
                <div class="lb-rank">{medal}</div>
                <div style="font-size:1rem;">{entry['level_icon']}</div>
                <div class="lb-name">{entry['student_name'] or 'Öğrenci'}{me_tag}</div>
                <div style="color:#64748b;font-size:.75rem;">Lv.{entry['level']}</div>
                <div class="lb-val">{val}</div>
                </div>""", unsafe_allow_html=True)

    # ── İstatistikler ──
    with sub_tabs[2]:
        st.markdown("#### 📊 Oyun İstatistiklerin")
        s_cols = st.columns(4)
        game_stats = [
            (str(profile.total_xp), "Toplam XP", "#6366F1"),
            (str(profile.weekly_xp), "Haftalık XP", "#10B981"),
            (str(profile.best_streak), "En İyi Seri", "#f59e0b"),
            (f"%{profile.accuracy}", "Doğruluk", "#EC4899"),
        ]
        for i, (val, lbl, clr) in enumerate(game_stats):
            with s_cols[i]:
                st.markdown(f"""<div class="adp-stat">
                <div class="num" style="color:{clr};">{val}</div>
                <div class="lbl">{lbl}</div></div>""", unsafe_allow_html=True)

        # XP kazanım tablosu
        st.markdown("#### 💰 XP Kazanım Rehberi")
        for action, xp in XP_REWARDS.items():
            label = action.replace("_", " ").title()
            st.markdown(f"- **{label}:** +{xp} XP")

        # Level yol haritası
        st.markdown("#### 🗺️ Seviye Yol Haritası")
        for lvl, threshold, name, icon in LEVEL_THRESHOLDS:
            reached = profile.level >= lvl
            check = "✅" if reached else "⬜"
            st.markdown(f"{check} {icon} **Level {lvl} — {name}** ({threshold} XP)")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. SPEAKING ASSESSMENT SEKMESİ
# ═══════════════════════════════════════════════════════════════════════════════

def _render_speaking_tab(student_id: str, student_name: str, grade: int):
    """Speaking Assessment ekranı."""
    from models.speaking_assessment import (
        SpeakingStore, SpeechAnalyzer, SpeakingTaskGenerator,
        SpeakingAttempt, SPEAKING_CRITERIA, FLUENCY_WPM_BENCHMARKS,
    )

    store = SpeakingStore()
    cefr = GRADE_TO_CEFR.get(grade, "A2")

    sub_tabs = st.tabs(["🎤 Konuşma Görevi", "📊 Sonuçlarım", "📈 İlerlemem"])

    # ── Konuşma Görevi ──
    with sub_tabs[0]:
        st.markdown(f"""<div class="adp-hero">
        <h2>🗣️ Speaking Assessment — {cefr}</h2>
        <div class="sub">CEFR konuşma değerlendirmesi · Pronunciation · Fluency · Accuracy</div>
        </div>""", unsafe_allow_html=True)

        # Görev seçimi
        tasks = SpeakingTaskGenerator.get_tasks_for_level(cefr)
        if not tasks:
            tasks = [{"type": "describe", "title": "Describe", "desc": "Talk about a topic", "duration": 60}]

        task_labels = [f"{t['title']} ({t['duration']}s)" for t in tasks]
        sel_idx = st.selectbox("Görev Seç", range(len(tasks)),
                                format_func=lambda i: task_labels[i],
                                key="speak_task_sel")
        sel_task = tasks[sel_idx]

        st.markdown(f"""<div class="adp-card">
        <div style="color:#c7d2fe;font-weight:700;font-size:1rem;">📋 {sel_task['title']}</div>
        <div style="color:#94A3B8;margin-top:4px;">{sel_task['desc']}</div>
        <div style="color:#818cf8;font-size:.82rem;margin-top:8px;">⏱️ Hedef süre: {sel_task['duration']} saniye</div>
        </div>""", unsafe_allow_html=True)

        # Opsiyonel konu
        topic = st.text_input("Konu (opsiyonel)", key="speak_topic",
                               placeholder="örn: My favourite hobby, School life...")

        # Web Speech API — Kayıt
        st.markdown("""<div class="speak-record">
        <div style="font-size:2.5rem;margin-bottom:8px;">🎤</div>
        <div style="color:#c7d2fe;font-weight:700;">Konuşmanı Kaydet</div>
        <div style="color:#64748b;font-size:.82rem;margin-top:4px;">
        Aşağıdaki butona bas → Konuş → Transkript otomatik oluşur</div>
        </div>""", unsafe_allow_html=True)

        # Speech Recognition HTML component
        rec_html = """
        <div id="speech-box" style="padding:10px;">
        <button id="recBtn" onclick="toggleRec()" style="background:linear-gradient(135deg,#6366F1,#8B5CF6);
        color:#fff;border:none;padding:10px 28px;border-radius:10px;font-size:14px;font-weight:700;cursor:pointer;">
        🎙️ Kayda Başla</button>
        <span id="status" style="color:#94A3B8;margin-left:12px;font-size:13px;"></span>
        <div id="timer" style="color:#f59e0b;font-size:20px;font-weight:700;margin-top:8px;">00:00</div>
        <div id="result" style="background:rgba(99,102,241,.06);border-radius:10px;padding:12px;
        margin-top:10px;color:#c7d2fe;font-size:14px;min-height:40px;display:none;"></div>
        </div>
        <script>
        let rec=null, isRec=false, start=0, timerInt=null;
        function toggleRec(){
          if(!isRec){
            if(!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)){
              document.getElementById('status').textContent='❌ Tarayıcı desteklemiyor';return;}
            const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
            rec=new SR();rec.lang='en-US';rec.continuous=true;rec.interimResults=true;
            let final='';
            rec.onresult=function(e){
              let interim='';
              for(let i=e.resultIndex;i<e.results.length;i++){
                if(e.results[i].isFinal) final+=e.results[i][0].transcript+' ';
                else interim+=e.results[i][0].transcript;}
              document.getElementById('result').style.display='block';
              document.getElementById('result').textContent=final+interim;
              // Push to Streamlit
              window.parent.postMessage({type:'streamlit:setComponentValue',
                value:JSON.stringify({transcript:final,duration:Math.round((Date.now()-start)/1000)})}, '*');
            };
            rec.start();isRec=true;start=Date.now();
            document.getElementById('recBtn').textContent='⏹️ Durdur';
            document.getElementById('recBtn').style.background='#EF4444';
            document.getElementById('status').textContent='Kayıt yapılıyor...';
            timerInt=setInterval(()=>{
              let s=Math.round((Date.now()-start)/1000);
              let m=Math.floor(s/60);s=s%60;
              document.getElementById('timer').textContent=
                String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');
            },1000);
          } else {
            rec.stop();isRec=false;
            document.getElementById('recBtn').textContent='🎙️ Kayda Başla';
            document.getElementById('recBtn').style.background='linear-gradient(135deg,#6366F1,#8B5CF6)';
            document.getElementById('status').textContent='✅ Kayıt tamamlandı';
            clearInterval(timerInt);
          }
        }
        </script>"""
        components.html(rec_html, height=220)

        # Manuel transkript girişi (fallback)
        st.markdown("**Veya transkripti elle gir:**")
        transcript = st.text_area("Transkript", key="speak_transcript", height=100,
                                   placeholder="I think that... My favourite thing is...")
        duration = st.number_input("Konuşma süresi (saniye)", 1, 600, sel_task["duration"],
                                    key="speak_duration")

        if st.button("📤 Değerlendir", key="speak_submit", type="primary",
                       use_container_width=True):
            if not transcript or len(transcript.strip()) < 3:
                st.warning("Lütfen konuşma transkripti gir veya mikrofon ile kaydet.")
            else:
                with st.spinner("Analiz ediliyor..."):
                    # Analiz
                    analysis = SpeechAnalyzer.analyze_transcript(transcript, duration, cefr)
                    scores = SpeechAnalyzer.auto_score(analysis, cefr)
                    fb = SpeechAnalyzer.generate_feedback(scores, analysis, cefr)

                    # Attempt oluştur
                    attempt = SpeakingAttempt(
                        student_id=student_id,
                        student_name=student_name,
                        cefr_level=cefr,
                        transcript=transcript,
                        duration_seconds=duration,
                        word_count=analysis["word_count"],
                        wpm=analysis["wpm"],
                        filler_count=analysis["filler_count"],
                        filler_ratio=analysis["filler_ratio"],
                        scores=scores,
                        feedback=fb["feedback"],
                        strengths=fb["strengths"],
                        improvements=fb["improvements"],
                    )
                    attempt.calculate_overall()
                    store.save_attempt(attempt)
                    st.session_state["last_speaking_result"] = attempt

                st.rerun()

        # Son sonuç göster
        last = st.session_state.get("last_speaking_result")
        if last:
            _render_speaking_result(last, cefr)

    # ── Sonuçlarım ──
    with sub_tabs[1]:
        attempts = store.get_student_attempts(student_id, limit=20)
        if not attempts:
            st.info("Henüz konuşma denemesi yapmadın.")
        else:
            for att in attempts:
                cefr_info_color = {"Pre-A1": "#EC4899", "A1": "#8B5CF6", "A2": "#06B6D4",
                                    "B1": "#10B981", "B2": "#3B82F6", "C1": "#F59E0B"}.get(att.achieved_cefr, "#6366F1")
                st.markdown(f"""<div class="adp-card" style="border-color:{cefr_info_color}30;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                <span style="background:{cefr_info_color};color:#fff;padding:3px 10px;border-radius:12px;
                font-weight:700;font-size:.82rem;">{att.achieved_cefr}</span>
                <span style="color:#94A3B8;margin-left:8px;font-size:.82rem;">{att.submitted_at[:10]}</span>
                </div>
                <div style="text-align:right;">
                <div style="color:#c7d2fe;font-weight:700;">{att.overall_score:.1f}/5.0</div>
                <div style="color:#64748b;font-size:.75rem;">{att.wpm} WPM · {att.word_count} kelime</div>
                </div></div></div>""", unsafe_allow_html=True)

    # ── İlerleme ──
    with sub_tabs[2]:
        stats = store.get_student_speaking_stats(student_id)
        st.markdown("#### 📈 Konuşma İlerlemesi")
        if stats["total_attempts"] == 0:
            st.info("Henüz veri yok. İlk konuşma denemeni yap!")
        else:
            sp_cols = st.columns(4)
            sp_items = [
                (str(stats["total_attempts"]), "Toplam Deneme", "#6366F1"),
                (f"{stats['avg_score']:.1f}", "Ort. Puan", "#10B981"),
                (f"{stats['avg_wpm']:.0f}", "Ort. WPM", "#f59e0b"),
                (f"{stats['total_words_spoken']}", "Toplam Kelime", "#EC4899"),
            ]
            for i, (val, lbl, clr) in enumerate(sp_items):
                with sp_cols[i]:
                    st.markdown(f"""<div class="adp-stat">
                    <div class="num" style="color:{clr};">{val}</div>
                    <div class="lbl">{lbl}</div></div>""", unsafe_allow_html=True)


def _render_speaking_result(attempt: SpeakingAttempt, target_cefr: str):
    """Konuşma değerlendirme sonucu."""
    from models.speaking_assessment import SPEAKING_CRITERIA

    cefr_colors = {"Pre-A1": "#EC4899", "A1": "#8B5CF6", "A2": "#06B6D4",
                    "B1": "#10B981", "B2": "#3B82F6", "C1": "#F59E0B"}
    color = cefr_colors.get(attempt.achieved_cefr, "#6366F1")

    st.markdown("---")
    st.markdown(f"""<div class="adp-card" style="border-color:{color}40;">
    <div style="display:flex;align-items:center;gap:20px;">
    <div class="speak-score">{attempt.overall_score:.1f}</div>
    <div>
    <div style="font-size:1rem;font-weight:700;color:#c7d2fe;">Speaking Sonucu</div>
    <div style="background:{color};color:#fff;display:inline-block;padding:3px 12px;
    border-radius:12px;font-weight:700;margin-top:4px;">{attempt.achieved_cefr}</div>
    <div style="color:#64748b;font-size:.82rem;margin-top:4px;">
    {attempt.wpm} WPM · {attempt.word_count} kelime · {attempt.duration_seconds}s
    </div></div></div></div>""", unsafe_allow_html=True)

    # Kriter detay
    st.markdown("#### 📊 Kriter Puanları")
    crit_colors = {"range": "#6366F1", "accuracy": "#10B981", "fluency": "#f59e0b",
                    "interaction": "#EC4899", "coherence": "#06B6D4"}
    for crit, info in SPEAKING_CRITERIA.items():
        score = attempt.scores.get(crit, 0)
        pct = round(score / 5 * 100)
        clr = crit_colors.get(crit, "#6366F1")
        st.markdown(f"""<div class="crit-row">
        <div class="crit-icon">{info['icon']}</div>
        <div class="crit-name">{info['name']}</div>
        <div class="crit-bar"><div class="crit-fill" style="width:{pct}%;background:{clr};"></div></div>
        <div class="crit-val">{score}/5</div>
        </div>""", unsafe_allow_html=True)

    # Feedback
    if attempt.feedback:
        st.markdown(f"#### 💬 Geri Bildirim")
        st.info(attempt.feedback)

    if attempt.strengths:
        st.markdown("**💪 Güçlü Yanlar:**")
        for s in attempt.strengths:
            st.markdown(f"- {s}")

    if attempt.improvements:
        st.markdown("**🎯 Geliştirilecek Alanlar:**")
        for imp in attempt.improvements:
            st.markdown(f"- {imp}")

    # Filler uyarı
    if attempt.filler_count > 3:
        st.warning(f"⚠️ {attempt.filler_count} filler kelime tespit edildi. 'Um', 'uh', 'like' yerine kısa duraklama yapmayı dene!")


# ═══════════════════════════════════════════════════════════════════════════════
# ANA RENDER
# ═══════════════════════════════════════════════════════════════════════════════

def render_adaptive_gamified():
    """Ana ekran — 3 sekme: Adaptif + Gamification + Speaking."""
    inject_common_css()
    _inject_css()
    styled_header("🚀 Akıllı Öğrenme Merkezi",
                  "Adaptif Öğrenme · Gamification · Speaking Assessment")

    # Öğrenci bilgileri
    student_id = st.session_state.get("student_id", "demo_student")
    student_name = st.session_state.get("student_name", "Öğrenci")
    grade = st.session_state.get("sinif", 5)
    sube = st.session_state.get("sube", "A")

    # Geri dön butonu
    if st.button("← Yabancı Dil Paneline Dön", key="adp_back"):
        st.session_state["yd_view"] = "dashboard"
        st.rerun()

    main_tabs = st.tabs(["🧠 Adaptif Öğrenme", "🏆 Gamification", "🗣️ Speaking Assessment"])

    with main_tabs[0]:
        _render_adaptive_tab(student_id, student_name, grade)

    with main_tabs[1]:
        _render_gamification_tab(student_id, student_name, grade, sube)

    with main_tabs[2]:
        _render_speaking_tab(student_id, student_name, grade)
