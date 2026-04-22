"""
SAG-01 Okul Sağlığı ve Sağlık Takip Modulu - Streamlit UI
==========================================================
Revir, ilac uygulama, kaza/olay, envanter, ilk yardim dolaplari,
seminerler, raporlar, KVKK erisim logu.
"""

from __future__ import annotations

import json, os, csv, io, uuid
from datetime import datetime, date, timedelta
from typing import Any

import streamlit as st
import pandas as pd

from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_students, get_student_display_options, get_sinif_sube_listesi
from utils.report_utils import ReportStyler
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome

from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("okul_sagligi")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("okul_sagligi",
        "Revir, saglik karti, ilac takibi, kaza kaydi, envanter, seminer yonetimi",
        [("6", "Bilesen"), ("AI", "Analiz"), ("PDF", "Rapor")])
except Exception:
    pass

from models.okul_sagligi import (
    SaglikBilesen, SaglikAyar, SaglikSettings,
    OgrenciSaglikKarti, RevirZiyareti, IlacUygulama, KazaOlay,
    SaglikEnvanter, DolapKarti, DolapIcerik, DolapKontrol,
    MalzemeSablonu, SeminerKonusu, Seminer, SeminerKatilim,
    TakipGorevi, ErisimLogu,
    SaglikDataStore, KVKKLogger, IlacOnayChecker, DolapDenetleyici, DashboardAggregator,
    REVIR_SONUCLARI, SIKAYET_KATEGORILERI, OLAY_TIPLERI, OLAY_LOKASYONLARI,
    ILAC_DURUMLARI, DOLAP_KONTROL_DURUMLARI, SEMINER_DURUMLARI,
    TAKIP_DURUMLARI, RISK_BAYRAKLARI, KAN_GRUPLARI, ERISIM_ISLEMLERI,
    BILESEN_KODLARI, VARSAYILAN_AKTIF_BILESENLER,
    _now, _today,
)

# ============================================================
# YARDIMCI FONKSIYONLAR
# ============================================================

def _get_sag_store() -> SaglikDataStore:
    base = os.path.join(get_tenant_dir(), "saglik")
    return SaglikDataStore(base)

def _gen_local_id(prefix: str = "tmp") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _sag_salgin_wrapper(store):
    """Salgin Takip wrapper — yeni ozellik dosyasindan cagirir."""
    try:
        from views._sag_yeni_ozellikler import render_salgin_takip
        render_salgin_takip(store)
    except Exception as _e:
        st.error(f"Salgin Takip yuklenemedi: {_e}")


def _sag_asi_wrapper(store):
    """Asi Takvimi wrapper."""
    try:
        from views._sag_yeni_ozellikler import render_asi_takvimi
        render_asi_takvimi(store)
    except Exception as _e:
        st.error(f"Asi Takvimi yuklenemedi: {_e}")


def _sag_risk_wrapper(store):
    """Risk Profili wrapper."""
    try:
        from views._sag_yeni_ozellikler import render_saglik_risk_profili
        render_saglik_risk_profili(store)
    except Exception as _e:
        st.error(f"Risk Profili yuklenemedi: {_e}")


def _sag_acil_wrapper(store):
    """Acil Durum Merkezi wrapper."""
    try:
        from views._sag_super_features import render_acil_durum_merkezi
        render_acil_durum_merkezi(store)
    except Exception as _e:
        st.error(f"Acil Durum yuklenemedi: {_e}")


def _sag_beslenme_wrapper(store):
    """Beslenme & Hijyen wrapper."""
    try:
        from views._sag_super_features import render_beslenme_hijyen
        render_beslenme_hijyen(store)
    except Exception as _e:
        st.error(f"Beslenme/Hijyen yuklenemedi: {_e}")


def _sag_spor_wrapper(store):
    """Spor Muafiyet wrapper."""
    try:
        from views._sag_super_features import render_spor_muafiyet
        render_spor_muafiyet(store)
    except Exception as _e:
        st.error(f"Spor Muafiyet yuklenemedi: {_e}")


def _sag_gelisim_wrapper(store):
    """Cocuk Gelisim wrapper."""
    try:
        from views._sag_mega_features import render_cocuk_gelisim
        render_cocuk_gelisim(store)
    except Exception as _e:
        st.error(f"Cocuk Gelisim yuklenemedi: {_e}")


def _sag_afet_wrapper(store):
    """Afet Yonetimi wrapper."""
    try:
        from views._sag_mega_features import render_afet_yonetimi
        render_afet_yonetimi(store)
    except Exception as _e:
        st.error(f"Afet Yonetimi yuklenemedi: {_e}")


def _sag_pasaport_wrapper(store):
    """Saglik Pasaportu wrapper."""
    try:
        from views._sag_mega_features import render_saglik_pasaportu
        render_saglik_pasaportu(store)
    except Exception as _e:
        st.error(f"Saglik Pasaportu yuklenemedi: {_e}")


def _sag_wellness_wrapper(store):
    try:
        from views._sag_zirve_features import render_wellness_endeksi
        render_wellness_endeksi(store)
    except Exception as _e:
        st.error(f"Wellness Endeksi yuklenemedi: {_e}")


def _sag_ai_tahmin_wrapper(store):
    try:
        from views._sag_zirve_features import render_ai_saglik_tahmin
        render_ai_saglik_tahmin(store)
    except Exception as _e:
        st.error(f"AI Tahmin yuklenemedi: {_e}")


def _sag_kampanya_wrapper(store):
    try:
        from views._sag_zirve_features import render_saglik_kampanya
        render_saglik_kampanya(store)
    except Exception as _e:
        st.error(f"Kampanya yuklenemedi: {_e}")

def _today_str() -> str:
    return date.today().isoformat()

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


# ============================================================
# CSS STILLERI
# ============================================================

def _inject_sag_css():
    inject_common_css("sag")
    st.markdown("""<style>
    :root {
        --sag-primary: #0d9488;
        --sag-primary-dark: #0f766e;
        --sag-success: #10b981;
        --sag-warning: #f59e0b;
        --sag-danger: #ef4444;
        --sag-purple: #8b5cf6;
        --sag-blue: #2563eb;
        --sag-dark: #0B0F19;
    }
    .stApp > header { background: transparent !important; }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(200,149,46,0.06);
        transition: all 0.3s ease; border-left: 4px solid #2563eb;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    </style>""", unsafe_allow_html=True)


_GRAD = {
    "#0d9488": ("rgba(13,148,136,0.10)", "rgba(13,148,136,0.25)"),
    "#10b981": ("rgba(16,185,129,0.10)", "rgba(16,185,129,0.25)"),
    "#2563eb": ("rgba(37,99,235,0.10)", "rgba(37,99,235,0.25)"),
    "#f59e0b": ("rgba(245,158,11,0.10)", "rgba(245,158,11,0.25)"),
    "#ef4444": ("rgba(239,68,68,0.10)", "rgba(239,68,68,0.25)"),
    "#8b5cf6": ("rgba(139,92,246,0.10)", "rgba(139,92,246,0.25)"),
    "#0f766e": ("rgba(15,118,110,0.10)", "rgba(15,118,110,0.25)"),
    "#ea580c": ("rgba(234,88,12,0.10)", "rgba(234,88,12,0.25)"),
    "#475569": ("rgba(71,85,105,0.10)", "rgba(71,85,105,0.25)"),
}




# ============================================================
# SEKME 1: DASHBOARD
# ============================================================

def _render_dashboard(store: SaglikDataStore):
    data = DashboardAggregator.get_dashboard_data(store)
    styled_stat_row([
        ("Bugün Revir", data["revir_bugun_sayi"], "#0d9488", "\U0001f3e5"),
        ("Planli Ilac", data["ilac_planli_sayi"], "#8b5cf6", "\U0001f48a"),
        ("Risk Öğrenci", data["risk_sayi"], "#ef4444", "\u26a0\ufe0f"),
        ("Açık Görev", data["acik_gorev_sayi"], "#f59e0b", "\U0001f4cb"),
        ("Dolap Uyari", data["dolap_uyari_sayi"], "#ea580c", "\U0001fa79"),
        ("Planli Seminer", data["planli_seminer_sayi"], "#2563eb", "\U0001f393"),
    ])

    c1, c2 = st.columns(2)
    with c1:
        styled_section("Bugünün Revir Ziyaretleri", "#0d9488")
        if data["revir_bugun"]:
            for r in data["revir_bugun"]:
                st.markdown(f"**{r.ziyaret_kodu}** | {r.ogrenci_adi} ({r.sinif}/{r.sube}) | "
                            f"{r.sikayet_kategorisi} | {r.sonuc}")
        else:
            styled_info_banner("Bugün revir ziyareti yok.", "info")

        styled_section("Planli İlaç Uygulamalari", "#8b5cf6")
        if data["ilac_planli"]:
            for i in data["ilac_planli"]:
                st.markdown(f"**{i.uygulama_kodu}** | {i.ogrenci_adi} | {i.ilac_adi} {i.doz} | "
                            f"Saat: {i.uygulama_saati}")
        else:
            styled_info_banner("Bugün planli ilac uygulamasi yok.", "info")

    with c2:
        styled_section("Kritik Risk Bayraklari", "#ef4444")
        if data["risk_ogrenciler"]:
            for k in data["risk_ogrenciler"][:10]:
                flags = ", ".join(k.risk_bayraklari)
                st.markdown(f"**{k.ogrenci_adi}** ({k.sinif}/{k.sube}) - {flags}")
        else:
            styled_info_banner("Risk bayrakli ogrenci yok.", "success")

        styled_section("Açık Takip Görevleri", "#f59e0b")
        if data["acik_gorevler"]:
            for g in data["acik_gorevler"][:5]:
                st.markdown(f"**{g.kaynak_kodu}** | {g.gorev_aciklamasi} | Son: {g.son_tarih}")
        else:
            styled_info_banner("Açık takip gorevi yok.", "success")

    if data["dolap_uyarilari"]:
        styled_section("Dolap Uyarilari", "#ea580c")
        for du in data["dolap_uyarilari"]:
            issues = []
            if du["uyarilar"]["eksik"]:
                issues.append(f"{len(du['uyarilar']['eksik'])} eksik")
            if du["uyarilar"]["skt_yaklasan"]:
                issues.append(f"{len(du['uyarilar']['skt_yaklasan'])} SKT yaklasan")
            if du["uyarilar"]["skt_gecen"]:
                issues.append(f"{len(du['uyarilar']['skt_gecen'])} SKT gecen")
            st.markdown(f"**{du['dolap']}**: {', '.join(issues)}")


# ============================================================
# SEKME 2: OGRENCI SAGLIK KARTI
# ============================================================

def _render_saglik_karti(store: SaglikDataStore):
    sub = st.tabs(["🔍 Kart Ara", "➕ Yeni Kart", "📋 Kart Listesi"])

    with sub[0]:
        styled_section("Öğrenci Sağlık Kartı Arama", "#0d9488")
        arama = st.text_input("Öğrenci adi ile ara", key="sag_kart_ara")
        if arama and len(arama) >= 2:
            q = arama.lower()
            kartlar = store.load_objects("saglik_kartlari")
            sonuclar = [k for k in kartlar if q in k.ogrenci_adi.lower()]
            if sonuclar:
                for k in sonuclar:
                    flags = ", ".join(k.risk_bayraklari) if k.risk_bayraklari else "-"
                    alerjiler = ", ".join(k.alerjiler) if k.alerjiler else "-"
                    st.markdown(f"**{k.ogrenci_adi}** ({k.sinif}/{k.sube}) | Kan: {k.kan_grubu} | "
                                f"Risk: {flags} | Alerji: {alerjiler}")
            else:
                styled_info_banner("Sonuc bulunamadı.", "info")

    with sub[1]:
        styled_section("Yeni Sağlık Kartı Oluştur", "#10b981")
        stu = _ogrenci_selectbox("sag_kart_ogrenci", "Öğrenci Seçin")

        kan = st.selectbox("Kan Grubu", KAN_GRUPLARI, key="sag_kart_kan")
        alerjiler_txt = st.text_input("Alerjiler (virgul ile ayirin)", key="sag_kart_alerji",
                                       help="Ornek: Penisilin, Fistik, Polen")
        kronik_txt = st.text_input("Kronik Durumlar (virgul ile ayirin)", key="sag_kart_kronik",
                                    help="Ornek: Astim, Epilepsi, Diyabet")
        ilaclar_txt = st.text_input("Surekli Ilaclar (virgul ile ayirin)", key="sag_kart_ilac")
        risk = st.multiselect("Risk Bayraklari", RISK_BAYRAKLARI, key="sag_kart_risk")

        styled_section("Acil İletişim", "#ef4444")
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            a1_ad = st.text_input("1. Kisi Ad Soyad", key="sag_kart_a1_ad")
        with ac2:
            a1_tel = st.text_input("1. Kisi Telefon", key="sag_kart_a1_tel")
        with ac3:
            a1_yak = st.text_input("1. Kisi Yakinlik", key="sag_kart_a1_yak", help="Ornek: Anne, Baba")
        ac4, ac5, ac6 = st.columns(3)
        with ac4:
            a2_ad = st.text_input("2. Kisi Ad Soyad", key="sag_kart_a2_ad")
        with ac5:
            a2_tel = st.text_input("2. Kisi Telefon", key="sag_kart_a2_tel")
        with ac6:
            a2_yak = st.text_input("2. Kisi Yakinlik", key="sag_kart_a2_yak")

        notlar = st.text_area("Notlar", key="sag_kart_notlar", height=80)

        if st.button("Sağlık Kartı Kaydet", type="primary", key="sag_kart_kaydet"):
            if not stu:
                st.error("Öğrenci secimi zorunludur.")
            else:
                existing = store.get_by_field("saglik_kartlari", "ogrenci_id", stu.get("id", ""))
                if existing:
                    st.error("Bu ogrenci için zaten saglik karti var.")
                else:
                    kart = OgrenciSaglikKarti(
                        ogrenci_id=stu.get("id", ""),
                        ogrenci_adi=f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip(),
                        sinif=str(stu.get("sinif", "")),
                        sube=str(stu.get("sube", "")),
                        kan_grubu=kan,
                        alerjiler=[a.strip() for a in alerjiler_txt.split(",") if a.strip()] if alerjiler_txt else [],
                        kronik_durumlar=[k.strip() for k in kronik_txt.split(",") if k.strip()] if kronik_txt else [],
                        surekli_ilaclar=[i.strip() for i in ilaclar_txt.split(",") if i.strip()] if ilaclar_txt else [],
                        risk_bayraklari=risk,
                        acil_iletisim_1_ad=a1_ad, acil_iletisim_1_tel=a1_tel, acil_iletisim_1_yakinlik=a1_yak,
                        acil_iletisim_2_ad=a2_ad, acil_iletisim_2_tel=a2_tel, acil_iletisim_2_yakinlik=a2_yak,
                        notlar=notlar,
                    )
                    store.upsert("saglik_kartlari", kart)
                    KVKKLogger.log(store, "olusturma", "saglik_karti", kart.id, kart.ogrenci_adi)
                    styled_info_banner(f"Sağlık karti oluşturuldu: {kart.ogrenci_adi}", "success")
                    st.rerun()

    with sub[2]:
        styled_section("Sağlık Kartı Listesi", "#0d9488")
        kartlar = store.load_objects("saglik_kartlari")
        if kartlar:
            rows = []
            for k in kartlar:
                rows.append({
                    "Öğrenci": k.ogrenci_adi, "Sınıf": f"{k.sinif}/{k.sube}",
                    "Kan": k.kan_grubu,
                    "Alerji": ", ".join(k.alerjiler) if k.alerjiler else "-",
                    "Kronik": ", ".join(k.kronik_durumlar) if k.kronik_durumlar else "-",
                    "Risk": ", ".join(k.risk_bayraklari) if k.risk_bayraklari else "-",
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Henuz saglik karti yok.", "info")


# ============================================================
# SEKME 3: REVIR ZIYARETI
# ============================================================

def _render_revir_ziyareti(store: SaglikDataStore):
    sub = st.tabs(["➕ Yeni Ziyaret", "📋 Ziyaret Listesi", "📝 Takip Görevleri"])

    with sub[0]:
        styled_section("Yeni Revir Ziyareti", "#0d9488")
        stu = _ogrenci_selectbox("sag_rev_ogrenci", "Öğrenci Seçin")
        r1, r2 = st.columns(2)
        with r1:
            sikayet_kat = st.selectbox("Sikayet Kategorisi", SIKAYET_KATEGORILERI, key="sag_rev_kat")
        with r2:
            saat = st.text_input("Basvuru Saati", value=datetime.now().strftime("%H:%M"), key="sag_rev_saat")
        sikayet = st.text_area("Sikayet Detayi", key="sag_rev_sikayet", height=80)
        mudahale = st.text_area("Yapilan Mudahale", key="sag_rev_mudahale", height=80)
        uygulayan = st.text_input("Uygulayan (Hemsire/Görevli)", key="sag_rev_uyg")
        v1, v2 = st.columns(2)
        with v1:
            veli_bilgi = st.checkbox("Veli Bilgilendirildi", key="sag_rev_veli")
        with v2:
            takip = st.checkbox("Takip Gerekiyor", key="sag_rev_takip")
        takip_notu = ""
        if takip:
            takip_notu = st.text_input("Takip Notu", key="sag_rev_takip_notu")
        sonuc = st.selectbox("Sonuc", REVIR_SONUCLARI, key="sag_rev_sonuc")

        if st.button("Revir Ziyareti Kaydet", type="primary", key="sag_rev_kaydet"):
            if not stu:
                st.error("Öğrenci secimi zorunludur.")
            else:
                ziy = RevirZiyareti(
                    ziyaret_kodu=store.next_revir_code(),
                    ogrenci_id=stu.get("id", ""),
                    ogrenci_adi=f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip(),
                    sinif=str(stu.get("sinif", "")), sube=str(stu.get("sube", "")),
                    basvuru_saati=saat,
                    sikayet=sikayet, sikayet_kategorisi=sikayet_kat,
                    mudahale=mudahale, uygulayan=uygulayan,
                    veli_bilgilendirildi=veli_bilgi,
                    veli_bilgilendirme_tarihi=_today_str() if veli_bilgi else "",
                    takip_gerekiyor=takip, takip_notu=takip_notu, sonuc=sonuc,
                )
                store.upsert("revir_ziyaretleri", ziy)
                KVKKLogger.log(store, "olusturma", "revir_ziyareti", ziy.id, ziy.ogrenci_adi)
                if takip:
                    gorev = TakipGorevi(
                        kaynak_tip="revir", kaynak_id=ziy.id, kaynak_kodu=ziy.ziyaret_kodu,
                        gorev_aciklamasi=f"Revir takip: {ziy.ogrenci_adi} - {sikayet_kat}",
                        atanan=uygulayan,
                        son_tarih=(date.today() + timedelta(days=3)).isoformat(),
                    )
                    store.upsert("takip_gorevleri", gorev)
                styled_info_banner(f"Revir ziyareti kaydedildi: {ziy.ziyaret_kodu}", "success")
                st.rerun()

    with sub[1]:
        styled_section("Revir Ziyaret Listesi", "#0d9488")
        ziyaretler = store.load_objects("revir_ziyaretleri")
        ziyaretler.sort(key=lambda x: x.created_at, reverse=True)
        f1, f2 = st.columns(2)
        with f1:
            filtre_sonuc = st.selectbox("Sonuc Filtre", ["Tümü"] + REVIR_SONUCLARI, key="sag_rev_filtre")
        with f2:
            filtre_tarih = st.date_input("Tarih", value=date.today(), key="sag_rev_tarih")
        filtered = ziyaretler
        if filtre_sonuc != "Tümü":
            filtered = [z for z in filtered if z.sonuc == filtre_sonuc]
        if filtre_tarih:
            t_str = filtre_tarih.isoformat()
            filtered = [z for z in filtered if z.basvuru_tarihi == t_str]
        if filtered:
            rows = []
            for z in filtered:
                rows.append({
                    "Kod": z.ziyaret_kodu, "Öğrenci": z.ogrenci_adi,
                    "Sınıf": f"{z.sinif}/{z.sube}", "Sikayet": z.sikayet_kategorisi,
                    "Mudahale": z.mudahale[:40] + "..." if len(z.mudahale) > 40 else z.mudahale,
                    "Sonuc": z.sonuc, "Saat": z.basvuru_saati,
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Kayıt bulunamadı.", "info")

    with sub[2]:
        styled_section("Açık Takip Görevleri", "#f59e0b")
        gorevler = store.load_objects("takip_gorevleri")
        acik = [g for g in gorevler if g.durum == "Açık"]
        if acik:
            for g in acik:
                gc1, gc2 = st.columns([3, 1])
                with gc1:
                    st.markdown(f"**{g.kaynak_kodu}** | {g.gorev_aciklamasi} | Son: {g.son_tarih}")
                with gc2:
                    if st.button("Tamamla", key=f"sag_tg_done_{g.id}"):
                        g.durum = "Tamamlandı"
                        g.tamamlanma_tarihi = _today_str()
                        g.updated_at = _now()
                        store.upsert("takip_gorevleri", g)
                        st.rerun()
        else:
            styled_info_banner("Açık takip gorevi yok.", "success")


# ============================================================
# SEKME 4: ILAC UYGULAMA
# ============================================================

def _render_ilac_uygulama(store: SaglikDataStore):
    settings = store.get_settings()
    sub = st.tabs(["➕ Yeni Uygulama", "📋 Uygulama Listesi", "📅 Planlanan"])

    with sub[0]:
        styled_section("Yeni İlaç Uygulama Kaydi", "#8b5cf6")
        stu = _ogrenci_selectbox("sag_ilac_ogrenci", "Öğrenci Seçin")
        i1, i2, i3 = st.columns(3)
        with i1:
            ilac_adi = st.text_input("Ilac Adi *", key="sag_ilac_adi")
        with i2:
            doz = st.text_input("Doz", key="sag_ilac_doz", help="Ornek: 5ml, 1 tablet")
        with i3:
            saat = st.text_input("Uygulama Saati", value=datetime.now().strftime("%H:%M"), key="sag_ilac_saat")
        uygulayan = st.text_input("Uygulayan", key="sag_ilac_uyg")
        i4, i5 = st.columns(2)
        with i4:
            veli_onay = st.selectbox("Veli Onay Durumu", ["Bekleniyor", "Onaylandi"], key="sag_ilac_vonay")
        with i5:
            dr_rapor = st.checkbox("Doktor Raporu Var", key="sag_ilac_drrapor")
        notlar = st.text_area("Notlar", key="sag_ilac_notlar", height=60)

        if st.button("Ilac Kaydini Oluştur", type="primary", key="sag_ilac_kaydet"):
            if not stu or not ilac_adi:
                st.error("Öğrenci ve ilac adi zorunludur.")
            else:
                uyg = IlacUygulama(
                    uygulama_kodu=store.next_ilac_code(),
                    ogrenci_id=stu.get("id", ""),
                    ogrenci_adi=f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip(),
                    sinif=str(stu.get("sinif", "")), sube=str(stu.get("sube", "")),
                    ilac_adi=ilac_adi, doz=doz, uygulama_saati=saat, uygulayan=uygulayan,
                    veli_onay_durumu=veli_onay, doktor_raporu_var=dr_rapor, notlar=notlar,
                )
                store.upsert("ilac_uygulamalari", uyg)
                KVKKLogger.log(store, "olusturma", "ilac_uygulama", uyg.id, uyg.ogrenci_adi)
                styled_info_banner(f"Ilac kaydi oluşturuldu: {uyg.uygulama_kodu}", "success")
                st.rerun()

    with sub[1]:
        styled_section("İlaç Uygulama Listesi", "#8b5cf6")
        uygulamalar = store.load_objects("ilac_uygulamalari")
        uygulamalar.sort(key=lambda x: x.created_at, reverse=True)
        if uygulamalar:
            for u in uygulamalar[:20]:
                uc1, uc2, uc3 = st.columns([3, 1, 1])
                with uc1:
                    st.markdown(f"**{u.uygulama_kodu}** | {u.ogrenci_adi} | {u.ilac_adi} {u.doz} | "
                                f"Durum: {u.durum} | Onay: {u.veli_onay_durumu}")
                with uc2:
                    if u.durum == "Planli":
                        can_do, reasons = IlacOnayChecker.can_complete(u, settings)
                        if can_do:
                            if st.button("Uygulandi", key=f"sag_ilac_done_{u.id}"):
                                u.durum = "Uygulandi"
                                u.updated_at = _now()
                                store.upsert("ilac_uygulamalari", u)
                                st.rerun()
                        else:
                            st.warning(" | ".join(reasons))
                with uc3:
                    if u.durum == "Planli":
                        if st.button("Iptal", key=f"sag_ilac_iptal_{u.id}"):
                            u.durum = "Iptal"
                            u.updated_at = _now()
                            store.upsert("ilac_uygulamalari", u)
                            st.rerun()
        else:
            styled_info_banner("Henuz ilac uygulama kaydi yok.", "info")

    with sub[2]:
        styled_section("Bugünkü Planlanan Uygulamalar", "#8b5cf6")
        planli = [u for u in store.load_objects("ilac_uygulamalari")
                  if u.durum == "Planli" and u.uygulama_tarihi == _today_str()]
        if planli:
            for p in planli:
                st.markdown(f"**{p.uygulama_kodu}** | {p.ogrenci_adi} | {p.ilac_adi} {p.doz} | "
                            f"Saat: {p.uygulama_saati} | Onay: {p.veli_onay_durumu}")
        else:
            styled_info_banner("Bugün planli uygulama yok.", "info")


# ============================================================
# SEKME 5: KAZA / OLAY
# ============================================================

def _render_kaza_olay(store: SaglikDataStore):
    sub = st.tabs(["➕ Yeni Olay", "📋 Olay Listesi"])

    with sub[0]:
        styled_section("Yeni Kaza / Olay Kaydi", "#ef4444")
        stu = _ogrenci_selectbox("sag_kaza_ogrenci", "Öğrenci Seçin")
        k1, k2, k3 = st.columns(3)
        with k1:
            olay_tipi = st.selectbox("Olay Tipi", OLAY_TIPLERI, key="sag_kaza_tip")
        with k2:
            lokasyon = st.selectbox("Lokasyon", OLAY_LOKASYONLARI, key="sag_kaza_lok")
        with k3:
            saat = st.text_input("Olay Saati", value=datetime.now().strftime("%H:%M"), key="sag_kaza_saat")
        aciklama = st.text_area("Olay Açıklaması", key="sag_kaza_aciklama", height=80)
        taniklar = st.text_input("Taniklar", key="sag_kaza_tanik")
        mudahale = st.text_area("Yapilan Mudahale / İlk Yardim", key="sag_kaza_mudahale", height=80)
        uygulayan = st.text_input("Uygulayan", key="sag_kaza_uyg")

        styled_section("İlk Yardim Checklist", "#f59e0b")
        checklist_items = [
            "Olay yeri guvenligi saglandi",
            "Yarali bilinci kontrol edildi",
            "Gerekli ilk yardim uygulamasi yapildi",
            "Veli bilgilendirildi",
            "Ambulans cagirildi",
            "Tutanak duzenlendi",
        ]
        checklist_results = []
        for item in checklist_items:
            yapildi = st.checkbox(item, key=f"sag_kaza_cl_{item[:15]}")
            checklist_results.append({"madde": item, "yapildi": yapildi})

        sonuc = st.selectbox("Sonuc", ["Sınıfa dondu", "Veli teslim", "Ambulans", "Hastane sevk", "Diger"],
                             key="sag_kaza_sonuc")
        veli_bilgi = st.checkbox("Veli Bilgilendirildi", key="sag_kaza_veli")

        if st.button("Kaza/Olay Kaydet", type="primary", key="sag_kaza_kaydet"):
            if not stu:
                st.error("Öğrenci secimi zorunludur.")
            else:
                olay = KazaOlay(
                    olay_kodu=store.next_kaza_code(),
                    ogrenci_id=stu.get("id", ""),
                    ogrenci_adi=f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip(),
                    sinif=str(stu.get("sinif", "")), sube=str(stu.get("sube", "")),
                    olay_saati=saat, olay_tipi=olay_tipi, olay_lokasyonu=lokasyon,
                    taniklar=taniklar, olay_aciklamasi=aciklama,
                    ilk_yardim_checklist=checklist_results,
                    mudahale=mudahale, uygulayan=uygulayan,
                    sonuc=sonuc, veli_bilgilendirildi=veli_bilgi,
                )
                store.upsert("kaza_olaylari", olay)
                KVKKLogger.log(store, "olusturma", "kaza_olay", olay.id, olay.ogrenci_adi)
                styled_info_banner(f"Kaza/olay kaydi oluşturuldu: {olay.olay_kodu}", "success")
                st.rerun()

    with sub[1]:
        styled_section("Kaza / Olay Listesi", "#ef4444")
        olaylar = store.load_objects("kaza_olaylari")
        olaylar.sort(key=lambda x: x.created_at, reverse=True)
        if olaylar:
            rows = []
            for o in olaylar:
                rows.append({
                    "Kod": o.olay_kodu, "Öğrenci": o.ogrenci_adi,
                    "Tip": o.olay_tipi, "Lokasyon": o.olay_lokasyonu,
                    "Tarih": o.olay_tarihi, "Saat": o.olay_saati,
                    "Sonuc": o.sonuc,
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Henuz kaza/olay kaydi yok.", "info")


# ============================================================
# SEKME 6: SAGLIK ENVANTERI
# ============================================================

def _render_envanter(store: SaglikDataStore):
    sub = st.tabs(["📋 Urun Listesi", "➕ Yeni Urun", "⚠️ Uyarilar"])

    with sub[0]:
        styled_section("Sağlık Envanteri", "#0f766e")
        envanter = store.load_objects("envanter")
        if envanter:
            rows = []
            for e in envanter:
                durum = "OK"
                if e.stok_miktari < e.min_stok:
                    durum = "STOK ALTI"
                if e.son_kullanma_tarihi:
                    try:
                        skt = date.fromisoformat(e.son_kullanma_tarihi)
                        if skt < date.today():
                            durum = "SKT GECMIS"
                        elif (skt - date.today()).days <= 30:
                            durum = "SKT YAKLASAN"
                    except (ValueError, TypeError):
                        pass
                rows.append({
                    "Urun": e.urun_adi, "Birim": e.birim,
                    "Stok": e.stok_miktari, "Min": e.min_stok,
                    "SKT": e.son_kullanma_tarihi or "-", "Durum": durum,
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Henuz envanter kaydi yok.", "info")

    with sub[1]:
        styled_section("Yeni Urun Ekle", "#10b981")
        e1, e2 = st.columns(2)
        with e1:
            urun_adi = st.text_input("Urun Adi *", key="sag_env_ad")
            birim = st.text_input("Birim", value="adet", key="sag_env_birim")
        with e2:
            stok = st.number_input("Stok Miktari", min_value=0, value=0, key="sag_env_stok")
            min_stok = st.number_input("Minimum Stok", min_value=0, value=0, key="sag_env_min")
        skt = st.date_input("Son Kullanma Tarihi (SKT)", value=None, key="sag_env_skt")
        kritik = st.checkbox("Kritik Malzeme", key="sag_env_kritik")

        if st.button("Urun Kaydet", type="primary", key="sag_env_kaydet"):
            if not urun_adi:
                st.error("Urun adi zorunludur.")
            else:
                item = SaglikEnvanter(
                    urun_kodu=_gen_local_id("INV"),
                    urun_adi=urun_adi, birim=birim,
                    stok_miktari=stok, min_stok=min_stok,
                    son_kullanma_tarihi=skt.isoformat() if skt else "",
                    kritik_mi=kritik,
                )
                store.upsert("envanter", item)
                styled_info_banner(f"Urun eklendi: {urun_adi}", "success")
                st.rerun()

    with sub[2]:
        styled_section("Stok ve SKT Uyarilari", "#f59e0b")
        envanter = store.load_objects("envanter")
        settings = store.get_settings()
        bugun = date.today()
        uyarilar = []
        for e in envanter:
            if e.stok_miktari < e.min_stok:
                uyarilar.append(f"**STOK ALTI:** {e.urun_adi} (stok: {e.stok_miktari}, min: {e.min_stok})")
            if e.son_kullanma_tarihi:
                try:
                    skt = date.fromisoformat(e.son_kullanma_tarihi)
                    if skt < bugun:
                        uyarilar.append(f"**SKT GECMIS:** {e.urun_adi} (SKT: {e.son_kullanma_tarihi})")
                    elif (skt - bugun).days <= settings.fak_skt_uyari_gun:
                        uyarilar.append(f"**SKT YAKLASAN:** {e.urun_adi} ({(skt - bugun).days} gun kaldi)")
                except (ValueError, TypeError):
                    pass
        if uyarilar:
            for u in uyarilar:
                st.markdown(u)
        else:
            styled_info_banner("Uyari yok. Tüm urunler uygun durumda.", "success")


# ============================================================
# SEKME 7: ILK YARDIM DOLAPLARI (FAK-01)
# ============================================================

def _render_ilk_yardim_dolaplari(store: SaglikDataStore):
    sub = st.tabs(["🗄️ Dolap Kartlari", "📦 Dolap Icerigi", "🔄 Periyodik Kontrol", "➕ Yeni Malzeme Ekle"])

    with sub[0]:
        styled_section("İlk Yardim Dolap Kartlari", "#ea580c")
        dolaplar = store.load_objects("dolap_kartlari")
        if dolaplar:
            for d in dolaplar:
                geciken = DolapDenetleyici.is_kontrol_geciken(d)
                durum_txt = "KONTROL GECIKTI" if geciken else "Normal"
                st.markdown(f"**{d.dolap_kodu}** - {d.dolap_adi or d.lokasyon} | "
                            f"Lokasyon: {d.lokasyon} | Sorumlu: {d.sorumlu} | "
                            f"Periyot: {d.kontrol_periyodu_gun} gun | Durum: {durum_txt}")
        else:
            styled_info_banner("Henuz dolap karti yok.", "info")

        styled_section("Yeni Dolap Ekle", "#10b981")
        d1, d2 = st.columns(2)
        with d1:
            dolap_adi = st.text_input("Dolap Adi", key="sag_fak_ad")
            lokasyon = st.text_input("Lokasyon", key="sag_fak_lok")
        with d2:
            sorumlu = st.text_input("Sorumlu", key="sag_fak_sor")
            periyot = st.number_input("Kontrol Periyodu (gun)", min_value=1, value=30, key="sag_fak_per")
        if st.button("Dolap Kaydet", type="primary", key="sag_fak_kaydet"):
            if not lokasyon:
                st.error("Lokasyon zorunludur.")
            else:
                dolap = DolapKarti(
                    dolap_kodu=store.next_dolap_code(),
                    dolap_adi=dolap_adi, lokasyon=lokasyon,
                    sorumlu=sorumlu, kontrol_periyodu_gun=periyot,
                    sonraki_kontrol_tarihi=(date.today() + timedelta(days=periyot)).isoformat(),
                )
                store.upsert("dolap_kartlari", dolap)
                styled_info_banner(f"Dolap eklendi: {dolap.dolap_kodu}", "success")
                st.rerun()

    with sub[1]:
        styled_section("Dolap Icerigi Yönetimi", "#ea580c")
        dolaplar = store.load_objects("dolap_kartlari")
        if not dolaplar:
            styled_info_banner("Önce dolap karti olusturun.", "warning")
        else:
            dolap_options = {f"{d.dolap_kodu} - {d.dolap_adi or d.lokasyon}": d for d in dolaplar}
            sec = st.selectbox("Dolap Secin", list(dolap_options.keys()), key="sag_fak_ic_sec")
            sel_dolap = dolap_options[sec]

            icerikler = store.find_by_field("dolap_icerikleri", "dolap_id", sel_dolap.id)
            if icerikler:
                rows = []
                for ic in icerikler:
                    rows.append({
                        "Malzeme": ic.malzeme_adi, "Stok": ic.stok_miktari,
                        "Min": ic.min_stok, "SKT": ic.son_kullanma_tarihi or "-",
                        "Kritik": "Evet" if ic.kritik_mi else "Hayir",
                    })
                st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

            # Sablondan malzeme ekle
            styled_section("Sablondan Malzeme Ekle", "#10b981")
            sablonlar = store.load_objects("malzeme_sablonlari")
            if sablonlar:
                sablon_opts = {f"{s.malzeme_kodu} - {s.malzeme_adi}": s for s in sablonlar}
                sablon_sec = st.selectbox("Malzeme Sablonu", list(sablon_opts.keys()), key="sag_fak_ic_sablon")
                sel_sablon = sablon_opts[sablon_sec]
                ic_stok = st.number_input("Stok Miktari", min_value=0, value=sel_sablon.varsayilan_min_stok, key="sag_fak_ic_stok")
                ic_skt = st.date_input("SKT", value=None, key="sag_fak_ic_skt")
                if st.button("Malzemeyi Dolaba Ekle", key="sag_fak_ic_ekle"):
                    ic = DolapIcerik(
                        dolap_id=sel_dolap.id,
                        malzeme_kodu=sel_sablon.malzeme_kodu, malzeme_adi=sel_sablon.malzeme_adi,
                        birim=sel_sablon.birim, stok_miktari=ic_stok, min_stok=sel_sablon.varsayilan_min_stok,
                        son_kullanma_tarihi=ic_skt.isoformat() if ic_skt else "",
                        kritik_mi=sel_sablon.kritik_mi,
                    )
                    store.upsert("dolap_icerikleri", ic)
                    styled_info_banner(f"Malzeme eklendi: {sel_sablon.malzeme_adi}", "success")
                    st.rerun()
            else:
                styled_info_banner("Malzeme sablonu yok. Ayarlar > CSV Import ile yukleyin veya Yeni Malzeme Ekle sekmesini kullanin.", "warning")

            # Uyarilar
            uyarilar = DolapDenetleyici.get_uyarilar(sel_dolap.id, store)
            if uyarilar["eksik"] or uyarilar["skt_yaklasan"] or uyarilar["skt_gecen"]:
                styled_section("Uyarilar", "#ef4444")
                for e in uyarilar["eksik"]:
                    st.markdown(f"**EKSIK:** {e['malzeme']} (stok: {e['stok']}, min: {e['min']})")
                for s in uyarilar["skt_yaklasan"]:
                    st.markdown(f"**SKT YAKLASAN:** {s['malzeme']} ({s['gun']} gun kaldi)")
                for s in uyarilar["skt_gecen"]:
                    st.markdown(f"**SKT GECMIS:** {s['malzeme']} (SKT: {s['skt']})")

    with sub[2]:
        styled_section("Periyodik Dolap Kontrolu", "#f59e0b")
        dolaplar = store.load_objects("dolap_kartlari")
        if not dolaplar:
            styled_info_banner("Önce dolap karti olusturun.", "warning")
        else:
            dolap_opts = {f"{d.dolap_kodu} - {d.dolap_adi or d.lokasyon}": d for d in dolaplar}
            sec_k = st.selectbox("Kontrol Edilecek Dolap", list(dolap_opts.keys()), key="sag_fak_kn_sec")
            sel_k = dolap_opts[sec_k]
            kontrolcu = st.text_input("Kontrolcu", key="sag_fak_kn_kisi")
            notlar_k = st.text_area("Kontrol Notları", key="sag_fak_kn_not", height=60)

            uyarilar = DolapDenetleyici.get_uyarilar(sel_k.id, store)
            eksikler = []
            for e in uyarilar["eksik"]:
                eksikler.append({"malzeme": e["malzeme"], "durum": "eksik"})
            for s in uyarilar["skt_gecen"]:
                eksikler.append({"malzeme": s["malzeme"], "durum": "skt_gecen"})

            durum = "Uygun"
            if uyarilar["skt_gecen"]:
                durum = "SKT Gecen Var"
            elif uyarilar["eksik"]:
                durum = "Eksik Var"

            if st.button("Kontrolu Kaydet", type="primary", key="sag_fak_kn_kaydet"):
                kontrol = DolapKontrol(
                    dolap_id=sel_k.id, dolap_kodu=sel_k.dolap_kodu,
                    kontrolcu=kontrolcu, durum=durum,
                    eksik_malzemeler=eksikler, notlar=notlar_k,
                )
                store.upsert("dolap_kontrolleri", kontrol)
                sel_k.son_kontrol_tarihi = _today_str()
                sel_k.sonraki_kontrol_tarihi = (date.today() + timedelta(days=sel_k.kontrol_periyodu_gun)).isoformat()
                sel_k.updated_at = _now()
                store.upsert("dolap_kartlari", sel_k)
                styled_info_banner(f"Kontrol kaydedildi. Durum: {durum}", "success")
                st.rerun()

            # Gecmis kontroller
            styled_section("Geçmiş Kontroller", "#475569")
            kontroller = store.find_by_field("dolap_kontrolleri", "dolap_id", sel_k.id)
            kontroller.sort(key=lambda x: x.created_at, reverse=True)
            if kontroller:
                for kn in kontroller[:10]:
                    st.markdown(f"{kn.kontrol_tarihi} | {kn.kontrolcu} | **{kn.durum}** | {kn.notlar}")
            else:
                styled_info_banner("Henuz kontrol kaydi yok.", "info")

    with sub[3]:
        styled_section("Yeni Malzeme Ekle (A7)", "#10b981")
        st.caption("Malzeme katalogu genisletme - eklenen malzeme dolap icerik seciminde gorunecektir.")
        m1, m2 = st.columns(2)
        with m1:
            m_kodu = st.text_input("Malzeme Kodu", key="sag_fak_m_kod", help="Ornek: FAK-M014")
            m_adi = st.text_input("Malzeme Adi *", key="sag_fak_m_ad")
        with m2:
            m_birim = st.text_input("Birim", value="adet", key="sag_fak_m_birim")
            m_min = st.number_input("Varsayilan Min Stok", min_value=0, value=1, key="sag_fak_m_min")
        m_kritik = st.checkbox("Kritik Malzeme", key="sag_fak_m_kritik")

        if st.button("Malzemeyi Katalogu Ekle", type="primary", key="sag_fak_m_kaydet"):
            if not m_adi:
                st.error("Malzeme adi zorunludur.")
            else:
                sablon = MalzemeSablonu(
                    malzeme_kodu=m_kodu or _gen_local_id("FAK-M"),
                    malzeme_adi=m_adi, birim=m_birim,
                    kritik_mi=m_kritik, varsayilan_min_stok=m_min,
                )
                store.upsert("malzeme_sablonlari", sablon)
                styled_info_banner(f"Malzeme katalogu eklendi: {m_adi}", "success")
                st.rerun()


# ============================================================
# SEKME 8: SEMINERLER (SEM-01)
# ============================================================

def _render_seminerler(store: SaglikDataStore):
    sub = st.tabs(["📋 Seminer Listesi", "➕ Yeni Seminer", "📝 Katilim / Yoklama", "➕ Yeni Konu Ekle"])

    with sub[0]:
        styled_section("Seminer Listesi", "#2563eb")
        seminerler = store.load_objects("seminerler")
        seminerler.sort(key=lambda x: x.created_at, reverse=True)
        if seminerler:
            rows = []
            for s in seminerler:
                rows.append({
                    "Kod": s.seminer_kodu, "Konu": s.konu_adi,
                    "Hedef": s.hedef_kitle, "Tarih": s.tarih,
                    "Yer": s.yer, "Egitmen": s.egitmen,
                    "Durum": s.durum, "Katilimci": s.katilimci_sayisi,
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Henuz seminer kaydi yok.", "info")

    with sub[1]:
        styled_section("Yeni Seminer Oluştur", "#10b981")
        konular = store.load_objects("seminer_konulari")
        if not konular:
            styled_info_banner("Konu havuzu bos. Ayarlar > CSV Import ile yukleyin veya Yeni Konu Ekle sekmesini kullanin.", "warning")
        else:
            konu_opts = {f"{k.konu_kodu} - {k.konu_adi}": k for k in konular}
            konu_sec = st.selectbox("Konu Secin", list(konu_opts.keys()), key="sag_sem_konu")
            sel_konu = konu_opts[konu_sec]

            s1, s2 = st.columns(2)
            with s1:
                tarih = st.date_input("Tarih", key="sag_sem_tarih")
                saat = st.text_input("Saat", value="10:00", key="sag_sem_saat")
            with s2:
                yer = st.text_input("Yer", key="sag_sem_yer")
                egitmen = st.text_input("Egitmen", key="sag_sem_egitmen")
            aciklama = st.text_area("Açıklama", key="sag_sem_aciklama", height=60)

            if st.button("Seminer Oluştur", type="primary", key="sag_sem_kaydet"):
                sem = Seminer(
                    seminer_kodu=store.next_seminer_code(),
                    konu_kodu=sel_konu.konu_kodu, konu_adi=sel_konu.konu_adi,
                    hedef_kitle=sel_konu.hedef_kitle,
                    tarih=tarih.isoformat() if tarih else "", saat=saat,
                    yer=yer, egitmen=egitmen, aciklama=aciklama,
                )
                store.upsert("seminerler", sem)
                styled_info_banner(f"Seminer oluşturuldu: {sem.seminer_kodu}", "success")
                st.rerun()

    with sub[2]:
        styled_section("Katilim / Yoklama", "#2563eb")
        seminerler = store.load_objects("seminerler")
        planli = [s for s in seminerler if s.durum == "Planli"]
        if not planli:
            styled_info_banner("Planli seminer yok.", "info")
        else:
            sem_opts = {f"{s.seminer_kodu} - {s.konu_adi} ({s.tarih})": s for s in planli}
            sem_sec = st.selectbox("Seminer Secin", list(sem_opts.keys()), key="sag_sem_kat_sec")
            sel_sem = sem_opts[sem_sec]

            students = load_shared_students()
            if students:
                mevcut_katilimlar = store.find_by_field("seminer_katilimlari", "seminer_id", sel_sem.id)
                mevcut_ids = {k.ogrenci_id for k in mevcut_katilimlar}

                st.caption(f"Toplam ogrenci: {len(students)}, Mevcut katilim: {len(mevcut_ids)}")

                if st.button("Tüm Öğrencileri Ekle", key="sag_sem_kat_tumunu"):
                    count = 0
                    for s in students:
                        sid = s.get("id", "")
                        if sid and sid not in mevcut_ids:
                            kat = SeminerKatilim(
                                seminer_id=sel_sem.id,
                                ogrenci_id=sid,
                                ogrenci_adi=f"{s.get('ad', '')} {s.get('soyad', '')}".strip(),
                                sinif=str(s.get("sinif", "")),
                                sube=str(s.get("sube", "")),
                            )
                            store.upsert("seminer_katilimlari", kat)
                            count += 1
                    sel_sem.katilimci_sayisi = len(mevcut_ids) + count
                    sel_sem.updated_at = _now()
                    store.upsert("seminerler", sel_sem)
                    styled_info_banner(f"{count} ogrenci eklendi.", "success")
                    st.rerun()

                if st.button("Semineri Tamamla", key="sag_sem_kat_tamam"):
                    sel_sem.durum = "Tamamlandı"
                    sel_sem.updated_at = _now()
                    store.upsert("seminerler", sel_sem)
                    styled_info_banner("Seminer tamamlandı.", "success")
                    st.rerun()

                if mevcut_katilimlar:
                    rows = [{"Öğrenci": k.ogrenci_adi, "Sınıf": f"{k.sinif}/{k.sube}",
                             "Katildi": "Evet" if k.katildi else "Hayir"} for k in mevcut_katilimlar]
                    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    with sub[3]:
        styled_section("Yeni Seminer Konusu Ekle (B)", "#10b981")
        st.caption("Konu havuzunu genisletin - eklenen konu seminer olusturma ekraninda gorunecektir.")
        nk1, nk2 = st.columns(2)
        with nk1:
            nk_kod = st.text_input("Konu Kodu", key="sag_sem_nk_kod", help="Ornek: SEM-K006")
            nk_adi = st.text_input("Konu Adi *", key="sag_sem_nk_ad")
        with nk2:
            nk_hedef = st.text_input("Hedef Kitle", key="sag_sem_nk_hedef", help="Ornek: Tümü, İlkokul+Ortaokul")
            nk_etiket = st.text_input("Etiket", key="sag_sem_nk_etiket")

        if st.button("Konu Ekle", type="primary", key="sag_sem_nk_kaydet"):
            if not nk_adi:
                st.error("Konu adi zorunludur.")
            else:
                konu = SeminerKonusu(
                    konu_kodu=nk_kod or _gen_local_id("SEM-K"),
                    konu_adi=nk_adi, hedef_kitle=nk_hedef, etiket=nk_etiket,
                )
                store.upsert("seminer_konulari", konu)
                styled_info_banner(f"Konu eklendi: {nk_adi}", "success")
                st.rerun()


# ============================================================
# SEKME 9: RAPORLAR
# ============================================================

def _render_raporlar(store: SaglikDataStore):
    sub = st.tabs(["🏥 Revir Raporu", "💊 Ilac Cizelgesi", "🚑 Kaza Analizi",
                    "🗄️ Dolap Uygunluk", "📅 Seminer Raporu", "📊 Aylık Özet"])

    with sub[0]:
        styled_section("Revir Ziyaret Raporu", "#0d9488")
        ziyaretler = store.load_objects("revir_ziyaretleri")
        if ziyaretler:
            styled_stat_row([
                ("Toplam Ziyaret", len(ziyaretler), "#0d9488", "\U0001f3e5"),
                ("Bugün", len([z for z in ziyaretler if z.basvuru_tarihi == _today_str()]), "#2563eb", "\U0001f4c5"),
                ("Takip Gerekli", len([z for z in ziyaretler if z.takip_gerekiyor]), "#f59e0b", "\u26a0\ufe0f"),
            ])
            # Sikayet dagilimi
            kat_count = {}
            for z in ziyaretler:
                k = z.sikayet_kategorisi or "Diger"
                kat_count[k] = kat_count.get(k, 0) + 1
            if kat_count:
                styled_section("Sikayet Dagilimi", "#8b5cf6")
                sorted_kat = dict(sorted(kat_count.items(), key=lambda x: x[1], reverse=True))
                c_sun, c_bar = st.columns(2)
                with c_sun:
                    st.markdown(ReportStyler.sunburst_chart_svg(sorted_kat, size=175), unsafe_allow_html=True)
                with c_bar:
                    st.markdown(ReportStyler.horizontal_bar_html(sorted_kat, color="#8b5cf6"), unsafe_allow_html=True)
        else:
            styled_info_banner("Henuz revir verisi yok.", "info")

    with sub[1]:
        styled_section("İlaç Uygulama Cizelgesi", "#8b5cf6")
        uygulamalar = store.load_objects("ilac_uygulamalari")
        if uygulamalar:
            rows = []
            for u in uygulamalar:
                rows.append({
                    "Öğrenci": u.ogrenci_adi, "Ilac": u.ilac_adi,
                    "Doz": u.doz, "Tarih": u.uygulama_tarihi,
                    "Saat": u.uygulama_saati, "Durum": u.durum,
                    "Onay": u.veli_onay_durumu,
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Henuz ilac verisi yok.", "info")

    with sub[2]:
        styled_section("Kaza / Olay Analizi", "#ef4444")
        olaylar = store.load_objects("kaza_olaylari")
        if olaylar:
            styled_stat_row([
                ("Toplam Olay", len(olaylar), "#ef4444", "\u26a0\ufe0f"),
            ])
            tip_count = {}
            lok_count = {}
            for o in olaylar:
                tip_count[o.olay_tipi] = tip_count.get(o.olay_tipi, 0) + 1
                lok_count[o.olay_lokasyonu] = lok_count.get(o.olay_lokasyonu, 0) + 1
            c1, c2 = st.columns(2)
            with c1:
                styled_section("Olay Tipi Dagilimi", "#ea580c")
                sorted_tip = dict(sorted(tip_count.items(), key=lambda x: x[1], reverse=True))
                st.markdown(ReportStyler.sunburst_chart_svg(sorted_tip, size=175), unsafe_allow_html=True)
            with c2:
                styled_section("Lokasyon Dagilimi", "#f59e0b")
                sorted_lok = dict(sorted(lok_count.items(), key=lambda x: x[1], reverse=True))
                st.markdown(ReportStyler.horizontal_bar_html(sorted_lok, color="#f59e0b"), unsafe_allow_html=True)
        else:
            styled_info_banner("Henuz kaza/olay verisi yok.", "info")

    with sub[3]:
        styled_section("İlk Yardim Dolabi Uygunluk Raporu", "#ea580c")
        dolaplar = store.load_objects("dolap_kartlari")
        if dolaplar:
            for d in dolaplar:
                uyarilar = DolapDenetleyici.get_uyarilar(d.id, store)
                geciken = DolapDenetleyici.is_kontrol_geciken(d)
                eksik_n = len(uyarilar["eksik"])
                skt_n = len(uyarilar["skt_yaklasan"]) + len(uyarilar["skt_gecen"])
                durum = "Uygun" if not eksik_n and not skt_n and not geciken else "Sorunlu"
                st.markdown(f"**{d.dolap_kodu}** - {d.lokasyon} | "
                            f"Eksik: {eksik_n}, SKT Sorun: {skt_n}, "
                            f"Kontrol: {'GECIKTI' if geciken else 'Normal'} | **{durum}**")
        else:
            styled_info_banner("Henuz dolap verisi yok.", "info")

    with sub[4]:
        styled_section("Seminer Katilim Raporu", "#2563eb")
        seminerler = store.load_objects("seminerler")
        if seminerler:
            rows = []
            for s in seminerler:
                rows.append({
                    "Kod": s.seminer_kodu, "Konu": s.konu_adi,
                    "Tarih": s.tarih, "Durum": s.durum,
                    "Katilimci": s.katilimci_sayisi,
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            styled_info_banner("Henuz seminer verisi yok.", "info")

    with sub[5]:
        styled_section("Aylık Okul Sağlığı Özet Raporu", "#0f766e")
        data = DashboardAggregator.get_dashboard_data(store)
        styled_stat_row([
            ("Toplam Revir", data["toplam_revir"], "#0d9488", "\U0001f3e5"),
            ("Toplam Kart", data["toplam_kart"], "#2563eb", "\U0001f4cb"),
            ("Toplam Olay", len(store.load_objects("kaza_olaylari")), "#ef4444", "\u26a0\ufe0f"),
            ("Toplam Seminer", len(store.load_objects("seminerler")), "#8b5cf6", "\U0001f393"),
        ])
        styled_info_banner("Detayli PDF rapor için asagidaki butonu kullanabilirsiniz.", "info")

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
        _os_revir_raw = store.load_list("revir_ziyaretleri")
        _os_kaza_raw = store.load_list("kaza_olaylari")
        _os_ilac_raw = store.load_list("ilac_uygulamalari")
        _os_kart_raw = store.load_list("saglik_kartlari")
        _os_seminer_raw = store.load_list("seminerler")
        _os_envanter_raw = store.load_list("envanter")
    except Exception:
        _os_revir_raw, _os_kaza_raw, _os_ilac_raw = [], [], []
        _os_kart_raw, _os_seminer_raw, _os_envanter_raw = [], [], []

    def _os_count_by_month(records, month_str, date_fields=("basvuru_tarihi", "created_at", "olay_tarihi", "uygulama_tarihi", "tarih")):
        c = 0
        for r in records:
            for df in date_fields:
                val = r.get(df, "")
                if val and val[:7] == month_str:
                    c += 1
                    break
        return c

    _os_comparisons = [
        {"label": "Revir Ziyaretleri", "current": _os_count_by_month(_os_revir_raw, _cur_month), "previous": _os_count_by_month(_os_revir_raw, _prev_month)},
        {"label": "Kaza/Olaylar", "current": _os_count_by_month(_os_kaza_raw, _cur_month), "previous": _os_count_by_month(_os_kaza_raw, _prev_month)},
        {"label": "İlaç Uygulamalari", "current": _os_count_by_month(_os_ilac_raw, _cur_month), "previous": _os_count_by_month(_os_ilac_raw, _prev_month)},
        {"label": "Seminerler", "current": _os_count_by_month(_os_seminer_raw, _cur_month), "previous": _os_count_by_month(_os_seminer_raw, _prev_month)},
    ]
    st.markdown(period_comparison_row_html(_os_comparisons), unsafe_allow_html=True)

    # ---- AI Onerileri ----
    _os_insights = []

    _toplam_revir = len(_os_revir_raw)
    _toplam_kaza = len(_os_kaza_raw)
    _toplam_kart = len(_os_kart_raw)
    _takip_gerekli = sum(1 for z in _os_revir_raw if z.get("takip_gerekiyor") in (True, "true", "True"))
    _kronik_cnt = sum(1 for k in _os_kart_raw if k.get("kronik_hastalik") not in (None, "", False, "Yok", "yok"))
    _skt_yaklasan = sum(1 for e in _os_envanter_raw if e.get("son_kullanma_tarihi", "") and e.get("son_kullanma_tarihi", "")[:7] <= (_now.replace(day=1) + _td(days=60)).strftime("%Y-%m") and e.get("son_kullanma_tarihi", "") >= _now.strftime("%Y-%m-%d"))

    _kaza_this_month = _os_count_by_month(_os_kaza_raw, _cur_month)
    if _kaza_this_month > 3:
        _os_insights.append({
            "icon": "\u26a0\ufe0f", "title": "Kaza/Olay Artisi",
            "text": f"Bu ay {_kaza_this_month} kaza/olay kaydi girildi. Guvenlik onlemlerinin gozden gecirilmesi ve risk alanlarinin belirlenmesi onerilir.",
            "color": "#ef4444"
        })

    if _takip_gerekli > 5:
        _os_insights.append({
            "icon": "\U0001f3e5", "title": "Takip Bekleyen Öğrenciler",
            "text": f"{_takip_gerekli} revir ziyaretinde takip gerekiyor. Bu ogrencilerin durumlarinin yakindan izlenmesi ve gerekirse aileyle iletisime gecilmesi onerilir.",
            "color": "#f59e0b"
        })

    if _kronik_cnt > 0:
        _os_insights.append({
            "icon": "\U0001f4ca", "title": "Kronik Hastalik Takibi",
            "text": f"{_kronik_cnt} ogrencinin kronik hastalik kaydi mevcut. Duzenli kontrol takvimi olusturulmasi ve ilac takibi yapilmasi onerilir.",
            "color": "#8b5cf6"
        })

    if _skt_yaklasan > 0:
        _os_insights.append({
            "icon": "\U0001f4e6", "title": "Son Kullanma Tarihi Yaklasan Malzeme",
            "text": f"{_skt_yaklasan} saglik malzemesinin son kullanma tarihi yaklasıyor. Envanter kontrolu ve yenileme siparisi verilmesi onerilir.",
            "color": "#ea580c"
        })

    _os_insights.append({
        "icon": "\U0001f4a1", "title": "Genel Oneri",
        "text": f"Toplam {_toplam_revir} revir ziyareti, {_toplam_kaza} kaza/olay, {_toplam_kart} saglik karti kayitli. Donemsel saglik taramalarinin planlanmasi ve hijyen egitimlerinin surdurul mesi onerilir.",
        "color": "#2563eb"
    })

    _os_insights.append({
        "icon": "\U0001f489", "title": "Asi Takibi",
        "text": "Öğrenci asi kayitlarinin guncellenmesi ve eksik asilarin tamamlanmasi için veli bilgilendirmesi yapilmasi onerilir.",
        "color": "#0d9488"
    })

    st.markdown(ai_recommendations_html(_os_insights), unsafe_allow_html=True)

    # ---- Kurumsal Kunye ----
    st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

    # ---- PDF Export ----
    st.markdown(_RS.section_divider_html("Okul Sağlığı PDF Raporu", "#1e40af"), unsafe_allow_html=True)
    if st.button("\U0001f4e5 Okul Sağlığı Raporu Oluştur (PDF)", key="os_full_pdf_btn", use_container_width=True):
        try:
            _sections = [
                {
                    "title": "Sağlık Genel İstatistikler",
                    "metrics": [
                        ("Revir Ziyareti", _toplam_revir, "#0d9488"),
                        ("Kaza/Olay", _toplam_kaza, "#ef4444"),
                        ("Sağlık Kartı", _toplam_kart, "#2563eb"),
                        ("Seminer", len(_os_seminer_raw), "#8b5cf6"),
                    ],
                    "text": f"Takip Gerekli: {_takip_gerekli} | Kronik Hastalik: {_kronik_cnt} | SKT Yaklasan Malzeme: {_skt_yaklasan}",
                },
                {
                    "title": "Donemsel Karsilastirma",
                    "text": " | ".join([f"{c['label']}: {c['current']} (onceki: {c['previous']})" for c in _os_comparisons]),
                },
            ]
            _pdf_bytes = generate_module_pdf("Okul Sağlığı Hizmetleri Raporu", _sections)
            render_pdf_download_button(_pdf_bytes, "okul_sagligi_raporu.pdf", "Okul Sağlığı Raporu Indir", "os_full_dl")
        except Exception as _e:
            st.error(f"PDF olusturulurken hata: {_e}")


# ============================================================
# SEKME 10: AYARLAR
# ============================================================

def _render_ayarlar(store: SaglikDataStore):
    sub = st.tabs(["🔧 Bilesen Yönetimi", "⚙️ Genel Ayarlar", "📥 CSV Import", "📜 Erisim Logu"])

    with sub[0]:
        styled_section("Secmeli Bilesen Yönetimi", "#0d9488")
        st.caption("Tik olmayan bilesen sistemde gorunmez. Degisiklikleri kaydetmek için butona basin.")
        bilesenler = store.load_objects("bilesenler")
        bilesen_map = {b.bilesen_kodu: b for b in bilesenler}

        new_states = {}
        for kod, adi in BILESEN_KODLARI.items():
            mevcut = bilesen_map.get(kod)
            varsayilan = kod in VARSAYILAN_AKTIF_BILESENLER
            aktif = mevcut.aktif_mi if mevcut else varsayilan
            new_states[kod] = st.checkbox(f"{kod} - {adi}", value=aktif, key=f"sag_bil_{kod}")

        if st.button("Bilesen Ayarlarini Kaydet", type="primary", key="sag_bil_kaydet"):
            for kod, adi in BILESEN_KODLARI.items():
                mevcut = bilesen_map.get(kod)
                if mevcut:
                    mevcut.aktif_mi = new_states[kod]
                    mevcut.updated_at = _now()
                    store.upsert("bilesenler", mevcut)
                else:
                    b = SaglikBilesen(bilesen_kodu=kod, bilesen_adi=adi, aktif_mi=new_states[kod])
                    store.upsert("bilesenler", b)
            styled_info_banner("Bilesen ayarlari kaydedildi.", "success")
            st.rerun()

    with sub[1]:
        styled_section("Genel Ayarlar", "#8b5cf6")
        settings = store.get_settings()
        kvkk = st.checkbox("KVKK Log Zorunlu", value=settings.kvkk_log_zorunlu, key="sag_ay_kvkk")
        med_onay = st.checkbox("Ilac: Veli Onayi Zorunlu", value=settings.med_onay_zorunlu, key="sag_ay_medonay")
        med_rapor = st.checkbox("Ilac: Doktor Raporu Zorunlu", value=settings.med_rapor_zorunlu, key="sag_ay_medrapor")
        fak_gun = st.number_input("Dolap SKT Uyari Esigi (gun)", min_value=1, value=settings.fak_skt_uyari_gun, key="sag_ay_fakgun")
        fak_gecikme = st.checkbox("Dolap Kontrol Gecikme Uyarisi", value=settings.fak_kontrol_gecikme_uyari, key="sag_ay_fakgec")
        rapor_maske = st.checkbox("Rapor Detay Maskeli", value=settings.rapor_detay_maskeli, key="sag_ay_maske")

        if st.button("Ayarlari Kaydet", type="primary", key="sag_ay_kaydet"):
            new_settings = SaglikSettings(
                kvkk_log_zorunlu=kvkk, med_onay_zorunlu=med_onay, med_rapor_zorunlu=med_rapor,
                fak_skt_uyari_gun=fak_gun, fak_kontrol_gecikme_uyari=fak_gecikme,
                rapor_detay_maskeli=rapor_maske,
            )
            store.save_settings(new_settings)
            styled_info_banner("Ayarlar kaydedildi.", "success")
            st.rerun()

    with sub[2]:
        styled_section("CSV Import", "#10b981")
        st.caption("SAG-01 kurulum dosyalarini iceri aktarin. Sira: Bilesenler > Ayarlar > Malzeme > Seminer Konulari")

        import_type = st.selectbox("Import Tipi", [
            "Bilesenler (SAG-01_IMPORT_Bilesenler.csv)",
            "Ayarlar (SAG-01_IMPORT_Ayarlar.csv)",
            "İlk Yardim Malzeme (SAG-01_IMPORT_İlkYardim_MalzemeListesi.csv)",
            "Seminer Konulari (SAG-01_IMPORT_Seminer_Konulari.csv)",
        ], key="sag_imp_tip")

        uploaded = st.file_uploader("CSV Dosyasi Yukle", type=["csv"], key="sag_imp_file")
        if uploaded:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(uploaded, allowed_types=["csv"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                uploaded = None
        if uploaded and st.button("Import Et", type="primary", key="sag_imp_run"):
            try:
                content = uploaded.getvalue().decode("utf-8-sig")
                reader = csv.DictReader(io.StringIO(content))
                rows = list(reader)
                count = 0

                if "Bilesenler" in import_type:
                    for r in rows:
                        b = SaglikBilesen(
                            bilesen_kodu=r.get("bilesen_kodu", ""),
                            bilesen_adi=r.get("bilesen_adi", ""),
                            aktif_mi=bool(int(r.get("aktif_mi", "0"))),
                            aciklama=r.get("aciklama", ""),
                        )
                        store.upsert("bilesenler", b)
                        count += 1

                elif "Ayarlar" in import_type:
                    for r in rows:
                        a = SaglikAyar(
                            ayar_kodu=r.get("ayar_kodu", ""),
                            ayar_adi=r.get("ayar_adi", ""),
                            deger=r.get("deger", ""),
                            aciklama=r.get("aciklama", ""),
                        )
                        store.upsert("ayarlar", a)
                        count += 1

                elif "Malzeme" in import_type:
                    for r in rows:
                        m = MalzemeSablonu(
                            malzeme_kodu=r.get("malzeme_kodu", ""),
                            malzeme_adi=r.get("malzeme_adi", ""),
                            birim=r.get("birim", "adet"),
                            kritik_mi=bool(int(r.get("kritik_mi", "0"))),
                            varsayilan_min_stok=int(r.get("varsayilan_min_stok", "0")),
                            aciklama=r.get("aciklama", ""),
                        )
                        store.upsert("malzeme_sablonlari", m)
                        count += 1

                elif "Seminer" in import_type:
                    for r in rows:
                        k = SeminerKonusu(
                            konu_kodu=r.get("konu_kodu", ""),
                            konu_adi=r.get("konu_adi", ""),
                            hedef_kitle=r.get("hedef_kitle", ""),
                            etiket=r.get("etiket", ""),
                            aciklama=r.get("aciklama", ""),
                        )
                        store.upsert("seminer_konulari", k)
                        count += 1

                styled_info_banner(f"{count} kayit basariyla import edildi.", "success")
                st.rerun()
            except Exception as e:
                st.error(f"Import hatasi: {e}")

    with sub[3]:
        styled_section("KVKK Erisim Logu", "#ef4444")
        loglar = store.load_list("erisim_logu")
        loglar.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        if loglar:
            filtre_tip = st.selectbox("İşlem Filtre", ["Tümü"] + ERISIM_ISLEMLERI, key="sag_log_filtre")
            filtered = loglar
            if filtre_tip != "Tümü":
                filtered = [l for l in filtered if l.get("islem") == filtre_tip]
            if filtered:
                rows = []
                for l in filtered[:50]:
                    rows.append({
                        "Tarih": l.get("timestamp", "")[:16],
                        "İşlem": l.get("islem", ""),
                        "Tip": l.get("entity_tipi", ""),
                        "Açıklama": l.get("entity_aciklama", ""),
                        "Kullanıcı": l.get("kullanici", ""),
                    })
                st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
            else:
                styled_info_banner("Filtre sonucu bos.", "info")
        else:
            styled_info_banner("Henuz erisim logu yok.", "info")


# ============================================================
# ANA RENDER FONKSIYONU
# ============================================================

def render_okul_sagligi():
    """Ana giris noktasi - app.py tarafindan cagrilir."""
    _inject_sag_css()
    styled_header(
        "Okul Sağlığı ve Sağlık Takip",
        "SAG-01 Revir, Ilac, Kaza, Envanter, İlk Yardim ve Seminer Yönetimi",
        "\U0001f3e5",
    )
    store = _get_sag_store()
    aktif = store.get_aktif_bilesenler()

    # Dinamik tab olusturma
    tab_names = ["\U0001f4ca Dashboard", "\U0001f4cb Sağlık Kartı"]
    tab_funcs = [_render_dashboard, _render_saglik_karti]

    if "REV-01" in aktif:
        tab_names.append("\U0001f3e5 Revir Ziyareti")
        tab_funcs.append(_render_revir_ziyareti)
    if "MED-01" in aktif:
        tab_names.append("\U0001f48a İlaç Uygulama")
        tab_funcs.append(_render_ilac_uygulama)
    if "INC-01" in aktif:
        tab_names.append("🚑 Kaza / Olay")
        tab_funcs.append(_render_kaza_olay)
    if "INV-01" in aktif:
        tab_names.append("\U0001f4e6 Envanter")
        tab_funcs.append(_render_envanter)
    if "FAK-01" in aktif:
        tab_names.append("🗄️ İlk Yardım Dolapları")
        tab_funcs.append(_render_ilk_yardim_dolaplari)
    if "SEM-01" in aktif:
        tab_names.append("📅 Seminerler")
        tab_funcs.append(_render_seminerler)

    tab_names.append("📈 Raporlar")
    tab_funcs.append(_render_raporlar)

    # YENİ: Salgın Takip
    tab_names.append("🌡️ Salgın Takip")
    tab_funcs.append(_sag_salgin_wrapper)
    # YENİ: Aşı Takvimi
    tab_names.append("💉 Aşı & Kontrol")
    tab_funcs.append(_sag_asi_wrapper)
    # YENİ: Risk Profili
    tab_names.append("🧠 Risk Profili")
    tab_funcs.append(_sag_risk_wrapper)

    # SÜPER: Acil Durum Merkezi
    tab_names.append("🚨 Acil Durum")
    tab_funcs.append(_sag_acil_wrapper)
    # SÜPER: Beslenme & Hijyen
    tab_names.append("🍎 Beslenme & Hijyen")
    tab_funcs.append(_sag_beslenme_wrapper)
    # SÜPER: Spor Muafiyet
    tab_names.append("🏃 Spor Muafiyet")
    tab_funcs.append(_sag_spor_wrapper)

    # MEGA: Çocuk Gelişim
    tab_names.append("📈 Çocuk Gelişim")
    tab_funcs.append(_sag_gelisim_wrapper)
    # MEGA: Afet Yönetimi
    tab_names.append("🆘 Afet Yönetimi")
    tab_funcs.append(_sag_afet_wrapper)
    # MEGA: Sağlık Pasaportu
    tab_names.append("🪪 Sağlık Pasaportu")
    tab_funcs.append(_sag_pasaport_wrapper)

    # ZİRVE: Wellness Endeksi
    tab_names.append("🌟 Wellness")
    tab_funcs.append(_sag_wellness_wrapper)
    # ZİRVE: AI Tahmin
    tab_names.append("🧠 AI Tahmin")
    tab_funcs.append(_sag_ai_tahmin_wrapper)
    # ZİRVE: Kampanya
    tab_names.append("🎓 Kampanya")
    tab_funcs.append(_sag_kampanya_wrapper)

    tab_names.append("\u2699\ufe0f Ayarlar")
    tab_funcs.append(_render_ayarlar)
    tab_names.append("\U0001f916 Smarti")
    tab_funcs.append(None)  # Smarti handled separately

    render_smarti_welcome("okul_sagligi")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("okul_sagligi_egitim_yili")

    tabs = st.tabs(tab_names)
    for i, func in enumerate(tab_funcs):
        with tabs[i]:
            if func is not None:
                func(store)
            else:
                # Smarti tab
                def _sag_smarti_context():
                    try:
                        k = len(store.load_objects("saglik_kartlari"))
                        z = len(store.load_objects("revir_ziyaretleri"))
                        iu = len(store.load_objects("ilac_uygulamalari"))
                        o = len(store.load_objects("kaza_olaylari"))
                        s = len(store.load_objects("seminerler"))
                        return f"Sağlık karti: {k}, Revir ziyareti: {z}, Ilac uygulama: {iu}, Kaza/olay: {o}, Seminer: {s}"
                    except Exception:
                        return ""
                render_smarti_chat("okul_sagligi", data_context_fn=_sag_smarti_context)
