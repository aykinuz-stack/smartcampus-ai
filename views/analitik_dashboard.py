"""
Analitik Dashboard Modulu
=========================
Okul yoneticileri icin kapsamli analitik panosu.
Ogrenci, ogretmen, sinif, akademik performans, devamsizlik ve
karsilastirma analizleri.
"""

from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "akademik"


def _load_json(path):
    p = Path(path)
    if not p.exists():
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_students():
    return _load_json(DATA_DIR / "students.json")


def _load_teachers():
    return _load_json(DATA_DIR / "teachers.json")


def _load_grades():
    return _load_json(DATA_DIR / "grades.json")


def _load_attendance():
    return _load_json(DATA_DIR / "attendance.json")


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
.dash-header{
    background:linear-gradient(90deg,#0f172a 0%,#1e3a5f 100%);
    padding:24px 28px;border-radius:14px;margin-bottom:18px;color:white;
}
.dash-header h2{margin:0;font-size:22px;}
.dash-header p{margin:4px 0 0;color:#94a3b8;font-size:13px;}
.section-title{
    font-size:16px;font-weight:600;color:#1e293b;
    border-bottom:2px solid #3b82f6;padding-bottom:6px;margin:18px 0 12px;
}
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


# ---------------------------------------------------------------------------
# Plotly helpers
# ---------------------------------------------------------------------------

_PALETTE = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#a855f7",
            "#06b6d4", "#ec4899", "#14b8a6", "#f97316", "#6366f1"]


def _px_bar(df, x, y, title="", color=None, **kw):
    if HAS_PLOTLY:
        fig = px.bar(df, x=x, y=y, title=title, color=color,
                     color_discrete_sequence=_PALETTE, **kw)
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20), height=360,
            font=dict(size=12), title_font_size=14,
        )
        return fig
    return None


def _px_pie(labels, values, title=""):
    if HAS_PLOTLY:
        fig = px.pie(names=labels, values=values, title=title,
                     color_discrete_sequence=_PALETTE)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=40, b=10),
            height=340, title_font_size=14,
        )
        return fig
    return None


def _px_line(df, x, y, title="", **kw):
    if HAS_PLOTLY:
        fig = px.line(df, x=x, y=y, title=title,
                      color_discrete_sequence=_PALETTE, markers=True, **kw)
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20), height=340,
            font=dict(size=12), title_font_size=14,
        )
        return fig
    return None


# ---------------------------------------------------------------------------
# Tab 1: Genel Bakis
# ---------------------------------------------------------------------------

def _tab_genel_bakis(students, teachers, grades, attendance):
    aktif_students = [s for s in students if s.get("durum") == "aktif"]
    aktif_teachers = [t for t in teachers if t.get("durum") == "aktif"]

    siniflar = set()
    for s in aktif_students:
        siniflar.add(f'{s.get("sinif")}-{s.get("sube")}')

    # Metrics
    cols = st.columns(4)
    with cols[0]:
        st.markdown(_metric_card("Toplam Ogrenci", len(aktif_students), "blue"), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(_metric_card("Toplam Ogretmen", len(aktif_teachers), "green"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(_metric_card("Sinif Sayisi", len(siniflar), "amber"), unsafe_allow_html=True)
    with cols[3]:
        avg_grade = 0
        if grades:
            puanlar = [g["puan"] for g in grades if g.get("puan") is not None]
            if puanlar:
                avg_grade = round(sum(puanlar) / len(puanlar), 1)
        st.markdown(_metric_card("Genel Not Ort.", avg_grade, "purple"), unsafe_allow_html=True)

    st.markdown("")

    # Charts row
    c1, c2 = st.columns(2)

    # Gender distribution
    with c1:
        _section("Cinsiyet Dagilimi")
        gender_counts = Counter(s.get("cinsiyet", "Bilinmiyor") for s in aktif_students)
        labels = list(gender_counts.keys())
        values = list(gender_counts.values())
        fig = _px_pie(labels, values, "Cinsiyet Dagilimi")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            df_g = pd.DataFrame({"Cinsiyet": labels, "Sayi": values})
            st.bar_chart(df_g.set_index("Cinsiyet"))

    # Grade-level distribution
    with c2:
        _section("Kademe Dagilimi")
        grade_counts = Counter(str(s.get("sinif", "0")) for s in aktif_students)
        sorted_grades = sorted(grade_counts.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0)
        labels = [f'{g}. Sinif' for g, _ in sorted_grades]
        values = [c for _, c in sorted_grades]
        fig = _px_bar(
            pd.DataFrame({"Sinif": labels, "Ogrenci Sayisi": values}),
            x="Sinif", y="Ogrenci Sayisi", title="Sinif Bazinda Ogrenci Sayisi"
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(pd.DataFrame({"Ogrenci": values}, index=labels))

    # Attendance trend (last 6 months)
    _section("Devamsizlik Trendi (Son 6 Ay)")
    today = date.today()
    months = []
    for i in range(5, -1, -1):
        d = today.replace(day=1) - timedelta(days=30 * i)
        months.append(d.strftime("%Y-%m"))

    month_absence = defaultdict(int)
    for a in attendance:
        t = a.get("tarih", "")
        if len(t) >= 7:
            ym = t[:7]
            if ym in months:
                month_absence[ym] += 1

    trend_data = pd.DataFrame({
        "Ay": months,
        "Devamsizlik": [month_absence.get(m, 0) for m in months],
    })

    # If no data at all, generate mock for demo
    if trend_data["Devamsizlik"].sum() == 0:
        random.seed(42)
        trend_data["Devamsizlik"] = [random.randint(15, 80) for _ in months]

    fig = _px_line(trend_data, x="Ay", y="Devamsizlik", title="Aylik Devamsizlik Sayisi")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(trend_data.set_index("Ay"))


# ---------------------------------------------------------------------------
# Tab 2: Akademik Performans
# ---------------------------------------------------------------------------

def _tab_akademik_performans(students, grades):
    if not grades:
        st.info("Henuz not verisi bulunmamaktadir.")
        return

    stu_map = {s["id"]: s for s in students}
    df_grades = pd.DataFrame(grades)

    # -- Average grade by class --
    _section("Sinif Bazinda Not Ortalamalari")
    df_grades["sinif_sube"] = df_grades.apply(
        lambda r: f'{r.get("sinif", "?")}-{r.get("sube", "?")}', axis=1
    )
    class_avg = df_grades.groupby("sinif_sube")["puan"].mean().reset_index()
    class_avg.columns = ["Sinif", "Ortalama"]
    class_avg["Ortalama"] = class_avg["Ortalama"].round(1)
    class_avg = class_avg.sort_values("Sinif")

    fig = _px_bar(class_avg, x="Sinif", y="Ortalama", title="Sinif Not Ortalamalari")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(class_avg.set_index("Sinif"))

    c1, c2 = st.columns(2)

    # -- Top 10 students --
    with c1:
        _section("En Basarili 10 Ogrenci")
        stu_avg = df_grades.groupby("student_id")["puan"].mean().reset_index()
        stu_avg.columns = ["student_id", "Ortalama"]
        stu_avg["Ortalama"] = stu_avg["Ortalama"].round(1)
        stu_avg = stu_avg.sort_values("Ortalama", ascending=False).head(10)

        rows = []
        for _, r in stu_avg.iterrows():
            s = stu_map.get(r["student_id"], {})
            rows.append({
                "Ogrenci": f'{s.get("ad", "?")} {s.get("soyad", "")}',
                "Sinif": f'{s.get("sinif", "?")}-{s.get("sube", "?")}',
                "Ortalama": r["Ortalama"],
            })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # -- Subject-wise performance --
    with c2:
        _section("Ders Bazinda Performans")
        subj_avg = df_grades.groupby("ders")["puan"].mean().reset_index()
        subj_avg.columns = ["Ders", "Ortalama"]
        subj_avg["Ortalama"] = subj_avg["Ortalama"].round(1)
        subj_avg = subj_avg.sort_values("Ortalama", ascending=False)

        fig = _px_bar(subj_avg, x="Ders", y="Ortalama", title="Ders Ortalamalari")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(subj_avg.set_index("Ders"))

    # -- Grade trend over months --
    _section("Aylik Not Trendi")
    df_grades["ay"] = pd.to_datetime(df_grades["tarih"], errors="coerce").dt.to_period("M").astype(str)
    monthly_avg = df_grades.groupby("ay")["puan"].mean().reset_index()
    monthly_avg.columns = ["Ay", "Ortalama"]
    monthly_avg["Ortalama"] = monthly_avg["Ortalama"].round(1)
    monthly_avg = monthly_avg.sort_values("Ay")

    fig = _px_line(monthly_avg, x="Ay", y="Ortalama", title="Aylik Not Ortalamasi Trendi")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(monthly_avg.set_index("Ay"))


# ---------------------------------------------------------------------------
# Tab 3: Devamsizlik Analizi
# ---------------------------------------------------------------------------

def _tab_devamsizlik(students, attendance):
    if not attendance:
        st.info("Henuz devamsizlik verisi bulunmamaktadir.")
        return

    stu_map = {s["id"]: s for s in students}
    df_att = pd.DataFrame(attendance)

    total_absence = len(df_att)
    devamsiz_count = len([a for a in attendance if a.get("turu") == "devamsiz"])
    unique_students = df_att["student_id"].nunique()
    izinli_count = len([a for a in attendance if a.get("turu") == "izinli"])

    # Metrics
    cols = st.columns(4)
    with cols[0]:
        st.markdown(_metric_card("Toplam Kayit", total_absence, "red"), unsafe_allow_html=True)
    with cols[1]:
        st.markdown(_metric_card("Devamsiz (Ozursuz)", devamsiz_count, "amber"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(_metric_card("Izinli/Raporlu", izinli_count, "green"), unsafe_allow_html=True)
    with cols[3]:
        st.markdown(_metric_card("Etkilenen Ogrenci", unique_students, "purple"), unsafe_allow_html=True)

    st.markdown("")

    c1, c2 = st.columns(2)

    # -- Class-wise absence --
    with c1:
        _section("Sinif Bazinda Devamsizlik")
        df_att["sinif_label"] = df_att["student_id"].apply(
            lambda sid: f'{stu_map.get(sid, {}).get("sinif", "?")}-{stu_map.get(sid, {}).get("sube", "?")}'
        )
        class_abs = df_att["sinif_label"].value_counts().reset_index()
        class_abs.columns = ["Sinif", "Devamsizlik"]
        class_abs = class_abs.sort_values("Sinif")

        fig = _px_bar(class_abs, x="Sinif", y="Devamsizlik", title="Sinif Bazinda Devamsizlik")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(class_abs.set_index("Sinif"))

    # -- Day of week pattern --
    with c2:
        _section("Gun Bazinda Devamsizlik")
        gun_map = {0: "Pazartesi", 1: "Sali", 2: "Carsamba", 3: "Persembe",
                   4: "Cuma", 5: "Cumartesi", 6: "Pazar"}
        df_att["gun"] = pd.to_datetime(df_att["tarih"], errors="coerce").dt.dayofweek
        day_counts = df_att["gun"].value_counts().reset_index()
        day_counts.columns = ["gun_no", "Sayi"]
        day_counts["Gun"] = day_counts["gun_no"].map(gun_map)
        day_counts = day_counts.sort_values("gun_no")

        fig = _px_bar(day_counts, x="Gun", y="Sayi", title="Hangi Gun Daha Cok Devamsizlik?")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(day_counts.set_index("Gun")["Sayi"])

    # -- Monthly trend --
    _section("Aylik Devamsizlik Trendi")
    df_att["ay"] = pd.to_datetime(df_att["tarih"], errors="coerce").dt.to_period("M").astype(str)
    monthly = df_att.groupby("ay").size().reset_index(name="Devamsizlik")
    monthly = monthly.sort_values("ay")
    monthly.columns = ["Ay", "Devamsizlik"]

    fig = _px_line(monthly, x="Ay", y="Devamsizlik", title="Aylik Devamsizlik Trendi")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(monthly.set_index("Ay"))

    # -- Top absent students --
    _section("En Cok Devamsizlik Yapan Ogrenciler")
    top_abs = df_att["student_id"].value_counts().head(10).reset_index()
    top_abs.columns = ["student_id", "Devamsizlik"]
    rows = []
    for _, r in top_abs.iterrows():
        s = stu_map.get(r["student_id"], {})
        rows.append({
            "Ogrenci": f'{s.get("ad", "?")} {s.get("soyad", "")}',
            "Sinif": f'{s.get("sinif", "?")}-{s.get("sube", "?")}',
            "Devamsizlik": r["Devamsizlik"],
        })
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Tab 4: Ogretmen Performans
# ---------------------------------------------------------------------------

def _tab_ogretmen(teachers, grades, students):
    aktif_teachers = [t for t in teachers if t.get("durum") == "aktif"]
    if not aktif_teachers:
        st.info("Henuz ogretmen verisi bulunmamaktadir.")
        return

    # -- Teacher count by branch --
    _section("Brans Bazinda Ogretmen Sayisi")
    branch_counts = Counter(t.get("brans", "Bilinmiyor") for t in aktif_teachers)
    bc_df = pd.DataFrame({"Brans": list(branch_counts.keys()), "Sayi": list(branch_counts.values())})
    bc_df = bc_df.sort_values("Sayi", ascending=False)

    fig = _px_bar(bc_df, x="Brans", y="Sayi", title="Brans Bazinda Ogretmen Dagilimi")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart(bc_df.set_index("Brans"))

    c1, c2 = st.columns(2)

    # -- Classes per teacher (estimate based on schedule or grades) --
    with c1:
        _section("Ogretmen Istatistikleri")
        stats = []
        for t in aktif_teachers:
            stats.append({
                "Ogretmen": f'{t.get("ad", "")} {t.get("soyad", "")}',
                "Brans": t.get("brans", "-"),
                "E-posta": t.get("email", "-"),
            })
        st.dataframe(pd.DataFrame(stats), use_container_width=True, hide_index=True)

    # -- Average student performance per teacher's subject --
    with c2:
        _section("Brans Bazinda Ogrenci Performansi")
        if grades:
            df_g = pd.DataFrame(grades)
            ders_avg = df_g.groupby("ders")["puan"].mean().reset_index()
            ders_avg.columns = ["Ders", "Ortalama"]
            ders_avg["Ortalama"] = ders_avg["Ortalama"].round(1)
            ders_avg = ders_avg.sort_values("Ortalama", ascending=False)

            # Map ders -> teacher brans
            brans_set = set(t.get("brans", "") for t in aktif_teachers)
            teacher_perf = []
            for _, row in ders_avg.iterrows():
                matched_teachers = [
                    f'{t.get("ad", "")} {t.get("soyad", "")}'
                    for t in aktif_teachers
                    if t.get("brans", "").lower() in row["Ders"].lower()
                    or row["Ders"].lower() in t.get("brans", "").lower()
                ]
                teacher_perf.append({
                    "Ders": row["Ders"],
                    "Ortalama": row["Ortalama"],
                    "Ogretmen": ", ".join(matched_teachers) if matched_teachers else "-",
                })
            if teacher_perf:
                st.dataframe(pd.DataFrame(teacher_perf), use_container_width=True, hide_index=True)
        else:
            st.info("Not verisi bulunamadi.")


# ---------------------------------------------------------------------------
# Tab 5: Karsilastirma
# ---------------------------------------------------------------------------

def _tab_karsilastirma(students, grades, attendance):
    _section("Sinif Karsilastirmasi")

    aktif = [s for s in students if s.get("durum") == "aktif"]
    sinif_labels = sorted(set(f'{s.get("sinif")}-{s.get("sube")}' for s in aktif))

    if len(sinif_labels) < 2:
        st.warning("Karsilastirma icin en az 2 sinif gereklidir.")
        return

    c1, c2 = st.columns(2)
    with c1:
        class_a = st.selectbox("Sinif A", sinif_labels, key="cmp_a")
    with c2:
        remaining = [s for s in sinif_labels if s != class_a]
        class_b = st.selectbox("Sinif B", remaining, key="cmp_b")

    if not class_a or not class_b:
        return

    def _class_students(label):
        parts = label.split("-")
        sinif = int(parts[0]) if parts[0].isdigit() else 0
        sube = parts[1] if len(parts) > 1 else ""
        return [s for s in aktif if s.get("sinif") == sinif and s.get("sube") == sube]

    stu_a = _class_students(class_a)
    stu_b = _class_students(class_b)
    ids_a = {s["id"] for s in stu_a}
    ids_b = {s["id"] for s in stu_b}

    # Grades
    grades_a = [g["puan"] for g in grades if g.get("student_id") in ids_a and g.get("puan") is not None]
    grades_b = [g["puan"] for g in grades if g.get("student_id") in ids_b and g.get("puan") is not None]
    avg_a = round(sum(grades_a) / len(grades_a), 1) if grades_a else 0
    avg_b = round(sum(grades_b) / len(grades_b), 1) if grades_b else 0

    # Attendance
    att_a = len([a for a in attendance if a.get("student_id") in ids_a])
    att_b = len([a for a in attendance if a.get("student_id") in ids_b])

    st.markdown("---")

    # Side-by-side comparison
    col1, col_mid, col2 = st.columns([5, 1, 5])

    with col1:
        st.markdown(f"### {class_a}")
        st.markdown(_metric_card("Ogrenci Sayisi", len(stu_a), "blue"), unsafe_allow_html=True)
        st.markdown("")
        st.markdown(_metric_card("Not Ortalamasi", avg_a, "green"), unsafe_allow_html=True)
        st.markdown("")
        st.markdown(_metric_card("Devamsizlik", att_a, "red"), unsafe_allow_html=True)

    with col_mid:
        st.markdown("<div style='text-align:center;padding-top:60px;font-size:32px;color:#94a3b8;'>VS</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"### {class_b}")
        st.markdown(_metric_card("Ogrenci Sayisi", len(stu_b), "blue"), unsafe_allow_html=True)
        st.markdown("")
        st.markdown(_metric_card("Not Ortalamasi", avg_b, "green"), unsafe_allow_html=True)
        st.markdown("")
        st.markdown(_metric_card("Devamsizlik", att_b, "red"), unsafe_allow_html=True)

    # Subject comparison chart
    if grades:
        _section("Ders Bazinda Karsilastirma")
        df_g = pd.DataFrame(grades)
        df_g_a = df_g[df_g["student_id"].isin(ids_a)]
        df_g_b = df_g[df_g["student_id"].isin(ids_b)]

        subjects = sorted(set(df_g_a["ders"].tolist() + df_g_b["ders"].tolist()))
        comp_rows = []
        for subj in subjects:
            pa = df_g_a[df_g_a["ders"] == subj]["puan"]
            pb = df_g_b[df_g_b["ders"] == subj]["puan"]
            comp_rows.append({
                "Ders": subj,
                class_a: round(pa.mean(), 1) if len(pa) > 0 else 0,
                class_b: round(pb.mean(), 1) if len(pb) > 0 else 0,
            })
        comp_df = pd.DataFrame(comp_rows)

        if HAS_PLOTLY and len(comp_df) > 0:
            fig = go.Figure()
            fig.add_trace(go.Bar(name=class_a, x=comp_df["Ders"], y=comp_df[class_a],
                                 marker_color=_PALETTE[0]))
            fig.add_trace(go.Bar(name=class_b, x=comp_df["Ders"], y=comp_df[class_b],
                                 marker_color=_PALETTE[3]))
            fig.update_layout(
                barmode="group", title="Ders Bazinda Not Karsilastirmasi",
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=40, b=20), height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
        elif len(comp_df) > 0:
            st.dataframe(comp_df, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render_analitik_dashboard():
    """Analitik Dashboard ana giris noktasi."""

    st.markdown(_CSS, unsafe_allow_html=True)

    st.markdown(
        '<div class="dash-header">'
        '<h2>Analitik Dashboard</h2>'
        '<p>Okul geneli akademik performans, devamsizlik ve karsilastirma analizleri</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Load data once
    students = _load_students()
    teachers = _load_teachers()
    grades = _load_grades()
    attendance = _load_attendance()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Genel Bakis",
        "Akademik Performans",
        "Devamsizlik Analizi",
        "Ogretmen Performans",
        "Karsilastirma",
    ])

    with tab1:
        _tab_genel_bakis(students, teachers, grades, attendance)
    with tab2:
        _tab_akademik_performans(students, grades)
    with tab3:
        _tab_devamsizlik(students, attendance)
    with tab4:
        _tab_ogretmen(teachers, grades, students)
    with tab5:
        _tab_karsilastirma(students, grades, attendance)
