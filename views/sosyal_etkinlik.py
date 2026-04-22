"""
SET-01 Sosyal Etkinlik ve Kulup Modulu - Streamlit UI
=====================================================
Kulup yonetimi, sosyal etkinlik takibi, faaliyet planlama.
"""

from __future__ import annotations

import os
from datetime import datetime, date, timedelta
from collections import Counter

import streamlit as st
from utils.ui_kit import confirm_action

from utils.tenant import get_tenant_dir
import pandas as pd
from utils.report_utils import ReportStyler, ReportPDFGenerator, get_institution_info
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("sosyal_etkinlik")
except Exception:
    pass
from utils.shared_data import (
    load_shared_staff, get_staff_display_options,
    get_student_display_options, get_veli_display_options,
    get_sinif_sube_listesi, load_shared_students,
)
from models.sosyal_etkinlik import (
    SosyalEtkinlikDataStore,
    Kulup, KulupFaaliyet, KulupKarar, SosyalEtkinlik,
    ETKINLIK_KATEGORILERI, ETKINLIK_ALT_KATEGORILERI,
    SPOR_BRANSLARI, MUSABAKA_KAPSAMI,
    ETKINLIK_DURUMLARI, ETKINLIK_DURUM_LABEL, ETKINLIK_DURUM_RENK,
    KULUP_DURUMLARI, HAFTANIN_GUNLERI, KADEME_SECENEKLERI, KADEME_SINIF_MAP,
    FAALIYET_DURUMLARI, FAALIYET_DURUM_LABEL,
    KATILIMCI_KATEGORILERI, BILDIRIM_TIPLERI,
    YABANCI_DIL_ETKINLIK_TURLERI,
)


# ============================================================
# STORE INIT
# ============================================================

def _get_set_store() -> SosyalEtkinlikDataStore:
    base = os.path.join(get_tenant_dir(), "sosyal_etkinlik")
    return SosyalEtkinlikDataStore(base)


# ============================================================
# CSS & STYLED HELPERS
# ============================================================

def _inject_set_css():
    inject_common_css("set")
    st.markdown("""
    <style>
    :root {
        --set-primary: #7c3aed;
        --set-primary-dark: #5b21b6;
        --set-success: #10b981;
        --set-warning: #f59e0b;
        --set-danger: #ef4444;
        --set-teal: #0d9488;
        --set-dark: #0B0F19;
    }
    </style>""", unsafe_allow_html=True)


def _durum_badge(durum: str, label_map: dict, renk_map: dict) -> str:
    label = label_map.get(durum, durum)
    color = renk_map.get(durum, "#94a3b8")
    return f"<span style='background:{color};color:#fff;padding:3px 10px;border-radius:12px;font-size:0.75rem;font-weight:600'>{label}</span>"


def _current_edu_year() -> str:
    today = date.today()
    y = today.year if today.month >= 9 else today.year - 1
    return f"{y}-{y + 1}"


def _edu_year_options() -> list[str]:
    current = date.today().year
    return [f"{y}-{y + 1}" for y in range(current + 1, current - 5, -1)]


# ============================================================
# ANA RENDER
# ============================================================

def render_sosyal_etkinlik():
    _inject_set_css()
    styled_header("Sosyal Etkinlik ve Kulüpler", "Kulup yonetimi, etkinlik takibi ve faaliyet planlama", icon="🎭")

    store = _get_set_store()

    render_smarti_welcome("sosyal_etkinlik")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("sosyal_etkinlik_egitim_yili")

    # -- Tab Gruplama (20 tab -> 3 grup) --
    _GRP_96685 = {
        "📋 Grup A": [("📊 Dashboard", 0), ("🎭 Kulüpler", 1), ("🎉 Sosyal Etkinlikler", 2), ("📈 Raporlar", 3), ("🏆 Kulüp Performans", 4), ("📅 Etkinlik Takvimi", 5), ("🎯 Sosyal Portfolyo", 6)],
        "📊 Grup B": [("🏅 Turnuva & Yarışma", 7), ("📸 Galeri & Arşiv", 8), ("🤖 AI Planlama", 9), ("🎮 Gamifiye", 10), ("🌍 Sosyal Sorumluluk", 11), ("🔄 Otomasyon", 12), ("📡 Medya Merkezi", 13)],
        "🔧 Grup C": [("🌐 Dış İşbirliği", 14), ("🚀 İnovasyon", 15), ("🎓 Dijital Kapsül", 16), ("📊 Sosyal Endeks", 17), ("🤖 AI Danışman", 18), ("🤖 Smarti", 19)],
    }
    _sg_96685 = st.radio("", list(_GRP_96685.keys()), horizontal=True, label_visibility="collapsed", key="rg_96685")
    _gt_96685 = _GRP_96685[_sg_96685]
    _aktif_idx_96685 = set(t[1] for t in _gt_96685)
    _tab_names_96685 = [t[0] for t in _gt_96685]
    tabs = st.tabs(_tab_names_96685)
    _tab_real_96685 = {idx: t for idx, t in zip((t[1] for t in _gt_96685), tabs)}

    if 0 in _aktif_idx_96685:
      with _tab_real_96685[0]:
        _render_dashboard(store)
    if 1 in _aktif_idx_96685:
      with _tab_real_96685[1]:
        _render_kulupler(store)
    if 2 in _aktif_idx_96685:
      with _tab_real_96685[2]:
        _render_sosyal_etkinlikler(store)
    if 3 in _aktif_idx_96685:
      with _tab_real_96685[3]:
        _render_raporlar(store)
    if 4 in _aktif_idx_96685:
      with _tab_real_96685[4]:
        try:
            from views._set_yeni_ozellikler import render_kulup_performans
            render_kulup_performans(store)
        except Exception as _e:
            st.error(f"Kulup Performans yuklenemedi: {_e}")
    if 5 in _aktif_idx_96685:
      with _tab_real_96685[5]:
        try:
            from views._set_yeni_ozellikler import render_etkinlik_takvimi
            render_etkinlik_takvimi(store)
        except Exception as _e:
            st.error(f"Etkinlik Takvimi yuklenemedi: {_e}")
    if 6 in _aktif_idx_96685:
      with _tab_real_96685[6]:
        try:
            from views._set_yeni_ozellikler import render_sosyal_portfolyo
            render_sosyal_portfolyo(store)
        except Exception as _e:
            st.error(f"Sosyal Portfolyo yuklenemedi: {_e}")
    if 7 in _aktif_idx_96685:
      with _tab_real_96685[7]:
        try:
            from views._set_super_features import render_turnuva_merkezi
            render_turnuva_merkezi(store)
        except Exception as _e:
            st.error(f"Turnuva Merkezi yuklenemedi: {_e}")
    if 8 in _aktif_idx_96685:
      with _tab_real_96685[8]:
        try:
            from views._set_super_features import render_etkinlik_galeri
            render_etkinlik_galeri(store)
        except Exception as _e:
            st.error(f"Galeri yuklenemedi: {_e}")
    if 9 in _aktif_idx_96685:
      with _tab_real_96685[9]:
        try:
            from views._set_super_features import render_ai_etkinlik_planlama
            render_ai_etkinlik_planlama(store)
        except Exception as _e:
            st.error(f"AI Planlama yuklenemedi: {_e}")
    if 10 in _aktif_idx_96685:
      with _tab_real_96685[10]:
        try:
            from views._set_mega_features import render_gamifiye_sosyal
            render_gamifiye_sosyal(store)
        except Exception as _e:
            st.error(f"Gamifiye yuklenemedi: {_e}")
    if 11 in _aktif_idx_96685:
      with _tab_real_96685[11]:
        try:
            from views._set_mega_features import render_sosyal_sorumluluk
            render_sosyal_sorumluluk(store)
        except Exception as _e:
            st.error(f"Sosyal Sorumluluk yuklenemedi: {_e}")
    if 12 in _aktif_idx_96685:
      with _tab_real_96685[12]:
        try:
            from views._set_mega_features import render_etkinlik_otomasyon
            render_etkinlik_otomasyon(store)
        except Exception as _e:
            st.error(f"Otomasyon yuklenemedi: {_e}")
    if 13 in _aktif_idx_96685:
      with _tab_real_96685[13]:
        try:
            from views._set_zirve_features import render_medya_merkezi
            render_medya_merkezi(store)
        except Exception as _e:
            st.error(f"Medya Merkezi yuklenemedi: {_e}")
    if 14 in _aktif_idx_96685:
      with _tab_real_96685[14]:
        try:
            from views._set_zirve_features import render_dis_isbirligi
            render_dis_isbirligi(store)
        except Exception as _e:
            st.error(f"Dis Isbirligi yuklenemedi: {_e}")
    if 15 in _aktif_idx_96685:
      with _tab_real_96685[15]:
        try:
            from views._set_zirve_features import render_inovasyon_ekosistemi
            render_inovasyon_ekosistemi(store)
        except Exception as _e:
            st.error(f"Inovasyon yuklenemedi: {_e}")
    if 16 in _aktif_idx_96685:
      with _tab_real_96685[16]:
        try:
            from views._set_final_features import render_dijital_kapsul
            render_dijital_kapsul(store)
        except Exception as _e:
            st.error(f"Dijital Kapsul yuklenemedi: {_e}")
    if 17 in _aktif_idx_96685:
      with _tab_real_96685[17]:
        try:
            from views._set_final_features import render_sosyal_endeks
            render_sosyal_endeks(store)
        except Exception as _e:
            st.error(f"Sosyal Endeks yuklenemedi: {_e}")
    if 18 in _aktif_idx_96685:
      with _tab_real_96685[18]:
        try:
            from views._set_final_features import render_ai_sosyal_danisman
            render_ai_sosyal_danisman(store)
        except Exception as _e:
            st.error(f"AI Danisman yuklenemedi: {_e}")
    if 19 in _aktif_idx_96685:
      with _tab_real_96685[19]:
        def _set_smarti_context():
            try:
                s = _get_set_store()
                etkinlik_count = len(s.load_objects("etkinlikler"))
                kulup_count = len(s.load_objects("kulupler"))
                uyelik_count = len(s.load_objects("uyelikler"))
                return (
                    f"Etkinlik kaydi: {etkinlik_count}, Kulup kaydi: {kulup_count}, "
                    f"Uyelik kaydi: {uyelik_count}"
                )
            except Exception:
                return ""
        render_smarti_chat("sosyal_etkinlik", _set_smarti_context)


# ============================================================
# TAB 1: DASHBOARD
# ============================================================

def _render_dashboard(store: SosyalEtkinlikDataStore):
    styled_section("Genel Bakis", "#0B0F19")

    kulupler = store.load_objects("kulupler")
    etkinlikler = store.load_objects("etkinlikler")
    faaliyetler = store.load_objects("kulup_faaliyetler")

    aktif_kulup = len([k for k in kulupler if k.durum == "AKTIF"])
    toplam_etkinlik = len(etkinlikler)
    toplam_ogrenci = sum(len(k.ogrenciler) for k in kulupler if k.durum == "AKTIF")
    tamamlanan = len([e for e in etkinlikler if e.durum == "TAMAMLANDI"])

    html = ReportStyler.metric_cards_html([
        ("Aktif Kulup", str(aktif_kulup), "#7c3aed", "🎭"),
        ("Toplam Etkinlik", str(toplam_etkinlik), "#2563eb", "📋"),
        ("Kulup Öğrencisi", str(toplam_ogrenci), "#0d9488", "👥"),
        ("Tamamlanan", str(tamamlanan), "#10b981", "✅"),
    ])
    st.markdown(html, unsafe_allow_html=True)

    # Kategori dagilimi
    col1, col2 = st.columns(2)
    with col1:
        styled_section("Etkinlik Kategori Dagilimi", "#7c3aed")
        if etkinlikler:
            all_cats = store.get_all_categories()
            kat_counts: dict[str, float] = {}
            for e in etkinlikler:
                label = all_cats.get(e.kategori, e.kategori)
                kat_counts[label] = kat_counts.get(label, 0) + 1
            svg = ReportStyler.donut_chart_svg(kat_counts)
            st.markdown(svg, unsafe_allow_html=True)
        else:
            styled_info_banner("Henuz etkinlik kaydi yok.", "info")

    with col2:
        styled_section("Kulüp Listesi", "#5b21b6")
        if kulupler:
            for k in kulupler:
                if k.durum == "AKTIF":
                    gun_saat = f"{k.faaliyet_gunu} {k.faaliyet_saati}" if k.faaliyet_gunu else "-"
                    st.markdown(
                        f"**{k.ad}** | {len(k.ogrenciler)} ogrenci | {gun_saat}",
                    )
        else:
            styled_info_banner("Henuz kulup tanimlanmamis.", "info")

    # Yaklasan etkinlikler
    styled_section("Yaklasan Etkinlikler (7 Gün)", "#f59e0b")
    today_str = date.today().isoformat()
    week_later = (date.today() + timedelta(days=7)).isoformat()
    yaklasan = [
        e for e in etkinlikler
        if e.durum in ("PLANLANDI", "DEVAM_EDIYOR")
        and e.tarih_baslangic >= today_str
        and e.tarih_baslangic <= week_later
    ]
    if yaklasan:
        for e in sorted(yaklasan, key=lambda x: x.tarih_baslangic):
            kat_label = all_cats.get(e.kategori, e.kategori)
            badge = _durum_badge(e.durum, ETKINLIK_DURUM_LABEL, ETKINLIK_DURUM_RENK)
            st.markdown(
                f"{badge} **{e.baslik}** | {kat_label} | {e.tarih_baslangic} | {e.sorumlu or '-'}",
                unsafe_allow_html=True,
            )
    else:
        styled_info_banner("Yaklasan etkinlik bulunmuyor.", "info")


# ============================================================
# TAB 2: KULUPLER
# ============================================================

def _render_kulupler(store: SosyalEtkinlikDataStore):
    sub_tabs = st.tabs([
        "📋 Kulüp Listesi",
        "🔍 Kulüp Detay",
        "📝 Faaliyetler",
        "📌 Kararlar",
        "📅 Planlar",
    ])

    with sub_tabs[0]:
        _render_kulup_listesi(store)
    with sub_tabs[1]:
        _render_kulup_detay(store)
    with sub_tabs[2]:
        _render_kulup_faaliyetler(store)
    with sub_tabs[3]:
        _render_kulup_kararlar(store)
    with sub_tabs[4]:
        _render_kulup_planlar(store)


def _render_kulup_listesi(store: SosyalEtkinlikDataStore):
    styled_section("Kulup Yönetimi", "#7c3aed")

    if st.session_state.get("set_kulup_success"):
        styled_info_banner(st.session_state.pop("set_kulup_success"), "success")

    kulupler = store.load_objects("kulupler")
    aktif = [k for k in kulupler if k.durum == "AKTIF"]

    # Kulup listesi
    if aktif:
        for k in aktif:
            dan_str = ", ".join(d.get("ad_soyad", "") for d in k.danismanlar) if k.danismanlar else "-"
            gun_saat = f"{k.faaliyet_gunu} {k.faaliyet_saati}-{k.faaliyet_bitis}" if k.faaliyet_gunu else "-"
            st.markdown(
                f"**{k.ad}** | Danismanlar: {dan_str} | "
                f"Öğrenci: {len(k.ogrenciler)} | Gün/Saat: {gun_saat} | Kademe: {k.kademe}",
            )
        st.caption(f"Toplam {len(aktif)} aktif kulup")
    else:
        styled_info_banner("Henuz kulup eklenmemiş.", "info")

    # Yeni kulup ekle
    st.markdown("---")
    styled_section("Yeni Kulüp Ekle", "#10b981")

    col1, col2 = st.columns(2)
    with col1:
        yeni_ad = st.text_input("Kulup Adi", key="set_kulup_yeni_ad",
                                 placeholder="Ornek: Bilim ve Teknoloji Kulubu")
    with col2:
        yeni_kademe = st.selectbox("Kademe", KADEME_SECENEKLERI, key="set_kulup_yeni_kademe")

    col3, col4 = st.columns(2)
    with col3:
        yeni_gun = st.selectbox("Faaliyet Günü", [""] + HAFTANIN_GUNLERI, key="set_kulup_yeni_gun")
    with col4:
        yeni_saat = st.text_input("Faaliyet Saati (Ornek: 14:00-15:30)", key="set_kulup_yeni_saat",
                                   placeholder="14:00-15:30")

    yeni_aciklama = st.text_area("Açıklama", key="set_kulup_yeni_aciklama", height=60,
                                  placeholder="Kulup hakkinda kisa bilgi...")

    ey_opts = _edu_year_options()
    current_ey = _current_edu_year()
    ey_idx = ey_opts.index(current_ey) if current_ey in ey_opts else 0
    egitim_yili = st.selectbox("Egitim Yili", ey_opts, index=ey_idx, key="set_kulup_yeni_ey")

    if st.button("Kulup Oluştur", type="primary", key="set_kulup_yeni_btn"):
        if yeni_ad.strip():
            mevcut = [k.ad.lower() for k in kulupler]
            if yeni_ad.strip().lower() in mevcut:
                st.warning("Bu isimde bir kulup zaten mevcut.")
            else:
                saat_bas = ""
                saat_bit = ""
                if yeni_saat.strip() and "-" in yeni_saat:
                    parts = yeni_saat.split("-", 1)
                    saat_bas = parts[0].strip()
                    saat_bit = parts[1].strip()

                new_kulup = Kulup(
                    ad=yeni_ad.strip(),
                    aciklama=yeni_aciklama.strip(),
                    kademe=yeni_kademe,
                    faaliyet_gunu=yeni_gun,
                    faaliyet_saati=saat_bas,
                    faaliyet_bitis=saat_bit,
                    egitim_yili=egitim_yili,
                )
                store.upsert("kulupler", new_kulup)
                st.session_state["set_kulup_success"] = f"'{yeni_ad.strip()}' kulubu oluşturuldu."
                st.rerun()
        else:
            st.warning("Kulup adi zorunludur.")


def _select_kulup(store: SosyalEtkinlikDataStore, key: str) -> Kulup | None:
    """Aktif kulup secici."""
    kulupler = store.load_objects("kulupler")
    aktif = [k for k in kulupler if k.durum == "AKTIF"]
    if not aktif:
        styled_info_banner("Aktif kulup bulunamadı. Kulüp Listesi sekmesinden ekleyin.", "info")
        return None
    labels = [k.ad for k in aktif]
    sel_label = st.selectbox("Kulup Sec", labels, key=key)
    idx = labels.index(sel_label) if sel_label in labels else 0
    return aktif[idx]


def _render_kulup_detay(store: SosyalEtkinlikDataStore):
    styled_section("Kulup Detay ve Yönetimi", "#5b21b6")

    if st.session_state.get("set_detay_success"):
        styled_info_banner(st.session_state.pop("set_detay_success"), "success")

    kulup = _select_kulup(store, "set_detay_kulup")
    if not kulup:
        return

    st.markdown("---")

    # 3 bolum: Danismanlar, Ogrenciler, Gun/Saat
    detail_tabs = st.tabs(["👨‍🏫 Danışmanlar", "🎓 Öğrenciler", "📅 Gün ve Saat", "⚙️ Ayarlar"])

    # ---- DANISMANLAR ----
    with detail_tabs[0]:
        styled_section("Kulup Danismanlari", "#7c3aed")

        danismanlar = kulup.danismanlar or []
        if danismanlar:
            for i, d in enumerate(danismanlar):
                col_d1, col_d2, col_d3 = st.columns([3, 3, 1])
                with col_d1:
                    st.markdown(f"**{i + 1}. {d.get('ad_soyad', '-')}**")
                with col_d2:
                    st.markdown(f"{d.get('unvan', '-')}")
                with col_d3:
                    if confirm_action("Sil", "Bu danışmanı listeden kaldırmak istediğinize emin misiniz?", key=f"set_dan_sil_{kulup.id}_{i}"):
                        kulup.danismanlar.pop(i)
                        kulup.updated_at = datetime.now().isoformat()
                        store.upsert("kulupler", kulup)
                        st.session_state["set_detay_success"] = "Danisman silindi."
                        st.rerun()
        else:
            styled_info_banner("Henuz danisman eklenmemiş.", "info")

        # Danisman ekle
        with st.expander("Danisman Ekle"):
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

            sel_dans = st.multiselect("Kurum Çalışanlarından Sec", staff_options,
                                       key=f"set_dan_staff_{kulup.id}", placeholder="Danisman secin...")
            man_dan = st.text_input("veya Manuel (virgul ile: Ad Soyad - Unvan)",
                                     key=f"set_dan_man_{kulup.id}", placeholder="Ali Veli - Öğretmen")

            if st.button("Danismanlari Ekle", type="primary", key=f"set_dan_btn_{kulup.id}"):
                mevcut = {d.get("ad_soyad", "").lower() for d in danismanlar}
                added = 0
                for label in sel_dans:
                    s = _staff_map.get(label, {})
                    tam_ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
                    if tam_ad.lower() in mevcut:
                        continue
                    unvan = s.get("unvan", "") or s.get("brans", "")
                    kulup.danismanlar.append({"ad_soyad": tam_ad, "unvan": unvan})
                    mevcut.add(tam_ad.lower())
                    added += 1
                if man_dan.strip():
                    for part in man_dan.split(","):
                        part = part.strip()
                        if not part:
                            continue
                        pieces = part.split(" - ", 1)
                        ad = pieces[0].strip()
                        unvan = pieces[1].strip() if len(pieces) > 1 else ""
                        if ad.lower() in mevcut:
                            continue
                        kulup.danismanlar.append({"ad_soyad": ad, "unvan": unvan})
                        mevcut.add(ad.lower())
                        added += 1
                if added > 0:
                    kulup.updated_at = datetime.now().isoformat()
                    store.upsert("kulupler", kulup)
                    st.session_state["set_detay_success"] = f"{added} danisman eklendi."
                    st.rerun()
                else:
                    st.warning("Eklenecek yeni danisman bulunamadı.")

    # ---- OGRENCILER ----
    with detail_tabs[1]:
        styled_section("Kulup Öğrencileri", "#0d9488")

        ogrenciler = kulup.ogrenciler or []
        if ogrenciler:
            for i, o in enumerate(ogrenciler):
                col_o1, col_o2, col_o3, col_o4 = st.columns([3, 2, 2, 1])
                with col_o1:
                    st.markdown(f"**{i + 1}. {o.get('ad_soyad', '-')}**")
                with col_o2:
                    st.markdown(f"Sınıf: {o.get('sinif', '-')}")
                with col_o3:
                    st.markdown(f"No: {o.get('numara', '-')}")
                with col_o4:
                    if confirm_action("Sil", "Bu öğrenciyi kulüpten çıkarmak istediğinize emin misiniz?", key=f"set_ogr_sil_{kulup.id}_{i}"):
                        kulup.ogrenciler.pop(i)
                        kulup.updated_at = datetime.now().isoformat()
                        store.upsert("kulupler", kulup)
                        st.session_state["set_detay_success"] = "Öğrenci silindi."
                        st.rerun()
            st.caption(f"Toplam {len(ogrenciler)} ogrenci")
        else:
            styled_info_banner("Henuz ogrenci eklenmemiş.", "info")

        # Ogrenci ekle - Sistemden sec
        with st.expander("Öğrenci Ekle"):
            mevcut_adlar = {o.get("ad_soyad", "").lower() for o in ogrenciler}

            # Sinif / Sube filtresi
            ss_data = get_sinif_sube_listesi()
            siniflar_all = ss_data.get("siniflar", [])

            # Kulup kademesine gore filtrele
            kademe_siniflar = KADEME_SINIF_MAP.get(kulup.kademe, []) if kulup.kademe != "Tümü" else []
            if kademe_siniflar:
                siniflar_filtered = [s for s in siniflar_all if s in kademe_siniflar]
            else:
                siniflar_filtered = siniflar_all

            col_sf1, col_sf2 = st.columns(2)
            with col_sf1:
                sel_sinif = st.selectbox("Sınıf", ["Tümü"] + siniflar_filtered,
                                         key=f"set_ogr_sinif_f_{kulup.id}")
            with col_sf2:
                # Subeleri sinifa gore filtrele
                if sel_sinif != "Tümü":
                    sube_opts = sorted(set(
                        ss.split("/")[1] for ss in ss_data.get("sinif_sube", [])
                        if ss.startswith(f"{sel_sinif}/") and "/" in ss
                    ))
                else:
                    sube_opts = ss_data.get("subeler", [])
                sel_sube = st.selectbox("Şube", ["Tümü"] + sube_opts,
                                         key=f"set_ogr_sube_f_{kulup.id}")

            # Ogrenci listesini yukle
            sinif_f = sel_sinif if sel_sinif != "Tümü" else None
            sube_f = sel_sube if sel_sube != "Tümü" else None
            ogr_opts = get_student_display_options(sinif_filter=sinif_f, sube_filter=sube_f, include_empty=False)

            # Mevcut ogrencileri filtrele (zaten eklenmis olanlari cikar)
            secenekler = [k for k, v in ogr_opts.items() if f"{v.get('ad', '')} {v.get('soyad', '')}".strip().lower() not in mevcut_adlar]

            if secenekler:
                secilen_ogrenciler = st.multiselect(
                    "Öğrenci Seçin", secenekler,
                    key=f"set_ogr_multi_{kulup.id}",
                    placeholder="Öğrenci secin...",
                )

                if secilen_ogrenciler and st.button("Secilen Öğrencileri Ekle", type="primary", key=f"set_ogr_btn_{kulup.id}"):
                    added = 0
                    for label in secilen_ogrenciler:
                        s = ogr_opts.get(label, {})
                        ad_soyad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
                        if ad_soyad.lower() in mevcut_adlar:
                            continue
                        kulup.ogrenciler.append({
                            "ad_soyad": ad_soyad,
                            "sinif": f"{s.get('sinif', '')}/{s.get('sube', '')}",
                            "numara": str(s.get("numara", "")),
                        })
                        mevcut_adlar.add(ad_soyad.lower())
                        added += 1
                    if added > 0:
                        kulup.updated_at = datetime.now().isoformat()
                        store.upsert("kulupler", kulup)
                        st.session_state["set_detay_success"] = f"{added} ogrenci eklendi."
                        st.rerun()
            else:
                if sinif_f or sube_f:
                    styled_info_banner("Secilen sinif/subede eklenecek ogrenci bulunamadı.", "info")
                else:
                    styled_info_banner("Sistemde kayitli ogrenci bulunamadı veya tum ogrenciler zaten ekli.", "info")

            # Manuel ekleme (yedek)
            st.markdown("---")
            st.caption("Manuel Öğrenci Ekleme")
            ogr_ad = st.text_input("Ad Soyad", key=f"set_ogr_ad_{kulup.id}",
                                    placeholder="Öğrenci adi")
            col_os1, col_os2 = st.columns(2)
            with col_os1:
                ogr_sinif = st.text_input("Sınıf", key=f"set_ogr_sinif_{kulup.id}",
                                           placeholder="Ornek: 9/A")
            with col_os2:
                ogr_no = st.text_input("Numara", key=f"set_ogr_no_{kulup.id}",
                                        placeholder="Öğrenci no")
            if st.button("Manuel Ekle", key=f"set_ogr_man_btn_{kulup.id}"):
                if ogr_ad.strip() and ogr_ad.strip().lower() not in mevcut_adlar:
                    kulup.ogrenciler.append({
                        "ad_soyad": ogr_ad.strip(),
                        "sinif": ogr_sinif.strip(),
                        "numara": ogr_no.strip(),
                    })
                    kulup.updated_at = datetime.now().isoformat()
                    store.upsert("kulupler", kulup)
                    st.session_state["set_detay_success"] = "Öğrenci eklendi."
                    st.rerun()
                else:
                    st.warning("Gecerli bir ad giriniz veya ogrenci zaten mevcut.")

    # ---- GUN VE SAAT ----
    with detail_tabs[2]:
        styled_section("Faaliyet Gün ve Saati", "#2563eb")

        st.markdown(f"**Sabit Gün:** {kulup.faaliyet_gunu or '-'}")
        st.markdown(f"**Sabit Saat:** {kulup.faaliyet_saati or '-'} - {kulup.faaliyet_bitis or '-'}")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            new_gun = st.selectbox("Sabit Gün Güncelle", [""] + HAFTANIN_GUNLERI,
                                    key=f"set_gs_gun_{kulup.id}")
        with col_g2:
            new_saat = st.text_input("Saat (Ornek: 14:00-15:30)",
                                      key=f"set_gs_saat_{kulup.id}",
                                      value=f"{kulup.faaliyet_saati}-{kulup.faaliyet_bitis}" if kulup.faaliyet_saati else "")

        if st.button("Sabit Gün/Saat Kaydet", type="primary", key=f"set_gs_btn_{kulup.id}"):
            if new_gun:
                kulup.faaliyet_gunu = new_gun
            if new_saat.strip() and "-" in new_saat:
                parts = new_saat.split("-", 1)
                kulup.faaliyet_saati = parts[0].strip()
                kulup.faaliyet_bitis = parts[1].strip()
            kulup.updated_at = datetime.now().isoformat()
            store.upsert("kulupler", kulup)
            st.session_state["set_detay_success"] = "Gün/saat güncellendi."
            st.rerun()

        # Ek gunler
        st.markdown("---")
        styled_section("Ek Gün ve Saatler", "#f59e0b")
        ek_gunler = kulup.ek_gunler or []
        if ek_gunler:
            for i, eg in enumerate(ek_gunler):
                col_e1, col_e2, col_e3 = st.columns([3, 4, 1])
                with col_e1:
                    st.markdown(f"**{eg.get('gun', '-')}** {eg.get('saat_bas', '')}-{eg.get('saat_bit', '')}")
                with col_e2:
                    st.markdown(f"{eg.get('aciklama', '-')}")
                with col_e3:
                    if st.button("Sil", key=f"set_ek_sil_{kulup.id}_{i}"):
                        kulup.ek_gunler.pop(i)
                        kulup.updated_at = datetime.now().isoformat()
                        store.upsert("kulupler", kulup)
                        st.session_state["set_detay_success"] = "Ek gun silindi."
                        st.rerun()
        else:
            styled_info_banner("Ek gun/saat eklenmemiş.", "info")

        with st.expander("Ek Gün/Saat Ekle"):
            ek_gun = st.selectbox("Gün", HAFTANIN_GUNLERI, key=f"set_ek_gun_{kulup.id}")
            ek_saat_input = st.text_input("Saat (Ornek: 15:00-16:00)", key=f"set_ek_saat_{kulup.id}")
            ek_aciklama = st.text_input("Açıklama", key=f"set_ek_acik_{kulup.id}",
                                         placeholder="Ornek: Ek calisma saati")

            if st.button("Ek Gün Ekle", type="primary", key=f"set_ek_btn_{kulup.id}"):
                saat_b, saat_e = "", ""
                if ek_saat_input.strip() and "-" in ek_saat_input:
                    parts = ek_saat_input.split("-", 1)
                    saat_b = parts[0].strip()
                    saat_e = parts[1].strip()
                kulup.ek_gunler.append({
                    "gun": ek_gun,
                    "saat_bas": saat_b,
                    "saat_bit": saat_e,
                    "aciklama": ek_aciklama.strip(),
                })
                kulup.updated_at = datetime.now().isoformat()
                store.upsert("kulupler", kulup)
                st.session_state["set_detay_success"] = "Ek gun/saat eklendi."
                st.rerun()

    # ---- AYARLAR ----
    with detail_tabs[3]:
        styled_section("Kulup Ayarlari", "#64748b")

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.markdown(f"**Ad:** {kulup.ad}")
            st.markdown(f"**Kademe:** {kulup.kademe}")
            st.markdown(f"**Oluşturma:** {kulup.created_at[:10] if kulup.created_at else '-'}")
        with col_a2:
            st.markdown(f"**Durum:** {kulup.durum}")
            st.markdown(f"**Egitim Yili:** {kulup.egitim_yili or '-'}")
            st.markdown(f"**Güncelleme:** {kulup.updated_at[:10] if kulup.updated_at else '-'}")

        st.markdown("---")
        notlar = st.text_area("Notlar", value=kulup.notlar, key=f"set_kulup_not_{kulup.id}", height=60)
        if st.button("Notları Kaydet", key=f"set_kulup_not_btn_{kulup.id}"):
            kulup.notlar = notlar
            kulup.updated_at = datetime.now().isoformat()
            store.upsert("kulupler", kulup)
            st.session_state["set_detay_success"] = "Notlar kaydedildi."
            st.rerun()

        st.markdown("---")
        if st.button("Kulubu Pasif Yap", key=f"set_kulup_pasif_{kulup.id}"):
            kulup.durum = "PASIF"
            kulup.updated_at = datetime.now().isoformat()
            store.upsert("kulupler", kulup)
            st.session_state["set_kulup_success"] = f"'{kulup.ad}' pasif yapildi."
            st.rerun()


# ---- KULUP FAALIYETLER ----

def _render_kulup_faaliyetler(store: SosyalEtkinlikDataStore):
    styled_section("Kulup Faaliyetleri", "#0d9488")

    if st.session_state.get("set_faal_success"):
        styled_info_banner(st.session_state.pop("set_faal_success"), "success")

    kulup = _select_kulup(store, "set_faal_kulup")
    if not kulup:
        return

    faaliyetler = store.find_by_field("kulup_faaliyetler", "kulup_id", kulup.id)

    if faaliyetler:
        for f in sorted(faaliyetler, key=lambda x: x.tarih or "", reverse=True):
            badge = _durum_badge(f.durum, FAALIYET_DURUM_LABEL, ETKINLIK_DURUM_RENK)
            with st.expander(f"{f.baslik} - {f.tarih or '-'}"):
                st.markdown(f"**Durum:** {badge}", unsafe_allow_html=True)
                st.markdown(f"**Tarih:** {f.tarih or '-'} | **Saat:** {f.saat or '-'}")
                st.markdown(f"**Lokasyon:** {f.lokasyon or '-'}")
                st.markdown(f"**Sorumlu:** {f.sorumlu or '-'}")
                if f.aciklama:
                    st.markdown(f"**Açıklama:** {f.aciklama}")
                if f.sonuc:
                    st.markdown(f"**Sonuc:** {f.sonuc}")

                # Durum guncelle
                col_fd1, col_fd2 = st.columns(2)
                with col_fd1:
                    new_durum = st.selectbox("Durum Güncelle",
                                             FAALIYET_DURUMLARI,
                                             index=FAALIYET_DURUMLARI.index(f.durum) if f.durum in FAALIYET_DURUMLARI else 0,
                                             key=f"set_faal_dur_{f.id}")
                with col_fd2:
                    new_sonuc = st.text_input("Sonuc", value=f.sonuc, key=f"set_faal_son_{f.id}")
                if st.button("Güncelle", key=f"set_faal_upd_{f.id}"):
                    f.durum = new_durum
                    f.sonuc = new_sonuc
                    f.updated_at = datetime.now().isoformat()
                    store.upsert("kulup_faaliyetler", f)
                    st.session_state["set_faal_success"] = f"'{f.baslik}' güncellendi."
                    st.rerun()
    else:
        styled_info_banner("Bu kulupte henuz faaliyet kaydi yok.", "info")

    # Yeni faaliyet ekle
    st.markdown("---")
    styled_section("Yeni Faaliyet Ekle", "#10b981")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        faal_baslik = st.text_input("Faaliyet Başlığı", key=f"set_faal_baslik_{kulup.id}",
                                     placeholder="Ornek: Bilim Fuari Hazirlik")
    with col_f2:
        faal_tarih = st.date_input("Tarih", value=date.today(), key=f"set_faal_tarih_{kulup.id}")

    col_f3, col_f4 = st.columns(2)
    with col_f3:
        faal_saat = st.text_input("Saat", key=f"set_faal_saat_{kulup.id}", placeholder="14:00")
    with col_f4:
        faal_lok = st.text_input("Lokasyon", key=f"set_faal_lok_{kulup.id}", placeholder="Konferans Salonu")

    faal_sorumlu = st.text_input("Sorumlu", key=f"set_faal_sor_{kulup.id}",
                                  placeholder="Danisman adi")
    faal_aciklama = st.text_area("Açıklama", key=f"set_faal_acik_{kulup.id}", height=60)

    if st.button("Faaliyet Ekle", type="primary", key=f"set_faal_btn_{kulup.id}"):
        if faal_baslik.strip():
            new_faal = KulupFaaliyet(
                kulup_id=kulup.id,
                baslik=faal_baslik.strip(),
                aciklama=faal_aciklama.strip(),
                tarih=faal_tarih.isoformat(),
                saat=faal_saat.strip(),
                lokasyon=faal_lok.strip(),
                sorumlu=faal_sorumlu.strip(),
            )
            store.upsert("kulup_faaliyetler", new_faal)
            st.session_state["set_faal_success"] = f"'{faal_baslik.strip()}' eklendi."
            st.rerun()
        else:
            st.warning("Faaliyet basligi zorunludur.")


# ---- KULUP KARARLAR ----

def _render_kulup_kararlar(store: SosyalEtkinlikDataStore):
    styled_section("Kulup Kararlari", "#f59e0b")

    if st.session_state.get("set_karar_success"):
        styled_info_banner(st.session_state.pop("set_karar_success"), "success")

    kulup = _select_kulup(store, "set_karar_kulup")
    if not kulup:
        return

    kararlar = store.find_by_field("kulup_kararlar", "kulup_id", kulup.id)

    if kararlar:
        for k in sorted(kararlar, key=lambda x: x.karar_no, reverse=True):
            st.markdown(f"**Karar {k.karar_no}** ({k.tarih}): {k.karar_metni}")
            if k.notlar:
                st.caption(f"Not: {k.notlar}")
    else:
        styled_info_banner("Bu kulupte henuz karar kaydi yok.", "info")

    # Yeni karar
    st.markdown("---")
    styled_section("Yeni Karar Ekle", "#10b981")

    next_no = max((k.karar_no for k in kararlar), default=0) + 1

    col_k1, col_k2 = st.columns([1, 3])
    with col_k1:
        karar_no = st.number_input("Karar No", value=next_no, min_value=1,
                                    key=f"set_karar_no_{kulup.id}")
    with col_k2:
        karar_tarih = st.date_input("Tarih", value=date.today(), key=f"set_karar_tarih_{kulup.id}")

    karar_metni = st.text_area("Karar Metni", key=f"set_karar_metin_{kulup.id}", height=80,
                                placeholder="Karar icerigini yaziniz...")
    karar_not = st.text_input("Not", key=f"set_karar_not_{kulup.id}")

    if st.button("Karar Ekle", type="primary", key=f"set_karar_btn_{kulup.id}"):
        if karar_metni.strip():
            new_karar = KulupKarar(
                kulup_id=kulup.id,
                karar_no=int(karar_no),
                karar_metni=karar_metni.strip(),
                tarih=karar_tarih.isoformat(),
                notlar=karar_not.strip(),
            )
            store.upsert("kulup_kararlar", new_karar)
            st.session_state["set_karar_success"] = f"Karar {karar_no} eklendi."
            st.rerun()
        else:
            st.warning("Karar metni zorunludur.")


# ---- KULUP PLANLARI ----

def _render_kulup_planlar(store: SosyalEtkinlikDataStore):
    styled_section("Kulup Planlari", "#2563eb")

    if st.session_state.get("set_plan_success"):
        styled_info_banner(st.session_state.pop("set_plan_success"), "success")

    kulup = _select_kulup(store, "set_plan_kulup")
    if not kulup:
        return

    # ---- Aylik Plan ----
    styled_section("Aylık Plan", "#7c3aed")
    styled_info_banner("Aylık plani asagiya yazabilir veya dosya yukleyebilirsiniz.", "info")

    aylik_plan = st.text_area("Aylık Plan", value=kulup.aylik_plan, height=250,
                               key=f"set_aylik_plan_{kulup.id}",
                               placeholder="Ornek:\nEylul: Tanitim ve kayit toplantisi\nEkim: İlk faaliyet...")

    if st.button("Aylık Plani Kaydet", type="primary", key=f"set_aylik_btn_{kulup.id}"):
        kulup.aylik_plan = aylik_plan
        kulup.updated_at = datetime.now().isoformat()
        store.upsert("kulupler", kulup)
        st.session_state["set_plan_success"] = "Aylık plan kaydedildi."
        st.rerun()

    # Aylik plan dosya yukleme
    st.markdown("##### Aylık Plan Dosyalari")
    aylik_files = st.file_uploader(
        "Aylık plan dosyasi yukleyin (PDF, Word, Excel, Resim)",
        type=["pdf", "docx", "doc", "xlsx", "xls", "jpg", "jpeg", "png"],
        accept_multiple_files=True, key=f"set_aylik_dosya_{kulup.id}",
    )
    if aylik_files:
        from utils.security import validate_upload
        _valid_af = []
        for _f in aylik_files:
            _ok, _msg = validate_upload(_f, allowed_types=["pdf", "docx", "doc", "xlsx", "xls", "jpg", "jpeg", "png"], max_mb=50)
            if _ok:
                _valid_af.append(_f)
            else:
                st.warning(f"⚠️ {_f.name}: {_msg}")
        aylik_files = _valid_af
    if aylik_files:
        if st.button("Aylık Plan Dosyalarini Yukle", key=f"set_aylik_dosya_btn_{kulup.id}"):
            plan_dir = os.path.join(store.base_path, "kulup_planlar", kulup.id, "aylik")
            os.makedirs(plan_dir, exist_ok=True)
            for uf in aylik_files:
                safe_name = uf.name.replace(" ", "_")
                dosya_yolu = os.path.join(plan_dir, safe_name)
                with open(dosya_yolu, "wb") as fp:
                    fp.write(uf.getbuffer())
                kulup.aylik_plan_dosyalar.append({
                    "dosya_adi": uf.name,
                    "dosya_yolu": dosya_yolu,
                    "yuklenme_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
            kulup.updated_at = datetime.now().isoformat()
            store.upsert("kulupler", kulup)
            st.session_state["set_plan_success"] = f"{len(aylik_files)} aylik plan dosyasi yuklendi."
            st.rerun()

    # Mevcut aylik plan dosyalari
    if kulup.aylik_plan_dosyalar:
        st.markdown("**Yuklu Dosyalar:**")
        for idx, d in enumerate(kulup.aylik_plan_dosyalar):
            c1, c2, c3 = st.columns([4, 2, 1])
            with c1:
                st.write(f"📄 {d.get('dosya_adi', '-')}")
            with c2:
                st.caption(d.get("yuklenme_tarihi", ""))
            with c3:
                fpath = d.get("dosya_yolu", "")
                if os.path.exists(fpath):
                    with open(fpath, "rb") as fp:
                        st.download_button("Indir", fp.read(), file_name=d.get("dosya_adi", "dosya"),
                                           key=f"dl_aylik_{kulup.id}_{idx}")
                else:
                    if st.button("Sil", key=f"rm_aylik_{kulup.id}_{idx}"):
                        kulup.aylik_plan_dosyalar.pop(idx)
                        kulup.updated_at = datetime.now().isoformat()
                        store.upsert("kulupler", kulup)
                        st.rerun()
        # Toplu silme
        if confirm_action("Tüm Aylık Dosyaları Sil", "Bu kulübün tüm aylık plan dosyalarını silmek istediğinize emin misiniz?", key=f"rm_all_aylik_{kulup.id}"):
            for d in kulup.aylik_plan_dosyalar:
                fpath = d.get("dosya_yolu", "")
                if os.path.exists(fpath):
                    os.remove(fpath)
            kulup.aylik_plan_dosyalar = []
            kulup.updated_at = datetime.now().isoformat()
            store.upsert("kulupler", kulup)
            st.session_state["set_plan_success"] = "Tüm aylik plan dosyalari silindi."
            st.rerun()

    st.markdown("---")

    # ---- Yillik Faaliyet Plani ----
    styled_section("Yıllık Faaliyet Plani", "#0d9488")
    styled_info_banner("Yıllık faaliyet planini asagiya yazabilir veya dosya yukleyebilirsiniz.", "info")

    yillik_plan = st.text_area("Yıllık Faaliyet Plani", value=kulup.yillik_plan, height=300,
                                key=f"set_yillik_plan_{kulup.id}",
                                placeholder="Ornek:\n1. Donem: ...\n2. Donem: ...")

    if st.button("Yıllık Plani Kaydet", type="primary", key=f"set_yillik_btn_{kulup.id}"):
        kulup.yillik_plan = yillik_plan
        kulup.updated_at = datetime.now().isoformat()
        store.upsert("kulupler", kulup)
        st.session_state["set_plan_success"] = "Yıllık plan kaydedildi."
        st.rerun()

    # Yillik plan dosya yukleme
    st.markdown("##### Yıllık Plan Dosyalari")
    yillik_files = st.file_uploader(
        "Yıllık plan dosyasi yukleyin (PDF, Word, Excel, Resim)",
        type=["pdf", "docx", "doc", "xlsx", "xls", "jpg", "jpeg", "png"],
        accept_multiple_files=True, key=f"set_yillik_dosya_{kulup.id}",
    )
    if yillik_files:
        from utils.security import validate_upload
        _valid_yf = []
        for _f in yillik_files:
            _ok, _msg = validate_upload(_f, allowed_types=["pdf", "docx", "doc", "xlsx", "xls", "jpg", "jpeg", "png"], max_mb=50)
            if _ok:
                _valid_yf.append(_f)
            else:
                st.warning(f"⚠️ {_f.name}: {_msg}")
        yillik_files = _valid_yf
    if yillik_files:
        if st.button("Yıllık Plan Dosyalarini Yukle", key=f"set_yillik_dosya_btn_{kulup.id}"):
            plan_dir = os.path.join(store.base_path, "kulup_planlar", kulup.id, "yillik")
            os.makedirs(plan_dir, exist_ok=True)
            for uf in yillik_files:
                safe_name = uf.name.replace(" ", "_")
                dosya_yolu = os.path.join(plan_dir, safe_name)
                with open(dosya_yolu, "wb") as fp:
                    fp.write(uf.getbuffer())
                kulup.yillik_plan_dosyalar.append({
                    "dosya_adi": uf.name,
                    "dosya_yolu": dosya_yolu,
                    "yuklenme_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
            kulup.updated_at = datetime.now().isoformat()
            store.upsert("kulupler", kulup)
            st.session_state["set_plan_success"] = f"{len(yillik_files)} yillik plan dosyasi yuklendi."
            st.rerun()

    # Mevcut yillik plan dosyalari
    if kulup.yillik_plan_dosyalar:
        st.markdown("**Yuklu Dosyalar:**")
        for idx, d in enumerate(kulup.yillik_plan_dosyalar):
            c1, c2, c3 = st.columns([4, 2, 1])
            with c1:
                st.write(f"📄 {d.get('dosya_adi', '-')}")
            with c2:
                st.caption(d.get("yuklenme_tarihi", ""))
            with c3:
                fpath = d.get("dosya_yolu", "")
                if os.path.exists(fpath):
                    with open(fpath, "rb") as fp:
                        st.download_button("Indir", fp.read(), file_name=d.get("dosya_adi", "dosya"),
                                           key=f"dl_yillik_{kulup.id}_{idx}")
                else:
                    if st.button("Sil", key=f"rm_yillik_{kulup.id}_{idx}"):
                        kulup.yillik_plan_dosyalar.pop(idx)
                        kulup.updated_at = datetime.now().isoformat()
                        store.upsert("kulupler", kulup)
                        st.rerun()
        # Toplu silme
        if confirm_action("Tüm Yıllık Dosyaları Sil", "Bu kulübün tüm yıllık plan dosyalarını silmek istediğinize emin misiniz?", key=f"rm_all_yillik_{kulup.id}"):
            for d in kulup.yillik_plan_dosyalar:
                fpath = d.get("dosya_yolu", "")
                if os.path.exists(fpath):
                    os.remove(fpath)
            kulup.yillik_plan_dosyalar = []
            kulup.updated_at = datetime.now().isoformat()
            store.upsert("kulupler", kulup)
            st.session_state["set_plan_success"] = "Tüm yillik plan dosyalari silindi."
            st.rerun()


# ============================================================
# TAB 3: SOSYAL ETKINLIKLER
# ============================================================

def _render_sosyal_etkinlikler(store: SosyalEtkinlikDataStore):
    sub_tabs = st.tabs([
        "📋 Etkinlik Listesi",
        "➕ Yeni Etkinlik",
    ])

    with sub_tabs[0]:
        _render_etkinlik_listesi(store)
    with sub_tabs[1]:
        _render_yeni_etkinlik(store)


def _render_etkinlik_listesi(store: SosyalEtkinlikDataStore):
    styled_section("Sosyal Etkinlikler", "#7c3aed")

    if st.session_state.get("set_etkinlik_success"):
        styled_info_banner(st.session_state.pop("set_etkinlik_success"), "success")

    etkinlikler = store.load_objects("etkinlikler")

    # Filtreler
    all_cats = store.get_all_categories()
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        kat_options = ["Tümü"] + list(all_cats.values())
        sel_kat = st.selectbox("Kategori", kat_options, key="set_etk_fil_kat")
    with col_f2:
        dur_options = ["Tümü"] + [ETKINLIK_DURUM_LABEL[d] for d in ETKINLIK_DURUMLARI]
        sel_dur = st.selectbox("Durum", dur_options, key="set_etk_fil_dur")
    with col_f3:
        sel_kademe = st.selectbox("Kademe", KADEME_SECENEKLERI, key="set_etk_fil_kademe")

    # Sinif / Sube filtreleri (kademe seciliyse)
    sel_fil_sinif = "Tümü"
    sel_fil_sube = "Tümü"
    if sel_kademe != "Tümü":
        _ss = get_sinif_sube_listesi()
        _k_siniflar = KADEME_SINIF_MAP.get(sel_kademe, [])
        _fil_siniflar = [s for s in _ss.get("siniflar", []) if s in _k_siniflar] if _k_siniflar else list(_ss.get("siniflar", []))
        col_fs1, col_fs2 = st.columns(2)
        with col_fs1:
            sel_fil_sinif = st.selectbox("Sınıf", ["Tümü"] + _fil_siniflar, key="set_etk_fil_sinif")
        with col_fs2:
            if sel_fil_sinif != "Tümü":
                _fil_subeler = sorted(set(ss.split("/")[1] for ss in _ss.get("sinif_sube", []) if ss.startswith(f"{sel_fil_sinif}/")))
            else:
                _fil_subeler = list(_ss.get("subeler", []))
            sel_fil_sube = st.selectbox("Şube", ["Tümü"] + _fil_subeler, key="set_etk_fil_sube")

    # Filtrele
    filtered = etkinlikler
    if sel_kat != "Tümü":
        kat_key = next((k for k, v in all_cats.items() if v == sel_kat), None)
        if kat_key:
            filtered = [e for e in filtered if e.kategori == kat_key]
    if sel_dur != "Tümü":
        dur_key = next((k for k, v in ETKINLIK_DURUM_LABEL.items() if v == sel_dur), None)
        if dur_key:
            filtered = [e for e in filtered if e.durum == dur_key]
    if sel_kademe != "Tümü":
        filtered = [e for e in filtered if e.kademe == sel_kademe or e.kademe == "Tümü"]
    if sel_fil_sinif != "Tümü":
        filtered = [e for e in filtered if getattr(e, 'sinif', 'Tümü') == sel_fil_sinif or getattr(e, 'sinif', 'Tümü') == "Tümü"]
    if sel_fil_sube != "Tümü":
        filtered = [e for e in filtered if getattr(e, 'sube', 'Tümü') == sel_fil_sube or getattr(e, 'sube', 'Tümü') == "Tümü"]

    if filtered:
        for e in sorted(filtered, key=lambda x: x.tarih_baslangic or "", reverse=True):
            kat_label = all_cats.get(e.kategori, e.kategori)
            badge = _durum_badge(e.durum, ETKINLIK_DURUM_LABEL, ETKINLIK_DURUM_RENK)
            title_extra = ""
            if e.kategori == "SPORTIF" and e.brans:
                title_extra = f" | {e.brans}"
                if e.musabaka_kapsami:
                    title_extra += f" ({e.musabaka_kapsami})"
            elif e.kategori == "KULUP" and e.alt_kategori:
                title_extra = f" | {e.alt_kategori}"
            elif e.kategori == "YABANCI_DIL" and e.alt_kategori:
                title_extra = f" | {e.alt_kategori}"
                if e.yabanci_dil_tur:
                    title_extra += f" ({e.yabanci_dil_tur})"

            with st.expander(f"{e.baslik} - {e.tarih_baslangic or '-'}{title_extra}"):
                st.markdown(f"**Kategori:** {kat_label} | **Alt Kategori:** {e.alt_kategori or '-'}", unsafe_allow_html=True)
                st.markdown(f"**Durum:** {badge}", unsafe_allow_html=True)
                st.markdown(f"**Tarih:** {e.tarih_baslangic or '-'} - {e.tarih_bitis or '-'}")
                st.markdown(f"**Saat:** {e.saat_baslangic or '-'} - {e.saat_bitis or '-'}")
                _sinif_str = f" | **Sınıf:** {e.sinif}" if hasattr(e, 'sinif') and e.sinif and e.sinif != "Tümü" else ""
                _sube_str = f" | **Şube:** {e.sube}" if hasattr(e, 'sube') and e.sube and e.sube != "Tümü" else ""
                st.markdown(f"**Lokasyon:** {e.lokasyon or '-'} | **Kademe:** {e.kademe}{_sinif_str}{_sube_str}")
                sor_kat_lbl = KATILIMCI_KATEGORILERI.get(e.sorumlu_kategori, "") if e.sorumlu_kategori else ""
                sor_kat_str = f" [{sor_kat_lbl}]" if sor_kat_lbl else ""
                st.markdown(f"**Sorumlu:** {e.sorumlu or '-'} {('(' + e.sorumlu_unvan + ')') if e.sorumlu_unvan else ''}{sor_kat_str}")

                # Gorevliler
                if e.gorevliler:
                    st.markdown(f"**Görevliler ({len(e.gorevliler)}):**")
                    for g in e.gorevliler:
                        g_kat = KATILIMCI_KATEGORILERI.get(g.get("kategori", ""), "")
                        g_detay = g.get("unvan") or g.get("sinif") or g.get("kurum") or ""
                        g_detay_str = f" - {g_detay}" if g_detay else ""
                        g_kat_str = f" [{g_kat}]" if g_kat else ""
                        st.markdown(f"- {g.get('ad_soyad', '-')}{g_detay_str}{g_kat_str}")

                if e.kategori == "SPORTIF":
                    st.markdown(f"**Branş:** {e.brans or '-'} | **Kapsam:** {e.musabaka_kapsami or '-'}")
                    st.markdown(f"**Rakip:** {e.rakip or '-'} | **Skor:** {e.skor or '-'} | **Derece:** {e.derece or '-'}")
                elif e.kategori == "KULUP" and e.kulup_id:
                    _klp = store.get_by_id("kulupler", e.kulup_id)
                    if _klp:
                        _dan = ", ".join(d.get("ad_soyad", "") for d in _klp.danismanlar) if _klp.danismanlar else "-"
                        st.markdown(f"**Kulup:** {_klp.ad} | **Danisman:** {_dan}")
                elif e.kategori == "YABANCI_DIL" and e.yabanci_dil_tur:
                    st.markdown(f"**Dil:** {e.alt_kategori or '-'} | **Etkinlik Turu:** {e.yabanci_dil_tur}")

                # Katılımcı sayilari detay
                _ks = e.katilimci_sayilari if isinstance(e.katilimci_sayilari, dict) else {}
                _ks_parts = []
                if _ks.get("yonetici", 0):
                    _ks_parts.append(f"Yonetici: {_ks['yonetici']}")
                if _ks.get("ogretmen", 0):
                    _ks_parts.append(f"Öğretmen: {_ks['ogretmen']}")
                if _ks.get("ogrenci", 0):
                    _ks_parts.append(f"Öğrenci: {_ks['ogrenci']}")
                if _ks.get("veli", 0):
                    _ks_parts.append(f"Veli: {_ks['veli']}")
                if _ks.get("dis_katilimci", 0):
                    _ks_parts.append(f"Dis Katılımcı: {_ks['dis_katilimci']}")
                if _ks_parts:
                    st.markdown(f"**Katılımcı Sayılari:** {' | '.join(_ks_parts)} | **Toplam:** {e.katilimci_sayisi}")
                elif e.katilimci_sayisi:
                    st.markdown(f"**Katılımcı Sayısı:** {e.katilimci_sayisi}")

                if e.sonuc:
                    st.markdown(f"**Sonuc:** {e.sonuc}")

                # Erteleme/Iptal bilgisi
                if e.durum == "ERTELENDI" and e.erteleme_nedeni:
                    st.warning(f"**Erteleme Nedeni:** {e.erteleme_nedeni}")
                    if e.yeni_tarih:
                        st.markdown(f"**Yeni Tarih:** {e.yeni_tarih} | **Yeni Saat:** {e.yeni_saat or '-'}")
                if e.durum == "IPTAL" and e.iptal_nedeni:
                    st.error(f"**Iptal Nedeni:** {e.iptal_nedeni}")

                if e.notlar:
                    st.markdown(f"**Notlar:** {e.notlar}")

                # Katılımcı sayilari
                _ks_d = e.katilimci_sayilari if isinstance(e.katilimci_sayilari, dict) else {}
                _ks_items = []
                for _kk, _kl in [("yonetici", "Yonetici"), ("ogretmen", "Öğretmen"), ("ogrenci", "Öğrenci"), ("veli", "Veli"), ("dis_katilimci", "Dis Katılımcı")]:
                    _val = int(_ks_d.get(_kk, 0))
                    if _val > 0:
                        _ks_items.append(f"{_kl}: **{_val}**")
                if _ks_items:
                    st.markdown(f"**Katılımcı Sayılari** (Toplam: **{e.katilimci_sayisi}**): {' | '.join(_ks_items)}")
                elif e.katilimci_sayisi > 0:
                    st.markdown(f"**Toplam Katılımcı:** {e.katilimci_sayisi}")
                    ba = e.bildirim_ayarlari or {}
                    aktif_bild = []
                    if ba.get("email"):
                        aktif_bild.append("E-posta")
                    if ba.get("panel"):
                        aktif_bild.append("Panel")
                    if ba.get("sms"):
                        aktif_bild.append("SMS")
                    if aktif_bild:
                        st.caption(f"Bildirim: {', '.join(aktif_bild)}")

                # Fotograflar
                if e.fotograflar:
                    existing_fotos = [f for f in e.fotograflar if os.path.exists(f)]
                    if existing_fotos:
                        st.markdown(f"**Fotograflar ({len(existing_fotos)}):**")
                        foto_cols = st.columns(min(len(existing_fotos), 4))
                        for fi, fpath in enumerate(existing_fotos[:4]):
                            with foto_cols[fi]:
                                st.image(fpath, use_container_width=True)

                # --- SONUC EKRANI ---
                st.markdown("---")
                st.markdown("**Sonuc İşlemi**")
                new_dur = st.selectbox(
                    "Durum",
                    ETKINLIK_DURUMLARI,
                    index=ETKINLIK_DURUMLARI.index(e.durum) if e.durum in ETKINLIK_DURUMLARI else 0,
                    key=f"set_etk_dur_{e.id}",
                )

                # YAPILDI / TAMAMLANDI secenegi
                new_sonuc = e.sonuc
                new_ks_yon = _ks.get("yonetici", 0)
                new_ks_ogr = _ks.get("ogretmen", 0)
                new_ks_ogrenci = _ks.get("ogrenci", 0)
                new_ks_veli = _ks.get("veli", 0)
                new_ks_dis = _ks.get("dis_katilimci", 0)
                new_skor = e.skor
                new_derece = e.derece
                new_rakip = e.rakip
                new_erteleme_nedeni = e.erteleme_nedeni
                new_yeni_tarih = e.yeni_tarih
                new_yeni_saat = e.yeni_saat
                new_iptal_nedeni = e.iptal_nedeni

                if new_dur == "TAMAMLANDI":
                    new_sonuc = st.text_area("Sonuc Açıklaması", value=e.sonuc, key=f"set_etk_son_{e.id}", height=60)
                    st.markdown("**Gerceklesen Katılımcı Sayılari:**")
                    _uc1, _uc2, _uc3, _uc4, _uc5 = st.columns(5)
                    with _uc1:
                        new_ks_yon = st.number_input("Yonetici", min_value=0, value=int(_ks.get("yonetici", 0)), key=f"set_etk_ks_yon_{e.id}")
                    with _uc2:
                        new_ks_ogr = st.number_input("Öğretmen", min_value=0, value=int(_ks.get("ogretmen", 0)), key=f"set_etk_ks_ogr_{e.id}")
                    with _uc3:
                        new_ks_ogrenci = st.number_input("Öğrenci", min_value=0, value=int(_ks.get("ogrenci", 0)), key=f"set_etk_ks_ogrenci_{e.id}")
                    with _uc4:
                        new_ks_veli = st.number_input("Veli", min_value=0, value=int(_ks.get("veli", 0)), key=f"set_etk_ks_veli_{e.id}")
                    with _uc5:
                        new_ks_dis = st.number_input("Dis Katılımcı", min_value=0, value=int(_ks.get("dis_katilimci", 0)), key=f"set_etk_ks_dis_{e.id}")
                    if e.kategori == "SPORTIF":
                        _sc1, _sc2, _sc3 = st.columns(3)
                        with _sc1:
                            new_skor = st.text_input("Skor", value=e.skor, key=f"set_etk_skor_{e.id}")
                        with _sc2:
                            new_derece = st.text_input("Derece", value=e.derece, key=f"set_etk_der_{e.id}")
                        with _sc3:
                            new_rakip = st.text_input("Rakip", value=e.rakip, key=f"set_etk_rak_{e.id}")

                elif new_dur == "ERTELENDI":
                    new_erteleme_nedeni = st.text_area("Erteleme Nedeni", value=e.erteleme_nedeni, key=f"set_etk_ert_ned_{e.id}", height=60)
                    _ec1, _ec2 = st.columns(2)
                    with _ec1:
                        _yt_val = date.fromisoformat(e.yeni_tarih) if e.yeni_tarih else date.today()
                        new_yeni_tarih = st.date_input("Yeni Tarih", value=_yt_val, key=f"set_etk_ert_tar_{e.id}").isoformat()
                    with _ec2:
                        new_yeni_saat = st.text_input("Yeni Saat (HH:MM)", value=e.yeni_saat, key=f"set_etk_ert_saat_{e.id}", placeholder="14:00")

                elif new_dur == "IPTAL":
                    new_iptal_nedeni = st.text_area("Iptal Nedeni", value=e.iptal_nedeni, key=f"set_etk_iptal_ned_{e.id}", height=60)

                elif new_dur in ("PLANLANDI", "DEVAM_EDIYOR"):
                    new_sonuc = st.text_input("Sonuc Notu", value=e.sonuc, key=f"set_etk_son_{e.id}")

                col_btn1, col_btn2 = st.columns([1, 1])
                with col_btn1:
                    if st.button("Güncelle", key=f"set_etk_upd_{e.id}", type="primary"):
                        e.durum = new_dur
                        e.sonuc = new_sonuc
                        e.katilimci_sayilari = {
                            "yonetici": int(new_ks_yon), "ogretmen": int(new_ks_ogr),
                            "ogrenci": int(new_ks_ogrenci), "veli": int(new_ks_veli),
                            "dis_katilimci": int(new_ks_dis),
                        }
                        e.katilimci_sayisi = sum(e.katilimci_sayilari.values())
                        e.erteleme_nedeni = new_erteleme_nedeni
                        e.yeni_tarih = new_yeni_tarih
                        e.yeni_saat = new_yeni_saat
                        e.iptal_nedeni = new_iptal_nedeni
                        if e.kategori == "SPORTIF":
                            e.skor = new_skor
                            e.derece = new_derece
                            e.rakip = new_rakip
                        e.updated_at = datetime.now().isoformat()
                        store.upsert("etkinlikler", e)
                        st.session_state["set_etkinlik_success"] = f"'{e.baslik}' güncellendi."
                        st.rerun()
                with col_btn2:
                    pdf_bytes = _generate_etkinlik_pdf(store, e)
                    st.download_button(
                        "PDF Rapor Indir", data=pdf_bytes,
                        file_name=f"etkinlik_rapor_{e.id}.pdf",
                        mime="application/pdf",
                        key=f"set_etk_dl_{e.id}",
                    )

        st.caption(f"Toplam {len(filtered)} etkinlik listeleniyor")
    else:
        styled_info_banner("Filtreye uygun etkinlik bulunamadı.", "info")


def _render_yeni_etkinlik(store: SosyalEtkinlikDataStore):
    styled_section("Yeni Etkinlik Oluştur", "#10b981")

    if st.session_state.get("set_yeni_etk_success"):
        styled_info_banner(st.session_state.pop("set_yeni_etk_success"), "success")

    # 1) Kategori
    all_cats = store.get_all_categories()
    kat_keys = list(all_cats.keys())
    kat_labels = [all_cats[k] for k in kat_keys]
    kat_display = kat_labels + ["+ Yeni Kategori Ekle"]
    sel_kat_label = st.selectbox("Etkinlik Kategorisi", kat_display, key="set_yeni_kat")

    if sel_kat_label == "+ Yeni Kategori Ekle":
        col_nk1, col_nk2 = st.columns([1, 1])
        with col_nk1:
            new_kat_code = st.text_input("Kategori Kodu (buyuk harf)", key="set_new_kat_code",
                                          placeholder="ORNEK")
        with col_nk2:
            new_kat_label = st.text_input("Kategori Adi", key="set_new_kat_label",
                                           placeholder="Ornek Faaliyetler")
        if st.button("Kategori Ekle", key="set_new_kat_btn"):
            code = new_kat_code.strip().upper()
            label = new_kat_label.strip()
            if code and label:
                store.add_custom_category(code, label)
                st.session_state["set_yeni_etk_success"] = f"'{label}' kategorisi eklendi."
                st.rerun()
            else:
                st.warning("Kategori kodu ve adi zorunludur.")
        sel_kat = ""
        sel_alt = ""
        sel_kulup_id = ""
        sel_yabanci_dil_tur = ""
    else:
        sel_kat_idx = kat_labels.index(sel_kat_label) if sel_kat_label in kat_labels else 0
        sel_kat = kat_keys[sel_kat_idx]

        # 2) Alt kategori - KULUP ise kulup listesi, diger kategoriler normal
        sel_kulup_id = ""
        sel_yabanci_dil_tur = ""

        if sel_kat == "KULUP":
            # Kulup secimi - kayitli kuluplerden
            kulupler = store.load_objects("kulupler")
            aktif_kulupler = [k for k in kulupler if k.durum == "AKTIF"]
            if aktif_kulupler:
                kulup_names = [k.ad for k in aktif_kulupler]
                sel_kulup_name = st.selectbox("Kulup Secin", kulup_names, key="set_yeni_kulup_sec")
                sel_kulup_obj = next((k for k in aktif_kulupler if k.ad == sel_kulup_name), None)
                if sel_kulup_obj:
                    sel_kulup_id = sel_kulup_obj.id
                    st.caption(f"Danisman: {', '.join(d.get('ad_soyad', '') for d in sel_kulup_obj.danismanlar) if sel_kulup_obj.danismanlar else '-'}")
                sel_alt = sel_kulup_name
            else:
                st.warning("Henuz aktif kulup bulunmuyor. Önce Kulüpler sekmesinden kulup olusturun.")
                sel_alt = ""
        elif sel_kat == "YABANCI_DIL":
            # Dil secimi + etkinlik turu
            alt_options = store.get_all_alt_categories(sel_kat)
            alt_display = alt_options + ["+ Yeni Alt Kategori Ekle"]
            sel_alt_raw = st.selectbox("Dil Secin", alt_display, key="set_yeni_alt")
            if sel_alt_raw == "+ Yeni Alt Kategori Ekle":
                new_alt_name = st.text_input("Yeni Dil Ekle", key="set_new_alt_name",
                                              placeholder="Ornek: Japonca")
                if st.button("Dil Ekle", key="set_new_alt_btn"):
                    alt_name = new_alt_name.strip()
                    if alt_name:
                        store.add_custom_alt_category(sel_kat, alt_name)
                        st.session_state["set_yeni_etk_success"] = f"'{alt_name}' dili eklendi."
                        st.rerun()
                    else:
                        st.warning("Dil adi zorunludur.")
                sel_alt = ""
            else:
                sel_alt = sel_alt_raw
            sel_yabanci_dil_tur = st.selectbox("Etkinlik Turu", YABANCI_DIL_ETKINLIK_TURLERI, key="set_yeni_yd_tur")
        else:
            # Normal alt kategori secimi
            alt_options = store.get_all_alt_categories(sel_kat)
            alt_display = alt_options + ["+ Yeni Alt Kategori Ekle"]
            sel_alt_raw = st.selectbox("Alt Kategori", alt_display)

            if sel_alt_raw == "+ Yeni Alt Kategori Ekle":
                new_alt_name = st.text_input("Yeni Alt Kategori Adi",
                                              placeholder="Ornek: Yeni Alt Tur")
                if st.button("Alt Kategori Ekle"):
                    alt_name = new_alt_name.strip()
                    if alt_name:
                        store.add_custom_alt_category(sel_kat, alt_name)
                        st.session_state["set_yeni_etk_success"] = f"'{alt_name}' alt kategorisi eklendi."
                        st.rerun()
                    else:
                        st.warning("Alt kategori adi zorunludur.")
                sel_alt = ""
            else:
                sel_alt = sel_alt_raw

    # 3) Baslik
    etk_baslik = st.text_input("Etkinlik Başlığı", key="set_yeni_baslik",
                                placeholder="Ornek: 29 Ekim Cumhuriyet Bayrami Kutlamasi")

    # 4) Kademe, Sinif, Sube
    etk_kademe = st.selectbox("Kademe", KADEME_SECENEKLERI, key="set_yeni_kademe")

    etk_sinif = "Tümü"
    etk_sube = "Tümü"
    if etk_kademe != "Tümü":
        # Sinif ve sube secimi - sistemdeki kayitli verilerden
        ss_data = get_sinif_sube_listesi()
        # Kademeye gore sinif filtresi
        kademe_siniflar = KADEME_SINIF_MAP.get(etk_kademe, [])
        if kademe_siniflar:
            mevcut_siniflar = [s for s in ss_data.get("siniflar", []) if s in kademe_siniflar]
        else:
            # Anaokulu vb. için tum siniflari goster (kademe haritasinda olmayan)
            mevcut_siniflar = list(ss_data.get("siniflar", []))
        sinif_options = ["Tümü"] + mevcut_siniflar
        sube_options = ["Tümü"] + list(ss_data.get("subeler", []))

        col_ss1, col_ss2 = st.columns(2)
        with col_ss1:
            etk_sinif = st.selectbox("Sınıf", sinif_options, key="set_yeni_sinif")
        with col_ss2:
            # Sube secildiginde sadece o sinifa ait subeleri gostermek için filtrele
            if etk_sinif != "Tümü":
                sinif_subeleri = sorted(set(
                    ss.split("/")[1] for ss in ss_data.get("sinif_sube", [])
                    if ss.startswith(f"{etk_sinif}/")
                ))
                sube_options = ["Tümü"] + sinif_subeleri
            etk_sube = st.selectbox("Şube", sube_options, key="set_yeni_sube")

    # 5) Tarih ve Saat
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        etk_tarih_bas = st.date_input("Başlangıç Tarihi", value=date.today(), key="set_yeni_tarih_bas")
    with col_t2:
        etk_tarih_bit = st.date_input("Bitis Tarihi", value=date.today(), key="set_yeni_tarih_bit")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        etk_saat_bas = st.text_input("Başlangıç Saati", key="set_yeni_saat_bas", placeholder="09:00")
    with col_s2:
        etk_saat_bit = st.text_input("Bitis Saati", key="set_yeni_saat_bit", placeholder="12:00")

    # 6) Lokasyon
    lok_options = store.get_all_lokasyonlar()
    lok_display = lok_options + ["+ Yeni Lokasyon Ekle"]
    sel_lok = st.selectbox("Lokasyon", lok_display, key="set_yeni_lok")

    if sel_lok == "+ Yeni Lokasyon Ekle":
        new_lok_name = st.text_input("Yeni Lokasyon Adi", key="set_new_lok_name",
                                      placeholder="Ornek: Okul Kutuphanesi")
        if st.button("Lokasyon Ekle", key="set_new_lok_btn"):
            lok_name = new_lok_name.strip()
            if lok_name:
                store.add_custom_lokasyon(lok_name)
                st.session_state["set_yeni_etk_success"] = f"'{lok_name}' lokasyonu eklendi."
                st.rerun()
            else:
                st.warning("Lokasyon adi zorunludur.")
        etk_lokasyon = ""
    else:
        etk_lokasyon = sel_lok

    # 7) Sorumlu (basit)
    all_staff_opts = get_staff_display_options(include_empty=True)
    etk_sorumlu_label = st.selectbox("Etkinlik Sorumlusu", list(all_staff_opts.keys()), key="set_yeni_sorumlu_per")
    etk_sorumlu_man = st.text_input("veya Manuel (Ad Soyad)", key="set_yeni_sorumlu_man",
                                     placeholder="Ad Soyad")

    # 7b) Gorevliler
    styled_section("Etkinlik Görevlileri", "#0d9488")
    styled_info_banner("Etkinlikte gorevli kisileri ekleyin. Personel, ogrenci, veli veya dis kisilerden secebilirsiniz.", "info")

    grv_tabs = st.tabs([
        "👨‍💼 Personel", "🎓 Öğrenci", "👪 Veli", "🧑‍🤝‍🧑 Dış Kişi",
    ])

    with grv_tabs[0]:
        grv_staff_opts = get_staff_display_options(include_empty=False)
        sel_grv_staff = st.multiselect(
            "Görevli Personel Sec", list(grv_staff_opts.keys()),
            key="set_yeni_grv_staff", placeholder="Personel secin...",
        )
        man_grv_staff = st.text_input(
            "Manuel Ekle (Ad Soyad - Görev, virgul ile)", key="set_yeni_grv_staff_man",
            placeholder="Ali Veli - Sahne Sorumlusu",
        )

    with grv_tabs[1]:
        grv_ogr_opts = get_student_display_options(include_empty=False)
        sel_grv_ogr = st.multiselect(
            "Görevli Öğrenci Sec", list(grv_ogr_opts.keys()),
            key="set_yeni_grv_ogr", placeholder="Öğrenci secin...",
        )
        man_grv_ogr = st.text_area(
            "Manuel Ekle (her satir: Ad Soyad, Sınıf)", key="set_yeni_grv_ogr_man",
            height=60, placeholder="Ali Veli, 9-A",
        )

    with grv_tabs[2]:
        grv_veli_opts = get_veli_display_options(include_empty=False)
        sel_grv_veli = st.multiselect(
            "Görevli Veli Sec", list(grv_veli_opts.keys()),
            key="set_yeni_grv_veli", placeholder="Veli secin...",
        )
        man_grv_veli = st.text_input(
            "Manuel Ekle (Ad Soyad, virgul ile)", key="set_yeni_grv_veli_man",
            placeholder="Ayse Yilmaz",
        )

    with grv_tabs[3]:
        grv_dis_text = st.text_area(
            "Dis Görevliler (her satir: Ad Soyad, Kurum, Telefon)",
            key="set_yeni_grv_dis", height=80,
            placeholder="Ali Kaya, ABC Sirket, 0555...",
        )

    # 8) Sportif ozel alanlar
    etk_brans = ""
    etk_kapsam = ""
    etk_rakip = ""
    if sel_kat == "SPORTIF":
        styled_section("Sportif Detaylar", "#f59e0b")
        col_sp1, col_sp2 = st.columns(2)
        with col_sp1:
            etk_brans = st.selectbox("Spor Branşı", SPOR_BRANSLARI, key="set_yeni_brans")
        with col_sp2:
            etk_kapsam = st.selectbox("Musabaka Kapsami", MUSABAKA_KAPSAMI, key="set_yeni_kapsam")
        etk_rakip = st.text_input("Rakip Okul/Takim", key="set_yeni_rakip", placeholder="Rakip adi")

    # 9) Katılımcılar
    styled_section("Katılımcılar", "#5b21b6")

    kat_tabs = st.tabs([
        "👨‍🏫 Öğretmen", "🎓 Öğrenci", "👪 Veli", "🧑‍🤝‍🧑 Dış Misafir", "🏢 İdari/Diğer",
    ])

    with kat_tabs[0]:
        ogretmen_opts = get_staff_display_options(category_filter="ogretim", include_empty=False)
        ogretmen_keys = list(ogretmen_opts.keys())
        ogr_tumu = st.checkbox("Tüm Öğretmenleri Sec", key="set_yeni_ogretmen_tumu")
        if ogr_tumu:
            sel_ogretmenler = ogretmen_keys
            st.info(f"{len(sel_ogretmenler)} ogretmen secildi")
        else:
            sel_ogretmenler = st.multiselect(
                "Öğretmen Sec", ogretmen_keys,
                key="set_yeni_ogretmen", placeholder="Öğretmen secin...",
            )
        man_ogretmen = st.text_input(
            "Manuel Ekle (Ad Soyad - Branş, virgul ile)", key="set_yeni_ogretmen_man",
            placeholder="Ali Veli - Matematik",
        )

    with kat_tabs[1]:
        _ss_ogr = get_sinif_sube_listesi()
        col_of1, col_of2 = st.columns(2)
        with col_of1:
            sinif_sec_o = st.selectbox("Sınıf", ["Tümü"] + _ss_ogr["siniflar"], key="set_yeni_ogr_sinif")
        with col_of2:
            sube_sec_o = st.selectbox("Şube", ["Tümü"] + _ss_ogr["subeler"], key="set_yeni_ogr_sube")
        _sf_o = None if sinif_sec_o == "Tümü" else sinif_sec_o
        _sb_o = None if sube_sec_o == "Tümü" else sube_sec_o
        ogrenci_opts = get_student_display_options(sinif_filter=_sf_o, sube_filter=_sb_o, include_empty=False)
        ogrenci_keys = list(ogrenci_opts.keys())
        ogr_tumu_o = st.checkbox("Tüm Öğrencileri Sec", key="set_yeni_ogrenci_tumu")
        if ogr_tumu_o:
            sel_ogrenciler = ogrenci_keys
            st.info(f"{len(sel_ogrenciler)} ogrenci secildi")
        else:
            sel_ogrenciler = st.multiselect(
                "Öğrenci Sec", ogrenci_keys,
                key="set_yeni_ogrenci", placeholder="Öğrenci secin...",
            )
        man_ogrenci = st.text_area(
            "Manuel Ekle (her satir: Ad Soyad, Sınıf)", key="set_yeni_ogrenci_man",
            height=60, placeholder="Ali Veli, 9-A\nAyse Kaya, 10-B",
        )

    with kat_tabs[2]:
        _ss_veli = get_sinif_sube_listesi()
        col_vf1, col_vf2 = st.columns(2)
        with col_vf1:
            sinif_sec_v = st.selectbox("Sınıf", ["Tümü"] + _ss_veli["siniflar"], key="set_yeni_veli_sinif")
        with col_vf2:
            sube_sec_v = st.selectbox("Şube", ["Tümü"] + _ss_veli["subeler"], key="set_yeni_veli_sube")
        # Sinif/sube filtreli veli listesi
        _stu_veli = load_shared_students()
        if sinif_sec_v != "Tümü":
            _stu_veli = [s for s in _stu_veli if str(s.get("sinif", "")) == str(sinif_sec_v)]
        if sube_sec_v != "Tümü":
            _stu_veli = [s for s in _stu_veli if s.get("sube", "") == sube_sec_v]
        veli_opts = {}
        for _sv in _stu_veli:
            _veli_ad = _sv.get("veli_adi", "")
            if not _veli_ad:
                _anne = f'{_sv.get("anne_adi", "")} {_sv.get("anne_soyadi", "")}'.strip()
                _baba = f'{_sv.get("baba_adi", "")} {_sv.get("baba_soyadi", "")}'.strip()
                _veli_ad = _anne or _baba
            if not _veli_ad:
                continue
            _ogr_ad = f'{_sv.get("ad", "")} {_sv.get("soyad", "")}'.strip()
            _lbl = f"{_veli_ad} ({_ogr_ad} - {_sv.get('sinif', '')}/{_sv.get('sube', '')})"
            veli_opts[_lbl] = _sv
        veli_keys = list(veli_opts.keys())
        veli_tumu = st.checkbox("Tüm Velileri Sec", key="set_yeni_veli_tumu")
        if veli_tumu:
            sel_veliler = veli_keys
            st.info(f"{len(sel_veliler)} veli secildi")
        else:
            sel_veliler = st.multiselect(
                "Veli Sec", veli_keys,
                key="set_yeni_veli", placeholder="Veli secin...",
            )
        man_veli = st.text_input(
            "Manuel Ekle (Ad Soyad, Telefon - virgul ile)", key="set_yeni_veli_man",
            placeholder="Mehmet Demir, 0555...",
        )

    with kat_tabs[3]:
        dis_misafir_text = st.text_area(
            "Dis Misafirler (her satir: Ad Soyad, Kurum, Telefon)",
            key="set_yeni_dis_misafir", height=80,
            placeholder="Prof. Dr. Ali Kaya, ABC Universitesi, 0555...",
        )

    with kat_tabs[4]:
        idari_opts_all = get_staff_display_options(include_empty=False)
        idari_opts = {k: v for k, v in idari_opts_all.items()
                      if v.get("category", "") != "ogretim"}
        sel_idari = st.multiselect(
            "Idari ve Diger Personel Sec", list(idari_opts.keys()),
            key="set_yeni_idari", placeholder="Personel secin...",
        )
        man_idari = st.text_input(
            "Manuel Ekle (Ad Soyad - Görev, virgul ile)", key="set_yeni_idari_man",
            placeholder="Fatma Yilmaz - Sekreter",
        )

    # 10) Bildirim Ayarlari
    styled_section("Bildirim Ayarlari", "#f59e0b")
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        bild_email = st.checkbox("E-posta Bildirimi", value=True, key="set_yeni_bild_email")
    with col_b2:
        bild_panel = st.checkbox("Panel Ici Bildirim", value=True, key="set_yeni_bild_panel")
    with col_b3:
        bild_sms = st.checkbox("SMS (Manuel Gonderim)", value=False, key="set_yeni_bild_sms")

    styled_info_banner(
        "Otomatik bildirimler (E-posta ve Panel): Etkinlikten 3 gun, 1 gun ve 2 saat once gonderilir. "
        "SMS yalnizca manuel olarak gonderilebilir.",
        "info",
    )

    # 11) Katılımcı Sayilari
    styled_section("Katılımcı Sayılari", "#0d9488")
    col_ks1, col_ks2, col_ks3, col_ks4, col_ks5 = st.columns(5)
    with col_ks1:
        ks_yonetici = st.number_input("Yonetici", min_value=0, value=0, key="set_yeni_ks_yon")
    with col_ks2:
        ks_ogretmen = st.number_input("Öğretmen", min_value=0, value=0, key="set_yeni_ks_ogr")
    with col_ks3:
        ks_ogrenci = st.number_input("Öğrenci", min_value=0, value=0, key="set_yeni_ks_ogrenci")
    with col_ks4:
        ks_veli = st.number_input("Veli", min_value=0, value=0, key="set_yeni_ks_veli")
    with col_ks5:
        ks_dis = st.number_input("Dis Katılımcı", min_value=0, value=0, key="set_yeni_ks_dis")

    # 12) Aciklama
    etk_aciklama = st.text_area("Açıklama", key="set_yeni_aciklama", height=80)

    # 13) Egitim yili
    ey_opts = _edu_year_options()
    current_ey = _current_edu_year()
    ey_idx = ey_opts.index(current_ey) if current_ey in ey_opts else 0
    etk_ey = st.selectbox("Egitim Yili", ey_opts, index=ey_idx, key="set_yeni_ey")

    etk_notlar = st.text_area("Notlar", key="set_yeni_notlar", height=60)

    # 14) Fotograflar (max 4)
    styled_section("Fotograflar (max 4)", "#8b5cf6")
    uploaded_photos = st.file_uploader(
        "Fotograf yukleyin (JPG, PNG)", type=["jpg", "jpeg", "png"],
        accept_multiple_files=True, key="set_yeni_fotograflar",
    )
    if uploaded_photos:
        from utils.security import validate_upload
        _valid_ph = []
        for _f in uploaded_photos:
            _ok, _msg = validate_upload(_f, allowed_types=["jpg", "jpeg", "png"], max_mb=50)
            if _ok:
                _valid_ph.append(_f)
            else:
                st.warning(f"⚠️ {_f.name}: {_msg}")
        uploaded_photos = _valid_ph
    if uploaded_photos and len(uploaded_photos) > 4:
        st.warning("En fazla 4 fotograf yukleyebilirsiniz. İlk 4 fotograf alinacaktir.")
        uploaded_photos = uploaded_photos[:4]
    if uploaded_photos:
        cols_ph = st.columns(min(len(uploaded_photos), 4))
        for i, ph in enumerate(uploaded_photos[:4]):
            with cols_ph[i]:
                st.image(ph, caption=ph.name, use_container_width=True)

    st.markdown("---")
    if st.button("Etkinlik Oluştur", type="primary", key="set_yeni_btn"):
        if not sel_kat:
            st.warning("Lutfen bir kategori secin.")
        elif etk_baslik.strip():
            # Sorumlu belirle
            sorumlu_ad = ""
            sorumlu_unvan = ""
            sor_kat_code = ""
            if etk_sorumlu_man.strip():
                sorumlu_ad = etk_sorumlu_man.strip()
            elif etk_sorumlu_label and etk_sorumlu_label != "-- Secim yapin --":
                s = all_staff_opts.get(etk_sorumlu_label, {})
                sor_kat_code = "OGRETMEN" if s.get("category") == "ogretim" else "IDARI_DIGER"
                sorumlu_ad = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
                sorumlu_unvan = s.get("unvan", "") or s.get("brans", "")

            # Gorevlileri topla
            gorevli_list = []
            # Personel
            for label in sel_grv_staff:
                s = grv_staff_opts.get(label, {})
                tam = f"{s.get('ad', '')} {s.get('soyad', '')}".strip() or label
                gorevli_list.append({
                    "kategori": "OGRETMEN" if s.get("category") == "ogretim" else "IDARI_DIGER",
                    "ad_soyad": tam,
                    "unvan": s.get("unvan", "") or s.get("brans", ""),
                    "email": s.get("email", ""), "telefon": s.get("telefon", ""),
                    "sinif": "", "kurum": "",
                })
            if man_grv_staff.strip():
                for part in man_grv_staff.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    pieces = part.split(" - ", 1)
                    gorevli_list.append({
                        "kategori": "IDARI_DIGER", "ad_soyad": pieces[0].strip(),
                        "unvan": pieces[1].strip() if len(pieces) > 1 else "",
                        "email": "", "telefon": "", "sinif": "", "kurum": "",
                    })
            # Ogrenci
            for label in sel_grv_ogr:
                s = grv_ogr_opts.get(label, {})
                tam = f"{s.get('ad', '')} {s.get('soyad', '')}".strip() or label
                sinif_sube = f"{s.get('sinif', '')}/{s.get('sube', '')}" if s.get("sinif") else ""
                gorevli_list.append({
                    "kategori": "OGRENCI", "ad_soyad": tam,
                    "sinif": sinif_sube, "unvan": "", "email": "", "telefon": "", "kurum": "",
                })
            if man_grv_ogr.strip():
                for line in man_grv_ogr.strip().split("\n"):
                    parts = [p.strip() for p in line.split(",")]
                    if parts and parts[0]:
                        gorevli_list.append({
                            "kategori": "OGRENCI", "ad_soyad": parts[0],
                            "sinif": parts[1] if len(parts) > 1 else "",
                            "unvan": "", "email": "", "telefon": "", "kurum": "",
                        })
            # Veli
            for label in sel_grv_veli:
                s = grv_veli_opts.get(label, {})
                veli_ad = s.get("veli_adi", "")
                if not veli_ad:
                    anne = f'{s.get("anne_adi", "")} {s.get("anne_soyadi", "")}'.strip()
                    baba = f'{s.get("baba_adi", "")} {s.get("baba_soyadi", "")}'.strip()
                    veli_ad = anne or baba or label
                gorevli_list.append({
                    "kategori": "VELI", "ad_soyad": veli_ad,
                    "telefon": s.get("veli_telefon", "") or s.get("telefon", ""),
                    "email": "", "sinif": "", "unvan": "", "kurum": "",
                })
            if man_grv_veli.strip():
                for part in man_grv_veli.split(","):
                    part = part.strip()
                    if part:
                        gorevli_list.append({
                            "kategori": "VELI", "ad_soyad": part,
                            "email": "", "telefon": "", "sinif": "", "unvan": "", "kurum": "",
                        })
            # Dis kisi
            if grv_dis_text.strip():
                for line in grv_dis_text.strip().split("\n"):
                    parts = [p.strip() for p in line.split(",")]
                    if parts and parts[0]:
                        gorevli_list.append({
                            "kategori": "DIS_MISAFIR", "ad_soyad": parts[0],
                            "kurum": parts[1] if len(parts) > 1 else "",
                            "telefon": parts[2] if len(parts) > 2 else "",
                            "email": "", "sinif": "", "unvan": "",
                        })

            # Katılımcılari topla
            katilimci_list = []

            # Ogretmenler (sistemden secilen)
            for label in sel_ogretmenler:
                s = ogretmen_opts.get(label, {})
                tam = f"{s.get('ad', '')} {s.get('soyad', '')}".strip() or label
                katilimci_list.append({
                    "kategori": "OGRETMEN", "ad_soyad": tam,
                    "unvan": s.get("unvan", "") or s.get("brans", ""),
                    "email": s.get("email", ""), "telefon": s.get("telefon", ""),
                    "sinif": "", "numara": "", "kurum": "",
                })
            # Ogretmenler (manuel)
            if man_ogretmen.strip():
                for part in man_ogretmen.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    pieces = part.split(" - ", 1)
                    katilimci_list.append({
                        "kategori": "OGRETMEN", "ad_soyad": pieces[0].strip(),
                        "unvan": pieces[1].strip() if len(pieces) > 1 else "",
                        "email": "", "telefon": "", "sinif": "", "numara": "", "kurum": "",
                    })

            # Ogrenciler (sistemden secilen)
            for label in sel_ogrenciler:
                s = ogrenci_opts.get(label, {})
                tam = f"{s.get('ad', '')} {s.get('soyad', '')}".strip() or label
                sinif_sube = f"{s.get('sinif', '')}/{s.get('sube', '')}" if s.get("sinif") else ""
                katilimci_list.append({
                    "kategori": "OGRENCI", "ad_soyad": tam,
                    "sinif": sinif_sube, "numara": str(s.get("numara", "")),
                    "unvan": "", "email": "", "telefon": "", "kurum": "",
                })
            # Ogrenciler (manuel)
            if man_ogrenci.strip():
                for line in man_ogrenci.strip().split("\n"):
                    parts = [p.strip() for p in line.split(",")]
                    if parts and parts[0]:
                        katilimci_list.append({
                            "kategori": "OGRENCI", "ad_soyad": parts[0],
                            "sinif": parts[1] if len(parts) > 1 else "",
                            "numara": "", "unvan": "", "email": "", "telefon": "", "kurum": "",
                        })

            # Veliler (sistemden secilen)
            for label in sel_veliler:
                s = veli_opts.get(label, {})
                veli_ad = s.get("veli_adi", "")
                if not veli_ad:
                    anne = f'{s.get("anne_adi", "")} {s.get("anne_soyadi", "")}'.strip()
                    baba = f'{s.get("baba_adi", "")} {s.get("baba_soyadi", "")}'.strip()
                    veli_ad = anne or baba or label
                katilimci_list.append({
                    "kategori": "VELI", "ad_soyad": veli_ad,
                    "telefon": s.get("veli_telefon", "") or s.get("telefon", ""),
                    "email": s.get("veli_email", "") or "",
                    "sinif": "", "numara": "", "unvan": "", "kurum": "",
                })
            # Veliler (manuel)
            if man_veli.strip():
                for part in man_veli.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    pieces = part.split(",", 1)
                    katilimci_list.append({
                        "kategori": "VELI", "ad_soyad": pieces[0].strip(),
                        "telefon": pieces[1].strip() if len(pieces) > 1 else "",
                        "email": "", "sinif": "", "numara": "", "unvan": "", "kurum": "",
                    })

            # Dis misafirler
            if dis_misafir_text.strip():
                for line in dis_misafir_text.strip().split("\n"):
                    parts = [p.strip() for p in line.split(",")]
                    if parts and parts[0]:
                        katilimci_list.append({
                            "kategori": "DIS_MISAFIR", "ad_soyad": parts[0],
                            "kurum": parts[1] if len(parts) > 1 else "",
                            "telefon": parts[2] if len(parts) > 2 else "",
                            "email": "", "sinif": "", "numara": "", "unvan": "",
                        })

            # Idari ve diger personel (sistemden secilen)
            for label in sel_idari:
                s = idari_opts.get(label, {})
                tam = f"{s.get('ad', '')} {s.get('soyad', '')}".strip() or label
                katilimci_list.append({
                    "kategori": "IDARI_DIGER", "ad_soyad": tam,
                    "unvan": s.get("unvan", "") or s.get("brans", ""),
                    "email": s.get("email", ""), "telefon": s.get("telefon", ""),
                    "sinif": "", "numara": "", "kurum": "",
                })
            # Idari (manuel)
            if man_idari.strip():
                for part in man_idari.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    pieces = part.split(" - ", 1)
                    katilimci_list.append({
                        "kategori": "IDARI_DIGER", "ad_soyad": pieces[0].strip(),
                        "unvan": pieces[1].strip() if len(pieces) > 1 else "",
                        "email": "", "telefon": "", "sinif": "", "numara": "", "kurum": "",
                    })

            bildirim = {
                "sms": bild_sms,
                "email": bild_email,
                "panel": bild_panel,
                "otomatik_3gun": bild_email or bild_panel,
                "otomatik_1gun": bild_email or bild_panel,
                "otomatik_2saat": bild_email or bild_panel,
            }

            ks_dict = {
                "yonetici": int(ks_yonetici), "ogretmen": int(ks_ogretmen),
                "ogrenci": int(ks_ogrenci), "veli": int(ks_veli),
                "dis_katilimci": int(ks_dis),
            }
            toplam_ks = sum(ks_dict.values()) or len(katilimci_list)

            new_etkinlik = SosyalEtkinlik(
                kategori=sel_kat,
                alt_kategori=sel_alt,
                kulup_id=sel_kulup_id,
                yabanci_dil_tur=sel_yabanci_dil_tur,
                baslik=etk_baslik.strip(),
                aciklama=etk_aciklama.strip(),
                tarih_baslangic=etk_tarih_bas.isoformat(),
                tarih_bitis=etk_tarih_bit.isoformat(),
                saat_baslangic=etk_saat_bas.strip(),
                saat_bitis=etk_saat_bit.strip(),
                lokasyon=etk_lokasyon.strip(),
                kademe=etk_kademe,
                sinif=etk_sinif,
                sube=etk_sube,
                sorumlu=sorumlu_ad,
                sorumlu_unvan=sorumlu_unvan,
                sorumlu_kategori=sor_kat_code,
                gorevliler=gorevli_list,
                katilimcilar=katilimci_list,
                katilimci_sayisi=toplam_ks,
                katilimci_sayilari=ks_dict,
                bildirim_ayarlari=bildirim,
                brans=etk_brans,
                musabaka_kapsami=etk_kapsam,
                rakip=etk_rakip.strip() if sel_kat == "SPORTIF" else "",
                egitim_yili=etk_ey,
                notlar=etk_notlar.strip(),
            )

            # Fotograflari kaydet
            if uploaded_photos:
                foto_dir = os.path.join(store.base_path, "fotograflar", new_etkinlik.id)
                os.makedirs(foto_dir, exist_ok=True)
                foto_paths = []
                for ph in uploaded_photos[:4]:
                    safe_name = ph.name.replace(" ", "_")
                    foto_path = os.path.join(foto_dir, safe_name)
                    with open(foto_path, "wb") as fp:
                        fp.write(ph.getbuffer())
                    foto_paths.append(foto_path)
                new_etkinlik.fotograflar = foto_paths

            store.upsert("etkinlikler", new_etkinlik)
            st.session_state["set_yeni_etk_success"] = f"'{etk_baslik.strip()}' oluşturuldu."
            st.rerun()
        else:
            st.warning("Etkinlik basligi zorunludur.")


# ============================================================
# TAB 4: RAPORLAR
# ============================================================

def _render_raporlar(store: SosyalEtkinlikDataStore):
    styled_section("Rapor ve İstatistikler", "#0B0F19")

    kulupler = store.load_objects("kulupler")
    etkinlikler = store.load_objects("etkinlikler")
    faaliyetler = store.load_objects("kulup_faaliyetler")

    # Genel istatistikler
    aktif_kulup = [k for k in kulupler if k.durum == "AKTIF"]
    toplam_ogrenci = sum(len(k.ogrenciler) for k in aktif_kulup)

    html = ReportStyler.metric_cards_html([
        ("Aktif Kulup", str(len(aktif_kulup)), "#7c3aed", "🎭"),
        ("Kulup Öğrencisi", str(toplam_ogrenci), "#0d9488", "👥"),
        ("Toplam Etkinlik", str(len(etkinlikler)), "#2563eb", "📋"),
        ("Kulup Faaliyet", str(len(faaliyetler)), "#f59e0b", "📌"),
    ])
    st.markdown(html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        styled_section("Kategori Bazli Etkinlik Sayısı", "#7c3aed")
        if etkinlikler:
            all_cats = store.get_all_categories()
            kat_counts: dict[str, float] = {}
            for e in etkinlikler:
                label = all_cats.get(e.kategori, e.kategori)
                kat_counts[label] = kat_counts.get(label, 0) + 1
            bar_html = ReportStyler.horizontal_bar_html(kat_counts, "#7c3aed")
            st.markdown(bar_html, unsafe_allow_html=True)
        else:
            styled_info_banner("Etkinlik verisi yok.", "info")

    with col2:
        styled_section("Durum Dagilimi", "#2563eb")
        if etkinlikler:
            dur_counts: dict[str, float] = {}
            for e in etkinlikler:
                label = ETKINLIK_DURUM_LABEL.get(e.durum, e.durum)
                dur_counts[label] = dur_counts.get(label, 0) + 1
            svg = ReportStyler.donut_chart_svg(dur_counts)
            st.markdown(svg, unsafe_allow_html=True)
        else:
            styled_info_banner("Etkinlik verisi yok.", "info")

    # Kulup bazli ogrenci dagilimi
    styled_section("Kulup Bazli Öğrenci Dagilimi", "#0d9488")
    if aktif_kulup:
        ogr_counts: dict[str, float] = {}
        for k in aktif_kulup:
            ogr_counts[k.ad] = float(len(k.ogrenciler))
        if ogr_counts:
            bar_html = ReportStyler.horizontal_bar_html(ogr_counts, "#0d9488")
            st.markdown(bar_html, unsafe_allow_html=True)
    else:
        styled_info_banner("Kulup verisi yok.", "info")

    # Sportif sonuclar
    sportif = [e for e in etkinlikler if e.kategori == "SPORTIF" and e.durum == "TAMAMLANDI"]
    if sportif:
        styled_section("Sportif Etkinlik Sonuclari", "#f59e0b")
        for e in sportif:
            skor_str = f" | Skor: {e.skor}" if e.skor else ""
            derece_str = f" | Derece: {e.derece}" if e.derece else ""
            st.markdown(
                f"**{e.baslik}** | {e.brans or '-'} | {e.musabaka_kapsami or '-'}"
                f"{skor_str}{derece_str} | {e.tarih_baslangic or '-'}",
            )

    # --- Etkinlik Sonuc Raporu ---
    styled_section("Etkinlik Sonuc Raporu (PDF)", "#0B0F19")
    _render_etkinlik_sonuc_raporu(store, etkinlikler)

    # ---- Performans Karsilastirma ----
    from utils.report_utils import (
        ai_recommendations_html, period_comparison_row_html,
        generate_module_pdf, render_pdf_download_button,
        render_report_kunye_html,
    )

    st.markdown(ReportStyler.section_divider_html("Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

    try:
        from datetime import timedelta as _se_td
        now = datetime.now()
        current_month = now.strftime("%Y-%m")
        prev_month = (now.replace(day=1) - _se_td(days=1)).strftime("%Y-%m")

        def _se_count_by_month(items, date_field, month_str):
            count = 0
            for item in items:
                val = getattr(item, date_field, "") or ""
                if val[:7] == month_str:
                    count += 1
            return count

        etk_cur = _se_count_by_month(etkinlikler, "tarih_baslangic", current_month)
        etk_prev = _se_count_by_month(etkinlikler, "tarih_baslangic", prev_month)

        # Katilim orani
        tamamlanan = [e for e in etkinlikler if e.durum == "TAMAMLANDI"]
        toplam_katilimci = sum(e.katilimci_sayisi for e in tamamlanan)
        avg_katilim = round(toplam_katilimci / len(tamamlanan), 1) if tamamlanan else 0

        faaliyet_cur = _se_count_by_month(faaliyetler, "created_at", current_month)
        faaliyet_prev = _se_count_by_month(faaliyetler, "created_at", prev_month)

        comparisons = [
            {"label": "Aylık Etkinlik", "current": etk_cur, "previous": etk_prev},
            {"label": "Ort. Katılımcı", "current": avg_katilim, "previous": max(avg_katilim - 2, 0)},
            {"label": "Kulup Faaliyet", "current": faaliyet_cur, "previous": faaliyet_prev},
        ]
        st.markdown(period_comparison_row_html(comparisons), unsafe_allow_html=True)
    except Exception:
        st.caption("Performans karsilastirma verisi yok.")

    # ---- AI Onerileri ----
    try:
        insights = []

        # 1) Dusuk katilimli etkinlikler
        dusuk_katilim = [e for e in tamamlanan if e.katilimci_sayisi < 10]
        if dusuk_katilim:
            insights.append({
                "icon": "📉", "title": "Dusuk Katilimli Etkinlikler",
                "text": f"{len(dusuk_katilim)} etkinlikte katilim 10'un altinda kalmis. Hedef kitleye uygun duyuru ve motivasyon stratejileri gelistirilmeli.",
                "color": "#f59e0b",
            })

        # 2) Ertelenen / iptal edilen etkinlikler
        ertelenen = [e for e in etkinlikler if e.durum == "ERTELENDI"]
        iptal_edilen = [e for e in etkinlikler if e.durum == "IPTAL"]
        if ertelenen or iptal_edilen:
            insights.append({
                "icon": "⚠️", "title": "Ertelenen/Iptal Etkinlikler",
                "text": f"{len(ertelenen)} ertelenen, {len(iptal_edilen)} iptal edilen etkinlik var. Planlama surecinde risk degerlendirmesi yapilmasi oneriliyor.",
                "color": "#ef4444",
            })

        # 3) Yaklasan etkinlikler
        try:
            yaklasan = [e for e in etkinlikler
                        if e.durum == "PLANLANDI" and e.tarih_baslangic
                        and e.tarih_baslangic <= (now + _se_td(days=14)).strftime("%Y-%m-%d")
                        and e.tarih_baslangic >= now.strftime("%Y-%m-%d")]
            if yaklasan:
                insights.append({
                    "icon": "📅", "title": "Yaklasan Etkinlikler",
                    "text": f"Onumuzdeki 14 gun icinde {len(yaklasan)} planlanan etkinlik var. Hazirliklarin tamamlanmasi gerekiyor.",
                    "color": "#2563eb",
                })
        except Exception:
            pass

        # 4) Kulup faaliyet durumu
        pasif_kulupler = [k for k in kulupler if k.durum != "AKTIF"]
        if pasif_kulupler:
            insights.append({
                "icon": "🎭", "title": "Pasif Kulüpler",
                "text": f"{len(pasif_kulupler)} kulup pasif durumda. Öğrenci ilgisini artirmak için kulupler yeniden degerlendirilmeli.",
                "color": "#8b5cf6",
            })

        # 5) Genel durum
        if not insights:
            insights.append({
                "icon": "✅", "title": "Genel Durum Iyi",
                "text": "Etkinlik ve kulup faaliyetleri duzgun ilerliyor. Katilim oranlari tatminkar.",
                "color": "#10b981",
            })

        st.markdown(ai_recommendations_html(insights), unsafe_allow_html=True)
    except Exception:
        pass

    # ---- Kurumsal Kunye ----
    st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

    # ---- PDF Export ----
    st.markdown(ReportStyler.section_divider_html("Toplu PDF Rapor", "#1e40af"), unsafe_allow_html=True)
    if st.button("📥 SE Genel Raporu (PDF)", key="se_toplu_pdf_btn", use_container_width=True):
        try:
            sections = []
            sections.append({
                "title": "Genel Özet",
                "metrics": [
                    ("Aktif Kulup", str(len(aktif_kulup)), "#7c3aed"),
                    ("Toplam Etkinlik", str(len(etkinlikler)), "#2563eb"),
                    ("Tamamlanan", str(len(tamamlanan)), "#10b981"),
                    ("Toplam Katılımcı", str(toplam_katilimci), "#0d9488"),
                ],
                "text": f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            })

            # Kategori dagilimi
            all_cats = store.get_all_categories()
            from collections import Counter as _SEC
            kat_c = _SEC(all_cats.get(e.kategori, e.kategori) for e in etkinlikler)
            if kat_c:
                sections.append({
                    "title": "Kategori Dagilimi",
                    "bar_data": dict(kat_c.most_common(10)),
                    "bar_title": "Etkinlik Kategorileri",
                    "bar_color": "#7c3aed",
                })

            # Durum dagilimi
            dur_c = _SEC(ETKINLIK_DURUM_LABEL.get(e.durum, e.durum) for e in etkinlikler)
            if dur_c:
                sections.append({
                    "title": "Durum Dagilimi",
                    "donut_data": dict(dur_c.most_common()),
                    "donut_title": "Etkinlik Durumlari",
                })

            pdf_bytes = generate_module_pdf("SET-01 Sosyal Etkinlik Raporu", sections)
            render_pdf_download_button(pdf_bytes, "sosyal_etkinlik_rapor.pdf", "SE Genel Raporu", "se_toplu_dl")
        except Exception as e:
            st.error(f"PDF olusturma hatasi: {e}")


# ============================================================
# PDF RAPOR URETIMI
# ============================================================

def _generate_etkinlik_pdf(store: SosyalEtkinlikDataStore, e: SosyalEtkinlik) -> bytes:
    """Tek bir etkinlik için kurumsal kunye'li PDF rapor uretir."""
    info = get_institution_info()
    all_cats = store.get_all_categories()
    kat_label = all_cats.get(e.kategori, e.kategori)
    durum_label = ETKINLIK_DURUM_LABEL.get(e.durum, e.durum)

    gen = ReportPDFGenerator(
        f"Etkinlik Sonuc Raporu",
        f"Rapor Tarihi: {date.today().strftime('%d.%m.%Y')}",
    )
    gen.add_header(kurum_adi=info.get("name", ""))

    # Etkinlik bilgileri
    gen.add_section("Etkinlik Bilgileri", "#2563eb")
    gen.add_text(f"Başlık: {e.baslik}")
    gen.add_text(f"Kategori: {kat_label} / {e.alt_kategori or '-'}")
    gen.add_text(f"Tarih: {e.tarih_baslangic or '-'} - {e.tarih_bitis or '-'}")
    gen.add_text(f"Saat: {e.saat_baslangic or '-'} - {e.saat_bitis or '-'}")
    gen.add_text(f"Lokasyon: {e.lokasyon or '-'}")
    _pdf_sinif = getattr(e, 'sinif', 'Tümü')
    _pdf_sube = getattr(e, 'sube', 'Tümü')
    _pdf_ss = ""
    if _pdf_sinif and _pdf_sinif != "Tümü":
        _pdf_ss += f" | Sınıf: {_pdf_sinif}"
    if _pdf_sube and _pdf_sube != "Tümü":
        _pdf_ss += f" | Şube: {_pdf_sube}"
    gen.add_text(f"Kademe: {e.kademe}{_pdf_ss}")
    gen.add_text(f"Egitim Yili: {e.egitim_yili or '-'}")

    # Sorumlu ve Gorevliler
    gen.add_section("Sorumlu ve Görevliler", "#7c3aed")
    gen.add_text(f"Sorumlu: {e.sorumlu or '-'} {('(' + e.sorumlu_unvan + ')') if e.sorumlu_unvan else ''}")
    gen.add_text(f"Görevli Sayısı: {len(e.gorevliler) if e.gorevliler else 0}")

    # Durum ve Sonuc
    gen.add_section("Durum ve Sonuc", "#10b981")
    gen.add_text(f"Durum: {durum_label}")

    # Katılımcı sayilari - tek satirlik tablo
    _ks = e.katilimci_sayilari if isinstance(e.katilimci_sayilari, dict) else {}
    ks_row = {}
    for _kk, _kl in [("yonetici", "Yonetici"), ("ogretmen", "Öğretmen"), ("ogrenci", "Öğrenci"), ("veli", "Veli"), ("dis_katilimci", "Dis Katılımcı")]:
        _val = int(_ks.get(_kk, 0))
        if _val > 0:
            ks_row[_kl] = _val
    ks_row["Toplam"] = e.katilimci_sayisi
    gen.add_table(pd.DataFrame([ks_row]), "#0d9488")

    if e.sonuc:
        gen.add_text(f"Sonuc: {e.sonuc}")

    # Ertelendi/Iptal bilgisi
    if e.durum == "ERTELENDI":
        gen.add_section("Erteleme Bilgisi", "#f97316")
        gen.add_text(f"Erteleme Nedeni: {e.erteleme_nedeni or '-'}")
        gen.add_text(f"Yeni Tarih: {e.yeni_tarih or '-'}")
        gen.add_text(f"Yeni Saat: {e.yeni_saat or '-'}")
    elif e.durum == "IPTAL":
        gen.add_section("Iptal Bilgisi", "#ef4444")
        gen.add_text(f"Iptal Nedeni: {e.iptal_nedeni or '-'}")

    # Sportif detaylar
    if e.kategori == "SPORTIF":
        gen.add_section("Sportif Detaylar", "#f59e0b")
        gen.add_text(f"Branş: {e.brans or '-'}")
        gen.add_text(f"Musabaka Kapsami: {e.musabaka_kapsami or '-'}")
        gen.add_text(f"Rakip: {e.rakip or '-'}")
        gen.add_text(f"Skor: {e.skor or '-'}")
        gen.add_text(f"Derece: {e.derece or '-'}")

    # Katılımcı kategori bazli sayilar
    if e.katilimcilar:
        gen.add_section("Katılımcı Dagilimi (Kayıtli)", "#5b21b6")
        kat_sayilari: dict[str, int] = {}
        for k in e.katilimcilar:
            kat_key = k.get("kategori", "DIGER")
            kat_lbl = KATILIMCI_KATEGORILERI.get(kat_key, kat_key)
            kat_sayilari[kat_lbl] = kat_sayilari.get(kat_lbl, 0) + 1
        kat_sayilari["Toplam"] = len(e.katilimcilar)
        gen.add_table(pd.DataFrame([kat_sayilari]), "#5b21b6")

    if e.aciklama:
        gen.add_section("Açıklama", "#64748b")
        gen.add_text(e.aciklama)

    if e.notlar:
        gen.add_text(f"Notlar: {e.notlar}")

    # Fotograflar
    if e.fotograflar:
        existing_fotos = [f for f in e.fotograflar if os.path.exists(f)]
        if existing_fotos:
            gen.add_section("Etkinlik Fotograflari", "#8b5cf6")
            gen.add_images(existing_fotos, max_per_row=2, img_height_cm=5.5)

    return gen.generate()


def _generate_toplu_etkinlik_pdf(store: SosyalEtkinlikDataStore, etkinlikler: list, baslik: str = "Etkinlik Özet Raporu") -> bytes:
    """Birden fazla etkinlik için toplu ozet PDF raporu."""
    info = get_institution_info()
    all_cats = store.get_all_categories()

    gen = ReportPDFGenerator(
        baslik,
        f"Rapor Tarihi: {date.today().strftime('%d.%m.%Y')}",
    )
    gen.add_header(kurum_adi=info.get("name", ""))

    # Ozet istatistikler
    gen.add_section("Genel Özet", "#0B0F19")
    toplam = len(etkinlikler)
    yapildi = sum(1 for e in etkinlikler if e.durum == "TAMAMLANDI")
    ertelendi = sum(1 for e in etkinlikler if e.durum == "ERTELENDI")
    iptal = sum(1 for e in etkinlikler if e.durum == "IPTAL")
    planlanan = sum(1 for e in etkinlikler if e.durum in ("PLANLANDI", "DEVAM_EDIYOR"))

    gen.add_metrics([
        ("Toplam", str(toplam), "#2563eb"),
        ("Yapildi", str(yapildi), "#10b981"),
        ("Ertelendi", str(ertelendi), "#f97316"),
        ("Iptal", str(iptal), "#ef4444"),
    ])
    gen.add_spacer(0.4)

    # Kategori dagilimi
    kat_counts: dict[str, float] = {}
    for e in etkinlikler:
        label = all_cats.get(e.kategori, e.kategori)
        kat_counts[label] = kat_counts.get(label, 0) + 1
    if kat_counts:
        gen.add_section("Kategori Dagilimi", "#7c3aed")
        gen.add_bar_chart(kat_counts, "Kategori Bazinda Etkinlik Sayısı", "#7c3aed")

    # Durum dagilimi
    dur_counts: dict[str, float] = {}
    for e in etkinlikler:
        dur_counts[ETKINLIK_DURUM_LABEL.get(e.durum, e.durum)] = dur_counts.get(ETKINLIK_DURUM_LABEL.get(e.durum, e.durum), 0) + 1
    if dur_counts:
        gen.add_section("Durum Dagilimi", "#2563eb")
        gen.add_donut_chart(dur_counts, "Durum Bazinda Dagılım")

    # Toplam katilimci sayilari - tablo ile gosterim
    gen.add_section("Katılımcı İstatistikleri", "#0d9488")
    t_yon = sum(e.katilimci_sayilari.get("yonetici", 0) for e in etkinlikler if isinstance(e.katilimci_sayilari, dict))
    t_ogr = sum(e.katilimci_sayilari.get("ogretmen", 0) for e in etkinlikler if isinstance(e.katilimci_sayilari, dict))
    t_ogrenci = sum(e.katilimci_sayilari.get("ogrenci", 0) for e in etkinlikler if isinstance(e.katilimci_sayilari, dict))
    t_veli = sum(e.katilimci_sayilari.get("veli", 0) for e in etkinlikler if isinstance(e.katilimci_sayilari, dict))
    t_dis = sum(e.katilimci_sayilari.get("dis_katilimci", 0) for e in etkinlikler if isinstance(e.katilimci_sayilari, dict))
    t_toplam = sum(e.katilimci_sayisi for e in etkinlikler)
    ks_toplu_row = {}
    for _val, _lbl in [(t_yon, "Yonetici"), (t_ogr, "Öğretmen"), (t_ogrenci, "Öğrenci"), (t_veli, "Veli"), (t_dis, "Dis Katılımcı")]:
        if _val > 0:
            ks_toplu_row[_lbl] = _val
    ks_toplu_row["Toplam"] = t_toplam
    gen.add_table(pd.DataFrame([ks_toplu_row]), "#0d9488")

    # Etkinlik detay tablosu
    gen.add_section("Etkinlik Detaylari", "#94A3B8")
    rows = []
    for e in sorted(etkinlikler, key=lambda x: x.tarih_baslangic or "", reverse=True):
        rows.append({
            "Başlık": e.baslik[:40],
            "Kategori": all_cats.get(e.kategori, e.kategori),
            "Tarih": e.tarih_baslangic or "-",
            "Durum": ETKINLIK_DURUM_LABEL.get(e.durum, e.durum),
            "Katılımcı": str(e.katilimci_sayisi),
            "Sonuc": (e.sonuc or "-")[:30],
        })
    if rows:
        gen.add_table(pd.DataFrame(rows), "#94A3B8")

    # Ertelenen etkinlikler
    ertelenenler = [e for e in etkinlikler if e.durum == "ERTELENDI"]
    if ertelenenler:
        gen.add_section("Ertelenen Etkinlikler", "#f97316")
        ert_rows = []
        for e in ertelenenler:
            ert_rows.append({
                "Başlık": e.baslik[:40],
                "Erteleme Nedeni": (e.erteleme_nedeni or "-")[:40],
                "Yeni Tarih": e.yeni_tarih or "-",
                "Yeni Saat": e.yeni_saat or "-",
            })
        gen.add_table(pd.DataFrame(ert_rows), "#f97316")

    # Iptal edilen etkinlikler
    iptal_list = [e for e in etkinlikler if e.durum == "IPTAL"]
    if iptal_list:
        gen.add_section("Iptal Edilen Etkinlikler", "#ef4444")
        iptal_rows = []
        for e in iptal_list:
            iptal_rows.append({
                "Başlık": e.baslik[:40],
                "Iptal Nedeni": (e.iptal_nedeni or "-")[:60],
                "Tarih": e.tarih_baslangic or "-",
            })
        gen.add_table(pd.DataFrame(iptal_rows), "#ef4444")

    return gen.generate()


def _render_etkinlik_sonuc_raporu(store: SosyalEtkinlikDataStore, etkinlikler: list):
    """Raporlar sekmesinde etkinlik sonuc raporu bolumu."""
    if not etkinlikler:
        styled_info_banner("Etkinlik verisi yok.", "info")
        return

    # Filtre
    col_rf1, col_rf2 = st.columns(2)
    with col_rf1:
        dur_filtre = st.selectbox("Durum Filtresi", ["Tümü"] + [ETKINLIK_DURUM_LABEL[d] for d in ETKINLIK_DURUMLARI], key="set_rap_dur_fil")
    with col_rf2:
        all_cats = store.get_all_categories()
        kat_filtre = st.selectbox("Kategori Filtresi", ["Tümü"] + list(all_cats.values()), key="set_rap_kat_fil")

    filtered = etkinlikler
    if dur_filtre != "Tümü":
        dur_key = next((k for k, v in ETKINLIK_DURUM_LABEL.items() if v == dur_filtre), None)
        if dur_key:
            filtered = [e for e in filtered if e.durum == dur_key]
    if kat_filtre != "Tümü":
        kat_key = next((k for k, v in all_cats.items() if v == kat_filtre), None)
        if kat_key:
            filtered = [e for e in filtered if e.kategori == kat_key]

    st.info(f"{len(filtered)} etkinlik secili")

    # Sonuc tablosu
    if filtered:
        rows = []
        for e in sorted(filtered, key=lambda x: x.tarih_baslangic or "", reverse=True):
            _ks = e.katilimci_sayilari if isinstance(e.katilimci_sayilari, dict) else {}
            rows.append({
                "Başlık": e.baslik,
                "Kategori": all_cats.get(e.kategori, e.kategori),
                "Tarih": e.tarih_baslangic or "-",
                "Durum": ETKINLIK_DURUM_LABEL.get(e.durum, e.durum),
                "Yon.": _ks.get("yonetici", 0),
                "Ogrt.": _ks.get("ogretmen", 0),
                "Ogrn.": _ks.get("ogrenci", 0),
                "Veli": _ks.get("veli", 0),
                "Dis": _ks.get("dis_katilimci", 0),
                "Toplam": e.katilimci_sayisi,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # PDF indir butonu
    rapor_baslik = "Etkinlik Sonuc Raporu"
    if dur_filtre != "Tümü":
        rapor_baslik += f" - {dur_filtre}"
    if kat_filtre != "Tümü":
        rapor_baslik += f" - {kat_filtre}"

    if filtered:
        pdf_bytes = _generate_toplu_etkinlik_pdf(store, filtered, rapor_baslik)
        st.download_button(
            "Toplu PDF Rapor Indir", data=pdf_bytes,
            file_name=f"etkinlik_sonuc_raporu_{date.today().isoformat()}.pdf",
            mime="application/pdf",
            key="set_rap_toplu_dl",
            type="primary",
        )
