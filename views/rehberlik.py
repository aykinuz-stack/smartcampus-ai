"""
RHB-01 Rehberlik ve Psikolojik Danismanlik Modulu - Streamlit UI
================================================================
Gorusme kayitlari, vaka takip, aile gorusmeleri, yonlendirme,
BEP, test/envanter, rehberlik plani, risk degerlendirme, raporlar.
"""

from __future__ import annotations

import os
from datetime import datetime, date
from typing import Any

import streamlit as st
import pandas as pd

from utils.tenant import get_tenant_dir
from utils.shared_data import (
    load_shared_students, get_student_display_options,
    get_sinif_sube_listesi, get_staff_name_list,
)
from utils.report_utils import ReportStyler, ReportPDFGenerator, get_institution_info
from utils.ui_kit import confirm_action
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("rehberlik")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("rehberlik",
        "41 sekmeli rehberlik — gorusme, vaka, BEP, 36 MEB formu, 20+ psikolojik test",
        [("41", "Sekme"), ("36", "MEB Form"), ("20+", "Test")])
except Exception:
    pass

import streamlit.components.v1 as components
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG

from models.rehberlik import (
    GorusmeKaydi, VakaKaydi, AileGorusme, Yonlendirme,
    BEPKaydi, TestEnvanter, RehberlikPlani, RiskDegerlendirme,
    TestSorusu, TestOturumu, TestCevap, TestDegerlendirici,
    HavuzImporter, TestPDFExporter, CercevePlanImporter,
    RehberlikDataStore, VakaTakipci, DashboardAggregator,
    GORUSME_TURLERI, GORUSME_KONULARI, GIZLILIK_SEVIYELERI,
    VAKA_ONCELIKLERI, VAKA_ONCELIK_LABEL, VAKA_ONCELIK_RENK,
    VAKA_DURUMLARI, VAKA_DURUM_LABEL, VAKA_DURUM_RENK,
    VELI_YAKINLIKLARI,
    YONLENDIRME_TURLERI, YONLENDIRME_KURUMLARI,
    YONLENDIRME_DURUMLARI, YONLENDIRME_DURUM_LABEL,
    BEP_DURUMLARI, BEP_DURUM_LABEL, BEP_ENGEL_TURLERI,
    TEST_KATEGORILERI, TEST_DURUMLARI, TEST_DURUM_LABEL,
    SORU_TIPLERI, SORU_TIPI_LABEL,
    LIKERT_SECENEKLER, EVET_HAYIR_SECENEKLER,
    OTURUM_DURUMLARI, OTURUM_DURUM_LABEL,
    PLAN_TURLERI, PLAN_TUR_LABEL, PLAN_HEDEF_KITLELER,
    RISK_SEVIYELERI, RISK_SEVIYE_LABEL, RISK_SEVIYE_RENK, RISK_ALANLARI,
    _now, _generate_test_erisim_kodu,
)
from models.test_havuzu import (
    HAZIR_TEST_KATALOGU, HAVUZ_KATEGORILERI,
    get_hazir_test, get_katalog_ozet,
)


EGITIM_YILI_SECENEKLERI = [
    "2023-2024",
    "2024-2025",
    "2025-2026",
    "2026-2027",
    "2027-2028",
]

# ============================================================
# YARDIMCI FONKSIYONLAR
# ============================================================

def _get_rhb_store() -> RehberlikDataStore:
    base = os.path.join(get_tenant_dir(), "rehberlik")
    return RehberlikDataStore(base)


def _ogrenci_selectbox(key: str, label: str = "Öğrenci Seçin") -> dict | None:
    students = load_shared_students()
    if not students:
        st.warning("Henuz ogrenci kaydi yok. Akademik Takip modulunden ogrenci ekleyin.")
        return None
    options = ["-- Secim yapin --"] + [
        f"{s.get('ad', '')} {s.get('soyad', '')} - {s.get('sinif', '')}/{s.get('sube', '')}"
        for s in students
    ]
    idx = st.selectbox(label, range(len(options)), format_func=lambda i: options[i], key=key)
    return students[idx - 1] if idx > 0 else None


def _ogrenci_sinif_sube_selectbox(key_prefix: str) -> dict | None:
    """Sinif/Sube filtreli ogrenci secimi."""
    ss = get_sinif_sube_listesi()
    siniflar = ["Tümü"] + ss.get("siniflar", [])
    subeler = ["Tümü"] + ss.get("subeler", [])
    c1, c2 = st.columns(2)
    with c1:
        sec_sinif = st.selectbox("Sınıf", siniflar, key=f"{key_prefix}_sinif")
    with c2:
        sec_sube = st.selectbox("Şube", subeler, key=f"{key_prefix}_sube")
    sf = None if sec_sinif == "Tümü" else sec_sinif
    su = None if sec_sube == "Tümü" else sec_sube
    opts = get_student_display_options(sinif_filter=sf, sube_filter=su, include_empty=True)
    labels = list(opts.keys())
    sel = st.selectbox("Öğrenci", labels, key=f"{key_prefix}_ogrenci")
    return opts.get(sel) if sel and sel != "-- Secim yapin --" else None


def _get_student_sinif_sube(stu: dict) -> str:
    return f"{stu.get('sinif', '')}/{stu.get('sube', '')}"


def _get_student_full_name(stu: dict) -> str:
    return f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip()


# ============================================================
# CSS STILLERI
# ============================================================

def _inject_rhb_css():
    inject_common_css("rhb")
    st.markdown("""<style>
    :root {
        --rhb-primary: #7c3aed;
        --rhb-primary-dark: #6d28d9;
        --rhb-success: #10b981;
        --rhb-warning: #f59e0b;
        --rhb-danger: #ef4444;
        --rhb-teal: #0d9488;
        --rhb-blue: #2563eb;
        --rhb-dark: #0B0F19;
    }
    .stApp > header { background: transparent !important; }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease; border-left: 4px solid #7c3aed;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    </style>""", unsafe_allow_html=True)


_GRAD = {
    "#7c3aed": ("rgba(124,58,237,0.10)", "rgba(124,58,237,0.25)"),
    "#6d28d9": ("rgba(109,40,217,0.10)", "rgba(109,40,217,0.25)"),
    "#10b981": ("rgba(16,185,129,0.10)", "rgba(16,185,129,0.25)"),
    "#2563eb": ("rgba(37,99,235,0.10)", "rgba(37,99,235,0.25)"),
    "#f59e0b": ("rgba(245,158,11,0.10)", "rgba(245,158,11,0.25)"),
    "#ef4444": ("rgba(239,68,68,0.10)", "rgba(239,68,68,0.25)"),
    "#0d9488": ("rgba(13,148,136,0.10)", "rgba(13,148,136,0.25)"),
    "#ea580c": ("rgba(234,88,12,0.10)", "rgba(234,88,12,0.25)"),
    "#64748b": ("rgba(100,116,139,0.10)", "rgba(100,116,139,0.25)"),
}




# ============================================================
# SEKME 1: DASHBOARD
# ============================================================

def _render_dashboard(store: RehberlikDataStore):
    data = DashboardAggregator.get_dashboard_data(store)

    # --- Ust KPI Satiri: Rehberlik ---
    styled_header("Rehberlik Özet", "Günlük görüşme ve vaka takibi", icon="💬")
    styled_stat_row([
        ("Bugün Görüşme", data["bugun_gorusme_sayi"], "#7c3aed", "\U0001F4AC"),
        ("Açık Vaka", data["acik_vaka_sayi"], "#ef4444", "\U0001F4C2"),
        ("Yuksek Risk", data["yuksek_risk_sayi"], "#ea580c", "\u26a0\ufe0f"),
        ("Takip Bekleyen", data["takip_sayi"], "#f59e0b", "\u23f0"),
        ("Aktif BEP", data["aktif_bep_sayi"], "#2563eb", "\U0001F4D1"),
        ("Açık Yönlendirme", data["acik_yon_sayi"], "#0d9488", "\U0001F517"),
    ])

    # --- Test & Envanter KPI Satiri ---
    styled_header("Test & Envanter Özet", "Psikolojik test ve envanter durumu", icon="📋")
    styled_stat_row([
        ("Toplam Test", data["toplam_test"], "#8b5cf6", "\U0001F4CB"),
        ("Toplam Soru", data["toplam_soru"], "#6366f1", "\u2753"),
        ("Online Aktif", data["online_aktif_test"], "#10b981", "\U0001F310"),
        ("Uygulanan", data["tamamlanan_oturum"], "#3b82f6", "\u2705"),
        ("Devam Eden", data["devam_oturum"], "#f59e0b", "\u23f3"),
        ("Cevap Kaydi", data["toplam_test_cevap"], "#ec4899", "\U0001F4CA"),
    ])

    # --- Genel Istatistik Banner ---
    st.markdown(f"""<div style="background:linear-gradient(135deg,#f0f4ff 0%,#e8ecff 100%);
        border-radius:12px;padding:16px 20px;margin:8px 0 16px 0;
        border:1px solid #c7d2fe;display:flex;gap:32px;flex-wrap:wrap;">
        <div><span style="color:#64748b;font-size:13px;">Toplam Gorusme</span><br>
        <b style="font-size:20px;color:#3730a3;">{data['toplam_gorusme']}</b></div>
        <div><span style="color:#64748b;font-size:13px;">Toplam Vaka</span><br>
        <b style="font-size:20px;color:#3730a3;">{data['toplam_vaka']}</b></div>
        <div><span style="color:#64748b;font-size:13px;">Toplam BEP</span><br>
        <b style="font-size:20px;color:#3730a3;">{data['toplam_bep']}</b></div>
        <div><span style="color:#64748b;font-size:13px;">Risk Değerlendirme</span><br>
        <b style="font-size:20px;color:#3730a3;">{data['toplam_risk']}</b></div>
        <div><span style="color:#64748b;font-size:13px;">Toplam Test</span><br>
        <b style="font-size:20px;color:#8b5cf6;">{data['toplam_test']}</b></div>
        <div><span style="color:#64748b;font-size:13px;">Toplam Oturum</span><br>
        <b style="font-size:20px;color:#3b82f6;">{data['toplam_oturum']}</b></div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        styled_section("Bugünün Görüşmeleri", "#7c3aed")
        if data["bugun_gorusmeler"]:
            for g in data["bugun_gorusmeler"]:
                st.markdown(f"""<div style="background:#111827;border-radius:10px;padding:12px;
                    margin:6px 0;border-left:3px solid #7c3aed;">
                    <b>{g.ogrenci_adi}</b> ({g.sinif_sube}) - {g.gorusme_turu}<br>
                    <small style="color:#64748b;">{g.saat_baslangic} | {g.gorusme_konusu} | {g.gorusen}</small>
                    </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Bugün planlanmis gorusme yok.")

        styled_section("Acil / Yuksek Öncelikli Vakalar", "#ef4444")
        acil_vakalar = [v for v in data["acik_vakalar"] if v.oncelik in ("ACIL", "YUKSEK")]
        if acil_vakalar:
            for v in acil_vakalar[:5]:
                renk = VAKA_ONCELIK_RENK.get(v.oncelik, "#64748b")
                st.markdown(f"""<div style="background:#111827;border-radius:10px;padding:12px;
                    margin:6px 0;border-left:3px solid {renk};">
                    <b>{v.vaka_kodu}</b> - {v.vaka_basligi}<br>
                    <small>{v.ogrenci_adi} ({v.sinif_sube}) | {VAKA_ONCELIK_LABEL.get(v.oncelik, v.oncelik)}</small>
                    </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Acil/yuksek oncelikli acik vaka yok.", "success")

    with c2:
        styled_section("Yaklasan Takipler (7 gun)", "#f59e0b")
        if data["takipler"]:
            for t in data["takipler"][:5]:
                k = t["kayit"]
                st.markdown(f"""<div style="background:#111827;border-radius:10px;padding:12px;
                    margin:6px 0;border-left:3px solid #f59e0b;">
                    <b>{k.ogrenci_adi}</b> ({k.sinif_sube}) - {t['tip']}<br>
                    <small style="color:#64748b;">{t['tarih']} ({t['gun']} gun sonra)</small>
                    </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Yaklasan takip yok.", "success")

        styled_section("Yuksek Riskli Öğrenciler", "#ea580c")
        if data["yuksek_risk"]:
            for r in data["yuksek_risk"][:5]:
                renk = RISK_SEVIYE_RENK.get(r.risk_seviyesi, "#64748b")
                st.markdown(f"""<div style="background:#111827;border-radius:10px;padding:12px;
                    margin:6px 0;border-left:3px solid {renk};">
                    <b>{r.ogrenci_adi}</b> ({r.sinif_sube})<br>
                    <small>{RISK_SEVIYE_LABEL.get(r.risk_seviyesi, '')} | {', '.join(r.risk_alanlari)}</small>
                    </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Yuksek riskli ogrenci yok.", "success")

    # --- Ultra Premium Plotly Grafikler ---
    import plotly.graph_objects as _go
    _PLT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0", family="Inter, system-ui"), margin=dict(l=20, r=20, t=40, b=20))

    c3, c4 = st.columns(2)
    with c3:
        styled_section("Görüşme Konu Dağılımı", "#7c3aed")
        if data["konu_dagilimi"]:
            _kn = data["konu_dagilimi"]
            _fig = _go.Figure(data=[_go.Pie(
                labels=list(_kn.keys()), values=list(_kn.values()), hole=0.45,
                marker=dict(colors=["#7c3aed", "#6366f1", "#3b82f6", "#06b6d4", "#10b981",
                                    "#f59e0b", "#ec4899", "#f97316"][:len(_kn)],
                            line=dict(color="#0f172a", width=2)),
                textinfo="label+percent", textfont=dict(size=10, color="#fff"),
            )])
            _fig.update_layout(**_PLT, height=340, showlegend=False,
                               title=dict(text="Konu Dağılımı", font=dict(size=14, color="#e2e8f0")),
                               annotations=[dict(text=f"<b>{sum(_kn.values())}</b><br>Görüşme",
                                                  x=0.5, y=0.5, font_size=14, font_color="#e2e8f0", showarrow=False)])
            st.plotly_chart(_fig, use_container_width=True, key="rh_konu_pie")
        else:
            st.info("Henuz gorusme kaydi yok.")

    with c4:
        styled_section("Risk Seviye Dağılımı", "#ea580c")
        if data["risk_dagilimi"]:
            _rd = data["risk_dagilimi"]
            _r_clrs = {"Düşük": "#22c55e", "Orta": "#f59e0b", "Yüksek": "#f97316", "Kritik": "#ef4444"}
            _r_c = [_r_clrs.get(k, "#64748b") for k in _rd.keys()]
            _fig2 = _go.Figure(data=[_go.Pie(
                labels=list(_rd.keys()), values=list(_rd.values()), hole=0.45,
                marker=dict(colors=_r_c, line=dict(color="#0f172a", width=2)),
                textinfo="label+value+percent", textfont=dict(size=10, color="#fff"),
                pull=[0.1 if "Kritik" in k or "Yüksek" in k else 0 for k in _rd.keys()],
            )])
            _fig2.update_layout(**_PLT, height=340, showlegend=False,
                                title=dict(text="Risk Dağılımı", font=dict(size=14, color="#e2e8f0")))
            st.plotly_chart(_fig2, use_container_width=True, key="rh_risk_pie")
        else:
            st.info("Henuz risk degerlendirme yok.")

    c5, c6 = st.columns(2)
    with c5:
        styled_section("Test Kategori Dağılımı", "#8b5cf6")
        if data["test_kategori_dagilimi"]:
            _tk = data["test_kategori_dagilimi"]
            _tc = ["#8b5cf6", "#6366f1", "#3b82f6", "#10b981", "#f59e0b", "#ec4899"]
            _fig3 = _go.Figure(data=[_go.Pie(
                labels=list(_tk.keys()), values=list(_tk.values()), hole=0.5,
                marker=dict(colors=_tc[:len(_tk)], line=dict(color="#0f172a", width=2)),
                textinfo="label+value", textfont=dict(size=9, color="#fff"),
            )])
            _fig3.update_layout(**_PLT, height=340, showlegend=False,
                                title=dict(text="Test Kategorileri", font=dict(size=14, color="#e2e8f0")))
            st.plotly_chart(_fig3, use_container_width=True, key="rh_test_pie")
        else:
            st.info("Henuz test kaydi yok.")

    with c6:
        styled_section("Test Katılım (Tamamlanan)", "#3b82f6")
        if data["test_katilim"]:
            _tp = data["test_katilim"]
            _tp_sorted = dict(sorted(_tp.items(), key=lambda x: -x[1]))
            _fig4 = _go.Figure(data=[_go.Bar(
                y=list(_tp_sorted.keys()), x=list(_tp_sorted.values()), orientation="h",
                marker=dict(color="#6366f1", line=dict(color="#818cf8", width=1)),
                text=list(_tp_sorted.values()), textposition="outside",
                textfont=dict(size=10, color="#e2e8f0"),
            )])
            _fig4.update_layout(**_PLT, height=340,
                                title=dict(text="Test Katılımı", font=dict(size=14, color="#e2e8f0")),
                                xaxis=dict(showgrid=True, gridcolor="#1e293b"),
                                yaxis=dict(showgrid=False, tickfont=dict(size=9)))
            st.plotly_chart(_fig4, use_container_width=True, key="rh_test_bar")
        else:
            st.info("Henuz tamamlanan test oturumu yok.")

    # Son 7 Gün — Plotly Bar
    styled_section("Son 7 Günde Tamamlanan Test Oturumları", "#10b981")
    if any(v > 0 for v in data["son7gun_values"]):
        _fig5 = _go.Figure(data=[_go.Bar(
            x=data["son7gun_labels"], y=data["son7gun_values"],
            marker=dict(color=["#8b5cf6" if v > 0 else "#1e293b" for v in data["son7gun_values"]],
                        line=dict(color="#a78bfa", width=1)),
            text=[int(v) for v in data["son7gun_values"]], textposition="outside",
            textfont=dict(size=11, color="#e2e8f0"),
        )])
        _fig5.update_layout(**_PLT, height=280,
                            title=dict(text="Son 7 Gün Test Oturumları", font=dict(size=14)),
                            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#1e293b"))
        st.plotly_chart(_fig5, use_container_width=True, key="rh_7gun_bar")
    else:
        styled_info_banner("Son 7 gunde tamamlanan test oturumu yok.")

    # --- Online Aktif Testler Listesi ---
    if data["online_aktif_testler"]:
        styled_section("Online Aktif Testler", "#10b981")
        for t in data["online_aktif_testler"]:
            erisim = getattr(t, "erisim_kodu", "-")
            soru_s = len(store.find_by_field("test_sorulari", "test_id", t.id))
            otr_s = sum(1 for o in data["tamamlanan_oturumlar"] if o.test_id == t.id)
            st.markdown(f"""<div style="background:#f0fdf4;border-radius:10px;padding:12px 16px;
                margin:6px 0;border-left:3px solid #10b981;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                <div><b>{getattr(t, 'test_adi', '-')}</b>
                <span style="background:#dbeafe;color:#1e40af;padding:2px 8px;border-radius:8px;font-size:11px;margin-left:8px;">
                {getattr(t, 'kategori', '-')}</span></div>
                <div style="display:flex;gap:16px;align-items:center;">
                    <span style="font-size:12px;color:#64748b;">{soru_s} soru</span>
                    <span style="font-size:12px;color:#64748b;">{otr_s} katilimci</span>
                    <span style="background:linear-gradient(135deg,#7c3aed,#6366f1);color:#fff;padding:4px 12px;
                        border-radius:8px;font-family:monospace;font-size:14px;font-weight:700;letter-spacing:2px;">
                        {erisim}</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # --- Son Tamamlanan Oturumlar ---
    if data["tamamlanan_oturumlar"]:
        styled_section("Son Tamamlanan Oturumlar", "#3b82f6")
        son_oturumlar = sorted(data["tamamlanan_oturumlar"],
                               key=lambda o: getattr(o, "bitis_zamani", ""), reverse=True)[:8]
        for o in son_oturumlar:
            test = store.get_by_id("testler", o.test_id)
            test_adi = getattr(test, "test_adi", "-") if test else "-"
            bitis = getattr(o, "bitis_zamani", "")[:16].replace("T", " ")
            st.markdown(f"""<div style="background:#111827;border-radius:10px;padding:10px 16px;
                margin:5px 0;border-left:3px solid #3b82f6;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                <div><b>{o.ogrenci_adi}</b> <span style="color:#64748b;">({o.sinif_sube})</span></div>
                <div style="display:flex;gap:12px;align-items:center;">
                    <span style="font-size:12px;color:#6366f1;">{test_adi}</span>
                    <span style="font-size:11px;color:#94a3b8;">{bitis}</span>
                    <span style="background:#dcfce7;color:#16a34a;padding:2px 8px;border-radius:8px;font-size:11px;">Tamamlandı</span>
                </div>
            </div>""", unsafe_allow_html=True)


# ============================================================
# SEKME 2: GORUSME KAYITLARI
# ============================================================

def _render_gorusme_kayitlari(store: RehberlikDataStore):
    sub = st.tabs(["➕ Yeni Görüşme", "📋 Görüşme Listesi", "📜 Öğrenci Geçmişi"])

    # --- Yeni Görüşme ---
    with sub[0]:
        styled_section("Yeni Görüşme Kaydi", "#7c3aed")
        stu = _ogrenci_sinif_sube_selectbox("grm_yeni")
        if not stu:
            return

        ogrenci_adi = _get_student_full_name(stu)
        sinif_sube = _get_student_sinif_sube(stu)

        c1, c2 = st.columns(2)
        with c1:
            gorusme_turu = st.selectbox("Görüşme Turu", GORUSME_TURLERI, key="grm_tur")
            gorusme_konusu = st.selectbox("Görüşme Konusu", GORUSME_KONULARI, key="grm_konu")
            gorusme_alt_konusu = st.text_input("Alt Konu", key="grm_alt_konu")
            tarih = st.date_input("Tarih", value=date.today(), key="grm_tarih")
        with c2:
            saat_baslangic = st.time_input("Başlangıç Saati", key="grm_saat_bas")
            saat_bitis = st.time_input("Bitis Saati", key="grm_saat_bit")
            staff = get_staff_name_list()
            gorusen = st.selectbox("Gorusen (Rehber)", [""] + staff, key="grm_gorusen")
            gizlilik = st.selectbox("Gizlilik Seviyesi", GIZLILIK_SEVIYELERI, key="grm_gizlilik")

        gorusme_ozeti = st.text_area("Görüşme Özeti", key="grm_ozet", height=100)
        gorusme_notlari = st.text_area("Görüşme Notları", key="grm_notlar", height=80)
        yapilan_mudahale = st.text_area("Yapilan Mudahale", key="grm_mudahale", height=80)

        c3, c4 = st.columns(2)
        with c3:
            sonraki_adim = st.text_input("Sonraki Adim", key="grm_sonraki")
            takip_tarihi = st.date_input("Takip Tarihi", value=None, key="grm_takip")
        with c4:
            # Vaka baglama
            vakalar = store.load_objects("vakalar")
            vaka_opts = {"": "-- Vaka bagla (opsiyonel) --"}
            for v in vakalar:
                if v.durum != "KAPANDI":
                    vaka_opts[v.id] = f"{v.vaka_kodu} - {v.ogrenci_adi} - {v.vaka_basligi}"
            vaka_sec = st.selectbox("Vaka Baglantisi", list(vaka_opts.keys()),
                                    format_func=lambda x: vaka_opts[x], key="grm_vaka")
            ey = st.selectbox("Egitim Yili", EGITIM_YILI_SECENEKLERI, index=1, key="grm_ey")

        if st.button("Görüşme Kaydet", type="primary", use_container_width=True, key="grm_kaydet"):
            if not gorusme_ozeti.strip():
                st.error("Görüşme ozeti bos birakilamaz.")
                return
            kod = store.next_gorusme_code()
            kayit = GorusmeKaydi(
                gorusme_kodu=kod,
                ogrenci_id=stu.get("id", ""),
                ogrenci_adi=ogrenci_adi,
                sinif_sube=sinif_sube,
                gorusme_turu=gorusme_turu,
                gorusme_konusu=gorusme_konusu,
                gorusme_alt_konusu=gorusme_alt_konusu,
                tarih=tarih.isoformat() if tarih else _today(),
                saat_baslangic=saat_baslangic.strftime("%H:%M") if saat_baslangic else "",
                saat_bitis=saat_bitis.strftime("%H:%M") if saat_bitis else "",
                gorusen=gorusen,
                gorusme_ozeti=gorusme_ozeti,
                gorusme_notlari=gorusme_notlari,
                yapilan_mudahale=yapilan_mudahale,
                sonraki_adim=sonraki_adim,
                takip_tarihi=takip_tarihi.isoformat() if takip_tarihi else "",
                vaka_id=vaka_sec,
                gizlilik_seviyesi=gizlilik,
                egitim_yili=ey,
            )
            store.upsert("gorusmeler", kayit)
            if vaka_sec:
                VakaTakipci.update_vaka_gorusme_count(store, vaka_sec)
            st.success(f"Görüşme kaydedildi: {kod}")
            st.rerun()

    # --- Görüşme Listesi ---
    with sub[1]:
        styled_section("Görüşme Listesi", "#7c3aed")
        gorusmeler = store.load_objects("gorusmeler")
        if not gorusmeler:
            styled_info_banner("Henuz gorusme kaydi yok.")
            return

        # Filtreler
        c1, c2, c3 = st.columns(3)
        with c1:
            f_konu = st.selectbox("Konu Filtre", ["Tümü"] + GORUSME_KONULARI, key="grm_f_konu")
        with c2:
            f_tur = st.selectbox("Tur Filtre", ["Tümü"] + GORUSME_TURLERI, key="grm_f_tur")
        with c3:
            f_ara = st.text_input("Öğrenci Ara", key="grm_f_ara")

        filtered = gorusmeler
        if f_konu != "Tümü":
            filtered = [g for g in filtered if g.gorusme_konusu == f_konu]
        if f_tur != "Tümü":
            filtered = [g for g in filtered if g.gorusme_turu == f_tur]
        if f_ara:
            f_lower = f_ara.lower()
            filtered = [g for g in filtered if f_lower in g.ogrenci_adi.lower()]

        filtered.sort(key=lambda g: g.tarih, reverse=True)

        for g in filtered:
            with st.expander(f"{g.gorusme_kodu} | {g.tarih} | {g.ogrenci_adi} ({g.sinif_sube}) - {g.gorusme_konusu}"):
                st.markdown(f"""
                **Tur:** {g.gorusme_turu} | **Konu:** {g.gorusme_konusu} | **Alt Konu:** {g.gorusme_alt_konusu}
                **Saat:** {g.saat_baslangic} - {g.saat_bitis} | **Gorusen:** {g.gorusen}
                **Gizlilik:** {g.gizlilik_seviyesi} | **Egitim Yili:** {g.egitim_yili}
                """)
                if g.gorusme_ozeti:
                    st.markdown(f"**Özet:** {g.gorusme_ozeti}")
                if g.gorusme_notlari:
                    st.markdown(f"**Notlar:** {g.gorusme_notlari}")
                if g.yapilan_mudahale:
                    st.markdown(f"**Mudahale:** {g.yapilan_mudahale}")
                if g.sonraki_adim:
                    st.markdown(f"**Sonraki Adim:** {g.sonraki_adim}")
                if g.takip_tarihi:
                    st.markdown(f"**Takip Tarihi:** {g.takip_tarihi}")
                if g.vaka_id:
                    vaka = store.get_by_id("vakalar", g.vaka_id)
                    if vaka:
                        st.markdown(f"**Bagli Vaka:** {vaka.vaka_kodu} - {vaka.vaka_basligi}")

                cc1, cc2 = st.columns(2)
                with cc1:
                    if confirm_action("Sil", "Bu görüşme kaydını silmek istediğinize emin misiniz?", key=f"grm_sil_{g.id}"):
                        store.delete_by_id("gorusmeler", g.id)
                        st.success("Görüşme silindi.")
                        st.rerun()

    # --- Öğrenci Geçmişi ---
    with sub[2]:
        styled_section("Öğrenci Rehberlik Geçmişi", "#6d28d9")
        stu_gecmis = _ogrenci_selectbox("grm_gecmis_ogr", "Öğrenci Seçin")
        if not stu_gecmis:
            return

        gecmis = VakaTakipci.get_ogrenci_gecmisi(store, stu_gecmis.get("id", ""))
        ogr_adi = _get_student_full_name(stu_gecmis)
        st.markdown(f"### {ogr_adi} - Rehberlik Geçmişi")

        categories = [
            ("Görüşmeler", gecmis["gorusmeler"], "#7c3aed"),
            ("Vakalar", gecmis["vakalar"], "#ef4444"),
            ("Aile Görüşmeleri", gecmis["aile_gorusmeleri"], "#f59e0b"),
            ("Yönlendirmeler", gecmis["yonlendirmeler"], "#0d9488"),
            ("BEP Kayıtlari", gecmis["bep_kayitlari"], "#2563eb"),
            ("Risk Değerlendirmeleri", gecmis["risk_degerlendirmeleri"], "#ea580c"),
        ]

        for cat_name, cat_list, cat_color in categories:
            styled_section(f"{cat_name} ({len(cat_list)})", cat_color)
            if not cat_list:
                st.caption("Kayıt yok.")
                continue
            for item in cat_list:
                d = item.to_dict() if hasattr(item, "to_dict") else item
                tarih = d.get("tarih", d.get("baslangic_tarihi", ""))
                baslik = d.get("gorusme_kodu", d.get("vaka_kodu", d.get("yonlendirme_kodu",
                    d.get("bep_kodu", d.get("test_kodu", "")))))
                aciklama = d.get("gorusme_ozeti", d.get("vaka_basligi", d.get("gorusme_nedeni",
                    d.get("yonlendirme_nedeni", d.get("engel_turu", d.get("aciklama", ""))))))
                st.markdown(f"""<div style="background:#111827;border-radius:8px;padding:10px;
                    margin:4px 0;border-left:3px solid {cat_color};">
                    <b>{baslik}</b> - {tarih}<br>
                    <small style="color:#64748b;">{aciklama[:120]}</small>
                    </div>""", unsafe_allow_html=True)


# ============================================================
# SEKME 3: VAKA TAKIP
# ============================================================

def _render_vaka_takip(store: RehberlikDataStore):
    sub = st.tabs(["➕ Yeni Vaka", "📋 Vaka Listesi", "🔍 Vaka Detay"])

    # --- Yeni Vaka ---
    with sub[0]:
        styled_section("Yeni Vaka Oluştur", "#ef4444")
        stu = _ogrenci_sinif_sube_selectbox("vk_yeni")
        if not stu:
            return

        ogrenci_adi = _get_student_full_name(stu)
        sinif_sube = _get_student_sinif_sube(stu)

        vaka_basligi = st.text_input("Vaka Başlığı", key="vk_baslik")
        vaka_aciklamasi = st.text_area("Vaka Açıklaması", key="vk_aciklama", height=100)

        c1, c2, c3 = st.columns(3)
        with c1:
            oncelik = st.selectbox("Öncelik", VAKA_ONCELIKLERI,
                                   format_func=lambda x: VAKA_ONCELIK_LABEL.get(x, x), key="vk_oncelik")
        with c2:
            risk = st.selectbox("Risk Seviyesi", RISK_SEVIYELERI,
                                format_func=lambda x: RISK_SEVIYE_LABEL.get(x, x), key="vk_risk")
        with c3:
            staff = get_staff_name_list()
            rehber = st.selectbox("Atanan Rehber", [""] + staff, key="vk_rehber")

        ilgili_konular = st.multiselect("Ilgili Konular", GORUSME_KONULARI, key="vk_konular")
        ey = st.selectbox("Egitim Yili", EGITIM_YILI_SECENEKLERI, index=1, key="vk_ey")

        if st.button("Vaka Oluştur", type="primary", use_container_width=True, key="vk_kaydet"):
            if not vaka_basligi.strip():
                st.error("Vaka basligi bos birakilamaz.")
                return
            kod = store.next_vaka_code()
            vaka = VakaKaydi(
                vaka_kodu=kod,
                ogrenci_id=stu.get("id", ""),
                ogrenci_adi=ogrenci_adi,
                sinif_sube=sinif_sube,
                vaka_basligi=vaka_basligi,
                vaka_aciklamasi=vaka_aciklamasi,
                oncelik=oncelik,
                risk_seviyesi=risk,
                atanan_rehber=rehber,
                ilgili_konular=ilgili_konular,
                egitim_yili=ey,
            )
            store.upsert("vakalar", vaka)
            st.success(f"Vaka oluşturuldu: {kod}")
            st.rerun()

    # --- Vaka Listesi ---
    with sub[1]:
        styled_section("Vaka Listesi", "#ef4444")
        vakalar = store.load_objects("vakalar")
        if not vakalar:
            styled_info_banner("Henuz vaka kaydi yok.")
            return

        c1, c2, c3 = st.columns(3)
        with c1:
            f_durum = st.selectbox("Durum", ["Tümü"] + VAKA_DURUMLARI,
                                   format_func=lambda x: VAKA_DURUM_LABEL.get(x, x) if x != "Tümü" else x,
                                   key="vk_f_durum")
        with c2:
            f_oncelik = st.selectbox("Öncelik", ["Tümü"] + VAKA_ONCELIKLERI,
                                     format_func=lambda x: VAKA_ONCELIK_LABEL.get(x, x) if x != "Tümü" else x,
                                     key="vk_f_oncelik")
        with c3:
            f_ara = st.text_input("Öğrenci Ara", key="vk_f_ara")

        filtered = vakalar
        if f_durum != "Tümü":
            filtered = [v for v in filtered if v.durum == f_durum]
        if f_oncelik != "Tümü":
            filtered = [v for v in filtered if v.oncelik == f_oncelik]
        if f_ara:
            f_lower = f_ara.lower()
            filtered = [v for v in filtered if f_lower in v.ogrenci_adi.lower()]

        filtered.sort(key=lambda v: v.baslangic_tarihi, reverse=True)

        for v in filtered:
            renk = VAKA_ONCELIK_RENK.get(v.oncelik, "#64748b")
            durum_renk = VAKA_DURUM_RENK.get(v.durum, "#64748b")
            with st.expander(f"{v.vaka_kodu} | {v.ogrenci_adi} ({v.sinif_sube}) - {v.vaka_basligi}"):
                st.markdown(f"""
                **Oncelik:** <span style="color:{renk};font-weight:700;">{VAKA_ONCELIK_LABEL.get(v.oncelik, v.oncelik)}</span> |
                **Durum:** <span style="color:{durum_renk};font-weight:700;">{VAKA_DURUM_LABEL.get(v.durum, v.durum)}</span> |
                **Risk:** {RISK_SEVIYE_LABEL.get(v.risk_seviyesi, v.risk_seviyesi)}
                """, unsafe_allow_html=True)
                st.markdown(f"**Rehber:** {v.atanan_rehber} | **Görüşme:** {v.gorusme_sayisi} | **Son:** {v.son_gorusme_tarihi}")
                if v.vaka_aciklamasi:
                    st.markdown(f"**Açıklama:** {v.vaka_aciklamasi}")
                if v.ilgili_konular:
                    st.markdown(f"**Konular:** {', '.join(v.ilgili_konular)}")

                cc1, cc2 = st.columns(2)
                with cc1:
                    yeni_durum = st.selectbox("Durum Güncelle", VAKA_DURUMLARI,
                                              format_func=lambda x: VAKA_DURUM_LABEL.get(x, x),
                                              index=VAKA_DURUMLARI.index(v.durum) if v.durum in VAKA_DURUMLARI else 0,
                                              key=f"vk_durum_{v.id}")
                    if st.button("Durumu Güncelle", key=f"vk_dgunc_{v.id}"):
                        v.durum = yeni_durum
                        if yeni_durum == "KAPANDI":
                            v.kapanis_tarihi = _today()
                        v.updated_at = _now()
                        store.upsert("vakalar", v)
                        st.success("Vaka durumu güncellendi.")
                        st.rerun()
                with cc2:
                    if confirm_action("Vakayı Sil", "Bu vakayı silmek istediğinize emin misiniz? Tüm vaka geçmişi silinecek.", key=f"vk_sil_{v.id}"):
                        store.delete_by_id("vakalar", v.id)
                        st.success("Vaka silindi.")
                        st.rerun()

    # --- Vaka Detay ---
    with sub[2]:
        styled_section("Vaka Detay", "#ef4444")
        vakalar = store.load_objects("vakalar")
        if not vakalar:
            styled_info_banner("Henuz vaka yok.")
            return

        vaka_opts = {v.id: f"{v.vaka_kodu} - {v.ogrenci_adi} - {v.vaka_basligi}" for v in vakalar}
        vaka_id = st.selectbox("Vaka Secin", list(vaka_opts.keys()),
                               format_func=lambda x: vaka_opts[x], key="vk_detay_sec")
        vaka = store.get_by_id("vakalar", vaka_id)
        if not vaka:
            return

        renk = VAKA_ONCELIK_RENK.get(vaka.oncelik, "#64748b")
        st.markdown(f"""
        ### {vaka.vaka_kodu} - {vaka.vaka_basligi}
        **Öğrenci:** {vaka.ogrenci_adi} ({vaka.sinif_sube}) |
        **Oncelik:** <span style="color:{renk};font-weight:700;">{VAKA_ONCELIK_LABEL.get(vaka.oncelik, '')}</span> |
        **Durum:** {VAKA_DURUM_LABEL.get(vaka.durum, '')} |
        **Risk:** {RISK_SEVIYE_LABEL.get(vaka.risk_seviyesi, '')}
        """, unsafe_allow_html=True)

        if vaka.vaka_aciklamasi:
            st.markdown(f"**Açıklama:** {vaka.vaka_aciklamasi}")

        # Bagli gorusmeler
        styled_section("Bagli Görüşmeler", "#7c3aed")
        bagli_gorusmeler = store.find_by_field("gorusmeler", "vaka_id", vaka.id)
        if bagli_gorusmeler:
            for g in sorted(bagli_gorusmeler, key=lambda x: x.tarih, reverse=True):
                st.markdown(f"- **{g.gorusme_kodu}** ({g.tarih}) - {g.gorusme_konusu}: {g.gorusme_ozeti[:80]}")
        else:
            st.caption("Bagli gorusme yok.")

        # Bagli aile gorusmeleri
        styled_section("Bagli Aile Görüşmeleri", "#f59e0b")
        bagli_aile = store.find_by_field("aile_gorusmeleri", "vaka_id", vaka.id)
        if bagli_aile:
            for a in sorted(bagli_aile, key=lambda x: x.tarih, reverse=True):
                st.markdown(f"- **{a.gorusme_kodu}** ({a.tarih}) - {a.veli_adi}: {a.gorusme_ozeti[:80]}")
        else:
            st.caption("Bagli aile gorusmesi yok.")

        # Bagli yonlendirmeler
        styled_section("Bagli Yönlendirmeler", "#0d9488")
        bagli_yon = store.find_by_field("yonlendirmeler", "vaka_id", vaka.id)
        if bagli_yon:
            for y in bagli_yon:
                st.markdown(f"- **{y.yonlendirme_kodu}** ({y.tarih}) - {y.yonlendirilen_kurum or y.yonlendirilen_kisi} | {YONLENDIRME_DURUM_LABEL.get(y.durum, y.durum)}")
        else:
            st.caption("Bagli yonlendirme yok.")

        # Bagli risk
        styled_section("Risk Değerlendirmeleri", "#ea580c")
        bagli_risk = store.find_by_field("risk_degerlendirmeleri", "vaka_id", vaka.id)
        if bagli_risk:
            for r in bagli_risk:
                st.markdown(f"- {r.tarih} - {RISK_SEVIYE_LABEL.get(r.risk_seviyesi, '')} | {', '.join(r.risk_alanlari)}")
        else:
            st.caption("Bagli risk degerlendirme yok.")


# ============================================================
# SEKME 4: AILE GORUSMELERI
# ============================================================

def _render_aile_gorusmeleri(store: RehberlikDataStore):
    sub = st.tabs(["➕ Yeni Aile Görüşmesi", "📋 Aile Görüşme Listesi"])

    with sub[0]:
        styled_section("Yeni Aile Görüşmesi", "#f59e0b")
        stu = _ogrenci_sinif_sube_selectbox("ag_yeni")
        if not stu:
            return

        ogrenci_adi = _get_student_full_name(stu)
        sinif_sube = _get_student_sinif_sube(stu)

        # Veli bilgisi otomatik doldurma
        veli_adi_default = stu.get("veli_adi", "")
        if not veli_adi_default:
            anne = f'{stu.get("anne_adi", "")} {stu.get("anne_soyadi", "")}'.strip()
            baba = f'{stu.get("baba_adi", "")} {stu.get("baba_soyadi", "")}'.strip()
            veli_adi_default = anne or baba

        c1, c2 = st.columns(2)
        with c1:
            veli_adi = st.text_input("Veli Adi", value=veli_adi_default, key="ag_veli_adi")
            veli_yakinligi = st.selectbox("Yakinligi", VELI_YAKINLIKLARI, key="ag_yakinlik")
            tarih = st.date_input("Tarih", value=date.today(), key="ag_tarih")
            saat = st.time_input("Saat", key="ag_saat")
        with c2:
            staff = get_staff_name_list()
            gorusen = st.selectbox("Gorusen", [""] + staff, key="ag_gorusen")
            gorusme_nedeni = st.text_input("Görüşme Nedeni", key="ag_neden")
            # Vaka baglama
            vakalar = store.load_objects("vakalar")
            vaka_opts = {"": "-- Vaka bagla (opsiyonel) --"}
            for v in vakalar:
                if v.durum != "KAPANDI":
                    vaka_opts[v.id] = f"{v.vaka_kodu} - {v.ogrenci_adi}"
            vaka_sec = st.selectbox("Vaka Baglantisi", list(vaka_opts.keys()),
                                    format_func=lambda x: vaka_opts[x], key="ag_vaka")

        gorusme_ozeti = st.text_area("Görüşme Özeti", key="ag_ozet", height=100)
        alinan_kararlar = st.text_area("Alinan Kararlar", key="ag_kararlar", height=80)
        veli_gorusu = st.text_area("Veli Gorusu", key="ag_veli_gorusu", height=80)

        c3, c4 = st.columns(2)
        with c3:
            sonraki_adim = st.text_input("Sonraki Adim", key="ag_sonraki")
            takip_tarihi = st.date_input("Takip Tarihi", value=None, key="ag_takip")
        with c4:
            ey = st.selectbox("Egitim Yili", EGITIM_YILI_SECENEKLERI, index=1, key="ag_ey")

        if st.button("Aile Görüşmesi Kaydet", type="primary", use_container_width=True, key="ag_kaydet"):
            if not gorusme_ozeti.strip():
                st.error("Görüşme ozeti bos birakilamaz.")
                return
            kod = store.next_aile_code()
            kayit = AileGorusme(
                gorusme_kodu=kod,
                ogrenci_id=stu.get("id", ""),
                ogrenci_adi=ogrenci_adi,
                sinif_sube=sinif_sube,
                veli_adi=veli_adi,
                veli_yakinligi=veli_yakinligi,
                tarih=tarih.isoformat() if tarih else _today(),
                saat=saat.strftime("%H:%M") if saat else "",
                gorusen=gorusen,
                gorusme_nedeni=gorusme_nedeni,
                gorusme_ozeti=gorusme_ozeti,
                alinan_kararlar=alinan_kararlar,
                veli_gorusu=veli_gorusu,
                sonraki_adim=sonraki_adim,
                takip_tarihi=takip_tarihi.isoformat() if takip_tarihi else "",
                vaka_id=vaka_sec,
                egitim_yili=ey,
            )
            store.upsert("aile_gorusmeleri", kayit)
            if vaka_sec:
                VakaTakipci.update_vaka_gorusme_count(store, vaka_sec)
            st.success(f"Aile gorusmesi kaydedildi: {kod}")
            st.rerun()

    with sub[1]:
        styled_section("Aile Görüşme Listesi", "#f59e0b")
        aile_gorusmeleri = store.load_objects("aile_gorusmeleri")
        if not aile_gorusmeleri:
            styled_info_banner("Henuz aile gorusmesi yok.")
            return

        f_ara = st.text_input("Öğrenci/Veli Ara", key="ag_f_ara")
        filtered = aile_gorusmeleri
        if f_ara:
            f_lower = f_ara.lower()
            filtered = [a for a in filtered if f_lower in a.ogrenci_adi.lower() or f_lower in a.veli_adi.lower()]

        filtered.sort(key=lambda a: a.tarih, reverse=True)

        for a in filtered:
            with st.expander(f"{a.gorusme_kodu} | {a.tarih} | {a.ogrenci_adi} - {a.veli_adi} ({a.veli_yakinligi})"):
                st.markdown(f"""
                **Neden:** {a.gorusme_nedeni} | **Gorusen:** {a.gorusen} | **Saat:** {a.saat}
                """)
                if a.gorusme_ozeti:
                    st.markdown(f"**Özet:** {a.gorusme_ozeti}")
                if a.alinan_kararlar:
                    st.markdown(f"**Kararlar:** {a.alinan_kararlar}")
                if a.veli_gorusu:
                    st.markdown(f"**Veli Gorusu:** {a.veli_gorusu}")
                if a.sonraki_adim:
                    st.markdown(f"**Sonraki Adim:** {a.sonraki_adim}")
                if a.takip_tarihi:
                    st.markdown(f"**Takip:** {a.takip_tarihi}")
                if confirm_action("Sil", "Bu aile görüşmesi kaydını silmek istediğinize emin misiniz?", key=f"ag_sil_{a.id}"):
                    store.delete_by_id("aile_gorusmeleri", a.id)
                    st.success("Aile görüşmesi silindi.")
                    st.rerun()


# ============================================================
# SEKME 5: YONLENDIRME
# ============================================================

def _render_yonlendirme(store: RehberlikDataStore):
    sub = st.tabs(["➕ Yeni Yönlendirme", "📋 Yönlendirme Listesi"])

    with sub[0]:
        styled_section("Yeni Yönlendirme", "#0d9488")
        stu = _ogrenci_sinif_sube_selectbox("yon_yeni")
        if not stu:
            return

        ogrenci_adi = _get_student_full_name(stu)
        sinif_sube = _get_student_sinif_sube(stu)

        c1, c2 = st.columns(2)
        with c1:
            tur = st.selectbox("Yönlendirme Turu", YONLENDIRME_TURLERI, key="yon_tur")
            tarih = st.date_input("Tarih", value=date.today(), key="yon_tarih")
        with c2:
            if tur == "Harici":
                kurum = st.selectbox("Yonlendirilen Kurum", YONLENDIRME_KURUMLARI, key="yon_kurum")
                kisi = st.text_input("Kisi (opsiyonel)", key="yon_kisi")
            else:
                kurum = ""
                staff = get_staff_name_list()
                kisi = st.selectbox("Yonlendirilen Kisi", [""] + staff, key="yon_kisi_dahili")

        yonlendirme_nedeni = st.text_area("Yönlendirme Nedeni", key="yon_neden", height=100)

        # Vaka baglama
        vakalar = store.load_objects("vakalar")
        vaka_opts = {"": "-- Vaka bagla (opsiyonel) --"}
        for v in vakalar:
            if v.durum != "KAPANDI":
                vaka_opts[v.id] = f"{v.vaka_kodu} - {v.ogrenci_adi}"
        vaka_sec = st.selectbox("Vaka Baglantisi", list(vaka_opts.keys()),
                                format_func=lambda x: vaka_opts[x], key="yon_vaka")
        ey = st.selectbox("Egitim Yili", EGITIM_YILI_SECENEKLERI, index=1, key="yon_ey")

        if st.button("Yönlendirme Kaydet", type="primary", use_container_width=True, key="yon_kaydet"):
            if not yonlendirme_nedeni.strip():
                st.error("Yönlendirme nedeni bos birakilamaz.")
                return
            kod = store.next_yon_code()
            kayit = Yonlendirme(
                yonlendirme_kodu=kod,
                ogrenci_id=stu.get("id", ""),
                ogrenci_adi=ogrenci_adi,
                sinif_sube=sinif_sube,
                yonlendirme_turu=tur,
                yonlendirme_nedeni=yonlendirme_nedeni,
                yonlendirilen_kurum=kurum,
                yonlendirilen_kisi=kisi,
                tarih=tarih.isoformat() if tarih else _today(),
                vaka_id=vaka_sec,
                egitim_yili=ey,
            )
            store.upsert("yonlendirmeler", kayit)
            st.success(f"Yönlendirme kaydedildi: {kod}")
            st.rerun()

    with sub[1]:
        styled_section("Yönlendirme Listesi", "#0d9488")
        yonlendirmeler = store.load_objects("yonlendirmeler")
        if not yonlendirmeler:
            styled_info_banner("Henuz yonlendirme kaydi yok.")
            return

        c1, c2 = st.columns(2)
        with c1:
            f_durum = st.selectbox("Durum", ["Tümü"] + YONLENDIRME_DURUMLARI,
                                   format_func=lambda x: YONLENDIRME_DURUM_LABEL.get(x, x) if x != "Tümü" else x,
                                   key="yon_f_durum")
        with c2:
            f_tur = st.selectbox("Tur", ["Tümü"] + YONLENDIRME_TURLERI, key="yon_f_tur")

        filtered = yonlendirmeler
        if f_durum != "Tümü":
            filtered = [y for y in filtered if y.durum == f_durum]
        if f_tur != "Tümü":
            filtered = [y for y in filtered if y.yonlendirme_turu == f_tur]

        filtered.sort(key=lambda y: y.tarih, reverse=True)

        for y in filtered:
            with st.expander(f"{y.yonlendirme_kodu} | {y.tarih} | {y.ogrenci_adi} - {y.yonlendirme_turu}"):
                st.markdown(f"""
                **Tur:** {y.yonlendirme_turu} | **Kurum:** {y.yonlendirilen_kurum} | **Kisi:** {y.yonlendirilen_kisi}
                **Durum:** {YONLENDIRME_DURUM_LABEL.get(y.durum, y.durum)}
                """)
                if y.yonlendirme_nedeni:
                    st.markdown(f"**Neden:** {y.yonlendirme_nedeni}")
                if y.sonuc_raporu:
                    st.markdown(f"**Sonuc Raporu:** {y.sonuc_raporu}")

                # Durum akisi guncelle
                mevcut_idx = YONLENDIRME_DURUMLARI.index(y.durum) if y.durum in YONLENDIRME_DURUMLARI else 0
                yeni_durum = st.selectbox("Durum Güncelle", YONLENDIRME_DURUMLARI,
                                          format_func=lambda x: YONLENDIRME_DURUM_LABEL.get(x, x),
                                          index=mevcut_idx, key=f"yon_durum_{y.id}")

                sonuc_raporu = ""
                if yeni_durum == "SONUCLANDI":
                    sonuc_raporu = st.text_area("Sonuc Raporu", value=y.sonuc_raporu, key=f"yon_sonuc_{y.id}")

                cc1, cc2 = st.columns(2)
                with cc1:
                    if st.button("Durumu Güncelle", key=f"yon_dgunc_{y.id}"):
                        y.durum = yeni_durum
                        if sonuc_raporu:
                            y.sonuc_raporu = sonuc_raporu
                            y.rapor_tarihi = _today()
                        y.updated_at = _now()
                        store.upsert("yonlendirmeler", y)
                        st.success("Yönlendirme güncellendi.")
                        st.rerun()
                with cc2:
                    if confirm_action("Sil", "Bu yönlendirme kaydını silmek istediğinize emin misiniz?", key=f"yon_sil_{y.id}"):
                        store.delete_by_id("yonlendirmeler", y.id)
                        st.success("Yönlendirme silindi.")
                        st.rerun()


# ============================================================
# SEKME 6: BEP
# ============================================================

def _render_bep(store: RehberlikDataStore):
    sub = st.tabs(["➕ Yeni BEP", "📋 BEP Listesi", "🔍 BEP Detay"])

    with sub[0]:
        styled_section("Yeni BEP Kaydi", "#2563eb")
        stu = _ogrenci_sinif_sube_selectbox("bep_yeni")
        if not stu:
            return

        ogrenci_adi = _get_student_full_name(stu)
        sinif_sube = _get_student_sinif_sube(stu)

        c1, c2 = st.columns(2)
        with c1:
            engel_turu = st.selectbox("Engel Turu", BEP_ENGEL_TURLERI, key="bep_engel")
            tani = st.text_input("Tani", key="bep_tani")
            baslangic = st.date_input("Başlangıç Tarihi", value=date.today(), key="bep_baslangic")
            bitis = st.date_input("Bitis Tarihi", value=None, key="bep_bitis")
        with c2:
            staff = get_staff_name_list()
            rehber = st.selectbox("Rehber Öğretmen", [""] + staff, key="bep_rehber")
            veli_onayi = st.checkbox("Veli Onayi Var", key="bep_veli_onay")
            ey = st.selectbox("Egitim Yili", EGITIM_YILI_SECENEKLERI, index=1, key="bep_ey")

        # Dinamik hedefler
        styled_section("Hedefler", "#2563eb")
        if "bep_hedefler" not in st.session_state:
            st.session_state.bep_hedefler = []

        for i, h in enumerate(st.session_state.bep_hedefler):
            cc1, cc2, cc3 = st.columns([4, 3, 1])
            with cc1:
                st.session_state.bep_hedefler[i]["hedef"] = st.text_input(
                    "Hedef", value=h.get("hedef", ""), key=f"bep_h_hedef_{i}")
            with cc2:
                st.session_state.bep_hedefler[i]["olcut"] = st.text_input(
                    "Olcut", value=h.get("olcut", ""), key=f"bep_h_olcut_{i}")
            with cc3:
                if st.button("X", key=f"bep_h_sil_{i}"):
                    st.session_state.bep_hedefler.pop(i)
                    st.rerun()

        if st.button("+ Hedef Ekle", key="bep_h_ekle"):
            st.session_state.bep_hedefler.append({"hedef": "", "olcut": ""})
            st.rerun()

        # Dinamik uyarlamalar
        styled_section("Uyarlamalar", "#2563eb")
        if "bep_uyarlamalar" not in st.session_state:
            st.session_state.bep_uyarlamalar = []

        for i, u in enumerate(st.session_state.bep_uyarlamalar):
            cc1, cc2, cc3 = st.columns([3, 4, 1])
            with cc1:
                st.session_state.bep_uyarlamalar[i]["ders"] = st.text_input(
                    "Ders", value=u.get("ders", ""), key=f"bep_u_ders_{i}")
            with cc2:
                st.session_state.bep_uyarlamalar[i]["aciklama"] = st.text_input(
                    "Uyarlama Açıklaması", value=u.get("aciklama", ""), key=f"bep_u_aciklama_{i}")
            with cc3:
                if st.button("X", key=f"bep_u_sil_{i}"):
                    st.session_state.bep_uyarlamalar.pop(i)
                    st.rerun()

        if st.button("+ Uyarlama Ekle", key="bep_u_ekle"):
            st.session_state.bep_uyarlamalar.append({"ders": "", "aciklama": ""})
            st.rerun()

        # Sorumlu ogretmenler
        sorumlu_ogretmenler = st.multiselect("Sorumlu Öğretmenler", staff, key="bep_sorumlular")

        degerlendirme = st.text_area("Değerlendirme Notları", key="bep_degerlendirme", height=80)

        if st.button("BEP Kaydet", type="primary", use_container_width=True, key="bep_kaydet"):
            if not tani.strip():
                st.error("Tani alani bos birakilamaz.")
                return
            kod = store.next_bep_code()
            kayit = BEPKaydi(
                bep_kodu=kod,
                ogrenci_id=stu.get("id", ""),
                ogrenci_adi=ogrenci_adi,
                sinif_sube=sinif_sube,
                engel_turu=engel_turu,
                tani=tani,
                baslangic_tarihi=baslangic.isoformat() if baslangic else _today(),
                bitis_tarihi=bitis.isoformat() if bitis else "",
                hedefler=[h for h in st.session_state.bep_hedefler if h.get("hedef")],
                uyarlamalar=[u for u in st.session_state.bep_uyarlamalar if u.get("ders")],
                sorumlu_ogretmenler=sorumlu_ogretmenler,
                rehber_ogretmen=rehber,
                veli_onayi=veli_onayi,
                degerlendirme_notlari=degerlendirme,
                egitim_yili=ey,
            )
            store.upsert("bep_kayitlari", kayit)
            st.session_state.bep_hedefler = []
            st.session_state.bep_uyarlamalar = []
            st.success(f"BEP kaydedildi: {kod}")
            st.rerun()

    with sub[1]:
        styled_section("BEP Listesi", "#2563eb")
        bepler = store.load_objects("bep_kayitlari")
        if not bepler:
            styled_info_banner("Henuz BEP kaydi yok.")
            return

        c1, c2 = st.columns(2)
        with c1:
            f_durum = st.selectbox("Durum", ["Tümü"] + BEP_DURUMLARI,
                                   format_func=lambda x: BEP_DURUM_LABEL.get(x, x) if x != "Tümü" else x,
                                   key="bep_f_durum")
        with c2:
            f_engel = st.selectbox("Engel Turu", ["Tümü"] + BEP_ENGEL_TURLERI, key="bep_f_engel")

        filtered = bepler
        if f_durum != "Tümü":
            filtered = [b for b in filtered if b.durum == f_durum]
        if f_engel != "Tümü":
            filtered = [b for b in filtered if b.engel_turu == f_engel]

        for b in filtered:
            with st.expander(f"{b.bep_kodu} | {b.ogrenci_adi} ({b.sinif_sube}) - {b.engel_turu}"):
                st.markdown(f"""
                **Tani:** {b.tani} | **Durum:** {BEP_DURUM_LABEL.get(b.durum, b.durum)}
                **Baslangic:** {b.baslangic_tarihi} | **Bitis:** {b.bitis_tarihi or '-'}
                **Rehber:** {b.rehber_ogretmen} | **Veli Onayi:** {'Evet' if b.veli_onayi else 'Hayir'}
                """)
                if b.hedefler:
                    st.markdown("**Hedefler:**")
                    for h in b.hedefler:
                        st.markdown(f"  - {h.get('hedef', '')} (Olcut: {h.get('olcut', '')})")
                if b.uyarlamalar:
                    st.markdown("**Uyarlamalar:**")
                    for u in b.uyarlamalar:
                        st.markdown(f"  - {u.get('ders', '')}: {u.get('aciklama', '')}")

                # Durum guncelle
                yeni_durum = st.selectbox("Durum Güncelle", BEP_DURUMLARI,
                                          format_func=lambda x: BEP_DURUM_LABEL.get(x, x),
                                          index=BEP_DURUMLARI.index(b.durum) if b.durum in BEP_DURUMLARI else 0,
                                          key=f"bep_durum_{b.id}")
                cc1, cc2 = st.columns(2)
                with cc1:
                    if st.button("Durumu Güncelle", key=f"bep_dgunc_{b.id}"):
                        b.durum = yeni_durum
                        b.updated_at = _now()
                        store.upsert("bep_kayitlari", b)
                        st.success("BEP güncellendi.")
                        st.rerun()
                with cc2:
                    if confirm_action("Sil", "Bu BEP kaydını silmek istediğinize emin misiniz?", key=f"bep_sil_{b.id}"):
                        store.delete_by_id("bep_kayitlari", b.id)
                        st.success("BEP silindi.")
                        st.rerun()

    with sub[2]:
        styled_section("BEP Detay", "#2563eb")
        bepler = store.load_objects("bep_kayitlari")
        if not bepler:
            styled_info_banner("Henuz BEP yok.")
            return

        bep_opts = {b.id: f"{b.bep_kodu} - {b.ogrenci_adi} - {b.engel_turu}" for b in bepler}
        bep_id = st.selectbox("BEP Secin", list(bep_opts.keys()),
                              format_func=lambda x: bep_opts[x], key="bep_detay_sec")
        bep = store.get_by_id("bep_kayitlari", bep_id)
        if not bep:
            return

        st.markdown(f"""
        ### {bep.bep_kodu} - {bep.ogrenci_adi} ({bep.sinif_sube})
        **Engel Turu:** {bep.engel_turu} | **Tani:** {bep.tani}
        **Durum:** {BEP_DURUM_LABEL.get(bep.durum, bep.durum)} | **Veli Onayi:** {'Evet' if bep.veli_onayi else 'Hayir'}
        **Baslangic:** {bep.baslangic_tarihi} | **Bitis:** {bep.bitis_tarihi or '-'}
        **Rehber:** {bep.rehber_ogretmen}
        """)

        if bep.hedefler:
            styled_section("Hedefler", "#2563eb")
            for i, h in enumerate(bep.hedefler):
                st.markdown(f"**{i+1}.** {h.get('hedef', '')} - Olcut: {h.get('olcut', '')}")

        if bep.uyarlamalar:
            styled_section("Uyarlamalar", "#0d9488")
            for u in bep.uyarlamalar:
                st.markdown(f"- **{u.get('ders', '')}:** {u.get('aciklama', '')}")

        if bep.sorumlu_ogretmenler:
            styled_section("Sorumlu Öğretmenler", "#7c3aed")
            for s in bep.sorumlu_ogretmenler:
                st.markdown(f"- {s}")

        if bep.degerlendirme_notlari:
            styled_section("Değerlendirme Notları", "#f59e0b")
            st.markdown(bep.degerlendirme_notlari)


# ============================================================
# SEKME 7: TEST VE ENVANTER
# ============================================================

def _render_test_envanter(store: RehberlikDataStore):
    sub = st.tabs(["🧪 Test Olustur & Uygula", "📊 Sonuclar", "👤 Bireysel Uygula"])

    with sub[0]:
        _render_test_olustur_uygula(store)
    with sub[1]:
        _render_test_sonuclar_birlesik(store)
    with sub[2]:
        _render_bireysel_test_uygula(store)


# ---------- Sub-tab 0: Bireysel Test Uygulama ----------

def _render_bireysel_test_uygula(store: RehberlikDataStore):
    """Rehber öğretmen öğrenci seçer → mevcut test seçer → soruları cevaplar → sonuç kaydedilir."""
    styled_header("Bireysel Test Uygula", "Öğrenci seçin, test seçin, soruları yanıtlayın", icon="👤")

    # ── 1. Öğrenci Seç ──
    try:
        from utils.shared_data import get_student_display_options
        students = get_student_display_options(include_empty=False)
    except Exception:
        students = {}

    if not students:
        st.warning("Öğrenci bulunamadı.")
        return

    sel_stu = st.selectbox("👤 Öğrenci Seçin:", [""] + list(students.keys()), key="btu_stu")
    if not sel_stu:
        st.info("Bir öğrenci seçin.")
        return

    stu_data = students.get(sel_stu, {})
    stu_id = stu_data.get("id", "")
    stu_name = f"{stu_data.get('ad', '')} {stu_data.get('soyad', '')}".strip()

    st.markdown(f"**Seçilen:** {stu_name} — {stu_data.get('sinif', '?')}/{stu_data.get('sube', '?')}")

    # ── 2. Test Seç (mevcut testlerden) ──
    testler = store.load_objects("testler")
    if not testler:
        st.warning("Henüz test oluşturulmamış. '➕ Yeni Test' veya '📚 Test Havuzu' sekmesinden test ekleyin.")
        return

    test_options = {t.id: f"{t.test_adi} ({t.test_kategorisi})" for t in testler}
    sel_test_id = st.selectbox("🧪 Test Seçin:", list(test_options.keys()),
                                format_func=lambda x: test_options[x], key="btu_test")

    test = store.get_by_id("testler", sel_test_id)
    if not test:
        return

    sorular = store.find_by_field("test_sorulari", "test_id", test.id)
    if not sorular:
        st.warning(f"'{test.test_adi}' testine henüz soru eklenmemiş. '✏️ Soru Oluştur' sekmesinden soru ekleyin.")
        return

    st.markdown(f"**Test:** {test.test_adi} | **Soru:** {len(sorular)} | **Tip:** {test.soru_tipi}")
    st.markdown("---")

    # ── 3. Önceki sonuçları göster ──
    onceki_oturumlar = [o for o in store.load_objects("test_oturumlari")
                        if o.ogrenci_id == stu_id and o.test_id == test.id]
    if onceki_oturumlar:
        tamamlanan = [o for o in onceki_oturumlar if o.durum == "TAMAMLANDI"]
        st.markdown(f"**Bu test daha önce {len(tamamlanan)} kez uygulanmış.**")

    # ── 4. Soruları Göster ve Cevapla ──
    st.markdown(f"### {test.test_adi}")
    st.markdown(f"*{test.test_kategorisi} — {len(sorular)} soru*")

    cevaplar = {}
    sorted_sorular = sorted(sorular, key=lambda s: s.sira if hasattr(s, 'sira') else 0)

    for si, soru in enumerate(sorted_sorular):
        soru_metin = soru.metin if hasattr(soru, 'metin') else soru.to_dict().get("metin", f"Soru {si+1}")
        soru_id = soru.id if hasattr(soru, 'id') else soru.to_dict().get("id", f"s_{si}")
        olcek = soru.olcek if hasattr(soru, 'olcek') else soru.to_dict().get("olcek", "")

        if test.soru_tipi == "LIKERT":
            likert_opts = ["1 — Hiç Katılmıyorum", "2 — Katılmıyorum", "3 — Kararsızım",
                           "4 — Katılıyorum", "5 — Tamamen Katılıyorum"]
            val = st.radio(f"**{si+1}.** {soru_metin}", likert_opts,
                           key=f"btu_q_{stu_id}_{test.id}_{si}", horizontal=True)
            puan = int(val[0]) if val else 0
            # Ters madde
            ters = soru.ters if hasattr(soru, 'ters') else soru.to_dict().get("ters", False)
            if ters:
                puan = 6 - puan
            cevaplar[soru_id] = {"puan": puan, "cevap": val, "olcek": olcek}
        elif test.soru_tipi == "EVET_HAYIR":
            val = st.radio(f"**{si+1}.** {soru_metin}", ["Evet", "Hayır"],
                           key=f"btu_q_{stu_id}_{test.id}_{si}", horizontal=True)
            puan = 1 if val == "Evet" else 0
            ters = soru.ters if hasattr(soru, 'ters') else soru.to_dict().get("ters", False)
            if ters:
                puan = 1 - puan
            cevaplar[soru_id] = {"puan": puan, "cevap": val, "olcek": olcek}
        else:
            val = st.text_input(f"**{si+1}.** {soru_metin}", key=f"btu_q_{stu_id}_{test.id}_{si}")
            cevaplar[soru_id] = {"puan": 0, "cevap": val, "olcek": olcek}

    # ── 5. Kaydet ──
    st.markdown("---")
    if st.button("💾 Testi Tamamla ve Kaydet", type="primary", use_container_width=True,
                 key=f"btu_save_{stu_id}_{test.id}"):
        from models.rehberlik import TestOturumu, TestCevap, _gen_id, _now

        # Oturum oluştur
        oturum = TestOturumu(
            test_id=test.id,
            ogrenci_id=stu_id,
            ogrenci_adi=stu_name,
            ogrenci_no=str(stu_data.get("numara", "")),
            sinif_sube=f"{stu_data.get('sinif', '')}/{stu_data.get('sube', '')}",
            durum="TAMAMLANDI",
            baslangic_zamani=_now(),
            bitis_zamani=_now(),
        )
        store.upsert("test_oturumlari", oturum)

        # Cevapları kaydet
        for soru_id, cvp in cevaplar.items():
            tc = TestCevap(
                oturum_id=oturum.id,
                test_id=test.id,
                soru_id=soru_id,
                ogrenci_id=stu_id,
                secilen_cevap=str(cvp.get("cevap", "")),
                puan=float(cvp.get("puan", 0)),
            )
            store.upsert("test_cevaplari", tc)

        # Ölçek bazlı özet hesapla
        olcek_toplam: dict[str, list] = {}
        for cvp in cevaplar.values():
            olc = cvp.get("olcek", "Genel")
            olcek_toplam.setdefault(olc, []).append(cvp["puan"])

        genel_puan = sum(c["puan"] for c in cevaplar.values())
        max_puan = len(cevaplar) * 5 if test.soru_tipi == "LIKERT" else len(cevaplar)

        st.success(f"✅ Test tamamlandı: {test.test_adi} — {stu_name}")
        st.markdown(f"**Toplam Puan:** {genel_puan}/{max_puan}")

        # Ölçek bazlı sonuçlar
        if olcek_toplam:
            st.markdown("**Ölçek Bazlı Sonuçlar:**")
            for olc, puanlar in sorted(olcek_toplam.items()):
                ort = sum(puanlar) / len(puanlar)
                st.markdown(f"- **{olc}:** Ort {ort:.1f} ({len(puanlar)} soru)")

        st.balloons()
        st.info("Sonuçlar kaydedildi. Öğrenci 360°, Erken Uyarı ve AI Destek'te otomatik görünecek.")


# ---------- Sub-tab 7b: Kayıt Modülü Testleri (Paylaşımlı) ----------

def _render_kayit_testleri():
    """Kayıt Modülü test türlerini (9 tür) rehberlik'ten uygula + sonuçları göster.
    Testler öğrenci seçerek uygulanır, sonuçlar kayıt modülü store'una kaydedilir.
    Böylece Öğrenci 360° ve tüm veri modülleri otomatik erişir."""
    styled_header("Test Uygula & Sonuçlar", "Çoklu Zeka, VARK, Seviye Tespit, CEFR, HHT-1, Checkup (9 Tür)", icon="🧪")

    st.markdown(
        '<div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;'
        'padding:12px 16px;border-radius:10px;margin-bottom:12px;">'
        '<p style="margin:0;font-size:.85rem;opacity:.9;">'
        'Bu testler Kayıt Modülü\'ndeki aynı test motorunu kullanır. '
        'Sonuçlar hem burada hem Kayıt Modülü\'nde görünür ve Öğrenci 360°\'a akar.</p></div>',
        unsafe_allow_html=True,
    )

    sub1, sub2 = st.tabs(["🧪 Test Uygula", "📊 Test Sonuçları"])

    # ── TAB 1: TEST UYGULA ──
    with sub1:
        # Öğrenci seçimi (shared_data'dan)
        try:
            from utils.shared_data import get_student_display_options
            students = get_student_display_options(include_empty=False)
        except Exception:
            students = {}

        if not students:
            st.warning("Öğrenci bulunamadı. Akademik Takip > Sınıf Listesi'nden öğrenci ekleyin.")
            return

        sel = st.selectbox("Öğrenci Seçin:", [""] + list(students.keys()), key="rhb_kt_stu_sel")
        if not sel:
            st.info("Test uygulamak için bir öğrenci seçin.")
            return

        stu = students.get(sel, {})
        stu_name = f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip()
        stu_id = stu.get("id", "")

        # Kayıt Modülü store'u üzerinden aday bul/oluştur
        try:
            from models.kayit_modulu import KayitDataStore, KayitAday, TEST_TURLERI
            from views.kayit_modulu import _render_genel_test, _save_test_result
            _km_store = KayitDataStore(_get_km_base_path())
            tum_adaylar = _km_store.load_all()

            # Öğrenci adıyla eşleşen aday bul
            aday = None
            for a in tum_adaylar:
                if stu_name.upper() in a.ogrenci_adi.upper():
                    aday = a
                    break

            # Yoksa yeni kayıt oluştur (sessizce)
            if not aday:
                aday = KayitAday(
                    ogrenci_adi=stu_name,
                    kademe=f"{stu.get('sinif', '')}. Sınıf",
                    hedef_sinif=str(stu.get('sinif', '')),
                    asama="Kayitli Ogrenci",
                )
                tum_adaylar.append(aday)
                _km_store.save_all(tum_adaylar)

            # Mevcut testleri göster
            if aday.testler:
                st.markdown(f"**Uygulanan testler ({len(aday.testler)}):**")
                for ti, t in enumerate(aday.testler):
                    st.markdown(f"- 🧪 **{t.get('test_adi', '?')}** — {str(t.get('tarih', ''))[:10]} ({t.get('sonuc', '-')})")

            # Test seçimi
            st.markdown("---")
            test_sec = st.selectbox("Test Türü Seçin:", TEST_TURLERI, key=f"rhb_kt_test_{stu_id}")

            # Test uygula
            _render_genel_test(_km_store, aday, test_sec)

        except ImportError:
            st.error("Kayıt Modülü yüklenemedi. Testleri Kayıt Modülü üzerinden uygulayabilirsiniz.")
        except Exception as e:
            st.error(f"Test yükleme hatası: {e}")

    # ── TAB 2: TÜM TEST SONUÇLARI ──
    with sub2:
        try:
            from models.erken_uyari import CrossModuleLoader
            all_tests = CrossModuleLoader.load_all_student_tests()
        except Exception:
            all_tests = []

        if not all_tests:
            st.info("Henüz test sonucu yok.")
            return

        # İstatistik
        test_types = {}
        for t in all_tests:
            tn = t.get("test_adi", "?")
            test_types[tn] = test_types.get(tn, 0) + 1

        rhb_cnt = sum(1 for t in all_tests if "Rehberlik" in t.get("kaynak", ""))
        km_cnt = sum(1 for t in all_tests if "Kayit" in t.get("kaynak", ""))
        st.markdown(f"**Toplam: {len(all_tests)} test | Rehberlik: {rhb_cnt} | Kayıt: {km_cnt} | {len(test_types)} tür**")

        cols = st.columns(min(len(test_types), 4))
        for i, (tn, cnt) in enumerate(sorted(test_types.items(), key=lambda x: -x[1])):
            with cols[i % len(cols)]:
                st.metric(tn[:25], cnt)

        st.markdown("---")

        # Öğrenci filtresi
        ogrenciler = sorted(set(t.get("ogrenci_adi", "?") for t in all_tests if t.get("ogrenci_adi")))
        sel_ogr = st.selectbox("Öğrenci Filtrele:", ["Tümü"] + ogrenciler, key="rhb_kt_ogr")
        filtered = all_tests if sel_ogr == "Tümü" else [t for t in all_tests if t.get("ogrenci_adi") == sel_ogr]

        for t in sorted(filtered, key=lambda x: x.get("tarih", ""), reverse=True):
            ogr = t.get("ogrenci_adi", "?")
            test_adi = t.get("test_adi", "?")
            tarih = str(t.get("tarih", ""))[:10]
            durum = t.get("durum", "-")
            kaynak = t.get("kaynak", "?")
            k_clr = "#2dd4bf" if "Rehberlik" in kaynak else "#a78bfa"

            with st.expander(f"🧪 {ogr} — {test_adi} ({tarih})"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"**Test:** {test_adi}")
                    st.markdown(f"**Durum:** {durum}")
                    st.markdown(f"**Kaynak:** :{('green' if 'Rehberlik' in kaynak else 'violet')}[{kaynak}]")
                    st.markdown(f"**Tarih:** {tarih}")
                    if t.get("genel_ortalama"):
                        st.markdown(f"**Genel Ortalama:** {t['genel_ortalama']}")
                with c2:
                    top3 = t.get("top3", [])
                    if top3:
                        st.markdown("**En Güçlü 3 Alan:**")
                        for item in top3:
                            st.markdown(f"- **{item.get('alan', '?')}:** {item.get('skor', '-')} ({item.get('seviye', '')})")

                skorlar = t.get("skorlar", {})
                if skorlar:
                    st.markdown("**Skor Detayı:**")
                    skor_cols = st.columns(min(len(skorlar), 4))
                    for si, (sk, sv) in enumerate(skorlar.items()):
                        with skor_cols[si % len(skor_cols)]:
                            try:
                                val = float(sv)
                                clr = "green" if val >= 7 else "orange" if val >= 5 else "red"
                                st.markdown(f":{clr}[**{sk}:** {sv}]")
                            except (ValueError, TypeError):
                                st.markdown(f"**{sk}:** {sv}")
                olcek_p = t.get("olcek_puanlari", {})
                if olcek_p:
                    st.markdown("**Ölçek Puanları:**")
                    for ok, ov in olcek_p.items():
                        st.markdown(f"- {ok}: {ov}")


def _get_km_base_path() -> str:
    """Kayıt modülü data path — tenant-aware."""
    try:
        from models.erken_uyari import _find_tenant_path
        p = _find_tenant_path("kayit_modulu")
        return str(p) if p else "data/kayit_modulu"
    except Exception:
        return "data/kayit_modulu"


# ---------- TAB 1: TEST OLUSTUR & UYGULA (Sade Akis) ----------

def _render_test_olustur_uygula(store: RehberlikDataStore):
    """Test Seç → Sınıf/Şube → Süre → Oluştur → Aktifleştir. Tek ekranda."""
    styled_header("Test Oluştur & Uygula", "Test seçin, sınıf/şube belirleyin, öğrencilere uygulayın", icon="🧪")

    # ── ADIM 1: Test Seç (Havuzdan) ──
    st.markdown("### 1. Test Seçin")
    from models.test_havuzu import HAZIR_TEST_KATALOGU, HAVUZ_KATEGORILERI

    # Kategori filtresi
    kat_list = ["Tümü"] + list(HAVUZ_KATEGORILERI.keys())
    sel_kat = st.selectbox("Kategori:", kat_list, key="tou_kat")

    if sel_kat == "Tümü":
        test_pool = HAZIR_TEST_KATALOGU
    else:
        keys = HAVUZ_KATEGORILERI.get(sel_kat, [])
        test_pool = [t for t in HAZIR_TEST_KATALOGU if t["key"] in keys]

    test_options = {t["key"]: f'{t["test_adi"]} ({len(t["sorular"])} soru — {t["kategori"]})' for t in test_pool}
    sel_test_key = st.selectbox("Test:", list(test_options.keys()),
                                 format_func=lambda x: test_options[x], key="tou_test")
    sel_test = next((t for t in HAZIR_TEST_KATALOGU if t["key"] == sel_test_key), None)

    if sel_test:
        st.markdown(f'<div style="background:#0d948815;border-left:3px solid #0d9488;padding:8px 12px;'
                    f'border-radius:0 8px 8px 0;margin:6px 0;font-size:13px;">'
                    f'<b>{sel_test["test_adi"]}</b> — {sel_test["kategori"]} | '
                    f'{len(sel_test["sorular"])} soru | {sel_test["soru_tipi"]} | '
                    f'{sel_test["hedef_kitle"]} | ~{sel_test["sure_dakika"]} dk<br>'
                    f'<span style="color:#64748b;font-size:11px;">{sel_test["aciklama"]}</span></div>',
                    unsafe_allow_html=True)

    # ── ADIM 2: Sınıf / Şube / Süre ──
    st.markdown("### 2. Uygulama Bilgileri")
    c1, c2, c3 = st.columns(3)
    with c1:
        _SINIFLAR = [f"{i}. Sınıf" for i in range(1, 13)]
        hedef_sinif = st.multiselect("Sınıf:", _SINIFLAR, key="tou_sinif")
    with c2:
        _SUBELER = ["Tümü", "A", "B", "C", "D", "E", "F"]
        hedef_sube = st.selectbox("Şube:", _SUBELER, key="tou_sube")
    with c3:
        sure = st.number_input("Süre (dk, 0=süresiz):", min_value=0, max_value=180,
                               value=sel_test["sure_dakika"] if sel_test else 15, key="tou_sure")

    c4, c5 = st.columns(2)
    with c4:
        uygulama_tarihi = st.date_input("Uygulama Tarihi:", value=date.today(), key="tou_tarih")
    with c5:
        staff = get_staff_name_list()
        uygulayan = st.selectbox("Uygulayan:", [""] + staff, key="tou_uygulayan")

    # ── ADIM 3: Oluştur ──
    st.markdown("### 3. Testi Oluştur ve Aktifleştir")
    if st.button("🧪 Testi Oluştur & Aktifleştir", type="primary", use_container_width=True, key="tou_create"):
        if not sel_test:
            st.error("Test seçin.")
            return
        if not hedef_sinif:
            st.error("En az bir sınıf seçin.")
            return

        # Test kaydı oluştur
        kod = store.next_test_code()
        erisim = _generate_test_erisim_kodu()
        kayit = TestEnvanter(
            test_kodu=kod,
            test_adi=sel_test["test_adi"],
            test_kategorisi=sel_test["kategori"],
            uygulama_tarihi=uygulama_tarihi.isoformat() if uygulama_tarihi else "",
            hedef_siniflar=hedef_sinif,
            hedef_sube=hedef_sube if hedef_sube != "Tümü" else "",
            uygulayan=uygulayan,
            soru_tipi=sel_test["soru_tipi"],
            sure_dakika=sure,
            olcekler=sel_test.get("olcekler", []),
            erisim_kodu=erisim,
            online_aktif=True,  # Direkt aktif
        )
        store.upsert("testler", kayit)

        # Soruları otomatik ekle
        for soru in sel_test["sorular"]:
            from models.rehberlik import TestSorusu
            ts = TestSorusu(
                test_id=kayit.id,
                sira=soru["sira"],
                metin=soru["metin"],
                olcek=soru.get("olcek", ""),
                ters=soru.get("ters", False),
            )
            store.upsert("test_sorulari", ts)

        st.success(f"✅ Test oluşturuldu ve aktifleştirildi!")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#7c3aed,#a78bfa);color:#fff;
            padding:16px 20px;border-radius:12px;margin:10px 0;text-align:center;">
            <div style="font-size:14px;">Öğrencilere bu kodu verin:</div>
            <div style="font-size:28px;font-weight:800;letter-spacing:4px;margin:8px 0;">{erisim}</div>
            <div style="font-size:12px;opacity:.8;">Öğrenciler "💻 Öğrenci Test Giriş" sekmesinden bu kodla teste girecek</div>
        </div>""", unsafe_allow_html=True)
        st.rerun()

    # ── AKTİF TESTLER LİSTESİ ──
    st.markdown("---")
    st.markdown("### Aktif Testler")
    testler = store.load_objects("testler")
    aktif = [t for t in testler if t.online_aktif]
    if not aktif:
        st.info("Henüz aktif test yok.")
    for t in sorted(aktif, key=lambda x: x.uygulama_tarihi or "", reverse=True):
        oturumlar = store.find_by_field("test_oturumlari", "test_id", t.id)
        tamamlanan = sum(1 for o in oturumlar if o.durum == "TAMAMLANDI")
        with st.expander(f"🧪 {t.test_adi} — Kod: **{t.erisim_kodu}** | {tamamlanan} öğrenci tamamladı"):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"**Sınıf:** {', '.join(t.hedef_siniflar)}")
                st.markdown(f"**Şube:** {t.hedef_sube or 'Tümü'}")
            with c2:
                st.markdown(f"**Süre:** {t.sure_dakika} dk")
                st.markdown(f"**Tarih:** {t.uygulama_tarihi}")
            with c3:
                st.markdown(f"**Uygulayan:** {t.uygulayan}")
                st.markdown(f"**Tamamlayan:** {tamamlanan}")
            # Pasifleştir butonu
            if st.button("⏹ Testi Kapat", key=f"tou_close_{t.id}"):
                t.online_aktif = False
                store.upsert("testler", t)
                st.success("Test kapatıldı.")
                st.rerun()

    # Pasif testler
    pasif = [t for t in testler if not t.online_aktif]
    if pasif:
        with st.expander(f"📋 Tamamlanan/Kapatılan Testler ({len(pasif)})"):
            for t in pasif:
                oturumlar = store.find_by_field("test_oturumlari", "test_id", t.id)
                tamamlanan = sum(1 for o in oturumlar if o.durum == "TAMAMLANDI")
                st.markdown(f"- {t.test_adi} ({t.test_kategorisi}) — {tamamlanan} öğrenci | Kod: {t.erisim_kodu}")


# ---------- TAB 3: SONUCLAR BİRLEŞİK ----------

def _render_test_sonuclar_birlesik(store: RehberlikDataStore):
    """Tüm test sonuçları — Rehberlik + Kayıt birleşik."""
    styled_header("Test Sonuçları", "Rehberlik Testleri + Kayıt Modülü Testleri — Birleşik Görünüm", icon="📊")

    # Rehberlik test sonuçları
    testler = store.load_objects("testler")
    oturumlar = store.load_objects("test_oturumlari")
    cevaplar = store.load_objects("test_cevaplari")
    tst_map = {t.id: t for t in testler}
    tamamlanan = [o for o in oturumlar if o.durum == "TAMAMLANDI"]

    # Kayıt testleri
    try:
        from models.erken_uyari import CrossModuleLoader
        kayit_tests = CrossModuleLoader.load_kayit_testler()
    except Exception:
        kayit_tests = []

    # İstatistik
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Rehberlik Testleri", f"{len(tamamlanan)} tamamlanan")
    with c2:
        st.metric("Kayıt Testleri", f"{len(kayit_tests)} sonuç")
    with c3:
        st.metric("Toplam", f"{len(tamamlanan) + len(kayit_tests)}")

    st.markdown("---")

    # Öğrenci filtresi
    ogr_set = set()
    for o in tamamlanan:
        if o.ogrenci_adi:
            ogr_set.add(o.ogrenci_adi)
    for t in kayit_tests:
        if t.get("ogrenci_adi"):
            ogr_set.add(t["ogrenci_adi"])

    sel_ogr = st.selectbox("Öğrenci Filtrele:", ["Tümü"] + sorted(ogr_set), key="tsb_ogr")

    # ── Rehberlik Sonuçları ──
    if tamamlanan:
        st.markdown("#### 🧠 Rehberlik Test Sonuçları")
        for o in sorted(tamamlanan, key=lambda x: x.bitis_zamani or "", reverse=True):
            if sel_ogr != "Tümü" and o.ogrenci_adi != sel_ogr:
                continue
            tst = tst_map.get(o.test_id)
            tst_adi = tst.test_adi if tst else "?"
            oc = [c for c in cevaplar if c.oturum_id == o.id]
            pp = [c.puan for c in oc if c.puan]
            avg = sum(pp) / len(pp) if pp else 0

            with st.expander(f"🧠 {o.ogrenci_adi} — {tst_adi} ({str(o.bitis_zamani or '')[:10]})"):
                st.markdown(f"**Test:** {tst_adi} | **Cevap:** {len(oc)} | **Ortalama:** {avg:.1f}")
                st.markdown(f"**Sınıf:** {o.sinif_sube} | **Tarih:** {str(o.bitis_zamani or '')[:10]}")
                # Ölçek bazlı
                if oc and tst:
                    olcek_map: dict[str, list] = {}
                    sorular = store.find_by_field("test_sorulari", "test_id", o.test_id)
                    soru_olcek = {s.id: (s.olcek if hasattr(s, 'olcek') else "") for s in sorular}
                    for c in oc:
                        olc = soru_olcek.get(c.soru_id, "Genel")
                        olcek_map.setdefault(olc, []).append(c.puan)
                    if olcek_map:
                        st.markdown("**Ölçek Bazlı:**")
                        for olc, plist in sorted(olcek_map.items()):
                            ort = sum(plist) / len(plist)
                            clr = "green" if ort >= 3.5 else "orange" if ort >= 2.5 else "red"
                            st.markdown(f"- :{clr}[**{olc}:** {ort:.1f}] ({len(plist)} soru)")

    # ── Kayıt Test Sonuçları ──
    if kayit_tests:
        st.markdown("#### 🧪 Kayıt Modülü Test Sonuçları")
        for t in sorted(kayit_tests, key=lambda x: x.get("tarih", ""), reverse=True):
            if sel_ogr != "Tümü" and t.get("ogrenci_adi") != sel_ogr:
                continue
            with st.expander(f"🧪 {t.get('ogrenci_adi', '?')} — {t.get('test_adi', '?')} ({str(t.get('tarih', ''))[:10]})"):
                st.markdown(f"**Test:** {t.get('test_adi', '?')} | **Sonuç:** {t.get('sonuc', '-')}")
                skorlar = t.get("skorlar", {})
                if skorlar:
                    st.markdown("**Skorlar:**")
                    for sk, sv in skorlar.items():
                        try:
                            val = float(sv)
                            clr = "green" if val >= 7 else "orange" if val >= 5 else "red"
                            st.markdown(f"- :{clr}[**{sk}:** {sv}]")
                        except (ValueError, TypeError):
                            st.markdown(f"- **{sk}:** {sv}")
                top3 = t.get("top3", [])
                if top3:
                    st.markdown("**En Güçlü 3:**")
                    for item in top3:
                        st.markdown(f"- **{item.get('alan', '?')}:** {item.get('skor', '-')} ({item.get('seviye', '')})")

    if not tamamlanan and not kayit_tests:
        st.info("Henüz test sonucu yok.")


# ---------- ESKİ Sub-tab 0: Test Havuzu ----------

def _render_test_havuzu(store: RehberlikDataStore):
    # --- Kurumsal Başlık ---
    styled_header("Test Havuzu", "Hazır Psikolojik Test ve Envanter Kataloğu", "🧠")

    # --- Veri hazırla ---
    katalog = get_katalog_ozet()
    importer = HavuzImporter(store)
    toplam = len(HAZIR_TEST_KATALOGU)
    aktarilan = sum(1 for t in HAZIR_TEST_KATALOGU if importer.is_already_imported(t["test_adi"]))

    # --- KPI Kartları ---
    styled_stat_row([
        ("Toplam Test", str(toplam), "#7c3aed", "📋"),
        ("Sisteme Aktarılan", str(aktarilan), "#10b981", "✅"),
        ("Bekleyen", str(toplam - aktarilan), "#f59e0b", "⏳"),
        ("Kategori", str(len(HAVUZ_KATEGORILERI)), "#2563eb", "🗂️"),
    ])

    st.markdown("")

    # --- Bilgi Banner ---
    styled_info_banner(
        "Rehberlik hizmetlerinde sık kullanılan standart psikolojik testler. "
        "Bir testi seçip sisteme aktarabilir, online uygulayabilir veya PDF olarak indirebilirsiniz.",
        "info", "📖"
    )

    st.markdown("")

    # --- Filtre Alanı ---
    styled_section("Filtre ve Arama", "#7c3aed")
    _flt_c1, _flt_c2 = st.columns([1, 1])
    with _flt_c1:
        kategori_sec = st.selectbox(
            "Kategori Filtresi",
            ["Tümü"] + list(HAVUZ_KATEGORILERI.keys()),
            key="hvz_kategori_filtre",
        )
    with _flt_c2:
        durum_sec = st.selectbox(
            "Durum Filtresi",
            ["Tümü", "Aktarılanlar", "Bekleyenler"],
            key="hvz_durum_filtre",
        )

    # Filtreleme uygula
    if kategori_sec != "Tümü":
        aktif_keys = HAVUZ_KATEGORILERI.get(kategori_sec, [])
        katalog = [k for k in katalog if k["key"] in aktif_keys]

    if durum_sec == "Aktarılanlar":
        katalog = [k for k in katalog if importer.is_already_imported(k["test_adi"])]
    elif durum_sec == "Bekleyenler":
        katalog = [k for k in katalog if not importer.is_already_imported(k["test_adi"])]

    st.markdown("")

    # --- Kategori renk haritası ---
    _KAT_RENK = {
        "Kaygı": ("#ef4444", "#fef2f2"), "Kişilik": ("#7c3aed", "#f5f3ff"),
        "Diğer": ("#64748b", "#111827"), "Yetenek": ("#2563eb", "#eff6ff"),
        "İlgi": ("#0d9488", "#f0fdfa"), "Depresyon": ("#f59e0b", "#fffbeb"),
        "Stres": ("#ea580c", "#fff7ed"), "Tarama": ("#6d28d9", "#f5f3ff"),
        "Sosyal": ("#0891b2", "#ecfeff"), "İletişim": ("#059669", "#ecfdf5"),
    }
    _TIP_RENK = {"LIKERT": "#7c3aed", "EVET_HAYIR": "#0d9488", "MCQ": "#2563eb"}

    # --- Test Kataloğu ---
    styled_section(f"Test Kataloğu ({len(katalog)} test)", "#6d28d9")

    if not katalog:
        styled_info_banner("Seçilen filtrelere uygun test bulunamadı.", "warning")
    else:
        for i, item in enumerate(katalog):
            havuz_data = get_hazir_test(item["key"])
            if not havuz_data:
                continue

            already = importer.is_already_imported(item["test_adi"])
            kat_renk, kat_bg = _KAT_RENK.get(item["kategori"], ("#64748b", "#111827"))
            tip_renk = _TIP_RENK.get(item["soru_tipi"], "#64748b")

            # Expander başlığı
            durum_icon = "✅" if already else "📝"
            exp_label = f"{durum_icon}  {item['test_adi']}  —  {item['kategori']}  ·  {item['soru_sayisi']} Soru"

            with st.expander(exp_label, expanded=False):
                # Üst bilgi kartı
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,{kat_bg},white);
                    border:1px solid {kat_renk}25;border-radius:12px;padding:16px 20px;margin-bottom:12px;">
                    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:10px;">
                        <span style="background:{kat_renk};color:white;padding:3px 12px;
                            border-radius:20px;font-size:12px;font-weight:600;">{item['kategori']}</span>
                        <span style="background:{tip_renk};color:white;padding:3px 12px;
                            border-radius:20px;font-size:12px;font-weight:600;">
                            {SORU_TIPI_LABEL.get(item["soru_tipi"], item["soru_tipi"])}</span>
                        {"<span style='background:#10b981;color:white;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:600;'>✓ Sisteme Aktarıldı</span>" if already else "<span style='background:#f59e0b;color:white;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:600;'>Bekliyor</span>"}
                    </div>
                    <div style="font-size:14px;color:#334155;line-height:1.6;">{item['aciklama']}</div>
                    <div style="display:flex;gap:16px;margin-top:10px;flex-wrap:wrap;">
                        <span style="color:#64748b;font-size:12px;">📊 <b>{item['olcek_sayisi']}</b> Alt Ölçek</span>
                        <span style="color:#64748b;font-size:12px;">🎯 <b>{item['hedef_kitle']}</b></span>
                        <span style="color:#64748b;font-size:12px;">📝 <b>{item.get('soru_sayisi', 0)}</b> Soru</span>
                        <span style="color:#64748b;font-size:12px;">⏱️ <b>{havuz_data.get('sure_dakika', 0)}</b> dk</span>
                    </div>
                </div>""", unsafe_allow_html=True)

                # Alt ölçekler
                if havuz_data.get("olcekler"):
                    olcek_chips = " ".join(
                        f'<span style="background:linear-gradient(135deg,{kat_bg},{kat_renk}15);'
                        f'border:1px solid {kat_renk}30;padding:4px 12px;border-radius:20px;'
                        f'font-size:12px;color:{kat_renk};font-weight:600;">{o}</span>'
                        for o in havuz_data["olcekler"]
                    )
                    st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <div style="font-size:12px;color:#94a3b8;font-weight:600;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Alt Ölçekler</div>
                        <div style="display:flex;gap:6px;flex-wrap:wrap;">{olcek_chips}</div>
                    </div>""", unsafe_allow_html=True)

                # Örnek sorular
                st.markdown("""<div style="font-size:12px;color:#94a3b8;font-weight:600;margin-bottom:6px;
                    text-transform:uppercase;letter-spacing:0.5px;">Örnek Sorular</div>""", unsafe_allow_html=True)
                for si, s in enumerate(havuz_data["sorular"][:5]):
                    ters_badge = (' <span style="background:#f59e0b20;color:#d97706;padding:1px 6px;'
                                  'border-radius:4px;font-size:10px;font-weight:600;">Ters</span>') if s.get("ters") else ""
                    olcek_tag = (f' <span style="color:#94a3b8;font-size:11px;">({s.get("olcek", "")})</span>')
                    st.markdown(f"""<div style="padding:6px 12px;background:{'#111827' if si % 2 == 0 else 'white'};
                        border-radius:6px;margin-bottom:2px;font-size:13px;color:#334155;">
                        <span style="color:{kat_renk};font-weight:700;margin-right:6px;">{s['sira']}.</span>
                        {s['metin']}{ters_badge}{olcek_tag}
                    </div>""", unsafe_allow_html=True)
                if len(havuz_data["sorular"]) > 5:
                    st.caption(f"... ve {len(havuz_data['sorular']) - 5} soru daha")

                st.markdown("")

                # Aksiyon butonları
                _ac1, _ac2, _ac3 = st.columns(3)
                with _ac1:
                    if already:
                        st.markdown("""<div style="background:#10b98115;color:#059669;padding:10px;
                            border-radius:8px;text-align:center;font-size:13px;font-weight:600;">
                            ✅ Bu test zaten sisteme aktarıldı</div>""", unsafe_allow_html=True)
                    else:
                        if st.button("📥 Sisteme Aktar", key=f"hvz_import_{item['key']}",
                                     type="primary", use_container_width=True):
                            importer.import_test(havuz_data)
                            st.success(f"Test başarıyla aktarıldı! ({item['soru_sayisi']} soru)")
                            st.rerun()

                with _ac2:
                    if st.button("📄 PDF İndir", key=f"hvz_pdf_{item['key']}",
                                 use_container_width=True):
                        tmp_test = TestEnvanter(
                            test_adi=havuz_data["test_adi"],
                            test_kategorisi=havuz_data["kategori"],
                            soru_tipi=havuz_data["soru_tipi"],
                            olcekler=havuz_data.get("olcekler", []),
                            sure_dakika=havuz_data.get("sure_dakika", 0),
                        )
                        tmp_sorular = []
                        for s in havuz_data["sorular"]:
                            tmp_sorular.append(TestSorusu(
                                sira_no=s["sira"],
                                soru_metni=s["metin"],
                                soru_tipi=havuz_data["soru_tipi"],
                                olcek=s.get("olcek", "Genel"),
                                ters_puanlama=s.get("ters", False),
                            ))
                        try:
                            from utils.report_utils import get_institution_info
                            _info = get_institution_info()
                            kurum = _info.get("name", "")
                            logo = _info.get("logo_path", "")
                        except Exception:
                            kurum, logo = "", ""
                        pdf_bytes = TestPDFExporter.generate_test_pdf(tmp_test, tmp_sorular, kurum, logo)
                        st.session_state[f"hvz_pdf_data_{item['key']}"] = pdf_bytes
                        st.rerun()

                with _ac3:
                    pdf_data = st.session_state.get(f"hvz_pdf_data_{item['key']}")
                    if pdf_data:
                        safe_name = item["test_adi"].replace(" ", "_").replace("(", "").replace(")", "")
                        st.download_button(
                            "💾 Kaydet",
                            data=pdf_data,
                            file_name=f"{safe_name}.pdf",
                            mime="application/pdf",
                            key=f"hvz_dl_{item['key']}",
                            use_container_width=True,
                        )


# ---------- Sub-tab 1: Yeni Test ----------

def _render_yeni_test(store: RehberlikDataStore):
    styled_section("Yeni Test/Envanter", "#0d9488")
    c1, c2 = st.columns(2)
    with c1:
        test_adi = st.text_input("Test Adi", key="tst_adi")
        test_kategorisi = st.selectbox("Kategori", TEST_KATEGORILERI, key="tst_kategori")
        uygulama_tarihi = st.date_input("Uygulama Tarihi", value=date.today(), key="tst_tarih")
        soru_tipi = st.selectbox("Soru Tipi", SORU_TIPLERI,
                                  format_func=lambda x: SORU_TIPI_LABEL.get(x, x),
                                  key="tst_soru_tipi")
    with c2:
        _TUM_SINIFLAR = ["Tümü", "Anasınıfı"] + [f"{i}. Sınıf" for i in range(1, 13)]
        _TUM_SUBELER = ["A", "B", "C", "D", "E", "F"]
        hedef_siniflar = st.multiselect("Hedef Sınıflar", _TUM_SINIFLAR, key="tst_siniflar")
        hedef_sube = st.selectbox("Hedef Şube", ["Tümü"] + _TUM_SUBELER, key="tst_sube")
        staff = get_staff_name_list()
        uygulayan = st.selectbox("Uygulayan", [""] + staff, key="tst_uygulayan")
        sure_dakika = st.number_input("Sure (dakika, 0=suresiz)", min_value=0,
                                       max_value=180, value=0, key="tst_sure")

    olcekler_text = st.text_input("Alt Olcekler (virgul ile ayirin)",
                                   placeholder="Kaygi, Depresyon, Sosyal, Ozguven",
                                   key="tst_olcekler")
    ey = st.selectbox("Egitim Yili", EGITIM_YILI_SECENEKLERI, index=1, key="tst_ey")

    if st.button("Test Kaydet", type="primary", use_container_width=True, key="tst_kaydet"):
        if not test_adi.strip():
            st.error("Test adi bos birakilamaz.")
            return
        kod = store.next_test_code()
        olcekler = [o.strip() for o in olcekler_text.split(",") if o.strip()] if olcekler_text else []
        kayit = TestEnvanter(
            test_kodu=kod,
            test_adi=test_adi,
            test_kategorisi=test_kategorisi,
            uygulama_tarihi=uygulama_tarihi.isoformat() if uygulama_tarihi else "",
            hedef_siniflar=hedef_siniflar,
            hedef_sube=hedef_sube if hedef_sube != "Tümü" else "",
            uygulayan=uygulayan,
            egitim_yili=ey,
            soru_tipi=soru_tipi,
            sure_dakika=sure_dakika,
            olcekler=olcekler,
            erisim_kodu=_generate_test_erisim_kodu(),
        )
        store.upsert("testler", kayit)
        st.success(f"Test kaydedildi: {kod} | Erisim Kodu: {kayit.erisim_kodu}")
        st.rerun()


# ---------- Sub-tab 2: Soru Oluştur ----------

def _render_soru_olustur(store: RehberlikDataStore):
    styled_section("Soru Oluştur / Düzenle", "#7c3aed")

    testler = store.load_objects("testler")
    if not testler:
        styled_info_banner("Henuz test kaydi yok. Önce 'Yeni Test' sekmesinden test olusturun.")
        return

    test_opts = {t.id: f"{t.test_kodu} - {t.test_adi} ({SORU_TIPI_LABEL.get(t.soru_tipi, t.soru_tipi)})"
                 for t in testler}
    test_id = st.selectbox("Test Secin", list(test_opts.keys()),
                           format_func=lambda x: test_opts[x], key="soru_test_sec")
    test = store.get_by_id("testler", test_id)
    if not test:
        return

    mevcut_sorular = store.find_by_field("test_sorulari", "test_id", test_id)
    mevcut_sorular.sort(key=lambda s: s.sira_no)

    if mevcut_sorular:
        st.markdown(f"**Mevcut Soru Sayısı:** {len(mevcut_sorular)}")
        with st.expander("Mevcut Sorulari Gor", expanded=False):
            for s in mevcut_sorular:
                col1, col2, col3 = st.columns([1, 6, 1])
                with col1:
                    st.markdown(f"**{s.sira_no}.**")
                with col2:
                    tip_l = SORU_TIPI_LABEL.get(s.soru_tipi, s.soru_tipi)
                    olcek_l = f" [{s.olcek}]" if s.olcek else ""
                    ters_l = " (Ters)" if s.ters_puanlama else ""
                    st.markdown(f"{s.soru_metni} `{tip_l}`{olcek_l}{ters_l}")
                with col3:
                    if confirm_action("Sil", "Bu test sorusunu silmek istediğinize emin misiniz?", key=f"soru_sil_{s.id}"):
                        store.delete_by_id("test_sorulari", s.id)
                        st.rerun()

    st.divider()
    styled_section("Yeni Soru Ekle", "#0d9488")

    soru_tipi = st.selectbox("Soru Tipi", SORU_TIPLERI,
                              format_func=lambda x: SORU_TIPI_LABEL.get(x, x),
                              index=SORU_TIPLERI.index(test.soru_tipi) if test.soru_tipi in SORU_TIPLERI else 0,
                              key="yeni_soru_tipi")

    soru_metni = st.text_area("Soru Metni", key="yeni_soru_metin", height=80)

    c1, c2 = st.columns(2)
    with c1:
        olcek_opts = ["Genel"] + (test.olcekler if test.olcekler else [])
        olcek = st.selectbox("Alt Olcek", olcek_opts, key="yeni_soru_olcek")
    with c2:
        sira_no = st.number_input("Sira No", min_value=1,
                                   value=len(mevcut_sorular) + 1, key="yeni_soru_sira")

    secenekler: list[dict] = []
    dogru_cevap = ""
    ters_puanlama = False

    if soru_tipi == "LIKERT":
        ters_puanlama = st.checkbox("Ters Puanlama", key="yeni_soru_ters")
        st.caption("Secenekler: 1-Kesinlikle Katilmiyorum ... 5-Kesinlikle Katiliyorum")
        secenekler = [dict(s) for s in LIKERT_SECENEKLER]

    elif soru_tipi == "EVET_HAYIR":
        st.caption("Secenekler: Evet / Hayir")
        secenekler = [dict(s) for s in EVET_HAYIR_SECENEKLER]

    elif soru_tipi == "MCQ":
        st.markdown("**Secenekler:**")
        for letter in ["A", "B", "C", "D"]:
            metin = st.text_input(f"Secenek {letter}", key=f"yeni_soru_sec_{letter}")
            secenekler.append({"label": letter, "metin": metin})
        dogru_cevap = st.selectbox("Dogru Cevap", ["A", "B", "C", "D"], key="yeni_soru_dogru")

    if st.button("Soru Ekle", type="primary", use_container_width=True, key="soru_ekle_btn"):
        if not soru_metni.strip():
            st.error("Soru metni bos birakilamaz.")
            return
        yeni_soru = TestSorusu(
            test_id=test_id,
            sira_no=sira_no,
            soru_metni=soru_metni,
            soru_tipi=soru_tipi,
            secenekler=secenekler,
            olcek=olcek if olcek != "Genel" else "",
            ters_puanlama=ters_puanlama,
            dogru_cevap=dogru_cevap,
        )
        store.upsert("test_sorulari", yeni_soru)
        st.success(f"Soru #{sira_no} eklendi.")
        st.rerun()

    # Toplu soru ekleme
    st.divider()
    with st.expander("Toplu Soru Ekleme (Hızlı Mod)"):
        st.caption("Her satira bir soru yazin. Alt olcek için | ayirici kullanin: Soru metni|Olcek")
        bulk_text = st.text_area("Sorular", height=200, key="bulk_soru_text",
                                  placeholder="Kendimi endiselti hissediyorum|Kaygi\nBaskalarina guveniyorum|Guven")
        if st.button("Toplu Ekle", key="bulk_soru_ekle"):
            lines = [l.strip() for l in bulk_text.split("\n") if l.strip()]
            start_sira = len(mevcut_sorular) + 1
            count = 0
            for i, line in enumerate(lines):
                parts = line.split("|")
                metin = parts[0].strip()
                olcek_val = parts[1].strip() if len(parts) > 1 else ""
                if not metin:
                    continue
                if soru_tipi == "LIKERT":
                    sec = [dict(s) for s in LIKERT_SECENEKLER]
                elif soru_tipi == "EVET_HAYIR":
                    sec = [dict(s) for s in EVET_HAYIR_SECENEKLER]
                else:
                    sec = []
                soru = TestSorusu(
                    test_id=test_id,
                    sira_no=start_sira + i,
                    soru_metni=metin,
                    soru_tipi=soru_tipi,
                    secenekler=sec,
                    olcek=olcek_val,
                )
                store.upsert("test_sorulari", soru)
                count += 1
            st.success(f"{count} soru eklendi.")
            st.rerun()


# ---------- Sub-tab 3: Test Listesi ----------

def _render_test_listesi(store: RehberlikDataStore):
    styled_section("Test Listesi", "#0d9488")
    testler = store.load_objects("testler")
    if not testler:
        styled_info_banner("Henuz test kaydi yok.")
        return

    c1, c2 = st.columns(2)
    with c1:
        f_kategori = st.selectbox("Kategori", ["Tümü"] + TEST_KATEGORILERI, key="tst_f_kategori")
    with c2:
        f_durum = st.selectbox("Durum", ["Tümü"] + TEST_DURUMLARI,
                               format_func=lambda x: TEST_DURUM_LABEL.get(x, x) if x != "Tümü" else x,
                               key="tst_f_durum")

    filtered = testler
    if f_kategori != "Tümü":
        filtered = [t for t in filtered if t.test_kategorisi == f_kategori]
    if f_durum != "Tümü":
        filtered = [t for t in filtered if t.durum == f_durum]

    filtered.sort(key=lambda t: t.uygulama_tarihi, reverse=True)

    for t in filtered:
        soru_sayisi = len(store.find_by_field("test_sorulari", "test_id", t.id))
        badge = f" | {soru_sayisi} soru" if soru_sayisi else ""
        online_badge = " | ONLINE AKTIF" if t.online_aktif else ""
        with st.expander(f"{t.test_kodu} | {t.test_adi} - {t.test_kategorisi} ({TEST_DURUM_LABEL.get(t.durum, t.durum)}){badge}{online_badge}"):
            st.markdown(f"""
            **Tarih:** {t.uygulama_tarihi} | **Uygulayan:** {t.uygulayan}
            **Hedef Siniflar:** {', '.join(t.hedef_siniflar) if t.hedef_siniflar else 'Tumu'}
            **Soru Tipi:** {SORU_TIPI_LABEL.get(t.soru_tipi, t.soru_tipi)} | **Sure:** {f'{t.sure_dakika} dk' if t.sure_dakika else 'Suresiz'}
            **Katilimci:** {t.katilimci_sayisi} | **Durum:** {TEST_DURUM_LABEL.get(t.durum, t.durum)}
            """)
            if t.olcekler:
                st.markdown(f"**Alt Olcekler:** {', '.join(t.olcekler)}")
            if t.genel_degerlendirme:
                st.markdown(f"**Genel Değerlendirme:** {t.genel_degerlendirme}")

            # Online test yonetimi
            st.markdown("---")
            st.markdown("**Online Test Yönetimi:**")
            if soru_sayisi == 0:
                st.warning("Bu teste henuz soru eklenmedi. 'Soru Oluştur' sekmesinden soru ekleyin.")
            else:
                online_durumu = st.toggle("Online Test Aktif", value=t.online_aktif, key=f"tst_online_{t.id}")
                if online_durumu != t.online_aktif:
                    t.online_aktif = online_durumu
                    if online_durumu and not t.erisim_kodu:
                        t.erisim_kodu = _generate_test_erisim_kodu()
                    t.updated_at = _now()
                    store.upsert("testler", t)
                    st.rerun()

                if t.online_aktif:
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg, #10b981, #059669); padding:16px;
                        border-radius:12px; color:white; text-align:center; margin:8px 0;">
                        <div style="font-size:14px;">Erisim Kodu</div>
                        <div style="font-size:28px; font-weight:bold; letter-spacing:4px; font-family:monospace;">
                            {t.erisim_kodu}
                        </div>
                    </div>""", unsafe_allow_html=True)

                    if st.button("Kodu Yenile", key=f"tst_kod_yenile_{t.id}"):
                        t.erisim_kodu = _generate_test_erisim_kodu()
                        t.updated_at = _now()
                        store.upsert("testler", t)
                        st.rerun()

                    oturumlar = store.find_by_field("test_oturumlari", "test_id", t.id)
                    tamamlanan = len([o for o in oturumlar if o.durum == "TAMAMLANDI"])
                    st.metric("Katilim", f"{tamamlanan} / {len(oturumlar)}")

            # PDF indirme butonu
            if soru_sayisi > 0:
                st.markdown("---")
                st.markdown("**PDF Export:**")
                pc1, pc2 = st.columns(2)
                with pc1:
                    if st.button("PDF Oluştur", key=f"tst_pdf_{t.id}", use_container_width=True):
                        test_sorulari = store.find_by_field("test_sorulari", "test_id", t.id)
                        try:
                            from utils.report_utils import get_institution_info
                            _info = get_institution_info()
                            kurum = _info.get("name", "")
                            logo = _info.get("logo_path", "")
                        except Exception:
                            kurum, logo = "", ""
                        pdf_data = TestPDFExporter.generate_test_pdf(t, test_sorulari, kurum, logo)
                        st.session_state[f"tst_pdf_data_{t.id}"] = pdf_data
                        st.rerun()
                with pc2:
                    pdf_d = st.session_state.get(f"tst_pdf_data_{t.id}")
                    if pdf_d:
                        safe = t.test_adi.replace(" ", "_").replace("(", "").replace(")", "")
                        st.download_button("PDF Indir", data=pdf_d,
                                           file_name=f"{safe}.pdf",
                                           mime="application/pdf",
                                           key=f"tst_dl_{t.id}",
                                           use_container_width=True)

            st.markdown("---")
            yeni_durum = st.selectbox("Durum Güncelle", TEST_DURUMLARI,
                                      format_func=lambda x: TEST_DURUM_LABEL.get(x, x),
                                      index=TEST_DURUMLARI.index(t.durum) if t.durum in TEST_DURUMLARI else 0,
                                      key=f"tst_durum_{t.id}")
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button("Durumu Güncelle", key=f"tst_dgunc_{t.id}"):
                    t.durum = yeni_durum
                    t.updated_at = _now()
                    store.upsert("testler", t)
                    st.success("Test güncellendi.")
                    st.rerun()
            with cc2:
                if st.button("Sil", key=f"tst_sil_{t.id}", type="secondary"):
                    store.delete_by_id("testler", t.id)
                    st.success("Test silindi.")
                    st.rerun()


# ---------- Sub-tab 4: Online Test ----------

def _clear_ptest_state():
    for k in list(st.session_state.keys()):
        if k.startswith("ptest_"):
            del st.session_state[k]


def _save_test_progress(store: RehberlikDataStore, oturum: TestOturumu, sorular: list):
    for soru in sorular:
        secilen = st.session_state.get("ptest_cevaplar", {}).get(soru.id, "")
        if secilen:
            existing = None
            for c in store.find_by_field("test_cevaplari", "oturum_id", oturum.id):
                if c.soru_id == soru.id:
                    existing = c
                    break
            if existing:
                existing.secilen_cevap = secilen
                existing.cevaplanma_zamani = _now()
                store.upsert("test_cevaplari", existing)
            else:
                cevap = TestCevap(
                    oturum_id=oturum.id,
                    test_id=oturum.test_id,
                    soru_id=soru.id,
                    ogrenci_id=oturum.ogrenci_id,
                    secilen_cevap=secilen,
                )
                store.upsert("test_cevaplari", cevap)


def _submit_test(store: RehberlikDataStore, oturum: TestOturumu, test: TestEnvanter, sorular: list):
    _save_test_progress(store, oturum, sorular)
    oturum.durum = "TAMAMLANDI"
    oturum.bitis_zamani = _now()
    try:
        start = datetime.fromisoformat(oturum.baslangic_zamani)
        oturum.toplam_sure = int((datetime.now() - start).total_seconds())
    except Exception:
        pass
    store.upsert("test_oturumlari", oturum)

    deg = TestDegerlendirici(store)
    result = deg.grade_oturum(oturum.id)

    test_obj = store.get_by_id("testler", test.id)
    if test_obj:
        if not test_obj.sonuclar:
            test_obj.sonuclar = []
        test_obj.sonuclar.append(result)
        test_obj.katilimci_sayisi = len(test_obj.sonuclar)
        test_obj.updated_at = _now()
        store.upsert("testler", test_obj)

    st.session_state.ptest_result = result
    st.session_state.ptest_started = False


def _render_test_sonucu_ogrenci():
    result = st.session_state.get("ptest_result", {})
    if not result:
        return
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #7c3aed, #a78bfa); padding:24px;
        border-radius:16px; color:white; text-align:center; margin-bottom:20px;">
        <div style="font-size:22px; font-weight:bold;">Test Tamamlandı</div>
        <div style="font-size:16px; margin-top:8px;">{result.get('ogrenci_adi', '')}</div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Puan", result.get("toplam_puan", 0))
    c2.metric("Cevaplanan", result.get("cevap_sayisi", 0))
    c3.metric("Bos", result.get("bos_sayisi", 0))

    if result.get("basari_yuzdesi") is not None:
        st.metric("Başarı Yuzdesi", f"%{result['basari_yuzdesi']:.1f}")

    if result.get("olcek_puanlari"):
        styled_section("Olcek Bazli Sonuclariniz", "#7c3aed")
        for olcek, puan in result["olcek_puanlari"].items():
            yorum = result.get("olcek_yorumlari", {}).get(olcek, "")
            renk = {"Çok Yuksek": "#ef4444", "Yuksek": "#f59e0b", "Orta": "#64748b",
                    "Dusuk": "#10b981", "Çok Dusuk": "#2563eb"}.get(yorum, "#64748b")
            st.markdown(f"**{olcek}:** {puan} "
                       f"<span style='background:{renk};color:white;padding:2px 8px;"
                       f"border-radius:4px;font-weight:bold;'>{yorum}</span>",
                       unsafe_allow_html=True)

    if st.button("Yeni Test Coz", type="primary", key="ptest_yeni"):
        _clear_ptest_state()
        st.rerun()


def _render_test_cozme(store: RehberlikDataStore):
    oturum = st.session_state.ptest_oturum
    test = store.get_by_id("testler", oturum.test_id)
    if not test:
        st.error("Test bulunamadı!")
        return

    sorular = store.find_by_field("test_sorulari", "test_id", test.id)
    sorular.sort(key=lambda s: s.sira_no)

    if not sorular:
        st.error("Bu testte soru bulunamadı!")
        return

    # Countdown timer
    if test.sure_dakika > 0:
        from datetime import timedelta
        start_time = datetime.fromisoformat(oturum.baslangic_zamani)
        end_time = start_time + timedelta(minutes=test.sure_dakika)
        now = datetime.now()
        remaining_seconds = int((end_time - now).total_seconds())

        if remaining_seconds <= 0:
            _submit_test(store, oturum, test, sorular)
            st.rerun()
            return

        mins = remaining_seconds // 60
        secs = remaining_seconds % 60
        if remaining_seconds <= 60:
            timer_color = "#dc3545"
        elif remaining_seconds <= 300:
            timer_color = "#fd7e14"
        elif remaining_seconds <= 600:
            timer_color = "#ffc107"
        else:
            timer_color = "#7c3aed"

        timer_html = f"""
        <div style="text-align:center;padding:12px;background:{timer_color};
            border-radius:12px;color:white;font-size:24px;font-weight:bold;">
            Kalan Sure: {mins:02d}:{secs:02d}
        </div>
        """
        st.markdown(timer_html, unsafe_allow_html=True)

    # Header
    st.markdown(f"### {test.test_adi}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Öğrenci", oturum.ogrenci_adi)
    c2.metric("Sınıf", oturum.sinif_sube)
    c3.metric("Soru", len(sorular))
    st.divider()

    # Init answers dict
    if "ptest_cevaplar" not in st.session_state:
        st.session_state.ptest_cevaplar = {}

    # Questions
    for soru in sorular:
        st.markdown(f"**{soru.sira_no}.** {soru.soru_metni}")
        current_answer = st.session_state.ptest_cevaplar.get(soru.id, "")

        if soru.soru_tipi == "LIKERT":
            options = [str(s["deger"]) for s in LIKERT_SECENEKLER]
            labels_map = {str(s["deger"]): s["label"] for s in LIKERT_SECENEKLER}
            idx = options.index(current_answer) if current_answer in options else None
            selected = st.radio(
                f"soru_{soru.sira_no}",
                options=options,
                format_func=lambda x, lm=labels_map: lm.get(x, x),
                index=idx,
                horizontal=True,
                key=f"ptest_q_{soru.id}",
                label_visibility="collapsed",
            )
            if selected:
                st.session_state.ptest_cevaplar[soru.id] = selected

        elif soru.soru_tipi == "EVET_HAYIR":
            cols = st.columns(2)
            for i, opt in enumerate(["Evet", "Hayir"]):
                with cols[i]:
                    is_sel = current_answer == opt
                    btn_type = "primary" if is_sel else "secondary"
                    if st.button(opt, key=f"ptest_q_{soru.id}_{opt}",
                                use_container_width=True, type=btn_type):
                        st.session_state.ptest_cevaplar[soru.id] = opt
                        st.rerun()

        elif soru.soru_tipi == "MCQ":
            choice_cols = st.columns(4)
            for i, choice in enumerate(["A", "B", "C", "D"]):
                with choice_cols[i]:
                    is_sel = current_answer == choice
                    metin = ""
                    for sec in soru.secenekler:
                        if sec.get("label") == choice:
                            metin = sec.get("metin", "")
                            break
                    btn_label = f"{choice}) {metin[:40]}" if metin else choice
                    if st.button(btn_label, key=f"ptest_q_{soru.id}_{choice}",
                                use_container_width=True,
                                type="primary" if is_sel else "secondary"):
                        st.session_state.ptest_cevaplar[soru.id] = choice
                        st.rerun()

        st.markdown("---")

    # Progress
    answered = sum(1 for s in sorular if st.session_state.ptest_cevaplar.get(s.id))
    total = len(sorular)
    st.progress(answered / total if total > 0 else 0)
    st.markdown(f"**Cevaplanan:** {answered} / {total}")

    if answered < total:
        bos_sorular = [str(s.sira_no) for s in sorular if not st.session_state.ptest_cevaplar.get(s.id)]
        st.warning(f"Bos sorular: {', '.join(bos_sorular)}")

    # Action buttons
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        if st.button("Testi Tamamla", type="primary", use_container_width=True, key="ptest_submit"):
            _submit_test(store, oturum, test, sorular)
            st.rerun()
    with col2:
        if st.button("Kaydet (Devam Et)", use_container_width=True, key="ptest_save"):
            _save_test_progress(store, oturum, sorular)
            st.success("Cevaplar kaydedildi!")
    with col3:
        if st.button("Çıkış", use_container_width=True, key="ptest_exit"):
            _clear_ptest_state()
            st.rerun()


def _render_online_test(store: RehberlikDataStore):
    # Init session state
    if "ptest_oturum" not in st.session_state:
        st.session_state.ptest_oturum = None
    if "ptest_started" not in st.session_state:
        st.session_state.ptest_started = False
    if "ptest_cevaplar" not in st.session_state:
        st.session_state.ptest_cevaplar = {}
    if "ptest_result" not in st.session_state:
        st.session_state.ptest_result = None

    # Show result if completed
    if st.session_state.ptest_result:
        _render_test_sonucu_ogrenci()
        return

    # Show test-taking if started
    if st.session_state.ptest_oturum and st.session_state.ptest_started:
        _render_test_cozme(store)
        return

    # Phase 1: Access code entry
    if not st.session_state.get("ptest_verified_id"):
        st.markdown("""<div style="background:linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
            padding:30px; border-radius:16px; text-align:center; color:white; margin-bottom:20px;">
            <div style="font-size:20px; font-weight:bold;">Psikolojik Test</div>
            <div style="font-size:14px; opacity:0.9;">Rehber ogretmeninizden aldiginiz erisim kodunu girin</div>
        </div>""", unsafe_allow_html=True)

        code_col1, code_col2 = st.columns([3, 1])
        with code_col1:
            access_code = st.text_input("Erisim Kodu", key="ptest_erisim_kodu",
                                         label_visibility="collapsed").strip().upper()
        with code_col2:
            verify_btn = st.button("Testi Bul", type="primary", use_container_width=True)


        if verify_btn and access_code:
            testler = store.load_objects("testler")
            found = None
            for t in testler:
                if getattr(t, "erisim_kodu", "") == access_code and t.online_aktif:
                    found = t
                    break
            if found:
                st.session_state["ptest_verified_id"] = found.id
                st.rerun()
            else:
                st.error("Gecersiz erisim kodu veya test aktif degil!")
        return

    # Phase 2: Student info + start
    test = store.get_by_id("testler", st.session_state["ptest_verified_id"])
    if not test or not test.online_aktif:
        st.error("Test artik aktif degil!")
        del st.session_state["ptest_verified_id"]
        st.rerun()
        return

    sorular = store.find_by_field("test_sorulari", "test_id", test.id)
    st.markdown(f"""<div style="background:linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        padding:20px; border-radius:12px; color:white; margin-bottom:16px;">
        <div style="font-size:22px; font-weight:bold;">{test.test_adi}</div>
        <div style="display:flex; gap:30px; margin-top:12px;">
            <span>{test.test_kategorisi}</span>
            <span>{len(sorular)} soru</span>
            <span>{f'{test.sure_dakika} dakika' if test.sure_dakika > 0 else 'Suresiz'}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Student selection
    students = load_shared_students()
    if not students:
        st.warning("Sistemde ogrenci kaydi bulunamadı.")
        return

    stu_options = get_student_display_options(students)
    with st.form("ptest_ogrenci_form"):
        stu_idx = st.selectbox("Öğrenci Seçin", range(len(stu_options)),
                               format_func=lambda i: stu_options[i], key="ptest_stu_idx")

        st.warning(f"""**Onemli Bilgiler:**
- Bu {'sureli (' + str(test.sure_dakika) + ' dk)' if test.sure_dakika > 0 else 'suresiz'} bir psikolojik testtir.
- Tum sorulari dikkatlice okuyun ve ictenlikle cevaplayin.
- Dogru veya yanlis cevap yoktur (kendinizi en iyi ifade eden secenegi secin).
{'- Sure bitiminde test otomatik kapanir.' if test.sure_dakika > 0 else ''}""")

        if st.form_submit_button("Testi Baslat", type="primary"):
            stu = students[stu_idx]
            ogr_id = stu.get("id", "")
            existing = store.get_test_oturumu_by_student(ogr_id, test.id)

            if existing and existing.durum == "TAMAMLANDI":
                st.error("Bu testi daha once tamamladiniz!")
            elif existing and existing.durum == "DEVAM":
                st.session_state.ptest_oturum = existing
                st.session_state.ptest_started = True
                mevcut_cevaplar = store.find_by_field("test_cevaplari", "oturum_id", existing.id)
                st.session_state.ptest_cevaplar = {c.soru_id: c.secilen_cevap for c in mevcut_cevaplar}
                st.rerun()
            else:
                oturum = TestOturumu(
                    test_id=test.id,
                    ogrenci_id=ogr_id,
                    ogrenci_adi=_get_student_full_name(stu),
                    ogrenci_no=str(stu.get("numara", "")),
                    sinif_sube=_get_student_sinif_sube(stu),
                    durum="DEVAM",
                    baslangic_zamani=_now(),
                )
                store.upsert("test_oturumlari", oturum)
                st.session_state.ptest_oturum = oturum
                st.session_state.ptest_started = True
                st.session_state.ptest_cevaplar = {}
                st.rerun()


# ---------- Sub-tab 5: Sonuclar ----------

def _render_sonuclar(store: RehberlikDataStore):
    styled_section("Sonuclar", "#0d9488")

    # Kurumsal kunye
    st.markdown(_kurumsal_header_html(), unsafe_allow_html=True)

    testler = store.load_objects("testler")
    if not testler:
        styled_info_banner("Henuz test kaydi yok.")
        return

    test_opts = {t.id: f"{t.test_kodu} - {t.test_adi}" for t in testler}
    test_id = st.selectbox("Test Secin", list(test_opts.keys()),
                           format_func=lambda x: test_opts[x], key="sonuc_test_sec")
    test = store.get_by_id("testler", test_id)
    if not test:
        return

    mode = st.radio("Mod", ["Online Sonuclar", "Manuel Sonuc Girişi"], horizontal=True, key="sonuc_mod")

    if mode == "Online Sonuclar":
        oturumlar = store.find_by_field("test_oturumlari", "test_id", test_id)
        tamamlanan = [o for o in oturumlar if o.durum == "TAMAMLANDI"]

        if not tamamlanan:
            styled_info_banner("Henuz tamamlanmis online oturum yok.")
            return

        rows = []
        for o in tamamlanan:
            result = next((r for r in (test.sonuclar or [])
                          if r.get("oturum_id") == o.id), None)
            rows.append({
                "Öğrenci": o.ogrenci_adi,
                "Sınıf/Şube": o.sinif_sube,
                "Sure (sn)": o.toplam_sure,
                "Toplam Puan": result.get("toplam_puan", "-") if result else "-",
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

        for o in tamamlanan:
            result = next((r for r in (test.sonuclar or []) if r.get("oturum_id") == o.id), None)
            if result:
                with st.expander(f"{o.ogrenci_adi} ({o.sinif_sube}) - Puan: {result.get('toplam_puan', '-')}"):
                    if result.get("olcek_puanlari"):
                        for olcek, puan in result["olcek_puanlari"].items():
                            yorum = result.get("olcek_yorumlari", {}).get(olcek, "")
                            renk = {"Çok Yuksek": "#ef4444", "Yuksek": "#f59e0b", "Orta": "#64748b",
                                    "Dusuk": "#10b981", "Çok Dusuk": "#2563eb"}.get(yorum, "#64748b")
                            st.markdown(f"**{olcek}:** {puan} "
                                       f"<span style='background:{renk};color:white;padding:2px 8px;"
                                       f"border-radius:4px;'>{yorum}</span>",
                                       unsafe_allow_html=True)
                    if result.get("basari_yuzdesi") is not None:
                        st.metric("Başarı", f"%{result['basari_yuzdesi']:.1f}")

    else:
        # Manuel sonuc girisi (mevcut mantik)
        testler_aktif = [t for t in testler if t.durum in ("PLANLANDI", "UYGULANDI", "DEGERLENDIRME")]
        if not testler_aktif or test.durum not in ("PLANLANDI", "UYGULANDI", "DEGERLENDIRME"):
            styled_info_banner("Bu test için manuel sonuc girisi yapilamaz.")
            return

        st.markdown(f"**{test.test_kodu} - {test.test_adi}** ({test.test_kategorisi})")

        all_students = load_shared_students()
        stu_filtered = all_students
        if test.hedef_siniflar:
            stu_filtered = [s for s in stu_filtered if str(s.get("sinif", "")) in test.hedef_siniflar]
        if test.hedef_sube:
            stu_filtered = [s for s in stu_filtered if s.get("sube", "") == test.hedef_sube]

        if not stu_filtered:
            styled_info_banner("Hedef sinif/subede ogrenci bulunamadı.")
            return

        mevcut_sonuclar = {s.get("ogrenci_id", ""): s for s in (test.sonuclar or [])
                          if isinstance(s, dict) and "ogrenci_id" in s}
        sonuc_data = []
        for stu in stu_filtered:
            ogr_id = stu.get("id", "")
            ogr_adi = _get_student_full_name(stu)
            sinif_sube = _get_student_sinif_sube(stu)
            mevcut = mevcut_sonuclar.get(ogr_id, {})

            cc1, cc2, cc3 = st.columns([3, 2, 3])
            with cc1:
                st.markdown(f"**{ogr_adi}** ({sinif_sube})")
            with cc2:
                puan = st.number_input("Puan", min_value=0, max_value=100,
                                       value=int(mevcut.get("puan", 0)),
                                       key=f"tst_p_{test.id}_{ogr_id}")
            with cc3:
                yorum = st.text_input("Yorum", value=mevcut.get("yorum", ""),
                                      key=f"tst_y_{test.id}_{ogr_id}")
            sonuc_data.append({
                "ogrenci_id": ogr_id,
                "ogrenci_adi": ogr_adi,
                "sinif_sube": sinif_sube,
                "puan": puan,
                "yorum": yorum,
            })

        genel_deg = st.text_area("Genel Değerlendirme", value=test.genel_degerlendirme or "", key="tst_genel_deg")

        if st.button("Sonuclari Kaydet", type="primary", use_container_width=True, key="tst_sonuc_kaydet"):
            # Mevcut online sonuclari koru, sadece manuel sonuclari guncelle
            online_sonuclar = [s for s in (test.sonuclar or []) if isinstance(s, dict) and "oturum_id" in s]
            test.sonuclar = online_sonuclar + sonuc_data
            test.katilimci_sayisi = len([s for s in sonuc_data if s.get("puan", 0) > 0]) + len(online_sonuclar)
            test.genel_degerlendirme = genel_deg
            if test.durum == "PLANLANDI":
                test.durum = "UYGULANDI"
            test.updated_at = _now()
            store.upsert("testler", test)
            st.success("Sonuclar kaydedildi.")
            st.rerun()


# ---------- Sub-tab 6: Sonuç Analizi ----------

def _kurumsal_header_html() -> str:
    """Kurumsal kunye header HTML'i."""
    try:
        info = get_institution_info()
        name = info.get("name", "")
        logo_path = info.get("logo_path", "")
    except Exception:
        name, logo_path = "", ""
    if not name:
        name = "Psikolojik Danismanlik Birimi"
    logo_html = ""
    if logo_path and os.path.exists(logo_path):
        import base64
        try:
            with open(logo_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            ext = logo_path.rsplit(".", 1)[-1].lower()
            mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "svg": "image/svg+xml"}.get(ext, "image/png")
            logo_html = f'<img src="data:{mime};base64,{b64}" style="height:48px;border-radius:8px;margin-right:14px;" />'
        except Exception:
            pass
    return f"""<div style="display:flex;align-items:center;gap:4px;margin-bottom:12px;padding:12px 18px;
        background:linear-gradient(135deg,#111827,#e2e8f0);border-radius:12px;border:1px solid #e2e8f0;">
        {logo_html}
        <div>
            <div style="font-size:16px;font-weight:700;color:#94A3B8;">{name}</div>
            <div style="font-size:12px;color:#64748b;">Rehberlik ve Psikolojik Danismanlik Servisi</div>
        </div>
    </div>"""


def _render_sonuc_analizi(store: RehberlikDataStore):
    styled_section("Sonuç Analizi", "#2563eb")

    # Kurumsal kunye
    st.markdown(_kurumsal_header_html(), unsafe_allow_html=True)

    testler = store.load_objects("testler")
    completed_tests = [t for t in testler if t.sonuclar]
    if not completed_tests:
        styled_info_banner("Henuz sonuc bulunan test yok.")
        return

    test_opts = {t.id: f"{t.test_kodu} - {t.test_adi}" for t in completed_tests}
    test_id = st.selectbox("Test Secin", list(test_opts.keys()),
                           format_func=lambda x: test_opts[x], key="analiz_test_sec")
    test = store.get_by_id("testler", test_id)
    if not test or not test.sonuclar:
        return

    # Filter results
    online_results = [r for r in test.sonuclar if isinstance(r, dict) and "oturum_id" in r]
    manuel_results = [r for r in test.sonuclar if isinstance(r, dict) and "oturum_id" not in r and "puan" in r]
    all_results = online_results + manuel_results

    if not all_results:
        styled_info_banner("Analiz için yeterli veri yok.")
        return

    # KPI
    toplam = len(all_results)
    if online_results and online_results[0].get("toplam_puan") is not None:
        ort_puan = sum(r.get("toplam_puan", 0) for r in online_results) / len(online_results)
    elif manuel_results:
        puanlar = [r.get("puan", 0) for r in manuel_results if r.get("puan", 0) > 0]
        ort_puan = sum(puanlar) / len(puanlar) if puanlar else 0
    else:
        ort_puan = 0

    styled_stat_row([
        ("Katilimci", str(toplam), "#7c3aed", "\U0001F4CA"),
        ("Ort. Puan", f"{ort_puan:.1f}", "#2563eb", "\U0001F4C8"),
        ("Online", str(len(online_results)), "#10b981", "\U0001F310"),
        ("Manuel", str(len(manuel_results)), "#f59e0b", "\u270D\uFE0F"),
    ])

    st.divider()

    from utils.report_utils import ReportStyler

    # Subscale analysis (only for online results with olcek data)
    if online_results and online_results[0].get("olcek_puanlari"):
        olcek_names = list(online_results[0]["olcek_puanlari"].keys())

        if olcek_names:
            styled_section("Olcek Bazli Analiz", "#7c3aed")

            # Average per subscale
            avg_per_olcek: dict[str, float] = {}
            for olcek in olcek_names:
                scores = [r["olcek_puanlari"].get(olcek, 0) for r in online_results if r.get("olcek_puanlari")]
                avg_per_olcek[olcek] = sum(scores) / len(scores) if scores else 0

            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                st.markdown("**Olcek Ortalama Puanlari**")
                bar_html = ReportStyler.horizontal_bar_html(
                    {k: round(v, 1) for k, v in avg_per_olcek.items()}, "#7c3aed"
                )
                st.markdown(bar_html, unsafe_allow_html=True)

            with col_chart2:
                # Sunburst chart: ic halka = olcekler, dis halka = ogrenci bazli
                st.markdown("**Olcek Dagilimi (Sunburst)**")
                inner_data = {k: round(v, 1) for k, v in avg_per_olcek.items()}
                outer_data: dict[str, list[tuple[str, float]]] = {}
                for olcek in olcek_names:
                    items = []
                    for r in online_results:
                        ogr_adi = r.get("ogrenci_adi", "?")
                        val = r.get("olcek_puanlari", {}).get(olcek, 0)
                        if val > 0:
                            items.append((ogr_adi, round(val, 1)))
                    if items:
                        outer_data[olcek] = items
                sunburst_html = ReportStyler.sunburst_chart_svg(
                    inner_data, outer_data, title=test.test_adi
                )
                st.markdown(sunburst_html, unsafe_allow_html=True)

            # Interpretation distribution
            st.divider()
            styled_section("Yorum Dagilimi", "#0d9488")

            yorum_dist: dict[str, float] = {}
            for r in online_results:
                for _olcek, yorum in r.get("olcek_yorumlari", {}).items():
                    yorum_dist[yorum] = yorum_dist.get(yorum, 0) + 1

            # Olcek bazli yorum dagilimlari
            olcek_yorum_dist: dict[str, dict[str, int]] = {}
            for r in online_results:
                for olcek, yorum in r.get("olcek_yorumlari", {}).items():
                    if olcek not in olcek_yorum_dist:
                        olcek_yorum_dist[olcek] = {}
                    olcek_yorum_dist[olcek][yorum] = olcek_yorum_dist[olcek].get(yorum, 0) + 1

            if yorum_dist:
                ycol1, ycol2 = st.columns(2)
                with ycol1:
                    st.markdown("**Genel Yorum Dagilimi**")
                    yorum_renk = ["#ef4444", "#f59e0b", "#64748b", "#10b981", "#2563eb"]
                    donut_html = ReportStyler.donut_chart_svg(yorum_dist, colors=yorum_renk)
                    st.markdown(donut_html, unsafe_allow_html=True)
                with ycol2:
                    st.markdown("**Olcek Bazli Yorum Detayi**")
                    yorum_sev = {"Çok Yuksek": "#ef4444", "Yuksek": "#f59e0b",
                                 "Orta": "#64748b", "Dusuk": "#10b981", "Çok Dusuk": "#2563eb"}
                    for olcek, dist in olcek_yorum_dist.items():
                        chips = " ".join(
                            f'<span style="background:{yorum_sev.get(y, "#64748b")};color:white;'
                            f'padding:2px 8px;border-radius:6px;font-size:11px;">{y}: {c}</span>'
                            for y, c in dist.items()
                        )
                        st.markdown(f"**{olcek}:** {chips}", unsafe_allow_html=True)

    # Student ranking
    st.divider()
    styled_section("Öğrenci Sıralamasi", "#0d9488")

    rank_rows = []
    for r in online_results:
        row: dict[str, Any] = {
            "Öğrenci": r.get("ogrenci_adi", ""),
            "Toplam Puan": r.get("toplam_puan", 0),
        }
        if r.get("olcek_puanlari"):
            for k, v in r["olcek_puanlari"].items():
                row[k] = v
        rank_rows.append(row)
    for r in manuel_results:
        if r.get("puan", 0) > 0:
            rank_rows.append({
                "Öğrenci": r.get("ogrenci_adi", ""),
                "Toplam Puan": r.get("puan", 0),
            })

    if rank_rows:
        rank_rows.sort(key=lambda x: x.get("Toplam Puan", 0), reverse=True)
        for i, row in enumerate(rank_rows):
            row["Sira"] = i + 1
        df = pd.DataFrame(rank_rows)
        cols_order = ["Sira", "Öğrenci", "Toplam Puan"] + [c for c in df.columns if c not in ("Sira", "Öğrenci", "Toplam Puan")]
        df = df[[c for c in cols_order if c in df.columns]]
        st.dataframe(df, use_container_width=True)

    # Student detail expanders with colored badges
    if online_results:
        st.divider()
        styled_section("Öğrenci Detay Raporlari", "#7c3aed")
        yorum_badge_renk = {"Çok Yuksek": "#ef4444", "Yuksek": "#f59e0b",
                            "Orta": "#64748b", "Dusuk": "#10b981", "Çok Dusuk": "#2563eb"}
        for r in online_results:
            ogr_adi = r.get("ogrenci_adi", "Bilinmeyen")
            with st.expander(f"{ogr_adi} - Toplam: {r.get('toplam_puan', 0)}"):
                if r.get("olcek_puanlari"):
                    det_cols = st.columns(min(len(r["olcek_puanlari"]), 4))
                    for ci, (olcek, puan) in enumerate(r["olcek_puanlari"].items()):
                        yorum = r.get("olcek_yorumlari", {}).get(olcek, "")
                        renk = yorum_badge_renk.get(yorum, "#64748b")
                        with det_cols[ci % len(det_cols)]:
                            st.markdown(f"""
                            <div style="background:linear-gradient(135deg,{renk}15,{renk}30);
                                border:1px solid {renk}40;border-radius:10px;padding:10px;text-align:center;margin:4px 0;">
                                <div style="font-size:12px;color:#64748b;font-weight:600;">{olcek}</div>
                                <div style="font-size:20px;font-weight:800;color:{renk};">{puan}</div>
                                <span style="background:{renk};color:white;padding:2px 8px;
                                    border-radius:6px;font-size:10px;">{yorum}</span>
                            </div>""", unsafe_allow_html=True)

                # Individual PDF export
                if st.button(f"PDF Rapor Indir", key=f"analiz_pdf_{r.get('oturum_id', '')}"):
                    _generate_student_result_pdf(store, test, r)


def _generate_student_result_pdf(store: RehberlikDataStore, test: TestEnvanter, result: dict):
    """Ogrenci bazli sonuc raporu PDF'i olustur."""
    try:
        info = get_institution_info()
        kurum = info.get("name", "")
    except Exception:
        kurum = ""

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.lib import colors as rl_colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    import io as _io

    from utils.shared_data import ensure_turkish_pdf_fonts
    font_name, _ = ensure_turkish_pdf_fonts()

    buf = _io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=2*cm, rightMargin=2*cm)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("PTitle", fontName=font_name, fontSize=16,
                               leading=20, alignment=1, spaceAfter=4))
    styles.add(ParagraphStyle("PSub", fontName=font_name, fontSize=10,
                               leading=13, alignment=1, textColor="#64748b", spaceAfter=10))
    styles.add(ParagraphStyle("PBody", fontName=font_name, fontSize=10,
                               leading=14, spaceAfter=2))
    styles.add(ParagraphStyle("PSec", fontName=font_name, fontSize=13,
                               leading=16, spaceBefore=14, spaceAfter=6, textColor="#94A3B8"))

    def _t(text):
        return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    elements = []
    elements.append(Paragraph(_t(kurum or "Psikolojik Danismanlik Birimi"), styles["PSub"]))
    elements.append(Paragraph(_t("Psikolojik Test Sonuc Raporu"), styles["PTitle"]))
    elements.append(Spacer(1, 0.3*cm))

    # Ogrenci + test bilgileri
    ogr_adi = result.get("ogrenci_adi", "")
    info_rows = [
        [Paragraph(f"<b>Öğrenci:</b> {_t(ogr_adi)}", styles["PBody"]),
         Paragraph(f"<b>Test:</b> {_t(test.test_adi)}", styles["PBody"])],
        [Paragraph(f"<b>Kategori:</b> {_t(test.test_kategorisi)}", styles["PBody"]),
         Paragraph(f"<b>Soru Tipi:</b> {_t(SORU_TIPI_LABEL.get(test.soru_tipi, test.soru_tipi))}", styles["PBody"])],
        [Paragraph(f"<b>Toplam Puan:</b> {result.get('toplam_puan', '-')}", styles["PBody"]),
         Paragraph(f"<b>Cevaplanan:</b> {result.get('cevap_sayisi', '-')}", styles["PBody"])],
    ]
    info_tbl = Table(info_rows, colWidths=[8.5*cm, 8.5*cm])
    info_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, rl_colors.HexColor("#e2e8f0")),
    ]))
    elements.append(info_tbl)
    elements.append(Spacer(1, 0.5*cm))

    # Olcek puanlari tablosu
    if result.get("olcek_puanlari"):
        elements.append(Paragraph("<b>Olcek Bazli Sonuclar</b>", styles["PSec"]))
        olcek_header = [
            Paragraph("<b>Olcek</b>", styles["PBody"]),
            Paragraph("<b>Puan</b>", styles["PBody"]),
            Paragraph("<b>Yorum</b>", styles["PBody"]),
        ]
        olcek_rows = [olcek_header]
        for olcek, puan in result["olcek_puanlari"].items():
            yorum = result.get("olcek_yorumlari", {}).get(olcek, "")
            olcek_rows.append([
                Paragraph(_t(olcek), styles["PBody"]),
                Paragraph(str(puan), styles["PBody"]),
                Paragraph(_t(yorum), styles["PBody"]),
            ])
        olcek_tbl = Table(olcek_rows, colWidths=[7*cm, 4*cm, 6*cm])
        olcek_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), rl_colors.HexColor("#7c3aed")),
            ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
            ("FONTNAME", (0, 0), (-1, -1), font_name),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, rl_colors.HexColor("#e2e8f0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [rl_colors.white, rl_colors.HexColor("#111827")]),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(olcek_tbl)

    elements.append(Spacer(1, 0.5*cm))
    from datetime import datetime as _dt
    elements.append(Paragraph(
        f"<i>Rapor Tarihi: {_dt.now().strftime('%d.%m.%Y %H:%M')}</i>", styles["PSub"]
    ))

    doc.build(elements)
    buf.seek(0)
    pdf_bytes = buf.getvalue()
    safe_name = f"{ogr_adi}_{test.test_adi}".replace(" ", "_")
    st.download_button(
        "PDF Kaydet",
        data=pdf_bytes,
        file_name=f"Sonuc_Rapor_{safe_name}.pdf",
        mime="application/pdf",
        key=f"analiz_dl_{result.get('oturum_id', '')}",
    )


# ============================================================
# SEKME 8: REHBERLIK PLANI
# ============================================================

def _render_rehberlik_plani(store: RehberlikDataStore):
    sub = st.tabs(["📐 Çerçeve Planı", "➕ Plan Oluştur", "📋 Plan Listesi"])

    # ==============================================================
    #  Sub-tab 1: CERCEVE PLANI  (Kademe + Ay + Kutucuk + Performans)
    # ==============================================================
    with sub[0]:
        styled_header("MEB Rehberlik Çerçeve Planı", "Kademe bazlı yıllık rehberlik etkinlik planı ve takibi", "📋")

        from models.rehberlik import CERCEVE_KADEME_MAP

        importer = CercevePlanImporter(store)
        available = importer.get_available_files()

        KADEME_RENKLER = {
            "Anaokulu": "#f59e0b", "İlkokul": "#2563eb",
            "Ortaokul": "#10b981", "Lise": "#ef4444",
        }
        AYLAR = ["Eylul", "Ekim", "Kasim", "Aralik", "Ocak",
                 "Subat", "Mart", "Nisan", "Mayis", "Haziran"]
        AY_LABEL = {
            "Eylul": "Eylül", "Ekim": "Ekim", "Kasim": "Kasım",
            "Aralik": "Aralık", "Ocak": "Ocak", "Subat": "Şubat",
            "Mart": "Mart", "Nisan": "Nisan", "Mayis": "Mayıs",
            "Haziran": "Haziran",
        }

        # Kademe + Yıl seçimi
        styled_section("Kademe ve Eğitim Yılı Seçimi", "#7c3aed")
        c1, c2 = st.columns([2, 1])
        with c1:
            kademe_opts = list(CERCEVE_KADEME_MAP.keys())
            kademe_labels = [CERCEVE_KADEME_MAP[k] for k in kademe_opts]
            kademe_idx = st.selectbox(
                "Kademe", range(len(kademe_opts)),
                format_func=lambda i: kademe_labels[i],
                key="cp_kademe_sel",
            )
            kademe_key = kademe_opts[kademe_idx]
            kademe_name = CERCEVE_KADEME_MAP[kademe_key]
        with c2:
            ey = st.selectbox("Eğitim Yılı", EGITIM_YILI_SECENEKLERI, index=1, key="cp_ey")

        renk = KADEME_RENKLER.get(kademe_name, "#7c3aed")

        # Otomatik import: seçilen kademe için plan yoksa otomatik yükle
        planlar = store.load_objects("planlar")
        cerceve = [p for p in planlar
                   if p.hedef_kitle == kademe_name and p.plan_turu == "YILLIK"
                   and p.hazirlayan == "MEB Rehberlik" and p.egitim_yili == ey]
        if not cerceve and kademe_key in available:
            count = importer.import_kademe(kademe_key, ey)
            if count > 0:
                st.toast(f"{kademe_name}: {count} aylık plan otomatik yüklendi!")
                st.rerun()

        # Yeniden yükle (import sonrası)
        planlar = store.load_objects("planlar")
        cerceve = [p for p in planlar
                   if p.hedef_kitle == kademe_name and p.plan_turu == "YILLIK"
                   and p.hazirlayan == "MEB Rehberlik" and p.egitim_yili == ey]

        if not cerceve:
            styled_info_banner(
                f"{kademe_name} kademesi için çerçeve plan bulunamadı. "
                f"Excel dosyalarını .streamlit/ veya assets/cerceve_planlari/ klasörüne koyun.",
                "warning",
            )
            return

        # Ay bazlı planları dict'e çevir
        ay_plan_map: dict[str, RehberlikPlani] = {}
        for p in cerceve:
            if p.ay:
                ay_plan_map[p.ay] = p

        # ---- GENEL PERFORMANS KPI ----
        toplam_etkinlik = 0
        tamamlanan_etkinlik = 0
        for p in cerceve:
            for e in p.etkinlikler:
                toplam_etkinlik += 1
                if e.get("durum") == "Tamamlandı":
                    tamamlanan_etkinlik += 1
        genel_oran = round(tamamlanan_etkinlik / toplam_etkinlik * 100) if toplam_etkinlik else 0
        eksik = toplam_etkinlik - tamamlanan_etkinlik

        st.markdown("")
        styled_stat_row([
            ("Toplam Etkinlik", str(toplam_etkinlik), renk, "📋"),
            ("Tamamlanan", str(tamamlanan_etkinlik), "#10b981", "✅"),
            ("Eksik Kalan", str(eksik), "#ef4444", "⏳"),
            ("İşlenme Oranı", f"%{genel_oran}", "#7c3aed", "📊"),
        ])

        st.markdown("")

        # ---- AYLIK SEKMELER ----
        mevcut_aylar = [a for a in AYLAR if a in ay_plan_map]
        if not mevcut_aylar:
            styled_info_banner("Bu kademe için aylık plan verisi yok.", "warning")
            return

        ay_tabs = st.tabs([f"📅 {AY_LABEL.get(a, a)}" for a in mevcut_aylar])

        for tab_idx, ay_key in enumerate(mevcut_aylar):
            with ay_tabs[tab_idx]:
                plan = ay_plan_map[ay_key]
                etkinlikler = plan.etkinlikler
                if not etkinlikler:
                    styled_info_banner(f"{AY_LABEL.get(ay_key, ay_key)} için etkinlik bulunamadı.", "info")
                    continue

                # Ay bazlı istatistik
                ay_toplam = len(etkinlikler)
                ay_tamam = sum(1 for e in etkinlikler if e.get("durum") == "Tamamlandı")
                ay_oran = round(ay_tamam / ay_toplam * 100) if ay_toplam else 0

                # Ay progress bar + özet
                ay_renk = "#10b981" if ay_oran >= 80 else "#f59e0b" if ay_oran >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="background:white;border:1px solid #e2e8f0;border-radius:12px;
                    padding:14px 20px;margin-bottom:16px;display:flex;align-items:center;gap:16px;">
                  <div style="flex:1;">
                    <div style="font-size:13px;font-weight:700;color:#94A3B8;margin-bottom:6px;">
                        {AY_LABEL.get(ay_key, ay_key)} İlerleme Durumu</div>
                    <div style="background:#e2e8f0;border-radius:8px;height:10px;overflow:hidden;">
                      <div style="background:linear-gradient(90deg,{ay_renk},{ay_renk}cc);
                           width:{ay_oran}%;height:100%;border-radius:8px;transition:width 0.3s;"></div>
                    </div>
                  </div>
                  <div style="min-width:140px;text-align:right;">
                    <span style="font-weight:800;color:{ay_renk};font-size:1.3rem;">%{ay_oran}</span>
                    <div style="font-size:13px;color:#334155;font-weight:600;margin-top:2px;">
                      {ay_tamam} / {ay_toplam} Etkinlik
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

                # Kutucuklu etkinlik listesi
                changed = False
                for ei, e in enumerate(etkinlikler):
                    etk_adi = e.get("etkinlik", "")
                    etk_tarih = e.get("tarih", "")
                    etk_hedef = e.get("hedef_turu", "")
                    etk_acik = e.get("aciklama", "")
                    mevcut_durum = e.get("durum", "Planli") == "Tamamlandı"

                    cb_key = f"cp_cb_{plan.id}_{ei}"

                    # Kart bazlı satır
                    _satir_bg = "#f0fdf4" if mevcut_durum else ("#111827" if ei % 2 == 0 else "white")
                    _satir_border = "#10b981" if mevcut_durum else "#e2e8f0"
                    st.markdown(f"""<div style="background:{_satir_bg};border:1px solid {_satir_border};
                        border-radius:10px;padding:2px 0;margin-bottom:4px;"></div>""",
                        unsafe_allow_html=True)

                    col_cb, col_txt = st.columns([0.05, 0.95])
                    with col_cb:
                        yeni_durum = st.checkbox(
                            f"e{ei+1}",
                            value=mevcut_durum,
                            key=cb_key,
                            label_visibility="collapsed",
                        )
                    with col_txt:
                        if yeni_durum:
                            st.markdown(
                                f"<div style='font-size:14px;line-height:1.5;'>"
                                f"<s style='color:#64748b;font-weight:500;'>{ei+1}. {etk_adi}</s>"
                                f"<span style='margin-left:10px;font-size:11px;background:#10b981;"
                                f"color:white;padding:2px 10px;border-radius:12px;font-weight:700;'>Tamamlandı</span></div>",
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f"<div style='font-size:14px;color:#0B0F19;line-height:1.5;'>"
                                f"<span style='color:{renk};font-weight:800;margin-right:4px;'>{ei+1}.</span>"
                                f"<span style='font-weight:600;'>{etk_adi}</span></div>",
                                unsafe_allow_html=True,
                            )
                        # Detay satırları
                        detay_parts = []
                        if etk_tarih:
                            detay_parts.append(f"📅 {etk_tarih}")
                        if etk_hedef:
                            detay_parts.append(f"🎯 {etk_hedef}")
                        if etk_acik:
                            detay_parts.append(f"📝 {etk_acik}")
                        if detay_parts:
                            st.markdown(
                                f"<div style='font-size:12px;color:#475569;font-weight:500;"
                                f"margin:-6px 0 6px 20px;line-height:1.6;'>"
                                f"{'&nbsp;&nbsp;|&nbsp;&nbsp;'.join(detay_parts)}</div>",
                                unsafe_allow_html=True,
                            )

                    # Durum değişikliği tespit et
                    yeni_str = "Tamamlandı" if yeni_durum else "Planli"
                    if yeni_str != e.get("durum", "Planli"):
                        etkinlikler[ei]["durum"] = yeni_str
                        changed = True

                # Değişiklik varsa kaydet
                if changed:
                    plan.etkinlikler = etkinlikler
                    plan.updated_at = _now()
                    store.upsert("planlar", plan)
                    st.rerun()

                # Eksik kalan etkinlikler özeti
                eksikler = [e for e in etkinlikler if e.get("durum") != "Tamamlandı"]
                if eksikler and ay_oran < 100:
                    with st.expander(f"⚠️ Eksik Kalan Etkinlikler ({len(eksikler)})"):
                        for _ek_i, e in enumerate(eksikler):
                            st.markdown(
                                f"<div style='padding:6px 12px;background:{'#fef2f2' if _ek_i % 2 == 0 else 'white'};"
                                f"border-radius:6px;margin-bottom:2px;font-size:13px;color:#94A3B8;font-weight:500;'>"
                                f"<span style='color:#ef4444;font-weight:700;margin-right:6px;'>•</span>"
                                f"{e.get('etkinlik', '')}</div>",
                                unsafe_allow_html=True,
                            )

        # ============================================================
        #  GRAFIK & PERFORMANS OLCUMLERI
        # ============================================================
        st.divider()
        styled_section("Performans Analizi", renk)

        # Ay bazli veri hazirla
        _CP_BLUE = "#4472C4"
        _CP_ORANGE = "#ED7D31"
        _CP_GOLD = "#FFC000"
        _CP_GRAY = "#A5A5A5"

        ay_labels = []
        ay_toplam_list = []
        ay_tamam_list = []
        ay_eksik_list = []
        ay_oran_list = []
        for a in mevcut_aylar:
            p = ay_plan_map[a]
            t = len(p.etkinlikler)
            d = sum(1 for e in p.etkinlikler if e.get("durum") == "Tamamlandı")
            o = round(d / t * 100) if t else 0
            ay_labels.append(AY_LABEL.get(a, a))
            ay_toplam_list.append(t)
            ay_tamam_list.append(d)
            ay_eksik_list.append(t - d)
            ay_oran_list.append(o)

        # ------ SOL: Yatay Bar Grafik  |  SAG: Donut Grafik ------
        gc1, gc2 = st.columns([3, 2])

        with gc1:
            import plotly.graph_objects as go

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                y=ay_labels, x=ay_tamam_list,
                name="Tamamlanan",
                orientation="h",
                marker_color=SC_COLORS[0],
                text=[f"{v}" for v in ay_tamam_list],
                textposition="auto",
            ))
            fig_bar.add_trace(go.Bar(
                y=ay_labels, x=ay_eksik_list,
                name="Eksik",
                orientation="h",
                marker_color=SC_COLORS[1],
                text=[f"{v}" for v in ay_eksik_list],
                textposition="auto",
            ))
            fig_bar.update_layout(
                barmode="stack",
                title=dict(text="Aylık Etkinlik Durumu", font=dict(size=14, color="#94A3B8")),
                xaxis=dict(title="Etkinlik Sayısı"),
                yaxis=dict(autorange="reversed"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            sc_bar(fig_bar, height=max(320, len(mevcut_aylar) * 38 + 80), horizontal=True)
            st.plotly_chart(fig_bar, use_container_width=True, key="cp_bar", config=SC_CHART_CFG)

        with gc2:
            fig_donut = go.Figure()
            fig_donut.add_trace(go.Pie(
                labels=["Tamamlanan", "Eksik"],
                values=[tamamlanan_etkinlik, eksik],
                hole=0.55,
                marker=dict(colors=SC_COLORS[:2], line=dict(color="#fff", width=2)),
                hoverinfo="label+value+percent",
            ))
            fig_donut.update_layout(
                title=dict(text="Genel Islenme", font=dict(size=14, color="#94A3B8")),
            )
            sc_pie(fig_donut, height=320, center_text=f"<b>%{genel_oran}</b>")
            st.plotly_chart(fig_donut, use_container_width=True, key="cp_donut", config=SC_CHART_CFG)

        # ------ Aylik Islenme Orani Bar Chart (yuzdelik) ------
        fig_pct = go.Figure()
        bar_colors = [
            SC_COLORS[0] if o >= 80 else SC_COLORS[3] if o >= 50 else SC_COLORS[4]
            for o in ay_oran_list
        ]
        fig_pct.add_trace(go.Bar(
            x=ay_labels, y=ay_oran_list,
            marker_color=bar_colors,
            text=[f"%{o}" for o in ay_oran_list],
            textposition="outside",
        ))
        fig_pct.update_layout(
            title=dict(text="Aylık Islenme Orani (%)", font=dict(size=14, color="#94A3B8")),
            yaxis=dict(range=[0, 110], title="Oran (%)"),
            shapes=[dict(
                type="line", x0=-0.5, x1=len(ay_labels) - 0.5,
                y0=80, y1=80,
                line=dict(color="#10b981", width=1.5, dash="dash"),
            )],
        )
        sc_bar(fig_pct, height=300)
        st.plotly_chart(fig_pct, use_container_width=True, key="cp_pct_bar", config=SC_CHART_CFG)

        # ------ Tablo: Satir Basi Yatay Bar ile ------
        styled_section("Detayli Performans Tablosu", _CP_BLUE)
        max_etkinlik = max(ay_toplam_list) if ay_toplam_list else 1

        tablo_rows = ""
        for i in range(len(ay_labels)):
            bar_w_tamam = round(ay_tamam_list[i] / max_etkinlik * 100) if max_etkinlik else 0
            bar_w_eksik = round(ay_eksik_list[i] / max_etkinlik * 100) if max_etkinlik else 0
            oran_renk = _CP_BLUE if ay_oran_list[i] >= 80 else _CP_GOLD if ay_oran_list[i] >= 50 else _CP_ORANGE
            tablo_rows += f"""
            <tr>
              <td style="font-weight:600;padding:8px 12px;border-bottom:1px solid #e2e8f0;
                  white-space:nowrap;">{ay_labels[i]}</td>
              <td style="text-align:center;padding:8px;border-bottom:1px solid #e2e8f0;">
                {ay_toplam_list[i]}</td>
              <td style="text-align:center;padding:8px;border-bottom:1px solid #e2e8f0;
                  color:{_CP_BLUE};font-weight:600;">{ay_tamam_list[i]}</td>
              <td style="text-align:center;padding:8px;border-bottom:1px solid #e2e8f0;
                  color:{_CP_ORANGE};font-weight:600;">{ay_eksik_list[i]}</td>
              <td style="padding:8px 12px;border-bottom:1px solid #e2e8f0;min-width:180px;">
                <div style="display:flex;height:16px;border-radius:3px;overflow:hidden;
                     background:#1A2035;">
                  <div style="width:{bar_w_tamam}%;background:{_CP_BLUE};"></div>
                  <div style="width:{bar_w_eksik}%;background:{_CP_ORANGE};"></div>
                </div>
              </td>
              <td style="text-align:center;padding:8px;border-bottom:1px solid #e2e8f0;">
                <span style="font-weight:700;color:{oran_renk};font-size:13px;">%{ay_oran_list[i]}</span>
              </td>
            </tr>"""

        # Ozet satiri
        tablo_rows += f"""
        <tr style="background:linear-gradient(90deg,#111827,#eef2ff);font-weight:700;">
          <td style="padding:10px 12px;border-top:2px solid {_CP_BLUE};">TOPLAM</td>
          <td style="text-align:center;padding:10px;border-top:2px solid {_CP_BLUE};">
            {toplam_etkinlik}</td>
          <td style="text-align:center;padding:10px;border-top:2px solid {_CP_BLUE};
              color:{_CP_BLUE};">{tamamlanan_etkinlik}</td>
          <td style="text-align:center;padding:10px;border-top:2px solid {_CP_BLUE};
              color:{_CP_ORANGE};">{eksik}</td>
          <td style="padding:10px 12px;border-top:2px solid {_CP_BLUE};">
            <div style="display:flex;height:16px;border-radius:3px;overflow:hidden;
                 background:#1A2035;">
              <div style="width:{genel_oran}%;background:{_CP_BLUE};"></div>
              <div style="width:{100 - genel_oran}%;background:{_CP_ORANGE};"></div>
            </div>
          </td>
          <td style="text-align:center;padding:10px;border-top:2px solid {_CP_BLUE};
              font-size:14px;color:{_CP_BLUE};">%{genel_oran}</td>
        </tr>"""

        st.markdown(f"""
        <div style="border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;margin:8px 0;">
          <table style="width:100%;border-collapse:collapse;font-size:12px;">
            <thead>
              <tr style="background:linear-gradient(90deg,{_CP_BLUE},{_CP_BLUE}dd);">
                <th style="padding:10px 12px;text-align:left;color:white;font-weight:700;">Ay</th>
                <th style="padding:10px;text-align:center;color:white;font-weight:700;">Toplam</th>
                <th style="padding:10px;text-align:center;color:white;font-weight:700;">Tamamlanan</th>
                <th style="padding:10px;text-align:center;color:white;font-weight:700;">Eksik</th>
                <th style="padding:10px;text-align:center;color:white;font-weight:700;">Grafik</th>
                <th style="padding:10px;text-align:center;color:white;font-weight:700;">Oran</th>
              </tr>
            </thead>
            <tbody>{tablo_rows}</tbody>
          </table>
        </div>""", unsafe_allow_html=True)

        # ------ Donem Bazli Sunburst (Ay > Durum) ------
        if len(mevcut_aylar) > 1:
            sb_labels = []
            sb_parents = []
            sb_values = []
            sb_colors = []

            # Root
            sb_labels.append(kademe_name)
            sb_parents.append("")
            sb_values.append(toplam_etkinlik)
            sb_colors.append(_CP_GRAY)

            for i, a in enumerate(ay_labels):
                # Ay dugumu
                sb_labels.append(a)
                sb_parents.append(kademe_name)
                sb_values.append(ay_toplam_list[i])
                sb_colors.append(_CP_BLUE if ay_oran_list[i] >= 80 else _CP_GOLD if ay_oran_list[i] >= 50 else _CP_ORANGE)

                # Tamamlanan yaprak
                if ay_tamam_list[i] > 0:
                    sb_labels.append(f"{a} - Tamam")
                    sb_parents.append(a)
                    sb_values.append(ay_tamam_list[i])
                    sb_colors.append(_CP_BLUE)

                # Eksik yaprak
                if ay_eksik_list[i] > 0:
                    sb_labels.append(f"{a} - Eksik")
                    sb_parents.append(a)
                    sb_values.append(ay_eksik_list[i])
                    sb_colors.append(_CP_ORANGE)

            fig_sun = go.Figure(go.Sunburst(
                labels=sb_labels,
                parents=sb_parents,
                values=sb_values,
                marker=dict(colors=sb_colors),
                branchvalues="total",
                textinfo="label+percent entry",
                textfont=dict(size=11),
                insidetextorientation="radial",
            ))
            fig_sun.update_layout(
                title=dict(text=f"{kademe_name} - Aylık Dagilim", font=dict(size=14, color="#94A3B8")),
                height=420,
                margin=dict(l=10, r=10, t=50, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_sun, use_container_width=True, key="cp_sunburst", config=SC_CHART_CFG)

        # Yeniden yukle butonu
        st.divider()
        if st.button("Planlari Yeniden Yukle", key="cp_reimport"):
            for p in cerceve:
                store.delete_by_id("planlar", p.id)
            importer.import_kademe(kademe_key, ey)
            st.success("Planlar yeniden yuklendi!")
            st.rerun()

    # ==============================================================
    #  Sub-tab 2: PLAN OLUSTUR
    # ==============================================================
    with sub[1]:
        styled_section("Rehberlik Planı Oluştur", "#7c3aed")
        c1, c2 = st.columns(2)
        with c1:
            plan_turu = st.selectbox("Plan Turu", PLAN_TURLERI,
                                     format_func=lambda x: PLAN_TUR_LABEL.get(x, x), key="rpl_tur")
            plan_adi = st.text_input("Plan Adi", key="rpl_adi")
            hedef_kitle = st.selectbox("Hedef Kitle", PLAN_HEDEF_KITLELER, key="rpl_hedef")
        with c2:
            donem = st.selectbox("Donem", ["1. Donem", "2. Donem", "Tüm Yil"], key="rpl_donem")
            aylar = ["Eylul", "Ekim", "Kasim", "Aralik", "Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran"]
            ay = st.selectbox("Ay", ["Tümü"] + aylar, key="rpl_ay")
            staff = get_staff_name_list()
            hazirlayan = st.selectbox("Hazirlayan", [""] + staff, key="rpl_hazirlayan")

        ey = st.selectbox("Egitim Yili", EGITIM_YILI_SECENEKLERI, index=1, key="rpl_ey")

        # Dinamik etkinlik listesi
        styled_section("Etkinlikler", "#7c3aed")
        if "rpl_etkinlikler" not in st.session_state:
            st.session_state.rpl_etkinlikler = []

        for i, e in enumerate(st.session_state.rpl_etkinlikler):
            cc1, cc2, cc3, cc4 = st.columns([3, 2, 2, 1])
            with cc1:
                st.session_state.rpl_etkinlikler[i]["etkinlik"] = st.text_input(
                    "Etkinlik", value=e.get("etkinlik", ""), key=f"rpl_e_ad_{i}")
            with cc2:
                st.session_state.rpl_etkinlikler[i]["tarih"] = st.text_input(
                    "Tarih/Hafta", value=e.get("tarih", ""), key=f"rpl_e_tarih_{i}")
            with cc3:
                st.session_state.rpl_etkinlikler[i]["durum"] = st.selectbox(
                    "Durum", ["Planli", "Tamamlandı", "Iptal"],
                    index=["Planli", "Tamamlandı", "Iptal"].index(e.get("durum", "Planli")),
                    key=f"rpl_e_durum_{i}")
            with cc4:
                if st.button("X", key=f"rpl_e_sil_{i}"):
                    st.session_state.rpl_etkinlikler.pop(i)
                    st.rerun()

        if st.button("+ Etkinlik Ekle", key="rpl_e_ekle"):
            st.session_state.rpl_etkinlikler.append({"etkinlik": "", "tarih": "", "durum": "Planli"})
            st.rerun()

        if st.button("Plan Kaydet", type="primary", use_container_width=True, key="rpl_kaydet"):
            if not plan_adi.strip():
                st.error("Plan adi bos birakilamaz.")
                return
            kod = store.next_plan_code()
            kayit = RehberlikPlani(
                plan_kodu=kod,
                plan_turu=plan_turu,
                plan_adi=plan_adi,
                hedef_kitle=hedef_kitle,
                donem=donem,
                ay=ay if ay != "Tümü" else "",
                etkinlikler=[e for e in st.session_state.rpl_etkinlikler if e.get("etkinlik")],
                hazirlayan=hazirlayan,
                egitim_yili=ey,
            )
            store.upsert("planlar", kayit)
            st.session_state.rpl_etkinlikler = []
            st.success(f"Plan kaydedildi: {kod}")
            st.rerun()

    # ==============================================================
    #  Sub-tab 3: PLAN LISTESI
    # ==============================================================
    with sub[2]:
        styled_section("Rehberlik Planlari", "#7c3aed")
        planlar = store.load_objects("planlar")
        if not planlar:
            styled_info_banner("Henuz plan yok.")
            return

        f_tur = st.selectbox("Plan Turu Filtre", ["Tümü"] + PLAN_TURLERI,
                             format_func=lambda x: PLAN_TUR_LABEL.get(x, x) if x != "Tümü" else x,
                             key="rpl_f_tur")
        filtered = planlar
        if f_tur != "Tümü":
            filtered = [p for p in filtered if p.plan_turu == f_tur]

        for p in filtered:
            with st.expander(f"{p.plan_kodu} | {PLAN_TUR_LABEL.get(p.plan_turu, p.plan_turu)} - {p.plan_adi}"):
                st.markdown(f"""
                **Hedef Kitle:** {p.hedef_kitle} | **Donem:** {p.donem} | **Ay:** {p.ay or 'Tumu'}
                **Hazirlayan:** {p.hazirlayan} | **Durum:** {p.durum}
                """)
                if p.etkinlikler:
                    st.markdown("**Etkinlikler:**")
                    for e in p.etkinlikler:
                        durum_emoji = "\u2705" if e.get("durum") == "Tamamlandı" else "\u23f3" if e.get("durum") == "Planli" else "\u274c"
                        st.markdown(f"  {durum_emoji} {e.get('etkinlik', '')} - {e.get('tarih', '')} ({e.get('durum', '')})")
                cc1, cc2 = st.columns(2)
                with cc1:
                    if st.button("Sil", key=f"rpl_sil_{p.id}", type="secondary"):
                        store.delete_by_id("planlar", p.id)
                        st.success("Plan silindi.")
                        st.rerun()


# ============================================================
# SEKME 9: RISK DEGERLENDIRME
# ============================================================

def _render_risk_degerlendirme(store: RehberlikDataStore):
    sub = st.tabs(["➕ Yeni Değerlendirme", "📋 Risk Listesi"])

    with sub[0]:
        styled_section("Yeni Risk Değerlendirme", "#ea580c")
        stu = _ogrenci_sinif_sube_selectbox("rd_yeni")
        if not stu:
            return

        ogrenci_adi = _get_student_full_name(stu)
        sinif_sube = _get_student_sinif_sube(stu)

        c1, c2 = st.columns(2)
        with c1:
            risk_seviyesi = st.selectbox("Risk Seviyesi", RISK_SEVIYELERI,
                                         format_func=lambda x: RISK_SEVIYE_LABEL.get(x, x), key="rd_seviye")
            risk_alanlari = st.multiselect("Risk Alanlari", RISK_ALANLARI, key="rd_alanlar")
            tarih = st.date_input("Tarih", value=date.today(), key="rd_tarih")
        with c2:
            staff = get_staff_name_list()
            degerlendiren = st.selectbox("Degerlendiren", [""] + staff, key="rd_degerlendiren")
            # Vaka baglama
            vakalar = store.load_objects("vakalar")
            vaka_opts = {"": "-- Vaka bagla (opsiyonel) --"}
            for v in vakalar:
                if v.durum != "KAPANDI":
                    vaka_opts[v.id] = f"{v.vaka_kodu} - {v.ogrenci_adi}"
            vaka_sec = st.selectbox("Vaka Baglantisi", list(vaka_opts.keys()),
                                    format_func=lambda x: vaka_opts[x], key="rd_vaka")

        aciklama = st.text_area("Açıklama", key="rd_aciklama", height=100)
        onlemler = st.text_area("Onlemler", key="rd_onlemler", height=80)
        takip_plani = st.text_area("Takip Plani", key="rd_takip", height=80)
        ey = st.selectbox("Egitim Yili", EGITIM_YILI_SECENEKLERI, index=1, key="rd_ey")

        if st.button("Risk Değerlendirme Kaydet", type="primary", use_container_width=True, key="rd_kaydet"):
            if not risk_alanlari:
                st.error("En az bir risk alani secilmelidir.")
                return
            kayit = RiskDegerlendirme(
                ogrenci_id=stu.get("id", ""),
                ogrenci_adi=ogrenci_adi,
                sinif_sube=sinif_sube,
                risk_seviyesi=risk_seviyesi,
                risk_alanlari=risk_alanlari,
                aciklama=aciklama,
                degerlendiren=degerlendiren,
                tarih=tarih.isoformat() if tarih else _today(),
                onlemler=onlemler,
                takip_plani=takip_plani,
                vaka_id=vaka_sec,
                egitim_yili=ey,
            )
            store.upsert("risk_degerlendirmeleri", kayit)
            st.success("Risk degerlendirme kaydedildi.")
            st.rerun()

    with sub[1]:
        styled_section("Risk Listesi", "#ea580c")
        riskler = store.load_objects("risk_degerlendirmeleri")
        if not riskler:
            styled_info_banner("Henuz risk degerlendirme yok.")
            return

        c1, c2 = st.columns(2)
        with c1:
            f_seviye = st.selectbox("Seviye", ["Tümü"] + RISK_SEVIYELERI,
                                    format_func=lambda x: RISK_SEVIYE_LABEL.get(x, x) if x != "Tümü" else x,
                                    key="rd_f_seviye")
        with c2:
            f_durum = st.selectbox("Durum", ["Tümü", "Aktif", "Kapandi"], key="rd_f_durum")

        filtered = riskler
        if f_seviye != "Tümü":
            filtered = [r for r in filtered if r.risk_seviyesi == f_seviye]
        if f_durum != "Tümü":
            filtered = [r for r in filtered if r.durum == f_durum]

        filtered.sort(key=lambda r: r.tarih, reverse=True)

        for r in filtered:
            renk = RISK_SEVIYE_RENK.get(r.risk_seviyesi, "#64748b")
            with st.expander(f"{r.ogrenci_adi} ({r.sinif_sube}) - {RISK_SEVIYE_LABEL.get(r.risk_seviyesi, '')} | {r.tarih}"):
                st.markdown(f"""
                **Risk Seviyesi:** <span style="color:{renk};font-weight:700;">{RISK_SEVIYE_LABEL.get(r.risk_seviyesi, '')}</span> |
                **Alanlar:** {', '.join(r.risk_alanlari)} | **Durum:** {r.durum}
                """, unsafe_allow_html=True)
                if r.aciklama:
                    st.markdown(f"**Açıklama:** {r.aciklama}")
                if r.onlemler:
                    st.markdown(f"**Onlemler:** {r.onlemler}")
                if r.takip_plani:
                    st.markdown(f"**Takip Plani:** {r.takip_plani}")
                if r.degerlendiren:
                    st.markdown(f"**Degerlendiren:** {r.degerlendiren}")

                cc1, cc2 = st.columns(2)
                with cc1:
                    yeni_durum = st.selectbox("Durum", ["Aktif", "Kapandi"],
                                              index=0 if r.durum == "Aktif" else 1,
                                              key=f"rd_durum_{r.id}")
                    if st.button("Durumu Güncelle", key=f"rd_dgunc_{r.id}"):
                        r.durum = yeni_durum
                        r.updated_at = _now()
                        store.upsert("risk_degerlendirmeleri", r)
                        st.success("Risk durumu güncellendi.")
                        st.rerun()
                with cc2:
                    if st.button("Sil", key=f"rd_sil_{r.id}", type="secondary"):
                        store.delete_by_id("risk_degerlendirmeleri", r.id)
                        st.success("Risk degerlendirme silindi.")
                        st.rerun()


# ============================================================
# SEKME 10: RAPORLAR
# ============================================================

def _render_raporlar(store: RehberlikDataStore):
    sub = st.tabs(["📊 Genel Özet", "💬 Görüşme Raporu", "📁 Vaka Raporu", "📋 BEP Raporu", "⚠️ Risk Raporu"])

    # --- Genel Ozet ---
    with sub[0]:
        styled_section("Genel Özet Raporu", "#7c3aed")
        data = DashboardAggregator.get_dashboard_data(store)

        metrics = [
            ("Toplam Görüşme", data["toplam_gorusme"], "#7c3aed", "\U0001F4AC"),
            ("Toplam Vaka", data["toplam_vaka"], "#ef4444", "\U0001F4C2"),
            ("Aktif BEP", data["aktif_bep_sayi"], "#2563eb", "\U0001F4D1"),
            ("Toplam Risk", data["toplam_risk"], "#ea580c", "\u26a0\ufe0f"),
        ]
        st.markdown(ReportStyler.metric_cards_html([
            (m[0], m[1], m[2], m[3]) for m in metrics
        ]), unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if data["konu_dagilimi"]:
                st.markdown(ReportStyler.horizontal_bar_html(data["konu_dagilimi"], color="#7c3aed"), unsafe_allow_html=True)
        with c2:
            if data["oncelik_dagilimi"]:
                st.markdown(ReportStyler.donut_chart_svg(data["oncelik_dagilimi"]), unsafe_allow_html=True)

        # PDF
        if st.button("PDF Oluştur", key="rpt_genel_pdf"):
            info = get_institution_info()
            pdf = ReportPDFGenerator("Rehberlik Genel Özet Raporu")
            pdf.add_header(kurum_adi=info.get("name", ""), logo_path=info.get("logo_path", ""))
            pdf.add_section("İstatistikler")
            pdf.add_metrics([(m[0], m[1], m[2]) for m in metrics])
            if data["konu_dagilimi"]:
                pdf.add_section("Görüşme Konu Dagilimi")
                pdf.add_bar_chart(data["konu_dagilimi"], color="#7c3aed")
            pdf_bytes = pdf.generate()
            st.download_button("PDF Indir", pdf_bytes, "rehberlik_genel_ozet.pdf", "application/pdf",
                               key="rpt_genel_dl")

    # --- Görüşme Raporu ---
    with sub[1]:
        styled_section("Görüşme Raporu", "#7c3aed")
        gorusmeler = store.load_objects("gorusmeler")
        if not gorusmeler:
            styled_info_banner("Henuz gorusme kaydi yok.")
            return

        c1, c2 = st.columns(2)
        with c1:
            baslangic = st.date_input("Başlangıç", value=date(date.today().year, 9, 1), key="rpt_grm_bas")
        with c2:
            bitis = st.date_input("Bitis", value=date.today(), key="rpt_grm_bit")

        bas_str = baslangic.isoformat()
        bit_str = bitis.isoformat()
        filtered = [g for g in gorusmeler if bas_str <= g.tarih <= bit_str]

        st.markdown(f"**Toplam:** {len(filtered)} gorusme")

        if filtered:
            rows = []
            for g in sorted(filtered, key=lambda x: x.tarih, reverse=True):
                rows.append({
                    "Kod": g.gorusme_kodu,
                    "Tarih": g.tarih,
                    "Öğrenci": g.ogrenci_adi,
                    "Sınıf": g.sinif_sube,
                    "Tur": g.gorusme_turu,
                    "Konu": g.gorusme_konusu,
                    "Gorusen": g.gorusen,
                })
            df = pd.DataFrame(rows)
            st.markdown(ReportStyler.colored_table_html(df, header_color="#7c3aed"), unsafe_allow_html=True)

            # PDF
            if st.button("PDF Oluştur", key="rpt_grm_pdf"):
                info = get_institution_info()
                pdf = ReportPDFGenerator("Görüşme Raporu",
                                         subtitle=f"{bas_str} - {bit_str}")
                pdf.add_header(kurum_adi=info.get("name", ""), logo_path=info.get("logo_path", ""))
                pdf.add_section("Görüşme Listesi")
                pdf.add_table(df, header_color="#7c3aed")
                pdf_bytes = pdf.generate()
                st.download_button("PDF Indir", pdf_bytes, "gorusme_raporu.pdf", "application/pdf",
                                   key="rpt_grm_dl")

    # --- Vaka Raporu ---
    with sub[2]:
        styled_section("Vaka Raporu", "#ef4444")
        vakalar = store.load_objects("vakalar")
        if not vakalar:
            styled_info_banner("Henuz vaka kaydi yok.")
            return

        # Durum dagilimi
        durum_dag: dict[str, float] = {}
        for v in vakalar:
            lbl = VAKA_DURUM_LABEL.get(v.durum, v.durum)
            durum_dag[lbl] = durum_dag.get(lbl, 0) + 1

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(ReportStyler.donut_chart_svg(durum_dag), unsafe_allow_html=True)
        with c2:
            oncelik_dag: dict[str, float] = {}
            for v in vakalar:
                lbl = VAKA_ONCELIK_LABEL.get(v.oncelik, v.oncelik)
                oncelik_dag[lbl] = oncelik_dag.get(lbl, 0) + 1
            st.markdown(ReportStyler.donut_chart_svg(oncelik_dag), unsafe_allow_html=True)

        rows = []
        for v in sorted(vakalar, key=lambda x: x.baslangic_tarihi, reverse=True):
            rows.append({
                "Kod": v.vaka_kodu,
                "Öğrenci": v.ogrenci_adi,
                "Sınıf": v.sinif_sube,
                "Başlık": v.vaka_basligi,
                "Öncelik": VAKA_ONCELIK_LABEL.get(v.oncelik, v.oncelik),
                "Durum": VAKA_DURUM_LABEL.get(v.durum, v.durum),
                "Görüşme": v.gorusme_sayisi,
            })
        df = pd.DataFrame(rows)
        st.markdown(ReportStyler.colored_table_html(df, header_color="#ef4444"), unsafe_allow_html=True)

        if st.button("PDF Oluştur", key="rpt_vk_pdf"):
            info = get_institution_info()
            pdf = ReportPDFGenerator("Vaka Raporu")
            pdf.add_header(kurum_adi=info.get("name", ""), logo_path=info.get("logo_path", ""))
            pdf.add_section("Vaka Durum Dagilimi")
            pdf.add_donut_chart(durum_dag, title="Vaka Durumu")
            pdf.add_section("Vaka Listesi")
            pdf.add_table(df, header_color="#ef4444")
            pdf_bytes = pdf.generate()
            st.download_button("PDF Indir", pdf_bytes, "vaka_raporu.pdf", "application/pdf",
                               key="rpt_vk_dl")

    # --- BEP Raporu ---
    with sub[3]:
        styled_section("BEP Raporu", "#2563eb")
        bepler = store.load_objects("bep_kayitlari")
        if not bepler:
            styled_info_banner("Henuz BEP kaydi yok.")
            return

        # Engel turu dagilimi
        engel_dag: dict[str, float] = {}
        for b in bepler:
            engel_dag[b.engel_turu] = engel_dag.get(b.engel_turu, 0) + 1

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(ReportStyler.donut_chart_svg(engel_dag), unsafe_allow_html=True)
        with c2:
            durum_dag_bep: dict[str, float] = {}
            for b in bepler:
                lbl = BEP_DURUM_LABEL.get(b.durum, b.durum)
                durum_dag_bep[lbl] = durum_dag_bep.get(lbl, 0) + 1
            st.markdown(ReportStyler.donut_chart_svg(durum_dag_bep), unsafe_allow_html=True)

        rows = []
        for b in bepler:
            rows.append({
                "Kod": b.bep_kodu,
                "Öğrenci": b.ogrenci_adi,
                "Sınıf": b.sinif_sube,
                "Engel Turu": b.engel_turu,
                "Durum": BEP_DURUM_LABEL.get(b.durum, b.durum),
                "Hedef Sayısı": len(b.hedefler),
            })
        df = pd.DataFrame(rows)
        st.markdown(ReportStyler.colored_table_html(df, header_color="#2563eb"), unsafe_allow_html=True)

        if st.button("PDF Oluştur", key="rpt_bep_pdf"):
            info = get_institution_info()
            pdf = ReportPDFGenerator("BEP Raporu")
            pdf.add_header(kurum_adi=info.get("name", ""), logo_path=info.get("logo_path", ""))
            pdf.add_section("Engel Turu Dagilimi")
            pdf.add_donut_chart(engel_dag, title="Engel Turleri")
            pdf.add_section("BEP Listesi")
            pdf.add_table(df, header_color="#2563eb")
            pdf_bytes = pdf.generate()
            st.download_button("PDF Indir", pdf_bytes, "bep_raporu.pdf", "application/pdf",
                               key="rpt_bep_dl")

    # --- Risk Raporu ---
    with sub[4]:
        styled_section("Risk Raporu", "#ea580c")
        riskler = store.load_objects("risk_degerlendirmeleri")
        if not riskler:
            styled_info_banner("Henuz risk degerlendirme yok.")
            return

        # Seviye dagilimi
        seviye_dag: dict[str, float] = {}
        for r in riskler:
            if r.durum == "Aktif":
                lbl = RISK_SEVIYE_LABEL.get(r.risk_seviyesi, r.risk_seviyesi)
                seviye_dag[lbl] = seviye_dag.get(lbl, 0) + 1

        # Alan dagilimi
        alan_dag: dict[str, float] = {}
        for r in riskler:
            if r.durum == "Aktif":
                for a in r.risk_alanlari:
                    alan_dag[a] = alan_dag.get(a, 0) + 1

        c1, c2 = st.columns(2)
        with c1:
            if seviye_dag:
                colors = [RISK_SEVIYE_RENK.get(k, "#64748b") for k in
                          ["DUSUK", "ORTA", "YUKSEK", "KRITIK"] if RISK_SEVIYE_LABEL.get(k, k) in seviye_dag]
                st.markdown(ReportStyler.donut_chart_svg(seviye_dag, colors=colors or None), unsafe_allow_html=True)
            else:
                st.info("Aktif risk yok.")
        with c2:
            if alan_dag:
                st.markdown(ReportStyler.horizontal_bar_html(alan_dag, color="#ea580c"), unsafe_allow_html=True)
            else:
                st.info("Risk alani verisi yok.")

        rows = []
        for r in sorted(riskler, key=lambda x: x.tarih, reverse=True):
            rows.append({
                "Öğrenci": r.ogrenci_adi,
                "Sınıf": r.sinif_sube,
                "Seviye": RISK_SEVIYE_LABEL.get(r.risk_seviyesi, r.risk_seviyesi),
                "Alanlar": ", ".join(r.risk_alanlari),
                "Durum": r.durum,
                "Tarih": r.tarih,
            })
        df = pd.DataFrame(rows)
        st.markdown(ReportStyler.colored_table_html(df, header_color="#ea580c"), unsafe_allow_html=True)

        if st.button("PDF Oluştur", key="rpt_risk_pdf"):
            info = get_institution_info()
            pdf = ReportPDFGenerator("Risk Değerlendirme Raporu")
            pdf.add_header(kurum_adi=info.get("name", ""), logo_path=info.get("logo_path", ""))
            pdf.add_section("Risk Seviye Dagilimi")
            if seviye_dag:
                pdf.add_donut_chart(seviye_dag, title="Aktif Risk Seviyeleri")
            pdf.add_section("Risk Listesi")
            pdf.add_table(df, header_color="#ea580c")
            pdf_bytes = pdf.generate()
            st.download_button("PDF Indir", pdf_bytes, "risk_raporu.pdf", "application/pdf",
                               key="rpt_risk_dl")

    # ================================================================
    # PERFORMANS KARSILASTIRMA + AI ONERILERI + KUNYE + PDF
    # ================================================================
    from utils.report_utils import (ai_recommendations_html, period_comparison_row_html,
                                     generate_module_pdf, render_pdf_download_button,
                                     render_report_kunye_html, ReportStyler as _RS)

    st.markdown(_RS.section_divider_html("Donemsel Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

    from datetime import datetime as _dt, timedelta as _td
    _now = _dt.now()
    _cur_month = _now.strftime("%Y-%m")
    _prev_month = (_now.replace(day=1) - _td(days=1)).strftime("%Y-%m")

    try:
        _gorusmeler_raw = store.load_list("gorusmeler")
        _vakalar_raw = store.load_list("vakalar")
        _bep_raw = store.load_list("bep_kayitlari")
        _risk_raw = store.load_list("risk_degerlendirmeleri")
    except Exception:
        _gorusmeler_raw, _vakalar_raw, _bep_raw, _risk_raw = [], [], [], []

    def _rhb_count_by_month(records, month_str, date_fields=("tarih", "created_at", "baslangic_tarihi")):
        c = 0
        for r in records:
            for df in date_fields:
                val = r.get(df, "")
                if val and val[:7] == month_str:
                    c += 1
                    break
        return c

    _rhb_comparisons = [
        {"label": "Görüşmeler", "current": _rhb_count_by_month(_gorusmeler_raw, _cur_month), "previous": _rhb_count_by_month(_gorusmeler_raw, _prev_month)},
        {"label": "Vakalar", "current": _rhb_count_by_month(_vakalar_raw, _cur_month), "previous": _rhb_count_by_month(_vakalar_raw, _prev_month)},
        {"label": "BEP Kayıtlari", "current": _rhb_count_by_month(_bep_raw, _cur_month), "previous": _rhb_count_by_month(_bep_raw, _prev_month)},
        {"label": "Risk Değerlendirme", "current": _rhb_count_by_month(_risk_raw, _cur_month), "previous": _rhb_count_by_month(_risk_raw, _prev_month)},
    ]
    st.markdown(period_comparison_row_html(_rhb_comparisons), unsafe_allow_html=True)

    # ---- AI Onerileri ----
    _rhb_insights = []

    _aktif_risk_cnt = sum(1 for r in _risk_raw if r.get("durum") == "Aktif")
    _toplam_gorusme = len(_gorusmeler_raw)
    _toplam_vaka = len(_vakalar_raw)
    _aktif_bep = sum(1 for b in _bep_raw if b.get("durum") == "Aktif")
    _tamamlanan_bep = sum(1 for b in _bep_raw if b.get("durum") == "Tamamlandı")
    _bep_total = len(_bep_raw)
    _bep_completion = round((_tamamlanan_bep / _bep_total) * 100, 1) if _bep_total > 0 else 0

    if _aktif_risk_cnt > 5:
        _rhb_insights.append({
            "icon": "\u26a0\ufe0f", "title": "Yuksek Risk Uyarisi",
            "text": f"Aktif risk degerlendirmesi {_aktif_risk_cnt} ogrenciye ulasti. Acil mudahale plani olusturulmasi ve ilgili ogretmenlerle koordinasyon saglanmasi onerilir.",
            "color": "#ef4444"
        })

    if _bep_total > 0 and _bep_completion < 50:
        _rhb_insights.append({
            "icon": "\U0001f4cb", "title": "BEP Tamamlanma Orani Dusuk",
            "text": f"BEP tamamlanma orani %{_bep_completion:.0f} seviyesinde. Hedeflerin guncellenmesi ve aile isbirligi arttirilmasi onerilir.",
            "color": "#f59e0b"
        })

    _cur_gorusme = _rhb_count_by_month(_gorusmeler_raw, _cur_month)
    _prev_gorusme = _rhb_count_by_month(_gorusmeler_raw, _prev_month)
    if _prev_gorusme > 0 and _cur_gorusme < _prev_gorusme * 0.7:
        _rhb_insights.append({
            "icon": "\U0001f4c9", "title": "Görüşme Sikligi Azaliyor",
            "text": f"Bu ay {_cur_gorusme} gorusme yapildi (onceki ay: {_prev_gorusme}). Öğrenci takibinin aksamamasi için gorusme planlama takviminin gozden gecirilmesi onerilir.",
            "color": "#ea580c"
        })

    if _toplam_vaka > 0 and _aktif_risk_cnt == 0:
        _rhb_insights.append({
            "icon": "\u2705", "title": "Risk Durumu Olumlu",
            "text": "Aktif risk degerlendirmesi bulunmuyor. Mevcut vaka takibi basariyla yurutulmektedir.",
            "color": "#10b981"
        })

    _rhb_insights.append({
        "icon": "\U0001f4a1", "title": "Genel Oneri",
        "text": f"Toplam {_toplam_gorusme} gorusme, {_toplam_vaka} vaka, {_aktif_bep} aktif BEP kaydi mevcut. Duzenli raporlama ve veli bilgilendirme toplantilari planlanmasi onerilir.",
        "color": "#2563eb"
    })

    _rhb_insights.append({
        "icon": "\U0001f4c6", "title": "Donemsel Değerlendirme",
        "text": "Donem sonu yaklasirken tum acik vakalarin degerlendirilmesi, BEP hedeflerinin guncellenmesi ve sonraki donem planlama calismalarinin baslatilmasi onerilir.",
        "color": "#8b5cf6"
    })

    st.markdown(ai_recommendations_html(_rhb_insights), unsafe_allow_html=True)

    # ---- Kurumsal Kunye ----
    st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

    # ---- PDF Export ----
    st.markdown(_RS.section_divider_html("Rehberlik Genel PDF Raporu", "#1e40af"), unsafe_allow_html=True)
    if st.button("\U0001f4e5 Rehberlik Tüm Rapor (PDF)", key="rhb_full_pdf_btn", use_container_width=True):
        try:
            _sections = [
                {
                    "title": "Genel İstatistikler",
                    "metrics": [
                        ("Görüşmeler", _toplam_gorusme, "#7c3aed"),
                        ("Vakalar", _toplam_vaka, "#ef4444"),
                        ("Aktif BEP", _aktif_bep, "#2563eb"),
                        ("Aktif Risk", _aktif_risk_cnt, "#ea580c"),
                    ],
                    "text": f"BEP Tamamlanma: %{_bep_completion:.0f} | Bu Ay Görüşme: {_cur_gorusme} | Önceki Ay: {_prev_gorusme}",
                },
                {
                    "title": "Donemsel Karsilastirma",
                    "text": " | ".join([f"{c['label']}: {c['current']} (onceki: {c['previous']})" for c in _rhb_comparisons]),
                },
            ]
            _pdf_bytes = generate_module_pdf("Rehberlik Servisi Raporu", _sections)
            render_pdf_download_button(_pdf_bytes, "rehberlik_raporu.pdf", "Rehberlik Raporu Indir", "rhb_full_dl")
        except Exception as _e:
            st.error(f"PDF olusturulurken hata: {_e}")


# ============================================================
# REHBERLİK BÜLTENLERİ — PREMIUM EDITION
# ============================================================

_AYLAR_TR = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
    7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık",
}

_BULTEN_KATEGORILER = ["Tümü", "Anaokulu", "İlkokul", "Ortaokul", "Lise"]
_BULTEN_RENK = {
    "Anaokulu": ("#f59e0b", "#d97706", "🧒"),
    "İlkokul":  ("#10b981", "#059669", "📗"),
    "Ortaokul": ("#3b82f6", "#2563eb", "📘"),
    "Lise":     ("#8b5cf6", "#7c3aed", "📕"),
}

_BULTEN_TEMALAR = {
    9: ("Okula Uyum ve Yeni Başlangıçlar", "🏫"),
    10: ("Arkadaşlık ve Sosyal Beceriler", "🤝"),
    11: ("Sorumluluk ve Öz Düzenleme", "📋"),
    12: ("Empati ve Yardımseverlik", "💝"),
    1: ("Hedef Belirleme ve Motivasyon", "🎯"),
    2: ("Sevgi, Saygı ve Değerler", "❤️"),
    3: ("Özgüven ve Bireysel Farklılıklar", "⭐"),
    4: ("Kitap Okuma ve Hayal Gücü", "📖"),
    5: ("Aile İletişimi ve Bağlar", "🏠"),
    6: ("Yaz Tatili ve Değerlendirme", "☀️"),
}

# Arşiv: (kademe, yıl, ay) — Eylül 2024 → Haziran 2026
_BULTEN_ARSIV: list[tuple[str, int, int]] = [
    # 2026
    ("Lise", 2026, 6), ("Ortaokul", 2026, 6), ("İlkokul", 2026, 6), ("Anaokulu", 2026, 6),
    ("Lise", 2026, 5), ("Ortaokul", 2026, 5), ("İlkokul", 2026, 5), ("Anaokulu", 2026, 5),
    ("Lise", 2026, 4), ("Ortaokul", 2026, 4), ("İlkokul", 2026, 4), ("Anaokulu", 2026, 4),
    ("Lise", 2026, 3), ("Ortaokul", 2026, 3), ("İlkokul", 2026, 3), ("Anaokulu", 2026, 3),
    ("Lise", 2026, 2), ("Ortaokul", 2026, 2), ("İlkokul", 2026, 2), ("Anaokulu", 2026, 2),
    ("Lise", 2026, 1), ("Ortaokul", 2026, 1), ("İlkokul", 2026, 1), ("Anaokulu", 2026, 1),
    # 2025
    ("Lise", 2025, 12), ("Ortaokul", 2025, 12), ("İlkokul", 2025, 12), ("Anaokulu", 2025, 12),
    ("Lise", 2025, 11), ("Ortaokul", 2025, 11), ("İlkokul", 2025, 11), ("Anaokulu", 2025, 11),
    ("Lise", 2025, 10), ("Ortaokul", 2025, 10), ("İlkokul", 2025, 10), ("Anaokulu", 2025, 10),
    ("Lise", 2025, 9), ("Ortaokul", 2025, 9), ("İlkokul", 2025, 9), ("Anaokulu", 2025, 9),
    ("Lise", 2025, 6), ("Ortaokul", 2025, 6), ("İlkokul", 2025, 6), ("Anaokulu", 2025, 6),
    ("Lise", 2025, 5), ("Ortaokul", 2025, 5), ("İlkokul", 2025, 5), ("Anaokulu", 2025, 5),
    ("Lise", 2025, 4), ("Ortaokul", 2025, 4), ("İlkokul", 2025, 4), ("Anaokulu", 2025, 4),
    ("Lise", 2025, 3), ("Ortaokul", 2025, 3), ("İlkokul", 2025, 3), ("Anaokulu", 2025, 3),
    ("Lise", 2025, 2), ("Ortaokul", 2025, 2), ("İlkokul", 2025, 2), ("Anaokulu", 2025, 2),
    ("Lise", 2025, 1), ("Ortaokul", 2025, 1), ("İlkokul", 2025, 1), ("Anaokulu", 2025, 1),
    # 2024
    ("Lise", 2024, 12), ("Ortaokul", 2024, 12), ("İlkokul", 2024, 12), ("Anaokulu", 2024, 12),
    ("Lise", 2024, 11), ("Ortaokul", 2024, 11), ("İlkokul", 2024, 11), ("Anaokulu", 2024, 11),
    ("Lise", 2024, 10), ("Ortaokul", 2024, 10), ("İlkokul", 2024, 10), ("Anaokulu", 2024, 10),
    ("Lise", 2024, 9), ("Ortaokul", 2024, 9), ("İlkokul", 2024, 9), ("Anaokulu", 2024, 9),
]

# ── Aylık Takvim (tüm kademeler ortak) ──
_BULTEN_TAKVIM = {
    9: [("1 Eylül", "Eğitim Öğretim Yılı Başlangıcı"), ("21 Eylül", "Dünya Barış Günü"), ("26 Eylül", "Avrupa Dil Günü")],
    10: [("1 Ekim", "Dünya Çocuk Günü"), ("4 Ekim", "Hayvanları Koruma Günü"), ("10 Ekim", "Dünya Ruh Sağlığı Günü"), ("29 Ekim", "Cumhuriyet Bayramı")],
    11: [("10 Kasım", "Atatürk'ü Anma Günü"), ("20 Kasım", "Dünya Çocuk Hakları Günü"), ("24 Kasım", "Öğretmenler Günü")],
    12: [("3 Aralık", "Engelliler Günü"), ("10 Aralık", "İnsan Hakları Günü"), ("31 Aralık", "Yılbaşı")],
    1: [("1 Ocak", "Yeni Yıl"), ("13 Ocak", "Basın Onur Günü")],
    2: [("14 Şubat", "Sevgililer Günü"), ("21 Şubat", "Dünya Ana Dili Günü"), ("24 Şubat", "Yarıyıl Tatili")],
    3: [("8 Mart", "Dünya Kadınlar Günü"), ("18 Mart", "Çanakkale Zaferi"), ("21 Mart", "Nevruz / Dünya Ormancılık Günü")],
    4: [("7 Nisan", "Dünya Sağlık Günü"), ("23 Nisan", "Ulusal Egemenlik ve Çocuk Bayramı")],
    5: [("1 Mayıs", "Emek ve Dayanışma Günü"), ("19 Mayıs", "Atatürk'ü Anma, Gençlik ve Spor Bayramı"), ("2. Pazar", "Anneler Günü")],
    6: [("1 Haziran", "Dünya Çocuk Günü"), ("5 Haziran", "Dünya Çevre Günü"), ("3. Pazar", "Babalar Günü"), ("Haziran Sonu", "Eğitim Yılı Sonu")],
}

# ── Motivasyon Alıntıları ──
_BULTEN_MOTIVASYON = {
    9: ("Her yeni başlangıç, yeni bir umut demektir.", "Hz. Mevlâna"),
    10: ("Gerçek arkadaş, güneş gibidir; karanlık günlerde bile ışığını hissedersin.", "Yunus Emre"),
    11: ("Hayatta en hakiki mürşit ilimdir.", "Mustafa Kemal Atatürk"),
    12: ("İnsanların en hayırlısı, insanlara faydalı olandır.", "Hz. Muhammed"),
    1: ("Hedefi olmayan gemiye hiçbir rüzgâr yardım edemez.", "Seneca"),
    2: ("Sevgi görmek değil, aynı yöne birlikte bakmaktır.", "Antoine de Saint-Exupéry"),
    3: ("Kendine inan; yarının güzelliği bugünkü cesaretinde gizlidir.", "Konfüçyüs"),
    4: ("Bir kitap, bin kapı açar.", "Türk Atasözü"),
    5: ("Ailenin gücü, birlikte geçirilen zamanda saklıdır.", "Virginia Satir"),
    6: ("Dinlenmek, yeni başlangıçlar için güç toplamaktır.", "Ovid"),
}

# ── İnfografik Verileri (ay bazlı, genel istatistikler) ──
_BULTEN_INFOGRAFIK = {
    9: [("Uyum Süreci", "İlk 2-4 hafta kritiktir", "⏱️"), ("Okul Başarısı", "Düzenli uyku %30 artırır", "😴"), ("Sosyal Gelişim", "İlk arkadaşlık 4-6 haftada kurulur", "🤗"), ("Beslenme", "Kahvaltı yapan öğrenci %20 daha başarılı", "🥣")],
    10: [("Arkadaşlık", "Çocukların %70'i okulda en iyi arkadaşını bulur", "💛"), ("Empati", "Empati eğitimi zorbalığı %40 azaltır", "🫂"), ("Oyun", "Serbest oyun sosyal becerileri %35 geliştirir", "🎮"), ("İletişim", "Aktif dinleme ilişki kalitesini %50 artırır", "👂")],
    11: [("Sorumluluk", "Ev görevi yapan çocuklar %25 daha başarılı", "✅"), ("Atatürk", "Eğitim en önemli millî meselemizdir", "🇹🇷"), ("Zaman", "Planlı çalışma verimi %40 artırır", "⏰"), ("Rutin", "Düzenli rutin kaygıyı %30 azaltır", "📅")],
    12: [("Empati", "Empati kurabilen çocuklar %60 daha mutlu", "💝"), ("Yardım", "Gönüllülük öz değeri %45 artırır", "🤲"), ("Paylaşma", "Paylaşma alışkanlığı 3-6 yaşta kazanılır", "🎁"), ("İnsan Hakları", "BM: 30 maddelik Evrensel Bildirge", "⚖️")],
    1: [("Hedef", "Yazılı hedef koyanlarda başarı %42 daha yüksek", "📝"), ("Motivasyon", "İçsel motivasyon 3 kat daha sürdürülebilir", "🔥"), ("Uyku", "8 saat uyku akademik başarıyı %25 artırır", "🛌"), ("Pozitif Düşünce", "Olumlu iç konuşma özgüveni %35 yükseltir", "💪")],
    2: [("Sevgi", "Koşulsuz sevgi güvenli bağlanmayı %80 güçlendirir", "❤️"), ("Saygı", "Saygılı iletişim çatışmayı %55 azaltır", "🤝"), ("Zorbalık", "Her 3 çocuktan 1'i zorbalığa maruz kalır", "🛡️"), ("Öz Değer", "Kendini seven çocuk %40 daha dirençli", "⭐")],
    3: [("Özgüven", "Özgüvenli çocuklar akademik olarak %30 daha başarılı", "💎"), ("Büyüme Zihniyeti", "Çaba odaklı övgü motivasyonu %40 artırır", "🌱"), ("Beden İmajı", "Ergenlerin %65'i görünüşünden kaygı duyar", "🪞"), ("Yetenek", "Her çocukta en az 1 güçlü alan mevcuttur", "🏆")],
    4: [("Okuma", "Günde 20 dk okuma yılda 1.8 milyon kelime demek", "📚"), ("Kelime", "Okuyan çocuklar %50 daha geniş kelime haznesine sahip", "🔤"), ("Hayal Gücü", "Hikâye dinleyen çocuklar %60 daha yaratıcı", "🌈"), ("Kütüphane", "Kütüphane kullanan çocuklar %35 daha başarılı", "🏛️")],
    5: [("Aile", "Birlikte yemek yiyen aileler %25 daha mutlu", "🍽️"), ("İletişim", "Kaliteli 15 dakika günde yeterli", "💬"), ("Dijital", "Aile ekran süresi kuralı stresi %30 azaltır", "📱"), ("Bağ", "Güvenli bağlanma akademik başarıyı %35 etkiler", "🔗")],
    6: [("Tatil", "Yapılandırılmış tatil gelişimi %40 destekler", "🏖️"), ("Doğa", "Doğada vakit geçirmek stresi %50 azaltır", "🌲"), ("Hareket", "Günde 60 dk fiziksel aktivite önerilir", "🏃"), ("Okuma", "Yaz okuma kaybı 2-3 aylık gerilemeye neden olur", "📖")],
}

# ── Mini Öz Değerlendirme Testleri (ay bazlı, kademe adaptasyonlu) ──
# (soru, [seçenekler], doğru_idx)
_BULTEN_TEST = {
    9: [
        ("Okula uyum sürecinde en önemli faktör nedir?", ["Yüksek not almak", "Güvenli ve destekleyici ortam", "Çok ödev yapmak"], 1),
        ("Yeni bir ortama alışma süresi ortalama ne kadardır?", ["1 gün", "2-4 hafta", "6 ay"], 1),
        ("Okul kaygısı yaşayan birine ne söylersiniz?", ["Korkma, bir şey yok", "Hislerini anlıyorum, birlikte çözeriz", "Herkes gidiyor, sen de git"], 1),
        ("Düzenli uyku saati neden önemlidir?", ["Sadece büyükler için gerekli", "Dikkat ve öğrenmeyi güçlendirir", "Önemli değil"], 1),
        ("Yeni arkadaş edinmenin ilk adımı nedir?", ["Beklemek", "Gülümsemek ve merhaba demek", "Yalnız kalmak"], 1),
    ],
    10: [
        ("İyi bir arkadaşın en önemli özelliği nedir?", ["Her şeye evet demek", "Dinlemek ve saygı duymak", "Hediye almak"], 1),
        ("Arkadaşınızla anlaşmazlık yaşadığınızda ne yapmalısınız?", ["Konuşmayı kesmek", "Duygularınızı sakin şekilde ifade etmek", "Başkalarına şikâyet etmek"], 1),
        ("Empati ne demektir?", ["Aynı şeyleri sevmek", "Kendini karşıdakinin yerine koyabilmek", "Her zaman haklı olmak"], 1),
        ("Akran baskısına karşı en etkili yöntem nedir?", ["Kabul etmek", "Hayır diyebilme becerisi geliştirmek", "Gruptan ayrılmak"], 1),
        ("Sosyal medyada dikkat edilmesi gereken en önemli konu nedir?", ["Çok beğeni almak", "Kişisel bilgileri korumak", "Herkesi eklemek"], 1),
    ],
    11: [
        ("Sorumluluk duygusu nasıl gelişir?", ["Doğuştan gelir", "Küçük görevlerle adım adım kazanılır", "Sadece büyüyünce oluşur"], 1),
        ("Etkili zaman yönetiminin ilk adımı nedir?", ["Her şeyi birden yapmak", "Öncelikleri belirlemek ve plan yapmak", "Son dakikaya bırakmak"], 1),
        ("Atatürk'ün eğitim hakkındaki görüşü nedir?", ["Gereksiz", "Hayatta en hakiki mürşit ilimdir", "Sadece zenginler için"], 1),
        ("Öz düzenleme becerisi ne anlama gelir?", ["Başkalarını kontrol etmek", "Kendi davranış ve duygularını yönetebilmek", "Hiçbir şey yapmamak"], 1),
        ("Sınav kaygısıyla başa çıkmanın en iyi yolu nedir?", ["Hiç çalışmamak", "Düzenli çalışma ve nefes egzersizleri", "Kaygıyı görmezden gelmek"], 1),
    ],
    12: [
        ("Empati kurmanın en etkili yolu nedir?", ["Nasihat vermek", "Karşıdakini dinleyip anlamaya çalışmak", "Kendi deneyimini anlatmak"], 1),
        ("Yardımseverliğin bireye katkısı nedir?", ["Zaman kaybı", "Öz değer duygusunu güçlendirir", "Etkisi yoktur"], 1),
        ("İnsan Hakları Evrensel Bildirgesi ne zaman kabul edildi?", ["1923", "1948", "2000"], 1),
        ("Gönüllülük çalışması çocuklara ne kazandırır?", ["Sadece yorgunluk", "Sorumluluk ve toplumsal duyarlılık", "Hiçbir şey"], 1),
        ("Paylaşma alışkanlığı en etkili nasıl kazandırılır?", ["Zorlama ile", "Model olma ve deneyimleme ile", "Ceza ile"], 1),
    ],
    1: [
        ("Etkili bir hedef nasıl olmalıdır?", ["Belirsiz ve genel", "Somut, ölçülebilir ve zamanlı", "Başkalarının koyduğu"], 1),
        ("İçsel motivasyon nedir?", ["Ödül için çalışmak", "Öğrenme keyfi ve merakla hareket etmek", "Cezadan kaçmak"], 1),
        ("Başarısızlık karşısında en sağlıklı tutum nedir?", ["Vazgeçmek", "Öğrenme fırsatı olarak görmek", "Kendini suçlamak"], 1),
        ("Pozitif iç konuşma ne demektir?", ["Yüksek sesle konuşmak", "Kendine cesaret verici ve yapıcı düşünceler yöneltmek", "Sorunları görmezden gelmek"], 1),
        ("Dönem değerlendirmesi neden önemlidir?", ["Not kıyaslamak için", "Güçlü-zayıf yönleri görmek ve plan yapmak için", "Önemli değil"], 1),
    ],
    2: [
        ("Koşulsuz sevgi ne anlama gelir?", ["Her istediğini vermek", "Kişiyi olduğu gibi kabul etmek", "Hiç kızmamak"], 1),
        ("Zorbalığa tanık olduğunuzda ne yapmalısınız?", ["İzlemek", "Güvendiğiniz bir yetişkine söylemek", "Katılmak"], 1),
        ("Öz sevgi neden önemlidir?", ["Bencillik demektir", "Başkalarını sevmenin ön koşuludur", "Gereksizdir"], 1),
        ("Duygusal zekâ geliştirilebilir mi?", ["Hayır, doğuştandır", "Evet, farkındalık ve pratikle gelişir", "Sadece çocuklarda"], 1),
        ("Siber zorbalığa maruz kalırsanız ilk adım ne olmalıdır?", ["Karşılık vermek", "Ekran görüntüsü alıp güvendiğiniz birine söylemek", "Hesabı silmek"], 1),
    ],
    3: [
        ("Özgüven nasıl gelişir?", ["Sadece başarıyla", "Deneyim, destek ve öz kabul ile", "Başkalarının övgüsüyle"], 1),
        ("Büyüme zihniyeti ne demektir?", ["Zekânın sabit olduğuna inanmak", "Yeteneklerin çabayla geliştirilebileceğine inanmak", "Her şeyi bilmek"], 1),
        ("Beden imajı sorunlarıyla başa çıkmanın en iyi yolu nedir?", ["Diyet yapmak", "Kendini olduğu gibi kabul etmek ve sağlıklı yaşamak", "Sosyal medyadan uzak durmak"], 1),
        ("Her insanın eşsiz olması ne anlama gelir?", ["Bazıları daha iyidir", "Herkesin farklı güçlü yönleri vardır", "Fark etmez"], 1),
        ("Hata yapmak hakkında doğru olan nedir?", ["Başarısızlık demektir", "Öğrenmenin doğal bir parçasıdır", "Kaçınılmalıdır"], 1),
    ],
    4: [
        ("Düzenli kitap okumanın en büyük faydası nedir?", ["Vakit geçirmek", "Kelime haznesini, hayal gücünü ve empatiyi geliştirmek", "Ödev yerine saymak"], 1),
        ("Eleştirel okuma ne demektir?", ["Her şeye itiraz etmek", "Okuduğunu sorgulayarak ve analiz ederek anlamak", "Hızlı okumak"], 1),
        ("23 Nisan'ın önemi nedir?", ["Tatil günü", "Ulusal egemenlik ve çocuk haklarını kutlamak", "Sadece bayram"], 1),
        ("Dijital okuryazarlık neden önemlidir?", ["İnternette hız için", "Doğru bilgiyi yanlıştan ayırabilmek için", "Sosyal medya için"], 1),
        ("Hayal gücü neden değerlidir?", ["Sadece çocuklar için", "Problem çözme ve yaratıcılığın temelini oluşturur", "Gerçekçi değil"], 1),
    ],
    5: [
        ("Kaliteli aile zamanı için en önemli unsur nedir?", ["Pahalı aktiviteler", "Dikkat ve ilgiyi tam vermek", "Çok zaman ayırmak"], 1),
        ("Etkili iletişimde en önemli beceri nedir?", ["Çok konuşmak", "Aktif dinlemek", "Haklı olduğunu kanıtlamak"], 1),
        ("Ergenlikte aile ilişkilerinin değişmesi normal midir?", ["Hayır, sorun var", "Evet, bağımsızlık arayışının doğal sonucudur", "Bilmiyorum"], 1),
        ("Aile içi çatışma çözümünde en etkili yöntem nedir?", ["Sessiz kalmak", "Saygılı bir şekilde duyguları ifade etmek", "Bağırmak"], 1),
        ("Çocuğun kendini değerli hissetmesi için ne gerekir?", ["Sürekli övmek", "Koşulsuz kabul ve ilgi göstermek", "Her istediğini vermek"], 1),
    ],
    6: [
        ("Verimli bir yaz tatili için en önemli unsur nedir?", ["Hiçbir şey yapmamak", "Dinlenme ve gelişimi dengeleyen bir plan", "Sürekli ders çalışmak"], 1),
        ("Yaz okuma kaybını önlemenin yolu nedir?", ["Önemli değil", "Tatilde de düzenli okuma alışkanlığı sürdürmek", "Sadece ders kitabı okumak"], 1),
        ("Doğada vakit geçirmenin faydası nedir?", ["Etkisi yok", "Stresi azaltır, yaratıcılığı ve dikkati artırır", "Sadece eğlence"], 1),
        ("Karne değerlendirmesinde doğru yaklaşım nedir?", ["Ceza vermek", "Güçlü yönleri kutlayıp gelişim alanlarını birlikte planlamak", "Görmezden gelmek"], 1),
        ("Yaz tatilinde güvenli internet kullanımı için ne yapılmalı?", ["Serbest bırakmak", "Aile olarak kurallar belirlemek", "İnterneti tamamen yasaklamak"], 1),
    ],
}

# ── Vaka Örnekleri (ay bazlı, kademe adaptasyonlu) ──
# (hikâye, soru, doğru yaklaşım)
_BULTEN_VAKA = {
    9: ("Yeni okula baslayan Elif, her sabah aglayarak uyaniyor ve okula gitmek istemiyor. Sinifta da arkadaslariyla iletisim kurmaaktan kaciniyor ve teneffuslerde ogretmeninin yanindan ayrilmiyor. Annesi her sabah evden cikmak icin uzun sure ugriasiiyor ve artik ne yapacagini bilemiyor. Elif'in bu davranisi son iki haftadir devam ediyor ve giderek yogunlasiyor.",
     "Elif'in ailesine ve ogretmenine ne tavsiye edersiniz? Bu durumu normallestirebilir miyiz?",
     "Elif'in yasadigi ayrilik kaygisi, okula baslama doneminde cocuklarin yuzde yirmisinde gorulen normal bir gelisimsel tepkidir. Aileye su adimlar onerilir: Kisa ve guler yuzlu vedalasma rutini olusturun; uzun vedalar kaygiyi arttirir. Elif'in okuldaki olumlu deneyimlerini her aksam konusun ve 'Bugun en cok neyi sevdin?' gibi sorular sorun. Ogretmenle is birligi yaparak Elif'e sinifta kucuk sorumluluklar verin, bu aidiyet duygusunu guclendirir. Sabirli olun — uyum sureci genellikle 2-4 hafta surer, ancak 6 haftadan uzun surerse rehberlik servisiyle gorusun. Onemli olan tutarlilik ve sakinliktir; ebeveynin kaygisi cocuga yansir."),
    10: ("Ahmet, sinifta surekli dislanan bir arkadasinin oldugunu fark ediyor. Diger cocuklar onu oyunlara almiiyor, ogle yemeginde kimse yanina oturmuyor ve bazen arkaasindan dalga geciyorlar. Ahmet durumdan rahatsiz oluyor ama mudahale ederse kendisinin de dislanmasindan korkuyor. Bir yandan vicdan azabi cekiyor, diger yandan akran baskinsi hissediyor.",
     "Ahmet ne yapmalidir? Bu durumda sessiz kalmanin sonuclari nelerdir?",
     "Ahmet'in hissettigi ikilem cok anlasilir ve yasina gore normal bir tepkidir. Ancak sessiz kalmak — bystander olmak — zorbaligi dolayli olarak desteklemek anlamina gelir. Ahmet su admlari atabilir: Dislanan arkadasina yaklasip onu oyunlara davet edebilir; bazen tek bir kisi bile fark yaratir. Durumu guvendigi bir ogretmene veya rehberlik servisine bildirebilir. Arkadaslariyla konusarak dalga gecmenin nedenlerini sorgulayabilir. Onemli olan Ahmet'in empati kapasitesini gelistirmesi ve dogru olan icin cesaret gostermesidir. Sessiz kalmak yerine destekci rolu ustlenmek hem magdura yardimci olur hem de Ahmet'in oz degerini guclendirir. Sinifta 'zorbaliga hayir' bilinci olusturmak icin rehberlik servisiyle etkinlikler planlanabilir."),
    11: ("Zeynep odevlerini surekli unutuyor, projeleri son dakikaya birakiyor ve calismaya baslamakta zorlaniyor. Ailesi once uyardi, sonra kizdi, sonra ceza verdi — televizyonu yasakladilr, telefonunu aldilr — ama hicbiri ise yaramadi. Zeynep artik 'nasil olsa yapamiyorum' diyerek tamamen vazgecmis gorunuyor. Notlari dusuyor ve ogretmenleri de ailesine sikayet ediyor.",
     "Zeynep'e nasil yardimci olunabilir? Ceza neden ise yaramiyor?",
     "Ceza yaklasimi Zeynep'in durumunda ise yaramiyor cunku sorunun koku motivasyon ve organizasyon becerisi eksikligindedir, disiplin eksikligi degildir. Su yaklasim onerilir: Oncelikle cezalari kaldirin ve Zeynep'le birlikte bir planlama sistemi kurun — gorunur bir gorev cizelgesi, renkli ajanda veya haftaliik plan tablosu kullanin. Buyuk gorevleri kucuk adimlara bolerek baslangiic engelini azaltin. Her kucuk basariyi samimi sekilde takdir edin; 'Aferin, bugunku odevini zamaninda yaptin!' gibi spesifik geri bildirimler verin. Zeynep'in kendi odul sistemini olusturmasina izin verin. Sorumluluk aliskanligi zaman ve tutarlilikla kazanilir; sabr gerektirir. Eger durum devam ederse dikkat eksikligi acisindan uzman degerlendirmesi onerilir."),
    12: ("Mert, sinifinda bu yil yeni gelen engelli bir arkadasiyla nasil iletisim kuracagini bilemiyor. Tekerlekli sandalye kullanan arkadasini grdugunde ne soyleyecegini bilemiyor, yardim etmek istiyor ama yanlis bir sey yapmaktan korkuyor. Diger arkadaslari da benzer sekilde mesafe koyunca engelli ogrenci sinifta yalniz kaliyor ve teneffuslerde kimseyle konusmuyor.",
     "Mert'e ve sinifa ne soylenmeli? Engelli bireylere karsi nasil bir tutum gelismeldir?",
     "Mert'in tereddut hissetmesi anlasilir bir durumdur ve aslinda onun empati kapasitesinin yuksek oldugunu gosterir. Mert'e soyle yol gosterilebilir: Arkadasina ismiyle hitap etsin ve herhangi bir arkadasina davrandigi gibi davransin — engel bir kisitlama degil, farkli bir deneyim bicimidir. Yardim etmek istediginde 'Sana yardimci olabilir miyim?' diye sormasi yeterlidir; izin almadan yardim etmek bazen rahatsiz edici olabilir. Onu aktivitelere davet etsin, ogle yemeginde yanina otursun, ortak ilgi alanlarini kesfetsin. Sinif duzeyinde rehberlik servisi tarafindan farkindalik etkinlikleri duzenlenmelidir. Herkesin farkli guclu yonleri oldugunu, engelin bir insani tanimlmadigini ve empatinin mesafeyi azalttigini vurgulayin. Kapsayici bir sinif ortami herkesin kazanmasidir."),
    1: ("Selin, birinci donem sinav sonuclari dusuk gelince tamamen motivasyonunu kaybetti. 'Ben aptalim, yapamam, ne kadar calisssam da olmuyor' diyerek kendini olumsuz etiketliyor. Derslerine calismay tamamen birakti, okulda donuk ve ilgisiz gorunuyor. Ailesi baskilya daha cok calismaya zorlayinca Selin daha da icerine kapandi ve aglamaya basladi.",
     "Selin'e nasil yaklasailmalidir? Bu olumsuz ic konusma nasil degistirilir?",
     "Selin'in yasadigi ogrenilmis caresizlik olarak tanimlanan bir durumdur ve ciddi sekilde ele alinmalidir. Oncelikle baskiyi tamamen kaldirin; baski motivasyonu artirmaz, aksine kaygiyi ve caresizlik hissini derinlestirir. Selin'le sefkatli bir sohbet kurun: 'Seni anliyorum, bu cok zor bir dnem olmus' diyerek duygularini onaylayin. Ardindan dusuncelerini sorgulamasina yardimci olun: 'Gercekten yapamaz misin yoksa henuz dogru yontemi bulamaadin mi?' Kucuk, ulsilabilir hedefler koyun — ornegin tek bir derste 5 puanlik iyilesme. Her basariyi kaydedin ve gosterin. 'Ben' dilini degistirin: 'Ben aptalim' yerine 'Bu konuyu henuz ogrenemedim' Basarisizlik son degil, ogrenme firsatidir. Gerekirse rehberlik servisi bireysel gorusmeler planlasin."),
    2: ("Can, sosyal medyada bir arkadasinin fotografinin altna kotu yorumlar yapildigini ve baska bir grupta onun hakkinda asagilayci mesajlar paylasildigini goruyor. Arkadasi bu durumdan habersiz gorunuyor ama Can fark ediyor. Can hem arkadasini korumak istiyor hem de durumu bildirirse kendisinin de hedef olmasindan endise ediyor. Grupta bazi yakin arkadaslari da var ve onlarla arasinin bozulmasindan korkuyor.",
     "Can ne yapmalidir? Siber zorbalik karsisinda sessiz kalmak dogru mudur?",
     "Siber zorbalik fiziksel zorbalik kadar zararlidir ve hatta kalici dijital izler biraktiigi icin daha da yikici olabilir. Can su adimlari atmalidir: Oncelikle ekran goruntuleri alip delil olarak saklasin — bu kanit sonraki asamalarda kritik oneme sahiptir. Guvendigi bir yetiskine (ogretmen, aile, rehberlik servisi) durumu bildirsin; bu ihbar degil, sorumluluk biilincidir. Zorbaliga katilmamali veya paylasmalari begenmemelidir. Magdur arkadasina destek oldugunu gostersin: 'Bunlari gordum, yanindayim' demesi bile buyuk fark yaratir. Can'in korkusu anlasilir ancak sessiz kalmak zorbaligi desteklemek anlamina gelir. Okulda siber zorbalik farkindalik programlari duzenlenmeli ve dijital vatandaslik egitimi verilmelidir. Gerekirse hukuki sureclerin baslatilabileecegi de aileye bildirilmelidir."),
    3: ("Ayse, son zamanlarda arkadaslari gibi gorunmediiii icin kendini begenmiyor. Sosyal medyadaki filtrelii fotograflarla kendisini karsilastiriyor ve surekli aynaya bakip uzuluyor. Eskiden sevdigi etkinliklere katilmak istemiyor, spor kiyafetlerini giymekten kaciniyor ve sinifta kendini geri planda tutuyor. Annesi Ayse'nin yeme aliskanliklrinda da degisiklikler fark etti — bazi ogunleri atlamaya basladi.",
     "Ayse'ye nasil destek olunabilir? Beden imgesi sorunlari ne zaman ciddi kabul edilmelidir?",
     "Ayse'nin yasadigi ergenlik doneminde oldukca yaygin olan bir beden imgesi sorunudur ancak yeme aliskanliklarindaki degisim ciddi bir uyari isaretidir. Su adimlar onerilir: Medyadaki goruntulerin duzenlenemis ve gercekci olmaadigini somut orneklerle konusun; filtre oncesi-sonrasi karsilastirmalar gosterin. Ayse'nin guclu yonlerini ve yeteneklerini fark ettirin — dis gorunus bir insanin degerinin yalnizca kucuk bir parcasidir. Aile olarak dis gorunusle ilgili yorumlardan tamamen kacinin ve karakter ile cabay ovun. Yeme aliskanliiklarindaki degisim, beden imajindaki memnuniyetsizlik ve sosyal cekilme bir arada goruldugunde mutlaka profesyonel destek alin — cocuk psikolougu veya ergen uzmani yonlendirmesi yapin. Erken mudahale bu tur sorunlarda kritik onem tasir."),
    4: ("Burak, hic kitap okumak istemiyor ve her firsatta 'Kitaplar sikici, neden okumam gerekiyor ki?' diyor. Ailesi zorlaynca odaine kapanip telefonuyla ilgileniyor. Ogretmeni de okuma odevlerini yapmadigindan sikayet ediyor. Aslinda Burak zeki ve merakli bir cocuk ama yazili metinlere karsi bir dirensi olusmus. Bilgisayar oyunlarinda karmasik hikayeleri takip edebiliyor ama kitabn elii almak istemiyor.",
     "Burak'in okuma aliskanligi nasil gelistiirlir? Zorlama dogru bir yontem midir?",
     "Zorlama okuma aliiskanliigii kazandirmakta en etkisiz yontemdir; hatta kitaba karsi olumsuz cagrisim yaratarak durumu daha da ktulestirebilir. Burak'in bilgisayar oyunlarindaki karmasik hikayeleri takip edebilmesi, onun anlama becerisinin iyi oldugunu gosterir — sorun kapasite degil motivasyondur. Su yaklasim onerilir: Ilgi alanina uygun kitaplar onerin — spor, bilim kurgu, cizgi roman, fantastik kurgu, macera hikayeleri. Birlikte kitapciya veya kutuphaaneye gidin ve kendi secmesine izin verin; secim ozgirluugu motivasyonu arttirir. Sesli kitap veya e-kitap seceneklerini deneyin — farkli formatllar farki cocuklara hitap eder. Evde bir 'okuma saati' geleneigi baslatin ve model olun: cocuk okumamiizi gorurse okumaya daha olumlu bakacaktir. Kitap hakkinda sohbet edin ama sorgulamaktan kacinin. Sabir gosterin; okuma aliskanligi zorlamayla degil, keyif ve kesfle kazanilir."),
    5: ("Deniz'in ailesi son aylarda surekli tartisiyor. Gece geç saatlere kadar yuksek sesle kavga ediyorlar ve bazen Deniz'in odasina kadar duyuluyor. Deniz okulda dikkati dagink ve mutsuz gorunuyor, ders basaairsi dustu ve eskiden cok aktif oldugu etkinlilklere katilmak istemiyor. Ogretmeni Deniz'in bazen ders sirasinda agladiigini fark etti. Deniz kimseye bir sey anlatmiyor ve soruldiginda 'Bir seyim yok' diyor.",
     "Deniz'e nasil destek olunabilir? Aile ici catismanin cocuklar uzerindeki etkileri nelerdir?",
     "Aile ici catisma cocuklarin duygusal sagligini derinden etkiler; surekli catismaya tanik olan cocuklarda kaygi, depresyon, dikkat sorunlari ve davranis bozukluklari gorulebilir. Deniz'e yaklasirken su adimlar izlenmelidir: Guvenli ve yargilamayan bir dinleme ortami olusturun — 'Seni dinlemek istiyorum, istedigin zaman konusabiliriz' mesaajini verin. Sucun asla kendisinde olmadigini acikca ve tekrarlayarak vurgulayiin; cocuklar sikllikla ebeveyn kavgalarindan kendilerini sorumlu tutarlar. Hislerini ifade etmesine izin verin ve duygularini normalleestirin. Rehberlik servisi duzenlii bireysel gorusmeler planlasin. Aileye mutlaka aile danismanligi yonlendirmesi yapin. Cocugun okul performansindaki dusus ve sosyal cekilme ciddi uyari isaretleridir ve erken mudahale gerektirir."),
    6: ("Ege, yaz tatlinde hic disari cikmiyor. Sabah kalktiigindan gece yatana kadar telefon, tablet ve bilgisayar basinda vakit geciriyor. Arkaadaslariyla bile sadece online oyunlar uzerinden iletisim kuruyor. Fiziksel aktivitesi nerdeyse sifir, uyku duzeni tamamen bozulmus — gece 3'te yatiyor, ogle sonrasi kalkiyor. Ailesi konusmayi denedi ama Ege 'Arkadaslarimla oynuyorum, ne var bunda?' diyerek savasvasiyor.",
     "Ege'nin ailesi ne yapmalidir? Asiri ekran kullainminin riskleri nelerdir?",
     "Asiri ekran kullanimi uyku bozukluugu, obezite, sosyal izolasyon, dikkat eksikligi ve hatta depresif belirtilere yol aacabilir. Ege'nin ailesine su yaklasim onerilir: Tamamen yasaklamak yerine birlikte dengeli kurallar belirleyin — ornegin gunluk 2-3 saat ekran suresi siniri ve gece 11'den sonra cihazlarin kapanmasi. Alternatif aktiviteler sunun ve mumkunse birlikte katiilin: yuzme kursu, bisiklet turu, aile yuruyusleri, spor kampi, yaz okulu. Arkadaslariyla yuzyuze bulusmaa firsatlari yaratin — evde oyun gecesi, parkta bulusma. Ekran suresini izlemek icin aile filtreleme uygulamalari kullanin. En onemlisi, otoriter bir tutum yerine isbirligi yaklasimi benimseyin: 'Birlikte bir plan yapalim' demek 'Yasakliyorum' demekten cok daha etkilidir. Uyku duzeninin duzeltilmesi oncelikli hedef olmalidir cunku diger sorunlarin cogu uyku duzensizligiyle bagaantilidir."),
}

# ── Aylık Kontrol Listesi (ay bazlı, genel) ──
_BULTEN_CHECKLIST = {
    9: ["Okul çantasını ve malzemelerini hazırladım", "Uyku düzenimi ayarladım", "Yeni arkadaşlarımla tanıştım", "Sınıf kurallarını öğrendim", "Haftalık ders programımı biliyorum"],
    10: ["Bu ay yeni bir arkadaşlık kurdum", "Bir arkadaşıma yardım ettim", "Duygularımı sağlıklı ifade ettim", "Farklılıklara saygı gösterdim", "Empati kurma pratiği yaptım"],
    11: ["Haftalık çalışma planımı oluşturdum", "Sorumluluklarımı zamanında yerine getirdim", "Atatürk hakkında yeni bir şey öğrendim", "Zamanımı etkili kullandım", "Öğretmenime minnettarlığımı ifade ettim"],
    12: ["Birine yardım eli uzattım", "Duygularımı tanıyıp ifade ettim", "Bir paylaşma eylemi gerçekleştirdim", "İnsan haklarını araştırdım", "Yılın güzel anılarını not ettim"],
    1: ["Yeni dönem hedeflerimi yazdım", "Çalışma düzenimi güncelledim", "Motivasyon kaynağımı belirledim", "Olumlu iç konuşma pratiği yaptım", "Geçen dönemi değerlendirdim"],
    2: ["Sevdiklerime sevgimi ifade ettim", "Bir iyilik eylemi gerçekleştirdim", "Kendimi olduğum gibi kabul ettim", "Zorbalıkla mücadele bilgimi güncelledim", "Bir değerimi fark edip yaşadım"],
    3: ["Güçlü yönlerimi listeledim", "Yeni bir şey denedim", "Hata yaptığımda kendime nazik davrandım", "Bireysel farklılıklara saygı gösterdim", "Özgüvenimi besleyen bir başarı yaşadım"],
    4: ["Bu ay en az bir kitap okudum", "Kütüphaneye gittim", "Okuduğum kitabı birine anlattım", "Eleştirel düşünme pratiği yaptım", "23 Nisan'ın anlamını düşündüm"],
    5: ["Ailemle kaliteli vakit geçirdim", "Dinleme becerimi geliştirdim", "Duygularımı aileme açtım", "Anneler Gününü kutladım", "Aile kurallarına uydum"],
    6: ["Yaz tatili planımı oluşturdum", "Karnemi sakin bir şekilde değerlendirdim", "Yaz okuma listemi hazırladım", "Açık havada aktivite planladım", "Bu yılın kazanımlarını not ettim"],
}

# ── Kaynak Önerileri (kademe grubu bazlı) ──
# kucuk = Anaokulu+İlkokul, buyuk = Ortaokul+Lise
# ── Veli Köşesi (ay bazlı, kademe gruplu) ──
# kucuk = Anaokulu+İlkokul, buyuk = Ortaokul+Lise
_BULTEN_VELI = {
    9: {"kucuk": {
        "mesaj": "Yeni eğitim öğretim yılına hoş geldiniz! Çocuğunuzun okula uyum sürecinde en büyük destekçisi sizsiniz.",
        "etkinlikler": ["Birlikte okul çantası hazırlayın ve heyecanı paylaşın", "Her akşam 'Bugün okulda ne öğrendin?' sohbeti kurun", "Yatmadan önce ertesi günün programını birlikte konuşun"],
        "ipucu": "Vedalaşırken kısa ve güler yüzlü olun. 'Öğleden sonra seni alacağım' gibi net zaman ifadeleri kaygıyı azaltır."
    }, "buyuk": {
        "mesaj": "Ergenlik döneminde çocuğunuz daha bağımsız olmak isteyebilir. Bunu kişisel almayın — bu gelişimsel bir ihtiyaçtır.",
        "etkinlikler": ["Ders programını birlikte inceleyin, ama organizasyonu ona bırakın", "Hafta sonu bir aile kahvaltısı geleneği başlatın", "Hedeflerini konuşup bir 'başarı duvarı' oluşturun"],
        "ipucu": "Soru sormak yerine paylaşım davet edin: 'Bugün ilginç bir şey oldu mu?' gibi açık uçlu sorular tercih edin."
    }},
    10: {"kucuk": {
        "mesaj": "Bu ay arkadaşlık ve sosyal beceriler üzerinde çalışıyoruz. Evde de bu becerileri destekleyebilirsiniz.",
        "etkinlikler": ["Çocuğunuzun bir arkadaşını eve davet edin", "Birlikte bir paylaşma oyunu oynayın (kutu oyunu vb.)", "Empati hikâyeleri okuyup karakterlerin duygularını konuşun"],
        "ipucu": "Çocuğunuz arkadaşlık sorunu yaşarsa dinleyin ve çözüm önerin ama kararı ona bırakın. Sosyal becerileri deneyimle öğrenirler."
    }, "buyuk": {
        "mesaj": "Ergenlik döneminde akran ilişkileri çok önemlidir. Çocuğunuzun arkadaşlık dinamiklerini merakla ama saygıyla takip edin.",
        "etkinlikler": ["Çocuğunuzun arkadaş grubunu tanımaya çalışın", "Siber zorbalık konusunu açık bir şekilde konuşun", "Sağlıklı sınır koyma becerisini birlikte pratik edin"],
        "ipucu": "Arkadaşlarını eleştirmek yerine 'Bu durumda nasıl hissettin?' gibi sorularla farkındalık oluşturun."
    }},
    11: {"kucuk": {
        "mesaj": "Kasım ayında sorumluluk ve öz düzenleme becerilerini destekliyoruz. Evdeki küçük görevler büyük fark yaratır.",
        "etkinlikler": ["Yaşına uygun bir ev görevi verin (masa toplama, çiçek sulama)", "Birlikte basit bir haftalık plan oluşturun", "10 Kasım'da Atatürk hakkında birlikte araştırma yapın"],
        "ipucu": "Çocuğunuz görevi unuttuğunda azarlamak yerine hatırlatıcı sistem kurun. Tutarlılık cezadan daha etkilidir."
    }, "buyuk": {
        "mesaj": "Sorumluluk almak ergenliğin en önemli gelişim görevlerinden biridir. Güvenerek bırakın, hatalardan öğrensinler.",
        "etkinlikler": ["Ders çalışma planını birlikte yapın ama uygulamayı ona bırakın", "Atatürk'ün liderlik özelliklerini tartışın", "Zaman yönetimi uygulaması kullanmayı önerin"],
        "ipucu": "Sürekli hatırlatma yerine doğal sonuçları deneyimlemesine izin verin. Ödevi unutursa sorumluluğu kendisi yaşasın."
    }},
    12: {"kucuk": {
        "mesaj": "Aralık ayı paylaşma, empati ve yardımseverlik temasıyla dolu. Birlikte güzel işler yapmanın tam zamanı!",
        "etkinlikler": ["Birlikte bir yardım kuruluşuna bağış hazırlayın", "Komşulara/yaşlılara yardım ziyareti düzenleyin", "Yılın güzel anılarını birlikte fotoğraflardan seçip albüm yapın"],
        "ipucu": "Paylaşma davranışını zorlama yerine model olarak öğretin. 'Birlikte verelim' demek 'ver' demekten daha etkilidir."
    }, "buyuk": {
        "mesaj": "Yıl sonu değerlendirmesi ve empati gelişimi için güzel bir ay. Çocuğunuzla açık ve yargılamadan konuşun.",
        "etkinlikler": ["İnsan hakları konusunda birlikte belgesel izleyin", "Bir gönüllülük projesine birlikte katılın", "Yılın artı ve eksilerini samimi bir sohbetle değerlendirin"],
        "ipucu": "Karne dönemine yaklaşırken not baskısı kurmak yerine çabayı takdir edin. 'Ne öğrendin?' sorusu 'Kaç aldın?' sorusundan değerlidir."
    }},
    1: {"kucuk": {
        "mesaj": "Yeni yıl, yeni hedefler! Çocuğunuzla birlikte küçük ama somut hedefler koymak motivasyonunu artırır.",
        "etkinlikler": ["Birlikte 3 yeni yıl hedefi belirleyin ve görünür bir yere asın", "Her hafta hedef takip sohbeti yapın", "Çocuğunuzla birlikte bir başarı günlüğü tutmaya başlayın"],
        "ipucu": "Hedefler çocuğun kendi istekleriyle belirlenmelidir. Sizin hedeflerinizi onlara dayatmak yerine 'Sen ne yapmak istersin?' diye sorun."
    }, "buyuk": {
        "mesaj": "İkinci dönem yeni bir başlangıç fırsatıdır. Geçen dönemin değerlendirmesini yapıcı ve destekleyici bir şekilde yapın.",
        "etkinlikler": ["Geçen dönemi not üzerinden değil, kazanımlar üzerinden değerlendirin", "Yeni dönem için SMART hedefler koyun", "Motivasyon kaynağını birlikte keşfedin (spor, müzik, sanat)"],
        "ipucu": "Karşılaştırma yapmayın. 'Ali daha iyi yapıyor' yerine 'Geçen döneme göre şurada geliştin' deyin."
    }},
    2: {"kucuk": {
        "mesaj": "Şubat ayı sevgi ve değerler temasıyla çocuğunuzun duygusal gelişimini destekleme zamanı.",
        "etkinlikler": ["Her gün bir 'seni seviyorum' notu bırakın çantasına", "Birlikte bir değerler ağacı çizin (dürüstlük, saygı, sevgi)", "Zorbalık konusunda yaşına uygun bir sohbet başlatın"],
        "ipucu": "Koşulsuz sevgi = 'Seni her zaman severim, bazen davranışını sevmem' ayrımını net yapın."
    }, "buyuk": {
        "mesaj": "Ergenlikte duygusal iniş çıkışlar normaldir. Yargılamadan dinlemek en güçlü desteğinizdir.",
        "etkinlikler": ["Siber güvenlik kurallarını birlikte gözden geçirin", "Sağlıklı ilişki özelliklerini konuşun", "Çocuğunuza öz değerini hatırlatan bir mektup yazın"],
        "ipucu": "Ergenlerin duygularını küçümsemeyin. 'Abartıyorsun' yerine 'Zor bir dönem geçirdiğini görüyorum' deyin."
    }},
    3: {"kucuk": {
        "mesaj": "Mart ayında özgüven ve bireysel farklılıklar üzerinde çalışıyoruz. Her çocuk benzersizdir!",
        "etkinlikler": ["Çocuğunuzun güçlü yönlerini birlikte listeleyin", "Yeni bir hobi denemesine destek olun", "Hata yapmanın öğrenmenin bir parçası olduğunu hikâyelerle anlatın"],
        "ipucu": "Çocuğunuzu başkalarıyla kıyaslamayın. 'Sen çok güzel resim yapıyorsun' yerine 'Sen çok emek vermişsin' deyin — çabayı övün."
    }, "buyuk": {
        "mesaj": "Ergenlikte beden imajı ve özgüven hassas konulardır. Destekleyici ve kabul edici bir ortam sunun.",
        "etkinlikler": ["Medya okuryazarlığı: filtrelerin ve düzenlemenin gerçeği nasıl değiştirdiğini konuşun", "Çocuğunuzun yeteneklerini keşfetmesi için farklı aktiviteler önerin", "Birlikte bir 'güçlü yönler kartı' oluşturun"],
        "ipucu": "Ergenlerin dış görünüşüyle ilgili yorumlardan kaçının. Karakter ve çaba odaklı geri bildirim verin."
    }},
    4: {"kucuk": {
        "mesaj": "Nisan ayı kitap okuma ve hayal gücü temasıyla dolu. Okuyan çocuk, düşünen çocuktur!",
        "etkinlikler": ["Her gece yatmadan önce birlikte 15 dakika kitap okuyun", "Kütüphaneye gidin, çocuğunuz kendi kitabını seçsin", "Okuduğunuz hikâyenin devamını birlikte hayal edin"],
        "ipucu": "Kitap seçimini çocuğa bırakın. Çizgi roman bile olsa okuma alışkanlığı kazandırmak önemlidir."
    }, "buyuk": {
        "mesaj": "Ergenler için okuma alışkanlığı eleştirel düşünme ve empati gelişiminin temelidir.",
        "etkinlikler": ["Aynı kitabı okuyup birlikte tartışın (aile kitap kulübü)", "23 Nisan'ın anlamını ve çocuk haklarını konuşun", "Bir kitap hediye edin — ilgi alanına uygun seçin"],
        "ipucu": "Okumayı ceza veya zorunluluk olarak sunmayın. Kendiniz de okuyarak model olun."
    }},
    5: {"kucuk": {
        "mesaj": "Mayıs ayı aile bağlarını güçlendirme zamanı. En değerli hediye: zaman ve ilgidir.",
        "etkinlikler": ["Teknolojisiz bir aile akşamı düzenleyin", "Anneler Günü için birlikte el yapımı hediye hazırlayın", "Çocuğunuzla sadece ikisinin olduğu özel bir gün planlayın"],
        "ipucu": "Kaliteli zaman uzun olmak zorunda değil. Tam dikkatle geçirilen 15 dakika, dalgın 3 saatten değerlidir."
    }, "buyuk": {
        "mesaj": "Ergenlik döneminde aile iletişimi zorlaşabilir ama kopmamalıdır. Açık kapı politikası uygulayın.",
        "etkinlikler": ["Haftada bir 'serbest konu' sohbeti yapın — gündem yok, yargılama yok", "Birlikte yemek pişirin veya bir aktivite seçin", "Ergenin mahremiyetine saygı gösterin ama ilginizi belli edin"],
        "ipucu": "Ergenlerle iletişim kurmak için araba yolculukları idealdir — göz teması yok, kaçış yok, sohbet akar."
    }},
    6: {"kucuk": {
        "mesaj": "Yaz tatili eğlence ve dinlenme zamanı ama yapılandırılmış bir plan gelişimi destekler.",
        "etkinlikler": ["Birlikte yaz tatili planı oluşturun (okuma, gezi, spor)", "Her gün en az 20 dakika okuma zamanı koyun", "Doğada vakit geçirin: piknik, yürüyüş, bahçe işleri"],
        "ipucu": "Ekran süresini tamamen yasaklamak yerine birlikte kurallar belirleyin. Denge anahtardır."
    }, "buyuk": {
        "mesaj": "Yaz tatili hem dinlenme hem kişisel gelişim fırsatıdır. Ergenlerin sorumluluğu paylaşmasını bekleyin.",
        "etkinlikler": ["Yaz stajı, kamp veya gönüllülük projesi araştırın", "Yeni bir beceri öğrenmeye teşvik edin (dil, müzik, kodlama)", "Karne sonuçlarını sakin ve yapıcı bir şekilde değerlendirin"],
        "ipucu": "Karneyi ceza/ödül aracı yapmayın. 'Bu sonuçtan ne öğrendin ve gelecek dönem ne değiştirmek istersin?' sorun."
    }},
}

# ── Ayın Hedef Planı (ay bazlı, motivasyonel cümleler) ──
_BULTEN_HEDEF = {
    9: {"baslik": "Yeni Başlangıçlar", "soz": "Bu ay kendime söz veriyorum...", "degerlendir": "İlk ayımı nasıl geçirdim?",
        "hedefler": ["Okulumda kendimi güvende hissetmeye çalışacağım", "En az bir yeni arkadaş edinmeye çalışacağım", "Ders programıma uyum sağlayacağım"],
        "duygular": [("Heyecanlı", "🤩"), ("Kaygılı", "😟"), ("Meraklı", "🧐"), ("Mutlu", "😊"), ("Kararsız", "🤔")]},
    10: {"baslik": "Arkadaşlık Hedefleri", "soz": "Bu ay arkadaşlık için...", "degerlendir": "Arkadaşlıklarım nasıl gidiyor?",
        "hedefler": ["Bir arkadaşımın yanında olacağım", "Farklılıklara saygı göstereceğim", "Empati kurmaya çalışacağım"],
        "duygular": [("Güvenli", "😌"), ("Huzurlu", "🥰"), ("Enerjik", "⚡"), ("Düşünceli", "🤔"), ("Neşeli", "😄")]},
    11: {"baslik": "Sorumluluk Hedefleri", "soz": "Bu ay sorumluluklarım için...", "degerlendir": "Sorumluluklarımı nasıl yerine getirdim?",
        "hedefler": ["Ödevlerimi zamanında yapacağım", "Odamı düzenli tutacağım", "Zaman planıma uyacağım"],
        "duygular": [("Kararlı", "💪"), ("Disiplinli", "📋"), ("Gurur", "🏆"), ("Yorgun", "😓"), ("Motive", "🔥")]},
    12: {"baslik": "Paylaşma ve Empati", "soz": "Bu ay paylaşmak için...", "degerlendir": "Bu ay kimlere yardım ettim?",
        "hedefler": ["Birine yardım eli uzatacağım", "Paylaşma yapacağım", "Empati kurma pratiği yapacağım"],
        "duygular": [("Cömert", "🤲"), ("Şükran", "🙏"), ("Huzurlu", "😌"), ("İlgili", "💝"), ("Kıymetli", "⭐")]},
    1: {"baslik": "Yeni Dönem Hedefleri", "soz": "İkinci dönem için kendime söz veriyorum...", "degerlendir": "Geçen dönemi nasıl değerlendiriyorum?",
        "hedefler": ["Derslerime düzenli çalışacağım", "Yeni bir beceri öğreneceğim", "Motivasyonumu yüksek tutacağım"],
        "duygular": [("Umutlu", "🌟"), ("Azimli", "💪"), ("Odaklanmış", "🎯"), ("Heyecanlı", "🤩"), ("Kararlı", "✊")]},
    2: {"baslik": "Sevgi ve Değer Hedefleri", "soz": "Bu ay sevgi için...", "degerlendir": "Kendimi ne kadar değerli hissediyorum?",
        "hedefler": ["Kendime nazik davranacağım", "Sevdiklerime sevgimi göstereceğim", "Zorbalığa karşı duracağım"],
        "duygular": [("Sevilmiş", "❤️"), ("Güçlü", "💪"), ("Güvenli", "🛡️"), ("Değerli", "💎"), ("Huzurlu", "😌")]},
    3: {"baslik": "Özgüven Hedefleri", "soz": "Bu ay kendime güvenmek için...", "degerlendir": "Kendimle barışık mıyım?",
        "hedefler": ["Güçlü yönlerimi keşfedeceğim", "Yeni bir şey denemeye cesaret edeceğim", "Hata yapınca kendimi affetmeyi öğreneceğim"],
        "duygular": [("Cesur", "🦁"), ("Özgüvenli", "⭐"), ("Meraklı", "🔍"), ("Kabul", "🤗"), ("Güçlü", "💪")]},
    4: {"baslik": "Okuma ve Keşif Hedefleri", "soz": "Bu ay okumak için...", "degerlendir": "Bu ay neler okudum?",
        "hedefler": ["En az bir kitap okuyacağım", "Kütüphaneye gideceğim", "Okuduğumu birine anlatacağım"],
        "duygular": [("İlham", "✨"), ("Hayal kuran", "🌈"), ("Bilge", "🦉"), ("Keşfeden", "🔭"), ("Zenginleşmiş", "📚")]},
    5: {"baslik": "Aile Bağı Hedefleri", "soz": "Bu ay ailem için...", "degerlendir": "Aileme ne kadar vakit ayırdım?",
        "hedefler": ["Ailemle kaliteli vakit geçireceğim", "Duygularımı ailemle paylaşacağım", "Ev işlerine yardım edeceğim"],
        "duygular": [("Minnettar", "🙏"), ("Bağlı", "🔗"), ("Huzurlu", "😌"), ("Sevecen", "🤗"), ("Güvende", "🏠")]},
    6: {"baslik": "Yaz Planı ve Değerlendirme", "soz": "Bu yaz tatilinde...", "degerlendir": "Bu yılı nasıl geçirdim?",
        "hedefler": ["Bir yaz okuma listesi oluşturacağım", "Yeni bir aktivite deneyeceğim", "Dinleneceğim ama gelişmeye devam edeceğim"],
        "duygular": [("Özgür", "🕊️"), ("Heyecanlı", "🤩"), ("Dinlenmiş", "😴"), ("Başarılı", "🏅"), ("Umutlu", "🌟")]},
}

_BULTEN_KAYNAKLAR = {
    9: {"kucuk": {"kitap": ["Okula Başlıyorum — Anna Kang", "İlk Günüm — Debi Gliori"], "video": ["Susam Sokağı — Okula Uyum", "TRT Çocuk — İlk Gün Heyecanı"], "uygulama": ["Khan Academy Kids", "Sago Mini Okul"]},
        "buyuk": {"kitap": ["Çocuk ve Ergen Gelişimi — Santrock", "Ergenlik Rehberi — Doğan Cüceloğlu"], "video": ["TED — Okula Uyum", "BrainPop — Stres Yönetimi"], "uygulama": ["Headspace", "Forest — Odaklanma"]}},
    10: {"kucuk": {"kitap": ["Küçük Prens — Saint-Exupéry", "Arkadaşım Olmak İster misin? — Eric Carle"], "video": ["TRT Çocuk — Arkadaşlık", "Sesame Street — Paylaşma"], "uygulama": ["Toca Life World", "PBS Kids Games"]},
         "buyuk": {"kitap": ["Duygusal Zekâ — Daniel Goleman", "Cesur Yeni Dünya — Aldous Huxley"], "video": ["TED — Empati ve İletişim", "Crash Course — Psikoloji"], "uygulama": ["Calm", "Moodfit"]}},
    11: {"kucuk": {"kitap": ["Atatürk — Yılmaz Özdil (Çocuk)", "Sorumluluk Benim İşim — Todd Parr"], "video": ["TRT Çocuk — Sorumluluk", "Animasyonlarla Atatürk"], "uygulama": ["Todoey Kids", "Epic! Okuma"]},
         "buyuk": {"kitap": ["Nutuk — Mustafa Kemal Atatürk", "7 Etkili Alışkanlık — Stephen Covey"], "video": ["TED — Zaman Yönetimi", "TRT — 10 Kasım Anma"], "uygulama": ["Todoist", "Notion"]}},
    12: {"kucuk": {"kitap": ["Gökkuşağı Balığı — Marcus Pfister", "Paylaşmak Güzeldir — Mo Willems"], "video": ["TRT Çocuk — Yardımlaşma", "İnsan Hakları Animasyonu"], "uygulama": ["Khan Academy Kids", "Sago Mini Friends"]},
         "buyuk": {"kitap": ["Suç ve Ceza — Dostoyevski", "Hayvan Çiftliği — George Orwell"], "video": ["TED — Gönüllülük", "İnsan Hakları Belgeseli"], "uygulama": ["GoVolunteer", "UN Refugee App"]}},
    1: {"kucuk": {"kitap": ["Yapabilirim! — Lois Ehlert", "Büyük Hayaller — Isabel Thomas"], "video": ["TRT Çocuk — Hedef Koyma", "Motivasyon Şarkıları"], "uygulama": ["ClassDojo", "Tynker Kids"]},
        "buyuk": {"kitap": ["Atomik Alışkanlıklar — James Clear", "Mindset — Carol Dweck"], "video": ["TED — Motivasyon Bilimi", "Ali Biçim — Hedef Belirleme"], "uygulama": ["Habitica", "Streaks"]}},
    2: {"kucuk": {"kitap": ["Seni Seviyorum — Sam McBratney", "Kırmızı Balık — Luo Ling"], "video": ["TRT Çocuk — Sevgi", "Animasyonlarla Değerler"], "uygulama": ["Breathe Kids", "Smiling Mind"]},
        "buyuk": {"kitap": ["Aşk — Erich Fromm", "Dönüşüm — Franz Kafka"], "video": ["TED — Kırılganlığın Gücü", "Siber Zorbalık Belgeseli"], "uygulama": ["ReThink", "STOPit"]}},
    3: {"kucuk": {"kitap": ["Farklı Ama Aynı — Todd Parr", "Ben Özelim — Karen Beaumont"], "video": ["TRT Çocuk — Kendini Tanı", "Sesame Street — Özgüven"], "uygulama": ["Moxie AI", "Sesame Workshop"]},
        "buyuk": {"kitap": ["Kendine Güven — Nathaniel Branden", "Var mısın? — Cüneyt Özdemir"], "video": ["TED — Beden Dili ve Özgüven", "Kişilik Testi Rehberi"], "uygulama": ["16Personalities", "MindShift"]}},
    4: {"kucuk": {"kitap": ["Küçük Prens — Saint-Exupéry", "MEB 365 Gün Öykü"], "video": ["TRT Çocuk — Masal Zamanı", "Sesli Kitap — Çocuk Klasikleri"], "uygulama": ["Epic! Okuma", "Duolingo ABC"]},
        "buyuk": {"kitap": ["Simyacı — Paulo Coelho", "1984 — George Orwell"], "video": ["TED — Okumanın Gücü", "Kitap Kulübü Rehberi"], "uygulama": ["Goodreads", "Kindle"]}},
    5: {"kucuk": {"kitap": ["Annem Nerede? — Julia Donaldson", "Babamla Gün — Yusuf Kaplan"], "video": ["TRT Çocuk — Aile", "Anneler Günü Etkinlikleri"], "uygulama": ["Family Link", "Canva Kids"]},
        "buyuk": {"kitap": ["Aile Terapisi — Virginia Satir", "Duyguların Dili — Adele Faber"], "video": ["TED — Aile İletişimi", "Ergenlik ve Aile"], "uygulama": ["Family Wall", "OurHome"]}},
    6: {"kucuk": {"kitap": ["Yaz Tatilim — Mehmet Güler", "Deniz Macerası — Julia Donaldson"], "video": ["TRT Çocuk — Güvenli Yaz", "Doğa Belgeseli"], "uygulama": ["Nature Cat", "PBS Outdoor"]},
        "buyuk": {"kitap": ["Siddhartha — Hermann Hesse", "Bozkırdaki Çekirdek — Cengiz Aytmatov"], "video": ["TED — Verimli Tatil", "Yaz Stajı Rehberi"], "uygulama": ["LinkedIn Learning", "Coursera"]}},
}

# ── Uzman Görüşü (P10) ──
_BULTEN_UZMAN = {
    9: {
        "baslik": "Okula Uyum Kaygısını Anlamak ve Yönetmek",
        "uzman": "Uzm. Çocuk Psikoloğu",
        "icerik": (
            "Okul başlangıcı, çocuklar için heyecan kadar kaygı da barındıran bir dönemdir. "
            "Ayrılık kaygısı özellikle ilk kez okula başlayan veya okul değiştiren çocuklarda yoğun şekilde görülebilir. "
            "Bu durum çocuğun güvenli bağlanma ilişkisinin bir göstergesidir ve tamamen normaldir.\n\n"
            "Ebeveynlerin bu süreçte yapabileceği en değerli şey, kendi kaygılarını kontrol altında tutmaktır. "
            "Çocuklar ebeveynlerinin duygusal durumlarını ayna gibi yansıtır. Sakin, kararlı ve güler yüzlü "
            "bir vedalaşma ritüeli oluşturmak, çocuğun okula uyum sürecini büyük ölçüde kolaylaştırır.\n\n"
            "İlk haftaları zor geçen çocukların büyük çoğunluğu 2-3 hafta içinde uyum sağlar. "
            "Ancak kaygı belirtileri 4 haftadan uzun sürerse profesyonel destek almaktan çekinmeyin."
        ),
        "oneri": "Her sabah aynı kısa vedalaşma cümlesini kullanın; tutarlılık güven oluşturur.",
    },
    10: {
        "baslik": "Sosyal Beceri Gelişiminde Ailenin Rolü",
        "uzman": "Sosyal Beceri Gelişim Uzmanı",
        "icerik": (
            "Sosyal beceriler, çocukların hayat boyu kullanacakları en temel araçlardan biridir. "
            "Paylaşma, sıra bekleme, empati kurma ve çatışma çözme gibi beceriler doğuştan gelmez; "
            "öğrenilir ve pratikle gelişir.\n\n"
            "Ebeveynler günlük yaşamda model olarak en etkili öğretmenlerdir. Komşuyla selamlaşma, "
            "markette sıra bekleme, bir hata yapıldığında özür dileme — tüm bu anlar çocuk için birer derstir.\n\n"
            "Çocuğunuzun arkadaşlık kurma sürecine müdahale etmek yerine gözlemci olun. "
            "Sorun yaşadığında çözüm sunmak yerine 'Sen olsan ne yapardın?' diye sorarak "
            "problem çözme becerisini destekleyin."
        ),
        "oneri": "Haftada en az bir kez çocuğunuzun bir arkadaşını eve davet edin veya parkta buluşma ayarlayın.",
    },
    11: {
        "baslik": "Öz Düzenleme: Çocuğunuzun İç Kontrol Mekanizması",
        "uzman": "Eğitim Psikoloğu",
        "icerik": (
            "Öz düzenleme, bir çocuğun duygularını, düşüncelerini ve davranışlarını bilinçli şekilde "
            "yönetebilme kapasitesidir. Akademik başarının en güçlü yordayıcılarından biri olarak "
            "kabul edilen bu beceri, erken çocukluk döneminde temellendirilir.\n\n"
            "Öz düzenleme becerisi güçlü olan çocuklar ders çalışırken odaklanabilir, hayal kırıklığıyla "
            "baş edebilir ve uzun vadeli hedefler için kısa vadeli isteklerini erteleyebilir.\n\n"
            "Bu beceriyi geliştirmek için çocuğa seçim yapma fırsatları sunun, duygularını isimlendirmesine "
            "yardımcı olun ve rutinler oluşturarak öngörülebilir bir ortam sağlayın."
        ),
        "oneri": "Günlük 10 dakikalık 'sessiz zaman' rutini oluşturun; bu sürede çocuk kitap okuma, çizim yapma veya hayal kurma gibi sakin etkinlikler yapsın.",
    },
    12: {
        "baslik": "Empati: Başkalarının Gözünden Dünyayı Görmek",
        "uzman": "Empati Gelişim Uzmanı",
        "icerik": (
            "Empati, bir başkasının duygularını anlama ve paylaşma yeteneğidir. Araştırmalar, empati "
            "becerisinin çocuklukta aktif olarak geliştirilebileceğini ve bu becerinin zorbalığı önlemede, "
            "sağlıklı ilişkiler kurmada ve toplumsal uyumda kritik rol oynadığını göstermektedir.\n\n"
            "Çocuklara empati öğretmenin en etkili yolu, onların duygularına empatiyle yaklaşmaktır. "
            "'Üzgün olduğunu görüyorum, arkadaşınla yaşadığın durum seni kırmış olabilir' gibi cümleler "
            "çocuğa hem anlaşıldığını hissettirir hem de duygu tanıma modeli sunar.\n\n"
            "Hikâye okuma sırasında karakterlerin duygularını konuşmak, haberlerdeki olaylara birlikte "
            "bakmak ve farklı kültürleri tanımak empatinin güçlü besleyicileridir."
        ),
        "oneri": "Yemek masasında 'Bugün birinin yüzünü güldürdün mü?' sorusunu günlük ritüel haline getirin.",
    },
    1: {
        "baslik": "Motivasyon ve Hedef Belirleme Psikolojisi",
        "uzman": "Motivasyon ve Hedef Belirleme Uzmanı",
        "icerik": (
            "Yeni yıl, çocuklar için de yetişkinler için de hedef koymanın ve yeniden başlamanın "
            "sembolik bir zamanıdır. Araştırmalar, hedef belirlemenin başarıyı %25-40 oranında "
            "artırdığını göstermektedir — ancak hedefin doğru formüle edilmesi şarttır.\n\n"
            "Çocuklara hedef koymayı öğretirken AKILLI hedef tekniğini kullanın: hedef Açık, "
            "Küçük adımlara bölünmüş, Izlenebilir, Lâyık (ulaşılabilir) ve zamanlı olmalıdır. "
            "'Daha iyi not alacağım' yerine 'Her gün 20 dakika matematik çalışacağım' daha etkilidir.\n\n"
            "İçsel motivasyonu desteklemek için sonuç yerine sürece odaklanın. "
            "'Aferin, 100 aldın' yerine 'Çok düzenli çalıştın, emeğinin karşılığını aldın' deyin."
        ),
        "oneri": "Çocuğunuzla birlikte bu yarıyıl için 3 küçük, ölçülebilir hedef belirleyin ve buzdolabına asın.",
    },
    2: {
        "baslik": "Zorbalığı Önlemede Ailenin Gücü",
        "uzman": "Zorbalık Önleme Uzmanı",
        "icerik": (
            "Akran zorbalığı, çocukların en sık karşılaştığı ve en az konuştuğu sorunlardan biridir. "
            "Araştırmalar her 3 çocuktan 1'inin hayatının bir döneminde zorbalığa maruz kaldığını "
            "göstermektedir. Sevgi ve saygı ayı olan Şubat'ta bu konuyu ele almak anlamlıdır.\n\n"
            "Zorbalıkla karşılaşan çocuklar genellikle utanç ve suçluluk hisseder, bu nedenle "
            "durumu aileyle paylaşmakta zorlanır. Açık iletişim kanalları kurmak, çocuğun 'Ne olursa "
            "olsun sana inanırım ve yanındayım' mesajını hissetmesi hayati önem taşır.\n\n"
            "Zorbalık yapan çocuğun ailesi de desteğe ihtiyaç duyar. Cezalandırma yerine davranışın "
            "arkasındaki nedeni anlamaya çalışmak daha kalıcı çözümler üretir."
        ),
        "oneri": "Çocuğunuzla haftada bir 'güvenli konuşma zamanı' ayarlayın; bu sürede yargılamadan dinleyin.",
    },
    3: {
        "baslik": "Sağlıklı Özgüven İnşa Etmek",
        "uzman": "Özgüven ve Benlik Gelişim Uzmanı",
        "icerik": (
            "Özgüven, bir çocuğun kendini değerli, yeterli ve sevilmeye layık hissetmesidir. "
            "Sağlıklı özgüven ne aşırı övgüyle şişirilir ne de eleştiriyle ezilir; "
            "gerçekçi ve koşulsuz kabul üzerine inşa edilir.\n\n"
            "Çocuğun özgüvenini besleyen en önemli şey koşulsuz sevgidir: 'Seni başarıların için değil, "
            "sen olduğun için seviyorum.' Bu mesaj, çocuğun hata yapma ve risk alma cesaretini artırır.\n\n"
            "Özgüveni güçlendirmek için çocuğa yaşına uygun sorumluluklar verin, "
            "başarılarını süreç odaklı kutlayın ve başarısızlıklarında yanında olduğunuzu hissettirin. "
            "Karşılaştırma yapmaktan kesinlikle kaçının."
        ),
        "oneri": "Her gün yatmadan önce çocuğunuza o gün iyi yaptığı bir şeyi söyleyin.",
    },
    4: {
        "baslik": "Okuma Alışkanlığının Bilimsel Temelleri",
        "uzman": "Okuma Alışkanlığı Uzmanı",
        "icerik": (
            "Düzenli kitap okuyan çocukların kelime hazinesi, empati kapasitesi ve analitik düşünme "
            "becerileri akranlarına göre belirgin şekilde yüksektir. Nörolojik araştırmalar, "
            "okumanın beynin birden fazla bölgesini aynı anda aktive ettiğini ortaya koymaktadır.\n\n"
            "Okuma alışkanlığı oluşturmada en kritik faktör, çocuğun okumayı bir zorunluluk değil "
            "bir keyif olarak deneyimlemesidir. Bunun için çocuğun ilgi alanlarına uygun kitaplar "
            "sunmak ve okuma ortamını cazip hale getirmek gerekir.\n\n"
            "Ebeveynin okuyan bir model olması, çocuğa verilebilecek en güçlü mesajdır. "
            "Birlikte okuma zamanı ayırmak, okunanları konuşmak ve kütüphane ziyaretleri "
            "alışkanlığı pekiştirir."
        ),
        "oneri": "Evde herkesin 20 dakika sessizce okuduğu günlük bir 'aile okuma saati' başlatın.",
    },
    5: {
        "baslik": "Aile İçi İletişimin Altın Kuralları",
        "uzman": "Aile Terapisti",
        "icerik": (
            "Sağlıklı aile iletişimi, çocuğun duygusal gelişiminin temel taşıdır. "
            "Araştırmalar, ebeveynleriyle açık iletişim kurabilen çocukların özgüven düzeylerinin "
            "daha yüksek, kaygı düzeylerinin ise daha düşük olduğunu göstermektedir.\n\n"
            "Etkili iletişimin üç temel bileşeni vardır: aktif dinleme, ben dili kullanma ve "
            "duygu yansıtma. 'Neden böyle yaptın?' yerine 'Bu durumda ne hissettin?' sorusu "
            "çocuğu savunmaya değil, paylaşmaya yönlendirir.\n\n"
            "Dijital çağda aile iletişiminin en büyük düşmanı ekranlardır. Yemek saatlerinde "
            "ve yatmadan önceki 30 dakikada ekransız zaman oluşturmak, kaliteli "
            "iletişim için alan açar."
        ),
        "oneri": "Her akşam yemeğinde herkesin günün en güzel anını paylaştığı bir 'sofra turu' yapın.",
    },
    6: {
        "baslik": "Yaz Tatilini Verimli ve Güvenli Planlamak",
        "uzman": "Çocuk Gelişim Uzmanı",
        "icerik": (
            "Yaz tatili, çocuklar için dinlenme ve yenilenme kadar öğrenmenin de devam ettiği "
            "bir dönem olmalıdır. Araştırmalar, yapılandırılmış bir yaz planı olmayan çocukların "
            "akademik becerilerinde %20'ye varan kayıp yaşayabildiğini göstermektedir.\n\n"
            "İdeal yaz planı üçlü denge üzerine kurulmalıdır: dinlenme-eğlence, öğrenme-gelişim "
            "ve sosyal-fiziksel aktivite. Her gün en az 30 dakika okuma, 1 saat fiziksel aktivite "
            "ve yaratıcı etkinlik zamanı ayrılması önerilir.\n\n"
            "Çocuğun tatil planlamasına katılması, sorumluluk ve öz yönetim becerilerini "
            "geliştirmek için mükemmel bir fırsattır. Birlikte bir yaz takvimi oluşturun."
        ),
        "oneri": "Çocuğunuzla birlikte bir 'yaz keşif listesi' hazırlayın: 10 kitap, 5 yeni beceri, 3 gezi hedefi.",
    },
}

# ── Sosyal-Duygusal Öğrenme Beceri Kartı (P11) ──
_BULTEN_SEL = {
    9: {
        "beceri": "Uyum / Adaptasyon",
        "tanim": "Yeni ortamlara, insanlara ve durumlara esnek bir şekilde ayak uydurabilme becerisidir.",
        "neden": "Okula uyum süreci, çocuğun yaşam boyu karşılaşacağı değişimlere hazırlık niteliğindedir.",
        "adimlar": [
            "Yeni ortamı tanımak için gözlem yap, acele etme.",
            "Tanıdık bir şey bul — benzer kurallar, tanıdık yüzler.",
            "Küçük adımlarla katılım göster, her şeyi birden yapmak zorunda değilsin.",
            "Zorlandığında güvendiğin bir yetişkine hissettiklerini anlat.",
        ],
        "senaryo": "Yeni bir sınıfa geldin ve kimseyi tanımıyorsun. Teneffüste ne yapardın?",
    },
    10: {
        "beceri": "Empati Kurma",
        "tanim": "Başka birinin duygularını anlama ve o kişinin yerine kendini koyabilme becerisidir.",
        "neden": "Empati, sağlıklı arkadaşlıkların ve toplumsal uyumun temel yapı taşıdır.",
        "adimlar": [
            "Karşındaki kişinin yüz ifadesine ve beden diline dikkat et.",
            "Kendine sor: 'Ben onun yerinde olsam ne hissederdim?'",
            "Duygusunu yansıt: 'Üzgün görünüyorsun, bir şey mi oldu?'",
            "Yardım teklif et, ama kabul etmezse saygı göster.",
        ],
        "senaryo": "Arkadaşın bugün çok sessiz ve kimseyle konuşmuyor. Ne yaparsın?",
    },
    11: {
        "beceri": "Öz Düzenleme",
        "tanim": "Duygularını, düşüncelerini ve davranışlarını duruma uygun şekilde yönetebilme becerisidir.",
        "neden": "Öz düzenleme, akademik başarı ve sosyal uyumun en güçlü belirleyicilerinden biridir.",
        "adimlar": [
            "Durumu fark et: 'Şu an ne hissediyorum?' diye sor.",
            "Dur ve nefes al — 3 derin nefes, burnundan al ağzından ver.",
            "Seçeneklerini düşün: 'Ne yapabilirim?' (en az 2 seçenek bul).",
            "En uygun davranışı seç ve uygula, sonra sonucu değerlendir.",
        ],
        "senaryo": "Çok istediğin bir oyuncağı alamadığında kendini çok kızgın hissediyorsun. Adımları uygula.",
    },
    12: {
        "beceri": "Yardımseverlik",
        "tanim": "Başkalarının ihtiyaçlarını fark edip karşılık beklemeden destek olabilme becerisidir.",
        "neden": "Yardımseverlik hem yardım edene hem alana mutluluk verir ve toplumsal dayanışmayı güçlendirir.",
        "adimlar": [
            "Çevrene dikkatli bak: Kimin yardıma ihtiyacı olabilir?",
            "Küçük adımlarla başla: kapıyı tutmak, çantasını taşımak.",
            "Yardımı teklif et, dayatma: 'Yardım edebilir miyim?' de.",
            "Teşekkür bekleme; yardım etmenin verdiği iyi hissi fark et.",
        ],
        "senaryo": "Kantinde yeni bir öğrenci masasını bulamıyor ve kaybolmuş görünüyor. Ne yaparsın?",
    },
    1: {
        "beceri": "Hedef Odaklılık",
        "tanim": "Belirlenen bir amaca ulaşmak için plan yapabilme ve o plana bağlı kalabilme becerisidir.",
        "neden": "Hedef odaklı çocuklar, zorluklarla karşılaştığında daha dirençli ve azimli olur.",
        "adimlar": [
            "Net bir hedef belirle: Ne istiyorum? Ne zaman ulaşacağım?",
            "Hedefe giden yolu küçük adımlara böl.",
            "Her gün en az bir adım at, küçük de olsa.",
            "İlerlemeyi takip et ve her küçük başarıyı kutla.",
        ],
        "senaryo": "Bu dönem matematik notunu yükseltmek istiyorsun ama nereden başlayacağını bilmiyorsun. Adımları uygula.",
    },
    2: {
        "beceri": "Öz Değer",
        "tanim": "Kendini olduğu gibi kabul edebilme ve değerli hissedebilme becerisidir.",
        "neden": "Sağlıklı öz değer duygusuna sahip çocuklar akran baskısına karşı daha dayanıklıdır.",
        "adimlar": [
            "Her gün kendinde beğendiğin bir özelliği hatırla.",
            "Kendini başkalarıyla kıyaslamak yerine dünkü halinle kıyasla.",
            "Hata yapmak insani bir durum; hatalarından ders çıkar.",
            "Seni seven ve destekleyen kişilerin sesine kulak ver.",
        ],
        "senaryo": "Sınıfta bir yarışmada sonuncu oldun ve çok üzgünsün. Kendinle nasıl konuşursun?",
    },
    3: {
        "beceri": "Cesaretli Olmak",
        "tanim": "Korkuya rağmen doğru bildiğini yapabilme ve risk alabilme becerisidir.",
        "neden": "Cesaret, yeni şeyler denemek, haksızlığa karşı durmak ve büyümek için gereklidir.",
        "adimlar": [
            "Korkunu kabul et — cesaret korkunun olmaması değil, korkuya rağmen harekete geçmektir.",
            "Küçük cesaret adımlarıyla başla: parmak kaldır, fikrini söyle.",
            "Cesaretli davrandığın anları hatırla, başarabildiğini bil.",
            "Kendine cesaretlendirici bir cümle söyle: 'Bunu yapabilirim!'",
        ],
        "senaryo": "Bir arkadaşına haksızlık yapıldığını görüyorsun ama müdahale etmekten çekiniyorsun. Ne yaparsın?",
    },
    4: {
        "beceri": "Eleştirel Düşünme",
        "tanim": "Bilgiyi sorgulayarak, farklı açılardan değerlendirerek doğru kararlar verebilme becerisidir.",
        "neden": "Eleştirel düşünme, bilgi çağında gerçeği yalandan ayırmanın en güçlü aracıdır.",
        "adimlar": [
            "Her duyduğun bilgiyi hemen kabul etme; 'Kaynağı ne?' diye sor.",
            "Farklı görüşleri dinle, tek taraflı düşünme.",
            "Kanıt ara: Bu bilgiyi destekleyen başka veriler var mı?",
            "Kendi fikrini oluştur ve gerekçelendir.",
        ],
        "senaryo": "İnternette okuduğun bir habere herkes inanıyor ama sana garip geldi. Ne yaparsın?",
    },
    5: {
        "beceri": "Etkili İletişim",
        "tanim": "Duygu ve düşüncelerini açık, saygılı ve anlaşılır biçimde ifade edebilme becerisidir.",
        "neden": "İletişim becerileri güçlü olan çocuklar ilişkilerinde daha mutlu ve başarılıdır.",
        "adimlar": [
            "Konuşmadan önce düşün: Ne söylemek istiyorum?",
            "'Ben dili' kullan: 'Sen hep...' yerine 'Ben ... hissediyorum' de.",
            "Karşındakini dinle — sözünü kesme, göz teması kur.",
            "Beden dilini kontrol et: ses tonu, yüz ifadesi, duruş.",
        ],
        "senaryo": "Annen seni yanlış anladı ve haksız yere kızdı. Ona duygularını nasıl anlatırsın?",
    },
    6: {
        "beceri": "Minnettarlık",
        "tanim": "Sahip olduğu güzel şeylerin farkında olma ve bunlar için şükran duyabilme becerisidir.",
        "neden": "Minnettarlık duyan çocuklar daha mutlu, daha iyimser ve daha dayanıklıdır.",
        "adimlar": [
            "Her gün minnettar olduğun 3 şeyi say — küçük şeyler de olabilir.",
            "Sana iyilik yapan kişilere teşekkür et, bunu alışkanlık haline getir.",
            "Bir minnettarlık günlüğü tut; yatmadan önce yaz.",
            "Başkalarına iyilik yaparak minnettarlığı yay.",
        ],
        "senaryo": "Bir yılı geride bırakıyorsun. Bu yıl seni mutlu eden 5 şeyi yaz ve bir kişiye teşekkür mektubu hazırla.",
    },
}

# ── Aktivite & Oyun Sayfası (P12) ──
_BULTEN_AKTIVITE = {
    9: {
        "baslik": "Tanışma Ağı Oyunu",
        "tur": "oyun",
        "malzemeler": ["Yün yumağı"],
        "adimlar": [
            "Çocuklar daire şeklinde otursun.",
            "Yün yumağını tutan çocuk adını ve en sevdiği şeyi söylesin.",
            "İpi ucundan tutarak yumağı başka birine atsın.",
            "Herkes katılana kadar devam edin — ortaya bir ağ oluşacak.",
            "Ağı birlikte kaldırın: 'Bu bizim arkadaşlık ağımız!' deyin.",
        ],
        "kazanim": "Sosyal bağ kurma, isim öğrenme ve aidiyet hissi geliştirme.",
    },
    10: {
        "baslik": "Duygu Maskeleri Atölyesi",
        "tur": "sanat",
        "malzemeler": ["Karton tabaklar", "Boya kalemleri", "Makas", "Çubuk veya lastik"],
        "adimlar": [
            "Her çocuğa bir karton tabak dağıtın.",
            "Tabağın bir yüzüne mutluluk, diğer yüzüne üzüntü maskesi çizsinler.",
            "Sırayla maskelerini gösterip o duyguyu yaşadıkları bir anı anlatsınlar.",
            "Hangi duygunun daha zor olduğunu konuşun.",
        ],
        "kazanim": "Duygu tanıma, duygu ifadesi ve empati becerilerini geliştirme.",
    },
    11: {
        "baslik": "Sorumluluk Takvimi Yapımı",
        "tur": "yazma",
        "malzemeler": ["A3 kâğıt", "Renkli kalemler", "Yıldız çıkartmaları"],
        "adimlar": [
            "Kâğıdı haftalık takvim şeklinde bölün (7 sütun).",
            "Çocuğun günlük sorumluluk listesi oluşturmasına yardım edin (oda toplama, çanta hazırlama vb.).",
            "Her tamamlanan görev için yıldız çıkartma yapıştırsın.",
            "Hafta sonunda yıldızları sayın ve başarıyı birlikte kutlayın.",
        ],
        "kazanim": "Öz düzenleme, sorumluluk bilinci ve planlama becerisi geliştirme.",
    },
    12: {
        "baslik": "İyilik Zinciri Etkinliği",
        "tur": "drama",
        "malzemeler": ["Renkli kâğıt şeritleri", "Yapıştırıcı"],
        "adimlar": [
            "Her çocuk bir kâğıt şeridine bu hafta yapacağı bir iyilik yazsın.",
            "Şeritleri birbirine bağlayarak bir zincir oluşturun.",
            "Zinciri sınıfa asın.",
            "Hafta boyunca iyilik yaptıkça yeni halkalar ekleyin.",
            "Ay sonunda zincirin uzunluğunu ölçün ve kutlayın.",
        ],
        "kazanim": "Yardımseverlik, empati ve toplumsal sorumluluk bilinci geliştirme.",
    },
    1: {
        "baslik": "Hedef Roketi Yapımı",
        "tur": "sanat",
        "malzemeler": ["Tuvalet kâğıdı rulosu", "Renkli kâğıtlar", "Yapıştırıcı", "Keçeli kalemler"],
        "adimlar": [
            "Ruloyu rokete dönüştürmek için renkli kâğıtlarla kaplayın.",
            "Raketin gövdesine bu dönemin 3 hedefini yazın.",
            "Kanatlarına hedeflere ulaşmak için atacağı adımları not edin.",
            "Roketi odaya veya sınıfa koyun; hedef tamamlandıkça yıldız ekleyin.",
        ],
        "kazanim": "Hedef belirleme, planlama ve motivasyon becerisi geliştirme.",
    },
    2: {
        "baslik": "Sevgi Kutusu",
        "tur": "yazma",
        "malzemeler": ["Küçük kutu veya zarf", "Renkli kâğıtlar", "Kalem"],
        "adimlar": [
            "Herkes için bir kutu veya zarf hazırlayın ve üzerine isim yazın.",
            "Her çocuk, diğer arkadaşları için güzel bir özelliğini yazsın.",
            "Kâğıtları ilgili kutulara atın.",
            "Herkes kendi kutusunu açsın ve gelen mesajları okusun.",
        ],
        "kazanim": "Öz değer hissi, olumlu geri bildirim verme ve alma becerisi.",
    },
    3: {
        "baslik": "Ben Özelim Kolajı",
        "tur": "sanat",
        "malzemeler": ["Dergi veya gazete", "Makas", "Yapıştırıcı", "A3 kâğıt"],
        "adimlar": [
            "Dergilerden kendilerini temsil eden resimler ve kelimeler kessinler.",
            "A3 kâğıdın ortasına fotoğraflarını veya isimlerini yapıştırsınlar.",
            "Etrafına kestikleri görselleri ve güçlü yönlerini yazarak kolaj oluştursunlar.",
            "Kolajlarını sınıfa sunarak kendilerini tanıtsınlar.",
        ],
        "kazanim": "Özgüven, kendini tanıma ve olumlu benlik algısı geliştirme.",
    },
    4: {
        "baslik": "Kitap Karakteri Canlandırma",
        "tur": "drama",
        "malzemeler": [],
        "adimlar": [
            "Her çocuk en sevdiği kitaptan bir karakter seçsin.",
            "Karakterin kostümünü basit malzemelerle hazırlasın.",
            "Sınıf önünde karakteri canlandırarak kitabı tanıtsın.",
            "Diğer çocuklar karaktere sorular sorsun.",
            "En yaratıcı canlandırmayı birlikte seçin.",
        ],
        "kazanim": "Okuma motivasyonu, yaratıcılık ve sunum becerisi geliştirme.",
    },
    5: {
        "baslik": "Aile Ağacı ve Hikâyemiz",
        "tur": "sanat",
        "malzemeler": ["A3 kâğıt", "Renkli kalemler", "Fotoğraflar (isteğe bağlı)"],
        "adimlar": [
            "Kâğıda büyük bir ağaç çizin.",
            "Dallarına aile bireylerinin isimlerini ve özelliklerini yazın.",
            "Yapraklara aileyle yaşanan güzel anıları ekleyin.",
            "Ağacın köküne 'Bizi bir arada tutan değerler' yazın ve doldurun.",
        ],
        "kazanim": "Aile bağları, aidiyet hissi ve iletişim becerisi geliştirme.",
    },
    6: {
        "baslik": "Yaz Hazine Haritası",
        "tur": "oyun",
        "malzemeler": ["Büyük kâğıt", "Renkli kalemler"],
        "adimlar": [
            "Kâğıda yaz tatili haritası çizin: ev, park, kütüphane, doğa vb.",
            "Her noktaya bir yaz görevi yazın (kitap oku, yüzme öğren, yeni yemek yap).",
            "Görevleri tamamladıkça harita üzerinde işaretlesin.",
            "Tüm görevleri tamamlayınca hazineye ulaşsın: aile ödülü.",
        ],
        "kazanim": "Planlama, hedef odaklılık ve yaz verimlilik becerisi geliştirme.",
    },
}

# ── Dünyadan İyi Uygulamalar (P13) ──
_BULTEN_DUNYA = {
    9: [
        ("🇫🇮 Finlandiya", "Okula uyum için ilk iki hafta ders işlenmez; çocuklar oyun ve sosyal etkinliklerle tanışır."),
        ("🇯🇵 Japonya", "Öğrenciler okulu kendileri temizler; bu uygulama sorumluluk ve aidiyet duygusu geliştirir."),
        ("🇩🇰 Danimarka", "Haftada bir 'Klassens Tid' (Sınıf Saati) yapılır; çocuklar duygularını ve sorunlarını paylaşır."),
    ],
    10: [
        ("🇳🇿 Yeni Zelanda", "Okullarda 'Buddy System' uygulanır; büyük öğrenciler küçüklere rehberlik eder."),
        ("🇸🇪 İsveç", "Okul öncesinde çocuklar doğada oynayarak sosyal becerilerini doğal yollarla geliştirir."),
        ("🇨🇦 Kanada", "Okullarda 'Roots of Empathy' programıyla bebekler sınıfa gelir, çocuklar empati öğrenir."),
    ],
    11: [
        ("🇸🇬 Singapur", "Öğrencilere 'Sorumluluk Pasaportu' verilir; tamamladıkları görevler damgalanır."),
        ("🇩🇪 Almanya", "İlkokullarda 'Waldorf' yaklaşımıyla çocuklar kendi tempolarında, öz düzenlemeli öğrenir."),
        ("🇰🇷 Güney Kore", "Okullarda 'Mindfulness' (Bilinçli Farkındalık) dersleri müfredata dahil edilmiştir."),
    ],
    12: [
        ("🇳🇱 Hollanda", "Okullar 'Sinterklaas' döneminde toplumsal yardım projeleri düzenler; çocuklar ihtiyaç sahiplerine hediye hazırlar."),
        ("🇬🇧 İngiltere", "Christmas Jumper Day ile çocuklar eğlenceli kazaklar giyerek yardım kuruluşlarına bağış toplar."),
        ("🇧🇷 Brezilya", "Okullarda 'Solidariedade' (Dayanışma) haftası düzenlenir; paylaşma ve yardımlaşma öne çıkar."),
    ],
    1: [
        ("🇺🇸 ABD", "Okullar yeni yılda 'Vision Board' (Hedef Panosu) etkinliği yapar; öğrenciler hayallerini görselleştirir."),
        ("🇫🇮 Finlandiya", "Öğrenciler kendi öğrenme hedeflerini belirler ve öğretmenle birlikte değerlendirir."),
        ("🇯🇵 Japonya", "Yeni yılda 'Kakizome' geleneğiyle çocuklar yıllık hedeflerini kaligrafiyle yazar."),
    ],
    2: [
        ("🇫🇮 Finlandiya", "KiVa programı ile zorbalık okulda sistematik şekilde önlenir; tüm öğrenciler eğitim alır."),
        ("🇦🇺 Avustralya", "Ulusal Zorbalık Karşıtı Hafta'da okullar farkındalık etkinlikleri düzenler."),
        ("🇳🇴 Norveç", "Olweus programı ile her sınıfta haftalık zorbalık önleme toplantıları yapılır."),
    ],
    3: [
        ("🇮🇹 İtalya", "Reggio Emilia yaklaşımında her çocuk biricik kabul edilir ve 100 dilde ifade etmesi desteklenir."),
        ("🇳🇿 Yeni Zelanda", "Maori kültüründen 'Mana' kavramı ile her bireyin doğuştan değerli olduğu öğretilir."),
        ("🇨🇦 Kanada", "Okullarda 'Strengths-Based Education' ile güçlü yönlere odaklanılır, zayıflıklara değil."),
    ],
    4: [
        ("🇮🇸 İzlanda", "Nüfusun %93'ü düzenli okur; okullar Jolabokaflod geleneğiyle kitap kültürünü yaşatır."),
        ("🇪🇪 Estonya", "Dijital kütüphaneler sayesinde her çocuk evinden binlerce kitaba ücretsiz erişir."),
        ("🇨🇺 Küba", "Okuma kampanyaları ile ülke genelinde okuma-yazma oranı %99'un üzerindedir."),
    ],
    5: [
        ("🇩🇰 Danimarka", "Hygge kültürü ile aileler günlük hayatta kaliteli birlikte zaman geçirmeye önem verir."),
        ("🇨🇴 Kolombiya", "Biblioburro projesiyle çocuklara eşeklerle köylere kitap taşınır; aileler birlikte okur."),
        ("🇯🇵 Japonya", "Aileler çocuklarıyla birlikte 'Ohanami' (çiçek seyretme) yaparak doğayla bağ kurar."),
    ],
    6: [
        ("🇸🇪 İsveç", "Yaz kamplarında çocuklar doğada hayatta kalma becerileri ve takım çalışması öğrenir."),
        ("🇺🇸 ABD", "Yaz okuma programları ile kütüphaneler çocuklara ödüllü okuma yarışmaları düzenler."),
        ("🇦🇺 Avustralya", "Tatilde 'Bush School' programıyla çocuklar açık havada öğrenmeye devam eder."),
    ],
}

# ── Bulmaca & Eğlence (P14) ──
_BULTEN_BULMACA = {
    9: {
        "bilmece": [
            ("Her sabah giderim, öğleden sonra dönerim. İçinde öğretmen, arkadaş, bilgi var. Ben neyim?", "Okul"),
            ("Sırtında taşırsın, içinde kitaplar, defterler var. Ben neyim?", "Çanta"),
            ("İlk günü heyecan, son günü hüzün. Ben neyim?", "Okul yılı"),
        ],
        "kelime": "Şu harfleri kullanarak 'okul' ile ilgili 5 kelime bul: O-K-U-L-A-R-K-A-D-A-Ş (Örnek: okul, arkadaş...)",
        "eglence": "Biliyor muydun? Dünyanın en eski okulu İtalya'daki Bologna Üniversitesi'dir ve 1088 yılında kurulmuştur!",
    },
    10: {
        "bilmece": [
            ("İki kişi arasında kurulur, görünmez ama hissedilir. Ben neyim?", "Arkadaşlık"),
            ("Paylaştıkça çoğalır, sakladıkça azalır. Ben neyim?", "Mutluluk"),
            ("El ele tutuşuruz, birlikte güleriz. Zor günde yanındayım. Ben neyim?", "Dost"),
        ],
        "kelime": "Bu duygu kelimelerinin harflerini karıştırdık. Çöz: LTMUUKUL (mutluluk), GİZÜNÜT (üzüntü), GNÇIŞA (şaşkın)",
        "eglence": "Biliyor muydun? Gülmek bulaşıcıdır! Bir kişi güldüğünde yanındakilerin gülme olasılığı %30 artar.",
    },
    11: {
        "bilmece": [
            ("Yapılacakları listeler, zamanı yönetir. Düzenli olanın en iyi dostudur. Ben neyim?", "Planlama"),
            ("Sabah erken kalkar, işini zamanında yapar. Herkesin güvendiği kişidir. Ben kimim?", "Sorumlu kişi"),
            ("Ne kadar kullanırsan o kadar güçlenir, kullanmazsan kaybolur. Ben neyim?", "İrade"),
        ],
        "kelime": "Sorumluluk kelimesinden en az 8 yeni kelime türet. (Örnek: rum, luk, sol, ...)",
        "eglence": "Biliyor muydun? İnsan beyni bir alışkanlığı otomatik hale getirmek için ortalama 66 gün tekrar ister!",
    },
    12: {
        "bilmece": [
            ("Verirsen çoğalır, tutarsan azalır. Kalpleri ısıtır. Ben neyim?", "Sevgi"),
            ("Gözle görünmez, elle tutulmaz ama hayatı güzelleştirir. Ben neyim?", "İyilik"),
            ("Başkasının yerine kendini koyarsın, onun gözünden bakarsın. Ben neyim?", "Empati"),
        ],
        "kelime": "Yardımseverlik labirentinde yolu bul: BAŞLA → paylaş → gülümse → yardım et → dinle → BİTİŞ. Her adımda o kelimeyle bir cümle kur.",
        "eglence": "Biliyor muydun? İyilik yapmak beyinde 'mutluluk hormonu' serotonin salgılatır — buna 'yardımcı coşkusu' denir!",
    },
    1: {
        "bilmece": [
            ("Yılın ilk günü doğar, 365 gün yaşar. Ben neyim?", "Yeni yıl"),
            ("Onu koyarsın, peşinden koşarsın. Ulaşınca mutlu olursun. Ben neyim?", "Hedef"),
            ("Başlamak için cesaret, devam etmek için sabır ister. Ben neyim?", "Azim"),
        ],
        "kelime": "MOTİVASYON kelimesindeki harflerle en az 10 kelime yaz. (Örnek: ton, yas, not...)",
        "eglence": "Biliyor muydun? Dünyada en çok yeni yıl kararı alan ülke ABD'dir ama kararların %80'i Şubat ayına kadar bırakılır!",
    },
    2: {
        "bilmece": [
            ("Rengi kırmızı, şekli kalp. Her yerde görürsün bu ayda. Ben neyim?", "Sevgi sembolü"),
            ("Saygı duyarsan sana da saygı duyulur. Verdiğin kadar alırsın. Ben neyim?", "Saygı"),
            ("Anneni, babını, arkadaşını — hepsini birleştiren güç. Ben neyim?", "Sevgi"),
        ],
        "kelime": "Kalp şeklinin içine SEVGİ ile ilgili akla gelen tüm kelimeleri yaz. Kaç kelime buldun?",
        "eglence": "Biliyor muydun? Sarılma sırasında vücut oksitosin hormonu salgılar. Günde 8 kez sarılmak duygusal sağlık için idealdir!",
    },
    3: {
        "bilmece": [
            ("Herkesin kendine ait bir tane var, hiçbiri aynı değil. Ben neyim?", "Parmak izi"),
            ("İçinden geleni yaparsın, 'yapabilirim' dersin. Ben neyim?", "Özgüven"),
            ("Aynaya baktığında görürsün, dünyada bir tanesi var. Ben kimim?", "Ben / Kendim"),
        ],
        "kelime": "ÖZGÜVEN kelimesini aşağıdan yukarıya yaz ve her harfle başlayan olumlu bir sıfat bul. (Ö: Özverili, Z: Zeki...)",
        "eglence": "Biliyor muydun? Dünyada 8 milyar insan var ve hiçbirinin parmak izi aynı değil — sen gerçekten benzersizsin!",
    },
    4: {
        "bilmece": [
            ("Sayfaları açarsın, dünyalar keşfedersin. Ben neyim?", "Kitap"),
            ("Yazarı var, karakterleri var, sonu merak edilir. Ben neyim?", "Roman"),
            ("Kelimelere hayat verir, seni başka dünyalara götürür. Ben neyim?", "Hayal gücü"),
        ],
        "kelime": "Kitap isimlerinden bilmece: 'K_Ç_K P_E_S' (Küçük Prens), '_İ_Y_C_' (Simyacı), 'P_N_K_O' (Pinokyo)",
        "eglence": "Biliyor muydun? Dünyanın en çok kitap okuyan ülkesi Hindistan'dır; haftada ortalama 10 saat okurlar!",
    },
    5: {
        "bilmece": [
            ("Evinin sıcaklığı, kalbin huzuru. Dünyanın en güzel yeri. Ben neyim?", "Yuva / Aile"),
            ("Koşulsuz sever, her zaman yanındadır. Ben kimim?", "Anne / Baba"),
            ("Küçükken kavga edersin, büyüyünce en yakın dostun olur. Ben kimim?", "Kardeş"),
        ],
        "kelime": "AİLE kelimesinden çıkan harflerle kelime türetme yarışı yap. En çok kelimeyi kim bulacak?",
        "eglence": "Biliyor muydun? Birlikte yemek yiyen ailelerin çocukları akademik olarak daha başarılı oluyor!",
    },
    6: {
        "bilmece": [
            ("Okullar kapanır, güneş açar. Deniz, kum, oyun zamanı. Ben neyim?", "Yaz tatili"),
            ("Güneş altında yüzersin, kumda kaleler yaparsın. Ben neredeyim?", "Plaj / Sahil"),
            ("9 ay çalıştın, şimdi dinlenme zamanı. Ama öğrenmeyi unutma! Ben neyim?", "Tatil"),
        ],
        "kelime": "YAZ TATİLİ bulmacası: Yaz aylarında yapılabilecek etkinlikleri A'dan Z'ye sırala. (A: Ağaçlara tırmanma, B: Bisiklet sürme...)",
        "eglence": "Biliyor muydun? Güneş ışığı D vitamini üretir ve bu vitamin mutluluk hormonlarını artırır. Günde 15 dakika güneşlen!",
    },
}

# ── Ayın Rol Modeli (P15) ──
_BULTEN_ROLMODEL = {
    9: {
        "isim": "Mustafa Kemal Atatürk",
        "alan": "Devlet Adamı / Eğitim Önderi",
        "hikaye": "Atatürk, eğitimin bir milletin geleceğini şekillendiren en güçlü araç olduğuna inanmıştır. "
                  "Cumhuriyet'in ilanından sonra eğitimde devrim niteliğinde değişiklikler yaparak "
                  "milyonlarca insanın okuma yazma öğrenmesini sağlamıştır.",
        "soz": "Bir millet, irfan ordusuna sahip olmadıkça, savaş meydanlarında ne kadar parlak zaferler elde ederse etsin, o zaferlerin kalıcı sonuçlar vermesi ancak irfan ordusuyla mümkündür.",
        "ders": "Eğitim, tüm başarıların ve değişimlerin temelidir. Öğrenmeye her yaşta devam etmek en büyük güçtür.",
    },
    10: {
        "isim": "Aziz Sancar",
        "alan": "Bilim İnsanı (Nobel Ödüllü)",
        "hikaye": "Mardin Savur'da mütevazı bir ailede büyüyen Aziz Sancar, azim ve çalışkanlığıyla "
                  "dünyanın en prestijli bilim ödülü olan Nobel'i kazanmıştır. "
                  "Başarısını her zaman arkadaşlarına, hocalarına ve ekip çalışmasına bağlamıştır.",
        "soz": "Başarının sırrı çok çalışmaktır. Yeteneğe güvenip tembellik edenler asla büyük işler başaramaz.",
        "ders": "Nereden geldiğin değil, ne kadar çalıştığın belirler. İyi arkadaşlar ve mentorlar yolculuğu kolaylaştırır.",
    },
    11: {
        "isim": "Marie Curie",
        "alan": "Bilim İnsanı (Fizik & Kimya)",
        "hikaye": "Tarihin ilk kadın Nobel ödüllü bilim insanı olan Marie Curie, iki farklı alanda Nobel kazanmıştır. "
                  "Kadınların üniversiteye gidemediği bir dönemde gizlice eğitim almış ve "
                  "kararlılığıyla bilim tarihini değiştirmiştir.",
        "soz": "Hayatta korkacak bir şey yok, sadece anlaşılacak şeyler var. Şimdi daha fazlasını anlama zamanı.",
        "ders": "Engeller, pes etmek için değil aşmak için vardır. Disiplin ve merak her kapıyı açar.",
    },
    12: {
        "isim": "Barış Manço",
        "alan": "Müzisyen / Kültür Elçisi",
        "hikaye": "Barış Manço, müziğiyle Türk kültürünü dünyaya tanıtmış, '7'den 77'ye' programıyla "
                  "çocukların kalbinde taht kurmuştur. Farklı ülkeleri gezerek kültürler arası "
                  "empati ve anlayış köprüleri inşa etmiştir.",
        "soz": "Çocuklar geleceğimizdir. Onlara sevgiyle yaklaşmak, onların dünyasına girmek en büyük görevimizdir.",
        "ders": "Farklılıkları anlamak ve saygı göstermek, dünyayı daha güzel bir yer yapar.",
    },
    1: {
        "isim": "Elon Musk",
        "alan": "Girişimci / Mühendis",
        "hikaye": "Güney Afrika'da zorbalığa maruz kalan bir çocukluktan, dünyayı değiştiren projelere uzanan "
                  "bir yolculuk. SpaceX ile uzaya, Tesla ile temiz enerjiye yönelen Musk, "
                  "büyük hedeflerin küçük adımlarla başladığını kanıtlamıştır.",
        "soz": "Bir şey yeterince önemliyse, başarı şansın düşük olsa bile yapmalısın.",
        "ders": "Büyük hedefler koymaktan korkma. Başarısızlık sürecin bir parçasıdır, öğrenmeye devam et.",
    },
    2: {
        "isim": "Mahatma Gandhi",
        "alan": "Barış Lideri",
        "hikaye": "Gandhi, şiddete başvurmadan Hindistan'ın bağımsızlığını kazanmış, sevgi ve saygının "
                  "dünyanın en güçlü silahı olduğunu kanıtlamıştır. 'Dünyada görmek istediğin "
                  "değişim sen ol' felsefesiyle milyonlara ilham vermiştir.",
        "soz": "Göz göze bırakırsak, tüm dünya kör olur.",
        "ders": "Sevgi ve saygı, şiddetten daha güçlüdür. Değişim kendimizden başlar.",
    },
    3: {
        "isim": "Frida Kahlo",
        "alan": "Ressam / Sanatçı",
        "hikaye": "Küçük yaşta ağır bir kaza geçiren Frida Kahlo, yatağa mahkûm olduğu dönemde "
                  "resim yapmaya başlamış ve acısını sanata dönüştürmüştür. Farklılıklarını "
                  "gizlemek yerine sanatının merkezine koyarak dünyaca ünlü bir sanatçı olmuştur.",
        "soz": "Kanatlarım varsa neden yürüyeyim ki?",
        "ders": "Farklılıkların seni zayıflatmaz, benzersiz yapar. Kendini olduğun gibi kabul et ve güçlü yönlerini keşfet.",
    },
    4: {
        "isim": "Elif Şafak",
        "alan": "Yazar",
        "hikaye": "Elif Şafak, çocukluğunda kitaplarla kurduğu bağı dünyaca ünlü bir yazarlık kariyerine "
                  "dönüştürmüştür. 19 dile çevrilen kitaplarıyla farklı kültürleri bir araya getiren "
                  "Şafak, okumanın empatiyi geliştirdiğine inanır.",
        "soz": "Bir hikâye okurken başka birinin gözünden dünyaya bakarsın. Bu dünyanın en güçlü empati aracıdır.",
        "ders": "Kitaplar dünyayı tanımamızın en güzel yoludur. Okumak, farklı hayatları ve bakış açılarını anlamaktır.",
    },
    5: {
        "isim": "Anne Frank",
        "alan": "Yazar / İnsan Hakları Sembolü",
        "hikaye": "İkinci Dünya Savaşı sırasında ailesiylen saklanmak zorunda kalan Anne Frank, "
                  "günlüğüne yazdıklarıyla milyonlara dokunmuştur. En zor koşullarda bile umudunu "
                  "ve ailesine olan sevgisini kaybetmemiştir.",
        "soz": "Her fırtınanın ardından güneşin tekrar açacağına inanıyorum.",
        "ders": "Aile bağları en zor zamanlarda bile güç verir. Sevdiklerimize olan bağlılığımız en büyük zenginliğimizdir.",
    },
    6: {
        "isim": "Hasan Kalyoncu",
        "alan": "Pilot / Kaşif",
        "hikaye": "Türk pilot ve kaşif Hasan Kalyoncu, ultralight uçakla dünya turu yapan ilk Türk olmuştur. "
                  "Hayallerinin peşinden giderek sınırları zorlamış, farklı kültürler ve coğrafyalar keşfetmiştir.",
        "soz": "Hayal kurmak yetmez, o hayali yaşamak için harekete geçmek gerek.",
        "ders": "Yaz tatili yeni şeyler keşfetmek için harika bir fırsat. Hayallerinin peşinden git, dünyayı keşfet.",
    },
}

# ── Günlük / Yansıtma Sayfası (P16) ──
_BULTEN_GUNLUK = {
    9: {
        "aciklama": "Eylul ayi yeni baslangiclarin, heyecanin ve bazen de kayginin bir arada yasandigi bir donemdir. Gunluk yazma bu duygulari anlamlandirmak ve uyum surecini kolaylastirmak icin guclu bir aractir. Hislerini kagida dokmek onlari daha iyi tanimanin ilk adimidir.",
        "soru1": "Okula geldigimde en cok ne hissediyorum? Bu duygu gunun ilerleyen saatlerinde degisiyor mu?",
        "soru2": "Bu hafta tanistigim yeni biri var mi? Onu nasil tanimlardim? Bende nasil bir izlenim birakti?",
        "soru3": "Okulda en cok hangi ani sevdim? Bu ani ozel kilan neydi?",
        "soru4": "Okulda kendimi en guevnde hissettigim yer veya an hangisi? Neden?",
        "tamamla": "Yeni okulumda/sinifimda en cok hosuma giden sey...",
        "ciz": "Hayalindeki okulu ciz. Nasil gorunurdu? Neler olurdu? Ideal okulunda hangi ozellikler bulunurdu?",
        "yansitma": "Gozlerini kapat ve bu haftanin en guzel anini hayal et. O anda ne goruyorsun, ne duyuyorsun, ne hissediyorsun? Butun detaylariyla gunlugune yaz.",
    },
    10: {
        "aciklama": "Arkadaslik, cocukluk ve ergenlik doneminin en onemli sosyal deneyimlerinden biridir. Arkadaslarimizla yasadiklarimizi yazmak, iliskilriimizi daha iyi anlamamiza ve sosyal becerilerimizi gelistirmemize yardimci olur. Bu ayin gunluk sorulari arkadaslik degerlerini kesfetmeye yoneliktir.",
        "soru1": "En iyi arkadasimi neden seviyorum? Onu ozel kilan 3 ozellik ne?",
        "soru2": "Bu hafta bir arkadasima nasil yardimci oldum? Bu yardim beni nasil hissettirdi?",
        "soru3": "Arkadaslarimla en sevdigim etkinlik ne? Bu etkinligi sevmemin nedeni ne?",
        "soru4": "Bu hafta bir arkadasim beni kirdiysa veya ben onu kirdiysam ne oldu? Bunu nasil cozebilirim?",
        "tamamla": "Iyi bir arkadas olmak icin en onemli sey...",
        "ciz": "En guzel arkadaslik aninizi ciz. O anda neler oluyordu? Kiminleydin ve ne yapiyordunuz?",
        "yansitma": "Arkadasligiin sana kattigi en degerli seyi dusun. Eger arkadaslarin olmasaydi hayatin nasil farkli olurdu? Bu dusuncelerini birkacu cmleyle yaz.",
    },
    11: {
        "aciklama": "Sorumluluk almak buyumenin en onemli adimilarindandri. Kendi davranislarimizi ve aliskaanlklarimizi gozlemlemek, oz duzenleme becerimizi gelistirmenin anahtaridir. Bu ayin gunluk sorulari seni kendi rutinlerini ve sorumluluk duyugunu kesfetmeye davet ediyor.",
        "soru1": "Bugun sorumluluklarimi yerine getirdim mi? Nasil hissettim? Tamamlamadiklarim icin kendime ne soylerim?",
        "soru2": "Kendimi kontrol etmekte zorlandiigim bir an oldu mu? Ne yaptim? Farkli ne yapabilirdim?",
        "soru3": "En cok hangi konuda daha duzenli olmak istiyorum? Bu degisim icin atabilecegim ilk adim ne?",
        "soru4": "Bugunun en verimli saati hangisiydi? O saatte neden daha basarili oldugumu dusunuyorum?",
        "tamamla": "Sorumluluk almak beni ... hissettiriyor cunku...",
        "ciz": "Gunluk rutinini gosteren bir saat ciz ve her saate ne yaptigini yaz. Ideal rutinin nasil olurdu?",
        "yansitma": "Sorumlulk aldginda ve basardiginda kendini nasil hissediyorsun? Bu hissi hatirlamak seni gelecek gorevler icin nasil motive edebilir?",
    },
    12: {
        "aciklama": "Aralik ayi, empati ve yardimseverlik temasiyala doludur. Baskalari icin bir sey yapmanin bizde uyandirdigi duygulari kesfetmek, hem duygusal zekamizi hem de toplumsal duyarliligimizi gelistirir. Bu ayin gunluk yazilari seni iyilik ve paylasma uzerine dusunmeye davet ediyor.",
        "soru1": "Bu hafta birinin yuzunu guldrmek icin ne yaptim? O kisinin tepkisi nasil oldu?",
        "soru2": "Birisi bana yardim ettiginde ne hissettim? Yardim almak bazen neden zor olur?",
        "soru3": "Dunyada neyi degistirmek isterdim? Bu degisim icin ben ne yapabilirim?",
        "soru4": "Bugun minnettar oldugum bir olay veya kisi var mi? Bunu o kisiye soyledim mi?",
        "tamamla": "Baskalarina yardim ettigimde icimde...",
        "ciz": "Dunyanin daha guzel bir yer olmasi icin yapilabilecekleri gosteren bir poster ciz. Senin katkin ne olurdu?",
        "yansitma": "Yardim etmek ve yardim almak arasinda nasil bir iliski var? Hangisi sana daha kolay geliyor ve neden? Bu uzerine birkacu cmle yaz.",
    },
    1: {
        "aciklama": "Yeni yil, yeni baslangiclarin ve hedeflerin zamanidir. Gecmis donemi degerlendirmek ve gelecek icin bilingli hedefler koymak, kisisel gelisimin temelidir. Bu ayin gunluk sorulari seni hem geriye bakmaaya hem de ileriye planlamaya davet ediyor.",
        "soru1": "Bu yil kendim icin en onemli 3 hedefim ne? Bu hedefleri neden sectim?",
        "soru2": "Gecen donem en cok neyi basardim? Bu basari icin neleri dogru yaptim?",
        "soru3": "Hedeflerime ulasmak icin her gun ne yapabilirim? Hangi aliskanliklarimi degistirmem gerekiyor?",
        "soru4": "Gecen donem en cok neyde zorlanddim? Bu zorlugu asmak icin bu donem ne farkli yapacagim?",
        "tamamla": "Bu yilin sonunda ... olmus olmak istiyorum cunku...",
        "ciz": "Yil sonunda hayalindeki basariyi gosteren bir resim ciz. O ana ulastiginda nasil hissedeceksin?",
        "yansitma": "Hedeflerine ulasma yolunddaki en buyuk engel ne? Bu engeli asmanin yollarini dusun ve 3 somut adim yaz.",
    },
    2: {
        "aciklama": "Subat ayi sevgi, saygi ve degerleri kesfetme zamanidir. Sevgiyi farkli bicimlerinde tanimak — aile sevgisi, arkadaslik, oz sevgi — duygusal zekamizi guclendirir. Bu ayin gunluk sorulari seni sevgi ve saygi uzerine derinlemesine dusunmeye davet ediyor.",
        "soru1": "En cok kimi seviyorum ve ona bunu son ne zaman soyledim? Sevgimi ifade etmek bana kolay mi geliyor?",
        "soru2": "Birisi bana saygsizlik ettiginde nasil tepki veriyorum? Bu tepkim saglikli mi?",
        "soru3": "Sevgi gostermenin benim icin en kolay yolu ne? Sozcuklerle mi, eylemlerle mi, hediyelerle mi?",
        "soru4": "Kendimi ne zaman en cok sevilmis hissediyorum? Bu duyguyu yarataan seyler neler?",
        "tamamla": "Sevilmek beni ... hissettiriyor ve ben sevgimi ... gosteriyorum.",
        "ciz": "Seni en cok mutlu eden ani ciz ve altina ne hissettiginii yaz. O anda kimler vardi?",
        "yansitma": "Sevgi dillerini dusun: olumlu sozler, kaliteli zaman, hediye, yardim etme, fiziksel temas. Senin sevgi dilin hangisi? Sevdiklerinin sevgi dili ne? Bu farkliliklari anlamak iliskilerini nasil iyilestirebilir?",
    },
    3: {
        "aciklama": "Mart ayi ozguven ve bireysel farkliliklari kutlama zamanidir. Kendini tanimak, guclu yonlerini kesfetmek ve benzersizligini takdir etmek saglikli bir benlik algisinin temelidir. Bu ayin gunluk sorulari seni ic dunyana yolculuga cikmaya davet ediyor.",
        "soru1": "Kendimde en cok begendgim 3 ozellik ne? Bu ozellikler bana ne kazandiriyor?",
        "soru2": "Son zamalarda basardiim ve gurur duydugum bir sey var mi? Bu basariya ulasimak icin ne yaptim?",
        "soru3": "Baskalarindan farkli olan hangi ozelligim beni ozel kiliyor? Bu farkliligi nasil degerlendirebilirim?",
        "soru4": "Hata yaptigimda kendime nasil daavraniyorum? Kendime bir arkadasima davrandiigim gibi mi yaklasiiyorum?",
        "tamamla": "Ben ozelim cunku...",
        "ciz": "Kendinin super kahraman versiyonunu ciz. Super gucun ne olurdu? Bu gucu nasil kullanirdin?",
        "yansitma": "Aynaya bak ve kendine 3 guzel sey soyle. Bunu yaparken ne hissettin? Kendimize nazik olmak neden bazen zor olur? Bu konudaki dusuncelerini yaz.",
    },
    4: {
        "aciklama": "Nisan ayi kitap okuma ve hayal gucunu kutlama zamanidir. Okudugu kitaplar uzerine yazmak, anlama derinligini arttirir ve elestirel dusunme becerisini gelistirir. Bu ayin gunluk sorulari seni okumanin buyuluuu dunyasini kesfetmeye davet ediyor.",
        "soru1": "Son okudigum kitap hangisi ve ne hissettirdi? Kitaptaki hangi sahne beni en cok etkiledi?",
        "soru2": "Bir kitap karakteri olsam kim olmak isterdim? Neden? O karakterin hangi ozelligi beni cezbediyor?",
        "soru3": "Bir kitap yazsam konusu ne olurdu? Ana karakter nasil bir kisi olurdu?",
        "soru4": "Okumak hayatiima ne katiyor? Kitap okumadigim donemlerle okuduguumuz donemleri karsilastirsam ne fark goruyorum?",
        "tamamla": "Kitap okurken en cok sevdigim sey...",
        "ciz": "Kendi kitabinin kapagini tasarla. Adi ve resmi nasil olurdu? Arka kapakta ne yazardi?",
        "yansitma": "Hayatinda okudugun en etkili kitabi dusun. O kitap seni nasil degistirdi? Baska birine neden onerirdin? Bu kitapla ilgili duygularini yaz.",
    },
    5: {
        "aciklama": "Mayis ayi aile baglarini kutlama ve guclendirme zamanidir. Ailemizle ilgili dusncelerimizi yazmak, minnettarlik duygumuz arttirir ve iletisim becerilerimizi gelistirir. Bu ayin gunluk sorulari seni aile ilisikleriin uzerine dusunmeye davet ediyor.",
        "soru1": "Aileme en son ne zaman tesekkur ettim? Neleer icin tesekkur ettim?",
        "soru2": "Ailemle en sevdigim etkinlik ne? Bu etkinligi ozel kilan ne?",
        "soru3": "Ailemi anlatan 3 kelime soylesem bunlar ne olurdu? Bu kelimeler neden aklima geldi?",
        "soru4": "Ailemle en son ne zaman gercekten kaliteli vakit gecirdim? O an ne yapiyorduk?",
        "tamamla": "Ailem benim icin onemli cunku...",
        "ciz": "Ailene bir tesekkur karti tasarla. Icine ne yazardin? Her aile uyesine ozel bir mesaj ekle.",
        "yansitma": "Ailenin sana verdigi en degerli hediye nedir? (Maddi olmayan) Bu hediyeyi takdir ettiini ona nasil gosterebilirsin?",
    },
    6: {
        "aciklama": "Haziran ayi yil sonu degerlendirmesi ve yaz tatiline haziirlik zamanidir. Geri donup bakmak, ogrenilenleri ozumsemek ve gelecege umutla bakmak icin mukkemmel bir zaman. Bu ayin gunluk sorulari seni bir yilin muhasebesini yapmaaya davet ediyor.",
        "soru1": "Bu yil ogrendigim en onemli 3 sey ne? Bunlari sadece derslerde mi yoksa hayatta mi ogrendim?",
        "soru2": "Yaz tatilinde en cok ne yapmak istiyorum? Bu etkinlikleri neden sectim?",
        "soru3": "Gelecek yil nasil bir insan olmak istiyorum? Bu ideal haline ulaasmak icin ne yapmaliyim?",
        "soru4": "Bu yil en cok kime tesekkur etmek istiyorum? Bunu yaptim mi?",
        "tamamla": "Bu ogretim yili bana ogretti ki...",
        "ciz": "Bu yilin en guzel anini gosteren bir resim ciz ve altina tarihini yaz. O an neden unutulamaz?",
        "yansitma": "Bu yili bir yolculuk olarak dusun. Nereden baslaadin, simaadi neredesin? Yol boyunca en zor tepe hangisiydi? En guzel manzara neredeydi? Bu yolculugu anlatan bir paragraf yaz.",
    },
}

# ── Dijital Okuryazarlık İpuçları (P17) ──
_BULTEN_DIJITAL = {
    9: {
        "baslik": "Güvenli İnternet Kullanımına Giriş",
        "ipuclari": [
            "İnternette asla gerçek adını, adresini ve telefon numaranı yabancılarla paylaşma.",
            "Şifrelerin en az 8 karakter olsun ve kimseyle paylaşma (anne-baba hariç).",
            "Tanımadığın kişilerden gelen mesajlara cevap verme, anne-babana göster.",
            "Güvenilir web siteleri genellikle 'https' ile başlar — kilit işaretini kontrol et.",
        ],
        "tehlike": "Tanımadığın kişilerin arkadaşlık isteklerini kabul etmek ciddi güvenlik riskleri oluşturabilir.",
        "kural": "Aile kuralı: İnternete bağlanmadan önce anne-babadan izin al ve ekran süresini birlikte belirleyin.",
    },
    10: {
        "baslik": "Siber Zorbalık Nedir, Nasıl Korunuruz?",
        "ipuclari": [
            "Birisi internette seni üzüyorsa veya korkutuyorsa hemen bir yetişkine söyle.",
            "Kırıcı mesajlara cevap verme — ekran görüntüsü al ve engelle.",
            "Başkalarını incitecek mesajlar, yorumlar veya fotoğraflar paylaşma.",
            "Arkadaşının fotoğrafını izni olmadan internete yükleme.",
        ],
        "tehlike": "Siber zorbalık fiziksel zorbalık kadar zararlıdır. Çocuklarda kaygı, depresyon ve okul kaçırma davranışına yol açabilir.",
        "kural": "Aile kuralı: İnternette birinin sizi rahatsız etmesi durumunda hemen bir yetişkine haber verin, bu sizi zayıf göstermez.",
    },
    11: {
        "baslik": "Ekran Süresi Yönetimi",
        "ipuclari": [
            "Okul dışı günlük ekran süresi ilkokul için 1 saat, ortaokul için 1.5 saat önerilir.",
            "Yatmadan en az 1 saat önce tüm ekranları kapat — mavi ışık uykunu bozar.",
            "Her 20 dakikada bir ekrandan 20 saniye uzağa bak (20-20-20 kuralı).",
            "Ekran yerine fiziksel aktivite, okuma veya aile zamanı koy.",
        ],
        "tehlike": "Aşırı ekran süresi uyku bozuklukları, konsantrasyon güçlüğü ve obezite riskini artırır.",
        "kural": "Aile kuralı: Yemek masasında ve yatak odasında telefon/tablet kullanılmaz.",
    },
    12: {
        "baslik": "Dijital Ayak İzi — İnternet Unutmaz",
        "ipuclari": [
            "İnternette paylaştığın her şey kalıcı olabilir — silsen bile birisi kaydetmiş olabilir.",
            "Bir şey paylaşmadan önce düşün: 'Bunu öğretmenim veya ailem görse ne der?'",
            "Fotoğraf paylaşırken arka planda ev adresi veya okul gibi bilgiler görünmemesine dikkat et.",
            "Eski hesaplarını ve kullanmadığın uygulamaları düzenli olarak temizle.",
        ],
        "tehlike": "Bugün paylaştığın bir fotoğraf veya yorum, yıllar sonra karşına çıkabilir ve seni olumsuz etkileyebilir.",
        "kural": "Aile kuralı: Paylaşmadan önce '3 saniye kuralı' uygulayın — gönder butonuna basmadan 3 saniye düşünün.",
    },
    1: {
        "baslik": "Sahte Haberleri ve Yanlış Bilgiyi Tanıma",
        "ipuclari": [
            "Bir haberi okuyunca hemen inanma — kaynağı kontrol et.",
            "Aynı haberi farklı kaynaklardan doğrula; tek kaynağa güvenme.",
            "Çok duygusal veya şok edici başlıklara dikkat et — tıklama tuzağı olabilir.",
            "Haberin tarihini kontrol et — eski haberler bazen yeni gibi paylaşılır.",
        ],
        "tehlike": "Yanlış bilgi hızla yayılır ve toplumda korku, panik ve ayrımcılığa neden olabilir.",
        "kural": "Aile kuralı: Bir bilgiyi paylaşmadan önce en az 2 farklı güvenilir kaynaktan doğrulayın.",
    },
    2: {
        "baslik": "Kişisel Gizlilik ve Mahremiyet",
        "ipuclari": [
            "Uygulama indirirken istenen izinleri kontrol et — kamera veya mikrofon izni gereksiz olabilir.",
            "Konum paylaşımını sadece gerektiğinde aç, sürekli açık bırakma.",
            "Wi-Fi ağlarına bağlanırken dikkatli ol — halka açık ağlarda kişisel bilgi girme.",
            "Her uygulama için farklı şifre kullan; şifre yöneticisi kullanabilirsin.",
        ],
        "tehlike": "Kişisel bilgilerin yanlış kişilerin eline geçmesi kimlik hırsızlığına yol açabilir.",
        "kural": "Aile kuralı: Yeni bir uygulama indirmeden önce birlikte gizlilik ayarlarını kontrol edin.",
    },
    3: {
        "baslik": "Sosyal Medya ve Benlik Algısı",
        "ipuclari": [
            "Sosyal medyadaki fotoğraflar filtrelenmiş ve düzenlenmiştir; gerçek hayatı yansıtmaz.",
            "Beğeni sayısı senin değerini belirlemez — gerçek ilişkiler ekrandan önemlidir.",
            "Kendini kötü hissettiren hesapları takipten çıkarmaktan çekinme.",
            "Sosyal medyada geçirdiğin zamanı takip et ve sınır koy.",
        ],
        "tehlike": "Sosyal medyada sürekli karşılaştırma yapmak özgüven düşüklüğü ve kaygıya yol açabilir.",
        "kural": "Aile kuralı: Sosyal medya hesabı açmadan önce yaş sınırını ve aile kurallarını birlikte belirleyin.",
    },
    4: {
        "baslik": "Dijital İçerik Okuma ve Değerlendirme",
        "ipuclari": [
            "E-kitaplar ve dijital kütüphaneler harika kaynaklar — ama basılı kitapların da yerini tutamaz.",
            "İnternetten araştırma yaparken birden fazla kaynak kullan ve kaynakları not et.",
            "Vikipedi iyi bir başlangıçtır ama tek kaynak olarak kullanma — alttaki referansları kontrol et.",
            "Ekrandan okurken gece modunu (dark mode) kullanarak göz sağlığını koru.",
        ],
        "tehlike": "Tek kaynağa dayalı araştırma yapma, yanlış veya eksik bilgiye dayanarak ödev hazırlama riski taşır.",
        "kural": "Aile kuralı: Her dijital araştırmada en az 3 farklı güvenilir kaynak kullanın.",
    },
    5: {
        "baslik": "Aile İçi Dijital Denge",
        "ipuclari": [
            "Aile yemeğinde telefonları masadan kaldırın — bu zaman birbirinize aittir.",
            "Hafta sonları 'dijital detoks' saatleri belirleyin — ekransız etkinlikler planlayın.",
            "Çocukların dijital dünyasına ilgi gösterin — ne oynadıklarını, ne izlediklerini sorun.",
            "Birlikte yapılabilecek dijital etkinlikler deneyin: aile fotoğraf albümü, birlikte video izleme.",
        ],
        "tehlike": "Her aile bireyinin ayrı ekrana bakması aile iletişimini ve bağlarını zayıflatır.",
        "kural": "Aile kuralı: Hafta sonları en az 2 saat birlikte ekransız vakit geçirin.",
    },
    6: {
        "baslik": "Yaz Tatilinde Teknoloji Dengesi",
        "ipuclari": [
            "Yaz tatilinde ekran süresini artırmak yerine dış mekan etkinliklerine yönel.",
            "Eğitici uygulamalar ve kodlama oyunları ile teknolojiyi verimli kullan.",
            "Doğa fotoğrafçılığı, blog yazma gibi yaratıcı dijital projeler dene.",
            "Günlük bir 'ekransız macera saati' belirle — doğayı keşfet, spor yap.",
        ],
        "tehlike": "Tatilde kontrolsüz ekran kullanımı uyku düzenini bozar ve okula dönüşü zorlaştırır.",
        "kural": "Aile kuralı: Yaz tatilinde de tutarlı ekran süresi kuralı uygulayın; tatil ekran tatili değildir.",
    },
}

# ── Sağlık & İyi Oluş Köşesi (P18) ──
_BULTEN_SAGLIK = {
    9: {
        "baslik": "Kaliteli Uyku: Başarının Gizli Anahtarı",
        "bilgi": (
            "Uyku, beynin gün boyunca öğrendiklerini işlediği ve hafızaya kaydettiği zamandır. "
            "İlkokul çağındaki çocukların günde 9-12 saat, ortaokul öğrencilerinin 8-10 saat "
            "uyuması önerilir. Yetersiz uyku dikkat dağınıklığı, sinirlilik ve bağışıklık "
            "zayıflığına neden olur."
        ),
        "ipuclari": [
            "Her gün aynı saatte yatıp aynı saatte kalk — hafta sonları da dahil.",
            "Yatmadan 1 saat önce ekranları kapat; mavi ışık uyku hormonunu baskılar.",
            "Yatak odasını karanlık, serin ve sessiz tut.",
            "Yatmadan önce rahatlatıcı bir rutin oluştur: kitap okuma, hafif müzik.",
        ],
        "tarif": "Uyku öncesi 'Muz-Süt Smoothie': 1 muz + 1 bardak ılık süt + 1 tatlı kaşığı bal. Muz magnezyum, süt triptofan içerir — ikisi de rahatlatıcıdır.",
    },
    10: {
        "baslik": "Sosyal Sağlık: Arkadaşlığın Gücü",
        "bilgi": (
            "İnsan sosyal bir varlıktır ve sağlıklı ilişkiler fiziksel sağlığı da doğrudan etkiler. "
            "Araştırmalar, güçlü sosyal bağları olan çocukların bağışıklık sistemlerinin daha güçlü, "
            "stres düzeylerinin daha düşük olduğunu göstermektedir. Yalnızlık, tıpkı fiziksel "
            "bir hastalık gibi vücudu olumsuz etkiler."
        ),
        "ipuclari": [
            "Her gün en az bir arkadaşınla kaliteli vakit geçir.",
            "Yeni insanlarla tanışmaktan çekinme — gülümse ve merhaba de.",
            "Sorun yaşadığında güvendiğin bir kişiyle konuş, içinde tutma.",
        ],
        "tarif": "Arkadaşlık günü 'Trail Mix': Fındık + kuru üzüm + ay çekirdeği + kuru meyve karışımı. Arkadaşlarınla paylaşarak ye — paylaşmak mutluluk artırır!",
    },
    11: {
        "baslik": "Beyin Dostu Beslenme",
        "bilgi": (
            "Beyin, vücuttaki en çok enerji tüketen organdır — aldığımız kalorinin %20'sini kullanır. "
            "Omega-3 yağ asitleri (balık, ceviz), antioksidanlar (meyve, sebze) ve demir "
            "(kırmızı et, ıspanak) beynin en önemli besin maddeleridir. Kahvaltı atlamak "
            "sabah derslerinde konsantrasyon kaybına neden olur."
        ),
        "ipuclari": [
            "Günü mutlaka kahvaltıyla başla — yumurta, peynir ve tam tahıl ekmeği ideal.",
            "Haftada en az 2 kez balık ye — omega-3 hafızayı güçlendirir.",
            "Bol su iç; hafif susuzluk bile dikkat ve hafızayı olumsuz etkiler.",
            "Şekerli atıştırmalıklar yerine meyve ve kuruyemiş tercih et.",
        ],
        "tarif": "Beyin güçlendirici 'Cevizli Muz Barı': 2 muz ez + 1 su bardağı yulaf + yarım bardak ceviz kır + 2 yemek kaşığı bal karıştır. Tepside yay, buzdolabında 2 saat beklet, dilimle.",
    },
    12: {
        "baslik": "Kış Sağlığı ve Bağışıklık Sistemi",
        "bilgi": (
            "Kış aylarında soğuk hava, kapalı ortamlar ve güneş ışığı azalması bağışıklık "
            "sistemini zayıflatır. C vitamini, D vitamini ve çinko bağışıklığın en önemli "
            "destekçileridir. Düzenli uyku, dengeli beslenme ve fiziksel aktivite kışın "
            "hasta olmama kalkanıdır."
        ),
        "ipuclari": [
            "Her gün en az 1 porsiyon turunçgil (portakal, mandalina) ye.",
            "Ellerini sık sık sabunla en az 20 saniye yıka.",
            "Kapalı ortamları düzenli olarak havalandır.",
            "Soğuk havada bile günde 30 dakika dışarıda vakit geçir.",
        ],
        "tarif": "Bağışıklık çayı: 1 bardak sıcak su + limon suyu + 1 tatlı kaşığı bal + taze zencefil rendesi. Günde 1-2 bardak için.",
    },
    1: {
        "baslik": "Yeni Yıl Sağlık Hedefleri",
        "bilgi": (
            "Yeni yıl, sağlıklı alışkanlıklar edinmek için mükemmel bir başlangıçtır. "
            "Araştırmalar, küçük ve spesifik hedeflerin büyük ve genel hedeflerden daha "
            "başarılı olduğunu göstermektedir. 'Daha sağlıklı olacağım' yerine "
            "'Her gün 1 meyve yiyeceğim' gibi somut hedefler koyun."
        ),
        "ipuclari": [
            "Her gün 8 bardak su içme hedefi koy ve takip et.",
            "Haftada en az 3 gün 30 dakika fiziksel aktivite yap.",
            "Günde 5 porsiyon meyve-sebze hedefle.",
            "Uyku saatini sabit tut; düzenli uyku sağlığın temelidir.",
        ],
        "tarif": "Sabah enerjisi 'Yeşil Smoothie': 1 muz + 1 avuç ıspanak + yarım elma + 1 bardak süt. Blenderdan geçir, güne enerjik başla!",
    },
    2: {
        "baslik": "Duygusal Sağlık ve Stres Yönetimi",
        "bilgi": (
            "Duygusal sağlık, fiziksel sağlık kadar önemlidir. Stres, kaygı ve üzüntü "
            "her insanın yaşadığı normal duygulardır — önemli olan bu duygularla baş etme "
            "becerisi geliştirmektir. Kronik stres bağışıklık sistemini zayıflatır, "
            "uyku bozuklukları ve konsantrasyon kaybına yol açar."
        ),
        "ipuclari": [
            "Stresli hissettiğinde 4-7-8 nefes tekniğini uygula: 4 say nefes al, 7 say tut, 8 say ver.",
            "Duygularını bir günlüğe yaz — yazmak rahatlatıcıdır.",
            "Fiziksel aktivite stres hormonlarını azaltır — dans et, yürü, spor yap.",
            "Güvendiğin biriyle konuş; paylaşılan yük hafifler.",
        ],
        "tarif": "Rahatlatıcı 'Papatya-Lavanta Suyu': 1 bardak soğuk su + 2-3 kurutulmuş papatya + 1 damla lavanta. Buzdolabında 1 saat beklet, rahatlatıcı etkisini hisset.",
    },
    3: {
        "baslik": "Beden Olumlaması ve Sağlıklı Beden Algısı",
        "bilgi": (
            "Her beden farklıdır ve her beden değerlidir. Özellikle ergenlik döneminde vücuttaki "
            "değişimler kafa karışıklığına neden olabilir. Medyadaki 'ideal beden' imajları "
            "gerçekçi değildir — sağlıklı olmak güzel olmaktan çok daha önemlidir."
        ),
        "ipuclari": [
            "Vücudunun yapabildiği şeylere odaklan: koşmak, oynamak, sarılmak.",
            "Aynaya bakınca güzel bir şey söyle: 'Gözlerim çok güzel' veya 'Güçlüyüm'.",
            "Yemeği keyifle ye, yasaklama — sezgisel beslenmeyi öğren.",
            "Bedeni eleştiren konuşmalardan uzak dur; olumlu çevreni koru.",
        ],
        "tarif": "Renkli meyve tabağı: Her renkte bir meyve seç (kırmızı çilek, turuncu mandalina, sarı muz, yeşil kivi, mor üzüm). Gözün de karnın da doyacak!",
    },
    4: {
        "baslik": "Göz Sağlığı ve Okuma Ergonomisi",
        "bilgi": (
            "Dijital çağda göz sağlığı kritik önem taşımaktadır. Uzun süre ekrana veya "
            "kitaba bakmak göz yorgunluğuna, baş ağrısına ve bulanık görmeye neden olabilir. "
            "20-20-20 kuralı en etkili koruma yöntemidir: Her 20 dakikada bir, "
            "20 saniye boyunca 20 adım uzağa bak."
        ),
        "ipuclari": [
            "Kitap okurken yeterli ve doğal aydınlatma sağla — göz kısmadan oku.",
            "Ekran parlaklığını ortam ışığına göre ayarla.",
            "Okuma mesafesi en az 30-40 cm olmalı — kitabı gözüne çok yakın tutma.",
            "Dışarıda vakit geçirmek miyop riskini azaltır — her gün en az 1 saat dışarıda ol.",
        ],
        "tarif": "Göz dostu atıştırmalık: Havuç çubukları + humus. Havuçtaki beta-karoten göz sağlığını korur, humus protein ve lif sağlar.",
    },
    5: {
        "baslik": "Açık Hava Aktivitesi ve Hareket",
        "bilgi": (
            "Çocukların günde en az 60 dakika orta-yoğun fiziksel aktivite yapması önerilir. "
            "Açık havada hareket etmek D vitamini üretimini artırır, ruh halini iyileştirir "
            "ve akademik performansı olumlu etkiler. Bahar ayları dış mekan aktiviteleri "
            "için ideal bir zamandır."
        ),
        "ipuclari": [
            "Her gün en az 30 dakika dışarıda oyna, yürü veya spor yap.",
            "Okul sonrası parkta vakit geçir — doğa stresi azaltır.",
            "Aile yürüyüşleri planlayın — haftada bir doğa yürüyüşü harika olur.",
            "Ekran başında geçirdiğin her saat için 15 dakika fiziksel aktivite yap.",
        ],
        "tarif": "Piknik enerjisi 'Meyve Şiş': Çilekleri, muz dilimlerini ve üzümleri tahta çubuklara diz. Eğlenceli, sağlıklı ve paylaşımcı!",
    },
    6: {
        "baslik": "Yaz Güvenliği ve Güneşten Korunma",
        "bilgi": (
            "Yaz aylarında güneş çarpması, sıvı kaybı ve güneş yanığı en sık karşılaşılan "
            "sağlık sorunlarıdır. Çocukların ince teni yetişkinlere göre güneşe karşı daha "
            "hassastır. Saat 11:00-16:00 arası güneş en güçlü olduğu saatlerdir ve "
            "doğrudan güneşten kaçınılmalıdır."
        ),
        "ipuclari": [
            "Dışarı çıkmadan 30 dakika önce en az SPF 30 güneş kremi sür.",
            "Şapka ve güneş gözlüğü kullan; açık renkli, bol giysiler giy.",
            "Her saat başı su iç — susuzluk hissetmeyi bekleme.",
            "Sıcak saatlerde gölgede kal; deniz ve havuzda güvenlik kurallarına uy.",
        ],
        "tarif": "Serinletici 'Karpuz Dondurması': Karpuz dilimlerini tahta çubuklara geçir, buzlukta 3 saat dondur. Şekersiz, doğal ve serinletici!",
    },
}

# ── Gelecek Ay Ön İzleme (P19) ──
_BULTEN_GELECEK = {
    9: {
        "gelecek_tema": "Arkadaşlık ve Sosyal Beceriler",
        "gelecek_ikon": "🤝",
        "on_izleme": "Ekim ayında arkadaşlık becerilerini güçlendireceğiz. Yeni arkadaşlar edinme, paylaşma ve birlikte çalışma konularını ele alacağız.",
        "hazirlık": "Çocuğunuzla birlikte 'İyi bir arkadaş nasıl olunur?' konusunu konuşun.",
        "kapanış": "Güzel bir eylül ayı geçirdik! Çocuğunuzun okula uyum süreci her geçen gün güçleniyor. Sabır ve sevginiz için teşekkür ederiz.",
    },
    10: {
        "gelecek_tema": "Sorumluluk ve Öz Düzenleme",
        "gelecek_ikon": "📋",
        "on_izleme": "Kasım ayında sorumluluk almayı ve kendini düzenleme becerilerini ele alacağız. Planlama, düzen ve öz kontrol temalı etkinlikler yapacağız.",
        "hazirlık": "Çocuğunuza evde küçük sorumluluklar verin — oda toplama, çanta hazırlama gibi.",
        "kapanış": "Arkadaşlıklarla dolu harika bir ekim geçirdik! Çocuğunuzun sosyal becerileri her gün gelişiyor.",
    },
    11: {
        "gelecek_tema": "Empati ve Yardımseverlik",
        "gelecek_ikon": "💝",
        "on_izleme": "Aralık ayında empati ve yardımseverlik temalarını işleyeceğiz. Başkalarını anlama, paylaşma ve dayanışma konularında etkinlikler hazırlıyoruz.",
        "hazirlık": "Birlikte ihtiyaç sahiplerine yardım edebileceğiniz bir etkinlik planlayın.",
        "kapanış": "Sorumluluk bilinciyle dolu bir kasım ayı geçirdik. Çocuğunuzun öz düzenleme becerilerindeki gelişimi fark edeceksiniz.",
    },
    12: {
        "gelecek_tema": "Hedef Belirleme ve Motivasyon",
        "gelecek_ikon": "🎯",
        "on_izleme": "Ocak ayında yeni yılın heyecanıyla hedef belirleme ve motivasyon konularını ele alacağız. Çocuklarımız kendi hedeflerini koymayı öğrenecek.",
        "hazirlık": "Yeni yıl için aile hedefleri belirleyebilirsiniz — çocuğunuzun da kendi hedefleri olsun.",
        "kapanış": "Empati ve paylaşımla dolu güzel bir aralık ayı geçirdik. İyi tatiller ve mutlu yıllar!",
    },
    1: {
        "gelecek_tema": "Sevgi, Saygı ve Değerler",
        "gelecek_ikon": "❤️",
        "on_izleme": "Şubat ayında sevgi, saygı ve temel değerler konularını işleyeceğiz. Zorbalık önleme ve sağlıklı ilişkiler de gündemimizde olacak.",
        "hazirlık": "Çocuğunuzla sevgi ve saygı hakkında konuşun; 'Saygı göstermek ne demektir?' sorusunu birlikte tartışın.",
        "kapanış": "Hedeflerle dolu enerjik bir ocak ayı geçirdik! Çocuğunuzun belirlediği hedeflere birlikte destek olmaya devam edin.",
    },
    2: {
        "gelecek_tema": "Özgüven ve Bireysel Farklılıklar",
        "gelecek_ikon": "⭐",
        "on_izleme": "Mart ayında özgüven ve bireysel farklılıkları kutlayacağız. Her çocuğun benzersiz ve değerli olduğunu vurgulayacağız.",
        "hazirlık": "Çocuğunuzun güçlü yönlerini ve benzersiz özelliklerini birlikte keşfedin.",
        "kapanış": "Sevgi ve saygıyla dolu bir şubat ayı geçirdik. Çocuğunuza olan sevginizi her fırsatta gösterin.",
    },
    3: {
        "gelecek_tema": "Kitap Okuma ve Hayal Gücü",
        "gelecek_ikon": "📖",
        "on_izleme": "Nisan ayında kitap okuma ve hayal gücü temalarını işleyeceğiz. 23 Nisan coşkusuyla okuma sevgisini pekiştireceğiz.",
        "hazirlık": "Çocuğunuzla birlikte kütüphaneye gidin ve birlikte kitap seçin.",
        "kapanış": "Özgüvenle parlayan bir mart ayı geçirdik! Çocuğunuzun kendine güveninin her gün arttığını göreceksiniz.",
    },
    4: {
        "gelecek_tema": "Aile İletişimi ve Bağlar",
        "gelecek_ikon": "🏠",
        "on_izleme": "Mayıs ayında aile iletişimi ve güçlü aile bağları konularını ele alacağız. Anneler Günü temasıyla aile sevgisini kutlayacağız.",
        "hazirlık": "Aile olarak birlikte kaliteli zaman geçirme planları yapın.",
        "kapanış": "Kitaplarla ve hayallerle dolu harika bir nisan ayı geçirdik! Okuma alışkanlığını yaz boyu sürdürmeyi hedefleyin.",
    },
    5: {
        "gelecek_tema": "Yaz Tatili ve Değerlendirme",
        "gelecek_ikon": "☀️",
        "on_izleme": "Haziran ayında yılı değerlendirip yaz tatiline hazırlanacağız. Güvenli ve verimli bir yaz için planlar yapacağız.",
        "hazirlık": "Çocuğunuzla birlikte yaz tatili planı yapmaya başlayın — okuma listesi, kamp, gezi planları.",
        "kapanış": "Aile bağlarımızı güçlendirdiğimiz güzel bir mayıs ayı geçirdik. Ailenizle birlikte olmanın keyfini çıkarın.",
    },
    6: {
        "gelecek_tema": "Yeni Maceralar ve Gelecek Yıl Heyecanı",
        "gelecek_ikon": "🌟",
        "on_izleme": "Harika bir eğitim yılını geride bırakıyoruz! Yaz tatilinde dinlenin, keşfedin ve gelecek yıl için enerji depolayın. Eylül'de daha güçlü buluşacağız!",
        "hazirlık": "Yaz boyunca haftada en az 3 kitap okumasını, fiziksel aktivite yapmasını ve yeni bir beceri öğrenmesini teşvik edin.",
        "kapanış": "Bir eğitim yılını daha birlikte tamamladık. Çocuğunuzun bu yıl gösterdiği gelişim ve büyüme gerçekten takdire değer. İyi tatiller, sağlıcakla kalın!",
    },
}

# ── P20: Kariyer Keşfi ──
_BULTEN_KARIYER = {
    9: {"baslik": "Meslek Dünyası", "tanim": "Hayalindeki meslek ne? Her meslek topluma farklı bir katkı sunar.",
        "meslekler": [("Öğretmen", "📚", "İnsanlara bilgi ve beceri kazandırır. Toplumun temel taşıdır."),
                      ("Doktor", "🏥", "İnsanların sağlığını korur ve tedavi eder. Fedakârlık gerektirir."),
                      ("Mühendis", "⚙️", "Problemlere yaratıcı çözümler üretir. Köprüler, binalar, yazılımlar tasarlar."),
                      ("Sanatçı", "🎨", "Duyguları ve düşünceleri sanat yoluyla ifade eder. Toplumu zenginleştirir.")],
        "soru": "Bu ay bir meslek araştırması yap: Hangi meslek seni heyecanlandırıyor? Neden?"},
    10: {"baslik": "Yeteneklerimi Keşfediyorum", "tanim": "Herkesin kendine özgü yetenekleri vardır. Önemli olan onları keşfetmektir.",
         "meslekler": [("Bilim İnsanı", "🔬", "Merak ederek keşfeder, deneyler yaparak gerçeği arar."),
                       ("Sporcu", "⚽", "Disiplin ve azimle hedeflerine ulaşır. Takım ruhu önemlidir."),
                       ("Gazeteci", "📰", "Olayları araştırır, halkı bilgilendirir. Doğruyu söylemek esastır."),
                       ("Çiftçi", "🌾", "Toprağı işler, insanları besler. Doğayla uyum içinde çalışır.")],
         "soru": "Hangi yeteneklerin var? Bu yeteneklerle hangi meslekleri yapabilirsin?"},
    11: {"baslik": "Girişimci Ruhu", "tanim": "Girişimciler hayalleri gerçeğe dönüştürür.",
         "meslekler": [("Yazılımcı", "💻", "Dijital dünyayı şekillendirir. Kodlarla çözüm üretir."),
                       ("Mimar", "🏗️", "Yaşam alanları tasarlar. Estetik ve işlevselliği birleştirir."),
                       ("Pilot", "✈️", "Gökyüzünde yolculuk eder. Sorumluluk ve dikkat gerektirir."),
                       ("Aşçı", "👨‍🍳", "Lezzetlerle mutluluk yaratır. Yaratıcılık ve sabır ister.")],
         "soru": "Bir gün kendi işini kurmak istersen, ne tür bir iş olurdu?"},
    12: {"baslik": "Takım Çalışması", "tanim": "Büyük başarılar takım çalışmasıyla gelir.",
         "meslekler": [("Hemşire", "💉", "Hasta bakımında doktorun en yakın yardımcısıdır."),
                       ("İtfaiyeci", "🚒", "Tehlikeli anlarda insanları kurtarır. Cesaret simgesidir."),
                       ("Psikolog", "🧠", "İnsanların ruh sağlığını korur ve iyileştirir."),
                       ("Veteriner", "🐾", "Hayvanların sağlığıyla ilgilenir. Sevgi ve şefkat gerektirir.")],
         "soru": "Bir takım projesi tasarla: Hangi meslekler birlikte çalışmalı?"},
    1: {"baslik": "Yeni Yıl, Yeni Hedefler", "tanim": "Kariyer yolculuğunda hedef belirlemek ilk adımdır.",
        "meslekler": [("Astronot", "🚀", "Uzayı keşfeder, bilime katkı sağlar."),
                      ("Arkeolog", "🏛️", "Geçmişi kazıyarak tarihi aydınlatır."),
                      ("Çevre Mühendisi", "🌿", "Doğayı koruyarak geleceği şekillendirir."),
                      ("Müzisyen", "🎵", "Melodilerle duyguları ifade eder, ruhu besler.")],
        "soru": "2026'da kendine bir kariyer hedefi koy. Bu hedef için ne yapmalısın?"},
    2: {"baslik": "Liderlik", "tanim": "Lider olmak için önce kendini tanımalısın.",
        "meslekler": [("Avukat", "⚖️", "Adaleti savunur, hakları korur."),
                      ("Diplomat", "🤝", "Ülkeler arası barış ve iş birliği sağlar."),
                      ("Öğretim Üyesi", "🎓", "Bilimsel araştırma yapar ve bilgiyi aktarır."),
                      ("Sosyal Hizmet Uzmanı", "❤️", "Toplumun dezavantajlı kesimlerine destek olur.")],
        "soru": "Hangi liderlik özelliklerine sahipsin? Hangilerini geliştirmek istersin?"},
    3: {"baslik": "Yaratıcılık ve Meslek", "tanim": "Yaratıcılık her meslekte fark yaratır.",
        "meslekler": [("Grafik Tasarımcı", "🎨", "Görsel iletişim dünyasını şekillendirir."),
                      ("Yönetmen", "🎬", "Hikayeleri görselleştirir, sinemayı sanatla buluşturur."),
                      ("Endüstri Tasarımcısı", "🛋️", "Günlük hayatı kolaylaştıran ürünler tasarlar."),
                      ("Robot Mühendisi", "🤖", "Geleceğin teknolojisini bugünden inşa eder.")],
        "soru": "Yaratıcılığını kullanarak hangi mesleği yapmak isterdin?"},
    4: {"baslik": "Bilim ve Teknoloji", "tanim": "Bilim ve teknoloji geleceği şekillendirir.",
        "meslekler": [("Veri Bilimci", "📊", "Büyük veriden anlamlı bilgiler çıkarır."),
                      ("Biyoteknolog", "🧬", "Canlı sistemleri kullanarak yeni ürünler geliştirir."),
                      ("Siber Güvenlik Uzmanı", "🔒", "Dijital dünyayı tehditlere karşı korur."),
                      ("Uzay Mühendisi", "🛰️", "Uzay araçları ve uyduları tasarlar.")],
        "soru": "Teknolojinin 10 yıl sonra hangi meslekleri değiştireceğini düşünüyorsun?"},
    5: {"baslik": "Topluma Hizmet", "tanim": "Mesleğinle topluma katkı sağlamak en anlamlı başarıdır.",
        "meslekler": [("Eczacı", "💊", "İlaçlar konusunda uzmanlaşarak sağlığa katkı sağlar."),
                      ("Diyetisyen", "🥗", "Sağlıklı beslenme planları oluşturarak yaşam kalitesini artırır."),
                      ("Fizyoterapist", "🏃", "Hareket kabiliyetini yeniden kazandırır."),
                      ("Polis", "👮", "Toplum güvenliğini sağlar ve huzuru korur.")],
        "soru": "Topluma en çok nasıl katkı sağlamak istersin?"},
    6: {"baslik": "Yaz ve Kariyer Planı", "tanim": "Yaz tatili kariyer keşfi için harika bir fırsat!",
        "meslekler": [("Deniz Biyoloğu", "🐠", "Deniz ekosistemini araştırır ve korur."),
                      ("Arıcı", "🐝", "Doğanın dengesini koruyarak bal üretir."),
                      ("Turist Rehberi", "🗺️", "Kültürel mirası tanıtarak insanları bilgilendirir."),
                      ("Fotoğrafçı", "📸", "Anları ölümsüzleştirir, hikayeleri görselleştirir.")],
        "soru": "Yaz tatilinde bir mesleği yakından tanımak için ne yapabilirsin?"},
}

# ── P21: Stres Yönetimi & Nefes ──
_BULTEN_STRES = {
    9: {"baslik": "Okula Başlama Stresi", "bilgi": "Yeni ortam ve değişiklikler stres yaratabilir. Bu doğaldır.",
        "nefes": "4-7-8 Tekniği: 4 saniye nefes al, 7 saniye tut, 8 saniye yavaşça ver.",
        "teknikler": ["Derin karın nefesi al — göbeğinin şişip indiğini hisset",
                      "Gözlerini kapat ve güvenli bir yeri hayal et",
                      "Ellerini yumruk yap, 5 saniye sık, bırak — kaslarının gevşemesini hisset",
                      "Sevdiğin bir şarkıyı içinden söyle"]},
    10: {"baslik": "Sınav Kaygısı", "bilgi": "Sınav kaygısı performansı düşürür. Doğru tekniklerle yönetilebilir.",
         "nefes": "Kare Nefes: 4sn nefes al → 4sn tut → 4sn ver → 4sn bekle. 4 kez tekrarla.",
         "teknikler": ["Sınavdan önce gece iyi uyu — en az 8 saat",
                       "Sınavda ilk önce kolay soruları çöz",
                       "Derin nefes al, omuzlarını gevşet",
                       "Olumsuz düşünceleri fark et ve 'Ben yapabilirim' ile değiştir"]},
    11: {"baslik": "Arkadaşlık Sorunları", "bilgi": "Arkadaşlık ilişkilerindeki sorunlar duygusal stres yaratır.",
         "nefes": "Balon Nefes: Karnında bir balon var gibi düşün. Nefes alınca şişir, verince söndür.",
         "teknikler": ["Duygularını tanı: 'Şu an ne hissediyorum?' diye sor",
                       "Güvendiğin bir yetişkinle konuş",
                       "Günlük tut — duygularını yazarak ifade et",
                       "Fiziksel aktivite yap — koşu, dans, yürüyüş"]},
    12: {"baslik": "Tatil Öncesi Stres", "bilgi": "Yılsonu ve tatil dönemi hem heyecan hem stres getirir.",
         "nefes": "Arı Nefesi: Nefes verirken ağzı kapatıp 'hmmmm' sesi çıkar. Titreşimi hisset.",
         "teknikler": ["Yapılacaklar listesi hazırla — kontrol hissi strese iyi gelir",
                       "Her gün 10 dakika sessizce otur",
                       "Sevdiğin bir hobiye zaman ayır",
                       "Ailenle kaliteli vakit geçir"]},
    1: {"baslik": "Yeni Yıl Motivasyonu", "bilgi": "Yeni yıl hedefleri motivasyon kaynağıdır ama baskı da yaratabilir.",
        "nefes": "Deniz Dalgası Nefesi: Nefes al — dalga kıyıya gelir. Nefes ver — dalga geri çekilir.",
        "teknikler": ["Küçük, ulaşılabilir hedefler koy",
                      "Her başarını kutla — ne kadar küçük olursa olsun",
                      "Kendini başkalarıyla kıyaslama",
                      "Günde 5 dakika meditasyon yap"]},
    2: {"baslik": "Performans Baskısı", "bilgi": "Başarı baskısı sağlıklı sınırlar içinde tutulmalıdır.",
        "nefes": "Mum Nefes: Bir mum hayal et. Nefes verirken alevi yavaşça sallamak ister gibi üfle.",
        "teknikler": ["Not = değer değil. Sen notlarından daha fazlasısın",
                      "Hata yapmak öğrenmenin bir parçasıdır",
                      "Mükemmeliyetçilik yerine 'yeterince iyi' de tamam",
                      "Zor hissettiğinde 3 şeyi gör, 2 şeyi duy, 1 şeye dokun"]},
    3: {"baslik": "Bahar Yorgunluğu", "bilgi": "Mevsim geçişlerinde beden ve zihin yorulabilir.",
        "nefes": "Çiçek Nefes: Bir çiçeği kokluyormuş gibi nefes al, sonra yavaşça ver.",
        "teknikler": ["Bol su iç ve taze meyve ye",
                      "Açık havada günde en az 30 dakika geçir",
                      "Uyku düzenini koru — her gün aynı saatte uyu",
                      "Sevdiğin bir arkadaşınla vakit geçir"]},
    4: {"baslik": "Değişim ve Uyum", "bilgi": "Hayattaki değişimlere uyum sağlamak stres yaratabilir ama güçlendirir.",
        "nefes": "Eller Nefes: Bir elin parmaklarını diğer elinle takip et. Yukarı çıkarken nefes al, inerken ver.",
        "teknikler": ["Değişimi bir tehdit değil, fırsat olarak gör",
                      "Kontrol edemediğin şeyleri kabul et",
                      "Güçlü yönlerini hatırla — daha önce neler başardın?",
                      "Doğada yürüyüş yap — doğa stres hormonlarını düşürür"]},
    5: {"baslik": "Yılsonu Stresi", "bilgi": "Sınavlar ve değerlendirmeler yoğun stres kaynağıdır.",
        "nefes": "Gökkuşağı Nefes: Her nefeste bir renk hayal et. 7 nefeste gökkuşağını tamamla.",
        "teknikler": ["Çalışma planı yap — son dakikaya bırakma",
                      "45 dakika çalış, 15 dakika mola ver",
                      "Mola zamanlarında ekrandan uzak dur",
                      "Başarılarını not et — motivasyonunu koru"]},
    6: {"baslik": "Tatile Hazırlık", "bilgi": "Yılın sona ermesi ve tatilin başlaması karışık duygular uyandırır.",
        "nefes": "Güneş Nefes: Güneşi içine çekiyormuş gibi nefes al, sıcaklığı hisset, yavaşça ver.",
        "teknikler": ["Bu yıl öğrendiklerini bir kağıda yaz",
                      "Arkadaşlarınla güzel anıları paylaş",
                      "Yaz için eğlenceli bir plan yap",
                      "Kendini ödüllendir — harika bir yıl geçirdin!"]},
}

# ── P22: İletişim Becerileri ──
_BULTEN_ILETISIM = {
    9: {"baslik": "Tanisma ve Ilk Izlenim",
        "senaryo": "Yeni sinifinda henuz kimseyi tanimiyorsun. Ilk gun cok heyecanli ve biraz da tedirginsin. Yanindaki sirada oturan cocuk da yeni gorunuyor ve o da kimseyle konusmuyor. Ikiniiz de birbirinize bakiyorsunuz ama konusmaya cesaret edemiyorsunuz.",
        "dogru": "Gulumse, goz temasi kur ve 'Merhaba, ben ... Senin adin ne?' de. Ortak ilgi alanlari bul: 'Hangi dersi en cok seviyorsun?' veya 'Teneffuste ne yapmak istersin?' gibi sorularla sohbeti baslat. Ilk adimi atan kisi genellikle en cok arkaadas edinendir.",
        "ipuclari": ["Goz temasi kurmak guven verir ve samimiyetini gosterir", "Karsindakinin adini kullan — 'Merhaba Ali!' demek onu ozel hissettirir", "Aktif dinle: basini salla, 'Hmm, anliyorum' de ve ilgi goster", "Konuyu karsindakine de sor: 'Sen ne dersin?' diyerek sohbeti iki yonlu yap", "Gulmeseme en evrensel iletisim aracidir — hic tanimadigin birini bile rahatlatir", "Ortak noktalar bul: ayni okul, ayni mahalle, ayni hobi"]},
    10: {"baslik": "Hayir Demeyi Ogrenmek",
         "senaryo": "Arkadasin senden odevini yapmanini istiyor. Daha once de birkaac kez boyle isteklerde bulundu ve sen her seferinde evet dedin. Simdi hayir demek istiyorsun ama kirmak da istemiyorsun. Eger hayir dersen arkadasligginizin bozulacagindan endise ediyorsun.",
         "dogru": "'Sana yardim etmek isterim ama odevini senin yapman gerekiyor, cunku ancak boylece ogrenebilirsin. Birlikte calisabiliriz, sana zor yerlerde yardimci olurum.' de. Sinirlarini korumak saglikli iliskilerin temelidir ve gercek arkadaslar senin sinirlarrina saygi duyar.",
         "ipuclari": ["'Hayir' demek kotu bir sey degildir; aksine saglikli sinirlarin ifadesidir", "Nazik ama kararli ol — ses tonun yumusak, sozlerin net olsun", "Alternatif sun: 'Bunu yapamam ama sunu yapabilirim' diyerek kapiyi tamamen kapatma", "Duygularini 'Ben' diliyle ifade et: 'Kendimi kullaniilmis hissediyorum' yerine 'Ben de kendi odevlerimi yetistirmek zorundayim'", "Hayir dedikten sonra sucluluk duymak normal ama zamanla kolaylasir", "Gercek arkadaslik karsilikli saygiya dayanir; seni kullaanan biri gercek arkadas degildir"]},
    11: {"baslik": "Empatiyle Dinleme",
         "senaryo": "Arkadasin uzgun gorunuyor ve sana derdini anlatmaya basliyor. Ailesiyle sorunlar yasiyor ve gozleri dolu. Sen onu dinlemek istiyorsun ama ne soyleyecegini bilmiyorsun. Aklina hemen cozum onerileri geliyor ama arkadasin sadece konusmak istiyor gibi gorunuyor.",
         "dogru": "Telefonunu birak, goz temasi kur, sozunu kesme ve 'Seni anliyorum, bu cok zor olmali' de. Hemen cozum sunma; bazen insanlar sadece dinlenmek ve anlasilmak ister. Arkadasin konusmasini bitiridikten sonra 'Sana nasil yardimci olabilirim?' diye sor.",
         "ipuclari": ["Cozum sunmadan once dinle — cogu zaman insanlar tavsiye degil anlayis arar", "Duygularini yansit: 'Cok uzulmus olmailisin' diyerek duygularini onayala", "Yargilama — sadece orada ol ve guvenli bir alan olustur", "Fiziksel olarak karsina don ve bedeninle ilgini goster", "Kendi deneyimlerinle karsilastirma yapma — 'Benim basima da geldi' demek bazen kucumseme gibi alginlanir", "Gizliligine saygi goster — anlattiklariini baskalariyla paylasmayacagini belli et"]},
    12: {"baslik": "Tesekkur ve Takdir",
         "senaryo": "Ogretmenin sana yilboyu cok yardimci oldu. Matematikte zorlaniiyordun ve o ekstra zaman ayirarak sana anlatti. Simdi yil sonu yaklasirken ona tesekkur etmek istiyorsun ama nasil yapacagini bilmiyorsun. Sozlu olarak soylemeye cekiniyorsun.",
         "dogru": "Samimi bir tesekkur karti yaz. Spesifik ol: 'Matematikte sabirla anlattiginiz icin cok tesekkur ederim. Sizin sayenizde artik kesirlerden korkmuyorum.' Genel bir 'tesekkurler' yerine somut ornekler vermek tesekkkurun samimiyetini ve degerini katlar.",
         "ipuclari": ["Spesifik tesekkur daha anlamlidir — 'Sabirla anlattiginiz icin' demek 'Tesekkurler' demekten cok daha etkilidir", "Yazili tesekkur kalicidir ve karsindaki kisi onu tekrar tekrar okuyabilir", "Goz temasiyla soyle — bakislarin samimiyetini gosterir", "Hediye degil samimiyet onemli — el yazisi bir not pahali bir hediyeden degerlidir", "Tesekkuru erteleme — aninda ifade etmek daha guclu bir etki birakir", "Tesekkur etmek sadece karsindakini degil, seni de mutlu eder"]},
    1: {"baslik": "Catisma Cozme",
        "senaryo": "Iki arkadasin kavga etti ve ikisi de senden taraf tutmanizi istiyorlar. Her ikisi de kendi haklai oldugunu iddia ediyor ve senin desteginizi bekliyor. Taraf tutarsan digerini kaybedeceksin, tutmazzsan ikisi de sana kiziyor. Cok zor bir durumdasin.",
        "dogru": "Taraf tutma. Her iki tarafi da ayri ayri dinle ve duygulairnii anladigini goster. 'Ikinizi de anliyorum, birlikte cozum bulalim' de. Arabulucu rolu ustlenerek her iki tarafin da ihtiyaclarini dinle ve ortak bir nokta bulmalarına yardimci ol. Uzlasma herkesin kazandigi bir cozumdur.",
        "ipuclari": ["Sakin ol — ofkeyle karar verme, bir adim geri cekil", "Her iki tarafi da dinle — hikayenin her zaman iki tarafi vardir", "'Ben' dili kullan: 'Ben soyle hissediyorum' diyerek duygularii ifade et", "Uzlasma ara — ikisi de kazansin; kaybet-kazan degil kazan-kazan hedefle", "Catisma sirasinda ses tonuna dikkat et — sakin ve duuk tonlu konusmak tansiyonu dusurur", "Gerekirse bir yetiskinden yardim iste — bazi catismalar cocuklarin cozebileceginin otesindedir"]},
    2: {"baslik": "Ozur Dileme Sanati",
        "senaryo": "Arkadasina kirici bir sey soyledin ve artik pismansin. O anda sinirliiydin ve aaginzdan kacan sozler onu derinden inciitti. Arkadasin senden uzaklast ve seninle konusmak istemiyor. Ozur dilemek istiyorsun ama reddedilmekten korkuyorsun.",
        "dogru": "Goz temasiyla, samimi bir sekilde 'Sana soyledigim sey yanlisti, ozur dilerim. Seni incitmek istemedim. O anda sinirliydi ve kontrlumu kaybettim, bu bir bahane degil ama sebebini aciklamak istiyorum.' de. Ozur diledikten sonra karsindakine zaman ver — affetme ani onun kararidir.",
        "ipuclari": ["Samimi ozur kisa ve nettir — uzun aciklamalar bazen bahane gibi algilanir", "Bahane uydurma — 'Ama sen de...' diye baslamak ozrun samimiyetini yok eder", "'Ama' kelimesinden kacin — 'Ozur dilerim ama...' demek aslinda ozur dilememek demektir", "Davranisini degistirecegini goster — sozler degil eylemler samimiyeti kanitlar", "Ozru uygun zamanda dile — kalabalik icinde degil, basbasa kaldiginda", "Karsi tarfin ozrunu kabul etmeme hakkina saygi goster — bazi yaralar zaman alir"]},
    3: {"baslik": "Beden Dili",
        "senaryo": "Sinifta sunum yapacaksin ve cok heyecanlisin. Ellerin titriyor, sesin titreyecek diye endiseleniyorsun ve sinifin onune cikmak istemiyorsun. Konunu iyi biliyorsun ama beden dilinin seni ele vereceginden korkuyorsun.",
        "dogru": "Dik dur, omuzlarini ac, goz temasi kur ve ellerini dogal hareketlerle kullan ama abartma. Sunum oncesi 3 derin nefes al, omuzlarini geriye cek ve gulumsemeye basla. Heyecani enerji olarak kullan — bedennin harekeli zihninin rahatlamasina yardimci olur.",
        "ipuclari": ["Kollarini kavusturma — kapalilik ve savunmacilik ifade eder", "Gulumse — karsindakini rahatlatir ve kendin de daha iyi hissedersin", "Yavas ve net konus — hizli konusmak heyecani arttirir", "Derin nefes al — heyecanini yonet, burun ndan 4 say nefes al, agizdan 6 say ver", "Goz temasini dagiit — sadece bir kisiye degil tum sinifa bak", "Eller cebinde olmamali — acik eller guven ve samimiyet ifade eder"]},
    4: {"baslik": "Dijital Iletisim",
        "senaryo": "Mesajlasirken arkadasina bir sey yazdin ama o yanlis anladi ve cok uzuldu. Espri olarak yazdigin cuumle, karsi tarafta kirici olarak algiillandi. Arkadasin sana kizmis mesajlar atiyor ve sen ne olduguunu anlayamadin.",
        "dogru": "Yazili mesajda ton ve mimik kaybolur, bu nedenle yanlis anlasailmalar cok yayginidr. 'Yanlis anlasilma olmus, kastettigim suydu...' diye hemen acikla. Mumkunse konuyu yuzyuze veya sesli arama ile coz cunku yazili iletisimde duygualar net aktarilamaz.",
        "ipuclari": ["Emoji ve ton belirtici kullan — yazi tonunu belli etmeye yardimci olur", "Onemli konulari yuzyuze konus — hassas meseleleri mesajla cozmeye calisma", "Mesaji gondermeden once tekrar oku — karsi taraf bunu nasil anlayabilir diye dusun", "BUYUK HARF = bagirmak demektir — tamami buyuk harfle yazma", "Sinirli olduguunda mesaj yazma — soguduktan sonra yaz", "Grup mesajlarinda dikkatli ol — herkesin gorebilecegi sey herkesi etkileyebilir"]},
    5: {"baslik": "Sunum Yapma",
        "senaryo": "Sinifta proje sunumu yapacaksin. Konun ilginc ama nasil anlatacagini bilmiyorsun. Arkadaslarin profesyonel sunumlar hazirliyorlar ve sen geride kalmak istemiyorsun. Hem icerigin hem de sunumun etkileyici olmasi gerekiyor.",
        "dogru": "Konunu iyi bil ve 3 ana mesaja odaklan. Anahtar noktalari kucuk kartlara not al ama ezberden okuma. Gorseller kullan — grafik, resim, kisa video. Aynada veya aile onunde en az 2 kez prova yap. Zamanlamaya dikkat et ve soruulara hazirlikli ol.",
        "ipuclari": ["Aynada prova yap — beden dilini ve mimiklerini gormeni saglar", "3 ana mesajina odaklan — her seyi anlatmaya calismak yerine onemli noktalari vurgula", "Sorulari onceden tahmin et — olasi sorulara cevap hazirla", "Heyecan = enerji, onu kullan! — heyecan kotu degildir, onu performans enerjisine donustur", "Sunuma bir soru veya ilginc bir bilgiyle basla — dikkati hemen cek", "Son cumlen akilda kalici olsun — dinleyicilere bir mesaj birak"]},
    6: {"baslik": "Vedalasma",
        "senaryo": "Yil sonu geldi ve bazi arkadaslarinla farkli okullara gideceksiniz. Yillaridir birlikte oldugunnuz insanlarla ayrilmak seni uzuyor. Son gunlerde herkes biraz dalgiin ve huzunlu. Bazi arkadaslarin vedaalasmaaktan kaciniyor cunku duygularniyla yuzlesmek istemiyorlar.",
        "dogru": "Guzel anilari paylas, iletisim bilgilerinii al ve vedalasirken duygulariini acikca ifade et. 'Seni cok ozleyecegim, birlikte gecirdigimiz zamanlar benim icin cok degerli' demek hem seni hem de arkadasini rahatlatir. Vedalassmak zordur ama her son yeni bir baslangiicin kapisini acar.",
        "ipuclari": ["Duygularini bastirma — vedalasmaak uzulebilir ve bu tamamen normaldir", "Iletisimi surdurme plani yap — telefon, mesaj, sosyal medya ile baglanti kurun", "Guzel bir hatira olustur — birlikte fotograf cekin, ani defteri hazirlayin", "Yeni baslangiclara acik ol — vedalassmak kayip degil, buyumenin bir parcasidir", "Arkadaslarina onlar icin ne kadar degerli olduklarini soylemekten cekinme", "Gelecekte tekrar bulusmak icin plan yapin — umut vedanin ilaciidr"]},
}

# ── P23: Zaman Yönetimi ──
_BULTEN_ZAMAN = {
    9: {"baslik": "Haftalık Program", "matris": [("Acil+Önemli", "🔴", "Hemen yap! Yarınki sınav, ödev teslimi"),
        ("Önemli+Acil Değil", "🟡", "Planla: Proje, spor, kitap okuma"),
        ("Acil+Önemli Değil", "🟠", "Delege et veya hızla bitir"),
        ("Ne Acil Ne Önemli", "⚪", "Ertele veya iptal et")],
        "ipucu": "Her Pazar akşamı haftalık planını yap. Önce önemli olanları yerleştir."},
    10: {"baslik": "Pomodoro Tekniği", "matris": [("25 dk Çalış", "🍅", "Tam konsantrasyonla çalış"),
         ("5 dk Mola", "☕", "Kısa ara: su iç, gerin"),
         ("4 Pomodoro = Büyük Mola", "🎮", "15-30 dk uzun ara"),
         ("Günde 8-10 Pomodoro", "🎯", "Verimli bir gün demektir")],
         "ipucu": "Telefonu sessize al, bildirimleri kapat, zamanlayıcı kur."},
    11: {"baslik": "Erteleme ile Mücadele", "matris": [("2 Dakika Kuralı", "⚡", "2 dk'dan kısa iş? Hemen yap!"),
         ("Parçalara Böl", "✂️", "Büyük görevi küçük adımlara ayır"),
         ("İlk Adım", "👣", "Sadece başla — motivasyon hareketle gelir"),
         ("Ödül Sistemi", "🎁", "Her tamamlanan görev için kendini ödüllendir")],
         "ipucu": "'Şimdi değilse ne zaman?' sorusu ertelemeyi yenmenin anahtarıdır."},
    12: {"baslik": "Sınav Takvimi", "matris": [("4 Hafta Önce", "📅", "Konuları listele, plan yap"),
         ("2 Hafta Önce", "📝", "Aktif tekrar, özet çıkar"),
         ("1 Hafta Önce", "🔄", "Deneme sınavı çöz, eksikleri tamamla"),
         ("Son Gece", "😴", "Tekrar yok! Erken uyu, güzel kahvaltı yap")],
         "ipucu": "Son dakika çalışması hafızayı zayıflatır. Planlı çalışma kalıcı öğrenme sağlar."},
    1: {"baslik": "Yeni Yıl Planlaması", "matris": [("Yıllık Hedef", "🎯", "3-5 büyük hedef belirle"),
        ("Aylık Plan", "📋", "Her ay bir hedefi küçük adımlara böl"),
        ("Haftalık Kontrol", "✅", "Her hafta ilerlemeyi değerlendir"),
        ("Günlük Rutin", "⏰", "Sabah rutini, çalışma, mola, hobi")],
        "ipucu": "SMART hedefler koy: Spesifik, Ölçülebilir, Ulaşılabilir, İlgili, Zamanlı."},
    2: {"baslik": "Konsantrasyon", "matris": [("Sessiz Ortam", "🤫", "Dikkat dağıtıcıları uzaklaştır"),
        ("Tek İş", "🎯", "Multitasking verimsizdir — tek işe odaklan"),
        ("Mola Zamanı", "⏸️", "Beyni dinlendir — 45dk+15dk kuralı"),
        ("Uyku", "💤", "8 saat uyku konsantrasyonun temelidir")],
        "ipucu": "Çalışma masanda sadece o dersin malzemeleri olsun. Diğer her şeyi kaldır."},
    3: {"baslik": "Önceliklendirme", "matris": [("A Listesi", "🔴", "Bugün yapılmalı — en fazla 3 madde"),
        ("B Listesi", "🟡", "Bu hafta yapılmalı"),
        ("C Listesi", "🟢", "Bu ay yapılabilir"),
        ("D Listesi", "⚪", "Yapmayabilirim — iptal et")],
        "ipucu": "Her sabah 'Bugün en önemli 3 şey ne?' sorusuyla güne başla."},
    4: {"baslik": "Verimli Çalışma", "matris": [("Aktif Tekrar", "🧠", "Oku, kapat, hatırla — ezber değil anlam"),
        ("Feynman Tekniği", "👨‍🏫", "Konuyu birine anlatıyormuş gibi özetle"),
        ("Çıktı Odaklı", "📊", "Soru çöz, özet yaz, şema çiz"),
        ("Aralıklı Tekrar", "📆", "Bugün öğren, yarın tekrar, 1 hafta sonra yine")],
        "ipucu": "Sadece okumak ≠ çalışmak. Aktif olarak bilgiyi işle, uygula, test et."},
    5: {"baslik": "Sınava Hazırlık", "matris": [("Konu Haritası", "🗺️", "Tüm konuları bir sayfaya çiz"),
        ("Zayıf Konular", "🎯", "Önce en zor konulara odaklan"),
        ("Deneme Sınavı", "📝", "Gerçek sınav koşullarında prova yap"),
        ("Dinlenme", "🧘", "Beyin dinlenmeden öğrenemez — molalar şart")],
        "ipucu": "Sınavdan önceki gece çalışma. Beyni dinlendir, erken uyu, güzel kahvaltı yap."},
    6: {"baslik": "Yaz Planı", "matris": [("Okuma", "📚", "Her hafta en az 1 kitap — liste hazırla"),
        ("Hobi", "🎨", "Yeni bir beceri öğren — müzik, spor, kodlama"),
        ("Gezi", "🏕️", "Doğa ve kültür gezileri plan"),
        ("Dinlenme", "😎", "Gerçek dinlenme — ekransız zamanlar")],
        "ipucu": "Tatil = tembellik değil. Okulda yapamadığın şeyleri yapma fırsatı!"},
}

# ── P24: Empati & Farkındalık ──
_BULTEN_EMPATI = {
    9: {"baslik": "Yeni Arkadasini Anla",
        "hikaye": "Mehmet yeni okuluna geldi ve kimseyi tanimiyor. Ailesi baska bir sehirden tasinmis ve Mehmet eski arkadaslarini, okulunu ve mahallesini cok ozluyor. Teneffuste tek basina oturuyor, kimseyle goz temasi kurmuyor ve ogle yemegini yalniz yiyor. Siniftaki diger cocuklar kendi gruplarinda egleniyor ama kimse Mehmet'e yaklasmiyor.",
        "dusunce": "Herkes bir zamanlar 'yeni' oldu ve o ilk gunlerin ne kadar zor oldugunu hatirlayin. Yalnizlik hissi cocuklarda derin izler birakabilir. Bir gulumseme ve 'Gel bizimle oyna!' cumlesi hayat degistirebilir. Arastirmalar, yeni ogrencilere ilk hafta yaklasan cocuklarin kendilerinin de sosyal becerilerinde belirgin gelisim gosterdigini ortaya koymustur.",
        "aktivite": "Bu hafta sinifinda yalniz oturan birine gidip tanis. Onunla ogle yemegi ye veya teneffuste birlikte oynayin. Nasil hissettigini gunlugune yaz.",
        "tartisma": ["Yeni bir yere gittiginde nasil hissedersin?", "Birisi sana yaklasip 'Merhaba' dese ne hissedersin?", "Yalniz birine yaklasmaak neden bazen cesaret ister?", "Sinifta herkesin kendini ait hissetmesi icin ne yapilabilir?"],
        "rol_oyunu": "Sinifta ikili olun. Biri 'yeni ogrenci', digeri 'eski ogrenci' rolunde olsun. Yeni ogrenci nasil hissediyor? Eski ogrenci ona nasil yaklasabilir? Rolleri degistirin ve her iki tarafi da deneyimleyin."},
    10: {"baslik": "Farkliliklara Saygi",
         "hikaye": "Sinifiniza tekerlekli sandalye kullanan Elif adinda bir ogrenci geldi. Elif cok akilli ve esnprituel bir cocuk ama bazi sinif arkadaslari onunla dalga geciyor, bazi arkadaslari ise 'kirar miyim' diye korktuklari icin ondan uzak duruyor. Elif teneffuslerde yalniz kaliyor ve sinifta giderek daha sessiz oluyor. Aslinda Elif futbol sohbetlerini cok seviyor ve satranc sampiyonu.",
         "dusunce": "Herkes essizdir ve degerlidir. Farkliliklar toplumu ve bizi zenginlestirir. Empati, kendini onun yerine koymak demektir: tekerlekli sandalyede olsan ve kimse seninle konusmasa nasil hissederdin? Engel, bir insanin kim oldugunu belirlemez; sadece bazi seyleri farkli sekilde yaptigini gosterir. Gercek guc, farkliliklari kutlayabilmektir.",
         "aktivite": "Bu hafta her gun farkli bir arkadasina samimi bir iltifat et. Iltifatlarin dis gorunusle degil, karakter ozellikleriyle ilgili olsun: 'Cok iyi dinliyorsun', 'Esprilerin harika', 'Cok dusunceli birisin'. Tepkilerini gozlemle ve gunlugune yaz.",
         "tartisma": ["Farklilik ne demektir? Hepimiz bir sekilde farkli degil miyiz?", "Dalga gecmenin karsi tarafta biraktigi iz ne olabilir?", "Engelli bir arkadasinla nasil iletisim kurabilirsin?", "Sinifta herkesin esit hissetmesi icin neler yapilabilir?"],
         "rol_oyunu": "Bir gun boyunca gozlerini baglaayarak (guvenli bir ortamda) basit isler yapmayi dene. Gormeden yemek yemeyi, yuruymeyi dene. Bu deneyim sana ne ogretti? Farkli bir bedende yasamak nasil bir sey olurdu?"},
    11: {"baslik": "Duygusal Zeka",
         "hikaye": "Sinif arkadasin Emre her zamanki gibi gulumsuyor ve 'Iyiyim' diyor ama son zamanlarda gozleri uzgun gorunuyor, teneffuslerde daha sessiz ve eskisi kadar enerjik degil. Bir gun ders arasinda Emre'nin gizlice agladigini goruyorsun. Ama o hala 'Bir seyim yok' diyor. Beden dili ve sozleri birbirini tutmuyor.",
         "dusunce": "Beden dili, sozlerden cok daha fazla sey anlatir; iletisimin yuzde doksandan fazlasi sozsuz yollarla gerceklesir. Iyi bir gozlemci olmak, baskalarinin gercek duygularini anlamanin anahtaridir. Duygusal zeka, duygulari tanimak, anlamak ve uygun sekilde yanit vermek demektir. Emre gibi duygularini gizleyen bireine 'Bir seyler farkli gorunuyor, konusmak istersen buradayim' demek en dogru yaklasimdir.",
         "aktivite": "Duygu gunlugu tut: Her gun 3 farkli duygu kaydet, her birini neyin tetikledigini ve bedeninde nasil hissettigini yaz. Bir hafta sonra gunlugune bakarak duygusal oruntullerini kesfet.",
         "tartisma": ["Insanlar neden bazen gercek duygularini gizler?", "Birinin beden dili ile sozleri uyusmazsa hangisine inanmaliyiz?", "Duygusal zeka ogrenilabilir mi? Nasil?", "Zorluuk yasayan birine nasil yaklasmaliyiz?"],
         "rol_oyunu": "Ikili olun. Bir kisi bir duygu canlandirsin (yuz ifadesi ve beden diliyle) ama sozle farkli bir sey soylesin. Digeri gercek duyguyu tahmin etsin. Beden dilini okuma becerinizi gelistirin."},
    12: {"baslik": "Paylasma ve Dayanisma",
         "hikaye": "Kis geldi ve havallar iyice soguddu. Sinifinda Ayse adinda bir arkadasinin kislik montu, botu ve eldiveni olmadigini fark ediyorsun. Ayse her gun ince bir ceketlee geliyor ve teneffuste usudugu icin disari cikmiyur. Diger cocuklar durumu fark etmis ama kimse bir sey soylemiyor. Ayse'nin ailesi maddi zorluklar yasiyor ama Ayse bu durumdan utandiigi icin kimseye soyleyemiyor.",
         "dusunce": "Yardim etmek sadece maddi degildir; bir tebessm, sicak bir soz, birlikte oturma teklifi de buyuk bir yardimdir. Ancak maddi yardim gerektiginde bunu onur kirici olmayan bir sekilde yapmak cok onemlidir. Sinifca organize edilen bir 'kis yardimlasmasi' hem ihtiyaci karsilar hem de kimseyi utandiirmaz. Dayanisma, birlikte guclu olmanin en guzel ifadesidir.",
         "aktivite": "Ailece kullanmadiginiz temiz kiyafetleri toplayin ve ihtiyac sahiplerine ulastirin. Okulda bir 'Dayanisma Gunuu' duzenlenmesini onerin. Ayrica bu hafta birine beklenmedik bir iyilik yapin ve nasil hissettiginiizi kaydedin.",
         "tartisma": ["Yardim etmek ile aciimak arasindaki fark nedir?", "Birinin ihtiyaci oldugunu fark ettiginde nasil yaklasabilirsin?", "Yardimi onur kirici olmadan nasil sunabiliriz?", "Kucuk iyilikler buyuk farklar yaratabilir mi? Ornekler ver."],
         "rol_oyunu": "Sinifca bir senaryo canlandirin: Bir ogrencinin ihtiyaci var ama utandigi icin soyleyemiyor. Sinif bunu nasil fark eder ve nasil yardim eder? Farkli yaklasim senaryolrini deneyin ve en etkili olani tartissin."},
    1: {"baslik": "Kendine Empati",
        "hikaye": "Sinavdan kotu not aldin. Cok calismistin ama sonuc bekledigin gibi cikmadi. Kendini cok kotu hissediyorsun ve icinden 'Ben aptalim, hic bir sey beceremiyorum' gibi dusunceler geciyor. Arkadaslarin iyi notlar almis ve sen onlarla karsilastirarak kendini daha da kotu hissediyorsun. Eve gitmek bile istemiyorsun.",
        "dusunce": "Kendine bir arkadasina davrandigin gibi davran. Eger en yakin arkadasin ayni durumda olsa ona ne soylerdin? Muhtemelen 'Herkes hata yapabilir, bir dahakiine daha iyi olacak, sen zeki birisin' derdin. Peki neden kendine boyle soylemiyorsun? Oz sefkat, zayiflik degil guc isaretidir. Kendinle konusma bicimini degistirmek oz guveni yeniden insa etmenin ilk adiimidir.",
        "aktivite": "Aynaya bak ve kendine 3 guzel sey soyle: 'Ben degerli bir insanim', 'Hata yapmak ogrenmenin parcasidir', 'Kendimi seviyorum'. Bunu 1 hafta boyunca her sabah tekrarla. Hafta sonunda kendine karsi tutumunun nasil degistigini gunlugune yaz.",
        "tartisma": ["Kendimize neden baskalarina davrandiigimizdan daha sert davraniiriz?", "Oz sefkat ile oz acima arasindaki fark nedir?", "Hata yapmak basarisizlik midir yoksa ogrenme firsati mi?", "Olumsuz ic konusmamizi nasil degistirebiliriz?"],
        "rol_oyunu": "Ikili olun. Bir kisi 'ic elestirmen' rolunde olumsuz seyler soylesin, digeri 'ic destekci' olarak her olumsuz dusunceye olumlu bir yanitl versin. Rolleri degistirin. Hangi ses daha guclu?"},
    2: {"baslik": "Sevgi ve Saygi",
        "hikaye": "14 Subat yaklassiyor ve sinifta herkes birbirine kart aliyor. Ama sinifinizda Ali adinda bir cocuk var, kimse ona kart vermiyor cunku o biraz farkli: sessiz, icine kappanik ve populer gruplara dahil degil. Ali bunu fark ediyor ve her gecen gun daha da uzuluyor. Aslinda Ali cok yetenekli bir ressam ve harika hikayeler yaziyor ama bunu kimse bilmiyor.",
        "dusunce": "Sevgi sadece romantik degildir. Arkadaslik, aile, dostluk — hepsi sevgidir ve her insan sevilmeyi hak eder. Populer olmak sevgiyi hak etmenin olcutu degildri. Herkes degerlidir ve her insaanda kesfedilmeyi bekleyen guzellikler vardir. Bazen en sessiz insanlar en derin dunyalara sahiptir; tek gereken onlara bir sans vermektir.",
        "aktivite": "Siniftaki herkese kucuk bir tesekkur notu yaz — isimleriyle ve spesifik bir ozelliklerini vurgulayarak. Herkes degerli hissetsin. Ozellikle sessiz ve icine kapanik arkadaslarima ekstra dikkat goster.",
        "tartisma": ["Sevgi sadece soylenmekle mi gosterilir?", "Populer olmak sevilmek anlamina gelir mi?", "Her insanda kesfedilmeyi bekleyen guzellikler var mi? Ornekler ver.", "Sinifta herkesin dahil hissetmesi icin neler yapilabliir?"],
        "rol_oyunu": "Sinifta bir 'Gizli Arkadas' haftasi baslatin. Herkes kura ile bir sinif arkadasi ceksin ve 1 hafta boyunca ona kucuk iyilikler yapsin (not birakma, yardim etme). Hafta sonunda gizli arkadaslar aciklansin."},
    3: {"baslik": "Dogaya Empati",
        "hikaye": "Parkta yururken coplerin icinde yasaamaya calisan bir kedi gorduun. Kedi zayif ve hastali gorunuyor, biri tarafindan terk edilmis olmali. Yanindan gecen insanlarin cogu onu gormezden geliyor. Bazi cocuklar onu korkutarak egleniyor. Kedi senden korkuyor ama ayni zamanda yardim bekler gibi bakiiyor.",
        "dusunce": "Empati sadece insanlara degil, tum canlilara karsi duyulur. Doga bizim evimiz ve icindeki her canli bizim sorumlulugumuz altindadir. Hayvanlara karsi gosterilen merhamet, insanlara karsi gosterilecek empaatniin temelini olusturur. Arastirmalar, hayvanlara karsi duyarli yetisen cocuklarin yetiskinlikte daha empatik ve sosyal olduklarini gostermiistir. Bir canliyin acisini gormezden gelmek, empati kasimizi zayiflatir.",
        "aktivite": "Bir hafta boyunca cevrendeki canliilari gozlemle: kuslari, bocekleri, sokak hayvanlarini, bitkileri. Her gun bir gozlemini kaydet. Onlar icin ne yapabileceginii dusun: su kabii birakmak, cop toplamak, cicek dikmek gibi kucuk adimlar at.",
        "tartisma": ["Hayvanlar duygu hisseder mi? Bunu nasil anlaariz?", "Insanlarin hayvanlara karsi sorumlulugu nedir?", "Cevre kirliligi hayvanlari nasil etkiler?", "Bir canliiya yardim etmek seni nasil hissettiirir?"],
        "rol_oyunu": "Sinifta bir 'Hayvanin Sesi' etkinligi yapin. Her ogrenci bir hayvan secsin ve o hayvanin gozunden dunya nasil gorunuyor onu anlaitsin. Insanlara ne soylemek isterdi? Bu etkinlik hayvanlara empati kurmamizi guclendirir."},
    4: {"baslik": "Onyargilari Kirmak",
        "hikaye": "Sinifiniiza Diyarbakirdan gelen Hasan adinda yeni bir ogrenci geldi. Hasan Turkce'yi farkli bir agivzle konusuyor ve bazen sozcukleri farkli telaffuz ediyor. Bazi sinif arkadaslari onun konusma tarziiyla dalga gecmeye basladi ve 'O bizden farkli' diyerek onu dislamaaya basladilar. Aslinda Hasan muhtesem bir futbolcu ve cok iyi ney ufluyor ama kimse onu tanimaya firsat vermiyor.",
        "dusunce": "Birini tanimadan yargilamak adaletsizliktir ve cogu zaman onyargilaarimiz gercegi yansitmaz. Herkese bir sans vermek hem bizim hem de onlarin hayatini zenginlestiirir. Turkiye 81 ile sahip zengin bir ulkedir ve her bolgenin kendine ozgu kulturel zenginlikleri vardir. Farkli agizlar, gelenekler ve yemekler ulkemizin kulturel hazinesidir. Onyargiilar bilgisizlikten dogar; tanimak onyargiyi yener.",
        "aktivite": "Farkli bir sehirden veya kulturden birini bul ve onunla sohhbet et. Nereden geldigini, orada hayatin nasil oldugunu, neleri sevdigini sor. Ogrendiklerini sinifla paylas. Ayrica kendi onyargilarini dusun: hakkinda yanlis dusundugun biri oldu mu?",
        "tartisma": ["Onyargi nedir ve nasil olusur?", "Birini tanimadan yargilamak adil midir?", "Farkli kulturlerden insanlarla tanismak bize ne kazandirir?", "Kendi onyargilaarimizin farkina nasil varabiliriz?"],
        "rol_oyunu": "Sinifta 'Yargisiz Gozlem' oyunu oynaayin. Ogretmen farkli kiyafet ve aksesuarlarla sinifa 3 'misafir' davet etsin (ogretmenler veya gonulluler). Ogrenciler ilk izlenimlerini yazsin, sonra misafirler kendilerini anlaitsinlar. Ilk izlenimler ne kadar dogru cikti? Bu etkinlik onyargilarin farkindaligini arttirir."},
    5: {"baslik": "Ailene Empati",
        "hikaye": "Akssam eve geldiginde annenin cok yorgun gorunduugunu fark ediyorsun. Butun gun calismis, alisveris yapmis, yemek hazirlamis ve evin islerini halletmis. Ama yine de sana 'Odevini yaptin mi? Ac misin?' diye soruyor. Baban da gec saatlere kadar calismis ve bitkin gorunuyor. Her ikisi de kendi yorgunluklarini bir kenara birakarak senin ihtiyaclaarinla ilgileniyorlar.",
        "dusunce": "Ailemiz bazen en cok ihmal ettigimiz insanlardir cunku onlarin sevgisini ve ozveriisini 'normal' olarak kabul ederiz. Ama bir an dur ve dusun: Ailen senin icin her gun ne kadar fedakarlik yapiyor? Onlari dinlemek, takdir etmek ve kucuk jestlerle sevgini gostermek hem onlari hem de seni mutlu eder. Empati ailede baslar ve ailede gucleniir.",
        "aktivite": "Bu hafta ailene surpiz yap: sabah erkenden kalkip kahvalti hazirla, aksam cay koy, ev islerinde yardim et veya her aile uyesine ozel bir tesekkur karti yaz. Onlarin tepkisini ve senin hislerini gunlugune kaydet.",
        "tartisma": ["Ailen senin icin neleri feda ediyor?", "Ailene en son ne zaman tesekkur ettin?", "Ebeveynlerin de duyguları ve zor gunleri olabilir mi?", "Aile icinde empati nasil gosterilir?"],
        "rol_oyunu": "Bir gun boyunca anne/babanin rolunu oyna: sabah kalk, kahvalti hazirla, evi topla, yemek planla. Bu deeneyim sana ebeveynligin ne kadar emek istedigini gosterecek. Deneyimini ailnle paylas."},
    6: {"baslik": "Veda ve Yeni Baslangiclar",
        "hikaye": "Yil sonu geldi ve bazi arkadaslarin baska okullara gidecek. Yillardir birlikte oldugunnuz, birlikte guldugunuz ve agladiginiz insanlarla ayrilma zamani geldi. Son haftalarda herkes biraz huzunlu; bazi arkadaslarin veda etmekten kaciniyor, bazilari ise asiri neseeli davranarak duygularini gizliyor. Sen de icinden karissik duygular geciyor — uzuntu, endise ama ayni zamanda yeni baslangiclara dair heyecan.",
        "dusunce": "Vedalar zordur ama her son yeni bir baslangiicin kapiisini acar. Anilar kalicidir ve gercek dostluklar mesafeye ragmen sureer. Duygularini bastirmak yerine yasaamak ve ifade etmek saglikli bir veda surecinin anahtaridir. Uzuntu hissetmek, o iliskilerin senin icin degerli oldugunu gosterir. Veda etmek kayip degil, buyumenin ve ilerlemenin dogal bir parcasidir.",
        "aktivite": "Sinifca bir ani defteri hazirlayin: herkes birbirine guzel bir mesaj yazsin, birlikte fotograflar yapisitirin ve en guzel aniilarinizi kaydedin. Bu deftter yillar sonra en degerli hazinelerinizden biri olacak.",
        "tartisma": ["Veda etmek neden zordur?", "Duygularimizi gizlemek mi yoksa ifade etmek mi daha saglikli?", "Uzaklasan arkadaslarla iletisimi nasil surdureebiliriz?", "Her son neden yeni bir baslangicin habercisidir?"],
        "rol_oyunu": "Sinifca bir 'Zaman Kapsulu' haziirlayin. Herkes bu yilin en guzel anisini, bir dilegi ve gelecek yil icin bir hedefi kagida yazsin. Hepsini bir kutuya koyun ve gelecek yil ayni tarihte acin. Farkli okullara gidenler icin fotograflarla dijital bir versiyon da hazirlanabilir."},
}

# ── P25: Kitap Kulübü ──
_BULTEN_KITAP = {
    9: {"kitap": "Kucuk Prens — Antoine de Saint-Exupery",
        "aciklama": "Bir cocugun gozunden buyuklerin dunyasini anlatan zamanisz bir basyapit. Kucuk Prens kendi gezegeninden ayrilarak farkli duyalari kesfeder ve her gezegende farkli bir yetiskin tipiyle karsilasir. Kitap, sevginin, dostlugun ve gercekten gormenin ne demek oldugunu cocuk masumiyetiyle sorgular.",
        "soru": "Kucuk Prens neden gulunu birakip gezegenleri dolasti? Sen olsan ne yapardin? 'Gozle gorulemez, ancak kalple bakinca gorulebilir' cumlesini nasil anliyorsun?",
        "oneri": ["Pollyanna — Eleanor H. Porter: Her durumda olumlu bir sey bulmanin hikayesi", "Charlie'nin Cikolata Fabrikasi — Roald Dahl: Hayal gucu ve iyi kalpli olmanin odulu", "Kralicicelerin Olmadigi Ulke — Sunay Akin: Cocuklarin gozunden farkli bir dunya", "Kardesimin Hikayesi — Zuhal Olgac: Kardes iliskisi ve aile baglari uzerine dokunaklai bir oykuu", "Benim Adim Feridun — Nazli Eray: Cocukluk masumiiyeti ve hayal gucunun gucu"],
        "etkinlik": "Kitabi okuduktan sonra kendi gezeegeninizi hayal edin: Gezegeninizde ne var? Kim yasiyor? Kurallari ne? Bunu resimleyin ve sinifta paylasiin."},
    10: {"kitap": "Seker Portakali — Jose Mauro de Vasconcelos",
         "aciklama": "Yoksulluk icinde buyuyen bes yasindaki Zeze'nin hayal dunyasi ve gerceklikle mucadelesi. Zeze, zorlu yasam kosullarina ragmen muhtesem bir hayal gucuyle basa cikar ve bir portakal agaciyla konusarak ic dunyasini paylassir. Kitap, cocukluk masumiiyeti, acinin donusturucuu gucu ve sevginin iyilestirici etkisini gozler onune serer.",
         "soru": "Zeze neden agaciyla konusuyordu? Hayal gucu bize nasil yardim eder? Zor zamanlarda hayallerin bir siginak olabilecegini dusunuyor musun?",
         "oneri": ["Cocuk Kalbi — Edmondo De Amicis: Okul, dostluk ve insanlik degerleiri uzerine klasik", "Heidi — Johanna Spyri: Doga, masumiiyet ve aile baglari", "Kucuk Kadin — Louisa May Alcott: Dort kiz kardesin buyume ve olgunlasma hikayesi", "Bogartaki Kurt — Cengiz Aytmatov: Doga ve insan iliskisi uzerine derin bir oykuu", "Benim Adim Kirmizi — Orhan Pamuk (gencler icin): Farkli bakis acilarindan anlatiilan bir hikaye"],
         "etkinlik": "Kitabin en etkileyici sahnesini resimleyin veya kisa bir oyun olarak canlandirin. Zeze'ye bir mektup yazin: 'Sevgili Zeze, sana sunu soylemek isterdim...'"},
    11: {"kitap": "Harry Potter ve Felsefe Tasi — J.K. Rowling",
         "aciklama": "Siradan bir cocugun buyuculuk dunyasini kesfi ve cesaret hikayesi. Harry Potter, merdiven altinda yasayan kimsesiz bir cocukken bir gun Hogwarts'tan kabul mektubu alir ve hayati tamamen degisir. Kitap, cesaretin, dostlugun ve dogru olani yapmanin oneimini vurgular.",
         "soru": "Harry neden Gryffindor'a secildi? Cesaret sence nasil tanimlanir? Harry'nin en cesur ani hangisiydi ve sen onun yerinde olsan ne yapardin?",
         "oneri": ["Hobbit — J.R.R. Tolkien: Macera, cesaret ve beklenmedik kahramanlik", "Narnia Gunlukleri — C.S. Lewis: Fantastik bir dunyada iyilik ve kotiuluk mucadelesi", "Percy Jackson — Rick Riordan: Yunan mitolojisi ve modern macera", "Eragon — Christopher Paolini: Bir gencin ejderha suvaarisi olma yolculugu", "Artemis Fowl — Eoin Colfer: Dahii bir cocugun fantastik dunyayla tanismasi"],
         "etkinlik": "Hogwarts'ta hangi binaya ait olurdunuz? Neden? Kendi buyulu okullunuzu tasarlayin: adi, dersleri, kurallari ve ozel ozelliklleri neler olurdu?"},
    12: {"kitap": "Bir Noel Sarkisi — Charles Dickens",
         "aciklama": "Cimri ve soguk kalpli Ebenezer Scrooge'un Noel gecesi uc ruhun ziyaretiyle yasadigi donusum hikayesi. Gecmis, simdi ve gelecek ruhlari Scrooge'a hayatinin gercek yuzunu gosterir ve o, comertligin ve sevginin degerini anlar. Kitap, insanlarin degisebilecegine dair umut veren zamansiz bir klasiktir.",
         "soru": "Insanlari degistiren sey nedir? Scrooge'u ne degistirdi? Sen hayatinda bir 'uyaniis' ani yasadin mi?",
         "oneri": ["Pamuk Prenses — Grimm Kardesler: Iyilik, kotiuluk ve adaletiin masali", "Kis Masallari Antolojisi: Farkli kulturlerden kis temalai hikayeler", "Kucuk Agac — e.e. cummings: Sahte gorunuslerin otesindeki gercek guzellik", "Bir Noel Gecesi — Nikolay Gogol: Rusya'dan eglenceli bir kis macearasi", "Karlar Ulkesi — Hans Christian Andersen: Sevginin buzu eritme gucu"],
         "etkinlik": "Scrooge'un donusum hikayesinden ilham alarak kendi 'degisim' hikaayenizi yazin. Hayatinizda degistirmek istediginiz bir aliskanlik var mi? Uc ruh size ne gosterirdi?"},
    1: {"kitap": "Matilda — Roald Dahl",
        "aciklama": "Super zeki kucuk bir kizin, onu anlamayan ailesine ve zalim okul muduru Bayan Trunchbull'a karsi mucadelesi. Matilda kitaplara siginarak ic dunyasini zenginlestirir ve sonunda kendi gucunu kesfeder. Kitap, zekanin, cesaretin ve kitap okumanin donusturucuu gucunu kutlar.",
        "soru": "Matilda guclu yonlerini nasil kesfetti? Senin super gucun ne? Bir yetiskin seni anlamasa ne yapardin?",
        "oneri": ["Pippi Uzunccorap — Astrid Lindgren: Bagimsiz, guclu ve eglenceli bir kiz", "Hayalet Avcilari — Cornelia Funke: Cesaret ve macera dolu bir arkadaslik hikayesi", "Bayan Frola'nin Sinifi — Jostein Gaarder: Felsefe ve merak dolu bir sinif deneyimi", "Cimcime'nin Gunlugu — Sevim Ak: Turk cocuk edebiyatinin sevilen karakteri", "Konussan Torba — Mavisel Yener: Eglenceli ve ogretici hikayeler serisi"],
        "etkinlik": "Matilda gibi siz de 'super gucunuzu' kesfeedin! Guclu yonlerinizi listeleyin ve bu gucu nasil kullanabileceginize dair kisa bir hikaye yazin."},
    2: {"kitap": "Sevgi Okulu — Edmondo De Amicis",
        "aciklama": "Bir Italyan cocugunun okul gunlugu araciliigiyla anlatilan dostluk, fedakarlik ve sevgi hikayeleri. Kitap, farkli sosyal siniflardan gelen cocuklarin birlikte buyumesini ve birbirlerinden ogrenmesini gozler onune serer. Her bolum, farkli bir deger uzerine dusunduren hikayelerle dolu etkileyici bir klasiktir.",
        "soru": "Kitaptaki hangi hikaye seni en cok etkiledi? Neden? Okul arkadasliklarinin hayatiindaki onemi nedir?",
        "oneri": ["Anne — Hector Malot: Kayip annesini arayan bir cocugun fedakarlik dolu yolculugu", "Degirmenimden Mektuplar — Alphonse Daudet: Doga, insanlik ve koy hayati", "Tomurcuk Cocuk — Fakir Baykurt: Turkiye kirsalinda bir cocugun egitim mucadelesi", "Seker Portakali — Vasconcelos: Yoksulluk ve hayal gucuunn donusturucu etkisi", "Kirmizi Bisiklet — Can Safak: Bir cocugun hayal ve gerceklik arasindaki yolculugu"],
        "etkinlik": "Kendi 'Sevgi Okulu' gunluugunuzu tutun. Bir hafta boyunca okulda yasadiginiz en guzel ani, en onemli dersi ve bir arkadasinizin size ogrettigi seyi yazin."},
    3: {"kitap": "Agaclari Diken Adam — Jean Giono",
        "aciklama": "Tek basina, sessizce ve yillarca emek vererek canak bir bolgeyi ormana donusturen bir cobanin ilham verici hikayesi. Elzeard Bouffier, hic bir karsilik beklemeden her gun yuz agac tohumuu ekerek cevresini donusturur. Kitap, bir insanin sabirla ve inancla dunyayi degistirebileecegini gosteren muhtesem bir allegoridir.",
        "soru": "Dogayla baris icinde yasamak icin neler yapabiliriz? Bir insan tek basina dunyyayi degistirebilir mi? Sen ne dikerdin?",
        "oneri": ["Orman Cocuklari — Elsa Beskow: Doga icinde buyumeenin masalsi hikayesi", "Bitki Adasi — Charlotte Taylor: Dogayla bag kurmanin ve uyumlu yasamnin onemi", "Heidi — Johanna Spyri: Alplerin dogasi ve cocukluk masumiyeti", "Kurk Mantolu Madonna — Sabahattin Ali: Dogaa ve insan iliskisi", "Kucuk Prens — Saint-Exupery: Gulune bakmak ve sorumluluk almak"],
        "etkinlik": "Okul bahcesine veya cevrenize bir agac veya bitki dikin. Buyumesini takip edin ve bir 'Agacim Gunlugu' tutun. 10 yil sonra bu agac nasil gorunecek?"},
    4: {"kitap": "Einstein'in Ruyalari — Alan Lightman",
        "aciklama": "Zamanin farkli isldigi duyalari hayal eden buyuleyici bir bilim kurgu. Her bolumde zaman farkli bir sekilde akar: birinde zaman yavaslaiyor, birinde geriye gidiyor, birinde dongusel. Albert Einstein'in 1905'te goreceelilik teorisini gelistirirken hayal etmis olabilecegi dualari kurgular. Bilim ve edebiyatin muhtesem birlesimi.",
        "soru": "Zaman geriye gidebilse ne degistirirdin? Zamanin yavasladigi bir dunyada yasamak ister miydin? Neden?",
        "oneri": ["Zaman Makinesi — H.G. Wells: Bilim kurgunun klasigi, gelecege yolculuk", "Yirmi Bin Fersah Denizin Altinda — Jules Verne: Bilim ve macera", "Marslii — Andy Weir: Mars'ta hayatta kalma mucadelesi", "Otostopcularin Galaksi Rehberi — Douglas Adams: Eglenceli ve felsefi bilim kurgu", "Dune — Frank Herbert: Epik bir gelecek evreni"],
        "etkinlik": "Kendi 'zaman dunyaniizi' yaraatin: Zamainiin farkli isldigi bir dunyada yasasaydiniz hayat nasil olurdu? Kisa bir hikaye yazin veya resimleyin."},
    5: {"kitap": "Beyaz Dis — Jack London",
        "aciklama": "Bir kurdun dogadan insanlarin dunyasina uyum saglama hikayesi. Beyaz Dis, vahsi dogada dogaar ve hayatta kalma mucadelesi verir. Sonra insanlarla tanisir, once zulm gorur ama sonunda sevgi ve guven bulur. Kitap, guvenin nasil kazanildgni, sevginin iyilestirici gucunu ve dogayla insan arasindaki baagi etkileyici bir sekilde anlatir.",
        "soru": "Beyaz Dis neden insanlara guvenmeyi ogrendi? Guven nasil kazanilir? Bir kez kirilan guven yeniden insa edilebilir mi?",
        "oneri": ["Hayvan Ciftligi — George Orwell: Toplumsal elestiri ve adalet", "Vahsi'nin Cagrisi — Jack London: Bir kopegin dogaya donus yolculugu", "Karabaas — Orhan Kemal: Insanlik ve sadakat", "Kucuk Kara Balik — Samed Behrengi: Cesaret ve kesfin hikayesi", "Watership Tepesi — Richard Adams: Tavsanlarin epik yolculugu"],
        "etkinlik": "Bir hayvan secin ve onun gozunden bir gun yasayin: Ne gorur, ne duyar, ne hisseder? Bu hayvanin gunluk hayatini anlatan kisa bir oykuu yazin."},
    6: {"kitap": "Robinson Crusoe — Daniel Defoe",
        "aciklama": "Issiz bir adada hayatta kalma ve umudunu koruma hikayesi. Robinson Crusoe, gemi kazasindan sonra issiz bir adaya duseir ve yillaarca tek basina yasar. Kendi basarisini insa eder, yiyecek bulur, barina yapar ve sonunda Cuma adini verdigi bir yerliyle arkadaslik kurar. Kitap, insanin dayanikliligini, umudun gucunu ve hayatta kalma icgudusunu kutlar.",
        "soru": "Issiz bir adada olsan yanina 3 sey alabilsen ne alirdin? Neden? Yalnizlikla nasil basa cikardin? Umudunu nasil koruurdun?",
        "oneri": ["Define Adasi — Robert Louis Stevenson: Korsanlar, hazine ve macera", "80 Gunde Devr-i Alem — Jules Verne: Dunya etrafinda heyecan dolu bir yarris", "Denizler Altinda 20.000 Fersah — Jules Verne: Okyanusun derinliklerinde kesif", "Mercan Adasi — Robert Michael Ballantyne: Ada macerasi ve hayatta kalma", "Gulliver'in Gezileri — Jonathan Swift: Farkli diyarlarda fantastik maceralar"],
        "etkinlik": "Kendi 'hayatta kalma planinizi' yazin: Issiz bir adada ilk 7 gun ne yapardiniz? Baraiak, su, yiyecek ve guvenlik icin planarinizi cizin ve sinifta sun."},
}

# ── P26-P29: Basit veri dict'leri ──
_BULTEN_SANAT = {
    9: {"baslik": "Duygu Paleti",
        "tanim": "Duygularimizi renklerle ifade etmek, ic dunyamizi kesfetmenin en guzel yollarindan biridir. Her duygunun kendine ozgu bir rengi vardir; ornegin mutluluk sari, huzun mavi, ofke kirmizi ile iliskilendirilebilir. Bu etkinlikte ogrenciler duygularini tanimlamayi, adlandirmayi ve sanatsal yollarla ifade etmeyi ogrenirler. Duygu paleti calismasi hem duygusal farkindaligi arttirir hem de yaratici ifade becerisini gelistirir.",
        "aktivite": "1) Kagidinin bir kosesine 6-8 farkli duygu yaz (mutluluk, uzuntu, ofke, korku, saskinlik, huzur, heyecan, minnettarlik). 2) Her duygu icin seni en iyi temsil eden bir renk sec ve o rengi duygunun yanina boya. 3) Kagidinin buyuk bolumune bu renklerle serbest bir resim ciz; hangi duyguyu daha cok hissediyorsan o rengi daha cok kullan. 4) Resmine duygularini yansitan bir isim ver. 5) Sinif arkadaslarinla resimlerini paylas ve farkli yorumlari kesfet.",
        "malzeme": "Boya kalemleri, sulu boya veya pastel boyalar, A3 beyaz kagit, paleta veya tabak (renk karistirmak icin)",
        "fayda": "Duygusal okuryazarlik gelisir, ic gozlem becerisi guclenir ve ogrenciler duygularini sozlu olmayan yollarla ifade etmeyi ogrenirler."},
    10: {"baslik": "Mandala Cizimi",
         "tanim": "Mandala, Sanskritce 'daire' anlamina gelir ve yuzyillardir meditasyon araci olarak kullanilmaktadir. Geometrik desenlerin tekrarlanmasi zihni sakinlestirir, odaklanmayi arttirir ve stresi azaltir. Mandala cizimi cocuklarda ince motor becerileri gelistirirken ayni zamanda sabir ve dikkat yogunlastirma kapasitesini de guclendirir. Arastirmalar, mandala boyamanin kaygili cocuklarda belirgin bir rahatlama etkisi yarattigini gostermektedir.",
         "aktivite": "1) Pergelle kagidinin ortasina buyuk bir daire ciz. 2) Daireyi cetvelle 8 esit parcaya bol. 3) Her parcaya simetrik geometrik desenler ekle: ucgenler, dalgalar, yapraklar, yildizlar. 4) Merkezden disa dogru katmanlar halinde desenleri zenginlestir. 5) Boyama asamasinda derin nefes egzersizi yap: bir deseni boyarken nefes al, sonrakinde nefes ver.",
         "malzeme": "Pergel, cetvel, silgi, ince uclu siyah kalem (0.5mm), renkli kalemler veya keceliler, beyaz A4 kagit",
         "fayda": "Odaklanma ve dikkat suresi uzar, stres ve kaygi azalir, ince motor beceriler gelisir ve estetik duyarlilik olusur."},
    11: {"baslik": "Kolaj Hayallerim",
         "tanim": "Vizyon panosu olarak da bilinen bu etkinlik, ogrencilerin hayallerini ve hedeflerini gorsel olarak somutlastirmasina yardimci olur. Arastirmalar, hedefleri gorsellestirenin o hedeflere ulasma olasiliginin yuzde kirktan fazla arttigini gostermektedir. Kolaj calismasi ayni zamanda ogrencilerin kendilerini tanimasina, ilgi alanlarini kesfetmesine ve gelecege dair umut beslemesine olanak tanir. Bu etkinlik ozellikle motivasyonu dusuk ogrencilerde olumlu bir ic gorunum olusturur.",
         "aktivite": "1) Bir karton uzerine ismini ve 'Hayallerim' basligini yaz. 2) Dergi ve gazetelerden hayallerini, hedeflerini ve seni mutlu eden seyleri temsil eden resimler kes. 3) Kestiklerini kartona estetik bir sekilde yerlestir ve yapistir. 4) Bos kalan yerlere motivasyon cumleleril ve kisisel hedeflerini yaz. 5) Kolajini sinifta sun ve hayallerini arkadaslarinla paylas.",
         "malzeme": "Eski dergiler ve gazeteler, makas, yapisitirici (sivi veya stick), buyuk karton (50x70), renkli kalemler, yapiskan notlar",
         "fayda": "Hedef belirleme becerisi gelisir, motivasyon artar, oz farkindalik guclenir ve yaratici dusunme kapasitesi desteklenir."},
    12: {"baslik": "Sukran Agaci",
         "tanim": "Minnettarlik duygusunu gorsel olarak ifade etmek, olumlu bakis acisini guclendirmenin etkili bir yoludur. Sukran agaci etkinligi ogrencilere hayatlarindaki guzel seyleri fark etmeyi, bunlari takdir etmeyi ve minnettar olmay ogretir. Pozitif psikoloji arastirmalari, duzellii minnettarlik pratigi yapan bireylerin daha mutlu, daha direncli ve sosyal iliskilerinde daha basarili olduklarini ortaya koymaktadir. Bu etkinlik sinif ici dayanismayi ve olumlu sinif iklimini de destekler.",
         "aktivite": "1) Buyuk bir kagida kalin bir agac govdesi ve dallari ciz. 2) Yesil ve sari kagitlardan yaprak sekilleri kes (en az 15-20 yaprak). 3) Her yapraga minnettar oldugun bir seyi yaz: kisiler, deneyimler, yetenekler, firsatlar. 4) Yapraklari agacin dallarik yapistir. 5) Agacin koklerine seni guclu kilan degerleri yaz. Sinifta ortak bir sukran agaci da olusturabilirsiniz.",
         "malzeme": "Buyuk beyaz kagit veya karton (70x100), yesil ve sari renkli kagitlar, makas, yapistirici, renkli yapiskan notlar, kalemler",
         "fayda": "Minnettarlik duygusu gelisir, olumlu bakis acisi guclenir, sinif ici baglanti ve aidiyet duygusu artar."},
    1: {"baslik": "Hedef Kolaji",
        "tanim": "Yeni yilin baslangicinda hedefleri goselleistirmek, motivasyonu artirmanin ve odaklanmanin guclu bir yoludur. Vizyon panosu teknigi, sporculardan is insanlarina kadar pek cok basarili kisi tarafindan kullanilmaktadir. Hedefleri somut gorsellere donusturmek beyinde hedefle ilgili agi aktive eder ve firsat farkindaligini arttirir. Bu etkinlik ogrencilerin yeni donem icin akademik, sosyal ve kisisel hedeflerini planlamasina yardimci olur.",
        "aktivite": "1) Kartonu uc bolume ayir: Akademik Hedefler, Kisisel Gelisim, Sosyal Hedefler. 2) Her bolum icin dergilerden ve gazetelerden hedeflerini temsil eden gorseller bul ve kes. 3) Gorselleri kartona yapistir ve yanlarjna somut hedef cumleleri yaz. 4) Kolajin merkezine yilin mottosu olacak bir cumle yaz. 5) Kolajini calisma masanin karsisina as ve her ay hedeflerini gozden gecir.",
        "malzeme": "Buyuk karton (50x70), dergiler ve gazeteler, makas, yapistirici, renkli kalemler, boya, sim",
        "fayda": "Hedef belirleme ve planlama becerisi gelisir, motivasyon artar, ogrenci kendi gelisim yolculuguna sahip cikar."},
    2: {"baslik": "Sevgi Karti",
        "tanim": "El yapimi bir kart hazilamak, sevgiyi en samimi sekilde ifade etmenin yollarindan biridir. Dijital cagda elle yazilmis bir mesajin degeri cok daha buyuktur. Sevgi karti etkinligi ogrencilere hem yaraticilik hem de duygusal ifade becerisi kazandirir. Kartlarin hazirlanma sureci, ogrencinin karsi tarafi dusunmesini, empati kurmasini ve duygularini sozculkelere dokmesinini saglar. Bu etkinlik ayrica ince motor becerileri ve estetik duyarlilig destekler.",
        "aktivite": "1) Kimlere kart hazirlayacagini belirle (en az 3 kisi: aile uyesi, arkadas, ogretmen). 2) Her kisi icin ozel bir tasarim dusun: en sevdigi renkler, hobiler, ortak anilar. 3) Kartonu ikiye katla ve kapagini susl: cicekler, kalpler, yildizlar veya soyut desenler. 4) Icine samimi ve spesifik bir mesaj yaz: 'Seni seviyorum cunku...' 5) Kartlari zarflara koy ve tesli et. Alicinin tepkisini gozlemle.",
        "malzeme": "Renkli kartonlar (A5), boya kalemleri, sim, yapiskan sticker, kurdele, makas, yapistirici, zarf",
        "fayda": "Duygusal ifade becerisi gelisir, empati guclenir, el becerisi artar ve sevgi dili zenginlesir."},
    3: {"baslik": "Doga Sanati",
        "tanim": "Land Art olarak da bilinen doga sanati, dogadaki malzemeleri kullanarak gecici sanat eserleri olusturma pratigidir. Bu etkinlik ogrencileri disa cikmaya, dogayla etkilesime girmeye ve cevrelerindeki guzellig farki etmeye tesvik eder. Doga sanati yaraticilik, problem cozme ve estetik duyarlilik becerilerini ayni anda gelistirir. Ayrica dogaya saygi ve cevre biilnci olusturmanin eglenceli bir yoludur. Mevsimsel degisimleri gozlemlemek ve dogal malzemelerle calisma cocuklarda duyusal deneyimi zenginlestirir.",
        "aktivite": "1) Okul bahcesinde veya parkta bir doga yuruyusu yap ve ilgini ceken dogal malzemeleri topla: yapraklar, dallar, taslar, cicekler, kozalaklar. 2) Duz bir zemin sec ve toplaadigin malzemelerle bir kompozisyon olustur: mandala, hayvan figuru veya soyut desen. 3) Eserini farkli acilardan fotgrafla. 4) Malzemeleri dogaya birak, eserinin gecici oldugunu kabul et. 5) Fotografini sinifta paylas ve yaratim surecini anlat.",
        "malzeme": "Dogal malzemeler (yaprak, dal, tas, cicek, kozalak), telefon veya fotograf makinesi",
        "fayda": "Doga baglantisi guclenir, yaraticilik ve problem cozme becerisi gelisir, cevre bilinci artar ve duyusal deneyim zenginlesir."},
    4: {"baslik": "Dunya Koyu",
        "tanim": "Dunya uzerindeki farkli kulturleri tanimak, hosgoru ve saygi duygusunu gelistirmenin en etkili yollarindan biridir. Bu etkinlikte ogrenciler farkli kitlardaki ulkelerin geleneklerini, yemeklerini, kiyafetlerini ve yasiayis bicimlerini arastirarak kulturel zenginligin farkina varirlar. Kulturlerarasi farkindalik, 21. yuzyilin en onemli yetkinliklerinden biri olarak kabul edilmektedir. Bu calisma ayrica cografya ve sosyal bilgiler dersleriyle de entegre edilebilir.",
        "aktivite": "1) Buyuk bir kagida dunya haritasinin ana hatlrini ciz. 2) Her kitayi farkli bir renge boya. 3) Her kita icin o bolgeye ozgu bilgiler arastir: geleneksel yemek, dans, kiyafet, festival. 4) Buldugun bilgileri ve gorselleri haritanin ilgili bolgesine yaz veya yapistir. 5) Haritanin altina 'Farkliliklar bizi zenginlestirir' basligi yaz ve sinifta sun.",
        "malzeme": "Buyuk beyaz kagit (70x100), atlas veya dunya haritasi referansi, renkli kalemler, dergilerden kesilmis gorseller, yapistirici",
        "fayda": "Kulturel farkindalik ve hosgoru gelisir, cografi bilgi artar, arastirma becerisi guclenir ve farkli bakis acilari kazanilir."},
    5: {"baslik": "Gelecek Mektubu",
        "tanim": "Gelecekteki kendine mektup yazmak, guclu bir oz yansitma ve hedef belirleme araci olarak kullanilir. Bu etkinlik ogrencilerin su anki duygulanini, hayallerini ve beklentilerini kaydederek gelecekte kendilerine bir zaman kapsulu birakmalarini saglar. Mektup yazma sureci, ic gozlem yapmayi, duygulari sozcuklere dokmeyi ve gelecege umutla bakmayi tesvik eder. Yillar sonra acildiginda ise kisisel gelisimin somut bir kaniti olarak buyuk duygusal deger tasir.",
        "aktivite": "1) Sessiz bir ortamda otur ve gozlerini kapat, 10 yil sonraki kendini hayal et. 2) Mektubuna 'Sevgili 10 yil sonraki ben...' diye basla. 3) Su anki hayallerin, korkularini, en cok sevdigin seyleri, arkadaslarini ve hedeflerini yaz. 4) Gelecekteki kendine tavsiyeler ver ve sorular sor. 5) Mektubu katla, zarfa koy ve uzerine 'Acilacak tarih: 2036' yaz. Guvenli bir yerde sakla.",
        "malzeme": "Guzel bir mektup kagidi, zarf, kalem (mumkunse dolma kalem), mumlak veya sticker (zarfi muhurlemek icin)",
        "fayda": "Oz yansitma ve ic gozlem becerisi gelisir, gelecek yonelimli dusunme guclenir, yazili ifade kapasitesi artar."},
    6: {"baslik": "Ani Kutusu",
        "tanim": "Yil boyunca biriktirilen kucuk anilari ozenle saklayacak bir ani kutusu olusturmak, hem yaratici bir el isi etkinligi hem de duygusal bir yil sonu degerlendirmesidir. Ani kutusu cocuklara zamani somut nesnelerle hatirlamayi, olumlu deneyimleri takdir etmeyi ve gecmise minnettarlikla bakmayi ogretir. Her nesne bir hikaye anlatir ve yillar sonra acildiginda o doneme ait duygulari canlandirir. Bu etkinlik ayrica organize etme, siniflandirma ve estetik duzenleme becerilerini de destekler.",
        "aktivite": "1) Bir kutu sec (ayakkabi kutusu idealdir) ve dis yuzeyini boya, kagit veya kumays ile kapla. 2) Kutunun kapagina yili ve ismini yaz, etrafini susl. 3) Yil boyunca biriktirdigin anilari kutoya yerlestir: fotograflar, biletler, notlar, kucuk hediyeler, basari belgeleri. 4) Her aniyla ilgili kisa bir not yaz: ne zaman, nerede, neden onemli. 5) Kutuyu guvenli bir yerde sakla ve her yilin sonunda yeni bir kutu olustur.",
        "malzeme": "Ayakkabi kutusu veya karton kutu, boya, renkli kagitlar, yapistirici, makas, ani esyalari (foto, bilet, not)",
        "fayda": "Ani biriktirme ve deger verme duygusu gelisir, organizasyon becerisi artar, yil sonu degerlendirmesi somutlasir."},
}

_BULTEN_DOGA = {
    9: {"baslik": "Okul Bahcesi Kesfi",
        "bilgi": "Okul bahcesindeki agaclar ve bitkiler bizim doga dostlarimizdir. Her agac havamizi temizler, golge saglar ve pek cok canliya ev sahipligi yapar. Turkiye'de okul bahcelerinde en sik rastlanan agaclar cinar, akasya, servi ve cesnelerdir. Bu agaclarin her birinin farkli yaprak sekilleri, cicekleri ve meyveleri vardir. Dogayi tanimak onu korumnanin ilk adimdir; cevremizdeki bitkileri tanidikca onlara karsi sorumluluk duygumuz da gelisir.",
        "gorev": "Okul bahcesinde 5 farkli bitki veya agac bul, yapraklarinin fotograflarini cek ve isimlerini arastir. Her biri icin bir bilgi karti hazirla: adi, yaprak sekli, ne zaman cicek acar, hangi canlilara ev sahipligi yapar. Bulgularini bir 'Okul Bahcesi Rehberi' posterine donustur.",
        "gozlem": "Bu ay yapraklarin renklerini, bahcedeki bocekleri ve kuslari gozlemle. Her gun 5 dakika sessizce oturup dogayi dinle.",
        "bilim": "Fotosentez: Bitkiler gunes isigini kullanarak karbondioksiti oksijene donusturur. Bir agac yilda ortalama 100 kg oksijen uretir."},
    10: {"baslik": "Sonbahar ve Mevsim Degisimi",
         "bilgi": "Sonbahar, doganin en renkli donus donemidir. Yapraklar neden renk degistirir? Gunler kisaldikca bitkiler klorofil uretimini yavaslatir. Yesil pigment azaldikca yapraklardaki sari (ksantofil) ve turuncu (karoten) pigmentler ortaya cikar. Bazi agaclarda ise antosiyanin pigmenti kirmizi ve mor tonlar olusturur. Bu suec agacin kisa hazirlanmasidir; yapraklari dokerek su kaybini onler ve enerjisini kok sistemine yonlendirir.",
         "gorev": "Farkli turlerden en az 10 farkli renkte yaprak topla. Her yapragi iki kagit arasina koyarak presle. Kuruduktan sonra bir yaprak albumu olustur ve her yapraginadin, rengini ve topladgin yeri yaz. Yapraklar arasindaki renk ve sekil farklarini karsilastir.",
         "gozlem": "Her hafta ayni agaci ziyaret et ve degisimini fotgrafla. Ay sonunda fotograflari yan yana koyarak mevsim gecisini gozlemle.",
         "bilim": "Klorofil molekulu gunes isigini emerek fotosentez icin enerji saglar. Sonbaharda klorofilin parcalanmasi diger pigmentlerin gorunnur olmasina neden olur."},
    11: {"baslik": "Goc Eden Kuslar",
         "bilgi": "Her sonbahar, milyonlarca kus binlerce kilometre yol kat ederek sicak ulkelere goc eder. Turkiye, Avrupa ile Afrika arasindaki en onemli kus goc yollarindan birinin uzerinde yer alir; ozellikle Istanbul Bogazii ve Belen Gecidi onemli goc noktalardir. Leylekler, kirlangiclar, ebabiller ve flamingolar en bilinen gocmen kuslardir. Kuslar gocten once yag depolayarak enerji biriktirirler ve yildizlari, gunes acisini ve hatta Dunya'nin manyetik alanini kullanarak yol bulurlar.",
         "gorev": "Pencerenden veya bahceden gokyuzunu gozlemle ve goc eden kus suruleri gormeye calis. Bir gozlem gunlugu tut: tarih, saat, hava durumu, gordugun kus turleri ve ucus yonleri. En az 3 gocmen kus turun arastir ve goc rotalarini bir harita uzerinde isaretle.",
         "gozlem": "Sabah erken saatler ve aksam uzeri kus gozlemi icin en uygun zamanlardir. Durbun varsa kullan, yoksa gozlerinle takip et. Kuslarin V formasyonunda ucmasinin nedenini arastir.",
         "bilim": "Kuslar V formasyonunda ucarak enerji tasarrufu yapar. Ondeki kusun kanat cirpmasi arkadakine yukari iten bir hava akimi olusturur ve bu sayede sure yuzde yetmis daha az enerji harcar."},
    12: {"baslik": "Kis Uykusu ve Hayatta Kalma",
         "bilgi": "Kissin soguk ve yiyecek kiitligi donemninde bazi hayvanlar kis uykusuna yatarak hayatta kalir. Bu surecte vucut sicakliklari duser, kalp atislari yavaslar ve metabolizma minimuuma iner. Ayilar, kirpiler, yarasalar, kaplumbagalar ve bazi sincap turleri kis uykusuna yatan hayvanlara ornek verilebilir. Ornegin bir kirpinin normal kalp atisi dakikada 190 iken kis uykusunda dakikada 20'ye duser. Kis uykusu gercek bir hayatta kalma stratejisidir ve evrim surecinde geislmistir.",
         "gorev": "Kis uykusuna yatan en az 5 hayvan arastir ve her biri icin bir bilgi karti hazirla: hayvain adi, kis uykusu suresi, vucut sicakligi degisimi, nerede uyur, ne zaman uyanir. Bulgularini renkli bir poster haline getir ve sinifta sun.",
         "gozlem": "Kis aylarinda bahcendeki veya parkindaki hayvanlari gozlemle. Hangi hayvanlar hala aktif? Kuslar, kediler ve kopekler kisa nasil uyum sagliyorlar? Gozlemlerini gunlugune yaz.",
         "bilim": "Hibernasyon (kis uykusu) sirasinda hayvanlar yaz boyunca biriktirdikleri yag depolarini enerji kaynagi olarak kullanirlar. Bazi turler kis boyunca hic yemek yemez ve su icmez."},
    1: {"baslik": "Su Dongusu ve Kar",
        "bilgi": "Su, gezegenimizde surekli bir dongu halindedir: denizlerden buhaslasir, bulutlari olusturur, yagmur veya kar olarak yeryuzune duser, nehirlere ve yeraltii sularina karisir ve tekrar denizlere ulasir. Duny'daki suyun yuzde dokusan yedisi tuzlu su, yuzde ucu tatli sudur ve bu tatli suyun buyuk bolumu buzullarda ve yer altinda bulunur. Kis aylarinda gozlemledigimiz kar, su buharinin atmosferde donarak kristallesmasiyle olusur. Her kar kristali altigen simetriye sahiptir ve hicbir kar tanesi birbirinin aynisi degildir.",
        "gorev": "Su dongusunu canlandiran bir deney yap: buyuk bir kavanoiza ilik su koy, agzini streç filmle kapat ve uzerine buz kupleri yerlestir. Kavanozun icinde buharlasman, yogunlasma ve yagisi gozlemle. Deneyi fotografla ve her asamayi acikla. Sonuclari bir deney raporu olarak yaz.",
        "gozlem": "Kar yagdiginda bir karton uzerine kar tanelerini yakalayip buyutecle incele. Farkli sekillerdeki kristalleri cizmeye calis. Hava sicakligi ile yagis turu arasindaki iliskiyi gozlemle.",
        "bilim": "Suyun uc hali vardir: kati (buz), sivi (su), gaz (su buhari). Su dongusunde bu uc hal arasinda surekli donusum yasanir. Bu dongu sayesinde Dunya'da yasam mumkun olur."},
    2: {"baslik": "Tohumlar ve Cimlenmne",
        "bilgi": "Her tohum, icinde tam bir bitkinin genetik bilgisini ve ilk gelisim icin gerekli besini tasir. Bir fasulye tohumu topragoa ektiiginizde once su emer ve siser, ardidnan tohum kabubu catlar ve kok ile filiz disari cikar. Bu mucizevi suece ciimlenme denir. Tohumlarin cimlenmesi icin su, sicaklik ve oksijene ihtiyac vardir; bazi tohumlar ise isik veya soguk donemei gibi ozel kosullar gerektirir. Dunyanin en buyuk tohumu hindistan cevizi palmiyesinin tohumudur ve 25 kg agirliginda olabilir.",
        "gorev": "Bir tohum ekme deneyi yap: islak pamuk uzerine nohut, mercimek veya fasulye tohumlari yerlestir. Her gun su ver ve buyumesini olc. Bir buyume gungugu tut: tarih, boy (mm), yaprak sayisi, gozlemler. En az 2 hafta boyunca takip et ve sonuclarini grafikle goster.",
        "gozlem": "Farkli kosullarda tohumlari karsilastir: biri isikta biri karanlikta, biri sicakta biri sogukta. Hangi kosulda daha hizli buyudugun gozlemle ve nedenini arastir.",
        "bilim": "Ciimlenme sirasinda tohum, depoladigi nisastayi enzimler yardimiyla sekere donusturur ve bu enerjiyle buyur. Yapraklar cikinca bitki fotosentez yaparak kendi besinini uretmeye baslar."},
    3: {"baslik": "Bahar Uyanisi",
        "bilgi": "Bahar, doganin en canli ve hareketli donemlerinden biridir. Gun uzunlugu arttkca bitkiler tomurcuklanmaya baslar, gocmen kuslar geri doner, kelebkler ve ari larlar ortaya cikar. 21 Mart'ta gece ve gunduz esitlenir; bu gune ilkbahar eksinoksu denir. Bahar aylarinda toprak isinir ve yer alti sulari yukselir, bu da bitki buyumesini hizlandirir. Turkiye'nin farkli bolgelkerinde bahar farkli zamanlarda gelir: Akdeniz'de Subat'ta baslarken Dogu Anadolu'da Nisan'i bulabilir.",
        "gorev": "Bir hafta boyunca her gun disari cik ve baarin bir belirtisini fotfgrafla: ilk cice acimi, tomurcuklanan dal, geri donen kus, ucan kelebek, bocek aktivitesi. Fotograflarini bir 'Bahar Takvimi' posterine donustur ve her gozlemin tarihini yaz. Gozlemlerini sinifta paylas.",
        "gozlem": "Ayni agaci veya bitkiyi her hafta ziyaret et ve degisimini kaydet. Bahardaki hayvan davranislarini gozlemle: kuslar yuva yapiyor mu? Arilar hangi ciceklere gidiyor?",
        "bilim": "Bitkiler gunes isiginin suresini algilayan fitokrom adli pigmentler sayesinde mevsimi anlar. Gun uzunlugu belirli bir esigi atiginda ciceklenme hormonu (florigen) uretilir ve bitki cicek acar."},
    4: {"baslik": "Dunya Gunu ve Cevre Koruma",
        "bilgi": "22 Nisan Dunya Gunu, 1970 yilindan bu yana her yil kutlanan ve cevr biilincini artirmayi amaclayan kuresel bir etkinliktir. Gezegenimiz ciddi cevre sorunlariyla karsi karsiadyr: iklim degisikligi, hava ve su kirliligi, orman tahribi, biyocesitlilik kaybi ve plastik kirliligi bunlarin basinda gelir. Her yil okyanuslara 8 milyon ton plastik atik karisir ve bu miktar her dakika bir cop kamyonu dolusu plastige esittir. Ancak bireysel adimlar buyuk fark yaratabilir.",
        "gorev": "Evde 1 hafta boyunca geri donusum yap: kagit, plastik, cam ve metal atiklari ayir. Tasarruf ettigin miktari kaydet. Ayrica bir gun boyunca harcadigin suyu olc ve tasarruf yontemleri gelistir. Bulgularini bir cevre raporu olarak yaz ve ailenle paylas.",
        "gozlem": "Cevrendeki cevre sorunlarini gozlemle: cop, hava kirliligi, su israfi. Her sorun icin bir cozum onerisi yaz. Okulda veya mahallende bir cevre temizlik etkinligi duzenlemeyi dusun.",
        "bilim": "Bir plastik sise dogada parcalanmak icin 450 yil gerektirir. Geri donusum sayesinde enerji tasarrufu saglanir: aluminyum geri donusumu yuzde doksan bes enerji tasarrufu saglar."},
    5: {"baslik": "Arilar ve Polinas yon",
        "bilgi": "Arilar, ekosistemin en onemli canlilarindan biridir ve dunyiadaki yiyeceklerin yaklasik yuzde yetmis besinin tozlasmasinda gorev alirlar. Bir bal arisi, yasami boyunca yalnizca bir cay kasiginin on ikide biri kadar bal uretir; ancak bir kovandaki 60.000 ari birlikte calsarak yilda 30 kg bal uretebilir. Ariler ciceklerden nektar toplarken polen tanelerini bir cicekten digerine tasir ve bu sayede bitkilerin uremesini saglar. Ne yazik ki pestisitler, habitat kaybi ve iklim degisikligi nedeniyle ari populasyonlari dunya genelinde hizla azalmaktadir.",
        "gorev": "Bahcede veya parkta arilari guvenli mesafeden gozlemle. Hangi cicekleri ziyaret ettiklerini, her cicekte ne kadar kaldiklarni ve renk tercihlerini kaydet. Gozlemlerini bir tablo halinde duzenlev ve ariilarin en cok hangi renk cicekleri tercih ettigini analiz et.",
        "gozlem": "Farkli saatlerde ari aktivitesini karsilastir: sabah, ogle, aksam. Hava durumunun arilarin davranislari uzerindeki etkisini gozlemle. Arilarin disinda hangi bocekler cicekleri ziyaret ediyor?",
        "bilim": "Arilar morotes isiogi gorebilirler ve ciceklerdeki morotes desenleri takip ederek nektara ulasirlar. Bir ari, koovandaki diger arilara yiyecek kaynaginin yerini 'dans' ederek anlatir; buna 'ari dansi' denir."},
    6: {"baslik": "Yaz ve Doga Kesfi",
        "bilgi": "Yaz tatili, dogayi kesfetmek ve aciik havada vakit gecirmek icin muhtesem bir firsattir. Uzun ve sicak gunler, hem bitki hem hayvan dunyasinda en aktif donemi olusturur. Yaz aylarinda bocekler, kelebekler ve kuslar en yogun sekilde gozlemlenebilir. Deniz, gol ve nehir kiyilari zengin ekosistemlere ev sahipligi yapar. Dogada vakit gecirmek cocuklarda stresi yuzde elli oraninda azaltir, yaratiicligi arttirir ve fiziksel sagligi destekler. Bu yaz, bir doga kaasfifi ol!",
        "gorev": "Yaz boyunca bir doga gunlugu tut: her gun gok yuzunu gozlemle (bulut sekilleri, gunes batisi renkleri), hava durumunu kaydet ve gordugn en az bir canliy (kus, bocek, bitki) not et. Haftada en az bir kez dogaa yuruyusu yap ve gozlemlerini ciz veya fotografla. Yaz sonunda gunlugunu ailene ve arkadaslarina sun.",
        "gozlem": "Gece gokyuzunu gozlemle: yildizlari, takimuizlarini ve ayin evrelerini kaydet. Farkli saatlerdeki bocek seslerini dinle ve kayit altina al. Bir bahcede veya parkta 1 metrekarelik bir alaandaki tum canlilari say.",
        "bilim": "Yaz gundnonumu (21 Haziran), kuzey yarimkurede yilin en uzun gunudur. Bu tarihte Gunes en yuksek noktasina ulasir ve gunduz suresi en fazla olur. Bu nedenle yaz aylari en sicak donemdir."},
}

_BULTEN_MINNETTARLIK = {
    9: {"baslik": "Yeni Baslangiclara Sukur",
        "mesaj": "Yeni bir okul yilina baslayabilmek ne buyuk bir ayircaliktir! Dunyadaki pek cok cocuk egitim imkanina sahip degil. Yeni bir yilin esiginde, sahip olduklarimizi takdir etmek ve minnettarlikla ilerlemeye baslamak icin muhtesem bir firsat onumuzdae.",
        "liste": ["Okuma yazma bildigim icin — bu beceri dunya nufusunun yuzde on besinin hala sahip olmadigi bir ayricailktir", "Bir okula gidebildigim icin — guvenli bir ogrenme ortamim var", "Arkadaslarim oldugu icin — birlikte gulecek, oynayacak ve ogrenecek insanlarim var", "Ailem beni sevdigi icin — kosulsuz bir destek sistemim var", "Sagilikli oldugum icin — her gun yeni seyler ogrenecek enerjim var", "Ogretmenlerim oldugu icin — bana rehberlik eden ve bilgi paylasan insanlar var"],
        "yansitma": "Bugun sahip oldugun ama her gun farkinda olmadigin 3 seyi dusun. Bunlari bir kagida yaz ve bir hafta boyunca her sabah oku.",
        "aile_etkinligi": "Akssam yemeginde her aile uyesi o gun icin minnettar oldugu bir seyi paylassin. Bu gelenehi her aksam tekrarlayarak minnettarlik kasini guclendirebilirsiniz."},
    10: {"baslik": "Ogretmenlerime Tesekkur",
         "mesaj": "Ogretmenler bilgi ve sevgiyle gelecegimizi sekillendirir. Hayatimizda iz birakan ogretmenlerimiz, yalnizca ders anlatan degil, bize degerli oldugmuzu hissettiren, sabriyla yol gosteren ve potansiyelimize inanan insanlardir. 24 Kasim yaklasirken ogretmenlerimize duyduugmuz minnettarligi ifade etmenin tam zamanidir.",
         "liste": ["Sabirla anlattiklari icin — ayni konuyu defalarca usanmadan tekrarladilar", "Bize guvendikleri icin — yapabilecegimize her zaman inandilr", "Hatalarimizi duzltikleri icin — hatalari ogrenme firsatina donusturduler", "Bize ilham verdikleri icin — yeni ufuklar acarak merakimizi atesleiler", "Her gun bizim icin cabaaladiklari icin — kendi zamanlairndan feragat ederek bize yatirim yaptilar", "Adaletli davrandiklari icin — her ogrenciye esit firsati ve ilgiyi sundular"],
         "yansitma": "Hayatinda en cok iz birakan ogretmeni dusun. O seni nasil etkiledi? Ona bir tesekkur mektubu yazsan ne yazardin? Bu hafta o mektubu gercekten yaz.",
         "aile_etkinligi": "Ailece cocugunuzun ogretmenine bir tesekkur karti veya kucuk bir jest hazirlayin. Anne babalar da kendi ogretmenlerinden anilrinai paylasarak cocuklara model olabilir."},
    11: {"baslik": "Arkadasliga Sukur",
         "mesaj": "Gercek arkadaslar hayatin en degerli hazineleridir. Araistirmalar, guclu arkadaslik baglarinin mutlulugu yuzde elli oraninda artirdigini gostermektedir. Gercek arkadaslik karsilikli guven, saygi ve kabul uzerine kurulur. Bu ay, hayatimizi zenginlestiren arkadaslarimiza duyduguumuz minnettarligi ifade etme zamani.",
         "liste": ["Benimle guldkleri icin — kahkaha paylasildikca cogilair", "Zor zamanlarimda yanimda olduklari icin — dusunce anlarimda elimi tuttilar", "Beni oldugum gibi kabul ettikleri icin — kusurlarimla birlikte sevdiler", "Palyasmayi ogrettikleri icin — comertligin guzelligi ancak paylasmakla anlasilir", "Hayatimi renklendirdikleri icin — onlar olmadan gunler ne kadar sönük olurdu", "Beni daha iyi bir insan yapitiklari icin — yanlarinda kendimin en iyi halini kesfettim"],
         "yansitma": "En yakin arkadasinla yasiadin en guzel aniyi hatirla. O ani ozel kilan neydi? Arkadasligginizin sana kattigi en degerli sey ne? Bu dusuncelerini arkadasinla paylas.",
         "aile_etkinligi": "Cocugunuzla birlikte bir 'Arkadaslik Agaci' cizin. Her dala bir arkadasinin ismini ve onu ozel kilan bir ozelligi yazin. Bu etkinlik cocugunuzun sosyal baglarini takdir etmesine yardimci olur."},
    12: {"baslik": "Yilin Muhasebesi",
         "mesaj": "Bu yil yasadigin guzel seyleri hatirla ve minnetarlikla an. Yil sonu degerlendirmesi yapmak, yasadiklarimizdan ders cikarmanin ve kisisel gelisimimizi gormnenin onemli bir yoludur. Her ylliin zorlulklari kadar guzelliklerini de fark etmek, olumlu bakis acimizi guclendirir ve gelecege umutla bakmamizi saglar.",
         "liste": ["Bu yil ogrendigim en onemli sey — hangi ders veya deneyim beni en cok gelistirdi", "En guzel anim — o ani yeniden yasamak istesem nasil anlatirdim", "En cok buyudugum an — hangi zorluk beni daha guclu kildi", "En cok tesekkur etmek istedigim kisi — kim bana en cok destek oldu", "Kendimle gurur duydugum an — hangi basarim beni en cok mutlu etti", "Yeni kesfettigim bir yetenegim veya ilgi alanim — bu yil kendimde ne kesfettim"],
         "yansitma": "Bu yili bir film olarak dusun. Filmin adi ne olurdu? En dramatik sahnesi ne? Mutlu sonu nasil olurdu? Bu yansitmayi yazili olarak yap.",
         "aile_etkinligi": "Ailece yil sonu sofrasinda herkes bu yilin en guzel 3 anini paylassin. Her aile uyesi digerlerine bu yil icin tesekkur etsin. Bu gelenehi her yil tekrarlayarak aile baglarini guclendirin."},
    1: {"baslik": "Sagliga Sukur",
        "mesaj": "Saglik en buyuk zenginiilktir ve cogu zaman degerini ancak kaybettigimizde anlairz. Her gun nefes alabilmek, yuruyebilmek, gorebilmek ve duyabilmek muhtesem birer hediyedir. Sagligimiza minnettarlik duymak, ayni zamanda onu koruma motivasyonumuzu da arttirir.",
        "liste": ["Kosabildigim icin — bedeenim beni istedigim yere tasiyor", "Gorebildigim icin — dunyanin guzelliklerini, sevdiklerimin yuzlerini gorebiliyorum", "Duyabildgim icin — muzigi, kus seslerini ve sevdiklerimin sesini duyabiliyorum", "Tadabildigim icin — yemeklerin lezzetini alabiliyorum", "Sarilabildigim icin — sevdiklerimi kucaklayabiliyorum", "Dusunedigim icin — ogrenebiliyor, hayal kurabiliyor ve plan yapabiliyorum"],
        "yansitma": "Bir gunlugune gozlerini kaapat ve sadece diger duyularinla yasmayi dene. Gormenin hayatinda ne kadar onemli oldugunu fark ettin mi? Bedeninin her parcasina ayri ayri tesekkur et.",
        "aile_etkinligi": "Ailece bir 'Saglik Minnettarlik Yuruyusu' yapin. Yururken her aile uyesi bedeninin bir parcasina tesekkur etsin. Yuruyus sonrasi saglikli bir atistirmalki hazirlayin ve birlikte tadi cikarin."},
    2: {"baslik": "Sevgiye Sukur",
        "mesaj": "Sevgi veren de alan da zenginlesir. Sevgi, insan hayatinin en temel ihtiyaclarindan biridir ve arastirmalar duzenlii sevgi ifade eden ailelerdeki cocuklarin duygusal olarak daha saglkili ve direncli olduklarini gostermektedir. Subat ayi, etrafimzdaki sevgiyi fark etmek ve takdir etmek icin harika bir firsattir.",
        "liste": ["Anneme ve babama — beni kosulsuz sevdkleri ve her zaman yanida olduklari icin", "Kardeslerime — benimle buyudkleri, kavga etsek de birbirimizi sevdigimiz icin", "Arkadaslarima — hayatimi renkleindirdikleri ve bana guven verdikleri icin", "Ogretmenlerime — sabirla ogrettikleri ve potansiyelime inandiklari icin", "Evcil hayvanima — kosulsuz sadakati ve sevgisiyle beni her gun mutlu ettigi icin", "Kendime — tum kusurlarimla birlikte degerli ve sevilmeye layik bir insan oldugum icin"],
        "yansitma": "Hayatindaki en onemli 5 kisiyi dusun. Her birine sevgini en son ne zaman ifade ettin? Bu hafta her birine sevgini gösteren kucuk bir jest yap: bir sariilma, bir tesekkur, bir surpriz.",
        "aile_etkinligi": "Aile uyelerinin birbirleirine 'Seni Seviyorum Cunku...' mektuplari yazin ve zarflara koyarak birbirinize verin. Bu mektuplari saklayarak zor zamanlarda tekrar okuyabilirsiniz."},
    3: {"baslik": "Dogaya Sukur",
        "mesaj": "Doga bize nefes, su, yemek ve guzelik verir. Gezegenimiz muhtesem bir yasam destek sistemidir: atmosfer bizi korur, bitkiler oksijen uretir, su dongusu yasami surduür ve toprak besinlerimizi yetisitirir. Baharin gelisiyle doga yeniden canlanirken, bu muhtesem sisteme duyduguumuz minnettarligi ifade etmenin tam zamanidir.",
        "liste": ["Temiz hava icin — her nefeste cigerlerimizi dolduran oksijen agaclarin hediyesidir", "Gunes isigi icin — bize isik, isi ve enerji verir, ruh halimizi iyilestirir", "Yagmur icin — topraagi besler, bitkileri buyutur ve suyumuzu yeniler", "Cicekler icin — renkleri ve kokularniyla dunyayi guzellestirirler", "Kuslarin sarkisi icin — her sabah bizi dogal bir melodi ile karsilarlar", "Mevsimler icin — her mevsim farkli bir guzellik ve ogrenme firsati sunar"],
        "yansitma": "Disari cik ve 10 dakika boyunca sessizce otur. Gozlerini kapat ve dogayi dinle: ruzgari, kuslari, yapraklarin hissirtisini. Actiginda etrafina bak ve 5 farkli dogal guzellik bul. Her birine icinden tesekkur et.",
        "aile_etkinligi": "Ailece bir doga yuruyusune cikin. Yol boyunca her aile uyesi dogada minnettar oldugu bir sey bulsun ve paylassin. Eve donuiste parktan (zarar vermeden) toplaadiginiz dogal malzemelrle bir minnettarlik kolaji yapiin."},
    4: {"baslik": "Ogrenmeye Sukur",
        "mesaj": "Her gun yeni bir sey ogrenebilmek muazzam bir hediyedir. Ogrenme kapasitemiz, bizi diger canlilrdan ayiran en onemli ozelliklerimizden biridir. Kitaplar, internet, ogretmenler, deneyimler ve hatta hatalarimiz — hepsi birer ogrenme kaynagdir. Ogrenmenin onundeki engellerin azaldigi bu cagda, bilgiye erisim imkanina sahip olmak buyuk bir ayricailktir.",
        "liste": ["Kitaplar icin — baska dunyalara, zamanlara ve zihinlere acilan kapilardir", "Internet icin — dunyanin butun bilgisine parmaklarimizin ucundan erisebiliyoruz", "Merak duygum icin — oogrenmeni baslaatan o icsel kivilcim her zaman yaaniyor", "Hata yapip ogrenebildigim icin — her hata aslinda kiligi degistirmis bir derstir", "Soru sorabildigim icin — soru sormak bilgeliiigin baslangicidir", "Farkli diller ve kulturler icin — her yeni dil yeni bir dunya demektir"],
        "yansitma": "Hayatiinda sana en cok sey ogreten 3 deneyimi dusun. Bunlar okul dersleri disinda da olabilir. Her deneyimden ne ogrendin? Bu ogrendiklerin bugunku hayatini nasil sekillendirdi?",
        "aile_etkinligi": "Ailece bir 'Ogrenme Festivali' yapin: her aile uyesi diger aile uyelerine bildiig bir konuyu ogretsin. Cocuk ebeveyne, ebeveyn cocuga bir sey ogretebilir. Boylece ogretmenin ve ogrenmenin karsilikli bir suec oldugunu yaasayarak ogrenirsiniz."},
    5: {"baslik": "Basarilara Sukur",
        "mesaj": "Kucuk ya da buyuk her basari kutlamay hak eder. Basari sadece buyuk zaferler degildir; her gun yaptign kucuk adimlar, gosteriiin cesaret ve ustesinden geldigin zorluklar da birer basaridir. Kendi basarilarini takdir etmek ozguveni guclendirir ve daha buyuk hedeflere ilham verir.",
        "liste": ["Bu yil yaptigm en iyi sey — hangi eylem veya karar beni en cok mutlu etti", "En zor basarigim gorev — hangi engelii asarak guclendigimi hissettim", "Kendimi astigim an — konfor alanindan cikarak ne basardim", "Birini mutlu ettigim an — bir baskasiin gulumsemesine vesile oldum", "Vazgecmedigim an — zorluklara ragmen devam ederek ne kazandim", "Yeni ogrendigim bir beceri — bu yil hangi yeni yetenegim ortaya cikti"],
        "yansitma": "Basariyi nasil tanimliyorsun? Basari sadece birinci olmak midir, yoksa daha genis bir anlami var mi? Bu yilki en buyuk 3 basarini yaz ve her birinin seni nasil hissettirdigini anlat.",
        "aile_etkinligi": "Ailece bir 'Basari Kutlama Gecesi' duzenleyin. Her aile uyesi bu yilki basarilarini anlaistin. Kucuk basarilarin da kutlanmasi cocuklarda basari motivasyonunu guclendirir. Birbirinizi alkislayin ve tebrik edin."},
    6: {"baslik": "Guzel Bir Yila Sukur",
        "mesaj": "Harika bir yili geride birakiyoruz. Her ana sukur! Bir egitim yilinin sonuna gelmek, pek cok deneyim, ogrenme ve buyume anlamna gelir. Bu yili tum guzelliikleriyle hatirlamak, zorluklarindan ders cikarmak ve yaz tatiline minnettarlikla baslamak icin mukemmel bir zaman.",
        "liste": ["Bu yilin en guzel surprizi — beklemedigm anda gelen o ozel an", "En cok guldugum an — kahkahayila paylastigim o unutulmaz olay", "En cok ogrendigim ders — sadece akademik degil, hayat dersi olarak", "En guzel arkadaslik animm — birlikte yasadigimiz o ozel deneyim", "Yaz tatilinde yapmak istedigim sey — dinlenme ve kesfin plani", "Gelecek yil icin en buyuk dileem — umut ve heyecanla bekledigim sey"],
        "yansitma": "Bu yili bir kitap olarak dusun. Kitabin basligi ne olurdu? En heyecanli bolumu hangisiydi? Kitabin son cumlesii ne olurdu? Bu duusunceleri gunlugune yaz.",
        "aile_etkinligi": "Ailece bir 'Yil Sonu Zaman Kapsulu' hazirlayin. Her aile uyesi bu yilin bir anisini, bir ogrendigi seyi ve gelecek yil icin bir dilegi bir kagida yazsin. Hepsini bir kutuya koyun ve gelecek yil ayni tarihte acin."},
}

# ── Ana İçerik Verisi ──
_BULTEN_ICERIK = {
    # ═══════════════ EYLÜL (9) ═══════════════
    ("Anaokulu", 9): {
        "g": "Çocuğunuz bu ay okul ortamıyla tanışıyor veya yeni bir eğitim yılına başlıyor. Ayrılık kaygısı bu dönemde sık karşılaşılan bir durumdur ve tamamen doğaldır. Sabır ve sevgiyle bu süreci birlikte aşacağız.",
        "b": [
            ("Ayrılık Kaygısını Anlamak", "Çocuklar güvenli bağlanma figürlerinden ayrıldıklarında kaygı yaşayabilirler. Bu süreçte sabırlı olmak ve çocuğa güven vermek büyük önem taşır. Kısa ve kararlı vedalaşma ritüelleri oluşturmak kaygıyı azaltmada en etkili yöntemdir."),
            ("Okul Rutini Oluşturma", "Düzenli uyku saatleri, sabah hazırlık rutini ve okul sonrası dinlenme zamanı belirlemek çocuğun güvende hissetmesini sağlar. Öngörülebilir bir günlük akış kaygıyı önemli ölçüde azaltır."),
            ("İlk Sosyal Adımlar", "Çocuğunuz yeni arkadaşlar edinecek, paylaşmayı ve sıra beklemeyi öğrenecektir. Her çocuğun sosyalleşme hızı farklıdır; kıyaslamaktan kaçınarak onu cesaretlendirin."),
        ],
        "v": ["Okula götürürken kısa ve güler yüzlü vedalar edin, uzatmayın", "Akşam 'Bugün en çok neyi sevdin?' diye sorun", "Sevdiği küçük bir nesneyi çantasına koymasına izin verin", "Olumsuz senaryoları çocuğun yanında konuşmaktan kaçının"],
        "e": "Birlikte 'Okulda Bir Gün' temalı resim çizin ve okul hakkında olumlu hikâyeler anlatın.",
    },
    ("İlkokul", 9): {
        "g": "Yeni eğitim öğretim yılı heyecanı ve kaygısı bir arada yaşanıyor. Bu ay öğrencilerimizin yeni sınıflarına, öğretmenlerine ve arkadaşlarına uyum sağlaması en önemli hedefimizdir.",
        "b": [
            ("Yeni Sınıfa Uyum", "Sınıf değişikliği, yeni öğretmen ve belki yeni arkadaşlar; tüm bu değişimler çocuk için stres kaynağı olabilir. Ancak doğru destekle bu süreç büyüme fırsatına dönüşür. İlk haftalarda çocuğunuzun duygularını dinleyin."),
            ("Çalışma Düzeni Kurma", "İlk haftalardan itibaren düzenli bir çalışma programı oluşturmak yılın geri kalanını kolaylaştırır. Sessiz bir çalışma köşesi ve belirli saatler bu düzenin temelini oluşturur."),
            ("Okul-Ev İş Birliği", "Velilerin öğretmenlerle iletişimde olması çocuğun uyum sürecini hızlandırır. Veli toplantılarına katılım ve okul etkinliklerini takip etmek çocuğunuza verdiğiniz değeri gösterir."),
        ],
        "v": ["Her gün okul çantasını birlikte hazırlayın", "Düzenli uyku saatlerine dikkat edin — en az 9-10 saat", "Öğretmenle tanışma toplantısına mutlaka katılın", "Çocuğunuzun deneyimlerini yargılamadan dinleyin"],
        "e": "Çocuğunuzla birlikte haftalık ders programını renkli bir şekilde hazırlayın ve çalışma köşesine asın.",
    },
    ("Ortaokul", 9): {
        "g": "Ortaokul dönemi, çocuktan ergene geçiş sürecinin başladığı kritik bir dönemdir. Akademik beklentilerin arttığı bu yılda hem akademik hem sosyal uyum sağlanması büyük önem taşır.",
        "b": [
            ("Ergenlik ve Değişim", "Fiziksel, duygusal ve bilişsel değişimler bu dönemin karakteristik özellikleridir. Öğrenciler kendilerini tanımaya, sorgulamaya ve yeni roller denemeye başlarlar. Bu değişimleri normalleştirmek önemlidir."),
            ("Akademik Sorumluluk", "Birden fazla öğretmen, farklı dersler ve artan ödev yükü ile tanışma zamanı. Ajanda kullanmak ve haftalık plan yapmak bu süreci kolaylaştırır. Öğrencinin kendi sorumluluğunu almasını teşvik edin."),
            ("Akran İlişkileri", "Arkadaş grupları ergenlik döneminde büyük önem kazanır. Sağlıklı arkadaşlık ilişkileri kurmak ve akran baskısıyla başa çıkmak bu dönemin temel becerileridir."),
        ],
        "v": ["Açık iletişim kurun, yargılamadan dinleyin", "Bağımsızlığını desteklerken sınırları net belirleyin", "Sosyal medya kullanımını birlikte planladığınız kurallarla düzenleyin", "Fiziksel aktiviteyi teşvik edin"],
        "e": "Birlikte yeni dönem hedeflerini yazın ve görünür bir yere asılacak bir 'hedef panosu' hazırlayın.",
    },
    ("Lise", 9): {
        "g": "Lise yılları kimlik oluşturma, kariyer keşfi ve gelecek planlaması açısından en kritik dönemdir. Bu ay uyum sürecinin yanı sıra akademik ve kariyer hedefleri üzerine odaklanıyoruz.",
        "b": [
            ("Lise Yaşamına Uyum", "Yeni ders yükleri, sınav sistemleri ve artan sorumluluklar lise öğrencilerini zorlayabilir. Etkili zaman yönetimi ve planlama bu sürecin anahtarıdır. Kendi programını yapabilen genç, başarıya daha yakındır."),
            ("Kariyer Keşfi", "Lise yılları meslekleri tanıma, güçlü yönleri keşfetme ve ilgi alanlarını belirleme zamanıdır. Kariyer günleri, mesleki tanıtımlar ve bireysel görüşmeler bu keşif yolculuğunda rehber olacaktır."),
            ("Stres Yönetimi", "Akademik baskı, sosyal beklentiler ve gelecek kaygısı gençlerde strese yol açabilir. Nefes egzersizleri, fiziksel aktivite ve düzenli uyku sağlıklı başa çıkma stratejilerinin temelidir."),
        ],
        "v": ["Gencin kendi kararlarını almasına fırsat verin", "Başarıyı sadece notlarla ölçmeyin, çabayı takdir edin", "Üniversite ve meslek araştırmasını birlikte yapın", "Arkadaş çevresini tanıyın, eve davet edin"],
        "e": "Gencin kendine 5 yıl sonrasına bir 'Gelecek Ben' mektubu yazmasını sağlayın ve zarfı birlikte saklayın.",
    },
    # ═══════════════ EKİM (10) ═══════════════
    ("Anaokulu", 10): {
        "g": "Ekim ayında çocuklarımız okul ortamına alışmaya başlıyor ve ilk gerçek arkadaşlıklarını kuruyor. Paylaşma, sıra bekleme ve birlikte oynama becerileri bu dönemde temel kazanımlardır.",
        "b": [
            ("Paylaşmayı Öğrenmek", "Oyuncaklarını ve materyalleri paylaşmak küçük çocuklar için zor olabilir. Bu beceri doğuştan gelmez, öğrenilir. Evde kardeşlerle veya ebeveynle paylaşma oyunları oynamak okuldaki uyumu kolaylaştırır."),
            ("İlk Arkadaşlıklar", "Çocuğunuz belki ilk gerçek arkadaşını bu dönemde edinecek. Arkadaşlık kavramı bu yaşta henüz gelişmektedir; bazen kavga edip hemen barışmaları normaldir. Müdahale etmek yerine yönlendirmek daha etkilidir."),
            ("Duygularını İfade Etme", "Mutluluk, kızgınlık, üzüntü gibi temel duyguları tanımak ve uygun şekilde ifade etmek sosyal becerilerin temelidir. Duygu kartları ve hikâyeler bu farkındalığı geliştirmede etkilidir."),
        ],
        "v": ["Evde paylaşma ve sıra bekleme oyunları oynayın", "Çocuğunuzun arkadaşlarının isimlerini öğrenin", "Duygu ifadesi için 'Sen şu an nasıl hissediyorsun?' sorusunu kullanın", "Parkta veya evde diğer çocuklarla oynama fırsatları yaratın"],
        "e": "Kartondan duygu yüzleri (mutlu, üzgün, kızgın, şaşkın) kesin ve günlük olaylar üzerinden hangi duyguyu hissettiğini sorun.",
    },
    ("İlkokul", 10): {
        "g": "Arkadaşlık ilişkileri ilkokul döneminde çocuğun okula bağlılığını ve mutluluğunu doğrudan etkiler. Bu ay iyi bir arkadaş olmanın ve çatışmaları sağlıklı çözmenin yollarını keşfediyoruz.",
        "b": [
            ("İyi Arkadaş Olmak", "Dinlemek, destek olmak, sözünde durmak ve hata yapınca özür dilemek iyi arkadaşlığın temel taşlarıdır. Çocuklara bu becerileri öğretmek onların sosyal yaşamını zenginleştirir."),
            ("Çatışma Çözme", "Arkadaşlar arasında anlaşmazlıklar doğaldır. Önemli olan bu durumları şiddet veya dışlama yerine konuşarak, uzlaşarak çözmektir. 'Ben dili' kullanmayı öğretmek en etkili yöntemdir."),
            ("Farklılıklara Saygı", "Her çocuk farklıdır ve bu farklılıklar zenginliktir. Farklı kültürler, yetenekler ve ilgi alanlarına saygı duymak empati gelişiminin temelidir."),
        ],
        "v": ["Çocuğunuzla 'iyi arkadaş nasıl olunur' konusunu konuşun", "Arkadaş sorunlarında çözümü önce kendisinin bulmasını teşvik edin", "Evde misafir çocuk ağırlayarak sosyal ortam yaratın", "Farklılıklara saygıyı günlük yaşamda modelleyin"],
        "e": "Çocuğunuzla bir 'Arkadaşlık Ağacı' çizin: dallarına arkadaşlarının isimlerini ve onları sevdiği özellikleri yazın.",
    },
    ("Ortaokul", 10): {
        "g": "Ergenlik döneminde akran ilişkileri hayati önem kazanır. Gençler kimliklerini arkadaş grupları üzerinden şekillendirmeye başlar. Sağlıklı ilişkiler kurmak ve akran baskısıyla başa çıkmak bu ayın odak noktasıdır.",
        "b": [
            ("Akran Baskısı", "Giyim, konuşma tarzı, sosyal medya kullanımı gibi konularda arkadaş grubunun etkisi artar. Gencin 'hayır' diyebilme becerisini geliştirmek onu olumsuz etkilerden korur."),
            ("Dijital Arkadaşlık", "Sosyal medya ve mesajlaşma uygulamaları arkadaşlık dinamiklerini değiştirdi. Siber zorbalık, dışlanma ve FOMO gibi riskler konusunda gençleri bilinçlendirmek gerekir."),
            ("Sağlıklı Sınırlar", "Hem fiziksel hem duygusal sınırlar koymayı öğrenmek ergenlik döneminin önemli kazanımlarından biridir. Kendi sınırlarını bilmek ve başkalarının sınırlarına saygı duymak sağlıklı ilişkilerin temelidir."),
        ],
        "v": ["Gencin arkadaş grubunu yargılamadan tanıyın", "Akran baskısı senaryoları üzerinden rol yapma oyunları oynayın", "Sosyal medyada geçirilen süreyi birlikte takip edin", "Kendinizden ergenlik dönemi arkadaşlık örnekleri paylaşın"],
        "e": "Aile olarak 'Dijital Detoks Akşamı' düzenleyin: telefonları kapatıp birlikte masa oyunu oynayın.",
    },
    ("Lise", 10): {
        "g": "Lise çağında arkadaşlıklar derinleşir ve romantik ilişkiler gündeme gelebilir. Sağlıklı iletişim becerileri, empati ve karşılıklı saygı bu dönemde kazandırılması gereken temel yetkinliklerdir.",
        "b": [
            ("İletişim Becerileri", "Aktif dinleme, empati kurma, duyguları yapıcı şekilde ifade etme ve çatışmayı yönetme becerileri hem arkadaşlık hem iş yaşamı için vazgeçilmezdir. Bu beceriler pratikle gelişir."),
            ("Sağlıklı İlişkiler", "İster arkadaşlık ister romantik olsun, sağlıklı ilişkiler karşılıklı saygı, güven ve iletişim üzerine kuruludur. Kontrol etme, kıskançlık ve manipülasyon uyarı işaretleridir."),
            ("Sosyal Sorumluluk", "Topluma katkıda bulunmak gençlerin öz değer duygusunu güçlendirir. Gönüllülük projeleri, toplum hizmeti ve dayanışma etkinlikleri bu bilinci geliştirir."),
        ],
        "v": ["Gencin özel alanına saygı gösterin ama iletişimi açık tutun", "Sağlıklı ilişki özelliklerini aile içinde modelleyin", "Gönüllülük projelerine birlikte katılın", "Gencin duygusal zekâsını destekleyen kitaplar önerin"],
        "e": "Gençle birlikte bir toplum hizmeti projesi planlayın — huzurevi ziyareti, çevre temizliği veya hayvan barınağı gibi.",
    },
    # ═══════════════ KASIM (11) ═══════════════
    ("Anaokulu", 11): {
        "g": "Kasım ayında çocuklarımız sorumluluk kavramıyla tanışıyor. Kendi eşyalarına sahip çıkma, basit görevleri yerine getirme ve düzen alışkanlığı kazanma bu dönemin hedefleridir.",
        "b": [
            ("Küçük Sorumluluklar", "Oyuncaklarını toplamak, çantasını asmak, ayakkabılarını çıkarmak gibi küçük görevler çocuğun sorumluluk duygusunu geliştirir. Bu görevleri oyunlaştırmak motivasyonu artırır."),
            ("Düzen ve Rutin", "Çocuklar tutarlı rutinlerle güvende hissederler. Sabah rutini, yemek zamanı kuralları ve yatma saati düzeni çocuğun öz düzenleme becerisini güçlendirir."),
            ("Atatürk ve Değerler", "10 Kasım ve Cumhuriyet Bayramı vesilesiyle çocuklara yaşına uygun şekilde vatan sevgisi, barış ve birlikte yaşama değerleri aktarılır."),
        ],
        "v": ["Evde yaşına uygun küçük görevler verin ve başardığında takdir edin", "Görev çizelgesi oluşturup tamamladıklarını işaretlemesini sağlayın", "Düzeni sağlamak için sabit rutinler belirleyin", "Atatürk hakkında yaşına uygun hikâyeler anlatın"],
        "e": "Bir 'Sorumluluk Yıldızı' tablosu yapın: her gün görevini yapınca yıldız yapıştırsın, hafta sonunda küçük bir ödül kazansın.",
    },
    ("İlkokul", 11): {
        "g": "Sorumluluk ve öz düzenleme ilkokul döneminde akademik başarının temelini oluşturur. Bu ay öğrencilerimiz ödev takibi, düzenli çalışma ve zaman yönetimi konularında desteklenmektedir.",
        "b": [
            ("Ödev Alışkanlığı", "Düzenli bir çalışma saati ve yeri belirlemek ödev alışkanlığının ilk adımıdır. Çocuğun ödevini kendi başına yapması, zorlandığında yardım istemesi teşvik edilmelidir."),
            ("Zaman Farkındalığı", "Saat kavramı ve zaman yönetimi ilkokul çağında gelişmeye başlar. Basit bir günlük program yaparak zamanını planlama becerisini destekleyebilirsiniz."),
            ("10 Kasım ve Cumhuriyet Değerleri", "Atatürk'ün eğitime verdiği önem, cumhuriyet değerleri ve yurttaşlık bilinci bu ay işlenen konular arasındadır. Çocuklarımız sorumlu birer birey olma yolunda ilerlemektedir."),
        ],
        "v": ["Her gün aynı saatte ödev çalışma rutini oluşturun", "Ödevini yapması için ödül-ceza yerine iç motivasyonu destekleyin", "Çocuğunuzla birlikte haftalık plan yapın", "Atatürk ve cumhuriyet konulu kitaplar birlikte okuyun"],
        "e": "Çocuğunuzla birlikte bir 'Haftalık Görev Planı' hazırlayın: ödev saatleri, spor, oyun ve aile zamanını renklendirerek planlayın.",
    },
    ("Ortaokul", 11): {
        "g": "Ortaokul öğrencileri artan ders yükü ve sınav baskısıyla karşı karşıyadır. Öz düzenleme, zaman yönetimi ve planlama becerileri bu dönemde kazandırılması gereken kritik yetkinliklerdir.",
        "b": [
            ("Etkili Çalışma Yöntemleri", "Her öğrencinin öğrenme stili farklıdır: görsel, işitsel veya kinestetik. Kendi öğrenme stilini keşfeden öğrenci daha verimli çalışır. Pomodoro tekniği, not alma stratejileri ve aktif tekrar etkili yöntemler arasındadır."),
            ("Sınav Kaygısı ile Başa Çıkma", "Sınav öncesi hafif kaygı performansı artırırken aşırı kaygı engelleyicidir. Nefes egzersizleri, pozitif iç konuşma ve yeterli uyku kaygıyı yönetmenin temel araçlarıdır."),
            ("Sorumluluk Bilinci", "Ödevlerini takip etme, sınıf kurallarına uyma ve topluma karşı görevlerini bilme bu dönemde içselleştirilmesi gereken değerlerdir."),
        ],
        "v": ["Ders çalışma ortamını sessiz ve düzenli tutun", "Sınav kaygısı belirtilerini fark edin: uyku bozuklukları, iştahsızlık, gerginlik", "Başarıyı yalnızca notla ölçmeyin, çabayı ve gelişimi takdir edin", "Gencin kendi çalışma planını yapmasını destekleyin"],
        "e": "Birlikte bir 'Çalışma Yöntemi Deneyi' yapın: bir hafta farklı çalışma tekniklerini deneyin ve hangisinin en etkili olduğunu keşfedin.",
    },
    ("Lise", 11): {
        "g": "Lise öğrencileri için Kasım ayı akademik yoğunluğun arttığı, sınavların yoğunlaştığı ve zaman yönetiminin kritik hâle geldiği bir dönemdir. Öz düzenleme becerileri bu dönemde hayat kurtarır.",
        "b": [
            ("Akademik Planlama", "Ders çalışma takvimi, sınav programı ve proje teslim tarihlerini tek bir planda birleştirmek büyük resmi görmek açısından önemlidir. Dijital araçlar veya klasik ajanda bu planlamayı kolaylaştırır."),
            ("Motivasyon ve Hedef", "Uzun vadeli hedefler (üniversite, kariyer) ile kısa vadeli hedefleri (sınavlar, projeler) ilişkilendirmek motivasyonu artırır. 'Bu dersi neden çalışıyorum?' sorusunun cevabını bulmak önemlidir."),
            ("10 Kasım ve Liderlik", "Atatürk'ün liderlik özellikleri, vizyoner düşüncesi ve eğitime verdiği değer gençler için ilham kaynağıdır. Liderlik sadece yönetmek değil, sorumluluk almak ve örnek olmaktır."),
        ],
        "v": ["Gencin kendi çalışma planını yapmasına güvenin, sadece rehberlik edin", "Sınav dönemlerinde uyku ve beslenme düzenine dikkat edin", "Başarısızlığı felaketleştirmeyin, öğrenme fırsatı olarak çerçeveleyin", "Gencin sosyal hayatını da korumasını destekleyin"],
        "e": "Gençle birlikte 'Etkili Zaman Yönetimi Matrisi' oluşturun: acil/önemli, önemli/acil değil, acil/önemli değil kategorileriyle görevleri sınıflandırın.",
    },
    # ═══════════════ ARALIK (12) ═══════════════
    ("Anaokulu", 12): {
        "g": "Aralık ayı empati ve yardımseverlik temasıyla çocuklarımızın duygusal gelişimini destekliyoruz. Başkalarının duygularını anlama ve yardım etme isteği bu yaşlarda atılan küçük adımlarla başlar.",
        "b": [
            ("Duyguları Tanıma", "Mutluluk, üzüntü, korku, kızgınlık gibi temel duyguları tanımak empati gelişiminin ilk adımıdır. Hikâye kitaplarındaki karakterlerin duygularını konuşmak bu farkındalığı artırır."),
            ("Yardım Etme Sevinci", "Masayı kurmaya yardım etmek, arkadaşına oyuncak vermek gibi küçük yardım davranışları çocuğun öz değer duygusunu güçlendirir. Yardım etmenin verdiği mutluluğu deneyimlemek önemlidir."),
            ("Paylaşma Kültürü", "Yıl sonu yaklaşırken paylaşma, dayanışma ve birlikte olma değerleri ön plana çıkar. Çocuğunuzla birlikte ihtiyaç sahiplerine yardım etmek güçlü bir değer eğitimidir."),
        ],
        "v": ["Hikâye okurken karakterlerin duygularını sorun: 'Sence nasıl hissetti?'", "Yardımseverlik davranışlarını takdir edin ve pekiştirin", "Birlikte kullanılmayan oyuncakları ihtiyaç sahiplerine bağışlayın", "Aile olarak dayanışma etkinliğine katılın"],
        "e": "Birlikte bir 'Yardım Kutusu' hazırlayın: kullanılmayan oyuncak ve kıyafetleri toplayıp ihtiyacı olanlara ulaştırın.",
    },
    ("İlkokul", 12): {
        "g": "Empati ve yardımseverlik değerleri bu ay öğrencilerimizin odak noktasıdır. Başkalarının perspektifinden bakabilme, yardım eli uzatma ve toplumsal dayanışma bilinci geliştirilmektedir.",
        "b": [
            ("Empati Nedir?", "Kendini başkasının yerine koyabilmek, onun duygularını anlayabilmek empati olarak tanımlanır. Empati kurabilen çocuklar daha güçlü sosyal ilişkiler kurar ve zorbalık davranışlarından uzak durur."),
            ("Gönüllülük ve Dayanışma", "Sınıfça bir yardım projesi organize etmek, ihtiyaç sahibi ailelere destek olmak veya çevre temizliği yapmak çocuklara toplumsal sorumluluk bilinci kazandırır."),
            ("İnsan Hakları Günü", "10 Aralık İnsan Hakları Günü vesilesiyle çocuklara temel haklar ve sorumluluklar hakkında yaşına uygun bilgiler aktarılır. Her insanın eşit ve değerli olduğu vurgulanır."),
        ],
        "v": ["Empati kurmayı günlük hayatta modelleyin", "Çocuğunuzla birlikte bir yardım projesine katılın", "Farklı yaşam koşullarından bahseden hikâyeler okuyun", "Çocuğunuzun iyilik yapmasını teşvik edin ve takdir edin"],
        "e": "Sınıfça veya aile olarak bir 'İyilik Zinciri' başlatın: her gün bir iyilik yapın ve kaydedin.",
    },
    ("Ortaokul", 12): {
        "g": "Ergenlik döneminde empati gelişimi derinleşir ve toplumsal farkındalık artar. Bu ay gençlerimizin perspektif alma, toplumsal sorumluluk ve gönüllülük konularında bilinçlenmelerini hedefliyoruz.",
        "b": [
            ("Perspektif Alma", "Farklı bakış açılarını anlayabilmek, önyargılardan arınabilmek ve eleştirel düşünce geliştirebilmek ergenlik döneminin önemli kazanımlarıdır. Tartışma ve münazara etkinlikleri bu beceriyi güçlendirir."),
            ("Toplumsal Duyarlılık", "Çevresel sorunlar, eşitsizlik, yoksulluk gibi toplumsal konulara duyarlı gençler geleceğin sorumlu vatandaşları olacaktır. Farkındalık projeleri bu duyarlılığı besler."),
            ("Değerler ve Etik", "Doğruluk, adalet, saygı ve sorumluluk gibi temel değerler bu dönemde içselleştirilir. Etik ikilemler üzerinde düşünmek ahlâki gelişimi destekler."),
        ],
        "v": ["Toplumsal konular hakkında gencin fikirlerini dinleyin", "Birlikte bir gönüllülük projesine katılın", "Haberleri birlikte izleyin ve farklı bakış açılarını tartışın", "Gencin empati kurmasını destekleyen film ve kitaplar önerin"],
        "e": "Aile olarak bir gönüllülük projesi seçin: huzurevi ziyareti, çevre temizliği veya sokak hayvanlarına yardım gibi.",
    },
    ("Lise", 12): {
        "g": "Lise çağında gençler toplumsal sorunlara karşı duyarlılık geliştirir ve aktif vatandaşlık bilinci oluşmaya başlar. Empati, sosyal sorumluluk ve etik değerler bu ayın temasıdır.",
        "b": [
            ("Sosyal Sorumluluk Projeleri", "Toplum hizmeti projeleri gençlerin empati, liderlik ve takım çalışması becerilerini geliştirirken üniversite başvurularında da önemli bir artı sağlar."),
            ("Küresel Vatandaşlık", "Dijital çağda gençler küresel sorunlardan haberdar ve etkilenmektedir. İklim değişikliği, insan hakları ve kültürlerarası diyalog gibi konularda bilinçli olmak önemlidir."),
            ("Yıl Sonu Değerlendirmesi", "Akademik ve kişisel gelişim açısından yılın ilk yarısını değerlendirmek, başarıları kutlamak ve gelişim alanlarını belirlemek ikinci yarı için motivasyon sağlar."),
        ],
        "v": ["Gencin toplumsal projelerine destek olun", "Etik konuları aile sofrasında tartışın", "Yıl sonu değerlendirmesini birlikte yapın, eleştiri yerine yönlendirin", "Gencin başarılarını küçük de olsa kutlayın"],
        "e": "Gençle birlikte bir 'Yıl Değerlendirme Günlüğü' yazın: yılın en güzel anıları, öğrenilen dersler ve yeni yıl hedefleri.",
    },
    # ═══════════════ OCAK (1) ═══════════════
    ("Anaokulu", 1): {
        "g": "Yeni yıl yeni umutlar demek! Ocak ayında çocuklarımızla küçük hedefler koymayı ve 'yapabilirim' duygusunu güçlendirmeyi hedefliyoruz. Her küçük başarı büyük özgüvenin yapı taşıdır.",
        "b": [
            ("Küçük Hedefler Büyük Mutluluklar", "Ayakkabısını kendi bağlamak, adını yazmak veya puzzle tamamlamak gibi küçük hedefler koymak çocuğun başarı duygusunu güçlendirir. Hedefi gerçekleştirdiğinde duyduğu gurur iç motivasyonu besler."),
            ("Yapabilirim Duygusu", "Çocuğunuza 'Yapamıyorum' yerine 'Henüz yapamıyorum ama öğreneceğim' demeyi öğretin. Büyüme zihniyeti küçük yaşlarda atılan tohumlarla gelişir."),
            ("Kış Mevsimi ve Sağlık", "Kış aylarında hijyen alışkanlıkları, doğru giyinme ve sağlıklı beslenme konuları çocuklarla paylaşılır. El yıkama, hapşırırken ağzını kapatma gibi alışkanlıklar pekiştirilir."),
        ],
        "v": ["Çocuğunuza basit ama ulaşılabilir hedefler koymasına yardımcı olun", "'Aferin, başardın!' yerine 'Çok çalıştın, emek verdin!' deyin", "Kış aylarında düzenli uyku ve beslenmeye özen gösterin", "Her akşam günün en güzel olayını birlikte hatırlayın"],
        "e": "Bir 'Başarı Kavanozuna' her gün başarılan bir şeyi kâğıda yazıp atın, ay sonunda birlikte okuyun.",
    },
    ("İlkokul", 1): {
        "g": "Yeni yılla birlikte ikinci yarıyılın planlaması başlıyor. Bu ay öğrencilerimizle hedef belirleme, motivasyon ve olumlu düşünce üzerine çalışıyoruz.",
        "b": [
            ("Dönem Değerlendirmesi", "İlk yarıyılı değerlendirmek, başarıları görmek ve gelişim alanlarını belirlemek önemlidir. Çocuğunuzla birlikte karnedeki güçlü ve geliştirilecek alanları konuşun."),
            ("Hedef Belirleme", "İkinci yarıyıl için somut ve ulaşılabilir hedefler koymak motivasyonu artırır. 'Matematik çarpım tablosunu öğreneceğim' gibi ölçülebilir hedefler daha etkilidir."),
            ("Pozitif İç Konuşma", "Çocuğunuza olumsuz düşüncelerini fark etmeyi ve olumluya çevirmeyi öğretin. 'Ben bunu hiç yapamam' yerine 'Bu zor ama deneyeceğim' demek büyük fark yaratır."),
        ],
        "v": ["Karneyi ceza aracı olarak kullanmayın, gelişim fırsatı olarak görün", "Çocuğunuzla birlikte 2-3 somut dönem hedefi belirleyin", "Olumlu iç konuşmayı siz de modelleyin", "Başarıları küçük de olsa kutlayın"],
        "e": "Birlikte bir 'Yeni Dönem Hedef Posteri' hazırlayın: hedefleri renkli kalemlerle yazın ve odaya asın.",
    },
    ("Ortaokul", 1): {
        "g": "Yeni yıl ve ikinci dönem planlaması bu ayın odağıdır. SMART hedefler belirleme, motivasyon kaynakları bulma ve akademik strateji oluşturma konularında gençlerimizi destekliyoruz.",
        "b": [
            ("SMART Hedefler", "Spesifik, Ölçülebilir, Ulaşılabilir, Gerçekçi ve Zamanlı hedefler koymak başarı oranını artırır. 'Daha çok çalışacağım' yerine 'Her gün 45 dakika matematik çalışacağım' daha etkilidir."),
            ("Motivasyon Kaynakları", "İçsel motivasyon (öğrenme keyfi, merak) dışsal motivasyondan (ödül, not) daha sürdürülebilirdir. Gencin ilgi alanlarıyla dersleri ilişkilendirmek motivasyonu artırır."),
            ("Sınav Hazırlık Stratejisi", "Düzenli tekrar, özetleme, soru çözme ve grup çalışması etkili sınav hazırlık yöntemleridir. Son gece çalışması yerine dağıtılmış tekrar daha kalıcı öğrenme sağlar."),
        ],
        "v": ["Gencin kendi hedeflerini belirlemesine alan tanıyın", "Motivasyon düşüklüğünde baskı yerine anlayış gösterin", "Çalışma ortamını birlikte düzenleyin", "Karnedeki notları gencin kendi değerlendirmesiyle konuşun"],
        "e": "Gençle 'Vizyon Panosu' oluşturun: dergi kesikleri, fotoğraflar ve yazılarla hedeflerini görselleştirin.",
    },
    ("Lise", 1): {
        "g": "Lise öğrencileri için Ocak ayı hem dönem değerlendirmesi hem de gelecek planlaması açısından kritik bir dönemdir. Üniversite hedefleri, kariyer planları ve kişisel gelişim bu ayın konularıdır.",
        "b": [
            ("Dönem Analizi", "İlk dönem performansını analiz etmek, güçlü ve zayıf yönleri belirlemek ikinci dönem stratejisini oluşturmanın temelidir. Not ortalamasının yanı sıra çalışma alışkanlıkları ve sosyal gelişim de değerlendirilmelidir."),
            ("Üniversite ve Kariyer", "Üniversite tercihleri, bölüm araştırması ve kariyer planlaması lise yıllarında şekillenmeye başlar. Açık günler, tanıtım etkinlikleri ve mesleki danışmanlık bu süreçte yol göstericidir."),
            ("Kişisel Gelişim", "Kitap okuma, yeni beceriler öğrenme, gönüllülük çalışmaları ve hobi geliştirme gencin çok yönlü gelişimini destekler."),
        ],
        "v": ["Gencin üniversite ve kariyer araştırmasına destek olun", "Baskı kurmak yerine birlikte plan yapın", "Gencin sosyal ve kişisel gelişimini de önemseyin", "İkinci dönem için gerçekçi beklentiler oluşturun"],
        "e": "Gençle birlikte ilgi duyduğu 3 meslek alanını araştırın: ne iş yapar, hangi eğitim gerekir, kariyer olanakları nelerdir.",
    },
    # ═══════════════ ŞUBAT (2) ═══════════════
    ("Anaokulu", 2): {
        "g": "Şubat ayı sevgi, saygı ve değerler temasıyla çocuklarımızın duygusal zekâsını geliştirmeye devam ediyoruz. Sevgiyi ifade etme, nazik olma ve başkalarına saygı duyma bu ayın kazanımlarıdır.",
        "b": [
            ("Sevgiyi İfade Etmek", "Her çocuğun sevgi dili farklıdır: kimisi sarılmayı, kimisi birlikte vakit geçirmeyi, kimisi iltifat almayı sever. Çocuğunuzun sevgi dilini keşfetmek ilişkinizi güçlendirir."),
            ("Nazik Sözler", "Teşekkür ederim, lütfen, özür dilerim gibi nazik ifadeler sosyal ilişkilerin temelidir. Bu ifadeleri çocuğun günlük yaşamında doğal hâle getirmek önemlidir."),
            ("Saygı Duygusu", "Büyüklere, arkadaşlara, hayvanlara ve doğaya saygı duymak çocuğun değer sisteminin temelini oluşturur."),
        ],
        "v": ["Her gün çocuğunuza sevgiyi sözel ve fiziksel olarak ifade edin", "Nazik sözleri siz de günlük hayatınızda kullanın", "Çocuğunuzla 'Sevgi nedir?' konusunu konuşun", "Birlikte sevdiklerinize küçük sürprizler hazırlayın"],
        "e": "Birlikte aile üyeleri ve arkadaşlar için el yapımı sevgi kartları hazırlayın.",
    },
    ("İlkokul", 2): {
        "g": "Sevgi, saygı ve hoşgörü bu ayın temasıdır. Farklılıklara değer verme, nazik olma ve sağlıklı ilişkiler kurma konularında çocuklarımızı destekliyoruz.",
        "b": [
            ("Saygı ve Hoşgörü", "Her insanın farklı olduğu ve bu farklılıkların zenginlik olduğu çocuklara küçük yaştan öğretilmelidir. Dini, kültürel, fiziksel farklılıklara saygı duymak empati gelişiminin önemli bir adımıdır."),
            ("Zorbalıkla Mücadele", "Fiziksel, sözel veya siber zorbalık her yaşta ciddi bir sorundur. Çocuğunuza zorbalığa maruz kalırsa veya tanık olursa ne yapması gerektiğini öğretin."),
            ("Öz Sevgi", "Kendini sevmek ve kabul etmek, başkalarını sevmenin ön koşuludur. Çocuğunuzun güçlü yönlerini fark etmesini sağlayın ve onu olduğu gibi kabul ettiğinizi hissettirin."),
        ],
        "v": ["Çocuğunuza koşulsuz sevgiyi hissettirin", "Zorbalık belirtilerine dikkat edin: okula gitmek istememe, huzursuzluk", "Farklılıklara saygıyı günlük yaşamda gösterin", "Çocuğunuzun güçlü yönlerini ona sık sık hatırlatın"],
        "e": "Bir 'Güçlü Yönler Güneşi' çizin: ortaya çocuğun adını yazın, ışınlarına güçlü yönlerini ve yeteneklerini ekleyin.",
    },
    ("Ortaokul", 2): {
        "g": "Ergenlik döneminde duygusal zekâ gelişimi, sağlıklı ilişkiler kurma ve değerler eğitimi önemli konular arasındadır. Bu ay empati, saygı ve duygusal farkındalık üzerine çalışıyoruz.",
        "b": [
            ("Duygusal Zekâ", "Duygularını tanıma, yönetme ve başkalarının duygularını anlama becerileri akademik başarı kadar hayat başarısı için de belirleyicidir. Duygusal zekâ geliştirilebilir bir beceridir."),
            ("Sağlıklı İlişkiler", "Ergenlikte arkadaşlık ve romantik ilişkiler yoğun duygular yaşatır. Sağlıklı sınırlar koymak, iletişim kurmak ve kendi değerlerini korumak bu dönemde öğrenilmesi gereken becerilerdir."),
            ("Siber Zorbalık", "Dijital ortamda gerçekleşen zorbalık gençler arasında yaygınlaşmaktadır. Farkındalık, raporlama ve destek arama yolları hakkında gençlerin bilgilendirilmesi önemlidir."),
        ],
        "v": ["Gencin duygularını yargılamadan dinleyin", "Sağlıklı ilişki özelliklerini aile içinde modelleyin", "Siber zorbalık konusunda açık konuşun ve güvenli yardım kanallarını anlatın", "Gencin öz değerini pekiştirin"],
        "e": "Gençle birlikte 'Duygu Günlüğü' tutun: her gün yaşadığı en yoğun duyguyu ve nedenini kısaca yazması yeterli.",
    },
    ("Lise", 2): {
        "g": "Değerler eğitimi, etik düşünce ve sağlıklı ilişkiler lise çağında derinleşen konulardır. Bu ay gençlerimizle sevgi, saygı, adalet ve bireysel değerler üzerine çalışıyoruz.",
        "b": [
            ("Kişisel Değerler Sistemi", "Gençlik yılları kendi değerler sisteminizi oluşturma zamanıdır. Hangi değerler sizin için önemli? Dürüstlük, adalet, özgürlük, başarı, aile... Bu değerleri belirlemek karar verme süreçlerinde pusula görevi görür."),
            ("Romantik İlişkiler ve Sınırlar", "Lise çağında romantik ilişkiler gençlerin gündemindedir. Sağlıklı bir ilişkinin temel unsurları: karşılıklı saygı, güven, iletişim ve bireysel alanın korunmasıdır."),
            ("Dijital Etik", "Çevrimiçi davranışlar, gizlilik, telif hakkı ve dijital ayak izi konularında bilinçli olmak dijital vatandaşlığın gereğidir."),
        ],
        "v": ["Değerler konusunu aile yemeğinde tartışın", "Gencin kendi değerlerini keşfetmesine alan tanıyın", "Dijital ayak izi konusunda farkındalık oluşturun", "Sağlıklı ilişki modellerini aile içinde yaşatın"],
        "e": "Gençle 'Kişisel Değerler Kartı' oluşturun: en önemli 5 değerini sıralasın ve her birinin hayatında nasıl yaşandığını örneklesin.",
    },
    # ═══════════════ MART (3) ═══════════════
    ("Anaokulu", 3): {
        "g": "Mart ayı 'Ben özelim!' temasıyla çocuklarımızın özgüvenini güçlendirmeye odaklanıyoruz. Her çocuğun eşsiz olduğunu, güçlü yönlerinin bulunduğunu keşfetmesi bu ayın hedefidir.",
        "b": [
            ("Ben Özelim", "Her çocuk farklı yeteneklere, ilgi alanlarına ve özelliklere sahiptir. Bu farklılıkları kutlamak çocuğun benlik değerini güçlendirir. 'Sen çok özelsin' mesajını sık sık verin."),
            ("Güçlü Yönlerimi Tanıyorum", "Resim yapmakta, şarkı söylemekte, koşmakta veya hikâye anlatmakta iyi olmak... Her çocuğun parlayan bir yönü vardır. Bu güçlü yönleri keşfetmek ve desteklemek özgüvenin temelidir."),
            ("Cesaret ve Deneme", "Yeni şeyler denemekten korkmamak, hata yapmanın öğrenmenin bir parçası olduğunu bilmek küçük yaşta kazandırılması gereken önemli bir tutumdur."),
        ],
        "v": ["Çocuğunuzu başka çocuklarla kıyaslamaktan kaçının", "Güçlü yönlerini fark ettikçe ona söyleyin", "Yeni deneyimler için cesaretlendirin ama zorlacı olmayın", "Hata yaptığında 'Olur, birlikte düzeltiriz' deyin"],
        "e": "Çocuğunuzla bir 'Ben Özelim' posteri hazırlayın: fotoğrafı, sevdiği şeyler, en iyi yaptığı şeyler ve hayalleri.",
    },
    ("İlkokul", 3): {
        "g": "Özgüven geliştirme ve bireysel farklılıkları tanıma bu ayın temasıdır. Çocuklarımız yeteneklerini keşfederken aynı zamanda başkalarının farklılıklarına saygı duymayı öğreniyor.",
        "b": [
            ("Özgüven Nasıl Gelişir?", "Özgüven başarı deneyimleriyle, koşulsuz kabul ve yapıcı geri bildirimle gelişir. Çocuğa 'akıllısın' yerine 'çok çalıştın' demek çaba odaklı bir yaklaşım sunar."),
            ("Yetenekleri Keşfetme", "Her çocuk farklı alanlarda yeteneklidir. Sanat, müzik, spor, fen, edebiyat... Farklı aktiviteler deneyerek çocuğun yeteneklerini keşfetmesine fırsat tanıyın."),
            ("8 Mart ve Eşitlik", "Dünya Kadınlar Günü vesilesiyle eşitlik, saygı ve herkesin değerli olduğu mesajları çocuklarla paylaşılır."),
        ],
        "v": ["Çocuğunuzun güçlü yönlerini vurgulayın, zayıf yönlerini kıyaslama aracı yapmayın", "Farklı aktiviteler deneme fırsatı yaratın", "Başarısızlıkta cesaretlendirici olun", "Eşitlik değerini evde yaşayarak öğretin"],
        "e": "Çocuğunuzla 'Yetenek Avcısı' oyunu oynayın: bir hafta boyunca her gün farklı bir aktivite deneyin ve en çok hangisini sevdiğini keşfedin.",
    },
    ("Ortaokul", 3): {
        "g": "Ergenlikte özgüven dalgalanmaları, beden imajı kaygıları ve kimlik arayışı yoğun yaşanır. Bu ay gençlerimizin öz kabulünü güçlendirmeyi ve bireysel farklılıkları kutlamayı hedefliyoruz.",
        "b": [
            ("Beden İmajı ve Öz Kabul", "Ergenlikte bedensel değişimler hızla yaşanır ve gençler görünüşleriyle ilgili kaygı duyabilir. Medyadaki gerçekçi olmayan güzellik standartlarını sorgulamak ve kendi bedenini kabul etmek önemlidir."),
            ("Kimlik Gelişimi", "Ben kimim? Ne istiyorum? Neye inanıyorum? Bu sorular ergenliğin temel sorularıdır. Gençlerin farklı rolleri ve kimlikleri denemesi bu dönemin doğal bir parçasıdır."),
            ("Güçlü Yönler ve Büyüme Zihniyeti", "Zekânın ve yeteneklerin sabit olmadığını, çabayla geliştirilebileceğini bilmek büyüme zihniyetinin temelidir. Bu zihniyet başarısızlıkları öğrenme fırsatına dönüştürür."),
        ],
        "v": ["Gencin görünüşüyle ilgili olumsuz yorumlardan kaçının", "Medya okuryazarlığını destekleyin", "Gencin farklı ilgi alanlarını keşfetmesine alan tanıyın", "Koşulsuz kabul mesajını sık sık verin"],
        "e": "Gençle birlikte 'Güçlü Yönler Envanteri' çıkarın: akademik, sosyal, sanatsal, sportif ve kişilik güçlerini listeleyin.",
    },
    ("Lise", 3): {
        "g": "Kimlik gelişimi, öz kabul ve bireysel farklılıklar lise çağının merkezî temalarıdır. Bu ay gençlerimizin kendilerini tanıma, kabul etme ve güçlü yönlerini değerlendirme sürecini destekliyoruz.",
        "b": [
            ("Kimlik ve Özgünlük", "Lise yılları gençlerin kendi kimliklerini oluşturdukları, değerlerini belirlediği ve yaşam felsefelerini şekillendirdiği dönemdir. Başkalarının beklentileri yerine kendi iç sesini dinlemek bu sürecin anahtarıdır."),
            ("Güçlü Yönleri Değerlendirme", "Kariyer seçimi ve gelecek planlamasında güçlü yönlerini tanımak büyük avantaj sağlar. Kişilik testleri, ilgi envanterleri ve rehberlik görüşmeleri bu keşif sürecinde yardımcıdır."),
            ("Kadınlar Günü ve Toplumsal Cinsiyet Eşitliği", "8 Mart Dünya Kadınlar Günü vesilesiyle toplumsal cinsiyet eşitliği, kadın hakları ve fırsat eşitliği konularında farkındalık oluşturulur."),
        ],
        "v": ["Gencin kendini ifade etme biçimine saygı gösterin", "Kariyer keşfi için kişilik ve ilgi testleri önerin", "Toplumsal cinsiyet eşitliğini evde yaşayın", "Gencin kendi kararlarını almasını destekleyin"],
        "e": "Gençle birlikte online bir kişilik testi veya ilgi envanteri yapın ve sonuçları konuşun.",
    },
    # ═══════════════ NİSAN (4) ═══════════════
    ("Anaokulu", 4): {
        "g": "Nisan ayı kitap okuma ve hayal gücü temasıyla çocuklarımızın bilişsel ve dilsel gelişimini destekliyoruz. Hikâye dinlemek, anlatmak ve hayal kurmak bu yaşın en değerli etkinlikleridir.",
        "b": [
            ("Hikâye Dinleme Keyfi", "Yatmadan önce hikâye okumak çocuğun dil gelişimini, hayal gücünü ve dikkat süresini artırır. Sesli okuma sırasında farklı sesler kullanmak ve sorular sormak etkileşimi güçlendirir."),
            ("Hayal Gücü ve Yaratıcılık", "Çocukların hayal dünyası sınırsızdır. Bu hayal gücünü desteklemek problem çözme, yaratıcılık ve esneklik becerilerini geliştirir. Yapılandırılmamış oyun zamanı bu gelişimin temelidir."),
            ("23 Nisan ve Çocuk Hakları", "Ulusal Egemenlik ve Çocuk Bayramı vesilesiyle çocuklara hakları, özgürlükleri ve sorumlulukları yaşına uygun şekilde aktarılır."),
        ],
        "v": ["Her gün en az 15-20 dakika birlikte kitap okuyun", "Çocuğunuzun hikâye anlatmasına fırsat verin", "Kütüphaneye birlikte gidin ve kitap seçmesine izin verin", "Ekran süresi yerine hikâye zamanı oluşturun"],
        "e": "Birlikte bir hikâye uydurun: siz bir cümle söyleyin, çocuğunuz devam ettirsin. Hikâyeyi resimleyerek bir kitapçık yapın.",
    },
    ("İlkokul", 4): {
        "g": "Kitap okuma alışkanlığı ve hayal gücü bu ayın temasıdır. Okuma sevgisi, eleştirel düşünce ve yaratıcılık ilkokul yıllarında atılan temelle hayat boyu sürer.",
        "b": [
            ("Okuma Alışkanlığı", "Düzenli kitap okuyan çocuklar daha geniş kelime hazinesine, daha güçlü anlama becerisine ve daha zengin hayal gücüne sahiptir. Evde bir okuma köşesi oluşturmak bu alışkanlığı destekler."),
            ("Kütüphane Kullanımı", "Okul ve halk kütüphanelerini kullanmak çocuğun kaynaklara erişimini artırır. Kütüphane ziyaretlerini düzenli hâle getirmek öğrenme motivasyonunu güçlendirir."),
            ("23 Nisan Kutlamaları", "Çocuklarımız bu bayramı kutlarken demokrasi, egemenlik ve çocuk hakları konularında farkındalık kazanır."),
        ],
        "v": ["Evde görünür bir kitaplık oluşturun", "Siz de çocuğunuzun yanında kitap okuyun — model olun", "Çocuğunuzun ilgi alanına göre kitap seçimine yardımcı olun", "Okunan kitaplar hakkında sohbet edin"],
        "e": "Bir 'Aile Okuma Maratonu' düzenleyin: hafta sonu herkes kendi kitabını okusun, sonra birbirine anlatsın.",
    },
    ("Ortaokul", 4): {
        "g": "Eleştirel okuma, araştırma becerisi ve bilgi okuryazarlığı dijital çağda her zamankinden önemlidir. Bu ay gençlerimizin okuma alışkanlığını güçlendirmeyi ve bilgi kaynaklarını değerlendirme becerisini geliştirmeyi hedefliyoruz.",
        "b": [
            ("Eleştirel Okuma", "Her okuduğunuza inanmayın, sorgulayın. Yazarın amacı nedir? Kanıtlar ne kadar güçlü? Farklı bakış açıları var mı? Bu sorular eleştirel düşüncenin kapısını açar."),
            ("Dijital Okuryazarlık", "İnternetteki bilgilerin doğruluğunu kontrol etme, güvenilir kaynak seçme ve dezenformasyondan korunma dijital çağın temel becerileridir."),
            ("23 Nisan ve Gençlik", "Millî egemenlik bilinci, demokratik değerler ve gençlerin toplumdaki rolü bu vesileyle tartışılır."),
        ],
        "v": ["Gence ilgi alanına uygun kitap listeleri önerin", "Birlikte kütüphane veya kitap fuarına gidin", "Haberleri birlikte analiz edin, doğruluk kontrolü yapın", "Dijital kaynak değerlendirme konusunda rehberlik edin"],
        "e": "Gençle birlikte bir kitap kulübü başlatın: ayda bir kitap okuyup aile olarak tartışın.",
    },
    ("Lise", 4): {
        "g": "Akademik okuma, araştırma becerileri ve entelektüel merak lise çağında derinleşmelidir. Bu ay gençlerimizin bilgi okuryazarlığı ve eleştirel düşünce becerilerini güçlendiriyoruz.",
        "b": [
            ("Akademik Okuma Stratejileri", "SQ3R (Gözden Geçir, Sorgula, Oku, Tekrarla, Gözden Geçir) gibi sistematik okuma teknikleri akademik metinlerin anlaşılmasını kolaylaştırır."),
            ("Araştırma Becerileri", "Güvenilir kaynak bulma, atıf yapma, bilgi sentezleme ve akademik dürüstlük üniversite hayatına hazırlık için temel becerilerdir."),
            ("Edebiyat ve Empati", "Roman, öykü ve şiir okumak farklı yaşamlara, kültürlere ve perspektiflere pencere açar. Edebiyat empati gelişiminin en güçlü araçlarından biridir."),
        ],
        "v": ["Gencin okuduğu kitaplar hakkında sohbet edin", "Akademik dürüstlük ve kaynak gösterme konusunu konuşun", "Farklı türlerde kitaplar denemeyi teşvik edin", "Gencin kendi okuma listesini oluşturmasını destekleyin"],
        "e": "Gençle birlikte bir 'Okuma Haritası' oluşturun: okunan kitapların haritasını çizin, bağlantılarını kurun.",
    },
    # ═══════════════ MAYIS (5) ═══════════════
    ("Anaokulu", 5): {
        "g": "Mayıs ayı aile bağları ve iletişim temasıyla ailelerimizi güçlendirmeyi hedefliyoruz. Anneler Günü vesilesiyle sevgi ifadesi, kaliteli zaman geçirme ve aile içi iletişim ön plandadır.",
        "b": [
            ("Kaliteli Aile Zamanı", "Çocuğunuzla geçirdiğiniz zamanın niteliği niceliğinden daha önemlidir. Telefonları bırakıp birlikte oynamak, konuşmak ve gülmek güçlü bağlar oluşturur."),
            ("Duyguları Paylaşma", "Aile içinde duyguların açıkça paylaşıldığı bir ortam çocuğun duygusal güvenliğini artırır. 'Seni seviyorum', 'Seninle gurur duyuyorum' gibi ifadeler çocuk için çok değerlidir."),
            ("Anneler Günü", "Annelerin fedakârlıkları, sevgileri ve emekleri bu vesileyle kutlanır. Çocuğunuzla birlikte annesine küçük bir sürpriz hazırlamak sevgi ifadesini somutlaştırır."),
        ],
        "v": ["Her gün en az 20 dakika çocuğunuza bölünmemiş ilgi verin", "Aile yemeklerini birlikte yemeye özen gösterin", "Çocuğunuza 'Seni seviyorum' demeyi ihmal etmeyin", "Birlikte yeni anılar oluşturacak aktiviteler planlayın"],
        "e": "Anne için el yapımı bir hediye hazırlayın: bir resim, bir kart veya küçük bir el izi tablosu.",
    },
    ("İlkokul", 5): {
        "g": "Aile iletişimi ve sağlıklı aile ilişkileri bu ayın temasıdır. Güçlü aile bağları çocuğun akademik başarısını, duygusal sağlığını ve sosyal gelişimini doğrudan etkiler.",
        "b": [
            ("Etkili Aile İletişimi", "Aktif dinleme, göz teması kurma, yargılamadan anlama ve duyguları ifade etme etkili iletişimin temel unsurlarıdır. Çocuğunuzla 'ne yaptın?' yerine 'bugün nasıl hissettin?' diye sorun."),
            ("Aile Kuralları ve Tutarlılık", "Net, tutarlı ve adil kurallar çocuğun güvenlik duygusunu artırır. Kuralları birlikte belirlemek çocuğun uyumunu kolaylaştırır."),
            ("Kardeş İlişkileri", "Kardeş kıskançlığı ve çatışması doğaldır. Her çocuğa özel zaman ayırmak ve kıyaslamaktan kaçınmak kardeş ilişkilerini güçlendirir."),
        ],
        "v": ["Çocuğunuzla günde en az bir öğün birlikte yiyin", "Haftalık aile toplantıları düzenleyin", "Kardeşleri birbirleriyle kıyaslamaktan kaçının", "Sorun çözmeyi birlikte yapın, çocuğu da dahil edin"],
        "e": "Haftalık bir 'Aile Toplantısı' başlatın: herkes sırayla söz alsın, haftanın güzellikleri ve sorunları konuşulsun.",
    },
    ("Ortaokul", 5): {
        "g": "Ergenlikte aile ilişkileri dönüşüm geçirir. Gençler bağımsızlık isterken aileler endişelenir. Bu ay sağlıklı iletişim, karşılıklı saygı ve bağımsızlık-güvenlik dengesini ele alıyoruz.",
        "b": [
            ("Ergenlikte Aile İlişkileri", "Ergen hem bağımsızlık hem güvenlik ister. Bu çelişkili ihtiyaçları anlamak ve dengelemek ailenin en önemli görevidir. Kontrol yerine rehberlik, baskı yerine diyalog tercih edilmelidir."),
            ("İletişim Engelleri", "Eleştiri, suçlama, küçümseme ve savunmacılık iletişimi zehirler. 'Ben dili' kullanmak, aktif dinlemek ve empati kurmak bu engelleri aşmanın yollarıdır."),
            ("Sınır Belirleme Sanatı", "Gence verilen özgürlük kademeli olmalıdır. Güven kazandıkça sınırları genişletmek gencin sorumluluk bilincini geliştirir."),
        ],
        "v": ["Gencin özel alanına saygı gösterin", "Eleştiri yerine 'ben dili' kullanın: 'Sen hep...' yerine 'Ben ... hissediyorum'", "Gencin kararlarını sorgulamak yerine gerekçelerini dinleyin", "Birlikte vakit geçirme fırsatları yaratın ama zorlamayın"],
        "e": "Aile olarak hafta sonu birlikte yapılacak bir aktivite seçin — gencin de fikri alınsın.",
    },
    ("Lise", 5): {
        "g": "Lise çağında gençler yetişkinliğe adım atarken aile dinamikleri yeniden şekillenir. Bağımsızlık ve aile bağları arasındaki denge bu ayın odak noktasıdır.",
        "b": [
            ("Bağımsızlık ve Sorumluluk", "Bağımsızlık kazanmak sorumluluk almayı gerektirir. Gence kademeli olarak daha fazla karar verme özgürlüğü tanımak ve sonuçlarıyla yüzleşmesine izin vermek olgunlaşma sürecini hızlandırır."),
            ("Aile İçi Çatışma Yönetimi", "Anlaşmazlıklar doğaldır; önemli olan çözüm biçimidir. Saygılı tartışma, uzlaşma ve gerektiğinde özür dileme sağlıklı çatışma yönetiminin unsurlarıdır."),
            ("Gelecek Planlamasında Aile Desteği", "Üniversite seçimi, kariyer planlaması gibi konularda aile desteği kritiktir. Yönlendirmek ile dayatmak arasındaki farkı korumak önemlidir."),
        ],
        "v": ["Gencin kararlarına saygı gösterin, hata yapmasına izin verin", "Gelecek planları konusunda baskı yerine rehberlik sunun", "Aile içi sorunları açık ve sakin bir şekilde konuşun", "Gencin başarılarını takdir edin, koşulsuz sevgiyi hissettirin"],
        "e": "Gençle 'Açık Mektup' yazın: birbirinize yazılı olarak duygularınızı, beklentilerinizi ve takdirlerinizi ifade edin.",
    },
    # ═══════════════ HAZİRAN (6) ═══════════════
    ("Anaokulu", 6): {
        "g": "Haziran ayı eğitim yılının sonu ve yaz tatilinin başlangıcıdır. Yıl boyunca kazanılan becerileri değerlendirme ve tatil planlaması bu ayın konularıdır.",
        "b": [
            ("Yıl Sonu Değerlendirmesi", "Çocuğunuz bu yıl çok büyüdü ve gelişti. Yeni arkadaşlar edindi, beceriler kazandı ve bağımsızlığını artırdı. Bu gelişimleri fark etmek ve kutlamak önemlidir."),
            ("Tatil Rutini", "Okul bitse de günlük rutinin tamamen bozulmaması önemlidir. Esnek ama düzenli bir yaz programı çocuğun güvende hissetmesini sağlar."),
            ("Güvenli Yaz", "Yaz aylarında su güvenliği, güneşten korunma ve açık alan güvenliği konularında çocukları bilgilendirmek önemlidir."),
        ],
        "v": ["Yaz tatilinde de düzenli uyku saatlerine dikkat edin", "Ekran süresi artışını kontrol altında tutun", "Doğada vakit geçirme fırsatları yaratın", "Çocuğunuzun yıl içindeki gelişimini takdir edin"],
        "e": "Birlikte bir 'Yaz Tatili Kutusu' hazırlayın: yapılacak aktiviteler listesini renkli kağıtlara yazıp kutuya atın, her gün birini çekin.",
    },
    ("İlkokul", 6): {
        "g": "Eğitim yılının son ayında karne değerlendirmesi, yaz tatili planlaması ve eğlenceli öğrenme etkinlikleri gündemdedir.",
        "b": [
            ("Karne Değerlendirmesi", "Karne bir ceza veya ödül aracı değil, gelişimin fotoğrafıdır. Güçlü yönleri kutlayın, gelişim alanları için birlikte plan yapın. Karnedeki notlar çocuğunuzun değerini belirlemez."),
            ("Verimli Yaz Tatili", "Tatil tamamen boş geçmemeli ama baskıcı da olmamalıdır. Okuma, doğa aktiviteleri, sanat ve spor ile zenginleştirilmiş bir tatil hem eğlenceli hem öğreticidir."),
            ("Güvenli İnternet", "Yaz tatilinde artan ekran süresiyle birlikte internet güvenliği tekrar gündeme gelir. Güvenli kullanım kurallarını birlikte gözden geçirin."),
        ],
        "v": ["Karneyi sakin bir ortamda birlikte değerlendirin", "Yaz okuma listesi oluşturun ve kütüphaneden kitap alın", "Günde en az 1 saat açık havada aktivite planlayın", "Ekran süresi kurallarını tatil için yeniden belirleyin"],
        "e": "Birlikte bir 'Yaz Okuma Pasaportu' hazırlayın: her kitap için bir damga, 10 kitapta özel bir ödül.",
    },
    ("Ortaokul", 6): {
        "g": "Yıl sonu değerlendirmesi ve yaz tatili planlaması ortaokul öğrencileri için hem dinlenme hem gelişim fırsatıdır. Bu ay verimli tatil planlaması ve öz değerlendirme konularını ele alıyoruz.",
        "b": [
            ("Yıl Sonu Öz Değerlendirme", "Akademik başarının yanı sıra sosyal beceriler, kişisel gelişim ve duygusal olgunluk açısından da yılı değerlendirmek önemlidir. Gencin kendi performansını değerlendirmesine fırsat verin."),
            ("Verimli Tatil Planı", "Tatil dinlenme zamanıdır ama tamamen pasif geçirmek de sağlıklı değildir. Hobi geliştirme, kitap okuma, spor yapma ve yeni beceriler öğrenme ile zenginleştirilmiş bir plan idealdir."),
            ("Yaz Kampları ve Aktiviteler", "Spor kampları, bilim atölyeleri, sanat kursları ve doğa kampları gençlerin farklı deneyimler yaşamasına olanak tanır."),
        ],
        "v": ["Gencin kendi tatil planını yapmasını destekleyin", "Zorunlu ders çalışma yerine merak odaklı öğrenmeyi teşvik edin", "Sosyal aktivitelere katılmasını destekleyin", "Ailece tatil planı yaparak birlikte vakit geçirin"],
        "e": "Gençle 'Yaz Hedefleri Listesi' oluşturun: öğrenmek istediği 3 şey, gitmek istediği 3 yer, yapmak istediği 3 aktivite.",
    },
    ("Lise", 6): {
        "g": "Lise öğrencileri için yaz tatili kariyer keşfi, kişisel gelişim ve dinlenme için değerli bir zaman dilimidir. Bu ay gençlerimizin tatili verimli değerlendirmelerini destekliyoruz.",
        "b": [
            ("Akademik Değerlendirme", "Yılın akademik performansını analiz etmek, başarıları kutlamak ve gelişim alanlarını belirlemek gelecek yıl stratejisinin temelini oluşturur."),
            ("Yaz Stajları ve Deneyimler", "Yaz stajları, gönüllülük projeleri ve iş deneyimleri gençlerin kariyer keşfine katkıda bulunur ve üniversite başvurularını güçlendirir."),
            ("Kendini Yenileme", "Tatil, gencin kendini keşfetmesi, yeni hobiler denemesi ve sosyal çevresini genişletmesi için ideal bir zamandır. Dinlenme ve yenilenme akademik performansa olumlu yansır."),
        ],
        "v": ["Gencin yaz planına saygı gösterin ama rehberlik edin", "Staj ve gönüllülük fırsatlarını birlikte araştırın", "Dinlenme ve eğlence zamanına da değer verin", "Aile olarak birlikte tatil planı yapın"],
        "e": "Gençle birlikte bir CV taslağı hazırlayın: yaz stajı veya gönüllülük başvurusu için.",
    },
}


def _build_bulten_html(kademe: str, ay: int, yil: int, kurum_adi: str) -> str:
    """Premium Edition bülten HTML — 20 sayfalı flipbook."""
    tema_baslik, tema_ikon = _BULTEN_TEMALAR.get(ay, ("Rehberlik Bülteni", "📰"))
    renk1, renk2, kat_ikon = _BULTEN_RENK.get(kademe, ("#6b7280", "#4b5563", "📄"))
    ay_adi = _AYLAR_TR.get(ay, "")
    icerik = _BULTEN_ICERIK.get((kademe, ay))
    if not icerik:
        return "<div style='padding:40px;text-align:center;color:#999'>İçerik bulunamadı.</div>"
    giris = icerik["g"]
    bolum_html = ""
    for baslik, txt in icerik["b"]:
        bolum_html += f'<div class="sec-block"><div class="sec-title">{baslik}</div><p>{txt}</p></div>'
    ipucu_html = "".join(f"<li>{t}</li>" for t in icerik["v"])
    etkinlik = icerik["e"]
    # Takvim
    takvim = _BULTEN_TAKVIM.get(ay, [])
    takvim_html = "".join(f'<div class="cal-item"><span class="cal-date">{d}</span><span class="cal-ev">{e}</span></div>' for d, e in takvim)
    # Motivasyon
    mot_text, mot_author = _BULTEN_MOTIVASYON.get(ay, ("", ""))
    # İnfografik
    infog = _BULTEN_INFOGRAFIK.get(ay, [])
    infog_html = ""
    for title, val, icon in infog:
        infog_html += f'<div class="info-card"><div class="info-icon">{icon}</div><div class="info-title">{title}</div><div class="info-val">{val}</div></div>'
    # Vaka
    vaka = _BULTEN_VAKA.get(ay, ("", "", ""))
    # Quiz
    quiz_items = _BULTEN_TEST.get(ay, [])
    quiz_html = ""
    for qi, (q, opts, ci) in enumerate(quiz_items):
        opts_html = ""
        for oi, o in enumerate(opts):
            opts_html += f'<label class="q-opt" data-q="{qi}" data-o="{oi}" data-c="{ci}" onclick="checkAns(this)"><span class="q-radio"></span>{o}</label>'
        quiz_html += f'<div class="q-block"><div class="q-text">{qi+1}. {q}</div>{opts_html}</div>'
    # Checklist
    cl_items = _BULTEN_CHECKLIST.get(ay, [])
    cl_html = "".join(f'<label class="cl-item" onclick="toggleCl(this)"><span class="cl-box"></span>{c}</label>' for c in cl_items)
    # Kaynaklar
    kaynak_data = _BULTEN_KAYNAKLAR.get(ay, {})
    k_group = "kucuk" if kademe in ("Anaokulu", "İlkokul") else "buyuk"
    kaynaklar = kaynak_data.get(k_group, {"kitap": [], "video": [], "uygulama": []})
    kaynak_html = ""
    for k in kaynaklar.get("kitap", []):
        kaynak_html += f'<div class="res-item"><span class="res-icon">📚</span>{k}</div>'
    for v in kaynaklar.get("video", []):
        kaynak_html += f'<div class="res-item"><span class="res-icon">🎬</span>{v}</div>'
    for a in kaynaklar.get("uygulama", []):
        kaynak_html += f'<div class="res-item"><span class="res-icon">📱</span>{a}</div>'

    # Veli Köşesi
    veli_data = _BULTEN_VELI.get(ay, {})
    v_group = "kucuk" if kademe in ("Anaokulu", "İlkokul") else "buyuk"
    veli = veli_data.get(v_group, {"mesaj": "", "etkinlikler": [], "ipucu": ""})
    veli_etk_html = "".join(f'<div class="veli-act"><span class="veli-num">{i+1}</span>{e}</div>' for i, e in enumerate(veli.get("etkinlikler", [])))

    # Hedef Planı
    hedef_data = _BULTEN_HEDEF.get(ay, {})
    hedef_items_html = "".join(
        f'<div class="hedef-item" onclick="toggleHedef(this)"><span class="hedef-box"></span>{h}</div>'
        for h in hedef_data.get("hedefler", [])
    )
    duygu_html = "".join(
        f'<span class="duygu-btn" onclick="selectDuygu(this)" data-d="{d[0]}">{d[1]} {d[0]}</span>'
        for d in hedef_data.get("duygular", [])
    )

    # ── Yeni sayfa verileri (P10-P19) ──
    # P10: Uzman Görüşü
    uzman = _BULTEN_UZMAN.get(ay, {})
    uzman_html = ""
    if uzman:
        uzman_html = f'''<div class="expert-card">
          <div class="expert-head"><span class="expert-badge">🎓 {uzman.get("uzman","")}</span></div>
          <div class="expert-topic">{uzman.get("baslik","")}</div>
          <div class="expert-body">{uzman.get("icerik","")}</div>
          <div class="expert-tip">💡 Öneri: {uzman.get("oneri","")}</div>
        </div>'''

    # P11: SEL Beceri Kartı
    sel = _BULTEN_SEL.get(ay, {})
    sel_adim_html = "".join(
        f'<div class="sel-step"><span class="sel-num">{i+1}</span>{a}</div>'
        for i, a in enumerate(sel.get("adimlar", []))
    )

    # P12: Aktivite
    akt = _BULTEN_AKTIVITE.get(ay, {})
    akt_malz_html = "".join(f'<span class="akt-tag">{m}</span>' for m in akt.get("malzemeler", []))
    akt_adim_html = "".join(
        f'<div class="akt-step"><span class="akt-num">{i+1}</span>{a}</div>'
        for i, a in enumerate(akt.get("adimlar", []))
    )

    # P13: Dünyadan Örnekler
    dunya = _BULTEN_DUNYA.get(ay, [])
    dunya_html = "".join(
        f'<div class="world-item"><div class="world-country">{ulke}</div><div class="world-desc">{acik}</div></div>'
        for ulke, acik in dunya
    )

    # P14: Bulmaca
    bulmaca = _BULTEN_BULMACA.get(ay, {})
    bilmece_html = "".join(
        f'<div class="riddle-item"><div class="riddle-q">❓ {s}</div><div class="riddle-a" style="display:none">💡 {c}</div><button class="vaka-btn" onclick="this.previousElementSibling.style.display=\'block\';this.style.display=\'none\'">Cevabı Gör</button></div>'
        for s, c in bulmaca.get("bilmece", [])
    )

    # P15: Rol Model
    rolmodel = _BULTEN_ROLMODEL.get(ay, {})

    # P16: Günlük
    gunluk = _BULTEN_GUNLUK.get(ay, {})

    # P17: Dijital Okuryazarlık
    dijital = _BULTEN_DIJITAL.get(ay, {})
    dijital_tip_html = "".join(
        f'<div class="digi-tip"><span class="digi-icon">✅</span>{t}</div>'
        for t in dijital.get("ipuclari", [])
    )

    # P18: Sağlık
    saglik = _BULTEN_SAGLIK.get(ay, {})
    saglik_tip_html = "".join(
        f'<div class="health-tip"><span class="health-icon">💚</span>{t}</div>'
        for t in saglik.get("ipuclari", [])
    )

    # P19: Gelecek Ay
    gelecek = _BULTEN_GELECEK.get(ay, {})

    # ── P20-P29 yeni sayfa verileri ──
    kariyer = _BULTEN_KARIYER.get(ay, {})
    kariyer_html = "".join(
        f'<div class="career-card"><div class="career-icon">{ikon}</div><div class="career-name">{isim}</div><div class="career-desc">{acik}</div></div>'
        for isim, ikon, acik in kariyer.get("meslekler", [])
    )

    stres = _BULTEN_STRES.get(ay, {})
    stres_teknik_html = "".join(
        f'<div class="stress-tip"><span class="stress-num">{i+1}</span>{t}</div>'
        for i, t in enumerate(stres.get("teknikler", []))
    )

    iletisim = _BULTEN_ILETISIM.get(ay, {})
    iletisim_ipucu_html = "".join(
        f'<div class="comm-tip"><span class="comm-check">✓</span>{t}</div>'
        for t in iletisim.get("ipuclari", [])
    )

    zaman = _BULTEN_ZAMAN.get(ay, {})
    zaman_matris_html = "".join(
        f'<div class="time-card"><div class="time-icon">{ikon}</div><div class="time-title">{baslik}</div><div class="time-desc">{acik}</div></div>'
        for baslik, ikon, acik in zaman.get("matris", [])
    )

    empati = _BULTEN_EMPATI.get(ay, {})
    kitap = _BULTEN_KITAP.get(ay, {})
    kitap_oneri_html = "".join(f'<div class="book-rec">📖 {k}</div>' for k in kitap.get("oneri", []))

    sanat = _BULTEN_SANAT.get(ay, {})
    doga = _BULTEN_DOGA.get(ay, {})
    minnet = _BULTEN_MINNETTARLIK.get(ay, {})
    minnet_liste_html = "".join(
        f'<div class="grat-item" onclick="toggleGrat(this)"><span class="grat-heart">♡</span>{m}</div>'
        for m in minnet.get("liste", [])
    )

    return f'''<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:linear-gradient(170deg,#faf8f5 0%,#fff9f0 30%,#f5f1ec 100%);
font-family:Georgia,'Times New Roman',serif;overflow:hidden;color:#1f2937}}
.app{{width:100%;height:100vh;display:flex;flex-direction:column}}
.hdr{{background:linear-gradient(135deg,{renk1},{renk2});padding:10px 20px;
display:flex;align-items:center;justify-content:space-between;
border-bottom:3px solid rgba(255,255,255,0.2);box-shadow:0 4px 20px rgba(0,0,0,.15)}}
.hdr h2{{color:#fff;font-size:15px;font-weight:800;letter-spacing:1px;text-shadow:0 1px 3px rgba(0,0,0,.3)}}
.hdr .sub{{color:rgba(255,255,255,.85);font-size:10px;font-weight:500}}
.hdr .badge{{background:rgba(255,255,255,.2);color:#fff;padding:3px 12px;border-radius:12px;font-size:10px;font-weight:700;backdrop-filter:blur(4px);border:1px solid rgba(255,255,255,.3)}}
.pages{{flex:1;overflow:hidden;position:relative}}
.pg{{position:absolute;inset:0;padding:28px 26px;display:none;opacity:0;
transform:translateX(30px);transition:all .35s ease;overflow-y:auto;
background:linear-gradient(170deg,#fffdf9,#faf8f5,#f5f1ec)}}
.pg.active{{display:block;opacity:1;transform:translateX(0)}}
.pg::-webkit-scrollbar{{width:5px}}.pg::-webkit-scrollbar-thumb{{background:{renk1}50;border-radius:4px}}
/* Cover — kuse kagit parlak gorunum */
.cover{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
background:linear-gradient(160deg,{renk1} 0%,{renk2} 40%,#1a1a2e 100%);
position:relative;overflow:hidden}}
.cover::before{{content:'';position:absolute;top:-30%;right:-20%;width:60%;height:80%;
background:radial-gradient(ellipse,rgba(255,255,255,.08),transparent 60%);pointer-events:none}}
.cover::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:4px;
background:linear-gradient(90deg,transparent,rgba(255,255,255,.4),transparent)}}
.cover .k-name{{font-size:11px;color:rgba(255,255,255,.7);letter-spacing:4px;text-transform:uppercase;margin-bottom:22px;
font-family:'Segoe UI',system-ui,sans-serif}}
.cover .t-icon{{font-size:64px;margin-bottom:16px;filter:drop-shadow(0 4px 20px rgba(0,0,0,.3))}}
.cover .tema{{font-size:22px;font-weight:900;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.3);letter-spacing:1px}}
.cover .k-badge{{display:inline-block;background:rgba(255,255,255,.15);backdrop-filter:blur(6px);
color:#fff;padding:6px 22px;border-radius:20px;font-size:12px;font-weight:700;margin:16px 0;
border:1px solid rgba(255,255,255,.25);box-shadow:0 4px 15px rgba(0,0,0,.2);
font-family:'Segoe UI',sans-serif}}
.cover .tarih{{font-size:30px;font-weight:900;color:#fff;margin-top:8px;text-shadow:0 2px 8px rgba(0,0,0,.3)}}
.cover .yil-text{{font-size:14px;color:rgba(255,255,255,.5);font-family:'Segoe UI',sans-serif}}
.cover .prem{{font-size:9px;color:rgba(255,255,255,.4);letter-spacing:3px;margin-top:20px;font-family:'Segoe UI',sans-serif}}
/* Content — dergi ici sayfa */
.pg-title{{font-size:18px;font-weight:800;color:{renk1};margin-bottom:16px;
padding-bottom:8px;border-bottom:3px solid {renk1};letter-spacing:0.5px;
font-family:'Segoe UI',system-ui,sans-serif}}
.intro{{font-size:13.5px;line-height:1.8;color:#374151;margin-bottom:18px;
padding:16px 18px;background:linear-gradient(135deg,#fffbeb,#fef3c7);border-radius:10px;
border-left:4px solid {renk1};box-shadow:0 2px 8px rgba(0,0,0,.04);text-align:justify}}
.sec-block{{margin-bottom:14px}}.sec-title{{font-size:14px;font-weight:800;color:{renk1};margin-bottom:6px;
font-family:'Segoe UI',system-ui,sans-serif}}
.sec-block p{{font-size:12.5px;line-height:1.75;color:#374151;text-align:justify}}
/* Infographic — kuse kartlar */
.info-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}}
.info-card{{background:#fff;border:1px solid #e5e7eb;border-radius:12px;
padding:16px;text-align:center;transition:all .25s;box-shadow:0 2px 8px rgba(0,0,0,.04)}}
.info-card:hover{{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.08);border-color:{renk1}}}
.info-icon{{font-size:32px;margin-bottom:8px}}.info-title{{font-size:12px;font-weight:800;color:{renk1};
font-family:'Segoe UI',sans-serif}}
.info-val{{font-size:11px;color:#374151;margin-top:5px;line-height:1.5}}
/* Calendar — kuse takvim */
.cal-item{{display:flex;align-items:center;gap:12px;padding:10px 14px;
background:#fff;border-radius:8px;margin-bottom:6px;
border-left:4px solid {renk1};box-shadow:0 1px 4px rgba(0,0,0,.04)}}
.cal-date{{font-size:11px;font-weight:800;color:{renk1};min-width:80px;
font-family:'Segoe UI',sans-serif}}
.cal-ev{{font-size:11.5px;color:#374151}}
/* Motivation — kuse alinti kutusu */
.mot-box{{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1px solid #fcd34d;
border-radius:14px;padding:22px;margin-top:16px;text-align:center;position:relative;
box-shadow:0 3px 12px rgba(0,0,0,.05)}}
.mot-box::before{{content:'\201C';position:absolute;top:4px;left:16px;font-size:48px;color:{renk1};opacity:.25;
font-family:Georgia,serif}}
.mot-text{{font-size:15px;font-style:italic;color:#1f2937;line-height:1.7}}
.mot-author{{font-size:12px;color:{renk1};margin-top:10px;font-weight:700;
font-family:'Segoe UI',sans-serif}}
/* Vaka — kuse hikaye kutusu */
.vaka-story{{background:#fff;border-radius:10px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,.04);
border-left:4px solid #f59e0b;margin-bottom:10px;font-size:12px;line-height:1.6;color:#1f2937}}
.vaka-q{{font-size:12px;font-weight:700;color:#f59e0b;margin-bottom:8px}}
.vaka-ans{{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:10px;
padding:12px;font-size:12px;line-height:1.6;color:#a7f3d0;display:none}}
.vaka-btn{{background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;border:none;
border-radius:8px;padding:6px 16px;font-size:11px;font-weight:700;cursor:pointer;margin-bottom:8px}}
/* Quiz */
.q-block{{margin-bottom:14px}}.q-text{{font-size:12px;font-weight:700;color:#1f2937;margin-bottom:6px}}
.q-opt{{display:block;padding:8px 12px;margin:3px 0;background:#fff;
border-radius:8px;font-size:11px;color:#1f2937;cursor:pointer;border:1px solid transparent;
transition:all .2s;display:flex;align-items:center;gap:8px}}
.q-opt:hover{{background:rgba(255,255,255,.08);border-color:{renk1}30}}
.q-radio{{width:16px;height:16px;border:2px solid {renk1}50;border-radius:50%;flex-shrink:0;
transition:all .2s;display:flex;align-items:center;justify-content:center}}
.q-opt.correct{{background:rgba(16,185,129,.15);border-color:#10b981;color:#a7f3d0}}
.q-opt.correct .q-radio{{border-color:#10b981;background:#10b981}}
.q-opt.correct .q-radio::after{{content:'\\2714';color:#fff;font-size:10px}}
.q-opt.wrong{{background:rgba(239,68,68,.15);border-color:#ef4444;color:#fca5a5}}
.q-opt.wrong .q-radio{{border-color:#ef4444;background:#ef4444}}
.q-opt.wrong .q-radio::after{{content:'\\2718';color:#fff;font-size:10px}}
/* Checklist */
.cl-item{{display:flex;align-items:center;gap:10px;padding:10px 14px;margin:4px 0;
background:#fff;border-radius:8px;font-size:12px;color:#1f2937;cursor:pointer;
border:1px solid transparent;transition:all .2s}}
.cl-item:hover{{background:rgba(255,255,255,.08)}}
.cl-box{{width:18px;height:18px;border:2px solid {renk1}50;border-radius:4px;flex-shrink:0;
transition:all .3s;display:flex;align-items:center;justify-content:center}}
.cl-item.checked{{opacity:.6}}.cl-item.checked .cl-box{{background:{renk1};border-color:{renk1}}}
.cl-item.checked .cl-box::after{{content:'\\2714';color:#fff;font-size:10px}}
/* Resources */
.res-item{{display:flex;align-items:center;gap:8px;padding:8px 12px;margin:4px 0;
background:#fff;border-radius:8px;font-size:11px;color:#1f2937}}
.res-icon{{font-size:16px;flex-shrink:0}}
/* Tips */
.tip-list{{list-style:none}}.tip-list li{{font-size:12px;line-height:1.6;color:#1f2937;padding:8px 12px 8px 28px;
margin:4px 0;background:#fff;border-radius:8px;border-left:3px solid {renk1};position:relative}}
.tip-list li::before{{content:"\\2714";position:absolute;left:8px;color:{renk1};font-weight:bold;font-size:11px}}
/* Activity */
.act-box{{background:linear-gradient(135deg,{renk1}12,{renk2}12);border:1px solid {renk1}30;
border-radius:12px;padding:16px;margin-top:12px}}
.act-box b{{color:{renk1};font-size:13px}}.act-box p{{font-size:12px;line-height:1.6;color:#1f2937;margin-top:4px}}
/* Veli Köşesi */
.veli-msg{{background:linear-gradient(135deg,rgba(245,158,11,.08),rgba(217,119,6,.08));border:1px solid rgba(245,158,11,.25);
border-radius:12px;padding:14px;font-size:12px;line-height:1.7;color:#fbbf24;margin-bottom:12px;
border-left:4px solid #f59e0b}}
.veli-act{{display:flex;align-items:flex-start;gap:10px;padding:10px 14px;margin:5px 0;
background:#fff;border-radius:8px;font-size:12px;color:#1f2937;line-height:1.5}}
.veli-num{{width:22px;height:22px;background:linear-gradient(135deg,{renk1},{renk2});color:#fff;
border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0}}
.veli-tip{{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:10px;
padding:12px;font-size:11px;line-height:1.6;color:#a7f3d0;margin-top:12px}}
.veli-tip::before{{content:"💡 İpucu: ";font-weight:700;color:#10b981}}
/* Hedef Planı */
.hedef-soz{{font-size:14px;font-weight:700;color:{renk1};text-align:center;margin:12px 0;
font-style:italic}}
.hedef-item{{display:flex;align-items:center;gap:10px;padding:12px 14px;margin:5px 0;
background:#fff;border-radius:10px;font-size:12px;color:#1f2937;cursor:pointer;
border:1px solid transparent;transition:all .25s}}
.hedef-item:hover{{background:rgba(255,255,255,.08)}}
.hedef-box{{width:20px;height:20px;border:2px solid {renk1}50;border-radius:50%;flex-shrink:0;
transition:all .3s;display:flex;align-items:center;justify-content:center}}
.hedef-item.done{{border-color:rgba(16,185,129,.3);background:rgba(16,185,129,.08)}}
.hedef-item.done .hedef-box{{background:#10b981;border-color:#10b981}}
.hedef-item.done .hedef-box::after{{content:'\\2714';color:#fff;font-size:10px}}
.duygu-sec{{margin-top:16px;text-align:center}}
.duygu-sec .lbl{{font-size:12px;font-weight:700;color:{renk1};margin-bottom:10px}}
.duygu-btn{{display:inline-block;padding:6px 12px;margin:3px;border-radius:20px;font-size:11px;
background:#fff;border:1px solid #e5e7eb;color:#1f2937;cursor:pointer;
transition:all .2s}}
.duygu-btn:hover{{border-color:{renk1};background:rgba(255,255,255,.08)}}
.duygu-btn.active{{background:linear-gradient(135deg,{renk1},{renk2});color:#fff;border-color:{renk1};
font-weight:700;transform:scale(1.1)}}
.deger-box{{margin-top:14px;text-align:center;padding:14px;background:#fff;
border-radius:12px;border:1px solid rgba(255,255,255,.06)}}
.deger-q{{font-size:12px;font-weight:600;color:{renk1};margin-bottom:8px}}
/* Expert */
.expert-card{{background:#fff;border:1px solid {renk1}20;border-radius:14px;padding:18px;margin-top:10px}}
.expert-head{{margin-bottom:10px}}
.expert-badge{{background:linear-gradient(135deg,{renk1},{renk2});color:#fff;padding:4px 14px;border-radius:20px;font-size:11px;font-weight:700}}
.expert-topic{{font-size:14px;font-weight:700;color:{renk1};margin:10px 0 8px}}
.expert-body{{font-size:12px;line-height:1.7;color:#1f2937}}
.expert-tip{{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:10px;
padding:12px;font-size:11px;line-height:1.6;color:#a7f3d0;margin-top:12px}}
/* SEL */
.sel-def{{font-size:12px;color:#4b5563;margin-bottom:6px;font-style:italic}}
.sel-why{{font-size:12px;color:#1f2937;margin-bottom:12px;padding:10px;background:#fff;border-radius:8px;border-left:3px solid {renk1}}}
.sel-step{{display:flex;align-items:flex-start;gap:10px;padding:10px 14px;margin:5px 0;
background:#fff;border-radius:8px;font-size:12px;color:#1f2937;line-height:1.5}}
.sel-num{{width:22px;height:22px;background:linear-gradient(135deg,{renk1},{renk2});color:#fff;
border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0}}
.sel-scenario{{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:10px;
padding:12px;font-size:12px;line-height:1.6;color:#fbbf24;margin-top:12px}}
/* Activity */
.akt-type{{font-size:10px;color:{renk1};text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}}
.akt-tags{{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}}
.akt-tag{{background:#f8fafc;border:1px solid {renk1}30;border-radius:16px;padding:3px 10px;font-size:10px;color:#4b5563}}
.akt-step{{display:flex;align-items:flex-start;gap:10px;padding:10px 14px;margin:5px 0;
background:#fff;border-radius:8px;font-size:12px;color:#1f2937;line-height:1.5}}
.akt-num{{width:22px;height:22px;background:linear-gradient(135deg,#10b981,#059669);color:#fff;
border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0}}
.akt-gain{{background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.2);border-radius:10px;
padding:12px;font-size:11px;line-height:1.6;color:#c4b5fd;margin-top:12px}}
/* World */
.world-item{{padding:14px;margin:8px 0;background:#fff;border-radius:10px;
border-left:3px solid {renk1}}}
.world-country{{font-size:13px;font-weight:700;color:{renk1};margin-bottom:4px}}
.world-desc{{font-size:12px;line-height:1.6;color:#1f2937}}
/* Riddle */
.riddle-item{{margin-bottom:14px;padding:12px;background:#fff;border-radius:10px}}
.riddle-q{{font-size:12px;font-weight:600;color:#1f2937;margin-bottom:6px}}
.riddle-a{{font-size:12px;color:#a7f3d0;padding:8px;background:rgba(16,185,129,.08);border-radius:8px;margin-bottom:6px}}
.fun-fact{{background:linear-gradient(135deg,{renk1}10,{renk2}10);border:1px solid {renk1}30;
border-radius:12px;padding:14px;margin-top:12px;font-size:12px;color:#1f2937;line-height:1.6}}
/* Role Model */
.rm-card{{background:#fff;border:1px solid {renk1}20;border-radius:14px;padding:18px;text-align:center}}
.rm-name{{font-size:16px;font-weight:800;color:{renk1};margin-bottom:2px}}
.rm-field{{font-size:11px;color:#4b5563;margin-bottom:12px}}
.rm-story{{font-size:12px;line-height:1.7;color:#1f2937;margin-bottom:12px;text-align:left}}
.rm-quote{{font-style:italic;font-size:13px;color:#1f2937;padding:12px;background:#fff;
border-radius:10px;border-left:3px solid {renk1};margin-bottom:10px;text-align:left}}
.rm-lesson{{font-size:11px;color:#a7f3d0;background:rgba(16,185,129,.08);border-radius:8px;padding:10px;text-align:left}}
/* Journal */
.journal-q{{font-size:12px;color:#1f2937;font-weight:600;margin:10px 0 4px}}
.journal-area{{min-height:36px;padding:10px;background:#fff;border-radius:8px;
border:1px solid #e5e7eb;font-size:12px;color:#1f2937;outline:none;line-height:1.5}}
.journal-prompt{{background:linear-gradient(135deg,{renk1}10,{renk2}10);border:1px solid {renk1}30;
border-radius:12px;padding:14px;margin-top:12px;font-size:12px;color:#1f2937}}
/* Digital */
.digi-tip{{display:flex;align-items:flex-start;gap:8px;padding:10px 12px;margin:5px 0;
background:#fff;border-radius:8px;font-size:12px;color:#1f2937;line-height:1.5}}
.digi-icon{{flex-shrink:0;font-size:14px}}
.digi-warn{{background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:10px;
padding:12px;font-size:11px;line-height:1.6;color:#fca5a5;margin-top:10px}}
.digi-warn::before{{content:"⚠️ Dikkat: ";font-weight:700;color:#ef4444}}
.digi-rule{{background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);border-radius:10px;
padding:12px;font-size:11px;line-height:1.6;color:#93c5fd;margin-top:8px}}
.digi-rule::before{{content:"📏 Aile Kuralı: ";font-weight:700;color:#3b82f6}}
/* Health */
.health-info{{font-size:12px;line-height:1.7;color:#1f2937;margin-bottom:12px;padding:14px;
background:#fff;border-radius:10px;border-left:3px solid #10b981}}
.health-tip{{display:flex;align-items:flex-start;gap:8px;padding:8px 12px;margin:4px 0;
background:#fff;border-radius:8px;font-size:12px;color:#1f2937;line-height:1.5}}
.health-icon{{flex-shrink:0}}
.health-recipe{{background:linear-gradient(135deg,rgba(16,185,129,.08),rgba(5,150,105,.08));
border:1px solid rgba(16,185,129,.25);border-radius:12px;padding:14px;margin-top:12px;
font-size:12px;line-height:1.6;color:#a7f3d0}}
.health-recipe::before{{content:"🥗 ";font-weight:700}}
/* Career */
.career-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}}
.career-card{{background:#fff;border:1px solid {renk1}20;border-radius:12px;padding:14px;text-align:center;transition:all .3s}}
.career-card:hover{{transform:translateY(-3px);border-color:{renk1}50;box-shadow:0 8px 20px rgba(0,0,0,.3)}}
.career-icon{{font-size:32px;margin-bottom:6px}}.career-name{{font-size:12px;font-weight:700;color:{renk1}}}
.career-desc{{font-size:10px;color:#4b5563;margin-top:4px;line-height:1.4}}
.career-q{{background:linear-gradient(135deg,{renk1}10,{renk2}10);border:1px solid {renk1}30;border-radius:12px;padding:14px;margin-top:12px;font-size:12px;color:#1f2937;line-height:1.6}}
/* Stress */
.breath-box{{background:linear-gradient(135deg,rgba(16,185,129,.08),rgba(5,150,105,.08));border:1px solid rgba(16,185,129,.25);
border-radius:14px;padding:18px;text-align:center;margin:12px 0;position:relative;overflow:hidden}}
.breath-circle{{width:80px;height:80px;border-radius:50%;background:radial-gradient(circle,{renk1}40,transparent);
margin:10px auto;animation:breathe 8s ease-in-out infinite}}
@keyframes breathe{{0%,100%{{transform:scale(.6);opacity:.4}}50%{{transform:scale(1.2);opacity:1}}}}
.breath-text{{font-size:14px;font-weight:700;color:#10b981;margin-top:6px}}
.breath-desc{{font-size:11px;color:#a7f3d0;margin-top:4px}}
.stress-tip{{display:flex;align-items:flex-start;gap:10px;padding:10px 14px;margin:5px 0;
background:#fff;border-radius:8px;font-size:12px;color:#1f2937;line-height:1.5}}
.stress-num{{width:22px;height:22px;background:linear-gradient(135deg,#10b981,#059669);color:#fff;
border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0}}
/* Communication */
.comm-scenario{{background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.2);border-radius:12px;
padding:14px;margin:10px 0;font-size:12px;line-height:1.7;color:#c4b5fd}}
.comm-correct{{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:12px;
padding:14px;margin:8px 0;font-size:12px;line-height:1.7;color:#a7f3d0;display:none}}
.comm-tip{{display:flex;align-items:flex-start;gap:8px;padding:8px 12px;margin:4px 0;
background:#fff;border-radius:8px;font-size:12px;color:#1f2937;line-height:1.5}}
.comm-check{{color:{renk1};font-weight:700;flex-shrink:0}}
/* Time */
.time-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}}
.time-card{{background:#fff;border:1px solid {renk1}20;border-radius:12px;padding:14px;transition:all .3s}}
.time-card:hover{{border-color:{renk1}50;transform:translateY(-2px)}}
.time-icon{{font-size:24px;margin-bottom:4px}}.time-title{{font-size:11px;font-weight:700;color:{renk1}}}
.time-desc{{font-size:10px;color:#4b5563;margin-top:4px;line-height:1.4}}
.time-tip{{background:linear-gradient(135deg,{renk1}10,{renk2}10);border:1px solid {renk1}30;border-radius:12px;padding:14px;margin-top:10px;font-size:12px;color:#1f2937;line-height:1.6}}
.time-tip::before{{content:"💡 ";font-weight:700}}
/* Empathy */
.empathy-story{{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:12px;
padding:16px;margin:10px 0;font-size:12px;line-height:1.7;color:#fbbf24}}
.empathy-think{{background:rgba(139,92,246,.08);border:1px solid rgba(139,92,246,.2);border-radius:12px;
padding:14px;margin:8px 0;font-size:12px;line-height:1.7;color:#c4b5fd}}
.empathy-act{{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:12px;
padding:14px;font-size:12px;line-height:1.7;color:#a7f3d0;margin-top:8px}}
.empathy-act::before{{content:"📝 Bu Haftanın Görevi: ";font-weight:700;color:#10b981}}
/* Book */
.book-main{{background:linear-gradient(135deg,{renk1}08,{renk2}08);border:1px solid {renk1}30;
border-radius:14px;padding:18px;margin:10px 0;text-align:center}}
.book-title{{font-size:15px;font-weight:800;color:{renk1};margin-bottom:4px}}
.book-desc{{font-size:12px;color:#1f2937;line-height:1.6;margin-top:6px;text-align:left}}
.book-q{{font-size:12px;font-weight:600;color:#fbbf24;margin-top:10px;padding:12px;background:rgba(245,158,11,.08);
border-radius:10px;border-left:4px solid #f59e0b;text-align:left}}
.book-rec{{padding:8px 12px;margin:4px 0;background:#fff;border-radius:8px;font-size:11px;color:#1f2937}}
/* Art */
.art-card{{background:linear-gradient(135deg,rgba(236,72,153,.08),rgba(168,85,247,.08));
border:1px solid rgba(236,72,153,.2);border-radius:14px;padding:18px;margin:10px 0}}
.art-name{{font-size:15px;font-weight:700;color:#ec4899;margin-bottom:4px}}
.art-desc{{font-size:12px;color:#f9a8d4;font-style:italic;margin-bottom:10px}}
.art-how{{font-size:12px;color:#1f2937;line-height:1.7;padding:12px;background:#fff;border-radius:10px}}
.art-mat{{font-size:11px;color:#4b5563;margin-top:8px;padding:8px 12px;background:#fff;border-radius:8px}}
.art-mat::before{{content:"🎨 Malzeme: ";font-weight:700;color:#a78bfa}}
/* Nature */
.nature-info{{font-size:12px;line-height:1.7;color:#1f2937;padding:14px;background:rgba(34,197,94,.06);
border-radius:10px;border-left:3px solid #22c55e;margin:10px 0}}
.nature-task{{background:linear-gradient(135deg,rgba(34,197,94,.08),rgba(22,163,74,.08));
border:1px solid rgba(34,197,94,.25);border-radius:12px;padding:16px;margin-top:10px;font-size:12px;line-height:1.7;color:#86efac}}
.nature-task::before{{content:"🌱 Görev: ";font-weight:700;color:#22c55e}}
/* Gratitude */
.grat-msg{{font-size:13px;font-style:italic;color:#fbbf24;text-align:center;margin:12px 0;
padding:14px;background:linear-gradient(135deg,rgba(245,158,11,.08),rgba(217,119,6,.08));
border-radius:14px;border:1px solid rgba(245,158,11,.25)}}
.grat-item{{display:flex;align-items:center;gap:10px;padding:12px 14px;margin:5px 0;
background:#fff;border-radius:10px;font-size:12px;color:#1f2937;cursor:pointer;
border:1px solid transparent;transition:all .25s}}
.grat-item:hover{{background:rgba(255,255,255,.08)}}
.grat-heart{{font-size:18px;color:rgba(239,68,68,.4);transition:all .3s;flex-shrink:0}}
.grat-item.loved{{border-color:rgba(239,68,68,.3);background:rgba(239,68,68,.06)}}
.grat-item.loved .grat-heart{{color:#ef4444;content:'♥'}}
/* Back Cover */
.back-cover{{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
background:radial-gradient(ellipse at 50% 50%,{renk1}08,transparent 60%),linear-gradient(180deg,#0a0a1a,#0B0F19)}}
.back-logo{{font-size:48px;margin-bottom:12px;filter:drop-shadow(0 0 25px {renk1}40)}}
.back-title{{font-size:14px;font-weight:700;color:{renk1};letter-spacing:2px}}
.back-sub{{font-size:10px;color:#64748b;margin-top:6px}}
.back-stats{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:18px 0;width:80%}}
.back-stat{{text-align:center;padding:10px;background:#fff;border-radius:10px;border:1px solid rgba(255,255,255,.06)}}
.back-stat-val{{font-size:20px;font-weight:800;color:{renk1}}}.back-stat-lbl{{font-size:9px;color:#64748b;margin-top:2px}}
/* Page number watermark */
.pg-num{{position:absolute;bottom:8px;right:14px;font-size:9px;color:rgba(255,255,255,.15);font-weight:700}}
/* Next Month */
.next-preview{{background:linear-gradient(135deg,{renk1}10,{renk2}10);border:1px solid {renk1}30;
border-radius:14px;padding:18px;text-align:center;margin-bottom:14px}}
.next-icon{{font-size:40px;margin-bottom:8px}}
.next-tema{{font-size:16px;font-weight:700;color:{renk1}}}
.next-desc{{font-size:12px;color:#1f2937;margin-top:6px;line-height:1.6}}
.next-prep{{font-size:12px;color:#4b5563;margin-top:10px;padding:12px;background:#fff;
border-radius:10px;border-left:3px solid {renk1}}}
.closing-msg{{text-align:center;padding:18px;margin-top:14px;font-size:12px;color:#4b5563;line-height:1.7;
background:rgba(255,255,255,.02);border-radius:12px;border:1px solid rgba(255,255,255,.05)}}
/* Controls */
.ctrls{{background:#0a0a1a;padding:6px 14px;display:flex;align-items:center;
justify-content:center;gap:8px;border-top:1px solid rgba(255,255,255,.06)}}
.btn{{background:linear-gradient(135deg,{renk1},{renk2});color:#fff;border:none;
border-radius:8px;padding:6px 14px;font-weight:700;font-size:11px;cursor:pointer;transition:all .2s}}
.btn:hover{{transform:translateY(-1px);box-shadow:0 4px 12px {renk1}40}}
.btn:disabled{{opacity:.3;cursor:not-allowed;transform:none}}
.btn.tts{{background:linear-gradient(135deg,#10b981,#059669)}}
.btn.tts.on{{background:linear-gradient(135deg,#ef4444,#dc2626);animation:pulse 1.5s infinite}}
.btn.share{{background:linear-gradient(135deg,#6366f1,#4f46e5)}}
.btn.pdf{{background:linear-gradient(135deg,#f59e0b,#d97706)}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.7}}}}
.pi{{color:{renk1};font-size:12px;font-weight:600;min-width:60px;text-align:center}}
.progress{{position:absolute;top:0;left:0;height:3px;background:linear-gradient(90deg,{renk1},{renk2});
transition:width .4s;z-index:10}}
/* TTS wave */
.tts-wave{{display:none;align-items:center;gap:2px;margin-left:6px}}
.tts-wave.on{{display:inline-flex}}
.tts-wave span{{width:3px;background:{renk1};border-radius:2px;animation:wave 1s ease-in-out infinite}}
.tts-wave span:nth-child(1){{height:8px;animation-delay:0s}}
.tts-wave span:nth-child(2){{height:14px;animation-delay:.1s}}
.tts-wave span:nth-child(3){{height:10px;animation-delay:.2s}}
.tts-wave span:nth-child(4){{height:16px;animation-delay:.3s}}
.tts-wave span:nth-child(5){{height:8px;animation-delay:.4s}}
@keyframes wave{{0%,100%{{transform:scaleY(.5)}}50%{{transform:scaleY(1.2)}}}}
</style></head>
<body>
<div class="app">
<div class="progress" id="prog" style="width:5%"></div>
<div class="hdr">
  <div><h2>{kat_ikon} {kademe} Rehberlik Bülteni</h2>
  <div class="sub">{kurum_adi} — Rehberlik Servisi</div></div>
  <div class="badge">{tema_ikon} {tema_baslik}</div>
</div>
<div class="pages" id="pages">
  <!-- P0: Cover -->
  <div class="pg cover active" data-pg="0">
    <div class="k-name">{kurum_adi}</div>
    <div class="t-icon">{tema_ikon}</div>
    <div class="tema">{tema_baslik}</div>
    <div class="k-badge">{kat_ikon} {kademe} Rehberlik Bülteni</div>
    <div class="tarih">{ay_adi}</div>
    <div class="yil-text">{yil}</div>
    <div class="prem">PREMIUM EDITION</div>
  </div>
  <!-- P1: İçerik -->
  <div class="pg" data-pg="1">
    <div class="pg-title">{tema_ikon} {tema_baslik}</div>
    <div class="intro">{giris}</div>
    {bolum_html}
  </div>
  <!-- P2: İnfografik -->
  <div class="pg" data-pg="2">
    <div class="pg-title">📊 Biliyor musunuz?</div>
    <div class="info-grid">{infog_html}</div>
    <div class="mot-box">
      <div class="mot-text">{mot_text}</div>
      <div class="mot-author">— {mot_author}</div>
    </div>
  </div>
  <!-- P3: Vaka Örneği -->
  <div class="pg" data-pg="3">
    <div class="pg-title">📖 Düşünelim — Vaka Örneği</div>
    <div class="vaka-story">{vaka[0]}</div>
    <div class="vaka-q">💬 {vaka[1]}</div>
    <button class="vaka-btn" onclick="this.nextElementSibling.style.display='block';this.style.display='none'">Önerilen Yaklaşımı Gör</button>
    <div class="vaka-ans">✅ {vaka[2]}</div>
  </div>
  <!-- P4: Takvim -->
  <div class="pg" data-pg="4">
    <div class="pg-title">📅 {ay_adi} Ayı Takvimi</div>
    {takvim_html}
    <div class="act-box">
      <b>🎯 Ayın Etkinliği</b>
      <p>{etkinlik}</p>
    </div>
  </div>
  <!-- P5: Veli Köşesi -->
  <div class="pg" data-pg="5">
    <div class="pg-title">👨‍👩‍👧‍👦 Veli Köşesi</div>
    <div class="veli-msg">{veli.get("mesaj", "")}</div>
    <div class="sec-title" style="margin-bottom:8px">🎯 Bu Ay Çocuğunuzla Yapabileceğiniz Etkinlikler</div>
    {veli_etk_html}
    <div class="veli-tip">{veli.get("ipucu", "")}</div>
  </div>
  <!-- P6: Mini Test -->
  <div class="pg" data-pg="6">
    <div class="pg-title">🧠 Mini Öz Değerlendirme</div>
    <div id="quizArea">{quiz_html}</div>
    <div id="quizResult" style="display:none;margin-top:14px;padding:14px;background:rgba(16,185,129,.1);
    border-radius:10px;border:1px solid rgba(16,185,129,.3);text-align:center">
      <div style="font-size:14px;font-weight:700;color:#10b981" id="quizScore"></div>
    </div>
  </div>
  <!-- P7: Kontrol Listesi + Kaynaklar -->
  <div class="pg" data-pg="7">
    <div class="pg-title">✅ Aylık Kontrol Listesi</div>
    {cl_html}
    <div style="margin-top:16px">
      <div class="pg-title">📚 Kaynak Önerileri</div>
      {kaynak_html}
    </div>
  </div>
  <!-- P8: Ayın Hedef Planı -->
  <div class="pg" data-pg="8">
    <div class="pg-title">🎯 Ayın Hedef Planı — {hedef_data.get("baslik", "")}</div>
    <div class="hedef-soz">"{hedef_data.get("soz", "")}"</div>
    {hedef_items_html}
    <div class="duygu-sec">
      <div class="lbl">{hedef_data.get("degerlendir", "Kendimi nasıl hissediyorum?")}</div>
      {duygu_html}
    </div>
    <div class="deger-box">
      <div class="deger-q">📝 Kendime Not</div>
      <div contenteditable="true" style="min-height:40px;padding:10px;background:#fff;
      border-radius:8px;border:1px solid #e5e7eb;font-size:12px;color:#1f2937;
      outline:none;margin-top:6px;line-height:1.5;text-align:left"
      placeholder="Buraya notunu yaz..."></div>
    </div>
  </div>
  <!-- P9: Öneriler -->
  <div class="pg" data-pg="9">
    <div class="pg-title">💡 Öneriler</div>
    <ul class="tip-list">{ipucu_html}</ul>
    <div class="act-box" style="margin-top:14px">
      <b>🎯 Ayın Etkinliği</b>
      <p>{etkinlik}</p>
    </div>
  </div>
  <!-- P10: Uzman Görüşü -->
  <div class="pg" data-pg="10">
    <div class="pg-title">🎓 Uzman Görüşü</div>
    {uzman_html}
  </div>
  <!-- P11: Sosyal-Duygusal Beceri -->
  <div class="pg" data-pg="11">
    <div class="pg-title">💎 Sosyal-Duygusal Beceri: {sel.get("beceri","")}</div>
    <div class="sel-def">{sel.get("tanim","")}</div>
    <div class="sel-why">🔑 {sel.get("neden","")}</div>
    <div class="sec-title" style="margin-bottom:8px">Adım Adım Uygula</div>
    {sel_adim_html}
    <div class="sel-scenario">🎭 Senaryo: {sel.get("senaryo","")}</div>
  </div>
  <!-- P12: Aktivite & Oyun -->
  <div class="pg" data-pg="12">
    <div class="pg-title">🎨 Aktivite: {akt.get("baslik","")}</div>
    <div class="akt-type">📌 {akt.get("tur","")}</div>
    <div class="akt-tags">{akt_malz_html}</div>
    <div class="sec-title" style="margin-bottom:8px">Nasıl Yapılır?</div>
    {akt_adim_html}
    <div class="akt-gain">🏆 Kazanım: {akt.get("kazanim","")}</div>
  </div>
  <!-- P13: Dünyadan Örnekler -->
  <div class="pg" data-pg="13">
    <div class="pg-title">🌍 Dünyadan Örnekler</div>
    {dunya_html}
  </div>
  <!-- P14: Bilmece & Eğlence -->
  <div class="pg" data-pg="14">
    <div class="pg-title">🧩 Bilmece & Eğlence</div>
    {bilmece_html}
    <div style="margin-top:10px"><div class="sec-title">🔤 Kelime Oyunu</div>
    <div style="font-size:12px;color:#1f2937;padding:10px;background:#fff;border-radius:8px">{bulmaca.get("kelime","")}</div></div>
    <div class="fun-fact">🤓 Biliyor muydunuz? {bulmaca.get("eglence","")}</div>
  </div>
  <!-- P15: Rol Model -->
  <div class="pg" data-pg="15">
    <div class="pg-title">⭐ Ayın İlham Kaynağı</div>
    <div class="rm-card">
      <div class="rm-name">{rolmodel.get("isim","")}</div>
      <div class="rm-field">{rolmodel.get("alan","")}</div>
      <div class="rm-story">{rolmodel.get("hikaye","")}</div>
      <div class="rm-quote">"{rolmodel.get("soz","")}"</div>
      <div class="rm-lesson">✨ Ders: {rolmodel.get("ders","")}</div>
    </div>
  </div>
  <!-- P16: Günlük / Yansıma -->
  <div class="pg" data-pg="16">
    <div class="pg-title">📓 Yansıma Günlüğü</div>
    <div class="journal-q">1. {gunluk.get("soru1","")}</div>
    <div class="journal-area" contenteditable="true" style="min-height:36px" placeholder="Düşüncelerini yaz..."></div>
    <div class="journal-q">2. {gunluk.get("soru2","")}</div>
    <div class="journal-area" contenteditable="true" style="min-height:36px" placeholder="Düşüncelerini yaz..."></div>
    <div class="journal-q">3. {gunluk.get("soru3","")}</div>
    <div class="journal-area" contenteditable="true" style="min-height:36px" placeholder="Düşüncelerini yaz..."></div>
    <div class="journal-prompt">✏️ Tamamla: "{gunluk.get("tamamla","")}"</div>
    <div class="journal-prompt" style="margin-top:8px">🎨 Çiz: {gunluk.get("ciz","")}</div>
  </div>
  <!-- P17: Dijital Okuryazarlık -->
  <div class="pg" data-pg="17">
    <div class="pg-title">📱 Dijital Dünya: {dijital.get("baslik","")}</div>
    {dijital_tip_html}
    <div class="digi-warn">{dijital.get("tehlike","")}</div>
    <div class="digi-rule">{dijital.get("kural","")}</div>
  </div>
  <!-- P18: Sağlık & İyi Oluş -->
  <div class="pg" data-pg="18">
    <div class="pg-title">🏥 Sağlık Köşesi: {saglik.get("baslik","")}</div>
    <div class="health-info">{saglik.get("bilgi","")}</div>
    {saglik_tip_html}
    <div class="health-recipe">{saglik.get("tarif","")}</div>
  </div>
  <!-- P19: Gelecek Ay -->
  <div class="pg" data-pg="19">
    <div class="pg-title">🔮 Gelecek Ay</div>
    <div class="next-preview">
      <div class="next-icon">{gelecek.get("gelecek_ikon","📰")}</div>
      <div class="next-tema">{gelecek.get("gelecek_tema","")}</div>
      <div class="next-desc">{gelecek.get("on_izleme","")}</div>
    </div>
    <div class="next-prep">📝 Hazırlık: {gelecek.get("hazirlık","")}</div>
  </div>
  <!-- P20: Kariyer Keşfi -->
  <div class="pg" data-pg="20">
    <div class="pg-title">💼 Kariyer Keşfi: {kariyer.get("baslik","Meslekleri Tanıyalım")}</div>
    <div class="intro">{kariyer.get("giris","Gelecekte hangi mesleği yapmak istersin? Bu ay farklı meslekleri keşfedelim!")}</div>
    <div class="career-grid">{kariyer_html}</div>
    <div class="act-box">
      <b>🤔 Düşün & Yaz</b>
      <p>{kariyer.get("soru","Bu mesleklerden hangisi seni heyecanlandırıyor? Neden?")}</p>
    </div>
  </div>
  <!-- P21: Stres Yönetimi -->
  <div class="pg" data-pg="21">
    <div class="pg-title">🧘 Stres Yönetimi: {stres.get("baslik","Sakin Kalmanın Yolları")}</div>
    <div class="intro">{stres.get("giris","Stres hepimizin yaşadığı doğal bir duygu. Onu yönetmeyi öğrenelim!")}</div>
    <div class="breath-box">
      <div class="breath-circle" id="breathCircle">
        <span class="breath-text" id="breathText">Nefes Al</span>
      </div>
      <div style="text-align:center;margin-top:8px;font-size:11px;color:#4b5563">Daireye odaklan ve nefes egzersizi yap</div>
    </div>
    <div class="stress-techniques">{stres_teknik_html}</div>
  </div>
  <!-- P22: İletişim Becerileri -->
  <div class="pg" data-pg="22">
    <div class="pg-title">🗣️ İletişim Becerileri: {iletisim.get("baslik","Etkili İletişim")}</div>
    <div class="intro">{iletisim.get("giris","Doğru iletişim, güçlü ilişkilerin anahtarıdır.")}</div>
    <div class="comm-scenario">
      <div class="comm-scene-title">📋 Senaryo</div>
      <div class="comm-scene-text">{iletisim.get("senaryo","")}</div>
    </div>
    <div class="comm-correct">
      <div class="comm-correct-title">✅ Doğru Yaklaşım</div>
      <div class="comm-correct-text">{iletisim.get("dogru_yaklasim","")}</div>
    </div>
    <div class="comm-tips">{iletisim_ipucu_html}</div>
  </div>
  <!-- P23: Zaman Yönetimi -->
  <div class="pg" data-pg="23">
    <div class="pg-title">⏰ Zaman Yönetimi: {zaman.get("baslik","Zamanını Verimli Kullan")}</div>
    <div class="intro">{zaman.get("giris","Zamanını iyi planlamak, başarının ilk adımıdır.")}</div>
    <div class="time-grid">{zaman_matris_html}</div>
    <div class="act-box">
      <b>💡 İpucu</b>
      <p>{zaman.get("ipucu","Her gün en önemli 3 görevini belirle ve önce onları yap!")}</p>
    </div>
  </div>
  <!-- P24: Empati & Farkındalık -->
  <div class="pg" data-pg="24">
    <div class="pg-title">💞 Empati & Farkındalık: {empati.get("baslik","Başkalarını Anlamak")}</div>
    <div class="intro">{empati.get("giris","Empati, kendini başkasının yerine koyabilme becerisidir.")}</div>
    <div class="empathy-story">
      <div class="empathy-story-title">📖 Hikâye</div>
      <div class="empathy-story-text">{empati.get("hikaye","")}</div>
    </div>
    <div class="empathy-thought">
      <span class="empathy-icon">💭</span>
      <span>{empati.get("dusunce","Bu durumda sen olsaydın ne hissederdin?")}</span>
    </div>
    <div class="act-box">
      <b>🎯 Haftalık Görev</b>
      <p>{empati.get("aktivite","Bu hafta bir arkadaşına beklemediği bir iyilik yap.")}</p>
    </div>
  </div>
  <!-- P25: Kitap Kulübü -->
  <div class="pg" data-pg="25">
    <div class="pg-title">📚 Kitap Kulübü: {kitap.get("baslik","Ayın Kitabı")}</div>
    <div class="intro">{kitap.get("giris","Okumak, zihnin en güzel egzersizidir.")}</div>
    <div class="book-main">
      <div class="book-cover-icon">📕</div>
      <div class="book-info">
        <div class="book-title">{kitap.get("kitap","")}</div>
        <div class="book-author">{kitap.get("yazar","")}</div>
        <div class="book-desc">{kitap.get("ozet","")}</div>
      </div>
    </div>
    <div class="act-box">
      <b>❓ Tartışma Sorusu</b>
      <p>{kitap.get("tartisma","Bu kitapta en çok hangi karakter seni etkiledi?")}</p>
    </div>
    <div style="margin-top:12px">
      <div style="font-size:12px;font-weight:700;color:{renk1};margin-bottom:6px">📖 Diğer Öneriler</div>
      {kitap_oneri_html}
    </div>
  </div>
  <!-- P26: Sanat Terapisi -->
  <div class="pg" data-pg="26">
    <div class="pg-title">🎨 Sanat Terapisi: {sanat.get("baslik","Sanatla İfade")}</div>
    <div class="intro">{sanat.get("giris","Sanat, duygularını ifade etmenin en güzel yoludur.")}</div>
    <div class="art-card">
      <div class="art-activity-name">🖌️ {sanat.get("aktivite","")}</div>
      <div class="art-desc">{sanat.get("aciklama","")}</div>
      <div class="art-materials">
        <b>Malzemeler:</b> {sanat.get("malzemeler","")}
      </div>
      <div class="art-steps">
        <b>Nasıl Yapılır:</b>
        <div class="art-steps-text">{sanat.get("adimlar","")}</div>
      </div>
    </div>
    <div class="act-box">
      <b>💬 Paylaş</b>
      <p>{sanat.get("paylasim","Eserini sınıfla paylaş ve ne hissettiğini anlat!")}</p>
    </div>
  </div>
  <!-- P27: Doğa & Çevre -->
  <div class="pg" data-pg="27">
    <div class="pg-title">🌿 Doğa & Çevre: {doga.get("baslik","Doğayı Koruyalım")}</div>
    <div class="intro">{doga.get("giris","Doğa bizim evimiz. Onu tanımak ve korumak hepimizin görevi.")}</div>
    <div class="nature-info">
      <div class="nature-fact-title">🌍 Biliyor muydun?</div>
      <div class="nature-fact">{doga.get("bilgi","")}</div>
    </div>
    <div class="act-box">
      <b>🎯 Bu Ayın Görevi</b>
      <p>{doga.get("gorev","")}</p>
    </div>
    <div style="margin-top:12px;background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:10px;padding:12px">
      <div style="font-size:12px;font-weight:700;color:#10b981;margin-bottom:4px">🌱 Ekolojik Ayak İzi</div>
      <div style="font-size:11px;color:#a7f3d0;line-height:1.6">{doga.get("eco_tip","Plastik poşet yerine bez torba kullan!")}</div>
    </div>
  </div>
  <!-- P28: Minnettarlık -->
  <div class="pg" data-pg="28">
    <div class="pg-title">🙏 Minnettarlık Köşesi: {minnet.get("baslik","Minnettar Olmak")}</div>
    <div class="intro">{minnet.get("giris","Sahip olduklarımızı fark etmek, mutluluğun anahtarıdır.")}</div>
    <div class="grat-list">{minnet_liste_html}</div>
    <div class="act-box" style="margin-top:14px">
      <b>✏️ Senin Sıran</b>
      <p>Bugün minnettar olduğun 3 şeyi düşün ve bir kağıda yaz. Kalbe dokunduğunda ❤️ olsun!</p>
    </div>
  </div>
  <!-- P29: Arka Kapak -->
  <div class="pg" data-pg="29">
    <div class="back-cover">
      <div class="back-logo">{kat_ikon}</div>
      <div class="back-title">{kurum_adi}</div>
      <div class="back-subtitle">Rehberlik Servisi</div>
      <div class="back-edition">{kademe} Rehberlik Bülteni — {ay_adi} {yil}</div>
      <div class="back-stats">
        <div class="back-stat-item">📄 30 Sayfa</div>
        <div class="back-stat-item">🧠 Psikolojik Rehberlik</div>
        <div class="back-stat-item">📊 Etkileşimli İçerik</div>
        <div class="back-stat-item">🎯 Kazanım Odaklı</div>
      </div>
      <div class="back-closing">
        {gelecek.get("kapanış","Bir sonraki sayımızda görüşmek üzere! Kendinize iyi bakın. 💛")}
      </div>
      <div style="margin-top:18px;font-size:9px;color:rgba(255,255,255,.3)">
        <span style="color:{renk1};font-size:9px">✦ PREMIUM EDITION — 30 SAYFA ✦</span><br>
        © {yil} {kurum_adi} — Tüm hakları saklıdır.
      </div>
    </div>
  </div>
</div>
<div class="ctrls">
  <button class="btn" id="bP" onclick="go(-1)" disabled>◀ Önceki</button>
  <span class="pi" id="pi">1 / 30</span>
  <button class="btn" id="bN" onclick="go(1)">Sonraki ▶</button>
  <span style="width:1px;height:16px;background:rgba(255,255,255,.1)"></span>
  <button class="btn tts" id="bT" onclick="toggleTTS()">🔊 Sesli Oku<div class="tts-wave" id="wave"><span></span><span></span><span></span><span></span><span></span></div></button>
  <button class="btn pdf" onclick="printBulten()">📄 PDF</button>
  <button class="btn share" onclick="shareBulten()">📤 Paylaş</button>
</div>
</div>
<script>
const pgs=document.querySelectorAll('.pg'),total=pgs.length;
let cur=0,speaking=false,answered=0;
function go(d){{
  if(cur+d<0||cur+d>=total)return;
  pgs[cur].classList.remove('active');pgs[cur].style.display='none';
  cur+=d;pgs[cur].style.display='block';
  requestAnimationFrame(()=>pgs[cur].classList.add('active'));
  document.getElementById('pi').textContent=(cur+1)+' / '+total;
  document.getElementById('bP').disabled=cur<=0;
  document.getElementById('bN').disabled=cur>=total-1;
  document.getElementById('prog').style.width=((cur+1)/total*100)+'%';
  if(speaking){{stopTTS();startTTS()}}
}}
// Quiz
function checkAns(el){{
  if(el.classList.contains('correct')||el.classList.contains('wrong'))return;
  const q=el.dataset.q,c=parseInt(el.dataset.c),o=parseInt(el.dataset.o);
  const siblings=document.querySelectorAll('[data-q="'+q+'"]');
  siblings.forEach(s=>{{s.style.pointerEvents='none'}});
  if(o===c){{el.classList.add('correct')}}else{{el.classList.add('wrong');
    siblings.forEach(s=>{{if(parseInt(s.dataset.o)===c)s.classList.add('correct')}})}}
  answered++;
  if(answered>={len(quiz_items)}){{
    const correct=document.querySelectorAll('.q-opt.correct').length;
    const unique=new Set([...document.querySelectorAll('.q-opt.correct')].map(e=>e.dataset.q)).size;
    document.getElementById('quizScore').textContent='Sonuç: '+unique+'/{len(quiz_items)} doğru!';
    document.getElementById('quizResult').style.display='block';
  }}
}}
// Checklist
function toggleCl(el){{el.classList.toggle('checked')}}
// Hedef Planı
function toggleHedef(el){{el.classList.toggle('done')}}
// Minnettarlık
function toggleGrat(el){{el.classList.toggle('liked');const h=el.querySelector('.grat-heart');if(h)h.textContent=el.classList.contains('liked')?'❤️':'♡'}}
// Nefes Egzersizi
(function(){{
  const bc=document.getElementById('breathCircle'),bt=document.getElementById('breathText');
  if(!bc||!bt)return;
  const phases=[['Nefes Al',4000,'scale(1.3)'],['Tut',4000,'scale(1.3)'],['Nefes Ver',4000,'scale(1)'],['Bekle',2000,'scale(1)']];
  let pi=0;function runBreath(){{bt.textContent=phases[pi][0];bc.style.transform=phases[pi][2];bc.style.transition='transform '+phases[pi][1]+'ms ease';setTimeout(()=>{{pi=(pi+1)%4;runBreath()}},phases[pi][1])}}runBreath();
}})()
function selectDuygu(el){{
  document.querySelectorAll('.duygu-btn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
}}
// TTS — Ultra NRT
let synth=window.speechSynthesis,utt=null,trVoice=null;
function findBestVoice(){{
  const voices=synth.getVoices();
  trVoice=voices.find(v=>v.lang==='tr-TR'&&v.name.includes('Natural'))||
    voices.find(v=>v.lang==='tr-TR'&&!v.localService)||
    voices.find(v=>v.lang==='tr-TR')||
    voices.find(v=>v.lang.startsWith('tr'))||null;
}}
if(synth.onvoiceschanged!==undefined)synth.onvoiceschanged=findBestVoice;
findBestVoice();
function startTTS(){{
  const p=pgs[cur];if(!p)return;
  const txt=p.innerText.replace(/\\s+/g,' ').trim();
  if(!txt)return;
  utt=new SpeechSynthesisUtterance(txt);
  utt.lang='tr-TR';utt.rate=0.92;utt.pitch=1.05;utt.volume=1;
  if(trVoice)utt.voice=trVoice;
  utt.onend=()=>{{if(speaking&&cur<total-1){{go(1)}}else{{stopTTS()}}}};
  synth.speak(utt);
}}
function stopTTS(){{synth.cancel();speaking=false;
  document.getElementById('bT').classList.remove('on');
  document.getElementById('wave').classList.remove('on');
  document.getElementById('bT').firstChild.textContent='🔊 Sesli Oku';
}}
function toggleTTS(){{
  if(speaking){{stopTTS()}}
  else{{speaking=true;
    document.getElementById('bT').classList.add('on');
    document.getElementById('wave').classList.add('on');
    document.getElementById('bT').firstChild.textContent='⏹ Durdur';
    startTTS()}}
}}
// PDF
function printBulten(){{
  const all=document.querySelectorAll('.pg');
  all.forEach(p=>{{p.style.display='block';p.classList.add('active');p.style.position='relative';
    p.style.transform='none';p.style.opacity='1';p.style.pageBreakAfter='always'}});
  document.querySelector('.ctrls').style.display='none';
  document.querySelector('.hdr').style.position='relative';
  document.getElementById('prog').style.display='none';
  window.print();
  location.reload();
}}
// Share
function shareBulten(){{
  const text='{kurum_adi} - {kademe} Rehberlik Bülteni ({ay_adi} {yil})';
  if(navigator.share){{navigator.share({{title:text,text:text}}).catch(()=>{{}})}}
  else{{navigator.clipboard.writeText(text).then(()=>alert('Kopyalandı!')).catch(()=>{{}})}}
}}
document.addEventListener('keydown',e=>{{
  if(e.key==='ArrowRight'||e.key===' ')go(1);
  else if(e.key==='ArrowLeft')go(-1);
}});
</script></body></html>'''


def _generate_bulten_pdf(kademe: str, ay: int, yil: int, kurum_adi: str) -> bytes:
    """Rehberlik Bulteni icin profesyonel 20 sayfalik PDF olustur."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm, mm
        from reportlab.lib import colors as rl_colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, KeepTogether,
        )
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
        import io as _io
    except ImportError:
        return b""

    from utils.shared_data import ensure_turkish_pdf_fonts
    font_name, font_bold = ensure_turkish_pdf_fonts()

    # ── Veri toplama ──
    tema_baslik, tema_ikon = _BULTEN_TEMALAR.get(ay, ("Rehberlik Bulteni", ""))
    renk1, renk2, kat_ikon = _BULTEN_RENK.get(kademe, ("#6b7280", "#4b5563", ""))
    ay_adi = _AYLAR_TR.get(ay, "")
    icerik = _BULTEN_ICERIK.get((kademe, ay), {})
    kademe_grup = "kucuk" if kademe in ("Anaokulu", "İlkokul") else "buyuk"

    takvim = _BULTEN_TAKVIM.get(ay, [])
    mot_text, mot_author = _BULTEN_MOTIVASYON.get(ay, ("", ""))
    infog = _BULTEN_INFOGRAFIK.get(ay, [])
    vaka = _BULTEN_VAKA.get(ay, ("", "", ""))
    quiz_items = _BULTEN_TEST.get(ay, [])
    cl_items = _BULTEN_CHECKLIST.get(ay, [])
    kaynak_data = _BULTEN_KAYNAKLAR.get(ay, {}).get(kademe_grup, {})
    veli_data = _BULTEN_VELI.get(ay, {}).get(kademe_grup, {})
    hedef_data = _BULTEN_HEDEF.get(ay, {})
    uzman = _BULTEN_UZMAN.get(ay, {})
    sel = _BULTEN_SEL.get(ay, {})
    akt = _BULTEN_AKTIVITE.get(ay, {})
    dunya = _BULTEN_DUNYA.get(ay, [])
    bulmaca = _BULTEN_BULMACA.get(ay, {})
    rolmodel = _BULTEN_ROLMODEL.get(ay, {})
    gunluk = _BULTEN_GUNLUK.get(ay, {})
    dijital = _BULTEN_DIJITAL.get(ay, {})
    saglik = _BULTEN_SAGLIK.get(ay, {})
    gelecek = _BULTEN_GELECEK.get(ay, {})

    # ── Renkler ──
    c_primary = rl_colors.HexColor(renk1)
    c_secondary = rl_colors.HexColor(renk2)
    c_dark = rl_colors.HexColor("#0a0e27")
    c_light_bg = rl_colors.HexColor("#fffdf9")
    c_white = rl_colors.white
    c_text = rl_colors.HexColor("#1f2937")
    c_muted = rl_colors.HexColor("#374151")
    c_accent_light = rl_colors.HexColor("#fffbeb")

    # ── Boyut ──
    PAGE_W, PAGE_H = A4
    MARGIN = 2 * cm
    CONTENT_W = PAGE_W - 2 * MARGIN

    buf = _io.BytesIO()

    footer_text = f"SmartCampus AI  -  Rehberlik Servisi  -  {kademe}  -  {ay_adi} {yil}"

    def _page_footer(canvas, doc):
        canvas.saveState()
        # Kuse kagit arka plan efekti
        canvas.setFillColor(rl_colors.Color(0.99, 0.98, 0.96))
        canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        # Header bar — koyu navy + altin aksanli
        canvas.setFillColor(c_dark)
        canvas.rect(0, PAGE_H - 20, PAGE_W, 20, fill=1, stroke=0)
        canvas.setFillColor(rl_colors.HexColor("#c9a84c"))
        canvas.rect(0, PAGE_H - 22, PAGE_W, 2, fill=1, stroke=0)
        canvas.setFont(font_name, 7)
        canvas.drawString(MARGIN, PAGE_H - 15, f"{kademe} Rehberlik Bulteni | {tema_baslik}")
        canvas.setFillColor(rl_colors.HexColor("#94a3b8"))
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 15, f"Sayfa {doc.page}")
        # Footer — koyu navy + altin cizgi
        canvas.setFillColor(c_dark)
        canvas.rect(0, 0, PAGE_W, 18, fill=1, stroke=0)
        canvas.setFillColor(rl_colors.HexColor("#c9a84c"))
        canvas.rect(0, 18, PAGE_W, 1.5, fill=1, stroke=0)
        canvas.setFillColor(rl_colors.HexColor("#c9a84c"))
        canvas.setFont(font_name, 6)
        canvas.drawCentredString(PAGE_W / 2, 6, footer_text)
        canvas.restoreState()

    def _cover_page(canvas, doc):
        """Ultra profesyonel kuse kapak sayfasi."""
        canvas.saveState()
        # Gradient arka plan (koyu -> acik)
        steps = 30
        for i in range(steps):
            ratio = i / steps
            r = 0.04 + ratio * 0.06
            g = 0.06 + ratio * 0.08
            b = 0.15 + ratio * 0.12
            canvas.setFillColor(rl_colors.Color(r, g, b))
            y = PAGE_H * (1 - ratio / 1.0)
            canvas.rect(0, y - PAGE_H / steps, PAGE_W, PAGE_H / steps + 1, fill=1, stroke=0)

        # Ust altin serit
        canvas.setFillColor(rl_colors.HexColor("#c9a84c"))
        canvas.rect(0, PAGE_H - 10, PAGE_W, 10, fill=1, stroke=0)

        # Kurum adi
        canvas.setFillColor(rl_colors.HexColor("#c9a84c"))
        canvas.setFont(font_bold, 10)
        canvas.drawCentredString(PAGE_W / 2, PAGE_H - 40, (kurum_adi or "SmartCampus AI").upper())
        canvas.setFont(font_name, 8)
        canvas.setFillColor(rl_colors.HexColor("#94a3b8"))
        canvas.drawCentredString(PAGE_W / 2, PAGE_H - 55, "Rehberlik ve Psikolojik Danismanlik Servisi")

        # Altin ayirici cizgi
        canvas.setStrokeColor(rl_colors.HexColor("#c9a84c"))
        canvas.setLineWidth(1)
        canvas.line(PAGE_W / 2 - 80, PAGE_H - 68, PAGE_W / 2 + 80, PAGE_H - 68)

        # Merkez alan
        cx, cy = PAGE_W / 2, PAGE_H / 2 + 60

        # Buyuk baslik
        canvas.setFillColor(c_white)
        canvas.setFont(font_bold, 32)
        canvas.drawCentredString(cx, cy + 30, "REHBERLIK")
        canvas.setFont(font_bold, 28)
        canvas.drawCentredString(cx, cy - 5, "BULTENI")

        # Altin ayirici
        canvas.setStrokeColor(rl_colors.HexColor("#c9a84c"))
        canvas.setLineWidth(2)
        canvas.line(cx - 60, cy - 22, cx + 60, cy - 22)

        # Tema
        canvas.setFillColor(rl_colors.HexColor("#c9a84c"))
        canvas.setFont(font_bold, 18)
        canvas.drawCentredString(cx, cy - 50, tema_baslik)

        # Ay/Yil — buyuk
        canvas.setFillColor(c_white)
        canvas.setFont(font_bold, 40)
        canvas.drawCentredString(cx, cy - 100, f"{ay_adi}")
        canvas.setFont(font_name, 16)
        canvas.setFillColor(rl_colors.HexColor("#94a3b8"))
        canvas.drawCentredString(cx, cy - 125, f"{yil}")

        # Kademe rozet — altin cerceveli
        canvas.setFillColor(rl_colors.HexColor("#c9a84c"))
        badge_w, badge_h = 160, 36
        canvas.roundRect(cx - badge_w / 2, cy - 180, badge_w, badge_h, 12, fill=1, stroke=0)
        canvas.setFillColor(c_dark)
        canvas.setFont(font_bold, 14)
        canvas.drawCentredString(cx, cy - 168, kademe)

        # Alt altin serit
        canvas.setFillColor(rl_colors.HexColor("#c9a84c"))
        canvas.rect(0, 0, PAGE_W, 12, fill=1, stroke=0)
        # Alt yazi
        canvas.setFillColor(c_dark)
        canvas.setFont(font_name, 7)
        canvas.drawCentredString(PAGE_W / 2, 3, "Aylik Egitim ve Rehberlik Bulteni")

        # Kenar — ince altin cerceve
        canvas.setStrokeColor(rl_colors.HexColor("#c9a84c"))
        canvas.setLineWidth(0.5)
        canvas.rect(15, 15, PAGE_W - 30, PAGE_H - 30, fill=0, stroke=1)

        canvas.restoreState()

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        topMargin=2.2 * cm, bottomMargin=1.8 * cm,
        leftMargin=MARGIN, rightMargin=MARGIN,
    )

    styles = getSampleStyleSheet()
    # Ozel stiller
    s_title = ParagraphStyle("BTitle", fontName=font_bold, fontSize=16,
                              leading=20, alignment=TA_CENTER, spaceAfter=8, textColor=c_dark)
    s_h1 = ParagraphStyle("BH1", fontName=font_bold, fontSize=14,
                            leading=18, spaceAfter=6, spaceBefore=10, textColor=c_dark)
    s_h2 = ParagraphStyle("BH2", fontName=font_bold, fontSize=12,
                            leading=15, spaceAfter=4, spaceBefore=6, textColor=c_text)
    s_h3 = ParagraphStyle("BH3", fontName=font_bold, fontSize=10,
                            leading=13, spaceAfter=3, spaceBefore=4, textColor=c_text)
    s_body = ParagraphStyle("BBody", fontName=font_name, fontSize=10,
                              leading=14, spaceAfter=5, alignment=TA_JUSTIFY, textColor=c_text)
    s_body_sm = ParagraphStyle("BBodySm", fontName=font_name, fontSize=9,
                                leading=12, spaceAfter=4, textColor=c_text)
    s_quote = ParagraphStyle("BQuote", fontName=font_name, fontSize=10,
                              leading=14, alignment=TA_CENTER, spaceAfter=4,
                              textColor=c_muted, fontStyle="italic" if font_name == "Helvetica" else None)
    s_quote_author = ParagraphStyle("BQuoteAuth", fontName=font_bold, fontSize=9,
                                      leading=12, alignment=TA_CENTER, spaceAfter=8, textColor=c_text)
    s_footer_note = ParagraphStyle("BFoot", fontName=font_name, fontSize=7,
                                     leading=10, alignment=TA_CENTER, textColor=c_muted)
    s_bullet = ParagraphStyle("BBullet", fontName=font_name, fontSize=9,
                                leading=13, spaceAfter=2, leftIndent=12,
                                bulletIndent=0, textColor=c_text)
    s_center = ParagraphStyle("BCenter", fontName=font_name, fontSize=9,
                                leading=13, alignment=TA_CENTER, spaceAfter=4, textColor=c_text)

    def _t(text):
        """HTML-safe text."""
        return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _section_header(title, color=None):
        """Renkli accent bar ile bolum basligi."""
        clr = color or c_primary
        bar = Table([[""]], colWidths=[CONTENT_W], rowHeights=[4])
        bar.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), clr),
            ("LEFTPADDING", (0, 0), (0, 0), 0),
            ("RIGHTPADDING", (0, 0), (0, 0), 0),
            ("TOPPADDING", (0, 0), (0, 0), 0),
            ("BOTTOMPADDING", (0, 0), (0, 0), 0),
        ]))
        return [bar, Spacer(1, 4), Paragraph(_t(title), s_h1)]

    def _info_box(text, bg_color=None):
        """Arka planli bilgi kutusu."""
        bg = bg_color or c_accent_light
        p = Paragraph(_t(text), s_body)
        t = Table([[p]], colWidths=[CONTENT_W - 12])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), bg),
            ("LEFTPADDING", (0, 0), (0, 0), 8),
            ("RIGHTPADDING", (0, 0), (0, 0), 8),
            ("TOPPADDING", (0, 0), (0, 0), 6),
            ("BOTTOMPADDING", (0, 0), (0, 0), 6),
            ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ]))
        return t

    def _spacer(h=0.3):
        return Spacer(1, h * cm)

    elements = []

    # ────────────────────────────────────────────────────────
    # SAYFA 1 — Kapak (bos sayfa, canvas uzerinde cizilecek)
    # ────────────────────────────────────────────────────────
    # Kapak canvas'ta cizilir, icerik alani bos birakilir
    elements.append(Spacer(1, 1))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 2 — Icerik
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header(f"{tema_baslik} - Icerik"))
    elements.append(_spacer(0.2))
    giris = icerik.get("g", "")
    if giris:
        elements.append(_info_box(giris))
        elements.append(_spacer(0.3))
    for baslik_b, txt_b in icerik.get("b", []):
        elements.append(Paragraph(f"<b>{_t(baslik_b)}</b>", s_h2))
        elements.append(Paragraph(_t(txt_b), s_body))
        elements.append(_spacer(0.15))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 3 — Infografik + Motivasyon
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Infografik"))
    elements.append(_spacer(0.2))
    if infog:
        info_rows = []
        row = []
        for idx_i, item in enumerate(infog):
            if len(item) >= 3:
                lbl, val, ico = item[0], item[1], item[2]
            else:
                lbl, val, ico = item[0] if len(item) > 0 else "", item[1] if len(item) > 1 else "", ""
            cell_p = Paragraph(f"<b>{_t(lbl)}</b><br/><font size='8'>{_t(val)}</font>", s_center)
            row.append(cell_p)
            if len(row) == 2 or idx_i == len(infog) - 1:
                while len(row) < 2:
                    row.append("")
                info_rows.append(row)
                row = []
        if info_rows:
            cw = CONTENT_W / 2 - 4
            tbl = Table(info_rows, colWidths=[cw, cw])
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), c_light_bg),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, rl_colors.HexColor("#e2e8f0")),
                ("ROUNDEDCORNERS", [4, 4, 4, 4]),
            ]))
            elements.append(tbl)
    elements.append(_spacer(0.4))
    # Motivasyon
    elements.extend(_section_header("Motivasyon"))
    elements.append(_spacer(0.2))
    if mot_text:
        elements.append(Paragraph(f'<i>"{_t(mot_text)}"</i>', s_quote))
        if mot_author:
            elements.append(Paragraph(f"- {_t(mot_author)}", s_quote_author))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 4 — Vaka Ornegi
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Vaka Ornegi"))
    elements.append(_spacer(0.2))
    if isinstance(vaka, (tuple, list)) and len(vaka) >= 3:
        elements.append(Paragraph(f"<b>Hikaye:</b> {_t(vaka[0])}", s_body))
        elements.append(_spacer(0.2))
        elements.append(Paragraph(f"<b>Soru:</b> {_t(vaka[1])}", s_body))
        elements.append(_spacer(0.2))
        elements.append(Paragraph(f"<b>Onerilen Yaklasim:</b> {_t(vaka[2])}", s_body))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 5 — Takvim + Etkinlik
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Takvim ve Etkinlik"))
    elements.append(_spacer(0.2))
    if takvim:
        cal_rows = [[Paragraph("<b>Tarih</b>", s_body_sm), Paragraph("<b>Etkinlik</b>", s_body_sm)]]
        for tarih, etkinlik in takvim:
            cal_rows.append([Paragraph(_t(tarih), s_body_sm), Paragraph(_t(etkinlik), s_body_sm)])
        cal_tbl = Table(cal_rows, colWidths=[4 * cm, CONTENT_W - 4 * cm])
        cal_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), c_primary),
            ("TEXTCOLOR", (0, 0), (-1, 0), c_white),
            ("BACKGROUND", (0, 1), (-1, -1), c_light_bg),
            ("GRID", (0, 0), (-1, -1), 0.5, rl_colors.HexColor("#e2e8f0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(cal_tbl)
    elements.append(_spacer(0.4))
    # Aylik aktivite
    etkinlik_text = icerik.get("e", "")
    if etkinlik_text:
        elements.append(Paragraph("<b>Aylik Etkinlik Onerisi</b>", s_h2))
        elements.append(_info_box(etkinlik_text))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 6 — Veli Kosesi
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Veli Kosesi"))
    elements.append(_spacer(0.2))
    if veli_data:
        mesaj = veli_data.get("mesaj", "")
        if mesaj:
            elements.append(_info_box(mesaj))
            elements.append(_spacer(0.2))
        etkinlikler = veli_data.get("etkinlikler", [])
        if etkinlikler:
            elements.append(Paragraph("<b>Etkinlik Onerileri</b>", s_h3))
            for et in etkinlikler:
                elements.append(Paragraph(f"  * {_t(et)}", s_bullet))
            elements.append(_spacer(0.2))
        ipucu = veli_data.get("ipucu", "")
        if ipucu:
            elements.append(Paragraph(f"<b>Ipucu:</b> {_t(ipucu)}", s_body))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 7 — Mini Test
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Mini Oz Degerlendirme Testi"))
    elements.append(_spacer(0.2))
    if quiz_items:
        for q_idx, q_item in enumerate(quiz_items, 1):
            soru_text = q_item[0] if len(q_item) > 0 else ""
            secenekler = q_item[1] if len(q_item) > 1 else []
            dogru_idx = q_item[2] if len(q_item) > 2 else -1
            elements.append(Paragraph(f"<b>{q_idx}. {_t(soru_text)}</b>", s_body))
            for s_idx, sec in enumerate(secenekler):
                marker = " [DOGRU]" if s_idx == dogru_idx else ""
                harf = chr(65 + s_idx)
                elements.append(Paragraph(f"    {harf}) {_t(sec)}{marker}", s_body_sm))
            elements.append(_spacer(0.15))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 8 — Kontrol Listesi + Kaynaklar
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Kontrol Listesi"))
    elements.append(_spacer(0.2))
    if cl_items:
        for cli in cl_items:
            elements.append(Paragraph(f"[ ] {_t(cli)}", s_bullet))
        elements.append(_spacer(0.3))

    elements.extend(_section_header("Kaynak Onerileri", c_secondary))
    elements.append(_spacer(0.2))
    if kaynak_data:
        for kaynak_tip, items in kaynak_data.items():
            tip_label = {"kitap": "Kitaplar", "video": "Videolar", "uygulama": "Uygulamalar"}.get(kaynak_tip, kaynak_tip)
            elements.append(Paragraph(f"<b>{tip_label}:</b>", s_h3))
            if isinstance(items, list):
                for item in items:
                    elements.append(Paragraph(f"  - {_t(item)}", s_body_sm))
            elements.append(_spacer(0.1))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 9 — Hedef Plani
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Hedef Plani"))
    elements.append(_spacer(0.2))
    if hedef_data:
        h_baslik = hedef_data.get("baslik", "")
        h_soz = hedef_data.get("soz", "")
        if h_baslik:
            elements.append(Paragraph(f"<b>{_t(h_baslik)}</b>", s_h2))
        if h_soz:
            elements.append(Paragraph(f"<i>{_t(h_soz)}</i>", s_body))
            elements.append(_spacer(0.2))
        for hedef in hedef_data.get("hedefler", []):
            elements.append(Paragraph(f"O  {_t(hedef)}", s_bullet))
        elements.append(_spacer(0.3))
        # Duygu secimi
        duygular = hedef_data.get("duygular", [])
        if duygular:
            elements.append(Paragraph("<b>Bu ay kendimi nasil hissediyorum?</b>", s_h3))
            duygu_strs = [d[0] if isinstance(d, (tuple, list)) else str(d) for d in duygular]
            elements.append(Paragraph("  |  ".join(_t(d) for d in duygu_strs), s_center))
        degerlendirme = hedef_data.get("degerlendir", "")
        if degerlendirme:
            elements.append(_spacer(0.2))
            elements.append(Paragraph(f"<b>Degerlendirme:</b> {_t(degerlendirme)}", s_body))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 10 — Oneriler (ipuclari + etkinlik from icerik)
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Oneriler"))
    elements.append(_spacer(0.2))
    ipuclari = icerik.get("v", [])
    if ipuclari:
        elements.append(Paragraph("<b>Velilere Ipuclari</b>", s_h2))
        for tip in ipuclari:
            elements.append(Paragraph(f"  * {_t(tip)}", s_bullet))
        elements.append(_spacer(0.3))
    etkinlik_i = icerik.get("e", "")
    if etkinlik_i:
        elements.append(Paragraph("<b>Etkinlik</b>", s_h2))
        elements.append(_info_box(etkinlik_i))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 11 — Uzman Gorusu
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Uzman Gorusu"))
    elements.append(_spacer(0.2))
    if uzman:
        uz_baslik = uzman.get("baslik", "")
        uz_uzman = uzman.get("uzman", "")
        uz_icerik = uzman.get("icerik", "")
        uz_oneri = uzman.get("oneri", "")
        if uz_uzman:
            # Uzman rozet
            badge_p = Paragraph(f"<b>{_t(uz_uzman)}</b>", s_center)
            badge_t = Table([[badge_p]], colWidths=[CONTENT_W / 2])
            badge_t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), c_primary),
                ("TEXTCOLOR", (0, 0), (0, 0), c_white),
                ("ALIGN", (0, 0), (0, 0), "CENTER"),
                ("TOPPADDING", (0, 0), (0, 0), 4),
                ("BOTTOMPADDING", (0, 0), (0, 0), 4),
                ("ROUNDEDCORNERS", [4, 4, 4, 4]),
            ]))
            elements.append(badge_t)
            elements.append(_spacer(0.2))
        if uz_baslik:
            elements.append(Paragraph(f"<b>{_t(uz_baslik)}</b>", s_h2))
        if uz_icerik:
            for para in str(uz_icerik).split("\n\n"):
                para = para.strip()
                if para:
                    elements.append(Paragraph(_t(para), s_body))
                    elements.append(_spacer(0.1))
        if uz_oneri:
            elements.append(_spacer(0.2))
            elements.append(Paragraph(f"<b>Oneri:</b> {_t(uz_oneri)}", s_body))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 12 — SEL Beceri
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Sosyal-Duygusal Ogrenme (SEL)"))
    elements.append(_spacer(0.2))
    if sel:
        beceri = sel.get("beceri", "")
        tanim_sel = sel.get("tanim", "")
        neden = sel.get("neden", "")
        adimlar = sel.get("adimlar", [])
        senaryo = sel.get("senaryo", "")
        if beceri:
            elements.append(Paragraph(f"<b>Beceri: {_t(beceri)}</b>", s_h2))
        if tanim_sel:
            elements.append(Paragraph(f"<b>Tanim:</b> {_t(tanim_sel)}", s_body))
        if neden:
            elements.append(Paragraph(f"<b>Neden Onemli:</b> {_t(neden)}", s_body))
        if adimlar:
            elements.append(_spacer(0.15))
            elements.append(Paragraph("<b>Adimlar:</b>", s_h3))
            for a_idx, adim in enumerate(adimlar, 1):
                elements.append(Paragraph(f"  {a_idx}. {_t(adim)}", s_bullet))
        if senaryo:
            elements.append(_spacer(0.2))
            elements.append(Paragraph(f"<b>Senaryo:</b> {_t(senaryo)}", s_body))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 13 — Aktivite
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Aktivite"))
    elements.append(_spacer(0.2))
    if akt:
        akt_baslik = akt.get("baslik", "")
        akt_tur = akt.get("tur", "")
        akt_malzeme = akt.get("malzemeler", [])
        akt_adimlar = akt.get("adimlar", [])
        akt_kazanim = akt.get("kazanim", "")
        if akt_baslik:
            elements.append(Paragraph(f"<b>{_t(akt_baslik)}</b>", s_h2))
        if akt_tur:
            elements.append(Paragraph(f"<b>Tur:</b> {_t(akt_tur)}", s_body))
        if akt_malzeme:
            elements.append(Paragraph(f"<b>Malzemeler:</b> {', '.join(_t(m) for m in akt_malzeme)}", s_body))
        if akt_adimlar:
            elements.append(_spacer(0.15))
            elements.append(Paragraph("<b>Adimlar:</b>", s_h3))
            for ai, ad in enumerate(akt_adimlar, 1):
                elements.append(Paragraph(f"  {ai}. {_t(ad)}", s_bullet))
        if akt_kazanim:
            elements.append(_spacer(0.2))
            elements.append(Paragraph(f"<b>Kazanim:</b> {_t(akt_kazanim)}", s_body))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 14 — Dunyadan Ornekler
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Dunyadan Ornekler"))
    elements.append(_spacer(0.2))
    if dunya:
        for ulke, aciklama in dunya:
            ulke_clean = _t(ulke)
            elements.append(Paragraph(f"<b>{ulke_clean}</b>", s_h3))
            elements.append(Paragraph(_t(aciklama), s_body))
            elements.append(_spacer(0.15))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 15 — Bilmece & Eglence
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Bilmece ve Eglence"))
    elements.append(_spacer(0.2))
    if bulmaca:
        bilmeceler = bulmaca.get("bilmece", [])
        if bilmeceler:
            elements.append(Paragraph("<b>Bilmeceler</b>", s_h2))
            for soru_b, cevap_b in bilmeceler:
                elements.append(Paragraph(f"<b>S:</b> {_t(soru_b)}", s_body))
                elements.append(Paragraph(f"<b>C:</b> {_t(cevap_b)}", s_body_sm))
                elements.append(_spacer(0.1))
        kelime = bulmaca.get("kelime", "")
        if kelime:
            elements.append(_spacer(0.2))
            elements.append(Paragraph("<b>Kelime Oyunu</b>", s_h2))
            elements.append(Paragraph(_t(kelime), s_body))
        eglence = bulmaca.get("eglence", "")
        if eglence:
            elements.append(_spacer(0.2))
            elements.append(Paragraph("<b>Eglenceli Bilgi</b>", s_h2))
            elements.append(_info_box(eglence))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 16 — Rol Model
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Rol Model"))
    elements.append(_spacer(0.2))
    if rolmodel:
        rm_isim = rolmodel.get("isim", "")
        rm_alan = rolmodel.get("alan", "")
        rm_hikaye = rolmodel.get("hikaye", "")
        rm_soz = rolmodel.get("soz", "")
        rm_ders = rolmodel.get("ders", "")
        if rm_isim:
            elements.append(Paragraph(f"<b>{_t(rm_isim)}</b>", s_h2))
        if rm_alan:
            elements.append(Paragraph(f"<i>{_t(rm_alan)}</i>", s_body))
        if rm_hikaye:
            elements.append(_spacer(0.15))
            elements.append(Paragraph(_t(rm_hikaye), s_body))
        if rm_soz:
            elements.append(_spacer(0.2))
            elements.append(Paragraph(f'<i>"{_t(rm_soz)}"</i>', s_quote))
        if rm_ders:
            elements.append(_spacer(0.2))
            elements.append(Paragraph(f"<b>Alinan Ders:</b> {_t(rm_ders)}", s_body))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 17 — Gunluk / Yansitma
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Gunluk / Yansitma"))
    elements.append(_spacer(0.2))
    if gunluk:
        aciklama_g = gunluk.get("aciklama", "")
        if aciklama_g:
            elements.append(_info_box(aciklama_g))
            elements.append(_spacer(0.2))
        for q_key in ["soru1", "soru2", "soru3", "soru4"]:
            q_val = gunluk.get(q_key, "")
            if q_val:
                elements.append(Paragraph(f"<b>{_t(q_val)}</b>", s_body))
                elements.append(Paragraph("_______________________________________________", s_body_sm))
                elements.append(_spacer(0.15))
        tamamla = gunluk.get("tamamla", "")
        if tamamla:
            elements.append(Paragraph(f"<b>Tamamla:</b> {_t(tamamla)}", s_body))
            elements.append(Paragraph("_______________________________________________", s_body_sm))
            elements.append(_spacer(0.15))
        yansitma_g = gunluk.get("yansitma", "")
        if yansitma_g:
            elements.append(Paragraph("<b>Yansitma Etkinligi</b>", s_h3))
            elements.append(_info_box(yansitma_g))
            elements.append(_spacer(0.15))
        ciz = gunluk.get("ciz", "")
        if ciz:
            elements.append(Paragraph(f"<b>Ciz:</b> {_t(ciz)}", s_body))
            draw_box = Table([[""]], colWidths=[CONTENT_W - 20], rowHeights=[3 * cm])
            draw_box.setStyle(TableStyle([
                ("BOX", (0, 0), (0, 0), 0.5, c_muted),
                ("BACKGROUND", (0, 0), (0, 0), c_light_bg),
            ]))
            elements.append(draw_box)
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 18 — Dijital Okuryazarlik
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Dijital Okuryazarlik"))
    elements.append(_spacer(0.2))
    if dijital:
        dij_baslik = dijital.get("baslik", "")
        dij_ipuclari = dijital.get("ipuclari", [])
        dij_tehlike = dijital.get("tehlike", "")
        dij_kural = dijital.get("kural", "")
        if dij_baslik:
            elements.append(Paragraph(f"<b>{_t(dij_baslik)}</b>", s_h2))
        if dij_ipuclari:
            for dip in dij_ipuclari:
                elements.append(Paragraph(f"  * {_t(dip)}", s_bullet))
            elements.append(_spacer(0.2))
        if dij_tehlike:
            # Uyari kutusu
            warn_p = Paragraph(f"<b>Uyari:</b> {_t(dij_tehlike)}", s_body)
            warn_t = Table([[warn_p]], colWidths=[CONTENT_W - 12])
            warn_t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), rl_colors.HexColor("#fef3c7")),
                ("LEFTPADDING", (0, 0), (0, 0), 8),
                ("RIGHTPADDING", (0, 0), (0, 0), 8),
                ("TOPPADDING", (0, 0), (0, 0), 6),
                ("BOTTOMPADDING", (0, 0), (0, 0), 6),
                ("ROUNDEDCORNERS", [4, 4, 4, 4]),
            ]))
            elements.append(warn_t)
            elements.append(_spacer(0.2))
        if dij_kural:
            elements.append(Paragraph(f"<b>{_t(dij_kural)}</b>", s_body))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 19 — Saglik Kosesi
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Saglik Kosesi"))
    elements.append(_spacer(0.2))
    if saglik:
        sag_baslik = saglik.get("baslik", "")
        sag_bilgi = saglik.get("bilgi", "")
        sag_ipuclari = saglik.get("ipuclari", [])
        sag_tarif = saglik.get("tarif", "")
        if sag_baslik:
            elements.append(Paragraph(f"<b>{_t(sag_baslik)}</b>", s_h2))
        if sag_bilgi:
            elements.append(Paragraph(_t(sag_bilgi), s_body))
            elements.append(_spacer(0.2))
        if sag_ipuclari:
            elements.append(Paragraph("<b>Ipuclari:</b>", s_h3))
            for sip in sag_ipuclari:
                elements.append(Paragraph(f"  * {_t(sip)}", s_bullet))
            elements.append(_spacer(0.2))
        if sag_tarif:
            elements.append(Paragraph(f"<b>Saglikli Tarif:</b> {_t(sag_tarif)}", s_body))
    elements.append(PageBreak())

    # ────────────────────────────────────────────────────────
    # SAYFA 20 — Gelecek Ay + Kapanis
    # ────────────────────────────────────────────────────────
    elements.extend(_section_header("Gelecek Ay On Izleme"))
    elements.append(_spacer(0.2))
    if gelecek:
        gel_tema = gelecek.get("gelecek_tema", "")
        gel_on = gelecek.get("on_izleme", "")
        gel_hazirlik = gelecek.get("hazirlık", "") or gelecek.get("hazırlık", "")
        gel_kapanis = gelecek.get("kapanış", "") or gelecek.get("kapanış", "")
        if gel_tema:
            elements.append(Paragraph(f"<b>Gelecek Ayin Temasi:</b> {_t(gel_tema)}", s_h2))
        if gel_on:
            elements.append(Paragraph(_t(gel_on), s_body))
            elements.append(_spacer(0.2))
        if gel_hazirlik:
            elements.append(Paragraph(f"<b>Hazirlik:</b> {_t(gel_hazirlik)}", s_body))
            elements.append(_spacer(0.2))
        if gel_kapanis:
            elements.append(_spacer(0.3))
            elements.extend(_section_header("Kapanis Mesaji", c_secondary))
            elements.append(_spacer(0.2))
            elements.append(_info_box(gel_kapanis))

    elements.append(_spacer(0.5))
    # Kapanis branding
    elements.append(Paragraph("SmartCampus AI - Rehberlik ve Psikolojik Danismanlik Servisi", s_footer_note))
    elements.append(Paragraph(f"{kurum_adi} - {kademe} - {ay_adi} {yil}", s_footer_note))
    elements.append(Paragraph("Bu bulten SmartCampus AI tarafindan otomatik olarak olusturulmustur.", s_footer_note))

    # ── PDF Olustur ──
    def _first_page(canvas, doc):
        _cover_page(canvas, doc)

    def _later_pages(canvas, doc):
        _page_footer(canvas, doc)

    doc.build(elements, onFirstPage=_first_page, onLaterPages=_later_pages)
    return buf.getvalue()


# ============================================================
# SEKME: MEB STANDART FORMLAR (36 Form)
# ============================================================

_MEB_BASE = "https://altinorduram.meb.k12.tr"

_MEB_FORMLAR = [
    # (Kategori, Form Adı, Dosya Yolu, İkon, Renk)
    # ── GÖRÜŞME FORMLARI ──
    ("Görüşme", "Öğrenci Görüşme Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095047_YYRENCY_GYRYYME_FORMU.docx", "💬", "#7c3aed"),
    ("Görüşme", "Öğrenci Ön Görüşme Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095152_YYRENCY_YN_GYRYYME_FORMU.docx", "💬", "#7c3aed"),
    ("Görüşme", "Veli Görüşme Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095651_VELY_GYRYYME_FORMU.docx", "👨‍👩‍👧", "#7c3aed"),
    ("Görüşme", "Öğretmen İle Görüşme Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095312_YYRETMEN_YLE_GYRYYME_FORMU.docx", "👨‍🏫", "#7c3aed"),
    ("Görüşme", "Disiplin Kurulu İçin Öğrenci Görüşme Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094501_DYSYPLYK_KURULU_YYYN_YYRENCY_GYRYYME_FORMU.docx", "⚖️", "#7c3aed"),
    # ── GÖZLEM & DEĞERLENDİRME ──
    ("Gözlem", "Öğrenci Gözlem Kaydı", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095111_YYRENCY_GYZLEM_KAYDI.docx", "👁️", "#3b82f6"),
    ("Gözlem", "Aile İçi Gözlem Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094257_AYLE_YYY_GYZLEM_FORMU.docx", "🏠", "#3b82f6"),
    ("Gözlem", "Özel Öğrenme Güçlüğü Gözlem Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095338_YZEL_YYRENME_GYYLYYY_GYZLEM_FORMU.docx", "📖", "#3b82f6"),
    ("Gözlem", "Dikkat Eksikliği ve Hiperaktivite Bozukluğu Gözlem Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094441_DYKKAT_EKSYKLYYY_VE_HYPERAKTYVYTE_BOZUKLUYU_DYRTYSELLYK_GYZLEM_FORMU.docx", "🧠", "#3b82f6"),
    # ── AİLE ──
    ("Aile", "Aile Bilgi Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094233_AYLE_BYLGY_FORMU.docx", "📋", "#0d9488"),
    ("Aile", "Ev Ziyareti Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094634_EV_ZYYARETY_FORMU.docx", "🏡", "#0d9488"),
    ("Aile", "Çocuğumu Tanıyorum Kendimi Tanıyorum Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094423_YOCUGUMU_TANIYORUM_KENDYMY_TANIYORUM_FORMU.docx", "👶", "#0d9488"),
    # ── YÖNLENDIRME ──
    ("Yönlendirme", "Eğitsel Değerlendirme İsteği Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094521_EYYTSEL_DEYERLENDYRME_YSTEYY_FORMU.docx", "📝", "#f59e0b"),
    ("Yönlendirme", "Psikolojik Destek Yönlendirme Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095405_PSiKOLOJiK_DESTEK_YYNLENDYRME_FORMU.docx", "🧭", "#f59e0b"),
    ("Yönlendirme", "Sağlık Kuruluşuna Yönlendirme Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095601_SAYLIK_KURULUYUNA_YYNLENDYRME_FORMU.docx", "🏥", "#f59e0b"),
    # ── RAPOR & TAKİP ──
    ("Rapor", "Bireysel Gelişim Raporu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094400_BYREYSEL_GELYYYM_RAPORU.docx", "📈", "#10b981"),
    ("Rapor", "Rehberlik Servisi Randevu Kayıt Çizelgesi", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095534_REHBERLYK_SERViSi_RANDEVU_KAYIT_YYZELGESY.docx", "📅", "#10b981"),
    ("Rapor", "Görüşme Aylık Kayıt Çizelgesi", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094657_GYRYYME_AYLIK_KAYIT_YYZELGESY.xlsx", "📊", "#10b981"),
    ("Rapor", "Görüşme Yıllık Kayıt Çizelgesi", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094719_GYRYYME_YILLIK_KAYIT_YYZELGESY.docx", "📊", "#10b981"),
    ("Rapor", "Özel Eğitim Öğrencisi Rapor Takip Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095508_REHBERLYK_SERViSY_YYYN_YZEL_EYYTYM_YYRENCYSY_RAPOR_TAKYP_FORMU.docx", "📑", "#10b981"),
    # ── GRUP ÇALIŞMA & ÖĞRENCİ TANINMA ──
    ("Grup", "Öğrenci Grup Çalışma Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095135_YYRENCY_GRUP_YALIYMASI_FORMU.docx", "👥", "#8b5cf6"),
    ("Grup", "Sosyometri", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095627_SOSYOMETRY.docx", "🔗", "#8b5cf6"),
    ("Grup", "Yol Haritam", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095848_YOL_HARYTAM.docx", "🗺️", "#8b5cf6"),
    ("Grup", "Yaşam Pencerem", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095820_YAYAM_PENCEREM.docx", "🪟", "#8b5cf6"),
    ("Grup", "Yaşam Pencerem Sınıf Sonuç Çizelgesi", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095723_YAYAM_PENCEREM_SINIF_SONUY_YiZELGESY.xlsx", "📊", "#8b5cf6"),
    ("Grup", "Kime Göre Ben Neyim", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094804_KYME_GYRE_BEN_NEYYM.docx", "🤔", "#8b5cf6"),
    ("Grup", "Kimdir Bu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094738_KYMDYR_BU.docx", "❓", "#8b5cf6"),
    ("Grup", "Bana Kendini Anlat", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094317_BANA_KENDYNY_ANLAT.docx", "🗣️", "#8b5cf6"),
    # ── İHTİYAÇ ANALİZİ & RİSK ──
    ("İhtiyaç", "Rehberlik Hizmetleri İhtiyaç Belirleme Formu", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095434_REHBERLYK_HYZMETLERY_YHTYYAY_BELYRLEME_FORMU_OKUL_PERSONELY_VE_VELY_YYYN.docx", "🎯", "#ef4444"),
    ("İhtiyaç", "Öğrenci Profili Belirleme — Sınıf Risk Haritası", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095246_YYRENCY_PROFYLY_BELYRLEME_PROGRAMI_SINIF_RYSK_HARYTASI.xlsx", "🗺️", "#ef4444"),
    ("İhtiyaç", "Öğrenci Profili Belirleme — Okul Risk Haritası", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095226_YYRENCY_PROFYLY_BELYRLEME_PROGRAMI_OKUL_RYSK_HARYTASI.xlsx", "🏫", "#ef4444"),
    # ── OKUL ÖNCESİ ──
    ("Okul Öncesi", "Okul Öncesi Rehberlik Programı Yıl Sonu Kazanım Kontrol", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24095028_OKUL_YNCESY_REHBERLYK_PROGRAMI_YIL_SONU_KAZANIM_KONTROL_LYSTESY.docx", "🎓", "#ec4899"),
    ("Okul Öncesi", "Okul Öncesi Kazanım Kontrol Sınıf Sonuç Çizelgesi", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094951_OKUL_YNCESY_REHBERLYK_PROGRAMI_KAZANIM_KONTROL_LYSETESY_SINIF_SONUY_YYZELGESY.xlsx", "📊", "#ec4899"),
    ("Okul Öncesi", "Okul Öncesi İhtiyaç Analizi", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094925_OKUL_YNCESY_REHBERLYK_PROGRAMI_YHTYYAY_ANALYZY.docx", "🎯", "#ec4899"),
    ("Okul Öncesi", "Okul Öncesi İhtiyaç Analizi Sınıf Sonuç Çizelgesi", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094856_OKUL_YNCESY_REHBERLYK_PROGRAMI_YHTYYAY_ANALYZY_SINIF_SONUY_YYZELGESY.xlsx", "📊", "#ec4899"),
    ("Okul Öncesi", "Okul Öncesi İhtiyaç Analizi Okul Sonuç Çizelgesi", "/meb_iys_dosyalar/52/01/191203/dosyalar/2017_10/24094831_OKUL_YNCESY_REHBERLYK_PROGRAMI_YHTYYAY_ANALYZY_OKUL_SONUYLARI.docx", "🏫", "#ec4899"),
]

_MEB_KATEGORILER = {
    "Görüşme": ("💬", "#7c3aed", "Öğrenci, veli, öğretmen ve disiplin görüşme formları"),
    "Gözlem": ("👁️", "#3b82f6", "Öğrenci gözlem, özel öğrenme güçlüğü ve DEHB gözlem formları"),
    "Aile": ("👨‍👩‍👧", "#0d9488", "Aile bilgi, ev ziyareti ve çocuk tanıma formları"),
    "Yönlendirme": ("🧭", "#f59e0b", "Eğitsel değerlendirme, psikolojik ve sağlık yönlendirme"),
    "Rapor": ("📈", "#10b981", "Bireysel gelişim raporu, randevu ve görüşme kayıt çizelgeleri"),
    "Grup": ("👥", "#8b5cf6", "Grup çalışma, sosyometri, yaşam pencerem, kimdir bu"),
    "İhtiyaç": ("🎯", "#ef4444", "İhtiyaç belirleme, sınıf ve okul risk haritaları"),
    "Okul Öncesi": ("🎓", "#ec4899", "Okul öncesi kazanım kontrol ve ihtiyaç analizi formları"),
}


def _render_meb_formlari():
    """MEB Rehberlik Hizmetleri Standart Formları — 36 form, kategorili görünüm."""
    styled_header("MEB Standart Formları", "Özel Eğitim ve Rehberlik Hizmetleri Genel Müdürlüğü — 36 Resmi Form", icon="📄")

    st.markdown(
        '<div style="background:linear-gradient(135deg,#0d9488,#14b8a6);color:#fff;'
        'padding:14px 18px;border-radius:12px;margin-bottom:14px;">'
        '<p style="margin:0;font-size:.85rem;opacity:.9;">'
        'MEB resmi rehberlik formları — indirmek için form kartına tıklayın. '
        'Formlar DOCX/XLSX formatında orijinal MEB kaynağından indirilir.</p></div>',
        unsafe_allow_html=True,
    )

    # Kategori istatistikleri
    from collections import Counter
    _kat_sayac = Counter(f[0] for f in _MEB_FORMLAR)
    _kat_cols = st.columns(len(_MEB_KATEGORILER))
    for i, (kat, (ikon, renk, aciklama)) in enumerate(_MEB_KATEGORILER.items()):
        with _kat_cols[i]:
            st.markdown(
                f'<div style="background:{renk}12;border:1px solid {renk}30;border-radius:10px;'
                f'padding:10px;text-align:center;">'
                f'<div style="font-size:1.3rem;">{ikon}</div>'
                f'<div style="font-size:.75rem;font-weight:700;color:{renk};">{kat}</div>'
                f'<div style="font-size:1.1rem;font-weight:800;color:{renk};">{_kat_sayac.get(kat, 0)}</div></div>',
                unsafe_allow_html=True,
            )

    # Filtre
    st.markdown("")
    kat_filtre = st.selectbox("Kategori Filtre:", ["Tümü"] + list(_MEB_KATEGORILER.keys()), key="meb_form_kat")

    if kat_filtre == "Tümü":
        goster = _MEB_FORMLAR
    else:
        goster = [f for f in _MEB_FORMLAR if f[0] == kat_filtre]

    # Formları kategoriye göre grupla
    from itertools import groupby
    for kat, formlar in groupby(goster, key=lambda x: x[0]):
        formlar = list(formlar)
        kat_info = _MEB_KATEGORILER.get(kat, ("📄", "#64748b", ""))
        st.markdown(
            f'<div style="background:{kat_info[1]}10;border-left:4px solid {kat_info[1]};'
            f'border-radius:0 10px 10px 0;padding:10px 14px;margin:12px 0 8px;">'
            f'<span style="font-size:1rem;">{kat_info[0]}</span> '
            f'<span style="font-weight:700;color:{kat_info[1]};font-size:.95rem;">{kat}</span> '
            f'<span style="color:#94a3b8;font-size:.78rem;">— {kat_info[2]}</span></div>',
            unsafe_allow_html=True,
        )

        # 3'lü grid
        rows = [formlar[i:i + 3] for i in range(0, len(formlar), 3)]
        for row in rows:
            cols = st.columns(3)
            for j, form in enumerate(row):
                _kat, _ad, _yol, _ikon, _renk = form
                _url = f"{_MEB_BASE}{_yol}"
                _ext = "XLSX" if _yol.endswith(".xlsx") else "DOCX"
                _ext_clr = "#10b981" if _ext == "XLSX" else "#3b82f6"
                with cols[j]:
                    st.markdown(
                        f'<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:12px;'
                        f'padding:14px;border:1px solid {_renk}25;min-height:100px;">'
                        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
                        f'<span style="font-size:1.2rem;">{_ikon}</span>'
                        f'<span style="background:{_ext_clr}20;color:{_ext_clr};padding:2px 8px;'
                        f'border-radius:6px;font-size:.65rem;font-weight:700;">{_ext}</span></div>'
                        f'<div style="color:#e2e8f0;font-weight:600;font-size:.85rem;line-height:1.3;">{_ad}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    if st.button(f"📥 İndir", key=f"meb_dl_{hash(_yol) & 0x7FFFFFFF}", use_container_width=True):
                        st.markdown(f'<meta http-equiv="refresh" content="0;url={_url}">', unsafe_allow_html=True)
                        st.info(f"İndirme başlatılıyor: {_ad}")


# ============================================================
# SEKME: AİLE BİLGİ FORMU (MEB B.K.G.1.c)
# ============================================================

def _render_aile_bilgi_formu(store: RehberlikDataStore):
    """MEB Aile Bilgi Formu — dijital form doldurma + listeleme + PDF."""
    from models.rehberlik import AileBilgiFormu

    styled_header("Aile Bilgi Formu", "MEB Özel Eğitim ve Rehberlik (B.K.G.1.c)", icon="📋")

    sub1, sub2 = st.tabs(["📋 Form Listesi", "➕ Yeni Form Doldur"])

    # ── Form Listesi ──
    with sub1:
        formlar = store.load_list("aile_bilgi_formlari")
        if not formlar:
            styled_info_banner("Henüz aile bilgi formu doldurulmamış.", "info", "📋")
        else:
            st.markdown(f"**Toplam {len(formlar)} form kayıtlı**")
            for f in sorted(formlar, key=lambda x: x.get("olusturma_zamani", ""), reverse=True):
                with st.expander(f"📋 {f.get('ogrenci_adi_soyadi', '?')} — {f.get('sinif_numarasi', '')} | {f.get('tarih', '')}"):
                    # Özet kartları
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f"**Öğrenci:** {f.get('ogrenci_adi_soyadi', '-')}")
                        st.markdown(f"**Sınıf:** {f.get('sinif_numarasi', '-')}")
                        st.markdown(f"**Veli:** {f.get('veli_adi_soyadi', '-')}")
                    with c2:
                        st.markdown(f"**Anne:** {f.get('anne_adi_soyadi', '-')}")
                        st.markdown(f"**Baba:** {f.get('baba_adi_soyadi', '-')}")
                        st.markdown(f"**Yaşam:** {f.get('kiminle_nerede_yasiyor', '-')}")
                    with c3:
                        st.markdown(f"**Kardeş:** Öz: {f.get('kardes_oz_sayisi', 0)}, Üvey: {f.get('kardes_uvey_sayisi', 0)}")
                        st.markdown(f"**Uygulayıcı:** {f.get('uygulayici', '-')}")
                        st.markdown(f"**Tarih:** {f.get('tarih', '-')}")

                    # Detay bölümleri
                    _sections = [
                        ("🏥 Sağlık", [("Süreğen hastalık", "suregen_hastalik"), ("Sürekli ilaç", "surekli_ilac"),
                                        ("Sürekli cihaz", "surekli_cihaz"), ("Etkisindeki olay", "etkisindeki_olay")]),
                        ("💰 Sosyo-Ekonomik", [("Aile yapısı", "aile_kimlerden_olusiyor"), ("Gelir durumu", "ortalama_gelir"),
                                                ("Ev sahipliği", "ev_sahipligi"), ("Kurum yardımı", "kurum_yardimi"),
                                                ("Bağımlılık", "bagimllik_durumu")]),
                        ("📚 Eğitim", [("Okul öncesi", "okul_oncesi_egitim"), ("Okula tutum", "okula_tutum"),
                                        ("Öğretmenlere tutum", "ogretmenlere_tutum"), ("Çalışma alanı", "ders_calisma_alani"),
                                        ("Ders desteği", "ders_destegi")]),
                        ("👶 Gelişim", [("Doğum öyküsü", "dogum_oykusu"), ("Konuşma", "konusma_baslangic"),
                                        ("Yürüme", "yurume_baslangic"), ("Günlük rutin", "gunluk_rutini")]),
                        ("👨‍👩‍👧 Aile İçi İletişim", [("Vakit geçirme", "vakit_gecirme"), ("Birlikte etkinlikler", "birlikte_etkinlikler"),
                                                        ("Karar alma", "karar_alma"), ("Aile kuralları", "aile_ici_kurallar")]),
                    ]
                    for sec_title, fields in _sections:
                        vals = [f.get(fk, "") for _, fk in fields]
                        if any(vals):
                            st.markdown(f"**{sec_title}:**")
                            for lbl, fk in fields:
                                v = f.get(fk, "")
                                if v:
                                    st.markdown(f"- {lbl}: {v}")

    # ── Yeni Form Doldur ──
    with sub2:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#0d9488,#14b8a6);color:#fff;'
            'padding:14px 18px;border-radius:12px;margin-bottom:14px;">'
            '<h4 style="margin:0;font-size:16px;">📋 MEB Aile Bilgi Formu (B.K.G.1.c)</h4>'
            '<p style="margin:3px 0 0;font-size:12px;opacity:.85;">'
            'Özel Eğitim ve Rehberlik Hizmetleri Genel Müdürlüğü — Öğrenci velisiyle ilk görüşme formu</p></div>',
            unsafe_allow_html=True,
        )

        # Öğrenci seçimi
        try:
            from utils.shared_data import get_student_display_options
            students = get_student_display_options(include_empty=False)
        except Exception:
            students = {}

        sel_stu = st.selectbox("Öğrenci Seçin:", [""] + list(students.keys()), key="abf_stu")
        stu_data = students.get(sel_stu, {}) if sel_stu else {}

        st.markdown("---")
        st.markdown("### 1. Öğrenci & Veli Bilgileri")
        _c1, _c2 = st.columns(2)
        with _c1:
            ogrenci_adi = st.text_input("Öğrencinin Adı Soyadı:", value=sel_stu.split("(")[0].strip() if sel_stu else "", key="abf_ogr_ad")
            okul = st.text_input("Okul:", key="abf_okul")
            sinif_no = st.text_input("Sınıfı/Numarası:", value=f"{stu_data.get('sinif','')}/{stu_data.get('sube','')}" if stu_data else "", key="abf_sinif")
            sinif_rehber = st.text_input("Sınıf/Şube Rehber Öğretmen:", key="abf_rehber")
        with _c2:
            veli_ad = st.text_input("Veli Adı Soyadı:", key="abf_veli_ad")
            yakinlik = st.selectbox("Öğrenciye Yakınlık:", ["Anne", "Baba", "Vasi", "Diğer"], key="abf_yakinlik")
            veli_egitim = st.text_input("Veli Eğitim/Meslek:", key="abf_veli_egitim")
            veli_tel = st.text_input("Veli Tel/E-posta:", key="abf_veli_tel")

        st.markdown("### 2. Anne - Baba - Bakım Veren")
        _p1, _p2, _p3 = st.columns(3)
        with _p1:
            st.markdown("**Anne**")
            anne_ad = st.text_input("Anne Adı Soyadı:", key="abf_anne_ad")
            anne_dogum = st.text_input("Doğum Yeri/Yılı:", key="abf_anne_dogum")
            anne_sag = st.selectbox("Sağ/Ölü:", ["Sağ", "Ölü"], key="abf_anne_sag")
            anne_evlilik = st.selectbox("Durum:", ["Birlikte", "Boşanmış", "Ayrı"], key="abf_anne_evlilik")
            anne_yeniden = st.text_input("Yeniden evlenme:", key="abf_anne_yeniden")
            anne_egitim = st.text_input("Eğitim/Meslek:", key="abf_anne_egitim")
            anne_tel = st.text_input("Tel/E-posta:", key="abf_anne_tel")
        with _p2:
            st.markdown("**Baba**")
            baba_ad = st.text_input("Baba Adı Soyadı:", key="abf_baba_ad")
            baba_dogum = st.text_input("Doğum Yeri/Yılı:", key="abf_baba_dogum")
            baba_sag = st.selectbox("Sağ/Ölü:", ["Sağ", "Ölü"], key="abf_baba_sag")
            baba_evlilik = st.selectbox("Durum:", ["Birlikte", "Boşanmış", "Ayrı"], key="abf_baba_evlilik")
            baba_yeniden = st.text_input("Yeniden evlenme:", key="abf_baba_yeniden")
            baba_egitim = st.text_input("Eğitim/Meslek:", key="abf_baba_egitim")
            baba_tel = st.text_input("Tel/E-posta:", key="abf_baba_tel")
        with _p3:
            st.markdown("**Bakım Veren Diğer Kişi**")
            bakim_ad = st.text_input("Adı Soyadı:", key="abf_bakim_ad")
            bakim_bilgi = st.text_area("Bilgi:", key="abf_bakim_bilgi", height=100)

        kiminle = st.selectbox("Öğrenci Kiminle/Nerede Yaşıyor?",
                               ["Aile", "Koruyucu Aile", "Akraba", "Barınma Tedbir Kararı", "Pansiyonlu Okul", "Diğer"],
                               key="abf_kiminle")

        st.markdown("### 3. Kardeş Bilgisi")
        _k1, _k2 = st.columns(2)
        with _k1:
            kardes_oz = st.number_input("Öz Kardeş Sayısı:", 0, 20, 0, key="abf_oz")
        with _k2:
            kardes_uvey = st.number_input("Üvey Kardeş Sayısı:", 0, 20, 0, key="abf_uvey")

        st.markdown("### 4. Sağlık Bilgileri")
        suregen = st.text_input("Süreğen hastalık:", key="abf_suregen")
        ilac = st.text_input("Sürekli kullanılan ilaç:", key="abf_ilac")
        cihaz = st.text_input("Sürekli kullanılan cihaz:", key="abf_cihaz")
        olay = st.text_input("Etkisi altındaki olay:", key="abf_olay")

        st.markdown("### 5. Sosyo-Ekonomik Durum")
        aile_yapi = st.text_input("Aileniz kimlerden oluşuyor?", key="abf_aile_yapi")
        ekonomi = st.text_input("Ekonomiye katkı sağlayanlar:", key="abf_ekonomi")
        gelir = st.text_input("Ortalama gelir durumu:", key="abf_gelir")
        ev = st.selectbox("Oturduğunuz ev kendinizin mi?", ["Evet", "Hayır (Kira)", "Diğer"], key="abf_ev")
        kurum_yardim = st.text_input("Kurum/kuruluş yardımı:", key="abf_yardim")
        suc = st.text_input("Suça karışmış birey:", key="abf_suc")
        yetersizlik = st.text_input("Yetersizlik/süreğen hastalık (yakınlık + engel):", key="abf_yetersizlik")
        bagimlilik = st.text_input("Sigara/alkol/madde/teknoloji bağımlılığı:", key="abf_bagimlilik")
        sosyo_diger = st.text_input("Sosyo-ekonomik diğer:", key="abf_sosyo_diger")

        st.markdown("### 6. Öğrencinin Eğitimi")
        okul_oncesi = st.text_input("Okul öncesi eğitim aldı mı?", key="abf_oo")
        okuma_yazma = st.text_input("Okuma yazmayı ne zaman öğrendi?", key="abf_oy")
        okula_tutum = st.text_input("Okula karşı tutumu:", key="abf_okul_tutum")
        ogretmen_tutum = st.text_input("Öğretmenlerine karşı tutumu:", key="abf_ogr_tutum")
        calisma_alani = st.selectbox("Evde ders çalışma alanı var mı?", ["Evet", "Hayır"], key="abf_alan")
        bagimsiz = st.text_input("Bağımsız çalışma alışkanlığı:", key="abf_bagimsiz")
        ders_kontrol = st.text_input("Ders kontrolü kim yapıyor?", key="abf_kontrol")
        ders_destek = st.text_input("Ders desteği (nereden)?", key="abf_destek")
        ulasim = st.text_input("Okula ulaşım:", key="abf_ulasim")

        st.markdown("### 7. Öğrencinin Gelişimi")
        dogum = st.text_input("Doğum öyküsü (şekli, erken/zamanında):", key="abf_dogum")
        konusma = st.text_input("Ne zaman konuşmaya başladı?", key="abf_konusma")
        yurume = st.text_input("Ne zaman yürümeye başladı?", key="abf_yurume")
        tuvalet = st.text_input("Tuvalet alışkanlığı ne zaman kazanıldı?", key="abf_tuvalet")
        dis_iletisim = st.text_input("Aile dışı kişilerle iletişimi:", key="abf_dis_iletisim")
        gunluk = st.text_area("Bir gününü nasıl geçirir?", key="abf_gunluk", height=80)

        st.markdown("### 8. Aile İçi İletişim")
        vakit = st.text_input("Çocuğunuz vaktini nasıl geçirmekten hoşlanır?", key="abf_vakit")
        etkinlik = st.text_input("Birlikte yapılan etkinlikler:", key="abf_etkinlik")
        karar = st.text_input("Ailede kararlar nasıl alınır?", key="abf_karar")
        kurallar = st.text_input("Aile içi kurallar:", key="abf_kurallar")
        hoslanilan = st.text_area("Hoşlanılan davranışlar:", key="abf_hoslanilan", height=60)
        hoslanilmayan = st.text_area("Hoşlanılmayan davranışlar:", key="abf_hoslanilmayan", height=60)

        st.markdown("### 9. Diğer & Uygulayıcı")
        diger = st.text_area("Diğer açıklamalar:", key="abf_diger", height=80)
        _u1, _u2 = st.columns(2)
        with _u1:
            uygulayici = st.text_input("Uygulayıcı Ad-Soyad:", key="abf_uygulayici")
        with _u2:
            tarih = st.date_input("Tarih:", key="abf_tarih")

        st.markdown("---")
        if st.button("💾 Formu Kaydet", key="abf_save", type="primary", use_container_width=True):
            if not ogrenci_adi:
                st.error("Öğrenci adı zorunludur.")
                return

            form = AileBilgiFormu(
                ogrenci_id=stu_data.get("id", ""),
                ogrenci_adi_soyadi=ogrenci_adi, okul=okul, sinif_numarasi=sinif_no,
                sinif_sube_rehber=sinif_rehber,
                veli_adi_soyadi=veli_ad, ogrenciye_yakinlik=yakinlik,
                veli_egitim_meslek=veli_egitim, veli_tel=veli_tel,
                anne_adi_soyadi=anne_ad, anne_dogum_yeri_yili=anne_dogum,
                anne_sag_olu=anne_sag, anne_birlikte_bosanmis=anne_evlilik,
                anne_yeniden_evlenme=anne_yeniden, anne_egitim_meslek=anne_egitim, anne_tel_eposta=anne_tel,
                baba_adi_soyadi=baba_ad, baba_dogum_yeri_yili=baba_dogum,
                baba_sag_olu=baba_sag, baba_birlikte_bosanmis=baba_evlilik,
                baba_yeniden_evlenme=baba_yeniden, baba_egitim_meslek=baba_egitim, baba_tel_eposta=baba_tel,
                bakim_veren_adi=bakim_ad, bakim_veren_bilgi=bakim_bilgi,
                kiminle_nerede_yasiyor=kiminle,
                kardes_oz_sayisi=kardes_oz, kardes_uvey_sayisi=kardes_uvey,
                suregen_hastalik=suregen, surekli_ilac=ilac, surekli_cihaz=cihaz, etkisindeki_olay=olay,
                aile_kimlerden_olusiyor=aile_yapi, ekonomiye_katki_saglayan=ekonomi,
                ortalama_gelir=gelir, ev_sahipligi=ev, kurum_yardimi=kurum_yardim,
                suca_karismis_birey=suc, yetersizlik_suregen_hastalik=yetersizlik,
                bagimllik_durumu=bagimlilik, sosyo_diger=sosyo_diger,
                okul_oncesi_egitim=okul_oncesi, okuma_yazma_zamani=okuma_yazma,
                okula_tutum=okula_tutum, ogretmenlere_tutum=ogretmen_tutum,
                ders_calisma_alani=calisma_alani, bagimsiz_calisma_aliskanligi=bagimsiz,
                ders_kontrol_eden=ders_kontrol, ders_destegi=ders_destek, okula_ulasim=ulasim,
                dogum_oykusu=dogum, konusma_baslangic=konusma, yurume_baslangic=yurume,
                tuvalet_aliskanligi=tuvalet, aile_disi_iletisim=dis_iletisim, gunluk_rutini=gunluk,
                vakit_gecirme=vakit, birlikte_etkinlikler=etkinlik, karar_alma=karar,
                aile_ici_kurallar=kurallar, hoslanilar_davranislar=hoslanilan,
                hoslanilmayan_davranislar=hoslanilmayan,
                diger_aciklamalar=diger, uygulayici=uygulayici,
                tarih=tarih.isoformat() if tarih else "",
            )
            store.upsert("aile_bilgi_formlari", form)
            st.success(f"✅ Aile Bilgi Formu kaydedildi: {ogrenci_adi}")
            st.rerun()


def _render_rehberlik_bultenleri():
    """Rehberlik Bültenleri sekmesi — Premium Edition."""
    from utils.shared_data import load_kurum_profili

    kp = load_kurum_profili()
    kurum_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")

    styled_section("Rehberlik Bültenleri Arşivi", "#7c3aed")
    st.caption(f"{kurum_adi} — Anaokulu, İlkokul, Ortaokul ve Lise rehberlik bültenleri — Premium Edition")

    # ── Filtreler ──
    yillar = sorted({b[1] for b in _BULTEN_ARSIV}, reverse=True)
    aylar_mevcut = sorted({b[2] for b in _BULTEN_ARSIV}, reverse=True)

    fc1, fc2, fc3 = st.columns([1, 1, 2])
    with fc1:
        sec_yil = st.selectbox("Yıl", ["Tümü"] + [str(y) for y in yillar], key="rbl_yil")
    with fc2:
        ay_opts = ["Tümü"] + [_AYLAR_TR[a] for a in aylar_mevcut]
        sec_ay = st.selectbox("Ay", ay_opts, key="rbl_ay")
    with fc3:
        sec_kat = st.radio("Kademe", _BULTEN_KATEGORILER, horizontal=True, key="rbl_kat")

    # ── Filtreleme ──
    filtered = list(_BULTEN_ARSIV)
    if sec_yil != "Tümü":
        filtered = [b for b in filtered if b[1] == int(sec_yil)]
    if sec_ay != "Tümü":
        ay_num = next(k for k, v in _AYLAR_TR.items() if v == sec_ay)
        filtered = [b for b in filtered if b[2] == ay_num]
    if sec_kat != "Tümü":
        filtered = [b for b in filtered if b[0] == sec_kat]

    st.markdown(f"**{len(filtered)}** bülten listeleniyor")

    if not filtered:
        st.info("Seçilen filtrelere uygun bülten bulunamadı.")
        return

    # ── Aktif bülten gösterimi ──
    active_key = "_rhb_active_bulten"
    ab = st.session_state.get(active_key)
    if ab and (not isinstance(ab, dict) or "kademe" not in ab):
        st.session_state[active_key] = None
        ab = None

    if ab:
        bc1, bc2 = st.columns([1, 1])
        with bc1:
            if st.button("← Bülten Listesine Dön", key="rbl_back"):
                st.session_state[active_key] = None
                st.rerun()
        with bc2:
            try:
                pdf_bytes = _generate_bulten_pdf(ab["kademe"], ab["ay"], ab["yil"], kurum_adi)
                if pdf_bytes and len(pdf_bytes) > 100:
                    ay_adi = _AYLAR_TR.get(ab["ay"], "")
                    fname = f"Bulten_{ab['kademe']}_{ay_adi}_{ab['yil']}.pdf"
                    st.download_button(
                        "📄 Kurumsal PDF İndir",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        key=f"rbl_pdf_dl_{ab['kademe']}_{ab['ay']}",
                        use_container_width=True,
                    )
                else:
                    st.warning("PDF oluşturulamadı")
            except Exception as e:
                st.error(f"PDF hatası: {str(e)[:100]}")
        html = _build_bulten_html(ab["kademe"], ab["ay"], ab["yil"], kurum_adi)
        st.components.v1.html(html, height=680, scrolling=False)
        return

    # ── Kart Grid ──
    cols_per_row = 4
    for i in range(0, len(filtered), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(filtered):
                break
            kademe, yil, ay = filtered[idx]
            renk1, renk2, icon = _BULTEN_RENK.get(kademe, ("#6b7280", "#4b5563", "📄"))
            ay_adi = _AYLAR_TR.get(ay, "")
            tema_baslik, tema_ikon = _BULTEN_TEMALAR.get(ay, ("", "📰"))
            with col:
                st.markdown(f'''<div style="background:linear-gradient(135deg,{renk1},{renk2});
                    border-radius:14px;padding:18px 14px;text-align:center;margin-bottom:8px;
                    min-height:160px;display:flex;flex-direction:column;justify-content:center;
                    border:1px solid rgba(255,255,255,.15);box-shadow:0 4px 15px rgba(0,0,0,.2)">
                    <div style="font-size:28px;margin-bottom:4px">{tema_ikon}</div>
                    <div style="font-size:12px;font-weight:700;color:#fff;opacity:.9">{kademe}</div>
                    <div style="font-size:20px;font-weight:800;color:#fff;margin:4px 0">{ay_adi}</div>
                    <div style="font-size:11px;color:rgba(255,255,255,.7)">{yil}</div>
                    <div style="font-size:9px;color:rgba(255,255,255,.4);margin-top:4px;font-style:italic">{tema_baslik}</div>
                </div>''', unsafe_allow_html=True)
                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button("📖 Oku", key=f"rbl_{idx}", use_container_width=True):
                        st.session_state[active_key] = {"kademe": kademe, "ay": ay, "yil": yil}
                        st.rerun()
                with bc2:
                    try:
                        _pdf = _generate_bulten_pdf(kademe, ay, yil, kurum_adi)
                        if _pdf and len(_pdf) > 100:
                            st.download_button("📄 PDF", data=_pdf,
                                               file_name=f"Bulten_{kademe}_{ay_adi}_{yil}.pdf",
                                               mime="application/pdf",
                                               key=f"rbl_dpdf_{idx}", use_container_width=True)
                    except Exception:
                        pass




# ============================================================
# ANA RENDER FONKSIYONU
# ============================================================

def render_rehberlik():
    """Ana giris noktasi - app.py'den cagrilir."""
    _inject_rhb_css()
    styled_header(
        "Rehberlik ve Psikolojik Danismanlik",
        "Öğrenci gorusme, vaka takip, aile gorusme, yonlendirme, BEP, test, plan ve risk degerlendirme",
        "\U0001F9E0",
    )

    store = _get_rhb_store()

    render_smarti_welcome("rehberlik")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("rehberlik_egitim_yili")

    # Veri dogrulama
    try:
        from utils.ui_common import veri_dogrulama_butonu, veri_dogrulama_sonucu
        veri_dogrulama_butonu("rehberlik")
        if st.session_state.get("_veri_kontrol_aktif_rehberlik"):
            sorunlar = []
            _gorusmeler = store.load_objects("gorusmeler")
            _vakalar = store.load_objects("vakalar")
            if len(_gorusmeler) == 0:
                sorunlar.append({"tip": "eksik", "alan": "Gorusme Kaydi", "sayi": 0, "oncelik": "orta"})
            if len(_vakalar) == 0:
                sorunlar.append({"tip": "eksik", "alan": "Vaka Kaydi", "sayi": 0, "oncelik": "orta"})
            veri_dogrulama_sonucu(sorunlar)
            st.session_state["_veri_kontrol_aktif_rehberlik"] = False
    except Exception:
        pass

    # Rehberlik sekme CSS — ekrana sığdır
    st.markdown("""<style>
    div[data-testid="stTabs"] [role="tablist"] button {
        padding: 6px 10px !important;
        font-size: 13px !important;
        min-width: 0 !important;
        white-space: nowrap !important;
    }
    div[data-testid="stTabs"] [role="tablist"] {
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        gap: 2px !important;
    }
    </style>""", unsafe_allow_html=True)

    # -- Tab Gruplama (32 tab -> 5 grup) --
    _GRP_21250 = {
        "📋 Grup A": [("📊Dashboard", 0), ("💬Görüşme", 1), ("📁Vaka", 2), ("👨‍👩‍👧Aile", 3), ("🔀Yönlendirme", 4), ("📄MEB Form", 5), ("🧪Test", 6)],
        "📊 Grup B": [("🧩Test Havuzu", 7), ("📝Test Oluştur", 8), ("📋Kayıt Testleri", 9), ("📊Sonuç Analizi", 10), ("🎓BEP", 11), ("📅Plan", 12), ("⚠️Risk", 13)],
        "🔧 Grup C": [("📰Bülten", 14), ("📈Rapor", 15), ("🧠Sosyo-Duygusal", 16), ("🤝Arabuluculuk", 17), ("🎯Kariyer", 18), ("🚨Kriz Müdahale", 19), ("📁Gelişim Dosyası", 20)],
        "📈 Grup D": [("👨‍👩‍👧Veli Eğitim", 21), ("🤖AI Risk Motor", 22), ("🧘Terapi Odası", 23), ("👥Grup Çalışması", 24), ("🌡️Okul İklimi", 25), ("🧬Psiko DNA", 26), ("🎮Gamifiye", 27)],
        "🎯 Grup E": [("📡İşbirliği", 28), ("📊Performans", 29), ("🔮Etkinlik", 30), ("🤖Smarti", 31)],
    }
    _sg_21250 = st.radio("", list(_GRP_21250.keys()), horizontal=True, label_visibility="collapsed", key="rg_21250")
    _gt_21250 = _GRP_21250[_sg_21250]
    _aktif_idx_21250 = set(t[1] for t in _gt_21250)
    _tab_names_21250 = [t[0] for t in _gt_21250]
    tabs = st.tabs(_tab_names_21250)
    _tab_real_21250 = {idx: t for idx, t in zip((t[1] for t in _gt_21250), tabs)}

    if 0 in _aktif_idx_21250:
      with _tab_real_21250[0]:
        _render_dashboard(store)
    if 1 in _aktif_idx_21250:
      with _tab_real_21250[1]:
        _render_gorusme_kayitlari(store)
    if 2 in _aktif_idx_21250:
      with _tab_real_21250[2]:
        _render_vaka_takip(store)
    if 3 in _aktif_idx_21250:
      with _tab_real_21250[3]:
        _render_aile_gorusmeleri(store)
    if 4 in _aktif_idx_21250:
      with _tab_real_21250[4]:
        _render_yonlendirme(store)
    if 5 in _aktif_idx_21250:
      with _tab_real_21250[5]:
        from views.meb_formlar import render_meb_dijital_formlar
        render_meb_dijital_formlar(store)
        with st.expander("📑 MEB Resmi Formları (36 form)", expanded=False):
            _render_meb_formlari()
    if 6 in _aktif_idx_21250:
      with _tab_real_21250[6]:
        _render_test_envanter(store)
        with st.expander("📋 Test Listesi", expanded=False):
            _render_test_listesi(store)
    if 7 in _aktif_idx_21250:
      with _tab_real_21250[7]:
        _render_test_havuzu(store)
    if 8 in _aktif_idx_21250:
      with _tab_real_21250[8]:
        _render_yeni_test(store)
        with st.expander("✏️ Soru Oluştur", expanded=False):
            _render_soru_olustur(store)
    if 9 in _aktif_idx_21250:
      with _tab_real_21250[9]:
        _render_kayit_testleri()
    if 10 in _aktif_idx_21250:
      with _tab_real_21250[10]:
        _render_sonuc_analizi(store)
    if 11 in _aktif_idx_21250:
      with _tab_real_21250[11]:
        _render_bep(store)
    if 12 in _aktif_idx_21250:
      with _tab_real_21250[12]:
        _render_rehberlik_plani(store)
    if 13 in _aktif_idx_21250:
      with _tab_real_21250[13]:
        _render_risk_degerlendirme(store)
    if 14 in _aktif_idx_21250:
      with _tab_real_21250[14]:
        _render_rehberlik_bultenleri()
    if 15 in _aktif_idx_21250:
      with _tab_real_21250[15]:
        _render_raporlar(store)

    # ── YENİ: Sosyo-Duygusal Takip ──
    if 16 in _aktif_idx_21250:
      with _tab_real_21250[16]:
        sd_tabs = st.tabs(["🧠 Sosyo-Duygusal Takip", "😊 Günlük Duygu Check-in"])
        with sd_tabs[0]:
            try:
                from views._rhb_yeni_ozellikler import render_sosyo_duygusal_takip
                render_sosyo_duygusal_takip()
            except Exception as _e:
                st.error(f"Sosyo-Duygusal Takip yuklenemedi: {_e}")
        with sd_tabs[1]:
            try:
                from views._mood_checkin import render_mood_rehber_panel
                render_mood_rehber_panel()
            except Exception as _e:
                st.error(f"Duygu Check-in paneli yüklenemedi: {_e}")

    # ── YENİ: Akran Arabuluculuk ──
    if 17 in _aktif_idx_21250:
      with _tab_real_21250[17]:
        try:
            from views._rhb_yeni_ozellikler import render_akran_arabuluculuk
            render_akran_arabuluculuk()
        except Exception as _e:
            st.error(f"Akran Arabuluculuk yuklenemedi: {_e}")

    # ── YENİ: Kariyer Rehberliği ──
    if 18 in _aktif_idx_21250:
      with _tab_real_21250[18]:
        try:
            from views._rhb_yeni_ozellikler import render_kariyer_rehberligi
            render_kariyer_rehberligi()
        except Exception as _e:
            st.error(f"Kariyer Rehberligi yuklenemedi: {_e}")

    # ── YENİ: Kriz Müdahale Protokolü ──
    if 19 in _aktif_idx_21250:
      with _tab_real_21250[19]:
        # Anonim İhbar kritik uyarı — kriz müdahale'nin en üstünde
        try:
            from views._ihbar_hatti import render_ihbar_uyari_badge, render_ihbar_inceleme_panel
            render_ihbar_uyari_badge()
        except Exception:
            pass

        kriz_tabs = st.tabs(["🚨 Kriz Müdahale", "🤫 Anonim İhbar İnceleme"])
        with kriz_tabs[0]:
            try:
                from views._rhb_yeni_ozellikler import render_kriz_mudahale
                render_kriz_mudahale()
            except Exception as _e:
                st.error(f"Kriz Mudahale yuklenemedi: {_e}")
        with kriz_tabs[1]:
            try:
                render_ihbar_inceleme_panel()
            except Exception as _e:
                st.error(f"İhbar hattı yüklenemedi: {_e}")

    # ── YENİ: Öğrenci Gelişim Dosyası ──
    if 20 in _aktif_idx_21250:
      with _tab_real_21250[20]:
        try:
            from views._rhb_yeni_ozellikler import render_ogrenci_gelisim_dosyasi
            render_ogrenci_gelisim_dosyasi()
        except Exception as _e:
            st.error(f"Gelisim Dosyasi yuklenemedi: {_e}")

    # ── YENİ: Veli Psiko-eğitim ──
    if 21 in _aktif_idx_21250:
      with _tab_real_21250[21]:
        try:
            from views._rhb_yeni_ozellikler import render_veli_psiko_egitim
            render_veli_psiko_egitim()
        except Exception as _e:
            st.error(f"Veli Psiko-egitim yuklenemedi: {_e}")

    # ── MEGA: AI Risk Tahmin Motoru ──
    if 22 in _aktif_idx_21250:
      with _tab_real_21250[22]:
        try:
            from views._rhb_yeni_ozellikler import render_ai_risk_tahmin
            render_ai_risk_tahmin()
        except Exception as _e:
            st.error(f"AI Risk Motor yuklenemedi: {_e}")

    # ── MEGA: Dijital Terapi Odası ──
    if 23 in _aktif_idx_21250:
      with _tab_real_21250[23]:
        try:
            from views._rhb_yeni_ozellikler import render_dijital_terapi_odasi
            render_dijital_terapi_odasi()
        except Exception as _e:
            st.error(f"Dijital Terapi Odasi yuklenemedi: {_e}")

    # ── MEGA: Grup Çalışması Planlayıcı ──
    if 24 in _aktif_idx_21250:
      with _tab_real_21250[24]:
        try:
            from views._rhb_yeni_ozellikler import render_grup_calismasi
            render_grup_calismasi()
        except Exception as _e:
            st.error(f"Grup Calismasi yuklenemedi: {_e}")

    # ── ULTRA MEGA: Okul İklimi Barometresi ──
    if 25 in _aktif_idx_21250:
      with _tab_real_21250[25]:
        try:
            from views._rhb_ultra_mega import render_okul_iklimi_barometresi
            render_okul_iklimi_barometresi()
        except Exception as _e:
            st.error(f"Okul Iklimi yuklenemedi: {_e}")

    # ── ULTRA MEGA: AI Psikolojik Profil ──
    if 26 in _aktif_idx_21250:
      with _tab_real_21250[26]:
        try:
            from views._rhb_ultra_mega import render_ai_psikolojik_profil
            render_ai_psikolojik_profil()
        except Exception as _e:
            st.error(f"Psiko DNA yuklenemedi: {_e}")

    # ── ULTRA MEGA: Gamifiye Gelişim ──
    if 27 in _aktif_idx_21250:
      with _tab_real_21250[27]:
        try:
            from views._rhb_ultra_mega import render_gamifiye_gelisim
            render_gamifiye_gelisim()
        except Exception as _e:
            st.error(f"Gamifiye yuklenemedi: {_e}")

    # ── FINAL: Çok Paydaşlı İşbirliği ──
    if 28 in _aktif_idx_21250:
      with _tab_real_21250[28]:
        try:
            from views._rhb_ultra_mega import render_isbirligi_paneli
            render_isbirligi_paneli()
        except Exception as _e:
            st.error(f"Isbirligi Paneli yuklenemedi: {_e}")

    # ── FINAL: Performans Karnesi ──
    if 29 in _aktif_idx_21250:
      with _tab_real_21250[29]:
        try:
            from views._rhb_ultra_mega import render_performans_karnesi
            render_performans_karnesi()
        except Exception as _e:
            st.error(f"Performans Karnesi yuklenemedi: {_e}")

    # ─�� FINAL: Etkinlik Analizi ──
    if 30 in _aktif_idx_21250:
      with _tab_real_21250[30]:
        try:
            from views._rhb_ultra_mega import render_etkinlik_analizi
            render_etkinlik_analizi()
        except Exception as _e:
            st.error(f"Etkinlik Analizi yuklenemedi: {_e}")

    if 31 in _aktif_idx_21250:
      with _tab_real_21250[31]:
        def _rhb_smarti_context():
            try:
                g = len(store.load_objects("gorusmeler"))
                v = len(store.load_objects("vakalar"))
                b = len(store.load_objects("bep_kayitlari"))
                r = len(store.load_objects("risk_degerlendirmeleri"))
                t = len(store.load_objects("testler"))
                return f"Toplam gorusme: {g}, Toplam vaka: {v}, BEP kaydi: {b}, Risk degerlendirme: {r}, Test sayisi: {t}"
            except Exception:
                return ""
        render_smarti_chat("rehberlik", data_context_fn=_rhb_smarti_context)
