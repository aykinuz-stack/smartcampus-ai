"""
KTP-01 Kutuphane Modulu - Streamlit UI
=======================================
Dashboard, kayitli materyaller, yeni kayit, odunc islemleri,
odunc takip, analiz, raporlar, ayarlar, Smarti.
"""

from __future__ import annotations

import os
from datetime import datetime, date, timedelta
from typing import Any

import streamlit as st
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("dijital_kutuphane")
except Exception:
    pass
from utils.ui_kit import confirm_action
import pandas as pd

from utils.tenant import get_tenant_dir
from models.kutuphane import (
    Materyal, OduncIslem, KutuphaneAyar, KutuphaneLog,
    KutuphaneDataStore, OduncAnalizcisi, KutuphaneRaporlayici, KutuphaneDashboard,
    MATERYAL_TURLERI, MATERYAL_KATEGORILERI, MATERYAL_DILLERI,
    MATERYAL_DURUMLARI, ODUNC_DURUMLARI, ODUNC_ALAN_TIPLERI,
    _now, _today,
)
from utils.auth import AuthManager
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG


# ============================================================
# RENK PALETI (Excel referans stili)
# ============================================================

_CLR_BLUE = "#4472C4"
_CLR_ORANGE = "#ED7D31"
_CLR_GOLD = "#FFC000"
_CLR_GRAY = "#A5A5A5"
_CLR_GREEN = "#70AD47"
_CLR_DARK = "#0B0F19"
_CLR_TEAL = "#2563eb"


# ============================================================
# YARDIMCI FONKSIYONLAR
# ============================================================

def _get_ktp_store() -> KutuphaneDataStore:
    base = os.path.join(get_tenant_dir(), "kutuphane")
    store = KutuphaneDataStore(base)
    store.auto_populate_defaults()
    return store


def _durum_badge(durum: str) -> str:
    renk_map = {
        "Aktif": _CLR_GREEN, "Pasif": _CLR_GRAY, "Kayip": "#ef4444", "Hurda": "#94a3b8",
        "Ödünç": _CLR_BLUE, "İade Edildi": _CLR_GREEN, "Gecikti": "#ef4444",
    }
    renk = renk_map.get(durum, _CLR_GRAY)
    return (f'<span style="background:{renk};color:#fff;padding:3px 10px;'
            f'border-radius:10px;font-size:11px;font-weight:600;">{durum}</span>')


# ============================================================
# CSS ENJEKSIYONU
# ============================================================

def _inject_ktp_css():
    inject_common_css("ktp")
    st.markdown("""<style>
    :root {
        --ktp-primary: #4472C4;
        --ktp-secondary: #ED7D31;
        --ktp-gold: #FFC000;
        --ktp-green: #70AD47;
        --ktp-dark: #0B0F19;
    }
    .stApp > header { background: transparent !important; }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #4472C4;
    }
    </style>""", unsafe_allow_html=True)


def _html_table(headers: list[str], rows_html: str, color: str = _CLR_BLUE) -> str:
    hdr = "".join(f'<th style="padding:8px 10px;color:#fff;text-align:left;">{h}</th>' for h in headers)
    return f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;
    border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;">
    <thead><tr style="background:linear-gradient(135deg,{_CLR_DARK},{color});">
    {hdr}</tr></thead><tbody>{rows_html}</tbody></table></div>"""


# ============================================================
# SEKME 1: DASHBOARD
# ============================================================

def _render_dashboard(store: KutuphaneDataStore):
    styled_header("Kutuphane Dashboard", "Envanter, odunc durumu ve trendler", icon="📚")

    # Gecikmeleri guncelle
    store.gecikme_guncelle()

    dash = KutuphaneDashboard(store)
    kpi = dash.kpi_hesapla()

    styled_stat_row([
        ("Toplam Materyal", str(kpi["toplam_adet"]), "info", "📚"),
        ("Mevcut", str(kpi["mevcut_adet"]), "success", "✅"),
        ("Ödünç", str(kpi["odunc_adet"]), _CLR_ORANGE, "🔄"),
        ("Geciken", str(kpi["geciken"]), "#ef4444" if kpi["geciken"] > 0 else _CLR_GRAY, "⏰"),
    ])

    styled_stat_row([
        ("Bugün Ödünç", str(kpi["bugun_odunc"]), "info", "📖"),
        ("Bugün İade", str(kpi["bugun_iade"]), _CLR_GREEN, "📥"),
        ("Toplam İşlem", str(kpi["toplam_odunc_islem"]), _CLR_GOLD, "📊"),
        ("Materyal Cesit", str(kpi["toplam_materyal"]), _CLR_TEAL, "📋"),
    ])

    try:
        import plotly.graph_objects as go

        col1, col2 = st.columns(2)

        with col1:
            styled_section("Tur Dagilimi", _CLR_BLUE)
            if kpi["tur_dagilimi"]:
                labels = list(kpi["tur_dagilimi"].keys())
                values = list(kpi["tur_dagilimi"].values())
                fig = go.Figure(go.Pie(
                    labels=labels, values=values, hole=0.55,
                    marker=dict(colors=SC_COLORS[:len(labels)], line=dict(color="#fff", width=2)),
                    textinfo="label+percent",
                ))
                sc_pie(fig, height=300)
                st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            else:
                st.info("Henuz materyal yok.")

        with col2:
            styled_section("Kategori Dagilimi", _CLR_ORANGE)
            if kpi["kategori_dagilimi"]:
                labels = list(kpi["kategori_dagilimi"].keys())[:10]
                values = [kpi["kategori_dagilimi"][k] for k in labels]
                fig = go.Figure(go.Bar(
                    y=labels, x=values, orientation="h",
                    marker_color=SC_COLORS[0],
                    text=[str(v) for v in values], textposition="auto",
                ))
                sc_bar(fig, height=300, horizontal=True)
                fig.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            else:
                st.info("Henuz materyal yok.")

        # Aylik trend
        styled_section("Aylık Ödünç/İade Trendi")
        analizcisi = OduncAnalizcisi(store)
        trend = analizcisi.aylik_odunc_trendi(12)
        if any(t["odunc"] > 0 or t["iade"] > 0 for t in trend):
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Ödünç", x=[t["ay"] for t in trend],
                                 y=[t["odunc"] for t in trend], marker_color=SC_COLORS[0],
                                 text=[str(t["odunc"]) for t in trend]))
            fig.add_trace(go.Bar(name="İade", x=[t["ay"] for t in trend],
                                 y=[t["iade"] for t in trend], marker_color=SC_COLORS[1],
                                 text=[str(t["iade"]) for t in trend]))
            sc_bar(fig, height=280)
            fig.update_layout(barmode="group", legend=dict(orientation="h", y=1.08))
            st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
        else:
            styled_info_banner("Henuz trend verisi yok.", "info", "📊")

    except ImportError:
        st.warning("Plotly yuklu degil.")

    # Geciken materyaller
    if kpi["geciken_liste"]:
        styled_section("Geciken Materyaller", "#ef4444")
        rows = ""
        for isl in kpi["geciken_liste"]:
            rows += f"""<tr>
                <td style="padding:6px 10px;">{isl.materyal_adi}</td>
                <td style="padding:6px 10px;">{isl.odunc_alan_adi}</td>
                <td style="padding:6px 10px;">{isl.iade_tarihi}</td>
                <td style="padding:6px 10px;color:#ef4444;font-weight:600;">{isl.gecikme_gun} gun</td>
            </tr>"""
        st.markdown(_html_table(["Materyal", "Ödünç Alan", "İade Tarihi", "Gecikme"], rows, "#ef4444"),
                    unsafe_allow_html=True)


# ============================================================
# SEKME 2: KAYITLI MATERYALLER
# ============================================================

def _render_kayitli_materyaller(store: KutuphaneDataStore):
    styled_header("Kayıtlı Materyaller", "Tüm materyallerin listesi ve detaylari")

    materyaller = store.load_objects("materyaller")
    if not materyaller:
        styled_info_banner("Henuz materyal kaydi yok. 'Yeni Materyal Kaydı' sekmesinden ekleyin.", "info", "📚")
        return

    # Filtreler
    c1, c2, c3 = st.columns(3)
    with c1:
        tur_f = st.selectbox("Tur", ["Tümü"] + MATERYAL_TURLERI, key="km_tur_f")
    with c2:
        kat_f = st.selectbox("Kategori", ["Tümü"] + MATERYAL_KATEGORILERI, key="km_kat_f")
    with c3:
        arama = st.text_input("Ara (baslik/yazar)", key="km_arama")

    filtered = materyaller
    if tur_f != "Tümü":
        filtered = [m for m in filtered if m.tur == tur_f]
    if kat_f != "Tümü":
        filtered = [m for m in filtered if m.kategori == kat_f]
    if arama:
        arama_l = arama.lower()
        filtered = [m for m in filtered if arama_l in m.baslik.lower() or arama_l in m.yazar.lower()]

    styled_info_banner(f"Toplam: {len(filtered)} materyal ({sum(m.adet for m in filtered)} adet)", "info", "📚")

    if filtered:
        rows = ""
        for m in sorted(filtered, key=lambda x: x.baslik):
            mevcut_renk = _CLR_GREEN if m.mevcut_adet > 0 else "#ef4444"
            rows += f"""<tr>
                <td style="padding:6px 10px;font-weight:600;">{m.materyal_kodu}</td>
                <td style="padding:6px 10px;">{m.baslik}</td>
                <td style="padding:6px 10px;">{m.yazar}</td>
                <td style="padding:6px 10px;">{m.tur}</td>
                <td style="padding:6px 10px;">{m.kategori}</td>
                <td style="padding:6px 10px;text-align:center;">{m.adet}</td>
                <td style="padding:6px 10px;text-align:center;color:{mevcut_renk};font-weight:600;">{m.mevcut_adet}</td>
                <td style="padding:6px 10px;">{m.raf_no}</td>
                <td style="padding:6px 10px;">{_durum_badge(m.durum)}</td>
            </tr>"""
        st.markdown(_html_table(
            ["Kod", "Başlık", "Yazar", "Tur", "Kategori", "Adet", "Mevcut", "Raf", "Durum"],
            rows, _CLR_BLUE
        ), unsafe_allow_html=True)

        # Silme / Duzenleme
        st.markdown("---")
        styled_section("Materyal İşlemleri")
        mat_opts = {f"{m.materyal_kodu} - {m.baslik}": m.id for m in filtered}
        secili = st.selectbox("Materyal Sec", list(mat_opts.keys()), key="km_sec")
        if secili:
            mat_id = mat_opts[secili]
            c1, c2, c3 = st.columns(3)
            with c1:
                yeni_durum = st.selectbox("Durum", MATERYAL_DURUMLARI, key="km_durum")
                if st.button("Durumu Güncelle", key="km_durum_btn"):
                    mat = store.get_by_id("materyaller", mat_id)
                    if mat:
                        mat.durum = yeni_durum
                        mat.updated_at = _now()
                        store.upsert("materyaller", mat)
                        st.success(f"Durum güncellendi: {yeni_durum}")
                        st.rerun()
            with c2:
                ek_adet = st.number_input("Eklenecek Adet", min_value=1, value=1, key="km_ek_adet")
                if st.button("Adet Ekle", key="km_adet_btn"):
                    mat = store.get_by_id("materyaller", mat_id)
                    if mat:
                        mat.adet += int(ek_adet)
                        mat.mevcut_adet += int(ek_adet)
                        mat.updated_at = _now()
                        store.upsert("materyaller", mat)
                        st.success(f"{ek_adet} adet eklendi.")
                        st.rerun()
            with c3:
                if confirm_action("Materyali Sil", "Bu materyali kayıtlardan silmek istediğinize emin misiniz?", key="km_sil_btn"):
                    store.delete_by_id("materyaller", mat_id)
                    st.success("Materyal silindi.")
                    st.rerun()


# ============================================================
# SEKME 3: YENI MATERYAL KAYDI
# ============================================================

def _render_yeni_materyal(store: KutuphaneDataStore):
    styled_header("Yeni Materyal Kaydı", "Kitap, dijital materyal ve diger kaynaklari ekleyin")

    with st.form("yeni_mat_form"):
        c1, c2 = st.columns(2)
        with c1:
            baslik = st.text_input("Başlık *", placeholder="Kitap/materyal adi", key="kutuphane_1")

            yazar = st.text_input("Yazar", placeholder="Yazar adi", key="kutuphane_2")

            tur = st.selectbox("Tur", MATERYAL_TURLERI, key="kutuphane_3")

            kategori = st.selectbox("Kategori", MATERYAL_KATEGORILERI, key="kutuphane_4")

            dil = st.selectbox("Dil", MATERYAL_DILLERI, key="kutuphane_5")

        with c2:
            isbn = st.text_input("ISBN", placeholder="978-XXX-XXX-XXX-X", key="kutuphane_6")

            yayinevi = st.text_input("Yayinevi", key="kutuphane_7")

            yayin_yili = st.number_input("Yayin Yili", min_value=1900, max_value=2040, value=2024, key="kutuphane_8")

            sayfa = st.number_input("Sayfa Sayısı", min_value=0, value=0, key="kutuphane_9")

            adet = st.number_input("Adet", min_value=1, value=1, key="kutuphane_10")


        c3, c4 = st.columns(2)
        with c3:
            raf_no = st.text_input("Raf No", placeholder="Orn: A-3-12", key="kutuphane_11")

            konum = st.text_input("Konum", placeholder="Orn: Ana Kutuphane", key="kutuphane_12")

        with c4:
            dijital_url = st.text_input("Dijital URL (dijital materyaller icin)", key="kutuphane_13")

            aciklama = st.text_area("Açıklama", height=68, key="kutuphane_14")


        submitted = st.form_submit_button("Materyal Kaydet", use_container_width=True)

    if submitted and baslik:
        mat = Materyal(
            materyal_kodu=store.next_materyal_code(),
            baslik=baslik, yazar=yazar, isbn=isbn,
            tur=tur, kategori=kategori, dil=dil,
            yayinevi=yayinevi, yayin_yili=int(yayin_yili),
            sayfa_sayisi=int(sayfa), adet=int(adet), mevcut_adet=int(adet),
            raf_no=raf_no, konum=konum, dijital_url=dijital_url, aciklama=aciklama,
        )
        store.upsert("materyaller", mat)
        user = AuthManager.get_current_user()
        store.log("materyal_ekle", "materyal", mat.id,
                  f"{baslik} ({tur}) x{adet}", user.get("name", ""))
        st.success(f"Materyal kaydedildi: {mat.materyal_kodu} - {baslik}")
        st.rerun()


# ============================================================
# SEKME 4: ODUNC ISLEMLERI
# ============================================================

def _render_odunc_islemleri(store: KutuphaneDataStore):
    styled_header("Ödünç İşlemleri", "Materyal odunc verme ve iade alma")

    sub_tabs = st.tabs(["📤 Ödünç Ver", "📥 İade Al", "🔄 Süre Uzat"])

    # --- Odunc Ver ---
    with sub_tabs[0]:
        styled_section("Ödünç Ver", _CLR_BLUE)
        materyaller = [m for m in store.load_objects("materyaller")
                       if m.durum == "Aktif" and m.mevcut_adet > 0]
        if not materyaller:
            styled_info_banner("Ödünç verilecek materyal yok.", "warning", "⚠️")
        else:
            with st.form("odunc_form"):
                mat_opts = {f"{m.materyal_kodu} - {m.baslik} (Mevcut: {m.mevcut_adet})": m.id
                            for m in sorted(materyaller, key=lambda x: x.baslik)}
                mat_sec = st.selectbox("Materyal", list(mat_opts.keys()), key="od_mat")

                c1, c2 = st.columns(2)
                with c1:
                    alan_tipi = st.selectbox("Ödünç Alan Tipi", ODUNC_ALAN_TIPLERI, key="od_tip")
                    alan_adi = st.text_input("Ad Soyad *", key="od_ad")
                with c2:
                    alan_sinif = st.text_input("Sınıf/Birim", key="od_sinif")
                    alan_id = st.text_input("Numara/ID", key="od_id")

                notlar = st.text_input("Notlar", key="od_not")
                submitted = st.form_submit_button("Ödünç Ver", use_container_width=True)

            if submitted and alan_adi and mat_sec:
                user = AuthManager.get_current_user()
                ok, msg = store.odunc_ver(
                    mat_opts[mat_sec], alan_tipi, alan_adi,
                    alan_sinif, alan_id, notlar, user.get("name", "")
                )
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    # --- Iade Al ---
    with sub_tabs[1]:
        styled_section("İade Al", _CLR_GREEN)
        aktif = [i for i in store.load_objects("odunc_islemleri") if i.durum in ("Ödünç", "Gecikti")]
        if not aktif:
            styled_info_banner("İade edilecek odunc islem yok.", "success", "✅")
        else:
            islem_opts = {f"{i.islem_kodu} - {i.materyal_adi} -> {i.odunc_alan_adi}": i.id
                         for i in sorted(aktif, key=lambda x: x.iade_tarihi)}
            secili = st.selectbox("İşlem Sec", list(islem_opts.keys()), key="ia_sec")

            if secili:
                isl = store.get_by_id("odunc_islemleri", islem_opts[secili])
                if isl:
                    gecikme_str = ""
                    if isl.iade_tarihi:
                        try:
                            beklenen = date.fromisoformat(isl.iade_tarihi)
                            if date.today() > beklenen:
                                gun = (date.today() - beklenen).days
                                gecikme_str = f" | **Gecikme: {gun} gun**"
                        except (ValueError, TypeError):
                            pass
                    styled_info_banner(
                        f"Materyal: {isl.materyal_adi} | Alan: {isl.odunc_alan_adi} | "
                        f"Ödünç: {isl.odunc_tarihi} | İade Beklenen: {isl.iade_tarihi}{gecikme_str}",
                        _CLR_BLUE, "📖"
                    )

                if st.button("İade Al", key="ia_btn", use_container_width=True):
                    user = AuthManager.get_current_user()
                    ok, msg = store.iade_al(islem_opts[secili], user.get("name", ""))
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    # --- Sure Uzat ---
    with sub_tabs[2]:
        styled_section("Sure Uzat", _CLR_GOLD)
        aktif = [i for i in store.load_objects("odunc_islemleri") if i.durum == "Ödünç"]
        if not aktif:
            styled_info_banner("Uzatilacak odunc islem yok.", "warning", "📋")
        else:
            islem_opts = {f"{i.islem_kodu} - {i.materyal_adi} -> {i.odunc_alan_adi} (Uzatma: {i.uzatma_sayisi})": i.id
                         for i in aktif}
            secili = st.selectbox("İşlem Sec", list(islem_opts.keys()), key="uz_sec")
            if st.button("Sureyi Uzat", key="uz_btn", use_container_width=True):
                user = AuthManager.get_current_user()
                ok, msg = store.uzat(islem_opts[secili], user.get("name", ""))
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)


# ============================================================
# SEKME 5: ODUNC TAKIP
# ============================================================

def _render_odunc_takip(store: KutuphaneDataStore):
    styled_header("Ödünç Takip", "Ödünç verilen materyallerin durumu")

    store.gecikme_guncelle()
    islemler = store.load_objects("odunc_islemleri")

    # Filtre
    durum_f = st.radio("Durum", ["Tümü", "Ödünç", "Gecikti", "İade Edildi"], horizontal=True, key="ot_durum")

    if durum_f != "Tümü":
        filtered = [i for i in islemler if i.durum == durum_f]
    else:
        filtered = islemler

    if not filtered:
        styled_info_banner("Kayıt bulunamadı.", "info", "📋")
        return

    aktif = [i for i in filtered if i.durum in ("Ödünç", "Gecikti")]
    iade = [i for i in filtered if i.durum == "İade Edildi"]
    geciken = [i for i in filtered if i.durum == "Gecikti"]

    styled_stat_row([
        ("Toplam", str(len(filtered)), _CLR_BLUE, "📊"),
        ("Aktif Ödünç", str(len(aktif)), _CLR_ORANGE, "🔄"),
        ("İade Edildi", str(len(iade)), "success", "✅"),
        ("Geciken", str(len(geciken)), "#ef4444" if geciken else _CLR_GRAY, "⏰"),
    ])

    rows = ""
    for i in sorted(filtered, key=lambda x: x.odunc_tarihi, reverse=True)[:100]:
        gecikme_html = f'<span style="color:#ef4444;font-weight:600;">{i.gecikme_gun}g</span>' if i.gecikme_gun > 0 else "-"
        rows += f"""<tr>
            <td style="padding:6px 10px;font-weight:600;">{i.islem_kodu}</td>
            <td style="padding:6px 10px;">{i.materyal_adi}</td>
            <td style="padding:6px 10px;">{i.odunc_alan_adi}</td>
            <td style="padding:6px 10px;">{i.odunc_alan_tipi}</td>
            <td style="padding:6px 10px;">{i.odunc_tarihi}</td>
            <td style="padding:6px 10px;">{i.iade_tarihi}</td>
            <td style="padding:6px 10px;">{i.gercek_iade_tarihi or "-"}</td>
            <td style="padding:6px 10px;text-align:center;">{gecikme_html}</td>
            <td style="padding:6px 10px;">{_durum_badge(i.durum)}</td>
        </tr>"""
    st.markdown(_html_table(
        ["Kod", "Materyal", "Ödünç Alan", "Tip", "Ödünç", "Beklenen İade", "Gercek İade", "Gecikme", "Durum"],
        rows, _CLR_BLUE
    ), unsafe_allow_html=True)


# ============================================================
# SEKME 6: ANALIZ
# ============================================================

def _render_analiz(store: KutuphaneDataStore):
    styled_header("Analiz", "Ödünç analizi, okuyucu profilleri ve tur dagilimlari")

    analizcisi = OduncAnalizcisi(store)

    sub_tabs = st.tabs(["📚 En Çok Okunan", "👤 En Aktif Okuyucular", "📋 Okuyucu Karnesi", "📊 Tür Analizi"])

    with sub_tabs[0]:
        styled_section("En Çok Ödünç Alinan Materyaller", _CLR_BLUE)
        en_cok = analizcisi.en_cok_okunan(15)
        if en_cok:
            try:
                import plotly.graph_objects as go
                fig = go.Figure(go.Bar(
                    y=[e["baslik"][:30] for e in en_cok],
                    x=[e["odunc_sayisi"] for e in en_cok],
                    orientation="h", marker_color=SC_COLORS[0],
                    text=[str(e["odunc_sayisi"]) for e in en_cok],
                    textposition="auto",
                ))
                sc_bar(fig, height=max(250, len(en_cok) * 30), horizontal=True)
                fig.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            except ImportError:
                for e in en_cok:
                    st.write(f"**{e['baslik']}** - {e['odunc_sayisi']} odunc")
        else:
            styled_info_banner("Henuz odunc verisi yok.", "info", "📊")

    with sub_tabs[1]:
        styled_section("En Aktif Okuyucular", _CLR_GREEN)
        okuyucular = analizcisi.en_aktif_okuyucular(15)
        if okuyucular:
            rows = ""
            for o in okuyucular:
                gecikme_renk = "#ef4444" if o["gecikme_sayisi"] > 0 else _CLR_GREEN
                rows += f"""<tr>
                    <td style="padding:6px 10px;font-weight:600;">{o['ad']}</td>
                    <td style="padding:6px 10px;">{o['tip']}</td>
                    <td style="padding:6px 10px;">{o['sinif']}</td>
                    <td style="padding:6px 10px;text-align:center;color:{_CLR_BLUE};font-weight:600;">{o['odunc_sayisi']}</td>
                    <td style="padding:6px 10px;text-align:center;color:{_CLR_GREEN};">{o['iade_sayisi']}</td>
                    <td style="padding:6px 10px;text-align:center;color:{gecikme_renk};">{o['gecikme_sayisi']}</td>
                </tr>"""
            st.markdown(_html_table(
                ["Ad Soyad", "Tip", "Sınıf", "Ödünç", "İade", "Gecikme"],
                rows, _CLR_GREEN
            ), unsafe_allow_html=True)

            try:
                import plotly.graph_objects as go
                fig = go.Figure(go.Bar(
                    x=[o["ad"][:15] for o in okuyucular[:10]],
                    y=[o["odunc_sayisi"] for o in okuyucular[:10]],
                    marker_color=SC_COLORS[0],
                    text=[str(o["odunc_sayisi"]) for o in okuyucular[:10]],
                    textposition="auto",
                ))
                sc_bar(fig, height=280)
                fig.update_layout(xaxis=dict(tickangle=-45))
                st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            except ImportError:
                pass
        else:
            styled_info_banner("Henuz okuyucu verisi yok.", "info", "📊")

    with sub_tabs[2]:
        styled_section("Okuyucu Karnesi", _CLR_GOLD)
        islemler = store.load_objects("odunc_islemleri")
        okuyucu_listesi = sorted(set(i.odunc_alan_adi for i in islemler if i.odunc_alan_adi))
        if not okuyucu_listesi:
            styled_info_banner("Henuz okuyucu verisi yok.", "info", "📊")
        else:
            secili = st.selectbox("Okuyucu Sec", okuyucu_listesi, key="ok_sec")
            if secili:
                karne = analizcisi.okuyucu_karnesi(secili)
                if karne:
                    styled_stat_row([
                        ("Toplam Ödünç", str(karne["toplam_odunc"]), "info", "📚"),
                        ("İade Edilen", str(karne["iade_edilen"]), "success", "✅"),
                        ("Geciken", str(karne["geciken"]), "#ef4444" if karne["geciken"] > 0 else _CLR_GRAY, "⏰"),
                        ("İade Orani", f"%{karne['iade_orani']:.0f}", _CLR_GOLD, "📊"),
                    ])

                    if karne["tur_dagilimi"]:
                        try:
                            import plotly.graph_objects as go
                            labels = list(karne["tur_dagilimi"].keys())
                            values = list(karne["tur_dagilimi"].values())
                            fig = go.Figure(go.Pie(
                                labels=labels, values=values, hole=0.55,
                                marker=dict(colors=SC_COLORS[:len(labels)], line=dict(color="#fff", width=2)),
                                textinfo="label+value",
                            ))
                            sc_pie(fig, height=280)
                            st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
                        except ImportError:
                            pass

    with sub_tabs[3]:
        styled_section("Tur Bazli Ödünç Analizi", _CLR_ORANGE)
        tur_dag = analizcisi.tur_dagilimi()
        if tur_dag:
            try:
                import plotly.graph_objects as go
                col1, col2 = st.columns(2)
                with col1:
                    fig = go.Figure(go.Pie(
                        labels=list(tur_dag.keys()), values=list(tur_dag.values()),
                        hole=0.55,
                        marker=dict(colors=SC_COLORS[:len(tur_dag)], line=dict(color="#fff", width=2)),
                        textinfo="label+percent",
                    ))
                    sc_pie(fig, height=300)
                    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)

                with col2:
                    # Sunburst: Tur > Kategori
                    kat_dag = analizcisi.kategori_dagilimi()
                    if kat_dag:
                        labels_sb = ["Kutuphane"] + list(tur_dag.keys()) + list(kat_dag.keys())
                        parents_sb = [""] + ["Kutuphane"] * len(tur_dag) + ["Kutuphane"] * len(kat_dag)
                        values_sb = [sum(tur_dag.values())] + list(tur_dag.values()) + list(kat_dag.values())
                        fig = go.Figure(go.Sunburst(
                            labels=labels_sb, parents=parents_sb, values=values_sb,
                            branchvalues="total",
                            marker=dict(colors=SC_COLORS[:len(labels_sb)]),
                        ))
                        fig.update_layout(
                            height=300, margin=dict(t=10, b=10, l=10, r=10),
                            paper_bgcolor="rgba(0,0,0,0)",
                        )
                        st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
            except ImportError:
                for t, v in tur_dag.items():
                    st.write(f"**{t}**: {v}")
        else:
            styled_info_banner("Henuz odunc verisi yok.", "info", "📊")


# ============================================================
# SEKME 7: RAPORLAR
# ============================================================

def _render_raporlar(store: KutuphaneDataStore):
    styled_header("Raporlar", "Günlük raporlar, envanter ozeti ve PDF export")

    sub_tabs = st.tabs(["📅 Günlük Rapor", "📦 Envanter Özeti", "⏰ Gecikme Raporu"])

    with sub_tabs[0]:
        styled_section("Günlük Rapor")
        tarih = st.date_input("Tarih", value=date.today(), key="rp_tarih")
        raporlayici = KutuphaneRaporlayici(store)
        ozet = raporlayici.gunluk_ozet(tarih.isoformat())

        styled_stat_row([
            ("Ödünç Verilen", str(ozet["odunc_sayisi"]), "info", "📖"),
            ("İade Alinan", str(ozet["iade_sayisi"]), _CLR_GREEN, "📥"),
            ("Geciken Toplam", str(ozet["geciken_sayisi"]), "#ef4444" if ozet["geciken_sayisi"] > 0 else _CLR_GRAY, "⏰"),
        ])

        if ozet["odunc_detay"]:
            styled_section("Ödünç Verilenler", _CLR_BLUE)
            rows = ""
            for i in ozet["odunc_detay"]:
                rows += f"""<tr>
                    <td style="padding:6px 10px;">{i.islem_kodu}</td>
                    <td style="padding:6px 10px;">{i.materyal_adi}</td>
                    <td style="padding:6px 10px;">{i.odunc_alan_adi}</td>
                    <td style="padding:6px 10px;">{i.iade_tarihi}</td>
                </tr>"""
            st.markdown(_html_table(["Kod", "Materyal", "Alan", "İade Tarihi"], rows, _CLR_BLUE),
                        unsafe_allow_html=True)

        if ozet["iade_detay"]:
            styled_section("İade Alinanlar", _CLR_GREEN)
            rows = ""
            for i in ozet["iade_detay"]:
                rows += f"""<tr>
                    <td style="padding:6px 10px;">{i.islem_kodu}</td>
                    <td style="padding:6px 10px;">{i.materyal_adi}</td>
                    <td style="padding:6px 10px;">{i.odunc_alan_adi}</td>
                    <td style="padding:6px 10px;">{i.gecikme_gun if i.gecikme_gun > 0 else '-'}</td>
                </tr>"""
            st.markdown(_html_table(["Kod", "Materyal", "Alan", "Gecikme (gun)"], rows, _CLR_GREEN),
                        unsafe_allow_html=True)

        # PDF export
        st.markdown("---")
        if st.button("PDF Rapor Oluştur", key="rp_pdf_btn"):
            try:
                from utils.report_utils import ReportPDFGenerator, get_institution_info
                pdf = ReportPDFGenerator(
                    f"Kutuphane Günlük Rapor - {tarih.isoformat()}",
                    f"Ödünç: {ozet['odunc_sayisi']} | İade: {ozet['iade_sayisi']} | Geciken: {ozet['geciken_sayisi']}"
                )
                info = get_institution_info()
                pdf.add_institution_header(info)
                pdf.add_section_header("Günlük Özet")
                data_rows = [
                    ["Ödünç Verilen", str(ozet["odunc_sayisi"])],
                    ["İade Alinan", str(ozet["iade_sayisi"])],
                    ["Geciken", str(ozet["geciken_sayisi"])],
                ]
                pdf.add_table(["İşlem", "Sayı"], data_rows)
                pdf_bytes = pdf.get_bytes()
                st.download_button("PDF Indir", data=pdf_bytes,
                                   file_name=f"kutuphane_gunluk_{tarih.isoformat()}.pdf",
                                   mime="application/pdf")
            except Exception as e:
                st.error(f"PDF olusturulamadi: {e}")

    with sub_tabs[1]:
        styled_section("Envanter Özeti")
        raporlayici = KutuphaneRaporlayici(store)
        env = raporlayici.envanter_ozeti()

        styled_stat_row([
            ("Materyal Cesit", str(env["toplam_cesit"]), "info", "📚"),
            ("Toplam Adet", str(env["toplam_adet"]), _CLR_TEAL, "📋"),
            ("Mevcut", str(env["mevcut_adet"]), "success", "✅"),
            ("Ödünç", str(env["odunc_adet"]), _CLR_ORANGE, "🔄"),
        ])

        try:
            import plotly.graph_objects as go
            col1, col2 = st.columns(2)
            with col1:
                if env["tur_dagilimi"]:
                    styled_section("Tur Dagilimi", _CLR_BLUE)
                    tur_labels = list(env["tur_dagilimi"].keys())
                    fig = go.Figure(go.Pie(
                        labels=tur_labels,
                        values=list(env["tur_dagilimi"].values()),
                        hole=0.55,
                        marker=dict(colors=SC_COLORS[:len(tur_labels)], line=dict(color="#fff", width=2)),
                        textinfo="label+value",
                    ))
                    sc_pie(fig, height=300)
                    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)

            with col2:
                if env["kategori_dagilimi"]:
                    styled_section("Kategori Dagilimi", _CLR_ORANGE)
                    labels = list(env["kategori_dagilimi"].keys())[:10]
                    values = [env["kategori_dagilimi"][k] for k in labels]
                    fig = go.Figure(go.Bar(
                        y=labels, x=values, orientation="h",
                        marker_color=SC_COLORS[0],
                        text=[str(v) for v in values], textposition="auto",
                    ))
                    sc_bar(fig, height=300, horizontal=True)
                    fig.update_layout(yaxis=dict(autorange="reversed"))
                    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
        except ImportError:
            pass

        # Doluluk orani donut
        try:
            import plotly.graph_objects as go
            if env["toplam_adet"] > 0:
                styled_section("Doluluk Orani")
                oran = env["doluluk_orani"]
                fig = go.Figure(go.Pie(
                    values=[oran, 100 - oran],
                    labels=["Ödünç", "Mevcut"],
                    hole=0.55,
                    marker=dict(colors=[SC_COLORS[3], "#e2e8f0"], line=dict(color="#fff", width=2)),
                    textinfo="none",
                ))
                sc_pie(fig, height=250, center_text=f"<b>%{oran:.1f}</b>")
                st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)
        except ImportError:
            pass

    with sub_tabs[2]:
        styled_section("Gecikme Raporu", "#ef4444")
        store.gecikme_guncelle()
        geciken = [i for i in store.load_objects("odunc_islemleri") if i.durum == "Gecikti"]
        if not geciken:
            styled_info_banner("Geciken materyal yok!", "success", "✅")
        else:
            styled_info_banner(f"{len(geciken)} adet geciken materyal var.", "error", "⏰")
            rows = ""
            for i in sorted(geciken, key=lambda x: x.gecikme_gun, reverse=True):
                rows += f"""<tr>
                    <td style="padding:6px 10px;">{i.materyal_adi}</td>
                    <td style="padding:6px 10px;">{i.odunc_alan_adi}</td>
                    <td style="padding:6px 10px;">{i.odunc_alan_tipi}</td>
                    <td style="padding:6px 10px;">{i.odunc_alan_sinif}</td>
                    <td style="padding:6px 10px;">{i.odunc_tarihi}</td>
                    <td style="padding:6px 10px;">{i.iade_tarihi}</td>
                    <td style="padding:6px 10px;color:#ef4444;font-weight:700;">{i.gecikme_gun} gun</td>
                </tr>"""
            st.markdown(_html_table(
                ["Materyal", "Ödünç Alan", "Tip", "Sınıf", "Ödünç Tarihi", "İade Tarihi", "Gecikme"],
                rows, "#ef4444"
            ), unsafe_allow_html=True)


# ============================================================
# SEKME 8: AYARLAR
# ============================================================

def _render_ayarlar(store: KutuphaneDataStore):
    styled_header("Ayarlar", "Kutuphane genel ayarlari")

    ayarlar = store.load_objects("kutuphane_ayarlar")
    if ayarlar:
        styled_section("Genel Ayarlar")
        for ayar in ayarlar:
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                st.text_input(ayar.ayar_adi, value=ayar.deger, key=f"ka_{ayar.id}", disabled=True)
            with c2:
                st.caption(ayar.aciklama)
            with c3:
                yeni = st.text_input("Yeni", key=f"ka_y_{ayar.id}")
                if yeni and yeni != ayar.deger:
                    if st.button("Güncelle", key=f"ka_b_{ayar.id}"):
                        ayar.deger = yeni
                        ayar.updated_at = _now()
                        store.upsert("kutuphane_ayarlar", ayar)
                        st.success(f"{ayar.ayar_adi} güncellendi.")
                        st.rerun()


# ============================================================
# SEKME 9: SMARTI
# ============================================================

def _render_smarti(store: KutuphaneDataStore):
    def _ktp_data_context() -> str:
        try:
            dash = KutuphaneDashboard(store)
            kpi = dash.kpi_hesapla()
            return (
                f"Toplam Materyal: {kpi['toplam_adet']}, "
                f"Mevcut: {kpi['mevcut_adet']}, "
                f"Ödünç: {kpi['odunc_adet']}, "
                f"Geciken: {kpi['geciken']}, "
                f"Bugün Ödünç: {kpi['bugun_odunc']}, "
                f"Bugün İade: {kpi['bugun_iade']}, "
                f"Toplam İşlem: {kpi['toplam_odunc_islem']}"
            )
        except Exception:
            return ""
    render_smarti_chat("kutuphane", _ktp_data_context)


# ============================================================
# SPOTLIGHT READING (Yabanci Dil modulunden)
# ============================================================

def _render_spotlight_reading_ktp():
    """Spotlight Reading sekmesi - Yabanci Dil modulundeki formati kullanir."""
    from views.yd_tools import (
        _render_spotlight_story_card,
        _build_spotlight_html,
    )
    from utils.spotlight_stories import get_stories_for_grade, get_total_story_count
    from utils.spotlight_unit_stories import (
        get_unit_stories, get_unit_story_list, get_unit_info,
        get_grades_with_units, get_total_unit_stories,
    )

    st.markdown(
        '<div style="background:linear-gradient(135deg,#1e1b4b,#312e81);border-radius:14px;'
        'padding:16px 24px;margin-bottom:16px;">'
        '<span style="font-size:1.3rem;font-weight:800;color:#e0e7ff;">📖 Spotlight Reading</span>'
        '<span style="color:#a5b4fc;font-size:.85rem;margin-left:12px;">'
        'İnteraktif Okuma — Tıklayarak Öğren, Dinleyerek Pekiştir</span></div>',
        unsafe_allow_html=True,
    )

    _CEFR = {0: "Pre-A1", 1: "A1", 2: "A1", 3: "A1", 4: "A1", 5: "A2", 6: "A2",
             7: "A2", 8: "A2", 9: "B1", 10: "B1+", 11: "B2", 12: "B2+"}
    _GLABELS = {0: "Okul Öncesi", **{g: f"{g}. Sınıf" for g in range(1, 13)}}

    _mode_tabs = st.tabs(["  📖 Bağımsız Metinler  ", "  📚 Ünite Metinleri  "])

    # ── MOD 1: BAGIMSIZ METİNLER ──
    with _mode_tabs[0]:
        _total = get_total_story_count()
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#e11d4810,#f43f5e10);'
            f'border:1px solid #e11d4833;border-radius:10px;padding:10px 16px;margin-bottom:10px;">'
            f'<span style="color:#e11d48;font-weight:700;">📖 Bağımsız Okuma Metinleri</span>'
            f'<span style="color:#94a3b8;font-size:.85rem;margin-left:8px;">'
            f'Sınıf bazlı hikayeler | Toplam {_total} hikaye</span></div>',
            unsafe_allow_html=True,
        )

        _gc1, _gc2 = st.columns([1, 2])
        with _gc1:
            _sr_grade = st.selectbox(
                "Sınıf Seç",
                list(range(0, 13)),
                index=5,
                format_func=lambda g: f"{_GLABELS[g]} ({_CEFR[g]})",
                key="ktp_spotlight_grade",
            )

        stories = get_stories_for_grade(_sr_grade)
        if not stories:
            st.info("Bu sınıf için henüz hikaye eklenmedi.")
        else:
            with _gc2:
                _story_titles = [
                    f"{s['illustration_emoji']} {s['title']} — {s['title_tr']}  (+{len(s['spotlight_words'])} kelime)"
                    for s in stories
                ]
                _sr_idx = st.selectbox("Hikaye Seç", range(len(stories)),
                                       format_func=lambda i: _story_titles[i],
                                       key="ktp_spotlight_story")
            story = stories[_sr_idx]
            _render_spotlight_story_card(story)

    # ── MOD 2: ÜNİTE METİNLERİ ──
    with _mode_tabs[1]:
        _unit_total = get_total_unit_stories()
        _unit_grades = get_grades_with_units()
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#6366f110,#818cf810);'
            f'border:1px solid #6366f133;border-radius:10px;padding:10px 16px;margin-bottom:10px;">'
            f'<span style="color:#6366f1;font-weight:700;">📚 Ünite Bazlı Okuma Parçaları</span>'
            f'<span style="color:#94a3b8;font-size:.85rem;margin-left:8px;">'
            f'Müfredat ünitelerine bağlı | Toplam {_unit_total} hikaye</span></div>',
            unsafe_allow_html=True,
        )

        if not _unit_grades:
            st.info("Henüz ünite bazlı hikaye eklenmedi.")
            return

        _uc1, _uc2, _uc3 = st.columns([1, 1, 2])
        with _uc1:
            _u_grade = st.selectbox(
                "Sınıf",
                _unit_grades,
                format_func=lambda g: f"{_GLABELS[g]} ({_CEFR[g]})",
                key="ktp_spotlight_unit_grade",
            )

        _u_units = get_unit_stories(_u_grade)
        _u_unit_nums = sorted(_u_units.keys())

        with _uc2:
            _u_unit = st.selectbox(
                "Ünite",
                _u_unit_nums,
                format_func=lambda u: f"Ünite {u}: {_u_units[u]['unit_name_tr']}",
                key="ktp_spotlight_unit_num",
            )

        _u_info = get_unit_info(_u_grade, _u_unit)
        _u_stories = get_unit_story_list(_u_grade, _u_unit)

        if not _u_stories:
            st.warning("Bu ünite için hikaye bulunamadı.")
            return

        st.markdown(
            f'<div style="background:linear-gradient(135deg,#312e81,#1e1b4b);border-radius:12px;'
            f'padding:12px 18px;margin:6px 0 10px 0;display:flex;align-items:center;gap:14px;">'
            f'<div style="background:rgba(99,102,241,.2);border-radius:10px;padding:10px 14px;text-align:center;">'
            f'<div style="font-size:1.4rem;font-weight:800;color:#a5b4fc;">Ünite {_u_unit}</div>'
            f'<div style="font-size:.7rem;color:#818cf8;">Hafta {_u_info.get("weeks","")}</div></div>'
            f'<div>'
            f'<div style="font-size:1.05rem;font-weight:700;color:#e0e7ff;">{_u_info["unit_name"]}</div>'
            f'<div style="font-size:.85rem;color:#a5b4fc;">{_u_info["unit_name_tr"]}</div>'
            f'</div>'
            f'<div style="margin-left:auto;background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.3);'
            f'border-radius:16px;padding:5px 14px;">'
            f'<span style="font-weight:700;color:#818cf8;">{len(_u_stories)}</span>'
            f'<span style="color:#a5b4fc;font-size:.78rem;margin-left:4px;">Parça</span></div></div>',
            unsafe_allow_html=True,
        )

        with _uc3:
            _u_story_titles = [
                f"{s['illustration_emoji']} {s['title']} — {s['title_tr']}"
                for s in _u_stories
            ]
            _u_idx = st.selectbox("Okuma Parçası", range(len(_u_stories)),
                                  format_func=lambda i: _u_story_titles[i],
                                  key="ktp_spotlight_unit_story")

        _render_spotlight_story_card(_u_stories[_u_idx])


# ============================================================
# ANA GIRIS NOKTASI
# ============================================================

def render_kutuphane():
    """KTP-01 modulu ana giris noktasi."""
    _inject_ktp_css()

    store = _get_ktp_store()

    tab_names = [
        "📊 Dashboard",
        "📚 Kayıtlı Materyaller",
        "➕ Yeni Materyal",
        "📖 Ödünç İşlemleri",
        "🔍 Ödünç Takip",
        "📊 Analiz",
        "📈 Raporlar",
        "📖 Spotlight Reading",
        "📖 Okuma Kulübü",
        "🔄 Envanter Takip",
        "⏰ Gecikme Yönetim",
        "⚙️ Ayarlar",
        "🤖 Smarti",
    ]

    render_smarti_welcome("kutuphane")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("kutuphane_egitim_yili")

    tabs = st.tabs(tab_names)

    with tabs[0]:
        _render_dashboard(store)
    with tabs[1]:
        _render_kayitli_materyaller(store)
    with tabs[2]:
        _render_yeni_materyal(store)
    with tabs[3]:
        _render_odunc_islemleri(store)
    with tabs[4]:
        _render_odunc_takip(store)
    with tabs[5]:
        _render_analiz(store)
    with tabs[6]:
        _render_raporlar(store)
    with tabs[7]:
        _render_spotlight_reading_ktp()
    with tabs[8]:
        try:
            from views._ktp_yeni_ozellikler import render_okuma_kulubu
            render_okuma_kulubu(store)
        except Exception as _e:
            st.error(f"Okuma Kulubu yuklenemedi: {_e}")
    with tabs[9]:
        try:
            from views._ktp_yeni_ozellikler import render_envanter_takip
            render_envanter_takip(store)
        except Exception as _e:
            st.error(f"Envanter Takip yuklenemedi: {_e}")
    with tabs[10]:
        try:
            from views._ktp_yeni_ozellikler import render_gecikme_yonetim
            render_gecikme_yonetim(store)
        except Exception as _e:
            st.error(f"Gecikme Yonetim yuklenemedi: {_e}")
    with tabs[11]:
        _render_ayarlar(store)
    with tabs[12]:
        _render_smarti(store)
