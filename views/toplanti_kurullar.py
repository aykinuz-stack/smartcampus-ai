"""
TOP-01 Toplanti ve Kurullar/Komisyonlar Modulu - Streamlit UI
==============================================================
Dashboard, Toplantı Yönetimi, Katilimci & Ajanda,
Kararlar & Aksiyonlar, Raporlar, Şablonlar ve Ayarlar.
"""

from __future__ import annotations

import os
from datetime import datetime, date, timedelta
from collections import Counter

import streamlit as st
import pandas as pd

from utils.tenant import get_tenant_dir
from utils.report_utils import ReportStyler, ReportPDFGenerator, get_institution_info, CHART_PALETTE
from utils.shared_data import load_shared_staff
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("toplanti")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("toplanti",
        "Toplanti planlama, kurul yonetimi, gundem, karar takibi, tutanak",
        [("5", "Kurul"), ("PDF", "Tutanak"), ("AI", "Ozet")])
except Exception:
    pass
from models.toplanti_kurullar import (
    ToplantiDataStore,
    MeetingType, Meeting, MeetingParticipant, AgendaItem,
    DecisionAction, MeetingAttachment, AgendaTemplate, MeetingGorev,
    KurulKomisyon,
    MeetingCodeGenerator, StatusManager, DecisionTracker,
    TOPLANTI_KATEGORILERI, TOPLANTI_DURUMLARI, DURUM_LABEL, DURUM_RENK,
    KATILIM_DURUMLARI, KATILIM_LABEL,
    KARAR_DURUMLARI, KARAR_LABEL, KARAR_RENK,
    ONCELIK_SEVIYELERI, ONCELIK_LABEL, ONCELIK_RENK,
    GOREV_DURUMLARI, GOREV_LABEL, GOREV_RENK,
    TEKRAR_TIPLERI, TEKRAR_LABEL,
    AJANDA_MADDE_TIPLERI, AJANDA_MADDE_LABEL,
    TOPLANTI_SONUCLARI, SONUC_LABEL, SONUC_RENK,
    KADEME_SECENEKLERI,
    KURUL_TUR_LABEL,
    ORGANIZATOR_ROLLER,
    STATUS_TRANSITIONS,
    DEFAULT_DYNAMIC_FIELD_DEFS,
)


# ============================================================
# STORE INIT
# ============================================================

def _get_top_store() -> ToplantiDataStore:
    base = os.path.join(get_tenant_dir(), "toplanti")
    store = ToplantiDataStore(base)
    _pop_key = "top01_defaults_populated"
    if _pop_key not in st.session_state:
        store.auto_populate_defaults()
        st.session_state[_pop_key] = True
    return store


# ============================================================
# CSS & STYLED HELPERS
# ============================================================

def _inject_top_css():
    inject_common_css("top")
    st.markdown("""
    <style>
    :root {
        --top-primary: #2563eb;
        --top-primary-dark: #1e40af;
        --top-success: #10b981;
        --top-warning: #f59e0b;
        --top-danger: #ef4444;
        --top-purple: #8b5cf6;
        --top-teal: #0d9488;
        --top-dark: #0B0F19;
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


def _inject_css():
    pass  # Tab styling now handled by inject_common_css in _inject_top_css


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
    return [f"{y}-{y + 1}" for y in range(current - 2, current + 2)]


def _durum_badge(durum: str) -> str:
    color = DURUM_RENK.get(durum, "#94a3b8")
    label = DURUM_LABEL.get(durum, durum)
    return (
        f'<span style="background:{color};color:#fff;padding:3px 10px;'
        f'border-radius:12px;font-size:11px;font-weight:700;">{label}</span>'
    )


def _karar_badge(durum: str) -> str:
    color = KARAR_RENK.get(durum, "#94a3b8")
    label = KARAR_LABEL.get(durum, durum)
    return (
        f'<span style="background:{color};color:#fff;padding:3px 10px;'
        f'border-radius:12px;font-size:11px;font-weight:700;">{label}</span>'
    )


def _gorev_badge(durum: str) -> str:
    color = GOREV_RENK.get(durum, "#94a3b8")
    label = GOREV_LABEL.get(durum, durum)
    return (
        f'<span style="background:{color};color:#fff;padding:3px 10px;'
        f'border-radius:12px;font-size:11px;font-weight:700;">{label}</span>'
    )


def _oncelik_badge(oncelik: str) -> str:
    color = ONCELIK_RENK.get(oncelik, "#94a3b8")
    label = ONCELIK_LABEL.get(oncelik, oncelik)
    return (
        f'<span style="background:{color};color:#fff;padding:3px 10px;'
        f'border-radius:12px;font-size:11px;font-weight:700;">{label}</span>'
    )


def _kategori_label(cat: str) -> str:
    return TOPLANTI_KATEGORILERI.get(cat, cat)


def _meeting_type_name(store: ToplantiDataStore, type_code: str) -> str:
    mt = store.get_by_field("meeting_types", "type_code", type_code)
    return mt.name if mt else type_code


def _select_meeting(store: ToplantiDataStore, key: str, label: str = "Toplanti Sec"):
    """Toplanti secici helper - string tabanlı selectbox ile Meeting objesi dondurur."""
    meetings = store.load_objects("meetings")
    if not meetings:
        styled_info_banner("Henuz toplanti kaydi bulunmuyor.", "info")
        return None
    meetings.sort(key=lambda x: x.tarih or "", reverse=True)
    labels = [
        f"{m.meeting_code} - {m.baslik or _meeting_type_name(store, m.type_code)} ({m.tarih})"
        for m in meetings
    ]
    sel_label = st.selectbox(label, labels, key=key)
    sel_idx = labels.index(sel_label) if sel_label in labels else 0
    return meetings[sel_idx]


# ============================================================
# MAIN RENDER
# ============================================================

def render_toplanti_kurullar():
    _inject_top_css()
    _inject_css()
    styled_header(
        "Toplanti ve Kurullar / Komisyonlar",
        "TOP-01 — Planlama, Katilimci, Ajanda, Karar Takibi ve Raporlama",
        icon="🏛️",
    )

    store = _get_top_store()

    render_smarti_welcome("toplanti_kurullar")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("toplanti_kurullar_egitim_yili")

    # -- Tab Gruplama (13 tab -> 2 grup) --
    _GRP_68433 = {
        "📋 Grup A": [("📊 Dashboard", 0), ("📅 Toplantı Yönetimi", 1), ("🎙️ Toplantı Yürütme", 2), ("📈 Raporlar", 3), ("📋 Şablonlar", 4), ("⚙️ Ayarlar", 5), ("💰 Verimlilik", 6)],
        "📊 Grup B": [("🎯 Karar Takip", 7), ("🧠 Hafıza", 8), ("🎛️ Komuta Merkezi", 9), ("📋 AI Hazırlık", 10), ("🛡️ Kurul Uyum", 11), ("🤖 Smarti", 12)],
    }
    _sg_68433 = st.radio("", list(_GRP_68433.keys()), horizontal=True, label_visibility="collapsed", key="rg_68433")
    _gt_68433 = _GRP_68433[_sg_68433]
    _aktif_idx_68433 = set(t[1] for t in _gt_68433)
    _tab_names_68433 = [t[0] for t in _gt_68433]
    tabs = st.tabs(_tab_names_68433)
    _tab_real_68433 = {idx: t for idx, t in zip((t[1] for t in _gt_68433), tabs)}

    if 0 in _aktif_idx_68433:
      with _tab_real_68433[0]:
        _render_dashboard(store)
    if 1 in _aktif_idx_68433:
      with _tab_real_68433[1]:
        _render_toplanti_yonetimi(store)
    if 2 in _aktif_idx_68433:
      with _tab_real_68433[2]:
        _render_katilimci_ajanda(store)
    if 3 in _aktif_idx_68433:
      with _tab_real_68433[3]:
        _render_raporlar(store)
    if 4 in _aktif_idx_68433:
      with _tab_real_68433[4]:
        _render_sablonlar(store)
    if 5 in _aktif_idx_68433:
      with _tab_real_68433[5]:
        _render_ayarlar(store)

    # SUPER: Verimlilik Motoru + Maliyet
    if 6 in _aktif_idx_68433:
      with _tab_real_68433[6]:
        try:
            from views._top_zirve import render_verimlilik_motoru
            render_verimlilik_motoru(store)
        except Exception as _e:
            st.error(f"Verimlilik Motoru yuklenemedi: {_e}")

    # SUPER: Karar & Aksiyon Takip Merkezi
    if 7 in _aktif_idx_68433:
      with _tab_real_68433[7]:
        try:
            from views._top_zirve import render_karar_takip
            render_karar_takip(store)
        except Exception as _e:
            st.error(f"Karar Takip yuklenemedi: {_e}")

    # SUPER: Zaman Makinesi + AI Hafiza
    if 8 in _aktif_idx_68433:
      with _tab_real_68433[8]:
        try:
            from views._top_zirve import render_toplanti_hafiza
            render_toplanti_hafiza(store)
        except Exception as _e:
            st.error(f"Toplanti Hafiza yuklenemedi: {_e}")

    # MEGA: Komuta Merkezi
    if 9 in _aktif_idx_68433:
      with _tab_real_68433[9]:
        try:
            from views._top_mega import render_toplanti_komuta
            render_toplanti_komuta(store)
        except Exception as _e:
            st.error(f"Komuta Merkezi yuklenemedi: {_e}")

    # MEGA: AI Hazirlik Asistani
    if 10 in _aktif_idx_68433:
      with _tab_real_68433[10]:
        try:
            from views._top_mega import render_ai_hazirlik
            render_ai_hazirlik(store)
        except Exception as _e:
            st.error(f"AI Hazirlik yuklenemedi: {_e}")

    # MEGA: Kurul Uyum Radari
    if 11 in _aktif_idx_68433:
      with _tab_real_68433[11]:
        try:
            from views._top_mega import render_kurul_uyum
            render_kurul_uyum(store)
        except Exception as _e:
            st.error(f"Kurul Uyum yuklenemedi: {_e}")

    if 12 in _aktif_idx_68433:
      with _tab_real_68433[12]:
        def _top_smarti_context():
            try:
                s = _get_top_store()
                toplanti_count = len(s.load_objects("meetings"))
                karar_count = len(s.load_objects("decisions"))
                aksiyon_count = len(s.load_objects("gorevler"))
                return (
                    f"Toplanti kaydi: {toplanti_count}, Karar kaydi: {karar_count}, "
                    f"Aksiyon kaydi: {aksiyon_count}"
                )
            except Exception:
                return ""
        render_smarti_chat("toplanti_kurullar", _top_smarti_context)


# ============================================================
# TAB 1: DASHBOARD
# ============================================================

def _render_dashboard(store: ToplantiDataStore):
    styled_section("Genel Bakis", "#0B0F19")

    col_y, _ = st.columns([1, 3])
    with col_y:
        ey_options = _edu_year_options()
        current_ey = _current_edu_year()
        idx = ey_options.index(current_ey) if current_ey in ey_options else 0
        egitim_yili = st.selectbox("Egitim Yili", ey_options, index=idx, key="top_dash_ey")

    meetings = store.load_objects("meetings")
    yil_meetings = [m for m in meetings if m.egitim_yili == egitim_yili]
    decisions = store.load_objects("decisions")
    today_str = date.today().isoformat()

    toplam = len(yil_meetings)
    bu_ay = sum(1 for m in yil_meetings if m.tarih and m.tarih[:7] == date.today().strftime("%Y-%m"))
    acik_karar = sum(1 for d in decisions if d.durum in ("ACIK", "DEVAM_EDIYOR"))
    geciken = sum(1 for d in decisions if d.durum in ("ACIK", "DEVAM_EDIYOR") and d.hedef_tarih and d.hedef_tarih < today_str)

    styled_stat_row([
        ("Toplam Toplanti", str(toplam), "#2563eb", "📋"),
        ("Bu Ay", str(bu_ay), "#10b981", "📅"),
        ("Açık Karar", str(acik_karar), "#f59e0b", "📝"),
        ("Geciken Aksiyon", str(geciken), "#ef4444", "⚠️"),
    ])

    st.markdown("---")

    # Kategori dagilimi - sunburst
    col1, col2 = st.columns(2)
    with col1:
        styled_section("Kategori Dagilimi", "#2563eb")
        inner_data: dict[str, float] = {}
        outer_data: dict[str, list[tuple[str, float]]] = {}
        for m in yil_meetings:
            cat_label = _kategori_label(m.category)
            inner_data[cat_label] = inner_data.get(cat_label, 0) + 1
            type_name = _meeting_type_name(store, m.type_code)
            if cat_label not in outer_data:
                outer_data[cat_label] = []
            found = False
            for i, (tn, cnt) in enumerate(outer_data[cat_label]):
                if tn == type_name:
                    outer_data[cat_label][i] = (type_name, cnt + 1)
                    found = True
                    break
            if not found:
                outer_data[cat_label].append((type_name, 1))
        if inner_data:
            st.markdown(
                ReportStyler.sunburst_chart_svg(inner_data, outer_data, title="Kategori / Tip", size=280),
                unsafe_allow_html=True,
            )
        else:
            styled_info_banner("Henuz toplanti kaydi bulunmuyor.", "info")

    with col2:
        styled_section("Durum Dagilimi", "#8b5cf6")
        durum_data: dict[str, float] = {}
        for m in yil_meetings:
            label = DURUM_LABEL.get(m.durum, m.durum)
            durum_data[label] = durum_data.get(label, 0) + 1
        if durum_data:
            durum_colors = [DURUM_RENK.get(d, "#94a3b8") for d in TOPLANTI_DURUMLARI if DURUM_LABEL.get(d) in durum_data]
            st.markdown(
                ReportStyler.donut_chart_svg(durum_data, colors=durum_colors, size=155),
                unsafe_allow_html=True,
            )
        else:
            styled_info_banner("Durum verisi bulunmuyor.", "info")

    st.markdown("---")

    # Yaklasan toplantilar
    styled_section("Yaklasan Toplantilar (7 Gün)", "#0d9488")
    yaklasan = [
        m for m in meetings
        if m.tarih and m.durum in ("TASLAK", "DAVET_GONDERILDI")
        and today_str <= m.tarih <= (date.today() + timedelta(days=7)).isoformat()
    ]
    if yaklasan:
        rows = []
        for m in sorted(yaklasan, key=lambda x: x.tarih):
            rows.append({
                "Kod": m.meeting_code,
                "Toplanti": m.baslik or _meeting_type_name(store, m.type_code),
                "Tarih": m.tarih,
                "Saat": m.saat_baslangic,
                "Lokasyon": m.lokasyon,
                "Durum": DURUM_LABEL.get(m.durum, m.durum),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        styled_info_banner("Yaklasan toplanti bulunmuyor.", "success")

    # Geciken aksiyonlar
    if geciken > 0:
        styled_section("Geciken Aksiyonlar", "#ef4444")
        overdue = DecisionTracker.get_overdue(store)
        # Show priority badges above the table
        for d in overdue[:10]:
            st.markdown(
                f'{_oncelik_badge(d.oncelik)} **{d.decision_no}** — {d.sorumlu}: '
                f'{(d.aksiyon_tanimi or d.karar_metni)[:60]}',
                unsafe_allow_html=True)
        rows = []
        for d in overdue[:10]:
            rows.append({
                "Karar No": d.decision_no,
                "Aksiyon": d.aksiyon_tanimi[:60] if d.aksiyon_tanimi else d.karar_metni[:60],
                "Sorumlu": d.sorumlu,
                "Hedef Tarih": d.hedef_tarih,
                "Öncelik": ONCELIK_LABEL.get(d.oncelik, d.oncelik),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ============================================================
# TAB 2: TOPLANTI YONETIMI
# ============================================================

def _render_toplanti_yonetimi(store: ToplantiDataStore):
    sub_tabs = st.tabs(["📋 Toplantı Listesi", "➕ Yeni Toplantı", "🔍 Toplantı Detay"])

    with sub_tabs[0]:
        _render_toplanti_listesi(store)
    with sub_tabs[1]:
        _render_yeni_toplanti(store)
    with sub_tabs[2]:
        _render_toplanti_detay(store)


def _render_toplanti_listesi(store: ToplantiDataStore):
    styled_section("Toplantı Listesi", "#2563eb")

    col1, col2, col3 = st.columns(3)
    with col1:
        kat_filter = st.selectbox("Kategori", ["Tümü"] + list(TOPLANTI_KATEGORILERI.values()), key="top_list_kat")
    with col2:
        durum_filter = st.selectbox("Durum", ["Tümü"] + [DURUM_LABEL[d] for d in TOPLANTI_DURUMLARI], key="top_list_dur")
    with col3:
        ey_filter = st.selectbox("Egitim Yili", ["Tümü"] + _edu_year_options(), key="top_list_ey")

    meetings = store.load_objects("meetings")

    if kat_filter != "Tümü":
        kat_code = [k for k, v in TOPLANTI_KATEGORILERI.items() if v == kat_filter]
        if kat_code:
            meetings = [m for m in meetings if m.category == kat_code[0]]
    if durum_filter != "Tümü":
        durum_code = [k for k, v in DURUM_LABEL.items() if v == durum_filter]
        if durum_code:
            meetings = [m for m in meetings if m.durum == durum_code[0]]
    if ey_filter != "Tümü":
        meetings = [m for m in meetings if m.egitim_yili == ey_filter]

    meetings.sort(key=lambda x: x.tarih or "", reverse=True)

    if not meetings:
        styled_info_banner("Filtrelerinize uygun toplanti bulunamadı.", "info")
        return

    rows = []
    for m in meetings:
        rows.append({
            "Kod": m.meeting_code,
            "Tip": _meeting_type_name(store, m.type_code),
            "Başlık": m.baslik or "-",
            "Tarih": m.tarih,
            "Kategori": _kategori_label(m.category),
            "Durum": DURUM_LABEL.get(m.durum, m.durum),
            "Organizator": m.organizator,
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.caption(f"Toplam {len(rows)} toplanti listelendi.")


def _get_organizator_options(store: ToplantiDataStore) -> list[str]:
    """Organizator rol listesini dondurur. Kullanici eklenmis roller dahil."""
    base = list(ORGANIZATOR_ROLLER)
    # Mevcut toplantilardaki ozel organizatorleri de ekle
    meetings = store.load_list("meetings")
    for m in meetings:
        org = m.get("organizator", "")
        if org and org not in base:
            base.append(org)
    return base


def _render_yeni_toplanti(store: ToplantiDataStore):
    styled_section("Yeni Toplantı Oluştur", "#10b981")

    # Basari mesajini goster (onceki form gonderiminden)
    if st.session_state.get("top_new_success"):
        styled_info_banner(st.session_state.pop("top_new_success"), "success")

    meeting_types = store.load_objects("meeting_types")
    active_types = [mt for mt in meeting_types if mt.is_active]

    if not active_types:
        styled_info_banner("Aktif toplanti tipi bulunamadı. Ayarlar sekmesinden varsayilan verileri yukleyin.", "warning")
        return

    # 1) Kategori secimi (+ Kurul/Komisyon)
    kat_keys = sorted(set(mt.category for mt in active_types))
    kat_labels = [_kategori_label(k) for k in kat_keys]
    kat_labels_full = kat_labels + ["Kurul / Komisyon"]
    sel_kat_label = st.selectbox("Toplanti Kategorisi", kat_labels_full, key="top_new_kat")

    # Kurul/Komisyon secildiyse
    selected_kurul = None
    if sel_kat_label == "Kurul / Komisyon":
        kurullar = store.load_objects("kurullar")
        aktif_kurullar = [k for k in kurullar if k.is_active]
        if not aktif_kurullar:
            styled_info_banner("Aktif kurul/komisyon bulunamadı. Kurul & Komisyonlar sekmesinden ekleyin.", "info")
            return
        kk_labels = [f"{k.ad} ({KURUL_TUR_LABEL.get(k.tur, k.tur)})" for k in aktif_kurullar]
        sel_kk_label = st.selectbox("Kurul / Komisyon Sec", kk_labels, key="top_new_kurul")
        sel_kk_idx = kk_labels.index(sel_kk_label) if sel_kk_label in kk_labels else 0
        selected_kurul = aktif_kurullar[sel_kk_idx]

        # Kurul secildiginde varsayilan bir meeting type kullan
        filtered_types = [mt for mt in active_types if mt.type_code == "AK-TOP"]
        if not filtered_types:
            filtered_types = active_types[:1]
        selected_type = filtered_types[0]
        selected_kat = selected_type.category
    else:
        sel_kat_idx = kat_labels.index(sel_kat_label) if sel_kat_label in kat_labels else 0
        selected_kat = kat_keys[sel_kat_idx]

        # 2) Toplanti tipi (kategoriye gore filtrelenmis)
        filtered_types = [mt for mt in active_types if mt.category == selected_kat]
        if not filtered_types:
            styled_info_banner("Bu kategoride aktif toplanti tipi yok.", "info")
            return

        type_names = [mt.name for mt in filtered_types]
        sel_type_name = st.selectbox("Toplanti Tipi", type_names, key="top_new_type")
        sel_type_idx = type_names.index(sel_type_name) if sel_type_name in type_names else 0
        selected_type = filtered_types[sel_type_idx]

    # 3) Kademe secimi
    kademe = st.selectbox("Kademe", KADEME_SECENEKLERI, key="top_new_kademe")

    # 4) Toplanti Sorumlusu
    org_options = _get_organizator_options(store)
    col_org1, col_org2 = st.columns([3, 2])
    with col_org1:
        organizator = st.selectbox("Toplantiyi Yapan (Sorumlu)", org_options, key="top_new_org")
    with col_org2:
        yeni_org = st.text_input("veya Yeni Ekle", key="top_new_org_custom",
                                  placeholder="Yeni rol/kisi yazin...")

    # 4) Tarih ve saat
    col1, col2, col3 = st.columns(3)
    with col1:
        tarih = st.date_input("Toplanti Tarihi", value=date.today(), key="top_new_tarih")
    with col2:
        saat_bas = st.time_input("Başlangıç Saati", key="top_new_saat_bas")
    with col3:
        saat_bit = st.time_input("Bitis Saati", key="top_new_saat_bit")

    # 5) Lokasyon
    lokasyon = st.text_input("Toplanti Yeri", key="top_new_lok")

    # 6) Gündem
    gundem = st.text_area("Toplanti Gündemi", key="top_new_gundem", height=120,
                           placeholder="Toplantida gorusulecek konulari yaziniz...")

    # 7) Katilimcilar (Kurum Aktif Calisanlarindan)
    staff_list = load_shared_staff()
    staff_options = []
    _staff_map: dict[str, dict] = {}
    for s in staff_list:
        tam_ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
        if not tam_ad:
            continue
        unvan = s.get("unvan", "")
        brans = s.get("brans", "")
        label = f"{tam_ad} - {unvan}" if unvan else (f"{tam_ad} - {brans}" if brans else tam_ad)
        staff_options.append(label)
        _staff_map[label] = s

    secili_katilimcilar = st.multiselect(
        "Katilimcilar (Kurum Çalışanları)",
        staff_options,
        key="top_new_katilimci",
        placeholder="Katilimci secin...",
    )
    ek_katilimcilar = st.text_input(
        "Ek Katilimci (listede olmayan, virgul ile ayirin)",
        key="top_new_ek_katilimci",
        placeholder="Ornek: Ali Veli - Dis Misafir, Ayse Demir - Veli",
    )

    # 8) Egitim yili
    ey_opts = _edu_year_options()
    current_ey = _current_edu_year()
    ey_idx = ey_opts.index(current_ey) if current_ey in ey_opts else 0
    egitim_yili = st.selectbox("Egitim Yili", ey_opts, index=ey_idx, key="top_new_ey")

    # 9) Dinamik alanlar (tipe gore)
    dynamic_values = {}
    if selected_type.dynamic_fields:
        st.markdown("**Ek Bilgiler**")
        for field_code in selected_type.dynamic_fields:
            field_def = next((f for f in DEFAULT_DYNAMIC_FIELD_DEFS if f["field_code"] == field_code), None)
            if not field_def:
                continue
            if field_def["field_type"] == "select" and field_def.get("options"):
                dynamic_values[field_code] = st.selectbox(
                    field_def["field_name"], field_def["options"],
                    key=f"top_dyn_{field_code}",
                )
            elif field_def["field_type"] == "multiselect" and field_def.get("options"):
                dynamic_values[field_code] = st.multiselect(
                    field_def["field_name"], field_def["options"],
                    key=f"top_dyn_{field_code}",
                )
            else:
                dynamic_values[field_code] = st.text_input(
                    field_def["field_name"], key=f"top_dyn_{field_code}",
                )

    notlar = st.text_area("Notlar (opsiyonel)", key="top_new_not", height=60)

    sablon_yukle = st.checkbox("Sablondan ajanda maddelerini otomatik yukle", value=True, key="top_new_sablon")

    st.markdown("---")
    if st.button("Toplanti Oluştur", type="primary", key="top_new_submit"):
        try:
            final_org = yeni_org.strip() if yeni_org.strip() else organizator
            meeting_code = MeetingCodeGenerator.generate_code(store, selected_type.type_code, egitim_yili)
            # Kurul/komisyon secildiyse baslik ve organizator kuruldan
            toplanti_baslik = selected_type.name
            if selected_kurul:
                toplanti_baslik = f"{selected_kurul.ad} Toplantisi"
                if selected_kurul.baskan and not yeni_org.strip():
                    final_org = selected_kurul.baskan
            new_meeting = Meeting(
                meeting_code=meeting_code,
                type_code=selected_type.type_code,
                category=selected_type.category,
                kademe=kademe,
                baslik=toplanti_baslik,
                tarih=tarih.isoformat(),
                saat_baslangic=saat_bas.strftime("%H:%M"),
                saat_bitis=saat_bit.strftime("%H:%M"),
                lokasyon=lokasyon,
                organizator=final_org,
                durum="TASLAK",
                tekrar_tipi=selected_type.default_frequency,
                egitim_yili=egitim_yili,
                gundem=gundem.strip(),
                notlar=notlar.strip(),
                dynamic_field_values=dynamic_values,
            )
            store.upsert("meetings", new_meeting)

            # Sablondan ajanda yukle
            if sablon_yukle:
                template = store.get_by_field("templates", "type_code", selected_type.type_code)
                if template and template.maddeler:
                    for madde in template.maddeler:
                        aj = AgendaItem(
                            meeting_id=new_meeting.id,
                            sira_no=madde.get("sira", 1),
                            madde_tipi=madde.get("tip", "BILGILENDIRME"),
                            baslik=madde.get("baslik", ""),
                            sure_dk=madde.get("sure_dk", 10),
                        )
                        store.upsert("agenda_items", aj)

            # Katilimcilari ekle (kurum calisanlarindan)
            for label in secili_katilimcilar:
                s = _staff_map.get(label, {})
                tam_ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip() if s else label.split(" - ")[0]
                unvan = s.get("unvan", "") or s.get("brans", "") if s else ""
                p = MeetingParticipant(
                    meeting_id=new_meeting.id,
                    ad_soyad=tam_ad,
                    rol=unvan,
                    gorev=s.get("category", "") if s else "",
                    katilim_durumu="DAVETLI",
                )
                store.upsert("participants", p)

            # Kurul/komisyon uyeleri otomatik ekle
            if selected_kurul:
                eklenen_adlar = {p.ad_soyad for p in store.find_by_field("participants", "meeting_id", new_meeting.id)}
                # Baskan
                if selected_kurul.baskan and selected_kurul.baskan not in eklenen_adlar:
                    p = MeetingParticipant(
                        meeting_id=new_meeting.id,
                        ad_soyad=selected_kurul.baskan,
                        rol=selected_kurul.baskan_unvan or "Baskan",
                        katilim_durumu="DAVETLI",
                    )
                    store.upsert("participants", p)
                    eklenen_adlar.add(selected_kurul.baskan)
                # Uyeler
                for uye in (selected_kurul.uyeler or []):
                    ad = uye.get("ad_soyad", "")
                    if ad and ad not in eklenen_adlar:
                        p = MeetingParticipant(
                            meeting_id=new_meeting.id,
                            ad_soyad=ad,
                            rol=uye.get("unvan", ""),
                            katilim_durumu="DAVETLI",
                        )
                        store.upsert("participants", p)
                        eklenen_adlar.add(ad)

            # Ek katilimcilar (manuel)
            if ek_katilimcilar.strip():
                for part in ek_katilimcilar.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    pieces = part.split(" - ", 1)
                    ad = pieces[0].strip()
                    rol = pieces[1].strip() if len(pieces) > 1 else ""
                    p = MeetingParticipant(
                        meeting_id=new_meeting.id,
                        ad_soyad=ad,
                        rol=rol,
                        katilim_durumu="DAVETLI",
                    )
                    store.upsert("participants", p)

            st.session_state["top_new_success"] = f"Toplanti basariyla oluşturuldu: {meeting_code}"
            st.rerun()
        except Exception as e:
            st.error(f"Toplanti olusturulurken hata: {e}")


def _render_toplanti_detay(store: ToplantiDataStore):
    styled_section("Toplanti Detay & İşlemler", "#8b5cf6")

    selected = _select_meeting(store, "top_detay_sec")
    if not selected:
        return

    # Ozet bilgiler
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Kod:** {selected.meeting_code}")
        st.markdown(f"**Tip:** {_meeting_type_name(store, selected.type_code)}")
        st.markdown(f"**Kategori:** {_kategori_label(selected.category)}")
    with col2:
        st.markdown(f"**Tarih:** {selected.tarih}")
        st.markdown(f"**Saat:** {selected.saat_baslangic} - {selected.saat_bitis}")
        st.markdown(f"**Lokasyon:** {selected.lokasyon}")
    with col3:
        st.markdown(f"**Sorumlu:** {selected.organizator}")
        st.markdown(f"**Durum:** {_durum_badge(selected.durum)}", unsafe_allow_html=True)
        st.markdown(f"**Egitim Yili:** {selected.egitim_yili}")

    # Gündem
    if selected.gundem:
        st.markdown(f"**Gündem:** {selected.gundem}")

    # Erteleme bilgisi
    if selected.ertelendi_mi and selected.eski_tarih:
        styled_info_banner(
            f"Bu toplanti ertelendi. Eski tarih: {selected.eski_tarih} {selected.eski_saat} | Not: {selected.erteleme_notu}",
            "warning",
        )

    # Iptal bilgisi
    if selected.iptal_mi:
        styled_info_banner("Bu toplanti iptal edilmistir.", "error")

    # Dinamik alan degerleri
    if selected.dynamic_field_values:
        st.markdown("**Ek Bilgiler:**")
        for fc, val in selected.dynamic_field_values.items():
            field_def = next((f for f in DEFAULT_DYNAMIC_FIELD_DEFS if f["field_code"] == fc), None)
            label = field_def["field_name"] if field_def else fc
            display_val = ", ".join(val) if isinstance(val, list) else str(val)
            st.markdown(f"- {label}: {display_val}")

    st.markdown("---")

    # Durum gecisi
    allowed = StatusManager.get_allowed_transitions(selected.durum)
    normal_transitions = [t for t in allowed if t not in ("IPTAL", "ERTELENDI")]
    special_actions = [t for t in allowed if t in ("IPTAL", "ERTELENDI")]

    if normal_transitions:
        st.markdown("**Durum Gecisi:**")
        cols = st.columns(len(normal_transitions))
        for i, target in enumerate(normal_transitions):
            with cols[i]:
                if st.button(DURUM_LABEL.get(target, target), key=f"top_trans_{selected.id}_{target}"):
                    selected.durum = target
                    if target == "ONAYLANDI":
                        selected.onay_tarihi = date.today().isoformat()
                    store.upsert("meetings", selected)
                    st.success(f"Durum güncellendi: {DURUM_LABEL.get(target, target)}")
                    st.rerun()

    # Iptal ve Erteleme islemleri
    if special_actions:
        st.markdown("---")
        col_act1, col_act2 = st.columns(2)

        if "IPTAL" in special_actions:
            with col_act1:
                with st.expander("Toplanti Iptal Et"):
                    iptal_notu = st.text_input("Iptal Nedeni", key=f"top_iptal_not_{selected.id}")
                    if st.button("Iptal Et", key=f"top_iptal_{selected.id}", type="primary"):
                        selected.durum = "IPTAL"
                        selected.iptal_mi = True
                        selected.notlar = f"{selected.notlar}\n[IPTAL] {iptal_notu}".strip()
                        store.upsert("meetings", selected)
                        st.success("Toplanti iptal edildi.")
                        st.rerun()

        if "ERTELENDI" in special_actions:
            with col_act2:
                with st.expander("Toplanti Ertele"):
                    yeni_tarih = st.date_input("Yeni Tarih", value=date.today(), key=f"top_ert_tarih_{selected.id}")
                    yeni_saat = st.time_input("Yeni Başlangıç Saati", key=f"top_ert_saat_{selected.id}")
                    yeni_saat_bit = st.time_input("Yeni Bitis Saati", key=f"top_ert_saat_bit_{selected.id}")
                    erteleme_notu = st.text_input("Erteleme Nedeni", key=f"top_ert_not_{selected.id}")
                    if st.button("Ertele", key=f"top_ertele_{selected.id}", type="primary"):
                        selected.eski_tarih = selected.tarih
                        selected.eski_saat = selected.saat_baslangic
                        selected.tarih = yeni_tarih.isoformat()
                        selected.saat_baslangic = yeni_saat.strftime("%H:%M")
                        selected.saat_bitis = yeni_saat_bit.strftime("%H:%M")
                        selected.durum = "ERTELENDI"
                        selected.ertelendi_mi = True
                        selected.erteleme_notu = erteleme_notu
                        store.upsert("meetings", selected)
                        st.success(f"Toplanti {yeni_tarih.isoformat()} tarihine ertelendi.")
                        st.rerun()

    # Tutanak
    if selected.durum in ("YAPILDI", "TUTANAK_TAMAM", "ONAYLANDI", "ARSIV"):
        st.markdown("---")
        styled_section("Tutanak", "#0d9488")
        tutanak = st.text_area("Tutanak Metni", value=selected.tutanak_metni, key=f"top_tut_{selected.id}", height=200)
        if st.button("Tutanagi Kaydet", key=f"top_tut_save_{selected.id}"):
            selected.tutanak_metni = tutanak
            store.upsert("meetings", selected)
            st.success("Tutanak kaydedildi.")


# ============================================================
# TAB 3: TOPLANTI YURUTME
# ============================================================

def _render_katilimci_ajanda(store: ToplantiDataStore):
    """Toplanti yurutme akisi: Sec -> Baslat -> Yoklama/Ajanda/Tutanak -> Kararlar -> Sonuclandir."""
    styled_section("Toplantı Yürütme", "#0B0F19")

    # Basari mesajlari
    if st.session_state.get("top_yrt_success"):
        styled_info_banner(st.session_state.pop("top_yrt_success"), "success")

    # 1) Toplanti secimi (sadece baslatilabilir/devam eden toplantilar)
    meetings = store.load_objects("meetings")
    eligible = [m for m in meetings if m.durum in ("TASLAK", "DAVET_GONDERILDI", "YAPILDI")]
    eligible.sort(key=lambda x: x.tarih or "", reverse=True)

    if not eligible:
        styled_info_banner(
            "Baslatilabilir veya devam eden toplanti bulunmuyor. "
            "Toplantı Yönetimi sekmesinden yeni toplanti olusturun.",
            "info",
        )
        return

    labels = [
        f"{m.meeting_code} - {m.baslik or _meeting_type_name(store, m.type_code)} ({m.tarih}) [{DURUM_LABEL.get(m.durum, m.durum)}]"
        for m in eligible
    ]
    sel_label = st.selectbox("Toplanti Sec", labels, key="top_yrt_sec")
    sel_idx = labels.index(sel_label) if sel_label in labels else 0
    selected = eligible[sel_idx]

    # 2) Toplanti bilgi ozeti
    st.markdown("---")
    col_i1, col_i2, col_i3 = st.columns(3)
    with col_i1:
        st.markdown(f"**Kod:** {selected.meeting_code}")
        st.markdown(f"**Tip:** {_meeting_type_name(store, selected.type_code)}")
    with col_i2:
        st.markdown(f"**Tarih:** {selected.tarih}")
        st.markdown(f"**Saat:** {selected.saat_baslangic} - {selected.saat_bitis}")
    with col_i3:
        st.markdown(f"**Lokasyon:** {selected.lokasyon}")
        st.markdown(f"**Durum:** {_durum_badge(selected.durum)}", unsafe_allow_html=True)

    if selected.gundem:
        st.markdown(f"**Gündem:** {selected.gundem}")

    # 3) Toplanti henuz baslamadiysa -> Baslat butonu
    if selected.durum in ("TASLAK", "DAVET_GONDERILDI"):
        st.markdown("---")
        styled_info_banner(
            "Toplanti henuz baslatilmadi. Baslatmak için asagidaki butonu kullanin.",
            "warning",
        )
        if st.button("Toplantiyi Baslat", type="primary", key="top_yrt_baslat"):
            selected.durum = "YAPILDI"
            store.upsert("meetings", selected)
            st.session_state["top_yrt_success"] = f"{selected.meeting_code} toplantisi baslatildi."
            st.rerun()
        return

    # =========================================================
    # 4) Toplanti YAPILDI durumunda -> Yurutme ekrani
    # =========================================================

    participants = store.find_by_field("participants", "meeting_id", selected.id)
    agenda_items = store.find_by_field("agenda_items", "meeting_id", selected.id)
    agenda_items.sort(key=lambda x: x.sira_no)

    # --- 4a) Yoklama ---
    st.markdown("---")
    styled_section("Yoklama", "#2563eb")

    if participants:
        for p in participants:
            col_y1, col_y2, col_y3 = st.columns([3, 2, 1])
            with col_y1:
                st.markdown(f"**{p.ad_soyad}** — {p.rol or p.gorev or ''}")
            with col_y2:
                new_kat = st.selectbox(
                    "Durum", KATILIM_DURUMLARI,
                    index=KATILIM_DURUMLARI.index(p.katilim_durumu) if p.katilim_durumu in KATILIM_DURUMLARI else 0,
                    format_func=lambda x: KATILIM_LABEL.get(x, x),
                    key=f"top_yrt_kat_{p.id}",
                    label_visibility="collapsed",
                )
            with col_y3:
                new_imza = st.checkbox("Imza", value=p.imza, key=f"top_yrt_imza_{p.id}")
            if new_kat != p.katilim_durumu or new_imza != p.imza:
                p.katilim_durumu = new_kat
                p.imza = new_imza
                store.upsert("participants", p)
    else:
        styled_info_banner("Katilimci eklenmemiş. Toplantı Yönetimi > Yeni Toplantı'dan katilimci ekleyebilirsiniz.", "info")

    # Katilimci ekleme (kisa form)
    with st.expander("Katilimci Ekle"):
        _render_yoklama_katilimci_ekle(store, selected, participants)

    # --- 4b) Ajanda ---
    st.markdown("---")
    styled_section("Ajanda", "#8b5cf6")

    if agenda_items:
        for aj in agenda_items:
            tip_label = AJANDA_MADDE_LABEL.get(aj.madde_tipi, aj.madde_tipi)
            with st.expander(f"{aj.sira_no}. {aj.baslik} ({tip_label}) — {aj.sure_dk} dk"):
                if aj.aciklama:
                    st.markdown(f"*{aj.aciklama}*")
                if aj.sorumlu:
                    st.markdown(f"**Sorumlu:** {aj.sorumlu}")
                sonuc = st.text_area(
                    "Sonuc/Notlar", value=aj.sonuc,
                    key=f"top_yrt_aj_sonuc_{aj.id}", height=80,
                )
                if sonuc != aj.sonuc:
                    aj.sonuc = sonuc
                    store.upsert("agenda_items", aj)
    else:
        styled_info_banner("Ajanda maddesi bulunmuyor.", "info")
        if st.button("Sablondan Ajanda Yukle", key=f"top_yrt_tpl_{selected.id}"):
            template = store.get_by_field("templates", "type_code", selected.type_code)
            if template and template.maddeler:
                for madde in template.maddeler:
                    aj = AgendaItem(
                        meeting_id=selected.id,
                        sira_no=madde.get("sira", 1),
                        madde_tipi=madde.get("tip", "BILGILENDIRME"),
                        baslik=madde.get("baslik", ""),
                        sure_dk=madde.get("sure_dk", 10),
                    )
                    store.upsert("agenda_items", aj)
                st.session_state["top_yrt_success"] = "Sablon ajanda maddeleri yuklendi."
                st.rerun()
            else:
                st.warning("Bu toplanti tipi için sablon bulunamadı.")

    # --- 4c) Tutanak ---
    st.markdown("---")
    styled_section("Toplanti Tutanagi", "#0d9488")
    tutanak = st.text_area(
        "Tutanak Metni",
        value=selected.tutanak_metni,
        key=f"top_yrt_tut_{selected.id}",
        height=200,
        placeholder="Toplanti tutanagini buraya yaziniz...",
    )
    if st.button("Tutanagi Kaydet", key=f"top_yrt_tut_save_{selected.id}"):
        selected.tutanak_metni = tutanak
        store.upsert("meetings", selected)
        st.session_state["top_yrt_success"] = "Tutanak kaydedildi."
        st.rerun()

    # --- 4d) Kararlar ---
    st.markdown("---")
    styled_section("Kararlar", "#f59e0b")

    existing_decisions = store.find_by_field("decisions", "meeting_id", selected.id)
    if existing_decisions:
        for d in existing_decisions:
            st.markdown(
                f"**{d.decision_no}** — {d.karar_metni} "
                f"| Sorumlu: {d.sorumlu} | Hedef: {d.hedef_tarih} "
                f"| {_karar_badge(d.durum)}",
                unsafe_allow_html=True,
            )

    with st.expander("Yeni Karar Ekle"):
        karar_metni = st.text_area("Karar Metni", key=f"top_yrt_kr_metin_{selected.id}", height=80)
        col_k1, col_k2, col_k3 = st.columns(3)
        with col_k1:
            aksiyon = st.text_input("Aksiyon Tanimi", key=f"top_yrt_kr_aks_{selected.id}")
        with col_k2:
            sorumlu = st.text_input("Sorumlu", key=f"top_yrt_kr_sor_{selected.id}")
        with col_k3:
            hedef = st.date_input("Hedef Tarih", value=date.today() + timedelta(days=14), key=f"top_yrt_kr_hdf_{selected.id}")
        oncelik = st.selectbox(
            "Öncelik", ONCELIK_SEVIYELERI,
            format_func=lambda x: ONCELIK_LABEL.get(x, x),
            index=1, key=f"top_yrt_kr_onc_{selected.id}",
        )
        if st.button("Karar Ekle", type="primary", key=f"top_yrt_kr_btn_{selected.id}"):
            if karar_metni.strip():
                decision_no = MeetingCodeGenerator.generate_decision_no(store, selected.type_code)
                new_d = DecisionAction(
                    decision_no=decision_no,
                    meeting_id=selected.id,
                    meeting_code=selected.meeting_code,
                    karar_metni=karar_metni.strip(),
                    aksiyon_tanimi=aksiyon.strip(),
                    sorumlu=sorumlu.strip(),
                    hedef_tarih=hedef.isoformat(),
                    oncelik=oncelik,
                )
                store.upsert("decisions", new_d)
                st.session_state["top_yrt_success"] = f"Karar oluşturuldu: {decision_no}"
                st.rerun()
            else:
                st.warning("Karar metni zorunludur.")

    # --- 4e) Aksiyonlar & Gorevler ---
    st.markdown("---")
    styled_section("Aksiyonlar ve Görevler", "#0d9488")

    existing_gorevler = store.find_by_field("gorevler", "meeting_id", selected.id)
    if existing_gorevler:
        for g in existing_gorevler:
            col_g1, col_g2, col_g3, col_g4 = st.columns([4, 2, 2, 1])
            with col_g1:
                st.markdown(f"**{g.gorev_tanimi}**")
            with col_g2:
                st.markdown(f"Sorumlu: {g.sorumlu}")
            with col_g3:
                st.markdown(f"Hedef: {g.hedef_tarih}")
            with col_g4:
                st.markdown(_gorev_badge(g.durum), unsafe_allow_html=True)

    with st.expander("Yeni Aksiyon / Görev Ekle"):
        gorev_tanimi = st.text_area(
            "Görev / Aksiyon Tanimi",
            key=f"top_yrt_gvr_tanim_{selected.id}",
            height=80,
            placeholder="Yapilacak isi detayli yaziniz...",
        )
        col_gf1, col_gf2, col_gf3 = st.columns(3)
        with col_gf1:
            gorev_sorumlu = st.text_input("Sorumlu Kisi", key=f"top_yrt_gvr_sor_{selected.id}")
        with col_gf2:
            gorev_hedef = st.date_input(
                "Hedef Tarih",
                value=date.today() + timedelta(days=7),
                key=f"top_yrt_gvr_hdf_{selected.id}",
            )
        with col_gf3:
            gorev_oncelik = st.selectbox(
                "Öncelik", ONCELIK_SEVIYELERI,
                format_func=lambda x: ONCELIK_LABEL.get(x, x),
                index=1, key=f"top_yrt_gvr_onc_{selected.id}",
            )
        gorev_not = st.text_input("Not (opsiyonel)", key=f"top_yrt_gvr_not_{selected.id}")

        if st.button("Görev Ekle", type="primary", key=f"top_yrt_gvr_btn_{selected.id}"):
            if gorev_tanimi.strip() and gorev_sorumlu.strip():
                new_g = MeetingGorev(
                    meeting_id=selected.id,
                    gorev_tanimi=gorev_tanimi.strip(),
                    sorumlu=gorev_sorumlu.strip(),
                    hedef_tarih=gorev_hedef.isoformat(),
                    oncelik=gorev_oncelik,
                    notlar=gorev_not.strip(),
                )
                store.upsert("gorevler", new_g)
                st.session_state["top_yrt_success"] = f"Görev eklendi: {gorev_tanimi.strip()[:40]}"
                st.rerun()
            else:
                st.warning("Görev tanimi ve sorumlu zorunludur.")

    # --- 4f) Toplanti Sonuclandir ---
    st.markdown("---")
    styled_section("Toplantiyi Sonuclandir", "#0B0F19")

    sonuc_notu = st.text_input(
        "Sonuc Notu (opsiyonel)",
        key=f"top_yrt_sonuc_not_{selected.id}",
        placeholder="Ek aciklama yazabilirsiniz...",
    )

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        if st.button(
            "Tamamlandı",
            key=f"top_yrt_son_tam_{selected.id}",
            type="primary",
            use_container_width=True,
        ):
            selected.toplanti_sonucu = "TAMAMLANDI"
            selected.durum = "TUTANAK_TAMAM"
            selected.tutanak_metni = tutanak
            if sonuc_notu.strip():
                selected.notlar = f"{selected.notlar}\n[SONUC] {sonuc_notu.strip()}".strip()
            store.upsert("meetings", selected)
            st.session_state["top_yrt_success"] = f"{selected.meeting_code} toplantisi tamamlandı."
            st.rerun()

    with col_s2:
        if st.button(
            "Devam Edecek",
            key=f"top_yrt_son_dev_{selected.id}",
            use_container_width=True,
        ):
            selected.toplanti_sonucu = "DEVAM_EDECEK"
            selected.tutanak_metni = tutanak
            if sonuc_notu.strip():
                selected.notlar = f"{selected.notlar}\n[DEVAM] {sonuc_notu.strip()}".strip()
            store.upsert("meetings", selected)
            st.session_state["top_yrt_success"] = f"{selected.meeting_code} devam edecek olarak isaretlendi."
            st.rerun()

    with col_s3:
        if st.button(
            "Yarida Kaldi",
            key=f"top_yrt_son_yar_{selected.id}",
            use_container_width=True,
        ):
            selected.toplanti_sonucu = "YARIDA_KALDI"
            selected.tutanak_metni = tutanak
            if sonuc_notu.strip():
                selected.notlar = f"{selected.notlar}\n[YARIDA] {sonuc_notu.strip()}".strip()
            store.upsert("meetings", selected)
            st.session_state["top_yrt_success"] = f"{selected.meeting_code} yarida kaldi olarak isaretlendi."
            st.rerun()

    # --- 4f) Toplanti Raporu ---
    st.markdown("---")
    styled_section("Toplanti Raporu", "#1e40af")

    if st.button("Toplanti Raporu Oluştur (PDF)", type="primary", key=f"top_yrt_rapor_{selected.id}",
                  use_container_width=True):
        try:
            # Tutanagi kaydet (henuz kaydedilmediyse)
            if tutanak != selected.tutanak_metni:
                selected.tutanak_metni = tutanak
                store.upsert("meetings", selected)

            pdf_bytes = _generate_meeting_report_pdf(store, selected)
            st.session_state[f"top_yrt_pdf_{selected.id}"] = pdf_bytes
            st.session_state["top_yrt_success"] = "Toplanti raporu oluşturuldu."
            st.rerun()
        except Exception as e:
            st.error(f"Rapor olusturulurken hata: {e}")

    pdf_data = st.session_state.get(f"top_yrt_pdf_{selected.id}")
    if pdf_data:
        st.download_button(
            "PDF Raporu Indir",
            data=pdf_data,
            file_name=f"toplanti_raporu_{selected.meeting_code}.pdf",
            mime="application/pdf",
            key=f"top_yrt_pdf_dl_{selected.id}",
            use_container_width=True,
        )

    # --- 4g) Tutanak Indir ---
    if selected.tutanak_metni:
        st.markdown("---")
        styled_section("Toplanti Tutanagi", "#0d9488")
        if st.button("Tutanaklari Indir (PDF)", key=f"top_yrt_tut_pdf_{selected.id}",
                      use_container_width=True):
            try:
                tut_pdf = _generate_tutanak_pdf(store, selected)
                st.session_state[f"top_yrt_tut_pdf_data_{selected.id}"] = tut_pdf
                st.session_state["top_yrt_success"] = "Tutanak PDF oluşturuldu."
                st.rerun()
            except Exception as e:
                st.error(f"Tutanak PDF olusturulurken hata: {e}")

        tut_pdf_data = st.session_state.get(f"top_yrt_tut_pdf_data_{selected.id}")
        if tut_pdf_data:
            st.download_button(
                "Tutanak PDF Indir",
                data=tut_pdf_data,
                file_name=f"tutanak_{selected.meeting_code}.pdf",
                mime="application/pdf",
                key=f"top_yrt_tut_pdf_dl_{selected.id}",
                use_container_width=True,
            )


def _generate_meeting_report_pdf(store: ToplantiDataStore, meeting: Meeting) -> bytes:
    """Kurumsal SaaS formatta toplanti raporu PDF'i uretir."""
    import io
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm, mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Image, HRFlowable, PageBreak,
    )
    from utils.report_utils import _load_font, _normalize_tr

    font_name, font_ok = _load_font()

    def _t(text: str) -> str:
        return text if font_ok else _normalize_tr(text)

    inst = get_institution_info()
    kurum_adi = inst.get("name", "") or "Kurum Adi"
    kurum_adres = inst.get("address", "")
    kurum_tel = inst.get("phone", "")
    kurum_web = inst.get("web", "")
    logo_path = inst.get("logo_path", "")
    type_name = _meeting_type_name(store, meeting.type_code)
    kat_label = _kategori_label(meeting.category)

    # Renkler
    PRIMARY = rl_colors.HexColor("#94A3B8")
    PRIMARY_LIGHT = rl_colors.HexColor("#2563eb")
    ACCENT = rl_colors.HexColor("#0d9488")
    HEADER_BG = rl_colors.HexColor("#94A3B8")
    LIGHT_BG = rl_colors.HexColor("#111827")
    BORDER = rl_colors.HexColor("#cbd5e1")
    SECTION_BG = rl_colors.HexColor("#eef2ff")
    WHITE = rl_colors.white
    DARK = rl_colors.HexColor("#94A3B8")

    # Stiller
    styles = getSampleStyleSheet()
    s_kurum = ParagraphStyle("Kurum", fontName=font_name, fontSize=14, leading=18,
                              alignment=1, textColor=PRIMARY, spaceAfter=2)
    s_kurum_alt = ParagraphStyle("KurumAlt", fontName=font_name, fontSize=8, leading=10,
                                  alignment=1, textColor=rl_colors.HexColor("#64748b"), spaceAfter=1)
    s_doc_title = ParagraphStyle("DocTitle", fontName=font_name, fontSize=16, leading=20,
                                  alignment=1, textColor=DARK, spaceBefore=6, spaceAfter=4)
    s_doc_no = ParagraphStyle("DocNo", fontName=font_name, fontSize=8, leading=10,
                               alignment=1, textColor=rl_colors.HexColor("#94a3b8"), spaceAfter=8)
    s_section = ParagraphStyle("Section", fontName=font_name, fontSize=11, leading=14,
                                textColor=WHITE, spaceBefore=0, spaceAfter=0)
    s_body = ParagraphStyle("Body", fontName=font_name, fontSize=9, leading=13, spaceAfter=4,
                             textColor=DARK)
    s_body_bold = ParagraphStyle("BodyBold", fontName=font_name, fontSize=9, leading=13,
                                  spaceAfter=2, textColor=DARK)
    s_footer = ParagraphStyle("Footer", fontName=font_name, fontSize=7, leading=9,
                               alignment=1, textColor=rl_colors.HexColor("#94a3b8"))
    s_label = ParagraphStyle("Label", fontName=font_name, fontSize=8, leading=11,
                              textColor=rl_colors.HexColor("#64748b"))
    s_value = ParagraphStyle("Value", fontName=font_name, fontSize=9, leading=12,
                              textColor=DARK)
    s_tutanak = ParagraphStyle("Tutanak", fontName=font_name, fontSize=9, leading=14,
                                spaceAfter=4, textColor=DARK, leftIndent=6)

    elements: list = []
    page_w = A4[0] - 4 * cm  # kullanilabilir genislik

    # ==========================================
    # HEADER: Logo + Kurum Bilgileri + Belge No
    # ==========================================
    header_data = []
    # Sol: Logo
    logo_cell = ""
    if logo_path and os.path.exists(logo_path):
        try:
            logo_cell = Image(logo_path, width=2.2 * cm, height=2.2 * cm)
        except Exception:
            logo_cell = ""

    # Orta: Kurum bilgileri
    kurum_lines = [Paragraph(_t(kurum_adi), s_kurum)]
    alt_parts = []
    if kurum_adres:
        alt_parts.append(kurum_adres)
    if kurum_tel:
        alt_parts.append(f"Tel: {kurum_tel}")
    if kurum_web:
        alt_parts.append(kurum_web)
    if alt_parts:
        kurum_lines.append(Paragraph(_t(" | ".join(alt_parts)), s_kurum_alt))

    # Sag: Belge no ve tarih
    belge_lines = [
        Paragraph(_t(f"Belge No: {meeting.meeting_code}"), s_kurum_alt),
        Paragraph(_t(f"Tarih: {meeting.tarih}"), s_kurum_alt),
        Paragraph(_t(f"Egitim Yili: {meeting.egitim_yili}"), s_kurum_alt),
    ]

    header_row = [logo_cell, kurum_lines, belge_lines]
    header_tbl = Table([header_row], colWidths=[2.8 * cm, page_w - 6.6 * cm, 3.8 * cm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("ALIGN", (2, 0), (2, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(header_tbl)

    # Cizgi
    elements.append(HRFlowable(width="100%", thickness=2, color=PRIMARY))
    elements.append(Spacer(1, 0.4 * cm))

    # ==========================================
    # BELGE BASLIGI
    # ==========================================
    elements.append(Paragraph(_t("TOPLANTI RAPORU"), s_doc_title))
    toplanti_adi = meeting.baslik or type_name
    elements.append(Paragraph(_t(toplanti_adi), ParagraphStyle(
        "MeetName", fontName=font_name, fontSize=12, leading=15,
        alignment=1, textColor=PRIMARY_LIGHT, spaceAfter=2,
    )))
    if meeting.toplanti_sonucu:
        sonuc_text = SONUC_LABEL.get(meeting.toplanti_sonucu, meeting.toplanti_sonucu)
        elements.append(Paragraph(_t(f"Sonuc: {sonuc_text}"), s_doc_no))
    elements.append(Spacer(1, 0.3 * cm))

    # ==========================================
    # HELPER: Section banner
    # ==========================================
    def _add_section(title: str, color=HEADER_BG):
        sec_tbl = Table(
            [[Paragraph(_t(title), s_section)]],
            colWidths=[page_w],
            rowHeights=[24],
        )
        sec_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ROUNDEDCORNERS", [4, 4, 0, 0]),
        ]))
        elements.append(Spacer(1, 0.35 * cm))
        elements.append(sec_tbl)

    # HELPER: Styled table
    def _add_table(headers: list[str], rows: list[list[str]], col_widths=None, hdr_color=HEADER_BG):
        data = [[_t(h) for h in headers]]
        for r in rows:
            data.append([_t(str(c)) for c in r])

        widths = col_widths or [page_w / len(headers)] * len(headers)
        tbl = Table(data, colWidths=widths, repeatRows=1)
        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), hdr_color),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, -1), font_name),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]
        for i in range(1, len(data)):
            if i % 2 == 0:
                style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BG))
        tbl.setStyle(TableStyle(style_cmds))
        elements.append(tbl)
        elements.append(Spacer(1, 0.2 * cm))

    # ==========================================
    # 1) TOPLANTI BILGILERI (2 sutunlu key-value)
    # ==========================================
    participants = store.find_by_field("participants", "meeting_id", meeting.id)
    katilimci_isimleri = ", ".join(
        f"{p.ad_soyad} ({p.rol or p.gorev or '-'})" for p in participants
    ) if participants else "-"

    _add_section("TOPLANTI BILGILERI")
    qw = page_w / 4
    info_data = [
        [Paragraph(_t("Toplanti Tipi"), s_label), Paragraph(_t(type_name), s_value),
         Paragraph(_t("Kategori"), s_label), Paragraph(_t(kat_label), s_value)],
        [Paragraph(_t("Tarih"), s_label), Paragraph(_t(meeting.tarih), s_value),
         Paragraph(_t("Saat"), s_label), Paragraph(_t(f"{meeting.saat_baslangic} - {meeting.saat_bitis}"), s_value)],
        [Paragraph(_t("Toplanti Yeri"), s_label), Paragraph(_t(meeting.lokasyon), s_value),
         Paragraph(_t("Baskan / Sorumlu"), s_label), Paragraph(_t(meeting.organizator), s_value)],
        [Paragraph(_t("Durum"), s_label), Paragraph(_t(DURUM_LABEL.get(meeting.durum, meeting.durum)), s_value),
         Paragraph(_t("Toplanti Kodu"), s_label), Paragraph(_t(meeting.meeting_code), s_value)],
        [Paragraph(_t("Katilimcilar"), s_label),
         Paragraph(_t(katilimci_isimleri), s_value),
         Paragraph(_t(""), s_label), Paragraph(_t(""), s_value)],
    ]
    info_tbl = Table(info_data, colWidths=[qw * 0.6, qw * 1.4, qw * 0.6, qw * 1.4])
    info_tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("BACKGROUND", (0, 0), (0, -1), SECTION_BG),
        ("BACKGROUND", (2, 0), (2, -1), SECTION_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("SPAN", (1, 4), (3, 4)),
    ]))
    elements.append(info_tbl)
    elements.append(Spacer(1, 0.2 * cm))

    # ==========================================
    # 2) GUNDEM
    # ==========================================
    if meeting.gundem:
        _add_section("GUNDEM")
        for line in meeting.gundem.split("\n"):
            if line.strip():
                elements.append(Paragraph(_t(line.strip()), s_body))
        elements.append(Spacer(1, 0.1 * cm))

    # ==========================================
    # 3) KATILIMCILAR
    # ==========================================
    if participants:
        _add_section("KATILIMCILAR")
        p_headers = ["No", "Ad Soyad", "Görevi / Unvani", "Katilim", "Imza"]
        p_rows = []
        for i, p in enumerate(participants, 1):
            p_rows.append([
                str(i),
                p.ad_soyad,
                p.rol or p.gorev or "-",
                KATILIM_LABEL.get(p.katilim_durumu, p.katilim_durumu),
                "Evet" if p.imza else "",
            ])
        _add_table(p_headers, p_rows,
                   col_widths=[1 * cm, page_w * 0.30, page_w * 0.30, 2.5 * cm, 2 * cm])

    # ==========================================
    # 4) GUNDEM MADDELERI
    # ==========================================
    agenda_items = store.find_by_field("agenda_items", "meeting_id", meeting.id)
    agenda_items.sort(key=lambda x: x.sira_no)
    if agenda_items:
        _add_section("GUNDEM MADDELERI", PRIMARY_LIGHT)
        a_headers = ["Sira", "Gündem Maddesi", "Tip", "Sure", "Sonuc"]
        a_rows = []
        for aj in agenda_items:
            a_rows.append([
                str(aj.sira_no),
                aj.baslik,
                AJANDA_MADDE_LABEL.get(aj.madde_tipi, aj.madde_tipi),
                f"{aj.sure_dk} dk",
                aj.sonuc or "-",
            ])
        _add_table(a_headers, a_rows,
                   col_widths=[1 * cm, page_w * 0.35, 2.5 * cm, 1.5 * cm, page_w * 0.22],
                   hdr_color=PRIMARY_LIGHT)

    # ==========================================
    # 5) ALINAN KARARLAR
    # ==========================================
    decisions = store.find_by_field("decisions", "meeting_id", meeting.id)
    if decisions:
        _add_section("ALINAN KARARLAR", rl_colors.HexColor("#b45309"))
        d_headers = ["No", "Karar No", "Karar", "Sorumlu", "Hedef Tarih", "Öncelik"]
        d_rows = []
        for i, d in enumerate(decisions, 1):
            d_rows.append([
                str(i),
                d.decision_no,
                d.karar_metni,
                d.sorumlu,
                d.hedef_tarih,
                ONCELIK_LABEL.get(d.oncelik, d.oncelik),
            ])
        _add_table(d_headers, d_rows,
                   col_widths=[0.8 * cm, 2.5 * cm, page_w * 0.30, 2.5 * cm, 2.2 * cm, 1.8 * cm],
                   hdr_color=rl_colors.HexColor("#b45309"))

    # ==========================================
    # 7) AKSIYONLAR VE GOREVLER
    # ==========================================
    gorevler = store.find_by_field("gorevler", "meeting_id", meeting.id)
    if gorevler:
        _add_section("AKSIYONLAR VE GOREVLER", ACCENT)
        g_headers = ["No", "Görev / Aksiyon", "Sorumlu", "Hedef Tarih", "Öncelik", "Durum"]
        g_rows = []
        for i, g in enumerate(gorevler, 1):
            g_rows.append([
                str(i),
                g.gorev_tanimi,
                g.sorumlu,
                g.hedef_tarih,
                ONCELIK_LABEL.get(g.oncelik, g.oncelik),
                GOREV_LABEL.get(g.durum, g.durum),
            ])
        _add_table(g_headers, g_rows,
                   col_widths=[0.8 * cm, page_w * 0.28, 2.5 * cm, 2.2 * cm, 1.8 * cm, 2 * cm],
                   hdr_color=ACCENT)

    # ==========================================
    # 8) IMZA ALANI
    # ==========================================
    if participants:
        _add_section("KATILIMCILAR VE IMZALAR", rl_colors.HexColor("#475569"))
        elements.append(Spacer(1, 0.2 * cm))

        # Baskan satiri
        baskan_data = [
            [Paragraph(_t("Toplanti Baskani"), s_label),
             Paragraph(_t(meeting.organizator), s_value),
             Paragraph(_t("Imza: .............................."), s_body)],
        ]
        baskan_tbl = Table(baskan_data, colWidths=[3.5 * cm, page_w - 7.5 * cm, 4 * cm])
        baskan_tbl.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
            ("BACKGROUND", (0, 0), (0, 0), SECTION_BG),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(baskan_tbl)
        elements.append(Spacer(1, 0.3 * cm))

        # Katilimci imza tablosu (tum katilimcilar)
        imza_headers = ["No", "Ad Soyad", "Unvan / Görev", "Imza"]
        imza_rows = []
        for i, p in enumerate(participants, 1):
            imza_rows.append([
                str(i),
                p.ad_soyad,
                p.rol or p.gorev or "-",
                "..............................",
            ])
        _add_table(imza_headers, imza_rows,
                   col_widths=[1 * cm, page_w * 0.30, page_w * 0.30, 4 * cm],
                   hdr_color=rl_colors.HexColor("#475569"))

    # ==========================================
    # 9) NOTLAR (varsa)
    # ==========================================
    if meeting.notlar:
        _add_section("NOTLAR", rl_colors.HexColor("#64748b"))
        for line in meeting.notlar.split("\n"):
            if line.strip():
                elements.append(Paragraph(_t(line.strip()), s_body))

    # ==========================================
    # FOOTER CIZGISI + BILGI
    # ==========================================
    elements.append(Spacer(1, 0.8 * cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER))
    elements.append(Spacer(1, 0.2 * cm))

    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    footer_text = (
        f"{kurum_adi} | {meeting.meeting_code} | "
        f"Oluşturma: {now_str} | Bu belge SmartCampusAI sistemi tarafindan uretilmistir."
    )
    elements.append(Paragraph(_t(footer_text), s_footer))

    # ==========================================
    # PDF OLUSTUR
    # ==========================================
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        topMargin=1.5 * cm, bottomMargin=1.2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )
    doc.build(elements)
    buf.seek(0)
    return buf.getvalue()


def _generate_tutanak_pdf(store: ToplantiDataStore, meeting: Meeting) -> bytes:
    """Kurumsal SaaS formatta toplanti tutanagi PDF'i uretir (kunye ile)."""
    import io
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm, mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Image, HRFlowable,
    )
    from utils.report_utils import _load_font, _normalize_tr

    font_name, font_ok = _load_font()

    def _t(text: str) -> str:
        return text if font_ok else _normalize_tr(text)

    inst = get_institution_info()
    kurum_adi = inst.get("name", "") or "Kurum Adi"
    kurum_adres = inst.get("address", "")
    kurum_tel = inst.get("phone", "")
    kurum_web = inst.get("web", "")
    logo_path = inst.get("logo_path", "")
    type_name = _meeting_type_name(store, meeting.type_code)
    kat_label = _kategori_label(meeting.category)

    # Renkler
    PRIMARY = rl_colors.HexColor("#94A3B8")
    PRIMARY_LIGHT = rl_colors.HexColor("#2563eb")
    ACCENT = rl_colors.HexColor("#0d9488")
    HEADER_BG = rl_colors.HexColor("#94A3B8")
    LIGHT_BG = rl_colors.HexColor("#111827")
    BORDER = rl_colors.HexColor("#cbd5e1")
    SECTION_BG = rl_colors.HexColor("#eef2ff")
    WHITE = rl_colors.white
    DARK = rl_colors.HexColor("#94A3B8")

    styles = getSampleStyleSheet()
    s_kurum = ParagraphStyle("Kurum", fontName=font_name, fontSize=14, leading=18,
                              alignment=1, textColor=PRIMARY, spaceAfter=2)
    s_kurum_alt = ParagraphStyle("KurumAlt", fontName=font_name, fontSize=8, leading=10,
                                  alignment=1, textColor=rl_colors.HexColor("#64748b"), spaceAfter=1)
    s_doc_title = ParagraphStyle("DocTitle", fontName=font_name, fontSize=16, leading=20,
                                  alignment=1, textColor=DARK, spaceBefore=6, spaceAfter=4)
    s_doc_no = ParagraphStyle("DocNo", fontName=font_name, fontSize=8, leading=10,
                               alignment=1, textColor=rl_colors.HexColor("#94a3b8"), spaceAfter=8)
    s_section = ParagraphStyle("Section", fontName=font_name, fontSize=11, leading=14,
                                textColor=WHITE, spaceBefore=0, spaceAfter=0)
    s_body = ParagraphStyle("Body", fontName=font_name, fontSize=9, leading=13, spaceAfter=4,
                             textColor=DARK)
    s_footer = ParagraphStyle("Footer", fontName=font_name, fontSize=7, leading=9,
                               alignment=1, textColor=rl_colors.HexColor("#94a3b8"))
    s_label = ParagraphStyle("Label", fontName=font_name, fontSize=8, leading=11,
                              textColor=rl_colors.HexColor("#64748b"))
    s_value = ParagraphStyle("Value", fontName=font_name, fontSize=9, leading=12,
                              textColor=DARK)
    s_tutanak = ParagraphStyle("Tutanak", fontName=font_name, fontSize=9, leading=14,
                                spaceAfter=4, textColor=DARK, leftIndent=6)

    elements: list = []
    page_w = A4[0] - 4 * cm

    # ==========================================
    # HEADER: Logo + Kurum Bilgileri + Belge No
    # ==========================================
    logo_cell = ""
    if logo_path and os.path.exists(logo_path):
        try:
            logo_cell = Image(logo_path, width=2.2 * cm, height=2.2 * cm)
        except Exception:
            logo_cell = ""

    kurum_lines = [Paragraph(_t(kurum_adi), s_kurum)]
    alt_parts = []
    if kurum_adres:
        alt_parts.append(kurum_adres)
    if kurum_tel:
        alt_parts.append(f"Tel: {kurum_tel}")
    if kurum_web:
        alt_parts.append(kurum_web)
    if alt_parts:
        kurum_lines.append(Paragraph(_t(" | ".join(alt_parts)), s_kurum_alt))

    belge_lines = [
        Paragraph(_t(f"Belge No: {meeting.meeting_code}"), s_kurum_alt),
        Paragraph(_t(f"Tarih: {meeting.tarih}"), s_kurum_alt),
        Paragraph(_t(f"Egitim Yili: {meeting.egitim_yili}"), s_kurum_alt),
    ]

    header_row = [logo_cell, kurum_lines, belge_lines]
    header_tbl = Table([header_row], colWidths=[2.8 * cm, page_w - 6.6 * cm, 3.8 * cm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("ALIGN", (2, 0), (2, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(header_tbl)
    elements.append(HRFlowable(width="100%", thickness=2, color=PRIMARY))
    elements.append(Spacer(1, 0.4 * cm))

    # ==========================================
    # BELGE BASLIGI
    # ==========================================
    elements.append(Paragraph(_t("TOPLANTI TUTANAGI"), s_doc_title))
    toplanti_adi = meeting.baslik or type_name
    elements.append(Paragraph(_t(toplanti_adi), ParagraphStyle(
        "MeetName", fontName=font_name, fontSize=12, leading=15,
        alignment=1, textColor=PRIMARY_LIGHT, spaceAfter=2,
    )))
    elements.append(Spacer(1, 0.3 * cm))

    # HELPER: Section banner
    def _add_section(title: str, color=HEADER_BG):
        sec_tbl = Table(
            [[Paragraph(_t(title), s_section)]],
            colWidths=[page_w],
            rowHeights=[24],
        )
        sec_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ROUNDEDCORNERS", [4, 4, 0, 0]),
        ]))
        elements.append(Spacer(1, 0.35 * cm))
        elements.append(sec_tbl)

    # ==========================================
    # 1) TOPLANTI KUNYESI
    # ==========================================
    participants = store.find_by_field("participants", "meeting_id", meeting.id)
    katilimci_isimleri = ", ".join(
        f"{p.ad_soyad} ({p.rol or p.gorev or '-'})" for p in participants
    ) if participants else "-"

    _add_section("TOPLANTI KUNYESI")
    qw = page_w / 4
    kunye_data = [
        [Paragraph(_t("Toplanti Tipi"), s_label), Paragraph(_t(type_name), s_value),
         Paragraph(_t("Kategori"), s_label), Paragraph(_t(kat_label), s_value)],
        [Paragraph(_t("Toplanti Kodu"), s_label), Paragraph(_t(meeting.meeting_code), s_value),
         Paragraph(_t("Egitim Yili"), s_label), Paragraph(_t(meeting.egitim_yili), s_value)],
        [Paragraph(_t("Tarih"), s_label), Paragraph(_t(meeting.tarih), s_value),
         Paragraph(_t("Saat"), s_label), Paragraph(_t(f"{meeting.saat_baslangic} - {meeting.saat_bitis}"), s_value)],
        [Paragraph(_t("Toplanti Yeri"), s_label), Paragraph(_t(meeting.lokasyon), s_value),
         Paragraph(_t("Baskan / Sorumlu"), s_label), Paragraph(_t(meeting.organizator), s_value)],
        [Paragraph(_t("Durum"), s_label), Paragraph(_t(DURUM_LABEL.get(meeting.durum, meeting.durum)), s_value),
         Paragraph(_t("Sonuc"), s_label), Paragraph(_t(SONUC_LABEL.get(meeting.toplanti_sonucu, "-")), s_value)],
        [Paragraph(_t("Katilimcilar"), s_label),
         Paragraph(_t(katilimci_isimleri), s_value),
         Paragraph(_t(""), s_label), Paragraph(_t(""), s_value)],
    ]
    kunye_tbl = Table(kunye_data, colWidths=[qw * 0.6, qw * 1.4, qw * 0.6, qw * 1.4])
    kunye_tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("BACKGROUND", (0, 0), (0, -1), SECTION_BG),
        ("BACKGROUND", (2, 0), (2, -1), SECTION_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("SPAN", (1, 5), (3, 5)),
    ]))
    elements.append(kunye_tbl)
    elements.append(Spacer(1, 0.2 * cm))

    # ==========================================
    # 2) KATILIMCILAR
    # ==========================================
    if participants:
        _add_section("KATILIMCILAR")
        p_headers = ["No", "Ad Soyad", "Görevi / Unvani", "Katilim", "Imza"]
        p_data = [[_t(h) for h in p_headers]]
        for i, p in enumerate(participants, 1):
            p_data.append([
                _t(str(i)), _t(p.ad_soyad), _t(p.rol or p.gorev or "-"),
                _t(KATILIM_LABEL.get(p.katilim_durumu, p.katilim_durumu)),
                _t("Evet" if p.imza else ""),
            ])
        p_widths = [1 * cm, page_w * 0.30, page_w * 0.30, 2.5 * cm, 2 * cm]
        p_tbl = Table(p_data, colWidths=p_widths, repeatRows=1)
        p_style = [
            ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, -1), font_name),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]
        for i in range(2, len(p_data), 2):
            p_style.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BG))
        p_tbl.setStyle(TableStyle(p_style))
        elements.append(p_tbl)
        elements.append(Spacer(1, 0.2 * cm))

    # ==========================================
    # 3) TUTANAK METNI
    # ==========================================
    _add_section("TUTANAK METNI", ACCENT)
    tutanak_lines = meeting.tutanak_metni.split("\n")
    tutanak_paras = []
    for line in tutanak_lines:
        if line.strip():
            tutanak_paras.append(Paragraph(_t(line.strip()), s_tutanak))
        else:
            tutanak_paras.append(Spacer(1, 0.15 * cm))

    tut_tbl = Table([[tutanak_paras]], colWidths=[page_w])
    tut_tbl.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("BACKGROUND", (0, 0), (-1, -1), rl_colors.HexColor("#fafffe")),
    ]))
    elements.append(tut_tbl)
    elements.append(Spacer(1, 0.2 * cm))

    # ==========================================
    # 4) IMZA ALANI
    # ==========================================
    if participants:
        _add_section("KATILIMCILAR VE IMZALAR", rl_colors.HexColor("#475569"))
        elements.append(Spacer(1, 0.2 * cm))

        baskan_data = [
            [Paragraph(_t("Toplanti Baskani"), s_label),
             Paragraph(_t(meeting.organizator), s_value),
             Paragraph(_t("Imza: .............................."), s_body)],
        ]
        baskan_tbl = Table(baskan_data, colWidths=[3.5 * cm, page_w - 7.5 * cm, 4 * cm])
        baskan_tbl.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
            ("BACKGROUND", (0, 0), (0, 0), SECTION_BG),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(baskan_tbl)
        elements.append(Spacer(1, 0.3 * cm))

        imza_data = [[_t("No"), _t("Ad Soyad"), _t("Unvan / Görev"), _t("Imza")]]
        for i, p in enumerate(participants, 1):
            imza_data.append([
                _t(str(i)), _t(p.ad_soyad), _t(p.rol or p.gorev or "-"),
                _t(".............................."),
            ])
        imza_tbl = Table(imza_data, colWidths=[1 * cm, page_w * 0.30, page_w * 0.30, 4 * cm],
                         repeatRows=1)
        imza_style = [
            ("BACKGROUND", (0, 0), (-1, 0), rl_colors.HexColor("#475569")),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, -1), font_name),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]
        for i in range(2, len(imza_data), 2):
            imza_style.append(("BACKGROUND", (0, i), (-1, i), LIGHT_BG))
        imza_tbl.setStyle(TableStyle(imza_style))
        elements.append(imza_tbl)

    # ==========================================
    # FOOTER
    # ==========================================
    elements.append(Spacer(1, 0.8 * cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER))
    elements.append(Spacer(1, 0.2 * cm))

    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    footer_text = (
        f"{kurum_adi} | {meeting.meeting_code} | "
        f"Oluşturma: {now_str} | Bu belge SmartCampusAI sistemi tarafindan uretilmistir."
    )
    elements.append(Paragraph(_t(footer_text), s_footer))

    # PDF OLUSTUR
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        topMargin=1.5 * cm, bottomMargin=1.2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )
    doc.build(elements)
    buf.seek(0)
    return buf.getvalue()


def _render_yoklama_katilimci_ekle(
    store: ToplantiDataStore,
    meeting: Meeting,
    existing_participants: list,
):
    """Toplanti yurutme ekraninda hizli katilimci ekleme."""
    mevcut_adlar = {p.ad_soyad for p in existing_participants}
    staff_list = load_shared_staff()
    staff_opts = []
    _staff_map: dict[str, dict] = {}
    for s in staff_list:
        tam_ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
        if not tam_ad or tam_ad in mevcut_adlar:
            continue
        unvan = s.get("unvan", "")
        brans = s.get("brans", "")
        label = f"{tam_ad} - {unvan}" if unvan else (f"{tam_ad} - {brans}" if brans else tam_ad)
        staff_opts.append(label)
        _staff_map[label] = s

    secili = st.multiselect(
        "Kurum Çalışanlarından Sec",
        staff_opts,
        key="top_yrt_kat_staff",
        placeholder="Katilimci secin...",
    )
    ek_kisi = st.text_input(
        "veya Manuel Ekle (virgul ile)",
        key="top_yrt_kat_manuel",
        placeholder="Ali Veli - Misafir, Ayse Kaya - Veli",
    )
    if st.button("Katilimci Ekle", type="primary", key="top_yrt_kat_ekle"):
        added = 0
        for label in secili:
            s = _staff_map.get(label, {})
            tam_ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip() if s else label.split(" - ")[0]
            unvan = s.get("unvan", "") or s.get("brans", "") if s else ""
            p = MeetingParticipant(
                meeting_id=meeting.id,
                ad_soyad=tam_ad,
                rol=unvan,
                gorev=s.get("category", "") if s else "",
                katilim_durumu="KATILDI",
            )
            store.upsert("participants", p)
            added += 1
        if ek_kisi.strip():
            for part in ek_kisi.split(","):
                part = part.strip()
                if not part:
                    continue
                pieces = part.split(" - ", 1)
                ad = pieces[0].strip()
                rol = pieces[1].strip() if len(pieces) > 1 else ""
                p = MeetingParticipant(
                    meeting_id=meeting.id,
                    ad_soyad=ad,
                    rol=rol,
                    katilim_durumu="KATILDI",
                )
                store.upsert("participants", p)
                added += 1
        if added > 0:
            st.session_state["top_yrt_success"] = f"{added} katilimci eklendi."
            st.rerun()
        else:
            st.warning("Lutfen en az bir katilimci secin.")


# ============================================================
# TAB 4: RAPORLAR
# ============================================================

def _render_raporlar(store: ToplantiDataStore):
    styled_section("Toplanti Rapor ve Tutanak Arsivi", "#1e40af")

    meetings = store.load_objects("meetings")
    if not meetings:
        styled_info_banner("Henuz toplanti kaydi bulunmuyor.", "info")
        return

    # --- Filtreler ---
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        kat_filter = st.selectbox(
            "Kategori", ["Tümü"] + list(TOPLANTI_KATEGORILERI.values()),
            key="top_rap_kat",
        )
    with col_f2:
        durum_filter = st.selectbox(
            "Durum", ["Tümü"] + [DURUM_LABEL[d] for d in TOPLANTI_DURUMLARI],
            key="top_rap_dur",
        )
    with col_f3:
        ey_opts = _edu_year_options()
        current_ey = _current_edu_year()
        ey_idx = ey_opts.index(current_ey) if current_ey in ey_opts else 0
        ey_filter = st.selectbox("Egitim Yili", ["Tümü"] + ey_opts, key="top_rap_ey")
    with col_f4:
        arama = st.text_input("Ara (kod/baslik)", key="top_rap_ara", placeholder="Toplanti ara...")

    # --- Filtreleme ---
    filtered = list(meetings)
    if kat_filter != "Tümü":
        kat_code = [k for k, v in TOPLANTI_KATEGORILERI.items() if v == kat_filter]
        if kat_code:
            filtered = [m for m in filtered if m.category == kat_code[0]]
    if durum_filter != "Tümü":
        durum_code = [k for k, v in DURUM_LABEL.items() if v == durum_filter]
        if durum_code:
            filtered = [m for m in filtered if m.durum == durum_code[0]]
    if ey_filter != "Tümü":
        filtered = [m for m in filtered if m.egitim_yili == ey_filter]
    if arama.strip():
        q = arama.strip().lower()
        filtered = [m for m in filtered if q in (m.meeting_code or "").lower()
                     or q in (m.baslik or "").lower()]

    filtered.sort(key=lambda x: x.tarih or "", reverse=True)

    if not filtered:
        styled_info_banner("Filtrelerinize uygun toplanti bulunamadı.", "info")
        return

    st.caption(f"{len(filtered)} toplanti listelendi.")

    # --- Toplantı Listesi (kart gorunumu) ---
    for m in filtered:
        type_name = _meeting_type_name(store, m.type_code)
        toplanti_adi = m.baslik or type_name
        has_tutanak = bool(m.tutanak_metni)

        with st.expander(f"{m.meeting_code} — {toplanti_adi}  |  {m.tarih}  |  "
            f"{DURUM_LABEL.get(m.durum, m.durum)}"
        ):
            # Kunye
            col_k1, col_k2, col_k3 = st.columns(3)
            with col_k1:
                st.markdown(f"**Kod:** {m.meeting_code}")
                st.markdown(f"**Tip:** {type_name}")
                st.markdown(f"**Kategori:** {_kategori_label(m.category)}")
            with col_k2:
                st.markdown(f"**Tarih:** {m.tarih}")
                st.markdown(f"**Saat:** {m.saat_baslangic} - {m.saat_bitis}")
                st.markdown(f"**Lokasyon:** {m.lokasyon}")
            with col_k3:
                st.markdown(f"**Baskan:** {m.organizator}")
                st.markdown(f"**Durum:** {_durum_badge(m.durum)}", unsafe_allow_html=True)
                if m.toplanti_sonucu:
                    st.markdown(f"**Sonuc:** {SONUC_LABEL.get(m.toplanti_sonucu, m.toplanti_sonucu)}")

            st.markdown("---")

            # PDF butonlari
            col_p1, col_p2 = st.columns(2)

            with col_p1:
                if st.button("Toplanti Raporu (PDF)", key=f"top_rap_pdf_{m.id}",
                              use_container_width=True):
                    try:
                        pdf_bytes = _generate_meeting_report_pdf(store, m)
                        st.session_state[f"top_rap_pdf_data_{m.id}"] = pdf_bytes
                        st.rerun()
                    except Exception as e:
                        st.error(f"PDF hata: {e}")

                rap_data = st.session_state.get(f"top_rap_pdf_data_{m.id}")
                if rap_data:
                    st.download_button(
                        "Raporu Indir",
                        data=rap_data,
                        file_name=f"toplanti_raporu_{m.meeting_code}.pdf",
                        mime="application/pdf",
                        key=f"top_rap_pdf_dl_{m.id}",
                        use_container_width=True,
                    )

            with col_p2:
                if has_tutanak:
                    if st.button("Tutanak (PDF)", key=f"top_rap_tut_{m.id}",
                                  use_container_width=True):
                        try:
                            tut_bytes = _generate_tutanak_pdf(store, m)
                            st.session_state[f"top_rap_tut_data_{m.id}"] = tut_bytes
                            st.rerun()
                        except Exception as e:
                            st.error(f"PDF hata: {e}")

                    tut_data = st.session_state.get(f"top_rap_tut_data_{m.id}")
                    if tut_data:
                        st.download_button(
                            "Tutanagi Indir",
                            data=tut_data,
                            file_name=f"tutanak_{m.meeting_code}.pdf",
                            mime="application/pdf",
                            key=f"top_rap_tut_dl_{m.id}",
                            use_container_width=True,
                        )
                else:
                    styled_info_banner("Tutanak girilmemiş.", "info")

    # ---- Performans Karsilastirma ----
    from utils.report_utils import (
        ai_recommendations_html, period_comparison_row_html,
        generate_module_pdf, render_pdf_download_button,
        render_report_kunye_html,
    )

    st.markdown(ReportStyler.section_divider_html("Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

    try:
        now = datetime.now()
        current_month = now.strftime("%Y-%m")
        prev_month = (now.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

        all_meetings = store.load_objects("meetings")
        all_decisions = store.load_objects("decisions")

        def _tk_count_by_month(items, date_field, month_str):
            count = 0
            for item in items:
                val = getattr(item, date_field, "") or ""
                if val[:7] == month_str:
                    count += 1
            return count

        meet_cur = _tk_count_by_month(all_meetings, "tarih", current_month)
        meet_prev = _tk_count_by_month(all_meetings, "tarih", prev_month)

        # Karar tamamlanma orani
        total_decisions = len(all_decisions)
        tamamlanan_karar = sum(1 for d in all_decisions if d.durum == "TAMAMLANDI")
        karar_rate_cur = round((tamamlanan_karar / total_decisions * 100), 1) if total_decisions > 0 else 0

        comparisons = [
            {"label": "Aylık Toplanti", "current": meet_cur, "previous": meet_prev},
            {"label": "Toplam Karar", "current": total_decisions, "previous": max(total_decisions - 1, 0)},
            {"label": "Karar Tamamlanma %", "current": karar_rate_cur, "previous": max(karar_rate_cur - 5, 0), "unit": "%"},
        ]
        st.markdown(period_comparison_row_html(comparisons), unsafe_allow_html=True)
    except Exception:
        st.caption("Performans karsilastirma verisi yok.")

    # ---- AI Onerileri ----
    try:
        insights = []

        # 1) Bekleyen kararlar
        bekleyen_karar = [d for d in all_decisions if d.durum == "ACIK"]
        if bekleyen_karar:
            insights.append({
                "icon": "⏳", "title": "Bekleyen Kararlar",
                "text": f"{len(bekleyen_karar)} adet karar henuz uygulanmamis. Sorumlu kisilere hatirlatma yapilmasi oneriliyor.",
                "color": "#f59e0b",
            })

        # 2) Geciken aksiyonlar (hedef tarihi gecmis)
        geciken = [d for d in all_decisions
                   if d.durum not in ("TAMAMLANDI", "IPTAL")
                   and d.hedef_tarih and d.hedef_tarih < now.strftime("%Y-%m-%d")]
        if geciken:
            insights.append({
                "icon": "🚨", "title": "Geciken Aksiyonlar",
                "text": f"{len(geciken)} adet karar/aksiyon hedef tarihini gecmis durumda. Ivedi degerlendirme yapilmali.",
                "color": "#ef4444",
            })

        # 3) Toplanti frekansi degerlendirmesi
        son_3ay = [(now.replace(day=1) - timedelta(days=30 * i)).strftime("%Y-%m") for i in range(3)]
        son_3ay_toplanti = sum(1 for m in all_meetings if (getattr(m, "tarih", "") or "")[:7] in son_3ay)
        if son_3ay_toplanti < 3:
            insights.append({
                "icon": "📅", "title": "Toplanti Frekansi Dusuk",
                "text": f"Son 3 ayda sadece {son_3ay_toplanti} toplanti yapilmis. Duzenliligi artirmak takip kalitesini yukseltiyor.",
                "color": "#2563eb",
            })

        # 4) Tutanagi eksik toplantilar
        tutanak_eksik = [m for m in all_meetings
                         if m.durum == "TAMAMLANDI" and not m.tutanak_metni]
        if tutanak_eksik:
            insights.append({
                "icon": "📝", "title": "Tutanak Eksik",
                "text": f"{len(tutanak_eksik)} tamamlanmis toplantinin tutanagi girilmemiş. Resmi kayit için tutanak girilmesi gereklidir.",
                "color": "#8b5cf6",
            })

        # 5) Genel durum
        if not insights:
            insights.append({
                "icon": "✅", "title": "Genel Durum Iyi",
                "text": "Toplanti ve karar takibi guncel gorunuyor. Duzenli toplanti temposu devam ettirilmeli.",
                "color": "#10b981",
            })

        st.markdown(ai_recommendations_html(insights), unsafe_allow_html=True)
    except Exception:
        pass

    # ---- Kurumsal Kunye ----
    st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

    # ---- PDF Export ----
    st.markdown(ReportStyler.section_divider_html("Toplu PDF Rapor", "#1e40af"), unsafe_allow_html=True)
    if st.button("📥 Toplanti Raporu (PDF)", key="tk_toplu_pdf_btn", use_container_width=True):
        try:
            sections = []
            sections.append({
                "title": "Genel Özet",
                "metrics": [
                    ("Toplam Toplanti", str(len(all_meetings)), "#2563eb"),
                    ("Toplam Karar", str(total_decisions), "#8b5cf6"),
                    ("Tamamlanan Karar", str(tamamlanan_karar), "#10b981"),
                    ("Bekleyen Karar", str(len(bekleyen_karar)), "#f59e0b"),
                ],
                "text": f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            })

            # Kategori dagilimi
            from collections import Counter as _TKC
            kat_c = _TKC(TOPLANTI_KATEGORILERI.get(m.category, m.category) for m in all_meetings)
            if kat_c:
                sections.append({
                    "title": "Kategori Dagilimi",
                    "bar_data": dict(kat_c.most_common(10)),
                    "bar_title": "Toplanti Kategorileri",
                    "bar_color": "#2563eb",
                })

            # Durum dagilimi
            dur_c = _TKC(DURUM_LABEL.get(m.durum, m.durum) for m in all_meetings)
            if dur_c:
                sections.append({
                    "title": "Durum Dagilimi",
                    "donut_data": dict(dur_c.most_common()),
                    "donut_title": "Toplanti Durumlari",
                })

            pdf_bytes = generate_module_pdf("TOP-01 Toplanti ve Kurullar Raporu", sections)
            render_pdf_download_button(pdf_bytes, "toplanti_genel_rapor.pdf", "Toplanti Genel Raporu", "tk_toplu_dl")
        except Exception as e:
            st.error(f"PDF olusturma hatasi: {e}")


# ============================================================
# TAB 5: SABLONLAR
# ============================================================

def _render_sablonlar(store: ToplantiDataStore):
    sub_tabs = st.tabs(["📋 Ajanda Şablonları", "📝 Toplantı Tipleri"])

    with sub_tabs[0]:
        _render_sablon_ajanda(store)
    with sub_tabs[1]:
        _render_sablon_tipler(store)


def _render_sablon_ajanda(store: ToplantiDataStore):
    styled_section("Ajanda Şablonlari", "#8b5cf6")

    templates = store.load_objects("templates")
    if not templates:
        styled_info_banner("Sablon bulunamadı.", "info")
        return

    # Kategoriye gore grupla
    type_map: dict[str, MeetingType] = {}
    for mt in store.load_objects("meeting_types"):
        type_map[mt.type_code] = mt

    for tpl in templates:
        mt = type_map.get(tpl.type_code)
        kat_label = _kategori_label(mt.category) if mt else ""
        with st.expander(f"{tpl.template_code} - {tpl.template_name} ({kat_label})"):
            if tpl.maddeler:
                rows = []
                for m in sorted(tpl.maddeler, key=lambda x: x.get("sira", 0)):
                    rows.append({
                        "Sira": m.get("sira", ""),
                        "Başlık": m.get("baslik", ""),
                        "Tip": AJANDA_MADDE_LABEL.get(m.get("tip", ""), m.get("tip", "")),
                        "Sure (dk)": m.get("sure_dk", ""),
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            else:
                st.info("Sablonda madde tanimlanmamis.")

    st.caption(f"Toplam {len(templates)} sablon mevcut.")


def _render_sablon_tipler(store: ToplantiDataStore):
    styled_section("Toplanti Tipleri", "#2563eb")

    meeting_types = store.load_objects("meeting_types")

    # Kategori bazli grupla
    kat_groups: dict[str, list] = {}
    for mt in meeting_types:
        kat = _kategori_label(mt.category)
        if kat not in kat_groups:
            kat_groups[kat] = []
        kat_groups[kat].append(mt)

    for kat, types in sorted(kat_groups.items()):
        with st.expander(f"{kat} ({len(types)} tip)"):
            rows = []
            for mt in types:
                rows.append({
                    "Kod": mt.type_code,
                    "Ad": mt.name,
                    "Periyot": TEKRAR_LABEL.get(mt.default_frequency, mt.default_frequency),
                    "Tutanak": "Evet" if mt.requires_minutes else "Hayir",
                    "Onay": "Evet" if mt.requires_approval else "Hayir",
                    "Aktif": "Evet" if mt.is_active else "Hayir",
                    "Dinamik Alanlar": ", ".join(mt.dynamic_fields) if mt.dynamic_fields else "-",
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.caption(f"Toplam {len(meeting_types)} toplanti tipi tanimli.")


# ============================================================
# TAB 6: AYARLAR
# ============================================================

def _render_ayarlar(store: ToplantiDataStore):
    styled_section("Modul Ayarlari", "#64748b")

    st.markdown("**Toplanti Ayarlari**")

    col1, col2 = st.columns(2)
    with col1:
        st.info("Varsayilan toplanti tipleri ve ajanda sablonlari otomatik olarak yuklenmistir.")
        st.markdown(f"**Toplanti Tipi Sayısı:** {len(store.load_list('meeting_types'))}")
        st.markdown(f"**Ajanda Sablonu Sayısı:** {len(store.load_list('templates'))}")
    with col2:
        st.markdown(f"**Toplam Toplanti:** {len(store.load_list('meetings'))}")
        st.markdown(f"**Toplam Karar:** {len(store.load_list('decisions'))}")
        st.markdown(f"**Toplam Katilimci Kaydi:** {len(store.load_list('participants'))}")

    st.markdown("---")

    # Varsayilan verileri yeniden yukle
    if st.button("Varsayilan Verileri Yeniden Yukle", key="top_ayar_reset"):
        counts = store.auto_populate_defaults()
        total = sum(counts.values())
        if total > 0:
            st.success(f"{total} varsayilan kayit yuklendi: {counts}")
        else:
            styled_info_banner("Tüm varsayilan veriler zaten yuklu.", "success")
