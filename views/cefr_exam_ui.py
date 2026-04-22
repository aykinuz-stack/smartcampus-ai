"""
SmartCampusAI — CEFR Mock Exam UI
====================================
Cambridge formatında sınav oluşturma + çözme + seviye raporu + sertifika.
Öğretmen: Sınav oluştur → yayınla
Öğrenci: Sınavı çöz → anında CEFR seviye raporu
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from models.cefr_exam import (
    CEFR_LEVELS, GRADE_TO_CEFR, EXAM_STRUCTURES,
    CEFRQuestion, CEFRExam, CEFRResult,
    CEFRQuestionGenerator, CEFRAutoGrader, CEFRExamStore,
)
from utils.ui_common import inject_common_css, styled_header
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("yabanci_dil")
except Exception:
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════

def _css():
    st.markdown("""<style>
    .cefr-hero{background:linear-gradient(135deg,#0f172a,#1e1b4b,#312e81);
    border-radius:16px;padding:24px;margin-bottom:16px;border:1.5px solid rgba(99,102,241,.25);}
    .cefr-hero h2{margin:0;color:#c7d2fe;font-size:1.3rem;}
    .cefr-hero .sub{color:#818cf8;font-size:.88rem;margin-top:4px;}
    .cefr-section{background:linear-gradient(135deg,#131825,#1a2035);border-radius:14px;
    padding:18px 22px;margin:12px 0;border:1px solid rgba(99,102,241,.15);}
    .cefr-section-title{font-size:1.05rem;font-weight:700;margin:0 0 4px 0;}
    .cefr-q{background:rgba(99,102,241,.04);border:1px solid rgba(99,102,241,.1);
    border-radius:10px;padding:14px 18px;margin:8px 0;}
    .cefr-q-num{color:#818cf8;font-weight:700;font-size:.85rem;}
    .cefr-passage{background:rgba(139,92,246,.06);border-left:4px solid #8B5CF6;
    border-radius:0 10px 10px 0;padding:14px 18px;margin:10px 0;color:#cbd5e1;
    font-size:.9rem;line-height:1.6;}
    .cefr-badge{display:inline-block;border-radius:20px;padding:6px 16px;
    font-weight:700;font-size:1.1rem;color:#fff;}
    .cefr-level-card{background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
    padding:20px;text-align:center;border:2px solid;}
    .cefr-cert{background:linear-gradient(135deg,#faf5ff,#ede9fe,#ddd6fe);
    border:3px solid #8B5CF6;border-radius:16px;padding:30px;text-align:center;color:#1e293b;}
    .cefr-cert h2{color:#6d28d9;margin:8px 0;font-size:1.5rem;}
    .cefr-cert .level{font-size:2rem;font-weight:800;color:#7c3aed;}
    .cefr-cert .detail{color:#64748b;font-size:.85rem;margin-top:8px;}
    .cefr-skill-bar{background:rgba(99,102,241,.1);border-radius:6px;height:20px;overflow:hidden;margin:4px 0;}
    .cefr-skill-fill{height:100%;border-radius:6px;transition:width .3s;}
    </style>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ÖĞRETMEN — SINAV OLUŞTUR + YÖNETİM
# ═══════════════════════════════════════════════════════════════════════════════

def render_cefr_teacher():
    """Öğretmen: CEFR mock exam oluştur + yayınla + sonuç gör."""
    _css()

    store = CEFRExamStore()

    grade_opts = {"Okul Öncesi": 0, **{f"{i}. Sınıf": i for i in range(1, 13)}}
    tabs = st.tabs(["📝 Sınav Oluştur", "📋 Mevcut Sınavlar", "📊 Sonuçlar"])

    # ── TAB 1: Sınav Oluştur ──
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            sel_label = st.selectbox("Sınıf", list(grade_opts.keys()), index=5, key="cefr_grade")
            grade = grade_opts[sel_label]
        with c2:
            cefr = GRADE_TO_CEFR.get(grade, "A2")
            cefr_info = CEFR_LEVELS.get(cefr, {})
            st.markdown(f"""
            <div style="background:rgba(99,102,241,.08);border-radius:10px;padding:12px 16px;margin-top:24px;">
            <span class="cefr-badge" style="background:{cefr_info.get('color','#6366F1')};">{cefr}</span>
            <span style="color:#94A3B8;margin-left:8px;">{cefr_info.get('cambridge','')}</span>
            </div>""", unsafe_allow_html=True)

        # Ünite aralığı
        c3, c4 = st.columns(2)
        with c3:
            unit_start = st.number_input("Başlangıç Ünite", 1, 10, 1, key="cefr_u_start")
        with c4:
            unit_end = st.number_input("Bitiş Ünite", 1, 10, 10, key="cefr_u_end")

        exam_name = st.text_input("Sınav Adı (opsiyonel)", key="cefr_exam_name",
                                   placeholder=f"{cefr_info.get('cambridge','')} Mock Exam")

        # Sınav yapısı bilgisi
        struct = EXAM_STRUCTURES.get(cefr, {})
        st.markdown(f"""
        <div class="cefr-section">
        <div class="cefr-section-title" style="color:#818cf8;">📋 Sınav Yapısı — {cefr_info.get('cambridge','')}</div>
        <div style="color:#94A3B8;font-size:.82rem;display:flex;gap:20px;margin-top:8px;">
        <span>🎧 Listening: {struct.get('listening',{}).get('questions',0)} soru</span>
        <span>📖 Reading: {struct.get('reading',struct.get('reading_writing',{})).get('questions',0)} soru</span>
        <span>✍️ Writing: {struct.get('writing',{}).get('parts',2)} bölüm</span>
        <span>🗣️ Speaking: {struct.get('speaking',{}).get('parts',4)} bölüm</span>
        <span>⏱️ {struct.get('total_duration',60)} dk</span>
        </div></div>""", unsafe_allow_html=True)

        if st.button("🎯 CEFR Mock Exam Oluştur", key="cefr_gen", type="primary",
                       use_container_width=True):
            with st.spinner(f"{cefr} Mock Exam oluşturuluyor..."):
                gen = CEFRQuestionGenerator(grade)
                unit_range = list(range(int(unit_start), int(unit_end) + 1))
                exam = gen.generate_exam(unit_range, exam_name or "")
                exam.status = "published"
                store.save_exam(exam)
                st.session_state["cefr_last_exam_id"] = exam.id
                st.success(f"✅ {exam.name} — {len(exam.questions)} soru oluşturuldu!")

    # ── TAB 2: Mevcut Sınavlar ──
    with tabs[1]:
        exams = store.list_exams()
        if not exams:
            st.info("Henüz sınav oluşturulmamış.")
        else:
            for exam in reversed(exams):
                cefr_info = CEFR_LEVELS.get(exam.cefr, {})
                secs = {k: len(v) for k, v in exam.sections.items()}
                with st.expander(f"📝 {exam.name} — {exam.cefr} ({len(exam.questions)} soru)", expanded=False):
                    st.markdown(f"""
                    **ID:** `{exam.id}` · **Tarih:** {exam.created_at[:10]}
                    · **Süre:** {exam.duration_min} dk · **Ünite:** {exam.unit_range}

                    | Bölüm | Soru |
                    |-------|------|
                    | 🎧 Listening | {secs.get('listening',0)} |
                    | 📖 Reading | {secs.get('reading',0)} |
                    | ✍️ Writing | {secs.get('writing',0)} |
                    | 🗣️ Speaking | {secs.get('speaking',0)} |
                    """)

    # ── TAB 3: Sonuçlar ──
    with tabs[2]:
        exams = store.list_exams()
        if exams:
            sel_exam = st.selectbox("Sınav Seçin",
                                     [f"{e.name} ({e.id})" for e in exams], key="cefr_res_sel")
            exam_id = sel_exam.split("(")[-1].rstrip(")")
            results = store.get_exam_results(exam_id)
            if results:
                for r in results:
                    _render_result_summary(r)
            else:
                st.info("Bu sınavı henüz kimse çözmemiş.")


# ═══════════════════════════════════════════════════════════════════════════════
# ÖĞRENCİ — SINAV ÇÖZ + SONUÇ GÖR
# ═══════════════════════════════════════════════════════════════════════════════

def render_cefr_student(student_id: str = "", student_name: str = "",
                         sinif: int = 5, sube: str = "A"):
    """Öğrenci: CEFR sınavı çöz + seviye raporu gör."""
    _css()

    store = CEFRExamStore()
    grade = sinif
    cefr = GRADE_TO_CEFR.get(grade, "A2")

    tabs = st.tabs(["📝 Sınav Çöz", "📊 Sonuçlarım", "🏆 Sertifikam"])

    # ── TAB 1: Sınav Çöz ──
    with tabs[0]:
        exams = [e for e in store.list_exams(grade) if e.status == "published"]
        if not exams:
            # Tüm sınavları da göster
            exams = [e for e in store.list_exams() if e.status == "published"]

        if not exams:
            st.info("Henüz yayınlanmış sınav yok. Öğretmeninizden sınav oluşturmasını isteyin.")
            return

        sel_exam_name = st.selectbox("Sınav Seçin",
                                      [f"{e.name}" for e in exams], key="cefr_stu_sel")
        exam = exams[[e.name for e in exams].index(sel_exam_name)]

        cefr_info = CEFR_LEVELS.get(exam.cefr, {})
        st.markdown(f"""<div class="cefr-hero">
        <h2>📝 {exam.name}</h2>
        <div class="sub">{exam.cefr} — {cefr_info.get('cambridge','')} · {exam.duration_min} dk · {len(exam.questions)} soru</div>
        </div>""", unsafe_allow_html=True)

        # Sınav bölümleri
        section_tabs = st.tabs(["🎧 Listening", "📖 Reading", "✍️ Writing", "🗣️ Speaking"])

        answers = {}

        # ── Listening ──
        with section_tabs[0]:
            listen_qs = [q for q in exam.questions if q.section == "listening"]
            _render_exam_section(listen_qs, "listening", answers, exam.id)

        # ── Reading ──
        with section_tabs[1]:
            read_qs = [q for q in exam.questions if q.section == "reading"]
            _render_exam_section(read_qs, "reading", answers, exam.id)

        # ── Writing ──
        with section_tabs[2]:
            write_qs = [q for q in exam.questions if q.section == "writing"]
            _render_exam_section(write_qs, "writing", answers, exam.id)

        # ── Speaking ──
        with section_tabs[3]:
            speak_qs = [q for q in exam.questions if q.section == "speaking"]
            _render_exam_section(speak_qs, "speaking", answers, exam.id)

        # Gönder butonu
        st.markdown("---")
        if st.button("📤 Sınavı Gönder ve Sonucu Gör", key="cefr_submit",
                       type="primary", use_container_width=True):
            # Session state'den cevapları topla
            for q in exam.questions:
                key = f"cefr_ans_{exam.id}_{q.id}"
                ans = st.session_state.get(key, "")
                if ans:
                    answers[q.id] = ans

            result = CEFRAutoGrader.grade_exam(exam, answers)
            result.student_id = student_id
            result.student_name = student_name
            result.sinif = sinif
            result.sube = sube
            store.save_result(result)
            st.session_state["cefr_last_result"] = result
            st.rerun()

        # Son sonucu göster
        last_result = st.session_state.get("cefr_last_result")
        if last_result:
            st.markdown("---")
            _render_result_report(last_result)

    # ── TAB 2: Sonuçlarım ──
    with tabs[1]:
        results = store.get_student_results(student_id, grade)
        if results:
            for r in reversed(results):
                _render_result_summary(r)
        else:
            st.info("Henüz sınav sonucunuz yok.")

    # ── TAB 3: Sertifika ──
    with tabs[2]:
        results = store.get_student_results(student_id, grade)
        if results:
            best = max(results, key=lambda r: r.percentage)
            _render_certificate(best, student_name)
        else:
            st.info("Sınav çözdüğünüzde sertifikanız burada görünecek.")


# ═══════════════════════════════════════════════════════════════════════════════
# SINAV BÖLÜM RENDER
# ═══════════════════════════════════════════════════════════════════════════════

def _render_exam_section(questions: list[CEFRQuestion], section: str,
                          answers: dict, exam_id: str):
    """Sınav bölümü — sorular interaktif."""
    if not questions:
        st.info(f"Bu bölümde soru yok.")
        return

    # Grupla by part
    parts: dict[int, list[CEFRQuestion]] = {}
    for q in questions:
        parts.setdefault(q.part, []).append(q)

    for part_num, part_qs in sorted(parts.items()):
        st.markdown(f"#### Part {part_num}")
        if part_qs and part_qs[0].instruction:
            st.markdown(f"*{part_qs[0].instruction}*")

        for q in part_qs:
            key = f"cefr_ans_{exam_id}_{q.id}"

            # Context (passage) göster
            if q.context and q == part_qs[0]:
                st.markdown(f'<div class="cefr-passage">{q.context}</div>', unsafe_allow_html=True)

            st.markdown(f'<span class="cefr-q-num">Q{q.q_num}</span>', unsafe_allow_html=True)

            if q.q_type == "mcq":
                st.markdown(f"**{q.stem}**")
                if q.choices:
                    opts = [f"{k}) {v}" for k, v in q.choices.items()]
                    sel = st.radio("", opts, key=key, label_visibility="collapsed")
                    if sel:
                        answers[q.id] = sel[0]  # Just the letter

            elif q.q_type == "fill_blank":
                st.markdown(f"**{q.stem}**")
                ans = st.text_input("", key=key, label_visibility="collapsed",
                                     placeholder="Write your answer...")
                if ans:
                    answers[q.id] = ans

            elif q.q_type == "true_false":
                st.markdown(f"**{q.stem}**")
                sel = st.radio("", ["True", "False"], key=key, label_visibility="collapsed",
                                horizontal=True)
                if sel:
                    answers[q.id] = sel

            elif q.q_type == "writing":
                st.markdown(f"**{q.stem}**")
                ans = st.text_area("", key=key, height=150, label_visibility="collapsed",
                                    placeholder="Write your answer here...")
                if ans:
                    answers[q.id] = ans

            elif q.q_type == "speaking":
                st.markdown(f"**{q.stem}**")
                # TTS ile soruyu sesli oku
                clean = q.stem.replace("'", "\\'")
                tts_h = f"""<button onclick="(function(){{const u=new SpeechSynthesisUtterance('{clean}');
                u.lang='en-US';u.rate=.8;speechSynthesis.speak(u)}})()"
                style="background:#f59e0b;color:#000;border:none;padding:5px 14px;border-radius:6px;
                cursor:pointer;font-size:12px;font-weight:600;">🔊 Listen</button>"""
                components.html(tts_h, height=40)
                ans = st.text_area("Your spoken answer (type it):", key=key, height=80,
                                    label_visibility="collapsed",
                                    placeholder="Type what you would say...")
                if ans:
                    answers[q.id] = ans


# ═══════════════════════════════════════════════════════════════════════════════
# SONUÇ RAPORU
# ═══════════════════════════════════════════════════════════════════════════════

def _render_result_summary(r: CEFRResult):
    """Kısa sonuç kartı."""
    cefr_info = CEFR_LEVELS.get(r.achieved_cefr, {})
    color = cefr_info.get("color", "#6366F1")
    st.markdown(f"""
    <div class="cefr-section" style="border-color:{color}40;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
        <span class="cefr-badge" style="background:{color};">{r.achieved_cefr}</span>
        <span style="color:#94A3B8;margin-left:8px;">{r.student_name or 'Öğrenci'} · {r.submitted_at[:10]}</span>
    </div>
    <div style="text-align:right;">
        <div style="color:#c7d2fe;font-size:1.2rem;font-weight:700;">%{r.percentage}</div>
        <div style="color:#64748b;font-size:.75rem;">{r.total_score}/{r.total_max}</div>
    </div>
    </div>
    <div style="display:flex;gap:16px;margin-top:10px;font-size:.8rem;color:#94A3B8;">
    <span>🎧 L: {r.listening_score}/{r.listening_max}</span>
    <span>📖 R: {r.reading_score}/{r.reading_max}</span>
    <span>✍️ W: {r.writing_score}/{r.writing_max}</span>
    <span>🗣️ S: {r.speaking_score}/{r.speaking_max}</span>
    </div></div>""", unsafe_allow_html=True)


def _render_result_report(r: CEFRResult):
    """Detaylı CEFR seviye raporu."""
    cefr_info = CEFR_LEVELS.get(r.achieved_cefr, {})
    color = cefr_info.get("color", "#6366F1")
    target_info = CEFR_LEVELS.get(r.cefr, {})

    st.markdown(f"""<div class="cefr-hero" style="border-color:{color};">
    <h2>📊 CEFR Seviye Raporu</h2>
    <div class="sub">{r.student_name} · Sınıf {r.sinif}/{r.sube} · {r.submitted_at[:10]}</div>
    </div>""", unsafe_allow_html=True)

    # Seviye kartı
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="cefr-level-card" style="border-color:{color};">
        <div style="color:#94A3B8;font-size:.8rem;">Tespit Edilen Seviye</div>
        <div class="cefr-badge" style="background:{color};font-size:1.5rem;margin:10px 0;">{r.achieved_cefr}</div>
        <div style="color:#94A3B8;font-size:.8rem;">{cefr_info.get('label','')}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.metric("Toplam Puan", f"{r.total_score}/{r.total_max}")
        st.metric("Yüzde", f"%{r.percentage}")
    with c3:
        st.markdown(f"""<div class="cefr-level-card" style="border-color:#64748b;">
        <div style="color:#94A3B8;font-size:.8rem;">Hedef Seviye</div>
        <div style="color:#818cf8;font-size:1.3rem;font-weight:700;margin:10px 0;">{r.next_cefr}</div>
        <div style="color:#94A3B8;font-size:.8rem;">%{r.distance_to_next} uzaklık</div>
        </div>""", unsafe_allow_html=True)

    # Bölüm puanları
    st.markdown("#### 📊 Bölüm Puanları")
    sections = [
        ("🎧 Listening", r.listening_score, r.listening_max, "#6366F1"),
        ("📖 Reading", r.reading_score, r.reading_max, "#10B981"),
        ("✍️ Writing", r.writing_score, r.writing_max, "#f59e0b"),
        ("🗣️ Speaking", r.speaking_score, r.speaking_max, "#EC4899"),
    ]
    cols = st.columns(4)
    for i, (label, score, max_s, clr) in enumerate(sections):
        with cols[i]:
            pct = round(score / max_s * 100, 1) if max_s > 0 else 0
            st.markdown(f"""
            <div style="text-align:center;">
            <div style="color:{clr};font-weight:700;font-size:.85rem;">{label}</div>
            <div style="font-size:1.1rem;color:#c7d2fe;font-weight:700;">{score}/{max_s}</div>
            <div class="cefr-skill-bar"><div class="cefr-skill-fill" style="width:{pct}%;background:{clr};"></div></div>
            <div style="color:#64748b;font-size:.75rem;">%{pct}</div>
            </div>""", unsafe_allow_html=True)

    # Beceri analizi
    if r.skill_breakdown:
        st.markdown("#### 🎯 Beceri Analizi")
        skill_colors = {"vocabulary": "#818cf8", "grammar": "#10B981",
                         "comprehension": "#f59e0b", "writing": "#EC4899",
                         "speaking": "#06B6D4", "other": "#64748b"}
        for sk, pct in sorted(r.skill_breakdown.items(), key=lambda x: -x[1]):
            clr = skill_colors.get(sk, "#64748b")
            emoji = {"vocabulary": "📚", "grammar": "📝", "comprehension": "📖",
                      "writing": "✍️", "speaking": "🗣️"}.get(sk, "📊")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin:4px 0;">
            <div style="width:120px;color:#94A3B8;font-size:.82rem;">{emoji} {sk.title()}</div>
            <div style="flex:1;">
            <div class="cefr-skill-bar"><div class="cefr-skill-fill" style="width:{pct}%;background:{clr};"></div></div>
            </div>
            <div style="width:50px;text-align:right;color:{clr};font-weight:700;font-size:.85rem;">%{pct}</div>
            </div>""", unsafe_allow_html=True)


def _render_certificate(r: CEFRResult, student_name: str = ""):
    """CEFR sertifika kartı."""
    cefr_info = CEFR_LEVELS.get(r.achieved_cefr, {})
    color = cefr_info.get("color", "#6366F1")
    name = student_name or r.student_name or "Student"

    st.markdown(f"""
    <div class="cefr-cert">
    <div style="font-size:.85rem;color:#64748b;letter-spacing:2px;">SMARTCAMPUS AI · ENGLISH LANGUAGE ASSESSMENT</div>
    <hr style="border-color:#8B5CF620;margin:12px 0;">
    <div style="font-size:1rem;color:#475569;">This is to certify that</div>
    <h2>{name}</h2>
    <div style="font-size:.9rem;color:#475569;">has demonstrated English language proficiency at</div>
    <div class="level">{r.achieved_cefr}</div>
    <div style="font-size:1rem;color:#6d28d9;font-weight:600;">{cefr_info.get('label','')}</div>
    <div style="font-size:.85rem;color:#64748b;margin-top:4px;">{cefr_info.get('cambridge','')}</div>
    <hr style="border-color:#8B5CF620;margin:12px 0;">
    <div class="detail">
    Score: {r.total_score}/{r.total_max} ({r.percentage}%) ·
    Listening: {r.listening_score}/{r.listening_max} ·
    Reading: {r.reading_score}/{r.reading_max} ·
    Writing: {r.writing_score}/{r.writing_max} ·
    Speaking: {r.speaking_score}/{r.speaking_max}
    </div>
    <div class="detail" style="margin-top:8px;">
    Grade {r.sinif} · {r.submitted_at[:10]} · SmartCampusAI 2025-2026
    </div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ANA RENDER
# ═══════════════════════════════════════════════════════════════════════════════

def render_cefr_exam():
    """Ana CEFR sınav ekranı — rol bazlı."""
    inject_common_css()
    styled_header("🏆 CEFR Mock Exam",
                  "Cambridge formatında seviye tespiti — Listening · Reading · Writing · Speaking")

    role = st.session_state.get("role", "teacher")
    if role in ("veli", "student", "ogrenci"):
        student_id = st.session_state.get("student_id", "")
        student_name = st.session_state.get("student_name", "")
        sinif = st.session_state.get("sinif", 5)
        sube = st.session_state.get("sube", "A")
        render_cefr_student(student_id, student_name, sinif, sube)
    else:
        render_cefr_teacher()
