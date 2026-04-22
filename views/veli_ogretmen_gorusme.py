"""
Veli-Ogretmen Gorusme Modulu
==============================
Veli-ogretmen gorusme planlama, takip ve istatistik sistemi.
"""

from __future__ import annotations

import json
import uuid
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "akademik"
GORUSME_FILE = DATA_DIR / "veli_ogretmen_gorusmeleri.json"


def _load_json(path):
    p = Path(path)
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _load_teachers():
    return _load_json(DATA_DIR / "teachers.json")


def _load_students():
    return _load_json(DATA_DIR / "students.json")


def _load_gorusmeler():
    return _load_json(GORUSME_FILE)


def _save_gorusmeler(data):
    _save_json(GORUSME_FILE, data)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KONU_SECENEKLERI = [
    "Akademik Durum",
    "Davranis",
    "Devamsizlik",
    "Genel Gorusme",
    "Ozel Egitim",
    "Rehberlik",
    "Diger",
]

DURUM_RENKLERI = {
    "onaylandi": "#22c55e",
    "bekliyor": "#f59e0b",
    "iptal": "#ef4444",
    "tamamlandi": "#3b82f6",
}

DURUM_LABELS = {
    "onaylandi": "Onaylandi",
    "bekliyor": "Bekliyor",
    "iptal": "Iptal Edildi",
    "tamamlandi": "Tamamlandi",
}

SAAT_DILIMLERI = [
    "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
    "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
    "15:00", "15:30", "16:00",
]

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_CSS = """
<style>
.metric-card{
    background:linear-gradient(135deg,#1e293b,#0f172a);
    padding:20px;border-radius:12px;border-left:4px solid;color:white;
}
.metric-card h3{font-size:14px;color:#94a3b8;margin:0 0 6px 0;font-weight:500;}
.metric-card .val{font-size:28px;font-weight:700;margin:0;}
.mc-blue{border-color:#3b82f6;} .mc-green{border-color:#22c55e;}
.mc-amber{border-color:#f59e0b;} .mc-red{border-color:#ef4444;}
.mc-purple{border-color:#a855f7;} .mc-cyan{border-color:#06b6d4;}
.gorusme-header{
    background:linear-gradient(90deg,#0f172a 0%,#1e3a5f 100%);
    padding:24px 28px;border-radius:14px;margin-bottom:18px;color:white;
}
.gorusme-header h2{margin:0;font-size:22px;}
.gorusme-header p{margin:4px 0 0;color:#94a3b8;font-size:13px;}
.meeting-card{
    background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;
    padding:14px 18px;margin-bottom:10px;border-left:4px solid;
}
.meeting-card .mc-title{font-weight:600;font-size:15px;color:#1e293b;margin:0;}
.meeting-card .mc-info{color:#64748b;font-size:13px;margin:3px 0 0;}
.status-badge{
    display:inline-block;padding:3px 10px;border-radius:12px;
    font-size:12px;font-weight:600;color:white;
}
.section-title{
    font-size:16px;font-weight:600;color:#1e293b;
    border-bottom:2px solid #3b82f6;padding-bottom:6px;margin:18px 0 12px;
}
.star{color:#f59e0b;font-size:18px;}
.star-empty{color:#cbd5e1;font-size:18px;}
</style>
"""


def _metric_card(title: str, value, color: str = "blue"):
    return (
        f'<div class="metric-card mc-{color}">'
        f'<h3>{title}</h3>'
        f'<p class="val">{value}</p>'
        f'</div>'
    )


def _section(title: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def _status_badge(durum: str):
    color = DURUM_RENKLERI.get(durum, "#94a3b8")
    label = DURUM_LABELS.get(durum, durum)
    return f'<span class="status-badge" style="background:{color};">{label}</span>'


def _star_rating(rating: int, max_stars: int = 5):
    filled = '<span class="star">&#9733;</span>' * rating
    empty = '<span class="star-empty">&#9733;</span>' * (max_stars - rating)
    return filled + empty


def _meeting_card(gorusme: dict, teachers_map: dict, students_map: dict):
    ogretmen = teachers_map.get(gorusme.get("ogretmen_id", ""), {})
    ogretmen_adi = f'{ogretmen.get("ad", "?")} {ogretmen.get("soyad", "")}'
    ogrenci = students_map.get(gorusme.get("ogrenci_id", ""), {})
    ogrenci_adi = f'{ogrenci.get("ad", "?")} {ogrenci.get("soyad", "")}'
    sinif = f'{ogrenci.get("sinif", "?")}-{ogrenci.get("sube", "?")}'
    tarih = gorusme.get("tarih", "-")
    saat = gorusme.get("saat", "-")
    konu = gorusme.get("konu", "-")
    durum = gorusme.get("durum", "bekliyor")
    veli_adi = gorusme.get("veli_adi", "-")
    badge = _status_badge(durum)
    border_color = DURUM_RENKLERI.get(durum, "#94a3b8")

    return (
        f'<div class="meeting-card" style="border-left-color:{border_color};">'
        f'<p class="mc-title">{konu} {badge}</p>'
        f'<p class="mc-info">Ogretmen: <b>{ogretmen_adi}</b> | '
        f'Ogrenci: <b>{ogrenci_adi}</b> ({sinif})</p>'
        f'<p class="mc-info">Veli: <b>{veli_adi}</b> | '
        f'Tarih: <b>{tarih}</b> | Saat: <b>{saat}</b></p>'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Tab 1: Gorusme Takvimi
# ---------------------------------------------------------------------------

def _tab_takvim(gorusmeler, teachers_map, students_map, teachers, students):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=4)  # Friday

    # Filters
    c1, c2, c3 = st.columns(3)
    teacher_names = ["Tumu"] + [
        f'{t.get("ad", "")} {t.get("soyad", "")}' for t in teachers if t.get("durum") == "aktif"
    ]
    with c1:
        sel_teacher = st.selectbox("Ogretmen Filtresi", teacher_names, key="cal_teacher")
    sinif_labels = ["Tumu"] + sorted(set(
        f'{s.get("sinif")}-{s.get("sube")}' for s in students if s.get("durum") == "aktif"
    ))
    with c2:
        sel_sinif = st.selectbox("Sinif Filtresi", sinif_labels, key="cal_sinif")
    durum_opts = ["Tumu"] + list(DURUM_LABELS.values())
    with c3:
        sel_durum = st.selectbox("Durum Filtresi", durum_opts, key="cal_durum")

    # Filter logic
    filtered = []
    for g in gorusmeler:
        # Teacher filter
        if sel_teacher != "Tumu":
            ogr = teachers_map.get(g.get("ogretmen_id", ""), {})
            ogr_name = f'{ogr.get("ad", "")} {ogr.get("soyad", "")}'
            if ogr_name != sel_teacher:
                continue
        # Sinif filter
        if sel_sinif != "Tumu":
            stu = students_map.get(g.get("ogrenci_id", ""), {})
            stu_sinif = f'{stu.get("sinif", "?")}-{stu.get("sube", "?")}'
            if stu_sinif != sel_sinif:
                continue
        # Durum filter
        if sel_durum != "Tumu":
            reverse_durum = {v: k for k, v in DURUM_LABELS.items()}
            if g.get("durum") != reverse_durum.get(sel_durum, ""):
                continue
        filtered.append(g)

    # This week
    _section(f"Bu Haftanin Gorusmeleri ({week_start.strftime('%d.%m')} - {week_end.strftime('%d.%m.%Y')})")
    this_week = []
    upcoming = []
    past = []
    for g in filtered:
        try:
            g_date = date.fromisoformat(g.get("tarih", "2000-01-01"))
        except ValueError:
            continue
        if week_start <= g_date <= week_end:
            this_week.append(g)
        elif g_date > today:
            upcoming.append(g)
        else:
            past.append(g)

    if this_week:
        this_week.sort(key=lambda x: (x.get("tarih", ""), x.get("saat", "")))
        for g in this_week:
            st.markdown(_meeting_card(g, teachers_map, students_map), unsafe_allow_html=True)
    else:
        st.info("Bu hafta planlanmis gorusme bulunmamaktadir.")

    # Upcoming
    if upcoming:
        _section("Yaklasan Gorusmeler")
        upcoming.sort(key=lambda x: (x.get("tarih", ""), x.get("saat", "")))
        for g in upcoming[:10]:
            st.markdown(_meeting_card(g, teachers_map, students_map), unsafe_allow_html=True)

    # All meetings list
    _section("Tum Gorusmeler")
    if filtered:
        rows = []
        for g in sorted(filtered, key=lambda x: x.get("tarih", ""), reverse=True):
            ogr = teachers_map.get(g.get("ogretmen_id", ""), {})
            stu = students_map.get(g.get("ogrenci_id", ""), {})
            rows.append({
                "Tarih": g.get("tarih", "-"),
                "Saat": g.get("saat", "-"),
                "Ogretmen": f'{ogr.get("ad", "?")} {ogr.get("soyad", "")}',
                "Ogrenci": f'{stu.get("ad", "?")} {stu.get("soyad", "")}',
                "Sinif": f'{stu.get("sinif", "?")}-{stu.get("sube", "?")}',
                "Konu": g.get("konu", "-"),
                "Durum": DURUM_LABELS.get(g.get("durum", ""), g.get("durum", "-")),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("Filtrelere uygun gorusme bulunamadi.")


# ---------------------------------------------------------------------------
# Tab 2: Yeni Gorusme Talebi
# ---------------------------------------------------------------------------

def _tab_yeni_talep(gorusmeler, teachers, students):
    _section("Yeni Gorusme Talebi Olustur")

    aktif_teachers = [t for t in teachers if t.get("durum") == "aktif"]
    aktif_students = [s for s in students if s.get("durum") == "aktif"]

    with st.form("yeni_gorusme_form", clear_on_submit=True):
        c1, c2 = st.columns(2)

        with c1:
            teacher_options = {
                f'{t.get("ad", "")} {t.get("soyad", "")} ({t.get("brans", "")})': t["id"]
                for t in aktif_teachers
            }
            sel_teacher = st.selectbox("Ogretmen", list(teacher_options.keys()))

            student_options = {
                f'{s.get("ad", "")} {s.get("soyad", "")} ({s.get("sinif")}-{s.get("sube")})': s["id"]
                for s in aktif_students
            }
            sel_student = st.selectbox("Ogrenci", list(student_options.keys()))

            konu = st.selectbox("Gorusme Konusu", KONU_SECENEKLERI)

        with c2:
            # Date selection - only weekdays
            min_date = date.today()
            max_date = date.today() + timedelta(days=60)
            sel_date = st.date_input(
                "Tarih", value=min_date, min_value=min_date, max_value=max_date,
                key="gorusme_tarih"
            )

            sel_saat = st.selectbox("Saat", SAAT_DILIMLERI)

            veli_adi = st.text_input("Veli Adi Soyadi")

        veli_notu = st.text_area("Veli Notu (Opsiyonel)", height=100,
                                 placeholder="Gorusme hakkinda eklemek istediginiz notlar...")

        submitted = st.form_submit_button("Gorusme Talebi Olustur", type="primary",
                                          use_container_width=True)

        if submitted:
            # Weekend check
            if sel_date and sel_date.weekday() >= 5:
                st.error("Hafta sonu gorusme planlanamaz. Lutfen hafta ici bir gun secin.")
            elif not sel_teacher:
                st.error("Lutfen bir ogretmen secin.")
            elif not sel_student:
                st.error("Lutfen bir ogrenci secin.")
            elif not veli_adi.strip():
                st.error("Lutfen veli adini girin.")
            else:
                # Check for conflict
                teacher_id = teacher_options.get(sel_teacher, "")
                date_str = sel_date.isoformat() if sel_date else ""
                conflict = any(
                    g.get("ogretmen_id") == teacher_id
                    and g.get("tarih") == date_str
                    and g.get("saat") == sel_saat
                    and g.get("durum") != "iptal"
                    for g in gorusmeler
                )

                if conflict:
                    st.error("Bu ogretmenin secilen tarih ve saatte zaten bir gorusmesi var. "
                             "Lutfen farkli bir zaman secin.")
                else:
                    student_id = student_options.get(sel_student, "")
                    stu = next((s for s in students if s["id"] == student_id), {})

                    new_meeting = {
                        "id": f"gor_{uuid.uuid4().hex[:8]}",
                        "ogretmen_id": teacher_id,
                        "ogrenci_id": student_id,
                        "veli_adi": veli_adi.strip(),
                        "tarih": date_str,
                        "saat": sel_saat,
                        "konu": konu,
                        "durum": "bekliyor",
                        "veli_notu": veli_notu.strip(),
                        "ogretmen_notu": "",
                        "puan": 0,
                        "olusturma_tarihi": datetime.now().isoformat(),
                        "akademik_yil": "2025-2026",
                    }
                    gorusmeler.append(new_meeting)
                    _save_gorusmeler(gorusmeler)
                    st.success("Gorusme talebi basariyla olusturuldu!")
                    st.balloons()


# ---------------------------------------------------------------------------
# Tab 3: Gecmis Gorusmeler
# ---------------------------------------------------------------------------

def _tab_gecmis(gorusmeler, teachers_map, students_map):
    _section("Tamamlanmis Gorusmeler")

    tamamlanan = [g for g in gorusmeler if g.get("durum") == "tamamlandi"]

    if not tamamlanan:
        st.info("Henuz tamamlanmis gorusme bulunmamaktadir.")

        # Show option to mark meetings as completed
        bekleyen = [g for g in gorusmeler if g.get("durum") in ("onaylandi", "bekliyor")]
        past_bekleyen = []
        today = date.today()
        for g in bekleyen:
            try:
                g_date = date.fromisoformat(g.get("tarih", "9999-12-31"))
                if g_date < today:
                    past_bekleyen.append(g)
            except ValueError:
                pass

        if past_bekleyen:
            _section("Tamamlanmasi Gereken Gorusmeler")
            st.warning(f"{len(past_bekleyen)} gecmis tarihli gorusme tamamlanmayi bekliyor.")
            for g in past_bekleyen:
                ogr = teachers_map.get(g.get("ogretmen_id", ""), {})
                stu = students_map.get(g.get("ogrenci_id", ""), {})
                label = (f'{g.get("tarih")} - {ogr.get("ad", "")} {ogr.get("soyad", "")} - '
                         f'{stu.get("ad", "")} {stu.get("soyad", "")}')

                with st.expander(label):
                    ogretmen_notu = st.text_area(
                        "Ogretmen Notu", key=f'note_{g["id"]}',
                        placeholder="Gorusme notlarini girin..."
                    )
                    puan = st.slider("Degerlendirme (1-5)", 1, 5, 3, key=f'rating_{g["id"]}')
                    if st.button("Tamamla", key=f'complete_{g["id"]}'):
                        g["durum"] = "tamamlandi"
                        g["ogretmen_notu"] = ogretmen_notu
                        g["puan"] = puan
                        _save_gorusmeler(gorusmeler)
                        st.success("Gorusme tamamlandi olarak isaretlendi!")
                        st.rerun()
        return

    # Sort by date descending
    tamamlanan.sort(key=lambda x: x.get("tarih", ""), reverse=True)

    for g in tamamlanan:
        ogr = teachers_map.get(g.get("ogretmen_id", ""), {})
        stu = students_map.get(g.get("ogrenci_id", ""), {})
        ogretmen_adi = f'{ogr.get("ad", "?")} {ogr.get("soyad", "")}'
        ogrenci_adi = f'{stu.get("ad", "?")} {stu.get("soyad", "")}'
        sinif = f'{stu.get("sinif", "?")}-{stu.get("sube", "?")}'
        tarih = g.get("tarih", "-")
        konu = g.get("konu", "-")
        puan = g.get("puan", 0)
        ogretmen_notu = g.get("ogretmen_notu", "")
        veli_notu = g.get("veli_notu", "")

        stars_html = _star_rating(puan)

        st.markdown(
            f'<div class="meeting-card" style="border-left-color:#3b82f6;">'
            f'<p class="mc-title">{konu} {_status_badge("tamamlandi")}</p>'
            f'<p class="mc-info">Ogretmen: <b>{ogretmen_adi}</b> | '
            f'Ogrenci: <b>{ogrenci_adi}</b> ({sinif}) | Tarih: <b>{tarih}</b></p>'
            f'<p class="mc-info">Degerlendirme: {stars_html}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if ogretmen_notu or veli_notu:
            with st.expander("Gorusme Notlari"):
                if ogretmen_notu:
                    st.markdown(f"**Ogretmen Notu:** {ogretmen_notu}")
                if veli_notu:
                    st.markdown(f"**Veli Notu:** {veli_notu}")


# ---------------------------------------------------------------------------
# Tab 4: Istatistik
# ---------------------------------------------------------------------------

_PALETTE = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#a855f7",
            "#06b6d4", "#ec4899", "#14b8a6", "#f97316", "#6366f1"]


def _tab_istatistik(gorusmeler, teachers_map, students_map):
    if not gorusmeler:
        st.info("Henuz gorusme verisi bulunmamaktadir.")
        return

    total = len(gorusmeler)
    tamamlanan = len([g for g in gorusmeler if g.get("durum") == "tamamlandi"])
    bekleyen = len([g for g in gorusmeler if g.get("durum") == "bekliyor"])
    iptal = len([g for g in gorusmeler if g.get("durum") == "iptal"])

    # Unique teachers with meetings
    teacher_ids = set(g.get("ogretmen_id", "") for g in gorusmeler)
    avg_per_teacher = round(total / len(teacher_ids), 1) if teacher_ids else 0

    # Metrics
    cols = st.columns(4)
    with cols[0]:
        st.markdown(_metric_card("Toplam Gorusme", total, "blue"), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(_metric_card("Tamamlanan", tamamlanan, "green"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(_metric_card("Bekleyen", bekleyen, "amber"), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(_metric_card("Ogretmen Basina Ort.", avg_per_teacher, "purple"), unsafe_allow_html=True)

    st.markdown("")

    c1, c2 = st.columns(2)

    # -- Topic distribution --
    with c1:
        _section("Konu Dagilimi")
        topic_counts = Counter(g.get("konu", "Diger") for g in gorusmeler)
        labels = list(topic_counts.keys())
        values = list(topic_counts.values())

        if HAS_PLOTLY:
            fig = px.pie(names=labels, values=values, title="En Cok Talep Edilen Konular",
                         color_discrete_sequence=_PALETTE)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                              margin=dict(l=10, r=10, t=40, b=10), height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            df_topic = pd.DataFrame({"Konu": labels, "Sayi": values})
            st.bar_chart(df_topic.set_index("Konu"))

    # -- Status distribution --
    with c2:
        _section("Durum Dagilimi")
        status_counts = Counter(DURUM_LABELS.get(g.get("durum", ""), "Bilinmiyor") for g in gorusmeler)
        labels = list(status_counts.keys())
        values = list(status_counts.values())

        if HAS_PLOTLY:
            colors = []
            rev_map = {v: k for k, v in DURUM_LABELS.items()}
            for lbl in labels:
                key = rev_map.get(lbl, "")
                colors.append(DURUM_RENKLERI.get(key, "#94a3b8"))
            fig = px.pie(names=labels, values=values, title="Gorusme Durumlari",
                         color_discrete_sequence=colors)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                              margin=dict(l=10, r=10, t=40, b=10), height=350)
            st.plotly_chart(fig, use_container_width=True)
        else:
            df_s = pd.DataFrame({"Durum": labels, "Sayi": values})
            st.bar_chart(df_s.set_index("Durum"))

    # -- Monthly trend --
    _section("Aylik Gorusme Trendi")
    month_counts = defaultdict(int)
    for g in gorusmeler:
        tarih = g.get("tarih", "")
        if len(tarih) >= 7:
            month_counts[tarih[:7]] += 1

    if month_counts:
        months_sorted = sorted(month_counts.keys())
        trend_df = pd.DataFrame({
            "Ay": months_sorted,
            "Gorusme Sayisi": [month_counts[m] for m in months_sorted],
        })
        if HAS_PLOTLY:
            fig = px.line(trend_df, x="Ay", y="Gorusme Sayisi",
                          title="Aylik Gorusme Sayisi", markers=True,
                          color_discrete_sequence=_PALETTE)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20), height=340,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.line_chart(trend_df.set_index("Ay"))

    # -- Teacher meeting counts --
    _section("Ogretmen Bazinda Gorusme Sayilari")
    teacher_meeting_counts = Counter(g.get("ogretmen_id", "") for g in gorusmeler)
    rows = []
    for tid, count in teacher_meeting_counts.most_common():
        t = teachers_map.get(tid, {})
        rows.append({
            "Ogretmen": f'{t.get("ad", "?")} {t.get("soyad", "")}',
            "Brans": t.get("brans", "-"),
            "Gorusme Sayisi": count,
        })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # -- Average rating --
    rated = [g for g in gorusmeler if g.get("puan", 0) > 0]
    if rated:
        _section("Degerlendirme Ozeti")
        avg_rating = round(sum(g["puan"] for g in rated) / len(rated), 1)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(_metric_card("Ortalama Puan", f"{avg_rating}/5", "cyan"), unsafe_allow_html=True)
        with c2:
            st.markdown(_metric_card("Degerlendirilen Gorusme", len(rated), "green"), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render_veli_ogretmen_gorusme():
    """Veli-Ogretmen Gorusme Modulu ana giris noktasi."""

    st.markdown(_CSS, unsafe_allow_html=True)

    st.markdown(
        '<div class="gorusme-header">'
        '<h2>Veli-Ogretmen Gorusme Sistemi</h2>'
        '<p>Gorusme planlama, takip ve degerlendirme platformu</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Load data
    teachers = _load_teachers()
    students = _load_students()
    gorusmeler = _load_gorusmeler()

    teachers_map = {t["id"]: t for t in teachers}
    students_map = {s["id"]: s for s in students}

    tab1, tab2, tab3, tab4 = st.tabs([
        "Gorusme Takvimi",
        "Yeni Gorusme Talebi",
        "Gecmis Gorusmeler",
        "Istatistik",
    ])

    with tab1:
        _tab_takvim(gorusmeler, teachers_map, students_map, teachers, students)
    with tab2:
        _tab_yeni_talep(gorusmeler, teachers, students)
    with tab3:
        _tab_gecmis(gorusmeler, teachers_map, students_map)
    with tab4:
        _tab_istatistik(gorusmeler, teachers_map, students_map)
