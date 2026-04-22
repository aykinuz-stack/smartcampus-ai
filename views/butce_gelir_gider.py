"""
BGG-01 Butce Gelir Gider Modulu - Streamlit UI
================================================
Dashboard, butce planlama, gelir/gider kayit, tahmini vs gerceklesen,
aylik takip, raporlar, ayarlar, Smarti.
"""

from __future__ import annotations

import os
from datetime import datetime, date
from typing import Any

import streamlit as st
from utils.ui_kit import confirm_action
import pandas as pd

from utils.tenant import get_tenant_dir
from models.butce_gelir_gider import (
    ButceKategori, ButcePlan, ButceKalemi,
    GelirKaydi, GiderKaydi, BGGAyar, BGGLog,
    BGGDataStore, ButceAnalizcisi, ButceRaporlayici, DashboardAggregator,
    DONEM_TURLERI, AYLAR_TAKVIM, AYLAR_EGITIM, AY_NUMARALARI,
    ISLEM_TIPLERI, BUTCE_DURUMLARI, KAYIT_DURUMLARI,
    ODEME_YONTEMLERI, FREKANS_TIPLERI,
    GELIR_ANA_KATEGORILERI, GIDER_ANA_KATEGORILERI,
    _now, _today,
)
from utils.auth import AuthManager
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("butce")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("butce",
        "Gelir-gider takibi, butce planlama, fatura yonetimi, mali raporlar",
        [("12", "Ay Plan"), ("AI", "Tahmin"), ("PDF", "Rapor")])
except Exception:
    pass


# ============================================================
# RENK PALETI (Excel referans stili)
# ============================================================

_CLR_BLUE = "#4472C4"
_CLR_ORANGE = "#ED7D31"
_CLR_GOLD = "#FFC000"
_CLR_GRAY = "#A5A5A5"
_CLR_GREEN = "#70AD47"
_CLR_DARK = "#0B0F19"


# ============================================================
# YARDIMCI FONKSIYONLAR
# ============================================================

def _get_bgg_store() -> BGGDataStore:
    base = os.path.join(get_tenant_dir(), "butce")
    store = BGGDataStore(base)
    store.auto_populate_defaults()
    return store


def _format_tutar(tutar: float) -> str:
    """Tutari 1.234.567,89 TL formatina cevir."""
    if tutar == 0:
        return "0,00 TL"
    neg = tutar < 0
    t = abs(tutar)
    tam = int(t)
    krs = round((t - tam) * 100)
    tam_str = f"{tam:,}".replace(",", ".")
    result = f"{tam_str},{str(krs).zfill(2)} TL"
    return f"-{result}" if neg else result


def _durum_badge(durum: str) -> str:
    renk_map = {
        "Taslak": "#94a3b8",
        "Onay Bekliyor": _CLR_GOLD,
        "Onaylandi": _CLR_GREEN,
        "Revize": _CLR_ORANGE,
        "Arsiv": _CLR_GRAY,
        "Beklemede": _CLR_GOLD,
        "Iptal": "#ef4444",
    }
    renk = renk_map.get(durum, _CLR_GRAY)
    return (
        f'<span style="background:{renk};color:#fff;padding:3px 10px;'
        f'border-radius:10px;font-size:11px;font-weight:600;">{durum}</span>'
    )


# ============================================================
# CSS ENJEKSIYONU
# ============================================================

def _inject_bgg_css():
    inject_common_css("bgg")
    st.markdown("""<style>
    :root {
        --bgg-primary: #4472C4;
        --bgg-secondary: #ED7D31;
        --bgg-gold: #FFC000;
        --bgg-gray: #A5A5A5;
        --bgg-green: #70AD47;
        --bgg-dark: #0B0F19;
    }
    .stApp > header { background: transparent !important; }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease; border-left: 4px solid #4472C4;
    }
    div[data-testid="stMetric"]:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    </style>""", unsafe_allow_html=True)


def _get_kategori_secenekleri(store: BGGDataStore, islem_tipi: str) -> list[tuple[str, str]]:
    """(kategori_kodu, kategori_adi) listesi dondurur."""
    kategoriler = store.load_objects("kategoriler")
    return [
        (k.kategori_kodu, f"{k.ikon} {k.kategori_adi}" if k.ikon else k.kategori_adi)
        for k in kategoriler
        if k.islem_tipi == islem_tipi and k.aktif
    ]


# ============================================================
# SEKME 1: DASHBOARD
# ============================================================

def _render_dashboard(store: BGGDataStore):
    styled_header("Bütçe Dashboard", "Gelir-gider ozeti, trendler ve performans", icon="💰")

    agg = DashboardAggregator(store)
    kpi = agg.kpi_hesapla()

    styled_stat_row([
        ("Yıllık Gelir", _format_tutar(kpi["yillik_gelir"]), "info", "💰"),
        ("Yıllık Gider", _format_tutar(kpi["yillik_gider"]), "info", "💳"),
        ("Net Bakiye", _format_tutar(kpi["yillik_net"]), _CLR_GREEN if kpi["yillik_net"] >= 0 else "#ef4444", "📊"),
        ("Gelir Gerceklesme", f"%{kpi['gelir_gerceklesme']:.1f}", _CLR_GOLD, "📈"),
    ])

    # Grafik: Gelir-Gider dagilimi
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        col1, col2 = st.columns(2)

        with col1:
            styled_section("Gelir Dagilimi", _CLR_BLUE)
            if kpi["gelir_dagilim"]:
                labels = list(kpi["gelir_dagilim"].keys())
                values = list(kpi["gelir_dagilim"].values())
                fig = go.Figure(go.Pie(
                    labels=labels, values=values, hole=0.55,
                    marker=dict(colors=SC_COLORS[:len(labels)], line=dict(color="#fff", width=2)),
                    textinfo="label+percent",
                ))
                sc_pie(fig, height=350)
                st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            else:
                st.info("Henuz gelir kaydı yok.")

        with col2:
            styled_section("Gider Dagilimi", _CLR_ORANGE)
            if kpi["gider_dagilim"]:
                labels = list(kpi["gider_dagilim"].keys())
                values = list(kpi["gider_dagilim"].values())
                fig = go.Figure(go.Pie(
                    labels=labels, values=values, hole=0.55,
                    marker=dict(colors=SC_COLORS[:len(labels)], line=dict(color="#fff", width=2)),
                    textinfo="label+percent",
                ))
                sc_pie(fig, height=350)
                st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            else:
                st.info("Henuz gider kaydı yok.")

        # Aylik trend
        styled_section("Aylık Gelir-Gider Trendi")
        raporlayici = ButceRaporlayici(store)
        trend = raporlayici.trend_analizi(12)
        if any(t["gelir"] > 0 or t["gider"] > 0 for t in trend):
            ay_labels = [t["ay"][:3] for t in trend]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=ay_labels, y=[t["gelir"] for t in trend],
                mode="lines+markers", name="Gelir",
                line=dict(color=SC_COLORS[0], width=3),
                marker=dict(size=8),
            ))
            fig.add_trace(go.Scatter(
                x=ay_labels, y=[t["gider"] for t in trend],
                mode="lines+markers", name="Gider",
                line=dict(color=SC_COLORS[3], width=3),
                marker=dict(size=8),
            ))
            fig.add_trace(go.Scatter(
                x=ay_labels, y=[t["net"] for t in trend],
                mode="lines+markers", name="Net",
                line=dict(color=SC_COLORS[1], width=2, dash="dot"),
                marker=dict(size=6),
            ))
            fig.update_layout(
                height=300, margin=dict(t=10, b=30, l=60, r=10),
                legend=dict(orientation="h", y=1.08),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(gridcolor="#1A2035", tickfont_size=9),
                xaxis=dict(gridcolor="#1A2035", tickfont_size=9),
            )
            st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
        else:
            styled_info_banner("Henuz trend verisi bulunmuyor.", "info", "📊")

    except ImportError:
        st.warning("Plotly yuklu degil. Grafikleri gormek için 'pip install plotly' calistirin.")

    # Son islemler
    styled_section("Son İşlemler")
    if kpi["son_islemler"]:
        rows = ""
        for isl in kpi["son_islemler"]:
            tip_renk = _CLR_BLUE if isl["tip"] == "Gelir" else _CLR_ORANGE
            tip_badge = f'<span style="background:{tip_renk};color:#fff;padding:2px 8px;border-radius:8px;font-size:11px;">{isl["tip"]}</span>'
            rows += f"""<tr>
                <td style="padding:8px 12px;">{tip_badge}</td>
                <td style="padding:8px 12px;">{isl['kategori']}</td>
                <td style="padding:8px 12px;font-weight:600;">{_format_tutar(isl['tutar'])}</td>
                <td style="padding:8px 12px;color:#64748b;">{isl['tarih']}</td>
            </tr>"""
        st.markdown(f"""<table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;">
            <thead><tr style="background:linear-gradient(135deg,{_CLR_DARK},{_CLR_BLUE});">
                <th style="padding:10px 12px;color:#fff;text-align:left;">Tip</th>
                <th style="padding:10px 12px;color:#fff;text-align:left;">Kategori</th>
                <th style="padding:10px 12px;color:#fff;text-align:left;">Tutar</th>
                <th style="padding:10px 12px;color:#fff;text-align:left;">Tarih</th>
            </tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)
    else:
        styled_info_banner("Henuz islem kaydı yok.", "info", "📋")


# ============================================================
# SEKME 2: BUTCE PLANLAMA
# ============================================================

def _render_butce_planlama(store: BGGDataStore):
    styled_header("Bütçe Planlama", "Yıllık butce plani olusturma ve kalem girisi")

    sub_tabs = st.tabs(["📋 Plan Listesi", "➕ Yeni Plan", "📝 Kalem Girişi"])

    # --- Plan Listesi ---
    with sub_tabs[0]:
        styled_section("Butce Planlari")
        planlar = store.load_objects("butce_planlari")
        if not planlar:
            styled_info_banner("Henuz butce plani olusturulmadi.", "info", "📋")
        else:
            rows = ""
            for p in planlar:
                if p.donem_turu == "Takvim Yili":
                    donem_str = f"1 Ocak - 31 Aralik {p.yil}"
                else:
                    donem_str = f"1 Eylul {p.yil} - 31 Agustos {p.yil_bitis}"
                rows += f"""<tr>
                    <td style="padding:8px 12px;font-weight:600;">{p.plan_kodu}</td>
                    <td style="padding:8px 12px;">{p.plan_adi}</td>
                    <td style="padding:8px 12px;">{p.donem_turu}</td>
                    <td style="padding:8px 12px;">{donem_str}</td>
                    <td style="padding:8px 12px;">{_durum_badge(p.durum)}</td>
                    <td style="padding:8px 12px;color:{_CLR_BLUE};font-weight:600;">{_format_tutar(p.toplam_tahmini_gelir)}</td>
                    <td style="padding:8px 12px;color:{_CLR_ORANGE};font-weight:600;">{_format_tutar(p.toplam_tahmini_gider)}</td>
                </tr>"""
            st.markdown(f"""<table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;">
                <thead><tr style="background:linear-gradient(135deg,{_CLR_DARK},{_CLR_BLUE});">
                    <th style="padding:10px 12px;color:#fff;text-align:left;">Kod</th>
                    <th style="padding:10px 12px;color:#fff;text-align:left;">Plan Adi</th>
                    <th style="padding:10px 12px;color:#fff;text-align:left;">Donem</th>
                    <th style="padding:10px 12px;color:#fff;text-align:left;">Yil</th>
                    <th style="padding:10px 12px;color:#fff;text-align:left;">Durum</th>
                    <th style="padding:10px 12px;color:#fff;text-align:left;">Tahmini Gelir</th>
                    <th style="padding:10px 12px;color:#fff;text-align:left;">Tahmini Gider</th>
                </tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)

            # Durum guncelleme
            st.markdown("---")
            styled_section("Durum Güncelle")
            plan_secenekleri = {f"{p.plan_kodu} - {p.plan_adi}": p.id for p in planlar}
            secili = st.selectbox("Plan Sec", list(plan_secenekleri.keys()), key="bp_durum_plan")
            if secili:
                yeni_durum = st.selectbox("Yeni Durum", BUTCE_DURUMLARI, key="bp_yeni_durum")
                if st.button("Durumu Güncelle", key="bp_durum_btn"):
                    plan = store.get_by_id("butce_planlari", plan_secenekleri[secili])
                    if plan:
                        plan.durum = yeni_durum
                        plan.updated_at = _now()
                        if yeni_durum == "Onaylandi":
                            user = AuthManager.get_current_user()
                            plan.onaylayan = user.get("name", "")
                            plan.onay_tarihi = _today()
                        store.upsert("butce_planlari", plan)
                        store.log("durum_guncelle", "plan", plan.id, f"Durum: {yeni_durum}")
                        st.success(f"Plan durumu '{yeni_durum}' olarak güncellendi.")
                        st.rerun()

    # --- Yeni Plan ---
    with sub_tabs[1]:
        styled_section("Yeni Butce Plani Oluştur")

        # Donem turu secimi (form disinda - dinamik guncelleme icin)
        donem = st.selectbox("Donem Turu", DONEM_TURLERI, key="bp_donem_turu")

        if donem == "Takvim Yili":
            styled_info_banner(
                "Takvim Yili: 1 Ocak - 31 Aralik (12 ay: Ocak → Aralik)",
                "info", "📅"
            )
        else:
            styled_info_banner(
                "Egitim Yili: 1 Eylul - 31 Agustos (12 ay: Eylul → Agustos)",
                "warning", "🎓"
            )

        with st.form("yeni_plan_form"):
            if donem == "Takvim Yili":
                plan_adi = st.text_input("Plan Adi",
                    placeholder=f"Orn: {date.today().year} Takvim Yili Butcesi")
                yil = st.number_input("Yil", min_value=2020, max_value=2040,
                                      value=date.today().year)
                donem_bilgi = f"1 Ocak {int(yil)} - 31 Aralik {int(yil)}"
            else:
                plan_adi = st.text_input("Plan Adi",
                    placeholder=f"Orn: {date.today().year}-{date.today().year+1} Egitim Yili Butcesi")
                yil = st.number_input("Başlangıç Yili", min_value=2020, max_value=2040,
                                      value=date.today().year)
                donem_bilgi = f"1 Eylul {int(yil)} - 31 Agustos {int(yil)+1}"

            st.markdown(f"**Donem:** {donem_bilgi}")
            aciklama = st.text_area("Açıklama", height=80)

            submitted = st.form_submit_button("Plan Oluştur", use_container_width=True)

        if submitted and plan_adi:
            user = AuthManager.get_current_user()
            yil_int = int(yil)
            yil_bitis_int = yil_int + 1 if donem == "Egitim Yili" else 0
            plan = ButcePlan(
                plan_kodu=store.next_plan_code(),
                plan_adi=plan_adi,
                donem_turu=donem,
                yil=yil_int,
                yil_bitis=yil_bitis_int,
                hazirlayan=user.get("name", ""),
                aciklama=aciklama,
            )
            store.upsert("butce_planlari", plan)
            store.log("plan_olustur", "plan", plan.id, f"Plan oluşturuldu: {plan_adi}")
            st.success(f"Plan oluşturuldu: {plan.plan_kodu} ({donem_bilgi})")
            st.rerun()

    # --- Kalem Girisi ---
    with sub_tabs[2]:
        styled_section("Butce Kalemi Girişi")
        planlar = store.load_objects("butce_planlari")
        if not planlar:
            styled_info_banner("Öncelikle bir butce plani olusturun.", "warning", "⚠️")
            return

        plan_secenekleri = {f"{p.plan_kodu} - {p.plan_adi}": p.id for p in planlar}
        secili_plan = st.selectbox("Butce Plani", list(plan_secenekleri.keys()), key="bk_plan_sec")
        if not secili_plan:
            return

        plan_id = plan_secenekleri[secili_plan]
        plan = store.get_by_id("butce_planlari", plan_id)

        # Ay etiketleri - donem turune gore
        if plan.donem_turu == "Takvim Yili":
            ay_labels = AYLAR_TAKVIM
            styled_info_banner(
                f"Takvim Yili: 1 Ocak - 31 Aralik {plan.yil} (Ocak → Aralik)",
                "info", "📅"
            )
        else:
            ay_labels = AYLAR_EGITIM
            styled_info_banner(
                f"Egitim Yili: 1 Eylul {plan.yil} - 31 Agustos {plan.yil_bitis} (Eylul → Agustos)",
                "warning", "🎓"
            )

        # Islem tipi secimi
        islem_tipi = st.radio("İşlem Tipi", ISLEM_TIPLERI, horizontal=True, key="bk_islem_tipi")

        # Mevcut kalemler
        kalemler = [k for k in store.find_by_field("butce_kalemleri", "plan_id", plan_id)
                    if k.islem_tipi == islem_tipi]

        # Yeni kalem ekleme
        with st.expander("Yeni Kalem Ekle", expanded=not kalemler):
            secenekler = _get_kategori_secenekleri(store, islem_tipi)
            if secenekler:
                kat_labels = [s[1] for s in secenekler]
                kat_idx = st.selectbox("Kategori", range(len(kat_labels)),
                                       format_func=lambda i: kat_labels[i], key="bk_kat_sec")
                kat_kod, kat_ad = secenekler[kat_idx]
                kat_ad_clean = kat_ad.split(" ", 1)[-1] if " " in kat_ad else kat_ad

                frekans = st.selectbox("Frekans", FREKANS_TIPLERI, key="bk_frekans")

                st.markdown(f"**12 Aylık Tahmini ({islem_tipi})**")
                ay_degerleri = {}
                cols = st.columns(6)
                for i in range(12):
                    with cols[i % 6]:
                        ay_degerleri[i + 1] = st.number_input(
                            ay_labels[i][:3], min_value=0.0, step=1000.0,
                            key=f"bk_ay_{i+1}", format="%.2f"
                        )

                aciklama = st.text_input("Açıklama", key="bk_aciklama")

                if st.button("Kalem Ekle", key="bk_ekle_btn"):
                    kalem = ButceKalemi(
                        plan_id=plan_id,
                        kategori_kodu=kat_kod,
                        kategori_adi=kat_ad_clean,
                        islem_tipi=islem_tipi,
                        frekans=frekans,
                        aciklama=aciklama,
                    )
                    for idx in range(1, 13):
                        setattr(kalem, f"ay_{str(idx).zfill(2)}", ay_degerleri.get(idx, 0.0))
                    kalem.hesapla_toplam()
                    store.upsert("butce_kalemleri", kalem)
                    store.plan_toplamlari_guncelle(plan_id)
                    store.log("kalem_ekle", "kalem", kalem.id, f"{kat_ad_clean} eklendi")
                    st.success(f"Kalem eklendi: {kat_ad_clean}")
                    st.rerun()

        # Mevcut kalemler tablosu
        if kalemler:
            styled_section(f"Mevcut {islem_tipi} Kalemleri")
            header_cells = "".join(
                f'<th style="padding:6px 8px;color:#fff;text-align:right;font-size:11px;">{ay_labels[i][:3]}</th>'
                for i in range(12)
            )
            rows = ""
            col_toplam = [0.0] * 12
            for k in kalemler:
                satir_vals = []
                for i in range(1, 13):
                    val = getattr(k, f"ay_{str(i).zfill(2)}", 0.0)
                    satir_vals.append(val)
                    col_toplam[i - 1] += val
                cells = "".join(
                    f'<td style="padding:6px 8px;text-align:right;font-size:12px;">{v:,.0f}</td>'
                    for v in satir_vals
                )
                rows += f"""<tr style="border-bottom:1px solid #e2e8f0;">
                    <td style="padding:6px 8px;font-weight:600;font-size:12px;">{k.kategori_adi}</td>
                    {cells}
                    <td style="padding:6px 8px;text-align:right;font-weight:700;color:{_CLR_BLUE if islem_tipi == 'Gelir' else _CLR_ORANGE};font-size:12px;">
                        {k.yillik_toplam:,.0f}</td>
                </tr>"""

            # Toplam satiri
            toplam_cells = "".join(
                f'<td style="padding:6px 8px;text-align:right;font-weight:700;font-size:12px;">{v:,.0f}</td>'
                for v in col_toplam
            )
            genel_toplam = sum(col_toplam)
            rows += f"""<tr style="background:#0B0F19;border-top:2px solid {_CLR_BLUE if islem_tipi == 'Gelir' else _CLR_ORANGE};">
                <td style="padding:6px 8px;font-weight:800;font-size:12px;">TOPLAM</td>
                {toplam_cells}
                <td style="padding:6px 8px;text-align:right;font-weight:800;font-size:13px;color:{_CLR_BLUE if islem_tipi == 'Gelir' else _CLR_ORANGE};">
                    {genel_toplam:,.0f}</td>
            </tr>"""

            st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:8px;overflow:hidden;">
                <thead><tr style="background:linear-gradient(135deg,{_CLR_DARK},{_CLR_BLUE if islem_tipi == 'Gelir' else _CLR_ORANGE});">
                    <th style="padding:6px 8px;color:#fff;text-align:left;font-size:11px;">Kategori</th>
                    {header_cells}
                    <th style="padding:6px 8px;color:#fff;text-align:right;font-size:11px;">Toplam</th>
                </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)

            # Kalem silme
            st.markdown("---")
            kalem_sil_sec = {f"{k.kategori_adi} ({_format_tutar(k.yillik_toplam)})": k.id for k in kalemler}
            sil_secim = st.selectbox("Silinecek Kalem", list(kalem_sil_sec.keys()), key="bk_sil_sec")
            if confirm_action("Kalemi Sil", "Seçili bütçe kalemini silmek istediğinize emin misiniz?", key="bk_sil_btn"):
                store.delete_by_id("butce_kalemleri", kalem_sil_sec[sil_secim])
                store.plan_toplamlari_guncelle(plan_id)
                st.success("Kalem silindi.")
                st.rerun()


# ============================================================
# SEKME 3: GELIR KAYIT
# ============================================================

def _render_gelir_kayit(store: BGGDataStore):
    styled_header("Gelir Kaydı", "Gelir islemlerini kaydedin ve yonetin")

    sub_tabs = st.tabs(["➕ Yeni Gelir", "📋 Gelir Listesi"])

    with sub_tabs[0]:
        styled_section("Yeni Gelir Kaydi", _CLR_BLUE)
        secenekler = _get_kategori_secenekleri(store, "Gelir")
        if not secenekler:
            styled_info_banner("Gelir kategorisi bulunamadı.", "warning", "⚠️")
            return

        with st.form("gelir_form"):
            c1, c2 = st.columns(2)
            with c1:
                kat_labels = [s[1] for s in secenekler]
                kat_idx = st.selectbox("Kategori", range(len(kat_labels)),
                                       format_func=lambda i: kat_labels[i], key="gk_kat")
                tarih = st.date_input("Tarih", value=date.today(), key="gk_tarih")
                tutar = st.number_input("Tutar (TL)", min_value=0.0, step=100.0,
                                        format="%.2f", key="gk_tutar")
            with c2:
                odeme = st.selectbox("Odeme Yontemi", ODEME_YONTEMLERI, key="gk_odeme")
                belge_no = st.text_input("Belge No", key="gk_belge")
                odeme_yapan = st.text_input("Odeme Yapan", key="gk_yapan")

            kdv = st.number_input("KDV Orani (%)", min_value=0.0, max_value=100.0,
                                  value=0.0, step=1.0, key="gk_kdv")
            aciklama = st.text_area("Açıklama", height=60, key="gk_aciklama")

            # Plan baglantisi
            planlar = store.load_objects("butce_planlari")
            plan_opts = ["(Plansiz)"] + [f"{p.plan_kodu} - {p.plan_adi}" for p in planlar]
            plan_sec = st.selectbox("Butce Plani (opsiyonel)", plan_opts, key="gk_plan")

            submitted = st.form_submit_button("Gelir Kaydet", use_container_width=True)

        if submitted and tutar > 0:
            kat_kod, kat_ad = secenekler[kat_idx]
            kat_ad_clean = kat_ad.split(" ", 1)[-1] if " " in kat_ad else kat_ad
            tarih_str = tarih.isoformat()
            ay_no = tarih.month
            ay_adi = list(AY_NUMARALARI.keys())[ay_no - 1]
            kdv_dahil = tutar * (1 + kdv / 100)

            plan_id = ""
            if plan_sec != "(Plansiz)" and planlar:
                idx = plan_opts.index(plan_sec) - 1
                if 0 <= idx < len(planlar):
                    plan_id = planlar[idx].id

            kayit = GelirKaydi(
                kayit_kodu=store.next_gelir_code(),
                plan_id=plan_id,
                kategori_kodu=kat_kod,
                kategori_adi=kat_ad_clean,
                tarih=tarih_str,
                ay=ay_adi,
                yil=tarih.year,
                tutar=tutar,
                kdv_orani=kdv,
                kdv_dahil_tutar=kdv_dahil,
                odeme_yontemi=odeme,
                belge_no=belge_no,
                odeme_yapan=odeme_yapan,
                aciklama=aciklama,
            )
            store.upsert("gelir_kayitlari", kayit)
            store.log("gelir_kayit", "gelir", kayit.id, f"{kat_ad_clean}: {_format_tutar(tutar)}")
            st.success(f"Gelir kaydedildi: {kayit.kayit_kodu} - {_format_tutar(tutar)}")
            st.rerun()

    with sub_tabs[1]:
        styled_section("Gelir Kayıtlari", _CLR_BLUE)
        gelirler = store.load_objects("gelir_kayitlari")
        if not gelirler:
            styled_info_banner("Henuz gelir kaydı yok.", "info", "💰")
            return

        # Filtre
        c1, c2 = st.columns(2)
        with c1:
            yil_filtre = st.selectbox("Yil", sorted(set(g.yil for g in gelirler), reverse=True),
                                      key="gk_yil_f")
        with c2:
            kat_filtre = st.selectbox("Kategori", ["Tümü"] + sorted(set(g.kategori_adi for g in gelirler)),
                                      key="gk_kat_f")

        filtered = [g for g in gelirler if g.yil == yil_filtre]
        if kat_filtre != "Tümü":
            filtered = [g for g in filtered if g.kategori_adi == kat_filtre]

        toplam = sum(g.tutar for g in filtered if g.durum != "Iptal")
        styled_info_banner(f"Toplam: {_format_tutar(toplam)} ({len(filtered)} kayit)", "info", "💰")

        if filtered:
            rows = ""
            for g in sorted(filtered, key=lambda x: x.tarih, reverse=True):
                rows += f"""<tr>
                    <td style="padding:6px 10px;font-weight:600;">{g.kayit_kodu}</td>
                    <td style="padding:6px 10px;">{g.kategori_adi}</td>
                    <td style="padding:6px 10px;">{g.tarih}</td>
                    <td style="padding:6px 10px;font-weight:600;color:{_CLR_BLUE};">{_format_tutar(g.tutar)}</td>
                    <td style="padding:6px 10px;">{g.odeme_yontemi}</td>
                    <td style="padding:6px 10px;">{_durum_badge(g.durum)}</td>
                </tr>"""
            st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;">
                <thead><tr style="background:linear-gradient(135deg,{_CLR_DARK},{_CLR_BLUE});">
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Kod</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Kategori</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Tarih</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Tutar</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Odeme</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Durum</th>
                </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)

            # Silme
            st.markdown("---")
            sil_opts = {f"{g.kayit_kodu} - {g.kategori_adi} ({_format_tutar(g.tutar)})": g.id for g in filtered}
            sil_sec = st.selectbox("Silinecek Kayıt", list(sil_opts.keys()), key="gk_sil_sec")
            if confirm_action("Kaydı Sil", "Seçili gelir kaydını silmek istediğinize emin misiniz?", key="gk_sil_btn"):
                store.delete_by_id("gelir_kayitlari", sil_opts[sil_sec])
                st.success("Gelir kaydı silindi.")
                st.rerun()


# ============================================================
# SEKME 4: GIDER KAYIT
# ============================================================

def _render_gider_kayit(store: BGGDataStore):
    styled_header("Gider Kaydı", "Gider islemlerini kaydedin ve yonetin")

    sub_tabs = st.tabs(["➕ Yeni Gider", "📋 Gider Listesi"])

    with sub_tabs[0]:
        styled_section("Yeni Gider Kaydi", _CLR_ORANGE)
        secenekler = _get_kategori_secenekleri(store, "Gider")
        if not secenekler:
            styled_info_banner("Gider kategorisi bulunamadı.", "warning", "⚠️")
            return

        with st.form("gider_form"):
            c1, c2 = st.columns(2)
            with c1:
                kat_labels = [s[1] for s in secenekler]
                kat_idx = st.selectbox("Kategori", range(len(kat_labels)),
                                       format_func=lambda i: kat_labels[i], key="gc_kat")
                tarih = st.date_input("Tarih", value=date.today(), key="gc_tarih")
                tutar = st.number_input("Tutar (TL)", min_value=0.0, step=100.0,
                                        format="%.2f", key="gc_tutar")
            with c2:
                odeme = st.selectbox("Odeme Yontemi", ODEME_YONTEMLERI, key="gc_odeme")
                fatura = st.text_input("Fatura Tipi", key="gc_fatura")
                tedarikci = st.text_input("Tedarikci Adi", key="gc_tedarikci")

            c3, c4 = st.columns(2)
            with c3:
                belge_no = st.text_input("Belge No", key="gc_belge")
            with c4:
                onaylayan = st.text_input("Onaylayan", key="gc_onaylayan")

            kdv = st.number_input("KDV Orani (%)", min_value=0.0, max_value=100.0,
                                  value=20.0, step=1.0, key="gc_kdv")
            aciklama = st.text_area("Açıklama", height=60, key="gc_aciklama")

            planlar = store.load_objects("butce_planlari")
            plan_opts = ["(Plansiz)"] + [f"{p.plan_kodu} - {p.plan_adi}" for p in planlar]
            plan_sec = st.selectbox("Butce Plani (opsiyonel)", plan_opts, key="gc_plan")

            submitted = st.form_submit_button("Gider Kaydet", use_container_width=True)

        if submitted and tutar > 0:
            kat_kod, kat_ad = secenekler[kat_idx]
            kat_ad_clean = kat_ad.split(" ", 1)[-1] if " " in kat_ad else kat_ad
            tarih_str = tarih.isoformat()
            ay_no = tarih.month
            ay_adi = list(AY_NUMARALARI.keys())[ay_no - 1]
            kdv_dahil = tutar * (1 + kdv / 100)

            plan_id = ""
            if plan_sec != "(Plansiz)" and planlar:
                idx = plan_opts.index(plan_sec) - 1
                if 0 <= idx < len(planlar):
                    plan_id = planlar[idx].id

            kayit = GiderKaydi(
                kayit_kodu=store.next_gider_code(),
                plan_id=plan_id,
                kategori_kodu=kat_kod,
                kategori_adi=kat_ad_clean,
                tarih=tarih_str,
                ay=ay_adi,
                yil=tarih.year,
                tutar=tutar,
                kdv_orani=kdv,
                kdv_dahil_tutar=kdv_dahil,
                odeme_yontemi=odeme,
                belge_no=belge_no,
                fatura_tipi=fatura,
                tedarikci_adi=tedarikci,
                onaylayan=onaylayan,
                aciklama=aciklama,
            )
            store.upsert("gider_kayitlari", kayit)
            store.log("gider_kayit", "gider", kayit.id, f"{kat_ad_clean}: {_format_tutar(tutar)}")
            st.success(f"Gider kaydedildi: {kayit.kayit_kodu} - {_format_tutar(tutar)}")
            st.rerun()

    with sub_tabs[1]:
        styled_section("Gider Kayıtlari", _CLR_ORANGE)
        giderler = store.load_objects("gider_kayitlari")
        if not giderler:
            styled_info_banner("Henuz gider kaydı yok.", "info", "💳")
            return

        c1, c2 = st.columns(2)
        with c1:
            yil_filtre = st.selectbox("Yil", sorted(set(g.yil for g in giderler), reverse=True),
                                      key="gc_yil_f")
        with c2:
            kat_filtre = st.selectbox("Kategori", ["Tümü"] + sorted(set(g.kategori_adi for g in giderler)),
                                      key="gc_kat_f")

        filtered = [g for g in giderler if g.yil == yil_filtre]
        if kat_filtre != "Tümü":
            filtered = [g for g in filtered if g.kategori_adi == kat_filtre]

        toplam = sum(g.tutar for g in filtered if g.durum != "Iptal")
        styled_info_banner(f"Toplam: {_format_tutar(toplam)} ({len(filtered)} kayit)", "info", "💳")

        if filtered:
            rows = ""
            for g in sorted(filtered, key=lambda x: x.tarih, reverse=True):
                rows += f"""<tr>
                    <td style="padding:6px 10px;font-weight:600;">{g.kayit_kodu}</td>
                    <td style="padding:6px 10px;">{g.kategori_adi}</td>
                    <td style="padding:6px 10px;">{g.tarih}</td>
                    <td style="padding:6px 10px;font-weight:600;color:{_CLR_ORANGE};">{_format_tutar(g.tutar)}</td>
                    <td style="padding:6px 10px;">{g.tedarikci_adi}</td>
                    <td style="padding:6px 10px;">{_durum_badge(g.durum)}</td>
                </tr>"""
            st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;">
                <thead><tr style="background:linear-gradient(135deg,{_CLR_DARK},{_CLR_ORANGE});">
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Kod</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Kategori</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Tarih</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Tutar</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Tedarikci</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Durum</th>
                </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)

            st.markdown("---")
            sil_opts = {f"{g.kayit_kodu} - {g.kategori_adi} ({_format_tutar(g.tutar)})": g.id for g in filtered}
            sil_sec = st.selectbox("Silinecek Kayıt", list(sil_opts.keys()), key="gc_sil_sec")
            if confirm_action("Kaydı Sil", "Seçili gider kaydını silmek istediğinize emin misiniz?", key="gc_sil_btn"):
                store.delete_by_id("gider_kayitlari", sil_opts[sil_sec])
                st.success("Gider kaydı silindi.")
                st.rerun()


# ============================================================
# SEKME 5: TAHMINI VS GERCEKLESEN
# ============================================================

def _render_tahmini_gerceklesen(store: BGGDataStore):
    styled_header("Tahmini vs Gerçekleşen", "Butce performans karsilastirmasi")

    planlar = store.load_objects("butce_planlari")
    if not planlar:
        styled_info_banner("Öncelikle bir butce plani olusturun.", "warning", "⚠️")
        return

    plan_secenekleri = {f"{p.plan_kodu} - {p.plan_adi}": p.id for p in planlar}
    secili = st.selectbox("Butce Plani", list(plan_secenekleri.keys()), key="tvg_plan")
    if not secili:
        return

    plan_id = plan_secenekleri[secili]
    plan = store.get_by_id("butce_planlari", plan_id)
    ay_labels = AYLAR_TAKVIM if plan.donem_turu == "Takvim Yili" else AYLAR_EGITIM

    ay_sec = st.selectbox("Ay", ay_labels, key="tvg_ay")

    analizcisi = ButceAnalizcisi(store)
    varyans = analizcisi.aylik_varyans(plan_id, ay_sec, plan.donem_turu)

    if not varyans:
        styled_info_banner("Bu ay için veri bulunamadı.", "info", "📊")
        return

    # Gelir ve gider ayir
    gelir_items = {k: v for k, v in varyans.items() if v["islem_tipi"] == "Gelir"}
    gider_items = {k: v for k, v in varyans.items() if v["islem_tipi"] == "Gider"}

    # Tablo
    def _varyans_tablosu(items: dict, baslik: str, renk: str):
        if not items:
            return
        styled_section(baslik, renk)
        rows = ""
        toplam_t, toplam_g = 0.0, 0.0
        for kod, v in items.items():
            fark = v["fark"]
            fark_pct = v["fark_yuzde"]
            fark_renk = _CLR_GREEN if fark >= 0 else "#ef4444"
            if v["islem_tipi"] == "Gider":
                fark_renk = "#ef4444" if fark > 0 else _CLR_GREEN
            toplam_t += v["tahmini"]
            toplam_g += v["gerceklesen"]
            rows += f"""<tr>
                <td style="padding:6px 10px;">{v['kategori_adi']}</td>
                <td style="padding:6px 10px;text-align:right;">{v['tahmini']:,.0f}</td>
                <td style="padding:6px 10px;text-align:right;">{v['gerceklesen']:,.0f}</td>
                <td style="padding:6px 10px;text-align:right;color:{fark_renk};font-weight:600;">{fark:+,.0f}</td>
                <td style="padding:6px 10px;text-align:right;color:{fark_renk};font-weight:600;">%{fark_pct:+.1f}</td>
            </tr>"""
        # Toplam
        t_fark = toplam_g - toplam_t
        t_pct = (t_fark / toplam_t * 100) if toplam_t else 0
        rows += f"""<tr style="background:#0B0F19;font-weight:700;border-top:2px solid {renk};">
            <td style="padding:6px 10px;">TOPLAM</td>
            <td style="padding:6px 10px;text-align:right;">{toplam_t:,.0f}</td>
            <td style="padding:6px 10px;text-align:right;">{toplam_g:,.0f}</td>
            <td style="padding:6px 10px;text-align:right;">{t_fark:+,.0f}</td>
            <td style="padding:6px 10px;text-align:right;">%{t_pct:+.1f}</td>
        </tr>"""
        st.markdown(f"""<table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;">
            <thead><tr style="background:linear-gradient(135deg,{_CLR_DARK},{renk});">
                <th style="padding:8px 10px;color:#fff;text-align:left;">Kategori</th>
                <th style="padding:8px 10px;color:#fff;text-align:right;">Tahmini</th>
                <th style="padding:8px 10px;color:#fff;text-align:right;">Gerçekleşen</th>
                <th style="padding:8px 10px;color:#fff;text-align:right;">Fark</th>
                <th style="padding:8px 10px;color:#fff;text-align:right;">Fark %</th>
            </tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        _varyans_tablosu(gelir_items, "Gelir Varyans", _CLR_BLUE)
    with col2:
        _varyans_tablosu(gider_items, "Gider Varyans", _CLR_ORANGE)

    # Grafik: Grouped bar
    try:
        import plotly.graph_objects as go
        styled_section("Tahmini vs Gerçekleşen Grafigi")

        all_items = list(varyans.values())
        kategoriler = [v["kategori_adi"] for v in all_items]
        tahmini_vals = [v["tahmini"] for v in all_items]
        gercek_vals = [v["gerceklesen"] for v in all_items]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Tahmini", x=kategoriler, y=tahmini_vals,
                             marker_color=SC_COLORS[0], text=tahmini_vals, textposition="outside"))
        fig.add_trace(go.Bar(name="Gerçekleşen", x=kategoriler, y=gercek_vals,
                             marker_color=SC_COLORS[1], text=gercek_vals, textposition="outside"))
        sc_bar(fig, height=350)
        fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.05),
                          xaxis=dict(tickangle=-45), margin=dict(t=10, b=80, l=60, r=10))
        st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)

        # Gerceklesme orani donut
        ozet = analizcisi.yillik_ozet(plan_id)
        if ozet:
            col1, col2 = st.columns(2)
            with col1:
                styled_section("Gelir Gerceklesme", _CLR_BLUE)
                oran = min(ozet["gelir_gerceklesme"], 100)
                fig_d = go.Figure(go.Pie(
                    values=[oran, 100 - oran],
                    labels=["Gerçekleşen", "Kalan"],
                    hole=0.55,
                    marker=dict(colors=[SC_COLORS[0], "#e2e8f0"], line=dict(color="#fff", width=2)),
                    textinfo="none",
                ))
                sc_pie(fig_d, height=250, center_text=f"<b>%{oran:.1f}</b>")
                st.plotly_chart(fig_d, use_container_width=True, config=SC_CHART_CFG)
            with col2:
                styled_section("Gider Gerceklesme", _CLR_ORANGE)
                oran = min(ozet["gider_gerceklesme"], 100)
                fig_d = go.Figure(go.Pie(
                    values=[oran, 100 - oran],
                    labels=["Gerçekleşen", "Kalan"],
                    hole=0.55,
                    marker=dict(colors=[SC_COLORS[3], "#e2e8f0"], line=dict(color="#fff", width=2)),
                    textinfo="none",
                ))
                sc_pie(fig_d, height=250, center_text=f"<b>%{oran:.1f}</b>")
                st.plotly_chart(fig_d, use_container_width=True, config=SC_CHART_CFG)

    except ImportError:
        pass


# ============================================================
# SEKME 6: AYLIK TAKIP
# ============================================================

def _render_aylik_takip(store: BGGDataStore):
    styled_header("Aylık Takip", "12 aylik gelir-gider tablosu ve trend grafigi")

    yil = st.number_input("Yil", min_value=2020, max_value=2040,
                          value=date.today().year, key="at_yil")

    raporlayici = ButceRaporlayici(store)
    tablo = raporlayici.aylik_gelir_gider_tablosu(int(yil))

    # Gorunum secimi
    gorunum = st.radio("Görünüm", ["Gelir & Gider", "Sadece Gelir", "Sadece Gider"],
                       horizontal=True, key="at_gorunum")

    # 12 aylik tablo
    styled_section("Aylık Özet Tablosu")
    header = '<th style="padding:8px 10px;color:#fff;text-align:left;">Ay</th>'
    if gorunum in ("Gelir & Gider", "Sadece Gelir"):
        header += '<th style="padding:8px 10px;color:#fff;text-align:right;">Gelir</th>'
    if gorunum in ("Gelir & Gider", "Sadece Gider"):
        header += '<th style="padding:8px 10px;color:#fff;text-align:right;">Gider</th>'
    if gorunum == "Gelir & Gider":
        header += '<th style="padding:8px 10px;color:#fff;text-align:right;">Net</th>'

    rows = ""
    toplam_g, toplam_c, toplam_n = 0.0, 0.0, 0.0
    for ay in AYLAR_TAKVIM:
        v = tablo[ay]
        toplam_g += v["gelir"]
        toplam_c += v["gider"]
        toplam_n += v["net"]
        net_renk = _CLR_GREEN if v["net"] >= 0 else "#ef4444"
        cells = ""
        if gorunum in ("Gelir & Gider", "Sadece Gelir"):
            cells += f'<td style="padding:8px 10px;text-align:right;color:{_CLR_BLUE};font-weight:600;">{v["gelir"]:,.0f}</td>'
        if gorunum in ("Gelir & Gider", "Sadece Gider"):
            cells += f'<td style="padding:8px 10px;text-align:right;color:{_CLR_ORANGE};font-weight:600;">{v["gider"]:,.0f}</td>'
        if gorunum == "Gelir & Gider":
            cells += f'<td style="padding:8px 10px;text-align:right;color:{net_renk};font-weight:700;">{v["net"]:+,.0f}</td>'
        rows += f'<tr style="border-bottom:1px solid #e2e8f0;"><td style="padding:8px 10px;font-weight:600;">{ay}</td>{cells}</tr>'

    # Toplam
    net_t_renk = _CLR_GREEN if toplam_n >= 0 else "#ef4444"
    t_cells = ""
    if gorunum in ("Gelir & Gider", "Sadece Gelir"):
        t_cells += f'<td style="padding:8px 10px;text-align:right;font-weight:800;color:{_CLR_BLUE};">{toplam_g:,.0f}</td>'
    if gorunum in ("Gelir & Gider", "Sadece Gider"):
        t_cells += f'<td style="padding:8px 10px;text-align:right;font-weight:800;color:{_CLR_ORANGE};">{toplam_c:,.0f}</td>'
    if gorunum == "Gelir & Gider":
        t_cells += f'<td style="padding:8px 10px;text-align:right;font-weight:800;color:{net_t_renk};">{toplam_n:+,.0f}</td>'
    rows += f'<tr style="background:#0B0F19;border-top:2px solid {_CLR_BLUE};"><td style="padding:8px 10px;font-weight:800;">TOPLAM</td>{t_cells}</tr>'

    st.markdown(f"""<table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;">
        <thead><tr style="background:linear-gradient(135deg,{_CLR_DARK},{_CLR_BLUE});">
            {header}
        </tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)

    # Trend grafigi
    try:
        import plotly.graph_objects as go
        styled_section("Aylık Trend Grafigi")
        ay_labels = [ay[:3] for ay in AYLAR_TAKVIM]
        gelir_vals = [tablo[ay]["gelir"] for ay in AYLAR_TAKVIM]
        gider_vals = [tablo[ay]["gider"] for ay in AYLAR_TAKVIM]
        net_vals = [tablo[ay]["net"] for ay in AYLAR_TAKVIM]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Gelir", x=ay_labels, y=gelir_vals,
                             marker_color=SC_COLORS[0], text=gelir_vals, textposition="outside"))
        fig.add_trace(go.Bar(name="Gider", x=ay_labels, y=gider_vals,
                             marker_color=SC_COLORS[1], text=gider_vals, textposition="outside"))
        fig.add_trace(go.Scatter(name="Net", x=ay_labels, y=net_vals,
                                 mode="lines+markers",
                                 line=dict(color=SC_COLORS[3], width=3),
                                 marker=dict(size=8)))
        sc_bar(fig, height=350)
        fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.08))
        st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
    except ImportError:
        pass


# ============================================================
# SEKME 7: RAPORLAR
# ============================================================

def _render_raporlar(store: BGGDataStore):
    styled_header("Raporlar", "Detayli butce raporlari ve PDF export")

    sub_tabs = st.tabs(["📊 Genel Özet", "💵 Gelir Raporu", "💳 Gider Raporu", "📉 Varyans Raporu"])

    with sub_tabs[0]:
        styled_section("Genel Bütçe Özeti")
        yil = st.number_input("Yil", min_value=2020, max_value=2040,
                              value=date.today().year, key="rp_go_yil")
        raporlayici = ButceRaporlayici(store)
        tablo = raporlayici.aylik_gelir_gider_tablosu(int(yil))

        toplam_gelir = sum(v["gelir"] for v in tablo.values())
        toplam_gider = sum(v["gider"] for v in tablo.values())
        toplam_net = toplam_gelir - toplam_gider

        styled_stat_row([
            ("Toplam Gelir", _format_tutar(toplam_gelir), "info", "💰"),
            ("Toplam Gider", _format_tutar(toplam_gider), "info", "💳"),
            ("Net Bakiye", _format_tutar(toplam_net), _CLR_GREEN if toplam_net >= 0 else "#ef4444", "📊"),
        ])

        try:
            import plotly.graph_objects as go

            # Aylik karsilastirma bar chart
            ay_labels = [ay[:3] for ay in AYLAR_TAKVIM]
            gelir_y = [tablo[ay]["gelir"] for ay in AYLAR_TAKVIM]
            gider_y = [tablo[ay]["gider"] for ay in AYLAR_TAKVIM]
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Gelir", x=ay_labels, y=gelir_y,
                                 marker_color=SC_COLORS[0], text=gelir_y, textposition="outside"))
            fig.add_trace(go.Bar(name="Gider", x=ay_labels, y=gider_y,
                                 marker_color=SC_COLORS[1], text=gider_y, textposition="outside"))
            sc_bar(fig, height=300)
            fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.08))
            st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
        except ImportError:
            pass

        # PDF export
        st.markdown("---")
        if st.button("PDF Rapor Oluştur", key="rp_go_pdf"):
            try:
                from utils.report_utils import ReportPDFGenerator, get_institution_info
                pdf = ReportPDFGenerator(
                    f"Butce Özet Raporu - {yil}",
                    f"Toplam Gelir: {_format_tutar(toplam_gelir)} | Toplam Gider: {_format_tutar(toplam_gider)}"
                )
                info = get_institution_info()
                pdf.add_institution_header(info)
                pdf.add_section_header("Aylık Gelir-Gider Tablosu")
                data_rows = []
                for ay in AYLAR_TAKVIM:
                    v = tablo[ay]
                    data_rows.append([ay, f"{v['gelir']:,.0f}", f"{v['gider']:,.0f}", f"{v['net']:+,.0f}"])
                pdf.add_table(["Ay", "Gelir", "Gider", "Net"], data_rows)
                pdf_bytes = pdf.get_bytes()
                st.download_button(
                    "PDF Indir", data=pdf_bytes,
                    file_name=f"butce_ozet_{yil}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"PDF olusturulamadi: {e}")

    with sub_tabs[1]:
        styled_section("Gelir Raporu", _CLR_BLUE)
        yil = st.number_input("Yil", min_value=2020, max_value=2040,
                              value=date.today().year, key="rp_gr_yil")
        raporlayici = ButceRaporlayici(store)
        dagilim = raporlayici.kategori_dagilimi("Gelir", int(yil))

        if dagilim:
            toplam = sum(d["tutar"] for d in dagilim)
            styled_info_banner(f"Toplam Gelir: {_format_tutar(toplam)} ({len(dagilim)} kategori)", "info", "💰")

            try:
                import plotly.graph_objects as go
                col1, col2 = st.columns(2)
                with col1:
                    bar_x = [d["tutar"] for d in dagilim]
                    fig = go.Figure(go.Bar(
                        y=[d["kategori"] for d in dagilim],
                        x=bar_x,
                        orientation="h",
                        marker_color=SC_COLORS[0],
                        text=bar_x, textposition="outside",
                    ))
                    sc_bar(fig, height=300, horizontal=True)
                    fig.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
                with col2:
                    pie_labels = [d["kategori"] for d in dagilim]
                    fig = go.Figure(go.Pie(
                        labels=pie_labels,
                        values=[d["tutar"] for d in dagilim],
                        hole=0.55,
                        marker=dict(colors=SC_COLORS[:len(pie_labels)], line=dict(color="#fff", width=2)),
                        textinfo="label+percent",
                    ))
                    sc_pie(fig, height=300)
                    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            except ImportError:
                pass
        else:
            styled_info_banner("Bu yil için gelir verisi yok.", "info", "📊")

    with sub_tabs[2]:
        styled_section("Gider Raporu", _CLR_ORANGE)
        yil = st.number_input("Yil", min_value=2020, max_value=2040,
                              value=date.today().year, key="rp_gd_yil")
        raporlayici = ButceRaporlayici(store)
        dagilim = raporlayici.kategori_dagilimi("Gider", int(yil))

        if dagilim:
            toplam = sum(d["tutar"] for d in dagilim)
            styled_info_banner(f"Toplam Gider: {_format_tutar(toplam)} ({len(dagilim)} kategori)", "info", "💳")

            try:
                import plotly.graph_objects as go
                col1, col2 = st.columns(2)
                with col1:
                    bar_x = [d["tutar"] for d in dagilim]
                    fig = go.Figure(go.Bar(
                        y=[d["kategori"] for d in dagilim],
                        x=bar_x,
                        orientation="h",
                        marker_color=SC_COLORS[1],
                        text=bar_x, textposition="outside",
                    ))
                    sc_bar(fig, height=350, horizontal=True)
                    fig.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
                with col2:
                    fig = go.Figure(go.Sunburst(
                        labels=["Giderler"] + [d["kategori"] for d in dagilim],
                        parents=[""] + ["Giderler"] * len(dagilim),
                        values=[toplam] + [d["tutar"] for d in dagilim],
                        marker=dict(colors=[SC_COLORS[7]] + SC_COLORS[:len(dagilim)]),
                        branchvalues="total",
                    ))
                    fig.update_layout(
                        height=350, margin=dict(t=10, b=10, l=10, r=10),
                        paper_bgcolor="rgba(0,0,0,0)",
                    )
                    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            except ImportError:
                pass
        else:
            styled_info_banner("Bu yil için gider verisi yok.", "info", "📊")

    with sub_tabs[3]:
        styled_section("Varyans Raporu")
        planlar = store.load_objects("butce_planlari")
        if not planlar:
            styled_info_banner("Butce plani olusturun.", "warning", "⚠️")
            return

        plan_secenekleri = {f"{p.plan_kodu} - {p.plan_adi}": p.id for p in planlar}
        secili = st.selectbox("Plan", list(plan_secenekleri.keys()), key="rp_vr_plan")
        if not secili:
            return

        plan_id = plan_secenekleri[secili]
        analizcisi = ButceAnalizcisi(store)
        ozet = analizcisi.yillik_ozet(plan_id)

        if ozet:
            styled_stat_row([
                ("Tahmini Gelir", _format_tutar(ozet["tahmini_gelir"]), "info", "📋"),
                ("Gercek Gelir", _format_tutar(ozet["gercek_gelir"]), _CLR_GREEN, "💰"),
                ("Tahmini Gider", _format_tutar(ozet["tahmini_gider"]), _CLR_ORANGE, "📋"),
                ("Gercek Gider", _format_tutar(ozet["gercek_gider"]), "#ef4444", "💳"),
            ])

            try:
                import plotly.graph_objects as go
                cats = ["Gelir", "Gider", "Net"]
                tahmini = [ozet["tahmini_gelir"], ozet["tahmini_gider"], ozet["tahmini_net"]]
                gercek = [ozet["gercek_gelir"], ozet["gercek_gider"], ozet["gercek_net"]]

                fig = go.Figure()
                fig.add_trace(go.Bar(name="Tahmini", x=cats, y=tahmini,
                                     marker_color=SC_COLORS[0], text=tahmini, textposition="outside"))
                fig.add_trace(go.Bar(name="Gerçekleşen", x=cats, y=gercek,
                                     marker_color=SC_COLORS[1], text=gercek, textposition="outside"))
                sc_bar(fig, height=300)
                fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.08))
                st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            except ImportError:
                pass


# ============================================================
# SEKME 8: AYARLAR
# ============================================================

def _render_ayarlar(store: BGGDataStore):
    styled_header("Ayarlar", "Kategori yonetimi ve genel ayarlar")

    sub_tabs = st.tabs(["📂 Kategoriler", "⚙️ Genel Ayarlar"])

    with sub_tabs[0]:
        styled_section("Kategori Yönetimi")
        islem_tipi = st.radio("İşlem Tipi", ISLEM_TIPLERI, horizontal=True, key="ay_islem")
        kategoriler = [k for k in store.load_objects("kategoriler") if k.islem_tipi == islem_tipi]

        # Ana kategoriler
        ana_kat = [k for k in kategoriler if not k.ust_kategori_kodu]
        alt_kat = [k for k in kategoriler if k.ust_kategori_kodu]

        if ana_kat:
            rows = ""
            for k in sorted(ana_kat, key=lambda x: x.sira):
                altlar = [a for a in alt_kat if a.ust_kategori_kodu == k.kategori_kodu]
                alt_str = ", ".join(a.kategori_adi for a in altlar) if altlar else "-"
                durum = "Aktif" if k.aktif else "Pasif"
                durum_renk = _CLR_GREEN if k.aktif else _CLR_GRAY
                rows += f"""<tr>
                    <td style="padding:6px 10px;">{k.ikon}</td>
                    <td style="padding:6px 10px;font-weight:600;">{k.kategori_kodu}</td>
                    <td style="padding:6px 10px;">{k.kategori_adi}</td>
                    <td style="padding:6px 10px;font-size:11px;color:#64748b;">{alt_str}</td>
                    <td style="padding:6px 10px;"><span style="color:{durum_renk};font-weight:600;">{durum}</span></td>
                </tr>"""
            st.markdown(f"""<table style="width:100%;border-collapse:collapse;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;">
                <thead><tr style="background:linear-gradient(135deg,{_CLR_DARK},{_CLR_BLUE if islem_tipi == 'Gelir' else _CLR_ORANGE});">
                    <th style="padding:8px 10px;color:#fff;">Ikon</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Kod</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Kategori</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Alt Kategoriler</th>
                    <th style="padding:8px 10px;color:#fff;text-align:left;">Durum</th>
                </tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)

        # Yeni kategori ekleme
        st.markdown("---")
        styled_section("Yeni Kategori Ekle")
        with st.form("yeni_kat_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                kat_kod = st.text_input("Kategori Kodu", placeholder="Orn: G09 veya C15")

            with c2:
                kat_ad = st.text_input("Kategori Adi")

            with c3:
                ust_kod = st.text_input("Ust Kategori Kodu (alt kategori icin)", placeholder="Orn: G01")

            c4, c5 = st.columns(2)
            with c4:
                ikon = st.text_input("Ikon (emoji)", placeholder="📌")

            with c5:
                renk = st.color_picker("Renk", value=_CLR_BLUE if islem_tipi == "Gelir" else _CLR_ORANGE)

            submitted = st.form_submit_button("Kategori Ekle")

        if submitted and kat_kod and kat_ad:
            yeni = ButceKategori(
                kategori_kodu=kat_kod,
                kategori_adi=kat_ad,
                islem_tipi=islem_tipi,
                ust_kategori_kodu=ust_kod,
                ikon=ikon,
                renk=renk,
                sira=len(kategoriler) + 1,
            )
            store.upsert("kategoriler", yeni)
            st.success(f"Kategori eklendi: {kat_ad}")
            st.rerun()

    with sub_tabs[1]:
        styled_section("Genel Ayarlar")
        ayarlar = store.load_objects("bgg_ayarlar")

        if ayarlar:
            for ayar in ayarlar:
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.text_input(ayar.ayar_adi, value=ayar.deger,
                                  key=f"ayar_{ayar.id}", disabled=True)
                with col2:
                    st.caption(ayar.aciklama)
                with col3:
                    yeni_deger = st.text_input("Yeni", key=f"ayar_yeni_{ayar.id}")
                    if yeni_deger and yeni_deger != ayar.deger:
                        if st.button("Güncelle", key=f"ayar_btn_{ayar.id}"):
                            ayar.deger = yeni_deger
                            ayar.updated_at = _now()
                            store.upsert("bgg_ayarlar", ayar)
                            st.success(f"{ayar.ayar_adi} güncellendi.")
                            st.rerun()
        else:
            styled_info_banner("Ayarlar yukleniyor...", "info")


# ============================================================
# SEKME 9: SMARTI
# ============================================================

def _render_smarti(store: BGGDataStore):
    def _bgg_data_context() -> str:
        try:
            agg = DashboardAggregator(store)
            kpi = agg.kpi_hesapla()
            return (
                f"Yıllık Gelir: {_format_tutar(kpi['yillik_gelir'])}, "
                f"Yıllık Gider: {_format_tutar(kpi['yillik_gider'])}, "
                f"Net: {_format_tutar(kpi['yillik_net'])}, "
                f"Gelir Gerceklesme: %{kpi['gelir_gerceklesme']:.1f}, "
                f"Gider Gerceklesme: %{kpi['gider_gerceklesme']:.1f}, "
                f"Plan Sayısı: {kpi['plan_sayisi']}, "
                f"Gelir Kayıt: {kpi['gelir_kayit_sayisi']}, "
                f"Gider Kayıt: {kpi['gider_kayit_sayisi']}"
            )
        except Exception:
            return ""
    render_smarti_chat("butce_gelir_gider", _bgg_data_context)


# ============================================================
# ANA GIRIS NOKTASI
# ============================================================

def render_butce_gelir_gider():
    """BGG-01 modulu ana giris noktasi."""
    _inject_bgg_css()

    store = _get_bgg_store()

    tab_names = [
        "📊 Dashboard",
        "📋 Bütçe Planlama",
        "💵 Gelir Kayıt",
        "💳 Gider Kayıt",
        "📅 Tahmini vs Gerçekleşen",
        "📅 Aylık Takip",
        "📈 Raporlar",
        "⚙️ Ayarlar",
        "🤖 Smarti",
    ]

    render_smarti_welcome("butce_gelir_gider")
    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("butce_gelir_gider_egitim_yili")
    tabs = st.tabs(tab_names)

    with tabs[0]:
        _render_dashboard(store)
    with tabs[1]:
        _render_butce_planlama(store)
    with tabs[2]:
        _render_gelir_kayit(store)
    with tabs[3]:
        _render_gider_kayit(store)
    with tabs[4]:
        _render_tahmini_gerceklesen(store)
    with tabs[5]:
        _render_aylik_takip(store)
    with tabs[6]:
        _render_raporlar(store)
    with tabs[7]:
        _render_ayarlar(store)
    with tabs[8]:
        _render_smarti(store)
