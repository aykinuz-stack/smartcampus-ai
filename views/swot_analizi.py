"""
SWI-01 SWOT Analizi Modulu - Streamlit UI
==========================================
Olcum yonetimi, anonim SWOT girisi, dashboard, raporlar, aksiyon plani.
"""
from __future__ import annotations

import csv
import io
import os
import uuid
from datetime import datetime, date, timedelta
from typing import Any

import streamlit as st
import pandas as pd

from utils.tenant import get_tenant_dir
from utils.auth import AuthManager
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("kurumsal_org")
except Exception:
    pass
from models.swot_analizi import (
    SwotDataStore, SwotOlcum, SwotMadde, SwotAksiyon,
    SwotAltKategori, SwotKademe, SwotAyar,
    SWOT_TURLERI, SWOT_TUR_ADLARI, SWOT_TUR_RENKLER, SWOT_TUR_IKONLAR,
    OLCUM_DURUMLARI, AKSIYON_DURUMLARI, SKOR_ESIKLERI,
    VARSAYILAN_ALT_KATEGORILER, VARSAYILAN_KADEMELER,
    _now, _today,
)


# ============================================================
# STORE FACTORY
# ============================================================

def _get_swot_store() -> SwotDataStore:
    base = os.path.join(get_tenant_dir(), "swot")
    store = SwotDataStore(base)
    store.seed_defaults()
    return store


# ============================================================
# CSS ENJEKSIYON
# ============================================================

def _inject_css():
    """Modul icin premium CSS enjekte et."""
    inject_common_css("swot")


# ============================================================
# ALT SEKME 1: DASHBOARD
# ============================================================

def _render_dashboard(store: SwotDataStore):
    styled_header("SWOT Dashboard", "Güncel olcum ozeti ve analizler", icon="📊")

    aktif = store.get_aktif_olcum()
    son = store.get_son_kilitli_olcum()

    hedef = aktif or son
    if not hedef:
        styled_info_banner("Henuz hicbir olcum yapilmadi. 'Olcum Yönetimi' sekmesinden yeni olcum olusturun.", banner_type="info", icon="📋")
        return

    durum_renk = "#10b981" if hedef.durum == "Açık" else "#ef4444" if hedef.durum == "Kilitli" else "#f59e0b"
    styled_info_banner(
        f"<b>{hedef.olcum_adi}</b> | Durum: <b style='color:{durum_renk}'>{hedef.durum}</b> | "
        f"Başlangıç: {hedef.baslangic} | Bitis: {hedef.bitis or '-'}", banner_type="info", icon="📊")

    ist = store.olcum_istatistik(hedef.id)

    styled_stat_row([
        ("Toplam Girdi", str(ist["toplam_girdi"]), "#2563eb", "📝"),
        ("Katilimci", str(ist["toplam_katilimci"]), "#8b5cf6", "👥"),
        ("Kirmizi", str(ist["kirmizi_sayisi"]), "#ef4444", "🔴"),
        ("Turuncu", str(ist["turuncu_sayisi"]), "#f59e0b", "🟠"),
    ])

    from utils.report_utils import ReportStyler

    # Tur dagilimi
    col_a, col_b = st.columns(2)
    with col_a:
        tur_data = {SWOT_TUR_ADLARI[k]: float(v) for k, v in ist["tur_dagilimi"].items() if v > 0}
        if tur_data:
            styled_section("S/W/O/T Dagilimi")
            st.markdown(
                ReportStyler.sunburst_chart_svg(tur_data, title="SWOT Tur Dagilimi"),
                unsafe_allow_html=True,
            )

    with col_b:
        if ist["kategori_dagilimi"]:
            styled_section("Alt Kategori Yogunlugu")
            sorted_kat = dict(sorted(ist["kategori_dagilimi"].items(), key=lambda x: x[1], reverse=True))
            st.markdown(
                ReportStyler.horizontal_bar_html(
                    {k: float(v) for k, v in sorted_kat.items()}, "#4472C4"
                ),
                unsafe_allow_html=True,
            )

    # Kademe dagilimi
    col_c, col_d = st.columns(2)
    with col_c:
        if ist["kademe_dagilimi"]:
            styled_section("Kademe Dagilimi")
            st.markdown(
                ReportStyler.sunburst_chart_svg(
                    {k: float(v) for k, v in ist["kademe_dagilimi"].items() if v > 0},
                    title="Kademe Dagilimi",
                ),
                unsafe_allow_html=True,
            )

    with col_d:
        styled_section("Top 10 (Yuksek Skor)")
        top = store.top_maddeler(hedef.id, 10)
        if top:
            rows = []
            for i, m in enumerate(top, 1):
                rows.append({
                    "Sira": i,
                    "Tur": f"{SWOT_TUR_IKONLAR[m.tur]} {SWOT_TUR_ADLARI[m.tur]}",
                    "Başlık": m.baslik[:60],
                    "Kategori": m.alt_kategori,
                    "Skor": m.skor,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.caption("Henuz veri yok.")

    # Kademe bazli kirilim
    kademeler = store.get_kademeler()
    if kademeler and ist["toplam_girdi"] > 0:
        styled_section("Kademe Bazli Kirilim")
        maddeler = store.olcum_maddeler(hedef.id)
        kad_tabs = st.tabs(kademeler)
        for kt, kad in zip(kad_tabs, kademeler):
            with kt:
                kad_m = [m for m in maddeler if m.kademe == kad]
                if not kad_m:
                    st.caption(f"{kad} için veri yok.")
                    continue
                st.metric("Girdi Sayısı", len(kad_m))
                tur_d = {}
                for m in kad_m:
                    tur_d[SWOT_TUR_ADLARI[m.tur]] = tur_d.get(SWOT_TUR_ADLARI[m.tur], 0) + 1
                if tur_d:
                    st.markdown(
                        ReportStyler.horizontal_bar_html(
                            {k: float(v) for k, v in tur_d.items()}, "#4472C4"
                        ),
                        unsafe_allow_html=True,
                    )
                kad_top = sorted(kad_m, key=lambda x: x.skor, reverse=True)[:5]
                rows2 = [{
                    "Tur": SWOT_TUR_ADLARI[m.tur],
                    "Başlık": m.baslik[:60],
                    "Skor": m.skor,
                } for m in kad_top]
                if rows2:
                    st.dataframe(pd.DataFrame(rows2), use_container_width=True, hide_index=True)


# ============================================================
# ALT SEKME 2: OLCUM YONETIMI
# ============================================================

def _render_olcum_yonetimi(store: SwotDataStore):
    styled_section("Olcum Yönetimi", "#2563eb")

    aktif = store.get_aktif_olcum()

    if aktif:
        styled_info_banner(
            f"Aktif Olcum: <b>{aktif.olcum_adi}</b> | "
            f"Başlangıç: {aktif.baslangic} | Bitis: {aktif.bitis or '-'}", banner_type="success", icon="🟢")

        if st.button("Olcumu Kapat ve Kilitle", type="primary", key="swot_kapat_btn"):
            aktif.durum = "Kilitli"
            aktif.updated_at = _now()
            # Istatistik guncelle
            ist = store.olcum_istatistik(aktif.id)
            aktif.toplam_katilimci = ist["toplam_katilimci"]
            aktif.toplam_girdi = ist["toplam_girdi"]
            store.upsert("olcumler", aktif)
            st.success("Olcum kilitlendi! Artik yeni giris yapilamaz.")
            st.rerun()
    else:
        styled_info_banner("Su anda aktif olcum yok. Asagidan yeni olcum olusturabilirsiniz.", banner_type="info", icon="📋")

    # Yeni olcum formu
    styled_section("Yeni Olcum Oluştur", "#10b981")
    with st.form("swot_yeni_olcum", clear_on_submit=True):
        k1, k2 = st.columns(2)
        with k1:
            olcum_adi = st.selectbox(
                "Donem Sec *",
                ["1. Donem", "2. Donem", "Tüm Yil"],
                key="swot_donem_adi_sec",
            )
        with k2:
            sure_gun = int(store.get_ayar("measurement_default_duration_days", "3"))
            olcum_sure = st.number_input("Sure (gun)", min_value=1, max_value=30,
                                          value=sure_gun, key="swot_sure")

        k3, k4 = st.columns(2)
        with k3:
            olcum_bas = st.date_input("Başlangıç Tarihi", value=date.today(), key="swot_bas")
        with k4:
            olcum_bit = st.date_input("Bitis Tarihi",
                                       value=date.today() + timedelta(days=sure_gun),
                                       key="swot_bit")

        kademeler = store.get_kademeler()
        kapsam = st.multiselect("Kapsam Kademeler", kademeler, default=kademeler,
                                 key="swot_kapsam")
        olcum_aciklama = st.text_area("Açıklama", key="swot_aciklama",
                                       placeholder="Olcum hakkinda kisa bilgi...")

        if st.form_submit_button("Olcum Oluştur ve Ac", type="primary"):
            if not olcum_adi:
                st.error("Olcum adi zorunludur.")
            elif aktif:
                st.error("Zaten aktif bir olcum var. Önce mevcut olcumu kapatin.")
            else:
                auth_user = AuthManager.get_current_user()
                yeni = SwotOlcum(
                    olcum_adi=olcum_adi,
                    aciklama=olcum_aciklama,
                    durum="Açık",
                    baslangic=olcum_bas.isoformat(),
                    bitis=f"{olcum_bit.isoformat()} 23:59:59",
                    kapsam_kademeler=kapsam,
                    olusturan=auth_user.get("name", ""),
                )
                store.upsert("olcumler", yeni)
                st.success(f"'{olcum_adi}' olcumu oluşturuldu ve acildi!")
                st.rerun()

    # Gecmis olcumler
    styled_section("Geçmiş Olcumler", "#64748b")
    olcumler = store.load_objects("olcumler")
    olcumler.sort(key=lambda x: x.created_at, reverse=True)
    for o in olcumler:
        d_renk = {"Açık": "#10b981", "Kilitli": "#ef4444", "Kapali": "#f59e0b", "Taslak": "#94a3b8"}.get(o.durum, "#64748b")
        st.markdown(
            f'<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;'
            f'padding:12px 16px;margin:6px 0;">'
            f'<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">'
            f'<span style="font-weight:700;color:#94A3B8;font-size:14px;">{o.olcum_adi}</span>'
            f'<span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;'
            f'border-radius:8px;font-size:11px;font-weight:600;">{o.durum}</span>'
            f'<span style="color:#64748b;font-size:12px;">{o.baslangic} - {o.bitis or "-"}</span>'
            f'<span style="color:#64748b;font-size:12px;">Girdi: {o.toplam_girdi} | '
            f'Katilimci: {o.toplam_katilimci}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )


# ============================================================
# ALT SEKME 3: SWOT GIRISI (ANONIM)
# ============================================================

def _render_swot_girisi(store: SwotDataStore):
    styled_section("SWOT Girişi", "#3b82f6")

    # Rol kontrolu: sadece ic paydaslar (Veli ve Ogrenci haric)
    auth_user = AuthManager.get_current_user()
    kullanici_rol = auth_user.get("role", "")
    if kullanici_rol in ("Veli", "Öğrenci"):
        styled_info_banner(
            "SWOT girisi yalnizca ic paydaslara (Yonetici, Öğretmen, Çalışan) aciktir.",
            "#ef4444", "🔒"
        )
        return

    aktif = store.get_aktif_olcum()
    if not aktif:
        styled_info_banner(
            "Su anda aktif olcum yok. Giriş yapmak için bir olcumun acik olmasi gerekir.", banner_type="error", icon="🔒")
        return

    styled_info_banner(
        f"Aktif Olcum: <b>{aktif.olcum_adi}</b> | "
        f"Kalan sure: {aktif.bitis or 'Belirsiz'}", banner_type="success", icon="🟢")

    st.markdown(
        '<div style="background:#fffbeb;border:1px solid #fbbf2440;border-radius:10px;'
        'padding:10px 14px;margin:8px 0;font-size:13px;color:#92400e;">'
        'Girişleriniz <b>anonim</b> olarak kaydedilir. Isminiz raporlarda gorunmez.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Anonim token: oturum bazli (ayni oturumda birlestirme icin)
    if "swot_anonim_token" not in st.session_state:
        st.session_state["swot_anonim_token"] = uuid.uuid4().hex[:12]
    anonim_token = st.session_state["swot_anonim_token"]

    kategoriler = store.get_alt_kategoriler()
    kademeler = store.get_kademeler()
    kapsam = aktif.kapsam_kademeler or kademeler

    # Mevcut girislerim
    mevcut = [m for m in store.olcum_maddeler(aktif.id) if m.anonim_token == anonim_token]

    # --- SWOT Tur / Kademe / Kategori secimi ---
    st.markdown("**Yeni SWOT Maddesi Ekle**")

    g1, g2 = st.columns(2)
    with g1:
        tur = st.selectbox(
            "Tur *",
            SWOT_TURLERI,
            format_func=lambda x: f"{SWOT_TUR_IKONLAR[x]} {SWOT_TUR_ADLARI[x]}",
            key="swot_tur",
        )
    with g2:
        alt_kat = st.selectbox("Alt Kategori *", kategoriler, key="swot_altkat")

    g3, g4 = st.columns(2)
    with g3:
        kademe = st.selectbox("Kademe *", kapsam, key="swot_kademe")
    with g4:
        pass

    # --- Kullanici Kilavuzu ---
    _SWOT_KILAVUZ = {
        "S": {
            "baslik": "Güçlü Yonler (Strengths)",
            "aciklama": "Kurumun ic kaynaklarindan dogan ustunlukler, avantajlar ve basarili yonler.",
            "ornekler": [
                "Deneyimli ve nitelikli ogretmen kadrosu",
                "Güçlü akademik basari gecmisi",
                "Modern egitim teknolojileri altyapisi",
                "Etkili liderlik ve yonetim yapisi",
                "Güçlü veli-okul isbirligi",
                "Zengin sosyal etkinlik programi",
                "Yuksek ogrenci memnuniyeti",
                "Finansal istikrar ve kaynak yeterliligi",
                "Etkili rehberlik ve psikolojik danismanlik",
                "Başarılı spor ve kultur takimlari",
                "Iyi planlanmis mufredat ve ogretim programi",
                "Dusuk personel devir orani",
            ],
        },
        "W": {
            "baslik": "Zayif Yonler (Weaknesses)",
            "aciklama": "Kurumun ic kaynaklarindaki eksiklikler, gelisime acik alanlar.",
            "ornekler": [
                "Fiziki alan ve sinif kapasitesi yetersizligi",
                "Teknoloji entegrasyonunda eksiklikler",
                "Öğretmen mesleki gelisim firsatlarinin azligi",
                "Öğrenci basarisinda siniflar arasi dengesizlik",
                "İletişim ve bilgi akisindaki aksakliklar",
                "Kutuphane ve laboratuvar kaynaklarinin yetersizligi",
                "Ölçme degerlendirme sistemindeki eksiklikler",
                "Burs ve mali destek imkanlarinin sinirli olmasi",
                "Yabanci dil egitiminde yetersizlik",
                "Özel egitim ihtiyaci olan ogrencilere destek eksikligi",
                "Velilerin okul sureclerine katilim dusuk",
                "Dijital icerik ve materyal yetersizligi",
            ],
        },
        "O": {
            "baslik": "Firsatlar (Opportunities)",
            "aciklama": "Dis cevreden kaynaklanan, kuruma avantaj saglayabilecek gelismeler.",
            "ornekler": [
                "Yeni egitim teknolojileri ve dijital donusum",
                "MEB destek programlari ve hibe firsatlari",
                "Uluslararasi isbirligi ve degisim programlari",
                "Uzaktan/hibrit egitim modellerinin yayginlasmasi",
                "Yerel isletmelerle staj ve isbirligi olanaklari",
                "Bolgede nufus artisi ve kayit potansiyeli",
                "STEM/STEAM egitim trendinin guclu talep gormesi",
                "Sosyal medya ile marka bilinirligini artirma",
                "Devlet tesvik ve vergi avantajlari",
                "Mezunlar agi ile guclenen kurum itibari",
                "Yeni mufredat degisiklikleri ve esneklik",
                "Toplumsal duyarlilik projelerinde liderlik firsati",
            ],
        },
        "T": {
            "baslik": "Tehditler (Threats)",
            "aciklama": "Dis cevreden kaynaklanan, kurumu olumsuz etkileyebilecek riskler.",
            "ornekler": [
                "Rekabet eden okullarin artmasi",
                "Ekonomik belirsizlik ve enflasyon etkisi",
                "Mevzuat ve yonetmelik degisiklikleri",
                "Nitelikli ogretmen bulma guclugu",
                "Teknolojik degisime uyum saglamada gecikmeler",
                "Öğrenci guvenligine yonelik artan riskler",
                "Veli beklentilerindeki hizli degisim",
                "Dogal afet ve salgin riskleri",
                "Sosyal medyada olumsuz alginin hizli yayilmasi",
                "Devlet politikalarindaki belirsizlikler",
                "Demografik degisim ve ogrenci sayisinda azalma",
                "Siber guvenlik tehditleri ve veri guvenligi riskleri",
            ],
        },
    }

    kilavuz = _SWOT_KILAVUZ.get(tur, {})
    if kilavuz:
        with st.expander(f"Kullanıcı Kilavuzu: {kilavuz['baslik']}", expanded=False):
            st.markdown(f"**{kilavuz['aciklama']}**")
            st.markdown("---")
            st.markdown("**Ornek Maddeler** *(bunlardan ilham alin veya kendi ifadenizi yazin):*")
            for i, ornek in enumerate(kilavuz["ornekler"], 1):
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;padding:3px 0;">'
                    f'<span style="background:{SWOT_TUR_RENKLER[tur]};color:#fff;width:20px;height:20px;'
                    f'border-radius:50%;display:inline-flex;align-items:center;justify-content:center;'
                    f'font-size:10px;font-weight:700;flex-shrink:0;">{i}</span>'
                    f'<span style="font-size:13px;color:#334155;">{ornek}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("**Puanlama** (1 = en dusuk, 5 = en yuksek)")
    p1, p2, p3 = st.columns(3)
    with p1:
        etki = st.slider("Etki", 1, 5, 3, key="swot_etki")
    with p2:
        olasilik = st.slider("Olasilik", 1, 5, 3, key="swot_olasilik")
    with p3:
        aciliyet = st.slider("Aciliyet", 1, 5, 3, key="swot_aciliyet")

    skor_preview = etki * olasilik * aciliyet
    skor_renk = "#ef4444" if skor_preview >= 60 else "#f59e0b" if skor_preview >= 40 else "#10b981"
    st.markdown(
        f'<div style="text-align:center;margin:8px 0;">'
        f'<span style="font-size:1.5rem;font-weight:800;color:{skor_renk};">'
        f'Skor: {skor_preview}</span>'
        f' <span style="font-size:0.8rem;color:#64748b;">(Etki x Olasilik x Aciliyet)</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # --- Madde madde ekleme ---
    st.markdown("---")
    st.markdown(
        f'<div style="background:{SWOT_TUR_RENKLER[tur]}10;border-left:4px solid {SWOT_TUR_RENKLER[tur]};'
        f'padding:10px 14px;border-radius:0 8px 8px 0;margin:6px 0;">'
        f'<b>{SWOT_TUR_IKONLAR[tur]} {SWOT_TUR_ADLARI[tur]}</b> maddelerini tek tek yazin ve Ekle butonuna basin.'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Session state ile gecici madde listesi
    _ss_key = f"swot_maddeler_{tur}_{alt_kat}_{kademe}"
    if _ss_key not in st.session_state:
        st.session_state[_ss_key] = []

    mc1, mc2 = st.columns([4, 1])
    with mc1:
        yeni_madde = st.text_input(
            "Madde yazin *", key="swot_yeni_madde",
            placeholder="Ornek: Deneyimli ogretmen kadrosu",
        )
    with mc2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        ekle_btn = st.button("Ekle", key="swot_madde_ekle_btn", type="primary", use_container_width=True)

    if ekle_btn and yeni_madde:
        st.session_state[_ss_key].append(yeni_madde.strip())
        st.rerun()

    # Eklenmis maddeleri goster
    gecici_maddeler = st.session_state.get(_ss_key, [])
    if gecici_maddeler:
        st.markdown(
            f'<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;'
            f'padding:12px 16px;margin:8px 0;">'
            f'<div style="font-weight:700;color:#334155;margin-bottom:8px;font-size:13px;">'
            f'{SWOT_TUR_IKONLAR[tur]} Eklenen Maddeler ({len(gecici_maddeler)})</div>',
            unsafe_allow_html=True,
        )
        for idx, md in enumerate(gecici_maddeler, 1):
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;padding:4px 0;">'
                f'<span style="background:{SWOT_TUR_RENKLER[tur]};color:#fff;width:22px;height:22px;'
                f'border-radius:50%;display:inline-flex;align-items:center;justify-content:center;'
                f'font-size:11px;font-weight:700;">{idx}</span>'
                f'<span style="font-size:13px;color:#94A3B8;">{md}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Sil ve Kaydet butonlari
        sc1, sc2, sc3 = st.columns([1, 1, 2])
        with sc1:
            if st.button("Tümü Kaydet", key="swot_toplu_kaydet", type="primary", use_container_width=True):
                kayit_sayisi = 0
                for md_text in gecici_maddeler:
                    madde = SwotMadde(
                        olcum_id=aktif.id,
                        tur=tur,
                        alt_kategori=alt_kat,
                        kademe=kademe,
                        baslik=md_text,
                        aciklama="",
                        etki=etki,
                        olasilik=olasilik,
                        aciliyet=aciliyet,
                        anonim_token=anonim_token,
                    )
                    store.upsert("maddeler", madde)
                    kayit_sayisi += 1
                st.session_state[_ss_key] = []
                st.success(f"{SWOT_TUR_IKONLAR[tur]} {kayit_sayisi} madde kaydedildi!")
                st.rerun()
        with sc2:
            if st.button("Listeyi Temizle", key="swot_temizle", type="secondary", use_container_width=True):
                st.session_state[_ss_key] = []
                st.rerun()
        with sc3:
            # Son maddeyi sil
            if st.button("Son Maddeyi Sil", key="swot_son_sil"):
                if st.session_state[_ss_key]:
                    st.session_state[_ss_key].pop()
                    st.rerun()

    # Benim girislerim
    if mevcut:
        styled_section(f"Girişlerim ({len(mevcut)})", "#8b5cf6")
        for m in sorted(mevcut, key=lambda x: x.created_at, reverse=True):
            s_renk = m.skor_renk
            st.markdown(
                f'<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;'
                f'padding:10px 14px;margin:4px 0;">'
                f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
                f'<span style="font-size:1.1rem">{SWOT_TUR_IKONLAR[m.tur]}</span>'
                f'<span style="font-weight:600;color:#94A3B8;font-size:13px;">{m.baslik}</span>'
                f'<span style="background:{SWOT_TUR_RENKLER[m.tur]}20;'
                f'color:{SWOT_TUR_RENKLER[m.tur]};padding:2px 6px;border-radius:6px;'
                f'font-size:11px;font-weight:600;">{SWOT_TUR_ADLARI[m.tur]}</span>'
                f'<span style="background:{s_renk}20;color:{s_renk};padding:2px 6px;'
                f'border-radius:6px;font-size:11px;font-weight:600;">Skor: {m.skor}</span>'
                f'<span style="color:#94a3b8;font-size:11px;">{m.alt_kategori} | {m.kademe}</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
            if st.button("Sil", key=f"swot_sil_{m.id}", type="secondary"):
                store.delete_by_id("maddeler", m.id)
                st.rerun()


# ============================================================
# ALT SEKME 4: SONUCLAR & RAPORLAR
# ============================================================

def _render_sonuclar(store: SwotDataStore):
    styled_section("Sonuclar & Raporlar", "#8b5cf6")

    # Olcum secimi
    olcumler = store.load_objects("olcumler")
    kilitli = [o for o in olcumler if o.durum in ("Kilitli", "Kapali")]
    kilitli.sort(key=lambda x: x.created_at, reverse=True)

    if not kilitli:
        aktif = store.get_aktif_olcum()
        if aktif:
            styled_info_banner(
                "Aktif olcum henuz devam ediyor. Raporlar olcum kilitlendikten sonra kullanilabilir.", banner_type="warning", icon="⏳")
        else:
            styled_info_banner("Henuz tamamlanmis olcum yok.", banner_type="info", icon="📋")
        return

    secenekler = {f"{o.olcum_adi} ({o.baslangic})": o.id for o in kilitli}
    secim = st.selectbox("Olcum Sec", list(secenekler.keys()), key="swot_rapor_olcum")
    olcum_id = secenekler[secim]
    olcum = store.get_by_id("olcumler", olcum_id)

    ist = store.olcum_istatistik(olcum_id)
    maddeler = store.olcum_maddeler(olcum_id)

    styled_stat_row([
        ("Toplam Girdi", str(ist["toplam_girdi"]), "#2563eb", "📝"),
        ("Katilimci", str(ist["toplam_katilimci"]), "#8b5cf6", "👥"),
        ("Ort. Skor", f"{ist['ort_skor']:.1f}", "#3b82f6", "📊"),
        ("Kirmizi", str(ist["kirmizi_sayisi"]), "#ef4444", "🔴"),
    ])

    from utils.report_utils import ReportStyler

    r_tabs = st.tabs(["📊 Genel Analiz", "📋 Detay Listesi", "🔍 Filtrele", "📥 PDF Rapor"])

    # -- Genel Analiz --
    with r_tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            tur_data = {SWOT_TUR_ADLARI[k]: float(v) for k, v in ist["tur_dagilimi"].items() if v > 0}
            if tur_data:
                styled_section("S/W/O/T Dagilimi")
                st.markdown(
                    ReportStyler.sunburst_chart_svg(tur_data, title="SWOT Dagilimi"),
                    unsafe_allow_html=True,
                )
        with col2:
            if ist["kategori_dagilimi"]:
                styled_section("Kategori Yogunlugu")
                st.markdown(
                    ReportStyler.horizontal_bar_html(
                        dict(sorted(
                            {k: float(v) for k, v in ist["kategori_dagilimi"].items()}.items(),
                            key=lambda x: x[1], reverse=True,
                        )),
                        "#4472C4",
                    ),
                    unsafe_allow_html=True,
                )

        # Top 10 her tur icin
        for tur_kodu in SWOT_TURLERI:
            top = store.top_maddeler(olcum_id, 5, tur=tur_kodu)
            if top:
                styled_section(
                    f"{SWOT_TUR_IKONLAR[tur_kodu]} Top 5 {SWOT_TUR_ADLARI[tur_kodu]}",
                    SWOT_TUR_RENKLER[tur_kodu],
                )
                rows = [{
                    "Sira": i,
                    "Başlık": m.baslik[:80],
                    "Kategori": m.alt_kategori,
                    "Kademe": m.kademe,
                    "Skor": m.skor,
                } for i, m in enumerate(top, 1)]
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # -- Detay Listesi --
    with r_tabs[1]:
        styled_section("Tüm Maddeler (Skor Sirasina Gore)")
        if maddeler:
            skor_sirali = sorted(maddeler, key=lambda x: x.skor, reverse=True)
            rows = [{
                "Tur": f"{SWOT_TUR_IKONLAR[m.tur]} {SWOT_TUR_ADLARI[m.tur]}",
                "Başlık": m.baslik,
                "Kategori": m.alt_kategori,
                "Kademe": m.kademe,
                "Etki": m.etki,
                "Olasilik": m.olasilik,
                "Aciliyet": m.aciliyet,
                "Skor": m.skor,
                "Öncelik": m.skor_etiket,
            } for m in skor_sirali]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.caption("Veri yok.")

    # -- Filtrele --
    with r_tabs[2]:
        styled_section("Filtreli Görüntülem")
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            f_tur = st.multiselect("Tur", SWOT_TURLERI,
                                     format_func=lambda x: SWOT_TUR_ADLARI[x],
                                     key="swot_f_tur")
        with f2:
            f_kat = st.multiselect("Kategori", store.get_alt_kategoriler(),
                                     key="swot_f_kat")
        with f3:
            f_kad = st.multiselect("Kademe", store.get_kademeler(), key="swot_f_kad")
        with f4:
            f_skor = st.slider("Min Skor", 1, 125, 1, key="swot_f_skor")

        filtreli = maddeler
        if f_tur:
            filtreli = [m for m in filtreli if m.tur in f_tur]
        if f_kat:
            filtreli = [m for m in filtreli if m.alt_kategori in f_kat]
        if f_kad:
            filtreli = [m for m in filtreli if m.kademe in f_kad]
        filtreli = [m for m in filtreli if m.skor >= f_skor]
        filtreli.sort(key=lambda x: x.skor, reverse=True)

        st.metric("Sonuc", len(filtreli))
        if filtreli:
            rows = [{
                "Tur": SWOT_TUR_ADLARI[m.tur],
                "Başlık": m.baslik,
                "Kategori": m.alt_kategori,
                "Kademe": m.kademe,
                "Skor": m.skor,
                "Öncelik": m.skor_etiket,
            } for m in filtreli]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            # Filtreli sonuc grafikleri
            col_fg, col_fk = st.columns(2)
            with col_fg:
                f_tur_dag = {}
                for m in filtreli:
                    f_tur_dag[SWOT_TUR_ADLARI[m.tur]] = f_tur_dag.get(SWOT_TUR_ADLARI[m.tur], 0) + 1
                if f_tur_dag:
                    st.markdown(
                        ReportStyler.sunburst_chart_svg(
                            {k: float(v) for k, v in f_tur_dag.items()},
                            title="Filtreli Tur Dagilimi",
                        ),
                        unsafe_allow_html=True,
                    )
            with col_fk:
                f_kat_dag = {}
                for m in filtreli:
                    f_kat_dag[m.alt_kategori] = f_kat_dag.get(m.alt_kategori, 0) + 1
                if f_kat_dag:
                    st.markdown(
                        ReportStyler.horizontal_bar_html(
                            dict(sorted({k: float(v) for k, v in f_kat_dag.items()}.items(),
                                        key=lambda x: x[1], reverse=True)),
                            "#ED7D31",
                        ),
                        unsafe_allow_html=True,
                    )

    # -- PDF Rapor --
    with r_tabs[3]:
        styled_section("PDF Rapor Oluştur")
        if st.button("SWOT Rapor PDF Oluştur", type="primary", key="swot_pdf_btn"):
            try:
                from utils.report_utils import ReportPDFGenerator, get_institution_info

                pdf = ReportPDFGenerator(
                    "SWOT Analiz Raporu",
                    f"{olcum.olcum_adi} | {olcum.baslangic} - {olcum.bitis or ''}",
                )
                info = get_institution_info()
                pdf.add_header(kurum_adi=info.get("name", ""))

                # Ozet
                pdf.add_section("Genel Özet")
                pdf.add_metrics([
                    ("Toplam Girdi", ist["toplam_girdi"], "#2563eb"),
                    ("Katilimci", ist["toplam_katilimci"], "#8b5cf6"),
                    ("Ort. Skor", f"{ist['ort_skor']:.1f}", "#3b82f6"),
                    ("Kirmizi Madde", ist["kirmizi_sayisi"], "#ef4444"),
                ])

                # Tur dagilimi
                tur_df = pd.DataFrame([
                    {"Tur": SWOT_TUR_ADLARI[k], "Adet": v}
                    for k, v in ist["tur_dagilimi"].items() if v > 0
                ])
                if not tur_df.empty:
                    pdf.add_section("S/W/O/T Dagilimi")
                    pdf.add_table(tur_df)
                    pdf.add_bar_chart(
                        {SWOT_TUR_ADLARI[k]: float(v) for k, v in ist["tur_dagilimi"].items() if v > 0},
                        "Tur Dagilimi", "#2563eb",
                    )

                # Kategori dagilimi
                if ist["kategori_dagilimi"]:
                    pdf.add_section("Alt Kategori Dagilimi")
                    kat_df = pd.DataFrame([
                        {"Kategori": k, "Adet": v}
                        for k, v in sorted(ist["kategori_dagilimi"].items(), key=lambda x: x[1], reverse=True)
                    ])
                    pdf.add_table(kat_df)
                    pdf.add_bar_chart(
                        {k: float(v) for k, v in ist["kategori_dagilimi"].items()},
                        "Kategori Yogunlugu", "#4472C4",
                    )

                # Top 10
                top_all = store.top_maddeler(olcum_id, 10)
                if top_all:
                    pdf.add_section("Top 10 Yuksek Öncelikli Maddeler")
                    top_df = pd.DataFrame([{
                        "Sira": i, "Tur": SWOT_TUR_ADLARI[m.tur],
                        "Başlık": m.baslik[:80], "Kategori": m.alt_kategori,
                        "Kademe": m.kademe, "Skor": m.skor,
                    } for i, m in enumerate(top_all, 1)])
                    pdf.add_table(top_df)

                # Tur bazli top 5
                for tur_kodu in SWOT_TURLERI:
                    top_t = store.top_maddeler(olcum_id, 5, tur=tur_kodu)
                    if top_t:
                        pdf.add_section(f"Top 5 {SWOT_TUR_ADLARI[tur_kodu]}")
                        t_df = pd.DataFrame([{
                            "Başlık": m.baslik[:80], "Kategori": m.alt_kategori,
                            "Kademe": m.kademe, "Skor": m.skor,
                        } for m in top_t])
                        pdf.add_table(t_df)

                # Aksiyon plani
                aksiyonlar = store.olcum_aksiyonlar(olcum_id)
                if aksiyonlar:
                    pdf.add_section("Aksiyon Plani")
                    ak_df = pd.DataFrame([{
                        "Madde": a.madde_baslik[:60],
                        "Aksiyon": a.aksiyon_baslik[:60],
                        "Sorumlu": a.sorumlu,
                        "Termin": a.termin_tarihi,
                        "Durum": a.durum,
                    } for a in aksiyonlar])
                    pdf.add_table(ak_df)

                pdf_bytes = pdf.generate()
                st.download_button(
                    "PDF Indir", pdf_bytes,
                    file_name=f"swot_rapor_{olcum.olcum_adi.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.success("PDF oluşturuldu!")
            except Exception as e:
                st.error(f"PDF olusturma hatasi: {e}")


# ============================================================
# ALT SEKME 5: AKSIYON PLANI
# ============================================================

def _render_aksiyon_plani(store: SwotDataStore):
    styled_section("Aksiyon Plani", "#ef4444")

    olcumler = store.load_objects("olcumler")
    tamamlanan = [o for o in olcumler if o.durum in ("Kilitli", "Kapali")]
    tamamlanan.sort(key=lambda x: x.created_at, reverse=True)

    if not tamamlanan:
        styled_info_banner("Henuz tamamlanmis olcum yok.", banner_type="info", icon="📋")
        return

    secenekler = {f"{o.olcum_adi} ({o.baslangic})": o.id for o in tamamlanan}
    secim = st.selectbox("Olcum", list(secenekler.keys()), key="swot_aksiyon_olcum")
    olcum_id = secenekler[secim]

    # Kirmizi maddeler
    maddeler = store.olcum_maddeler(olcum_id)
    kirmizi = [m for m in maddeler if m.skor >= SKOR_ESIKLERI["kirmizi"]]
    kirmizi.sort(key=lambda x: x.skor, reverse=True)

    aksiyonlar = store.olcum_aksiyonlar(olcum_id)
    aksiyon_madde_ids = {a.madde_id for a in aksiyonlar}

    styled_stat_row([
        ("Kirmizi Madde", str(len(kirmizi)), "#ef4444", "🔴"),
        ("Aksiyon Tanimli", str(len(aksiyonlar)), "#10b981", "✅"),
        ("Aksiyonsuz", str(len(kirmizi) - len(aksiyon_madde_ids & {m.id for m in kirmizi})), "#f59e0b", "⚠️"),
    ])

    # Aksiyon tablosu
    if aksiyonlar:
        styled_section("Mevcut Aksiyonlar")
        for a in aksiyonlar:
            d_renk = {"Açık": "#ef4444", "Devam Ediyor": "#f59e0b", "Tamamlandı": "#10b981", "Iptal": "#64748b"}.get(a.durum, "#64748b")
            st.markdown(
                f'<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;'
                f'padding:10px 14px;margin:4px 0;">'
                f'<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
                f'<span style="font-weight:600;color:#94A3B8;font-size:13px;">{a.aksiyon_baslik}</span>'
                f'<span style="background:{d_renk}20;color:{d_renk};padding:2px 6px;'
                f'border-radius:6px;font-size:11px;font-weight:600;">{a.durum}</span>'
                f'<span style="color:#64748b;font-size:11px;">Sorumlu: {a.sorumlu or "-"} | '
                f'Termin: {a.termin_tarihi or "-"}</span>'
                f'</div>'
                f'<div style="color:#94a3b8;font-size:11px;margin-top:4px;">Madde: {a.madde_baslik[:80]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            with st.expander(f"Durum Güncelle: {a.aksiyon_baslik[:40]}"):
                yeni_durum = st.selectbox("Durum", AKSIYON_DURUMLARI,
                                           index=AKSIYON_DURUMLARI.index(a.durum) if a.durum in AKSIYON_DURUMLARI else 0,
                                           key=f"swot_ak_durum_{a.id}")
                yeni_not = st.text_input("Not", value=a.notlar, key=f"swot_ak_not_{a.id}")
                if st.button("Güncelle", key=f"swot_ak_gun_{a.id}"):
                    a.durum = yeni_durum
                    a.notlar = yeni_not
                    a.updated_at = _now()
                    store.upsert("aksiyonlar", a)
                    st.success("Aksiyon güncellendi!")
                    st.rerun()

    # Yeni aksiyon ekle
    styled_section("Yeni Aksiyon Ekle", "#10b981")
    aksiyonsuz = [m for m in kirmizi if m.id not in aksiyon_madde_ids]

    if not aksiyonsuz:
        if kirmizi:
            styled_info_banner("Tüm kirmizi maddeler için aksiyon tanimlanmis.", banner_type="success", icon="✅")
        else:
            styled_info_banner("Kirmizi madde bulunmuyor.", banner_type="info", icon="📋")
        return

    madde_sec = {f"[{m.skor}] {SWOT_TUR_ADLARI[m.tur]}: {m.baslik[:60]}": m for m in aksiyonsuz}
    secili_label = st.selectbox("Madde Sec", list(madde_sec.keys()), key="swot_ak_madde")
    secili_madde = madde_sec[secili_label]

    with st.form("swot_yeni_aksiyon", clear_on_submit=True):
        ak_baslik = st.text_input("Aksiyon Başlığı *", key="swot_ak_baslik")
        ak1, ak2 = st.columns(2)
        with ak1:
            ak_sorumlu = st.text_input("Sorumlu", key="swot_ak_sorumlu")
        with ak2:
            ak_termin = st.date_input("Termin Tarihi", value=date.today() + timedelta(days=30),
                                       key="swot_ak_termin")
        ak_kpi = st.text_input("KPI / Başarı Kriteri", key="swot_ak_kpi")

        if st.form_submit_button("Aksiyon Oluştur", type="primary"):
            if not ak_baslik:
                st.error("Aksiyon basligi zorunludur.")
            else:
                aksiyon = SwotAksiyon(
                    olcum_id=olcum_id,
                    madde_id=secili_madde.id,
                    madde_baslik=secili_madde.baslik,
                    madde_tur=secili_madde.tur,
                    aksiyon_baslik=ak_baslik,
                    sorumlu=ak_sorumlu,
                    termin_tarihi=ak_termin.isoformat(),
                    kpi=ak_kpi,
                )
                store.upsert("aksiyonlar", aksiyon)
                st.success("Aksiyon oluşturuldu!")
                st.rerun()


# ============================================================
# ALT SEKME 6: AYARLAR & IMPORT
# ============================================================

def _render_ayarlar_import(store: SwotDataStore):
    styled_section("Ayarlar & Import", "#64748b")

    ay_tabs = st.tabs(["📂 Alt Kategoriler", "🎓 Kademeler", "⚙️ Ayarlar", "📤 CSV Import"])

    # -- Alt Kategoriler --
    with ay_tabs[0]:
        styled_section("Alt Kategoriler", "#4472C4")
        kategoriler = store.load_objects("alt_kategoriler")
        kategoriler.sort(key=lambda x: x.sira)

        for kat in kategoriler:
            durum = "Aktif" if kat.aktif else "Pasif"
            d_renk = "#10b981" if kat.aktif else "#ef4444"
            st.markdown(
                f'<div style="background:#111827;border:1px solid #e2e8f0;border-radius:8px;'
                f'padding:8px 12px;margin:3px 0;display:flex;align-items:center;gap:8px;">'
                f'<span style="font-weight:600;color:#94A3B8;font-size:13px;">{kat.alt_kategori}</span>'
                f'<span style="background:{d_renk}20;color:{d_renk};padding:1px 6px;'
                f'border-radius:6px;font-size:10px;font-weight:600;">{durum}</span>'
                f'<span style="color:#94a3b8;font-size:10px;">Sira: {kat.sira}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with st.expander("Yeni Alt Kategori Ekle"):
            yeni_kat = st.text_input("Kategori Adi", key="swot_yeni_kat")
            yeni_sira = st.number_input("Sira", min_value=1, value=len(kategoriler) + 1,
                                         key="swot_yeni_kat_sira")
            if st.button("Ekle", key="swot_kat_ekle"):
                if yeni_kat:
                    store.upsert("alt_kategoriler", SwotAltKategori(
                        alt_kategori=yeni_kat, aktif=True, sira=yeni_sira
                    ))
                    st.success(f"'{yeni_kat}' eklendi!")
                    st.rerun()

    # -- Kademeler --
    with ay_tabs[1]:
        styled_section("Kademeler", "#10b981")
        kademeler = store.load_objects("kademeler")
        kademeler.sort(key=lambda x: x.sira)

        for kad in kademeler:
            durum = "Aktif" if kad.aktif else "Pasif"
            d_renk = "#10b981" if kad.aktif else "#ef4444"
            st.markdown(
                f'<div style="background:#111827;border:1px solid #e2e8f0;border-radius:8px;'
                f'padding:8px 12px;margin:3px 0;display:flex;align-items:center;gap:8px;">'
                f'<span style="font-weight:600;color:#94A3B8;font-size:13px;">{kad.kademe_adi}</span>'
                f'<span style="background:{d_renk}20;color:{d_renk};padding:1px 6px;'
                f'border-radius:6px;font-size:10px;font-weight:600;">{durum}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with st.expander("Yeni Kademe Ekle"):
            yeni_kad = st.text_input("Kademe Adi", key="swot_yeni_kad")
            yeni_kad_sira = st.number_input("Sira", min_value=1, value=len(kademeler) + 1,
                                              key="swot_yeni_kad_sira")
            if st.button("Ekle", key="swot_kad_ekle"):
                if yeni_kad:
                    store.upsert("kademeler", SwotKademe(
                        kademe_adi=yeni_kad, aktif=True, sira=yeni_kad_sira
                    ))
                    st.success(f"'{yeni_kad}' eklendi!")
                    st.rerun()

    # -- Ayarlar --
    with ay_tabs[2]:
        styled_section("Sistem Ayarlari", "#f59e0b")
        ayarlar = store.load_objects("ayarlar")
        for ayar in ayarlar:
            with st.expander(f"{ayar.ayar_anahtari}: {ayar.deger}"):
                st.caption(ayar.aciklama)
                yeni_deger = st.text_input("Deger", value=ayar.deger,
                                            key=f"swot_ayar_{ayar.id}")
                if st.button("Kaydet", key=f"swot_ayar_btn_{ayar.id}"):
                    ayar.deger = yeni_deger
                    store.upsert("ayarlar", ayar)
                    st.success("Ayar güncellendi!")
                    st.rerun()

    # -- CSV Import --
    with ay_tabs[3]:
        styled_section("CSV Import", "#8b5cf6")
        st.markdown("""
        **Import Dosyalari:**
        1. **Alt Kategoriler CSV** - `alt_kategori, aktif, sira`
        2. **Kademe CSV** - `kademe_adi, aktif, sira`
        3. **Ayarlar CSV** - `ayar_anahtari, deger, aciklama`
        4. **Sablon SWOT Maddeleri CSV** - `tur, alt_kategori, kademe, baslik, etki, olasilik, aciliyet, not`
        """)

        import_tipi = st.selectbox("Import Tipi",
                                     ["Alt Kategoriler", "Kademeler", "Ayarlar", "Sablon SWOT Maddeleri"],
                                     key="swot_import_tipi")
        uploaded = st.file_uploader("CSV Dosyasi", type=["csv"], key="swot_import_csv")

        if uploaded:
            from utils.security import validate_upload
            _ok, _msg = validate_upload(uploaded, allowed_types=["csv"], max_mb=100)
            if not _ok:
                st.error(f"⚠️ {_msg}")
                uploaded = None
        if uploaded and st.button("Import Et", type="primary", key="swot_import_btn"):
            try:
                content = uploaded.read().decode("utf-8-sig")
                reader = csv.DictReader(io.StringIO(content))
                rows = list(reader)
                count = 0

                if import_tipi == "Alt Kategoriler":
                    for row in rows:
                        store.upsert("alt_kategoriler", SwotAltKategori(
                            alt_kategori=row.get("alt_kategori", "").strip(),
                            aktif=row.get("aktif", "1").strip() == "1",
                            sira=int(row.get("sira", 0)),
                        ))
                        count += 1

                elif import_tipi == "Kademeler":
                    for row in rows:
                        store.upsert("kademeler", SwotKademe(
                            kademe_adi=row.get("kademe_adi", "").strip(),
                            aktif=row.get("aktif", "1").strip() == "1",
                            sira=int(row.get("sira", 0)),
                        ))
                        count += 1

                elif import_tipi == "Ayarlar":
                    for row in rows:
                        store.upsert("ayarlar", SwotAyar(
                            ayar_anahtari=row.get("ayar_anahtari", "").strip(),
                            deger=row.get("deger", "").strip(),
                            aciklama=row.get("aciklama", "").strip(),
                        ))
                        count += 1

                elif import_tipi == "Sablon SWOT Maddeleri":
                    # Sablon maddeler olcum olmadan eklenir (template)
                    aktif_olcum = store.get_aktif_olcum()
                    if not aktif_olcum:
                        st.warning("Sablon maddeleri eklemek için aktif bir olcum gereklidir.")
                    else:
                        for row in rows:
                            store.upsert("maddeler", SwotMadde(
                                olcum_id=aktif_olcum.id,
                                tur=row.get("tur", "S").strip().upper(),
                                alt_kategori=row.get("alt_kategori", "").strip(),
                                kademe=row.get("kademe", "TUMU").strip(),
                                baslik=row.get("baslik", "").strip(),
                                etki=int(row.get("etki", 3)),
                                olasilik=int(row.get("olasilik", 3)),
                                aciliyet=int(row.get("aciliyet", 3)),
                                anonim_token="import",
                            ))
                            count += 1

                st.success(f"{count} kayit basariyla import edildi!")
                st.rerun()
            except Exception as e:
                st.error(f"Import hatasi: {e}")


# ============================================================
# ANA RENDER FONKSIYONU
# ============================================================

def render_swot_analizi():
    """SWOT Analizi modulu ana giris noktasi."""
    _inject_css()
    store = _get_swot_store()

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("swot_analizi_egitim_yili")

    sub_tabs = st.tabs([
        "📊 Dashboard",
        "📏 Olcum Yönetimi",
        "✏️ SWOT Girişi",
        "📈 Sonuclar & Raporlar",
        "🎯 Aksiyon Plani",
        "⚙️ Ayarlar & Import",
        "🤖 Smarti",
    ])

    with sub_tabs[0]:
        _render_dashboard(store)
    with sub_tabs[1]:
        _render_olcum_yonetimi(store)
    with sub_tabs[2]:
        _render_swot_girisi(store)
    with sub_tabs[3]:
        _render_sonuclar(store)
    with sub_tabs[4]:
        _render_aksiyon_plani(store)
    with sub_tabs[5]:
        _render_ayarlar_import(store)
    with sub_tabs[6]:
        try:
            from views.ai_destek import render_smarti_chat
            render_smarti_chat(modul="swot_analizi")
        except Exception:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
                'padding:20px;border-radius:12px;text-align:center;margin:20px 0">'
                '<h3 style="margin:0">🤖 Smarti AI</h3>'
                '<p style="margin:8px 0 0;opacity:.85">Smarti AI asistanı bu modülde aktif. '
                'Sorularınızı yazın, AI destekli yanıtlar alın.</p></div>',
                unsafe_allow_html=True)
            user_q = st.text_area("Smarti'ye sorunuzu yazın:", key="smarti_q_swot_analizi")
            if st.button("Gönder", key="smarti_send_swot_analizi"):
                if user_q.strip():
                    try:
                        from openai import OpenAI
                        import os
                        api_key = os.environ.get("OPENAI_API_KEY", "")
                        if api_key:
                            client = OpenAI(api_key=api_key)
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen SmartCampus AI'nin Smarti asistanısın. swot_analizi modülü hakkında Türkçe yardım et."},
                                    {"role": "user", "content": user_q}
                                ],
                                temperature=0.7, max_tokens=500)
                            st.markdown(resp.choices[0].message.content)
                        else:
                            st.warning("API anahtarı tanımlı değil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")
