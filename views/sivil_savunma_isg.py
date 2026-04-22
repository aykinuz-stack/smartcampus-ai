"""
SSG-01 Sivil Savunma, ISG ve Okul/Öğrenci Güvenliği Takip Modulu - Streamlit UI
=================================================================================
Dashboard, Sivil Savunma (A), ISG (B), Okul/Öğrenci Güvenliği (C),
Olay Kayıtları, Raporlar ve Ayarlar.
"""

from __future__ import annotations

import os
from datetime import datetime, date
from collections import Counter

import streamlit as st
import pandas as pd

from utils.tenant import get_tenant_dir
from utils.report_utils import ReportStyler, ReportPDFGenerator, get_institution_info, CHART_PALETTE
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("sivil_savunma")
except Exception:
    pass
from models.sivil_savunma_isg import (
    SSGDataStore,
    SSGAyar, SSGSorumlu, ChecklistItem, ChecklistKayit,
    TatbikatPlani, TatbikatChecklist, TatbikatKaydi,
    RiskTehlike, RiskKaydi, DenetimKaydi, OlayKaydi, EylemPlani,
    RiskCalculator, TatbikatScorer, ChecklistValidator, TatbikatPlanner,
    CHECKLIST_DURUMLARI, ISLEM_TIPLERI, ONAY_DURUMLARI,
    TATBIKAT_TIPLERI, TATBIKAT_PUANLARI, TATBIKAT_PUAN_MAP,
    RISK_SEVIYELERI, RISK_SEVIYE_RENK, RISK_AKSIYON_DURUMLARI,
    DENETIM_DURUMLARI, OLAY_TIPLERI, OLAY_DURUMLARI,
    EYLEM_DURUMLARI, EYLEM_PLAN_DURUMLARI,
    BOLUM_KODLARI, ONAY_ROLLER, SORUMLU_ROLLER, SORUMLU_ROL_ADI,
    DEFAULT_DENETIM_SABLONLARI,
)


# ============================================================
# STORE INIT
# ============================================================

def _get_ssg_store() -> SSGDataStore:
    base = os.path.join(get_tenant_dir(), "ssg")
    store = SSGDataStore(base)
    _pop_key = "ssg01_defaults_populated"
    if _pop_key not in st.session_state:
        store.auto_populate_defaults()
        st.session_state[_pop_key] = True
    return store


# ============================================================
# CSS & STYLED HELPERS
# ============================================================

def _inject_ssg_css():
    inject_common_css("ssg")
    st.markdown("""
    <style>
    :root {
        --ssg-primary: #2563eb;
        --ssg-primary-dark: #1e40af;
        --ssg-success: #10b981;
        --ssg-warning: #f59e0b;
        --ssg-danger: #ef4444;
        --ssg-purple: #8b5cf6;
        --ssg-teal: #0d9488;
        --ssg-dark: #0B0F19;
    }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #2563eb;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
        border: none !important; border-radius: 10px !important; font-weight: 600 !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
    }
    hr { border: none !important; height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, #cbd5e1 50%, transparent 100%) !important; }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# YARDIMCI FONKSIYONLAR
# ============================================================

def _current_edu_year() -> str:
    today = date.today()
    if today.month >= 9:
        return f"{today.year}-{today.year + 1}"
    return f"{today.year - 1}-{today.year}"


def _edu_year_options() -> list[str]:
    current = date.today().year
    years = []
    for y in range(current - 2, current + 2):
        years.append(f"{y}-{y + 1}")
    return years


def _durum_renk(durum: str) -> str:
    return {
        "Yapildi": "#10b981",
        "Devam Ediyor": "#f59e0b",
        "Yapilmadi": "#ef4444",
    }.get(durum, "#64748b")


def _durum_badge(durum: str) -> str:
    color = _durum_renk(durum)
    return (
        f'<span style="background:{color};color:#fff;padding:3px 10px;'
        f'border-radius:12px;font-size:11px;font-weight:700;">{durum}</span>'
    )


def _risk_badge(seviye: str) -> str:
    color = RISK_SEVIYE_RENK.get(seviye, "#A5A5A5")
    label = seviye.capitalize()
    return (
        f'<span style="background:{color};color:#fff;padding:3px 10px;'
        f'border-radius:12px;font-size:11px;font-weight:700;">{label}</span>'
    )


def _onay_badge(durum: str) -> str:
    colors = {"Bekliyor": "#f59e0b", "Onaylandi": "#10b981", "Reddedildi": "#ef4444"}
    color = colors.get(durum, "#64748b")
    return (
        f'<span style="background:{color};color:#fff;padding:3px 10px;'
        f'border-radius:12px;font-size:11px;font-weight:700;">{durum}</span>'
    )


# ============================================================
# MAIN RENDER
# ============================================================

def render_sivil_savunma_isg():
    """Ana giris noktasi."""
    _inject_ssg_css()
    styled_header(
        "Sivil Savunma, ISG ve Okul/Öğrenci Güvenliği",
        "SSG-01 — Planlama, Kontrol, Olay Bildirimi ve Raporlama",
        icon="🛡️",
    )

    store = _get_ssg_store()

    render_smarti_welcome("sivil_savunma_isg")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("sivil_savunma_isg_egitim_yili")

    # -- Tab Gruplama (14 tab -> 2 grup) --
    _GRP_81327 = {
        "📋 Grup A": [("📊 Dashboard", 0), ("🛡️ Sivil Savunma", 1), ("⚠️ İSG", 2), ("🔒 Okul Güvenliği", 3), ("📋 Olay Kayıtları", 4), ("📈 Raporlar", 5), ("🗺️ Acil Durum", 6)],
        "📊 Grup B": [("🔥 Risk Haritası", 7), ("📊 Güvenlik Kontrol", 8), ("🎓 Eğitim Akademisi", 9), ("🌡️ İSG Ölçüm", 10), ("🛡️ Zorbalık Önleme", 11), ("⚙️ Ayarlar", 12), ("🤖 Smarti", 13)],
    }
    _sg_81327 = st.radio("", list(_GRP_81327.keys()), horizontal=True, label_visibility="collapsed", key="rg_81327")
    _gt_81327 = _GRP_81327[_sg_81327]
    _aktif_idx_81327 = set(t[1] for t in _gt_81327)
    _tab_names_81327 = [t[0] for t in _gt_81327]
    tabs = st.tabs(_tab_names_81327)
    _tab_real_81327 = {idx: t for idx, t in zip((t[1] for t in _gt_81327), tabs)}

    if 0 in _aktif_idx_81327:
      with _tab_real_81327[0]:
        _render_dashboard(store)
    if 1 in _aktif_idx_81327:
      with _tab_real_81327[1]:
        _render_sivil_savunma(store)
    if 2 in _aktif_idx_81327:
      with _tab_real_81327[2]:
        _render_isg(store)
    if 3 in _aktif_idx_81327:
      with _tab_real_81327[3]:
        _render_okul_ogrenci(store)
    if 4 in _aktif_idx_81327:
      with _tab_real_81327[4]:
        _render_olay_kayitlari(store)
    if 5 in _aktif_idx_81327:
      with _tab_real_81327[5]:
        _render_raporlar(store)
    if 6 in _aktif_idx_81327:
      with _tab_real_81327[6]:
        try:
            from views._ssg_yeni_ozellikler import render_acil_durum_merkezi
            render_acil_durum_merkezi(store)
        except Exception as _e:
            st.error(f"Acil Durum Merkezi yuklenemedi: {_e}")
    if 7 in _aktif_idx_81327:
      with _tab_real_81327[7]:
        try:
            from views._ssg_yeni_ozellikler import render_yangin_afet_risk
            render_yangin_afet_risk(store)
        except Exception as _e:
            st.error(f"Risk Haritasi yuklenemedi: {_e}")
    if 8 in _aktif_idx_81327:
      with _tab_real_81327[8]:
        try:
            from views._ssg_yeni_ozellikler import render_guvenlik_kontrol
            render_guvenlik_kontrol(store)
        except Exception as _e:
            st.error(f"Guvenlik Kontrol yuklenemedi: {_e}")
    if 9 in _aktif_idx_81327:
      with _tab_real_81327[9]:
        try:
            from views._ssg_super_features import render_egitim_akademisi
            render_egitim_akademisi(store)
        except Exception as _e:
            st.error(f"Egitim Akademisi yuklenemedi: {_e}")
    if 10 in _aktif_idx_81327:
      with _tab_real_81327[10]:
        try:
            from views._ssg_super_features import render_isg_olcum
            render_isg_olcum(store)
        except Exception as _e:
            st.error(f"ISG Olcum yuklenemedi: {_e}")
    if 11 in _aktif_idx_81327:
      with _tab_real_81327[11]:
        try:
            from views._ssg_super_features import render_zorbalik_onleme
            render_zorbalik_onleme(store)
        except Exception as _e:
            st.error(f"Zorbalik Onleme yuklenemedi: {_e}")
    if 12 in _aktif_idx_81327:
      with _tab_real_81327[12]:
        _render_ayarlar(store)
    if 13 in _aktif_idx_81327:
      with _tab_real_81327[13]:
        def _ssg_smarti_context():
            try:
                s = _get_ssg_store()
                olay_count = len(s.load_objects("olaylar"))
                risk_count = len(s.load_objects("riskler"))
                denetim_count = len(s.load_objects("denetimler"))
                tatbikat_count = len(s.load_objects("tatbikatlar"))
                return (
                    f"Olay kaydi: {olay_count}, Risk kaydi: {risk_count}, "
                    f"Denetim kaydi: {denetim_count}, Tatbikat kaydi: {tatbikat_count}"
                )
            except Exception:
                return ""
        render_smarti_chat("sivil_savunma_isg", _ssg_smarti_context)


# ============================================================
# TAB 1: DASHBOARD
# ============================================================

def _render_dashboard(store: SSGDataStore):
    styled_section("Genel Bakis", "#0B0F19")

    # Anonim İhbar kritik uyarısı — dashboard'un en üstünde
    try:
        from views._ihbar_hatti import render_ihbar_uyari_badge
        render_ihbar_uyari_badge()
    except Exception:
        pass

    col_y, _ = st.columns([1, 3])
    with col_y:
        egitim_yili = st.selectbox("Egitim Yili", _edu_year_options(),
                                    index=_edu_year_options().index(_current_edu_year())
                                    if _current_edu_year() in _edu_year_options() else 0,
                                    key="ssg_dash_ey")

    items = store.load_objects("checklist_items")
    aktif_items = [i for i in items if i.is_active]
    kayitlar = store.load_objects("checklist_kayitlari")
    yil_kayitlar = [k for k in kayitlar if k.egitim_yili == egitim_yili]

    kayit_map = {k.item_code: k for k in yil_kayitlar}
    yapildi = sum(1 for i in aktif_items if kayit_map.get(i.item_code, ChecklistKayit()).durum == "Yapildi")
    devam = sum(1 for i in aktif_items if kayit_map.get(i.item_code, ChecklistKayit()).durum == "Devam Ediyor")
    yapilmadi = len(aktif_items) - yapildi - devam

    styled_stat_row([
        ("Toplam Madde", str(len(aktif_items)), "#2563eb", "📋"),
        ("Yapildi", str(yapildi), "#10b981", "✅"),
        ("Devam Ediyor", str(devam), "#f59e0b", "🔄"),
        ("Yapilmadi", str(yapilmadi), "#ef4444", "❌"),
    ])

    # Uyari bannerlari
    sorumlular = store.load_objects("sorumlular")
    for rol in SORUMLU_ROLLER:
        sor = next((s for s in sorumlular if s.rol == rol), None)
        if not sor or not sor.var_mi:
            styled_info_banner(f"{SORUMLU_ROL_ADI.get(rol, rol)} atanmamis!", "warning")

    # Tatbikat gecikme uyarisi
    tatbikat_kayitlari = store.load_objects("tatbikat_kayitlari")
    for tk in tatbikat_kayitlari:
        if tk.durum == "Planlandi" and tk.tarih:
            try:
                plan_date = date.fromisoformat(tk.tarih)
                if plan_date < date.today():
                    styled_info_banner(
                        f"Geciken tatbikat: {tk.tatbikat_type} ({tk.tarih})", "danger"
                    )
            except ValueError:
                pass

    # Bolum bazli ozet tablo
    styled_section("Bolum Bazli Özet")
    bolum_data = []
    for sec_code, sec_name in BOLUM_KODLARI.items():
        sec_items = [i for i in aktif_items if i.section == sec_code]
        sec_yapildi = sum(1 for i in sec_items if kayit_map.get(i.item_code, ChecklistKayit()).durum == "Yapildi")
        sec_devam = sum(1 for i in sec_items if kayit_map.get(i.item_code, ChecklistKayit()).durum == "Devam Ediyor")
        sec_yapilmadi = len(sec_items) - sec_yapildi - sec_devam
        sec_onay = sum(1 for i in sec_items if kayit_map.get(i.item_code, ChecklistKayit()).onay_durumu == "Onaylandi")
        bolum_data.append({
            "Bolum": f"{sec_code}) {sec_name}",
            "Toplam": len(sec_items),
            "Yapildi": sec_yapildi,
            "Devam": sec_devam,
            "Yapilmadi": sec_yapilmadi,
            "Onayli": sec_onay,
        })
    if bolum_data:
        df = pd.DataFrame(bolum_data)
        st.markdown(ReportStyler.colored_table_html(df, "#1e40af"), unsafe_allow_html=True)

    # Sunburst grafik
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        styled_section("Bolum / Durum Dagilimi", "#4472C4")
        inner_data: dict[str, float] = {}
        outer_data: dict[str, list[tuple[str, float]]] = {}
        for sec_code, sec_name in BOLUM_KODLARI.items():
            sec_items_list = [i for i in aktif_items if i.section == sec_code]
            if not sec_items_list:
                continue
            inner_data[sec_name] = len(sec_items_list)
            subs = []
            for durum in CHECKLIST_DURUMLARI:
                cnt = sum(1 for i in sec_items_list if kayit_map.get(i.item_code, ChecklistKayit()).durum == durum)
                if cnt > 0:
                    subs.append((durum, cnt))
            if subs:
                outer_data[sec_name] = subs
        if inner_data:
            st.markdown(
                ReportStyler.sunburst_chart_svg(inner_data, outer_data, title="Bolum/Durum", size=175),
                unsafe_allow_html=True,
            )

    with col_g2:
        styled_section("Durum Dagilimi", "#ED7D31")
        bar_dict = {"Yapildi": yapildi, "Devam Ediyor": devam, "Yapilmadi": yapilmadi}
        st.markdown(ReportStyler.horizontal_bar_html(bar_dict, "#ED7D31"), unsafe_allow_html=True)

    # Risk ozeti
    risk_kayitlari = store.load_objects("risk_kayitlari")
    if risk_kayitlari:
        styled_section("Risk Özeti", "#ef4444")
        acik_risk = [r for r in risk_kayitlari if r.durum != "Kapandi"]
        kritik = sum(1 for r in acik_risk if r.seviye == "kritik")
        yuksek = sum(1 for r in acik_risk if r.seviye == "yuksek")
        orta = sum(1 for r in acik_risk if r.seviye == "orta")
        dusuk_c = sum(1 for r in acik_risk if r.seviye == "dusuk")
        styled_stat_row([
            ("Kritik", str(kritik), "#ef4444", "🔴"),
            ("Yuksek", str(yuksek), "#ED7D31", "🟠"),
            ("Orta", str(orta), "#FFC000", "🟡"),
            ("Dusuk", str(dusuk_c), "#10b981", "🟢"),
        ])


# ============================================================
# TAB 2: A) SIVIL SAVUNMA
# ============================================================

def _render_sivil_savunma(store: SSGDataStore):
    styled_section("A) Sivil Savunma", "#1e40af")

    sub_tabs = st.tabs(["☑️ Checklist", "🚨 Tatbikatlar", "👤 Sorumlu"])

    with sub_tabs[0]:
        _render_checklist_section(store, "A")

    with sub_tabs[1]:
        _render_tatbikatlar(store)

    with sub_tabs[2]:
        _render_sorumlu(store, "ss_sorumlusu")


def _render_checklist_section(store: SSGDataStore, section: str):
    """Belirli bir bolumun checklist maddelerini gosterir."""
    col_y, _ = st.columns([1, 3])
    with col_y:
        egitim_yili = st.selectbox("Egitim Yili", _edu_year_options(),
                                    index=_edu_year_options().index(_current_edu_year())
                                    if _current_edu_year() in _edu_year_options() else 0,
                                    key=f"ssg_cl_{section}_ey")

    items = [i for i in store.load_objects("checklist_items") if i.section == section and i.is_active]
    kayitlar = store.load_objects("checklist_kayitlari")
    kayit_map = {k.item_code: k for k in kayitlar if k.egitim_yili == egitim_yili}

    require_doc_ayar = store.get_ayar("require_document_on_done") == "1"

    if not items:
        styled_info_banner("Bu bolumde aktif checklist maddesi yok.", "info")
        return

    # Stat ozet
    yapildi_cnt = sum(1 for i in items if kayit_map.get(i.item_code, ChecklistKayit()).durum == "Yapildi")
    devam_cnt = sum(1 for i in items if kayit_map.get(i.item_code, ChecklistKayit()).durum == "Devam Ediyor")
    yapilmadi_cnt = len(items) - yapildi_cnt - devam_cnt
    styled_stat_row([
        ("Toplam", str(len(items)), "#2563eb", "📋"),
        ("Yapildi", str(yapildi_cnt), "#10b981", "✅"),
        ("Devam", str(devam_cnt), "#f59e0b", "🔄"),
        ("Yapilmadi", str(yapilmadi_cnt), "#ef4444", "❌"),
    ])

    # Her madde için expander
    for item in items:
        kayit = kayit_map.get(item.item_code)
        if not kayit:
            kayit = ChecklistKayit(item_code=item.item_code, egitim_yili=egitim_yili)

        durum_icon = {"Yapildi": "✅", "Devam Ediyor": "🔄", "Yapilmadi": "❌"}.get(kayit.durum, "❌")
        with st.expander(f"{durum_icon} {item.item_code} — {item.item_name}"):
            c1, c2 = st.columns(2)
            with c1:
                new_durum = st.selectbox("Durum", CHECKLIST_DURUMLARI,
                                          index=CHECKLIST_DURUMLARI.index(kayit.durum) if kayit.durum in CHECKLIST_DURUMLARI else 0,
                                          key=f"cl_dur_{section}_{item.item_code}")
            with c2:
                sorumlu = st.text_input("Sorumlu", value=kayit.sorumlu, key=f"cl_sor_{section}_{item.item_code}")

            c3, c4 = st.columns(2)
            with c3:
                hedef = st.date_input("Hedef Tarih",
                                       value=date.fromisoformat(kayit.hedef_tarih) if kayit.hedef_tarih else None,
                                       key=f"cl_ht_{section}_{item.item_code}")
            with c4:
                tam_tarih = st.date_input("Tamamlanma Tarihi",
                                           value=date.fromisoformat(kayit.tamamlanma_tarihi) if kayit.tamamlanma_tarihi else None,
                                           key=f"cl_tt_{section}_{item.item_code}")

            c5, c6 = st.columns(2)
            with c5:
                bakim = st.checkbox("Bakım Yapıldı", value=kayit.bakim_yapildi, key=f"cl_bkm_{section}_{item.item_code}")
            with c6:
                kontrol = st.checkbox("Kontrol Yapildi", value=kayit.kontrol_yapildi, key=f"cl_knt_{section}_{item.item_code}")

            # Onay
            onay_col1, onay_col2 = st.columns(2)
            with onay_col1:
                onay_d = st.selectbox("Onay Durumu", ONAY_DURUMLARI,
                                       index=ONAY_DURUMLARI.index(kayit.onay_durumu) if kayit.onay_durumu in ONAY_DURUMLARI else 0,
                                       key=f"cl_ond_{section}_{item.item_code}")
            with onay_col2:
                onaylayan = st.text_input("Onaylayan", value=kayit.onaylayan, key=f"cl_ony_{section}_{item.item_code}")

            notlar = st.text_area("Notlar", value=kayit.notlar, key=f"cl_not_{section}_{item.item_code}")

            # Evrak yukleme
            evrak_str = ", ".join(kayit.evraklar) if kayit.evraklar else "Evrak yok"
            st.caption(f"Mevcut evraklar: {evrak_str}")
            yeni_evrak = st.text_input("Yeni evrak adi ekle (virgul ile ayirin)",
                                        key=f"cl_evr_{section}_{item.item_code}")

            if st.button("Kaydet", key=f"cl_save_{section}_{item.item_code}", type="primary"):
                kayit.durum = new_durum
                kayit.sorumlu = sorumlu
                kayit.hedef_tarih = hedef.isoformat() if hedef else ""
                kayit.tamamlanma_tarihi = tam_tarih.isoformat() if tam_tarih else ""
                kayit.bakim_yapildi = bakim
                kayit.kontrol_yapildi = kontrol
                kayit.onay_durumu = onay_d
                kayit.onaylayan = onaylayan
                kayit.notlar = notlar

                if yeni_evrak:
                    for e in yeni_evrak.split(","):
                        e = e.strip()
                        if e and e not in kayit.evraklar:
                            kayit.evraklar.append(e)

                # Dogrulama
                if new_durum == "Yapildi":
                    ok, errors = ChecklistValidator.validate_status_change(
                        kayit, new_durum, require_doc_ayar
                    )
                    if not ok:
                        for err in errors:
                            st.warning(err)
                        st.stop()

                store.upsert("checklist_kayitlari", kayit)
                st.success(f"{item.item_code} kaydedildi.")
                st.rerun()


def _render_tatbikatlar(store: SSGDataStore):
    """Tatbikat planlari ve kayitlari."""
    styled_section("Tatbikat Planlari", "#4472C4")

    col_y, col_gen = st.columns([1, 1])
    with col_y:
        ey = st.selectbox("Egitim Yili", _edu_year_options(),
                           index=_edu_year_options().index(_current_edu_year())
                           if _current_edu_year() in _edu_year_options() else 0,
                           key="ssg_tat_ey")
    with col_gen:
        st.write("")
        st.write("")
        if st.button("Otomatik Plan Oluştur", key="ssg_tat_gen", type="primary"):
            cnt = TatbikatPlanner.generate_for_year(store, ey)
            st.success(f"{cnt} tatbikat planlandi.")
            st.rerun()

    # Planlari goster
    planlar = store.load_objects("tatbikat_planlari")
    for plan in planlar:
        st.markdown(
            f"**{plan.tatbikat_type}** — Aylar: {plan.months} | "
            f"Yıllık Adet: {plan.count_per_year} | "
            f"Zorunlu: {'Evet' if plan.is_required else 'Hayir'}"
        )

    st.divider()
    styled_section("Tatbikat Kayıtlari", "#ED7D31")

    kayitlar = store.load_objects("tatbikat_kayitlari")
    sorular = store.load_objects("tatbikat_checklist")

    if not kayitlar:
        styled_info_banner("Henuz tatbikat kaydi yok. Otomatik Plan Oluştur butonunu kullanin.", "info")

    for kayit in kayitlar:
        status_icon = "✅" if kayit.durum == "Tamamlandı" else "📅"
        with st.expander(f"{status_icon} {kayit.tatbikat_type} — {kayit.tarih} ({kayit.durum})"):
            c1, c2, c3 = st.columns(3)
            with c1:
                tarih = st.date_input("Tarih",
                                       value=date.fromisoformat(kayit.tarih) if kayit.tarih else date.today(),
                                       key=f"tat_tar_{kayit.id}")
            with c2:
                lokasyon = st.text_input("Lokasyon", value=kayit.lokasyon, key=f"tat_lok_{kayit.id}")
            with c3:
                katilimci = st.number_input("Katilimci Sayısı", min_value=0, value=kayit.katilimci_sayisi,
                                             key=f"tat_kat_{kayit.id}")

            sorumlu = st.text_input("Sorumlu", value=kayit.sorumlu, key=f"tat_sor_{kayit.id}")

            # Puanlama
            tip_sorular = [s for s in sorular if s.tatbikat_type == kayit.tatbikat_type]
            if tip_sorular:
                st.markdown("**Puanlama:**")
                for soru in tip_sorular:
                    mevcut = kayit.puanlar.get(soru.question_code, "Uygunsuz")
                    puan = st.selectbox(
                        f"{soru.question_code}: {soru.question_text}",
                        TATBIKAT_PUANLARI,
                        index=TATBIKAT_PUANLARI.index(mevcut) if mevcut in TATBIKAT_PUANLARI else 2,
                        key=f"tat_p_{kayit.id}_{soru.question_code}",
                    )
                    kayit.puanlar[soru.question_code] = puan

            durum = st.selectbox("Durum", ["Planlandi", "Tamamlandı"],
                                  index=1 if kayit.durum == "Tamamlandı" else 0,
                                  key=f"tat_dur_{kayit.id}")

            notlar = st.text_area("Notlar", value=kayit.notlar, key=f"tat_not_{kayit.id}")

            if st.button("Kaydet", key=f"tat_save_{kayit.id}", type="primary"):
                kayit.tarih = tarih.isoformat()
                kayit.lokasyon = lokasyon
                kayit.katilimci_sayisi = katilimci
                kayit.sorumlu = sorumlu
                kayit.durum = durum
                kayit.notlar = notlar

                if durum == "Tamamlandı" and tip_sorular:
                    kayit = TatbikatScorer.calculate_score(kayit, sorular)

                store.upsert("tatbikat_kayitlari", kayit)
                st.success("Tatbikat kaydedildi.")
                st.rerun()

            if kayit.durum == "Tamamlandı" and kayit.yuzde_skor > 0:
                st.markdown(
                    f"**Skor:** {kayit.toplam_skor} | **Yuzde:** %{kayit.yuzde_skor}"
                )


def _render_sorumlu(store: SSGDataStore, rol: str):
    """Sorumlu bilgisi goruntuleme/duzenleme."""
    rol_adi = SORUMLU_ROL_ADI.get(rol, rol)
    styled_section(rol_adi, "#8b5cf6")

    sorumlular = store.load_objects("sorumlular")
    sor = next((s for s in sorumlular if s.rol == rol), None)
    if not sor:
        sor = SSGSorumlu(rol=rol)

    var_mi = st.toggle(f"{rol_adi} Atanmis mi?", value=sor.var_mi, key=f"sor_var_{rol}")

    if var_mi:
        c1, c2 = st.columns(2)
        with c1:
            ad = st.text_input("Ad Soyad", value=sor.ad_soyad, key=f"sor_ad_{rol}")
            unvan = st.text_input("Unvan", value=sor.unvan, key=f"sor_unvan_{rol}")
        with c2:
            iletisim = st.text_input("İletişim (telefon/email)", value=sor.iletisim, key=f"sor_ilt_{rol}")
            belge = st.text_input("Belge/Sertifika", value=sor.belge_dosyasi, key=f"sor_blg_{rol}")

        gorev_evrak = st.text_input("Görevlendirme Evraki", value=sor.gorevlendirme_evrak, key=f"sor_gev_{rol}")

        if st.button("Kaydet", key=f"sor_save_{rol}", type="primary"):
            sor.var_mi = True
            sor.ad_soyad = ad
            sor.unvan = unvan
            sor.iletisim = iletisim
            sor.belge_dosyasi = belge
            sor.gorevlendirme_evrak = gorev_evrak
            store.upsert("sorumlular", sor)
            st.success(f"{rol_adi} bilgileri kaydedildi.")
            st.rerun()
    else:
        if sor.var_mi:
            sor.var_mi = False
            store.upsert("sorumlular", sor)
            st.rerun()
        styled_info_banner(f"{rol_adi} henuz atanmamis.", "warning")


# ============================================================
# TAB 3: B) ISG
# ============================================================

def _render_isg(store: SSGDataStore):
    styled_section("B) Is Sagligi ve Guvenligi", "#0d9488")

    sub_tabs = st.tabs(["⚠️ Risk Analizi", "🔍 Denetim", "🚧 Olay/Ramak Kala", "👷 İSG Uzmanı"])

    with sub_tabs[0]:
        _render_risk_analizi(store)
    with sub_tabs[1]:
        _render_denetim(store)
    with sub_tabs[2]:
        _render_olay_bolum(store, "B")
    with sub_tabs[3]:
        _render_sorumlu(store, "isg_uzmani")


def _render_risk_analizi(store: SSGDataStore):
    """Risk analizi kayitlari ve yeni risk ekleme."""
    styled_section("Risk Analizi", "#ef4444")

    risk_kayitlari = store.load_objects("risk_kayitlari")
    tehlikeler = store.load_objects("risk_tehlikeler")

    # Stat
    acik = [r for r in risk_kayitlari if r.durum != "Kapandi"]
    styled_stat_row([
        ("Toplam Risk", str(len(risk_kayitlari)), "#2563eb", "📊"),
        ("Açık", str(len(acik)), "#ef4444", "⚠️"),
        ("Kapandi", str(len(risk_kayitlari) - len(acik)), "#10b981", "✅"),
    ])

    # Risk matris (5x5)
    styled_section("Risk Matrisi (5x5)", "#4472C4")
    matris = [[0]*5 for _ in range(5)]
    for r in risk_kayitlari:
        if 1 <= r.olasilik <= 5 and 1 <= r.siddet <= 5:
            matris[r.olasilik - 1][r.siddet - 1] += 1

    matris_html = '<table style="border-collapse:collapse;margin:10px 0;width:100%;max-width:500px;">'
    matris_html += '<tr><th style="padding:8px;border:1px solid #e2e8f0;background:#1e40af;color:#fff;">O\\S</th>'
    for s in range(1, 6):
        matris_html += f'<th style="padding:8px;border:1px solid #e2e8f0;background:#1e40af;color:#fff;text-align:center;">{s}</th>'
    matris_html += '</tr>'

    for o in range(5, 0, -1):
        matris_html += f'<tr><td style="padding:8px;border:1px solid #e2e8f0;background:#1e40af;color:#fff;font-weight:700;text-align:center;">{o}</td>'
        for s in range(1, 6):
            skor = o * s
            _, seviye = RiskCalculator.calculate_score(o, s)
            color = RISK_SEVIYE_RENK.get(seviye, "#A5A5A5")
            cnt = matris[o - 1][s - 1]
            cell_text = f"{skor}" + (f"<br><b>{cnt}</b>" if cnt > 0 else "")
            matris_html += f'<td style="padding:8px;border:1px solid #e2e8f0;background:{color}20;text-align:center;font-size:12px;">{cell_text}</td>'
        matris_html += '</tr>'
    matris_html += '</table>'
    st.markdown(matris_html, unsafe_allow_html=True)
    st.caption("O = Olasilik, S = Siddet. Hucrelerdeki sayilar risk skor ve (mevcut risk adedi).")

    # Mevcut riskler
    styled_section("Risk Kayıtları")
    for risk in risk_kayitlari:
        seviye_icon = {"kritik": "🔴", "yuksek": "🟠", "orta": "🟡", "dusuk": "🟢"}.get(risk.seviye, "⚪")
        with st.expander(f"{seviye_icon} {risk.tehlike} — Skor: {risk.skor} ({risk.seviye.capitalize()}) [{risk.durum}]"):
            c1, c2 = st.columns(2)
            with c1:
                lokasyon = st.text_input("Lokasyon", value=risk.lokasyon, key=f"rsk_lok_{risk.id}")
                tehlike_txt = st.text_input("Tehlike", value=risk.tehlike, key=f"rsk_teh_{risk.id}")
                risk_tanimi = st.text_area("Risk Tanimi", value=risk.risk_tanimi, key=f"rsk_tan_{risk.id}")
            with c2:
                olasilik = st.slider("Olasilik", 1, 5, value=risk.olasilik, key=f"rsk_ola_{risk.id}")
                siddet = st.slider("Siddet", 1, 5, value=risk.siddet, key=f"rsk_sid_{risk.id}")
                skor, seviye = RiskCalculator.calculate_score(olasilik, siddet)
                st.markdown(f"**Skor:** {skor} | **Seviye:** {_risk_badge(seviye)}", unsafe_allow_html=True)

            mevcut_onlem = st.text_area("Mevcut Onlem", value=risk.mevcut_onlem, key=f"rsk_onl_{risk.id}")
            onerilen = st.text_area("Onerilen Aksiyon", value=risk.onerilen_aksiyon, key=f"rsk_aks_{risk.id}")

            c3, c4 = st.columns(2)
            with c3:
                r_sorumlu = st.text_input("Sorumlu", value=risk.sorumlu, key=f"rsk_sor_{risk.id}")
                r_durum = st.selectbox("Durum", RISK_AKSIYON_DURUMLARI,
                                        index=RISK_AKSIYON_DURUMLARI.index(risk.durum) if risk.durum in RISK_AKSIYON_DURUMLARI else 0,
                                        key=f"rsk_dur_{risk.id}")
            with c4:
                r_hedef = st.date_input("Hedef Tarih",
                                         value=date.fromisoformat(risk.hedef_tarih) if risk.hedef_tarih else None,
                                         key=f"rsk_ht_{risk.id}")

            if st.button("Güncelle", key=f"rsk_save_{risk.id}", type="primary"):
                risk.lokasyon = lokasyon
                risk.tehlike = tehlike_txt
                risk.risk_tanimi = risk_tanimi
                risk.olasilik = olasilik
                risk.siddet = siddet
                risk.skor = skor
                risk.seviye = seviye
                risk.mevcut_onlem = mevcut_onlem
                risk.onerilen_aksiyon = onerilen
                risk.sorumlu = r_sorumlu
                risk.hedef_tarih = r_hedef.isoformat() if r_hedef else ""
                risk.durum = r_durum
                store.upsert("risk_kayitlari", risk)
                st.success("Risk güncellendi.")
                st.rerun()

            if st.button("Sil", key=f"rsk_del_{risk.id}"):
                store.delete_by_id("risk_kayitlari", risk.id)
                st.success("Risk silindi.")
                st.rerun()

    # Yeni risk ekle
    styled_section("Yeni Risk Ekle", "#10b981")
    with st.form("new_risk_form"):
        nc1, nc2 = st.columns(2)
        with nc1:
            n_lokasyon = st.text_input("Lokasyon")

            tehlike_options = [t.hazard_name for t in tehlikeler]
            tehlike_options.append("Diger")
            n_tehlike_sec = st.selectbox("Tehlike Secin", tehlike_options)

            if n_tehlike_sec == "Diger":
                n_tehlike = st.text_input("Tehlike (el ile)")

            else:
                n_tehlike = n_tehlike_sec
            n_risk_tanimi = st.text_area("Risk Tanimi")

        with nc2:
            n_olasilik = st.slider("Olasilik", 1, 5, value=3)

            n_siddet = st.slider("Siddet", 1, 5, value=3)

            n_skor, n_seviye = RiskCalculator.calculate_score(n_olasilik, n_siddet)
            st.markdown(f"**Skor:** {n_skor} | **Seviye:** {_risk_badge(n_seviye)}", unsafe_allow_html=True)
            n_sorumlu = st.text_input("Sorumlu")

            n_hedef = st.date_input("Hedef Tarih")


        n_onlem = st.text_area("Mevcut Onlem")

        n_aksiyon = st.text_area("Onerilen Aksiyon")


        if st.form_submit_button("Risk Ekle", type="primary"):
            if not n_tehlike:
                st.warning("Tehlike alani zorunludur.")
            else:
                # hazard_code bul
                hz = next((t for t in tehlikeler if t.hazard_name == n_tehlike), None)
                h_code = hz.hazard_code if hz else ""
                new_risk = RiskKaydi(
                    hazard_code=h_code,
                    lokasyon=n_lokasyon,
                    tehlike=n_tehlike,
                    risk_tanimi=n_risk_tanimi,
                    olasilik=n_olasilik,
                    siddet=n_siddet,
                    skor=n_skor,
                    seviye=n_seviye,
                    mevcut_onlem=n_onlem,
                    onerilen_aksiyon=n_aksiyon,
                    sorumlu=n_sorumlu,
                    hedef_tarih=n_hedef.isoformat() if n_hedef else "",
                )
                store.upsert("risk_kayitlari", new_risk)
                st.success("Yeni risk eklendi.")
                st.rerun()


def _render_denetim(store: SSGDataStore):
    """ISG / OG Denetim kayitlari."""
    styled_section("Denetim Kayıtlari", "#4472C4")

    kayitlar = store.load_objects("denetim_kayitlari")

    styled_stat_row([
        ("Toplam Denetim", str(len(kayitlar)), "#2563eb", "📝"),
        ("Taslak", str(sum(1 for k in kayitlar if k.durum == "Taslak")), "#f59e0b", "📄"),
        ("Tamamlandı", str(sum(1 for k in kayitlar if k.durum == "Tamamlandı")), "#10b981", "✅"),
    ])

    for kayit in kayitlar:
        sablon = next((s for s in DEFAULT_DENETIM_SABLONLARI if s["template_code"] == kayit.template_code), None)
        sablon_adi = sablon["template_name"] if sablon else kayit.template_code
        with st.expander(f"📝 {sablon_adi} — {kayit.donem_ay}/{kayit.donem_yil} [{kayit.durum}]"):
            c1, c2, c3 = st.columns(3)
            with c1:
                denetci = st.text_input("Denetci", value=kayit.denetci, key=f"den_dnc_{kayit.id}")
            with c2:
                ay = st.number_input("Ay", 1, 12, value=kayit.donem_ay, key=f"den_ay_{kayit.id}")
            with c3:
                yil = st.number_input("Yil", 2020, 2030, value=kayit.donem_yil, key=f"den_yil_{kayit.id}")

            durum = st.selectbox("Durum", DENETIM_DURUMLARI,
                                  index=DENETIM_DURUMLARI.index(kayit.durum) if kayit.durum in DENETIM_DURUMLARI else 0,
                                  key=f"den_dur_{kayit.id}")

            # Bulgular
            bulgular_text = "\n".join(kayit.bulgular) if kayit.bulgular else ""
            bulgular_input = st.text_area("Bulgular (her satir bir bulgu)", value=bulgular_text, key=f"den_blg_{kayit.id}")

            notlar = st.text_area("Notlar", value=kayit.notlar, key=f"den_not_{kayit.id}")

            skor = st.number_input("Yuzde Skor", 0.0, 100.0, value=kayit.yuzde_skor, key=f"den_skor_{kayit.id}")

            if st.button("Kaydet", key=f"den_save_{kayit.id}", type="primary"):
                kayit.denetci = denetci
                kayit.donem_ay = ay
                kayit.donem_yil = yil
                kayit.durum = durum
                kayit.bulgular = [b.strip() for b in bulgular_input.split("\n") if b.strip()]
                kayit.notlar = notlar
                kayit.yuzde_skor = skor
                store.upsert("denetim_kayitlari", kayit)
                st.success("Denetim kaydedildi.")
                st.rerun()

    # Yeni denetim ekle
    styled_section("Yeni Denetim", "#10b981")
    with st.form("new_denetim_form"):
        sablon_options = [f"{s['template_code']} - {s['template_name']}" for s in DEFAULT_DENETIM_SABLONLARI]
        sablon_sec = st.selectbox("Sablon", sablon_options)

        template_code = sablon_sec.split(" - ")[0] if sablon_sec else ""

        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            n_denetci = st.text_input("Denetci")

        with dc2:
            n_ay = st.number_input("Ay", 1, 12, value=date.today().month)

        with dc3:
            n_yil = st.number_input("Yil", 2020, 2030, value=date.today().year)


        if st.form_submit_button("Denetim Oluştur", type="primary"):
            new_den = DenetimKaydi(
                template_code=template_code,
                donem_ay=n_ay,
                donem_yil=n_yil,
                denetci=n_denetci,
            )
            store.upsert("denetim_kayitlari", new_den)
            st.success("Yeni denetim oluşturuldu.")
            st.rerun()


def _render_olay_bolum(store: SSGDataStore, bolum: str):
    """Belirli bir bolumun olay kayitlarini gosterir."""
    bolum_adi = BOLUM_KODLARI.get(bolum, bolum)
    styled_section(f"Olay Kayıtları — {bolum_adi}", "#ef4444")

    olaylar = [o for o in store.load_objects("olay_kayitlari") if o.bolum == bolum]

    styled_stat_row([
        ("Toplam", str(len(olaylar)), "#2563eb", "📋"),
        ("Açık", str(sum(1 for o in olaylar if o.durum == "Açık")), "#ef4444", "🔴"),
        ("Inceleniyor", str(sum(1 for o in olaylar if o.durum == "Inceleniyor")), "#f59e0b", "🟡"),
        ("Kapandi", str(sum(1 for o in olaylar if o.durum == "Kapandi")), "#10b981", "🟢"),
    ])

    for olay in olaylar:
        icon = {"Açık": "🔴", "Inceleniyor": "🟡", "Kapandi": "🟢"}.get(olay.durum, "⚪")
        with st.expander(f"{icon} {olay.olay_no} — {olay.olay_tipi} ({olay.durum})"):
            c1, c2 = st.columns(2)
            with c1:
                tipi = st.selectbox("Olay Tipi", OLAY_TIPLERI,
                                     index=OLAY_TIPLERI.index(olay.olay_tipi) if olay.olay_tipi in OLAY_TIPLERI else 0,
                                     key=f"olay_tip_{olay.id}")
                tarih = st.date_input("Tarih",
                                       value=date.fromisoformat(olay.tarih) if olay.tarih else date.today(),
                                       key=f"olay_tar_{olay.id}")
                lokasyon = st.text_input("Lokasyon", value=olay.lokasyon, key=f"olay_lok_{olay.id}")
            with c2:
                siddet = st.text_input("Siddet", value=olay.siddet, key=f"olay_sid_{olay.id}")
                durum = st.selectbox("Durum", OLAY_DURUMLARI,
                                      index=OLAY_DURUMLARI.index(olay.durum) if olay.durum in OLAY_DURUMLARI else 0,
                                      key=f"olay_dur_{olay.id}")
                ilgili = st.text_input("Ilgili Kisiler", value=olay.ilgili_kisiler, key=f"olay_ilg_{olay.id}")

            aciklama = st.text_area("Açıklama", value=olay.aciklama, key=f"olay_ack_{olay.id}")
            onlem = st.text_area("Alinan Onlem", value=olay.onlem_alinan, key=f"olay_onl_{olay.id}")
            aksiyon = st.text_area("Aksiyon Plani", value=olay.aksiyon_plani, key=f"olay_aks_{olay.id}")

            # Onay
            oc1, oc2 = st.columns(2)
            with oc1:
                onay_d = st.selectbox("Onay Durumu", ONAY_DURUMLARI,
                                       index=ONAY_DURUMLARI.index(olay.onay_durumu) if olay.onay_durumu in ONAY_DURUMLARI else 0,
                                       key=f"olay_ond_{olay.id}")
            with oc2:
                onaylayan = st.text_input("Onaylayan", value=olay.onaylayan, key=f"olay_ony_{olay.id}")

            if st.button("Güncelle", key=f"olay_save_{olay.id}", type="primary"):
                olay.olay_tipi = tipi
                olay.tarih = tarih.isoformat()
                olay.lokasyon = lokasyon
                olay.siddet = siddet
                olay.durum = durum
                olay.ilgili_kisiler = ilgili
                olay.aciklama = aciklama
                olay.onlem_alinan = onlem
                olay.aksiyon_plani = aksiyon
                olay.onay_durumu = onay_d
                olay.onaylayan = onaylayan
                if onay_d == "Onaylandi":
                    olay.onay_tarihi = datetime.now().isoformat()
                store.upsert("olay_kayitlari", olay)
                st.success("Olay güncellendi.")
                st.rerun()

    # Yeni olay bildirimi
    styled_section("Yeni Olay Bildirimi", "#10b981")
    with st.form(f"new_olay_form_{bolum}"):
        oc1, oc2 = st.columns(2)
        with oc1:
            n_tipi = st.selectbox("Olay Tipi", OLAY_TIPLERI)

            n_tarih = st.date_input("Tarih", value=date.today())

            n_lokasyon = st.text_input("Lokasyon")

        with oc2:
            n_siddet = st.text_input("Siddet")

            n_ilgili = st.text_input("Ilgili Kisiler")


        n_aciklama = st.text_area("Açıklama")

        n_onlem = st.text_area("Alinan Onlem")


        if st.form_submit_button("Olay Bildir", type="primary"):
            if not n_aciklama:
                st.warning("Açıklama zorunludur.")
            else:
                new_olay = OlayKaydi(
                    olay_no=store.next_olay_no(),
                    olay_tipi=n_tipi,
                    bolum=bolum,
                    tarih=n_tarih.isoformat(),
                    lokasyon=n_lokasyon,
                    aciklama=n_aciklama,
                    ilgili_kisiler=n_ilgili,
                    siddet=n_siddet,
                    onlem_alinan=n_onlem,
                )
                store.upsert("olay_kayitlari", new_olay)
                st.success(f"Olay bildirimi oluşturuldu: {new_olay.olay_no}")
                st.rerun()


# ============================================================
# TAB 4: C) OKUL/OGRENCI GUVENLIGI
# ============================================================

def _render_okul_ogrenci(store: SSGDataStore):
    styled_section("C) Okul/Öğrenci Güvenliği", "#8b5cf6")

    sub_tabs = st.tabs([
        "🔐 Güvenlik Kontrolleri",
        "📢 Olay Bildirimi",
        "📋 Eylem Planı",
        "👤 OG Sorumlusu",
        "🤫 Anonim İhbar",
    ])

    with sub_tabs[0]:
        _render_checklist_section(store, "C")

    with sub_tabs[1]:
        _render_olay_bolum(store, "C")

    with sub_tabs[2]:
        _render_eylem_plani(store)

    with sub_tabs[3]:
        _render_sorumlu(store, "og_sorumlusu")

    with sub_tabs[4]:
        try:
            from views._ihbar_hatti import render_ihbar_gonder_panel, render_ihbar_inceleme_panel
            ihbar_tabs = st.tabs(["📨 İhbar Gönder (Herkes)", "🔐 İnceleme (Yetkili)"])
            with ihbar_tabs[0]:
                render_ihbar_gonder_panel()
            with ihbar_tabs[1]:
                render_ihbar_inceleme_panel()
        except ImportError:
            st.info("Anonim İhbar modülü yüklü değil.")
        except Exception as _e:
            st.error(f"İhbar hattı yüklenemedi: {_e}")


def _render_eylem_plani(store: SSGDataStore):
    """Akran zorbaligi eylem plani."""
    styled_section("Siddeti Engelleme ve Akran Zorbaligi Eylem Plani", "#8b5cf6")

    col_y, _ = st.columns([1, 3])
    with col_y:
        ey = st.selectbox("Egitim Yili", _edu_year_options(),
                           index=_edu_year_options().index(_current_edu_year())
                           if _current_edu_year() in _edu_year_options() else 0,
                           key="ssg_eylem_ey")

    planlar = store.load_objects("eylem_planlari")
    plan = next((p for p in planlar if p.egitim_yili == ey), None)

    if not plan:
        if st.button("Eylem Plani Oluştur", key="ssg_eylem_create", type="primary"):
            from models.sivil_savunma_isg import DEFAULT_EYLEM_PLANI
            maddeler = []
            for ep in DEFAULT_EYLEM_PLANI:
                maddeler.append({
                    "ay": ep.get("default_month", ""),
                    "eylem": ep.get("action_text", ""),
                    "sorumlu": ep.get("owner_role", ""),
                    "durum": "Planli",
                    "kanit": "",
                })
            new_plan = EylemPlani(
                plan_code="EYLEM-OG-01",
                egitim_yili=ey,
                maddeler=maddeler,
            )
            store.upsert("eylem_planlari", new_plan)
            st.success("Eylem plani oluşturuldu.")
            st.rerun()
        return

    # Plan durumu
    plan_acik = plan.durum == "Açık"
    st.markdown(
        f"**Plan Durumu:** {_durum_badge('Yapildi' if not plan_acik else 'Devam Ediyor')} "
        f"({'Açık — duzenleme yapilabiilir' if plan_acik else 'Kapali — kilitli'})",
        unsafe_allow_html=True,
    )

    if plan_acik:
        if st.button("Plani Kapat ve Kilitle", key="ssg_eylem_close"):
            plan.durum = "Kapali"
            store.upsert("eylem_planlari", plan)
            st.success("Plan kapatildi ve kilitlendi.")
            st.rerun()

    # Maddeler tablosu
    if plan.maddeler:
        for idx, madde in enumerate(plan.maddeler):
            with st.expander(f"📌 {madde.get('ay', '')} — {madde.get('eylem', '')[:50]}"):
                if plan_acik:
                    mc1, mc2 = st.columns(2)
                    with mc1:
                        m_ay = st.text_input("Ay", value=madde.get("ay", ""), key=f"ep_ay_{idx}")
                        m_eylem = st.text_input("Eylem", value=madde.get("eylem", ""), key=f"ep_eyl_{idx}")
                    with mc2:
                        m_sorumlu = st.text_input("Sorumlu", value=madde.get("sorumlu", ""), key=f"ep_sor_{idx}")
                        m_durum = st.selectbox("Durum", EYLEM_DURUMLARI,
                                                index=EYLEM_DURUMLARI.index(madde.get("durum", "Planli")) if madde.get("durum", "Planli") in EYLEM_DURUMLARI else 0,
                                                key=f"ep_dur_{idx}")
                    m_kanit = st.text_input("Kanit", value=madde.get("kanit", ""), key=f"ep_kan_{idx}")

                    if st.button("Madde Güncelle", key=f"ep_save_{idx}"):
                        plan.maddeler[idx] = {
                            "ay": m_ay, "eylem": m_eylem, "sorumlu": m_sorumlu,
                            "durum": m_durum, "kanit": m_kanit,
                        }
                        store.upsert("eylem_planlari", plan)
                        st.success("Madde güncellendi.")
                        st.rerun()
                else:
                    st.markdown(f"**Ay:** {madde.get('ay', '')} | **Sorumlu:** {madde.get('sorumlu', '')}")
                    st.markdown(f"**Durum:** {madde.get('durum', '')} | **Kanit:** {madde.get('kanit', '-')}")

    # Yeni madde ekle (plan acikken)
    if plan_acik:
        styled_section("Yeni Madde Ekle", "#10b981")
        with st.form("new_ep_madde"):
            ec1, ec2 = st.columns(2)
            with ec1:
                ne_ay = st.text_input("Ay")

                ne_eylem = st.text_input("Eylem")

            with ec2:
                ne_sorumlu = st.text_input("Sorumlu")


            if st.form_submit_button("Ekle", type="primary"):
                if ne_eylem:
                    plan.maddeler.append({
                        "ay": ne_ay, "eylem": ne_eylem, "sorumlu": ne_sorumlu,
                        "durum": "Planli", "kanit": "",
                    })
                    store.upsert("eylem_planlari", plan)
                    st.success("Madde eklendi.")
                    st.rerun()


# ============================================================
# TAB 5: OLAY KAYITLARI (tum bolumler)
# ============================================================

def _render_olay_kayitlari(store: SSGDataStore):
    styled_section("Tüm Olay Kayıtları", "#ef4444")

    olaylar = store.load_objects("olay_kayitlari")

    # Filtreler
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        f_bolum = st.selectbox("Bolum", ["Tümü"] + list(BOLUM_KODLARI.keys()), key="olay_f_bol")
    with fc2:
        f_tip = st.selectbox("Tip", ["Tümü"] + OLAY_TIPLERI, key="olay_f_tip")
    with fc3:
        f_durum = st.selectbox("Durum", ["Tümü"] + OLAY_DURUMLARI, key="olay_f_dur")
    with fc4:
        f_tarih = st.date_input("Tarihten itibaren", value=None, key="olay_f_tar")

    # Filtrele
    filtered = olaylar
    if f_bolum != "Tümü":
        filtered = [o for o in filtered if o.bolum == f_bolum]
    if f_tip != "Tümü":
        filtered = [o for o in filtered if o.olay_tipi == f_tip]
    if f_durum != "Tümü":
        filtered = [o for o in filtered if o.durum == f_durum]
    if f_tarih:
        f_tarih_str = f_tarih.isoformat()
        filtered = [o for o in filtered if o.tarih >= f_tarih_str]

    styled_stat_row([
        ("Toplam", str(len(filtered)), "#2563eb", "📋"),
        ("Açık", str(sum(1 for o in filtered if o.durum == "Açık")), "#ef4444", "🔴"),
        ("Inceleniyor", str(sum(1 for o in filtered if o.durum == "Inceleniyor")), "#f59e0b", "🟡"),
        ("Kapandi", str(sum(1 for o in filtered if o.durum == "Kapandi")), "#10b981", "🟢"),
    ])

    if not filtered:
        styled_info_banner("Filtrelere uyan olay bulunamadı.", "info")
        return

    # Tablo
    tablo_data = []
    for o in filtered:
        bolum_adi = BOLUM_KODLARI.get(o.bolum, o.bolum)
        tablo_data.append({
            "Olay No": o.olay_no,
            "Bolum": bolum_adi,
            "Tip": o.olay_tipi,
            "Tarih": o.tarih,
            "Lokasyon": o.lokasyon,
            "Durum": o.durum,
            "Onay": o.onay_durumu,
        })
    df = pd.DataFrame(tablo_data)
    st.markdown(ReportStyler.colored_table_html(df, "#ef4444"), unsafe_allow_html=True)

    # Detay expanderlar
    for olay in filtered:
        icon = {"Açık": "🔴", "Inceleniyor": "🟡", "Kapandi": "🟢"}.get(olay.durum, "⚪")
        with st.expander(f"{icon} {olay.olay_no} — {olay.olay_tipi}"):
            st.markdown(f"**Bolum:** {BOLUM_KODLARI.get(olay.bolum, olay.bolum)} | "
                        f"**Tarih:** {olay.tarih} | **Lokasyon:** {olay.lokasyon}")
            st.markdown(f"**Siddet:** {olay.siddet}")
            st.markdown(f"**Açıklama:** {olay.aciklama}")
            st.markdown(f"**Onlem:** {olay.onlem_alinan}")
            st.markdown(f"**Aksiyon:** {olay.aksiyon_plani}")
            st.markdown(
                f"**Durum:** {olay.durum} | **Onay:** {_onay_badge(olay.onay_durumu)}",
                unsafe_allow_html=True,
            )


# ============================================================
# TAB 6: RAPORLAR
# ============================================================

def _render_raporlar(store: SSGDataStore):
    styled_section("Raporlar", "#0B0F19")

    sub_tabs = st.tabs([
        "📊 Genel Özet",
        "🛡️ Sivil Savunma",
        "⚠️ ISG Risk Analizi",
        "🔍 ISG Denetim",
        "📋 Olay Raporları",
        "📝 Eylem Planı",
    ])

    with sub_tabs[0]:
        _render_rapor_genel(store)
    with sub_tabs[1]:
        _render_rapor_sivil_savunma(store)
    with sub_tabs[2]:
        _render_rapor_risk(store)
    with sub_tabs[3]:
        _render_rapor_denetim(store)
    with sub_tabs[4]:
        _render_rapor_olay(store)
    with sub_tabs[5]:
        _render_rapor_eylem(store)

    # ---- Performans Karsilastirma ----
    from utils.report_utils import (
        ai_recommendations_html, period_comparison_row_html,
        generate_module_pdf, render_pdf_download_button,
        render_report_kunye_html,
    )

    st.markdown(ReportStyler.section_divider_html("Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

    try:
        from datetime import timedelta
        now = datetime.now()
        current_month = now.strftime("%Y-%m")
        prev_month = (now.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

        olaylar = store.load_objects("olay_kayitlari")
        risk_kayitlari = store.load_objects("risk_kayitlari")
        denetim_kayitlari = store.load_objects("denetim_kayitlari")
        tatbikat_kayitlari = store.load_objects("tatbikat_kayitlari")

        def _ssg_count_by_month(items, date_field, month_str):
            count = 0
            for item in items:
                val = getattr(item, date_field, "") or ""
                if val.startswith(month_str):
                    count += 1
                elif not val and hasattr(item, "created_at"):
                    ca = getattr(item, "created_at", "") or ""
                    if ca[:7] == month_str:
                        count += 1
            return count

        def _ssg_count_denetim_by_month(items, month_str):
            count = 0
            try:
                y, m = month_str.split("-")
                y, m = int(y), int(m)
            except (ValueError, AttributeError):
                return 0
            for item in items:
                if getattr(item, "donem_yil", 0) == y and getattr(item, "donem_ay", 0) == m:
                    count += 1
            return count

        olay_cur = _ssg_count_by_month(olaylar, "tarih", current_month)
        olay_prev = _ssg_count_by_month(olaylar, "tarih", prev_month)
        risk_cur = _ssg_count_by_month(risk_kayitlari, "created_at", current_month)
        risk_prev = _ssg_count_by_month(risk_kayitlari, "created_at", prev_month)
        denetim_cur = _ssg_count_denetim_by_month(denetim_kayitlari, current_month)
        denetim_prev = _ssg_count_denetim_by_month(denetim_kayitlari, prev_month)

        comparisons = [
            {"label": "Olay Kaydı", "current": olay_cur, "previous": olay_prev},
            {"label": "Risk Değerlendirme", "current": risk_cur, "previous": risk_prev},
            {"label": "Denetim", "current": denetim_cur, "previous": denetim_prev},
        ]
        st.markdown(period_comparison_row_html(comparisons), unsafe_allow_html=True)
    except Exception:
        st.caption("Performans karsilastirma verisi yok.")

    # ---- AI Onerileri ----
    try:
        insights = []

        # 1) Geciken tatbikatlar
        tatbikat_planlari = store.load_objects("tatbikat_planlari")
        tamamlanan_tipler = {t.tatbikat_type for t in tatbikat_kayitlari if t.durum == "Tamamlandı"}
        eksik_tatbikat = [p.tatbikat_type for p in tatbikat_planlari
                          if p.is_required and p.tatbikat_type not in tamamlanan_tipler]
        if eksik_tatbikat:
            insights.append({
                "icon": "🚨", "title": "Eksik Tatbikatlar",
                "text": f"{len(eksik_tatbikat)} zorunlu tatbikat henuz tamamlanmadi: {', '.join(eksik_tatbikat[:3])}. Tatbikat planini kontrol edin.",
                "color": "#ef4444",
            })

        # 2) Yuksek riskli acik kalemler
        yuksek_risk = [r for r in risk_kayitlari if r.seviye in ("kritik", "yuksek") and r.durum == "Açık"]
        if yuksek_risk:
            insights.append({
                "icon": "⚠️", "title": "Yuksek Riskli Açık Kalemler",
                "text": f"{len(yuksek_risk)} adet kritik/yuksek seviye risk kalemi hala acik durumda. Öncelikli olarak aksiyona gecilmesi oneriliyor.",
                "color": "#f59e0b",
            })

        # 3) Tamamlanmamis denetimler
        taslak_denetim = [d for d in denetim_kayitlari if d.durum == "Taslak"]
        if taslak_denetim:
            insights.append({
                "icon": "📋", "title": "Taslak Denetimler",
                "text": f"{len(taslak_denetim)} adet denetim kaydi taslak asamasinda. Denetimleri tamamlayip onaya sunun.",
                "color": "#2563eb",
            })

        # 4) Acik olay kayitlari
        acik_olaylar = [o for o in olaylar if o.durum == "Açık"]
        if acik_olaylar:
            insights.append({
                "icon": "📝", "title": "Açık Olay Kayıtları",
                "text": f"{len(acik_olaylar)} adet olay kaydi henuz kapatilmamis. Olaylarin aksiyon planlari takip edilmelidir.",
                "color": "#8b5cf6",
            })

        # 5) Genel durum
        if not insights:
            insights.append({
                "icon": "✅", "title": "Genel Durum Iyi",
                "text": "Tüm tatbikatlar, denetimler ve risk takipleri guncel gorunuyor. Mevcut durum basarili.",
                "color": "#10b981",
            })

        st.markdown(ai_recommendations_html(insights), unsafe_allow_html=True)
    except Exception:
        pass

    # ---- Kurumsal Kunye ----
    st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

    # ---- PDF Export ----
    st.markdown(ReportStyler.section_divider_html("Toplu PDF Rapor", "#1e40af"), unsafe_allow_html=True)
    if st.button("📥 SSG Genel Raporu (PDF)", key="ssg_toplu_pdf_btn", use_container_width=True):
        try:
            sections = []
            # Ozet metrikler
            sections.append({
                "title": "Genel Özet",
                "metrics": [
                    ("Olay Kaydı", str(len(olaylar)), "#ef4444"),
                    ("Risk Kaydi", str(len(risk_kayitlari)), "#f59e0b"),
                    ("Denetim", str(len(denetim_kayitlari)), "#4472C4"),
                    ("Tatbikat", str(len(tatbikat_kayitlari)), "#10b981"),
                ],
                "text": f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            })

            # Risk dagilimi
            if risk_kayitlari:
                from collections import Counter as _C
                sev_c = _C(r.seviye for r in risk_kayitlari)
                bar_d = {s.capitalize(): float(sev_c.get(s, 0)) for s in ["kritik", "yuksek", "orta", "dusuk"] if sev_c.get(s, 0) > 0}
                sections.append({
                    "title": "Risk Seviye Dagilimi",
                    "bar_data": bar_d,
                    "bar_title": "Risk Seviyeleri",
                    "bar_color": "#ef4444",
                })

            # Olay tipleri
            if olaylar:
                from collections import Counter as _C2
                tip_c = _C2(o.olay_tipi for o in olaylar)
                sections.append({
                    "title": "Olay Tip Dagilimi",
                    "bar_data": dict(tip_c.most_common(10)),
                    "bar_title": "Olay Tipleri",
                    "bar_color": "#4472C4",
                })

            pdf_bytes = generate_module_pdf("SSG-01 Sivil Savunma, ISG Raporu", sections)
            render_pdf_download_button(pdf_bytes, "ssg_genel_rapor.pdf", "SSG Genel Raporu", "ssg_toplu_dl")
        except Exception as e:
            st.error(f"PDF olusturma hatasi: {e}")


def _render_rapor_genel(store: SSGDataStore):
    styled_section("Genel Özet Raporu", "#2563eb")

    col_y, _ = st.columns([1, 3])
    with col_y:
        ey = st.selectbox("Egitim Yili", _edu_year_options(),
                           index=_edu_year_options().index(_current_edu_year())
                           if _current_edu_year() in _edu_year_options() else 0,
                           key="ssg_rap_genel_ey")

    items = [i for i in store.load_objects("checklist_items") if i.is_active]
    kayitlar = store.load_objects("checklist_kayitlari")
    yil_kayit_map = {k.item_code: k for k in kayitlar if k.egitim_yili == ey}

    # Bolum bazli tablo
    bolum_data = []
    for sec_code, sec_name in BOLUM_KODLARI.items():
        sec_items = [i for i in items if i.section == sec_code]
        yapildi = sum(1 for i in sec_items if yil_kayit_map.get(i.item_code, ChecklistKayit()).durum == "Yapildi")
        devam = sum(1 for i in sec_items if yil_kayit_map.get(i.item_code, ChecklistKayit()).durum == "Devam Ediyor")
        yapilmadi = len(sec_items) - yapildi - devam
        yuzde = round(yapildi / len(sec_items) * 100, 1) if sec_items else 0
        bolum_data.append({
            "Bolum": f"{sec_code}) {sec_name}",
            "Toplam": len(sec_items),
            "Yapildi": yapildi,
            "Devam": devam,
            "Yapilmadi": yapilmadi,
            "Tamamlanma %": f"%{yuzde}",
        })

    df = pd.DataFrame(bolum_data)
    st.markdown(ReportStyler.colored_table_html(df, "#1e40af"), unsafe_allow_html=True)

    # Sunburst
    sb_inner: dict[str, float] = {}
    sb_outer: dict[str, list[tuple[str, float]]] = {}
    for sec_code, sec_name in BOLUM_KODLARI.items():
        sec_items = [i for i in items if i.section == sec_code]
        if not sec_items:
            continue
        sb_inner[sec_name] = len(sec_items)
        subs = []
        for d in CHECKLIST_DURUMLARI:
            cnt = sum(1 for i in sec_items if yil_kayit_map.get(i.item_code, ChecklistKayit()).durum == d)
            if cnt > 0:
                subs.append((d, cnt))
        if subs:
            sb_outer[sec_name] = subs
    if sb_inner:
        st.markdown(
            ReportStyler.sunburst_chart_svg(sb_inner, sb_outer, title="Bolum/Durum", size=280),
            unsafe_allow_html=True,
        )

    # PDF
    if st.button("PDF Indir", key="ssg_rap_genel_pdf", type="primary"):
        info = get_institution_info()
        pdf = ReportPDFGenerator(f"SSG-01 Genel Özet — {ey}", info.get("name", ""))
        pdf.add_table("Bolum Bazli Özet", df)
        pdf_bytes = pdf.generate()
        st.download_button("PDF Indir", data=pdf_bytes, file_name=f"SSG01_Genel_Özet_{ey}.pdf",
                           mime="application/pdf", key="ssg_rap_genel_dl")


def _render_rapor_sivil_savunma(store: SSGDataStore):
    styled_section("Sivil Savunma Raporu", "#1e40af")

    items = [i for i in store.load_objects("checklist_items") if i.section == "A" and i.is_active]
    kayitlar = store.load_objects("checklist_kayitlari")

    col_y, _ = st.columns([1, 3])
    with col_y:
        ey = st.selectbox("Egitim Yili", _edu_year_options(),
                           index=_edu_year_options().index(_current_edu_year())
                           if _current_edu_year() in _edu_year_options() else 0,
                           key="ssg_rap_ss_ey")

    kayit_map = {k.item_code: k for k in kayitlar if k.egitim_yili == ey}

    tablo_data = []
    for item in items:
        k = kayit_map.get(item.item_code, ChecklistKayit())
        tablo_data.append({
            "Kod": item.item_code,
            "Madde": item.item_name[:60],
            "Durum": k.durum,
            "Bakım": "Evet" if k.bakim_yapildi else "-",
            "Kontrol": "Evet" if k.kontrol_yapildi else "-",
            "Onay": k.onay_durumu,
            "Evrak": len(k.evraklar),
        })
    df = pd.DataFrame(tablo_data)
    st.markdown(ReportStyler.colored_table_html(df, "#1e40af"), unsafe_allow_html=True)

    # Tatbikat ozeti
    tatbikatlar = store.load_objects("tatbikat_kayitlari")
    tamamlanan = [t for t in tatbikatlar if t.durum == "Tamamlandı"]
    if tamamlanan:
        styled_section("Tatbikat Özeti", "#4472C4")
        tat_data = []
        for t in tamamlanan:
            tat_data.append({
                "Tip": t.tatbikat_type,
                "Tarih": t.tarih,
                "Lokasyon": t.lokasyon,
                "Katilimci": t.katilimci_sayisi,
                "Skor %": t.yuzde_skor,
            })
        df_tat = pd.DataFrame(tat_data)
        st.markdown(ReportStyler.colored_table_html(df_tat, "#4472C4", "Skor %"), unsafe_allow_html=True)

    # PDF
    if st.button("PDF Indir", key="ssg_rap_ss_pdf", type="primary"):
        info = get_institution_info()
        pdf = ReportPDFGenerator(f"Sivil Savunma Raporu — {ey}", info.get("name", ""))
        pdf.add_table("A) Sivil Savunma Checklist", df)
        if tamamlanan:
            pdf.add_table("Tatbikat Özeti", df_tat)
        pdf_bytes = pdf.generate()
        st.download_button("PDF Indir", data=pdf_bytes, file_name=f"SSG01_SivilSavunma_{ey}.pdf",
                           mime="application/pdf", key="ssg_rap_ss_dl")


def _render_rapor_risk(store: SSGDataStore):
    styled_section("ISG Risk Analizi Raporu", "#ef4444")

    risk_kayitlari = store.load_objects("risk_kayitlari")

    if not risk_kayitlari:
        styled_info_banner("Henuz risk kaydi yok.", "info")
        return

    # Risk dagilimi
    seviye_counter = Counter(r.seviye for r in risk_kayitlari)
    bar_dict_r: dict[str, float] = {}
    for sev in ["kritik", "yuksek", "orta", "dusuk"]:
        cnt = seviye_counter.get(sev, 0)
        if cnt > 0:
            bar_dict_r[sev.capitalize()] = cnt

    if bar_dict_r:
        st.markdown(ReportStyler.horizontal_bar_html(bar_dict_r, "#ef4444"), unsafe_allow_html=True)

    # Tablo
    tablo_data = []
    for r in risk_kayitlari:
        tablo_data.append({
            "Lokasyon": r.lokasyon,
            "Tehlike": r.tehlike,
            "O": r.olasilik,
            "S": r.siddet,
            "Skor": r.skor,
            "Seviye": r.seviye.capitalize(),
            "Durum": r.durum,
            "Sorumlu": r.sorumlu,
        })
    df = pd.DataFrame(tablo_data)
    st.markdown(ReportStyler.colored_table_html(df, "#ef4444"), unsafe_allow_html=True)

    # Sunburst: Lokasyon/Seviye
    sb_inner_r: dict[str, float] = {}
    sb_outer_r: dict[str, list[tuple[str, float]]] = {}
    loc_groups: dict[str, list[str]] = {}
    for r in risk_kayitlari:
        loc = r.lokasyon or "Belirtilmemis"
        if loc not in loc_groups:
            loc_groups[loc] = []
        loc_groups[loc].append(r.seviye)

    for loc, seviyes in loc_groups.items():
        sb_inner_r[loc] = len(seviyes)
        sev_counter = Counter(seviyes)
        subs = [(sev.capitalize(), cnt) for sev, cnt in sev_counter.items()]
        if subs:
            sb_outer_r[loc] = subs

    if sb_inner_r:
        st.markdown(
            ReportStyler.sunburst_chart_svg(sb_inner_r, sb_outer_r, title="Lokasyon/Seviye", size=175),
            unsafe_allow_html=True,
        )

    # PDF
    if st.button("PDF Indir", key="ssg_rap_risk_pdf", type="primary"):
        info = get_institution_info()
        pdf = ReportPDFGenerator("ISG Risk Analizi Raporu", info.get("name", ""))
        pdf.add_table("Risk Kayıtları", df)
        pdf_bytes = pdf.generate()
        st.download_button("PDF Indir", data=pdf_bytes, file_name="SSG01_RiskAnalizi.pdf",
                           mime="application/pdf", key="ssg_rap_risk_dl")


def _render_rapor_denetim(store: SSGDataStore):
    styled_section("ISG Denetim Raporu", "#4472C4")

    kayitlar = store.load_objects("denetim_kayitlari")

    if not kayitlar:
        styled_info_banner("Henuz denetim kaydi yok.", "info")
        return

    tablo_data = []
    for k in kayitlar:
        sablon = next((s for s in DEFAULT_DENETIM_SABLONLARI if s["template_code"] == k.template_code), None)
        sablon_adi = sablon["template_name"] if sablon else k.template_code
        tablo_data.append({
            "Sablon": sablon_adi,
            "Donem": f"{k.donem_ay}/{k.donem_yil}",
            "Denetci": k.denetci,
            "Skor %": k.yuzde_skor,
            "Durum": k.durum,
            "Bulgu Sayısı": len(k.bulgular),
        })
    df = pd.DataFrame(tablo_data)
    st.markdown(ReportStyler.colored_table_html(df, "#4472C4", "Skor %"), unsafe_allow_html=True)

    # PDF
    if st.button("PDF Indir", key="ssg_rap_den_pdf", type="primary"):
        info = get_institution_info()
        pdf = ReportPDFGenerator("ISG Denetim Raporu", info.get("name", ""))
        pdf.add_table("Denetim Kayıtlari", df)
        pdf_bytes = pdf.generate()
        st.download_button("PDF Indir", data=pdf_bytes, file_name="SSG01_Denetim.pdf",
                           mime="application/pdf", key="ssg_rap_den_dl")


def _render_rapor_olay(store: SSGDataStore):
    styled_section("Olay Raporlari", "#ef4444")

    olaylar = store.load_objects("olay_kayitlari")

    if not olaylar:
        styled_info_banner("Henuz olay kaydi yok.", "info")
        return

    # Istatistikler
    tip_counter = Counter(o.olay_tipi for o in olaylar)
    durum_counter = Counter(o.durum for o in olaylar)
    bolum_counter = Counter(BOLUM_KODLARI.get(o.bolum, o.bolum) for o in olaylar)

    col1, col2 = st.columns(2)
    with col1:
        styled_section("Tip Dagilimi", "#4472C4")
        bar_dict_tip = dict(tip_counter.most_common())
        if bar_dict_tip:
            st.markdown(ReportStyler.horizontal_bar_html(bar_dict_tip, "#4472C4"), unsafe_allow_html=True)

    with col2:
        styled_section("Bolum Dagilimi", "#ED7D31")
        bar_dict_bol = dict(bolum_counter.most_common())
        if bar_dict_bol:
            st.markdown(ReportStyler.horizontal_bar_html(bar_dict_bol, "#ED7D31"), unsafe_allow_html=True)

    # Tablo
    tablo_data = []
    for o in olaylar:
        tablo_data.append({
            "Olay No": o.olay_no,
            "Bolum": BOLUM_KODLARI.get(o.bolum, o.bolum),
            "Tip": o.olay_tipi,
            "Tarih": o.tarih,
            "Durum": o.durum,
            "Onay": o.onay_durumu,
        })
    df = pd.DataFrame(tablo_data)
    st.markdown(ReportStyler.colored_table_html(df, "#ef4444"), unsafe_allow_html=True)

    # PDF
    if st.button("PDF Indir", key="ssg_rap_olay_pdf", type="primary"):
        info = get_institution_info()
        pdf = ReportPDFGenerator("Olay Raporlari", info.get("name", ""))
        pdf.add_table("Olay Kayıtları", df)
        pdf_bytes = pdf.generate()
        st.download_button("PDF Indir", data=pdf_bytes, file_name="SSG01_Olaylar.pdf",
                           mime="application/pdf", key="ssg_rap_olay_dl")


def _render_rapor_eylem(store: SSGDataStore):
    styled_section("Eylem Plani Raporu", "#8b5cf6")

    col_y, _ = st.columns([1, 3])
    with col_y:
        ey = st.selectbox("Egitim Yili", _edu_year_options(),
                           index=_edu_year_options().index(_current_edu_year())
                           if _current_edu_year() in _edu_year_options() else 0,
                           key="ssg_rap_eylem_ey")

    planlar = store.load_objects("eylem_planlari")
    plan = next((p for p in planlar if p.egitim_yili == ey), None)

    if not plan or not plan.maddeler:
        styled_info_banner(f"{ey} için eylem plani bulunamadı.", "info")
        return

    st.markdown(f"**Plan Durumu:** {plan.durum}")

    tablo_data = []
    for madde in plan.maddeler:
        tablo_data.append({
            "Ay": madde.get("ay", ""),
            "Eylem": madde.get("eylem", ""),
            "Sorumlu": madde.get("sorumlu", ""),
            "Durum": madde.get("durum", ""),
            "Kanit": "Var" if madde.get("kanit", "") else "-",
        })
    df = pd.DataFrame(tablo_data)
    st.markdown(ReportStyler.colored_table_html(df, "#8b5cf6"), unsafe_allow_html=True)

    # Stat
    tamamlanan = sum(1 for m in plan.maddeler if m.get("durum") == "Tamamlandı")
    styled_stat_row([
        ("Toplam Madde", str(len(plan.maddeler)), "#8b5cf6", "📋"),
        ("Tamamlandı", str(tamamlanan), "#10b981", "✅"),
        ("Tamamlanma %", f"%{round(tamamlanan / len(plan.maddeler) * 100, 1) if plan.maddeler else 0}", "#4472C4", "📊"),
    ])

    # PDF
    if st.button("PDF Indir", key="ssg_rap_eylem_pdf", type="primary"):
        info = get_institution_info()
        pdf = ReportPDFGenerator(f"Eylem Plani Raporu — {ey}", info.get("name", ""))
        pdf.add_table("Akran Zorbaligi Eylem Plani", df)
        pdf_bytes = pdf.generate()
        st.download_button("PDF Indir", data=pdf_bytes, file_name=f"SSG01_EylemPlani_{ey}.pdf",
                           mime="application/pdf", key="ssg_rap_eylem_dl")


# ============================================================
# TAB 7: AYARLAR
# ============================================================

def _render_ayarlar(store: SSGDataStore):
    styled_section("Ayarlar", "#0B0F19")

    sub_tabs = st.tabs(["⚙️ Genel Ayarlar", "☑️ Checklist Maddeleri", "🚨 Tatbikat Ayarları", "👥 Onay Rolleri"])

    with sub_tabs[0]:
        _render_ayar_genel(store)
    with sub_tabs[1]:
        _render_ayar_checklist(store)
    with sub_tabs[2]:
        _render_ayar_tatbikat(store)
    with sub_tabs[3]:
        _render_ayar_roller(store)


def _render_ayar_genel(store: SSGDataStore):
    styled_section("Genel Ayarlar", "#2563eb")

    ayarlar = store.load_objects("ayarlar")

    for ayar in ayarlar:
        with st.expander(f"⚙️ {ayar.ayar_kodu} — {ayar.aciklama}"):
            new_val = st.text_input("Deger", value=ayar.deger, key=f"ayar_val_{ayar.ayar_kodu}")

            if st.button("Kaydet", key=f"ayar_save_{ayar.ayar_kodu}"):
                ayar.deger = new_val
                store.upsert("ayarlar", ayar)
                st.success(f"{ayar.ayar_kodu} güncellendi.")
                st.rerun()


def _render_ayar_checklist(store: SSGDataStore):
    styled_section("Checklist Maddeleri", "#4472C4")

    items = store.load_objects("checklist_items")

    # Bolum filtre
    f_bolum = st.selectbox("Bolum Filtre", ["Tümü"] + list(BOLUM_KODLARI.keys()), key="ayar_cl_bol")
    if f_bolum != "Tümü":
        items = [i for i in items if i.section == f_bolum]

    for item in items:
        aktif_icon = "🟢" if item.is_active else "🔴"
        with st.expander(f"{aktif_icon} {item.item_code} — {item.item_name}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Bolum:** {item.section} | **Kategori:** {item.category}")
                st.markdown(f"**Periyot:** {item.frequency_type}")
            with c2:
                st.markdown(f"**Evrak Zorunlu:** {'Evet' if item.requires_document else 'Hayir'}")
                st.markdown(f"**Onay Zorunlu:** {'Evet' if item.requires_approval else 'Hayir'}")

            new_active = st.toggle("Aktif", value=item.is_active, key=f"ayar_ci_akt_{item.item_code}")

            if new_active != item.is_active:
                item.is_active = new_active
                store.upsert("checklist_items", item)
                st.success(f"{item.item_code} {'aktif' if new_active else 'pasif'} yapildi.")
                st.rerun()


def _render_ayar_tatbikat(store: SSGDataStore):
    styled_section("Tatbikat Ayarlari", "#ED7D31")

    planlar = store.load_objects("tatbikat_planlari")

    for plan in planlar:
        with st.expander(f"📅 {plan.plan_code} — {plan.tatbikat_type}"):
            st.markdown(f"**Aylar:** {plan.months} | **Yıllık Adet:** {plan.count_per_year}")
            st.markdown(f"**Zorunlu:** {'Evet' if plan.is_required else 'Hayir'}")

    styled_section("Tatbikat Checklist Sorulari")

    sorular = store.load_objects("tatbikat_checklist")
    for soru in sorular:
        st.markdown(
            f"- **{soru.question_code}** ({soru.tatbikat_type}): {soru.question_text} "
            f"[Agirlik: {soru.weight}]"
        )


def _render_ayar_roller(store: SSGDataStore):
    styled_section("Onay Rolleri", "#8b5cf6")

    roller_ayar = store.get_ayar("approval_roles")
    roller = [r.strip() for r in roller_ayar.split(";") if r.strip()] if roller_ayar else ONAY_ROLLER

    st.markdown("Mevcut onay rolleri:")
    for rol in roller:
        st.markdown(f"- {rol}")

    new_roles = st.text_input("Rolleri duzenle (noktalı virgul ile ayirin)", value=";".join(roller),
                               key="ayar_roller_input")

    if st.button("Kaydet", key="ayar_roller_save", type="primary"):
        ayar = store.get_by_field("ayarlar", "ayar_kodu", "approval_roles")
        if ayar:
            ayar.deger = new_roles
            store.upsert("ayarlar", ayar)
        else:
            new_ayar = SSGAyar(ayar_kodu="approval_roles", deger=new_roles,
                                aciklama="Onay atabilen roller")
            store.upsert("ayarlar", new_ayar)
        st.success("Roller güncellendi.")
        st.rerun()
