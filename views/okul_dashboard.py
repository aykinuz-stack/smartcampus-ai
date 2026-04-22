"""
Okul Dashboard + MEB Raporlama + Veri Disa Aktarma
====================================================
Okul geneli analitik dashboard, MEB uyumlu raporlama ve
CSV/TXT veri disa aktarma islevleri.
"""
from __future__ import annotations

import csv
import io
import os
import json
from datetime import datetime, date, timedelta
from typing import Any

import streamlit as st

from utils.ui_common import _render_html


# ---------------------------------------------------------------------------
# Yardimci: veri yukleyiciler
# ---------------------------------------------------------------------------

def _load_json(filepath: str) -> list[dict[str, Any]]:
    """JSON dosyasini yukle, hata varsa bos liste dondur."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _get_gam_profiles() -> list[dict[str, Any]]:
    """Gamification profillerini yukle."""
    try:
        from utils.tenant import get_data_path
        base = get_data_path("gamification")
    except Exception:
        base = os.path.join("data", "gamification")
    return _load_json(os.path.join(base, "profiles.json"))


def _get_activity_log() -> list[dict[str, Any]]:
    """Gamification aktivite logunu yukle."""
    try:
        from utils.tenant import get_data_path
        base = get_data_path("gamification")
    except Exception:
        base = os.path.join("data", "gamification")
    return _load_json(os.path.join(base, "activity_log.json"))


def _get_students() -> list[dict[str, Any]]:
    """Ogrenci listesini yukle."""
    try:
        from utils.tenant import get_data_path
        base = get_data_path("akademik")
    except Exception:
        base = os.path.join("data", "akademik")
    return _load_json(os.path.join(base, "students.json"))


# ---------------------------------------------------------------------------
# Ana render fonksiyonu
# ---------------------------------------------------------------------------

def render_okul_dashboard() -> None:
    """Okul dashboard ana fonksiyonu — 4 sekmeli."""
    _render_html("""
    <div style="
        background:linear-gradient(135deg,#0f172a,#1e293b);
        border:1px solid #1e3a5f;
        border-radius:14px;
        padding:16px 24px;
        margin-bottom:16px;
        font-family:'Segoe UI',sans-serif;
    ">
        <div style="color:#e2e8f0;font-size:20px;font-weight:800;">Okul Dashboard</div>
        <div style="color:#94a3b8;font-size:12px;margin-top:4px;">
            Okul geneli analitik, karsilastirma, MEB raporlama ve veri disa aktarma
        </div>
    </div>
    """)

    tab_genel, tab_sinif, tab_meb, tab_export = st.tabs([
        "Genel Bakis",
        "Sinif Karsilastirma",
        "MEB Rapor",
        "Veri Disa Aktarma",
    ])

    with tab_genel:
        _render_genel_bakis()

    with tab_sinif:
        _render_sinif_karsilastirma()

    with tab_meb:
        _render_meb_rapor()

    with tab_export:
        _render_veri_export()


# ---------------------------------------------------------------------------
# Tab A: Genel Bakis
# ---------------------------------------------------------------------------

def _render_genel_bakis() -> None:
    """Genel bakis: toplam ogrenci, aktif ogrenci, modul kullanim, top 10, trend."""
    profiles = _get_gam_profiles()
    activities = _get_activity_log()
    students = _get_students()

    total_students = len(students) if students else len(profiles)
    today_str = date.today().isoformat()

    # Bugun aktif
    active_today = len({
        a.get("user_id") for a in activities
        if a.get("timestamp", "")[:10] == today_str
    })

    # Haftalik aktif
    week_ago = (date.today() - timedelta(days=7)).isoformat()
    active_weekly = len({
        a.get("user_id") for a in activities
        if a.get("timestamp", "")[:10] >= week_ago
    })

    # Istatistik kartlari
    _render_html(f"""
    <div style="
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:12px;
        margin-bottom:20px;
    ">
        <div style="
            background:linear-gradient(135deg,#0f172a,#162032);
            border:1px solid #1e3a5f;
            border-radius:12px;
            padding:16px;
            text-align:center;
            font-family:'Segoe UI',sans-serif;
        ">
            <div style="color:#94a3b8;font-size:11px;text-transform:uppercase;font-weight:600;">
                Toplam Ogrenci
            </div>
            <div style="color:#6366f1;font-size:28px;font-weight:800;margin-top:4px;">
                {total_students}
            </div>
        </div>
        <div style="
            background:linear-gradient(135deg,#0f172a,#162032);
            border:1px solid #1e3a5f;
            border-radius:12px;
            padding:16px;
            text-align:center;
            font-family:'Segoe UI',sans-serif;
        ">
            <div style="color:#94a3b8;font-size:11px;text-transform:uppercase;font-weight:600;">
                Bugun Aktif
            </div>
            <div style="color:#22c55e;font-size:28px;font-weight:800;margin-top:4px;">
                {active_today}
            </div>
        </div>
        <div style="
            background:linear-gradient(135deg,#0f172a,#162032);
            border:1px solid #1e3a5f;
            border-radius:12px;
            padding:16px;
            text-align:center;
            font-family:'Segoe UI',sans-serif;
        ">
            <div style="color:#94a3b8;font-size:11px;text-transform:uppercase;font-weight:600;">
                Haftalik Aktif
            </div>
            <div style="color:#f59e0b;font-size:28px;font-weight:800;margin-top:4px;">
                {active_weekly}
            </div>
        </div>
    </div>
    """)

    # Modul kullanim dagilimi
    module_counts: dict[str, int] = {}
    for a in activities:
        mod = a.get("module", "diger")
        module_counts[mod] = module_counts.get(mod, 0) + 1

    total_actions = max(sum(module_counts.values()), 1)
    module_colors = {
        "matematik": "#6366f1",
        "sanat": "#f59e0b",
        "bilisim": "#22c55e",
        "genel": "#94a3b8",
    }

    bars_html = ""
    for mod, count in sorted(module_counts.items(), key=lambda x: x[1], reverse=True)[:6]:
        pct = int(count / total_actions * 100)
        color = module_colors.get(mod, "#64748b")
        mod_display = mod.capitalize() if mod else "Diger"
        bars_html += f"""
        <div style="margin-bottom:8px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:2px;">
                <span style="color:#e2e8f0;font-size:12px;font-weight:600;">{mod_display}</span>
                <span style="color:#94a3b8;font-size:11px;">{count} islem ({pct}%)</span>
            </div>
            <div style="background:#0f172a;border-radius:4px;height:10px;overflow:hidden;">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:4px;"></div>
            </div>
        </div>
        """

    if bars_html:
        _render_html(f"""
        <div style="
            background:#1e293b;
            border:1px solid #1e3a5f;
            border-radius:10px;
            padding:16px;
            margin-bottom:16px;
            font-family:'Segoe UI',sans-serif;
        ">
            <div style="color:#e2e8f0;font-size:14px;font-weight:700;margin-bottom:12px;">
                Modul Kullanim Dagilimi
            </div>
            {bars_html}
        </div>
        """)

    # Top 10 ogrenci
    sorted_profiles = sorted(profiles, key=lambda p: p.get("total_xp", 0), reverse=True)[:10]
    if sorted_profiles:
        rows_html = ""
        for i, p in enumerate(sorted_profiles, start=1):
            name = p.get("display_name", p.get("user_id", ""))
            xp = p.get("total_xp", 0)
            lvl = p.get("level", 1)
            xp_fmt = f"{xp:,}".replace(",", ".")
            bg = "#1a2744" if i <= 3 else ("#162032" if i % 2 == 0 else "#0f172a")
            rows_html += f"""
            <tr style="background:{bg};">
                <td style="padding:6px 10px;color:#f59e0b;font-weight:700;text-align:center;">{i}</td>
                <td style="padding:6px 10px;color:#e2e8f0;font-weight:600;">{name}</td>
                <td style="padding:6px 10px;color:#6366f1;font-weight:700;text-align:right;">{xp_fmt} XP</td>
                <td style="padding:6px 10px;color:#94a3b8;text-align:center;">Lv.{lvl}</td>
            </tr>
            """

        _render_html(f"""
        <div style="margin-bottom:16px;">
            <div style="color:#e2e8f0;font-size:14px;font-weight:700;margin-bottom:8px;">
                En Iyi 10 Ogrenci
            </div>
            <table style="width:100%;border-collapse:collapse;border:1px solid #1e3a5f;
                border-radius:10px;overflow:hidden;font-family:'Segoe UI',sans-serif;">
                <thead>
                    <tr style="background:#0f3460;">
                        <th style="padding:8px 10px;color:#94a3b8;font-size:11px;">Sira</th>
                        <th style="padding:8px 10px;color:#94a3b8;font-size:11px;text-align:left;">Isim</th>
                        <th style="padding:8px 10px;color:#94a3b8;font-size:11px;text-align:right;">XP</th>
                        <th style="padding:8px 10px;color:#94a3b8;font-size:11px;">Seviye</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """)

    # Son 7 gun aktivite trendi
    day_counts: dict[str, int] = {}
    for i in range(7):
        d = (date.today() - timedelta(days=6 - i)).isoformat()
        day_counts[d] = 0
    for a in activities:
        ts = a.get("timestamp", "")[:10]
        if ts in day_counts:
            day_counts[ts] += 1

    max_count = max(day_counts.values()) if day_counts.values() else 1
    max_count = max(max_count, 1)

    trend_bars = ""
    for d, count in day_counts.items():
        h = max(4, int(count / max_count * 80))
        day_label = d[5:]  # MM-DD
        trend_bars += f"""
        <div style="display:flex;flex-direction:column;align-items:center;flex:1;">
            <div style="
                width:24px;
                height:{h}px;
                background:linear-gradient(180deg,#6366f1,#818cf8);
                border-radius:4px 4px 0 0;
                margin-bottom:4px;
            "></div>
            <span style="color:#94a3b8;font-size:9px;">{day_label}</span>
            <span style="color:#e2e8f0;font-size:10px;font-weight:600;">{count}</span>
        </div>
        """

    _render_html(f"""
    <div style="
        background:#1e293b;
        border:1px solid #1e3a5f;
        border-radius:10px;
        padding:16px;
        font-family:'Segoe UI',sans-serif;
    ">
        <div style="color:#e2e8f0;font-size:14px;font-weight:700;margin-bottom:12px;">
            Son 7 Gun Aktivite Trendi
        </div>
        <div style="display:flex;align-items:flex-end;gap:8px;height:100px;">
            {trend_bars}
        </div>
    </div>
    """)


# ---------------------------------------------------------------------------
# Tab B: Sinif Karsilastirma
# ---------------------------------------------------------------------------

def _render_sinif_karsilastirma() -> None:
    """Sinif bazli karsilastirma tablosu."""
    profiles = _get_gam_profiles()

    # Mevcut siniflar
    grades = sorted({p.get("grade", "") for p in profiles if p.get("grade")})
    if not grades:
        st.info("Henuz sinif bilgisi olan profil bulunamadi.")
        return

    selected_grade = st.selectbox(
        "Sinif Filtresi",
        options=["Tum Siniflar"] + grades,
        key="okul_dash_sinif_filter",
    )

    # Sinif bazli istatistikler
    sinif_data: dict[str, dict[str, Any]] = {}
    for p in profiles:
        grade = p.get("grade", "")
        if not grade:
            continue
        if selected_grade != "Tum Siniflar" and grade != selected_grade:
            continue

        sube = p.get("sube", "")
        sinif_key = f"{grade}/{sube}" if sube else grade

        if sinif_key not in sinif_data:
            sinif_data[sinif_key] = {
                "toplam": 0,
                "toplam_xp": 0,
                "en_yuksek_xp": 0,
                "en_iyi": "",
            }
        sd = sinif_data[sinif_key]
        sd["toplam"] += 1
        xp = p.get("total_xp", 0)
        sd["toplam_xp"] += xp
        if xp > sd["en_yuksek_xp"]:
            sd["en_yuksek_xp"] = xp
            sd["en_iyi"] = p.get("display_name", p.get("user_id", ""))

    if not sinif_data:
        st.info("Secilen filtreye uygun veri bulunamadi.")
        return

    rows_html = ""
    for sinif_key in sorted(sinif_data.keys()):
        sd = sinif_data[sinif_key]
        ort_xp = sd["toplam_xp"] // max(sd["toplam"], 1)
        ort_xp_fmt = f"{ort_xp:,}".replace(",", ".")
        en_yuksek_fmt = f"{sd['en_yuksek_xp']:,}".replace(",", ".")

        rows_html += f"""
        <tr style="background:#162032;border-bottom:1px solid #1e293b;">
            <td style="padding:10px 14px;color:#e2e8f0;font-weight:700;">{sinif_key}</td>
            <td style="padding:10px 14px;color:#94a3b8;text-align:center;">{sd['toplam']}</td>
            <td style="padding:10px 14px;color:#6366f1;font-weight:700;text-align:right;">{ort_xp_fmt}</td>
            <td style="padding:10px 14px;color:#f59e0b;font-weight:600;text-align:right;">{en_yuksek_fmt}</td>
            <td style="padding:10px 14px;color:#e2e8f0;">{sd['en_iyi']}</td>
        </tr>
        """

    _render_html(f"""
    <div style="overflow-x:auto;">
    <table style="
        width:100%;
        border-collapse:collapse;
        border:1px solid #1e3a5f;
        border-radius:10px;
        overflow:hidden;
        font-family:'Segoe UI',sans-serif;
    ">
        <thead>
            <tr style="background:#0f3460;">
                <th style="padding:10px 14px;color:#94a3b8;font-size:11px;text-align:left;">Sinif</th>
                <th style="padding:10px 14px;color:#94a3b8;font-size:11px;">Ogrenci Sayisi</th>
                <th style="padding:10px 14px;color:#94a3b8;font-size:11px;text-align:right;">Ort. XP</th>
                <th style="padding:10px 14px;color:#94a3b8;font-size:11px;text-align:right;">En Yuksek XP</th>
                <th style="padding:10px 14px;color:#94a3b8;font-size:11px;text-align:left;">En Iyi Ogrenci</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    </div>
    """)


# ---------------------------------------------------------------------------
# Tab C: MEB Rapor
# ---------------------------------------------------------------------------

def _render_meb_rapor() -> None:
    """MEB uyumlu ozet rapor uretimi."""
    profiles = _get_gam_profiles()
    activities = _get_activity_log()
    students = _get_students()

    total_students = len(students) if students else len(profiles)
    today = date.today()
    today_str = today.strftime("%d.%m.%Y")

    # Modul bazli islem sayilari
    module_counts: dict[str, int] = {}
    for a in activities:
        mod = a.get("module", "diger")
        module_counts[mod] = module_counts.get(mod, 0) + 1

    # Kazanim ozeti (profil bazli ortalama XP)
    total_xp = sum(p.get("total_xp", 0) for p in profiles)
    avg_xp = total_xp // max(len(profiles), 1) if profiles else 0

    # Rapor metni
    rapor_lines = [
        "=" * 60,
        "MILLI EGITIM BAKANLIGI - DIJITAL EGITIM RAPORU",
        "=" * 60,
        f"Rapor Tarihi: {today_str}",
        f"Kurum: SmartCampus AI Egitim Platformu",
        "",
        "1. GENEL BILGILER",
        "-" * 40,
        f"   Toplam Ogrenci Sayisi: {total_students}",
        f"   Aktif Profil Sayisi:   {len(profiles)}",
        f"   Toplam Etkilesim:      {sum(module_counts.values())}",
        f"   Ortalama XP:           {avg_xp}",
        "",
        "2. MODUL BAZLI KULLANIM",
        "-" * 40,
    ]

    for mod, count in sorted(module_counts.items(), key=lambda x: x[1], reverse=True):
        mod_display = mod.capitalize() if mod else "Diger"
        rapor_lines.append(f"   {mod_display:.<30} {count:>6} islem")

    rapor_lines += [
        "",
        "3. OGRENME CIKTILARI",
        "-" * 40,
        f"   Ortalama seviye:       {sum(p.get('level', 1) for p in profiles) / max(len(profiles), 1):.1f}",
        f"   Toplam kazanilan rozet: {sum(len(p.get('badges_earned', [])) for p in profiles)}",
        "",
        "=" * 60,
        f"Rapor otomatik olarak {today_str} tarihinde olusturulmustur.",
        "SmartCampus AI Egitim Yonetim Platformu",
        "=" * 60,
    ]

    rapor_text = "\n".join(rapor_lines)

    _render_html(f"""
    <div style="
        background:#0f172a;
        border:1px solid #1e3a5f;
        border-radius:10px;
        padding:20px;
        font-family:'Courier New',monospace;
        color:#e2e8f0;
        font-size:12px;
        white-space:pre-wrap;
        max-height:500px;
        overflow-y:auto;
        margin-bottom:16px;
    ">{rapor_text}</div>
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="TXT olarak indir",
            data=rapor_text,
            file_name=f"meb_rapor_{today.isoformat()}.txt",
            mime="text/plain",
            key="meb_rapor_txt_dl",
        )

    with col2:
        # CSV ozet
        csv_buf = io.StringIO()
        writer = csv.writer(csv_buf)
        writer.writerow(["Modul", "Islem Sayisi"])
        for mod, count in sorted(module_counts.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([mod.capitalize() if mod else "Diger", count])
        writer.writerow([])
        writer.writerow(["Metrik", "Deger"])
        writer.writerow(["Toplam Ogrenci", total_students])
        writer.writerow(["Aktif Profil", len(profiles)])
        writer.writerow(["Ortalama XP", avg_xp])

        st.download_button(
            label="CSV olarak indir",
            data=csv_buf.getvalue(),
            file_name=f"meb_rapor_{today.isoformat()}.csv",
            mime="text/csv",
            key="meb_rapor_csv_dl",
        )


# ---------------------------------------------------------------------------
# Tab D: Veri Disa Aktarma
# ---------------------------------------------------------------------------

def _render_veri_export() -> None:
    """CSV veri disa aktarma: aktiviteler, profiller, odevler."""
    st.markdown(
        '<div style="color:#e2e8f0;font-size:14px;font-weight:700;margin-bottom:12px;">'
        'Veri Disa Aktarma</div>',
        unsafe_allow_html=True,
    )

    # Tarih araligi
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Baslangic Tarihi",
            value=date.today() - timedelta(days=30),
            key="export_start_date",
        )
    with col2:
        end_date = st.date_input(
            "Bitis Tarihi",
            value=date.today(),
            key="export_end_date",
        )

    st.markdown("---")

    # 1) Aktivite logu export
    st.markdown(
        '<div style="color:#6366f1;font-size:13px;font-weight:700;margin-bottom:8px;">'
        'Aktivite Kayitlari</div>',
        unsafe_allow_html=True,
    )
    activities = _get_activity_log()
    start_str = start_date.isoformat() if start_date else ""
    end_str = end_date.isoformat() if end_date else ""

    filtered = [
        a for a in activities
        if start_str <= a.get("timestamp", "")[:10] <= end_str
    ]

    st.markdown(f"Toplam {len(filtered)} kayit ({start_str} - {end_str})")

    if filtered:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["user_id", "action", "module", "xp", "timestamp"])
        for a in filtered:
            writer.writerow([
                a.get("user_id", ""),
                a.get("action", ""),
                a.get("module", ""),
                a.get("xp", 0),
                a.get("timestamp", ""),
            ])
        st.download_button(
            label="Aktiviteleri Indir (CSV)",
            data=buf.getvalue(),
            file_name=f"aktiviteler_{start_str}_{end_str}.csv",
            mime="text/csv",
            key="export_activities_csv",
        )

    st.markdown("---")

    # 2) Gamification profilleri export
    st.markdown(
        '<div style="color:#6366f1;font-size:13px;font-weight:700;margin-bottom:8px;">'
        'Gamification Profilleri</div>',
        unsafe_allow_html=True,
    )
    profiles = _get_gam_profiles()
    st.markdown(f"Toplam {len(profiles)} profil")

    if profiles:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow([
            "user_id", "display_name", "grade", "sube",
            "total_xp", "level", "level_name",
            "streak_days", "best_streak", "badge_count",
            "weekly_xp", "monthly_xp",
        ])
        for p in profiles:
            writer.writerow([
                p.get("user_id", ""),
                p.get("display_name", ""),
                p.get("grade", ""),
                p.get("sube", ""),
                p.get("total_xp", 0),
                p.get("level", 1),
                p.get("level_name", ""),
                p.get("streak_days", 0),
                p.get("best_streak", 0),
                len(p.get("badges_earned", [])),
                p.get("weekly_xp", 0),
                p.get("monthly_xp", 0),
            ])
        st.download_button(
            label="Profilleri Indir (CSV)",
            data=buf.getvalue(),
            file_name="gamification_profiller.csv",
            mime="text/csv",
            key="export_profiles_csv",
        )

    st.markdown("---")

    # 3) Odev tamamlanma export
    st.markdown(
        '<div style="color:#6366f1;font-size:13px;font-weight:700;margin-bottom:8px;">'
        'Odev Tamamlanma Kayitlari</div>',
        unsafe_allow_html=True,
    )

    # Odev verisi yukle
    try:
        from utils.tenant import get_data_path
        akd_base = get_data_path("akademik")
    except Exception:
        akd_base = os.path.join("data", "akademik")

    odevler_path = os.path.join(akd_base, "odevler.json")
    teslimler_path = os.path.join(akd_base, "odev_teslimler.json")
    odevler = _load_json(odevler_path)
    teslimler = _load_json(teslimler_path)

    total_odev = len(odevler)
    total_teslim = len(teslimler)
    st.markdown(f"{total_odev} odev, {total_teslim} teslim kaydi")

    if teslimler:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["odev_id", "ogrenci_id", "teslim_tarihi", "puan", "durum"])
        for t in teslimler:
            writer.writerow([
                t.get("odev_id", ""),
                t.get("ogrenci_id", ""),
                t.get("teslim_tarihi", ""),
                t.get("puan", ""),
                t.get("durum", ""),
            ])
        st.download_button(
            label="Odev Teslimlerini Indir (CSV)",
            data=buf.getvalue(),
            file_name="odev_teslimler.csv",
            mime="text/csv",
            key="export_odev_csv",
        )
    elif odevler:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["odev_id", "baslik", "ders", "sinif", "son_tarih"])
        for o in odevler:
            writer.writerow([
                o.get("id", ""),
                o.get("baslik", ""),
                o.get("ders", ""),
                o.get("sinif", ""),
                o.get("son_tarih", ""),
            ])
        st.download_button(
            label="Odev Listesini Indir (CSV)",
            data=buf.getvalue(),
            file_name="odevler.csv",
            mime="text/csv",
            key="export_odevler_csv",
        )
    else:
        st.info("Henuz odev verisi bulunamadi.")
