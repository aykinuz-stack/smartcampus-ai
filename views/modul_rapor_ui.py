"""
Modul Rapor UI -- Ogretmen, Veli, Ogrenci icin rapor arayuzu.
=============================================================
CSS-only grafikler: conic-gradient pasta, div bar chart, trend.
"""
from __future__ import annotations

import io
import streamlit as st
from datetime import date, timedelta

from utils.ui_common import styled_header, styled_section, _render_html
from models.modul_rapor import (
    get_modul_rapor_store,
    ModulRaporStore,
    MODUL_ADLARI,
    MODUL_RENKLERI,
)


# ══════════════════════════════════════════════════════════════════════════════
# CSS TEMA
# ══════════════════════════════════════════════════════════════════════════════

_CSS_INJECTED_KEY = "_modul_rapor_css_injected"


def _inject_rapor_css():
    """Dark-theme CSS (tek sefer enjekte)."""
    if st.session_state.get(_CSS_INJECTED_KEY):
        return
    _render_html("""
    <style>
    .mr-stat-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 16px; padding: 18px; text-align: center;
        border: 1px solid rgba(99,102,241,0.15);
    }
    .mr-stat-val {
        font-size: 2rem; font-weight: 800; color: #818cf8 !important; line-height: 1.1;
    }
    .mr-stat-lbl {
        font-size: 0.8rem; color: #94a3b8 !important; margin-top: 4px;
    }
    .mr-profil {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 18px; padding: 22px; margin-bottom: 16px;
        border: 1px solid rgba(99,102,241,0.15);
    }
    .mr-profil-name {
        font-size: 1.3rem; font-weight: 700; color: #e2e8f0 !important;
    }
    .mr-profil-sub {
        font-size: 0.85rem; color: #94a3b8 !important; margin-top: 2px;
    }
    .mr-konu-row {
        display: flex; align-items: center; padding: 8px 12px; margin-bottom: 6px;
        background: #0f172a; border-radius: 10px; border: 1px solid #1e293b;
    }
    .mr-konu-label {
        min-width: 140px; font-size: 0.85rem; color: #e2e8f0 !important; font-weight: 600;
    }
    .mr-konu-bar-bg {
        flex: 1; height: 22px; background: #1e293b; border-radius: 8px; overflow: hidden; position: relative;
    }
    .mr-konu-bar-fill {
        height: 100%; border-radius: 8px; transition: width 0.5s ease;
    }
    .mr-konu-bar-txt {
        position: absolute; right: 8px; top: 2px; font-size: 0.75rem; color: #e2e8f0 !important; font-weight: 700;
    }
    .mr-card-guclu {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border-radius: 12px; padding: 14px; margin-bottom: 8px;
        border: 1px solid rgba(16,185,129,0.3);
    }
    .mr-card-zayif {
        background: linear-gradient(135deg, #7c2d12, #9a3412);
        border-radius: 12px; padding: 14px; margin-bottom: 8px;
        border: 1px solid rgba(249,115,22,0.3);
    }
    .mr-ai-box {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 14px; padding: 18px; margin-top: 12px;
        border: 1px solid rgba(99,102,241,0.2);
    }
    .mr-trend-row {
        display: flex; align-items: center; margin-bottom: 4px;
    }
    .mr-trend-date {
        min-width: 80px; font-size: 0.75rem; color: #94a3b8 !important;
    }
    .mr-trend-bar {
        height: 16px; border-radius: 6px; transition: width 0.4s;
    }
    .mr-trend-cnt {
        font-size: 0.7rem; color: #e2e8f0 !important; margin-left: 6px;
    }
    </style>
    """)
    st.session_state[_CSS_INJECTED_KEY] = True


# ══════════════════════════════════════════════════════════════════════════════
# CSS GRAFIK YARDIMCILARI
# ══════════════════════════════════════════════════════════════════════════════

def _css_pie_chart(data: dict, renk_map: dict | None = None, size: int = 180) -> str:
    """conic-gradient CSS pie chart HTML dondur. data = {label: count}."""
    toplam = sum(data.values())
    if toplam == 0:
        return '<div style="color:#94a3b8;text-align:center;padding:20px">Veri yok</div>'

    default_colors = ["#818cf8", "#a78bfa", "#0ea5e9", "#10b981", "#f59e0b", "#ef4444", "#ec4899"]
    segments = []
    cumulative = 0
    legend_items = []

    for idx, (label, count) in enumerate(data.items()):
        if renk_map and label in renk_map:
            color = renk_map[label]
        else:
            color = default_colors[idx % len(default_colors)]
        pct = (count / toplam) * 100 if toplam else 0
        start = cumulative
        cumulative += pct
        segments.append(f"{color} {start:.1f}% {cumulative:.1f}%")
        legend_items.append(
            f'<div style="display:flex;align-items:center;margin:3px 0">'
            f'<div style="width:12px;height:12px;border-radius:3px;background:{color};margin-right:6px"></div>'
            f'<span style="font-size:0.8rem;color:#e2e8f0">{label}: {count} (%{pct:.0f})</span></div>'
        )

    gradient = ", ".join(segments) if segments else "#1e293b 0% 100%"
    legend_html = "".join(legend_items)

    return f"""
    <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap">
        <div style="width:{size}px;height:{size}px;border-radius:50%;
                     background:conic-gradient({gradient});
                     box-shadow:0 4px 20px rgba(0,0,0,0.3);flex-shrink:0"></div>
        <div>{legend_html}</div>
    </div>
    """


def _css_bar_chart(items: list[dict], label_key: str = "konu", value_key: str = "ort_puan", max_val: float = 100) -> str:
    """CSS div bar chart HTML. items = [{konu, ort_puan, ...}]."""
    if not items:
        return '<div style="color:#94a3b8;padding:10px">Veri yok</div>'

    rows = []
    for item in items:
        label = item.get(label_key, "")
        val = item.get(value_key, 0)
        pct = min((val / max_val) * 100, 100) if max_val else 0
        if val >= 70:
            color = "#10b981"
        elif val >= 50:
            color = "#f59e0b"
        else:
            color = "#ef4444"
        rows.append(f"""
        <div class="mr-konu-row">
            <div class="mr-konu-label">{label}</div>
            <div class="mr-konu-bar-bg">
                <div class="mr-konu-bar-fill" style="width:{pct:.1f}%;background:{color}"></div>
                <div class="mr-konu-bar-txt">{val}</div>
            </div>
        </div>
        """)
    return "".join(rows)


def _css_trend_chart(trend: list[dict], max_count: int = 0) -> str:
    """CSS horizontal bar trend chart."""
    if not trend:
        return '<div style="color:#94a3b8;padding:10px">Son 30 gun icin veri yok</div>'

    if max_count == 0:
        max_count = max((t.get("aktivite_sayisi", 1) for t in trend), default=1)
    if max_count == 0:
        max_count = 1

    rows = []
    for t in trend:
        tarih = t.get("tarih", "")[-5:]  # MM-DD
        cnt = t.get("aktivite_sayisi", 0)
        ort = t.get("ort_puan", 0)
        pct = min((cnt / max_count) * 100, 100)
        if ort >= 70:
            color = "#10b981"
        elif ort >= 50:
            color = "#f59e0b"
        else:
            color = "#818cf8"
        rows.append(f"""
        <div class="mr-trend-row">
            <div class="mr-trend-date">{tarih}</div>
            <div style="flex:1;height:16px;background:#1e293b;border-radius:6px;overflow:hidden">
                <div class="mr-trend-bar" style="width:{pct:.1f}%;background:{color}"></div>
            </div>
            <div class="mr-trend-cnt">{cnt} ak / {ort} puan</div>
        </div>
        """)
    return "".join(rows)


def _stat_cards_html(cards: list[tuple[str, str]]) -> str:
    """4-lu stat kart HTML. cards = [(deger, etiket), ...]."""
    cols_html = ""
    for val, lbl in cards:
        cols_html += f"""
        <div style="flex:1;min-width:120px">
            <div class="mr-stat-card">
                <div class="mr-stat-val">{val}</div>
                <div class="mr-stat-lbl">{lbl}</div>
            </div>
        </div>
        """
    return f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px">{cols_html}</div>'


# ══════════════════════════════════════════════════════════════════════════════
# PDF RAPOR URETICI
# ══════════════════════════════════════════════════════════════════════════════

def _generate_pdf_text(ogrenci_adi: str, rapor: dict) -> str:
    """Indirilebilir metin raporu olustur."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"  MODUL RAPORU - {ogrenci_adi}")
    lines.append(f"  Tarih: {date.today().isoformat()}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Toplam Aktivite: {rapor.get('toplam_aktivite', 0)}")
    lines.append(f"Toplam Sure: {rapor.get('toplam_sure_dk', 0)} dk")
    lines.append(f"Ortalama Puan: {rapor.get('ortalama_puan', 0)}")
    lines.append("")

    lines.append("--- MODUL DAGILIMI ---")
    for m, cnt in rapor.get("modul_dagilimi", {}).items():
        lines.append(f"  {MODUL_ADLARI.get(m, m)}: {cnt} aktivite")
    lines.append("")

    lines.append("--- KONU BAZLI PERFORMANS ---")
    for k in rapor.get("konu_bazli", []):
        lines.append(f"  {k['konu']}: {k['ort_puan']} puan ({k['aktivite_sayisi']} aktivite, {k['toplam_sure']} dk)")
    lines.append("")

    guclu = rapor.get("guclu_konular", [])
    if guclu:
        lines.append("--- GUCLU KONULAR ---")
        for k in guclu:
            lines.append(f"  + {k['konu']}: {k['ort_puan']} puan")
        lines.append("")

    zayif = rapor.get("zayif_konular", [])
    if zayif:
        lines.append("--- GELISTIRILMESI GEREKEN KONULAR ---")
        for k in zayif:
            lines.append(f"  - {k['konu']}: {k['ort_puan']} puan")
        lines.append("")

    lines.append("--- AI ANALIZ ---")
    lines.append(rapor.get("ai_analiz", ""))
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# OGRENCI DETAY RENDER (paylasilan)
# ══════════════════════════════════════════════════════════════════════════════

def _render_ogrenci_detay(store: ModulRaporStore, ogrenci_id: str, ogrenci_adi: str,
                          sinif: str = "", modul_filter: str | None = None,
                          key_prefix: str = "mrd"):
    """Tek ogrenci detay raporu — profil, pie, bar, trend, guclu/zayif, AI, PDF."""

    modul_arg = modul_filter if modul_filter and modul_filter != "tumu" else None
    rapor = store.get_ogrenci_raporu(ogrenci_id, modul=modul_arg)

    # Profil karti
    _render_html(f"""
    <div class="mr-profil">
        <div class="mr-profil-name">{ogrenci_adi}</div>
        <div class="mr-profil-sub">Sinif: {sinif} | Toplam: {rapor['toplam_aktivite']} aktivite | Ortalama: {rapor['ortalama_puan']} puan</div>
    </div>
    """)

    if rapor["toplam_aktivite"] == 0:
        _render_html('<div style="color:#94a3b8;padding:20px;text-align:center">Henuz aktivite verisi bulunmuyor.</div>')
        return

    # Stat kartlari
    _render_html(_stat_cards_html([
        (str(rapor["toplam_aktivite"]), "Toplam Aktivite"),
        (f"{rapor['toplam_sure_dk']} dk", "Toplam Sure"),
        (str(rapor["ortalama_puan"]), "Ort. Puan"),
        (str(len(rapor.get("guclu_konular", []))), "Guclu Konu"),
    ]))

    # Pasta grafik: modul dagilimi
    styled_section("Modul Dagilimi", "#818cf8")
    pie_data = {}
    for m, cnt in rapor["modul_dagilimi"].items():
        if cnt > 0:
            pie_data[MODUL_ADLARI.get(m, m)] = cnt
    if pie_data:
        _render_html(_css_pie_chart(pie_data, renk_map={
            "Matematik Koyu": "#818cf8",
            "Sanat Sokagi": "#a78bfa",
            "Bilisim Vadisi": "#0ea5e9",
        }))
    else:
        _render_html('<div style="color:#94a3b8;padding:10px">Tek modul aktif</div>')

    # Bar chart: konu bazli puanlar
    if rapor["konu_bazli"]:
        styled_section("Konu Bazli Performans", "#3b82f6")
        _render_html(_css_bar_chart(rapor["konu_bazli"][:15]))

    # Gunluk trend
    if rapor["gunluk_trend"]:
        styled_section("Son 30 Gun Aktivite Trendi", "#10b981")
        _render_html(_css_trend_chart(rapor["gunluk_trend"]))

    # Guclu konular
    guclu = rapor.get("guclu_konular", [])
    zayif = rapor.get("zayif_konular", [])

    if guclu or zayif:
        c1, c2 = st.columns(2)
        with c1:
            styled_section("Guclu Konular", "#10b981")
            for k in guclu:
                _render_html(f"""
                <div class="mr-card-guclu">
                    <div style="font-weight:700;color:#a7f3d0 !important;font-size:0.9rem">{k['konu']}</div>
                    <div style="font-size:0.8rem;color:#6ee7b7 !important">{k['ort_puan']} puan | {k['aktivite_sayisi']} aktivite</div>
                </div>
                """)
        with c2:
            styled_section("Gelistirilmesi Gereken", "#f59e0b")
            if zayif:
                for k in zayif:
                    _render_html(f"""
                    <div class="mr-card-zayif">
                        <div style="font-weight:700;color:#fed7aa !important;font-size:0.9rem">{k['konu']}</div>
                        <div style="font-size:0.8rem;color:#fdba74 !important">{k['ort_puan']} puan | {k['aktivite_sayisi']} aktivite</div>
                    </div>
                    """)
            else:
                _render_html('<div style="color:#94a3b8;padding:10px">Tum konularda basarili!</div>')

    # AI Analiz
    styled_section("AI Analiz Raporu", "#6366f1")
    _render_html(f"""
    <div class="mr-ai-box">
        <div style="font-size:0.9rem;color:#e2e8f0 !important;line-height:1.7">{rapor['ai_analiz']}</div>
    </div>
    """)

    # PDF indir
    pdf_text = _generate_pdf_text(ogrenci_adi, rapor)
    st.download_button(
        label="Raporu Indir (TXT)",
        data=pdf_text.encode("utf-8"),
        file_name=f"modul_rapor_{ogrenci_id}_{date.today().isoformat()}.txt",
        mime="text/plain",
        key=f"{key_prefix}_pdf_dl_{ogrenci_id}",
    )


# ══════════════════════════════════════════════════════════════════════════════
# OGRETMEN RAPOR EKRANI
# ══════════════════════════════════════════════════════════════════════════════

def render_ogretmen_rapor(modul_filter: str | None = None, key_prefix: str = "mr_ogr"):
    """Ogretmen rapor ekrani — sinif secimi, ozet, ogrenci detay.

    modul_filter: None = tum moduller, "matematik" / "sanat" / "bilisim" = tek modul.
    """
    _inject_rapor_css()
    store = get_modul_rapor_store()

    modul_label = MODUL_ADLARI.get(modul_filter, "Tum Moduller") if modul_filter else "Tum Moduller"
    styled_section(f"Ogrenci Raporu - {modul_label}", "#6366f1")

    # Filtreler
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        sinif = st.selectbox("Sinif", [str(i) for i in range(1, 13)], index=4, key=f"{key_prefix}_sinif")
    with fc2:
        sube = st.selectbox("Sube", ["Tumu", "A", "B", "C", "D", "E", "F"], key=f"{key_prefix}_sube")
    with fc3:
        if modul_filter is None:
            modul_sec = st.selectbox("Modul", ["Tumu", "Matematik", "Sanat", "Bilisim"], key=f"{key_prefix}_modul")
            eff_modul = {"Matematik": "matematik", "Sanat": "sanat", "Bilisim": "bilisim"}.get(modul_sec)
        else:
            st.text_input("Modul", value=modul_label, disabled=True, key=f"{key_prefix}_modul_fix")
            eff_modul = modul_filter
    with fc4:
        tarih_sec = st.selectbox("Tarih", ["Son 7 Gun", "Son 30 Gun", "Tum Zamanlar"], index=1, key=f"{key_prefix}_tarih")

    eff_sube = None if sube == "Tumu" else sube
    tarih_bas = None
    tarih_bit = None
    if tarih_sec == "Son 7 Gun":
        tarih_bas = (date.today() - timedelta(days=7)).isoformat()
        tarih_bit = date.today().isoformat()
    elif tarih_sec == "Son 30 Gun":
        tarih_bas = (date.today() - timedelta(days=30)).isoformat()
        tarih_bit = date.today().isoformat()

    # ── SINIF OZETI ─────────────────────────────────────────────────────────
    styled_section("Sinif Ozeti", "#3b82f6")

    sinif_rapor = store.get_sinif_raporu(sinif, sube=eff_sube)

    _render_html(_stat_cards_html([
        (str(sinif_rapor.get("ogrenci_sayisi", 0)), "Toplam Ogrenci"),
        (str(sinif_rapor.get("aktif_ogrenci", 0)), "Aktif Ogrenci"),
        (str(sinif_rapor.get("ort_puan", 0)), "Ortalama Puan"),
        (str(sinif_rapor.get("toplam_aktivite", 0)), "Toplam Aktivite"),
    ]))

    # Modul dagilim pasta grafigi
    modul_dag = sinif_rapor.get("modul_dagilimi", {})
    pie_data = {}
    for m, cnt in modul_dag.items():
        if cnt > 0:
            pie_data[MODUL_ADLARI.get(m, m)] = cnt
    if pie_data:
        _render_html(_css_pie_chart(pie_data, renk_map={
            "Matematik Koyu": "#818cf8",
            "Sanat Sokagi": "#a78bfa",
            "Bilisim Vadisi": "#0ea5e9",
        }))

    # Konu bazli basari tablosu
    konu_dag = sinif_rapor.get("konu_dagilimi", {})
    if konu_dag:
        styled_section("Konu Dagilimi", "#f59e0b")
        tablo_rows = ""
        for konu, cnt in sorted(konu_dag.items(), key=lambda x: x[1], reverse=True)[:20]:
            tablo_rows += f"""
            <tr>
                <td style="padding:6px 12px;color:#e2e8f0;border-bottom:1px solid #1e293b">{konu}</td>
                <td style="padding:6px 12px;color:#818cf8;border-bottom:1px solid #1e293b;text-align:center;font-weight:700">{cnt}</td>
            </tr>
            """
        _render_html(f"""
        <table style="width:100%;border-collapse:collapse;background:#0f172a;border-radius:10px;overflow:hidden;margin-bottom:16px">
            <thead><tr>
                <th style="padding:10px 12px;color:#94a3b8;text-align:left;border-bottom:2px solid #334155;font-size:0.8rem">Konu</th>
                <th style="padding:10px 12px;color:#94a3b8;text-align:center;border-bottom:2px solid #334155;font-size:0.8rem">Aktivite Sayisi</th>
            </tr></thead>
            <tbody>{tablo_rows}</tbody>
        </table>
        """)

    # En basarili ogrenciler
    en_basarili = sinif_rapor.get("en_basarili_ogrenciler", [])
    if en_basarili:
        styled_section("En Basarili Ogrenciler (Top 10)", "#10b981")
        rows_html = ""
        for idx, o in enumerate(en_basarili, 1):
            badge = ["", "&#129351;", "&#129352;", "&#129353;"]
            medal = badge[idx] if idx <= 3 else f"<span style='color:#94a3b8'>{idx}.</span>"
            rows_html += f"""
            <tr>
                <td style="padding:6px 12px;color:#e2e8f0;border-bottom:1px solid #1e293b">{medal}</td>
                <td style="padding:6px 12px;color:#e2e8f0;border-bottom:1px solid #1e293b">{o['ogrenci_adi']}</td>
                <td style="padding:6px 12px;color:#10b981;border-bottom:1px solid #1e293b;text-align:center;font-weight:700">{o['ort_puan']}</td>
                <td style="padding:6px 12px;color:#94a3b8;border-bottom:1px solid #1e293b;text-align:center">{o['aktivite_sayisi']}</td>
            </tr>
            """
        _render_html(f"""
        <table style="width:100%;border-collapse:collapse;background:#0f172a;border-radius:10px;overflow:hidden;margin-bottom:16px">
            <thead><tr>
                <th style="padding:10px 12px;color:#94a3b8;text-align:left;border-bottom:2px solid #334155;font-size:0.8rem;width:40px">#</th>
                <th style="padding:10px 12px;color:#94a3b8;text-align:left;border-bottom:2px solid #334155;font-size:0.8rem">Ogrenci</th>
                <th style="padding:10px 12px;color:#94a3b8;text-align:center;border-bottom:2px solid #334155;font-size:0.8rem">Ort. Puan</th>
                <th style="padding:10px 12px;color:#94a3b8;text-align:center;border-bottom:2px solid #334155;font-size:0.8rem">Aktivite</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        """)

    # ── OGRENCI SEC ─────────────────────────────────────────────────────────
    st.markdown("---")
    styled_section("Ogrenci Detay Raporu", "#a855f7")

    ogrenci_listesi = store.get_sinif_ogrenci_listesi(sinif, sube=eff_sube)

    if not ogrenci_listesi:
        _render_html('<div style="color:#94a3b8;padding:20px;text-align:center">Bu sinifta henuz aktivite verisi bulunan ogrenci yok.</div>')
        return

    ogr_options = {o["ogrenci_id"]: f"{o['ogrenci_adi']} ({o.get('sube', '')} - {o['ort_puan']} puan)" for o in ogrenci_listesi}
    secili_id = st.selectbox(
        "Ogrenci Secin",
        options=list(ogr_options.keys()),
        format_func=lambda x: ogr_options.get(x, x),
        key=f"{key_prefix}_ogr_sec",
    )

    if secili_id:
        secili = next((o for o in ogrenci_listesi if o["ogrenci_id"] == secili_id), None)
        if secili:
            _render_ogrenci_detay(
                store, secili_id, secili["ogrenci_adi"],
                sinif=f"{sinif}/{secili.get('sube', '')}",
                modul_filter=eff_modul,
                key_prefix=f"{key_prefix}_det",
            )


# ══════════════════════════════════════════════════════════════════════════════
# VELI / OGRENCI RAPOR EKRANI
# ══════════════════════════════════════════════════════════════════════════════

def render_veli_ogrenci_rapor(ogrenci_id: str, ogrenci_adi: str, sinif: str = "",
                              modul_filter: str | None = None, key_prefix: str = "mr_veli"):
    """Veli / ogrenci icin modul raporu — tab filtreleme ile.

    modul_filter: None = tab goster, "matematik"/"sanat"/"bilisim" = direkt filtreli.
    """
    _inject_rapor_css()
    store = get_modul_rapor_store()

    if modul_filter:
        # Tek modul — direkt render
        _render_ogrenci_detay(
            store, ogrenci_id, ogrenci_adi,
            sinif=sinif,
            modul_filter=modul_filter,
            key_prefix=f"{key_prefix}_{modul_filter}",
        )
    else:
        # Tab secimli
        t_tumu, t_mat, t_snt, t_blsm = st.tabs([
            "Tumu",
            "Matematik Koyu",
            "Sanat Sokagi",
            "Bilisim Vadisi",
        ])
        with t_tumu:
            _render_ogrenci_detay(store, ogrenci_id, ogrenci_adi, sinif=sinif,
                                  modul_filter=None, key_prefix=f"{key_prefix}_tum")
        with t_mat:
            _render_ogrenci_detay(store, ogrenci_id, ogrenci_adi, sinif=sinif,
                                  modul_filter="matematik", key_prefix=f"{key_prefix}_mat")
        with t_snt:
            _render_ogrenci_detay(store, ogrenci_id, ogrenci_adi, sinif=sinif,
                                  modul_filter="sanat", key_prefix=f"{key_prefix}_snt")
        with t_blsm:
            _render_ogrenci_detay(store, ogrenci_id, ogrenci_adi, sinif=sinif,
                                  modul_filter="bilisim", key_prefix=f"{key_prefix}_blsm")
