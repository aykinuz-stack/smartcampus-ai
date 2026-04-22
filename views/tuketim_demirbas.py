"""
TDM-01 Günlük Tüketim ve Demirbas Modulu - Streamlit UI
========================================================
Dashboard, gunluk tuketim, stok durumu, tuketim raporlari,
demirbas kayit, zimmet yonetimi, AI tavsiye, ayarlar.
"""

from __future__ import annotations

import json, os, csv, io, uuid
from datetime import datetime, date, timedelta
from typing import Any

import streamlit as st
from utils.ui_kit import confirm_action
import pandas as pd

from utils.tenant import get_tenant_dir
from utils.shared_data import load_shared_staff, get_staff_display_options

from models.tuketim_demirbas import (
    TuketimKategori, TuketimUrunu, TuketimHareketi,
    DemirbasKategori, Demirbas, ZimmetKaydi, TuketimZimmet,
    TDMAyar, TDMLog,
    Tedarikci, SatinAlmaTalebi, FiyatTeklifi, SiparisTakip,
    TDMDataStore, StokYoneticisi, TuketimAnalizcisi,
    DemirbasRaporlayici, AITavsiyeMotoru,
    TUKETIM_KATEGORILERI, HAREKET_TIPLERI,
    HAREKET_NEDENLERI_GIRIS, HAREKET_NEDENLERI_CIKIS,
    DEMIRBAS_DURUMLARI, ZIMMET_DURUMLARI,
    DEMIRBAS_KATEGORILERI, BIRIMLER, LOKASYONLAR,
    SATIN_ALMA_DURUMLARI, SATIN_ALMA_ONCELIKLERI, ODEME_YONTEMLERI,
    _now, _today,
)
from utils.auth import AuthManager
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("tuketim_demirbas")
except Exception:
    pass


# ============================================================
# YARDIMCI FONKSIYONLAR
# ============================================================

def _get_tdm_store() -> TDMDataStore:
    base = os.path.join(get_tenant_dir(), "tdm")
    return TDMDataStore(base)


def _today_str() -> str:
    return date.today().isoformat()


def _format_currency(val: float) -> str:
    return f"{val:,.2f} TL"


def _format_number(val: float) -> str:
    if val == int(val):
        return f"{int(val):,}"
    return f"{val:,.1f}"


# Varsayilan okul tuketim urunleri
_VARSAYILAN_URUNLER = [
    # (urun_adi, kategori, birim, min_stok, birim_fiyat)
    ("A4 Fotokopi Kagidi (500'lu)", "Kirtasiye", "paket", 20, 85.0),
    ("A3 Fotokopi Kagidi (500'lu)", "Kirtasiye", "paket", 5, 150.0),
    ("Toner (Siyah)", "Kirtasiye", "adet", 5, 450.0),
    ("Toner (Renkli)", "Kirtasiye", "adet", 3, 650.0),
    ("Tahta Kalemi (Siyah)", "Kirtasiye", "adet", 20, 15.0),
    ("Tahta Kalemi (Mavi)", "Kirtasiye", "adet", 15, 15.0),
    ("Tahta Kalemi (Kirmizi)", "Kirtasiye", "adet", 10, 15.0),
    ("Tahta Kalemi (Yesil)", "Kirtasiye", "adet", 10, 15.0),
    ("Tahta Silgisi", "Kirtasiye", "adet", 10, 25.0),
    ("Tukenmez Kalem (Mavi)", "Kirtasiye", "kutu", 5, 45.0),
    ("Tukenmez Kalem (Siyah)", "Kirtasiye", "kutu", 5, 45.0),
    ("Kurşun Kalem", "Kirtasiye", "kutu", 5, 35.0),
    ("Silgi", "Kirtasiye", "kutu", 3, 30.0),
    ("Zimba Makinesi Teli", "Kirtasiye", "kutu", 10, 12.0),
    ("Atas", "Kirtasiye", "kutu", 5, 8.0),
    ("Dosya Klasor (Genis)", "Kirtasiye", "adet", 20, 18.0),
    ("Telli Dosya", "Kirtasiye", "paket", 10, 35.0),
    ("Poset Dosya", "Kirtasiye", "paket", 10, 25.0),
    ("Yapiskan Bant", "Kirtasiye", "adet", 10, 12.0),
    ("Makas", "Kirtasiye", "adet", 5, 20.0),
    ("Cetvel (30cm)", "Kirtasiye", "adet", 10, 10.0),
    ("Post-it Not Kagidi", "Kirtasiye", "paket", 10, 15.0),
    ("Boya Kalemi (12'li)", "Kirtasiye", "paket", 10, 35.0),
    ("Cizim Kagidi (100'lu)", "Kirtasiye", "paket", 5, 40.0),
    ("Camasir Suyu (5 Lt)", "Temizlik", "adet", 10, 55.0),
    ("Yuzey Temizleyici (5 Lt)", "Temizlik", "adet", 10, 45.0),
    ("Cam Temizleyici (5 Lt)", "Temizlik", "adet", 5, 40.0),
    ("Sivi Sabun (5 Lt)", "Temizlik", "adet", 10, 50.0),
    ("Tuvalet Kagidi (32'li)", "Temizlik", "paket", 10, 180.0),
    ("Kagit Havlu (12'li)", "Temizlik", "paket", 8, 120.0),
    ("Cop Torbasi (Buyuk)", "Temizlik", "rulo", 15, 30.0),
    ("Cop Torbasi (Orta)", "Temizlik", "rulo", 15, 22.0),
    ("Paspas Kovasi + Paspas", "Temizlik", "adet", 3, 85.0),
    ("Supurge", "Temizlik", "adet", 3, 45.0),
    ("Faras", "Temizlik", "adet", 3, 20.0),
    ("Dezenfektan Sprey", "Temizlik", "adet", 10, 35.0),
    ("Eldiven (100'lu)", "Temizlik", "kutu", 5, 65.0),
    ("Fotokopi Makinesi Bakım Kiti", "Ofis Malzemesi", "adet", 2, 250.0),
    ("Hesap Makinesi", "Ofis Malzemesi", "adet", 3, 80.0),
    ("Mouse", "Ofis Malzemesi", "adet", 3, 60.0),
    ("Klavye", "Ofis Malzemesi", "adet", 2, 120.0),
    ("USB Bellek (32GB)", "Ofis Malzemesi", "adet", 5, 65.0),
    ("Pil (AA) 4'lu", "Elektrik/Elektronik", "paket", 10, 35.0),
    ("Pil (AAA) 4'lu", "Elektrik/Elektronik", "paket", 5, 35.0),
    ("Ampul (LED)", "Elektrik/Elektronik", "adet", 10, 25.0),
    ("Uzatma Kablosu", "Elektrik/Elektronik", "adet", 3, 80.0),
    ("Su (19 Lt Damacana)", "Mutfak/Yemekhane", "adet", 10, 40.0),
    ("Cay (1 Kg)", "Mutfak/Yemekhane", "adet", 5, 120.0),
    ("Seker (5 Kg)", "Mutfak/Yemekhane", "adet", 3, 95.0),
    ("Kahve (500 Gr)", "Mutfak/Yemekhane", "adet", 3, 80.0),
    ("Bardak (Karton 50'li)", "Mutfak/Yemekhane", "paket", 10, 25.0),
    ("Pecete (100'lu)", "Mutfak/Yemekhane", "paket", 10, 15.0),
    ("İlk Yardim Malzemesi", "Saglik Malzemesi", "adet", 5, 30.0),
    ("Maske (50'li)", "Saglik Malzemesi", "kutu", 5, 50.0),
]


def _seed_varsayilan_urunler(store: TDMDataStore):
    """Varsayilan okul tuketim urunlerini yukler (ilk kurulumda)."""
    mevcut = store.load_list("tuketim_urunleri")
    if mevcut:
        return  # Zaten urun var
    for i, (ad, kat, birim, min_stok, fiyat) in enumerate(_VARSAYILAN_URUNLER, 1):
        urun = TuketimUrunu(
            urun_kodu=f"TU-{str(i).zfill(4)}",
            urun_adi=ad,
            kategori=kat,
            birim=birim,
            stok=0.0,
            min_stok=float(min_stok),
            birim_fiyat=fiyat,
        )
        store.upsert("tuketim_urunleri", urun)


# ============================================================
# CSS STILLERI
# ============================================================

def _inject_tdm_css():
    inject_common_css("tdm")
    st.markdown("""<style>
    :root {
        --tdm-primary: #2563eb;
        --tdm-secondary: #ea580c;
        --tdm-success: #10b981;
        --tdm-warning: #f59e0b;
        --tdm-danger: #ef4444;
        --tdm-purple: #8b5cf6;
        --tdm-dark: #0B0F19;
    }
    .stApp > header { background: transparent !important; }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease; border-left: 4px solid #2563eb;
    }
    div[data-testid="stMetric"]:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    </style>""", unsafe_allow_html=True)


# ============================================================
# SEKME 1: DASHBOARD
# ============================================================

def _render_dashboard(store: TDMDataStore):
    styled_header("Dashboard", "Günlük ozet, stok uyarilari, tuketim trendi", icon="📦")

    # KPI'lar
    bugun = _today_str()
    hareketler = store.load_objects("tuketim_hareketleri")
    h_bugun = [h for h in hareketler if h.tarih == bugun]
    giris_bugun = sum(h.miktar for h in h_bugun if h.tip == "Giriş")
    cikis_bugun = sum(h.miktar for h in h_bugun if h.tip == "Çıkış")
    giris_tutar = sum(h.toplam_tutar for h in h_bugun if h.tip == "Giriş")
    cikis_tutar = sum(h.toplam_tutar for h in h_bugun if h.tip == "Çıkış")

    uyarilar = StokYoneticisi.get_stok_uyarilari(store)
    db_ozet = DemirbasRaporlayici.ozet(store)

    # Aylik tuketim
    ay_bas = date.today().replace(day=1).isoformat()
    ay_ozet = TuketimAnalizcisi.donem_ozet(store, ay_bas, bugun)

    styled_stat_row([
        ("Bugün Giriş", _format_number(giris_bugun), "#10b981", "📥"),
        ("Bugün Çıkış", _format_number(cikis_bugun), "#ef4444", "📤"),
        ("Stok Uyari", str(len(uyarilar)), "#f59e0b", "⚠️"),
        ("Toplam Demirbas", str(db_ozet["toplam"]), "#8b5cf6", "🏷️"),
        ("Aktif Zimmet", str(db_ozet["aktif_zimmet"]), "#ea580c", "📋"),
        ("Aylık Tuketim", _format_currency(ay_ozet["cikis_tutar"]), "#2563eb", "💰"),
    ])

    # Son 7 gun trendi
    c1, c2 = st.columns(2)
    with c1:
        styled_section("Son 7 Gün Tuketim Trendi")
        trend = TuketimAnalizcisi.gunluk_trend(store, 7)
        if any(v["cikis"] > 0 for v in trend.values()):
            from utils.report_utils import ReportStyler
            bar_data = {t[-5:]: v["cikis"] for t, v in trend.items()}
            st.markdown(ReportStyler.horizontal_bar_html(bar_data, "#4472C4"), unsafe_allow_html=True)
        else:
            styled_info_banner("Henuz tuketim verisi bulunmuyor.", banner_type="info", icon="📊")

    with c2:
        styled_section("Stok Uyarilari")
        if uyarilar:
            for u in uyarilar[:8]:
                urun = u["urun"]
                renk = u["renk"]
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                background:{renk}10;border-left:3px solid {renk};border-radius:6px;margin:4px 0;font-size:13px;">
                <span style="font-weight:700;color:{renk};">{urun.urun_adi}</span>
                <span style="color:#64748b;margin-left:auto;">Stok: {urun.stok} {urun.birim} (Min: {urun.min_stok})</span>
                </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Tüm stoklar yeterli seviyede.", banner_type="success", icon="✅")

    # Son hareketler
    styled_section("Son Hareketler")
    son_hareketler = sorted(hareketler, key=lambda h: h.created_at, reverse=True)[:10]
    if son_hareketler:
        rows = []
        for h in son_hareketler:
            tip_renk = "🟢" if h.tip == "Giriş" else "🔴"
            rows.append({
                "Tip": f"{tip_renk} {h.tip}",
                "Urun": h.urun_adi,
                "Demirbas Kat.": getattr(h, "demirbas_kategori", "") or "-",
                "Miktar": f"{_format_number(h.miktar)} {h.birim}",
                "Tutar": _format_currency(h.toplam_tutar),
                "Tarih": h.tarih,
                "Neden": h.neden,
                "Teslim Eden": h.teslim_eden,
                "Teslim Alan": h.teslim_alan,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        styled_info_banner("Henuz hareket kaydi bulunmuyor.", banner_type="info", icon="📝")


# ============================================================
# SEKME 2: GUNLUK TUKETIM
# ============================================================

def _render_gunluk_tuketim(store: TDMDataStore):
    styled_header("Günlük Tüketim", "Giriş/cikis kaydi ve gunluk hareket listesi")

    sub_tabs = st.tabs(["⚡ Hızlı Giriş/Çıkış", "📋 Günün Hareketleri", "📅 Tarih Seçimli"])

    # --- Hizli Giris/Cikis ---
    with sub_tabs[0]:
        styled_section("Yeni Hareket Kaydi")
        urunler = store.load_objects("tuketim_urunleri")
        aktif_urunler = [u for u in urunler if u.aktif]

        if not aktif_urunler:
            styled_info_banner("Henuz urun tanimi yok. Asagidan veya Ayarlar sekmesinden urun ekleyin.", banner_type="warning", icon="⚠️")

        # 1) Kategori secimi
        kategoriler = store.load_objects("tuketim_kategorileri")
        kat_adlari = sorted(set(k.ad for k in kategoriler)) if kategoriler else TUKETIM_KATEGORILERI
        secili_kat = st.selectbox("Urun Kategorisi", ["-- Kategori secin --"] + kat_adlari, key="tdm_hr_kat")

        # 2) Secilen kategoriye gore urunleri filtrele
        secili_urun = None
        if secili_kat and secili_kat != "-- Kategori secin --":
            kat_urunler = [u for u in aktif_urunler if u.kategori == secili_kat]
            if kat_urunler:
                urun_options = ["-- Urun secin --"] + [
                    f"{u.urun_adi} [{u.stok} {u.birim}]" for u in kat_urunler
                ]
                urun_idx = st.selectbox("Urun", range(len(urun_options)),
                                        format_func=lambda i: urun_options[i], key="tdm_hr_urun")
                if urun_idx > 0:
                    secili_urun = kat_urunler[urun_idx - 1]
            else:
                styled_info_banner(f"\"{secili_kat}\" kategorisinde henuz urun yok. Asagidan ekleyebilirsiniz.", banner_type="warning", icon="⚠️")

        # 3) Hareket formu
        if secili_urun:
            c1, c2 = st.columns(2)
            with c1:
                tip = st.radio("Hareket Tipi", HAREKET_TIPLERI, horizontal=True, key="tdm_hr_tip")
            with c2:
                nedenler = HAREKET_NEDENLERI_GIRIS if tip == "Giriş" else HAREKET_NEDENLERI_CIKIS
                neden = st.selectbox("Neden", nedenler, key="tdm_hr_neden")

            c3, c4 = st.columns(2)
            with c3:
                miktar = st.number_input("Miktar", min_value=0.0, step=1.0, key="tdm_hr_miktar")
            with c4:
                birim_fiyat = st.number_input("Birim Fiyat (TL)", min_value=0.0, step=0.01,
                                              value=secili_urun.birim_fiyat, key="tdm_hr_fiyat")

            # Demirbas kategorisi
            db_kat_list = [k.ad for k in store.load_objects("demirbas_kategorileri")]
            if not db_kat_list:
                db_kat_list = DEMIRBAS_KATEGORILERI
            mevcut_db_kat = secili_urun.demirbas_kategori or ""

            if tip == "Çıkış" and mevcut_db_kat:
                # Cikis'ta demirbas kategorisi otomatik gelir (urunle ayni)
                db_kat_idx = db_kat_list.index(mevcut_db_kat) if mevcut_db_kat in db_kat_list else 0
                secili_db_kat = st.selectbox(
                    "Demirbas Kategorisi", db_kat_list,
                    index=db_kat_idx, key="tdm_hr_db_kat",
                    disabled=True, help="Urunun giris kaydindaki demirbas kategorisi"
                )
            else:
                # Giris'te veya henuz atanmamissa kullanici secer
                varsayilan_idx = db_kat_list.index(mevcut_db_kat) if mevcut_db_kat in db_kat_list else 0
                secili_db_kat = st.selectbox(
                    "Demirbas Kategorisi", db_kat_list,
                    index=varsayilan_idx,
                    help="Bu urunun bagli oldugu demirbas turu"
                )

            # Teslim eden / alan
            if tip == "Giriş":
                teslim_alan = st.text_input("Teslim Alan", key="tdm_hr_teslim_alan",
                                            help="Malzemeyi teslim alan kisi")
                teslim_eden = ""
            else:
                ct1, ct2 = st.columns(2)
                with ct1:
                    teslim_eden = st.text_input("Teslim Eden", key="tdm_hr_teslim_eden",
                                                help="Malzemeyi depodan teslim eden kisi")
                with ct2:
                    teslim_alan = st.text_input("Teslim Alan", key="tdm_hr_teslim_alan2",
                                                help="Malzemeyi teslim alan kisi")

            aciklama = st.text_area("Açıklama (opsiyonel)", height=68, key="tdm_hr_aciklama")

            if miktar > 0:
                toplam = miktar * birim_fiyat
                st.info(f"Toplam tutar: {_format_currency(toplam)} | Mevcut stok: {secili_urun.stok} {secili_urun.birim} | Demirbas: {secili_db_kat}")

                if tip == "Çıkış" and miktar > secili_urun.stok:
                    st.error(f"Yetersiz stok! Mevcut: {secili_urun.stok} {secili_urun.birim}")

            if st.button("Kaydet", key="tdm_hr_kaydet", use_container_width=True, type="primary"):
                if miktar <= 0:
                    st.error("Miktar 0'dan buyuk olmalidir.")
                else:
                    hareket = TuketimHareketi(
                        urun_id=secili_urun.id,
                        urun_adi=secili_urun.urun_adi,
                        kategori=secili_urun.kategori,
                        demirbas_kategori=secili_db_kat,
                        saat=datetime.now().strftime("%H:%M"),
                        tip=tip,
                        miktar=miktar,
                        birim=secili_urun.birim,
                        birim_fiyat=birim_fiyat,
                        neden=neden,
                        aciklama=aciklama,
                        teslim_eden=teslim_eden,
                        teslim_alan=teslim_alan,
                        kaydeden=st.session_state.get("auth_user", {}).get("name", ""),
                    )
                    ok, msg = store.hareket_kaydet(hareket)
                    if ok:
                        # Urune demirbas kategorisini kaydet
                        if secili_urun.demirbas_kategori != secili_db_kat:
                            secili_urun.demirbas_kategori = secili_db_kat
                            secili_urun.updated_at = datetime.now().isoformat()
                            store.upsert("tuketim_urunleri", secili_urun)

                        # Otomatik zimmet islemleri
                        zimmet_msg = ""
                        if tip == "Giriş" and teslim_alan:
                            tz = store.tuketim_zimmet_giris(hareket, teslim_alan)
                            if tz:
                                zimmet_msg = f" | Zimmet: {teslim_alan} ({hareket.miktar} {hareket.birim})"
                                store.log("tuketim_zimmet_giris", "tuketim_zimmet", tz.id,
                                          f"{hareket.urun_adi} -> {teslim_alan}: {hareket.miktar} {hareket.birim}")
                        elif tip == "Çıkış" and teslim_alan:
                            z_ok, z_msg = store.tuketim_zimmet_cikis(
                                hareket, teslim_eden, teslim_alan)
                            if z_ok:
                                zimmet_msg = f" | {z_msg}"
                                store.log("tuketim_zimmet_cikis", "tuketim_zimmet", hareket.id, z_msg)

                        st.success(msg + zimmet_msg)
                        store.log("hareket_kaydi", "tuketim", hareket.id, msg)
                        st.rerun()
                    else:
                        st.error(msg)

        # 4) Hizli Yeni Kategori Ekle
        st.markdown("---")
        col_kat, col_urun = st.columns(2)
        with col_kat:
            with st.expander("Yeni Kategori Ekle"):
                hk_ad = st.text_input("Kategori Adi", key="tdm_hr_ykat_ad")
                if st.button("Kategori Ekle", key="tdm_hr_ykat_btn"):
                    if hk_ad:
                        store.upsert("tuketim_kategorileri",
                                     TuketimKategori(kod=hk_ad[:3].upper(), ad=hk_ad))
                        st.success(f"Kategori eklendi: {hk_ad}")
                        st.rerun()
                    else:
                        st.error("Kategori adi girin.")

        # 5) Hizli Yeni Urun Ekle
        with col_urun:
            with st.expander("Yeni Urun Ekle"):
                hu_ad = st.text_input("Urun Adi", key="tdm_hr_yurun_ad")
                hu_kat_list = [k.ad for k in store.load_objects("tuketim_kategorileri")]
                if not hu_kat_list:
                    hu_kat_list = TUKETIM_KATEGORILERI
                hu_kat = st.selectbox("Kategori", hu_kat_list, key="tdm_hr_yurun_kat")
                hu_c1, hu_c2 = st.columns(2)
                with hu_c1:
                    hu_birim = st.selectbox("Birim", BIRIMLER, key="tdm_hr_yurun_birim")
                    hu_min = st.number_input("Min Stok", min_value=0.0, step=1.0, key="tdm_hr_yurun_min")
                with hu_c2:
                    hu_fiyat = st.number_input("Birim Fiyat (TL)", min_value=0.0, step=0.01, key="tdm_hr_yurun_fiyat")
                    hu_stok = st.number_input("Başlangıç Stok", min_value=0.0, step=1.0, key="tdm_hr_yurun_stok")
                if st.button("Urun Ekle", key="tdm_hr_yurun_btn", type="primary"):
                    if hu_ad:
                        yeni_kod = store.next_urun_code()
                        yeni = TuketimUrunu(
                            urun_kodu=yeni_kod, urun_adi=hu_ad, kategori=hu_kat,
                            birim=hu_birim, stok=hu_stok, min_stok=hu_min, birim_fiyat=hu_fiyat,
                        )
                        store.upsert("tuketim_urunleri", yeni)
                        st.success(f"Urun eklendi: {yeni_kod} - {hu_ad}")
                        st.rerun()
                    else:
                        st.error("Urun adi girin.")

    # --- Gunun Hareketleri ---
    with sub_tabs[1]:
        styled_section("Bugünün Hareketleri")
        bugun = _today_str()
        hareketler = store.load_objects("tuketim_hareketleri")
        h_bugun = [h for h in hareketler if h.tarih == bugun]
        h_bugun.sort(key=lambda h: h.created_at, reverse=True)

        if h_bugun:
            giris_t = sum(h.miktar for h in h_bugun if h.tip == "Giriş")
            cikis_t = sum(h.miktar for h in h_bugun if h.tip == "Çıkış")
            giris_tl = sum(h.toplam_tutar for h in h_bugun if h.tip == "Giriş")
            cikis_tl = sum(h.toplam_tutar for h in h_bugun if h.tip == "Çıkış")

            styled_stat_row([
                ("Giriş", _format_number(giris_t), "#10b981", "📥"),
                ("Çıkış", _format_number(cikis_t), "#ef4444", "📤"),
                ("Giriş Tutar", _format_currency(giris_tl), "#10b981", "💰"),
                ("Çıkış Tutar", _format_currency(cikis_tl), "#ef4444", "💸"),
            ])

            rows = []
            for h in h_bugun:
                rows.append({
                    "Kod": h.hareket_kodu,
                    "Saat": h.saat,
                    "Tip": h.tip,
                    "Urun": h.urun_adi,
                    "Demirbas Kat.": getattr(h, "demirbas_kategori", "") or "-",
                    "Miktar": f"{_format_number(h.miktar)} {h.birim}",
                    "Tutar": _format_currency(h.toplam_tutar),
                    "Neden": h.neden,
                    "Teslim Eden": h.teslim_eden,
                    "Teslim Alan": h.teslim_alan,
                    "Kaydeden": h.kaydeden,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner("Bugün henuz hareket yok.", banner_type="info", icon="📝")

    # --- Tarih Secimli ---
    with sub_tabs[2]:
        styled_section("Tarih Secimli Görüntüleme")
        secilen_tarih = st.date_input("Tarih secin", value=date.today(), key="tdm_hr_tarih_sec")
        tarih_str = secilen_tarih.isoformat()

        hareketler = store.load_objects("tuketim_hareketleri")
        h_tarih = [h for h in hareketler if h.tarih == tarih_str]
        h_tarih.sort(key=lambda h: h.created_at, reverse=True)

        if h_tarih:
            giris_t = sum(h.miktar for h in h_tarih if h.tip == "Giriş")
            cikis_t = sum(h.miktar for h in h_tarih if h.tip == "Çıkış")
            st.info(f"Toplam: {len(h_tarih)} hareket | Giriş: {_format_number(giris_t)} | Çıkış: {_format_number(cikis_t)}")

            rows = []
            for h in h_tarih:
                rows.append({
                    "Kod": h.hareket_kodu,
                    "Saat": h.saat,
                    "Tip": h.tip,
                    "Urun": h.urun_adi,
                    "Demirbas Kat.": getattr(h, "demirbas_kategori", "") or "-",
                    "Miktar": f"{_format_number(h.miktar)} {h.birim}",
                    "Tutar": _format_currency(h.toplam_tutar),
                    "Neden": h.neden,
                    "Teslim Eden": h.teslim_eden,
                    "Teslim Alan": h.teslim_alan,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner(f"{tarih_str} tarihinde hareket bulunmuyor.", banner_type="info", icon="📅")


# ============================================================
# SEKME 3: STOK DURUMU
# ============================================================

def _render_stok_durumu(store: TDMDataStore):
    styled_header("Stok Durumu", "Tüm urunlerin guncel stok seviyeleri")

    urunler = store.load_objects("tuketim_urunleri")
    aktif_urunler = [u for u in urunler if u.aktif]

    if not aktif_urunler:
        styled_info_banner("Henuz urun tanimi yok.", banner_type="warning", icon="⚠️")
        return

    sub_tabs = st.tabs(["📊 Kategori Bazlı Stok", "📋 Tüm Ürünler Tablosu", "💰 Stok Değeri"])

    # ---- Kategori Bazli Stok ----
    with sub_tabs[0]:
        # Genel KPI
        stok_deger = StokYoneticisi.stok_degeri(store)
        uyarilar = StokYoneticisi.get_stok_uyarilari(store)
        stoklu_urun = len([u for u in aktif_urunler if u.stok > 0])

        styled_stat_row([
            ("Toplam Urun", str(len(aktif_urunler)), "#2563eb", "📦"),
            ("Stoklu Urun", str(stoklu_urun), "#10b981", "✅"),
            ("Stok Degeri", _format_currency(stok_deger["toplam"]), "#8b5cf6", "💰"),
            ("Kritik Stok", str(len([u for u in uyarilar if u["seviye"] == "kritik"])), "#ef4444", "🔴"),
            ("Bos Stok", str(len([u for u in uyarilar if u["seviye"] == "bos"])), "#6b7280", "⚫"),
        ])

        # Kategori bazli gruplama
        kat_map: dict[str, list] = {}
        for u in aktif_urunler:
            kat = u.kategori or "Diger"
            kat_map.setdefault(kat, []).append(u)

        for kat_adi in sorted(kat_map.keys()):
            kat_urunler = kat_map[kat_adi]
            kat_stok_toplam = sum(u.stok for u in kat_urunler)
            kat_deger_toplam = sum(u.stok * u.birim_fiyat for u in kat_urunler)
            kat_stoklu = len([u for u in kat_urunler if u.stok > 0])

            # Kategori baslik rengi
            kat_renk = "#2563eb"
            if any(u.stok <= u.min_stok and u.stok > 0 for u in kat_urunler):
                kat_renk = "#f59e0b"
            if any(u.stok <= 0 for u in kat_urunler):
                kat_renk = "#ef4444"
            if all(u.stok > u.min_stok * 1.5 for u in kat_urunler if u.min_stok > 0):
                kat_renk = "#10b981"

            with st.expander(f"📁 {kat_adi}  —  {len(kat_urunler)} urun | "
                f"Stoklu: {kat_stoklu} | Deger: {_format_currency(kat_deger_toplam)}",
                expanded=(kat_stoklu > 0),
            ):
                rows = []
                for u in sorted(kat_urunler, key=lambda x: x.urun_adi):
                    if u.stok <= 0:
                        durum = "⚫ Bos"
                    elif u.stok <= u.min_stok:
                        durum = "🔴 Kritik"
                    elif u.stok <= u.min_stok * 1.5:
                        durum = "🟡 Dusuk"
                    else:
                        durum = "🟢 Yeterli"
                    rows.append({
                        "Kod": u.urun_kodu,
                        "Urun": u.urun_adi,
                        "Stok": f"{_format_number(u.stok)} {u.birim}",
                        "Min Stok": f"{_format_number(u.min_stok)}",
                        "Durum": durum,
                        "Birim Fiyat": _format_currency(u.birim_fiyat),
                        "Stok Degeri": _format_currency(u.stok * u.birim_fiyat),
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ---- Tum Urunler Tablosu (Stok Detay) ----
    with sub_tabs[1]:
        styled_section("Stok Detay Tablosu - Tüm Urunler")

        # Filtre
        kategoriler = sorted(set(u.kategori for u in aktif_urunler if u.kategori))
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            kat_filtre = st.selectbox("Kategori", ["Tümü"] + kategoriler, key="tdm_stok_kat")
        with c2:
            durum_filtre = st.selectbox("Durum", ["Tümü", "Stoklu", "Bos", "Kritik"], key="tdm_stok_dur")
        with c3:
            siralama = st.selectbox("Sıralama", ["Urun Adi (A-Z)", "Stok (Az->Çok)", "Stok (Çok->Az)"], key="tdm_stok_sira")

        gosterilecek = list(aktif_urunler)
        if kat_filtre != "Tümü":
            gosterilecek = [u for u in gosterilecek if u.kategori == kat_filtre]
        if durum_filtre == "Stoklu":
            gosterilecek = [u for u in gosterilecek if u.stok > 0]
        elif durum_filtre == "Bos":
            gosterilecek = [u for u in gosterilecek if u.stok <= 0]
        elif durum_filtre == "Kritik":
            gosterilecek = [u for u in gosterilecek if 0 < u.stok <= u.min_stok]

        if siralama == "Stok (Az->Çok)":
            gosterilecek.sort(key=lambda u: u.stok)
        elif siralama == "Stok (Çok->Az)":
            gosterilecek.sort(key=lambda u: u.stok, reverse=True)
        else:
            gosterilecek.sort(key=lambda u: u.urun_adi)

        st.info(f"Toplam {len(gosterilecek)} urun listeleniyor")

        rows = []
        for u in gosterilecek:
            if u.stok <= 0:
                durum = "⚫ Bos"
            elif u.stok <= u.min_stok:
                durum = "🔴 Kritik"
            elif u.stok <= u.min_stok * 1.5:
                durum = "🟡 Dusuk"
            else:
                durum = "🟢 Yeterli"

            tahmini = StokYoneticisi.tahmini_bitis(store, u.id)
            tahmin_str = tahmini if tahmini else "-"

            rows.append({
                "Kod": u.urun_kodu,
                "Urun": u.urun_adi,
                "Kategori": u.kategori,
                "Stok": f"{_format_number(u.stok)} {u.birim}",
                "Min Stok": f"{_format_number(u.min_stok)} {u.birim}",
                "Durum": durum,
                "Birim Fiyat": _format_currency(u.birim_fiyat),
                "Stok Degeri": _format_currency(u.stok * u.birim_fiyat),
                "Tahmini Bitis": tahmin_str,
            })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner("Filtreye uyan urun bulunamadı.", banner_type="info", icon="📦")

    # ---- Stok Degeri ----
    with sub_tabs[2]:
        styled_section("Stok Deger Analizi")
        stok_deger = StokYoneticisi.stok_degeri(store)

        styled_stat_row([
            ("Toplam Stok Degeri", _format_currency(stok_deger["toplam"]), "#2563eb", "💰"),
            ("Kategori Sayısı", str(len(stok_deger["kategori_dagilimi"])), "#8b5cf6", "📁"),
        ])

        if stok_deger["kategori_dagilimi"]:
            styled_section("Kategori Bazli Deger Dagilimi")

            # Tablo
            kat_rows = []
            for kat, deger in sorted(stok_deger["kategori_dagilimi"].items(), key=lambda x: x[1], reverse=True):
                oran = (deger / stok_deger["toplam"] * 100) if stok_deger["toplam"] > 0 else 0
                kat_rows.append({
                    "Kategori": kat,
                    "Stok Degeri": _format_currency(deger),
                    "Oran": f"%{oran:.1f}",
                })
            st.dataframe(pd.DataFrame(kat_rows), use_container_width=True, hide_index=True)

            # Sunburst grafik (ic: kategori toplam, dis: urun detay)
            from utils.report_utils import ReportStyler
            deger_map = {k: v for k, v in stok_deger["kategori_dagilimi"].items() if v > 0}
            if deger_map:
                # Her kategorideki urunleri al (dis halka icin)
                urunler = store.load_objects("tuketim_urunleri")
                outer = {}
                for kat in deger_map:
                    kat_urunler = [(u.urun_adi, u.stok * u.birim_fiyat)
                                   for u in urunler if u.aktif and u.kategori == kat
                                   and u.stok * u.birim_fiyat > 0]
                    kat_urunler.sort(key=lambda x: x[1], reverse=True)
                    outer[kat] = kat_urunler[:6]  # En degerli 6 urun
                st.markdown(
                    ReportStyler.sunburst_chart_svg(
                        deger_map, outer, title="Kategori Bazli Stok Degeri"
                    ),
                    unsafe_allow_html=True,
                )


# ============================================================
# SEKME 4: TUKETIM RAPORLARI
# ============================================================

def _render_tuketim_raporlari(store: TDMDataStore):
    styled_header("Tüketim Raporları", "Günlük, haftalik, aylik ve karsilastirmali raporlar")

    sub_tabs = st.tabs(["📅 Günlük", "📆 Haftalık", "📊 Aylık", "📅 Tarih Aralığı", "🔄 Karşılaştırma", "📄 PDF Rapor"])

    # --- Gunluk ---
    with sub_tabs[0]:
        styled_section("Günlük Rapor")
        secilen = st.date_input("Tarih", value=date.today(), key="tdm_rap_gun")
        tarih_str = secilen.isoformat()
        ozet = TuketimAnalizcisi.donem_ozet(store, tarih_str, tarih_str)

        styled_stat_row([
            ("Toplam Hareket", str(ozet["toplam_hareket"]), "#2563eb", "📊"),
            ("Giriş", _format_number(ozet["giris_adet"]), "#10b981", "📥"),
            ("Çıkış", _format_number(ozet["cikis_adet"]), "#ef4444", "📤"),
            ("Çıkış Tutar", _format_currency(ozet["cikis_tutar"]), "#ea580c", "💸"),
        ])

        if ozet["kategori_cikis"]:
            from utils.report_utils import ReportStyler
            col_bar, col_sun = st.columns([1, 1])
            with col_bar:
                styled_section("Kategori Bazli Tuketim")
                st.markdown(ReportStyler.horizontal_bar_html(ozet["kategori_cikis"], "#4472C4"), unsafe_allow_html=True)
            with col_sun:
                styled_section("Tuketim Dagilimi")
                cikis_map = {k: v for k, v in ozet["kategori_cikis"].items() if v > 0}
                if cikis_map:
                    st.markdown(
                        ReportStyler.sunburst_chart_svg(cikis_map, title="Kategori Dagilimi"),
                        unsafe_allow_html=True,
                    )

        if ozet["en_cok_tuketilen"]:
            styled_section("En Çok Tuketilen Urunler")
            rows = [{"Urun": u["urun_adi"], "Miktar": _format_number(u["miktar"])} for u in ozet["en_cok_tuketilen"]]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # --- Haftalik ---
    with sub_tabs[1]:
        styled_section("Haftalık Rapor")
        bugun = date.today()
        hafta_bas = (bugun - timedelta(days=bugun.weekday())).isoformat()
        hafta_bit = bugun.isoformat()
        st.info(f"Bu hafta: {hafta_bas} - {hafta_bit}")

        ozet = TuketimAnalizcisi.donem_ozet(store, hafta_bas, hafta_bit)
        styled_stat_row([
            ("Hareket", str(ozet["toplam_hareket"]), "#4472C4", "📊"),
            ("Giriş", _format_number(ozet["giris_adet"]), "#10b981", "📥"),
            ("Çıkış", _format_number(ozet["cikis_adet"]), "#ef4444", "📤"),
            ("Tuketim Tutar", _format_currency(ozet["cikis_tutar"]), "#ED7D31", "💸"),
        ])

        # Gun bazli karsilastirma
        trend = TuketimAnalizcisi.gunluk_trend(store, 7)
        if any(v["cikis"] > 0 for v in trend.values()):
            from utils.report_utils import ReportStyler
            col_bar, col_sun = st.columns([1, 1])
            with col_bar:
                styled_section("Gün Bazli Tuketim")
                bar_data = {}
                gun_adlari = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"]
                for t, v in trend.items():
                    try:
                        d = date.fromisoformat(t)
                        gun_adi = gun_adlari[d.weekday()]
                        bar_data[f"{gun_adi} ({t[-5:]})"] = v["cikis"]
                    except (ValueError, IndexError):
                        bar_data[t] = v["cikis"]
                st.markdown(ReportStyler.horizontal_bar_html(bar_data, "#4472C4"), unsafe_allow_html=True)
            with col_sun:
                if ozet["kategori_cikis"]:
                    styled_section("Haftalık Kategori Dagilimi")
                    cikis_map = {k: v for k, v in ozet["kategori_cikis"].items() if v > 0}
                    if cikis_map:
                        st.markdown(
                            ReportStyler.sunburst_chart_svg(cikis_map, title="Kategori Dagilimi"),
                            unsafe_allow_html=True,
                        )

    # --- Aylik ---
    with sub_tabs[2]:
        styled_section("Aylık Rapor")
        bugun = date.today()
        ay_bas = bugun.replace(day=1).isoformat()
        ay_bit = bugun.isoformat()
        st.info(f"Bu ay: {ay_bas} - {ay_bit}")

        ozet = TuketimAnalizcisi.donem_ozet(store, ay_bas, ay_bit)
        styled_stat_row([
            ("Hareket", str(ozet["toplam_hareket"]), "#4472C4", "📊"),
            ("Giriş Tutar", _format_currency(ozet["giris_tutar"]), "#10b981", "💰"),
            ("Çıkış Tutar", _format_currency(ozet["cikis_tutar"]), "#ef4444", "💸"),
        ])

        # Onceki ayla karsilastirma
        onceki_ay_bit = (bugun.replace(day=1) - timedelta(days=1))
        onceki_ay_bas = onceki_ay_bit.replace(day=1).isoformat()
        onceki_ay_bit_str = onceki_ay_bit.isoformat()

        kars = TuketimAnalizcisi.karsilastir(store, onceki_ay_bas, onceki_ay_bit_str, ay_bas, ay_bit)
        degisim = kars["cikis_tutar_degisim"]
        ok = "📈" if degisim > 0 else "📉" if degisim < 0 else "➡️"
        renk = "#ef4444" if degisim > 0 else "#10b981" if degisim < 0 else "#64748b"
        styled_info_banner(
            f"Önceki aya gore tuketim tutari degisimi: <b style='color:{renk};'>%{degisim:+.1f} {ok}</b>",
            renk, "📊"
        )

        if ozet["kategori_cikis"]:
            from utils.report_utils import ReportStyler
            col_bar, col_sun = st.columns([1, 1])
            with col_bar:
                styled_section("Kategori Bazli Tuketim")
                st.markdown(
                    ReportStyler.horizontal_bar_html(
                        {k: v for k, v in ozet["kategori_cikis"].items() if v > 0}, "#4472C4"
                    ),
                    unsafe_allow_html=True,
                )
            with col_sun:
                styled_section("Kategori Bazli Dagilim")
                cikis_map = {k: v for k, v in ozet["kategori_cikis"].items() if v > 0}
                if cikis_map:
                    # Urun detayli sunburst
                    hareketler = store.load_objects("tuketim_hareketleri")
                    ay_hareketler = [h for h in hareketler
                                     if h.tip == "Çıkış" and ay_bas <= h.tarih <= ay_bit]
                    outer = {}
                    for kat in cikis_map:
                        urun_map: dict[str, float] = {}
                        for h in ay_hareketler:
                            if h.kategori == kat:
                                urun_map[h.urun_adi] = urun_map.get(h.urun_adi, 0) + h.miktar
                        items = sorted(urun_map.items(), key=lambda x: x[1], reverse=True)[:6]
                        outer[kat] = items
                    st.markdown(
                        ReportStyler.sunburst_chart_svg(
                            cikis_map, outer if any(outer.values()) else None,
                            title="Aylık Tuketim Dagilimi"
                        ),
                        unsafe_allow_html=True,
                    )

        if ozet["en_cok_tuketilen"]:
            styled_section("En Çok Tuketilen 10 Urun")
            rows = [{"Sira": i+1, "Urun": u["urun_adi"], "Miktar": _format_number(u["miktar"])}
                    for i, u in enumerate(ozet["en_cok_tuketilen"])]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # --- Tarih Araligi ---
    with sub_tabs[3]:
        styled_section("Özel Tarih Araligi")
        c1, c2 = st.columns(2)
        with c1:
            bas = st.date_input("Başlangıç", value=date.today() - timedelta(days=30), key="tdm_rap_bas")
        with c2:
            bit = st.date_input("Bitis", value=date.today(), key="tdm_rap_bit")

        ozet = TuketimAnalizcisi.donem_ozet(store, bas.isoformat(), bit.isoformat())
        styled_stat_row([
            ("Hareket", str(ozet["toplam_hareket"]), "#4472C4", "📊"),
            ("Giriş", _format_number(ozet["giris_adet"]), "#10b981", "📥"),
            ("Çıkış", _format_number(ozet["cikis_adet"]), "#ef4444", "📤"),
            ("Çıkış Tutar", _format_currency(ozet["cikis_tutar"]), "#ED7D31", "💸"),
        ])

        if ozet["kategori_cikis"]:
            from utils.report_utils import ReportStyler
            col_bar, col_sun = st.columns([1, 1])
            with col_bar:
                styled_section("Kategori Bazli Tuketim")
                st.markdown(
                    ReportStyler.horizontal_bar_html(
                        {k: v for k, v in ozet["kategori_cikis"].items() if v > 0}, "#4472C4"
                    ),
                    unsafe_allow_html=True,
                )
            with col_sun:
                styled_section("Tuketim Dagilimi")
                cikis_map = {k: v for k, v in ozet["kategori_cikis"].items() if v > 0}
                if cikis_map:
                    hareketler = store.load_objects("tuketim_hareketleri")
                    donem_hr = [h for h in hareketler
                                if h.tip == "Çıkış" and bas.isoformat() <= h.tarih <= bit.isoformat()]
                    outer = {}
                    for kat in cikis_map:
                        urun_map: dict[str, float] = {}
                        for h in donem_hr:
                            if h.kategori == kat:
                                urun_map[h.urun_adi] = urun_map.get(h.urun_adi, 0) + h.miktar
                        items = sorted(urun_map.items(), key=lambda x: x[1], reverse=True)[:6]
                        outer[kat] = items
                    st.markdown(
                        ReportStyler.sunburst_chart_svg(
                            cikis_map, outer if any(outer.values()) else None,
                            title="Donem Tuketim Dagilimi"
                        ),
                        unsafe_allow_html=True,
                    )

        if ozet["en_cok_tuketilen"]:
            styled_section("En Çok Tuketilen Urunler")
            rows = [{"Urun": u["urun_adi"], "Miktar": _format_number(u["miktar"])} for u in ozet["en_cok_tuketilen"]]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # --- Karsilastirma ---
    with sub_tabs[4]:
        styled_section("Donem Karsilastirmasi")
        st.markdown("**Donem 1**")
        c1, c2 = st.columns(2)
        with c1:
            d1_bas = st.date_input("Başlangıç", value=date.today() - timedelta(days=60), key="tdm_kars_d1_bas")
        with c2:
            d1_bit = st.date_input("Bitis", value=date.today() - timedelta(days=31), key="tdm_kars_d1_bit")

        st.markdown("**Donem 2**")
        c3, c4 = st.columns(2)
        with c3:
            d2_bas = st.date_input("Başlangıç", value=date.today() - timedelta(days=30), key="tdm_kars_d2_bas")
        with c4:
            d2_bit = st.date_input("Bitis", value=date.today(), key="tdm_kars_d2_bit")

        if st.button("Karsilastir", key="tdm_kars_btn", type="primary"):
            kars = TuketimAnalizcisi.karsilastir(
                store, d1_bas.isoformat(), d1_bit.isoformat(),
                d2_bas.isoformat(), d2_bit.isoformat(),
            )
            c_a, c_b = st.columns(2)
            with c_a:
                styled_section(f"Donem 1: {d1_bas} - {d1_bit}")
                st.metric("Tuketim Adet", _format_number(kars["donem1"]["cikis_adet"]))
                st.metric("Tuketim Tutar", _format_currency(kars["donem1"]["cikis_tutar"]))
            with c_b:
                styled_section(f"Donem 2: {d2_bas} - {d2_bit}")
                st.metric("Tuketim Adet", _format_number(kars["donem2"]["cikis_adet"]),
                           delta=f"%{kars['cikis_adet_degisim']:+.1f}")
                st.metric("Tuketim Tutar", _format_currency(kars["donem2"]["cikis_tutar"]),
                           delta=f"%{kars['cikis_tutar_degisim']:+.1f}")

            # Yan yana sunburst chart karsilastirmasi
            from utils.report_utils import ReportStyler
            d1_ozet = TuketimAnalizcisi.donem_ozet(store, d1_bas.isoformat(), d1_bit.isoformat())
            d2_ozet = TuketimAnalizcisi.donem_ozet(store, d2_bas.isoformat(), d2_bit.isoformat())

            d1_kat = {k: v for k, v in d1_ozet.get("kategori_cikis", {}).items() if v > 0}
            d2_kat = {k: v for k, v in d2_ozet.get("kategori_cikis", {}).items() if v > 0}

            if d1_kat or d2_kat:
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    if d1_kat:
                        st.markdown(
                            ReportStyler.sunburst_chart_svg(
                                d1_kat, title=f"Donem 1", size=280
                            ),
                            unsafe_allow_html=True,
                        )
                    else:
                        styled_info_banner("Donem 1 için veri yok.", banner_type="info", icon="📊")
                with col_d2:
                    if d2_kat:
                        st.markdown(
                            ReportStyler.sunburst_chart_svg(
                                d2_kat, title=f"Donem 2", size=280
                            ),
                            unsafe_allow_html=True,
                        )
                    else:
                        styled_info_banner("Donem 2 için veri yok.", banner_type="info", icon="📊")

    # --- PDF Rapor ---
    with sub_tabs[5]:
        styled_section("PDF Rapor Oluştur")
        c1, c2 = st.columns(2)
        with c1:
            pdf_bas = st.date_input("Başlangıç", value=date.today().replace(day=1), key="tdm_pdf_bas")
        with c2:
            pdf_bit = st.date_input("Bitis", value=date.today(), key="tdm_pdf_bit")

        if st.button("PDF Oluştur", key="tdm_pdf_btn", type="primary"):
            try:
                from utils.report_utils import ReportPDFGenerator, get_institution_info
                ozet = TuketimAnalizcisi.donem_ozet(store, pdf_bas.isoformat(), pdf_bit.isoformat())
                stok = StokYoneticisi.stok_degeri(store)

                pdf = ReportPDFGenerator(
                    "Tuketim Raporu",
                    f"{pdf_bas.isoformat()} - {pdf_bit.isoformat()}",
                )
                info = get_institution_info()
                pdf.add_header(kurum_adi=info.get("name", ""))

                pdf.add_section("Genel Özet")
                pdf.add_metrics([
                    ("Toplam Hareket", ozet["toplam_hareket"], "#2563eb"),
                    ("Giriş Adet", f"{ozet['giris_adet']:.0f}", "#10b981"),
                    ("Çıkış Adet", f"{ozet['cikis_adet']:.0f}", "#ef4444"),
                    ("Çıkış Tutar", f"{ozet['cikis_tutar']:.2f} TL", "#ea580c"),
                ])

                if ozet["kategori_cikis"]:
                    pdf.add_section("Kategori Bazli Tuketim")
                    kat_df = pd.DataFrame([
                        {"Kategori": k, "Miktar": f"{v:.0f}"}
                        for k, v in sorted(ozet["kategori_cikis"].items(), key=lambda x: x[1], reverse=True)
                    ])
                    pdf.add_table(kat_df)
                    pdf.add_bar_chart(ozet["kategori_cikis"], "Kategori Dagilimi", "#2563eb")

                if ozet["en_cok_tuketilen"]:
                    pdf.add_section("En Çok Tuketilen Urunler")
                    top_df = pd.DataFrame([
                        {"Sira": i+1, "Urun": u["urun_adi"], "Miktar": f"{u['miktar']:.0f}"}
                        for i, u in enumerate(ozet["en_cok_tuketilen"])
                    ])
                    pdf.add_table(top_df)

                pdf.add_section("Stok Durumu")
                pdf.add_text(f"Toplam Stok Degeri: {stok['toplam']:.2f} TL")

                pdf_bytes = pdf.generate()
                st.download_button(
                    "PDF Indir", pdf_bytes,
                    file_name=f"tuketim_raporu_{pdf_bas}_{pdf_bit}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.success("PDF oluşturuldu!")
            except Exception as e:
                st.error(f"PDF olusturma hatasi: {e}")

    # ============================================================
    # PERFORMANS KARSILASTIRMA, AI ONERILERI, PDF, KUNYE
    # ============================================================
    try:
        from utils.report_utils import (
            ai_recommendations_html, period_comparison_row_html,
            generate_module_pdf, render_pdf_download_button,
            render_report_kunye_html, ReportStyler as _RS,
        )

        st.markdown(_RS.section_divider_html("Performans Karsilastirma", "#0d9488"), unsafe_allow_html=True)

        now = datetime.now()
        cur_m_start = now.replace(day=1).isoformat()[:10]
        cur_m_end = now.isoformat()[:10]
        prev_m_end_dt = now.replace(day=1) - timedelta(days=1)
        prev_m_start = prev_m_end_dt.replace(day=1).isoformat()[:10]
        prev_m_end = prev_m_end_dt.isoformat()[:10]

        cur_tuk = TuketimAnalizcisi.donem_ozet(store, cur_m_start, cur_m_end)
        prev_tuk = TuketimAnalizcisi.donem_ozet(store, prev_m_start, prev_m_end)

        demirbaslar_all = store.load_objects("demirbaslar")
        cur_demirbas_count = len([d for d in demirbaslar_all
                                  if hasattr(d, "created_at") and d.created_at[:7] == now.strftime("%Y-%m")])
        prev_demirbas_count = len([d for d in demirbaslar_all
                                   if hasattr(d, "created_at") and d.created_at[:7] == prev_m_end_dt.strftime("%Y-%m")])

        stok_val = StokYoneticisi.stok_degeri(store)

        comparisons = [
            {"label": "Tuketim Maliyet (TL)", "current": cur_tuk["cikis_tutar"], "previous": prev_tuk["cikis_tutar"]},
            {"label": "Tuketim Adet", "current": cur_tuk["cikis_adet"], "previous": prev_tuk["cikis_adet"]},
            {"label": "Yeni Demirbas", "current": cur_demirbas_count, "previous": prev_demirbas_count},
            {"label": "Giriş Adet", "current": cur_tuk["giris_adet"], "previous": prev_tuk["giris_adet"]},
        ]
        st.markdown(period_comparison_row_html(comparisons), unsafe_allow_html=True)

        # ---- AI Onerileri ----
        insights = []

        # 1) Maliyet optimizasyonu
        if cur_tuk["cikis_tutar"] > 0 and prev_tuk["cikis_tutar"] > 0:
            maliyet_degisim = ((cur_tuk["cikis_tutar"] - prev_tuk["cikis_tutar"]) / prev_tuk["cikis_tutar"]) * 100
            if maliyet_degisim > 20:
                insights.append({
                    "icon": "💸", "title": "Maliyet Artisi Uyarisi",
                    "text": f"Tuketim maliyeti onceki aya gore <b>%{maliyet_degisim:.1f}</b> artti. "
                            f"En cok tuketilen urunlerde alternatif tedarikci veya toplu alis indirimi arastirilmali.",
                    "color": "#ef4444",
                })
            elif maliyet_degisim < -10:
                insights.append({
                    "icon": "✅", "title": "Maliyet Tasarrufu",
                    "text": f"Tuketim maliyeti onceki aya gore <b>%{abs(maliyet_degisim):.1f}</b> azaldi. "
                            f"Başarılı maliyet yonetimi devam ettirilmeli.",
                    "color": "#10b981",
                })

        # 2) Stok uyarisi
        kritik_urunler = StokYoneticisi.kritik_stok(store) if hasattr(StokYoneticisi, "kritik_stok") else []
        if kritik_urunler:
            insights.append({
                "icon": "📦", "title": "Kritik Stok Uyarisi",
                "text": f"<b>{len(kritik_urunler)}</b> urun kritik stok seviyesinin altinda. "
                        f"Acil tedarik sureci baslatilmali.",
                "color": "#f59e0b",
            })
        else:
            insights.append({
                "icon": "📦", "title": "Stok Durumu",
                "text": f"Toplam stok degeri: <b>{stok_val.get('toplam', 0):,.2f} TL</b>. "
                        f"Stok seviyeleri normal aralikta.",
                "color": "#2563eb",
            })

        # 3) En cok tuketilen urunler
        if cur_tuk["en_cok_tuketilen"]:
            top3 = cur_tuk["en_cok_tuketilen"][:3]
            urun_list = ", ".join([f"<b>{u['urun_adi']}</b> ({u['miktar']:.0f})" for u in top3])
            insights.append({
                "icon": "🔥", "title": "En Çok Tuketilen Urunler",
                "text": f"Bu ay en cok tuketilen: {urun_list}. "
                        f"Bu urunler için toplu alis veya alternatif urun degerlendirmesi yapilabilir.",
                "color": "#8b5cf6",
            })

        # 4) Kategori analizi
        kat_cikis = cur_tuk.get("kategori_cikis", {})
        if kat_cikis:
            en_cok_kat = max(kat_cikis, key=kat_cikis.get)
            insights.append({
                "icon": "📊", "title": "Kategori Analizi",
                "text": f"En yuksek tuketim kategorisi: <b>{en_cok_kat}</b> ({kat_cikis[en_cok_kat]:,.0f} adet). "
                        f"Bu kategoride tasarruf plani hazirlanabilir.",
                "color": "#0d9488",
            })

        # 5) Demirbas onerileri
        toplam_demirbas = len(demirbaslar_all)
        if toplam_demirbas > 0:
            aktif_demirbas = len([d for d in demirbaslar_all
                                  if hasattr(d, "durum") and d.durum in ("Aktif", "Kullanimda")])
            kullanim_orani = (aktif_demirbas / toplam_demirbas) * 100
            insights.append({
                "icon": "🏷️", "title": "Demirbas Verimlilik",
                "text": f"Toplam <b>{toplam_demirbas}</b> demirbas kayitli, <b>{aktif_demirbas}</b> aktif kullanımda "
                        f"(<b>%{kullanim_orani:.0f}</b>). Kullanilmayan varliklar için "
                        f"yeniden dagitim veya hurda islemleri degerlendirilebilir.",
                "color": "#ea580c",
            })

        if insights:
            st.markdown(ai_recommendations_html(insights), unsafe_allow_html=True)

        # ---- Kurumsal Kunye ----
        st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

        # ---- PDF Export ----
        st.markdown(_RS.section_divider_html("PDF Genel Rapor", "#1e40af"), unsafe_allow_html=True)
        if st.button("📥 Tuketim & Demirbas Genel Raporu (PDF)", key="td_pdf_export_btn", use_container_width=True):
            try:
                sections = [
                    {
                        "title": "Bu Ay Tuketim Özeti",
                        "metrics": [
                            ("Hareket", str(cur_tuk["toplam_hareket"]), "#2563eb"),
                            ("Giriş", f"{cur_tuk['giris_adet']:.0f}", "#10b981"),
                            ("Çıkış", f"{cur_tuk['cikis_adet']:.0f}", "#ef4444"),
                            ("Tutar", f"{cur_tuk['cikis_tutar']:,.2f} TL", "#ea580c"),
                        ],
                    },
                    {
                        "title": "Stok Durumu",
                        "text": f"Toplam Stok Degeri: {stok_val.get('toplam', 0):,.2f} TL | "
                                f"Toplam Demirbas: {toplam_demirbas} adet",
                    },
                ]
                kat_data = {k: v for k, v in kat_cikis.items() if v > 0}
                if kat_data:
                    sections.append({
                        "title": "Kategori Bazli Tuketim",
                        "bar_data": kat_data,
                        "bar_title": "Kategori Dagilimi",
                        "bar_color": "#4472C4",
                    })
                if insights:
                    import re as _re
                    oneri_text = "\n".join([f"- {i['title']}: {_re.sub(r'<[^>]+>', '', i['text'])}" for i in insights])
                    sections.append({"title": "AI Onerileri", "text": oneri_text})

                pdf_bytes = generate_module_pdf("Tuketim & Demirbas Raporu", sections)
                render_pdf_download_button(pdf_bytes, "td_raporu.pdf", "Tuketim & Demirbas Raporu", "td_dl")
            except Exception as e:
                st.error(f"PDF olusturma hatasi: {e}")
    except Exception:
        pass  # report_utils yuklenemezse sessizce gec


# ============================================================
# SEKME 5: DEMIRBAS KAYIT
# ============================================================

def _render_demirbas_kayit(store: TDMDataStore):
    styled_header("Demirbaş Kayıt", "Tüm demirbas kayitlari ve yeni kayit")

    sub_tabs = st.tabs(["📋 Demirbaş Listesi", "➕ Yeni Demirbaş", "🔍 Demirbaş Detay"])

    # --- Liste ---
    with sub_tabs[0]:
        styled_section("Demirbaş Listesi")
        demirbaslar = store.load_objects("demirbaslar")

        if not demirbaslar:
            styled_info_banner("Henuz demirbas kaydi yok.", banner_type="info", icon="🏷️")
        else:
            # Filtre
            c1, c2, c3 = st.columns(3)
            with c1:
                kategoriler = sorted(set(d.kategori for d in demirbaslar if d.kategori))
                kat_f = st.selectbox("Kategori", ["Tümü"] + kategoriler, key="tdm_db_kat_f")
            with c2:
                durum_f = st.selectbox("Durum", ["Tümü"] + DEMIRBAS_DURUMLARI, key="tdm_db_dur_f")
            with c3:
                arama = st.text_input("Arama", key="tdm_db_arama", placeholder="Ad, kod, marka...")

            filtrelenmis = demirbaslar
            if kat_f != "Tümü":
                filtrelenmis = [d for d in filtrelenmis if d.kategori == kat_f]
            if durum_f != "Tümü":
                filtrelenmis = [d for d in filtrelenmis if d.durum == durum_f]
            if arama:
                q = arama.lower()
                filtrelenmis = [d for d in filtrelenmis if q in d.ad.lower() or q in d.demirbas_kodu.lower() or q in d.marka.lower()]

            ozet = DemirbasRaporlayici.ozet(store)
            styled_stat_row([
                ("Toplam", str(ozet["toplam"]), "#8b5cf6", "🏷️"),
                ("Aktif", str(ozet["durum_dagilim"].get("Aktif", 0)), "#10b981", "✅"),
                ("Zimmetli", str(ozet["durum_dagilim"].get("Zimmetli", 0)), "#ea580c", "📋"),
                ("Toplam Deger", _format_currency(ozet["toplam_deger"]), "#2563eb", "💰"),
            ])

            rows = []
            for d in filtrelenmis:
                rows.append({
                    "Kod": d.demirbas_kodu,
                    "Ad": d.ad,
                    "Kategori": d.kategori,
                    "Marka": d.marka,
                    "Model": d.model,
                    "Lokasyon": d.lokasyon,
                    "Durum": d.durum,
                    "Fiyat": _format_currency(d.fiyat),
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # --- Yeni Demirbas ---
    with sub_tabs[1]:
        styled_section("Yeni Demirbas Kaydi")

        yeni_kod = store.next_demirbas_code()
        st.info(f"Demirbas Kodu: **{yeni_kod}**")

        c1, c2 = st.columns(2)
        with c1:
            db_ad = st.text_input("Demirbas Adi", key="tdm_db_ad")
            db_kat = st.selectbox("Kategori", DEMIRBAS_KATEGORILERI, key="tdm_db_kat")
            db_marka = st.text_input("Marka", key="tdm_db_marka")
            db_model = st.text_input("Model", key="tdm_db_model")
        with c2:
            db_seri = st.text_input("Seri No", key="tdm_db_seri")
            db_lokasyon = st.selectbox("Lokasyon", LOKASYONLAR, key="tdm_db_lok")
            db_fiyat = st.number_input("Satın Alma Fiyati (TL)", min_value=0.0, step=1.0, key="tdm_db_fiyat")
            db_tarih = st.date_input("Satın Alma Tarihi", value=date.today(), key="tdm_db_tarih")

        c3, c4 = st.columns(2)
        with c3:
            db_garanti = st.date_input("Garanti Bitis", value=None, key="tdm_db_garanti")
        with c4:
            db_durum = st.selectbox("Durum", DEMIRBAS_DURUMLARI, key="tdm_db_durum")

        db_notlar = st.text_area("Notlar", height=68, key="tdm_db_notlar")

        if st.button("Kaydet", key="tdm_db_kaydet", type="primary", use_container_width=True):
            if not db_ad:
                st.error("Demirbas adi zorunludur.")
            else:
                yeni = Demirbas(
                    demirbas_kodu=yeni_kod,
                    ad=db_ad,
                    kategori=db_kat,
                    marka=db_marka,
                    model=db_model,
                    seri_no=db_seri,
                    lokasyon=db_lokasyon,
                    satin_alma_tarihi=db_tarih.isoformat() if db_tarih else "",
                    fiyat=db_fiyat,
                    durum=db_durum,
                    garanti_bitis=db_garanti.isoformat() if db_garanti else "",
                    notlar=db_notlar,
                )
                store.upsert("demirbaslar", yeni)
                store.log("demirbas_kaydi", "demirbas", yeni.id, f"{yeni_kod} - {db_ad}")
                st.success(f"Demirbas kaydedildi: {yeni_kod} - {db_ad}")
                st.rerun()

    # --- Demirbas Detay ---
    with sub_tabs[2]:
        styled_section("Demirbas Detay")
        demirbaslar = store.load_objects("demirbaslar")
        if not demirbaslar:
            styled_info_banner("Demirbas kaydi yok.", banner_type="info", icon="🏷️")
            return

        db_options = ["-- Demirbas secin --"] + [f"{d.demirbas_kodu} - {d.ad}" for d in demirbaslar]
        db_idx = st.selectbox("Demirbas", range(len(db_options)), format_func=lambda i: db_options[i], key="tdm_db_detay_sec")

        if db_idx > 0:
            secili = demirbaslar[db_idx - 1]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Kod:** {secili.demirbas_kodu}")
                st.markdown(f"**Ad:** {secili.ad}")
                st.markdown(f"**Kategori:** {secili.kategori}")
                st.markdown(f"**Marka/Model:** {secili.marka} {secili.model}")
                st.markdown(f"**Seri No:** {secili.seri_no}")
            with c2:
                st.markdown(f"**Lokasyon:** {secili.lokasyon}")
                st.markdown(f"**Durum:** {secili.durum}")
                st.markdown(f"**Fiyat:** {_format_currency(secili.fiyat)}")
                st.markdown(f"**Satın Alma:** {secili.satin_alma_tarihi}")
                st.markdown(f"**Garanti Bitis:** {secili.garanti_bitis or '-'}")

            if secili.notlar:
                st.markdown(f"**Notlar:** {secili.notlar}")

            # Zimmet gecmisi
            styled_section("Zimmet Geçmişi")
            zimmetler = store.find_by_field("zimmet_kayitlari", "demirbas_id", secili.id)
            if zimmetler:
                rows = []
                for z in sorted(zimmetler, key=lambda x: x.created_at, reverse=True):
                    rows.append({
                        "Kod": z.zimmet_kodu,
                        "Personel": z.personel_adi,
                        "Unvan": z.personel_unvan,
                        "Zimmet Tarihi": z.zimmet_tarihi,
                        "İade Tarihi": z.iade_tarihi or "-",
                        "Durum": z.durum,
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            else:
                st.info("Bu demirbas için zimmet kaydi bulunmuyor.")


# ============================================================
# SEKME 6: ZIMMET YONETIMI
# ============================================================

def _render_zimmet_yonetimi(store: TDMDataStore):
    styled_header("Zimmet Yönetimi", "Tuketim malzeme zimmeti, demirbas zimmeti, PDF form")

    # Genel KPI
    tz_ozet = store.tuketim_zimmet_ozet()
    db_ozet = DemirbasRaporlayici.ozet(store)
    styled_stat_row([
        ("Tuketim Zimmet", str(tz_ozet["aktif_zimmet"]), "#4472C4", "📦"),
        ("Personel", str(tz_ozet["personel_sayisi"]), "#ED7D31", "👤"),
        ("Tuketim Deger", _format_currency(tz_ozet["toplam_deger"]), "#FFC000", "💰"),
        ("Demirbas Zimmet", str(db_ozet["durum_dagilim"].get("Zimmetli", 0)), "#8b5cf6", "🏷️"),
    ])

    sub_tabs = st.tabs([
        "📋 Tüketim Zimmetleri", "📥 Zimmet Formu Giriş", "📤 Zimmet Formu Çıkış",
        "🗄️ Demirbaş Zimmet", "🔄 Demirbaş İade", "📄 Zimmet PDF"
    ])

    # ===== TUKETIM ZIMMETLERI (aktif liste) =====
    with sub_tabs[0]:
        styled_section("Aktif Tuketim Zimmetleri")
        tum_tz = store.load_objects("tuketim_zimmetleri")
        aktif_tz = [z for z in tum_tz if z.durum == "Aktif" and z.miktar > 0]

        if aktif_tz:
            # Personel bazli gruplama
            personel_map: dict[str, list] = {}
            for z in aktif_tz:
                personel_map.setdefault(z.personel_adi, []).append(z)

            for p_adi in sorted(personel_map.keys()):
                zimmetler = personel_map[p_adi]
                toplam = sum(z.miktar * z.birim_fiyat for z in zimmetler)
                with st.expander(f"{p_adi} — {len(zimmetler)} kalem | Deger: {_format_currency(toplam)}",
                    expanded=False,
                ):
                    rows = []
                    for z in zimmetler:
                        rows.append({
                            "Zimmet Kodu": z.zimmet_kodu,
                            "Urun": z.urun_adi,
                            "Urun Kodu": z.urun_kodu,
                            "Kategori": z.kategori,
                            "Demirbas Kat.": z.demirbas_kategori,
                            "Miktar": f"{_format_number(z.miktar)} {z.birim}",
                            "Birim Fiyat": _format_currency(z.birim_fiyat),
                            "Toplam Deger": _format_currency(z.miktar * z.birim_fiyat),
                            "Tarih": z.zimmet_tarihi,
                        })
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner("Aktif tuketim zimmeti bulunmuyor.", banner_type="info", icon="📦")

        # Tum gecmis
        if tum_tz:
            styled_section("Tüm Tuketim Zimmet Geçmişi")
            tum_tz.sort(key=lambda z: z.created_at, reverse=True)
            rows = []
            for z in tum_tz[:50]:
                rows.append({
                    "Kod": z.zimmet_kodu,
                    "Urun": z.urun_adi,
                    "Personel": z.personel_adi,
                    "Miktar": f"{_format_number(z.miktar)} {z.birim}",
                    "Tip": z.tip,
                    "Durum": z.durum,
                    "Tarih": z.zimmet_tarihi,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ===== ZIMMET FORMU GIRIS =====
    with sub_tabs[1]:
        styled_section("Zimmet Formu - Giriş (Teslim Alma)", "#4472C4")
        styled_info_banner(
            "Tuketim malzemesi teslim alindiginda zimmet kaydi olusturulur. "
            "Hızlı Giriş/Çıkış ekranindan yapilan girisler otomatik zimmetlenir.", banner_type="info", icon="📥")

        urunler = store.load_objects("tuketim_urunleri")
        aktif_urunler = [u for u in urunler if u.aktif and u.stok > 0]

        if not aktif_urunler:
            styled_info_banner("Stokta urun bulunmuyor.", banner_type="warning", icon="⚠️")
        else:
            urun_options = ["-- Urun secin --"] + [
                f"{u.urun_kodu} - {u.urun_adi} [{u.stok} {u.birim}]" for u in aktif_urunler
            ]
            urun_idx = st.selectbox("Urun", range(len(urun_options)),
                                     format_func=lambda i: urun_options[i], key="tdm_zg_urun")

            if urun_idx > 0:
                secili = aktif_urunler[urun_idx - 1]

                staff = load_shared_staff()
                if staff:
                    p_options = ["-- Teslim Alan secin --"] + [
                        f"{s.get('ad', '')} {s.get('soyad', '')} - {s.get('unvan', '')}" + (f" ({s.get('brans', '')})" if s.get('brans') else "")
                        for s in staff
                    ]
                    p_idx = st.selectbox("Teslim Alan", range(len(p_options)),
                                          format_func=lambda i: p_options[i], key="tdm_zg_per")
                    if p_idx > 0:
                        p = staff[p_idx - 1]
                        zg_personel = f"{p.get('ad', '')} {p.get('soyad', '')}".strip()
                        zg_unvan = p.get("unvan", "")
                    else:
                        zg_personel = ""
                        zg_unvan = ""
                else:
                    zg_personel = st.text_input("Teslim Alan Adi", key="tdm_zg_per_ad")
                    zg_unvan = st.text_input("Unvani", key="tdm_zg_per_unv")

                zg_miktar = st.number_input(f"Miktar ({secili.birim})", min_value=0.0,
                                             max_value=secili.stok, step=1.0, key="tdm_zg_miktar")
                zg_not = st.text_area("Notlar", height=60, key="tdm_zg_not")

                if zg_miktar > 0 and zg_personel:
                    st.info(f"Zimmetlenecek: {_format_number(zg_miktar)} {secili.birim} {secili.urun_adi} -> {zg_personel}")

                if st.button("Zimmet Kaydet", key="tdm_zg_btn", type="primary", use_container_width=True):
                    if not zg_personel:
                        st.error("Teslim alan kisi secin.")
                    elif zg_miktar <= 0:
                        st.error("Miktar 0'dan buyuk olmalidir.")
                    else:
                        # Stoktan dusup hareket + zimmet olustur
                        hareket = TuketimHareketi(
                            urun_id=secili.id, urun_adi=secili.urun_adi,
                            kategori=secili.kategori,
                            demirbas_kategori=secili.demirbas_kategori,
                            saat=datetime.now().strftime("%H:%M"),
                            tip="Giriş", miktar=zg_miktar, birim=secili.birim,
                            birim_fiyat=secili.birim_fiyat, neden="Zimmet",
                            teslim_alan=zg_personel, aciklama=zg_not,
                            kaydeden=st.session_state.get("auth_user", {}).get("name", ""),
                        )
                        hareket.hareket_kodu = store.next_hareket_code()
                        hareket.toplam_tutar = zg_miktar * secili.birim_fiyat
                        store.upsert("tuketim_hareketleri", hareket)

                        tz = store.tuketim_zimmet_giris(hareket, zg_personel, zg_unvan, zg_not)
                        if tz:
                            st.success(
                                f"Zimmet oluşturuldu: {tz.zimmet_kodu} | "
                                f"{_format_number(zg_miktar)} {secili.birim} {secili.urun_adi} -> {zg_personel}"
                            )
                            store.log("zimmet_formu_giris", "tuketim_zimmet", tz.id,
                                      f"{secili.urun_adi} -> {zg_personel}")
                            st.rerun()

    # ===== ZIMMET FORMU CIKIS =====
    with sub_tabs[2]:
        styled_section("Zimmet Formu - Çıkış (Devir / İade)", "#ED7D31")
        styled_info_banner(
            "Zimmetli malzemeyi baska kisiye devretmek veya iade etmek için kullanin. "
            "Kismen devir desteklenir (10 kalemden 3'unu devret gibi).",
            "#ED7D31", "📤"
        )

        tum_tz = store.load_objects("tuketim_zimmetleri")
        aktif_tz = [z for z in tum_tz if z.durum == "Aktif" and z.miktar > 0]

        if not aktif_tz:
            styled_info_banner("Aktif tuketim zimmeti bulunmuyor.", banner_type="info", icon="📋")
        else:
            z_options = ["-- Zimmet secin --"] + [
                f"{z.zimmet_kodu} - {z.urun_adi} ({z.personel_adi}: {_format_number(z.miktar)} {z.birim})"
                for z in aktif_tz
            ]
            z_idx = st.selectbox("Kaynak Zimmet", range(len(z_options)),
                                  format_func=lambda i: z_options[i], key="tdm_zc_kaynak")

            if z_idx > 0:
                kaynak_z = aktif_tz[z_idx - 1]
                st.info(
                    f"Kaynak: **{kaynak_z.personel_adi}** | "
                    f"{kaynak_z.urun_adi}: **{_format_number(kaynak_z.miktar)} {kaynak_z.birim}**"
                )

                islem_turu = st.radio("İşlem Turu", ["Devir (Baska Kisiye)", "İade"], horizontal=True, key="tdm_zc_tip")

                zc_miktar = st.number_input(
                    f"Miktar ({kaynak_z.birim})", min_value=0.0,
                    max_value=kaynak_z.miktar, step=1.0, key="tdm_zc_miktar"
                )

                if islem_turu == "Devir (Baska Kisiye)":
                    staff = load_shared_staff()
                    if staff:
                        p_options = ["-- Teslim Alan secin --"] + [
                            f"{s.get('ad', '')} {s.get('soyad', '')} - {s.get('unvan', '')}" + (f" ({s.get('brans', '')})" if s.get('brans') else "")
                            for s in staff
                        ]
                        p_idx = st.selectbox("Teslim Alan (Yeni Zimmetli)", range(len(p_options)),
                                              format_func=lambda i: p_options[i], key="tdm_zc_per")
                        if p_idx > 0:
                            p = staff[p_idx - 1]
                            zc_alan = f"{p.get('ad', '')} {p.get('soyad', '')}".strip()
                            zc_alan_unvan = p.get("unvan", "")
                        else:
                            zc_alan = ""
                            zc_alan_unvan = ""
                    else:
                        zc_alan = st.text_input("Teslim Alan Adi", key="tdm_zc_per_ad")
                        zc_alan_unvan = st.text_input("Unvani", key="tdm_zc_per_unv")
                else:
                    zc_alan = ""
                    zc_alan_unvan = ""

                zc_not = st.text_area("Notlar", height=60, key="tdm_zc_not")

                if zc_miktar > 0:
                    kalan = kaynak_z.miktar - zc_miktar
                    if islem_turu == "Devir (Baska Kisiye)":
                        st.info(
                            f"Devir: {_format_number(zc_miktar)} {kaynak_z.birim} "
                            f"({kaynak_z.personel_adi} -> {zc_alan or '?'}) | "
                            f"Kalan zimmet: {_format_number(kalan)} {kaynak_z.birim}"
                        )
                    else:
                        st.info(
                            f"İade: {_format_number(zc_miktar)} {kaynak_z.birim} "
                            f"({kaynak_z.personel_adi}) | Kalan zimmet: {_format_number(kalan)} {kaynak_z.birim}"
                        )

                if st.button("İşlem Yap", key="tdm_zc_btn", type="primary", use_container_width=True):
                    if zc_miktar <= 0:
                        st.error("Miktar 0'dan buyuk olmalidir.")
                    elif islem_turu == "Devir (Baska Kisiye)" and not zc_alan:
                        st.error("Teslim alan kisi secin.")
                    else:
                        # Zimmet guncelle
                        kaynak_z.miktar -= zc_miktar
                        kaynak_z.updated_at = _now()
                        if kaynak_z.miktar <= 0:
                            kaynak_z.durum = "Devredildi" if islem_turu.startswith("Devir") else "İade Edildi"
                            kaynak_z.miktar = 0
                        islem_str = f"{islem_turu}: -{_format_number(zc_miktar)}"
                        if zc_alan:
                            islem_str += f" -> {zc_alan}"
                        kaynak_z.notlar = f"{kaynak_z.notlar}\n{islem_str}".strip()
                        store.upsert("tuketim_zimmetleri", kaynak_z)

                        # Devir ise yeni kisiye zimmet olustur
                        if islem_turu.startswith("Devir") and zc_alan:
                            mevcut_alan = store._bul_aktif_tuketim_zimmet(kaynak_z.urun_id, zc_alan)
                            if mevcut_alan:
                                mevcut_alan.miktar += zc_miktar
                                mevcut_alan.updated_at = _now()
                                mevcut_alan.notlar = f"{mevcut_alan.notlar}\nDevir: +{_format_number(zc_miktar)} <- {kaynak_z.personel_adi}".strip()
                                store.upsert("tuketim_zimmetleri", mevcut_alan)
                            else:
                                yeni_tz = TuketimZimmet(
                                    zimmet_kodu=store.next_tuketim_zimmet_code(),
                                    urun_id=kaynak_z.urun_id, urun_kodu=kaynak_z.urun_kodu,
                                    urun_adi=kaynak_z.urun_adi, kategori=kaynak_z.kategori,
                                    demirbas_kategori=kaynak_z.demirbas_kategori,
                                    personel_adi=zc_alan, personel_unvan=zc_alan_unvan,
                                    miktar=zc_miktar, birim=kaynak_z.birim,
                                    birim_fiyat=kaynak_z.birim_fiyat,
                                    tip="Çıkış",
                                    notlar=zc_not or f"Devir: {kaynak_z.personel_adi} -> {zc_alan}",
                                )
                                store.upsert("tuketim_zimmetleri", yeni_tz)

                        store.log("zimmet_formu_cikis", "tuketim_zimmet", kaynak_z.id, islem_str)
                        st.success(f"İşlem tamamlandı: {islem_str}")
                        st.rerun()

    # ===== DEMIRBAS ZIMMET =====
    with sub_tabs[3]:
        styled_section("Demirbas Zimmet Atama")
        demirbaslar = store.load_objects("demirbaslar")
        uygun_db = [d for d in demirbaslar if d.durum == "Aktif"]

        if not uygun_db:
            styled_info_banner("Zimmet atanabilecek demirbas yok (Aktif durumda olmali).", "#f59e0b", "⚠️")
        else:
            db_options = ["-- Demirbas secin --"] + [f"{d.demirbas_kodu} - {d.ad} ({d.kategori})" for d in uygun_db]
            db_idx = st.selectbox("Demirbas", range(len(db_options)), format_func=lambda i: db_options[i], key="tdm_za_db")

            staff = load_shared_staff()
            if staff:
                p_options = ["-- Personel secin --"] + [
                    f"{s.get('ad', '')} {s.get('soyad', '')} - {s.get('unvan', '')}"
                    for s in staff
                ]
                p_idx = st.selectbox("Personel", range(len(p_options)), format_func=lambda i: p_options[i], key="tdm_za_per")
            else:
                p_idx = 0
                personel_ad = st.text_input("Personel Adi", key="tdm_za_per_ad")
                personel_unvan = st.text_input("Personel Unvani", key="tdm_za_per_unv")

            notlar = st.text_area("Notlar", height=68, key="tdm_za_not")

            if st.button("Zimmet Ata", key="tdm_za_btn", type="primary", use_container_width=True):
                if db_idx == 0:
                    st.error("Demirbas secin.")
                else:
                    secili_db = uygun_db[db_idx - 1]
                    if staff and p_idx > 0:
                        p = staff[p_idx - 1]
                        p_adi = f"{p.get('ad', '')} {p.get('soyad', '')}".strip()
                        p_unv = p.get("unvan", "")
                    elif not staff:
                        p_adi = personel_ad
                        p_unv = personel_unvan
                    else:
                        st.error("Personel secin.")
                        p_adi = ""
                        p_unv = ""
                    if p_adi:
                        ok, msg = store.zimmet_ata(secili_db.id, p_adi, p_unv, notlar)
                        if ok:
                            st.success(msg)
                            store.log("zimmet_atama", "zimmet", "", msg)
                            st.rerun()
                        else:
                            st.error(msg)

        # Aktif demirbas zimmetleri
        styled_section("Aktif Demirbas Zimmetleri")
        aktif = store.find_by_field("zimmet_kayitlari", "durum", "Aktif")
        if aktif:
            rows = []
            for z in aktif:
                rows.append({
                    "Kod": z.zimmet_kodu, "Demirbas": z.demirbas_adi,
                    "Personel": z.personel_adi, "Tarih": z.zimmet_tarihi,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner("Aktif demirbas zimmeti yok.", banner_type="info", icon="📋")

    # ===== DEMIRBAS IADE =====
    with sub_tabs[4]:
        styled_section("Demirbas Zimmet İade")
        aktif_zimmetler = store.find_by_field("zimmet_kayitlari", "durum", "Aktif")
        if not aktif_zimmetler:
            styled_info_banner("Aktif demirbas zimmeti bulunmuyor.", banner_type="info", icon="📋")
        else:
            z_options = ["-- Zimmet secin --"] + [
                f"{z.zimmet_kodu} - {z.demirbas_adi} ({z.personel_adi})"
                for z in aktif_zimmetler
            ]
            z_idx = st.selectbox("Zimmet", range(len(z_options)),
                                  format_func=lambda i: z_options[i], key="tdm_zi_sec")
            iade_durum = st.selectbox("İade Durumu", ["İade Edildi", "Kayip", "Hurda"], key="tdm_zi_dur")
            iade_not = st.text_area("İade Notu", height=68, key="tdm_zi_not")

            if st.button("İade Et", key="tdm_zi_btn", type="primary", use_container_width=True):
                if z_idx == 0:
                    st.error("Zimmet secin.")
                else:
                    secili_z = aktif_zimmetler[z_idx - 1]
                    ok, msg = store.zimmet_iade(secili_z.id, iade_durum, iade_not)
                    if ok:
                        st.success(msg)
                        store.log("zimmet_iade", "zimmet", secili_z.id, msg)
                        st.rerun()
                    else:
                        st.error(msg)

    # ===== ZIMMET PDF =====
    with sub_tabs[5]:
        styled_section("Zimmet Formu PDF", "#4472C4")
        styled_info_banner(
            "Kisi bazli zimmet formu olusturarak imza alabilirsiniz. "
            "Tuketim malzemeleri ve demirbas zimmetleri tek PDF'te birlestirilir.", banner_type="info", icon="📄")

        # Personel secimi
        tum_tz = store.load_objects("tuketim_zimmetleri")
        aktif_tz = [z for z in tum_tz if z.durum == "Aktif" and z.miktar > 0]
        aktif_db = store.find_by_field("zimmet_kayitlari", "durum", "Aktif")

        tum_personeller = sorted(set(
            [z.personel_adi for z in aktif_tz] +
            [z.personel_adi for z in aktif_db]
        ))

        if not tum_personeller:
            styled_info_banner("Aktif zimmet kaydi bulunmuyor.", banner_type="info", icon="📋")
        else:
            secili_personel = st.selectbox("Personel Secin", tum_personeller, key="tdm_zpdf_per")

            if st.button("PDF Oluştur", key="tdm_zpdf_btn", type="primary", use_container_width=True):
                try:
                    from utils.report_utils import ReportPDFGenerator, get_institution_info

                    pdf = ReportPDFGenerator("Zimmet Formu", f"Personel: {secili_personel}")
                    info = get_institution_info()
                    pdf.add_header(kurum_adi=info.get("name", ""))

                    # Tuketim zimmetleri
                    kisi_tz = [z for z in aktif_tz if z.personel_adi == secili_personel]
                    if kisi_tz:
                        pdf.add_section("Tuketim Malzemeleri Zimmeti")
                        tz_rows = []
                        for z in kisi_tz:
                            tz_rows.append({
                                "Zimmet Kodu": z.zimmet_kodu,
                                "Urun": z.urun_adi,
                                "Urun Kodu": z.urun_kodu,
                                "Kategori": z.kategori,
                                "Miktar": f"{z.miktar:.0f} {z.birim}",
                                "Birim Fiyat": f"{z.birim_fiyat:.2f} TL",
                                "Toplam": f"{z.miktar * z.birim_fiyat:.2f} TL",
                                "Tarih": z.zimmet_tarihi,
                            })
                        pdf.add_table(pd.DataFrame(tz_rows))
                        toplam_tz = sum(z.miktar * z.birim_fiyat for z in kisi_tz)
                        pdf.add_text(f"Tuketim Malzemesi Toplam Deger: {toplam_tz:.2f} TL")

                    # Demirbas zimmetleri
                    kisi_db = [z for z in aktif_db if z.personel_adi == secili_personel]
                    if kisi_db:
                        pdf.add_section("Demirbas Zimmeti")
                        db_rows = []
                        for z in kisi_db:
                            db_rows.append({
                                "Zimmet Kodu": z.zimmet_kodu,
                                "Demirbas": z.demirbas_adi,
                                "Demirbas Kodu": z.demirbas_kodu,
                                "Tarih": z.zimmet_tarihi,
                            })
                        pdf.add_table(pd.DataFrame(db_rows))

                    # Imza alani
                    pdf.add_spacer(1.5)
                    pdf.add_text(
                        "Yukaridaki malzeme ve demirbaslarin tarafima zimmetlendigini, "
                        "ozenle kullanacagimi ve istendiginde iade edecegimi kabul ve taahhut ederim."
                    )
                    pdf.add_spacer(1.0)

                    imza_df = pd.DataFrame([{
                        "Teslim Eden": "........................",
                        "Teslim Alan": "........................",
                    }, {
                        "Teslim Eden": "(Ad Soyad / Imza)",
                        "Teslim Alan": f"{secili_personel}",
                    }, {
                        "Teslim Eden": "Tarih: ....../....../........",
                        "Teslim Alan": "Tarih: ....../....../........",
                    }])
                    pdf.add_table(imza_df, header_color="#44546A")

                    pdf_bytes = pdf.generate()
                    st.download_button(
                        "PDF Indir", pdf_bytes,
                        file_name=f"zimmet_formu_{secili_personel.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                    st.success("Zimmet formu PDF oluşturuldu!")
                except Exception as e:
                    st.error(f"PDF olusturma hatasi: {e}")


# ============================================================
# SEKME 7: AI TAVSIYE
# ============================================================

def _render_ai_tavsiye(store: TDMDataStore):
    styled_header("AI Tavsiye", "Tuketim analizi, tasarruf onerileri, anormallik tespiti")

    sub_tabs = st.tabs(["📊 Tüketim Analizi", "🔄 Dönem Karşılaştırma"])

    with sub_tabs[0]:
        styled_section("AI Tuketim Analizi")
        styled_info_banner(
            "Son 30 gunluk tuketim verilerinizi analiz eder, anormallikleri tespit eder ve tasarruf onerileri sunar.", banner_type="info", icon="🤖")

        if st.button("Analiz Baslat", key="tdm_ai_analiz", type="primary", use_container_width=True):
            prompt = AITavsiyeMotoru.analiz_prompt(store)

            try:
                from openai import OpenAI
                api_key = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))
                if not api_key:
                    st.error("OpenAI API anahtari bulunamadı. secrets.toml veya env degiskeni ayarlayin.")
                else:
                    with st.spinner("AI analiz yapiyor..."):
                        client = OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=1500,
                            temperature=0.7,
                        )
                        sonuc = response.choices[0].message.content
                    st.markdown("---")
                    st.markdown(sonuc)
            except ImportError:
                st.error("openai paketi yuklu degil. `pip install openai` calistirin.")
            except Exception as e:
                st.error(f"AI analiz hatasi: {e}")

    with sub_tabs[1]:
        styled_section("AI Donem Karsilastirma")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Donem 1**")
            ai_d1_bas = st.date_input("Bas", value=date.today() - timedelta(days=60), key="tdm_ai_d1b")
            ai_d1_bit = st.date_input("Bit", value=date.today() - timedelta(days=31), key="tdm_ai_d1e")
        with c2:
            st.markdown("**Donem 2**")
            ai_d2_bas = st.date_input("Bas", value=date.today() - timedelta(days=30), key="tdm_ai_d2b")
            ai_d2_bit = st.date_input("Bit", value=date.today(), key="tdm_ai_d2e")

        if st.button("AI Karsilastirma", key="tdm_ai_kars", type="primary", use_container_width=True):
            prompt = AITavsiyeMotoru.karsilastirma_prompt(
                store, ai_d1_bas.isoformat(), ai_d1_bit.isoformat(),
                ai_d2_bas.isoformat(), ai_d2_bit.isoformat(),
            )
            try:
                from openai import OpenAI
                api_key = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))
                if not api_key:
                    st.error("OpenAI API anahtari bulunamadı.")
                else:
                    with st.spinner("AI karsilastirma yapiyor..."):
                        client = OpenAI(api_key=api_key)
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=1200,
                            temperature=0.7,
                        )
                        sonuc = response.choices[0].message.content
                    st.markdown("---")
                    st.markdown(sonuc)
            except ImportError:
                st.error("openai paketi yuklu degil.")
            except Exception as e:
                st.error(f"AI hatasi: {e}")


# ============================================================
# SEKME 8: AYARLAR
# ============================================================

def _render_ayarlar(store: TDMDataStore):
    styled_header("Ayarlar", "Kategori, urun tanimlari ve CSV import")

    sub_tabs = st.tabs(["📦 Tüketim Kategorileri", "🏷️ Ürün Tanımları", "🗄️ Demirbaş Kategorileri", "📥 CSV Import"])

    # --- Tuketim Kategorileri ---
    with sub_tabs[0]:
        styled_section("Tuketim Kategorileri")
        kategoriler = store.load_objects("tuketim_kategorileri")

        # Varsayilan kategorileri yukle
        if not kategoriler:
            for kat in TUKETIM_KATEGORILERI:
                yeni = TuketimKategori(kod=kat[:3].upper(), ad=kat)
                store.upsert("tuketim_kategorileri", yeni)
            kategoriler = store.load_objects("tuketim_kategorileri")

        if kategoriler:
            rows = [{"Kod": k.kod, "Ad": k.ad, "Açıklama": k.aciklama} for k in kategoriler]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        with st.expander("Yeni Kategori Ekle"):
            c1, c2 = st.columns(2)
            with c1:
                yk_kod = st.text_input("Kod", key="tdm_yk_kod")
            with c2:
                yk_ad = st.text_input("Ad", key="tdm_yk_ad")
            yk_aciklama = st.text_input("Açıklama", key="tdm_yk_acik")

            if st.button("Ekle", key="tdm_yk_btn"):
                if yk_kod and yk_ad:
                    store.upsert("tuketim_kategorileri", TuketimKategori(kod=yk_kod, ad=yk_ad, aciklama=yk_aciklama))
                    st.success(f"Kategori eklendi: {yk_ad}")
                    st.rerun()
                else:
                    st.error("Kod ve ad zorunlu.")

    # --- Urun Tanimlari ---
    with sub_tabs[1]:
        styled_section("Urun Tanımlari")
        urunler = store.load_objects("tuketim_urunleri")
        if urunler:
            rows = [{
                "Kod": u.urun_kodu, "Ad": u.urun_adi, "Kategori": u.kategori,
                "Birim": u.birim, "Stok": u.stok, "Min Stok": u.min_stok,
                "Birim Fiyat": _format_currency(u.birim_fiyat),
            } for u in urunler]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        with st.expander("Yeni Urun Ekle"):
            yeni_kod = store.next_urun_code()
            st.info(f"Urun Kodu: **{yeni_kod}**")

            c1, c2 = st.columns(2)
            with c1:
                yu_ad = st.text_input("Urun Adi", key="tdm_yu_ad")
                kat_listesi = [k.ad for k in store.load_objects("tuketim_kategorileri")]
                if not kat_listesi:
                    kat_listesi = TUKETIM_KATEGORILERI
                yu_kat = st.selectbox("Kategori", kat_listesi, key="tdm_yu_kat")
                yu_birim = st.selectbox("Birim", BIRIMLER, key="tdm_yu_birim")
            with c2:
                yu_stok = st.number_input("Başlangıç Stok", min_value=0.0, step=1.0, key="tdm_yu_stok")
                yu_min = st.number_input("Min Stok", min_value=0.0, step=1.0, key="tdm_yu_min")
                yu_fiyat = st.number_input("Birim Fiyat (TL)", min_value=0.0, step=0.01, key="tdm_yu_fiyat")

            if st.button("Urun Ekle", key="tdm_yu_btn", type="primary"):
                if not yu_ad:
                    st.error("Urun adi zorunlu.")
                else:
                    yeni = TuketimUrunu(
                        urun_kodu=yeni_kod,
                        urun_adi=yu_ad,
                        kategori=yu_kat,
                        birim=yu_birim,
                        stok=yu_stok,
                        min_stok=yu_min,
                        birim_fiyat=yu_fiyat,
                    )
                    store.upsert("tuketim_urunleri", yeni)
                    store.log("urun_ekleme", "urun", yeni.id, f"{yeni_kod} - {yu_ad}")
                    st.success(f"Urun eklendi: {yeni_kod} - {yu_ad}")
                    st.rerun()

    # --- Demirbas Kategorileri ---
    with sub_tabs[2]:
        styled_section("Demirbas Kategorileri")
        dk_list = store.load_objects("demirbas_kategorileri")

        if not dk_list:
            for kat in DEMIRBAS_KATEGORILERI:
                store.upsert("demirbas_kategorileri", DemirbasKategori(kod=kat[:3].upper(), ad=kat))
            dk_list = store.load_objects("demirbas_kategorileri")

        if dk_list:
            rows = [{"Kod": k.kod, "Ad": k.ad, "Açıklama": k.aciklama} for k in dk_list]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        col_kat, col_mlz = st.columns(2)

        # --- Yeni Demirbas Kategorisi Ekle ---
        with col_kat:
            styled_section("Yeni Demirbas Kategorisi Ekle", "#ea580c")
            dk_kod = st.text_input("Kategori Kodu", key="tdm_dk_kod", placeholder="ORN: BIL")
            dk_ad = st.text_input("Kategori Adi", key="tdm_dk_ad", placeholder="Ornek: Bilisim Ekipmani")
            dk_aciklama = st.text_input("Açıklama (opsiyonel)", key="tdm_dk_acik", placeholder="Kategori aciklamasi")

            if st.button("Demirbas Kategorisi Ekle", key="tdm_dk_btn", type="primary", use_container_width=True):
                if dk_kod and dk_ad:
                    store.upsert("demirbas_kategorileri",
                                 DemirbasKategori(kod=dk_kod.upper(), ad=dk_ad, aciklama=dk_aciklama))
                    st.success(f"Kategori eklendi: {dk_ad}")
                    store.log("kategori_ekleme", "demirbas_kategori", "", f"Demirbas kategorisi: {dk_ad}")
                    st.rerun()
                else:
                    st.error("Kod ve ad alanlari zorunludur.")

        # --- Tuketim Malzemeleri Ekle ---
        with col_mlz:
            styled_section("Tuketim Malzemeleri Ekle", "#4472C4")
            tm_ad = st.text_input("Malzeme Adi", key="tdm_tm_ad", placeholder="Ornek: A4 Kagit")
            kat_listesi = [k.ad for k in store.load_objects("tuketim_kategorileri")]
            if not kat_listesi:
                kat_listesi = TUKETIM_KATEGORILERI
            tm_kat = st.selectbox("Kategori", kat_listesi, key="tdm_tm_kat")
            tm_c1, tm_c2 = st.columns(2)
            with tm_c1:
                tm_birim = st.selectbox("Birim", BIRIMLER, key="tdm_tm_birim")
                tm_min = st.number_input("Min Stok", min_value=0.0, step=1.0, key="tdm_tm_min")
            with tm_c2:
                tm_fiyat = st.number_input("Birim Fiyat (TL)", min_value=0.0, step=0.01, key="tdm_tm_fiyat")
                tm_stok = st.number_input("Başlangıç Stok", min_value=0.0, step=1.0, key="tdm_tm_stok")

            if st.button("Tuketim Malzemesi Ekle", key="tdm_tm_btn", type="primary", use_container_width=True):
                if tm_ad:
                    yeni_kod = store.next_urun_code()
                    yeni = TuketimUrunu(
                        urun_kodu=yeni_kod, urun_adi=tm_ad, kategori=tm_kat,
                        birim=tm_birim, stok=tm_stok, min_stok=tm_min, birim_fiyat=tm_fiyat,
                    )
                    store.upsert("tuketim_urunleri", yeni)
                    store.log("malzeme_ekleme", "tuketim_urun", yeni.id, f"{yeni_kod} - {tm_ad}")
                    st.success(f"Tuketim malzemesi eklendi: {yeni_kod} - {tm_ad}")
                    st.rerun()
                else:
                    st.error("Malzeme adi zorunludur.")

    # --- CSV Import ---
    with sub_tabs[3]:
        styled_section("CSV Import")
        import_tipi = st.selectbox("Import Tipi", [
            "Tuketim Urunleri",
            "Demirbaslar",
        ], key="tdm_imp_tip")

        uploaded = st.file_uploader("CSV Dosyasi Yukle", type=["csv"], key="tdm_imp_file")

        if uploaded:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(uploaded, allowed_types=["csv"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                uploaded = None
        if uploaded and st.button("Import Et", key="tdm_imp_btn", type="primary"):
            try:
                content = uploaded.getvalue().decode("utf-8")
                reader = csv.DictReader(io.StringIO(content), delimiter=";")
                rows = list(reader)

                if import_tipi == "Tuketim Urunleri":
                    count = 0
                    for row in rows:
                        urun = TuketimUrunu(
                            urun_kodu=row.get("urun_kodu", store.next_urun_code()),
                            urun_adi=row.get("urun_adi", ""),
                            kategori=row.get("kategori", ""),
                            birim=row.get("birim", "adet"),
                            stok=float(row.get("stok", 0)),
                            min_stok=float(row.get("min_stok", 0)),
                            birim_fiyat=float(row.get("birim_fiyat", 0)),
                        )
                        if urun.urun_adi:
                            store.upsert("tuketim_urunleri", urun)
                            count += 1
                    st.success(f"{count} urun import edildi.")
                    st.rerun()

                elif import_tipi == "Demirbaslar":
                    count = 0
                    for row in rows:
                        db = Demirbas(
                            demirbas_kodu=row.get("demirbas_kodu", store.next_demirbas_code()),
                            ad=row.get("ad", ""),
                            kategori=row.get("kategori", ""),
                            marka=row.get("marka", ""),
                            model=row.get("model", ""),
                            seri_no=row.get("seri_no", ""),
                            lokasyon=row.get("lokasyon", ""),
                            satin_alma_tarihi=row.get("satin_alma_tarihi", ""),
                            fiyat=float(row.get("fiyat", 0)),
                            durum=row.get("durum", "Aktif"),
                        )
                        if db.ad:
                            store.upsert("demirbaslar", db)
                            count += 1
                    st.success(f"{count} demirbas import edildi.")
                    st.rerun()

            except Exception as e:
                st.error(f"Import hatasi: {e}")


# ============================================================
# SEKME: SATIN ALMA
# ============================================================

def _render_satin_alma(store: TDMDataStore):
    sub = st.tabs(["➕ Yeni Talep", "📋 Talepler", "💰 Fiyat Teklifleri",
                    "🏢 Tedarikçi Rehberi", "📦 Sipariş Takip", "📈 TD Raporlar"])

    # ----- ALT SEKME 1: YENI TALEP -----
    with sub[0]:
        styled_section("Yeni Satın Alma Talebi", "#2563eb")

        auth_user = AuthManager.get_current_user()
        talep_eden = auth_user.get("name", "")

        k1, k2 = st.columns(2)
        with k1:
            st.text_input("Talep Eden", value=talep_eden, disabled=True, key="sa_talep_eden")
        with k2:
            oncelik = st.selectbox("Öncelik", SATIN_ALMA_ONCELIKLERI, index=1, key="sa_oncelik")

        # Kalem yonetimi (session state)
        if "sa_kalemler" not in st.session_state:
            st.session_state["sa_kalemler"] = []

        styled_section("Kalem Ekle", "#10b981")
        urunler = store.load_objects("tuketim_urunleri")
        urun_adi_list = ["-- Serbest gir --"] + sorted(set(u.urun_adi for u in urunler if u.aktif))

        kk1, kk2, kk3, kk4 = st.columns([3, 1, 1, 1])
        with kk1:
            secilen_urun = st.selectbox("Urun", urun_adi_list, key="sa_urun_sec")
            if secilen_urun == "-- Serbest gir --":
                serbest_adi = st.text_input("Urun Adi", key="sa_serbest_adi")
            else:
                serbest_adi = ""
        with kk2:
            kalem_miktar = st.number_input("Miktar", min_value=0.0, step=1.0, key="sa_kalem_miktar")
        with kk3:
            kalem_birim = st.selectbox("Birim", BIRIMLER, key="sa_kalem_birim")
        with kk4:
            kalem_fiyat = st.number_input("Tahmini Birim Fiyat (TL)", min_value=0.0,
                                           step=10.0, key="sa_kalem_fiyat")

        kd1, kd2 = st.columns(2)
        with kd1:
            kalem_kat = st.selectbox("Tuketim Kategorisi", [""] + TUKETIM_KATEGORILERI,
                                      key="sa_kalem_kat")
        with kd2:
            kalem_db_kat = st.selectbox("Demirbas Kategorisi (opsiyonel)",
                                         [""] + DEMIRBAS_KATEGORILERI, key="sa_kalem_db_kat")

        if st.button("Kalem Ekle", key="sa_kalem_ekle_btn", type="secondary"):
            u_adi = serbest_adi if secilen_urun == "-- Serbest gir --" else secilen_urun
            if u_adi and kalem_miktar > 0:
                # Mevcut urunden fiyat bilgisi al
                if not kalem_fiyat and secilen_urun != "-- Serbest gir --":
                    for u in urunler:
                        if u.urun_adi == secilen_urun:
                            kalem_fiyat = u.birim_fiyat
                            break
                st.session_state["sa_kalemler"].append({
                    "urun_adi": u_adi,
                    "miktar": kalem_miktar,
                    "birim": kalem_birim,
                    "tahmini_fiyat": kalem_fiyat,
                    "kategori": kalem_kat,
                    "demirbas_kategori": kalem_db_kat,
                })
                st.rerun()
            else:
                styled_info_banner("Urun adi ve miktar gereklidir.", banner_type="error", icon="")

        # Kalem listesi goster
        kalemler = st.session_state.get("sa_kalemler", [])
        if kalemler:
            styled_section(f"Kalemler ({len(kalemler)} adet)", "#8b5cf6")
            toplam = 0.0
            for i, km in enumerate(kalemler):
                tutar = km["miktar"] * km["tahmini_fiyat"]
                toplam += tutar
                c1, c2 = st.columns([8, 1])
                with c1:
                    db_badge = (f' <span style="background:#ea580c20;color:#ea580c;'
                                f'padding:1px 6px;border-radius:6px;font-size:10px;">'
                                f'DB: {km["demirbas_kategori"]}</span>'
                                if km.get("demirbas_kategori") else "")
                    st.markdown(
                        f'<div style="background:#111827;border:1px solid #e2e8f0;'
                        f'border-radius:8px;padding:8px 12px;margin:3px 0;'
                        f'display:flex;justify-content:space-between;align-items:center;">'
                        f'<span><b>{km["urun_adi"]}</b> - {km["miktar"]:.0f} {km["birim"]}'
                        f'{db_badge}</span>'
                        f'<span style="color:#2563eb;font-weight:700;">'
                        f'{tutar:,.2f} TL</span></div>',
                        unsafe_allow_html=True,
                    )
                with c2:
                    if st.button("X", key=f"sa_kalem_sil_{i}"):
                        st.session_state["sa_kalemler"].pop(i)
                        st.rerun()

            st.markdown(
                f'<div style="text-align:right;font-size:16px;font-weight:700;'
                f'color:#94A3B8;margin:8px 0;">Toplam Tahmini: '
                f'<span style="color:#2563eb;">{toplam:,.2f} TL</span></div>',
                unsafe_allow_html=True,
            )

        talep_notlar = st.text_area("Notlar", key="sa_talep_notlar", height=80)

        if st.button("Talebi Kaydet", type="primary", key="sa_talep_kaydet"):
            if not kalemler:
                styled_info_banner("En az bir kalem ekleyin.", banner_type="error", icon="")
            else:
                toplam_t = sum(k["miktar"] * k["tahmini_fiyat"] for k in kalemler)
                talep = SatinAlmaTalebi(
                    talep_kodu=store.next_talep_code(),
                    talep_eden=talep_eden,
                    oncelik=oncelik,
                    kalemler=list(kalemler),
                    toplam_tahmini_tutar=toplam_t,
                    notlar=talep_notlar,
                )
                store.upsert("satin_alma_talepleri", talep)
                store.log("satin_alma_talep", "talep", talep.id,
                          f"Yeni talep: {talep.talep_kodu} ({len(kalemler)} kalem)",
                          talep_eden)
                st.session_state["sa_kalemler"] = []
                styled_info_banner(
                    f"Talep oluşturuldu: {talep.talep_kodu} | "
                    f"Toplam: {toplam_t:,.2f} TL", banner_type="success", icon="")
                st.rerun()

    # ----- ALT SEKME 2: TALEPLER -----
    with sub[1]:
        styled_section("Satın Alma Talepleri", "#2563eb")

        talepler = store.load_objects("satin_alma_talepleri")
        talepler.sort(key=lambda t: t.created_at, reverse=True)

        # Filtreler
        f1, f2 = st.columns(2)
        with f1:
            filtre_durum = st.selectbox("Durum Filtre", ["Tümü"] + SATIN_ALMA_DURUMLARI,
                                         key="sa_filtre_durum")
        with f2:
            filtre_oncelik = st.selectbox("Öncelik Filtre",
                                           ["Tümü"] + SATIN_ALMA_ONCELIKLERI,
                                           key="sa_filtre_oncelik")

        if filtre_durum != "Tümü":
            talepler = [t for t in talepler if t.durum == filtre_durum]
        if filtre_oncelik != "Tümü":
            talepler = [t for t in talepler if t.oncelik == filtre_oncelik]

        if not talepler:
            styled_info_banner("Talep bulunamadı.", banner_type="info", icon="")
        else:
            styled_stat_row([
                ("Toplam Talep", len(talepler), "#2563eb", ""),
                ("Bekleyen", len([t for t in talepler if t.durum in ("Taslak", "Teklif Bekleniyor", "Onay Bekliyor")]), "#f59e0b", ""),
                ("Onaylanan", len([t for t in talepler if t.durum in ("Onaylandi", "Siparis Verildi", "Teslim Alindi")]), "#10b981", ""),
                ("Red/Iptal", len([t for t in talepler if t.durum in ("Red", "Iptal")]), "#ef4444", ""),
            ])

        durum_renk = {
            "Taslak": "#94a3b8", "Teklif Bekleniyor": "#f59e0b",
            "Teklif Alindi": "#8b5cf6", "Onay Bekliyor": "#ea580c",
            "Onaylandi": "#10b981", "Red": "#ef4444",
            "Siparis Verildi": "#2563eb", "Teslim Alindi": "#059669",
            "Iptal": "#64748b",
        }
        oncelik_renk = {
            "Dusuk": "#94a3b8", "Normal": "#2563eb",
            "Yuksek": "#f59e0b", "Acil": "#ef4444",
        }

        for t in talepler:
            d_renk = durum_renk.get(t.durum, "#64748b")
            o_renk = oncelik_renk.get(t.oncelik, "#2563eb")
            kalem_sayisi = len(t.kalemler)

            st.markdown(
                f'<div style="background:#111827;border:1px solid #e2e8f0;'
                f'border-radius:10px;padding:12px 16px;margin:6px 0;">'
                f'<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">'
                f'<span style="font-weight:700;color:#94A3B8;font-size:14px;">'
                f'{t.talep_kodu}</span>'
                f'<span style="color:#64748b;font-size:12px;">{t.talep_tarihi}</span>'
                f'<span style="color:#64748b;font-size:12px;">{t.talep_eden}</span>'
                f'<span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;'
                f'border-radius:8px;font-size:11px;font-weight:600;">{t.durum}</span>'
                f'<span style="background:{o_renk}20;color:{o_renk};padding:2px 8px;'
                f'border-radius:8px;font-size:11px;font-weight:600;">{t.oncelik}</span>'
                f'<span style="color:#64748b;font-size:12px;">{kalem_sayisi} kalem</span>'
                f'<span style="color:#2563eb;font-weight:700;margin-left:auto;">'
                f'{t.toplam_tahmini_tutar:,.2f} TL</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

            with st.expander(f"Detay: {t.talep_kodu}", expanded=False):
                # Kalem tablosu
                if t.kalemler:
                    for km in t.kalemler:
                        tutar = km.get("miktar", 0) * km.get("tahmini_fiyat", 0)
                        st.markdown(
                            f'- **{km.get("urun_adi", "")}** | '
                            f'{km.get("miktar", 0):.0f} {km.get("birim", "")} | '
                            f'{km.get("tahmini_fiyat", 0):,.2f} TL/br | '
                            f'Toplam: {tutar:,.2f} TL'
                            f'{" | DB: " + km.get("demirbas_kategori", "") if km.get("demirbas_kategori") else ""}'
                        )
                if t.notlar:
                    st.caption(f"Not: {t.notlar}")

                # Durum aksiyonlari
                bc1, bc2, bc3, bc4 = st.columns(4)
                if t.durum == "Taslak":
                    with bc1:
                        if st.button("Teklif Iste", key=f"sa_teklif_iste_{t.id}"):
                            t.durum = "Teklif Bekleniyor"
                            t.updated_at = _now()
                            store.upsert("satin_alma_talepleri", t)
                            st.rerun()
                    with bc4:
                        if st.button("Iptal Et", key=f"sa_iptal_{t.id}"):
                            t.durum = "Iptal"
                            t.updated_at = _now()
                            store.upsert("satin_alma_talepleri", t)
                            st.rerun()
                elif t.durum == "Teklif Alindi":
                    with bc1:
                        if st.button("Onaya Gonder", key=f"sa_onaya_{t.id}"):
                            t.durum = "Onay Bekliyor"
                            t.updated_at = _now()
                            store.upsert("satin_alma_talepleri", t)
                            st.rerun()
                elif t.durum == "Onay Bekliyor":
                    with bc1:
                        if st.button("Onayla", key=f"sa_onayla_{t.id}", type="primary"):
                            auth_u = AuthManager.get_current_user()
                            t.durum = "Onaylandi"
                            t.onaylayan = auth_u.get("name", "")
                            t.onay_tarihi = _today()
                            t.updated_at = _now()
                            store.upsert("satin_alma_talepleri", t)
                            st.rerun()
                    with bc2:
                        if st.button("Reddet", key=f"sa_reddet_{t.id}"):
                            t.durum = "Red"
                            t.updated_at = _now()
                            store.upsert("satin_alma_talepleri", t)
                            st.rerun()
                elif t.durum == "Onaylandi":
                    with bc1:
                        if st.button("Siparis Ver", key=f"sa_siparis_{t.id}", type="primary"):
                            # Secilen teklif bilgilerinden siparis olustur
                            teklif = None
                            if t.secilen_teklif_id:
                                teklif = store.get_by_id("fiyat_teklifleri", t.secilen_teklif_id)
                            ted_adi = teklif.tedarikci_adi if teklif else ""
                            beklenen = ""
                            if teklif and teklif.teslim_suresi_gun > 0:
                                from datetime import timedelta as _td
                                beklenen = (date.today() + _td(days=teklif.teslim_suresi_gun)).isoformat()
                            sip = SiparisTakip(
                                siparis_kodu=store.next_siparis_code(),
                                talep_id=t.id,
                                teklif_id=t.secilen_teklif_id,
                                tedarikci_adi=ted_adi,
                                beklenen_teslim=beklenen,
                            )
                            store.upsert("siparis_takipleri", sip)
                            t.durum = "Siparis Verildi"
                            t.updated_at = _now()
                            store.upsert("satin_alma_talepleri", t)
                            store.log("siparis_olustur", "siparis", sip.id,
                                      f"Siparis: {sip.siparis_kodu} / {ted_adi}",
                                      AuthManager.get_current_user().get("name", ""))
                            st.rerun()
                elif t.durum == "Siparis Verildi":
                    with bc1:
                        teslim_alan_kisi = st.text_input("Teslim Alan",
                                                          key=f"sa_teslim_alan_{t.id}")
                    with bc2:
                        if st.button("Teslim Al", key=f"sa_teslim_{t.id}", type="primary"):
                            # Siparisi bul
                            siparisler = store.load_objects("siparis_takipleri")
                            sip_found = None
                            for sp in siparisler:
                                if sp.talep_id == t.id and sp.durum == "Siparis Verildi":
                                    sip_found = sp
                                    break
                            if sip_found:
                                ok, msg = store.teslim_al_ve_stokla(
                                    sip_found.id,
                                    teslim_alan_kisi or AuthManager.get_current_user().get("name", ""),
                                )
                                if ok:
                                    styled_info_banner(msg, banner_type="success", icon="")
                                else:
                                    styled_info_banner(msg, banner_type="error", icon="")
                                st.rerun()
                            else:
                                styled_info_banner("Siparis bulunamadı.", banner_type="error", icon="")

    # ----- ALT SEKME 3: FIYAT TEKLIFLERI -----
    with sub[2]:
        styled_section("Fiyat Teklifi Yönetimi", "#8b5cf6")

        # Talep secimi
        talepler_all = store.load_objects("satin_alma_talepleri")
        teklif_uygun = [t for t in talepler_all
                        if t.durum in ("Teklif Bekleniyor", "Teklif Alindi", "Onay Bekliyor")]
        talep_options = {f"{t.talep_kodu} - {t.talep_eden} ({t.durum})": t
                         for t in teklif_uygun}

        if not talep_options:
            styled_info_banner("Teklif alinabilecek talep yok. "
                                "Önce 'Yeni Talep' olusturup 'Teklif Iste' yapin.", banner_type="info", icon="")
        else:
            secilen_talep_label = st.selectbox(
                "Talep Sec", list(talep_options.keys()), key="sa_teklif_talep_sec")
            secilen_talep = talep_options.get(secilen_talep_label)

            if secilen_talep:
                # Mevcut teklifler yukle
                tum_teklifler = [ft for ft in store.load_objects("fiyat_teklifleri")
                                 if ft.talep_id == secilen_talep.id]

                # Tedarikci listesi
                tedarikciler = store.load_objects("tedarikciler")
                aktif_ted = [t for t in tedarikciler if t.aktif]
                ted_options_map = {f"{t.firma_adi} ({t.yetkili_kisi})": t for t in aktif_ted}

                # Talep kalemleri (teklif formu icin)
                talep_kalemleri = secilen_talep.kalemler or []

                # ---- 1. / 2. / 3. TEKLIF EKRANLARI ----
                teklif_labels = ["1️⃣ 1. Teklif", "2️⃣ 2. Teklif", "3️⃣ 3. Teklif", "⚖️ Karşılaştırma"]
                ft_tabs = st.tabs(teklif_labels)

                for teklif_idx in range(3):
                    with ft_tabs[teklif_idx]:
                        sira = teklif_idx + 1
                        mevcut_ft = tum_teklifler[teklif_idx] if teklif_idx < len(tum_teklifler) else None

                        if mevcut_ft:
                            # Mevcut teklif goster
                            secildi_badge = (' <span style="background:#10b98120;color:#10b981;'
                                             'padding:2px 8px;border-radius:8px;font-size:11px;'
                                             'font-weight:700;">SECILDI</span>'
                                             if mevcut_ft.secildi else "")
                            styled_section(
                                f"{sira}. Teklif: {mevcut_ft.tedarikci_adi}", "#0d9488")
                            st.markdown(
                                f'<div style="background:#f0fdf4;border:2px solid #10b981;'
                                f'border-radius:12px;padding:16px;margin:8px 0;">'
                                f'<div style="display:flex;justify-content:space-between;'
                                f'align-items:center;margin-bottom:12px;">'
                                f'<div><b style="font-size:16px;">{mevcut_ft.teklif_kodu}</b>'
                                f' - {mevcut_ft.tedarikci_adi}{secildi_badge}</div>'
                                f'<div style="text-align:right;">'
                                f'<div style="font-size:11px;color:#64748b;">'
                                f'Teklif: {mevcut_ft.teklif_tarihi} | '
                                f'Gecerlilik: {mevcut_ft.gecerlilik_tarihi or "-"}</div>'
                                f'<div style="font-size:11px;color:#64748b;">'
                                f'Teslim: {mevcut_ft.teslim_suresi_gun} gun | '
                                f'{mevcut_ft.odeme_yontemi}</div></div></div>',
                                unsafe_allow_html=True,
                            )

                            # Kalem detaylari
                            kalem_rows = ""
                            for km in mevcut_ft.kalemler:
                                kalem_rows += (
                                    f'<tr><td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;">'
                                    f'{km.get("urun_adi", "")}</td>'
                                    f'<td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;'
                                    f'text-align:center;">{km.get("miktar", 0):.0f} {km.get("birim", "")}</td>'
                                    f'<td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;'
                                    f'text-align:right;">{km.get("birim_fiyat", 0):,.2f} TL</td>'
                                    f'<td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;'
                                    f'text-align:right;font-weight:700;">'
                                    f'{km.get("toplam", 0):,.2f} TL</td></tr>'
                                )

                            st.markdown(
                                f'<table style="width:100%;border-collapse:collapse;font-size:13px;">'
                                f'<thead><tr style="background:#1A2035;">'
                                f'<th style="padding:8px 10px;text-align:left;">Urun</th>'
                                f'<th style="padding:8px 10px;text-align:center;">Miktar</th>'
                                f'<th style="padding:8px 10px;text-align:right;">Birim Fiyat</th>'
                                f'<th style="padding:8px 10px;text-align:right;">Toplam</th>'
                                f'</tr></thead><tbody>{kalem_rows}</tbody></table>'
                                f'<div style="display:flex;justify-content:flex-end;gap:20px;'
                                f'margin-top:10px;padding:8px 10px;">'
                                f'<span>Ara Toplam: <b>{mevcut_ft.toplam_tutar:,.2f} TL</b></span>'
                                f'<span>KDV (%{mevcut_ft.kdv_orani:.0f}): '
                                f'<b>{mevcut_ft.kdv_dahil_tutar - mevcut_ft.toplam_tutar:,.2f} TL</b></span>'
                                f'<span style="font-size:16px;">Genel Toplam: '
                                f'<b style="color:#2563eb;">{mevcut_ft.kdv_dahil_tutar:,.2f} TL</b></span>'
                                f'</div></div>',
                                unsafe_allow_html=True,
                            )
                            if mevcut_ft.notlar:
                                st.caption(f"Not: {mevcut_ft.notlar}")

                            # Teklif sec butonu
                            if not mevcut_ft.secildi and secilen_talep.durum == "Teklif Bekleniyor":
                                if st.button(f"Bu Teklifi Sec ({sira}. Teklif)",
                                             key=f"sa_teklif_sec_{mevcut_ft.id}",
                                             type="primary"):
                                    for old_ft in tum_teklifler:
                                        if old_ft.secildi:
                                            old_ft.secildi = False
                                            store.upsert("fiyat_teklifleri", old_ft)
                                    mevcut_ft.secildi = True
                                    store.upsert("fiyat_teklifleri", mevcut_ft)
                                    secilen_talep.secilen_teklif_id = mevcut_ft.id
                                    secilen_talep.durum = "Teklif Alindi"
                                    secilen_talep.updated_at = _now()
                                    store.upsert("satin_alma_talepleri", secilen_talep)
                                    st.rerun()

                            # Sil butonu
                            if confirm_action("Teklifi Sil", "Bu fiyat teklifini silmek istediğinize emin misiniz?", key=f"sa_teklif_sil_{mevcut_ft.id}"):
                                store.delete_by_id("fiyat_teklifleri", mevcut_ft.id)
                                if secilen_talep.secilen_teklif_id == mevcut_ft.id:
                                    secilen_talep.secilen_teklif_id = ""
                                    secilen_talep.durum = "Teklif Bekleniyor"
                                    secilen_talep.updated_at = _now()
                                    store.upsert("satin_alma_talepleri", secilen_talep)
                                st.rerun()
                        else:
                            # Yeni teklif formu
                            styled_section(f"{sira}. Teklif Ekle", "#ea580c")

                            if not aktif_ted:
                                styled_info_banner(
                                    "Tedarikci bulunmuyor. Önce 'Tedarikci Rehberi' sekmesinden "
                                    "tedarikci ekleyin.", banner_type="warning", icon="")
                            else:
                                secilen_ted_label = st.selectbox(
                                    "Tedarikci", ["-- Tedarikci secin --"] + list(ted_options_map.keys()),
                                    key=f"sa_ft_ted_{teklif_idx}")
                                secilen_ted = ted_options_map.get(secilen_ted_label)

                                if secilen_ted:
                                    fk1, fk2, fk3 = st.columns(3)
                                    with fk1:
                                        ft_kdv = st.number_input(
                                            "KDV Orani (%)", value=20.0, step=1.0,
                                            key=f"sa_ft_kdv_{teklif_idx}")
                                    with fk2:
                                        ft_odeme = st.selectbox(
                                            "Odeme Yontemi", ODEME_YONTEMLERI,
                                            key=f"sa_ft_odeme_{teklif_idx}")
                                    with fk3:
                                        ft_teslim_gun = st.number_input(
                                            "Teslim Suresi (gun)", min_value=0, value=7,
                                            key=f"sa_ft_teslim_{teklif_idx}")

                                    ft_gecerlilik = st.date_input(
                                        "Gecerlilik Tarihi", key=f"sa_ft_gec_{teklif_idx}")

                                    st.markdown("**Kalem Fiyatlandirma:**")
                                    ft_kalemler = []
                                    ft_toplam = 0.0
                                    for km_idx, km in enumerate(talep_kalemleri):
                                        fc1, fc2, fc3 = st.columns([4, 2, 2])
                                        with fc1:
                                            st.text(f'{km.get("urun_adi", "")} '
                                                    f'({km.get("miktar", 0):.0f} {km.get("birim", "")})')
                                        with fc2:
                                            bf = st.number_input(
                                                "Birim Fiyat", min_value=0.0, step=1.0,
                                                value=float(km.get("tahmini_fiyat", 0)),
                                                key=f"sa_ft_bf_{teklif_idx}_{km_idx}")
                                        with fc3:
                                            kalem_top = km.get("miktar", 0) * bf
                                            ft_toplam += kalem_top
                                            st.text(f"Toplam: {kalem_top:,.2f} TL")

                                        ft_kalemler.append({
                                            "urun_adi": km.get("urun_adi", ""),
                                            "miktar": km.get("miktar", 0),
                                            "birim": km.get("birim", ""),
                                            "birim_fiyat": bf,
                                            "toplam": kalem_top,
                                            "kategori": km.get("kategori", ""),
                                            "demirbas_kategori": km.get("demirbas_kategori", ""),
                                        })

                                    kdv_dahil = ft_toplam * (1 + ft_kdv / 100)
                                    st.markdown(
                                        f'<div style="text-align:right;margin:8px 0;">'
                                        f'Ara Toplam: <b>{ft_toplam:,.2f} TL</b> | '
                                        f'KDV Dahil: <b style="color:#2563eb;">'
                                        f'{kdv_dahil:,.2f} TL</b></div>',
                                        unsafe_allow_html=True,
                                    )

                                    ft_notlar = st.text_area(
                                        "Teklif Notları", key=f"sa_ft_not_{teklif_idx}",
                                        height=60)

                                    if st.button(f"{sira}. Teklifi Kaydet", type="primary",
                                                 key=f"sa_ft_kaydet_{teklif_idx}"):
                                        teklif = FiyatTeklifi(
                                            teklif_kodu=store.next_teklif_code(),
                                            talep_id=secilen_talep.id,
                                            tedarikci_id=secilen_ted.id,
                                            tedarikci_adi=secilen_ted.firma_adi,
                                            gecerlilik_tarihi=(
                                                ft_gecerlilik.isoformat() if ft_gecerlilik else ""),
                                            kalemler=ft_kalemler,
                                            toplam_tutar=ft_toplam,
                                            kdv_orani=ft_kdv,
                                            kdv_dahil_tutar=kdv_dahil,
                                            odeme_yontemi=ft_odeme,
                                            teslim_suresi_gun=ft_teslim_gun,
                                            notlar=ft_notlar,
                                        )
                                        store.upsert("fiyat_teklifleri", teklif)
                                        store.log("fiyat_teklifi", "teklif", teklif.id,
                                                  f"{sira}. Teklif: {teklif.teklif_kodu} / "
                                                  f"{secilen_ted.firma_adi}",
                                                  AuthManager.get_current_user().get("name", ""))
                                        styled_info_banner(
                                            f"{sira}. Teklif kaydedildi: {teklif.teklif_kodu} | "
                                            f"{kdv_dahil:,.2f} TL", banner_type="success", icon="")
                                        st.rerun()

                # ---- KARSILASTIRMA SEKMESI ----
                with ft_tabs[3]:
                    styled_section("Teklif Karsilastirma Tablosu", "#2563eb")

                    if len(tum_teklifler) < 2:
                        styled_info_banner(
                            "Karsilastirma için en az 2 teklif gereklidir. "
                            "1. ve 2. Teklif sekmelerinden teklif ekleyin.", banner_type="warning", icon="")
                    else:
                        # Baslik satiri
                        baslik_cols = '<th style="padding:10px;text-align:left;' \
                                      'background:#94A3B8;color:white;min-width:140px;">Kalem</th>'
                        for i, ft in enumerate(tum_teklifler[:3]):
                            secildi_stil = "border:2px solid #10b981;" if ft.secildi else ""
                            baslik_cols += (
                                f'<th style="padding:10px;text-align:center;'
                                f'background:#94A3B8;color:white;min-width:160px;{secildi_stil}">'
                                f'{i + 1}. Teklif<br>'
                                f'<span style="font-size:11px;font-weight:400;color:#94a3b8;">'
                                f'{ft.tedarikci_adi}</span></th>'
                            )

                        # Kalem satirlari
                        kalem_satirlari = ""
                        kalem_adlari = []
                        for km in talep_kalemleri:
                            kalem_adlari.append(km.get("urun_adi", ""))

                        for k_idx, k_adi in enumerate(kalem_adlari):
                            fiyatlar = []
                            for ft in tum_teklifler[:3]:
                                if k_idx < len(ft.kalemler):
                                    fiyatlar.append(ft.kalemler[k_idx].get("birim_fiyat", 0))
                                else:
                                    fiyatlar.append(0)

                            en_dusuk = min(f for f in fiyatlar if f > 0) if any(f > 0 for f in fiyatlar) else 0

                            miktar = talep_kalemleri[k_idx].get("miktar", 0) if k_idx < len(talep_kalemleri) else 0
                            birim = talep_kalemleri[k_idx].get("birim", "") if k_idx < len(talep_kalemleri) else ""
                            kalem_satirlari += (
                                f'<tr><td style="padding:8px 10px;border-bottom:1px solid #e2e8f0;'
                                f'font-weight:600;">{k_adi}'
                                f'<br><span style="font-size:11px;color:#64748b;font-weight:400;">'
                                f'{miktar:.0f} {birim}</span></td>'
                            )
                            for f_idx, fiyat in enumerate(fiyatlar):
                                toplam_k = miktar * fiyat
                                en_dusuk_mi = fiyat == en_dusuk and fiyat > 0 and len([x for x in fiyatlar if x > 0]) > 1
                                bg = "#f0fdf4" if en_dusuk_mi else "#fff"
                                renk = "#10b981" if en_dusuk_mi else "#94A3B8"
                                badge = (' <span style="background:#10b98130;color:#10b981;'
                                         'padding:1px 5px;border-radius:4px;font-size:9px;'
                                         'font-weight:700;">EN UYGUN</span>'
                                         if en_dusuk_mi else "")
                                kalem_satirlari += (
                                    f'<td style="padding:8px 10px;border-bottom:1px solid #e2e8f0;'
                                    f'text-align:center;background:{bg};">'
                                    f'<span style="font-weight:700;color:{renk};">'
                                    f'{fiyat:,.2f} TL</span>{badge}'
                                    f'<br><span style="font-size:11px;color:#64748b;">'
                                    f'{toplam_k:,.2f} TL</span></td>'
                                )
                            kalem_satirlari += "</tr>"

                        # Ozet satirlari (Ara Toplam, KDV, Genel Toplam)
                        ozet_rows = ""
                        for ozet_adi, alan, bold in [
                            ("Ara Toplam", "toplam_tutar", False),
                            ("KDV", None, False),
                            ("GENEL TOPLAM", "kdv_dahil_tutar", True),
                        ]:
                            ozet_rows += (
                                f'<tr style="background:#111827;"><td style="padding:8px 10px;'
                                f'font-weight:700;border-top:2px solid #e2e8f0;">{ozet_adi}</td>'
                            )
                            tutarlar = []
                            for ft in tum_teklifler[:3]:
                                if alan:
                                    tutarlar.append(getattr(ft, alan, 0))
                                else:
                                    tutarlar.append(ft.kdv_dahil_tutar - ft.toplam_tutar)

                            en_dusuk_t = min(t for t in tutarlar if t > 0) if any(t > 0 for t in tutarlar) else 0

                            for t_val in tutarlar:
                                en_uygun = (t_val == en_dusuk_t and t_val > 0
                                            and alan == "kdv_dahil_tutar"
                                            and len([x for x in tutarlar if x > 0]) > 1)
                                fs = "18px" if bold else "13px"
                                fw = "800" if bold else "600"
                                bg = "#f0fdf4" if en_uygun else "#111827"
                                renk = "#10b981" if en_uygun else "#2563eb" if bold else "#94A3B8"
                                badge_t = (' <span style="background:#10b98130;color:#10b981;'
                                           'padding:2px 6px;border-radius:6px;font-size:10px;'
                                           'font-weight:700;">EN UYGUN</span>'
                                           if en_uygun else "")
                                ozet_rows += (
                                    f'<td style="padding:8px 10px;text-align:center;'
                                    f'border-top:2px solid #e2e8f0;background:{bg};">'
                                    f'<span style="font-size:{fs};font-weight:{fw};color:{renk};">'
                                    f'{t_val:,.2f} TL</span>{badge_t}</td>'
                                )
                            ozet_rows += "</tr>"

                        # Teslim suresi + Odeme satirlari
                        ekstra_rows = ""
                        for bilgi_adi, attr in [("Teslim Suresi", "teslim_suresi_gun"),
                                                 ("Odeme Yontemi", "odeme_yontemi")]:
                            ekstra_rows += (
                                f'<tr><td style="padding:6px 10px;color:#64748b;'
                                f'font-size:12px;">{bilgi_adi}</td>'
                            )
                            for ft in tum_teklifler[:3]:
                                val = getattr(ft, attr, "")
                                if attr == "teslim_suresi_gun":
                                    val = f"{val} gun"
                                ekstra_rows += (
                                    f'<td style="padding:6px 10px;text-align:center;'
                                    f'font-size:12px;color:#64748b;">{val}</td>'
                                )
                            ekstra_rows += "</tr>"

                        st.markdown(
                            f'<div style="overflow-x:auto;border-radius:12px;'
                            f'border:1px solid #e2e8f0;box-shadow:0 4px 12px rgba(0,0,0,.08);'
                            f'margin:10px 0;">'
                            f'<table style="width:100%;border-collapse:collapse;font-size:13px;">'
                            f'<thead><tr>{baslik_cols}</tr></thead>'
                            f'<tbody>{kalem_satirlari}{ozet_rows}{ekstra_rows}</tbody>'
                            f'</table></div>',
                            unsafe_allow_html=True,
                        )

                        # Teklif secim butonlari
                        if secilen_talep.durum == "Teklif Bekleniyor":
                            styled_section("Teklif Sec", "#10b981")
                            sec_cols = st.columns(len(tum_teklifler[:3]))
                            for s_idx, ft in enumerate(tum_teklifler[:3]):
                                with sec_cols[s_idx]:
                                    label = f"{s_idx + 1}. Teklifi Sec ({ft.tedarikci_adi})"
                                    if ft.secildi:
                                        st.success(f"{s_idx + 1}. Teklif secili")
                                    elif st.button(label, key=f"sa_kars_sec_{ft.id}",
                                                   type="primary", use_container_width=True):
                                        for old_ft in tum_teklifler:
                                            if old_ft.secildi:
                                                old_ft.secildi = False
                                                store.upsert("fiyat_teklifleri", old_ft)
                                        ft.secildi = True
                                        store.upsert("fiyat_teklifleri", ft)
                                        secilen_talep.secilen_teklif_id = ft.id
                                        secilen_talep.durum = "Teklif Alindi"
                                        secilen_talep.updated_at = _now()
                                        store.upsert("satin_alma_talepleri", secilen_talep)
                                        st.rerun()

    # ----- ALT SEKME 4: TEDARIKCI REHBERI -----
    with sub[3]:
        styled_section("Tedarikci Rehberi", "#0d9488")

        tedarikciler = store.load_objects("tedarikciler")
        aktif_ted = [t for t in tedarikciler if t.aktif]
        pasif_ted = [t for t in tedarikciler if not t.aktif]

        styled_stat_row([
            ("Toplam Tedarikci", len(tedarikciler), "#0d9488", ""),
            ("Aktif", len(aktif_ted), "#10b981", ""),
            ("Pasif", len(pasif_ted), "#94a3b8", ""),
        ])

        # Liste
        for ted in sorted(tedarikciler, key=lambda x: x.firma_adi):
            durum_badge = (
                '<span style="background:#10b98120;color:#10b981;padding:2px 6px;'
                'border-radius:6px;font-size:10px;font-weight:700;">Aktif</span>'
                if ted.aktif else
                '<span style="background:#94a3b820;color:#94a3b8;padding:2px 6px;'
                'border-radius:6px;font-size:10px;font-weight:700;">Pasif</span>'
            )
            gruplar = ", ".join(ted.urun_gruplari) if ted.urun_gruplari else "-"
            st.markdown(
                f'<div style="background:#111827;border:1px solid #e2e8f0;'
                f'border-radius:8px;padding:10px 14px;margin:4px 0;">'
                f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
                f'<b>{ted.tedarikci_kodu}</b>'
                f'<span style="font-weight:700;">{ted.firma_adi}</span>'
                f'<span style="color:#64748b;font-size:12px;">{ted.yetkili_kisi}</span>'
                f'<span style="color:#64748b;font-size:12px;">{ted.telefon}</span>'
                f'{durum_badge}'
                f'<span style="color:#8b5cf6;font-size:11px;margin-left:auto;">'
                f'{gruplar}</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

        # Yeni tedarikci ekleme
        with st.expander("Yeni Tedarikci Ekle", expanded=not tedarikciler):
            nt1, nt2 = st.columns(2)
            with nt1:
                nt_firma = st.text_input("Firma Adi *", key="sa_nt_firma")
                nt_yetkili = st.text_input("Yetkili Kisi", key="sa_nt_yetkili")
                nt_telefon = st.text_input("Telefon", key="sa_nt_tel")
                nt_email = st.text_input("Email", key="sa_nt_email")
            with nt2:
                nt_adres = st.text_area("Adres", key="sa_nt_adres", height=68)
                nt_vergi_no = st.text_input("Vergi No", key="sa_nt_vergino")
                nt_vergi_d = st.text_input("Vergi Dairesi", key="sa_nt_vergid")
                nt_gruplar = st.multiselect(
                    "Urun Gruplari",
                    TUKETIM_KATEGORILERI + DEMIRBAS_KATEGORILERI,
                    key="sa_nt_gruplar",
                )
            nt_notlar = st.text_area("Notlar", key="sa_nt_notlar", height=50)

            if st.button("Tedarikci Kaydet", type="primary", key="sa_nt_kaydet"):
                if not nt_firma:
                    styled_info_banner("Firma adi gereklidir.", banner_type="error", icon="")
                else:
                    yeni_ted = Tedarikci(
                        tedarikci_kodu=store.next_tedarikci_code(),
                        firma_adi=nt_firma,
                        yetkili_kisi=nt_yetkili,
                        telefon=nt_telefon,
                        email=nt_email,
                        adres=nt_adres,
                        vergi_no=nt_vergi_no,
                        vergi_dairesi=nt_vergi_d,
                        urun_gruplari=nt_gruplar,
                        notlar=nt_notlar,
                    )
                    store.upsert("tedarikciler", yeni_ted)
                    styled_info_banner(
                        f"Tedarikci eklendi: {yeni_ted.tedarikci_kodu} - {nt_firma}", banner_type="success", icon="")
                    st.rerun()

    # ----- ALT SEKME 5: SIPARIS TAKIP -----
    with sub[4]:
        styled_section("Siparis Takip", "#ea580c")

        siparisler = store.load_objects("siparis_takipleri")
        siparisler.sort(key=lambda s: s.created_at, reverse=True)

        aktif_sip = [s for s in siparisler if s.durum == "Siparis Verildi"]
        teslim_sip = [s for s in siparisler if s.durum == "Teslim Alindi"]

        styled_stat_row([
            ("Toplam Siparis", len(siparisler), "#ea580c", ""),
            ("Aktif (Bekleyen)", len(aktif_sip), "#f59e0b", ""),
            ("Teslim Alinan", len(teslim_sip), "#10b981", ""),
        ])

        for sip in siparisler:
            sip_renk = "#f59e0b" if sip.durum == "Siparis Verildi" else "#10b981"
            gecikme = ""
            if sip.durum == "Siparis Verildi" and sip.beklenen_teslim:
                try:
                    bek = date.fromisoformat(sip.beklenen_teslim)
                    if date.today() > bek:
                        fark = (date.today() - bek).days
                        gecikme = (f' <span style="background:#ef444420;color:#ef4444;'
                                   f'padding:1px 6px;border-radius:6px;font-size:10px;'
                                   f'font-weight:700;">{fark} gun gecikme</span>')
                except ValueError:
                    pass

            st.markdown(
                f'<div style="background:#111827;border:1px solid #e2e8f0;'
                f'border-radius:10px;padding:12px 16px;margin:6px 0;">'
                f'<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">'
                f'<b>{sip.siparis_kodu}</b>'
                f'<span style="color:#64748b;">{sip.tedarikci_adi}</span>'
                f'<span style="color:#64748b;font-size:12px;">'
                f'Siparis: {sip.siparis_tarihi}</span>'
                f'<span style="color:#64748b;font-size:12px;">'
                f'Beklenen: {sip.beklenen_teslim or "-"}</span>'
                f'<span style="background:{sip_renk}20;color:{sip_renk};padding:2px 8px;'
                f'border-radius:8px;font-size:11px;font-weight:600;">{sip.durum}</span>'
                f'{gecikme}'
                f'</div></div>',
                unsafe_allow_html=True,
            )

            if sip.durum == "Siparis Verildi":
                with st.expander(f"Teslim Al: {sip.siparis_kodu}"):
                    st_alan = st.text_input("Teslim Alan Kisi",
                                             key=f"sa_sip_alan_{sip.id}")
                    if st.button("Teslim Al ve Stokla", type="primary",
                                 key=f"sa_sip_teslim_{sip.id}"):
                        ok, msg = store.teslim_al_ve_stokla(
                            sip.id,
                            st_alan or AuthManager.get_current_user().get("name", ""),
                        )
                        if ok:
                            styled_info_banner(msg, banner_type="success", icon="")
                        else:
                            styled_info_banner(msg, banner_type="error", icon="")
                        st.rerun()
            elif sip.durum == "Teslim Alindi":
                st.caption(
                    f"Teslim: {sip.gercek_teslim} | Alan: {sip.teslim_alan}")

    # ----- ALT SEKME 6: RAPORLAR -----
    with sub[5]:
        styled_header("Satın Alma Raporlari", "Günlük, haftalik, aylik, yillik ve tarih aralikli raporlar")

        r_tabs = st.tabs(["📅 Günlük", "📆 Haftalık", "📊 Aylık", "📈 Yıllık", "📅 Tarih Aralığı", "📄 PDF Rapor"])

        # -- yardimci: talepleri tarih araligina gore filtrele --
        def _sa_donem_verileri(bas_str: str, bit_str: str):
            """Satin alma verilerini donem için hesapla."""
            talepler = store.load_objects("satin_alma_talepleri")
            teklifler = store.load_objects("fiyat_teklifleri")
            siparisler = store.load_objects("siparis_takipleri")
            tedarikciler = store.load_objects("tedarikciler")

            donem_talepler = [t for t in talepler
                              if bas_str <= (t.talep_tarihi or t.created_at[:10]) <= bit_str]
            donem_siparisler = [s for s in siparisler
                                if bas_str <= (s.siparis_tarihi or s.created_at[:10]) <= bit_str]
            donem_teklifler = [f for f in teklifler
                               if bas_str <= (f.teklif_tarihi or f.created_at[:10]) <= bit_str]

            toplam_talep = len(donem_talepler)
            onaylanan = len([t for t in donem_talepler if t.durum in ("Onaylandi", "Siparis Verildi", "Teslim Alindi")])
            reddedilen = len([t for t in donem_talepler if t.durum == "Red"])
            bekleyen = len([t for t in donem_talepler if t.durum in ("Taslak", "Teklif Bekleniyor", "Teklif Alindi", "Onay Bekliyor")])

            toplam_tahmini = sum(t.toplam_tahmini_tutar for t in donem_talepler)
            # Gerceklesen tutar: secilen tekliflerin KDV dahil tutari
            gerceklesen_tutar = 0.0
            for t in donem_talepler:
                if t.secilen_teklif_id:
                    teklif = store.get_by_id("fiyat_teklifleri", t.secilen_teklif_id)
                    if teklif:
                        gerceklesen_tutar += teklif.kdv_dahil_tutar

            teslim_alinan = len([s for s in donem_siparisler if s.durum == "Teslim Alindi"])
            aktif_siparis = len([s for s in donem_siparisler if s.durum == "Siparis Verildi"])

            # Durum dagilimi
            durum_dagilimi: dict[str, int] = {}
            for t in donem_talepler:
                durum_dagilimi[t.durum] = durum_dagilimi.get(t.durum, 0) + 1

            # Oncelik dagilimi
            oncelik_dagilimi: dict[str, int] = {}
            for t in donem_talepler:
                oncelik_dagilimi[t.oncelik] = oncelik_dagilimi.get(t.oncelik, 0) + 1

            # Tedarikci bazli tutar
            tedarikci_tutar: dict[str, float] = {}
            for ft in donem_teklifler:
                if ft.secildi and ft.kdv_dahil_tutar > 0:
                    tedarikci_tutar[ft.tedarikci_adi] = tedarikci_tutar.get(ft.tedarikci_adi, 0) + ft.kdv_dahil_tutar

            # Kategori bazli talep (kalemlerden)
            kategori_talep: dict[str, int] = {}
            for t in donem_talepler:
                for k in (t.kalemler or []):
                    kat = k.get("kategori", "Diger") or "Diger"
                    kategori_talep[kat] = kategori_talep.get(kat, 0) + 1

            # Detay tablosu
            detay_rows = []
            for t in donem_talepler:
                kalem_sayisi = len(t.kalemler) if t.kalemler else 0
                detay_rows.append({
                    "Talep Kodu": t.talep_kodu,
                    "Tarih": t.talep_tarihi or t.created_at[:10],
                    "Talep Eden": t.talep_eden,
                    "Kalem": kalem_sayisi,
                    "Tahmini Tutar": f"{t.toplam_tahmini_tutar:,.2f} TL",
                    "Öncelik": t.oncelik,
                    "Durum": t.durum,
                })

            return {
                "toplam_talep": toplam_talep,
                "onaylanan": onaylanan,
                "reddedilen": reddedilen,
                "bekleyen": bekleyen,
                "toplam_tahmini": toplam_tahmini,
                "gerceklesen_tutar": gerceklesen_tutar,
                "teslim_alinan": teslim_alinan,
                "aktif_siparis": aktif_siparis,
                "durum_dagilimi": durum_dagilimi,
                "oncelik_dagilimi": oncelik_dagilimi,
                "tedarikci_tutar": tedarikci_tutar,
                "kategori_talep": kategori_talep,
                "detay_rows": detay_rows,
                "donem_talepler": donem_talepler,
            }

        def _sa_goster_istatistik(veri: dict, donem_adi: str):
            """Satin alma istatistiklerini goster."""
            from utils.report_utils import ReportStyler

            styled_stat_row([
                ("Toplam Talep", str(veri["toplam_talep"]), "#2563eb", "📋"),
                ("Onaylanan", str(veri["onaylanan"]), "#10b981", "✅"),
                ("Bekleyen", str(veri["bekleyen"]), "#f59e0b", "⏳"),
                ("Reddedilen", str(veri["reddedilen"]), "#ef4444", "❌"),
            ])
            styled_stat_row([
                ("Tahmini Tutar", f"{veri['toplam_tahmini']:,.2f} TL", "#4472C4", "💰"),
                ("Gerceklesen", f"{veri['gerceklesen_tutar']:,.2f} TL", "#10b981", "💳"),
                ("Teslim Alinan", str(veri["teslim_alinan"]), "#8b5cf6", "📦"),
                ("Aktif Siparis", str(veri["aktif_siparis"]), "#ea580c", "🚚"),
            ])

            # Grafikler
            col_a, col_b = st.columns(2)
            with col_a:
                if veri["durum_dagilimi"]:
                    styled_section("Durum Dagilimi")
                    durum_renkleri = {
                        "Taslak": "#94a3b8", "Teklif Bekleniyor": "#60a5fa",
                        "Teklif Alindi": "#38bdf8", "Onay Bekliyor": "#f59e0b",
                        "Onaylandi": "#10b981", "Red": "#ef4444",
                        "Siparis Verildi": "#8b5cf6", "Teslim Alindi": "#059669",
                        "Iptal": "#6b7280",
                    }
                    st.markdown(
                        ReportStyler.sunburst_chart_svg(
                            {k: float(v) for k, v in veri["durum_dagilimi"].items()},
                            title=f"{donem_adi} Durum Dagilimi",
                        ),
                        unsafe_allow_html=True,
                    )
            with col_b:
                if veri["oncelik_dagilimi"]:
                    styled_section("Öncelik Dagilimi")
                    st.markdown(
                        ReportStyler.sunburst_chart_svg(
                            {k: float(v) for k, v in veri["oncelik_dagilimi"].items()},
                            title=f"{donem_adi} Öncelik Dagilimi",
                        ),
                        unsafe_allow_html=True,
                    )

            col_c, col_d = st.columns(2)
            with col_c:
                if veri["tedarikci_tutar"]:
                    styled_section("Tedarikci Bazli Harcama")
                    st.markdown(
                        ReportStyler.horizontal_bar_html(
                            dict(sorted(veri["tedarikci_tutar"].items(), key=lambda x: x[1], reverse=True)),
                            "#4472C4",
                        ),
                        unsafe_allow_html=True,
                    )
            with col_d:
                if veri["kategori_talep"]:
                    styled_section("Kategori Bazli Talep Sayısı")
                    st.markdown(
                        ReportStyler.horizontal_bar_html(
                            dict(sorted(veri["kategori_talep"].items(), key=lambda x: x[1], reverse=True)),
                            "#ED7D31",
                        ),
                        unsafe_allow_html=True,
                    )

            # Detay tablosu
            if veri["detay_rows"]:
                styled_section("Talep Detaylari")
                st.dataframe(
                    pd.DataFrame(veri["detay_rows"]),
                    use_container_width=True,
                    hide_index=True,
                )

        # ---- Gunluk ----
        with r_tabs[0]:
            styled_section("Günlük Satın Alma Raporu")
            sa_gun = st.date_input("Tarih", value=date.today(), key="sa_rap_gun")
            veri = _sa_donem_verileri(sa_gun.isoformat(), sa_gun.isoformat())
            if veri["toplam_talep"] == 0:
                styled_info_banner("Bu tarih için satin alma talebi bulunamadı.", banner_type="info", icon="📊")
            else:
                _sa_goster_istatistik(veri, f"Günlük ({sa_gun.isoformat()})")

        # ---- Haftalik ----
        with r_tabs[1]:
            styled_section("Haftalık Satın Alma Raporu")
            bugun_h = date.today()
            hafta_bas_h = (bugun_h - timedelta(days=bugun_h.weekday())).isoformat()
            hafta_bit_h = bugun_h.isoformat()
            st.info(f"Bu hafta: {hafta_bas_h} - {hafta_bit_h}")

            veri = _sa_donem_verileri(hafta_bas_h, hafta_bit_h)
            if veri["toplam_talep"] == 0:
                styled_info_banner("Bu hafta için satin alma talebi bulunamadı.", banner_type="info", icon="📊")
            else:
                _sa_goster_istatistik(veri, f"Haftalık ({hafta_bas_h} - {hafta_bit_h})")

        # ---- Aylik ----
        with r_tabs[2]:
            styled_section("Aylık Satın Alma Raporu")
            bugun_a = date.today()
            ay_bas_a = bugun_a.replace(day=1).isoformat()
            ay_bit_a = bugun_a.isoformat()
            st.info(f"Bu ay: {ay_bas_a} - {ay_bit_a}")

            veri = _sa_donem_verileri(ay_bas_a, ay_bit_a)
            if veri["toplam_talep"] == 0:
                styled_info_banner("Bu ay için satin alma talebi bulunamadı.", banner_type="info", icon="📊")
            else:
                _sa_goster_istatistik(veri, f"Aylık ({ay_bas_a} - {ay_bit_a})")

                # Onceki ayla karsilastirma
                onceki_ay_bit_a = (bugun_a.replace(day=1) - timedelta(days=1))
                onceki_ay_bas_a = onceki_ay_bit_a.replace(day=1).isoformat()
                onceki_veri = _sa_donem_verileri(onceki_ay_bas_a, onceki_ay_bit_a.isoformat())
                if onceki_veri["toplam_talep"] > 0:
                    onceki_tutar = onceki_veri["gerceklesen_tutar"]
                    bu_tutar = veri["gerceklesen_tutar"]
                    if onceki_tutar > 0:
                        degisim = ((bu_tutar - onceki_tutar) / onceki_tutar) * 100
                        ok = "📈" if degisim > 0 else "📉" if degisim < 0 else "➡️"
                        renk = "#ef4444" if degisim > 0 else "#10b981" if degisim < 0 else "#64748b"
                        styled_info_banner(
                            f"Önceki aya gore harcama degisimi: <b style='color:{renk};'>%{degisim:+.1f} {ok}</b>",
                            renk, "📊"
                        )

        # ---- Yillik ----
        with r_tabs[3]:
            styled_section("Yıllık Satın Alma Raporu")
            bugun_y = date.today()
            yil_sec = st.selectbox("Yil", list(range(bugun_y.year, bugun_y.year - 3, -1)),
                                    key="sa_rap_yil")
            yil_bas = f"{yil_sec}-01-01"
            yil_bit = f"{yil_sec}-12-31" if yil_sec < bugun_y.year else bugun_y.isoformat()
            st.info(f"Donem: {yil_bas} - {yil_bit}")

            veri = _sa_donem_verileri(yil_bas, yil_bit)
            if veri["toplam_talep"] == 0:
                styled_info_banner("Bu yil için satin alma talebi bulunamadı.", banner_type="info", icon="📊")
            else:
                _sa_goster_istatistik(veri, f"Yıllık ({yil_sec})")

                # Ay bazli trend
                from utils.report_utils import ReportStyler
                ay_adlari = ["Oca", "Sub", "Mar", "Nis", "May", "Haz",
                             "Tem", "Agu", "Eyl", "Eki", "Kas", "Ara"]
                ay_talep: dict[str, float] = {}
                ay_tutar: dict[str, float] = {}
                son_ay = 12 if yil_sec < bugun_y.year else bugun_y.month
                for ay in range(1, son_ay + 1):
                    ay_b = f"{yil_sec}-{ay:02d}-01"
                    if ay < 12:
                        ay_e_d = date(yil_sec, ay + 1, 1) - timedelta(days=1)
                    else:
                        ay_e_d = date(yil_sec, 12, 31)
                    ay_e = ay_e_d.isoformat()
                    ay_veri = _sa_donem_verileri(ay_b, ay_e)
                    ay_talep[ay_adlari[ay - 1]] = float(ay_veri["toplam_talep"])
                    ay_tutar[ay_adlari[ay - 1]] = ay_veri["gerceklesen_tutar"]

                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    if any(v > 0 for v in ay_talep.values()):
                        styled_section("Aylık Talep Trendi")
                        st.markdown(
                            ReportStyler.horizontal_bar_html(
                                {k: v for k, v in ay_talep.items() if v > 0}, "#4472C4"
                            ),
                            unsafe_allow_html=True,
                        )
                with col_t2:
                    if any(v > 0 for v in ay_tutar.values()):
                        styled_section("Aylık Harcama Trendi (TL)")
                        st.markdown(
                            ReportStyler.horizontal_bar_html(
                                {k: v for k, v in ay_tutar.items() if v > 0}, "#10b981"
                            ),
                            unsafe_allow_html=True,
                        )

        # ---- Tarih Araligi ----
        with r_tabs[4]:
            styled_section("Özel Tarih Araligi")
            tc1, tc2 = st.columns(2)
            with tc1:
                sa_bas = st.date_input("Başlangıç", value=date.today() - timedelta(days=30),
                                        key="sa_rap_ta_bas")
            with tc2:
                sa_bit = st.date_input("Bitis", value=date.today(), key="sa_rap_ta_bit")

            veri = _sa_donem_verileri(sa_bas.isoformat(), sa_bit.isoformat())
            if veri["toplam_talep"] == 0:
                styled_info_banner("Secilen tarih araliginda satin alma talebi bulunamadı.", banner_type="info", icon="📊")
            else:
                _sa_goster_istatistik(veri, f"Donem ({sa_bas} - {sa_bit})")

        # ---- PDF Rapor ----
        with r_tabs[5]:
            styled_section("Satın Alma PDF Rapor")
            pc1, pc2 = st.columns(2)
            with pc1:
                sa_pdf_bas = st.date_input("Başlangıç",
                                            value=date.today().replace(day=1),
                                            key="sa_pdf_bas")
            with pc2:
                sa_pdf_bit = st.date_input("Bitis", value=date.today(), key="sa_pdf_bit")

            if st.button("PDF Oluştur", key="sa_pdf_btn", type="primary"):
                try:
                    from utils.report_utils import ReportPDFGenerator, get_institution_info
                    veri = _sa_donem_verileri(sa_pdf_bas.isoformat(), sa_pdf_bit.isoformat())

                    pdf = ReportPDFGenerator(
                        "Satın Alma Raporu",
                        f"{sa_pdf_bas.isoformat()} - {sa_pdf_bit.isoformat()}",
                    )
                    info = get_institution_info()
                    pdf.add_header(kurum_adi=info.get("name", ""))

                    # Genel ozet
                    pdf.add_section("Genel Özet")
                    pdf.add_metrics([
                        ("Toplam Talep", veri["toplam_talep"], "#2563eb"),
                        ("Onaylanan", veri["onaylanan"], "#10b981"),
                        ("Bekleyen", veri["bekleyen"], "#f59e0b"),
                        ("Reddedilen", veri["reddedilen"], "#ef4444"),
                    ])
                    pdf.add_metrics([
                        ("Tahmini Tutar", f"{veri['toplam_tahmini']:,.2f} TL", "#4472C4"),
                        ("Gerceklesen", f"{veri['gerceklesen_tutar']:,.2f} TL", "#10b981"),
                        ("Teslim Alinan", veri["teslim_alinan"], "#8b5cf6"),
                        ("Aktif Siparis", veri["aktif_siparis"], "#ea580c"),
                    ])

                    # Durum dagilimi
                    if veri["durum_dagilimi"]:
                        pdf.add_section("Durum Dagilimi")
                        durum_df = pd.DataFrame([
                            {"Durum": k, "Adet": v}
                            for k, v in sorted(veri["durum_dagilimi"].items(), key=lambda x: x[1], reverse=True)
                        ])
                        pdf.add_table(durum_df)
                        pdf.add_bar_chart(
                            {k: float(v) for k, v in veri["durum_dagilimi"].items()},
                            "Durum Dagilimi", "#2563eb",
                        )

                    # Tedarikci bazli harcama
                    if veri["tedarikci_tutar"]:
                        pdf.add_section("Tedarikci Bazli Harcama")
                        ted_df = pd.DataFrame([
                            {"Tedarikci": k, "Tutar (TL)": f"{v:,.2f}"}
                            for k, v in sorted(veri["tedarikci_tutar"].items(), key=lambda x: x[1], reverse=True)
                        ])
                        pdf.add_table(ted_df)
                        pdf.add_bar_chart(veri["tedarikci_tutar"], "Tedarikci Harcamalari", "#4472C4")

                    # Kategori dagilimi
                    if veri["kategori_talep"]:
                        pdf.add_section("Kategori Bazli Talep Sayısı")
                        kat_df = pd.DataFrame([
                            {"Kategori": k, "Adet": v}
                            for k, v in sorted(veri["kategori_talep"].items(), key=lambda x: x[1], reverse=True)
                        ])
                        pdf.add_table(kat_df)
                        pdf.add_bar_chart(
                            {k: float(v) for k, v in veri["kategori_talep"].items()},
                            "Kategori Dagilimi", "#ED7D31",
                        )

                    # Detay tablosu
                    if veri["detay_rows"]:
                        pdf.add_section("Talep Detaylari")
                        pdf.add_table(pd.DataFrame(veri["detay_rows"]))

                    pdf_bytes = pdf.generate()
                    st.download_button(
                        "PDF Indir", pdf_bytes,
                        file_name=f"satin_alma_raporu_{sa_pdf_bas}_{sa_pdf_bit}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                    st.success("PDF rapor oluşturuldu!")
                except Exception as e:
                    st.error(f"PDF olusturma hatasi: {e}")


# ============================================================
# ANA RENDER FONKSIYONU
# ============================================================

def render_tuketim_demirbas():
    """TDM-01 modulu ana giris noktasi."""
    _inject_tdm_css()

    store = _get_tdm_store()

    # Ilk kurulumda varsayilan urunleri ve kategorileri yukle
    _seed_varsayilan_urunler(store)
    if not store.load_list("tuketim_kategorileri"):
        for kat in TUKETIM_KATEGORILERI:
            store.upsert("tuketim_kategorileri", TuketimKategori(kod=kat[:3].upper(), ad=kat))
    if not store.load_list("demirbas_kategorileri"):
        for kat in DEMIRBAS_KATEGORILERI:
            store.upsert("demirbas_kategorileri", DemirbasKategori(kod=kat[:3].upper(), ad=kat))

    tab_names = [
        "📊 Dashboard",
        "📦 Günlük Tüketim",
        "📊 Stok Durumu",
        "📈 Tüketim Raporları",
        "🗄️ Demirbaş Kayıt",
        "📝 Zimmet Yönetimi",
        "🛒 Satın Alma",
        "🤖 AI Tavsiye",
        "🔄 Yaşam Döngüsü",
        "💰 Harcama Analiz",
        "🏗️ Envanter Sayım",
        "📱 QR Takip",
        "🔮 Stok Tahmin",
        "🏢 Varlık Endeksi",
        "🔧 Bakım Tahmin",
        "🏪 Tedarik Zinciri",
        "🌱 Sürdürülebilirlik",
        "🧬 Dijital İkiz",
        "🎯 Bütçe Planlama",
        "🏆 Verimlilik",
        "🔗 Denetim Zinciri",
        "🌐 IoT Ekosistem",
        "🎓 Varlık Akademi",
        "⚙️ Ayarlar",
        "🤖 Smarti",
    ]

    render_smarti_welcome("tuketim_demirbas")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("tuketim_demirbas_egitim_yili")

    tabs = st.tabs(tab_names)

    with tabs[0]:
        _render_dashboard(store)
    with tabs[1]:
        _render_gunluk_tuketim(store)
    with tabs[2]:
        _render_stok_durumu(store)
    with tabs[3]:
        _render_tuketim_raporlari(store)
    with tabs[4]:
        _render_demirbas_kayit(store)
    with tabs[5]:
        _render_zimmet_yonetimi(store)
    with tabs[6]:
        _render_satin_alma(store)
    with tabs[7]:
        _render_ai_tavsiye(store)
    with tabs[8]:
        try:
            from views._tdm_yeni_ozellikler import render_yasam_dongusu
            render_yasam_dongusu(store)
        except Exception as _e:
            st.error(f"Yasam Dongusu yuklenemedi: {_e}")
    with tabs[9]:
        try:
            from views._tdm_yeni_ozellikler import render_harcama_analizi
            render_harcama_analizi(store)
        except Exception as _e:
            st.error(f"Harcama Analizi yuklenemedi: {_e}")
    with tabs[10]:
        try:
            from views._tdm_yeni_ozellikler import render_envanter_sayim
            render_envanter_sayim(store)
        except Exception as _e:
            st.error(f"Envanter Sayim yuklenemedi: {_e}")
    with tabs[11]:
        try:
            from views._tdm_super_features import render_qr_takip
            render_qr_takip(store)
        except Exception as _e:
            st.error(f"QR Takip yuklenemedi: {_e}")
    with tabs[12]:
        try:
            from views._tdm_super_features import render_stok_tahmin
            render_stok_tahmin(store)
        except Exception as _e:
            st.error(f"Stok Tahmin yuklenemedi: {_e}")
    with tabs[13]:
        try:
            from views._tdm_super_features import render_varlik_endeksi
            render_varlik_endeksi(store)
        except Exception as _e:
            st.error(f"Varlik Endeksi yuklenemedi: {_e}")
    with tabs[14]:
        try:
            from views._tdm_mega_features import render_bakim_tahmin
            render_bakim_tahmin(store)
        except Exception as _e:
            st.error(f"Bakim Tahmin yuklenemedi: {_e}")
    with tabs[15]:
        try:
            from views._tdm_mega_features import render_tedarik_zinciri
            render_tedarik_zinciri(store)
        except Exception as _e:
            st.error(f"Tedarik Zinciri yuklenemedi: {_e}")
    with tabs[16]:
        try:
            from views._tdm_mega_features import render_surdurulebilirlik
            render_surdurulebilirlik(store)
        except Exception as _e:
            st.error(f"Surdurulebilirlik yuklenemedi: {_e}")
    with tabs[17]:
        try:
            from views._tdm_zirve_features import render_dijital_ikiz
            render_dijital_ikiz(store)
        except Exception as _e:
            st.error(f"Dijital Ikiz yuklenemedi: {_e}")
    with tabs[18]:
        try:
            from views._tdm_zirve_features import render_butce_planlama
            render_butce_planlama(store)
        except Exception as _e:
            st.error(f"Butce Planlama yuklenemedi: {_e}")
    with tabs[19]:
        try:
            from views._tdm_zirve_features import render_verimlilik_liderlik
            render_verimlilik_liderlik(store)
        except Exception as _e:
            st.error(f"Verimlilik Liderlik yuklenemedi: {_e}")
    with tabs[20]:
        try:
            from views._tdm_final_features import render_blokzincir_denetim
            render_blokzincir_denetim(store)
        except Exception as _e:
            st.error(f"Denetim Zinciri yuklenemedi: {_e}")
    with tabs[21]:
        try:
            from views._tdm_final_features import render_iot_ekosistem
            render_iot_ekosistem(store)
        except Exception as _e:
            st.error(f"IoT Ekosistem yuklenemedi: {_e}")
    with tabs[22]:
        try:
            from views._tdm_final_features import render_varlik_akademi
            render_varlik_akademi(store)
        except Exception as _e:
            st.error(f"Varlik Akademi yuklenemedi: {_e}")
    with tabs[23]:
        _render_ayarlar(store)
    with tabs[24]:
        def _tdm_data_context():
            try:
                demirbaslar = store.load_objects("demirbaslar")
                tuketim_urunleri = store.load_objects("tuketim_urunleri")
                siparisler = store.load_objects("siparis_takipleri")
                return (
                    f"Toplam demirbas sayisi: {len(demirbaslar)}\n"
                    f"Toplam tuketim urunu sayisi: {len(tuketim_urunleri)}\n"
                    f"Toplam siparis sayisi: {len(siparisler)}"
                )
            except Exception:
                return ""
        render_smarti_chat("tuketim_demirbas", _tdm_data_context)
