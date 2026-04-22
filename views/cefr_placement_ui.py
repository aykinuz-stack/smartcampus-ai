"""
SmartCampusAI — CEFR Seviye Tespit Sinavi UI
==============================================
Sene Basi / Sene Sonu — Gercek CEFR seviye olcumu.
Ogretmen: Sinav olustur + yonet + raporlar
Ogrenci: Sinav coz + sonuclar
Veri Kaynagi: KOI > Iletisim > Sinif Listeleri (load_shared_students)
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components
from datetime import date

from models.cefr_exam import (
    CEFR_LEVELS, CEFR_ORDER, GRADE_TO_CEFR,
    CEFRPlacementExam, CEFRPlacementResult, CEFRQuestion,
    CEFRPlacementQuestionGenerator, CEFRPlacementGrader, CEFRPlacementStore,
)
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("yabanci_dil")
except Exception:
    pass
from utils.shared_data import load_shared_students, get_sinif_sube_listesi, get_sinif_ogrenci_listesi


# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════

def _css():
    st.markdown("""<style>
    .cp-hero{background:linear-gradient(135deg,#0f172a,#1e1b4b,#312e81);
    border-radius:16px;padding:24px;margin-bottom:16px;border:1.5px solid rgba(99,102,241,.25);}
    .cp-hero h2{margin:0;color:#c7d2fe;font-size:1.3rem;}
    .cp-hero .sub{color:#818cf8;font-size:.88rem;margin-top:4px;}
    .cp-section{background:linear-gradient(135deg,#131825,#1a2035);border-radius:14px;
    padding:18px 22px;margin:12px 0;border:1px solid rgba(99,102,241,.15);}
    .cp-badge{display:inline-block;border-radius:20px;padding:6px 16px;
    font-weight:700;font-size:1.1rem;color:#fff;}
    .cp-level-card{background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
    padding:20px;text-align:center;border:2px solid;}
    .cp-bar{background:rgba(99,102,241,.1);border-radius:6px;height:20px;overflow:hidden;margin:4px 0;}
    .cp-fill{height:100%;border-radius:6px;transition:width .3s;}
    .cp-q{background:rgba(99,102,241,.04);border:1px solid rgba(99,102,241,.1);
    border-radius:10px;padding:14px 18px;margin:8px 0;}
    .cp-delta-up{color:#10b981;font-weight:700;}
    .cp-delta-down{color:#ef4444;font-weight:700;}
    .cp-delta-same{color:#94a3b8;font-weight:700;}
    </style>""", unsafe_allow_html=True)


def _academic_year() -> str:
    today = date.today()
    if today.month >= 9:
        return f"{today.year}-{today.year + 1}"
    return f"{today.year - 1}-{today.year}"


# ═══════════════════════════════════════════════════════════════════════════════
# AI DESTEKLİ CEFR ANALİZ
# ═══════════════════════════════════════════════════════════════════════════════

def _generate_ai_cefr_analysis(result: CEFRPlacementResult,
                                prev_result: CEFRPlacementResult | None = None) -> str | None:
    """OpenAI ile ogrenci CEFR placement sonucu analizi uretir."""
    try:
        from utils.smarti_helper import _get_client, _get_ai_response
        client = _get_client()
        if not client:
            return None

        # Mevcut sonuc
        listen_pct = round(result.listening_score / result.listening_max * 100, 1) if result.listening_max > 0 else 0
        read_pct = round(result.reading_score / result.reading_max * 100, 1) if result.reading_max > 0 else 0
        grammar_pct = round(result.use_of_english_score / result.use_of_english_max * 100, 1) if result.use_of_english_max > 0 else 0
        write_pct = round(result.writing_score / result.writing_max * 100, 1) if result.writing_max > 0 else 0

        level_scores = ", ".join(f"{k}: %{v}" for k, v in result.score_by_level.items()) if result.score_by_level else "-"

        context = f"""
Ogrenci: {result.student_name}
Sinif: {result.sinif}. Sinif / {result.sube} Subesi
Donem: {"Sene Basi" if result.period == "sene_basi" else "Sene Sonu"} ({result.academic_year})
Hedef CEFR Seviyesi: {result.target_cefr}
Tespit Edilen CEFR Seviyesi: {result.placed_cefr}
Genel Basari: %{result.percentage}
Bolum Puanlari: Listening %{listen_pct}, Reading %{read_pct}, Use of English (Grammar) %{grammar_pct}, Writing %{write_pct}
Seviye Bazli Performans: {level_scores}
Hedefin Altinda mi: {"Evet" if result.is_below_target else "Hayir"}
Hedefin Ustunde mi: {"Evet" if result.is_above_target else "Hayir"}
"""

        # Onceki sonuc varsa karsilastirma ekle
        if prev_result:
            prev_listen = round(prev_result.listening_score / prev_result.listening_max * 100, 1) if prev_result.listening_max > 0 else 0
            prev_read = round(prev_result.reading_score / prev_result.reading_max * 100, 1) if prev_result.reading_max > 0 else 0
            prev_grammar = round(prev_result.use_of_english_score / prev_result.use_of_english_max * 100, 1) if prev_result.use_of_english_max > 0 else 0
            prev_write = round(prev_result.writing_score / prev_result.writing_max * 100, 1) if prev_result.writing_max > 0 else 0

            context += f"""
--- ONCEKI SINAV SONUCU ---
Donem: {"Sene Basi" if prev_result.period == "sene_basi" else "Sene Sonu"} ({prev_result.academic_year})
Onceki CEFR Seviyesi: {prev_result.placed_cefr}
Onceki Genel Basari: %{prev_result.percentage}
Onceki Bolum Puanlari: Listening %{prev_listen}, Reading %{prev_read}, Grammar %{prev_grammar}, Writing %{prev_write}
Degisim: %{result.percentage - prev_result.percentage:+.1f}
Seviye Degisimi: {prev_result.placed_cefr} → {result.placed_cefr}
"""

        messages = [
            {"role": "system", "content": (
                "Sen uzman bir Ingilizce dil egitimcisi ve CEFR degerlendirme uzmanisin. "
                "Turkce analiz yaz. Ogrencinin CEFR seviye tespit sinavi sonucunu analiz et. "
                "Onceki ve sonraki sonuc varsa ilerleme/gerileme karsilastirmasi yap. "
                "Markdown formatinda, basliklar ve maddeler kullanarak yaz. "
                "Icerigi su bolumlerle yapilandir:\n"
                "1. **Genel Degerlendirme** (2-3 cumle)\n"
                "2. **Guclu Yonler** (hangi beceriler iyi)\n"
                "3. **Gelistirilmesi Gereken Alanlar** (hangi becerilerde eksik)\n"
                "4. **Ilerleme Analizi** (onceki sonuc varsa karsilastir)\n"
                "5. **Oneriler** (somut, uygulanabilir 4-5 madde — evde/okulda yapilabilecekler)\n"
                "6. **Hedef** (bir sonraki donem icin hedef CEFR seviyesi ve basari yuzdesi)\n"
                "Kisa ve ogrenci/veli icin anlasilir yaz. Emoji kullanabilirsin."
            )},
            {"role": "user", "content": f"CEFR Seviye Tespit Sinavi Sonucu:\n{context}"},
        ]

        return _get_ai_response(client, messages)
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# OGRETMEN — SINAV OLUSTUR + YONET + RAPORLAR
# ═══════════════════════════════════════════════════════════════════════════════

def _render_teacher():
    store = CEFRPlacementStore()
    tabs = st.tabs(["📝 Sinav Olustur", "📋 Sinav Yonet", "📊 Raporlar"])

    # ── TAB 1: Sinav Olustur ──
    with tabs[0]:
        styled_section("CEFR Seviye Tespit Sinavi Olustur", "#6366f1")

        st.markdown(
            '<div style="background:linear-gradient(135deg,#eef2ff,#e0e7ff);color:#3730a3;'
            'padding:12px 18px;border-radius:10px;margin-bottom:16px;font-size:0.87rem;'
            'border-left:4px solid #6366f1">'
            '<b>Veri Kaynagi:</b> KOI > Iletisim > Sinif Listeleri. '
            'Ogrenci eklemek icin <b>Kurumsal Organizasyon</b> modulunu kullanin.</div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            ac_year = st.text_input("Egitim-Ogretim Yili", value=_academic_year(), key="cp_year")
        with c2:
            period = st.selectbox("Donem", ["sene_basi", "sene_sonu"],
                                   format_func=lambda x: "Sene Basi" if x == "sene_basi" else "Sene Sonu",
                                   key="cp_period")
        with c3:
            grade_opts = {f"{i}. Sinif": i for i in range(1, 13)}
            grade_label = st.selectbox("Sinif", list(grade_opts.keys()), index=4, key="cp_grade")
            grade = grade_opts[grade_label]

        cefr = GRADE_TO_CEFR.get(grade, "A2")
        cefr_info = CEFR_LEVELS.get(cefr, {})

        # Sube secimi
        students_all = load_shared_students()

        def _sinif_match(s, g):
            """String/int agnostik sinif karsilastirma."""
            try:
                return int(s.get("sinif", 0)) == int(g)
            except (ValueError, TypeError):
                return str(s.get("sinif", "")) == str(g)

        available_subes = sorted(set(
            s.get("sube", "") for s in students_all
            if _sinif_match(s, grade) and s.get("durum", "aktif") == "aktif"
        ))
        sube_opts = ["Tum Subeler"] + available_subes
        sube_sel = st.selectbox("Sube", sube_opts, key="cp_sube")
        sube = "" if sube_sel == "Tum Subeler" else sube_sel

        # Ogrenci sayisi
        students_filtered = [
            s for s in students_all
            if _sinif_match(s, grade) and s.get("durum", "aktif") == "aktif"
            and (not sube or s.get("sube") == sube)
        ]
        student_count = len(students_filtered)

        # Bilgi karti
        st.markdown(f"""
        <div class="cp-section">
        <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
            <span class="cp-badge" style="background:{cefr_info.get('color','#6366F1')};">{cefr}</span>
            <span style="color:#94A3B8;margin-left:8px;">{cefr_info.get('cambridge','')}</span>
        </div>
        <div style="color:#818cf8;font-weight:700;">{student_count} ogrenci</div>
        </div>
        <div style="color:#94a3b8;font-size:.82rem;margin-top:8px;">
        Hedef seviye: {cefr} | Test seviyeleri: {cefr} +/- 1 seviye |
        {'Sene Basi' if period == 'sene_basi' else 'Sene Sonu'} | {ac_year}
        </div></div>""", unsafe_allow_html=True)

        if student_count == 0:
            st.info("Bu sinifta henuz aktif ogrenci yok. Sinav olusturulabilir, ogrenciler sonra eklenebilir.")

        if st.button("🎯 CEFR Seviye Tespit Sinavi Olustur", key="cp_gen",
                       type="primary", use_container_width=True):
            with st.spinner(f"{grade_label} — {cefr} Placement sinavi olusturuluyor..."):
                gen = CEFRPlacementQuestionGenerator(grade)
                exam = gen.generate_placement_exam(period, ac_year, sinif=grade, sube=sube)
                exam.status = "created"  # Ogretmen Baslat deyince active olacak
                store.save_exam(exam)
                st.success(f"✅ {exam.name} — {len(exam.questions)} soru olusturuldu! "
                           f"Sinav Yonet sekmesinden BASLATABILIRSINIZ.")

        # Olusturulan sinavlari hemen goster
        recent = store.list_exams(grade=grade, academic_year=ac_year)
        if recent:
            st.markdown("---")
            st.markdown(f"**Bu sinif icin mevcut sinavlar ({len(recent)} adet):**")
            for ex in reversed(recent[-5:]):
                _p = "Sene Basi" if ex.period == "sene_basi" else "Sene Sonu"
                st.markdown(f"- 📋 **{ex.name}** | {_p} | {len(ex.questions)} soru | "
                            f"Durum: `{ex.status}` | {ex.created_at[:10]}")

    # ── TAB 2: Sinav Yonet — Olcme Mantigi ──
    with tabs[1]:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:14px;
        padding:14px 18px;margin-bottom:12px;border:1px solid rgba(34,197,94,0.2);">
        <div style="font-size:.9rem;font-weight:700;color:#86efac;">📡 CEFR Sinav Uygula & Degerlendir</div>
        <div style="font-size:.75rem;color:#64748b;margin-top:2px;">
        1) Sinavi olustur → 2) Baslat → 3) Ogrenciler cozer → 4) Degerlendir</div>
        </div>""", unsafe_allow_html=True)

        exams = store.list_exams()
        if not exams:
            st.info("Henuz CEFR sinavi olusturulmamis. 'Sinav Olustur' sekmesinden baslatin.")
        else:
            # Kategorize
            aktif = [e for e in exams if e.status == "published"]
            bekleyen = [e for e in exams if e.status == "created"]
            bitmis = [e for e in exams if e.status == "closed"]

            # ── AKTİF SINAVLAR ──
            for exam in aktif:
                ci = CEFR_LEVELS.get(exam.cefr, {})
                period_label = "Sene Basi" if exam.period == "sene_basi" else "Sene Sonu"
                exam_results = store.get_class_results(exam.sinif, exam.sube or "", exam.id)

                st.markdown(f"""<div style="background:linear-gradient(135deg,#052e16,#14532d);
                border-radius:14px;padding:16px 20px;margin:8px 0;border:1.5px solid rgba(34,197,94,0.3);">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                <div style="font-size:1rem;font-weight:700;color:#86efac;">🟢 {exam.name}</div>
                <div style="font-size:.82rem;color:#4ade80;margin-top:2px;">
                {exam.sinif}. Sinif · {exam.cefr} · {len(exam.questions)} soru · {exam.duration_min} dk ·
                {period_label} {exam.academic_year}</div>
                </div>
                <div style="text-align:right;">
                <div style="font-size:1.2rem;font-weight:900;color:#22c55e;">
                {len(exam_results)} sonuc</div>
                </div></div></div>""", unsafe_allow_html=True)

                bc1, bc2, bc3 = st.columns(3)
                with bc1:
                    if exam_results:
                        if st.button(f"📊 DEGERLENDIR ({len(exam_results)})", key=f"cp_grade_{exam.id}",
                                       type="primary", use_container_width=True):
                            st.success(f"✅ {len(exam_results)} sonuc mevcut — Raporlar sekmesinden inceleyin.")
                with bc2:
                    if st.button("🔴 Sinavi Bitir", key=f"cp_end_{exam.id}", use_container_width=True):
                        exam.status = "closed"
                        store.save_exam(exam)
                        st.success("Sinav tamamlandi!")
                        st.rerun()
                with bc3:
                    if st.button("📝 Soru Onizle", key=f"cp_preview_{exam.id}", use_container_width=True):
                        st.session_state[f"_cp_preview_{exam.id}"] = not st.session_state.get(f"_cp_preview_{exam.id}", False)

                if st.session_state.get(f"_cp_preview_{exam.id}"):
                    with st.expander("Soru Onizleme", expanded=True):
                        for i, q in enumerate(exam.questions[:10]):
                            stem = getattr(q, "stem", "") if hasattr(q, "stem") else q.get("stem", "") if isinstance(q, dict) else ""
                            st.markdown(f"**Q{i+1}.** {stem[:150]}")

            # ── BEKLEYEN SINAVLAR ──
            if bekleyen:
                st.markdown("---")
                st.markdown("**Baslatilmayi Bekleyen Sinavlar:**")
                for exam in bekleyen:
                    period_label = "Sene Basi" if exam.period == "sene_basi" else "Sene Sonu"
                    bc1, bc2 = st.columns([3, 1])
                    with bc1:
                        st.markdown(f"⚪ **{exam.name}** — {exam.sinif}. Sinif · {exam.cefr} · "
                                    f"{len(exam.questions)} soru · {period_label}")
                    with bc2:
                        if st.button("🟢 Baslat", key=f"cp_start_{exam.id}", type="primary",
                                       use_container_width=True):
                            exam.status = "published"
                            store.save_exam(exam)
                            st.success(f"✅ CEFR sinavi baslatildi! Ogrenciler artik cozebilir.")
                            st.rerun()

            # ── BİTMİŞ SINAVLAR ──
            if bitmis:
                with st.expander(f"🏁 Tamamlanan Sinavlar ({len(bitmis)})", expanded=False):
                    for exam in bitmis:
                        period_label = "Sene Basi" if exam.period == "sene_basi" else "Sene Sonu"
                        exam_results = store.get_class_results(exam.sinif, exam.sube or "", exam.id)
                        st.markdown(f"✅ **{exam.name}** — {len(exam_results)} sonuc · {period_label} {exam.academic_year}")

    # ── TAB 3: Raporlar ──
    with tabs[2]:
        _render_reports(store)


# ═══════════════════════════════════════════════════════════════════════════════
# RAPORLAR
# ═══════════════════════════════════════════════════════════════════════════════

def _render_reports(store: CEFRPlacementStore):
    styled_section("CEFR Seviye Tespit Raporlari", "#8b5cf6")

    rtabs = st.tabs(["👤 Ogrenci Raporu", "📊 Sinif Raporu", "📈 Karsilastirma (Sene Basi vs Sonu)"])

    ac_year = st.session_state.get("cp_year", _academic_year())

    # ── Ogrenci Raporu ──
    with rtabs[0]:
        students = load_shared_students()
        active = [s for s in students if s.get("durum", "aktif") == "aktif"]
        if not active:
            st.info("Aktif ogrenci bulunamadi.")
            return

        student_opts = {f"{s.get('ad','')} {s.get('soyad','')} — {s.get('sinif','')}/{s.get('sube','')}": s
                         for s in active}
        sel = st.selectbox("Ogrenci Secin", [""] + list(student_opts.keys()), key="cp_rep_stu")
        if sel and sel in student_opts:
            stu = student_opts[sel]
            results = store.get_student_results(stu.get("id", ""), ac_year)
            if not results:
                st.info("Bu ogrencinin henuz placement sonucu yok.")
            else:
                sorted_results = sorted(results, key=lambda x: x.submitted_at, reverse=True)
                for idx, r in enumerate(sorted_results):
                    prev = sorted_results[idx + 1] if idx + 1 < len(sorted_results) else None
                    _render_placement_result(r, prev)

    # ── Sinif Raporu ──
    with rtabs[1]:
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            r_grade = st.selectbox("Sinif", list(range(1, 13)), index=4, key="cp_rep_grade")
        with rc2:
            students_cls = [s for s in load_shared_students()
                            if s.get("sinif") == r_grade and s.get("durum", "aktif") == "aktif"]
            r_subes = sorted(set(s.get("sube", "") for s in students_cls))
            r_sube = st.selectbox("Sube", r_subes if r_subes else ["A"], key="cp_rep_sube")
        with rc3:
            r_period = st.selectbox("Donem", ["sene_basi", "sene_sonu"],
                                     format_func=lambda x: "Sene Basi" if x == "sene_basi" else "Sene Sonu",
                                     key="cp_rep_period")

        results = store.get_period_results(r_grade, r_sube, r_period, ac_year)
        if not results:
            st.info("Bu sinif/sube/donem icin sonuc bulunamadi.")
        else:
            # Istatistikler
            avg_pct = round(sum(r.percentage for r in results) / len(results), 1)
            level_dist = {}
            for r in results:
                level_dist[r.placed_cefr] = level_dist.get(r.placed_cefr, 0) + 1

            styled_stat_row([
                ("Ogrenci", str(len(results)), "#6366f1", "👨‍🎓"),
                ("Ortalama", f"%{avg_pct}", "#10b981", "📊"),
                ("En Yuksek", f"%{max(r.percentage for r in results)}", "#f59e0b", "🏆"),
            ])

            # CEFR dagilim
            st.markdown("#### CEFR Seviye Dagilimi")
            for level in CEFR_ORDER:
                cnt = level_dist.get(level, 0)
                if cnt > 0:
                    pct = round(cnt / len(results) * 100)
                    clr = CEFR_LEVELS.get(level, {}).get("color", "#6366f1")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;margin:4px 0;">
                    <div style="width:60px;color:#94a3b8;font-weight:700;">{level}</div>
                    <div style="flex:1;"><div class="cp-bar"><div class="cp-fill" style="width:{pct}%;background:{clr};"></div></div></div>
                    <div style="width:80px;text-align:right;color:{clr};font-weight:700;">{cnt} (%{pct})</div>
                    </div>""", unsafe_allow_html=True)

            # Ogrenci tablosu
            st.markdown("#### Ogrenci Detay")
            import pandas as pd
            df_data = []
            for r in sorted(results, key=lambda x: -x.percentage):
                df_data.append({
                    "Ogrenci": r.student_name,
                    "CEFR": r.placed_cefr,
                    "Hedef": r.target_cefr,
                    "Puan": f"{r.total_score}/{r.total_max}",
                    "%": r.percentage,
                    "Listening": f"{r.listening_score}/{r.listening_max}",
                    "Reading": f"{r.reading_score}/{r.reading_max}",
                    "Grammar": f"{r.use_of_english_score}/{r.use_of_english_max}",
                    "Writing": f"{r.writing_score}/{r.writing_max}",
                })
            st.dataframe(pd.DataFrame(df_data), use_container_width=True)

    # ── Karsilastirma ──
    with rtabs[2]:
        kc1, kc2 = st.columns(2)
        with kc1:
            k_grade = st.selectbox("Sinif", list(range(1, 13)), index=4, key="cp_cmp_grade")
        with kc2:
            students_k = [s for s in load_shared_students()
                          if s.get("sinif") == k_grade and s.get("durum", "aktif") == "aktif"]
            k_subes = sorted(set(s.get("sube", "") for s in students_k))
            k_sube = st.selectbox("Sube", k_subes if k_subes else ["A"], key="cp_cmp_sube")

        comp = store.get_comparison(k_grade, k_sube, ac_year)
        if not comp["sene_basi"] and not comp["sene_sonu"]:
            st.info("Karsilastirma icin hem Sene Basi hem Sene Sonu sonucu gerekli.")
        else:
            basi_cnt = len(comp["sene_basi"])
            sonu_cnt = len(comp["sene_sonu"])
            styled_stat_row([
                ("Sene Basi", str(basi_cnt), "#6366f1", "📋"),
                ("Sene Sonu", str(sonu_cnt), "#10b981", "📋"),
                ("Karsilastirilan", str(len(comp["deltas"])), "#f59e0b", "📈"),
            ])

            if comp["deltas"]:
                st.markdown("#### Ogrenci Ilerleme Tablosu")
                import pandas as pd
                rows = []
                for d in sorted(comp["deltas"], key=lambda x: -x["delta_pct"]):
                    delta = d["delta_pct"]
                    if delta > 0:
                        arrow = "↑"
                    elif delta < 0:
                        arrow = "↓"
                    else:
                        arrow = "→"
                    rows.append({
                        "Ogrenci": d["student_name"],
                        "Sene Basi CEFR": d["basi_cefr"],
                        "Sene Basi %": d["basi_pct"],
                        "Sene Sonu CEFR": d["sonu_cefr"],
                        "Sene Sonu %": d["sonu_pct"],
                        "Degisim": f"{arrow} {delta:+.1f}%",
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

                # Ozet
                improved = sum(1 for d in comp["deltas"] if d["delta_pct"] > 0)
                declined = sum(1 for d in comp["deltas"] if d["delta_pct"] < 0)
                same = sum(1 for d in comp["deltas"] if d["delta_pct"] == 0)
                st.markdown(f"""
                <div class="cp-section">
                <div style="display:flex;gap:30px;justify-content:center;font-size:1rem;">
                <span class="cp-delta-up">↑ Yukselenler: {improved}</span>
                <span class="cp-delta-same">→ Ayni Kalanlar: {same}</span>
                <span class="cp-delta-down">↓ Dusenler: {declined}</span>
                </div></div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SONUC GOSTERIMI
# ═══════════════════════════════════════════════════════════════════════════════

def _render_placement_result(r: CEFRPlacementResult, prev_result: CEFRPlacementResult | None = None):
    """Tek ogrenci placement sonucu + AI analiz."""
    ci = CEFR_LEVELS.get(r.placed_cefr, {})
    color = ci.get("color", "#6366f1")
    period_label = "Sene Basi" if r.period == "sene_basi" else "Sene Sonu"

    st.markdown(f"""<div class="cp-hero" style="border-color:{color};">
    <h2>📋 CEFR Seviye Tespit Raporu — {period_label}</h2>
    <div class="sub">{r.student_name} · Sinif {r.sinif}/{r.sube} · {r.academic_year} · {r.submitted_at[:10]}</div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="cp-level-card" style="border-color:{color};">
        <div style="color:#94a3b8;font-size:.8rem;">Tespit Edilen Seviye</div>
        <div class="cp-badge" style="background:{color};font-size:1.5rem;margin:10px 0;">{r.placed_cefr}</div>
        <div style="color:#94a3b8;font-size:.8rem;">{ci.get('label','')}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        target_ci = CEFR_LEVELS.get(r.target_cefr, {})
        st.markdown(f"""<div class="cp-level-card" style="border-color:{target_ci.get('color','#64748b')};">
        <div style="color:#94a3b8;font-size:.8rem;">Hedef Seviye ({r.sinif}. Sinif)</div>
        <div style="color:#818cf8;font-size:1.3rem;font-weight:700;margin:10px 0;">{r.target_cefr}</div>
        <div style="color:#94a3b8;font-size:.8rem;">{target_ci.get('label','')}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.metric("Toplam Puan", f"{r.total_score}/{r.total_max}")
        st.metric("Yuzde", f"%{r.percentage}")

    # Bolum puanlari
    st.markdown("#### Bolum Puanlari")
    sections = [
        ("🎧 Listening", r.listening_score, r.listening_max, "#6366f1"),
        ("📖 Reading", r.reading_score, r.reading_max, "#10b981"),
        ("📝 Use of English", r.use_of_english_score, r.use_of_english_max, "#f59e0b"),
        ("✍️ Writing", r.writing_score, r.writing_max, "#ec4899"),
    ]
    cols = st.columns(4)
    for i, (label, score, max_s, clr) in enumerate(sections):
        with cols[i]:
            pct = round(score / max_s * 100, 1) if max_s > 0 else 0
            st.markdown(f"""
            <div style="text-align:center;">
            <div style="color:{clr};font-weight:700;font-size:.85rem;">{label}</div>
            <div style="font-size:1.1rem;color:#c7d2fe;font-weight:700;">{score}/{max_s}</div>
            <div class="cp-bar"><div class="cp-fill" style="width:{pct}%;background:{clr};"></div></div>
            <div style="color:#64748b;font-size:.75rem;">%{pct}</div>
            </div>""", unsafe_allow_html=True)

    # Seviye bazli puanlar
    if r.score_by_level:
        st.markdown("#### Seviye Bazli Performans")
        for lvl in CEFR_ORDER:
            pct = r.score_by_level.get(lvl, 0)
            if pct > 0 or lvl in (r.score_by_level or {}):
                clr = CEFR_LEVELS.get(lvl, {}).get("color", "#6366f1")
                status = "✅" if pct >= 60 else "❌"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin:4px 0;">
                <div style="width:80px;color:#94a3b8;font-weight:700;">{status} {lvl}</div>
                <div style="flex:1;"><div class="cp-bar"><div class="cp-fill" style="width:{pct}%;background:{clr};"></div></div></div>
                <div style="width:60px;text-align:right;color:{clr};font-weight:700;">%{pct}</div>
                </div>""", unsafe_allow_html=True)

    # ── AI Destekli Degerlendirme ──
    ai_cache_key = f"_cp_ai_{r.id}"
    if ai_cache_key not in st.session_state:
        st.session_state[ai_cache_key] = None

    with st.expander("🤖 AI Destekli CEFR Degerlendirme ve Tavsiyeler", expanded=False):
        if st.session_state[ai_cache_key]:
            st.markdown(st.session_state[ai_cache_key])
        else:
            if st.button("🤖 AI Analiz Olustur", key=f"cp_ai_btn_{r.id}",
                           type="primary", use_container_width=True):
                with st.spinner("AI analiz olusturuluyor..."):
                    ai_text = _generate_ai_cefr_analysis(r, prev_result)
                    if ai_text:
                        st.session_state[ai_cache_key] = ai_text
                        st.rerun()
                    else:
                        st.warning("AI analiz olusturulamadi. OpenAI API anahtarini kontrol edin.")


# ═══════════════════════════════════════════════════════════════════════════════
# OGRENCI — SINAV COZ + SONUCLAR
# ═══════════════════════════════════════════════════════════════════════════════

def _render_student(student_id: str = "", student_name: str = "",
                     sinif: int = 5, sube: str = "A"):
    store = CEFRPlacementStore()
    tabs = st.tabs(["📝 Sinav Coz", "📊 Sonuclarim"])

    with tabs[0]:
        exams = [e for e in store.list_exams(grade=sinif)
                 if e.status == "published" and (not e.sube or e.sube == sube)]
        if not exams:
            exams = [e for e in store.list_exams() if e.status == "published"]

        if not exams:
            st.info("Henuz yayinlanmis placement sinavi yok.")
            return

        sel_name = st.selectbox("Sinav Secin",
                                 [f"{e.name} ({e.academic_year})" for e in exams], key="cp_stu_sel")
        exam = exams[[f"{e.name} ({e.academic_year})" for e in exams].index(sel_name)]

        ci = CEFR_LEVELS.get(exam.cefr, {})
        st.markdown(f"""<div class="cp-hero">
        <h2>📋 {exam.name}</h2>
        <div class="sub">{exam.cefr} — {ci.get('cambridge','')} · {exam.duration_min} dk · {len(exam.questions)} soru
        · Seviyeler: {', '.join(exam.levels_tested)}</div>
        </div>""", unsafe_allow_html=True)

        # Bolumler
        section_tabs = st.tabs(["🎧 Listening", "📖 Reading", "📝 Use of English", "✍️ Writing"])
        answers = {}

        section_map = [
            (section_tabs[0], "listening"),
            (section_tabs[1], "reading"),
            (section_tabs[2], "use_of_english"),
            (section_tabs[3], "writing"),
        ]

        for tab, section_key in section_map:
            with tab:
                section_qs = [q for q in exam.questions if q.section == section_key]
                if not section_qs:
                    st.info("Bu bolumde soru yok.")
                    continue
                for q in section_qs:
                    key = f"cp_ans_{exam.id}_{q.id}"
                    st.markdown(f'<div class="cp-q">', unsafe_allow_html=True)
                    st.markdown(f"**Q{q.q_num}.** {q.instruction}")

                    if q.q_type == "mcq":
                        st.markdown(f"**{q.stem}**")
                        if q.choices:
                            opts = [f"{k}) {v}" for k, v in q.choices.items()]
                            sel = st.radio("", opts, key=key, label_visibility="collapsed")
                            if sel:
                                answers[q.id] = sel[0]
                    elif q.q_type == "fill_blank":
                        st.markdown(f"**{q.stem}**")
                        ans = st.text_input("", key=key, label_visibility="collapsed",
                                             placeholder="Write your answer...")
                        if ans:
                            answers[q.id] = ans
                    elif q.q_type == "writing":
                        st.markdown(f"**{q.stem}**")
                        ans = st.text_area("", key=key, height=120, label_visibility="collapsed",
                                            placeholder="Write your answer here...")
                        if ans:
                            answers[q.id] = ans

                    st.markdown("</div>", unsafe_allow_html=True)

        # Gonder
        st.markdown("---")
        if st.button("📤 Sinavi Gonder ve Sonucu Gor", key="cp_submit",
                       type="primary", use_container_width=True):
            # Session state'den cevaplari topla
            for q in exam.questions:
                key = f"cp_ans_{exam.id}_{q.id}"
                ans = st.session_state.get(key, "")
                if ans:
                    answers[q.id] = ans if q.q_type != "mcq" else ans[0] if ans else ""

            result = CEFRPlacementGrader.grade_exam(exam, answers)
            result.student_id = student_id
            result.student_name = student_name
            result.sinif = sinif
            result.sube = sube
            store.save_result(result)
            st.session_state["cp_last_result"] = result
            st.rerun()

        last = st.session_state.get("cp_last_result")
        if last:
            st.markdown("---")
            # Onceki sonucu bul
            all_prev = store.get_student_results(student_id)
            prev_for_last = None
            if all_prev:
                older = [r for r in all_prev if r.submitted_at < last.submitted_at]
                if older:
                    prev_for_last = max(older, key=lambda x: x.submitted_at)
            _render_placement_result(last, prev_for_last)

    with tabs[1]:
        results = store.get_student_results(student_id)
        if results:
            sorted_r = sorted(results, key=lambda x: x.submitted_at, reverse=True)
            for idx, r in enumerate(sorted_r):
                prev = sorted_r[idx + 1] if idx + 1 < len(sorted_r) else None
                _render_placement_result(r, prev)
        else:
            st.info("Henuz placement sonucunuz yok.")


# ═══════════════════════════════════════════════════════════════════════════════
# ANA RENDER
# ═══════════════════════════════════════════════════════════════════════════════

def render_cefr_placement():
    """CEFR Seviye Tespit ana ekrani — rol bazli."""
    inject_common_css()
    _css()
    styled_header("📋 CEFR Seviye Tespit Sinavi",
                  "Sene Basi / Sene Sonu — Gercek CEFR seviye olcumu")

    role = st.session_state.get("role", "teacher")
    if role in ("veli", "student", "ogrenci"):
        student_id = st.session_state.get("student_id", "")
        student_name = st.session_state.get("student_name", "")
        sinif = st.session_state.get("sinif", 5)
        sube = st.session_state.get("sube", "A")
        _render_student(student_id, student_name, sinif, sube)
    else:
        _render_teacher()
