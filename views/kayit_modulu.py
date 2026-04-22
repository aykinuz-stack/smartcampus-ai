"""
Kayit Modulu — Bagimsiz Ogrenci Kayit Surec Takip
===================================================
Pipeline + Gunluk Isler + Aday Islemleri + Istatistikler.
Tamamen bagimsiz — kendi verisi, kendi is mantigi.
"""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime
from typing import Any

import streamlit as st

from utils.ui_common import inject_common_css, styled_header, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("kayit_modulu")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    from models.kayit_modulu import get_kayit_store as _gks
    _ks = _gks().istatistikler() if hasattr(_gks(), 'istatistikler') else {}
    modul_hosgeldin("kayit_modulu",
        "7 asamali pipeline, AI lead scoring, 12 ay data arama kampanyasi",
        [(str(_ks.get("toplam", 0)), "Aday"), (str(_ks.get("kesin_kayit", 0)), "Kayit"), ("7", "Asama")])
except Exception:
    pass
from models.kayit_modulu import (
    KayitAday, KayitDataStore, get_kayit_store,
    PIPELINE_ASAMALARI, PIPELINE_INFO, KADEME_SECENEKLERI, KANAL_SECENEKLERI,
    SINIF_SECENEKLERI, CINSIYET_SECENEKLERI, OKUL_TURU_SECENEKLERI,
    ARAMA_SONUCLARI, GORUSME_SONUCLARI, MAX_ULASIM_YOK_ARAMA,
    TEST_TURLERI, IHTIYAC_KATEGORILERI, IHTIYAC_ONCELIK,
    AY_ADLARI, KAMPANYA_ARACLARI, SABIT_KAMPANYALAR,
    arama_kaydet, gorusme_kaydet, fiyat_kaydet, sozlesme_kaydet, kesin_kayit_yap,
    KAYIP_NEDENLERI, KAYIP_NEDEN_LISTESI, VARSAYILAN_KONTENJAN,
)


# ============================================================
# ANA RENDER
# ============================================================

def render_kayit_modulu():
    inject_common_css()
    styled_header("Kayit Modulu", "Aday Pipeline Yonetimi — Giris'ten Kesin Kayit'a", icon="🎯")

    store = get_kayit_store()
    adaylar = store.load_all()

    # ── OTOMATIK CRON SCANNER ──
    # Sayfa her acilisinda kontrol et; son 4 saat icinde calismadiysa tetikle.
    # Zaman bazli otomasyonlar (fiyat 3 gun, olumsuz 30 gun, dogum gunu, isi dustu,
    # randevu reminder) bu tarama ile canlanir.
    try:
        from models.kayit_otomasyon import cron_tara, cron_gerekli_mi, son_cron_zamani
        if cron_gerekli_mi(saat_esigi=4):
            _cron_sonuc = cron_tara(adaylar)
            if not _cron_sonuc.get("atlandi") and _cron_sonuc.get("toplam_tetiklendi", 0) > 0:
                st.toast(
                    f"⚡ Otomasyon taramasi: {_cron_sonuc['toplam_tetiklendi']} yeni tetikleme",
                    icon="🔔",
                )
    except Exception:
        pass

    # Yönetici özet banner
    _stats = store.istatistikler()
    from models.kayit_takip_engine import gun_sonu_ozet
    _gso = gun_sonu_ozet(adaylar)
    _bugun = date.today().isoformat()
    _bugun_arama = sum(sum(1 for ar in a.aramalar if ar.get("tarih", "")[:10] == _bugun) for a in adaylar)
    _bugun_kayit = sum(1 for a in adaylar if a.kapanma_tarihi and a.kapanma_tarihi[:10] == _bugun and a.asama == "kesin_kayit")

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border:1px solid #334155;'
        f'border-radius:12px;padding:10px 16px;margin-bottom:10px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">'
        f'<div><span style="color:#94a3b8;font-size:11px;">Toplam</span> <b style="color:#6366f1;font-size:16px;">{_stats["toplam"]}</b></div>'
        f'<div><span style="color:#94a3b8;font-size:11px;">Aktif</span> <b style="color:#f59e0b;font-size:16px;">{_stats["aktif"]}</b></div>'
        f'<div><span style="color:#94a3b8;font-size:11px;">Kayıt</span> <b style="color:#22c55e;font-size:16px;">{_stats["kesin_kayit"]}</b></div>'
        f'<div><span style="color:#94a3b8;font-size:11px;">Dönüşüm</span> <b style="color:#3b82f6;font-size:16px;">%{_stats["donusum"]:.0f}</b></div>'
        f'<div><span style="color:#94a3b8;font-size:11px;">🔥Sıcak</span> <b style="color:#ef4444;font-size:16px;">{_gso["sicak"]}</b></div>'
        f'<div><span style="color:#94a3b8;font-size:11px;">⏰Geciken</span> <b style="color:#f97316;font-size:16px;">{_gso["geciken"]}</b></div>'
        f'<div><span style="color:#94a3b8;font-size:11px;">Bugün</span> <b style="color:#22c55e;font-size:16px;">{_bugun_arama}📞 {_bugun_kayit}✅</b></div>'
        f'</div></div>',
        unsafe_allow_html=True)

    try:
        from utils.ui_common import geri_sayim_sayaci
        geri_sayim_sayaci("2026-06-30", "Kayıt Kapanış", "🎯")
    except Exception:
        pass

    # Veri dogrulama
    try:
        from utils.ui_common import veri_dogrulama_butonu, veri_dogrulama_sonucu
        veri_dogrulama_butonu("kayit_modulu")
        if st.session_state.get("_veri_kontrol_aktif_kayit_modulu"):
            sorunlar = []
            if _stats.get("toplam", 0) == 0:
                sorunlar.append({"tip": "eksik", "alan": "Aday Kaydi", "sayi": 0, "oncelik": "yuksek"})
            _no_tel = sum(1 for a in adaylar if not a.telefon)
            if _no_tel > 0:
                sorunlar.append({"tip": "eksik", "alan": "Telefon Eksik Aday", "sayi": _no_tel, "oncelik": "orta"})
            veri_dogrulama_sonucu(sorunlar)
            st.session_state["_veri_kontrol_aktif_kayit_modulu"] = False
    except Exception:
        pass

    # ══════════════════════════════════════════════════════════
    # KURUMSAL MODUL KILAVUZLARI — Tum Modulleri Tek Yerden Indir
    # Tek modul (dropdown ile sec) veya TUM MODULLER (ZIP olarak)
    # ══════════════════════════════════════════════════════════
    with st.expander("📘 **Kurumsal Modül Kılavuzları** — Tüm modüller için PDF rehberi",
                       expanded=False):
        st.markdown(
            '<div style="background:linear-gradient(135deg,#0B1E3F 0%,#1e293b 100%);'
            'border:2px solid #C8952E;border-radius:12px;padding:14px 18px;margin:6px 0;'
            'box-shadow:0 4px 25px #C8952E25">'
            '<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">'
            '<div style="font-size:2rem">📚</div>'
            '<div style="flex:1;min-width:240px">'
            '<div style="color:#C8952E;font-size:0.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase">PREMIUM DIGITAL HANDBOOK LIBRARY</div>'
            '<div style="color:#fff;font-size:1.15rem;font-weight:800;margin-top:2px">33 Modülün Kurumsal Kılavuzları</div>'
            '<div style="color:#94a3b8;font-size:0.78rem;margin-top:2px">'
            'Her modül için ayrı PDF • Sekme detayları • Otomasyonlar • Arka plan motorları • Veri yapıları'
            '</div></div></div></div>',
            unsafe_allow_html=True,
        )

        try:
            from models.genel_modul_kilavuzu import (
                MODUL_REGISTRY, list_moduller, generate_pdf, generate_zip_all
            )
            _kilavuz_yuklendi = True
        except Exception as _ie:
            st.error(f"❌ Kılavuz modülü yüklenemedi: {_ie}")
            _kilavuz_yuklendi = False

        if _kilavuz_yuklendi:
            try:
                from utils.shared_data import load_kurum_profili
                _kp = load_kurum_profili() or {}
                _kurum_adi_pdf = (_kp.get("kurum_adi") or _kp.get("okul_adi")
                                   or _kp.get("name") or "SmartCampus AI")
            except Exception:
                _kurum_adi_pdf = "SmartCampus AI"

            # ── 2 SEKMELI: Tek Modul / Tum Moduller (ZIP) ──
            _kil_tab1, _kil_tab2 = st.tabs([
                "📄 Tek Modül PDF",
                "📦 Tüm Modüller (ZIP)",
            ])

            # ═══════════ TAB 1: TEK MODUL ═══════════
            with _kil_tab1:
                st.caption(
                    "📖 Bir modül seçin — kurumsal PDF kılavuzu hemen indirin. "
                    "Her PDF; modülün sekmeleri, otomasyonları, arka plan motorları, "
                    "veri dosyaları ve kullanım senaryolarını içerir."
                )

                # Modul listesi (kategori bazli grupla, dropdown'a koy)
                _moduller = list_moduller()
                _modul_dict = {f"{e}  {ad}": mid for mid, ad, e in _moduller}

                _sec_label = st.selectbox(
                    "Modül Seç",
                    options=list(_modul_dict.keys()),
                    key="km_kil_modul_sec",
                    help="Hangi modülün PDF kılavuzunu istiyorsunuz?",
                )
                _secili_mid = _modul_dict.get(_sec_label, "kayit_modulu")

                # Cache key — secilen module gore ayri PDF'ler
                _cache_key = f"_km_kil_pdf_{_secili_mid}"

                # PDF yoksa otomatik uret (ilk secilis)
                if _cache_key not in st.session_state:
                    with st.spinner(f"📖 {_sec_label} kılavuzu hazırlanıyor (~2 saniye)..."):
                        try:
                            _pdf_bytes = generate_pdf(_secili_mid, _kurum_adi_pdf)
                            if _pdf_bytes and len(_pdf_bytes) > 1000:
                                st.session_state[_cache_key] = _pdf_bytes
                            else:
                                st.session_state[_cache_key] = None
                        except Exception as _e:
                            st.session_state[_cache_key] = None
                            st.error(f"PDF üretilemedi: {_e}")

                _pdf = st.session_state.get(_cache_key)
                if _pdf:
                    _boyut_kb = len(_pdf) / 1024
                    _meta = MODUL_REGISTRY.get(_secili_mid, {})
                    _tab_n = len(_meta.get("tablar", []))
                    _otom_n = len(_meta.get("otomasyonlar", []))

                    st.markdown(
                        f'<div style="background:linear-gradient(90deg,#16a34a20,#22c55e10);'
                        f'border:1px solid #22c55e60;border-radius:8px;padding:10px 14px;margin:8px 0">'
                        f'<span style="color:#22c55e;font-size:0.8rem;font-weight:700">✓ PDF HAZIR</span>'
                        f'<span style="color:#94a3b8;font-size:0.78rem"> • '
                        f'<b style="color:#e2e8f0">{_boyut_kb:.1f} KB</b> • '
                        f'<b style="color:#e2e8f0">{_tab_n} sekme</b> • '
                        f'<b style="color:#e2e8f0">{_otom_n} otomasyon</b></span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    _safe_ad = "".join(c if c.isalnum() or c in "_-" else "_"
                                        for c in _meta.get("ad", _secili_mid))
                    st.download_button(
                        label=f"📥  {_meta.get('ad', _secili_mid).upper()} PDF'YİNİ İNDİR",
                        data=_pdf,
                        file_name=f"{_safe_ad}_Kilavuzu_{date.today().isoformat()}.pdf",
                        mime="application/pdf",
                        key=f"km_kil_dl_{_secili_mid}",
                        type="primary",
                        use_container_width=True,
                    )
                else:
                    st.warning("PDF üretilemedi. Tekrar deneyin.")
                    if st.button("🔄 Tekrar Dene", key=f"km_kil_retry_{_secili_mid}"):
                        if _cache_key in st.session_state:
                            del st.session_state[_cache_key]
                        st.rerun()

            # ═══════════ TAB 2: TUM MODULLER ZIP ═══════════
            with _kil_tab2:
                st.caption(
                    "📦 Tüm 33 modülün PDF kılavuzlarını **tek ZIP dosyası** olarak indirin. "
                    "Her PDF dosyası ZIP içinde modül adıyla yer alır."
                )

                _zip_cache_key = "_km_kil_zip_all"

                if _zip_cache_key not in st.session_state:
                    if st.button(
                        "🔨  TÜM 33 MODÜLÜN ZIP'İNİ ÜRET",
                        key="km_kil_zip_uret",
                        type="primary",
                        use_container_width=True,
                        help="Tüm modüllerin PDF'leri bir ZIP'te paketlenir (~15-30 saniye)",
                    ):
                        with st.spinner("📦 33 modülün PDF'i üretiliyor + ZIP'leniyor (~30 saniye)..."):
                            try:
                                _zip_bytes = generate_zip_all(_kurum_adi_pdf)
                                if _zip_bytes and len(_zip_bytes) > 1000:
                                    st.session_state[_zip_cache_key] = _zip_bytes
                                    st.success(
                                        f"✅ ZIP hazır! **{len(_zip_bytes) / 1024:.1f} KB** • "
                                        f"33 modülün kurumsal PDF kılavuzları"
                                    )
                                else:
                                    st.error("ZIP üretilemedi")
                            except Exception as _e:
                                st.error(f"Hata: {_e}")
                                import traceback
                                with st.expander("Detay"):
                                    st.code(traceback.format_exc())
                    else:
                        st.info(
                            "ℹ️ Yukarıdaki butona basın — 33 modülün PDF'i üretilip "
                            "ZIP olarak indirme butonu hazır olacak."
                        )

                _zip = st.session_state.get(_zip_cache_key)
                if _zip:
                    st.markdown(
                        f'<div style="background:linear-gradient(90deg,#16a34a20,#22c55e10);'
                        f'border:1px solid #22c55e60;border-radius:8px;padding:10px 14px;margin:8px 0">'
                        f'<span style="color:#22c55e;font-size:0.8rem;font-weight:700">✓ ZIP HAZIR</span>'
                        f'<span style="color:#94a3b8;font-size:0.78rem"> • '
                        f'<b style="color:#e2e8f0">{len(_zip) / 1024:.1f} KB</b> • '
                        f'<b style="color:#e2e8f0">33 modül</b> • '
                        f'<b style="color:#e2e8f0">~33 PDF</b></span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        label="📥  TÜM MODÜLLERİN ZIP'İNİ İNDİR",
                        data=_zip,
                        file_name=f"Tum_Modul_Kilavuzlari_{date.today().isoformat()}.zip",
                        mime="application/zip",
                        key="km_kil_zip_dl",
                        type="primary",
                        use_container_width=True,
                    )
                    if st.button("🔄 Yeniden Üret", key="km_kil_zip_reset",
                                  use_container_width=True):
                        del st.session_state[_zip_cache_key]
                        st.rerun()

            # Modul listesi ozeti
            with st.expander(f"📚 Tüm {len(MODUL_REGISTRY)} Modül Listesi", expanded=False):
                _kategori_grup = {}
                for _mid, _meta in MODUL_REGISTRY.items():
                    _kat = _meta.get("kategori", "DIGER")
                    _kategori_grup.setdefault(_kat, []).append(
                        f"{_meta.get('emoji', '📦')} **{_meta.get('ad', _mid)}**"
                    )
                for _kat, _liste in sorted(_kategori_grup.items()):
                    st.markdown(f"**{_kat}** ({len(_liste)} modül)")
                    for _li in _liste:
                        st.markdown(f"- {_li}")
                    st.markdown("")

    # ── Kompakt + satira sigan tab stili ──
    st.markdown("""
    <style>
    /* Kayit Modulu tab listesini satirlara bolumlendir ve sıkıştır */
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab-list"] {
        gap: 3px !important;
        flex-wrap: wrap !important;
        overflow-x: visible !important;
        padding: 4px 0 !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab"] {
        padding: 4px 10px !important;
        min-height: 30px !important;
        height: 30px !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
        border-radius: 6px !important;
        background: #131825 !important;
        border: 1px solid #334155 !important;
        color: #cbd5e1 !important;
        transition: all 0.15s ease !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab"]:hover {
        background: #1e293b !important;
        border-color: #64748b !important;
        color: #e2e8f0 !important;
    }
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0B1E3F, #1e293b) !important;
        border-color: #C8952E !important;
        color: #C8952E !important;
        box-shadow: 0 2px 8px #C8952E20 !important;
    }
    /* Streamlit'in alt cizgisini gizle (kendi border'imiz var) */
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab-highlight"],
    div[data-testid="stTabs"] > div:first-child [data-baseweb="tab-border"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── 2 Seviyeli Tab Yapisi: ust seviye grup secimi, alt seviye sekmeler ──
    _KAYIT_GRUPLARI = {
        "📋 Aday Yonetimi": [
            ("📋 Günlük", 1), ("🔄 Pipeline", 2), ("➕ Yeni Aday", 3),
            ("📊 İstatistik", 4), ("✅ Kayıt Olanlar", 32), ("📞 Arama Destek", 34),
        ],
        "📣 Pazarlama": [
            ("📣 Kampanya", 5), ("📢 Outreach", 11), ("📈 Kampanya Performans", 29),
            ("🔗 Referans Zinciri", 22), ("🎪 Etkinlik", 15),
        ],
        "⚡ Otomasyon & AI": [
            ("⚡ Otomasyon", 6), ("🎤 Sesli Asistan", 14), ("🔮 AI Tahmin", 28),
            ("🧠 Zeki Motorlar", 17), ("💎 Konuşma Madeni", 13),
        ],
        "📉 Analiz & Strateji": [
            ("🎯 Rakip", 8), ("🚨 Risk Radar", 12), ("🌡️ Isı Haritası", 20),
            ("📉 Kayıp Analizi", 23), ("📅 YoY Sezon", 24),
            ("🔍 İhtiyaç Analizi", 31), ("🧪 Testler", 30),
        ],
        "🏫 Operasyon": [
            ("🏫 Tur", 7), ("🧮 Yerleştirme", 9), ("🎓 Kontenjan", 25),
            ("💻 Bilgi İşlem", 33), ("🏆 Skorboard", 10),
        ],
        "👑 Premium Araclar": [
            ("✨ Kapanış Silahları", 16), ("👑 Üst Düzey", 18), ("🛡️ Kayıp Kalkanı", 19),
            ("🎯 Kapanış Radar", 21), ("⚔️ Savaş Odası", 26), ("🗺️ Yolculuk Haritası", 27),
        ],
    }

    _secili_grup = st.radio(
        "Bolum sec", list(_KAYIT_GRUPLARI.keys()),
        horizontal=True, label_visibility="collapsed",
    )
    _grup_tablar = _KAYIT_GRUPLARI[_secili_grup]
    _tab_isimleri = [t[0] for t in _grup_tablar]
    _tab_numaralari = [t[1] for t in _grup_tablar]
    _acilan_tabs = st.tabs(_tab_isimleri)

    # Aktif tab map — sadece secili grubun tablari gercek, digerlerini atla
    _aktif_set = set(_tab_numaralari)
    _tab_map = {}
    for i, real_tab in zip(_tab_numaralari, _acilan_tabs):
        _tab_map[i] = real_tab

    # Secili gruptaki tablari ata, digerlerini None yap (with blogu atlanir)
    tab1 = _tab_map.get(1)
    tab2 = _tab_map.get(2)
    tab3 = _tab_map.get(3)
    tab4 = _tab_map.get(4)
    tab5 = _tab_map.get(5)
    tab6 = _tab_map.get(6)
    tab7 = _tab_map.get(7)
    tab8 = _tab_map.get(8)
    tab9 = _tab_map.get(9)
    tab10 = _tab_map.get(10)
    tab11 = _tab_map.get(11)
    tab12 = _tab_map.get(12)
    tab13 = _tab_map.get(13)
    tab14 = _tab_map.get(14)
    tab15 = _tab_map.get(15)
    tab16 = _tab_map.get(16)
    tab17 = _tab_map.get(17)
    tab18 = _tab_map.get(18)
    tab19 = _tab_map.get(19)
    tab20 = _tab_map.get(20)
    tab21 = _tab_map.get(21)
    tab22 = _tab_map.get(22)
    tab23 = _tab_map.get(23)
    tab24 = _tab_map.get(24)
    tab25 = _tab_map.get(25)
    tab26 = _tab_map.get(26)
    tab27 = _tab_map.get(27)
    tab28 = _tab_map.get(28)
    tab29 = _tab_map.get(29)
    tab30 = _tab_map.get(30)
    tab31 = _tab_map.get(31)
    tab32 = _tab_map.get(32)
    tab33 = _tab_map.get(33)
    tab34 = _tab_map.get(34)

    if tab1 is not None:
      with tab1:
        _render_gunluk_isler(store, adaylar)

    if tab2 is not None:
      with tab2:
        _render_pipeline(store, adaylar)

    if tab3 is not None:
      with tab3:
        _render_yeni_aday(store)

    if tab4 is not None:
      with tab4:
        _render_istatistikler(store, adaylar)
        st.markdown("---")
        _render_personel_performans(adaylar)
        st.markdown("---")
        _render_raporlar(store, adaylar)

    if tab5 is not None:
      with tab5:
        _render_kampanyalar(store, adaylar)

    # ZIRVE: Otomasyon Atolyesi
    if tab6 is not None:
      with tab6:
        try:
            from utils.kayit_otomasyon_ui import render_otomasyon_atolyesi
            render_otomasyon_atolyesi()
        except Exception as e:
            st.error(f"Otomasyon yuklenemedi: {e}")

    # ZIRVE: Tur Rezervasyon
    if tab7 is not None:
      with tab7:
        try:
            from utils.kayit_tur_ui import render_tur_paneli
            render_tur_paneli()
        except Exception as e:
            st.error(f"Tur paneli yuklenemedi: {e}")

    # ZIRVE: Rakip Istihbarat
    if tab8 is not None:
      with tab8:
        try:
            from utils.kayit_rakip_ui import render_rakip_panel
            render_rakip_panel(adaylar)
        except Exception as e:
            st.error(f"Rakip paneli yuklenemedi: {e}")

    # ULTRA: Sinif Yerlestirme Optimizatoru
    if tab9 is not None:
      with tab9:
        try:
            from utils.kayit_yerlestirme_ui import render_yerlestirme_paneli
            render_yerlestirme_paneli()
        except Exception as e:
            st.error(f"Yerlestirme paneli yuklenemedi: {e}")

    # MEGA: Koordinator Skorboard
    if tab10 is not None:
      with tab10:
        try:
            from utils.kayit_skorboard_ui import render_skorboard_paneli
            render_skorboard_paneli()
        except Exception as e:
            st.error(f"Skorboard yuklenemedi: {e}")

    # ZIRVE: Toplu Outreach Cannon
    if tab11 is not None:
      with tab11:
        try:
            from utils.kayit_outreach_ui import render_outreach_panel
            render_outreach_panel(adaylar)
        except Exception as e:
            st.error(f"Outreach yuklenemedi: {e}")

    # ZIRVE: Risk Radar
    if tab12 is not None:
      with tab12:
        try:
            from utils.kayit_radar_ui import render_risk_radar_paneli
            render_risk_radar_paneli(adaylar)
        except Exception as e:
            st.error(f"Risk radar yuklenemedi: {e}")

    # ZIRVE: Konusma Zekasi Madeni
    if tab13 is not None:
      with tab13:
        try:
            from utils.kayit_konusma_madeni_ui import render_konusma_madeni_paneli
            render_konusma_madeni_paneli(adaylar)
        except Exception as e:
            st.error(f"Konusma madeni yuklenemedi: {e}")

    # YENI: Sesli Aday Asistani (Voice-First)
    if tab14 is not None:
      with tab14:
        try:
            from utils.kayit_sesli_asistan_ui import render_sesli_asistan_paneli
            render_sesli_asistan_paneli()
        except Exception as e:
            st.error(f"Sesli asistan yuklenemedi: {e}")

    # YENI: Aile Etkinlik Merkezi
    if tab15 is not None:
      with tab15:
        try:
            from utils.kayit_etkinlik_ui import render_etkinlik_paneli
            render_etkinlik_paneli(adaylar)
        except Exception as e:
            st.error(f"Etkinlik paneli yuklenemedi: {e}")

    # YENI: Kapanış Silahları (Geleceğin Kitabı + Korku Yıkıcı + Kişisel URL)
    if tab16 is not None:
      with tab16:
        try:
            _render_kapanis_silahlari(store, adaylar)
        except Exception as e:
            st.error(f"Kapanış silahları yuklenemedi: {e}")
            import traceback
            st.code(traceback.format_exc())

    # YENI: Zeki Motorlar (Pişmanlık + Çocuğun Sesi + Sessiz Red)
    if tab17 is not None:
      with tab17:
        try:
            _render_zeki_motorlar(store, adaylar)
        except Exception as e:
            st.error(f"Zeki motorlar yuklenemedi: {e}")
            import traceback
            st.code(traceback.format_exc())

    # YENI: Üst Düzey (Gelir Optimizasyon + Kurumsal Kanal + CEO Cockpit)
    if tab18 is not None:
      with tab18:
        try:
            _render_ust_duzey(store, adaylar)
        except Exception as e:
            st.error(f"Üst düzey modüller yuklenemedi: {e}")
            import traceback
            st.code(traceback.format_exc())

    # YENI: Kayıp Kalkanı (5dk Kuralı + Parmak İzi + Son Mil)
    if tab19 is not None:
      with tab19:
        try:
            _render_kayip_kalkani(store, adaylar)
        except Exception as e:
            st.error(f"Kayıp kalkanı yuklenemedi: {e}")
            import traceback
            st.code(traceback.format_exc())

    # ZİRVE: Veli Isı Haritası + Anlık Müdahale
    if tab20 is not None:
      with tab20:
        _render_isi_haritasi(store, adaylar)

    # ZİRVE: Bir Adım Kaldı — Akıllı Kapanış Radar
    if tab21 is not None:
      with tab21:
        _render_kapanis_radar(store, adaylar)

    # ZİRVE: Veliden Veliye Referans Zinciri
    if tab22 is not None:
      with tab22:
        _render_referans_zinciri(store, adaylar)

    # ZİRVE: Kayıp Nedeni Analizi
    if tab23 is not None:
      with tab23:
        _render_kayip_analizi(store, adaylar)

    # ZİRVE: Sezonluk YoY Karşılaştırma
    if tab24 is not None:
      with tab24:
        _render_yoy_sezon(store, adaylar)

    # ZİRVE: Dinamik Kontenjan Yönetimi
    if tab25 is not None:
      with tab25:
        _render_kontenjan_yonetimi(store, adaylar)

    # ULTRA MEGA: Savaş Odası
    if tab26 is not None:
      with tab26:
        try:
            from views._kayit_ultra_mega import render_savas_odasi
            render_savas_odasi(store, adaylar)
        except Exception as _e:
            st.error(f"Savaş Odası yüklenemedi: {_e}")

    # ULTRA MEGA: Yolculuk Haritası
    if tab27 is not None:
      with tab27:
        try:
            from views._kayit_ultra_mega import render_yolculuk_haritasi
            render_yolculuk_haritasi(store, adaylar)
        except Exception as _e:
            st.error(f"Yolculuk Haritası yüklenemedi: {_e}")

    # ULTRA MEGA: AI Tahmin + Gelir Projeksiyon
    if tab28 is not None:
      with tab28:
        try:
            from views._kayit_ultra_mega import render_ai_tahmin
            render_ai_tahmin(store, adaylar)
        except Exception as _e:
            st.error(f"AI Tahmin yüklenemedi: {_e}")

    if tab29 is not None:
      with tab29:
        _render_kampanya_performans_tab(store, adaylar)
    if tab30 is not None:
      with tab30:
        _render_testler(store, adaylar)
    if tab31 is not None:
      with tab31:
        _render_ihtiyac_analizi(store, adaylar)
    if tab32 is not None:
      with tab32:
        _render_kayit_olanlar(store, adaylar)
    if tab33 is not None:
      with tab33:
        _render_ogrenci_bilgi_islem(store, adaylar)
    if tab34 is not None:
      with tab34:
        _render_arama_destek()


# ============================================================
# KAMPANYALAR
# ============================================================

_AY_RENK = {
    1: "#38bdf8", 2: "#38bdf8", 3: "#4ade80", 4: "#4ade80", 5: "#4ade80", 6: "#fbbf24",
    7: "#fbbf24", 8: "#fb923c", 9: "#fb923c", 10: "#a78bfa", 11: "#a78bfa", 12: "#38bdf8",
}
_AY_IKON = {
    1: "❄️", 2: "❄️", 3: "🌱", 4: "🌸", 5: "☀️", 6: "🌞",
    7: "🏖️", 8: "📚", 9: "🏫", 10: "🍂", 11: "🍁", 12: "🎄",
}


def _render_kampanyalar(store: KayitDataStore, adaylar: list[KayitAday]):
    """Kampanya yonetimi — aylara gore otomatik + manuel kampanyalar."""
    bugun = date.today()
    secili_yil = bugun.year

    st.markdown(
        '<div style="background:linear-gradient(135deg,#f59e0b,#d97706);border-radius:12px;'
        'padding:1.2rem 1.5rem;margin-bottom:1rem">'
        '<h3 style="color:#fff;margin:0">📣 Kampanya Merkezi</h3>'
        '<p style="color:#fef3c7;margin:0.3rem 0 0 0;font-size:0.9rem">'
        'AI destekli kampanya planlama + icerik uretimi + olcum + takvim</p></div>',
        unsafe_allow_html=True)

    kamp_tabs = st.tabs(["📣 Kampanyalar", "🎯 Sonuç Takip", "🤝 Referans", "🤖 AI İçerik", "📅 Takvim"])

    with kamp_tabs[1]:
        _render_kampanya_sonuc_takip(store, adaylar)
    with kamp_tabs[2]:
        _render_referans_sistemi(store, adaylar)
    with kamp_tabs[3]:
        _render_kampanya_ai_icerik(bugun)
    with kamp_tabs[4]:
        _render_kampanya_takvim(bugun.year)
    with kamp_tabs[0]:
        _render_kampanya_listesi(store, adaylar, bugun, secili_yil)
        # Kademe Bazlı Premium Kampanyalar
        _render_kademe_kampanyalar(bugun)


def _render_kampanya_listesi(store, adaylar, bugun, secili_yil):
    """Kampanya listesi alt sekmesi — mevcut kampanyalar + AI öneri."""
    # AI Kampanya Önerisi
    with st.expander("🤖 AI Kampanya Stratejisti — Bu Ay Ne Yapmalıyız?", expanded=False):
        _kamp_cache = f"_km_kamp_ai_{bugun.month}_{bugun.year}"
        if _kamp_cache in st.session_state:
            st.markdown(st.session_state[_kamp_cache])
        elif st.button("AI Kampanya Planı Oluştur", key="km_kamp_ai_btn", type="primary", use_container_width=True):
            with st.spinner("AI kampanya stratejisi hazırlıyor..."):
                from models.kayit_sifir_kayip import ai_kampanya_onerisi
                try:
                    from utils.shared_data import load_kurum_profili
                    kp = load_kurum_profili()
                    kurum = kp.get("kurum_adi", kp.get("name", "")) or ""
                except Exception:
                    kurum = ""
                aktif_sayi = sum(1 for a in adaylar if a.aktif)
                result = ai_kampanya_onerisi(bugun.month, kurum, aktif_sayi)
                if result:
                    st.session_state[_kamp_cache] = result
                    st.markdown(result)

    # Otomatik olustur (yoksa)
    store.ensure_kampanyalar(secili_yil)
    tum_kamp = store.load_kampanyalar()
    yil_kamp = [k for k in tum_kamp if k.get("yil") == secili_yil]

    # Kampanya istatistikleri
    aktif_ay = bugun.month
    bu_ay_kamp = [k for k in yil_kamp if k.get("ay") == aktif_ay]
    toplam_maliyet = sum(k.get("maliyet", 0) for k in yil_kamp)
    # Kampanya bazli aday sayisi
    kamp_adlari = set(k.get("ad", "") for k in yil_kamp)
    kamp_aday_sayac = {ad: sum(1 for a in adaylar if a.kampanya and ad.lower().startswith(a.kampanya.lower()[:8])) for ad in kamp_adlari}

    mc = st.columns(4)
    _stats = [
        (mc[0], f"{_AY_IKON.get(aktif_ay, '📅')} Bu Ay", len(bu_ay_kamp), _AY_RENK.get(aktif_ay, "#f59e0b")),
        (mc[1], "Yillik Toplam", len(yil_kamp), "#6366f1"),
        (mc[2], "Toplam Maliyet", f"{toplam_maliyet:,.0f}₺", "#ef4444"),
        (mc[3], "Aktif Ay", f"{AY_ADLARI[aktif_ay - 1]}", "#10b981"),
    ]
    for col, lbl, val, clr in _stats:
        with col:
            st.markdown(
                f'<div style="background:{clr}12;border:2px solid {clr}30;border-radius:10px;'
                f'padding:10px;text-align:center">'
                f'<div style="font-size:1.4rem;font-weight:800;color:{clr}">{val}</div>'
                f'<div style="font-size:0.65rem;color:#94a3b8">{lbl}</div></div>',
                unsafe_allow_html=True)

    st.markdown("")

    # Ay secici
    ay_secenekler = [f"{_AY_IKON.get(i, '')} {AY_ADLARI[i - 1]}" for i in range(1, 13)]
    secili_ay_idx = st.selectbox("Ay Sec", range(12), index=aktif_ay - 1,
                                  format_func=lambda i: ay_secenekler[i], key="kmp_ay_sec")
    secili_ay = secili_ay_idx + 1
    ay_renk = _AY_RENK.get(secili_ay, "#f59e0b")
    ay_ikon = _AY_IKON.get(secili_ay, "📅")

    # Bu ayin kampanyalari
    ay_kamp = sorted([k for k in yil_kamp if k.get("ay") == secili_ay],
                     key=lambda x: (0 if x.get("sabit") else 1, x.get("ad", "")))

    st.markdown(
        f'<div style="background:{ay_renk}12;border:2px solid {ay_renk}30;border-radius:12px;'
        f'padding:1rem 1.5rem;margin:0.5rem 0">'
        f'<div style="display:flex;justify-content:space-between;align-items:center">'
        f'<div><span style="font-size:1.3rem">{ay_ikon}</span> '
        f'<strong style="color:{ay_renk};font-size:1.1rem">{AY_ADLARI[secili_ay - 1]} {secili_yil}</strong>'
        f'<span style="color:#94a3b8;font-size:0.85rem;margin-left:8px">({len(ay_kamp)} kampanya)</span></div>'
        f'<div style="font-size:1.5rem;font-weight:800;color:{ay_renk}">'
        f'{sum(k.get("maliyet", 0) for k in ay_kamp):,.0f}₺</div></div></div>',
        unsafe_allow_html=True)

    # Kampanya kartlari
    if not ay_kamp:
        styled_info_banner(f"{AY_ADLARI[secili_ay - 1]} icin kampanya tanimlanmamis.", "info")
    else:
        for idx, k in enumerate(ay_kamp):
            k_id = k.get("id", "")
            sabit = k.get("sabit", False)
            badge = '<span style="background:#059669;color:#fff;padding:2px 8px;border-radius:10px;font-size:0.65rem;font-weight:700">SABİT</span>' if sabit else '<span style="background:#6366f1;color:#fff;padding:2px 8px;border-radius:10px;font-size:0.65rem;font-weight:700">MANUEL</span>'
            araclar_pills = " ".join(
                f'<span style="background:#1e293b;color:#94a3b8;padding:2px 8px;border-radius:10px;font-size:0.68rem">{a}</span>'
                for a in k.get("araclar", [])[:6]
            )
            maliyet = k.get("maliyet", 0)
            maliyet_clr = "#ef4444" if maliyet > 30000 else ("#f59e0b" if maliyet > 10000 else "#4ade80")

            # KPI bar (varsa)
            kpi = k.get("kpiler", {})
            kpi_html = ""
            if kpi:
                kpi_html = (
                    f'<div style="margin-top:8px;padding:8px 10px;background:#0f172a;border-radius:8px;'
                    f'border:1px solid #1e293b">'
                    f'<div style="font-size:0.68rem;font-weight:700;color:#f59e0b;margin-bottom:4px">PERFORMANS HEDEFLERİ</div>'
                    f'<div style="display:flex;flex-wrap:wrap;gap:6px">'
                    f'<span style="background:#3b82f615;border:1px solid #3b82f640;color:#60a5fa;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600">'
                    f'Günlük: {kpi.get("gunluk_arama", 0)} arama</span>'
                    f'<span style="background:#6366f115;border:1px solid #6366f140;color:#a5b4fc;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600">'
                    f'Aylık: {kpi.get("aylik_arama", 0)} arama</span>'
                    f'<span style="background:#10b98115;border:1px solid #10b98140;color:#34d399;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600">'
                    f'Ulaşma: %{kpi.get("ulasma_yuzde", 0)}</span>'
                    f'<span style="background:#f59e0b15;border:1px solid #f59e0b40;color:#fbbf24;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600">'
                    f'Görüşme: %{kpi.get("gorusme_yuzde", 0)}</span>'
                    f'<span style="background:#8b5cf615;border:1px solid #8b5cf640;color:#c4b5fd;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600">'
                    f'Randevu: %{kpi.get("randevu_yuzde", 0)}</span>'
                    f'<span style="background:#22c55e15;border:1px solid #22c55e40;color:#4ade80;padding:2px 8px;border-radius:6px;font-size:0.7rem;font-weight:600">'
                    f'Kayıt: %{kpi.get("kayit_yuzde", 0)}</span>'
                    f'</div></div>'
                )

            st.markdown(
                f'<div style="background:#111827;border:1px solid #1e293b;border-left:4px solid {ay_renk};'
                f'border-radius:0 10px 10px 0;padding:12px 16px;margin:6px 0">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">'
                f'<div style="flex:1;min-width:200px">'
                f'<div style="display:flex;align-items:center;gap:8px">'
                f'<strong style="color:#e2e8f0;font-size:0.95rem">{k.get("ad", "")}</strong> {badge}</div>'
                f'<div style="color:#94a3b8;font-size:0.8rem;margin-top:4px">{k.get("aciklama", "")}</div>'
                f'<div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:4px">{araclar_pills}</div></div>'
                f'<div style="text-align:right;min-width:120px">'
                f'<div style="font-size:1.1rem;font-weight:800;color:{maliyet_clr}">{maliyet:,.0f}₺</div>'
                f'<div style="font-size:0.7rem;color:#64748b">Sorumlu: {k.get("sorumlu", "-")}</div>'
                f'</div></div>{kpi_html}</div>',
                unsafe_allow_html=True)

            # Görevli atama (data arama kampanyalari icin)
            gorevliler = k.get("gorevliler")
            if gorevliler is not None:
                with st.expander(f"👥 Görevli Ata — {k.get('ad', '')[:30]}", expanded=False):
                    try:
                        from utils.shared_data import get_ik_employee_names
                        _p_list = [""] + get_ik_employee_names()
                    except Exception:
                        _p_list = [""]
                    gc1, gc2, gc3 = st.columns(3)
                    with gc1:
                        _ar = st.selectbox("📞 Arayan", _p_list,
                                           index=_p_list.index(gorevliler.get("arayan", "")) if gorevliler.get("arayan", "") in _p_list else 0,
                                           key=f"kmp_gr_ar_{k_id}_{secili_ay}")
                    with gc2:
                        _gr = st.selectbox("🤝 Görüşmeci", _p_list,
                                           index=_p_list.index(gorevliler.get("gorusmeci", "")) if gorevliler.get("gorusmeci", "") in _p_list else 0,
                                           key=f"kmp_gr_gr_{k_id}_{secili_ay}")
                    with gc3:
                        _sz = st.selectbox("📄 Sözleşmeci", _p_list,
                                           index=_p_list.index(gorevliler.get("sozlesmeci", "")) if gorevliler.get("sozlesmeci", "") in _p_list else 0,
                                           key=f"kmp_gr_sz_{k_id}_{secili_ay}")
                    if st.button("Görevlileri Kaydet", key=f"kmp_gr_save_{k_id}_{secili_ay}", use_container_width=True):
                        k["gorevliler"] = {"arayan": _ar, "gorusmeci": _gr, "sozlesmeci": _sz}
                        store.update_kampanya(k_id, {"gorevliler": k["gorevliler"]})
                        st.success("Görevliler kaydedildi!")
                        st.rerun()

            # Düzenle / İptal / Sil butonları
            _durum = k.get("durum", "aktif")
            if _durum == "iptal":
                st.markdown(
                    '<div style="background:#ef444420;border:1px solid #ef4444;border-radius:8px;'
                    'padding:6px 12px;text-align:center;font-size:0.8rem;font-weight:700;color:#ef4444">'
                    '❌ İPTAL EDİLDİ</div>', unsafe_allow_html=True)

            with st.expander(f"✏️ Düzenle — {k.get('ad', '')[:30]}", expanded=False):
                with st.form(f"kmp_edit_{k_id}_{secili_ay}"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        e_ad = st.text_input("Kampanya Adı", value=k.get("ad", ""), key=f"kmp_e_ad_{k_id}_{secili_ay}")
                    with ec2:
                        e_maliyet = st.number_input("Maliyet (TL)", min_value=0, step=1000,
                                                     value=int(k.get("maliyet", 0)), key=f"kmp_e_mal_{k_id}_{secili_ay}")
                    ec3, ec4 = st.columns(2)
                    with ec3:
                        e_sorumlu = st.text_input("Sorumlu", value=k.get("sorumlu", ""), key=f"kmp_e_sor_{k_id}_{secili_ay}")
                    with ec4:
                        e_araclar = st.multiselect("Araçlar", KAMPANYA_ARACLARI,
                                                    default=k.get("araclar", []), key=f"kmp_e_ara_{k_id}_{secili_ay}")
                    e_aciklama = st.text_area("Açıklama", value=k.get("aciklama", ""), height=68,
                                               key=f"kmp_e_ack_{k_id}_{secili_ay}")
                    e_durum = st.selectbox("Durum", ["aktif", "iptal", "tamamlandi"],
                                            index=["aktif", "iptal", "tamamlandi"].index(_durum) if _durum in ("aktif", "iptal", "tamamlandi") else 0,
                                            key=f"kmp_e_dur_{k_id}_{secili_ay}")

                    if st.form_submit_button("Değişiklikleri Kaydet", type="primary", use_container_width=True):
                        store.update_kampanya(k_id, {
                            "ad": e_ad,
                            "maliyet": e_maliyet,
                            "sorumlu": e_sorumlu,
                            "araclar": e_araclar,
                            "aciklama": e_aciklama,
                            "durum": e_durum,
                        })
                        st.success(f'"{e_ad}" güncellendi!')
                        st.rerun()

            # Hızlı butonlar
            _btn_cols = st.columns(3)
            with _btn_cols[0]:
                if _durum != "iptal":
                    if st.button("❌ İptal Et", key=f"kmp_iptal_{k_id}_{secili_ay}"):
                        store.update_kampanya(k_id, {"durum": "iptal"})
                        st.success(f'"{k.get("ad", "")}" iptal edildi.')
                        st.rerun()
                else:
                    if st.button("✅ Tekrar Aktif", key=f"kmp_aktif_{k_id}_{secili_ay}"):
                        store.update_kampanya(k_id, {"durum": "aktif"})
                        st.success(f'"{k.get("ad", "")}" tekrar aktif edildi.')
                        st.rerun()
            with _btn_cols[2]:
                if not sabit:
                    if st.button("🗑️ Sil", key=f"kmp_sil_{k_id}_{secili_ay}",
                                 help=f'{k.get("ad", "")} kampanyasini sil'):
                        store.delete_kampanya(k_id)
                        st.success(f'"{k.get("ad", "")}" silindi.')
                        st.rerun()

    # ── Yeni Kampanya Ekle ──
    st.markdown("---")
    st.markdown(
        f'<div style="background:#6366f115;border-left:4px solid #6366f1;border-radius:0 10px 10px 0;'
        f'padding:10px 14px;margin-bottom:10px">'
        f'<strong style="color:#a5b4fc;font-size:0.95rem">➕ {AY_ADLARI[secili_ay - 1]} Ayina Yeni Kampanya Ekle</strong></div>',
        unsafe_allow_html=True)

    with st.form(f"kmp_yeni_{secili_ay}", clear_on_submit=True):
        fc1, fc2 = st.columns(2)
        with fc1:
            yeni_ad = st.text_input("Kampanya Adi *", placeholder="Orn: Ozel Indirim Kampanyasi", key=f"kmp_ad_{secili_ay}")
        with fc2:
            yeni_maliyet = st.number_input("Maliyet (TL)", min_value=0, step=1000, key=f"kmp_mal_{secili_ay}")
        fc3, fc4 = st.columns(2)
        with fc3:
            yeni_sorumlu = st.text_input("Sorumlu", value="Kayit Ofisi", key=f"kmp_sor_{secili_ay}")
        with fc4:
            yeni_araclar = st.multiselect("Araclar", KAMPANYA_ARACLARI, key=f"kmp_ara_{secili_ay}")
        yeni_aciklama = st.text_input("Aciklama", placeholder="Kampanya aciklamasi...", key=f"kmp_ack_{secili_ay}")

        if st.form_submit_button("Kampanya Ekle", type="primary", use_container_width=True):
            if not yeni_ad:
                st.error("Kampanya adi zorunludur.")
            else:
                import uuid as _uuid
                store.add_kampanya({
                    "id": f"kmp_{_uuid.uuid4().hex[:8]}",
                    "ad": yeni_ad,
                    "ay": secili_ay,
                    "yil": secili_yil,
                    "maliyet": yeni_maliyet,
                    "sorumlu": yeni_sorumlu,
                    "araclar": yeni_araclar,
                    "aciklama": yeni_aciklama,
                    "durum": "aktif",
                    "sabit": False,
                })
                st.success(f'"{yeni_ad}" — {AY_ADLARI[secili_ay - 1]} ayina eklendi!')
                st.rerun()

    # ── Yillik Ozet Tablosu ──
    with st.expander("📊 Yillik Kampanya Ozeti", expanded=False):
        for ay_no in range(1, 13):
            ak = [k for k in yil_kamp if k.get("ay") == ay_no]
            if not ak:
                continue
            r = _AY_RENK.get(ay_no, "#94a3b8")
            i = _AY_IKON.get(ay_no, "📅")
            m = sum(k.get("maliyet", 0) for k in ak)
            aktif_mark = " ◀" if ay_no == aktif_ay else ""
            names = ", ".join(k.get("ad", "")[:20] for k in ak[:4])
            if len(ak) > 4:
                names += f" +{len(ak) - 4}"
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:10px;padding:6px 10px;margin:2px 0;'
                f'background:{"#1e293b" if ay_no != aktif_ay else f"{r}15"};border-radius:6px;'
                f'border-left:3px solid {r}">'
                f'<span style="min-width:100px;color:{r};font-weight:700">{i} {AY_ADLARI[ay_no - 1]}{aktif_mark}</span>'
                f'<span style="min-width:30px;color:{r};font-weight:800">{len(ak)}</span>'
                f'<span style="flex:1;color:#94a3b8;font-size:0.8rem">{names}</span>'
                f'<span style="color:{"#ef4444" if m > 30000 else "#f59e0b"};font-weight:700;min-width:80px;text-align:right">'
                f'{m:,.0f}₺</span></div>',
                unsafe_allow_html=True)

    # ── PDF RAPOR INDIRME ──
    st.markdown("---")
    st.markdown(
        '<div style="background:#17255415;border-left:4px solid #3b82f6;border-radius:0 10px 10px 0;'
        'padding:10px 14px;margin-bottom:10px">'
        '<strong style="color:#93c5fd;font-size:0.95rem">📥 Kampanya Raporu Indir</strong></div>',
        unsafe_allow_html=True)

    pdf_tur = st.radio("Rapor Turu", ["Aylik", "Yillik"], horizontal=True, key="kmp_pdf_tur")

    if pdf_tur == "Aylik":
        pdf_ay = st.selectbox("Ay", range(12), index=secili_ay - 1,
                               format_func=lambda i: f"{_AY_IKON.get(i + 1, '')} {AY_ADLARI[i]}",
                               key="kmp_pdf_ay")
        pdf_kamp = [k for k in yil_kamp if k.get("ay") == pdf_ay + 1]
        pdf_baslik = f"{AY_ADLARI[pdf_ay]} {secili_yil}"
    else:
        pdf_kamp = yil_kamp
        pdf_baslik = f"{secili_yil} Yili"

    pdf_bytes = _generate_kampanya_pdf(pdf_kamp, pdf_baslik, secili_yil, adaylar)
    if pdf_bytes:
        st.download_button(
            f"📥 {pdf_baslik} Kampanya Raporu PDF",
            data=pdf_bytes,
            file_name=f"Kampanya_Raporu_{pdf_baslik.replace(' ', '_')}.pdf",
            mime="application/pdf",
            key="kmp_pdf_indir",
            use_container_width=True)


def _generate_kampanya_pdf(kampanyalar: list[dict], baslik: str, yil: int,
                            adaylar: list) -> bytes | None:
    """Kampanya raporu PDF — aylik veya yillik."""
    try:
        from utils.report_utils import ReportPDFGenerator
        from utils.shared_data import load_kurum_profili
        import pandas as _pd

        kp = load_kurum_profili()
        k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")
        logo_path = kp.get("logo_path", "")

        pdf = ReportPDFGenerator(
            f"Kampanya Raporu — {baslik}",
            f"{k_adi} | Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        )
        pdf.add_header(k_adi, logo_path)

        # ── GENEL OZET ──
        pdf.add_section("Genel Ozet", "#f59e0b")
        toplam_kamp = len(kampanyalar)
        toplam_maliyet = sum(k.get("maliyet", 0) for k in kampanyalar)
        sabit_cnt = sum(1 for k in kampanyalar if k.get("sabit"))
        manuel_cnt = toplam_kamp - sabit_cnt
        pdf.add_metrics([
            ("Toplam Kampanya", toplam_kamp, "#f59e0b"),
            ("Toplam Maliyet", f"{toplam_maliyet:,.0f} TL", "#ef4444"),
            ("Sabit", sabit_cnt, "#10b981"),
            ("Manuel", manuel_cnt, "#6366f1"),
        ])
        pdf.add_spacer(0.3)

        # ── AY BAZLI KIRILIM ──
        aylar_set = sorted(set(k.get("ay", 0) for k in kampanyalar))
        for ay_no in aylar_set:
            if ay_no < 1 or ay_no > 12:
                continue
            ay_kamp = [k for k in kampanyalar if k.get("ay") == ay_no]
            ay_maliyet = sum(k.get("maliyet", 0) for k in ay_kamp)
            renk = _AY_RENK.get(ay_no, "#f59e0b")

            pdf.add_section(
                f"{_AY_IKON.get(ay_no, '')} {AY_ADLARI[ay_no - 1]} {yil} — {len(ay_kamp)} Kampanya — {ay_maliyet:,.0f} TL",
                renk)

            rows = []
            for k in ay_kamp:
                tur = "Sabit" if k.get("sabit") else "Manuel"
                arac_str = ", ".join(k.get("araclar", [])[:5])
                rows.append({
                    "Kampanya": k.get("ad", "")[:30],
                    "Tur": tur,
                    "Maliyet": f'{k.get("maliyet", 0):,.0f} TL',
                    "Sorumlu": k.get("sorumlu", "-")[:15],
                    "Araclar": arac_str[:40],
                })
            pdf.add_table(_pd.DataFrame(rows), renk)

            # Her kampanyanin aciklamasi
            for k in ay_kamp:
                aciklama = k.get("aciklama", "")
                if aciklama:
                    pdf.add_text(f"▸ {k.get('ad', '')}: {aciklama}")
            pdf.add_spacer(0.2)

        # ── MALIYET DAGILIMI GRAFIGI ──
        if len(aylar_set) > 1:
            pdf.add_section("Maliyet Dagilimi", "#7c3aed")
            maliyet_data = {}
            for ay_no in aylar_set:
                if ay_no < 1 or ay_no > 12:
                    continue
                m = sum(k.get("maliyet", 0) for k in kampanyalar if k.get("ay") == ay_no)
                if m > 0:
                    maliyet_data[AY_ADLARI[ay_no - 1]] = m
            if maliyet_data:
                renk_listesi = [_AY_RENK.get(ay_no, "#94a3b8") for ay_no in aylar_set if ay_no >= 1 and ay_no <= 12]
                pdf.add_donut_chart(maliyet_data, "Aylara Gore Maliyet Dagilimi", renk_listesi)

            # Maliyet tablosu
            mal_rows = []
            for ay_no in aylar_set:
                if ay_no < 1 or ay_no > 12:
                    continue
                ak = [k for k in kampanyalar if k.get("ay") == ay_no]
                m = sum(k.get("maliyet", 0) for k in ak)
                mal_rows.append({
                    "Ay": f"{AY_ADLARI[ay_no - 1]}",
                    "Kampanya Sayisi": len(ak),
                    "Maliyet": f"{m:,.0f} TL",
                })
            mal_rows.append({
                "Ay": "TOPLAM",
                "Kampanya Sayisi": toplam_kamp,
                "Maliyet": f"{toplam_maliyet:,.0f} TL",
            })
            pdf.add_table(_pd.DataFrame(mal_rows), "#7c3aed")

        # ── ARAC DAGILIMI ──
        pdf.add_section("Arac/Kanal Dagilimi", "#0ea5e9")
        from collections import Counter as _Counter
        arac_sayac = _Counter()
        for k in kampanyalar:
            for a in k.get("araclar", []):
                arac_sayac[a] += 1
        if arac_sayac:
            arac_rows = [{"Arac": a, "Kullanim": c} for a, c in arac_sayac.most_common()]
            pdf.add_table(_pd.DataFrame(arac_rows), "#0ea5e9")
            arac_chart = dict(arac_sayac.most_common(10))
            pdf.add_donut_chart(arac_chart, "En Cok Kullanilan Araclar")

        # ── KAMPANYA BAZLI ADAY SAYISI ──
        if adaylar:
            pdf.add_section("Kampanya Bazli Aday Sayisi", "#10b981")
            kamp_adlari = sorted(set(k.get("ad", "") for k in kampanyalar))
            aday_rows = []
            for ad in kamp_adlari:
                cnt = sum(1 for a in adaylar if a.kampanya and (
                    a.kampanya.lower() in ad.lower() or ad.lower().startswith(a.kampanya.lower()[:10])))
                kayit = sum(1 for a in adaylar if a.kampanya and a.asama == "kesin_kayit" and (
                    a.kampanya.lower() in ad.lower() or ad.lower().startswith(a.kampanya.lower()[:10])))
                if cnt > 0:
                    aday_rows.append({"Kampanya": ad[:35], "Aday": cnt, "Kayit": kayit})
            if aday_rows:
                pdf.add_table(_pd.DataFrame(aday_rows), "#10b981")

        pdf.add_spacer(0.5)
        pdf.add_text(f"Bu rapor {datetime.now().strftime('%d.%m.%Y %H:%M')} tarihinde SmartCampus AI tarafindan olusturulmustur.")

        return pdf.generate()
    except Exception:
        return None


# ============================================================
# KAMPANYA — AI İÇERİK ÜRETİCİ
# ============================================================

def _render_kademe_kampanyalar(bugun):
    """Kademe bazlı premium kampanyalar — aya göre filtrelenen."""
    from models.kayit_modulu import KADEME_KAMPANYALAR
    ay = bugun.month

    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#8b5cf6,#6d28d9);color:#fff;'
        'padding:14px 18px;border-radius:10px;margin:8px 0;">'
        '<b>🎯 Kademe Bazlı Premium Kampanyalar</b>'
        '<p style="margin:2px 0 0;font-size:11px;opacity:.85;">'
        'Her kademeye özel, aya göre filtrelenen kampanya önerileri</p></div>',
        unsafe_allow_html=True)

    kademe_renkler = {
        "Anaokulu": ("#f59e0b", "🧒"),
        "Ilkokul": ("#10b981", "📗"),
        "Ortaokul": ("#3b82f6", "📘"),
        "Lise": ("#8b5cf6", "📕"),
    }

    for kademe, kampanyalar in KADEME_KAMPANYALAR.items():
        # Bu ay aktif olanlar
        bu_ay = [k for k in kampanyalar if ay in k.get("aylar", [])]
        diger = [k for k in kampanyalar if ay not in k.get("aylar", [])]
        renk, ikon = kademe_renkler.get(kademe, ("#64748b", "📄"))

        with st.expander(f"{ikon} {kademe} ({len(bu_ay)} aktif / {len(kampanyalar)} toplam)", expanded=bool(bu_ay)):
            if bu_ay:
                st.markdown(f'<div style="color:{renk};font-weight:700;font-size:13px;margin-bottom:6px;">'
                            f'Bu Ay Aktif Kampanyalar:</div>', unsafe_allow_html=True)
                for k in bu_ay:
                    st.markdown(
                        f'<div style="background:{renk}12;border-left:3px solid {renk};'
                        f'padding:10px 14px;border-radius:0 8px 8px 0;margin:4px 0;">'
                        f'<div style="font-weight:700;color:{renk};font-size:13px;">{k["ad"]}</div>'
                        f'<div style="color:#94a3b8;font-size:11px;margin-top:2px;">Hedef: {k.get("hedef", "-")}</div>'
                        f'<div style="color:#cbd5e1;font-size:12px;margin-top:4px;font-style:italic;">"{k.get("mesaj", "")}"</div>'
                        f'<div style="color:#64748b;font-size:11px;margin-top:4px;">{k.get("aciklama", "")}</div>'
                        f'<div style="color:#94a3b8;font-size:10px;margin-top:2px;">'
                        f'Kanallar: {", ".join(k.get("araclar", []))} | Bütçe: {k.get("maliyet", 0):,} TL</div></div>',
                        unsafe_allow_html=True)
            if diger:
                st.markdown(f'<div style="color:#64748b;font-size:11px;margin-top:6px;">Diğer aylar ({len(diger)}):</div>',
                            unsafe_allow_html=True)
                for k in diger:
                    ay_adlari = {1: "Oca", 2: "Şub", 3: "Mar", 4: "Nis", 5: "May", 6: "Haz",
                                 7: "Tem", 8: "Ağu", 9: "Eyl", 10: "Eki", 11: "Kas", 12: "Ara"}
                    aylar_str = ", ".join(ay_adlari.get(a, "?") for a in k.get("aylar", []))
                    st.markdown(f'<div style="color:#64748b;font-size:11px;padding:2px 0;">'
                                f'• {k["ad"]} ({aylar_str})</div>', unsafe_allow_html=True)


def _render_kampanya_sonuc_takip(store: KayitDataStore, adaylar: list[KayitAday]):
    """Kampanya sonuç takibi — başlat/durdur + hedef/gerçekleşen + ROI."""
    import plotly.graph_objects as go

    st.markdown(
        '<div style="background:linear-gradient(135deg,#10b981,#059669);color:#fff;'
        'padding:14px 18px;border-radius:10px;margin-bottom:12px;">'
        '<b>🎯 Kampanya Sonuç Takibi</b>'
        '<p style="margin:2px 0 0;font-size:11px;opacity:.85;">'
        'Her kampanyanın durumu, hedefi, gerçekleşeni, ROI — tek ekranda</p></div>',
        unsafe_allow_html=True)

    sonuclar = store.kampanya_sonuclari(adaylar)
    if not sonuclar:
        st.info("Henüz kampanya verisi yok.")
        return

    # Filtre
    bugun = date.today()
    tum_kamp = store.load_kampanyalar()
    fc1, fc2 = st.columns(2)
    with fc1:
        durum_f = st.selectbox("Durum:", ["Tümü", "aktif", "beklemede", "tamamlandi"], key="kst_durum")
    with fc2:
        ay_f = st.selectbox("Ay:", ["Tümü"] + list(range(1, 13)),
                             format_func=lambda x: {1: "Oca", 2: "Şub", 3: "Mar", 4: "Nis", 5: "May", 6: "Haz",
                                                     7: "Tem", 8: "Ağu", 9: "Eyl", 10: "Eki", 11: "Kas", 12: "Ara"}.get(x, str(x)) if x != "Tümü" else "Tümü",
                             key="kst_ay")

    # Genel istatistik
    toplam_aday = sum(s["aday_sayisi"] for s in sonuclar.values())
    toplam_kayit = sum(s["kayit_sayisi"] for s in sonuclar.values())
    toplam_butce = sum(s["kampanya"].get("maliyet", 0) for s in sonuclar.values())
    genel_don = (toplam_kayit / toplam_aday * 100) if toplam_aday > 0 else 0

    sc = st.columns(4)
    with sc[0]:
        st.metric("Toplam Aday", str(toplam_aday))
    with sc[1]:
        st.metric("Toplam Kayıt", str(toplam_kayit))
    with sc[2]:
        st.metric("Genel Dönüşüm", f"%{genel_don:.0f}")
    with sc[3]:
        maliyet_kayit = (toplam_butce / max(toplam_kayit, 1))
        st.metric("Kayıt Başı Maliyet", f"{maliyet_kayit:,.0f} TL")

    st.markdown("---")

    # Kampanya listesi — detaylı
    for kid, s in sorted(sonuclar.items(), key=lambda x: x[1]["aday_sayisi"], reverse=True):
        k = s["kampanya"]
        if durum_f != "Tümü" and k.get("durum", "") != durum_f:
            continue
        if ay_f != "Tümü" and k.get("ay") != ay_f:
            continue

        durum = k.get("durum", "beklemede")
        d_clr = {"aktif": "#22c55e", "beklemede": "#f59e0b", "tamamlandi": "#3b82f6", "iptal": "#ef4444"}.get(durum, "#64748b")
        d_icon = {"aktif": "🟢", "beklemede": "🟡", "tamamlandi": "🔵", "iptal": "🔴"}.get(durum, "⚪")
        hedef_a = k.get("hedef_aday", 0)
        hedef_k = k.get("hedef_kayit", 0)

        with st.expander(f'{d_icon} {k.get("ad", "?")} — {s["aday_sayisi"]} aday, {s["kayit_sayisi"]} kayıt ({durum})'):
            # Üst bilgi
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                st.markdown(f'**Ay:** {k.get("ay", "?")} | **Yıl:** {k.get("yil", "")}')
                st.markdown(f'**Bütçe:** {k.get("maliyet", 0):,} TL')
                st.markdown(f'**Kanallar:** {", ".join(k.get("araclar", []))}')
            with ic2:
                st.markdown(f'**Aday:** {s["aday_sayisi"]} (hedef: {hedef_a or "-"})')
                st.markdown(f'**Kayıt:** {s["kayit_sayisi"]} (hedef: {hedef_k or "-"})')
                st.markdown(f'**Dönüşüm:** %{s["donusum"]:.0f}')
            with ic3:
                st.markdown(f'**Aktif:** {s["aktif_sayisi"]}')
                st.markdown(f'**Olumsuz:** {s["olumsuz_sayisi"]}')
                if hedef_a > 0:
                    pct = s["aday_sayisi"] / hedef_a * 100
                    st.markdown(f'**Hedef Başarı:** %{pct:.0f}')

            # Yönetim butonları
            bc1, bc2, bc3, bc4 = st.columns(4)
            with bc1:
                if durum != "aktif" and st.button("🟢 Başlat", key=f"kst_baslat_{kid}"):
                    store.update_kampanya(kid, {"durum": "aktif", "baslangic_tarihi": date.today().isoformat()})
                    st.rerun()
            with bc2:
                if durum == "aktif" and st.button("⏹ Durdur", key=f"kst_durdur_{kid}"):
                    store.update_kampanya(kid, {"durum": "tamamlandi", "bitis_tarihi": date.today().isoformat()})
                    st.rerun()
            with bc3:
                if st.button("🎯 Hedef Koy", key=f"kst_hedef_{kid}"):
                    st.session_state[f"_kst_hedef_edit_{kid}"] = True
            with bc4:
                if st.button("💰 Bütçe", key=f"kst_butce_{kid}"):
                    st.session_state[f"_kst_butce_edit_{kid}"] = True

            # Hedef düzenleme
            if st.session_state.get(f"_kst_hedef_edit_{kid}"):
                hc1, hc2, hc3 = st.columns(3)
                with hc1:
                    _ha = st.number_input("Hedef Aday", value=hedef_a, min_value=0, key=f"kst_ha_{kid}")
                with hc2:
                    _hk = st.number_input("Hedef Kayıt", value=hedef_k, min_value=0, key=f"kst_hk_{kid}")
                with hc3:
                    if st.button("Kaydet", key=f"kst_hkaydet_{kid}"):
                        store.update_kampanya(kid, {"hedef_aday": _ha, "hedef_kayit": _hk})
                        del st.session_state[f"_kst_hedef_edit_{kid}"]
                        st.rerun()

            # Bütçe düzenleme
            if st.session_state.get(f"_kst_butce_edit_{kid}"):
                _bh = st.number_input("Harcanan Bütçe (TL)", value=float(k.get("butce_harcanan", 0)),
                                       min_value=0.0, step=1000.0, key=f"kst_bh_{kid}")
                if st.button("Bütçe Kaydet", key=f"kst_bkaydet_{kid}"):
                    store.update_kampanya(kid, {"butce_harcanan": _bh})
                    del st.session_state[f"_kst_butce_edit_{kid}"]
                    st.rerun()

    # En iyi/en kötü kampanya
    if sonuclar:
        st.markdown("---")
        st.markdown("### En İyi vs En Kötü Kampanya")
        aktif_sonuclar = {k: v for k, v in sonuclar.items() if v["aday_sayisi"] > 0}
        if aktif_sonuclar:
            en_iyi = max(aktif_sonuclar.items(), key=lambda x: x[1]["donusum"])
            en_kotu = min(aktif_sonuclar.items(), key=lambda x: x[1]["donusum"])
            ci1, ci2 = st.columns(2)
            with ci1:
                st.markdown(f'<div style="background:#22c55e15;border-left:3px solid #22c55e;padding:10px;border-radius:0 8px 8px 0;">'
                            f'<b style="color:#22c55e;">🏆 En İyi:</b> {en_iyi[1]["kampanya"]["ad"]}<br>'
                            f'{en_iyi[1]["aday_sayisi"]} aday → {en_iyi[1]["kayit_sayisi"]} kayıt (%{en_iyi[1]["donusum"]:.0f})</div>',
                            unsafe_allow_html=True)
            with ci2:
                st.markdown(f'<div style="background:#ef444415;border-left:3px solid #ef4444;padding:10px;border-radius:0 8px 8px 0;">'
                            f'<b style="color:#ef4444;">⚠️ En Kötü:</b> {en_kotu[1]["kampanya"]["ad"]}<br>'
                            f'{en_kotu[1]["aday_sayisi"]} aday → {en_kotu[1]["kayit_sayisi"]} kayıt (%{en_kotu[1]["donusum"]:.0f})</div>',
                            unsafe_allow_html=True)

        # Top 10 bar grafik
        top10 = sorted(aktif_sonuclar.items(), key=lambda x: x[1]["aday_sayisi"], reverse=True)[:10]
        if top10:
            labels = [v["kampanya"]["ad"][:20] for _, v in top10]
            aday_vals = [v["aday_sayisi"] for _, v in top10]
            kayit_vals = [v["kayit_sayisi"] for _, v in top10]

            fig = go.Figure()
            fig.add_trace(go.Bar(name="Aday", x=labels, y=aday_vals, marker_color="#6366f1"))
            fig.add_trace(go.Bar(name="Kayıt", x=labels, y=kayit_vals, marker_color="#22c55e"))
            fig.update_layout(barmode='group', height=350, title="Top 10 Kampanya — Aday vs Kayıt",
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font=dict(color='#e2e8f0'), margin=dict(l=30, r=10, t=50, b=80),
                              xaxis=dict(tickangle=30))
            st.plotly_chart(fig, use_container_width=True, key="kst_top10")


def _render_referans_sistemi(store: KayitDataStore, adaylar: list[KayitAday]):
    """Referans/tavsiye sistemi — mevcut veliden gelen adaylar."""
    st.markdown(
        '<div style="background:linear-gradient(135deg,#8b5cf6,#6d28d9);color:#fff;'
        'padding:14px 18px;border-radius:10px;margin-bottom:12px;">'
        '<b>🤝 Referans & Tavsiye Sistemi</b>'
        '<p style="margin:2px 0 0;font-size:11px;opacity:.85;">'
        'Mevcut velilerden gelen tavsiyeler — en etkili aday kaynağı</p></div>',
        unsafe_allow_html=True)

    # Referanslı adaylar
    referansli = [a for a in adaylar if a.referans_veli]
    referanssiz = [a for a in adaylar if not a.referans_veli]

    # İstatistik
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1:
        st.metric("Referanslı Aday", str(len(referansli)))
    with rc2:
        ref_kayit = sum(1 for a in referansli if a.asama == "kesin_kayit")
        st.metric("Referanslı Kayıt", str(ref_kayit))
    with rc3:
        ref_don = (ref_kayit / len(referansli) * 100) if referansli else 0
        genel_don = (sum(1 for a in adaylar if a.asama == "kesin_kayit") / len(adaylar) * 100) if adaylar else 0
        st.metric("Referans Dönüşüm", f"%{ref_don:.0f}", delta=f"{ref_don - genel_don:+.0f}% genel fark")
    with rc4:
        # Kim en çok tavsiye etti
        tavsiyeciler = {}
        for a in referansli:
            t = a.referans_veli
            tavsiyeciler[t] = tavsiyeciler.get(t, 0) + 1
        en_cok = max(tavsiyeciler.items(), key=lambda x: x[1])[0] if tavsiyeciler else "-"
        st.metric("En Çok Tavsiye", en_cok)

    st.markdown("---")

    # Referans listesi
    if referansli:
        st.markdown("### Referansla Gelen Adaylar")
        for a in sorted(referansli, key=lambda x: x.olusturma_tarihi, reverse=True):
            d_clr = "#22c55e" if a.asama == "kesin_kayit" else "#f59e0b" if a.aktif else "#ef4444"
            st.markdown(
                f'<div style="background:{d_clr}10;border-left:3px solid {d_clr};'
                f'padding:6px 12px;border-radius:0 6px 6px 0;margin:3px 0;font-size:12px;">'
                f'<b>{a.ogrenci_adi}</b> (Veli: {a.veli_adi}) — {a.pipeline_info["label"]}'
                f'<br><span style="color:#94a3b8;">Tavsiye eden: <b>{a.referans_veli}</b>'
                f' ({a.referans_tipi or "?"})</span></div>',
                unsafe_allow_html=True)

    # Tavsiyeci sıralama
    if tavsiyeciler:
        st.markdown("### En Çok Tavsiye Edenler")
        for veli, cnt in sorted(tavsiyeciler.items(), key=lambda x: -x[1]):
            kayit_cnt = sum(1 for a in referansli if a.referans_veli == veli and a.asama == "kesin_kayit")
            st.markdown(f'<div style="background:#8b5cf615;border-left:2px solid #8b5cf6;'
                        f'padding:4px 10px;border-radius:0 4px 4px 0;margin:2px 0;font-size:12px;">'
                        f'<b>{veli}</b> — {cnt} tavsiye, {kayit_cnt} kayıt</div>',
                        unsafe_allow_html=True)

    if not referansli:
        st.info("Henüz referansla gelen aday yok. Yeni aday eklerken 'referans_veli' alanını doldurun.")


def _render_kampanya_ai_icerik(bugun):
    """AI ile kampanya içerik üretimi — kanal bazlı veya toplu paket."""
    from models.kayit_sifir_kayip import ai_kampanya_icerik, ai_toplu_icerik_paketi, AY_OZELLIKLERI
    ay_adlari = {1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
                 7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"}

    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff;'
        'padding:14px 18px;border-radius:10px;margin-bottom:12px;">'
        '<b>🤖 AI İçerik Üretici</b> — Kampanya için hazır kullanılacak içerikler üretin'
        '<p style="margin:2px 0 0;font-size:11px;opacity:.85;">'
        'Instagram, Facebook, WhatsApp, SMS, Email, Afiş, Broşür — hepsi tek tıkla</p></div>',
        unsafe_allow_html=True)

    try:
        from utils.shared_data import load_kurum_profili
        kp = load_kurum_profili()
        kurum = kp.get("kurum_adi", kp.get("name", "")) or ""
    except Exception:
        kurum = ""

    # Ay seçimi
    sel_ay = st.selectbox("Ay:", list(ay_adlari.keys()),
                           format_func=lambda x: f"{ay_adlari[x]} — {AY_OZELLIKLERI.get(x, {}).get('tema', '')}",
                           index=bugun.month - 1, key="kamp_ai_ay")

    # Ayın özellikleri kartı
    oz = AY_OZELLIKLERI.get(sel_ay, {})
    if oz:
        st.markdown(
            f'<div style="background:#f59e0b15;border-left:3px solid #f59e0b;padding:10px 14px;'
            f'border-radius:0 8px 8px 0;margin:6px 0;font-size:12px;">'
            f'<b>Tema:</b> {oz.get("tema", "-")}<br>'
            f'<b>MEB Takvim:</b> {oz.get("meb", "-")}<br>'
            f'<b>Fırsatlar:</b> {oz.get("firsatlar", "-")}<br>'
            f'<b>Hedef Kitle:</b> {oz.get("hedef_kitle", "-")}<br>'
            f'<b>Rakip Durum:</b> {oz.get("rakip_durum", "-")}</div>',
            unsafe_allow_html=True)

    st.markdown("---")

    # İki seçenek: Tek kanal veya Toplu paket
    mod = st.radio("Mod:", ["📦 Toplu İçerik Paketi (Tüm Kanallar)", "🎯 Tek Kanal İçerik"],
                    horizontal=True, key="kamp_ai_mod")

    if mod.startswith("📦"):
        kampanya_adi = st.text_input("Kampanya Adı:", placeholder="Erken Kayıt İndirimi", key="kamp_ai_toplu_ad")
        if st.button("📦 Toplu İçerik Paketi Üret", type="primary", use_container_width=True, key="kamp_ai_toplu_btn"):
            if not kampanya_adi:
                st.error("Kampanya adı girin.")
                return
            with st.spinner("AI tüm kanallar için içerik üretiyor..."):
                result = ai_toplu_icerik_paketi(kampanya_adi, sel_ay, kurum)
                if result:
                    st.session_state[f"_kamp_toplu_{sel_ay}"] = result
                    st.markdown(result)
                else:
                    st.error("API anahtarı bulunamadı.")
        if f"_kamp_toplu_{sel_ay}" in st.session_state:
            st.markdown(st.session_state[f"_kamp_toplu_{sel_ay}"])
    else:
        c1, c2 = st.columns(2)
        with c1:
            kampanya_adi = st.text_input("Kampanya Adı:", key="kamp_ai_tek_ad")
            hedef_kitle = st.text_input("Hedef Kitle:", placeholder="8. sınıf velileri", key="kamp_ai_hk")
        with c2:
            kanallar = ["Instagram", "Facebook", "WhatsApp", "SMS", "Email", "Google Ads",
                         "YouTube", "TikTok", "Billboard", "Brosur", "Website"]
            kanal = st.selectbox("Kanal:", kanallar, key="kamp_ai_kanal")
        if st.button(f"🎯 {kanal} İçeriği Üret", type="primary", use_container_width=True, key="kamp_ai_tek_btn"):
            if not kampanya_adi:
                st.error("Kampanya adı girin.")
                return
            with st.spinner(f"AI {kanal} içeriği üretiyor..."):
                result = ai_kampanya_icerik(kampanya_adi, hedef_kitle, kanal, sel_ay, kurum)
                if result:
                    st.session_state[f"_kamp_tek_{kanal}_{sel_ay}"] = result
                    st.markdown(result)
        _tek_key = f"_kamp_tek_{kanal}_{sel_ay}" if 'kanal' in dir() else ""
        if _tek_key and _tek_key in st.session_state:
            st.markdown(st.session_state[_tek_key])


# ============================================================
# KAMPANYA — PERFORMANS & ROI
# ============================================================

def _render_kampanya_performans_tab(store: KayitDataStore, adaylar: list[KayitAday]):
    """Kampanya performans analizi — dönüşüm, ROI, karşılaştırma."""
    import plotly.graph_objects as go

    st.markdown(
        '<div style="background:linear-gradient(135deg,#10b981,#059669);color:#fff;'
        'padding:14px 18px;border-radius:10px;margin-bottom:12px;">'
        '<b>📊 Kampanya Performans Analizi</b></div>',
        unsafe_allow_html=True)

    tum_kamp = store.load_kampanyalar()
    if not tum_kamp:
        st.info("Henüz kampanya verisi yok.")
        return

    # Kampanya bazlı aday sayısı
    kamp_data = {}
    for a in adaylar:
        k = a.kampanya or "Belirsiz"
        kamp_data.setdefault(k, {"aday": 0, "kayit": 0, "olumsuz": 0})
        kamp_data[k]["aday"] += 1
        if a.asama == "kesin_kayit":
            kamp_data[k]["kayit"] += 1
        elif a.asama == "olumsuz":
            kamp_data[k]["olumsuz"] += 1

    if not kamp_data:
        st.info("Adaylara kampanya atanmamış.")
        return

    # Tablo
    st.markdown("### Kampanya Bazlı Dönüşüm")
    rows = []
    for k, v in sorted(kamp_data.items(), key=lambda x: x[1]["aday"], reverse=True):
        donusum = (v["kayit"] / v["aday"] * 100) if v["aday"] > 0 else 0
        rows.append({"Kampanya": k[:30], "Aday": v["aday"], "Kayıt": v["kayit"],
                     "Olumsuz": v["olumsuz"], "Dönüşüm %": f"{donusum:.0f}%"})
    import pandas as pd
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Grafik — en iyi 10
    top10 = sorted(kamp_data.items(), key=lambda x: x[1]["aday"], reverse=True)[:10]
    if top10:
        labels = [k[:20] for k, v in top10]
        aday_vals = [v["aday"] for k, v in top10]
        kayit_vals = [v["kayit"] for k, v in top10]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Aday", x=labels, y=aday_vals, marker_color="#6366f1"))
        fig.add_trace(go.Bar(name="Kayıt", x=labels, y=kayit_vals, marker_color="#22c55e"))
        fig.update_layout(barmode='group', height=350, title="Kampanya Bazlı Aday vs Kayıt",
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font=dict(color='#cbd5e1'))
        st.plotly_chart(fig, use_container_width=True, key="kamp_perf_chart")

    # Kanal bazlı
    st.markdown("### Kanal Bazlı Dönüşüm")
    kanal_data = {}
    for a in adaylar:
        k = a.kanal or "Belirsiz"
        kanal_data.setdefault(k, {"aday": 0, "kayit": 0})
        kanal_data[k]["aday"] += 1
        if a.asama == "kesin_kayit":
            kanal_data[k]["kayit"] += 1

    if kanal_data:
        kanal_rows = []
        for k, v in sorted(kanal_data.items(), key=lambda x: x[1]["aday"], reverse=True):
            don = (v["kayit"] / v["aday"] * 100) if v["aday"] > 0 else 0
            kanal_rows.append({"Kanal": k, "Aday": v["aday"], "Kayıt": v["kayit"], "Dönüşüm %": f"{don:.0f}%"})
        df2 = pd.DataFrame(kanal_rows)
        st.dataframe(df2, use_container_width=True, hide_index=True)

    # AI Performans Analizi
    with st.expander("🤖 AI Performans Analizi"):
        if st.button("AI Analiz Yap", key="kamp_perf_ai_btn"):
            with st.spinner("AI kampanya performansını analiz ediyor..."):
                from models.kayit_sifir_kayip import ai_kampanya_performans
                stats = {
                    "toplam_kampanya": len(tum_kamp),
                    "toplam_aday": len(adaylar),
                    "kayit": sum(1 for a in adaylar if a.asama == "kesin_kayit"),
                    "olumsuz": sum(1 for a in adaylar if a.asama == "olumsuz"),
                    "en_iyi_kampanya": max(kamp_data.items(), key=lambda x: x[1]["kayit"])[0] if kamp_data else "-",
                    "en_iyi_kanal": max(kanal_data.items(), key=lambda x: x[1]["kayit"])[0] if kanal_data else "-",
                }
                result = ai_kampanya_performans(stats)
                if result:
                    st.markdown(result)


# ============================================================
# KAMPANYA — TAKVİM
# ============================================================

def _render_kampanya_takvim(yil: int):
    """Yıllık kampanya takvimi — görsel."""
    from models.kayit_sifir_kayip import AY_OZELLIKLERI

    st.markdown(
        '<div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;'
        'padding:14px 18px;border-radius:10px;margin-bottom:12px;">'
        f'<b>📅 {yil} Kampanya Takvimi</b></div>',
        unsafe_allow_html=True)

    ay_adlari = {1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
                 7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"}

    # Yoğunluk renkleri
    yogunluk = {
        1: "#3b82f6", 2: "#3b82f6", 3: "#f59e0b", 4: "#f59e0b",
        5: "#f97316", 6: "#ef4444", 7: "#ef4444", 8: "#f97316",
        9: "#f59e0b", 10: "#3b82f6", 11: "#3b82f6", 12: "#f59e0b",
    }

    # 4x3 grid
    for row in range(4):
        cols = st.columns(3)
        for col_idx in range(3):
            ay = row * 3 + col_idx + 1
            oz = AY_OZELLIKLERI.get(ay, {})
            renk = yogunluk.get(ay, "#64748b")
            bugun = date.today()
            aktif = "border:3px solid #fff;" if ay == bugun.month and yil == bugun.year else ""
            with cols[col_idx]:
                st.markdown(
                    f'<div style="background:{renk}20;border-left:4px solid {renk};{aktif}'
                    f'border-radius:0 10px 10px 0;padding:10px 12px;margin:4px 0;min-height:100px;">'
                    f'<div style="font-size:14px;font-weight:800;color:{renk};">{ay_adlari[ay]}</div>'
                    f'<div style="font-size:10px;color:#94a3b8;margin-top:2px;">{oz.get("tema", "-")}</div>'
                    f'<div style="font-size:9px;color:#64748b;margin-top:4px;">'
                    f'MEB: {oz.get("meb", "-")[:40]}</div>'
                    f'<div style="font-size:9px;color:{renk};margin-top:2px;font-weight:600;">'
                    f'{oz.get("firsatlar", "-")[:50]}</div></div>',
                    unsafe_allow_html=True)


# ============================================================
# PIPELINE
# ============================================================

def _render_pipeline(store: KayitDataStore, adaylar: list[KayitAday]):
    # Kanban gorunum
    try:
        from utils.ui_common import kanban_panosu
        pipeline_kanban = {
            "Aday": [{"baslik": a.label, "atanan": "", "renk": "#94A3B8"} for a in adaylar if a.asama == "aday"][:5],
            "Arandi": [{"baslik": a.label, "atanan": "", "renk": "#3B82F6"} for a in adaylar if a.asama == "arandi"][:5],
            "Randevu": [{"baslik": a.label, "atanan": "", "renk": "#0891B2"} for a in adaylar if a.asama == "randevu"][:5],
            "Gorusme": [{"baslik": a.label, "atanan": "", "renk": "#7C3AED"} for a in adaylar if a.asama == "gorusme"][:5],
            "Fiyat": [{"baslik": a.label, "atanan": "", "renk": "#F59E0B"} for a in adaylar if a.asama == "fiyat_verildi"][:5],
            "Sozlesme": [{"baslik": a.label, "atanan": "", "renk": "#10B981"} for a in adaylar if a.asama == "sozlesme"][:5],
            "Kayit": [{"baslik": a.label, "atanan": "", "renk": "#059669"} for a in adaylar if a.asama == "kesin_kayit"][:5],
        }
        with st.expander("🗂️ Kanban Görünüm (Pipeline)", expanded=False):
            kanban_panosu(pipeline_kanban, "kayit_modulu")
    except Exception:
        pass

    sayac = store.pipeline_sayac()

    # Sayac bari
    cols = st.columns(len(PIPELINE_ASAMALARI) + 1)
    for i, key in enumerate(PIPELINE_ASAMALARI):
        info = PIPELINE_INFO[key]
        cnt = sayac.get(key, 0)
        with cols[i]:
            st.markdown(
                f'<div style="text-align:center;padding:10px 2px;background:{info["bg"]};'
                f'border:2px solid {info["color"]}40;border-radius:10px">'
                f'<div style="font-size:1.4rem;font-weight:800;color:{info["color"]}">{cnt}</div>'
                f'<div style="font-size:0.6rem;font-weight:700;color:{info["color"]}">'
                f'{info["emoji"]} {info["label"]}</div></div>',
                unsafe_allow_html=True)
    with cols[-1]:
        olumsuz = sayac.get("olumsuz", 0)
        st.markdown(
            f'<div style="text-align:center;padding:10px 2px;background:#450a0a;'
            f'border:2px solid #f8717140;border-radius:10px">'
            f'<div style="font-size:1.4rem;font-weight:800;color:#f87171">{olumsuz}</div>'
            f'<div style="font-size:0.6rem;font-weight:700;color:#f87171">❌ Olumsuz</div></div>',
            unsafe_allow_html=True)

    st.markdown("")

    # Filtre
    filtre = st.selectbox("Asama", ["Tumu (Aktif)"] + [PIPELINE_INFO[k]["label"] for k in PIPELINE_ASAMALARI] + ["Olumsuz"],
                           key="km_pip_filtre")

    if filtre == "Tumu (Aktif)":
        filtreli = [a for a in adaylar if a.aktif]
    elif filtre == "Olumsuz":
        filtreli = [a for a in adaylar if a.asama == "olumsuz"]
    else:
        target = next((k for k, v in PIPELINE_INFO.items() if v["label"] == filtre), "aday")
        filtreli = [a for a in adaylar if a.asama == target]

    # Akıllı sıralama — ısı + gecikme + eskalasyon
    from models.kayit_takip_engine import sirala_oncelik, gun_sonu_ozet, hesapla_isi
    filtreli_akilli = sirala_oncelik(filtreli)
    st.caption(f"{len(filtreli)} aday (akıllı öncelik sıralı)")

    # AI Pipeline Insight
    if filtreli:
        with st.expander("🤖 AI Pipeline Analizi", expanded=False):
            _pip_cache = f"_km_pip_insight_{date.today().isoformat()}"
            if _pip_cache in st.session_state:
                st.markdown(st.session_state[_pip_cache])
            elif st.button("AI Analiz Yap", key="km_pip_ai"):
                with st.spinner("AI pipeline analiz ediyor..."):
                    from models.kayit_ai_engine import ai_pipeline_insight
                    stats = store.istatistikler()
                    stats["takip_geciken"] = len(store.takip_gecikenler())
                    stats["bugun_aranacak"] = len(store.bugun_aranacak())
                    result = ai_pipeline_insight(stats)
                    if result:
                        st.session_state[_pip_cache] = result
                        st.markdown(result)

    for _item in filtreli_akilli:
        a = _item["aday"]
        _isi = _item["isi"]
        _gec = _item["gecikme"]
        _esk = _item["eskalasyon"]
        info = a.pipeline_info
        gun = a.gun_gecti
        acil_renk = "#f87171" if gun > 7 else ("#fbbf24" if gun > 3 else "#4ade80")
        acil_text = f"{gun}g" if gun < 999 else ""

        # Isı badge
        isi_html = (f'<div style="background:{_isi["renk"]};color:#fff;padding:2px 8px;border-radius:10px;'
                    f'font-size:0.6rem;font-weight:700;display:inline-block;margin-left:4px;">'
                    f'{_isi["isi"]} {_isi["skor"]}</div>')

        # Eskalasyon uyarısı
        esk_html = ""
        if _esk:
            esk_html = (f'<div style="background:#ef444420;border-left:2px solid #ef4444;padding:3px 8px;'
                        f'margin-top:3px;border-radius:0 4px 4px 0;font-size:0.7rem;color:#fca5a5;">'
                        f'🚨 {_esk["kime"]}: {_esk["mesaj"]}</div>')

        # Lead Score badge (cached per session)
        _ls_key = f"_ls_{a.id}"
        ls = st.session_state.get(_ls_key)
        ls_html = ""
        if ls:
            ls_clr = "#22c55e" if ls.get("skor", 0) > 75 else "#f59e0b" if ls.get("skor", 0) > 50 else "#ef4444"
            ls_html = (f'<div style="background:{ls_clr};color:#fff;padding:2px 8px;border-radius:10px;'
                       f'font-size:0.65rem;font-weight:700;display:inline-block;margin-left:6px;">'
                       f'%{ls.get("skor", 0)}</div>')

        st.markdown(
            f'<div style="display:flex;align-items:center;gap:12px;padding:10px 14px;margin:4px 0;'
            f'background:{info["bg"]};border:1px solid {info["color"]}30;border-left:4px solid {info["color"]};'
            f'border-radius:0 10px 10px 0">'
            f'<div style="flex:1">'
            f'<div style="display:flex;justify-content:space-between;align-items:center">'
            f'<span style="font-weight:700;color:#f1f5f9;font-size:0.95rem">{a.label}{isi_html}{ls_html}</span>'
            f'<span style="font-size:0.75rem;color:{acil_renk};font-weight:600">{acil_text}</span></div>'
            f'<div style="font-size:0.8rem;color:#94a3b8;margin-top:2px">'
            f'📞 {a.veli_telefon or "-"} | 🎓 {a.kademe or "-"} | '
            f'Arama: {a.arama_sayisi} | Gorusme: {a.gorusme_sayisi}</div>'
            f'{esk_html}</div>'
            f'<div style="text-align:center;min-width:90px">'
            f'<div style="background:{info["color"]};color:#fff;padding:4px 10px;'
            f'border-radius:14px;font-size:0.7rem;font-weight:700;margin-bottom:3px">'
            f'{info["emoji"]} {info["label"]}</div>'
            f'<div style="font-size:0.65rem;color:{info["color"]};font-weight:600">'
            f'→ {info.get("aksiyon", "")}</div></div></div>',
            unsafe_allow_html=True)
        # Aday İşlem butonu
        if st.button(f"👤 İşlem Yap: {a.label}", key=f"pip_islem_{a.id}", use_container_width=True):
            st.session_state["_km_pip_secili"] = a.id

    # ── Seçili aday varsa işlem ekranını göster ──
    _secili_id = st.session_state.get("_km_pip_secili")
    if _secili_id:
        _secili_aday = store.get_by_id(_secili_id)
        if _secili_aday:
            st.markdown("---")
            if st.button("← Pipeline Listesine Dön", key="pip_geri"):
                del st.session_state["_km_pip_secili"]
                st.rerun()
            _render_aday_islem(store, adaylar, secili_id=_secili_id)


# ============================================================
# GUNLUK ISLER
# ============================================================

def _render_gunluk_isler(store: KayitDataStore, adaylar: list[KayitAday]):
    bugun_str = date.today().isoformat()

    # Verileri topla
    geciken = [a for a in store.takip_gecikenler() if a.asama not in ("randevu",)]
    aranacak = store.bugun_aranacak()
    randevu_bugun = [a for a in adaylar if a.asama == "randevu" and a.aktif and a.randevu_tarihi and a.randevu_tarihi[:10] == bugun_str]
    randevu_diger = [a for a in adaylar if a.asama == "randevu" and a.aktif and (not a.randevu_tarihi or a.randevu_tarihi[:10] != bugun_str)]
    gorusme_takip = [a for a in adaylar if a.asama == "gorusme" and a.aktif and a.takip_gecikti]
    fiyat = [a for a in adaylar if a.asama in ("gorusme", "fiyat_verildi") and a.aktif]
    sozlesme = [a for a in adaylar if a.asama == "sozlesme" and a.aktif]

    bugun_aramalar = [(a, ar) for a in adaylar for ar in a.aramalar if ar.get("tarih", "")[:10] == bugun_str]
    bugun_gorusmeler = [(a, gr) for a in adaylar for gr in a.gorusmeler if gr.get("tarih", "")[:10] == bugun_str]
    bugun_testler = [(a, t) for a in adaylar for t in a.testler if t.get("tarih", "")[:10] == bugun_str]
    bugun_yeni = [a for a in adaylar if a.olusturma_tarihi[:10] == bugun_str]
    bugun_kayit = [a for a in adaylar if a.kapanma_tarihi and a.kapanma_tarihi[:10] == bugun_str and a.asama == "kesin_kayit"]
    bugun_yapilan = len(bugun_aramalar) + len(bugun_gorusmeler) + len(bugun_testler) + len(bugun_kayit)

    toplam_is = len(aranacak) + len(geciken) + len(randevu_bugun) + len(gorusme_takip) + len(fiyat) + len(sozlesme)

    # ── AI GUNLUK BRIEF ──
    with st.expander("🤖 AI Günlük Brifing", expanded=False):
        _brief_cache = f"_km_brief_{bugun_str}"
        if _brief_cache in st.session_state:
            st.markdown(st.session_state[_brief_cache])
        elif st.button("AI Brifing Al", key="km_gunluk_ai"):
            with st.spinner("AI günlük brifing hazırlıyor..."):
                from models.kayit_ai_engine import ai_gunluk_brief
                stats = store.istatistikler()
                result = ai_gunluk_brief(
                    bugun_aranacak=len(aranacak), takip_geciken=len(geciken),
                    randevular=len(randevu_bugun), toplam_aktif=stats.get("aktif", 0),
                    donusum=stats.get("donusum_yuzde", 0),
                )
                if result:
                    st.session_state[_brief_cache] = result
                    st.markdown(result)
                else:
                    st.info("API anahtarı bulunamadı veya hata oluştu.")

    # ── BASLIK ──
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0ea5e9,#3b82f6);border-radius:12px;'
        f'padding:1rem 1.5rem;margin-bottom:1rem">'
        f'<div style="display:flex;justify-content:space-between;align-items:center">'
        f'<div><h3 style="color:#fff;margin:0">📋 Gunluk Calisma Programi</h3>'
        f'<p style="color:#bfdbfe;margin:0.2rem 0 0 0;font-size:0.85rem">{bugun_str} | {toplam_is} bekleyen | {bugun_yapilan} tamamlanan</p></div>'
        f'<div style="text-align:right"><div style="font-size:2rem;font-weight:800;color:#fff">{toplam_is}</div>'
        f'<div style="color:#bfdbfe;font-size:0.75rem">Bekleyen</div></div></div></div>',
        unsafe_allow_html=True)

    # ── SAYAC KARTLARI ──
    gc = st.columns(7)
    _items = [
        (gc[0], "Aranacak", len(aranacak), "#0ea5e9", "📞"),
        (gc[1], "Geciken", len(geciken), "#f87171", "⚠️"),
        (gc[2], "Randevu", len(randevu_bugun), "#fb923c", "📅"),
        (gc[3], "Gorusme", len(gorusme_takip), "#60a5fa", "🤝"),
        (gc[4], "Fiyat", len(fiyat), "#a78bfa", "💰"),
        (gc[5], "Sozlesme", len(sozlesme), "#38bdf8", "📄"),
        (gc[6], "Yeni", len(bugun_yeni), "#10b981", "➕"),
    ]
    for col, lbl, val, clr, icon in _items:
        with col:
            st.markdown(
                f'<div style="background:{clr}12;border:2px solid {clr}30;border-radius:10px;'
                f'padding:10px;text-align:center">'
                f'<div style="font-size:1.4rem;font-weight:800;color:{clr}">{icon} {val}</div>'
                f'<div style="font-size:0.65rem;color:#94a3b8">{lbl}</div></div>',
                unsafe_allow_html=True)

    # ── Tiklanabilir aday karti helper ──
    _click_counter = [0]

    def _clickable_aday(a: KayitAday, icon: str, color: str, extra_text: str, key_prefix: str):
        _click_counter[0] += 1
        unique_key = f"gi_{key_prefix}_{a.id}_{_click_counter[0]}"
        bc1, bc2 = st.columns([4, 1])
        with bc1:
            st.markdown(
                f'<div style="padding:6px 10px;background:{color}08;border-radius:6px;border-left:3px solid {color};margin:2px 0">'
                f'<span style="color:{color};font-weight:700">{icon}</span> '
                f'<span style="color:#e2e8f0;font-weight:600">{a.ogrenci_adi}</span> '
                f'<span style="color:#94a3b8;font-size:0.82rem">({a.veli_adi})</span> '
                f'<span style="color:#64748b;font-size:0.8rem">{extra_text}</span></div>',
                unsafe_allow_html=True)
        with bc2:
            if st.button("👤 İşlem", key=unique_key, use_container_width=True):
                st.session_state["gi_islem_aday"] = a.id

    # ════════════════════════════════════════════════
    # HER BOLUM AYRI EXPANDER — tikla ac / tikla kapa
    # ════════════════════════════════════════════════

    # 1) GECIKEN TAKIPLER
    if geciken:
        with st.expander(f"⚠️ Geciken Takipler ({len(geciken)})", expanded=False):
            for i, a in enumerate(geciken):
                _clickable_aday(a, "⚠️", "#f87171", f'{a.gun_gecti} gun gecikti | 📞 {a.veli_telefon or "-"}', f"gec{i}")

    # 2) ARANACAKLAR
    if aranacak:
        with st.expander(f"📞 Aranacaklar ({len(aranacak)})", expanded=False):
            for i, a in enumerate(aranacak):
                _clickable_aday(a, "📞", "#0ea5e9", f'#{a.arama_sayisi + 1}. arama | 📞 {a.veli_telefon or "-"}', f"ara{i}")

    # 3) BUGUNUN RANDEVULARI
    if randevu_bugun:
        with st.expander(f"📅 Bugunun Randevulari ({len(randevu_bugun)})", expanded=False):
            for i, a in enumerate(randevu_bugun):
                _clickable_aday(a, "📅", "#fb923c", f'{a.randevu_saati or "?"} | {a.kademe} | 📞 {a.veli_telefon or "-"}', f"rv{i}")

    # 4) DIGER RANDEVULAR
    if randevu_diger:
        with st.expander(f"📅 Diger Randevular ({len(randevu_diger)})", expanded=False):
            for i, a in enumerate(randevu_diger):
                _clickable_aday(a, "📅", "#f59e0b", f'{a.randevu_tarihi or "?"} | 📞 {a.veli_telefon or "-"}', f"rvd{i}")

    # 5) GORUSME TAKIP GECIKEN
    if gorusme_takip:
        with st.expander(f"🤝 Gorusme Takip Geciken ({len(gorusme_takip)})", expanded=False):
            for i, a in enumerate(gorusme_takip):
                _clickable_aday(a, "🤝", "#ea580c", f'{a.gun_gecti}g gecikti | 📞 {a.veli_telefon or "-"}', f"gtk{i}")

    # 6) FIYAT / GORUSME
    if fiyat:
        with st.expander(f"💰 Fiyat / Gorusme Bekleyen ({len(fiyat)})", expanded=False):
            for i, a in enumerate(fiyat):
                fb_a = a.fiyat_bilgi or {}
                ucret_a = float(fb_a.get("genel_toplam_final", fb_a.get("brut_toplam", 0)) or 0)
                ucret_txt = f"💰 {ucret_a:,.0f} TL" if ucret_a > 0 else "Fiyat yok"
                _clickable_aday(a, "💰", "#a78bfa", f'{ucret_txt} | 📞 {a.veli_telefon or "-"}', f"fiy{i}")

    # 7) SOZLESME BEKLEYEN
    if sozlesme:
        with st.expander(f"📄 Sozlesme Bekleyen ({len(sozlesme)})", expanded=False):
            for i, a in enumerate(sozlesme):
                _clickable_aday(a, "📄", "#38bdf8", f'{a.kademe} {a.hedef_sinif} | 📞 {a.veli_telefon or "-"}', f"szl{i}")

    # 8) BUGUN YAPILAN ISLEMLER
    if bugun_yapilan > 0:
        with st.expander(f"✅ Bugun Yapilan Islemler ({bugun_yapilan})", expanded=False):
            for i, (a, ar) in enumerate(bugun_aramalar):
                not_text = ar.get("not", "") or ""
                _clickable_aday(a, "📞", "#facc15", f'— {ar.get("sonuc", "")}{f" | {not_text[:40]}" if not_text else ""}', f"ba{i}")
            for i, (a, gr) in enumerate(bugun_gorusmeler):
                not_text = gr.get("not", "") or ""
                _clickable_aday(a, "🤝", "#60a5fa", f'— {gr.get("sonuc", "")}{f" | {not_text[:40]}" if not_text else ""}', f"bg{i}")
            for i, (a, t) in enumerate(bugun_testler):
                _clickable_aday(a, "🧪", "#a78bfa", f'— {t.get("test_adi", "")} ({t.get("sonuc", "")})', f"bt{i}")
            for i, a in enumerate(bugun_kayit):
                fb_k = a.fiyat_bilgi or {}
                ucret_k = float(fb_k.get("genel_toplam_final", fb_k.get("brut_toplam", 0)) or 0)
                _clickable_aday(a, "✅", "#4ade80", f'KAYIT — {a.kademe} {a.hedef_sinif}{f" | {ucret_k:,.0f} TL" if ucret_k > 0 else ""}', f"bk{i}")

    # 9) YENI ADAYLAR
    if bugun_yeni:
        with st.expander(f"➕ Bugun Eklenen Yeni Adaylar ({len(bugun_yeni)})", expanded=False):
            for i, a in enumerate(bugun_yeni):
                _clickable_aday(a, "➕", "#10b981", f'{a.kademe} {a.hedef_sinif} | {a.kanal or "-"}', f"yn{i}")

    if toplam_is == 0 and bugun_yapilan == 0:
        styled_info_banner("Bugun yapilacak is yok. Tum adaylar guncel.", "success")

    # ── BUGÜN YAPILAN İŞLEMLERİN KAYITLARI ──
    if bugun_aramalar or bugun_gorusmeler or bugun_kayit:
        st.markdown("---")
        with st.expander(f"📜 Bugün Yapılan İşlemler ({bugun_yapilan})", expanded=False):
            if bugun_aramalar:
                st.markdown("**📞 Bugün Yapılan Aramalar:**")
                for a, ar in bugun_aramalar:
                    not_txt = ar.get("not", ar.get("notlar", ""))[:60]
                    st.markdown(f'<div style="background:#0ea5e910;border-left:2px solid #0ea5e9;'
                                f'padding:4px 10px;border-radius:0 4px 4px 0;margin:2px 0;font-size:12px;">'
                                f'📞 <b>{a.ogrenci_adi}</b> — {ar.get("sonuc", "?")} '
                                f'{"| " + not_txt if not_txt else ""}</div>',
                                unsafe_allow_html=True)
            if bugun_gorusmeler:
                st.markdown("**🤝 Bugün Yapılan Görüşmeler:**")
                for a, gr in bugun_gorusmeler:
                    not_txt = gr.get("not", gr.get("notlar", ""))[:60]
                    st.markdown(f'<div style="background:#f59e0b10;border-left:2px solid #f59e0b;'
                                f'padding:4px 10px;border-radius:0 4px 4px 0;margin:2px 0;font-size:12px;">'
                                f'🤝 <b>{a.ogrenci_adi}</b> — {gr.get("sonuc", "?")} '
                                f'{"| " + not_txt if not_txt else ""}</div>',
                                unsafe_allow_html=True)
            if bugun_kayit:
                st.markdown("**✅ Bugün Kesin Kayıtlar:**")
                for a in bugun_kayit:
                    st.markdown(f'<div style="background:#22c55e10;border-left:2px solid #22c55e;'
                                f'padding:4px 10px;border-radius:0 4px 4px 0;margin:2px 0;font-size:12px;">'
                                f'✅ <b>{a.ogrenci_adi}</b> — Kesin Kayıt!</div>',
                                unsafe_allow_html=True)

    # ── İŞLEM EKRANI — Günlük İşler'den doğrudan aday işlem ──
    islem_id = st.session_state.get("gi_islem_aday")
    if islem_id:
        islem_aday = next((a for a in adaylar if a.id == islem_id), None)
        if islem_aday:
            st.markdown("---")
            if st.button("← Günlük İşlere Dön", key="gi_geri"):
                del st.session_state["gi_islem_aday"]
                st.rerun()
            _render_aday_islem(store, adaylar, secili_id=islem_id)

    # Eski detay paneli (geriye uyumluluk)
    detay_id = st.session_state.get("gi_detay_aday")
    if detay_id:
        detay_aday = next((a for a in adaylar if a.id == detay_id), None)
        if detay_aday:
            _render_gunluk_aday_detay(store, detay_aday)


def _render_gunluk_aday_detay(store: KayitDataStore, aday: KayitAday):
    """Gunluk isler icinde tiklanan adayin detay paneli."""
    info = aday.pipeline_info
    fb = aday.fiyat_bilgi or {}
    toplam_ucret = float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0)

    st.markdown("---")
    # Baslik
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{info["bg"]},{info["color"]}15);'
        f'border:2px solid {info["color"]};border-radius:14px;padding:16px 20px;margin:8px 0">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'
        f'<div>'
        f'<div style="font-size:1.1rem;font-weight:800;color:#f1f5f9">{info["emoji"]} {aday.ogrenci_adi}</div>'
        f'<div style="font-size:0.85rem;color:#94a3b8;margin-top:4px">'
        f'👤 {aday.veli_adi} | 📞 {aday.veli_telefon or "-"} | 🎓 {aday.kademe or "-"} {aday.hedef_sinif or ""} | '
        f'📢 {aday.kanal or "-"}</div></div>'
        f'<div style="background:{info["color"]};color:#fff;padding:6px 16px;border-radius:20px;'
        f'font-size:0.85rem;font-weight:700">{info["label"]}</div></div></div>',
        unsafe_allow_html=True)

    # Mini metrikler
    mc = st.columns(5)
    _m = [
        (mc[0], "Arama", aday.arama_sayisi, "#facc15"),
        (mc[1], "Gorusme", aday.gorusme_sayisi, "#60a5fa"),
        (mc[2], "Test", len(aday.testler), "#a78bfa"),
        (mc[3], "Ihtiyac", len(aday.ihtiyaclar), "#10b981"),
        (mc[4], "Ucret", f"{toplam_ucret / 1000:.0f}K" if toplam_ucret > 0 else "-", "#ec4899"),
    ]
    for col, lbl, val, clr in _m:
        with col:
            st.markdown(f'<div style="background:{clr}10;border:1px solid {clr}25;border-radius:8px;padding:6px;text-align:center"><div style="font-size:1.1rem;font-weight:800;color:{clr}">{val}</div><div style="font-size:0.6rem;color:#94a3b8">{lbl}</div></div>', unsafe_allow_html=True)

    # Arama gecmisi
    if aday.aramalar:
        with st.expander(f"📞 Arama Gecmisi ({aday.arama_sayisi})", expanded=False):
            for ar in aday.aramalar:
                not_text = ar.get("not", "") or ar.get("notlar", "")
                tarih = str(ar.get("tarih", ""))[:16].replace("T", " ")
                st.markdown(
                    f'<div style="padding:6px 10px;margin:3px 0;background:#111827;border-radius:6px;border-left:3px solid #facc15">'
                    f'<span style="color:#facc15;font-weight:700">#{ar.get("arama_no", "")}</span> '
                    f'<span style="color:#e2e8f0">{ar.get("sonuc", "")}</span> '
                    f'<span style="color:#64748b;font-size:0.75rem">({tarih})</span>'
                    f'{f"<div style=color:#94a3b8;font-size:0.8rem;margin-top:2px>📝 {not_text}</div>" if not_text else ""}</div>',
                    unsafe_allow_html=True)

    # Gorusme gecmisi
    if aday.gorusmeler:
        with st.expander(f"🤝 Gorusme Gecmisi ({aday.gorusme_sayisi})", expanded=False):
            for gr in aday.gorusmeler:
                not_text = gr.get("not", "") or gr.get("notlar", "")
                tarih = str(gr.get("tarih", ""))[:16].replace("T", " ")
                st.markdown(
                    f'<div style="padding:6px 10px;margin:3px 0;background:#111827;border-radius:6px;border-left:3px solid #60a5fa">'
                    f'<span style="color:#60a5fa;font-weight:700">#{gr.get("gorusme_no", "")}</span> '
                    f'<span style="color:#e2e8f0">{gr.get("sonuc", "")}</span> '
                    f'<span style="color:#64748b;font-size:0.75rem">({tarih})</span>'
                    f'{f"<div style=color:#94a3b8;font-size:0.8rem;margin-top:2px>📝 {not_text}</div>" if not_text else ""}</div>',
                    unsafe_allow_html=True)

    # Test sonuclari
    if aday.testler:
        with st.expander(f"🧪 Test Sonuclari ({len(aday.testler)})", expanded=False):
            for t in aday.testler:
                skorlar = t.get("skorlar", {})
                skor_text = " | ".join(f"{k}:{v}" for k, v in skorlar.items()) if skorlar else ""
                t_notlar = str(t.get("notlar", ""))[:80]
                not_div = f'<div style="color:#64748b;font-size:0.78rem">📝 {t_notlar}</div>' if t.get("notlar") else ""
                skor_span = f'<span style="color:#94a3b8;font-size:0.78rem">{skor_text[:100]}</span>' if skor_text else ""
                st.markdown(
                    f'<div style="padding:6px 10px;margin:3px 0;background:#111827;border-radius:6px;border-left:3px solid #a78bfa">'
                    f'<span style="color:#a78bfa;font-weight:700">{t.get("test_adi", "")}</span> '
                    f'<span style="color:#e2e8f0">— {t.get("sonuc", "")}</span><br>'
                    f'{skor_span}{not_div}</div>',
                    unsafe_allow_html=True)

    # Ihtiyac analizi
    if aday.ihtiyaclar:
        with st.expander(f"🎯 Ihtiyac Analizi ({len(aday.ihtiyaclar)})", expanded=False):
            for ih in aday.ihtiyaclar:
                onc = ih.get("oncelik", "Orta")
                onc_clr = {"Yuksek": "#f87171", "Orta": "#fbbf24", "Dusuk": "#4ade80"}.get(onc, "#94a3b8")
                ih_aciklama = str(ih.get("aciklama", ""))
                aciklama_html = f' — <span style="color:#94a3b8;font-size:0.82rem">{ih_aciklama}</span>' if ih_aciklama else ""
                st.markdown(
                    f'<div style="padding:6px 10px;margin:3px 0;background:#111827;border-radius:6px;border-left:3px solid {onc_clr}">'
                    f'<span style="color:{onc_clr};font-weight:700;font-size:0.8rem">[{onc}]</span> '
                    f'<span style="color:#e2e8f0">{ih.get("kategori", "")}</span>'
                    f'{aciklama_html}</div>',
                    unsafe_allow_html=True)

    # Fiyat bilgisi
    if fb:
        with st.expander("💰 Fiyat Bilgisi", expanded=False):
            st.markdown(
                f'<div style="padding:10px;background:#111827;border-radius:8px;color:#e2e8f0;font-size:0.85rem">'
                f'Liste: {fb.get("liste_fiyati", 0):,.0f} TL | Indirim: %{fb.get("toplam_indirim", 0):.0f} | '
                f'KDV Dahil: {fb.get("kdv_dahil", 0):,.0f} TL | Pesinat: {fb.get("pesinat", 0):,.0f} TL<br>'
                f'<strong style="color:#10b981;font-size:1rem">TOPLAM: {toplam_ucret:,.0f} TL</strong></div>',
                unsafe_allow_html=True)

    # Genel notlar
    if aday.notlar:
        with st.expander("📝 Genel Notlar", expanded=False):
            st.markdown(f'<div style="color:#94a3b8;font-size:0.85rem;white-space:pre-wrap">{aday.notlar}</div>',
                        unsafe_allow_html=True)

    # ── AI Kayit Senaryosu ──
    ai_key = f"gi_ai_{aday.id}"
    result_key = f"{ai_key}_result"

    st.markdown("")
    if st.button("🤖 AI Kayit Senaryosu Olustur", key=ai_key, type="primary", use_container_width=True):
        with st.spinner("AI tum verileri analiz ediyor..."):
            result = _call_ai_son_analiz(aday)
            if result:
                st.session_state[result_key] = result

    result = st.session_state.get(result_key, "")
    if result:
        _render_ai_result(result)
        pdf_bytes = _generate_ai_analiz_pdf(aday, result)
        if pdf_bytes:
            st.download_button("📥 Kayit Senaryosu PDF", data=pdf_bytes,
                               file_name=f"KayitSenaryosu_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                               mime="application/pdf", key=f"{ai_key}_pdf", use_container_width=True)

    # Kapat butonu
    if st.button("✕ Detay Panelini Kapat", key=f"gi_kapat_{aday.id}"):
        del st.session_state["gi_detay_aday"]
        st.rerun()


# ============================================================
# YENI ADAY GIRISI
# ============================================================

def _render_yeni_aday(store: KayitDataStore):
    st.markdown(
        '<div style="background:#6366f115;border-left:4px solid #6366f1;border-radius:0 10px 10px 0;'
        'padding:12px 16px;margin-bottom:14px">'
        '<strong style="color:#a5b4fc;font-size:1rem">➕ Yeni Aday Kaydi</strong></div>',
        unsafe_allow_html=True)

    with st.form("km_yeni_aday_form", clear_on_submit=True):
        st.markdown(
            '<div style="color:#94a3b8;font-size:0.85rem;margin-bottom:8px">* isaretli alanlar zorunludur</div>',
            unsafe_allow_html=True)

        # Veli bilgileri
        st.markdown(
            '<div style="background:#6366f110;border-left:3px solid #6366f1;border-radius:0 6px 6px 0;'
            'padding:6px 10px;margin:8px 0"><strong style="color:#a5b4fc;font-size:0.9rem">👤 Veli Bilgileri</strong></div>',
            unsafe_allow_html=True)
        vc1, vc2, vc3 = st.columns(3)
        with vc1:
            veli_adi = st.text_input("Veli Adi Soyadi *", key="km_veli_adi", placeholder="Orn: Aykin Uzcu")
        with vc2:
            veli_tel = st.text_input("Telefon *", key="km_veli_tel", placeholder="05XX XXX XXXX")
        with vc3:
            veli_email = st.text_input("E-posta", key="km_veli_email")

        # Ogrenci bilgileri
        st.markdown(
            '<div style="background:#10b98110;border-left:3px solid #10b981;border-radius:0 6px 6px 0;'
            'padding:6px 10px;margin:8px 0"><strong style="color:#6ee7b7;font-size:0.9rem">🎓 Ogrenci Bilgileri</strong></div>',
            unsafe_allow_html=True)
        oc1, oc2, oc3 = st.columns(3)
        with oc1:
            ogr_adi = st.text_input("Ogrenci Adi *", key="km_ogr_adi", placeholder="Orn: Oguzhan Uzcu")
        with oc2:
            cinsiyet = st.selectbox("Cinsiyet", [""] + CINSIYET_SECENEKLERI, key="km_cinsiyet")
        with oc3:
            kademe = st.selectbox("Kademe *", KADEME_SECENEKLERI, key="km_kademe")

        oc4, oc5, oc6 = st.columns(3)
        with oc4:
            mevcut_sinif = st.selectbox("Mevcut Sinifi (su an okudugu)", [""] + SINIF_SECENEKLERI, key="km_mevcut_sinif")
        with oc5:
            hedef_sinif = st.selectbox("Hedef Sinif (bu okulda okuyacagi)", [""] + SINIF_SECENEKLERI, key="km_hedef_sinif")
        with oc6:
            okul_turu = st.selectbox("Okul Turu (mevcut)", [""] + OKUL_TURU_SECENEKLERI, key="km_okul_turu")

        oc7, oc8 = st.columns([2, 1])
        with oc7:
            mevcut_okul = st.text_input("Mevcut Okulu", key="km_mevcut_okul", placeholder="Su an okudugu okulun adi")
        with oc8:
            from datetime import date as _d, timedelta as _td
            ogr_dogum = st.date_input(
                "Öğrenci Doğum Tarihi",
                value=None,
                min_value=_d(2005, 1, 1),
                max_value=_d.today(),
                key="km_ogr_dogum",
                help="Doğum günü otomasyonu için",
            )

        # Kampanya & kaynak
        st.markdown(
            '<div style="background:#f59e0b10;border-left:3px solid #f59e0b;border-radius:0 6px 6px 0;'
            'padding:6px 10px;margin:8px 0"><strong style="color:#fde68a;font-size:0.9rem">📢 Kampanya & Kaynak</strong></div>',
            unsafe_allow_html=True)
        kc1, kc2 = st.columns(2)
        with kc1:
            kampanya = st.text_input("Kampanya", key="km_kampanya", placeholder="Orn: Bursluluk Sinavi")
        with kc2:
            kanal = st.selectbox("Kaynak/Kanal", KANAL_SECENEKLERI, key="km_kanal")

        # UTM Attribution — opsiyonel, sosyal medya/reklam takibi
        with st.expander("📊 UTM Attribution (reklam takibi)", expanded=False):
            uc1, uc2 = st.columns(2)
            with uc1:
                utm_source = st.text_input(
                    "UTM Source", key="km_utm_source",
                    placeholder="instagram / facebook / google / organic",
                    help="Adayın geldiği platform/kaynak",
                )
                utm_medium = st.text_input(
                    "UTM Medium", key="km_utm_medium",
                    placeholder="cpc / social / email / sms / organic",
                    help="Pazarlama kanalı tipi",
                )
            with uc2:
                utm_campaign = st.text_input(
                    "UTM Campaign", key="km_utm_campaign",
                    placeholder="erken_kayit_2026 / bursluluk_sinavi",
                    help="Kampanya slug/kod",
                )
                utm_content = st.text_input(
                    "UTM Content", key="km_utm_content",
                    placeholder="banner_a / video_1",
                    help="A/B test için içerik kodu",
                )

        notlar = st.text_area("Not", key="km_notlar", height=68, placeholder="Opsiyonel...")

        # ── REFERANS (Opsiyonel) ──
        with st.expander("🤝 Referans / Tavsiye (varsa)"):
            rf1, rf2, rf3 = st.columns(3)
            with rf1:
                ref_veli = st.text_input("Tavsiye Eden Veli", key="km_ref_veli", placeholder="Mevcut veli adi")
            with rf2:
                ref_ogr = st.text_input("Tavsiye Edenin Öğrencisi", key="km_ref_ogr")
            with rf3:
                ref_tipi = st.selectbox("Referans Tipi", ["", "Mevcut Veli", "Mezun", "Personel", "Diğer"], key="km_ref_tipi")

        # ── VELİ PROFİLİ (Opsiyonel — sonra da doldurulabilir) ──
        with st.expander("👤 Veli Profili (opsiyonel — sonra da doldurabilirsiniz)"):
            vp1, vp2 = st.columns(2)
            with vp1:
                vp_meslek = st.text_input("Veli Mesleği", key="km_vp_meslek", placeholder="Doktor, avukat, esnaf...")
                vp_egitim = st.selectbox("Eğitim Seviyesi", ["", "İlkokul", "Ortaokul", "Lise", "Üniversite", "Yüksek Lisans/Doktora"], key="km_vp_egitim")
                vp_karar = st.selectbox("Karar Verici", ["", "Anne", "Baba", "İkisi Birlikte", "Büyükanne/Büyükbaba", "Diğer"], key="km_vp_karar")
                vp_cocuk = st.text_input("Diğer Çocuklar (yaş/okul)", key="km_vp_cocuk", placeholder="2 çocuk: 8 yaş devlet, 12 yaş özel")
            with vp2:
                vp_neden = st.text_area("Neden Okul Değiştirmek İstiyor?", key="km_vp_neden", height=68, placeholder="Mevcut okuldan memnuniyetsizlik, taşınma, kalite arayışı...")
                vp_butce = st.selectbox("Bütçe Beklentisi", ["", "Ekonomik", "Orta", "Yüksek", "Fiyat önemsiz"], key="km_vp_butce")
                vp_rakip = st.text_input("Baktığı Diğer Okullar", key="km_vp_rakip", placeholder="X Koleji, Y Okulu...")
                vp_zaman = st.selectbox("Ne Zaman Karar Verecek?", ["", "Hemen", "1 Hafta", "1 Ay", "Dönem Sonu", "Belirsiz"], key="km_vp_zaman")
            vp_kriter = st.multiselect("Karar Kriterleri (en önemliler)", [
                "Akademik başarı", "Öğretmen kalitesi", "Fiziksel ortam", "Ulaşım/servis",
                "Fiyat", "Yabancı dil", "Sosyal etkinlikler", "Spor imkanları",
                "Güvenlik", "Bireysel ilgi", "Teknoloji", "Burs/indirim",
                "Referans/tavsiye", "Okul kültürü", "Üniversiteye hazırlık"
            ], key="km_vp_kriter")

        # ── ÖĞRENCİ PROFİLİ (Opsiyonel) ──
        with st.expander("🎓 Öğrenci Profili (opsiyonel — sonra da doldurabilirsiniz)"):
            op1, op2 = st.columns(2)
            with op1:
                op_basari = st.selectbox("Akademik Başarı", ["", "Çok Başarılı (90+)", "Başarılı (70-89)", "Orta (50-69)", "Düşük (50 altı)"], key="km_op_basari")
                op_guclu = st.text_input("Güçlü Dersler", key="km_op_guclu", placeholder="Matematik, Fen...")
                op_zayif = st.text_input("Zayıf Dersler", key="km_op_zayif", placeholder="İngilizce, Sosyal...")
                op_davranis = st.selectbox("Davranış Durumu", ["", "Çok İyi", "İyi", "Orta", "Sorunlu"], key="km_op_davranis")
            with op2:
                op_ihtiyac = st.selectbox("Özel İhtiyaç", ["", "Yok", "DEHB", "ÖÖG", "Üstün Zeka", "Fiziksel", "Diğer"], key="km_op_ihtiyac")
                op_sosyal = st.selectbox("Sosyal Beceriler", ["", "Çok İyi", "İyi", "Orta", "Zayıf"], key="km_op_sosyal")
                op_hobi = st.text_input("Hobiler/İlgi Alanları", key="km_op_hobi", placeholder="Futbol, piyano, resim...")
                op_memnun = st.selectbox("Önceki Okul Memnuniyeti", ["", "Çok Memnun", "Memnun", "Kısmen", "Memnun Değil"], key="km_op_memnun")
            op_istek = st.text_input("Öğrencinin İsteği", key="km_op_istek", placeholder="Okul değiştirmek istiyor mu? Ne istiyor?")

        if st.form_submit_button("Kaydet", type="primary", use_container_width=True):
            if not veli_adi or not ogr_adi or not veli_tel:
                st.error("Veli adi, ogrenci adi ve telefon zorunludur.")
            else:
                # Veli profil dict
                _veli_profil = {}
                if vp_meslek: _veli_profil["meslek"] = vp_meslek
                if vp_egitim: _veli_profil["egitim"] = vp_egitim
                if vp_karar: _veli_profil["karar_verici"] = vp_karar
                if vp_cocuk: _veli_profil["diger_cocuklar"] = vp_cocuk
                if vp_neden: _veli_profil["neden_degistirmek_istiyor"] = vp_neden
                if vp_butce: _veli_profil["butce_beklentisi"] = vp_butce
                if vp_rakip: _veli_profil["rakip_okullar"] = vp_rakip
                if vp_zaman: _veli_profil["karar_zamani"] = vp_zaman
                if vp_kriter: _veli_profil["karar_kriterleri"] = vp_kriter
                # Öğrenci profil dict
                _ogr_profil = {}
                if op_basari: _ogr_profil["akademik_basari"] = op_basari
                if op_guclu: _ogr_profil["guclu_dersler"] = op_guclu
                if op_zayif: _ogr_profil["zayif_dersler"] = op_zayif
                if op_davranis: _ogr_profil["davranis_durumu"] = op_davranis
                if op_ihtiyac: _ogr_profil["ozel_ihtiyac"] = op_ihtiyac
                if op_sosyal: _ogr_profil["sosyal_beceriler"] = op_sosyal
                if op_hobi: _ogr_profil["hobiler"] = op_hobi
                if op_memnun: _ogr_profil["onceki_okul_memnuniyet"] = op_memnun
                if op_istek: _ogr_profil["ogrenci_istegi"] = op_istek

                yeni = KayitAday(
                    veli_adi=veli_adi, veli_telefon=veli_tel, veli_email=veli_email,
                    ogrenci_adi=ogr_adi, kademe=kademe, kanal=kanal,
                    cinsiyet=cinsiyet, mevcut_sinif=mevcut_sinif,
                    hedef_sinif=hedef_sinif, okul_turu=okul_turu,
                    mevcut_okul=mevcut_okul,
                    ogrenci_dogum_tarihi=(ogr_dogum.isoformat() if ogr_dogum else ""),
                    kampanya=kampanya, notlar=notlar,
                    utm_source=utm_source, utm_medium=utm_medium,
                    utm_campaign=utm_campaign, utm_content=utm_content,
                    referans_veli=ref_veli, referans_ogrenci=ref_ogr,
                    referans_tipi=ref_tipi,
                    veli_profil=_veli_profil,
                    ogrenci_profil=_ogr_profil,
                )
                store.add(yeni)
                # ZIRVE: Otomasyon trigger — yeni aday
                try:
                    from models.kayit_otomasyon import trigger_yeni_aday
                    n_otom = trigger_yeni_aday(yeni)
                    if n_otom > 0:
                        st.toast(f"⚡ {n_otom} otomasyon kuyruğa eklendi", icon="🚀")
                except Exception:
                    pass
                # MEGA: XP kazandirma — aday olustur
                try:
                    from models.kayit_skorboard import xp_kazandir
                    user = st.session_state.get("auth_user", {})
                    res = xp_kazandir(user.get("name", "Koordinator"), "aday_olustur")
                    if res["kazanilan_xp"] > 0:
                        st.toast(f"🎮 +{res['kazanilan_xp']} XP", icon="✨")
                    if res["yeni_seviye"]:
                        st.balloons()
                        st.toast(f"🎉 Seviye atladin! Lvl {res['current_level']}", icon="🏆")
                    for r in res["yeni_rozetler"]:
                        st.toast(f"{r['icon']} Yeni rozet: {r['ad']}", icon="🎖️")
                except Exception:
                    pass
                st.success(f"'{veli_adi} — {ogr_adi}' aday olarak kaydedildi!")
                st.rerun()


# ============================================================
# ADAY ISLEM (sec + aksiyon yap)
# ============================================================

def _render_ai_son_analiz(aday: KayitAday):
    """AI Kayit Senaryosu — adayin tum verileriyle durum grafikleri + kayit senaryosu + PDF."""
    ai_key = f"km_ai_son_{aday.id}"
    result_key = f"{ai_key}_result"

    # ── BASLIK ──
    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed 0%,#4f46e5 40%,#10b981 100%);border-radius:12px;'
        'padding:1.2rem 1.5rem;margin:0.8rem 0">'
        '<h3 style="color:#fff;margin:0">🎯 Kayit Senaryosu</h3>'
        '<p style="color:#c7d2fe;margin:0.3rem 0 0 0;font-size:0.85rem">'
        'AI destekli aday degerlendirme — durum analizi — kayit stratejisi — sifir hata gorusme senaryosu</p></div>',
        unsafe_allow_html=True)

    # ── DURUM KARTLARI ──
    try:
        surec_gun = (date.today() - date.fromisoformat(aday.olusturma_tarihi[:10])).days
    except (ValueError, TypeError):
        surec_gun = 0

    fb = aday.fiyat_bilgi or {}
    toplam_ucret = float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0)

    mc = st.columns(6)
    _kartlar = [
        (mc[0], "📞 Arama", str(aday.arama_sayisi), "#facc15"),
        (mc[1], "🤝 Gorusme", str(aday.gorusme_sayisi), "#60a5fa"),
        (mc[2], "🧪 Test", str(len(aday.testler)), "#a78bfa"),
        (mc[3], "🎯 Ihtiyac", str(len(aday.ihtiyaclar)), "#10b981"),
        (mc[4], "📅 Gun", str(surec_gun), "#f59e0b"),
        (mc[5], "💰 Ucret", f"{toplam_ucret / 1000:.0f}K" if toplam_ucret > 0 else "-", "#ec4899"),
    ]
    for col, lbl, val, clr in _kartlar:
        with col:
            st.markdown(
                f'<div style="background:{clr}12;border:2px solid {clr}30;border-radius:10px;padding:10px;text-align:center">'
                f'<div style="font-size:1.5rem;font-weight:800;color:{clr}">{val}</div>'
                f'<div style="font-size:0.65rem;color:#94a3b8">{lbl}</div></div>',
                unsafe_allow_html=True)

    # ── DURUM GRAFIKLERI ──
    gc1, gc2 = st.columns(2)
    with gc1:
        # Surec ilerleme grafigi
        asamalar_done = {"aday": 1, "arandi": 2, "randevu": 3, "gorusme": 4, "fiyat_verildi": 5, "sozlesme": 6, "kesin_kayit": 7}
        current = asamalar_done.get(aday.asama, 0)
        pipe_data = {
            "Tamamlanan": current,
            "Kalan": 7 - current,
        }
        pie_img = _make_pie_chart(pipe_data, f"Pipeline: {aday.pipeline_info.get('label', '')}",
                                  ["#10b981", "#1e293b"])
        if pie_img:
            st.image(pie_img, use_container_width=True)

    with gc2:
        # Test skor ozeti (varsa)
        if aday.testler:
            son_test = aday.testler[-1]
            skorlar = son_test.get("skorlar", {})
            if skorlar:
                numeric_skorlar = {k: v for k, v in skorlar.items() if isinstance(v, (int, float))}
                if numeric_skorlar:
                    pie_img2 = _make_pie_chart(numeric_skorlar, f'Son Test: {son_test.get("test_adi", "")[:25]}')
                    if pie_img2:
                        st.image(pie_img2, use_container_width=True)
        else:
            st.markdown(
                '<div style="background:#1e293b;border-radius:10px;padding:2rem;text-align:center;color:#64748b">'
                '<div style="font-size:2rem">🧪</div>Henuz test yok</div>',
                unsafe_allow_html=True)

    # ── AI BUTON ──
    if st.button("🤖 AI Kayit Senaryosu Olustur", key=ai_key, type="primary", use_container_width=True):
        with st.spinner("AI tum verileri analiz ediyor ve kayit senaryosu hazirlaniyor..."):
            result = _call_ai_son_analiz(aday)
            if result:
                st.session_state[result_key] = result

    # ── SONUC ──
    result = st.session_state.get(result_key, "")
    if result:
        _render_ai_result(result)

        # PDF indir
        st.markdown("")
        pdf_bytes = _generate_ai_analiz_pdf(aday, result)
        if pdf_bytes:
            st.download_button("📥 Kayit Senaryosu PDF Indir", data=pdf_bytes,
                               file_name=f"KayitSenaryosu_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                               mime="application/pdf", key=f"{ai_key}_pdf", use_container_width=True)


def _call_ai_son_analiz(aday: KayitAday) -> str:
    """Adayin TUM verilerini AI'ya gonderip kapsamli degerlendirme al."""
    try:
        from utils.smarti_helper import _ensure_env, _get_client
        _ensure_env()
        client = _get_client()
        if not client:
            return ""

        # Arama gecmisi
        arama_ozet = ""
        for ar in aday.aramalar:
            not_text = ar.get("not", "") or ar.get("notlar", "")
            arama_ozet += f"- {ar.get('arama_no', '')}. Arama ({str(ar.get('tarih', ''))[:10]}): {ar.get('sonuc', '')}"
            if not_text:
                arama_ozet += f" | Not: {not_text}"
            arama_ozet += "\n"

        # Gorusme gecmisi
        gorusme_ozet = ""
        for gr in aday.gorusmeler:
            not_text = gr.get("not", "") or gr.get("notlar", "")
            gorusme_ozet += f"- {gr.get('gorusme_no', '')}. Gorusme ({str(gr.get('tarih', ''))[:10]}): {gr.get('sonuc', '')}"
            if not_text:
                gorusme_ozet += f" | Not: {not_text}"
            gorusme_ozet += "\n"

        # Test sonuclari (DETAYLI — her skor, her olcek, top3)
        test_ozet = ""
        for t in aday.testler:
            test_ozet += f"\n=== {t.get('test_adi', '?')} ({str(t.get('tarih', ''))[:10]}) ===\n"
            test_ozet += f"  Sonuc: {t.get('sonuc', '-')}\n"
            skorlar = t.get("skorlar", {})
            if skorlar:
                test_ozet += "  TUM SKORLAR:\n"
                for k, v in sorted(skorlar.items(), key=lambda x: float(x[1]) if isinstance(x[1], (int, float)) else 0, reverse=True):
                    try:
                        val = float(v)
                        seviye = "COK GUCLU" if val >= 8 else "GUCLU" if val >= 6 else "ORTA" if val >= 4 else "ZAYIF"
                        test_ozet += f"    {k}: {v}/10 ({seviye})\n"
                    except (ValueError, TypeError):
                        test_ozet += f"    {k}: {v}\n"
            top3 = t.get("top3", [])
            if top3:
                test_ozet += "  EN GUCLU 3 ALAN:\n"
                for item in top3:
                    test_ozet += f"    1. {item.get('alan', '?')}: {item.get('skor', '-')} ({item.get('seviye', '')})\n"
            if t.get("notlar"):
                test_ozet += f"  UZMAN NOTU: {t['notlar']}\n"

        # Ihtiyac analizi (DETAYLI — oncelik sirali)
        ihtiyac_ozet = ""
        # Oncelik sirala: Acil > Yuksek > Orta > Dusuk
        _oncelik_sira = {"Acil": 0, "Yuksek": 1, "Orta": 2, "Dusuk": 3}
        _sorted_ih = sorted(aday.ihtiyaclar, key=lambda x: _oncelik_sira.get(x.get("oncelik", ""), 9))
        for ih in _sorted_ih:
            oncelik = ih.get('oncelik', '-')
            onc_emoji = {"Acil": "🔴", "Yuksek": "🟠", "Orta": "🟡", "Dusuk": "🟢"}.get(oncelik, "⚪")
            ihtiyac_ozet += f"- {onc_emoji} [{oncelik}] {ih.get('kategori', '')}: {ih.get('aciklama', '')}\n"

        # Fiyat
        fiyat_ozet = ""
        fb = aday.fiyat_bilgi or {}
        if fb:
            gt = fb.get("genel_toplam_final", fb.get("brut_toplam", 0))
            fiyat_ozet = f"Liste: {fb.get('liste_fiyati', 0):,.0f} TL | Indirim: %{fb.get('toplam_indirim', 0):.0f} | Toplam: {float(gt or 0):,.0f} TL"

        # Genel notlar
        genel_notlar = aday.notlar or ""

        # Surec suresi
        try:
            d1 = date.fromisoformat(aday.olusturma_tarihi[:10])
            surec_gun = (date.today() - d1).days
        except (ValueError, TypeError):
            surec_gun = 0

        # Kacinci aramada ulasildigi
        ilk_ulasim = "Henuz ulasilmadi"
        for ar in aday.aramalar:
            if ar.get("sonuc") not in ("Ulasim yok — tekrar aranacak", "Mesaj birakildi", "Telefon yanlis"):
                ilk_ulasim = f"{ar.get('arama_no', '?')}. aramada ulasildi"
                break

        # Kacinci gorusmede geldi
        ilk_gorusme = "Henuz gorusme yok"
        for gr in aday.gorusmeler:
            if gr.get("sonuc") != "Veli gelmedi":
                ilk_gorusme = f"{gr.get('gorusme_no', '?')}. gorusmede yuz yuze gorusuldu"
                break

        from utils.ai_rules import inject_rules as _air_km
        system_prompt = _air_km("""Sen Turkiye'nin en basarili ozel okul kayit danismanisin. 20+ yil deneyimlisin. Her gorusmeden MUTLAK KESIN KAYIT ile cikma hedefindesin. Sifir hata toleransin var.

═══ TEMEL ILKE: TANIMADAN IHTIYACINI BELIRLEMEDEN HEDEFE ULASILMAZ ═══

Bir adayi kayit ettirmek icin 3 seyi MUTLAKA bilmelisin:
1. VELI KIM? (profil, meslek, egitim, karar verici, butce, motivasyon)
2. VELININ GERCEK IHTIYACI NE? (ihtiyac analizi — 22 kategori)
3. OGRENCI NASIL BIRI? (testler, basari, guclu/zayif, karakter)

Bu 3 bilgi olmadan ASLA genel konusma yapma. Her cumlen bu verilere dayanmali.

═══ IHTIYAC ANALIZI NASIL KULLANILIR ═══

Ihtiyac analizindeki HER KATEGORI velinin GERCEK karar kriteridir.
SADECE velinin belirttigi ihtiyaclara odaklan — gereksiz konulardan bahsetme!

Ornek:
- Veli "Akademik Basari" + "Yabanci Dil" secmisse → SADECE bunlardan konus
  SPOR tesislerinden bahsetme, veli ilgilenmiyorsa gereksiz!
- Veli "Fiyat" + "Burs" secmisse → deger/fiyat oranini vurgula, burs olanagini anlat
  Fiziksel ortamdan bahsetme, velinin derdi bu degil!
- Veli "Guvenlik" + "Bireysel Ilgi" secmisse → kamera sistemi + dusuk sinif mevcudu anlat
  Universite hazirliktan bahsetme, cocuk 2. sinifta!

KURAL: Velinin BELIRTMEDIGI ihtiyac hakkinda konusma. Sadece belirttikleri uzerinden git.

═══ TEST SONUCLARI NASIL KULLANILIR ═══

Her test sonucu ogrencinin GERCEK durumunu gosterir. Bunu veliye DOGRU sunmalisin:

COKLU ZEKA TESTI:
- Guclu alanlar (7+/10) = "Cocugunuzun dogal yetenegi burada, biz bunu destekliyoruz"
- Zayif alanlar (4-/10) = SOYLEME, bunun yerine "Gelistirilebilir alanlar var, programimiz bunu hedefliyor"
- Ornek: Muziksel 9.0 → "Cocugunuz muzik alaninda cok yetenekli, muzik programimiz/koromuz/orkestramiz buna cok uygun"
- Ornek: Mantiksal 4.2 → "Matematik ogrenme yontemimiz farkli, somut materyallerle ogretiyoruz" (zayif DEME)

OGRENME STILI (VARK):
- Bu cocugun NASIL OGRENMESI gerektigini gosterir
- Gorsel baskinsa → "Akilli tahta + gorsel materyallerle ogretim yapiyoruz"
- Isitsel baskinsa → "Tartisma tabanli dersler + sesli ogrenme"
- Okuma-Yazma baskinsa → "Not tutma + ozet cikarma destekli ders isliyoruz"
- Kinestetik baskinsa → "Deneysel ogrenme + laboratuvar + proje bazli egitim"
- VELIYE SOYLE: "Cocugunuz X tarzinda ogreniyor, bizim siniflarimiz tam buna uygun"

SEVIYE TESPIT SINAVI:
- Puan YUKSEKSE (70+) → "Cocugunuz basarili, biz bunu daha ileriye tasiyoruz"
- Puan DUSUKSE (50-) → "Bazi alanlarda destek gerekiyor — bizim destek programimiz tam bunu cozuyor"
  ASLA "cocugunuz basarisiz" DEME → "Potansiyeli var ama dogru yontemle cikarilmamis" de
- Ders bazli analiz yap → "Matematigi guclu ama Fen'de destek lazim — Fen laboratuvarimiz bunu cozuyor"

CEFR YABANCI DIL:
- A1/A2 → "Seviye dusuk ama yogun Ingilizce programimizla 1 yilda B1'e cikariz"
- B1+ → "Iyi seviye — native speaker ogretmenlerimizle daha ileriye tasiyoruz"

HHT-1 (Okula Hazirlik):
- Hazir → "Cocugunuz hazir, uyum programimiz ile hemen adapte olacak"
- Kismi → "Bazi alanlarda olgunlasma gerekiyor — anasinifi programimiz tam bunu hedefliyor"

═══ NOTLAR NASIL KULLANILIR ═══

Aramalarda ve gorusmelerde alinan HER NOT velinin GERCEK dusuncesidir:
- "Pahali" → Fiyat hassasiyeti — deger onerisi + taksit + burs vurgula
- "Dusunecegiz" → Kararsizlik — aciliyet yarat + kontenjan sinirli de
- "Esimle konusacagim" → Karar verici veli degil — ES'i gorusmeye davet et
- "Baska okullara bakiyoruz" → Rakip tehdit — farklilasma + ozel teklif
- "Cocuk istemiyor" → Cocuk korkusu — deneme dersi + cocukla tanisma teklif et
- "Uzakta" → Ulasim sorunu — servis bilgisi + guzergah anlat
- "Arkadasi var mevcut okulda" → Sosyal kaygi — sinif mevcudu dusuk + hemen arkadas edinir
Velinin kullandigi HER KELIMEYI analiz et ve senaryoya yansit.

═══ VELI PROFILI NASIL KULLANILIR ═══

- Meslek DOKTOR/AVUKAT → Resmi dil, data odakli sunum, somut basari oranlari
- Meslek ESNAF → Samimi dil, guven odakli, referans/tavsiye vurgula
- Egitim UNIVERSITE → Akademik program detayi, ogretmen kalitesi
- Egitim ILKOKUL → Basit, anlasilir, somut orneklerle anlat
- Butce EKONOMIK → Taksit + burs + erken kayit indirimi one cikar
- Butce FIYAT ONEMSIZ → Kalite + prestij + farklilasma vurgula
- Karar verici ANNE → Duygusal baglanti kur, guvenlik vurgula
- Karar verici BABA → Rasyonel, ROI odakli, gelecek yatirim dili
- Karar verici IKISI → Her ikisine ayri mesaj hazirla

Bir adayin TUM verilerini (profil, aramalar, gorusmeler, notlar, testler, ihtiyac analizi, fiyat, surec suresi) inceleyeceksin.
Amacin: Bu adayi %100 kayit ettirmek icin kusursuz bir senaryo olusturmak.

YANITINI su formatta ver:

## 📊 ADAY PROFIL OZETI
(Kim bu aday, ne ariyor, ne asamada, kac gundur surec devam ediyor — 3-4 cumle)

## 🎯 KAYIT IHTIMALI SKORU
Skor: ?/100
### ✅ Olumlu Sinyaller
(Tum verilerdeki olumlu isaretleri madde madde listele — her birini somut veriye dayandır)
### ⚠️ Risk Faktorleri
(Kaydi engelleyebilecek riskler — her birinin cozumunu de yaz)
### 🔑 Kilit Karar Faktoru
(Kayit kararini BELIRLEYECEK tek en onemli sey — 1 cumle)

## 📞 ILETISIM ANALIZI
(Kacinci aramada ulasildi, gorusmelerin seyri, notlardaki gizli ipuclari, velinin iletisim tarzı ve tercihleri)

## 🧪 AKADEMIK PROFIL
(Test sonuclari, guclu/zayif alanlar, ogrenci potansiyeli, okulun bu ogrenciye ne katacagi)

## 🎯 VELININ GERCEK MOTIVASYONU
(Ihtiyac + notlardan cikarilan gercek sebep — veli aslinda ne istiyor, neye deger veriyor, neye para oduyor)

## 🏆 SIFIR HATA KAYIT SENARYOSU

### ADIM 1: HAZIRLLIK (gorusmeden once)
(Hangi belgeleri hazirla, hangi bilgileri topla, ortami nasil kur)

### ADIM 2: ACILIS (ilk 3 dakika)
(Tam kelimesi kelimesine acilis cumlesi — güven + sicaklik + profesyonellik)
**Acilis Cumlesi:** "..."

### ADIM 3: BAGLANTI KUR (3 dakika)
(Velinin ihtiyaclarına referans vererek empati kur — notlardaki detayları kullan)
**Cumle:** "..."

### ADIM 4: TEST SONUCU SUN (5 dakika)
(SADECE yapilan testleri sun — yapilmamis test hakkinda konusma)
Her test icin:
a) Guclu yonu soyle: "Cocugunuzun [alan] alaninda cok guclu — [skor] puan"
b) Okulun bu guce cevabi: "Biz bu yetenegi [program/etkinlik] ile destekliyoruz"
c) Gelisim alani (zayif DEME): "Su alanda potansiyel var — [destek programi] ile aciga cikariyoruz"
d) Ogrenme stili: "Cocugunuz [VARK sonucu] tarzinda ogreniyor — siniflarimiz tam buna uygun"
**Cumle ornegi:** "Test sonuclarina baktığımızda [isim]'in [guclu alan] alaninda cok basarili oldugunu goruyoruz..."

### ADIM 5: IHTIYACA OZEL COZUM SUN (5 dakika)
(SADECE velinin belirttigi ihtiyaclara cevap ver — gereksiz konu acma!)
Her ihtiyac icin:
a) Velinin ihtiyacini tekrarla: "Siz [ihtiyac] konusunda hassassiniz, cok haklisiniz"
b) Okulun SOMUT cevabi: "[Program/ogretmen/tesis] ile bu ihtiyaci karsiliyoruz"
c) Kanit: "[Basari orani/referans/gercek ornek]"
Velinin BELIRTMEDIGI ihtiyac hakkinda KONUSMA — vakit kaybi + guven kaybettirir.
**Cumle ornegi:** "Siz [ihtiyac] konusunda cok haklisiniz. Biz tam da bu nedenle..."

### ADIM 6: FIYAT & DEGER (3 dakika)
(Fiyati nasil sunacaginiz — once deger, sonra fiyat, indirim/kampanya vurgusu)
**Cumle:** "..."

### ADIM 7: KAYIT YONLENDIRME (2 dakika)
(Dogrudan kayit talebi — yumusak ama kararlı — secenekler sun, "hangisini tercih edersiniz" formatı)
**Cumle:** "..."

### ADIM 8: ITIRAZ KARSILAMA
Her itiraz icin birebir cevap:
- **"Dusunecegiz"** → ...
- **"Esimle/babasi ile konusacagim"** → ...
- **"Baska okullara da bakiyoruz"** → ...
- **"Fiyat yuksek"** → ...
- **"Cocuk istemiyor/korkuyor"** → ...
- **"Zamanlama uygun degil"** → ...

### ADIM 9: KAPATIS
(Karar alindiysa: sozlesme yonlendirme. Alinmadiysa: sonraki gorusme + aciliyet)
**Evet ise:** "..."
**Hayir ise:** "..."

### ADIM 10: GORUSME SONRASI (24 saat icinde)
(Tesekkur mesaji + takip plani + hatirlatma zamanlari)

## ⚡ ACILIYET STRATEJISI
(Bu aday icin neden SIMDI kayit olmali — 3 guclu aciliyet cumlesi)

## 📅 7 GUNLUK TAKIP PLANI
- **Gun 1:** ...
- **Gun 2:** ...
- **Gun 3:** ...
- **Gun 4:** ...
- **Gun 5:** ...
- **Gun 6:** ...
- **Gun 7:** ...

## 💎 ALTIN KURAL
(Bu adayi MUTLAK kayit ettirmek icin uyulmasi gereken TEK kural — 1 guclu cumle)

ONEMLI KURALLAR:
- Her cumle HAZIR KULLANILACAK sekilde yaz — kelimesi kelimesine
- Notlardaki her ipucunu kullan
- Velinin ismini cumlelerde kullan
- Ogrencinin ismini cumlelerde kullan
- Test sonuclarini somut olarak referans goster
- Hic bir gorusme kayip donusmemeli — her gorusmeden kayit cikmali
- Turkce yaz, samimi ama profesyonel ol""")  # inject_rules kapanisi

        user_prompt = f"""ADAY BILGILERI:
- Ogrenci: {aday.ogrenci_adi} | Veli: {aday.veli_adi}
- Kademe: {aday.kademe} | Mevcut: {aday.mevcut_sinif} -> Hedef: {aday.hedef_sinif}
- Cinsiyet: {aday.cinsiyet} | Mevcut Okul: {aday.mevcut_okul} ({aday.okul_turu})
- Kanal: {aday.kanal} | Kampanya: {aday.kampanya}
- Pipeline: {aday.pipeline_info.get('label', aday.asama)}
- Surec Suresi: {surec_gun} gun (ilk kayit: {aday.olusturma_tarihi})
- {ilk_ulasim} | {ilk_gorusme}

ARAMA GECMISI ({aday.arama_sayisi} arama):
{arama_ozet if arama_ozet else "Hic arama yapilmamis."}

GORUSME GECMISI ({aday.gorusme_sayisi} gorusme):
{gorusme_ozet if gorusme_ozet else "Hic gorusme yapilmamis."}

TEST SONUCLARI ({len(aday.testler)} test):
{test_ozet if test_ozet else "Hic test uygulanmamis."}

IHTIYAC ANALIZI ({len(aday.ihtiyaclar)} kategori):
{ihtiyac_ozet if ihtiyac_ozet else "Ihtiyac analizi yapilmamis."}

{"FIYAT: " + fiyat_ozet if fiyat_ozet else "Fiyat henuz verilmemis."}

{"GENEL NOTLAR:" + chr(10) + genel_notlar if genel_notlar else "Ek not yok."}

VELI PROFILI:
{chr(10).join(f'- {k}: {v}' for k, v in (aday.veli_profil or {}).items() if v) or 'Veli profili henuz doldurulmamis.'}

OGRENCI PROFILI:
{chr(10).join(f'- {k}: {v}' for k, v in (aday.ogrenci_profil or {}).items() if v) or 'Ogrenci profili henuz doldurulmamis.'}

Bu adayin TUM verilerini analiz et — veli profili, ogrenci profili, testler, ihtiyaclar, aramalar, gorusmeler, notlar HEPSINI birlestir. Kayit olma ihtimalini degerlendir. Somut aksiyon plani olustur."""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=4096,
            temperature=0.7,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        st.error(f"AI analiz hatasi: {e}")
        return ""


def _generate_ai_analiz_pdf(aday: KayitAday, ai_result: str) -> bytes | None:
    """AI Kayit Senaryosu PDF — profesyonel rapor + grafikler."""
    try:
        from utils.report_utils import ReportPDFGenerator
        from utils.shared_data import load_kurum_profili
        import pandas as _pd

        kp = load_kurum_profili()
        k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")
        logo_path = kp.get("logo_path", "")

        fb = aday.fiyat_bilgi or {}
        toplam_ucret = float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0)
        try:
            surec_gun = (date.today() - date.fromisoformat(aday.olusturma_tarihi[:10])).days
        except (ValueError, TypeError):
            surec_gun = 0

        pdf = ReportPDFGenerator(
            f"AI Kayit Senaryosu — {aday.ogrenci_adi}",
            f"Veli: {aday.veli_adi} | {aday.kademe} {aday.hedef_sinif} | {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        )
        pdf.add_header(k_adi, logo_path)

        # Metrikler
        pdf.add_section("Aday Durum Ozeti", "#3b82f6")
        pdf.add_metrics([
            ("Arama", str(aday.arama_sayisi), "#facc15"),
            ("Gorusme", str(aday.gorusme_sayisi), "#60a5fa"),
            ("Test", str(len(aday.testler)), "#a78bfa"),
            ("Ihtiyac", str(len(aday.ihtiyaclar)), "#10b981"),
            ("Gun", str(surec_gun), "#f59e0b"),
        ])
        pdf.add_text(f"Ogrenci: {aday.ogrenci_adi} | Veli: {aday.veli_adi} | Tel: {aday.veli_telefon}")
        pdf.add_text(f"Kademe: {aday.kademe} | Hedef: {aday.hedef_sinif} | Kanal: {aday.kanal} | Kampanya: {aday.kampanya}")
        pdf.add_text(f"Asama: {aday.pipeline_info.get('label', aday.asama)} | Mevcut Okul: {aday.mevcut_okul} ({aday.okul_turu})")
        if toplam_ucret > 0:
            pdf.add_text(f"Fiyat: {toplam_ucret:,.0f} TL | Indirim: %{fb.get('toplam_indirim', 0):.0f}")
        pdf.add_spacer(0.3)

        # Pipeline grafigi
        asamalar_done = {"aday": 1, "arandi": 2, "randevu": 3, "gorusme": 4, "fiyat_verildi": 5, "sozlesme": 6, "kesin_kayit": 7}
        current = asamalar_done.get(aday.asama, 0)
        pdf.add_donut_chart({"Tamamlanan": current, "Kalan": 7 - current},
                            f"Pipeline Ilerleme: {aday.pipeline_info.get('label', '')}", ["#10b981", "#1e293b"])

        # Test skor grafigi
        if aday.testler:
            for t in aday.testler:
                skorlar = t.get("skorlar", {})
                numeric = {k: v for k, v in skorlar.items() if isinstance(v, (int, float)) and v > 0}
                if numeric:
                    pdf.add_donut_chart(numeric, f'{t.get("test_adi", "")}: {t.get("sonuc", "")}')

        # Arama gecmisi tablosu
        if aday.aramalar:
            pdf.add_section("Arama Gecmisi", "#facc15")
            ar_rows = [{"#": ar.get("arama_no", ""), "Tarih": str(ar.get("tarih", ""))[:10],
                         "Sonuc": ar.get("sonuc", ""), "Not": (ar.get("not", "") or "")[:50]} for ar in aday.aramalar]
            pdf.add_table(_pd.DataFrame(ar_rows), "#facc15")

        # Gorusme gecmisi tablosu
        if aday.gorusmeler:
            pdf.add_section("Gorusme Gecmisi", "#60a5fa")
            gr_rows = [{"#": gr.get("gorusme_no", ""), "Tarih": str(gr.get("tarih", ""))[:10],
                         "Sonuc": gr.get("sonuc", ""), "Not": (gr.get("not", "") or "")[:50]} for gr in aday.gorusmeler]
            pdf.add_table(_pd.DataFrame(gr_rows), "#60a5fa")

        # Ihtiyac analizi
        if aday.ihtiyaclar:
            pdf.add_section("Ihtiyac Analizi", "#10b981")
            ih_rows = [{"Oncelik": ih.get("oncelik", ""), "Kategori": ih.get("kategori", ""),
                         "Aciklama": ih.get("aciklama", "")[:50]} for ih in aday.ihtiyaclar]
            pdf.add_table(_pd.DataFrame(ih_rows), "#10b981")

        # AI Kayit Senaryosu
        pdf.add_section("AI KAYIT SENARYOSU", "#7c3aed")

        _section_colors = {
            "PROFIL": "#3b82f6", "KAYIT": "#10b981", "ILETISIM": "#facc15", "AKADEMIK": "#a78bfa",
            "MOTIVASYON": "#ec4899", "SIFIR HATA": "#7c3aed", "SENARYO": "#7c3aed",
            "ADIM": "#0ea5e9", "ACILIYET": "#ef4444", "TAKIP": "#14b8a6", "ALTIN": "#C8952E",
            "HAZIRLIK": "#8b5cf6", "ACILIS": "#10b981", "BAGLANTI": "#3b82f6", "TEST": "#a78bfa",
            "COZUM": "#0ea5e9", "FIYAT": "#f59e0b", "YONLENDIRME": "#ec4899", "ITIRAZ": "#ef4444",
            "KAPATIS": "#10b981", "SONRASI": "#14b8a6", "RISK": "#ef4444", "SINYAL": "#4ade80",
        }

        current_lines: list[str] = []

        def flush():
            nonlocal current_lines
            for ln in current_lines:
                if ln.strip():
                    pdf.add_text(ln.strip())
            current_lines = []

        for line in ai_result.split("\n"):
            stripped = line.strip()
            if stripped.startswith("## "):
                flush()
                title = stripped.lstrip("#").strip()
                color = "#7c3aed"
                for key, clr in _section_colors.items():
                    if key in title.upper():
                        color = clr
                        break
                pdf.add_section(title, color)
            elif stripped.startswith("### "):
                flush()
                pdf.add_text(f"▸ {stripped.lstrip('#').strip()}")
            else:
                current_lines.append(line)
        flush()

        pdf.add_spacer(0.5)
        pdf.add_text(f"Bu rapor {datetime.now().strftime('%d.%m.%Y %H:%M')} tarihinde SmartCampus AI tarafindan olusturulmustur.")
        pdf.add_text("Sifir hata kayit senaryosu — her gorusmeden kesin kayit hedeflenmektedir.")

        return pdf.generate()
    except Exception:
        return None


def _render_aday_gecmis_notlar(store: KayitDataStore, aday: KayitAday):
    """Adayin tum surec gecmisi + notlar — kronolojik zaman cizelgesi."""

    # Tum olaylari kronolojik sirala
    events: list[dict] = []

    # Aramalar
    for ar in aday.aramalar:
        events.append({
            "tarih": ar.get("tarih", ""),
            "tip": "arama",
            "emoji": "📞",
            "renk": "#facc15",
            "baslik": f'{ar.get("arama_no", "")}. Arama — {ar.get("sonuc", "")}',
            "not": ar.get("not", "") or ar.get("notlar", ""),
        })

    # Gorusmeler
    for gr in aday.gorusmeler:
        events.append({
            "tarih": gr.get("tarih", ""),
            "tip": "gorusme",
            "emoji": "🤝",
            "renk": "#60a5fa",
            "baslik": f'{gr.get("gorusme_no", "")}. Gorusme — {gr.get("sonuc", "")}',
            "not": gr.get("not", "") or gr.get("notlar", ""),
        })

    # Testler
    for t in aday.testler:
        events.append({
            "tarih": t.get("tarih", ""),
            "tip": "test",
            "emoji": "🧪",
            "renk": "#a78bfa",
            "baslik": f'{t.get("test_adi", "")} — {t.get("sonuc", "")}',
            "not": t.get("notlar", ""),
        })

    # Genel notlar (eger varsa)
    if aday.notlar:
        events.append({
            "tarih": aday.olusturma_tarihi,
            "tip": "not",
            "emoji": "📝",
            "renk": "#94a3b8",
            "baslik": "Genel Not",
            "not": aday.notlar,
        })

    # Sirala (yeniden eskiye)
    events.sort(key=lambda x: x.get("tarih", ""), reverse=True)

    # Goster
    with st.expander(f"📜 Surec Gecmisi & Notlar ({len(events)} kayit)", expanded=False):
        if not events:
            st.caption("Henuz islem kaydi yok.")
        else:
            for ev in events:
                tarih_str = str(ev["tarih"])[:16].replace("T", " ") if ev["tarih"] else "-"
                not_text = ev.get("not", "")
                not_html = f'<div style="color:#e2e8f0;font-size:0.82rem;margin-top:3px;padding-left:12px;border-left:2px solid {ev["renk"]}30">{not_text}</div>' if not_text else ""
                st.markdown(
                    f'<div style="padding:8px 12px;margin:4px 0;background:#111827;border:1px solid #1e293b;'
                    f'border-radius:8px;border-left:4px solid {ev["renk"]}">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<span style="color:{ev["renk"]};font-weight:700;font-size:0.88rem">{ev["emoji"]} {ev["baslik"]}</span>'
                    f'<span style="color:#64748b;font-size:0.75rem">{tarih_str}</span></div>'
                    f'{not_html}</div>',
                    unsafe_allow_html=True)

        # ── Not Ekle ──
        st.markdown("")
        st.markdown(
            '<div style="color:#6ee7b7;font-weight:700;margin:8px 0">📝 Not Ekle</div>',
            unsafe_allow_html=True)
        not_tipleri = ["Genel Not", "Arama Notu", "Gorusme Notu", "Veli Talebi", "Takip Notu", "Diger"]
        nc1, nc2 = st.columns([1, 3])
        with nc1:
            not_tipi = st.selectbox("Not Tipi", not_tipleri, key=f"km_not_tip_{aday.id}")
        with nc2:
            not_icerik = st.text_area("Not", key=f"km_not_icerik_{aday.id}", height=80,
                                       placeholder="Aday hakkinda not ekleyin...")
        if st.button("💾 Notu Kaydet", type="primary", key=f"km_not_kaydet_{aday.id}", use_container_width=True):
            if not_icerik.strip():
                tum = store.load_all()
                for a in tum:
                    if a.id == aday.id:
                        # Notu uygun yere ekle
                        if not_tipi == "Arama Notu":
                            a.aramalar.append({
                                "arama_no": 0,
                                "tarih": datetime.now().isoformat(),
                                "sonuc": "Not eklendi",
                                "not": f"[{not_tipi}] {not_icerik.strip()}",
                            })
                        elif not_tipi == "Gorusme Notu":
                            a.gorusmeler.append({
                                "gorusme_no": 0,
                                "tarih": datetime.now().isoformat(),
                                "sonuc": "Not eklendi",
                                "not": f"[{not_tipi}] {not_icerik.strip()}",
                            })
                        else:
                            # Genel not — notlar alanina ekle
                            mevcut = a.notlar or ""
                            tarih_str = datetime.now().strftime("%d.%m.%Y %H:%M")
                            yeni_not = f"[{tarih_str} | {not_tipi}] {not_icerik.strip()}"
                            a.notlar = f"{mevcut}\n{yeni_not}".strip() if mevcut else yeni_not
                        a.son_islem_tarihi = date.today().isoformat()
                        break
                store.save_all(tum)
                st.success(f"Not kaydedildi: {not_tipi}")
                st.rerun()
            else:
                st.warning("Not icerigi bos olamaz.")


def _render_aday_islem(store: KayitDataStore, adaylar: list[KayitAday], secili_id: str = ""):
    if not adaylar:
        styled_info_banner("Henuz aday yok. Yeni Aday sekmesinden ekleyin.", "info")
        return

    # Pipeline'dan gelen seçili aday
    if secili_id:
        aday = store.get_by_id(secili_id)
        if aday:
            # Doğrudan aday işlem ekranına git (aşağıda devam)
            pass
        else:
            st.error("Aday bulunamadı.")
            return
    else:
        # Aday secici
        aktif_adaylar = [a for a in adaylar if a.aktif]
        tum_adaylar = adaylar

        goster = st.radio("Goster", ["Aktif Adaylar", "Tum Adaylar"], horizontal=True, key="km_islem_goster")
        liste = aktif_adaylar if goster == "Aktif Adaylar" else tum_adaylar

        options = ["-- Aday Sec --"] + [
            f"{a.pipeline_info['emoji']} {a.label} [{a.pipeline_info['label']}]" for a in liste
        ]
        sec = st.selectbox("Aday", options, key="km_islem_sec")

        if sec == "-- Aday Sec --":
            st.info("Islem yapmak icin bir aday secin.")
            return

    if not secili_id:
        idx = options.index(sec) - 1
        aday = liste[idx]
    info = aday.pipeline_info

    # Durum banner
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{info["bg"]},{info["color"]}10);'
        f'border:2px solid {info["color"]};border-radius:14px;padding:16px 20px;margin:8px 0 16px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'
        f'<div>'
        f'<div style="font-size:1.15rem;font-weight:800;color:#f1f5f9">{info["emoji"]} {aday.label}</div>'
        f'<div style="font-size:0.85rem;color:#94a3b8;margin-top:4px">'
        f'📞 {aday.veli_telefon or "-"} | 🎓 {aday.kademe or "-"} | '
        f'📢 {aday.kampanya or "-"} | {aday.kanal or "-"}</div></div>'
        f'<div style="text-align:right">'
        f'<div style="background:{info["color"]};color:#fff;padding:6px 16px;border-radius:20px;'
        f'font-size:0.85rem;font-weight:700">{info["label"]}</div>'
        f'<div style="font-size:0.75rem;color:{info["color"]};margin-top:4px">→ {info.get("aksiyon", "")}</div>'
        f'</div></div></div>',
        unsafe_allow_html=True)

    # Ilerleme bari
    done_idx = PIPELINE_ASAMALARI.index(aday.asama) if aday.asama in PIPELINE_ASAMALARI else 0
    steps_html = '<div style="display:flex;gap:3px;margin-bottom:14px">'
    for i, key in enumerate(PIPELINE_ASAMALARI):
        si = PIPELINE_INFO[key]
        is_done = i <= done_idx and aday.asama != "olumsuz"
        bg = si["color"] if is_done else "#1e293b"
        txt = "#fff" if is_done else "#4b5563"
        radius = "8px 0 0 8px" if i == 0 else ("0 8px 8px 0" if i == len(PIPELINE_ASAMALARI) - 1 else "0")
        steps_html += (
            f'<div style="flex:1;text-align:center;padding:5px 2px;background:{bg};'
            f'border-radius:{radius};font-size:0.6rem;font-weight:700;color:{txt}">{si["label"]}</div>'
        )
    steps_html += '</div>'
    st.markdown(steps_html, unsafe_allow_html=True)

    # ── SUREC GECMISI + NOTLAR (her aday icin gorunur) ──
    _render_aday_gecmis_notlar(store, aday)

    # ── SONUÇ EKRANI (arama/görüşme sonrası) ──
    _sonuc_key = f"_km_sonuc_{aday.id}"
    if _sonuc_key in st.session_state:
        _s = st.session_state[_sonuc_key]
        _s_tip = _s.get("tip", "")
        _s_icon = "📞" if _s_tip == "arama" else "🤝"
        _s_clr = "#0ea5e9" if _s_tip == "arama" else "#f59e0b"
        _s_baslik = f'{_s.get("no", "")}. {"Arama" if _s_tip == "arama" else "Görüşme"} Kaydedildi'

        st.markdown(
            f'<div style="background:linear-gradient(135deg,{_s_clr}20,{_s_clr}08);'
            f'border:2px solid {_s_clr};border-radius:14px;padding:16px 20px;margin-bottom:12px;">'
            f'<h3 style="margin:0;color:{_s_clr};">{_s_icon} {_s_baslik}</h3>'
            f'<div style="margin-top:8px;color:#e2e8f0;">'
            f'<div style="font-size:14px;"><b>Aday:</b> {_s.get("aday_label", "")}</div>'
            f'<div style="font-size:14px;"><b>Sonuç:</b> {_s.get("sonuc", "-")}</div>'
            f'<div style="font-size:13px;"><b>Tarih:</b> {_s.get("tarih", "")}</div>'
            + (f'<div style="background:#1e293b;border-radius:8px;padding:8px 12px;margin-top:8px;'
               f'font-size:13px;color:#cbd5e1;"><b>📝 Not:</b> {_s["not"]}</div>' if _s.get("not") else '')
            + (f'<div style="color:#60a5fa;font-size:12px;margin-top:4px;">ℹ️ {_s["mesaj"]}</div>' if _s.get("mesaj") else '')
            + (f'<div style="color:#fbbf24;font-size:13px;margin-top:6px;font-weight:700;">'
               f'📅 Sonraki Takip: {_s["takip"]}</div>' if _s.get("takip") else '')
            + '</div>',
            unsafe_allow_html=True)

        # AI Not Analizi sonucu
        na = _s.get("ai_analiz")
        if na:
            _na_clr = {"olumlu": "#22c55e", "olumsuz": "#ef4444", "endiseli": "#f59e0b",
                        "kizgin": "#ef4444", "kararsiz": "#f59e0b", "notr": "#64748b"}.get(na.get("duygu"), "#64748b")
            st.markdown(
                f'<div style="background:{_na_clr}12;border-left:4px solid {_na_clr};'
                f'border-radius:0 10px 10px 0;padding:12px 16px;margin-top:8px;">'
                f'<div style="font-weight:700;color:{_na_clr};font-size:14px;">🤖 AI Not Analizi</div>'
                f'<div style="margin-top:6px;color:#cbd5e1;">'
                f'<div>😊 <b>Duygu:</b> {na.get("duygu", "-")}</div>'
                f'<div>🎯 <b>Niyet:</b> {na.get("niyet", "-")}</div>'
                f'<div>⚡ <b>Önem:</b> {na.get("onem", "-")}</div>'
                + (f'<div style="margin-top:4px;color:#fca5a5;">⚠️ <b>Risk Sinyali:</b> {na["risk_sinyali"]}</div>' if na.get("risk_sinyali") else '')
                + (f'<div style="margin-top:4px;color:#86efac;">✅ <b>Fırsat:</b> {na["firsat_sinyali"]}</div>' if na.get("firsat_sinyali") else '')
                + f'<div style="margin-top:6px;padding-top:6px;border-top:1px solid {_na_clr}30;'
                  f'color:{_na_clr};font-weight:700;font-size:13px;">'
                  f'→ Sonraki Adım: {na.get("sonraki_aksiyon", "-")}</div>'
                + '</div></div>',
                unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Kapat butonu
        if st.button("✓ Tamam, devam et", key=f"km_sonuc_kapat_{aday.id}", use_container_width=True):
            del st.session_state[_sonuc_key]
            st.rerun()

        st.markdown("---")

    # ── VERİ DOLULUK GÖSTERGESİ ──
    from models.kayit_ai_engine import veri_doluluk_analizi, veri_eksik_uyari
    _vda = veri_doluluk_analizi(aday)
    _vdu = veri_eksik_uyari(aday)
    _vd_clr = "#22c55e" if _vda["toplam_yuzde"] >= 70 else "#f59e0b" if _vda["toplam_yuzde"] >= 40 else "#ef4444"
    st.markdown(
        f'<div style="background:#0f172a;border:1px solid {_vd_clr}40;border-radius:10px;'
        f'padding:10px 14px;margin-bottom:8px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span style="color:#94a3b8;font-size:12px;">📊 Veri Doluluk</span>'
        f'<span style="color:{_vd_clr};font-weight:800;font-size:16px;">%{_vda["toplam_yuzde"]}</span></div>'
        f'<div style="background:#1e293b;border-radius:4px;height:6px;margin-top:4px;">'
        f'<div style="background:{_vd_clr};height:6px;border-radius:4px;width:{_vda["toplam_yuzde"]}%;"></div></div>'
        + (f'<div style="margin-top:4px;">'
           + "".join(f'<span style="display:inline-block;background:{_vd_clr}20;border-radius:4px;'
                     f'padding:1px 6px;margin:1px;font-size:10px;color:{_vd_clr};">'
                     f'{k["kaynak"]}:{k["yuzde"]}%</span>' for k in _vda["kaynaklar"])
           + '</div>')
        + (''.join(f'<div style="color:#fca5a5;font-size:10px;margin-top:2px;">⚠ {u}</div>' for u in _vdu) if _vdu else '')
        + '</div>',
        unsafe_allow_html=True)

    # AI Yol Haritası butonu
    if st.button("🗺️ AI Yol Haritası (Tüm Veriye Dayalı)", key=f"km_yh_{aday.id}", use_container_width=True):
        with st.spinner("AI yol haritası çiziyor..."):
            from models.kayit_ai_engine import ai_yol_haritasi
            result = ai_yol_haritasi(aday)
            if result:
                st.session_state[f"_km_yh_{aday.id}"] = result
    if f"_km_yh_{aday.id}" in st.session_state:
        with st.expander("🗺️ AI Yol Haritası", expanded=True):
            st.markdown(st.session_state[f"_km_yh_{aday.id}"])

    # ── AŞAMA REHBERİ ──
    from models.kayit_ai_engine import get_asama_rehber
    _rehber = get_asama_rehber(aday.asama)
    if _rehber.get("yapilacaklar"):
        _rclr = {"aday": "#3b82f6", "arandi": "#f59e0b", "randevu": "#8b5cf6",
                 "gorusme": "#f97316", "fiyat_verildi": "#ef4444", "sozlesme": "#10b981",
                 "kesin_kayit": "#22c55e"}.get(aday.asama, "#64748b")
        st.markdown(
            f'<div style="background:{_rclr}12;border:1px solid {_rclr}40;border-radius:10px;'
            f'padding:12px 16px;margin-bottom:10px;">'
            f'<div style="color:{_rclr};font-weight:700;font-size:14px;">{_rehber["baslik"]}</div>'
            f'<div style="color:#94a3b8;font-size:12px;margin-top:2px;">Hedef: {_rehber["hedef"]}</div>'
            f'<div style="margin-top:6px;">'
            + "".join(f'<div style="color:#cbd5e1;font-size:11px;padding:1px 0;">☐ {y}</div>' for y in _rehber["yapilacaklar"])
            + f'</div>'
            f'<div style="color:#fbbf24;font-size:11px;margin-top:4px;font-weight:600;">⚠ {_rehber["dikkat"]}</div>'
            f'<div style="color:#60a5fa;font-size:10px;margin-top:2px;">AI: {_rehber["ai_destek"]}</div></div>',
            unsafe_allow_html=True)

    # ── SIFIR KAYIP KONTROL ──
    from models.kayit_sifir_kayip import sifir_kayip_kontrol
    _sk = sifir_kayip_kontrol(aday)
    if _sk:
        _sk_clr = "#ef4444" if _sk["aciliyet"] == "KRITIK" else "#f97316" if _sk["aciliyet"] == "YUKSEK" else "#f59e0b"
        st.markdown(
            f'<div style="background:{_sk_clr}15;border:2px solid {_sk_clr};border-radius:10px;'
            f'padding:12px 16px;margin-bottom:10px;">'
            f'<b style="color:{_sk_clr};font-size:14px;">🚨 KAYIP RİSKİ: {_sk["aciliyet"]}</b>'
            f'<div style="color:#fca5a5;font-size:12px;margin-top:4px;">Neden: {_sk["risk_nedeni"]}</div>'
            f'<div style="color:#86efac;font-size:12px;margin-top:4px;">Kurtarma: {_sk["kurtarma_plani"]}</div></div>',
            unsafe_allow_html=True)

    # ── AI ADAY ASİSTANI ──
    with st.expander("🤖 AI Asistan — Bu aday hakkında her şeyi sor", expanded=False):
        _asistan_soru = st.text_input("Sorunuzu yazın (boş bırakırsanız genel analiz):",
                                       key=f"km_asistan_q_{aday.id}", placeholder="Bu veliyi nasıl ikna edebilirim?")
        _ac1, _ac2 = st.columns(2)
        with _ac1:
            if st.button("🤖 Asistana Sor", key=f"km_asistan_btn_{aday.id}", use_container_width=True):
                with st.spinner("AI düşünüyor..."):
                    from models.kayit_sifir_kayip import ai_aday_asistani
                    result = ai_aday_asistani(aday, _asistan_soru)
                    if result:
                        st.session_state[f"_km_asistan_{aday.id}"] = result
        with _ac2:
            if st.button("🔄 Alternatif Strateji", key=f"km_alt_btn_{aday.id}", use_container_width=True):
                with st.spinner("AI alternatif üretiyor..."):
                    from models.kayit_sifir_kayip import ai_alternatif_strateji
                    result = ai_alternatif_strateji(aday)
                    if result:
                        st.session_state[f"_km_alt_{aday.id}"] = result
        if f"_km_asistan_{aday.id}" in st.session_state:
            st.markdown(st.session_state[f"_km_asistan_{aday.id}"])
        if f"_km_alt_{aday.id}" in st.session_state:
            st.markdown(st.session_state[f"_km_alt_{aday.id}"])

    # ── AI SON ANALIZ EKRANI ──
    _render_ai_son_analiz(aday)

    # ── ISLEM SEKMELERI ──
    if aday.asama == "olumsuz":
        st.markdown(
            '<div style="background:#450a0a;border:2px solid #f87171;border-radius:10px;'
            'padding:14px;text-align:center"><span style="color:#fca5a5;font-size:1rem;font-weight:700">'
            '❌ Bu aday olumsuz sonuclanmistir.</span></div>',
            unsafe_allow_html=True)
        # AI Kayıp Analizi
        if st.button("🤖 AI Kayıp Analizi — Neden kaybettik? Geri kazanılabilir mi?",
                      key=f"km_ai_kayip_{aday.id}", type="primary", use_container_width=True):
            with st.spinner("AI kayıp analizi yapıyor..."):
                from models.kayit_ai_engine import ai_kayip_analizi
                result = ai_kayip_analizi(aday)
                if result:
                    st.session_state[f"_km_kayip_{aday.id}"] = result
        if f"_km_kayip_{aday.id}" in st.session_state:
            st.markdown(st.session_state[f"_km_kayip_{aday.id}"])
    elif aday.asama == "kesin_kayit":
        st.markdown(
            '<div style="background:#052e16;border:2px solid #4ade80;border-radius:10px;'
            'padding:14px;text-align:center">'
            '<span style="color:#4ade80;font-size:1.1rem;font-weight:800">✅ Kesin Kayit Tamamlanmistir</span><br>'
            '<span style="color:#6ee7b7;font-size:0.85rem">Bu aday salt okunurdur. Detaylar icin "Kayit Olanlar" sekmesine bakiniz.</span>'
            '</div>',
            unsafe_allow_html=True)
        # AI Hoş Geldin Süreci
        if st.button("🤖 AI Hoş Geldin Süreci (İlk 30 Gün Planı)", key=f"km_ai_hg_{aday.id}",
                      type="primary", use_container_width=True):
            with st.spinner("AI hoş geldin planı hazırlıyor..."):
                from models.kayit_ai_engine import ai_hosgeldin_sureci
                result = ai_hosgeldin_sureci(aday)
                if result:
                    st.session_state[f"_km_hg_{aday.id}"] = result
        if f"_km_hg_{aday.id}" in st.session_state:
            st.markdown(st.session_state[f"_km_hg_{aday.id}"])
        # Salt okunur bilgi goster
        fb = aday.fiyat_bilgi or {}
        sb = aday.sozlesme_bilgi or {}
        st.markdown(
            f'<div style="background:#111827;border:1px solid #334155;border-radius:8px;'
            f'padding:12px;margin:10px 0;color:#94a3b8;font-size:0.85rem">'
            f'<strong style="color:#e2e8f0">Ozet:</strong> '
            f'Kayit Tarihi: {aday.kapanma_tarihi or "-"} | '
            f'Toplam Ucret: {float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0):,.0f} TL | '
            f'Arama: {aday.arama_sayisi} | Gorusme: {aday.gorusme_sayisi} | Test: {len(aday.testler)}</div>',
            unsafe_allow_html=True)
    else:
        # ZIRVE: Aday 360 Akilli Karne (premium ust panel)
        try:
            from utils.kayit_aday_360 import render_aday_360_karne
            render_aday_360_karne(aday)
        except Exception:
            pass

        # ZIRVE: Yolculuk Haritasi (collapsible)
        with st.expander("🗺️ Yolculuk Haritasi (Customer Journey)", expanded=False):
            try:
                from utils.kayit_yolculuk import render_yolculuk_haritasi
                render_yolculuk_haritasi(aday)
            except Exception as _e:
                st.error(f"Yolculuk haritasi yuklenemedi: {_e}")

        # MEGA: Aday DNA Esleme (Lookalike)
        with st.expander("🧬 DNA Esleme (Gecmis Benzer Adaylar)", expanded=False):
            try:
                from utils.kayit_lookalike_ui import render_lookalike_paneli
                render_lookalike_paneli(aday)
            except Exception as _e:
                st.error(f"Lookalike paneli yuklenemedi: {_e}")

        at1, at2, at3, at4, at5, at6, at7 = st.tabs([
            f"  📞 {info['aksiyon']}  " if aday.asama in ("aday", "arandi") else "  📞 Arama  ",
            "  🤝 Gorusme  ",
            "  💰 Fiyat  ",
            "  📄 Sozlesme  ",
            "  📋 MEB Sozlesme  ",
            "  👤 Profil  ",
            "  📁 Belge Vault  ",
        ])

        # ZIRVE: Belge Vault sekmesi
        with at7:
            try:
                from utils.kayit_belge_ui import render_belge_vault
                render_belge_vault(aday)
            except Exception as _e:
                st.error(f"Belge vault yuklenemedi: {_e}")

        # ── ARAMA ──
        with at1:
            if aday.asama == "randevu":
                styled_info_banner("✅ Randevu alindi — Gorusme sekmesinden devam edin. Ama takip aramasi da yapabilirsiniz.", "success")
                # AI Randevu Yöneticisi
                if st.button("🤖 AI Randevu Yöneticisi (Onay + Hatırlatma + Checklist)", key=f"km_ai_randevu_{aday.id}"):
                    with st.spinner("AI randevu planı hazırlıyor..."):
                        from models.kayit_ai_engine import ai_randevu_yonetici
                        result = ai_randevu_yonetici(aday)
                        if result:
                            st.session_state[f"_km_randevu_{aday.id}"] = result
                if f"_km_randevu_{aday.id}" in st.session_state:
                    st.markdown(st.session_state[f"_km_randevu_{aday.id}"])
            # Arama her aşamada yapılabilir
            if aday.asama in ("aday", "arandi", "randevu", "gorusme", "fiyat_verildi", "sozlesme"):
                st.markdown(
                    f'<div style="color:#7dd3fc;font-weight:700;margin-bottom:8px">'
                    f'📞 {aday.arama_sayisi + 1}. Arama Kaydi</div>',
                    unsafe_allow_html=True)
                # Ulasim yok uyarisi
                if aday.ulasim_yok_sayisi > 0:
                    st.markdown(
                        f'<div style="background:#450a0a80;border:1px solid #f8717130;border-radius:6px;'
                        f'padding:6px 10px;margin-bottom:8px;color:#fca5a5;font-size:0.85rem">'
                        f'⚠️ Ardisik {aday.ulasim_yok_sayisi} kez ulasim yok. '
                        f'({MAX_ULASIM_YOK_ARAMA} kez olursa otomatik olumsuz kapanir)</div>',
                        unsafe_allow_html=True)

                # AI Arama Script + Lead Score
                _ai_col1, _ai_col2 = st.columns(2)
                with _ai_col1:
                    if st.button("🤖 AI Arama Senaryosu", key=f"km_ai_script_{aday.id}", use_container_width=True):
                        with st.spinner("AI senaryo hazırlıyor..."):
                            from models.kayit_ai_engine import ai_arama_script
                            result = ai_arama_script(aday)
                            if result:
                                st.session_state[f"_km_script_{aday.id}"] = result
                with _ai_col2:
                    if st.button("📊 AI Lead Skor", key=f"km_ai_ls_{aday.id}", use_container_width=True):
                        with st.spinner("Olasılık hesaplanıyor..."):
                            from models.kayit_ai_engine import ai_lead_score
                            ls = ai_lead_score(aday)
                            if ls:
                                st.session_state[f"_ls_{aday.id}"] = ls
                                ls_clr = "#22c55e" if ls.get("skor", 0) > 75 else "#f59e0b" if ls.get("skor", 0) > 50 else "#ef4444"
                                st.markdown(f'<div style="background:{ls_clr}20;border-left:3px solid {ls_clr};'
                                            f'padding:8px 12px;border-radius:0 8px 8px 0;">'
                                            f'<b style="color:{ls_clr};">Kayıt Olasılığı: %{ls["skor"]} ({ls.get("seviye", "?")})</b>'
                                            f'<br><span style="color:#94a3b8;font-size:12px;">{ls.get("neden", "")}</span>'
                                            f'<br><span style="color:#60a5fa;font-size:12px;">Aksiyon: {ls.get("aksiyon", "")}</span></div>',
                                            unsafe_allow_html=True)
                if f"_km_script_{aday.id}" in st.session_state:
                    st.markdown(st.session_state[f"_km_script_{aday.id}"])

                with st.form(f"km_arama_{aday.id}"):
                    sonuc = st.selectbox("Arama Sonucu *", ARAMA_SONUCLARI, key=f"km_ar_s_{aday.id}")

                    # Randevu alindi secilirse tarih/saat goster
                    r_tarih = ""
                    r_saat = ""
                    if sonuc == "Randevu alindi":
                        rc1, rc2 = st.columns(2)
                        with rc1:
                            r_tarih_input = st.date_input("Randevu Tarihi", key=f"km_ar_rt_{aday.id}")
                            r_tarih = str(r_tarih_input)
                        with rc2:
                            r_saat = st.text_input("Randevu Saati", placeholder="14:00", key=f"km_ar_rs_{aday.id}")

                    not_text = st.text_area("Not", key=f"km_ar_n_{aday.id}", height=68)
                    try:
                        from utils.shared_data import get_ik_employee_names
                        _personel_list = [""] + get_ik_employee_names()
                    except Exception:
                        _personel_list = [""]
                    arayan = st.selectbox("Aramayı Yapan", _personel_list, key=f"km_ar_yapan_{aday.id}")

                    if st.form_submit_button("Aramayi Kaydet", type="primary", use_container_width=True):
                        arama_no = aday.arama_sayisi + 1
                        mesaj = arama_kaydet(store, aday.id, sonuc, not_text,
                                             randevu_tarihi=r_tarih, randevu_saati=r_saat,
                                             yapan_kisi=arayan)
                        # Sonuç ekranı verisi oluştur
                        _sonuc = {
                            "tip": "arama", "no": arama_no, "sonuc": sonuc,
                            "not": not_text, "mesaj": mesaj or "",
                            "aday_label": aday.label, "tarih": date.today().isoformat(),
                            "takip": "",
                        }
                        # Takip tarihi
                        _guncellenmis = store.get_by_id(aday.id)
                        if _guncellenmis and _guncellenmis.sonraki_takip:
                            _sonuc["takip"] = _guncellenmis.sonraki_takip
                        # AI Not Analizi
                        # AI analiz — not varsa not analizi, yoksa sonuç analizi
                        _analiz_text = not_text.strip() if not_text.strip() else f"Arama sonucu: {sonuc}"
                        try:
                            from models.kayit_sifir_kayip import ai_not_analiz
                            from models.kayit_ai_engine import _aday_ozet
                            na = ai_not_analiz(_aday_ozet(aday), _analiz_text)
                            if na:
                                _sonuc["ai_analiz"] = na
                        except Exception:
                            pass
                        st.session_state[f"_km_sonuc_{aday.id}"] = _sonuc
                        st.rerun()

        # ── GORUSME ──
        with at2:
            if aday.asama in ("randevu", "gorusme", "arandi", "fiyat_verildi", "sozlesme"):
                st.markdown(
                    f'<div style="color:#fdba74;font-weight:700;margin-bottom:8px">'
                    f'🤝 {aday.gorusme_sayisi + 1}. Gorusme Kaydi</div>',
                    unsafe_allow_html=True)

                # ZIRVE: Gorusme Co-Pilot acici
                _copilot_key = f"_copilot_open_{aday.id}"
                if st.button("🎙️ Co-Pilot ile Görüş (Canlı AI Asistan)",
                             key=f"km_copilot_btn_{aday.id}",
                             use_container_width=True, type="primary"):
                    st.session_state[_copilot_key] = True

                if st.session_state.get(_copilot_key):
                    try:
                        from utils.kayit_gorusme_copilot import render_gorusme_copilot
                        render_gorusme_copilot(aday.id)
                    except Exception as e:
                        st.error(f"Co-Pilot hatasi: {e}")
                    if st.button("✕ Co-Pilot'u Kapat", key=f"km_copilot_close_{aday.id}",
                                 use_container_width=True):
                        st.session_state[_copilot_key] = False
                        st.rerun()
                    st.markdown("---")

                # AI Görüşme Stratejisi (klasik)
                if st.button("🤖 AI Görüşme Stratejisi", key=f"km_ai_gor_{aday.id}", use_container_width=True):
                    with st.spinner("AI strateji hazırlıyor..."):
                        from models.kayit_ai_engine import ai_gorusme_stratejisi
                        result = ai_gorusme_stratejisi(aday)
                        if result:
                            st.session_state[f"_km_gor_ai_{aday.id}"] = result
                if f"_km_gor_ai_{aday.id}" in st.session_state:
                    with st.expander("📋 AI Görüşme Planı", expanded=True):
                        st.markdown(st.session_state[f"_km_gor_ai_{aday.id}"])
                with st.form(f"km_gorusme_{aday.id}"):
                    sonuc = st.selectbox("Gorusme Sonucu *", GORUSME_SONUCLARI, key=f"km_gr_s_{aday.id}")
                    not_text = st.text_area("Not", key=f"km_gr_n_{aday.id}", height=68)
                    try:
                        from utils.shared_data import get_ik_employee_names
                        _personel_list2 = [""] + get_ik_employee_names()
                    except Exception:
                        _personel_list2 = [""]
                    gorusmeci = st.selectbox("Görüşmeyi Yapan", _personel_list2, key=f"km_gr_yapan_{aday.id}")
                    if st.form_submit_button("Gorusmeyi Kaydet", type="primary", use_container_width=True):
                        gor_no = aday.gorusme_sayisi + 1
                        mesaj = gorusme_kaydet(store, aday.id, sonuc, not_text, yapan_kisi=gorusmeci)
                        _sonuc = {
                            "tip": "gorusme", "no": gor_no, "sonuc": sonuc,
                            "not": not_text, "mesaj": mesaj or "",
                            "aday_label": aday.label, "tarih": date.today().isoformat(),
                            "takip": "",
                        }
                        _guncellenmis = store.get_by_id(aday.id)
                        if _guncellenmis and _guncellenmis.sonraki_takip:
                            _sonuc["takip"] = _guncellenmis.sonraki_takip
                        _analiz_text2 = not_text.strip() if not_text.strip() else f"Gorusme sonucu: {sonuc}"
                        try:
                            from models.kayit_sifir_kayip import ai_not_analiz
                            from models.kayit_ai_engine import _aday_ozet
                            na = ai_not_analiz(_aday_ozet(aday), _analiz_text2)
                            if na:
                                _sonuc["ai_analiz"] = na
                        except Exception:
                            pass
                        # ZIRVE: Otomasyon trigger — gorusme tamamlandi
                        try:
                            from models.kayit_otomasyon import trigger_gorusme_tamamlandi
                            n_otom = trigger_gorusme_tamamlandi(aday)
                            if n_otom > 0:
                                _sonuc["otomasyon"] = f"⚡ {n_otom} otomasyon kuyruğa eklendi"
                        except Exception:
                            pass
                        # MEGA: XP — gorusme
                        try:
                            from models.kayit_skorboard import xp_kazandir
                            user = st.session_state.get("auth_user", {})
                            ad = gorusmeci or user.get("name", "Koordinator")
                            eylem = "gorusme_olumlu" if "olumlu" in sonuc.lower() else "gorusme"
                            res = xp_kazandir(ad, eylem)
                            if res["kazanilan_xp"] > 0:
                                _sonuc["xp"] = f"🎮 +{res['kazanilan_xp']} XP kazandi"
                            if res["yeni_seviye"]:
                                _sonuc["level_up"] = f"🏆 Seviye atladi: Lvl {res['current_level']}"
                        except Exception:
                            pass
                        st.session_state[f"_km_sonuc_{aday.id}"] = _sonuc
                        st.rerun()

        # ── FIYAT ──
        with at3:
            if aday.asama in ("gorusme", "fiyat_verildi", "randevu"):
                st.markdown(
                    '<div style="color:#c4b5fd;font-weight:700;margin-bottom:8px">💰 Fiyat Teklifi</div>',
                    unsafe_allow_html=True)

                # ZIRVE: AI Muzakere Botu acici
                _muz_key = f"_muz_open_{aday.id}"
                if st.button("🤖 AI Muzakere Botu (Veli ile Pazarlik)",
                             key=f"km_muz_btn_{aday.id}",
                             use_container_width=True, type="primary"):
                    st.session_state[_muz_key] = True

                if st.session_state.get(_muz_key):
                    try:
                        from utils.kayit_muzakere_ui import render_muzakere_panel
                        render_muzakere_panel(aday)
                    except Exception as e:
                        st.error(f"Muzakere paneli hatasi: {e}")
                    if st.button("✕ Muzakere Panelini Kapat",
                                 key=f"km_muz_close_{aday.id}",
                                 use_container_width=True):
                        st.session_state[_muz_key] = False
                        st.rerun()
                    st.markdown("---")

                # AI Fiyat Optimizer
                if st.button("🤖 AI Fiyat Stratejisi", key=f"km_ai_fiyat_{aday.id}", use_container_width=True):
                    with st.spinner("AI fiyat stratejisi hazırlıyor..."):
                        from models.kayit_ai_engine import ai_fiyat_optimizer
                        result = ai_fiyat_optimizer(aday)
                        if result:
                            st.session_state[f"_km_fiyat_ai_{aday.id}"] = result
                if f"_km_fiyat_ai_{aday.id}" in st.session_state:
                    with st.expander("💡 AI Fiyat Önerisi", expanded=True):
                        st.markdown(st.session_state[f"_km_fiyat_ai_{aday.id}"])
                with st.form(f"km_fiyat_{aday.id}"):
                    # Liste fiyati
                    liste = st.number_input("Liste Fiyati (TL)", min_value=0.0, step=1000.0, key=f"km_f_l_{aday.id}")

                    # Indirimler
                    st.markdown(
                        '<div style="background:#a78bfa10;border-left:3px solid #a78bfa;border-radius:0 6px 6px 0;'
                        'padding:6px 10px;margin:8px 0"><strong style="color:#c4b5fd;font-size:0.9rem">Indirimler (%)</strong></div>',
                        unsafe_allow_html=True)
                    ic1, ic2 = st.columns(2)
                    with ic1:
                        ind_kampanya = st.number_input("Kampanya Indirimi (%)", min_value=0.0, max_value=50.0, step=5.0, key=f"km_f_ik_{aday.id}")
                        ind_bursluluk = st.number_input("Bursluluk Sinavi Indirimi (%)", min_value=0.0, max_value=100.0, step=5.0, key=f"km_f_ib_{aday.id}")
                        ind_kardes = st.number_input("Kardes Indirimi (%)", min_value=0.0, max_value=25.0, step=5.0, key=f"km_f_ikr_{aday.id}")
                    with ic2:
                        ind_kurucu = st.number_input("Kurucu/Mudur Indirimi (%)", min_value=0.0, max_value=50.0, step=5.0, key=f"km_f_ikm_{aday.id}")
                        ind_yetenek = st.number_input("Bireysel Yetenek Indirimi (%)", min_value=0.0, max_value=50.0, step=5.0, key=f"km_f_iy_{aday.id}")
                        ind_diger = st.number_input("Diger Indirim (%)", min_value=0.0, max_value=50.0, step=5.0, key=f"km_f_id_{aday.id}")

                    toplam_indirim = ind_kampanya + ind_bursluluk + ind_kardes + ind_kurucu + ind_yetenek + ind_diger
                    if toplam_indirim > 100:
                        st.error(f"Toplam indirim %100'u gecemez! Mevcut: %{toplam_indirim:.0f}")
                        toplam_indirim = 100.0

                    # KDV
                    st.markdown("---")
                    kdv_orani = st.number_input("KDV Orani (%)", min_value=0.0, max_value=25.0, value=10.0, step=1.0, key=f"km_f_kdv_{aday.id}")

                    # Hesaplama — temel
                    indirimli = liste * (1 - toplam_indirim / 100)
                    kdv_dahil = indirimli * (1 + kdv_orani / 100)

                    # Indirim detay
                    ind_detay = []
                    if ind_kampanya > 0: ind_detay.append(f"Kampanya %{ind_kampanya:.0f}")
                    if ind_bursluluk > 0: ind_detay.append(f"Bursluluk %{ind_bursluluk:.0f}")
                    if ind_kardes > 0: ind_detay.append(f"Kardes %{ind_kardes:.0f}")
                    if ind_kurucu > 0: ind_detay.append(f"Kurucu/Mudur %{ind_kurucu:.0f}")
                    if ind_yetenek > 0: ind_detay.append(f"Yetenek %{ind_yetenek:.0f}")
                    if ind_diger > 0: ind_detay.append(f"Diger %{ind_diger:.0f}")
                    ind_text = " + ".join(ind_detay) if ind_detay else "Indirim yok"

                    st.markdown(
                        f'<div style="background:#172554;border:1px solid #60a5fa30;border-radius:8px;'
                        f'padding:10px;margin:8px 0;color:#93c5fd;font-size:0.85rem">'
                        f'Liste: {liste:,.0f} | Indirim: %{toplam_indirim:.0f} ({ind_text}) | '
                        f'KDV %{kdv_orani:.0f} Dahil: <strong>{kdv_dahil:,.0f} TL</strong></div>',
                        unsafe_allow_html=True)

                    # Pesinat (1. taksit) + Taksit + Odeme gunu
                    st.markdown(
                        '<div style="background:#10b98110;border-left:3px solid #10b981;border-radius:0 6px 6px 0;'
                        'padding:6px 10px;margin:12px 0 6px"><strong style="color:#6ee7b7;font-size:0.9rem">'
                        'Odeme Plani (Pesinat = 1. Taksit)</strong></div>',
                        unsafe_allow_html=True)

                    tp1, tp2, tp3 = st.columns(3)
                    with tp1:
                        pesinat = st.number_input("Pesinat / 1. Taksit (TL)", min_value=0.0, step=500.0, key=f"km_f_p_{aday.id}")
                    with tp2:
                        taksit = st.number_input("Kalan Taksit Sayisi", min_value=1, max_value=12, value=8, key=f"km_f_t_{aday.id}",
                                                  help="Pesinat haric kalan taksit sayisi")
                    with tp3:
                        odeme_gunu = st.number_input("Odeme Gunu (ayin kaci)", min_value=1, max_value=31, value=min(date.today().day, 28), key=f"km_f_gun_{aday.id}",
                                                      help="Varsayilan: kayit tarihi gunu. Degistirirseniz tum taksitler bu gune sabitlenir.")

                    # Vade farki
                    aylik_vade = st.number_input("Aylik Vade Farki (%)", min_value=0.0, max_value=10.0, value=0.0, step=0.5, key=f"km_f_vade_{aday.id}",
                                                  help="0 = vade farksiz. Oran girilirse taksitlere vade farki eklenir.")

                    kalan = kdv_dahil - pesinat
                    toplam_vade_orani = aylik_vade * taksit
                    vade_farki_tutari = kalan * (toplam_vade_orani / 100)
                    vadeli_kalan = kalan + vade_farki_tutari
                    taksit_tutar = vadeli_kalan / taksit if taksit > 0 else 0
                    genel_toplam = pesinat + vadeli_kalan
                    toplam_taksit_adedi = 1 + taksit  # pesinat + kalan taksitler

                    # Taksit takvimi
                    from datetime import date as _date
                    bugun = _date.today()
                    taksit_plani = []
                    # 1. taksit = pesinat (bugun)
                    taksit_plani.append({"no": 1, "tarih": bugun.strftime("%d.%m.%Y"), "tutar": pesinat, "tip": "Pesinat"})
                    # Kalan taksitler
                    for ti in range(1, taksit + 1):
                        ay_offset = ti
                        yil = bugun.year + (bugun.month + ay_offset - 1) // 12
                        ay = (bugun.month + ay_offset - 1) % 12 + 1
                        gun = min(odeme_gunu, 28)  # subat guvenligi
                        taksit_tarih = _date(yil, ay, gun)
                        taksit_plani.append({"no": ti + 1, "tarih": taksit_tarih.strftime("%d.%m.%Y"), "tutar": taksit_tutar, "tip": f"{ti}. Taksit"})

                    # Ozet
                    st.markdown(
                        f'<div style="background:#052e16;border:1px solid #4ade8040;border-radius:8px;'
                        f'padding:10px;margin:8px 0;color:#6ee7b7;font-size:0.85rem">'
                        f'<strong>Odeme Plani:</strong> 1 Pesinat + {taksit} Taksit = <strong>{toplam_taksit_adedi} odeme</strong><br>'
                        f'Pesinat: {pesinat:,.0f} TL ({bugun.strftime("%d.%m.%Y")})<br>'
                        f'{taksit}x {taksit_tutar:,.0f} TL/ay (her ayin {odeme_gunu}. gunu)'
                        f'{f" | Vade farki: %{toplam_vade_orani:.1f} (+{vade_farki_tutari:,.0f} TL)" if aylik_vade > 0 else ""}<br>'
                        f'<strong style="font-size:1rem">TOPLAM: {genel_toplam:,.0f} TL</strong></div>',
                        unsafe_allow_html=True)

                    # Taksit tablosu
                    with st.expander(f"📅 Taksit Takvimi ({toplam_taksit_adedi} odeme)", expanded=False):
                        tablo_html = '<table style="width:100%;border-collapse:collapse;font-size:0.85rem">'
                        tablo_html += '<tr style="background:#1e40af;color:#fff"><th style="padding:6px 10px;text-align:left">#</th><th style="padding:6px 10px">Tarih</th><th style="padding:6px 10px">Tip</th><th style="padding:6px 10px;text-align:right">Tutar</th></tr>'
                        for tp in taksit_plani:
                            bg = "#052e16" if tp["tip"] == "Pesinat" else ("#111827" if tp["no"] % 2 == 0 else "#1e293b")
                            clr = "#4ade80" if tp["tip"] == "Pesinat" else "#e2e8f0"
                            tablo_html += (
                                f'<tr style="background:{bg}"><td style="padding:6px 10px;color:{clr};font-weight:600">{tp["no"]}</td>'
                                f'<td style="padding:6px 10px;color:#94a3b8;text-align:center">{tp["tarih"]}</td>'
                                f'<td style="padding:6px 10px;color:{clr}">{tp["tip"]}</td>'
                                f'<td style="padding:6px 10px;color:{clr};text-align:right;font-weight:600">{tp["tutar"]:,.0f} TL</td></tr>'
                            )
                        tablo_html += f'<tr style="background:#059669"><td colspan="3" style="padding:8px 10px;color:#fff;font-weight:700">TOPLAM</td><td style="padding:8px 10px;color:#fff;font-weight:800;text-align:right">{genel_toplam:,.0f} TL</td></tr>'
                        tablo_html += '</table>'
                        st.markdown(tablo_html, unsafe_allow_html=True)

                    # ── EK HIZMETLER ──
                    st.markdown("---")
                    st.markdown(
                        '<div style="background:#f59e0b10;border-left:3px solid #f59e0b;border-radius:0 6px 6px 0;'
                        'padding:6px 10px;margin:8px 0"><strong style="color:#fde68a;font-size:0.9rem">🎯 Ek Hizmetler (KDV Haric TL)</strong></div>',
                        unsafe_allow_html=True)

                    # Yemek
                    ek1, ek2, ek3 = st.columns(3)
                    with ek1:
                        ek_kahvalti = st.number_input("Kahvalti", min_value=0.0, step=100.0, key=f"km_ek_kah_{aday.id}")
                    with ek2:
                        ek_ogle = st.number_input("Ogle Yemegi", min_value=0.0, step=100.0, key=f"km_ek_ogle_{aday.id}")
                    with ek3:
                        ek_ara = st.number_input("Ara Ogun", min_value=0.0, step=100.0, key=f"km_ek_ara_{aday.id}")

                    # Diger hizmetler
                    ek4, ek5, ek6 = st.columns(3)
                    with ek4:
                        ek_servis = st.number_input("Servis", min_value=0.0, step=100.0, key=f"km_ek_servis_{aday.id}")
                    with ek5:
                        ek_kiyafet = st.number_input("Kiyafet", min_value=0.0, step=100.0, key=f"km_ek_kiyafet_{aday.id}")
                    with ek6:
                        ek_kitap = st.number_input("Kitap-Kirtasiye", min_value=0.0, step=100.0, key=f"km_ek_kitap_{aday.id}")

                    ek7, ek8, ek9 = st.columns(3)
                    with ek7:
                        ek_dijital = st.number_input("Dijital Kaynaklar", min_value=0.0, step=100.0, key=f"km_ek_dijital_{aday.id}")
                    with ek8:
                        ek_pansiyon = st.number_input("Pansiyon/Yatili", min_value=0.0, step=100.0, key=f"km_ek_pansiyon_{aday.id}")
                    with ek9:
                        ek_etut = st.number_input("Etut/Kurs", min_value=0.0, step=100.0, key=f"km_ek_etut_{aday.id}")

                    ek10, ek11 = st.columns(2)
                    with ek10:
                        ek_spor = st.number_input("Spor/Sanat/Bilisim", min_value=0.0, step=100.0, key=f"km_ek_spor_{aday.id}")
                    with ek11:
                        ek_diger = st.number_input("Diger Ek Hizmet", min_value=0.0, step=100.0, key=f"km_ek_diger_{aday.id}")

                    ek_toplam = ek_kahvalti + ek_ogle + ek_ara + ek_servis + ek_kiyafet + ek_kitap + ek_dijital + ek_pansiyon + ek_etut + ek_spor + ek_diger
                    ek_kdv = ek_toplam * (kdv_orani / 100)
                    ek_kdv_dahil = ek_toplam + ek_kdv

                    ek_pesinat = st.number_input("Ek Hizmetler Pesinat (TL)", min_value=0.0, max_value=ek_kdv_dahil if ek_kdv_dahil > 0 else 999999.0, step=500.0, key=f"km_ek_pesinat_{aday.id}")
                    ek_kalan = ek_kdv_dahil - ek_pesinat

                    if ek_toplam > 0:
                        # Ek hizmet detay
                        _ek_items = []
                        if ek_kahvalti > 0: _ek_items.append(f"Kahvalti: {ek_kahvalti:,.0f}")
                        if ek_ogle > 0: _ek_items.append(f"Ogle: {ek_ogle:,.0f}")
                        if ek_ara > 0: _ek_items.append(f"Ara Ogun: {ek_ara:,.0f}")
                        if ek_servis > 0: _ek_items.append(f"Servis: {ek_servis:,.0f}")
                        if ek_kiyafet > 0: _ek_items.append(f"Kiyafet: {ek_kiyafet:,.0f}")
                        if ek_kitap > 0: _ek_items.append(f"Kitap: {ek_kitap:,.0f}")
                        if ek_dijital > 0: _ek_items.append(f"Dijital: {ek_dijital:,.0f}")
                        if ek_pansiyon > 0: _ek_items.append(f"Pansiyon: {ek_pansiyon:,.0f}")
                        if ek_etut > 0: _ek_items.append(f"Etut: {ek_etut:,.0f}")
                        if ek_spor > 0: _ek_items.append(f"Spor/Sanat: {ek_spor:,.0f}")
                        if ek_diger > 0: _ek_items.append(f"Diger: {ek_diger:,.0f}")

                        _ek_pesinat_text = f' | Pesinat: {ek_pesinat:,.0f} | Kalan: {ek_kalan:,.0f}' if ek_pesinat > 0 else ""
                        st.markdown(
                            f'<div style="background:#422006;border:1px solid #f59e0b40;border-radius:8px;'
                            f'padding:10px;margin:8px 0;color:#fde68a;font-size:0.85rem">'
                            f'<strong>Ek Hizmetler:</strong> {" | ".join(_ek_items)}<br>'
                            f'Toplam: {ek_toplam:,.0f} + KDV %{kdv_orani:.0f}: {ek_kdv:,.0f} = '
                            f'<strong>{ek_kdv_dahil:,.0f} TL</strong>{_ek_pesinat_text}</div>',
                            unsafe_allow_html=True)

                    # ── GENEL TOPLAM (Egitim + Ek Hizmetler) ──
                    st.markdown("---")
                    _brut_toplam = kdv_dahil + ek_kdv_dahil
                    _toplam_pesinat = pesinat + ek_pesinat
                    _ek_kalan_val = ek_kdv_dahil - ek_pesinat
                    _taksitlendirilecek = (kdv_dahil - pesinat) + _ek_kalan_val
                    if aylik_vade > 0:
                        _taksitlendirilecek += vade_farki_tutari
                    _taksit_final = _taksitlendirilecek / taksit if taksit > 0 else 0
                    _genel_toplam_final = _toplam_pesinat + _taksitlendirilecek

                    st.markdown(
                        f'<div style="background:#059669;border-radius:10px;padding:14px 18px;margin:8px 0;color:#fff">'
                        f'<div style="font-size:0.85rem;margin-bottom:6px">'
                        f'Egitim (KDV Dahil): <strong>{kdv_dahil:,.0f}</strong> | '
                        f'Ek Hizmetler (KDV Dahil): <strong>{ek_kdv_dahil:,.0f}</strong> | '
                        f'Brut Toplam: <strong>{_brut_toplam:,.0f}</strong></div>'
                        f'<div style="font-size:1.3rem;font-weight:800">GENEL TOPLAM: {_genel_toplam_final:,.0f} TL</div>'
                        f'<div style="font-size:0.8rem;margin-top:4px">'
                        f'Pesinat (1. Taksit): {pesinat:,.0f} (egitim) + {ek_pesinat:,.0f} (ek) = <strong>{_toplam_pesinat:,.0f}</strong><br>'
                        f'{taksit} Taksit x <strong>{_taksit_final:,.0f} TL/ay</strong> (her ayin {odeme_gunu}. gunu)'
                        f'{f" | Vade farki: +{vade_farki_tutari:,.0f}" if aylik_vade > 0 else ""}</div></div>',
                        unsafe_allow_html=True)

                    if st.form_submit_button("Fiyat Kaydet", type="primary", use_container_width=True):
                        _ek_data = {
                            "kahvalti": ek_kahvalti, "ogle_yemegi": ek_ogle, "ara_ogun": ek_ara,
                            "servis": ek_servis, "kiyafet": ek_kiyafet, "kitap_kirtasiye": ek_kitap,
                            "dijital": ek_dijital, "pansiyon": ek_pansiyon, "etut_kurs": ek_etut,
                            "spor_sanat": ek_spor, "diger": ek_diger,
                            "toplam": ek_toplam, "kdv": ek_kdv, "kdv_dahil": ek_kdv_dahil,
                            "pesinat": ek_pesinat, "kalan": ek_kalan,
                            "tarih": datetime.now().isoformat(),
                        }
                        fiyat_kaydet(store, aday.id, {
                            "liste_fiyati": liste,
                            "kdv_orani": kdv_orani,
                            "toplam_indirim": toplam_indirim,
                            "ind_kampanya": ind_kampanya,
                            "ind_bursluluk": ind_bursluluk,
                            "ind_kardes": ind_kardes,
                            "ind_kurucu": ind_kurucu,
                            "ind_yetenek": ind_yetenek,
                            "ind_diger": ind_diger,
                            "indirim_detay": ind_text,
                            "kdv_dahil": kdv_dahil, "pesinat": pesinat,
                            "taksit_sayisi": taksit, "taksit_tutari": taksit_tutar,
                            "toplam_taksit_adedi": toplam_taksit_adedi,
                            "odeme_gunu": odeme_gunu,
                            "aylik_vade_farki": aylik_vade,
                            "vade_farki_tutari": vade_farki_tutari,
                            "genel_toplam": genel_toplam,
                            "ek_hizmetler_toplam": ek_kdv_dahil,
                            "ek_pesinat": ek_pesinat,
                            "toplam_pesinat": _toplam_pesinat,
                            "brut_toplam": _brut_toplam,
                            "genel_toplam_final": _genel_toplam_final,
                            "taksit_plani": taksit_plani,
                            "tarih": datetime.now().isoformat(),
                        }, ek_hizmetler=_ek_data)
                        st.session_state[f"_km_sonuc_{aday.id}"] = {
                            "tip": "fiyat", "no": 0, "sonuc": "Fiyat Teklifi Kaydedildi",
                            "not": f"Toplam: {_genel_toplam_final:,.0f} TL | İndirim: %{_toplam_ind:.0f} | Taksit: {_taksit_sayisi}x",
                            "mesaj": "Veliye fiyat teklifi sunuldu. Takip araması yapılmalı.",
                            "aday_label": aday.label, "tarih": date.today().isoformat(), "takip": "",
                        }
                        st.rerun()
            else:
                styled_info_banner("Oncelikle gorusme asamasini tamamlayin.", "info")

            # Mevcut fiyat + PDF butonlari
            if aday.fiyat_bilgi:
                fb = aday.fiyat_bilgi
                eb = aday.ek_hizmetler
                st.markdown("---")
                st.markdown(
                    f'<div style="background:#172554;border:1px solid #60a5fa30;border-radius:8px;'
                    f'padding:10px;margin-top:8px;color:#93c5fd;font-size:0.85rem">'
                    f'<strong>Kayitli Fiyat:</strong> Egitim KDV Dahil: {fb.get("kdv_dahil", 0):,.0f} TL | '
                    f'Ek Hizmetler: {fb.get("ek_hizmetler_toplam", 0):,.0f} TL | '
                    f'Pesinat: {fb.get("toplam_pesinat", fb.get("pesinat", 0)):,.0f} | '
                    f'Taksit: {fb.get("taksit_sayisi", 0)}x {fb.get("taksit_tutari", 0):,.0f} | '
                    f'<strong>Genel Toplam: {fb.get("genel_toplam_final", fb.get("brut_toplam", 0)):,.0f} TL</strong></div>',
                    unsafe_allow_html=True)

                # PDF cikti secenekleri
                st.markdown(
                    '<div style="color:#94a3b8;font-weight:600;margin:10px 0 6px">📄 PDF Cikti</div>',
                    unsafe_allow_html=True)
                pdf_c1, pdf_c2, pdf_c3 = st.columns(3)
                with pdf_c1:
                    _pdf_egitim = _generate_fiyat_pdf(aday, "egitim")
                    if _pdf_egitim:
                        st.download_button("📄 Egitim Hizmetleri PDF", data=_pdf_egitim,
                                           file_name=f"Fiyat_Egitim_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                                           mime="application/pdf", key=f"km_pdf_eg_{aday.id}", use_container_width=True)
                with pdf_c2:
                    if eb and eb.get("toplam", 0) > 0:
                        _pdf_ek = _generate_fiyat_pdf(aday, "ek_hizmet")
                        if _pdf_ek:
                            st.download_button("📄 Ek Hizmetler PDF", data=_pdf_ek,
                                               file_name=f"Fiyat_EkHizmet_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                                               mime="application/pdf", key=f"km_pdf_ek_{aday.id}", use_container_width=True)
                    else:
                        st.button("📄 Ek Hizmet Yok", disabled=True, key=f"km_pdf_ek_d_{aday.id}", use_container_width=True)
                with pdf_c3:
                    _pdf_tam = _generate_fiyat_pdf(aday, "tam")
                    if _pdf_tam:
                        st.download_button("📄 Tam Fiyat Teklifi PDF", data=_pdf_tam,
                                           file_name=f"Fiyat_Tam_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                                           mime="application/pdf", key=f"km_pdf_tam_{aday.id}", use_container_width=True)

        # ── SOZLESME (MEB Formati) ──
        with at4:
            if aday.asama in ("fiyat_verildi", "sozlesme"):
                st.markdown(
                    '<div style="background:#38bdf810;border-left:3px solid #38bdf8;border-radius:0 8px 8px 0;'
                    'padding:10px 14px;margin-bottom:10px">'
                    '<strong style="color:#7dd3fc;font-size:1rem">📄 MEB Ogrenci Kayit Sozlesmesi</strong></div>',
                    unsafe_allow_html=True)
                # AI Sözleşme Danışmanı
                if st.button("🤖 AI Sözleşme Danışmanı (Kontrol Listesi + İmza Stratejisi)",
                             key=f"km_ai_sozl_{aday.id}", use_container_width=True):
                    with st.spinner("AI sözleşme stratejisi hazırlıyor..."):
                        from models.kayit_ai_engine import ai_sozlesme_danismani
                        result = ai_sozlesme_danismani(aday)
                        if result:
                            st.session_state[f"_km_sozl_ai_{aday.id}"] = result
                if f"_km_sozl_ai_{aday.id}" in st.session_state:
                    with st.expander("📋 AI Sözleşme Planı", expanded=True):
                        st.markdown(st.session_state[f"_km_sozl_ai_{aday.id}"])

                fb = aday.fiyat_bilgi or {}
                eb = aday.ek_hizmetler or {}

                with st.form(f"km_sozlesme_{aday.id}"):
                    # Kurum bilgileri
                    try:
                        from utils.shared_data import load_kurum_profili
                        kp = load_kurum_profili()
                    except Exception:
                        kp = {}
                    kurum_adi = kp.get("kurum_adi", kp.get("name", ""))

                    st.markdown(
                        f'<div style="background:#0c4a6e;border:1px solid #38bdf840;border-radius:8px;'
                        f'padding:10px;margin-bottom:10px;text-align:center;color:#7dd3fc;font-size:0.85rem">'
                        f'T.C. MILLI EGITIM BAKANLIGI<br>OZEL OGRETIM KURUMLARI GENEL MUDURLUGU<br>'
                        f'<strong style="font-size:1rem">OGRENCI KAYIT SOZLESMESI</strong><br>'
                        f'<span style="color:#94a3b8">Ozel Okul Adi: {kurum_adi}</span></div>',
                        unsafe_allow_html=True)

                    # 1. Ogrenci bilgileri
                    st.markdown(
                        '<div style="background:#172554;border-left:3px solid #60a5fa;border-radius:0 6px 6px 0;'
                        'padding:6px 10px;margin:10px 0 6px"><strong style="color:#93c5fd">OGRENCININ BILGILERI</strong></div>',
                        unsafe_allow_html=True)
                    oc1, oc2 = st.columns(2)
                    with oc1:
                        s_ogr_tc = st.text_input("T.C. Kimlik No", key=f"km_s_otc_{aday.id}", max_chars=11)
                        s_ogr_adi = st.text_input("Adi ve Soyadi", value=aday.ogrenci_adi, key=f"km_s_oad_{aday.id}")
                        s_ogr_sinif = st.text_input("Sinifi", value=aday.hedef_sinif or aday.mevcut_sinif or "", key=f"km_s_osn_{aday.id}")
                    with oc2:
                        s_ogr_kayit = st.date_input("Okula Kayit Tarihi", key=f"km_s_okt_{aday.id}")
                        s_ogr_adres = st.text_area("Ev Adresi", key=f"km_s_oadr_{aday.id}", height=68)
                        s_egitim_yili = st.text_input("Egitim Yili", value="2025-2026", key=f"km_s_ey_{aday.id}")

                    # 2. Veli bilgileri
                    st.markdown(
                        '<div style="background:#172554;border-left:3px solid #60a5fa;border-radius:0 6px 6px 0;'
                        'padding:6px 10px;margin:10px 0 6px"><strong style="color:#93c5fd">OGRENCININ VELI/VASI BILGILERI</strong></div>',
                        unsafe_allow_html=True)
                    vc1, vc2 = st.columns(2)
                    with vc1:
                        s_veli_tc = st.text_input("T.C. Kimlik No", key=f"km_s_vtc_{aday.id}", max_chars=11)
                        s_veli_adi = st.text_input("Adi ve Soyadi", value=aday.veli_adi, key=f"km_s_vad_{aday.id}")
                        s_veli_meslek = st.text_input("Meslegi", key=f"km_s_vms_{aday.id}")
                        s_veli_cep = st.text_input("Cep Telefonu", value=aday.veli_telefon, key=f"km_s_vcp_{aday.id}")
                    with vc2:
                        s_veli_is_tel = st.text_input("Is Telefonu", key=f"km_s_vit_{aday.id}")
                        s_veli_email = st.text_input("e-Posta", value=aday.veli_email, key=f"km_s_vem_{aday.id}")
                        s_veli_ev = st.text_area("Ev Adresi", key=f"km_s_vea_{aday.id}", height=50)
                        s_veli_is = st.text_area("Is Adresi", key=f"km_s_via_{aday.id}", height=50)

                    # 3. Odeme bilgileri (fiyattan otomatik)
                    st.markdown(
                        '<div style="background:#172554;border-left:3px solid #60a5fa;border-radius:0 6px 6px 0;'
                        'padding:6px 10px;margin:10px 0 6px"><strong style="color:#93c5fd">ODEME BILGILERI</strong></div>',
                        unsafe_allow_html=True)

                    if fb:
                        st.markdown(
                            f'<div style="background:#1e293b;border:1px solid #334155;border-radius:8px;'
                            f'padding:10px;margin:6px 0;color:#e2e8f0;font-size:0.85rem">'
                            f'Egitim KDV Dahil: <strong>{fb.get("kdv_dahil", 0):,.0f} TL</strong> | '
                            f'Ek Hizmetler: <strong>{fb.get("ek_hizmetler_toplam", 0):,.0f} TL</strong> | '
                            f'Brut Toplam: <strong>{fb.get("brut_toplam", 0):,.0f} TL</strong><br>'
                            f'Pesinat: {fb.get("toplam_pesinat", fb.get("pesinat", 0)):,.0f} TL | '
                            f'Taksit: {fb.get("taksit_sayisi", 0)}x {fb.get("taksit_tutari", 0):,.0f} TL | '
                            f'Indirim: %{fb.get("toplam_indirim", 0):.0f} ({fb.get("indirim_detay", "")})<br>'
                            f'<strong style="color:#4ade80">Genel Toplam: {fb.get("genel_toplam_final", fb.get("brut_toplam", 0)):,.0f} TL</strong></div>',
                            unsafe_allow_html=True)
                    else:
                        styled_info_banner("Fiyat bilgisi bulunamadi — once Fiyat sekmesinden kaydedin.", "warning")

                    # 4. Odeme sekli
                    s_odeme_sekli = st.selectbox("Odeme Sekli", ["Taksit", "Pesin"], key=f"km_s_os_{aday.id}")

                    # 5. Burs / indirim
                    st.markdown(
                        '<div style="background:#172554;border-left:3px solid #60a5fa;border-radius:0 6px 6px 0;'
                        'padding:6px 10px;margin:10px 0 6px"><strong style="color:#93c5fd">BURS VE INDIRIM</strong></div>',
                        unsafe_allow_html=True)
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        s_burs_var = st.checkbox("Burs aliyor mu?", key=f"km_s_bv_{aday.id}")
                        if s_burs_var:
                            s_burs_oran = st.number_input("Burs Orani (%)", min_value=0.0, max_value=100.0, key=f"km_s_bo_{aday.id}")
                        else:
                            s_burs_oran = 0.0
                    with bc2:
                        s_ucretsiz_neden = st.selectbox("Ucretsiz Okuma Nedeni",
                                                         ["Yok", "Sehit/Gazi Cocugu", "2828/5395 Sayili Kanun", "Diger"],
                                                         key=f"km_s_un_{aday.id}")

                    # 6. Ozel hususlar
                    st.markdown(
                        '<div style="background:#172554;border-left:3px solid #60a5fa;border-radius:0 6px 6px 0;'
                        'padding:6px 10px;margin:10px 0 6px"><strong style="color:#93c5fd">OZEL HUSUSLAR</strong></div>',
                        unsafe_allow_html=True)
                    s_ozel1 = st.text_input("Ozel Husus 1", key=f"km_s_oh1_{aday.id}")
                    s_ozel2 = st.text_input("Ozel Husus 2", key=f"km_s_oh2_{aday.id}")

                    # 7. Sozlesme tarihi
                    st.markdown("---")
                    st1, st2 = st.columns(2)
                    with st1:
                        s_sozlesme_tarihi = st.date_input("Sozlesme Tarihi", key=f"km_s_st_{aday.id}")
                    with st2:
                        s_sozlesme_yeri = st.text_input("Sozlesme Yeri", value=kurum_adi, key=f"km_s_sy_{aday.id}")

                    # Sözleşmeyi yapan kişi
                    try:
                        from utils.shared_data import get_ik_employee_names
                        _personel_list3 = [""] + get_ik_employee_names()
                    except Exception:
                        _personel_list3 = [""]
                    sozlesmeci = st.selectbox("Sözleşmeyi Yapan", _personel_list3, key=f"km_sz_yapan_{aday.id}")

                    # Butonlar
                    st.markdown("---")
                    sb1, sb2, sb3 = st.columns(3)
                    with sb1:
                        sozlesme_btn = st.form_submit_button("📄 Sozlesme Kaydet", use_container_width=True)
                    with sb2:
                        kayit_btn = st.form_submit_button("✅ Kesin Kayit Yap", type="primary", use_container_width=True)
                    with sb3:
                        taslak_btn = st.form_submit_button("💾 Taslak Kaydet", use_container_width=True)

                    _sozlesme_data = {
                        "sozlesme_tarihi": str(s_sozlesme_tarihi),
                        "sozlesme_yeri": s_sozlesme_yeri,
                        "egitim_yili": s_egitim_yili,
                        "ogrenci_tc": s_ogr_tc,
                        "ogrenci_adi": s_ogr_adi,
                        "ogrenci_sinif": s_ogr_sinif,
                        "ogrenci_kayit_tarihi": str(s_ogr_kayit),
                        "ogrenci_adres": s_ogr_adres,
                        "veli_tc": s_veli_tc,
                        "veli_adi": s_veli_adi,
                        "veli_meslek": s_veli_meslek,
                        "veli_cep": s_veli_cep,
                        "veli_is_tel": s_veli_is_tel,
                        "veli_email": s_veli_email,
                        "veli_ev_adres": s_veli_ev,
                        "veli_is_adres": s_veli_is,
                        "odeme_sekli": s_odeme_sekli,
                        "burs_orani": s_burs_oran,
                        "ucretsiz_okuma": s_ucretsiz_neden,
                        "ozel_husus_1": s_ozel1,
                        "ozel_husus_2": s_ozel2,
                        "toplam_ucret": fb.get("genel_toplam_final", fb.get("brut_toplam", 0)),
                        "pesinat": fb.get("toplam_pesinat", fb.get("pesinat", 0)),
                        "taksit_sayisi": fb.get("taksit_sayisi", 0),
                        "taksit_tutari": fb.get("taksit_tutari", 0),
                        "tarih": datetime.now().isoformat(),
                    }

                    if sozlesme_btn:
                        sozlesme_kaydet(store, aday.id, _sozlesme_data, yapan_kisi=sozlesmeci)
                        st.success("Sozlesme kaydedildi!")
                        st.rerun()
                    if kayit_btn:
                        _sozlesme_data["kayit_sonucu"] = "Kesin Kayit"
                        sozlesme_kaydet(store, aday.id, _sozlesme_data, yapan_kisi=sozlesmeci)
                        kesin_kayit_yap(store, aday.id)
                        # Sonuç ekranı + otomatik hoş geldin
                        st.session_state[f"_km_sonuc_{aday.id}"] = {
                            "tip": "kesin_kayit", "no": 0, "sonuc": "Kesin Kayıt Tamamlandı!",
                            "not": f"Sözleşme imzalandı. Kayıt sınıf/şube atanacak.",
                            "mesaj": "Hoş geldin süreci otomatik başlatılıyor...",
                            "aday_label": aday.label, "tarih": date.today().isoformat(), "takip": "",
                        }
                        # Otomatik AI hoş geldin süreci
                        try:
                            from models.kayit_ai_engine import ai_hosgeldin_sureci
                            hg = ai_hosgeldin_sureci(aday)
                            if hg:
                                st.session_state[f"_km_hg_{aday.id}"] = hg
                        except Exception:
                            pass
                        st.balloons()
                        st.rerun()
                    if taslak_btn:
                        _sozlesme_data["kayit_sonucu"] = "Taslak"
                        sozlesme_kaydet(store, aday.id, _sozlesme_data, yapan_kisi=sozlesmeci)
                        st.success("Taslak kaydedildi.")
                        st.rerun()

                # Kayitli sozlesme varsa PDF indir
                if aday.sozlesme_bilgi:
                    st.markdown("---")
                    st.markdown('<div style="color:#94a3b8;font-weight:600;margin:6px 0">📄 Sozlesme PDF</div>',
                                unsafe_allow_html=True)
                    _pdf_sozlesme = _generate_sozlesme_pdf(aday)
                    if _pdf_sozlesme:
                        st.download_button("📄 MEB Sozlesme PDF Indir", data=_pdf_sozlesme,
                                           file_name=f"Sozlesme_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                                           mime="application/pdf", key=f"km_spdf_{aday.id}", use_container_width=True)
            else:
                styled_info_banner("Oncelikle fiyat asamasini tamamlayin.", "info")

        # ── MEB SOZLESME (Word birebir) ──
        with at5:
            _render_meb_sozlesme(store, aday)

        # ── PROFİL DÜZENLEME ──
        with at6:
            _render_profil_duzenle(store, aday)

    # ── ADAY RAPOR PDF ──
    st.markdown("---")
    if st.button("📄 Aday Süreç Raporu PDF İndir", key=f"km_pdf_rapor_{aday.id}", use_container_width=True):
        try:
            from models.kayit_ai_engine import generate_aday_rapor_pdf
            _kurum = ""
            try:
                from utils.shared_data import load_kurum_profili
                kp = load_kurum_profili()
                _kurum = kp.get("kurum_adi", kp.get("name", "")) or ""
            except Exception:
                pass
            _rpdf = generate_aday_rapor_pdf(aday, _kurum)
            if _rpdf:
                st.download_button("📥 PDF İndir", data=_rpdf,
                                   file_name=f"Aday_Rapor_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                                   mime="application/pdf", key=f"km_rpdf_dl_{aday.id}", use_container_width=True)
        except Exception as e:
            st.error(f"PDF hatası: {e}")

    # ── TAM KRONOLOJİK TİMELINE ──
    st.markdown(
        '<div style="background:linear-gradient(135deg,#1e293b,#0f172a);border-radius:10px;'
        'padding:12px 16px;margin-bottom:8px;">'
        '<b style="color:#e2e8f0;">📋 Tam Süreç Geçmişi — Kronolojik Timeline</b>'
        '<p style="color:#64748b;font-size:11px;margin:2px 0 0;">Tüm aramalar, görüşmeler, testler, ihtiyaçlar, fiyat, sözleşme — notlarıyla birlikte</p></div>',
        unsafe_allow_html=True)

    tum_olaylar = []
    # Aday kaydı
    tum_olaylar.append({"tarih": aday.olusturma_tarihi, "tip": "kayit", "baslik": "Aday kaydedildi",
                         "detay": f'{aday.kademe} | {aday.mevcut_okul or "-"} | Kanal: {aday.kanal or "-"}',
                         "not": aday.notlar or "", "renk": "#4ade80", "ikon": "➕"})
    # Aramalar (notlarıyla)
    for ar in aday.aramalar:
        not_txt = ar.get("not", ar.get("notlar", ""))
        tum_olaylar.append({"tarih": ar.get("tarih", "")[:16], "tip": "arama",
                             "baslik": f'{ar["arama_no"]}. Arama: {ar["sonuc"]}',
                             "detay": f'📞 {aday.veli_telefon or "-"}',
                             "not": not_txt, "renk": "#0ea5e9", "ikon": "📞"})
    # Görüşmeler (notlarıyla)
    for gr in aday.gorusmeler:
        not_txt = gr.get("not", gr.get("notlar", ""))
        tum_olaylar.append({"tarih": gr.get("tarih", "")[:16], "tip": "gorusme",
                             "baslik": f'{gr["gorusme_no"]}. Görüşme: {gr["sonuc"]}',
                             "detay": "", "not": not_txt, "renk": "#ea580c", "ikon": "🤝"})
    # Testler
    for t in aday.testler:
        skorlar = t.get("skorlar", {})
        skor_txt = ", ".join(f'{k}: {v}' for k, v in list(skorlar.items())[:4]) if skorlar else ""
        top3 = t.get("top3", [])
        top3_txt = " | ".join(f'{x.get("alan","")}: {x.get("skor","")}' for x in top3[:3]) if top3 else ""
        tum_olaylar.append({"tarih": t.get("tarih", "")[:16], "tip": "test",
                             "baslik": f'🧪 Test: {t.get("test_adi", "?")} — {t.get("sonuc", "")}',
                             "detay": top3_txt or skor_txt,
                             "not": t.get("notlar", ""), "renk": "#8b5cf6", "ikon": "🧪"})
    # İhtiyaç analizi
    if aday.ihtiyaclar:
        kategoriler = [f'{ih.get("oncelik", "")}: {ih.get("kategori", "")}' for ih in aday.ihtiyaclar[:5]]
        tum_olaylar.append({"tarih": aday.son_islem_tarihi, "tip": "ihtiyac",
                             "baslik": f'🎯 İhtiyaç Analizi: {len(aday.ihtiyaclar)} kategori',
                             "detay": " | ".join(kategoriler),
                             "not": "", "renk": "#0d9488", "ikon": "🎯"})
    # Profil
    vp = aday.veli_profil or {}
    op = aday.ogrenci_profil or {}
    if vp or op:
        profil_ozet = []
        if vp.get("meslek"):
            profil_ozet.append(f'Meslek: {vp["meslek"]}')
        if vp.get("butce_beklentisi"):
            profil_ozet.append(f'Bütçe: {vp["butce_beklentisi"]}')
        if vp.get("karar_verici"):
            profil_ozet.append(f'Karar: {vp["karar_verici"]}')
        if op.get("akademik_basari"):
            profil_ozet.append(f'Başarı: {op["akademik_basari"]}')
        if profil_ozet:
            tum_olaylar.append({"tarih": aday.son_islem_tarihi, "tip": "profil",
                                 "baslik": "👤 Profil Güncellendi",
                                 "detay": " | ".join(profil_ozet),
                                 "not": "", "renk": "#6366f1", "ikon": "👤"})
    # Fiyat
    if aday.fiyat_bilgi:
        fb = aday.fiyat_bilgi
        toplam = float(fb.get("genel_toplam_final", fb.get("brut_toplam", fb.get("kdv_dahil", 0))) or 0)
        indirim = fb.get("toplam_indirim", 0)
        tum_olaylar.append({"tarih": fb.get("tarih", "")[:16], "tip": "fiyat",
                             "baslik": f'💰 Fiyat Teklifi: {toplam:,.0f} TL',
                             "detay": f'İndirim: %{indirim} | Taksit: {fb.get("taksit_sayisi", "-")}x',
                             "not": "", "renk": "#a78bfa", "ikon": "💰"})
    # Sözleşme
    if aday.sozlesme_bilgi:
        sb = aday.sozlesme_bilgi
        tum_olaylar.append({"tarih": sb.get("tarih", sb.get("sozlesme_tarihi", ""))[:16], "tip": "sozlesme",
                             "baslik": f'📄 Sözleşme: {sb.get("kayit_sonucu", "Kaydedildi")}',
                             "detay": f'Toplam: {sb.get("toplam_ucret", "-")} | Ödeme: {sb.get("odeme_sekli", "-")}',
                             "not": "", "renk": "#38bdf8", "ikon": "📄"})
    # Referans
    if aday.referans_veli:
        tum_olaylar.append({"tarih": aday.olusturma_tarihi, "tip": "referans",
                             "baslik": f'🤝 Referans: {aday.referans_veli}',
                             "detay": f'Tip: {aday.referans_tipi or "-"} | Öğrenci: {aday.referans_ogrenci or "-"}',
                             "not": "", "renk": "#ec4899", "ikon": "🤝"})
    # Kesin kayıt / olumsuz
    if aday.asama == "kesin_kayit":
        tum_olaylar.append({"tarih": aday.kapanma_tarihi, "tip": "kayit_tamam",
                             "baslik": "✅ Kesin Kayıt Tamamlandı!", "detay": f'Sınıf: {aday.kayit_sinif or "-"}',
                             "not": "", "renk": "#10b981", "ikon": "✅"})
    if aday.asama == "olumsuz":
        son_sonuc = ""
        if aday.aramalar:
            son_sonuc = aday.aramalar[-1].get("sonuc", "")
        if aday.gorusmeler:
            son_sonuc = aday.gorusmeler[-1].get("sonuc", "")
        tum_olaylar.append({"tarih": aday.kapanma_tarihi, "tip": "olumsuz",
                             "baslik": f'❌ Olumsuz: {son_sonuc}', "detay": "",
                             "not": "", "renk": "#f87171", "ikon": "❌"})

    # Sırala
    tum_olaylar.sort(key=lambda x: x.get("tarih", ""))

    # Render
    for i, ev in enumerate(tum_olaylar):
        is_last = i == len(tum_olaylar) - 1
        connector = "" if is_last else f'<div style="width:2px;height:12px;background:{ev["renk"]}30;margin-left:11px"></div>'
        not_html = ""
        if ev.get("not"):
            not_html = (f'<div style="background:#1e293b;border-radius:4px;padding:4px 8px;margin-top:3px;'
                        f'font-size:0.75rem;color:#cbd5e1;">📝 {ev["not"][:120]}</div>')
        detay_html = ""
        if ev.get("detay"):
            detay_html = f'<div style="font-size:0.72rem;color:#94a3b8;margin-top:1px;">{ev["detay"][:100]}</div>'

        st.markdown(
            f'<div><div style="display:flex;align-items:flex-start;gap:10px">'
            f'<div style="width:24px;height:24px;border-radius:50%;background:{ev["renk"]};'
            f'display:flex;align-items:center;justify-content:center;font-weight:800;'
            f'font-size:0.65rem;color:#fff;flex-shrink:0;margin-top:2px;">{ev["ikon"]}</div>'
            f'<div style="flex:1;padding:6px 10px;background:{ev["renk"]}08;border:1px solid {ev["renk"]}20;border-radius:8px">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="color:#e2e8f0;font-weight:600;font-size:0.85rem">{ev["baslik"]}</span>'
            f'<span style="font-size:0.7rem;color:#64748b;">{ev["tarih"]}</span></div>'
            f'{detay_html}{not_html}'
            f'</div></div>{connector}</div>',
            unsafe_allow_html=True)


# ============================================================
# ISTATISTIKLER
# ============================================================

def _render_istatistikler(store: KayitDataStore, adaylar: list[KayitAday]):
    stats = store.istatistikler()
    import plotly.graph_objects as go

    # ── ISI HARİTASI ÖZET ──
    from models.kayit_takip_engine import gun_sonu_ozet
    _gso = gun_sonu_ozet(adaylar)
    _isi_cols = st.columns(6)
    _isi_data = [
        ("🔥 Sıcak", str(_gso["sicak"]), "#ef4444"),
        ("🌡️ Ilık", str(_gso["ilik"]), "#f59e0b"),
        ("❄️ Soğuk", str(_gso["soguk"]), "#3b82f6"),
        ("🧊 Buz", str(_gso["buz"]), "#64748b"),
        ("⏰ Geciken", str(_gso["geciken"]), "#f97316"),
        ("🚨 Eskalasyon", str(_gso["eskalasyon_gereken"]), "#ef4444"),
    ]
    for i, (lbl, val, clr) in enumerate(_isi_data):
        with _isi_cols[i]:
            st.markdown(
                f'<div style="background:{clr}15;border:1px solid {clr}40;border-radius:10px;'
                f'padding:10px;text-align:center;">'
                f'<div style="font-size:1.5rem;font-weight:800;color:{clr};">{val}</div>'
                f'<div style="font-size:.7rem;color:{clr};">{lbl}</div></div>',
                unsafe_allow_html=True)

    # Sıfır Kayıp Taraması — gömülü, aç/kapa, grid kart düzeni
    from models.kayit_sifir_kayip import toplu_sifir_kayip_tarama
    _sk_list = toplu_sifir_kayip_tarama(adaylar)
    if _sk_list:
        _kritik_n = sum(1 for x in _sk_list if x.get("aciliyet") == "KRITIK")
        with st.expander(
            f"🚨  SIFIR KAYIP ALARM  •  {len(_sk_list)} aday risk altında  •  {_kritik_n} kritik",
            expanded=False,
        ):
            st.markdown(
                """
                <style>
                .sk-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
                         gap:8px;margin-top:6px;}
                .sk-card{background:linear-gradient(135deg,#1a0606 0%,#0f0303 100%);
                         border:1px solid #f8717130;border-left:3px solid var(--sk-clr,#ef4444);
                         border-radius:8px;padding:9px 11px;transition:all .2s;}
                .sk-card:hover{border-color:var(--sk-clr,#ef4444);transform:translateY(-1px);
                               box-shadow:0 4px 12px var(--sk-glow,#ef444425);}
                .sk-head{display:flex;align-items:center;justify-content:space-between;gap:6px;}
                .sk-name{color:#fecaca;font-size:12px;font-weight:700;
                         white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;}
                .sk-pill{background:var(--sk-clr,#ef4444);color:#fff;padding:1px 7px;
                         border-radius:8px;font-size:9px;font-weight:700;text-transform:uppercase;
                         white-space:nowrap;}
                .sk-risk{color:#fca5a5;font-size:10.5px;margin-top:4px;line-height:1.35;
                         display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
                         overflow:hidden;}
                .sk-save{color:#86efac;font-size:10px;margin-top:4px;line-height:1.3;
                         padding-top:4px;border-top:1px dashed #f8717125;
                         display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
                         overflow:hidden;}
                .sk-save b{color:#bbf7d0;font-weight:700;}
                </style>
                """,
                unsafe_allow_html=True,
            )
            _sk_html = '<div class="sk-grid">'
            for _ski in _sk_list:
                _aciliyet = _ski.get("aciliyet", "ORTA")
                _ski_clr = "#ef4444" if _aciliyet == "KRITIK" else "#f97316"
                _ski_glow = f"{_ski_clr}30"
                _label = str(_ski.get("aday_label", "—"))
                _risk = str(_ski.get("risk_nedeni", ""))
                _kurt = str(_ski.get("kurtarma_plani", ""))
                _sk_html += (
                    f'<div class="sk-card" style="--sk-clr:{_ski_clr};--sk-glow:{_ski_glow};">'
                    f'<div class="sk-head">'
                    f'<div class="sk-name">👤 {_label}</div>'
                    f'<span class="sk-pill">{_aciliyet}</span>'
                    f'</div>'
                    f'<div class="sk-risk">⚠️ {_risk}</div>'
                    f'<div class="sk-save"><b>🛟 Kurtarma:</b> {_kurt}</div>'
                    f'</div>'
                )
            _sk_html += '</div>'
            st.markdown(_sk_html, unsafe_allow_html=True)

    # Kritik eskalasyonlar — gömülü, aç/kapa, grid kart düzeni
    if _gso["kritik_adaylar"]:
        _esk_count = len(_gso["kritik_adaylar"])
        with st.expander(f"🚨  Eskalasyon Gereken Adaylar  •  {_esk_count} kayıt", expanded=False):
            st.markdown(
                """
                <style>
                .esk-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));
                          gap:8px;margin-top:6px;}
                .esk-card{background:linear-gradient(135deg,#450a0a 0%,#1a0606 100%);
                          border:1px solid #f8717140;border-left:3px solid #ef4444;
                          border-radius:8px;padding:8px 10px;transition:all .2s;}
                .esk-card:hover{border-color:#ef4444;transform:translateY(-1px);
                                box-shadow:0 4px 12px #ef444425;}
                .esk-name{color:#fecaca;font-size:12px;font-weight:700;
                          white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
                .esk-meta{color:#fca5a5;font-size:10px;opacity:.85;margin-top:2px;
                          display:flex;align-items:center;gap:4px;}
                .esk-pill{background:#7f1d1d;color:#fecaca;padding:1px 6px;border-radius:8px;
                          font-size:9px;font-weight:600;text-transform:uppercase;}
                .esk-reason{color:#fda4af;font-size:10px;margin-top:3px;line-height:1.3;
                            display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
                            overflow:hidden;}
                </style>
                """,
                unsafe_allow_html=True,
            )
            _cards_html = '<div class="esk-grid">'
            for _ka in _gso["kritik_adaylar"]:
                _aday = str(_ka.get("aday", "—"))
                _kime = str(_ka.get("kime", "—"))
                _neden = str(_ka.get("neden", ""))
                _cards_html += (
                    f'<div class="esk-card">'
                    f'<div class="esk-name">👤 {_aday}</div>'
                    f'<div class="esk-meta"><span class="esk-pill">→ {_kime}</span></div>'
                    f'<div class="esk-reason">{_neden}</div>'
                    f'</div>'
                )
            _cards_html += '</div>'
            st.markdown(_cards_html, unsafe_allow_html=True)

    st.markdown("---")

    # Ultra Premium Stat Kartları
    _BG = "#0B0F19"
    _CARD = "#131825"
    _cards = st.columns(6)
    _stat_data = [
        ("Toplam Aday", str(stats["toplam"]), "#6366f1", "👥"),
        ("Aktif", str(stats["aktif"]), "#f59e0b", "🔄"),
        ("Kesin Kayıt", str(stats["kesin_kayit"]), "#10b981", "✅"),
        ("Dönüşüm", f'%{stats["donusum"]:.1f}', "#3b82f6", "📈"),
        ("Olumsuz", str(stats.get("olumsuz", 0)), "#ef4444", "❌"),
        ("Bekleyen", str(stats["toplam"] - stats["kesin_kayit"] - stats.get("olumsuz", 0)), "#8b5cf6", "⏳"),
    ]
    for i, (lbl, val, clr, ic) in enumerate(_stat_data):
        with _cards[i]:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{_CARD},{_BG});border-radius:14px;'
                f'padding:16px;border:1px solid {clr}25;text-align:center;">'
                f'<div style="font-size:2rem;opacity:.06;color:{clr};position:absolute;top:4px;right:10px;">{ic}</div>'
                f'<div style="color:#94a3b8;font-size:.72rem;text-transform:uppercase;">{lbl}</div>'
                f'<div style="font-size:1.8rem;font-weight:800;color:{clr};margin:4px 0;">{val}</div></div>',
                unsafe_allow_html=True)

    # Pipeline Funnel + Pasta — yan yana
    sayac = store.pipeline_sayac()
    toplam = max(stats["toplam"], 1)

    fc1, fc2 = st.columns(2)

    # Funnel Chart
    with fc1:
        funnel_labels = []
        funnel_values = []
        funnel_colors = []
        for key in PIPELINE_ASAMALARI + ["olumsuz"]:
            info = PIPELINE_INFO.get(key, PIPELINE_INFO["aday"])
            cnt = sayac.get(key, 0)
            funnel_labels.append(info["label"])
            funnel_values.append(cnt)
            funnel_colors.append(info["color"])

        fig = go.Figure(go.Funnel(
            y=funnel_labels, x=funnel_values,
            marker=dict(color=funnel_colors, line=dict(width=1, color="#0f172a")),
            textposition="inside", textinfo="value+percent initial",
            textfont=dict(size=11, color="#fff"),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"), margin=dict(l=10, r=10, t=40, b=10),
            title=dict(text="Pipeline Dönüşüm Hunisi", font=dict(size=14, color="#e2e8f0")),
            height=380,
        )
        st.plotly_chart(fig, use_container_width=True, key="kayit_funnel")

    # Pasta — Aşama dağılımı
    with fc2:
        pie_labels = [PIPELINE_INFO.get(k, PIPELINE_INFO["aday"])["label"] for k in PIPELINE_ASAMALARI + ["olumsuz"]]
        pie_values = [sayac.get(k, 0) for k in PIPELINE_ASAMALARI + ["olumsuz"]]
        pie_colors = [PIPELINE_INFO.get(k, PIPELINE_INFO["aday"])["color"] for k in PIPELINE_ASAMALARI + ["olumsuz"]]

        fig2 = go.Figure(data=[go.Pie(
            labels=pie_labels, values=pie_values, hole=0.45,
            marker=dict(colors=pie_colors, line=dict(color="#0f172a", width=2)),
            textinfo="label+percent", textfont=dict(size=10, color="#fff"),
            pull=[0.05 if v == max(pie_values) else 0 for v in pie_values],
        )])
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"), margin=dict(l=10, r=10, t=40, b=10),
            title=dict(text="Aşama Dağılımı", font=dict(size=14, color="#e2e8f0")),
            height=380, showlegend=False,
            annotations=[dict(text=f"<b>{toplam}</b><br>Aday", x=0.5, y=0.5,
                              font_size=14, font_color="#e2e8f0", showarrow=False)],
        )
        st.plotly_chart(fig2, use_container_width=True, key="kayit_pie")

    # Kampanya + Kanal — yan yana bar charts
    kc1, kc2 = st.columns(2)

    with kc1:
        kamp_sayac = Counter(a.kampanya or "(Bilinmiyor)" for a in adaylar)
        if kamp_sayac:
            kamps = list(kamp_sayac.most_common(10))
            kamp_names = [k for k, _ in kamps]
            kamp_counts = [c for _, c in kamps]
            kamp_kayit = [sum(1 for a in adaylar if a.kampanya == k and a.asama == "kesin_kayit") for k in kamp_names]

            fig3 = go.Figure()
            fig3.add_trace(go.Bar(x=kamp_names, y=kamp_counts, name="Aday",
                                  marker=dict(color="#6366f1", opacity=0.7),
                                  text=kamp_counts, textposition="outside"))
            fig3.add_trace(go.Bar(x=kamp_names, y=kamp_kayit, name="Kayıt",
                                  marker=dict(color="#10b981"),
                                  text=kamp_kayit, textposition="outside"))
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0", size=10), margin=dict(l=10, r=10, t=40, b=10),
                title=dict(text="Kampanya Performansı", font=dict(size=14)),
                barmode="group", height=350,
                xaxis=dict(showgrid=False, tickfont=dict(size=8)),
                yaxis=dict(showgrid=True, gridcolor="#1e293b"),
                legend=dict(bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig3, use_container_width=True, key="kayit_kamp")

    with kc2:
        kanal_sayac = Counter(a.kanal or "(Bilinmiyor)" for a in adaylar)
        if kanal_sayac:
            kanals = list(kanal_sayac.most_common(10))
            kanal_names = [k for k, _ in kanals]
            kanal_counts = [c for _, c in kanals]
            _k_colors = ["#6366f1", "#3b82f6", "#06b6d4", "#10b981", "#f59e0b",
                         "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6", "#f97316"]

            fig4 = go.Figure(data=[go.Pie(
                labels=kanal_names, values=kanal_counts, hole=0.5,
                marker=dict(colors=_k_colors[:len(kanal_names)], line=dict(color="#0f172a", width=2)),
                textinfo="label+value", textfont=dict(size=9, color="#fff"),
            )])
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"), margin=dict(l=10, r=10, t=40, b=10),
                title=dict(text="Kanal Dağılımı", font=dict(size=14)),
                height=350, showlegend=False,
            )
            st.plotly_chart(fig4, use_container_width=True, key="kayit_kanal")

    # ═══════════════════════════════════════
    # DÖNEMSEL KARŞILAŞTIRMA
    # ═══════════════════════════════════════
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;'
        'padding:14px 18px;border-radius:10px;margin:8px 0;">'
        '<b>📅 Dönemsel Karşılaştırma</b>'
        '<p style="margin:2px 0 0;font-size:11px;opacity:.85;">'
        'Bu yıl vs geçen yıl — aynı dönemde ne durumdaydık?</p></div>',
        unsafe_allow_html=True)

    bugun = date.today()
    bu_yil = bugun.year
    gecen_yil = bu_yil - 1

    # Tüm adayları yıl bazlı grupla
    def _yil_ay(aday_obj):
        try:
            t = aday_obj.olusturma_tarihi[:10]
            return int(t[:4]), int(t[5:7])
        except (ValueError, TypeError, IndexError):
            return 0, 0

    # Bu yıl vs geçen yıl — ay bazlı
    bu_yil_aylik = {}
    gecen_yil_aylik = {}
    for a in adaylar:
        y, m = _yil_ay(a)
        if y == bu_yil:
            bu_yil_aylik.setdefault(m, {"aday": 0, "kayit": 0, "olumsuz": 0})
            bu_yil_aylik[m]["aday"] += 1
            if a.asama == "kesin_kayit":
                bu_yil_aylik[m]["kayit"] += 1
            elif a.asama == "olumsuz":
                bu_yil_aylik[m]["olumsuz"] += 1
        elif y == gecen_yil:
            gecen_yil_aylik.setdefault(m, {"aday": 0, "kayit": 0, "olumsuz": 0})
            gecen_yil_aylik[m]["aday"] += 1
            if a.asama == "kesin_kayit":
                gecen_yil_aylik[m]["kayit"] += 1
            elif a.asama == "olumsuz":
                gecen_yil_aylik[m]["olumsuz"] += 1

    # Yıl toplamları
    bu_yil_toplam = sum(d["aday"] for d in bu_yil_aylik.values())
    gecen_yil_toplam = sum(d["aday"] for d in gecen_yil_aylik.values())
    bu_yil_kayit = sum(d["kayit"] for d in bu_yil_aylik.values())
    gecen_yil_kayit = sum(d["kayit"] for d in gecen_yil_aylik.values())
    bu_yil_don = (bu_yil_kayit / bu_yil_toplam * 100) if bu_yil_toplam > 0 else 0
    gecen_yil_don = (gecen_yil_kayit / gecen_yil_toplam * 100) if gecen_yil_toplam > 0 else 0

    # Karşılaştırma kartları
    kc = st.columns(4)
    _kart = [
        (f"Aday ({bu_yil})", bu_yil_toplam, f"Aday ({gecen_yil})", gecen_yil_toplam),
        (f"Kayıt ({bu_yil})", bu_yil_kayit, f"Kayıt ({gecen_yil})", gecen_yil_kayit),
        (f"Dönüşüm ({bu_yil})", f"%{bu_yil_don:.0f}", f"Dönüşüm ({gecen_yil})", f"%{gecen_yil_don:.0f}"),
    ]
    for i, (l1, v1, l2, v2) in enumerate(_kart):
        with kc[i]:
            # Değişim hesapla
            try:
                n1 = float(str(v1).replace("%", ""))
                n2 = float(str(v2).replace("%", ""))
                if n2 > 0:
                    degisim = ((n1 - n2) / n2) * 100
                    d_clr = "#22c55e" if degisim > 0 else "#ef4444"
                    d_txt = f"+{degisim:.0f}%" if degisim > 0 else f"{degisim:.0f}%"
                else:
                    d_clr = "#64748b"
                    d_txt = "—"
            except (ValueError, TypeError):
                d_clr = "#64748b"
                d_txt = "—"

            st.markdown(
                f'<div style="background:#131825;border-radius:10px;padding:12px;border:1px solid #334155;">'
                f'<div style="font-size:11px;color:#94a3b8;">{l1}</div>'
                f'<div style="font-size:20px;font-weight:800;color:#e2e8f0;">{v1}</div>'
                f'<div style="font-size:10px;color:#64748b;margin-top:4px;">{l2}: {v2}</div>'
                f'<div style="font-size:11px;color:{d_clr};font-weight:700;">Değişim: {d_txt}</div></div>',
                unsafe_allow_html=True)

    # Bu ay vs geçen yılın aynı ayı
    with kc[3]:
        bu_ay_data = bu_yil_aylik.get(bugun.month, {"aday": 0, "kayit": 0})
        gecen_ay_data = gecen_yil_aylik.get(bugun.month, {"aday": 0, "kayit": 0})
        ay_adlari = {1: "Oca", 2: "Şub", 3: "Mar", 4: "Nis", 5: "May", 6: "Haz",
                     7: "Tem", 8: "Ağu", 9: "Eyl", 10: "Eki", 11: "Kas", 12: "Ara"}
        ay_adi = ay_adlari.get(bugun.month, "?")
        st.markdown(
            f'<div style="background:#131825;border-radius:10px;padding:12px;border:1px solid #f59e0b40;">'
            f'<div style="font-size:11px;color:#fbbf24;">{ay_adi} {bu_yil} vs {ay_adi} {gecen_yil}</div>'
            f'<div style="font-size:16px;font-weight:800;color:#fbbf24;">'
            f'{bu_ay_data["aday"]} vs {gecen_ay_data["aday"]} aday</div>'
            f'<div style="font-size:12px;color:#94a3b8;">'
            f'{bu_ay_data["kayit"]} vs {gecen_ay_data["kayit"]} kayıt</div></div>',
            unsafe_allow_html=True)

    # Aylık trend grafiği — bu yıl vs geçen yıl
    if bu_yil_aylik or gecen_yil_aylik:
        aylar = sorted(set(list(bu_yil_aylik.keys()) + list(gecen_yil_aylik.keys())))
        ay_labels = [ay_adlari.get(a, str(a)) for a in aylar]
        bu_vals = [bu_yil_aylik.get(a, {}).get("aday", 0) for a in aylar]
        gecen_vals = [gecen_yil_aylik.get(a, {}).get("aday", 0) for a in aylar]
        bu_kayit = [bu_yil_aylik.get(a, {}).get("kayit", 0) for a in aylar]
        gecen_kayit = [gecen_yil_aylik.get(a, {}).get("kayit", 0) for a in aylar]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=ay_labels, y=bu_vals, name=f"Aday {bu_yil}",
                                        mode="lines+markers", line=dict(color="#6366f1", width=3),
                                        marker=dict(size=8)))
        fig_trend.add_trace(go.Scatter(x=ay_labels, y=gecen_vals, name=f"Aday {gecen_yil}",
                                        mode="lines+markers", line=dict(color="#6366f1", width=2, dash="dash"),
                                        marker=dict(size=6), opacity=0.5))
        fig_trend.add_trace(go.Bar(x=ay_labels, y=bu_kayit, name=f"Kayıt {bu_yil}",
                                    marker_color="#22c55e", opacity=0.7))
        fig_trend.add_trace(go.Bar(x=ay_labels, y=gecen_kayit, name=f"Kayıt {gecen_yil}",
                                    marker_color="#22c55e", opacity=0.3))
        fig_trend.update_layout(
            title=f"Aylık Aday & Kayıt Trendi — {bu_yil} vs {gecen_yil}",
            height=400, barmode="group",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"), margin=dict(l=30, r=10, t=50, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig_trend, use_container_width=True, key="kayit_donem_trend")

    # Dönüşüm oranı karşılaştırma
    if bu_yil_aylik and gecen_yil_aylik:
        don_aylar = sorted(set(list(bu_yil_aylik.keys()) + list(gecen_yil_aylik.keys())))
        bu_don_vals = []
        gecen_don_vals = []
        for a in don_aylar:
            bd = bu_yil_aylik.get(a, {"aday": 0, "kayit": 0})
            gd = gecen_yil_aylik.get(a, {"aday": 0, "kayit": 0})
            bu_don_vals.append((bd["kayit"] / bd["aday"] * 100) if bd["aday"] > 0 else 0)
            gecen_don_vals.append((gd["kayit"] / gd["aday"] * 100) if gd["aday"] > 0 else 0)

        don_labels = [ay_adlari.get(a, str(a)) for a in don_aylar]
        fig_don = go.Figure()
        fig_don.add_trace(go.Scatter(x=don_labels, y=bu_don_vals, name=f"Dönüşüm % {bu_yil}",
                                      mode="lines+markers+text", text=[f"%{v:.0f}" for v in bu_don_vals],
                                      textposition="top center",
                                      line=dict(color="#f59e0b", width=3), marker=dict(size=8)))
        fig_don.add_trace(go.Scatter(x=don_labels, y=gecen_don_vals, name=f"Dönüşüm % {gecen_yil}",
                                      mode="lines+markers", line=dict(color="#f59e0b", width=2, dash="dash"),
                                      opacity=0.5))
        fig_don.update_layout(
            title=f"Aylık Dönüşüm Oranı — {bu_yil} vs {gecen_yil}",
            height=300, yaxis=dict(range=[0, 100], title="%"),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"), margin=dict(l=40, r=10, t=50, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig_don, use_container_width=True, key="kayit_donem_donusum")

    # AI Dönemsel Analiz
    with st.expander("🤖 AI Dönemsel Karşılaştırma Analizi"):
        if st.button("AI Analiz Yap", key="km_donem_ai"):
            with st.spinner("AI dönemsel analiz yapıyor..."):
                from models.kayit_ai_engine import _call_gpt
                _stats_text = f"""DONEMSEL KARSILASTIRMA:
Bu yil ({bu_yil}): {bu_yil_toplam} aday, {bu_yil_kayit} kayit, %{bu_yil_don:.0f} donusum
Gecen yil ({gecen_yil}): {gecen_yil_toplam} aday, {gecen_yil_kayit} kayit, %{gecen_yil_don:.0f} donusum

Bu ay ({ay_adlari.get(bugun.month, '?')}):
  {bu_yil}: {bu_yil_aylik.get(bugun.month, {}).get('aday', 0)} aday, {bu_yil_aylik.get(bugun.month, {}).get('kayit', 0)} kayit
  {gecen_yil}: {gecen_yil_aylik.get(bugun.month, {}).get('aday', 0)} aday, {gecen_yil_aylik.get(bugun.month, {}).get('kayit', 0)} kayit

Aylik dagilim {bu_yil}: {dict(sorted(bu_yil_aylik.items()))}
Aylik dagilim {gecen_yil}: {dict(sorted(gecen_yil_aylik.items()))}"""

                result = _call_gpt(
                    "Kayit istatistikleri analisti. Bu yil vs gecen yil karsilastirma yap. "
                    "Trend, iyilesen/kotulesen alanlar, oneri ver. Turkce, kisa, aksiyona donuk. "
                    "Format: ## Trend | ## Guclu Noktalar | ## Dikkat | ## Oneri",
                    _stats_text, 800)
                if result:
                    st.markdown(result)

    # ═══════════════════════════════════════
    # PREMIUM PERFORMANS ANALİZİ
    # ═══════════════════════════════════════
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#ef4444,#f97316);color:#fff;'
        'padding:14px 18px;border-radius:10px;margin:8px 0;">'
        '<b>🏆 Premium Performans Analizi</b>'
        '<p style="margin:2px 0 0;font-size:11px;opacity:.85;">'
        'Tüm aşamalarda dönüşüm oranları + süre analizi + darboğaz tespiti</p></div>',
        unsafe_allow_html=True)

    # ── AŞAMA BAZLI DÖNÜŞÜM ──
    st.markdown("### Aşama Bazlı Dönüşüm Analizi")
    asamalar = ["aday", "arandi", "randevu", "gorusme", "fiyat_verildi", "sozlesme", "kesin_kayit"]
    asama_label = {"aday": "Yeni Aday", "arandi": "Arandı", "randevu": "Randevu", "gorusme": "Görüşme",
                   "fiyat_verildi": "Fiyat Verildi", "sozlesme": "Sözleşme", "kesin_kayit": "Kesin Kayıt"}

    # Her aşamaya kaç aday ulaştı
    asama_sayilar = {}
    for a in adaylar:
        mevcut = a.asama
        # Bu aday hangi aşamalardan geçti — pipeline sırasına göre
        gecti = []
        if a.asama == "olumsuz":
            # Olumsuz — en son hangi aşamadaydı?
            if a.gorusmeler:
                gecti = asamalar[:4]  # gorusmeye kadar
            elif a.aramalar:
                gecti = asamalar[:2]  # arandi'ya kadar
            else:
                gecti = asamalar[:1]
        elif mevcut in asamalar:
            idx = asamalar.index(mevcut)
            gecti = asamalar[:idx + 1]
        else:
            gecti = asamalar[:1]
        for as_key in gecti:
            asama_sayilar[as_key] = asama_sayilar.get(as_key, 0) + 1

    # Dönüşüm tablosu
    if asama_sayilar:
        donusum_rows = []
        prev_count = asama_sayilar.get("aday", len(adaylar))
        for as_key in asamalar:
            count = asama_sayilar.get(as_key, 0)
            if prev_count > 0:
                don_pct = (count / prev_count * 100)
                kayip = prev_count - count
            else:
                don_pct = 0
                kayip = 0
            toplam_don = (count / max(asama_sayilar.get("aday", 1), 1) * 100)
            donusum_rows.append({
                "label": asama_label.get(as_key, as_key),
                "count": count,
                "donusum": don_pct,
                "toplam_don": toplam_don,
                "kayip": kayip,
            })
            prev_count = count

        # Funnel bar grafiği
        fig_funnel = go.Figure()
        fig_funnel.add_trace(go.Funnel(
            y=[r["label"] for r in donusum_rows],
            x=[r["count"] for r in donusum_rows],
            textinfo="value+percent initial",
            marker=dict(color=["#6366f1", "#8b5cf6", "#a78bfa", "#f59e0b", "#f97316", "#10b981", "#22c55e"]),
        ))
        fig_funnel.update_layout(
            title="Pipeline Dönüşüm Hunisi",
            height=350, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"), margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig_funnel, use_container_width=True, key="perf_funnel")

        # Aşama kartları — her aşamada kaç aday, dönüşüm, kayıp
        cols = st.columns(len(donusum_rows))
        for i, r in enumerate(donusum_rows):
            clr = ["#6366f1", "#8b5cf6", "#a78bfa", "#f59e0b", "#f97316", "#10b981", "#22c55e"][i % 7]
            with cols[i]:
                st.markdown(
                    f'<div style="background:{clr}15;border:1px solid {clr}40;border-radius:8px;'
                    f'padding:8px;text-align:center;min-height:90px;">'
                    f'<div style="font-size:18px;font-weight:800;color:{clr};">{r["count"]}</div>'
                    f'<div style="font-size:9px;color:#94a3b8;">{r["label"]}</div>'
                    f'<div style="font-size:10px;color:#22c55e;">%{r["donusum"]:.0f} dönüşüm</div>'
                    f'<div style="font-size:9px;color:#ef4444;">{r["kayip"]} kayıp</div></div>',
                    unsafe_allow_html=True)

    # ── SÜRE ANALİZİ ──
    st.markdown("### Süre Analizi — Kayıt Ne Kadar Sürüyor?")
    kayitli = [a for a in adaylar if a.asama == "kesin_kayit" and a.kapanma_tarihi and a.olusturma_tarihi]
    if kayitli:
        sureler = []
        for a in kayitli:
            try:
                d1 = date.fromisoformat(a.olusturma_tarihi[:10])
                d2 = date.fromisoformat(a.kapanma_tarihi[:10])
                sureler.append((d2 - d1).days)
            except (ValueError, TypeError):
                pass
        if sureler:
            ort_sure = sum(sureler) / len(sureler)
            min_sure = min(sureler)
            max_sure = max(sureler)
            sc1, sc2, sc3, sc4 = st.columns(4)
            with sc1:
                st.metric("Ortalama Süre", f"{ort_sure:.0f} gün")
            with sc2:
                st.metric("En Hızlı", f"{min_sure} gün")
            with sc3:
                st.metric("En Yavaş", f"{max_sure} gün")
            with sc4:
                st.metric("Kayıt Sayısı", str(len(sureler)))

            # Süre dağılımı
            import numpy as np
            bins = [0, 7, 14, 30, 60, 90, 999]
            bin_labels = ["0-7 gün", "8-14 gün", "15-30 gün", "31-60 gün", "61-90 gün", "90+ gün"]
            hist_vals = [0] * len(bin_labels)
            for s in sureler:
                for bi in range(len(bins) - 1):
                    if bins[bi] <= s < bins[bi + 1]:
                        hist_vals[bi] += 1
                        break

            fig_sure = go.Figure()
            fig_sure.add_trace(go.Bar(
                x=bin_labels, y=hist_vals,
                marker_color=["#22c55e", "#22c55e", "#f59e0b", "#f59e0b", "#ef4444", "#ef4444"],
                text=[str(v) for v in hist_vals], textposition="outside",
            ))
            fig_sure.update_layout(
                title="Kayıt Süresi Dağılımı", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"), margin=dict(l=30, r=10, t=40, b=30),
            )
            st.plotly_chart(fig_sure, use_container_width=True, key="perf_sure")
    else:
        st.info("Henüz kesin kayıt olmadığı için süre analizi yapılamıyor.")

    # ── ARAMA PERFORMANSI ──
    st.markdown("### Arama Performansı")
    toplam_arama = sum(a.arama_sayisi for a in adaylar)
    arama_sonuc = {}
    for a in adaylar:
        for ar in a.aramalar:
            s = ar.get("sonuc", "?")
            arama_sonuc[s] = arama_sonuc.get(s, 0) + 1

    if arama_sonuc:
        ac1, ac2 = st.columns(2)
        with ac1:
            st.metric("Toplam Arama", str(toplam_arama))
            randevu_cnt = arama_sonuc.get("Randevu alindi", 0)
            if toplam_arama > 0:
                st.metric("Arama → Randevu %", f"%{randevu_cnt / toplam_arama * 100:.0f}")
            # Pasta grafik
            fig_arama = go.Figure(data=[go.Pie(
                labels=list(arama_sonuc.keys()), values=list(arama_sonuc.values()),
                hole=0.4, marker_colors=["#22c55e", "#f59e0b", "#3b82f6", "#ef4444", "#64748b",
                                          "#8b5cf6", "#f97316", "#ec4899"][:len(arama_sonuc)],
            )])
            fig_arama.update_layout(
                title="Arama Sonuç Dağılımı", height=300, showlegend=True,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0", size=10), margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig_arama, use_container_width=True, key="perf_arama_pie")

        with ac2:
            # Ortalama kaç aramada kayıt?
            kayitli_arama = [a.arama_sayisi for a in adaylar if a.asama == "kesin_kayit"]
            if kayitli_arama:
                st.metric("Kayıt Başına Ort. Arama", f"{sum(kayitli_arama) / len(kayitli_arama):.1f}")
            # Ortalama kaç aramada randevu?
            randevu_arama = [a.arama_sayisi for a in adaylar if a.asama in ("randevu", "gorusme", "fiyat_verildi", "sozlesme", "kesin_kayit")]
            if randevu_arama:
                st.metric("Randevu Başına Ort. Arama", f"{sum(randevu_arama) / len(randevu_arama):.1f}")
            # Ulaşım yok oranı
            ulasim_yok = arama_sonuc.get("Ulasim yok — tekrar aranacak", 0)
            if toplam_arama > 0:
                st.metric("Ulaşım Yok %", f"%{ulasim_yok / toplam_arama * 100:.0f}")

    # ── GÖRÜŞME PERFORMANSI ──
    st.markdown("### Görüşme Performansı")
    toplam_gorusme = sum(a.gorusme_sayisi for a in adaylar)
    gor_sonuc = {}
    for a in adaylar:
        for gr in a.gorusmeler:
            s = gr.get("sonuc", "?")
            gor_sonuc[s] = gor_sonuc.get(s, 0) + 1

    if gor_sonuc:
        gc1, gc2 = st.columns(2)
        with gc1:
            st.metric("Toplam Görüşme", str(toplam_gorusme))
            olumlu = sum(v for k, v in gor_sonuc.items() if "olumlu" in k.lower())
            if toplam_gorusme > 0:
                st.metric("Görüşme Olumlu %", f"%{olumlu / toplam_gorusme * 100:.0f}")
            # Pasta
            fig_gor = go.Figure(data=[go.Pie(
                labels=list(gor_sonuc.keys()), values=list(gor_sonuc.values()),
                hole=0.4, marker_colors=["#22c55e", "#f59e0b", "#3b82f6", "#ef4444", "#64748b",
                                          "#8b5cf6", "#f97316"][:len(gor_sonuc)],
            )])
            fig_gor.update_layout(
                title="Görüşme Sonuç Dağılımı", height=300, showlegend=True,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0", size=10), margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig_gor, use_container_width=True, key="perf_gor_pie")

        with gc2:
            kayitli_gor = [a.gorusme_sayisi for a in adaylar if a.asama == "kesin_kayit" and a.gorusme_sayisi > 0]
            if kayitli_gor:
                st.metric("Kayıt Başına Ort. Görüşme", f"{sum(kayitli_gor) / len(kayitli_gor):.1f}")
            gelmedi = sum(v for k, v in gor_sonuc.items() if "gelmedi" in k.lower())
            if toplam_gorusme > 0:
                st.metric("Gelmedi %", f"%{gelmedi / toplam_gorusme * 100:.0f}")

    # ── KAYIP ANALİZİ ──
    st.markdown("### Kayıp Analizi — Nerede Kaybediyoruz?")
    olumsuzlar = [a for a in adaylar if a.asama == "olumsuz"]
    if olumsuzlar:
        # Olumsuzların son aşaması
        kayip_asama = {}
        kayip_neden = {}
        for a in olumsuzlar:
            if a.gorusmeler:
                son_asama = "Görüşme Sonrası"
            elif a.aramalar:
                son_asama = "Arama Aşaması"
            else:
                son_asama = "İlk Aşama"
            kayip_asama[son_asama] = kayip_asama.get(son_asama, 0) + 1
            # Son arama/görüşme sonucu
            son_sonuc = ""
            if a.aramalar:
                son_sonuc = a.aramalar[-1].get("sonuc", "")
            if a.gorusmeler:
                son_sonuc = a.gorusmeler[-1].get("sonuc", "")
            if son_sonuc:
                kayip_neden[son_sonuc] = kayip_neden.get(son_sonuc, 0) + 1

        kc1, kc2 = st.columns(2)
        with kc1:
            st.metric("Toplam Kayıp", str(len(olumsuzlar)))
            if len(adaylar) > 0:
                st.metric("Kayıp Oranı", f"%{len(olumsuzlar) / len(adaylar) * 100:.0f}")
            # Kayıp aşama pasta
            fig_kayip = go.Figure(data=[go.Pie(
                labels=list(kayip_asama.keys()), values=list(kayip_asama.values()),
                hole=0.4, marker_colors=["#ef4444", "#f97316", "#f59e0b"],
            )])
            fig_kayip.update_layout(
                title="Kayıp Nerede Oluyor?", height=280,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0", size=10), margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig_kayip, use_container_width=True, key="perf_kayip_pie")

        with kc2:
            st.markdown("**Kayıp Nedenleri:**")
            for neden, cnt in sorted(kayip_neden.items(), key=lambda x: -x[1]):
                pct = cnt / len(olumsuzlar) * 100
                st.markdown(f'<div style="background:#ef444415;border-left:2px solid #ef4444;'
                            f'padding:4px 10px;border-radius:0 4px 4px 0;margin:2px 0;font-size:12px;">'
                            f'<b>{neden}</b> — {cnt} aday (%{pct:.0f})</div>',
                            unsafe_allow_html=True)

    # ── TEST PERFORMANSI ──
    st.markdown("### Test Performansı")
    test_yapilan = sum(1 for a in adaylar if a.testler)
    toplam_test = sum(len(a.testler) for a in adaylar)
    test_turleri = {}
    for a in adaylar:
        for t in a.testler:
            tn = t.get("test_adi", "?")
            test_turleri[tn] = test_turleri.get(tn, 0) + 1

    if test_turleri:
        tc1, tc2 = st.columns(2)
        with tc1:
            st.metric("Test Yapılan Aday", str(test_yapilan))
            st.metric("Toplam Test", str(toplam_test))
            if len(adaylar) > 0:
                st.metric("Test Uygulama %", f"%{test_yapilan / len(adaylar) * 100:.0f}")
        with tc2:
            fig_test = go.Figure(data=[go.Bar(
                x=list(test_turleri.values()),
                y=[k[:25] for k in test_turleri.keys()],
                orientation='h',
                marker_color="#8b5cf6",
                text=[str(v) for v in test_turleri.values()],
                textposition="outside",
            )])
            fig_test.update_layout(
                title="Test Türü Dağılımı", height=300,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"), margin=dict(l=120, r=30, t=40, b=10),
            )
            st.plotly_chart(fig_test, use_container_width=True, key="perf_test_bar")

    # ── KADEME PERFORMANSI ──
    st.markdown("### Kademe Bazlı Performans")
    kademe_data = {}
    for a in adaylar:
        k = a.kademe or "Belirsiz"
        kademe_data.setdefault(k, {"aday": 0, "kayit": 0, "olumsuz": 0})
        kademe_data[k]["aday"] += 1
        if a.asama == "kesin_kayit":
            kademe_data[k]["kayit"] += 1
        elif a.asama == "olumsuz":
            kademe_data[k]["olumsuz"] += 1

    if kademe_data:
        kademe_labels = list(kademe_data.keys())
        kademe_aday = [kademe_data[k]["aday"] for k in kademe_labels]
        kademe_kayit = [kademe_data[k]["kayit"] for k in kademe_labels]
        kademe_don = [(kademe_data[k]["kayit"] / kademe_data[k]["aday"] * 100) if kademe_data[k]["aday"] > 0 else 0 for k in kademe_labels]

        fig_kademe = go.Figure()
        fig_kademe.add_trace(go.Bar(name="Aday", x=kademe_labels, y=kademe_aday, marker_color="#6366f1"))
        fig_kademe.add_trace(go.Bar(name="Kayıt", x=kademe_labels, y=kademe_kayit, marker_color="#22c55e"))
        fig_kademe.add_trace(go.Scatter(name="Dönüşüm %", x=kademe_labels, y=kademe_don,
                                         mode="lines+markers+text", yaxis="y2",
                                         text=[f"%{v:.0f}" for v in kademe_don], textposition="top center",
                                         line=dict(color="#f59e0b", width=3), marker=dict(size=10)))
        fig_kademe.update_layout(
            title="Kademe Bazlı Aday vs Kayıt vs Dönüşüm",
            height=350, barmode="group",
            yaxis2=dict(overlaying="y", side="right", range=[0, 100], title="%"),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"), margin=dict(l=30, r=40, t=50, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig_kademe, use_container_width=True, key="perf_kademe")

    # ═══════════════════════════════════════
    # HEDEF PERFORMANS SİSTEMİ
    # ═══════════════════════════════════════
    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#10b981,#059669);color:#fff;'
        'padding:14px 18px;border-radius:10px;margin:8px 0;">'
        '<b>🎯 Hedef & Gerçekleşen Performans</b>'
        '<p style="margin:2px 0 0;font-size:11px;opacity:.85;">'
        'Teşvik edici, zorlayıcı ama gerçekçi hedefler — başarı burada ölçülür</p></div>',
        unsafe_allow_html=True)

    hedefler = store.load_hedefler()
    bugun = date.today()
    ay_key = f"{bugun.year}-{bugun.month:02d}"

    # Mevcut ay hedefleri
    ay_hedef = hedefler.get(ay_key, {})

    # Gerçekleşen değerler (bu ay)
    bu_ay_adaylar = [a for a in adaylar if a.olusturma_tarihi[:7] == ay_key]
    bu_ay_kayit = sum(1 for a in adaylar if a.kapanma_tarihi and a.kapanma_tarihi[:7] == ay_key and a.asama == "kesin_kayit")
    bu_ay_arama = sum(sum(1 for ar in a.aramalar if ar.get("tarih", "")[:7] == ay_key) for a in adaylar)
    bu_ay_gorusme = sum(sum(1 for gr in a.gorusmeler if gr.get("tarih", "")[:7] == ay_key) for a in adaylar)
    bu_ay_test = sum(sum(1 for t in a.testler if t.get("tarih", "")[:7] == ay_key) for a in adaylar)
    aktif_sayisi = sum(1 for a in adaylar if a.aktif)
    bu_ay_donusum = (bu_ay_kayit / len(bu_ay_adaylar) * 100) if bu_ay_adaylar else 0

    # Hedef belirleme formu
    with st.expander("⚙️ Hedef Belirle / Güncelle", expanded=not bool(ay_hedef)):
        st.markdown(
            '<div style="color:#fbbf24;font-size:12px;margin-bottom:8px;">'
            '💡 İdeal hedef: Geçen ay gerçekleşenin %15-25 üstü. '
            'Çok düşük = motivasyon kaybı. Çok yüksek = moral bozukluğu. '
            'Teşvik edici + zorlayıcı = ideal.</div>',
            unsafe_allow_html=True)

        # Geçen ay gerçekleşen (referans için)
        gecen_ay_key = f"{bugun.year}-{bugun.month - 1:02d}" if bugun.month > 1 else f"{bugun.year - 1}-12"
        gecen_ay_adaylar = [a for a in adaylar if a.olusturma_tarihi[:7] == gecen_ay_key]
        gecen_ay_kayit = sum(1 for a in adaylar if a.kapanma_tarihi and a.kapanma_tarihi[:7] == gecen_ay_key and a.asama == "kesin_kayit")

        if gecen_ay_adaylar or gecen_ay_kayit:
            st.markdown(f'<div style="color:#94a3b8;font-size:11px;">📊 Geçen ay referans: '
                        f'{len(gecen_ay_adaylar)} aday, {gecen_ay_kayit} kayıt</div>',
                        unsafe_allow_html=True)

        with st.form(f"km_hedef_{ay_key}"):
            hc1, hc2, hc3 = st.columns(3)
            with hc1:
                h_aday = st.number_input("🎯 Hedef Yeni Aday", min_value=0, value=ay_hedef.get("aday", 30), key="h_aday")
                h_kayit = st.number_input("🎯 Hedef Kesin Kayıt", min_value=0, value=ay_hedef.get("kayit", 8), key="h_kayit")
            with hc2:
                h_arama = st.number_input("🎯 Hedef Arama", min_value=0, value=ay_hedef.get("arama", 100), key="h_arama")
                h_gorusme = st.number_input("🎯 Hedef Görüşme", min_value=0, value=ay_hedef.get("gorusme", 20), key="h_gorusme")
            with hc3:
                h_test = st.number_input("🎯 Hedef Test", min_value=0, value=ay_hedef.get("test", 15), key="h_test")
                h_donusum = st.number_input("🎯 Hedef Dönüşüm %", min_value=0, max_value=100,
                                             value=ay_hedef.get("donusum", 25), key="h_donusum")

            if st.form_submit_button("💾 Hedefleri Kaydet", type="primary", use_container_width=True):
                hedefler[ay_key] = {
                    "aday": h_aday, "kayit": h_kayit, "arama": h_arama,
                    "gorusme": h_gorusme, "test": h_test, "donusum": h_donusum,
                }
                store.save_hedefler(hedefler)
                st.success("Hedefler kaydedildi!")
                st.rerun()

    # Hedef vs Gerçekleşen karşılaştırma
    if ay_hedef:
        st.markdown(f"### 🎯 Hedef vs Gerçekleşen — {bugun.strftime('%B %Y')}")

        metrikler = [
            ("Yeni Aday", len(bu_ay_adaylar), ay_hedef.get("aday", 0), "#6366f1"),
            ("Kesin Kayıt", bu_ay_kayit, ay_hedef.get("kayit", 0), "#22c55e"),
            ("Arama", bu_ay_arama, ay_hedef.get("arama", 0), "#3b82f6"),
            ("Görüşme", bu_ay_gorusme, ay_hedef.get("gorusme", 0), "#f59e0b"),
            ("Test", bu_ay_test, ay_hedef.get("test", 0), "#8b5cf6"),
            ("Dönüşüm %", round(bu_ay_donusum), ay_hedef.get("donusum", 0), "#f97316"),
        ]

        # Progress bar kartları
        cols = st.columns(3)
        for i, (label, gercek, hedef, renk) in enumerate(metrikler):
            with cols[i % 3]:
                pct = (gercek / hedef * 100) if hedef > 0 else 0
                pct = min(pct, 100)
                if pct >= 100:
                    durum_clr = "#22c55e"
                    durum_txt = "✅ HEDEF AŞILDI!"
                elif pct >= 75:
                    durum_clr = "#f59e0b"
                    durum_txt = "🔥 Hedefe yakın"
                elif pct >= 50:
                    durum_clr = "#f97316"
                    durum_txt = "⚡ Devam et"
                else:
                    durum_clr = "#ef4444"
                    durum_txt = "⚠️ Geride"

                st.markdown(
                    f'<div style="background:#131825;border:1px solid {renk}40;border-radius:10px;'
                    f'padding:12px;margin:4px 0;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<span style="color:#94a3b8;font-size:11px;">{label}</span>'
                    f'<span style="color:{durum_clr};font-size:10px;font-weight:700;">{durum_txt}</span></div>'
                    f'<div style="display:flex;align-items:baseline;gap:4px;margin-top:4px;">'
                    f'<span style="font-size:22px;font-weight:800;color:{renk};">{gercek}</span>'
                    f'<span style="font-size:12px;color:#64748b;">/ {hedef}</span></div>'
                    f'<div style="background:#1e293b;border-radius:4px;height:8px;margin-top:6px;">'
                    f'<div style="background:{durum_clr};height:8px;border-radius:4px;'
                    f'width:{pct:.0f}%;transition:width 0.5s;"></div></div>'
                    f'<div style="color:#64748b;font-size:10px;margin-top:2px;text-align:right;">%{pct:.0f}</div></div>',
                    unsafe_allow_html=True)

        # Hedef başarı grafiği
        import plotly.graph_objects as go
        fig_hedef = go.Figure()
        h_labels = [m[0] for m in metrikler]
        h_gercek = [m[1] for m in metrikler]
        h_hedef = [m[2] for m in metrikler]
        h_pct = [(g / h * 100) if h > 0 else 0 for g, h in zip(h_gercek, h_hedef)]

        fig_hedef.add_trace(go.Bar(name="Gerçekleşen", x=h_labels, y=h_pct,
                                    marker_color=["#22c55e" if p >= 100 else "#f59e0b" if p >= 75 else "#ef4444" for p in h_pct],
                                    text=[f"%{p:.0f}" for p in h_pct], textposition="outside"))
        fig_hedef.add_shape(type="line", x0=-0.5, x1=len(h_labels) - 0.5, y0=100, y1=100,
                             line=dict(color="#22c55e", width=2, dash="dash"))
        fig_hedef.update_layout(
            title="Hedef Başarı Oranları (%)", height=350,
            yaxis=dict(range=[0, max(max(h_pct) * 1.2, 110)], title="Başarı %"),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"), margin=dict(l=40, r=10, t=50, b=30),
            annotations=[dict(x=len(h_labels) - 0.5, y=100, text="HEDEF", showarrow=False,
                              font=dict(color="#22c55e", size=10))]
        )
        st.plotly_chart(fig_hedef, use_container_width=True, key="perf_hedef_chart")

        # Genel başarı yüzdesi
        genel_pct = sum(h_pct) / len(h_pct) if h_pct else 0
        g_clr = "#22c55e" if genel_pct >= 100 else "#f59e0b" if genel_pct >= 75 else "#ef4444"
        st.markdown(
            f'<div style="background:{g_clr}15;border:2px solid {g_clr};border-radius:12px;'
            f'padding:16px;text-align:center;margin:8px 0;">'
            f'<div style="font-size:14px;color:{g_clr};">Genel Hedef Başarısı</div>'
            f'<div style="font-size:36px;font-weight:800;color:{g_clr};">%{genel_pct:.0f}</div></div>',
            unsafe_allow_html=True)

    # ── RAKİP OKUL ANALİZİ ──
    st.markdown("### Rakip Okul Analizi")
    rakip_data = {}
    for a in adaylar:
        vp = a.veli_profil or {}
        rakipler = vp.get("rakip_okullar", "")
        if rakipler:
            for r in rakipler.replace(",", "|").replace("/", "|").replace(";", "|").split("|"):
                r = r.strip()
                if r and len(r) > 2:
                    rakip_data.setdefault(r, {"toplam": 0, "kayit": 0, "kaybedilen": 0})
                    rakip_data[r]["toplam"] += 1
                    if a.asama == "kesin_kayit":
                        rakip_data[r]["kayit"] += 1
                    elif a.asama == "olumsuz":
                        rakip_data[r]["kaybedilen"] += 1

    if rakip_data:
        import pandas as pd
        rows = []
        for okul, v in sorted(rakip_data.items(), key=lambda x: -x[1]["toplam"]):
            kazanma = (v["kayit"] / v["toplam"] * 100) if v["toplam"] > 0 else 0
            rows.append({"Rakip Okul": okul, "Bakan Aday": v["toplam"], "Bize Kayıt": v["kayit"],
                         "Kaybedilen": v["kaybedilen"], "Kazanma %": f"%{kazanma:.0f}"})
        df_rakip = pd.DataFrame(rows)
        st.dataframe(df_rakip, use_container_width=True, hide_index=True)

        # En çok kaybettiğimiz okul
        if any(v["kaybedilen"] > 0 for v in rakip_data.values()):
            en_cok_kayip = max(rakip_data.items(), key=lambda x: x[1]["kaybedilen"])
            st.markdown(f'<div style="background:#ef444415;border-left:3px solid #ef4444;padding:8px 12px;'
                        f'border-radius:0 8px 8px 0;margin:4px 0;font-size:12px;">'
                        f'⚠️ En çok kaybettiğimiz rakip: <b>{en_cok_kayip[0]}</b> — {en_cok_kayip[1]["kaybedilen"]} aday</div>',
                        unsafe_allow_html=True)
    else:
        st.info("Rakip okul verisi yok — Aday profillerinde 'Baktığı Diğer Okullar' alanını doldurun.")

    # ── AI PERFORMANS YORUMU ──
    with st.expander("🤖 AI Performans Yorumu"):
        if st.button("AI Performans Analizi Yap", key="km_perf_ai"):
            with st.spinner("AI performans analiz ediyor..."):
                from models.kayit_ai_engine import _call_gpt
                _p_text = f"""PERFORMANS VERILERI:
Toplam aday: {len(adaylar)}
Kesin kayit: {sum(1 for a in adaylar if a.asama == 'kesin_kayit')}
Olumsuz: {len(olumsuzlar) if 'olumsuzlar' in dir() else 0}
Donusum: %{stats['donusum']:.1f}
Toplam arama: {toplam_arama}
Toplam gorusme: {toplam_gorusme}
Test yapilan aday: {test_yapilan if 'test_yapilan' in dir() else 0}
Arama sonuclari: {arama_sonuc}
Gorusme sonuclari: {gor_sonuc if 'gor_sonuc' in dir() else {}}
Kayip asamalari: {kayip_asama if 'kayip_asama' in dir() else {}}
Kademe dagilimi: {kademe_data if 'kademe_data' in dir() else {}}"""

                result = _call_gpt(
                    "Kayit sureci performans analistisin. Verileri analiz et. "
                    "Format: ## Genel Durum | ## Guclu Yonler | ## Darbogazlar | ## Kayip Analizi | ## Oneri (5 madde). "
                    "Turkce, somut, aksiyona donuk.",
                    _p_text, 1200)
                if result:
                    st.markdown(result)


# ============================================================
# RAPORLAR SEKMESI
# ============================================================

def _make_pie_chart(data: dict, title: str, colors: list[str] | None = None) -> bytes | None:
    """Matplotlib ile pasta grafigi olustur, PNG bytes dondur."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        filtered = {k: v for k, v in data.items() if v > 0}
        if not filtered:
            return None

        labels = list(filtered.keys())
        values = list(filtered.values())

        _default_colors = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#3b82f6",
                           "#8b5cf6", "#ec4899", "#14b8a6", "#fb923c", "#a78bfa",
                           "#38bdf8", "#4ade80", "#fbbf24", "#f87171", "#0ea5e9"]
        clrs = (colors or _default_colors)[:len(values)]

        fig, ax = plt.subplots(figsize=(5, 3.5))
        fig.patch.set_facecolor("#0f172a")
        wedges, texts, autotexts = ax.pie(
            values, labels=None, autopct=lambda p: f"{p:.0f}%" if p > 3 else "",
            colors=clrs, startangle=90, pctdistance=0.75,
            wedgeprops=dict(width=0.45, edgecolor="#0f172a", linewidth=2))
        for t in autotexts:
            t.set_color("#ffffff")
            t.set_fontsize(8)
            t.set_fontweight("bold")

        ax.legend(
            [f"{l} ({v})" for l, v in zip(labels, values)],
            loc="center left", bbox_to_anchor=(1, 0.5),
            fontsize=7, frameon=False,
            labelcolor="#94a3b8")
        ax.set_title(title, color="#e2e8f0", fontsize=10, fontweight="bold", pad=10)

        import io
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=120, bbox_inches="tight",
                    facecolor="#0f172a", edgecolor="none")
        plt.close(fig)
        buf.seek(0)
        return buf.getvalue()
    except Exception:
        return None


def _render_personel_performans(adaylar: list[KayitAday]):
    """Personel bazli arama / gorusme / sozlesme performans raporu."""
    from utils.ui_common import styled_section
    styled_section("Personel Performans Raporu", "#f59e0b")

    # Tum arama/gorusme/sozlesme kayitlarindan yapan_kisi topla
    personel_stats: dict[str, dict] = {}

    for aday in adaylar:
        for ar in aday.aramalar:
            kisi = ar.get("yapan_kisi", "")
            if not kisi:
                continue
            if kisi not in personel_stats:
                personel_stats[kisi] = {"arama": 0, "ulasilan": 0, "randevu": 0,
                                         "gorusme": 0, "fiyat": 0, "sozlesme": 0, "kayit": 0}
            personel_stats[kisi]["arama"] += 1
            sonuc = ar.get("sonuc", "")
            if sonuc and "Ulasim yok" not in sonuc and "Mesaj birakildi" not in sonuc:
                personel_stats[kisi]["ulasilan"] += 1
            if "Randevu" in sonuc:
                personel_stats[kisi]["randevu"] += 1

        for gr in aday.gorusmeler:
            kisi = gr.get("yapan_kisi", "")
            if not kisi:
                continue
            if kisi not in personel_stats:
                personel_stats[kisi] = {"arama": 0, "ulasilan": 0, "randevu": 0,
                                         "gorusme": 0, "fiyat": 0, "sozlesme": 0, "kayit": 0}
            personel_stats[kisi]["gorusme"] += 1
            sonuc = gr.get("sonuc", "")
            if "Fiyat" in sonuc or "Sozlesme" in sonuc:
                personel_stats[kisi]["fiyat"] += 1

        sb = aday.sozlesme_bilgi
        if sb and sb.get("yapan_kisi"):
            kisi = sb["yapan_kisi"]
            if kisi not in personel_stats:
                personel_stats[kisi] = {"arama": 0, "ulasilan": 0, "randevu": 0,
                                         "gorusme": 0, "fiyat": 0, "sozlesme": 0, "kayit": 0}
            personel_stats[kisi]["sozlesme"] += 1
            if aday.asama == "kesin_kayit":
                personel_stats[kisi]["kayit"] += 1

    if not personel_stats:
        st.info("Henuz personel bazli kayit yok. Arama/gorusme/sozlesme formlarinda 'Yapan Kisi' secilerek veri olusur.")
        return

    # Tablo
    import pandas as pd
    rows = []
    for kisi, s in sorted(personel_stats.items(), key=lambda x: x[1]["arama"], reverse=True):
        ulasma_oran = (s["ulasilan"] / s["arama"] * 100) if s["arama"] > 0 else 0
        rows.append({
            "Personel": kisi,
            "📞 Arama": s["arama"],
            "✅ Ulaşılan": s["ulasilan"],
            "📊 Ulaşma %": f"{ulasma_oran:.0f}%",
            "📅 Randevu": s["randevu"],
            "🤝 Görüşme": s["gorusme"],
            "💰 Fiyat": s["fiyat"],
            "📄 Sözleşme": s["sozlesme"],
            "🎯 Kayıt": s["kayit"],
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Kisi bazli karsilastirma bari
    if len(personel_stats) >= 2:
        st.markdown("")
        kisiler = list(personel_stats.keys())
        metrikler = ["arama", "ulasilan", "gorusme", "sozlesme", "kayit"]
        renk_map = {"arama": "#3b82f6", "ulasilan": "#10b981", "gorusme": "#f59e0b",
                    "sozlesme": "#8b5cf6", "kayit": "#22c55e"}
        import plotly.graph_objects as go
        fig = go.Figure()
        for m in metrikler:
            fig.add_trace(go.Bar(
                name=m.title(),
                x=kisiler,
                y=[personel_stats[k][m] for k in kisiler],
                marker_color=renk_map.get(m, "#6366f1"),
            ))
        fig.update_layout(
            barmode="group",
            title="Personel Karşılaştırma",
            paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
            font=dict(color="#e2e8f0", size=12),
            height=350, margin=dict(l=40, r=20, t=50, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)


def _render_raporlar(store: KayitDataStore, adaylar: list[KayitAday]):
    """Otomatik durum raporlari — pipeline asamalarina gore detayli kirilim + pasta grafikleri."""
    st.markdown(
        '<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);border-radius:12px;'
        'padding:1.2rem 1.5rem;margin-bottom:1rem">'
        '<h3 style="color:#fff;margin:0">📑 Kayit Surec Raporlari</h3>'
        '<p style="color:#c7d2fe;margin:0.3rem 0 0 0;font-size:0.9rem">'
        'Tum asamalarin detayli kirilimi + pasta grafikleri + PDF rapor</p></div>',
        unsafe_allow_html=True)

    if not adaylar:
        styled_info_banner("Henuz aday kaydi yok.", "info")
        return

    # ── Genel Ozet Metrikler ──
    toplam = len(adaylar)
    aktif = [a for a in adaylar if a.aktif]
    kesin = [a for a in adaylar if a.asama == "kesin_kayit"]
    olumsuz_l = [a for a in adaylar if a.asama == "olumsuz"]
    donusum = (len(kesin) / toplam * 100) if toplam > 0 else 0

    mc = st.columns(5)
    _ozet = [
        (mc[0], "Toplam Aday", toplam, "#6366f1"),
        (mc[1], "Aktif Surec", len(aktif), "#f59e0b"),
        (mc[2], "Kesin Kayit", len(kesin), "#10b981"),
        (mc[3], "Olumsuz", len(olumsuz_l), "#ef4444"),
        (mc[4], "Donusum", f"%{donusum:.1f}", "#3b82f6"),
    ]
    for col, lbl, val, clr in _ozet:
        with col:
            st.markdown(
                f'<div style="background:{clr}12;border:2px solid {clr}30;border-radius:12px;'
                f'padding:14px;text-align:center">'
                f'<div style="font-size:1.8rem;font-weight:800;color:{clr}">{val}</div>'
                f'<div style="font-size:0.75rem;color:#94a3b8">{lbl}</div></div>',
                unsafe_allow_html=True)

    st.markdown("")

    # ── PASTA GRAFIKLERI ──
    pipeline_sayac = Counter(a.asama for a in adaylar)

    gc1, gc2 = st.columns(2)
    with gc1:
        pie_data = {}
        for key in PIPELINE_ASAMALARI + ["olumsuz"]:
            info = PIPELINE_INFO.get(key, {})
            cnt = pipeline_sayac.get(key, 0)
            if cnt > 0:
                pie_data[info.get("label", key)] = cnt
        pie_img = _make_pie_chart(pie_data, "Pipeline Dagilimi",
                                  ["#4ade80", "#facc15", "#fb923c", "#60a5fa", "#a78bfa", "#38bdf8", "#10b981", "#f87171"])
        if pie_img:
            st.image(pie_img, use_container_width=True)

    with gc2:
        kanal_sayac = Counter(a.kanal or "(Bilinmiyor)" for a in adaylar)
        kanal_top = dict(kanal_sayac.most_common(8))
        pie_img2 = _make_pie_chart(kanal_top, "Kanal Dagilimi")
        if pie_img2:
            st.image(pie_img2, use_container_width=True)

    gc3, gc4 = st.columns(2)
    with gc3:
        kamp_sayac = Counter(a.kampanya or "(Bilinmiyor)" for a in adaylar)
        kamp_top = dict(kamp_sayac.most_common(8))
        pie_img3 = _make_pie_chart(kamp_top, "Kampanya Dagilimi")
        if pie_img3:
            st.image(pie_img3, use_container_width=True)

    with gc4:
        kademe_sayac = Counter(a.kademe or "(Bilinmiyor)" for a in adaylar)
        pie_img4 = _make_pie_chart(dict(kademe_sayac.most_common(8)), "Kademe Dagilimi",
                                   ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"])
        if pie_img4:
            st.image(pie_img4, use_container_width=True)

    # Cinsiyet + Okul Turu pastalari
    gc_co1, gc_co2 = st.columns(2)
    with gc_co1:
        cinsiyet_sayac = Counter(a.cinsiyet or "(Belirtilmemis)" for a in adaylar)
        pie_cin = _make_pie_chart(dict(cinsiyet_sayac.most_common()), "Cinsiyet Dagilimi",
                                  ["#3b82f6", "#ec4899", "#94a3b8"])
        if pie_cin:
            st.image(pie_cin, use_container_width=True)
    with gc_co2:
        okul_turu_sayac = Counter(a.okul_turu or "(Belirtilmemis)" for a in adaylar)
        pie_okul = _make_pie_chart(dict(okul_turu_sayac.most_common()), "Mevcut Okul Turu Dagilimi",
                                   ["#f59e0b", "#6366f1", "#94a3b8"])
        if pie_okul:
            st.image(pie_okul, use_container_width=True)

    # Arama sonucu pasta
    tum_son_aramalar = [a.son_arama_sonucu for a in adaylar if a.son_arama_sonucu]
    if tum_son_aramalar:
        gc5, gc6 = st.columns(2)
        with gc5:
            arama_sonuc_sayac = Counter(tum_son_aramalar)
            pie_img5 = _make_pie_chart(dict(arama_sonuc_sayac.most_common(8)), "Son Arama Sonuclari")
            if pie_img5:
                st.image(pie_img5, use_container_width=True)
        with gc6:
            # Gorusme sonucu pasta
            tum_gorusme_sonuc = []
            for a in adaylar:
                if a.gorusmeler:
                    tum_gorusme_sonuc.append(a.gorusmeler[-1].get("sonuc", ""))
            if tum_gorusme_sonuc:
                gorusme_sonuc_sayac = Counter(s for s in tum_gorusme_sonuc if s)
                pie_img6 = _make_pie_chart(dict(gorusme_sonuc_sayac.most_common(8)), "Son Gorusme Sonuclari")
                if pie_img6:
                    st.image(pie_img6, use_container_width=True)

    st.markdown("")

    # ── DONUSUM HUNISI ──
    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed,#4f46e5);border-radius:12px;'
        'padding:1rem 1.5rem;margin:1rem 0">'
        '<h4 style="color:#fff;margin:0">🔻 Donusum Hunisi — Aday\'dan Kayit\'a</h4></div>',
        unsafe_allow_html=True)

    aranan_cnt = sum(1 for a in adaylar if a.aramalar)
    cevap_veren_cnt = sum(1 for a in adaylar if a.aramalar and any(
        ar.get("sonuc") not in ("Ulasim yok — tekrar aranacak", "Mesaj birakildi", "Telefon yanlis")
        for ar in a.aramalar))
    gorusmeye_gelen_cnt = sum(1 for a in adaylar if a.gorusmeler and any(
        gr.get("sonuc") != "Veli gelmedi" for gr in a.gorusmeler))
    fiyat_alan_cnt = sum(1 for a in adaylar if a.fiyat_bilgi)
    sozlesme_imza_cnt = sum(1 for a in adaylar if a.asama in ("sozlesme", "kesin_kayit"))
    kayit_olan_cnt = len(kesin)

    _funnel = [
        ("Toplam Aday", toplam, "#6366f1"),
        ("Aranan", aranan_cnt, "#f59e0b"),
        ("Aramaya Cevap Veren", cevap_veren_cnt, "#0ea5e9"),
        ("Gorusmeye Gelen", gorusmeye_gelen_cnt, "#3b82f6"),
        ("Fiyat Alan", fiyat_alan_cnt, "#a78bfa"),
        ("Sozlesme Imzalayan", sozlesme_imza_cnt, "#38bdf8"),
        ("Kesin Kayit", kayit_olan_cnt, "#10b981"),
    ]
    for lbl, cnt, clr in _funnel:
        pct = (cnt / toplam * 100) if toplam > 0 else 0
        bar_w = max(pct, 3)
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin:4px 0">'
            f'<span style="min-width:170px;font-size:0.82rem;color:#94a3b8;text-align:right">{lbl}</span>'
            f'<div style="flex:1;background:#1e293b;border-radius:6px;height:28px;overflow:hidden;position:relative">'
            f'<div style="width:{bar_w}%;height:100%;background:{clr};border-radius:6px;'
            f'display:flex;align-items:center;padding:0 10px">'
            f'<span style="color:#fff;font-size:0.78rem;font-weight:700">{cnt}</span></div></div>'
            f'<span style="min-width:50px;font-size:0.78rem;color:{clr};font-weight:700">%{pct:.0f}</span></div>',
            unsafe_allow_html=True)

    # Hunisi pasta grafigi
    hc1, hc2 = st.columns(2)
    with hc1:
        funnel_data = {f"{l} ({c})": c for l, c, _ in _funnel if c > 0}
        if funnel_data:
            pie_funnel = _make_pie_chart(funnel_data, "Donusum Hunisi",
                                         ["#6366f1", "#f59e0b", "#0ea5e9", "#3b82f6", "#a78bfa", "#38bdf8", "#10b981"])
            if pie_funnel:
                st.image(pie_funnel, use_container_width=True)
    with hc2:
        # Aranan vs Cevap Veren ayirimi
        aranip_cevap = cevap_veren_cnt
        aranip_cevapsiz = aranan_cnt - cevap_veren_cnt
        if aranan_cnt > 0:
            arama_ayrim = {"Cevap Veren": aranip_cevap, "Cevap Vermeyen": aranip_cevapsiz}
            pie_arama = _make_pie_chart(arama_ayrim, f"Arama Sonucu: {aranan_cnt} aranmis",
                                        ["#10b981", "#ef4444"])
            if pie_arama:
                st.image(pie_arama, use_container_width=True)

    st.markdown("")

    # ── Asama Bazli Detayli Raporlar ──

    # 1) ADAY - Yeni girilenler
    aday_listesi = [a for a in adaylar if a.asama == "aday"]
    _render_asama_rapor("🟢 Aday Olarak Kayit Edilenler", "#4ade80", aday_listesi,
                        "Henuz aranmamis / ilk temas bekleniyor")

    # 2) ARANDI - Arama durumu kirilimi
    _render_arama_kirilim_rapor(adaylar)

    # 3) RANDEVU ALINANLAR
    randevu_listesi = [a for a in adaylar if a.asama == "randevu"]
    _render_asama_rapor("🟠 Randevu Alinanlar", "#fb923c", randevu_listesi,
                        "Randevu tarihi belirlenmis, gorusme bekliyor")

    # 4) GORUSME - Gorusme kirilimi
    _render_gorusme_kirilim_rapor(adaylar)

    # 5) FIYAT VERILENLER
    fiyat_listesi = [a for a in adaylar if a.asama == "fiyat_verildi"]
    _render_asama_rapor("🟣 Fiyat Verilenler", "#a78bfa", fiyat_listesi,
                        "Fiyat teklifi yapildi, veli karar asamasinda")

    # 6) SOZLESME IMZALAYANLAR
    sozlesme_listesi = [a for a in adaylar if a.asama == "sozlesme"]
    _render_asama_rapor("🔷 Sozlesme Imzalayanlar", "#38bdf8", sozlesme_listesi,
                        "Sozlesme yapildi, kesin kayit bekleniyor")

    # 7) KESIN KAYIT OLANLAR
    _render_asama_rapor("✅ Kesin Kayit Olanlar", "#10b981", kesin,
                        "Kayit tamamlandi")

    # 8) OLUMSUZ SONUCLANANLAR
    _render_asama_rapor("❌ Olumsuz Sonuclananlar", "#ef4444", olumsuz_l,
                        "Kayit sureci olumsuz sonuclandi")

    # ── PDF Rapor ──
    st.markdown("---")
    st.markdown(
        '<div style="background:#172554;border:1px solid #3b82f6;border-radius:10px;padding:1rem;margin:1rem 0">'
        '<strong style="color:#93c5fd;font-size:1rem">📥 Toplu Rapor Indir</strong></div>',
        unsafe_allow_html=True)
    pdf_bytes = _generate_genel_durum_raporu_pdf(adaylar)
    if pdf_bytes:
        st.download_button("📥 Genel Durum Raporu PDF", data=pdf_bytes,
                           file_name=f"KayitModulu_GenelDurumRaporu_{date.today().isoformat()}.pdf",
                           mime="application/pdf", key="km_genel_rapor_pdf", use_container_width=True)


def _render_asama_rapor(baslik: str, renk: str, liste: list[KayitAday], aciklama: str):
    """Tek asama icin kart + aday listesi."""
    with st.expander(f"{baslik} ({len(liste)})", expanded=False):
        st.markdown(
            f'<div style="background:{renk}12;border-left:4px solid {renk};border-radius:0 10px 10px 0;'
            f'padding:10px 14px;margin-bottom:10px">'
            f'<strong style="color:{renk}">{len(liste)} aday</strong>'
            f'<span style="color:#94a3b8;font-size:0.8rem;margin-left:8px">{aciklama}</span></div>',
            unsafe_allow_html=True)
        if not liste:
            st.caption("Bu asamada aday yok.")
            return
        for a in sorted(liste, key=lambda x: x.son_islem_tarihi or "", reverse=True):
            fb = a.fiyat_bilgi or {}
            ucret = float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0)
            ucret_text = f" | 💰 {ucret:,.0f} TL" if ucret > 0 else ""
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;padding:6px 10px;margin:3px 0;'
                f'background:#111827;border:1px solid #1e293b;border-radius:6px;border-left:3px solid {renk}">'
                f'<span style="color:#e2e8f0;font-weight:600;min-width:160px">{a.ogrenci_adi}</span>'
                f'<span style="color:#94a3b8;font-size:0.8rem">👤 {a.veli_adi}</span>'
                f'<span style="color:#94a3b8;font-size:0.8rem">🎓 {a.kademe or "-"} {a.hedef_sinif or ""}</span>'
                f'<span style="color:#94a3b8;font-size:0.8rem">📞 {a.arama_sayisi} arama | 🤝 {a.gorusme_sayisi} gorusme{ucret_text}</span>'
                f'<span style="color:#64748b;font-size:0.75rem;margin-left:auto">{a.son_islem_tarihi[:10] if a.son_islem_tarihi else "-"}</span>'
                f'</div>',
                unsafe_allow_html=True)


def _render_arama_kirilim_rapor(adaylar: list[KayitAday]):
    """Arama durumu kirilimi: 1-5. arama bazli dagilim."""
    # Tum aktif + arandi adaylar
    arama_adaylari = [a for a in adaylar if a.asama in ("aday", "arandi") and a.aramalar]
    bekleyenler = [a for a in adaylar if a.asama in ("aday", "arandi") and not a.aramalar]

    with st.expander(f"🟡 Arama Durumlari (Toplam: {len(arama_adaylari) + len(bekleyenler)})", expanded=False):
        st.markdown(
            '<div style="background:#fbbf2412;border-left:4px solid #fbbf24;border-radius:0 10px 10px 0;'
            'padding:10px 14px;margin-bottom:10px">'
            '<strong style="color:#fbbf24">Arama Kirilimi</strong></div>',
            unsafe_allow_html=True)

        # Arama bekleyenler
        st.markdown(f'<div style="color:#f59e0b;font-weight:700;margin:8px 0">📵 Arama Bekleyenler: {len(bekleyenler)}</div>',
                    unsafe_allow_html=True)
        for a in bekleyenler[:10]:
            st.markdown(
                f'<div style="padding:4px 10px;margin:2px 0;background:#422006;border-radius:4px;font-size:0.8rem;color:#fde68a">'
                f'{a.ogrenci_adi} — {a.veli_adi} | {a.kademe or "-"} | Kayit: {a.olusturma_tarihi[:10]}</div>',
                unsafe_allow_html=True)
        if len(bekleyenler) > 10:
            st.caption(f"... ve {len(bekleyenler) - 10} aday daha")

        # Arama sayisina gore kirilim
        for arama_no in range(1, 6):
            grubu = [a for a in arama_adaylari if a.arama_sayisi == arama_no]
            if not grubu:
                continue
            # Sonuc bazli kirilim
            sonuc_sayac = Counter(a.son_arama_sonucu for a in grubu)
            st.markdown(f'<div style="color:#facc15;font-weight:700;margin:12px 0 4px">📞 {arama_no}. Arama: {len(grubu)} aday</div>',
                        unsafe_allow_html=True)
            for sonuc, cnt in sonuc_sayac.most_common():
                clr = "#4ade80" if "olumlu" in sonuc.lower() or "Randevu" in sonuc else (
                    "#ef4444" if "olumsuz" in sonuc.lower() or "yanlis" in sonuc.lower() else "#94a3b8")
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;padding:4px 10px;margin:2px 0;'
                    f'background:#1e293b;border-radius:4px;font-size:0.8rem">'
                    f'<span style="color:{clr};font-weight:600;min-width:200px">{sonuc}</span>'
                    f'<span style="color:#e2e8f0;font-weight:700">{cnt}</span></div>',
                    unsafe_allow_html=True)

        # 5+ arama
        cok_aranan = [a for a in arama_adaylari if a.arama_sayisi >= 5]
        if cok_aranan:
            st.markdown(f'<div style="color:#ef4444;font-weight:700;margin:12px 0 4px">🔴 5+ Arama (Kritik): {len(cok_aranan)} aday</div>',
                        unsafe_allow_html=True)
            for a in cok_aranan:
                st.markdown(
                    f'<div style="padding:4px 10px;margin:2px 0;background:#450a0a;border-radius:4px;font-size:0.8rem;color:#fca5a5">'
                    f'{a.ogrenci_adi} — {a.arama_sayisi} arama | Son: {a.son_arama_sonucu}</div>',
                    unsafe_allow_html=True)


def _render_gorusme_kirilim_rapor(adaylar: list[KayitAday]):
    """Gorusme durumu kirilimi: 1-5. gorusme bazli dagilim."""
    gorusme_adaylari = [a for a in adaylar if a.gorusmeler]

    with st.expander(f"🔵 Gorusme Durumlari (Toplam: {len(gorusme_adaylari)})", expanded=False):
        st.markdown(
            '<div style="background:#60a5fa12;border-left:4px solid #60a5fa;border-radius:0 10px 10px 0;'
            'padding:10px 14px;margin-bottom:10px">'
            '<strong style="color:#60a5fa">Gorusme Kirilimi</strong></div>',
            unsafe_allow_html=True)

        if not gorusme_adaylari:
            st.caption("Henuz gorusme kaydi yok.")
            return

        for gorusme_no in range(1, 6):
            grubu = [a for a in gorusme_adaylari if a.gorusme_sayisi == gorusme_no]
            if not grubu:
                continue
            sonuc_sayac = Counter(
                a.gorusmeler[-1].get("sonuc", "") if a.gorusmeler else ""
                for a in grubu
            )
            st.markdown(f'<div style="color:#60a5fa;font-weight:700;margin:12px 0 4px">🤝 {gorusme_no}. Gorusme: {len(grubu)} aday</div>',
                        unsafe_allow_html=True)
            for sonuc, cnt in sonuc_sayac.most_common():
                clr = "#4ade80" if "olumlu" in sonuc.lower() else (
                    "#ef4444" if "olumsuz" in sonuc.lower() else "#94a3b8")
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;padding:4px 10px;margin:2px 0;'
                    f'background:#1e293b;border-radius:4px;font-size:0.8rem">'
                    f'<span style="color:{clr};font-weight:600;min-width:240px">{sonuc or "-"}</span>'
                    f'<span style="color:#e2e8f0;font-weight:700">{cnt}</span></div>',
                    unsafe_allow_html=True)

        # 5+ gorusme
        cok_gorusen = [a for a in gorusme_adaylari if a.gorusme_sayisi >= 5]
        if cok_gorusen:
            st.markdown(f'<div style="color:#f59e0b;font-weight:700;margin:12px 0 4px">⚠️ 5+ Gorusme: {len(cok_gorusen)} aday</div>',
                        unsafe_allow_html=True)
            for a in cok_gorusen:
                son_gr = a.gorusmeler[-1] if a.gorusmeler else {}
                st.markdown(
                    f'<div style="padding:4px 10px;margin:2px 0;background:#422006;border-radius:4px;font-size:0.8rem;color:#fde68a">'
                    f'{a.ogrenci_adi} — {a.gorusme_sayisi} gorusme | Son: {son_gr.get("sonuc", "-")}</div>',
                    unsafe_allow_html=True)


def _generate_genel_durum_raporu_pdf(adaylar: list[KayitAday]) -> bytes | None:
    """Ultra profesyonel Genel Durum Raporu PDF — ReportPDFGenerator ile."""
    try:
        from utils.report_utils import ReportPDFGenerator
        from utils.shared_data import load_kurum_profili
        import pandas as _pd

        kp = load_kurum_profili()
        k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")
        logo_path = kp.get("logo_path", "")

        toplam = len(adaylar)
        pipeline_sayac = Counter(a.asama for a in adaylar)
        kesin_cnt = pipeline_sayac.get("kesin_kayit", 0)
        olumsuz_cnt = pipeline_sayac.get("olumsuz", 0)
        aktif_cnt = sum(1 for a in adaylar if a.aktif)
        donusum_pct = (kesin_cnt / toplam * 100) if toplam > 0 else 0

        pdf = ReportPDFGenerator(
            "Ogrenci Kayit Surec Raporu",
            f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')} | Toplam: {toplam} aday",
        )
        pdf.add_header(k_adi, logo_path)

        # ── 1. GENEL OZET METRIKLERI ──
        pdf.add_section("Genel Ozet", "#6366f1")
        pdf.add_metrics([
            ("Toplam Aday", toplam, "#6366f1"),
            ("Aktif Surec", aktif_cnt, "#f59e0b"),
            ("Kesin Kayit", kesin_cnt, "#10b981"),
            ("Olumsuz", olumsuz_cnt, "#ef4444"),
            (f"Donusum %{donusum_pct:.1f}", f"%{donusum_pct:.1f}", "#3b82f6"),
        ])
        pdf.add_spacer(0.4)

        # ── 2. PIPELINE DAGILIMI ──
        pdf.add_section("Pipeline Dagilimi", "#8b5cf6")
        pipe_rows = []
        pipe_data = {}
        pipe_colors = ["#4ade80", "#facc15", "#fb923c", "#60a5fa", "#a78bfa", "#38bdf8", "#10b981", "#f87171"]
        for key in PIPELINE_ASAMALARI + ["olumsuz"]:
            info = PIPELINE_INFO.get(key, {})
            cnt = pipeline_sayac.get(key, 0)
            pct = (cnt / toplam * 100) if toplam > 0 else 0
            lbl = info.get("label", key)
            pipe_rows.append({"Asama": f'{info.get("emoji", "")} {lbl}', "Aday": cnt, "Oran": f"%{pct:.0f}"})
            if cnt > 0:
                pipe_data[lbl] = cnt
        pdf.add_table(_pd.DataFrame(pipe_rows), "#8b5cf6")
        if pipe_data:
            pdf.add_donut_chart(pipe_data, "Pipeline Dagilimi", pipe_colors)

        # ── 3. ARAMA KIRILIMI ──
        pdf.add_section("Arama Kirilimi", "#f59e0b")
        aranmamis = sum(1 for a in adaylar if not a.aramalar and a.aktif)
        arama_rows = [{"Durum": "Arama Bekleyenler", "Sayi": aranmamis}]
        arama_chart = {}
        if aranmamis > 0:
            arama_chart["Bekleyen"] = aranmamis
        for arama_no in range(1, 6):
            cnt = sum(1 for a in adaylar if a.arama_sayisi == arama_no)
            if cnt > 0:
                arama_rows.append({"Durum": f"{arama_no}. Arama Yapilmis", "Sayi": cnt})
                arama_chart[f"{arama_no}. Arama"] = cnt
        cnt_5plus = sum(1 for a in adaylar if a.arama_sayisi >= 5)
        if cnt_5plus:
            arama_rows.append({"Durum": "5+ Arama (Kritik)", "Sayi": cnt_5plus})
        pdf.add_table(_pd.DataFrame(arama_rows), "#f59e0b")

        # Arama sonuc dagilimi
        tum_son_aramalar = [a.son_arama_sonucu for a in adaylar if a.son_arama_sonucu]
        if tum_son_aramalar:
            sonuc_sayac = Counter(tum_son_aramalar)
            sonuc_rows = [{"Sonuc": s, "Sayi": c} for s, c in sonuc_sayac.most_common()]
            pdf.add_text("Son Arama Sonuclari:")
            pdf.add_table(_pd.DataFrame(sonuc_rows), "#d97706")
            sonuc_chart = {s[:25]: c for s, c in sonuc_sayac.most_common(8)}
            pdf.add_donut_chart(sonuc_chart, "Arama Sonuclari Dagilimi")
        elif arama_chart:
            pdf.add_donut_chart(arama_chart, "Arama Dagilimi")

        # ── 4. GORUSME KIRILIMI ──
        pdf.add_section("Gorusme Kirilimi", "#0ea5e9")
        gorusme_adaylari = [a for a in adaylar if a.gorusmeler]
        gorusme_rows = [{"Durum": "Toplam Gorusen Aday", "Sayi": len(gorusme_adaylari)}]
        gorusme_chart = {}
        for gorusme_no in range(1, 6):
            cnt = sum(1 for a in gorusme_adaylari if a.gorusme_sayisi == gorusme_no)
            if cnt > 0:
                gorusme_rows.append({"Durum": f"{gorusme_no}. Gorusme Yapilmis", "Sayi": cnt})
                gorusme_chart[f"{gorusme_no}. Gorusme"] = cnt
        pdf.add_table(_pd.DataFrame(gorusme_rows), "#0ea5e9")

        # Gorusme sonuc dagilimi
        tum_gorusme_sonuc = [a.gorusmeler[-1].get("sonuc", "") for a in gorusme_adaylari if a.gorusmeler]
        if tum_gorusme_sonuc:
            gr_sonuc_sayac = Counter(s for s in tum_gorusme_sonuc if s)
            if gr_sonuc_sayac:
                gr_sonuc_rows = [{"Sonuc": s, "Sayi": c} for s, c in gr_sonuc_sayac.most_common()]
                pdf.add_text("Son Gorusme Sonuclari:")
                pdf.add_table(_pd.DataFrame(gr_sonuc_rows), "#0284c7")
                pdf.add_donut_chart(dict(gr_sonuc_sayac.most_common(8)), "Gorusme Sonuclari")
        elif gorusme_chart:
            pdf.add_donut_chart(gorusme_chart, "Gorusme Dagilimi")

        # ── 5. FIYAT DURUMU ──
        pdf.add_section("Fiyat Verilmis Adaylar", "#a78bfa")
        fiyat_adaylari = [a for a in adaylar if a.fiyat_bilgi]
        toplam_teklif = sum(float(a.fiyat_bilgi.get("genel_toplam_final", a.fiyat_bilgi.get("brut_toplam", 0)) or 0) for a in fiyat_adaylari)
        pdf.add_metrics([
            ("Fiyat Verilmis", len(fiyat_adaylari), "#a78bfa"),
            ("Toplam Teklif", f"{toplam_teklif:,.0f} TL", "#8b5cf6"),
        ])
        if fiyat_adaylari:
            fiyat_rows = []
            for a in fiyat_adaylari:
                fb = a.fiyat_bilgi or {}
                ucret = float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0)
                fiyat_rows.append({
                    "Ogrenci": a.ogrenci_adi[:25],
                    "Veli": a.veli_adi[:20],
                    "Kademe": a.kademe or "-",
                    "Toplam": f"{ucret:,.0f} TL",
                    "Asama": PIPELINE_INFO.get(a.asama, {}).get("label", a.asama),
                })
            pdf.add_table(_pd.DataFrame(fiyat_rows), "#a78bfa")

        # ── 6. SOZLESME DURUMU ──
        pdf.add_section("Sozlesme Durumu", "#38bdf8")
        sozlesme_adaylari = [a for a in adaylar if a.asama == "sozlesme"]
        pdf.add_metrics([("Sozlesme Imzalayan", len(sozlesme_adaylari), "#38bdf8")])
        if sozlesme_adaylari:
            soz_rows = [{"Ogrenci": a.ogrenci_adi, "Veli": a.veli_adi, "Kademe": a.kademe or "-"} for a in sozlesme_adaylari]
            pdf.add_table(_pd.DataFrame(soz_rows), "#38bdf8")

        # ── 7. KESIN KAYIT LISTESI ──
        pdf.add_section("Kesin Kayit Listesi", "#10b981")
        kesin_listesi = [a for a in adaylar if a.asama == "kesin_kayit"]
        toplam_gelir = 0.0
        if kesin_listesi:
            kayit_rows = []
            for a in sorted(kesin_listesi, key=lambda x: x.kapanma_tarihi or "", reverse=True):
                fb = a.fiyat_bilgi or {}
                ucret = float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0)
                toplam_gelir += ucret
                kayit_rows.append({
                    "Ogrenci": a.ogrenci_adi[:25],
                    "Veli": a.veli_adi[:20],
                    "Kademe": f"{a.kademe or '-'} {a.hedef_sinif or ''}",
                    "Ucret": f"{ucret:,.0f} TL",
                    "Kayit Tarihi": (a.kapanma_tarihi or "-")[:10],
                    "Kanal": a.kanal or "-",
                })
            pdf.add_table(_pd.DataFrame(kayit_rows), "#10b981")
            pdf.add_metrics([
                ("Toplam Kayit", len(kesin_listesi), "#10b981"),
                ("Toplam Gelir", f"{toplam_gelir:,.0f} TL", "#059669"),
            ])
        else:
            pdf.add_text("Henuz kesin kayit yok.")

        # ── 8. OLUMSUZ SONUCLANANLAR ──
        olumsuz_listesi = [a for a in adaylar if a.asama == "olumsuz"]
        if olumsuz_listesi:
            pdf.add_section("Olumsuz Sonuclananlar", "#ef4444")
            olm_rows = []
            for a in olumsuz_listesi:
                olm_rows.append({
                    "Ogrenci": a.ogrenci_adi[:25],
                    "Veli": a.veli_adi[:20],
                    "Arama": a.arama_sayisi,
                    "Gorusme": a.gorusme_sayisi,
                    "Son Sonuc": a.son_arama_sonucu[:30] if a.son_arama_sonucu else "-",
                })
            pdf.add_table(_pd.DataFrame(olm_rows), "#ef4444")

        # ── 9. KAMPANYA PERFORMANSI ──
        pdf.add_section("Kampanya Performansi", "#ec4899")
        kamp_sayac = Counter(a.kampanya or "(Bilinmiyor)" for a in adaylar)
        kamp_rows = []
        kamp_data = {}
        for kamp, cnt in kamp_sayac.most_common(10):
            kayit_cnt = sum(1 for a in adaylar if a.kampanya == kamp and a.asama == "kesin_kayit")
            cvr = f"%{kayit_cnt / cnt * 100:.0f}" if cnt > 0 else "%0"
            kamp_rows.append({"Kampanya": kamp, "Aday": cnt, "Kayit": kayit_cnt, "Donusum": cvr})
            kamp_data[kamp[:20]] = cnt
        pdf.add_table(_pd.DataFrame(kamp_rows), "#ec4899")
        if kamp_data:
            pdf.add_donut_chart(kamp_data, "Kampanya Dagilimi")

        # ── 10. KANAL PERFORMANSI ──
        pdf.add_section("Kanal Performansi", "#14b8a6")
        kanal_sayac = Counter(a.kanal or "(Bilinmiyor)" for a in adaylar)
        kanal_rows = []
        kanal_data = {}
        for kanal, cnt in kanal_sayac.most_common(10):
            kayit_cnt = sum(1 for a in adaylar if a.kanal == kanal and a.asama == "kesin_kayit")
            cvr = f"%{kayit_cnt / cnt * 100:.0f}" if cnt > 0 else "%0"
            kanal_rows.append({"Kanal": kanal, "Aday": cnt, "Kayit": kayit_cnt, "Donusum": cvr})
            kanal_data[kanal[:20]] = cnt
        pdf.add_table(_pd.DataFrame(kanal_rows), "#14b8a6")
        if kanal_data:
            pdf.add_donut_chart(kanal_data, "Kanal Dagilimi")

        # ── 11. KADEME DAGILIMI ──
        pdf.add_section("Kademe Dagilimi", "#3b82f6")
        kademe_sayac = Counter(a.kademe or "(Bilinmiyor)" for a in adaylar)
        kademe_rows = []
        kademe_data = {}
        for kademe, cnt in kademe_sayac.most_common():
            kayit_cnt = sum(1 for a in adaylar if a.kademe == kademe and a.asama == "kesin_kayit")
            kademe_rows.append({"Kademe": kademe, "Aday": cnt, "Kayit": kayit_cnt})
            if cnt > 0:
                kademe_data[kademe] = cnt
        pdf.add_table(_pd.DataFrame(kademe_rows), "#3b82f6")
        if kademe_data:
            pdf.add_donut_chart(kademe_data, "Kademe Dagilimi", ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"])

        # ── 12. CINSIYET DAGILIMI ──
        pdf.add_section("Cinsiyet Dagilimi", "#ec4899")
        cinsiyet_sayac = Counter(a.cinsiyet or "(Belirtilmemis)" for a in adaylar)
        cin_rows = []
        cin_data = {}
        for cin, cnt in cinsiyet_sayac.most_common():
            kayit_cnt = sum(1 for a in adaylar if (a.cinsiyet or "(Belirtilmemis)") == cin and a.asama == "kesin_kayit")
            cin_rows.append({"Cinsiyet": cin, "Aday": cnt, "Kayit": kayit_cnt})
            if cnt > 0:
                cin_data[cin] = cnt
        pdf.add_table(_pd.DataFrame(cin_rows), "#ec4899")
        if cin_data:
            pdf.add_donut_chart(cin_data, "Cinsiyet Dagilimi", ["#3b82f6", "#ec4899", "#94a3b8"])

        # ── 13. OKUL TURU DAGILIMI ──
        pdf.add_section("Mevcut Okul Turu Dagilimi", "#f59e0b")
        okul_sayac = Counter(a.okul_turu or "(Belirtilmemis)" for a in adaylar)
        okul_rows = []
        okul_data = {}
        for okul, cnt in okul_sayac.most_common():
            kayit_cnt = sum(1 for a in adaylar if (a.okul_turu or "(Belirtilmemis)") == okul and a.asama == "kesin_kayit")
            okul_rows.append({"Okul Turu": okul, "Aday": cnt, "Kayit": kayit_cnt})
            if cnt > 0:
                okul_data[okul] = cnt
        pdf.add_table(_pd.DataFrame(okul_rows), "#f59e0b")
        if okul_data:
            pdf.add_donut_chart(okul_data, "Okul Turu Dagilimi", ["#f59e0b", "#6366f1", "#94a3b8"])

        # ── 14. DONUSUM HUNISI (FUNNEL) ──
        pdf.add_section("Donusum Hunisi — Aday'dan Kayit'a", "#7c3aed")
        toplam_aday = toplam
        aranan = sum(1 for a in adaylar if a.aramalar)
        cevap_veren = sum(1 for a in adaylar if a.aramalar and any(
            ar.get("sonuc") not in ("Ulasim yok — tekrar aranacak", "Mesaj birakildi", "Telefon yanlis")
            for ar in a.aramalar))
        gorusmeye_gelen = sum(1 for a in adaylar if a.gorusmeler and any(
            gr.get("sonuc") != "Veli gelmedi" for gr in a.gorusmeler))
        fiyat_alan = sum(1 for a in adaylar if a.fiyat_bilgi)
        sozlesme_imza = sum(1 for a in adaylar if a.asama in ("sozlesme", "kesin_kayit"))
        kayit_olan = kesin_cnt

        funnel_items = [
            ("Toplam Aday", toplam_aday),
            ("Aranan", aranan),
            ("Aramaya Cevap Veren", cevap_veren),
            ("Gorusmeye Gelen", gorusmeye_gelen),
            ("Fiyat Alan", fiyat_alan),
            ("Sozlesme Imzalayan", sozlesme_imza),
            ("Kesin Kayit", kayit_olan),
        ]
        funnel_rows = []
        for label, cnt in funnel_items:
            oran = f"%{cnt / toplam_aday * 100:.1f}" if toplam_aday > 0 else "%0"
            onceki_oran = ""
            funnel_rows.append({"Asama": label, "Sayi": cnt, "Oran (Toplama)": oran})
        pdf.add_table(_pd.DataFrame(funnel_rows), "#7c3aed")
        funnel_data = {f"{label} ({cnt})": cnt for label, cnt in funnel_items if cnt > 0}
        if funnel_data:
            pdf.add_donut_chart(funnel_data, "Donusum Hunisi",
                                ["#6366f1", "#f59e0b", "#0ea5e9", "#3b82f6", "#a78bfa", "#38bdf8", "#10b981"])

        # ── 15. SUREC PERFORMANSI ──
        pdf.add_section("Surec Performansi", "#C8952E")
        # Ortalama surec suresi (kesin kayit olanlarin)
        surec_gunleri = []
        for a in kesin_listesi:
            try:
                d1 = date.fromisoformat(a.olusturma_tarihi[:10])
                d2 = date.fromisoformat((a.kapanma_tarihi or a.son_islem_tarihi)[:10])
                surec_gunleri.append((d2 - d1).days)
            except (ValueError, TypeError):
                pass
        ort_surec = sum(surec_gunleri) / len(surec_gunleri) if surec_gunleri else 0
        ort_arama = sum(a.arama_sayisi for a in kesin_listesi) / len(kesin_listesi) if kesin_listesi else 0
        ort_gorusme = sum(a.gorusme_sayisi for a in kesin_listesi) / len(kesin_listesi) if kesin_listesi else 0
        pdf.add_metrics([
            ("Ort. Surec", f"{ort_surec:.0f} gun", "#C8952E"),
            ("Ort. Arama", f"{ort_arama:.1f}", "#f59e0b"),
            ("Ort. Gorusme", f"{ort_gorusme:.1f}", "#0ea5e9"),
        ])

        pdf.add_spacer(0.5)
        pdf.add_text(f"Bu rapor {datetime.now().strftime('%d.%m.%Y %H:%M')} tarihinde SmartCampus AI tarafindan otomatik olusturulmustur.")

        return pdf.generate()
    except Exception:
        return None


# ============================================================
# FIYAT PDF URETICI
# ============================================================

def _generate_fiyat_pdf(aday, tur: str = "tam") -> bytes | None:
    """Fiyat teklifi PDF. tur: 'egitim', 'ek_hizmet', 'tam'"""
    try:
        from utils.report_utils import ReportPDFGenerator
        from utils.shared_data import load_kurum_profili
        import pandas as _pd

        kp = load_kurum_profili()
        k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")

        fb = aday.fiyat_bilgi or {}
        eb = aday.ek_hizmetler or {}

        baslik_map = {
            "egitim": "Egitim Hizmetleri Fiyat Teklifi",
            "ek_hizmet": "Ek Hizmetler Fiyat Teklifi",
            "tam": "Fiyat Teklifi (Tam)",
        }

        pdf = ReportPDFGenerator(baslik_map.get(tur, "Fiyat Teklifi"), k_adi)
        pdf.add_header(k_adi)

        # Aday bilgileri
        pdf.add_section("Aday Bilgileri")
        aday_rows = [
            {"Bilgi": "Veli", "Deger": aday.veli_adi},
            {"Bilgi": "Ogrenci", "Deger": aday.ogrenci_adi},
            {"Bilgi": "Telefon", "Deger": aday.veli_telefon},
            {"Bilgi": "Kademe", "Deger": aday.kademe},
            {"Bilgi": "Tarih", "Deger": fb.get("tarih", "")[:10]},
        ]
        pdf.add_table(_pd.DataFrame(aday_rows))

        # Egitim hizmetleri
        if tur in ("egitim", "tam"):
            pdf.add_section("Egitim Hizmetleri")
            egitim_rows = [
                {"Kalem": "Liste Fiyati", "Tutar": f'{fb.get("liste_fiyati", 0):,.0f} TL'},
                {"Kalem": f'Indirim %{fb.get("toplam_indirim", 0):.0f}', "Tutar": f'-{fb.get("liste_fiyati", 0) * fb.get("toplam_indirim", 0) / 100:,.0f} TL'},
                {"Kalem": f'KDV %{fb.get("kdv_orani", 10):.0f}', "Tutar": f'+{fb.get("kdv_dahil", 0) - fb.get("liste_fiyati", 0) * (1 - fb.get("toplam_indirim", 0) / 100):,.0f} TL'},
                {"Kalem": "KDV Dahil Toplam", "Tutar": f'{fb.get("kdv_dahil", 0):,.0f} TL'},
                {"Kalem": "Pesinat", "Tutar": f'{fb.get("pesinat", 0):,.0f} TL'},
            ]
            pdf.add_table(_pd.DataFrame(egitim_rows))

            # Indirim detay
            ind_text = fb.get("indirim_detay", "")
            if ind_text:
                pdf.add_text(f"Indirim Detay: {ind_text}")

            # Taksit
            taksit_s = fb.get("taksit_sayisi", 0)
            taksit_t = fb.get("taksit_tutari", 0)
            vade = fb.get("aylik_vade_farki", 0)
            if taksit_s:
                vade_text = f" (Aylik vade farki: %{vade:.1f})" if vade > 0 else " (Vade farksiz)"
                pdf.add_text(f"Taksit: {taksit_s} x {taksit_t:,.0f} TL/ay{vade_text}")

        # Ek hizmetler
        if tur in ("ek_hizmet", "tam") and eb and eb.get("toplam", 0) > 0:
            pdf.add_section("Ek Hizmetler")
            ek_rows = []
            _ek_kalemleri = [
                ("kahvalti", "Kahvalti"), ("ogle_yemegi", "Ogle Yemegi"), ("ara_ogun", "Ara Ogun"),
                ("servis", "Servis"), ("kiyafet", "Kiyafet"), ("kitap_kirtasiye", "Kitap-Kirtasiye"),
                ("dijital", "Dijital Kaynaklar"), ("pansiyon", "Pansiyon/Yatili"),
                ("etut_kurs", "Etut/Kurs"), ("spor_sanat", "Spor/Sanat/Bilisim"), ("diger", "Diger"),
            ]
            for key, label in _ek_kalemleri:
                val = eb.get(key, 0)
                if val and val > 0:
                    ek_rows.append({"Hizmet": label, "Tutar (KDV Haric)": f"{val:,.0f} TL"})
            if ek_rows:
                pdf.add_table(_pd.DataFrame(ek_rows))
            pdf.add_text(f"Ek Hizmetler Toplam: {eb.get('toplam', 0):,.0f} TL")
            pdf.add_text(f"KDV: {eb.get('kdv', 0):,.0f} TL")
            pdf.add_text(f"Ek Hizmetler KDV Dahil: {eb.get('kdv_dahil', 0):,.0f} TL")
            ek_pes = eb.get("pesinat", 0)
            if ek_pes > 0:
                pdf.add_text(f"Ek Hizmetler Pesinat: {ek_pes:,.0f} TL")
                pdf.add_text(f"Ek Hizmetler Kalan: {eb.get('kalan', 0):,.0f} TL")

        # Genel toplam (sadece tam modda)
        if tur == "tam":
            pdf.add_section("GENEL TOPLAM")
            toplam_rows = [
                {"Kalem": "Egitim (KDV Dahil)", "Tutar": f'{fb.get("kdv_dahil", 0):,.0f} TL'},
                {"Kalem": "Ek Hizmetler (KDV Dahil)", "Tutar": f'{fb.get("ek_hizmetler_toplam", 0):,.0f} TL'},
                {"Kalem": "Brut Toplam", "Tutar": f'{fb.get("brut_toplam", 0):,.0f} TL'},
                {"Kalem": "Toplam Pesinat", "Tutar": f'{fb.get("toplam_pesinat", 0):,.0f} TL'},
                {"Kalem": "GENEL TOPLAM", "Tutar": f'{fb.get("genel_toplam_final", fb.get("brut_toplam", 0)):,.0f} TL'},
            ]
            pdf.add_table(_pd.DataFrame(toplam_rows))
            taksit_s = fb.get("taksit_sayisi", 0)
            taksit_t = fb.get("taksit_tutari", 0)
            if taksit_s:
                pdf.add_text(f"Odeme Plani: {taksit_s} x {taksit_t:,.0f} TL/ay")

        pdf.add_spacer(0.5)
        pdf.add_text(f"Bu teklif {datetime.now().strftime('%d.%m.%Y')} tarihinde olusturulmustur.")

        return pdf.generate()
    except Exception:
        return b""


# ============================================================
# SOZLESME PDF (MEB FORMATI)
# ============================================================

MEB_GENEL_HUSUSLAR = [
    "Ogrencinin bir sonraki egitim ve ogretim yilinda okulumuzun ara sinifina devam etmek istemesi durumunda; a) Egitim ucreti, yukarida 'Odeme Bilgileri' bolumunde ogrenci icin belirlenen 'Egitim Ucreti' uzerinden en fazla Ozel Ogretim Kurumlari Yonetmeliginin 53'uncu maddesinin birinci fikrasinda yer alan '[(bir onceki yilin Aralik ayi yillik Yurt ici UFE+bir onceki yilin Aralik ayi yillik TUFE)/2]x1,05 oranindan fazla artis yapilamaz.' hukmu kapsaminda artis yapilacaktir.",
    "Kurumumuz, Ozel Ogretim Kurumlari Yonetmeliginin 53'uncu maddesinde yer alan hukum geregi ders kitabi adi altinda hicbir ucret talep etmeyecektir.",
    "Kurumumuz, bir sonraki yilin egitim ucretini ve diger ucretlerini, ocak ayindan itibaren mayis ayinin sonuna kadar ilan eder.",
    "Sosyal ve kulturel faaliyetler, gezi ve gozlem gibi diger etkinlikler icin ucretler, faaliyet oncesi belirlenir.",
    "Kurumumuz ogrenci veya veli/vasilerinden beceri egitimi / staj calismasi / yaz uygulamasi adi altinda ayri bir ucret talep etmeyecektir.",
    "Kurumumuz suresi icinde ucretlerini ilan etmemesi halinde, bir onceki yilin sozlesmesindeki ucretler gecerli olacaktir.",
    "Tum ucretler kurum adina acilan ve valilige bildirilen banka hesabina yatirilarak tahsil edilir. e-Okul sistemine islenir.",
    "Okulumuz, ders yili sonunda ucret odemesi yapmayan ogrencinin kaydini yenilemeyebilir.",
    "Ozel Ogretim Kurumlari Yonetmeliginin 56'nci maddesi hukmlerince; ogretim yili baslamadan ogrencinin ayrılmasi halinde yillik ucretin yuzde onu disindaki kismi iade edilir.",
    "Ucretsiz okuma hakki kazanan ogrencinin bu haklari yalniz o ogretim yili icin gecerli olacaktir. Ancak sehit, gazi ve korunma karari verilen cocuklar okulun ogrenim suresince ucretsiz okutulur.",
    "Yonetmeligin 54'uncu maddesi kapsaminda indirim orani ilan edilen egitim ucretinin %50'sinden fazla olamaz. Kardes indirimi en fazla %25'tir.",
    "Ucretsiz okuma uygun bulunmasi halinde odenen ucret, egitim basladiktan en gec bir ay icerisinde geri odenir.",
    "Kurumumuzdan ayrilan burslu ogrencilerden ogrenim gordugu sure icin ucret talep edilmeyecektir.",
    "Ogrenci kilik ve kiyafetlerine iliskin hususlar MEB Ozel Ogretim Kurumlari Yonetmeliginin 64'uncu maddesi kapsaminda yurutulecektir.",
    "Egitim desteginden faydalanan ogrenci ucretinin Bakanlikca karsilanacak destek disinda kalan bedelini veli/vasi odemekle yukumludur.",
    "Yonetmeligin Ek 2'nci maddesine gore ucretsiz veya %51+ burslu okutulan ogrencinin egitim destegi iptal edilmek uzere Bakanliga bildirilir.",
    "Devam durumu ile ilgili islemler MEB ilgili yonetmelikleri dogrultusunda yurutulur.",
    "Bu sozlesmedeki hususlarin yerine getirilmesi icin veli/vasi tarafindan belirtilen adres yasal ikametgah adresi kabul edilir. Adres degisikligi 15 gun icinde yazili bildirilmelidir.",
]

def _generate_sozlesme_pdf(aday) -> bytes | None:
    """MEB formati sozlesme PDF."""
    try:
        from utils.report_utils import ReportPDFGenerator
        from utils.shared_data import load_kurum_profili
        import pandas as _pd

        kp = load_kurum_profili()
        k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")

        sb = aday.sozlesme_bilgi or {}
        fb = aday.fiyat_bilgi or {}
        eb = aday.ek_hizmetler or {}

        pdf = ReportPDFGenerator("MEB Ogrenci Kayit Sozlesmesi", k_adi)
        pdf.add_header(k_adi)

        # Baslik
        pdf.add_text("T.C. MILLI EGITIM BAKANLIGI")
        pdf.add_text("OZEL OGRETIM KURUMLARI GENEL MUDURLUGU")
        pdf.add_text("OGRENCI KAYIT SOZLESMESI (OZEL OKULLAR ICIN)")
        pdf.add_text(f"Ozel Okul Adi: {k_adi}")
        pdf.add_spacer(0.3)

        # Ogrenci bilgileri
        pdf.add_section("OGRENCININ BILGILERI")
        ogr_rows = [
            {"Alan": "T.C. Kimlik No", "Deger": sb.get("ogrenci_tc", "-")},
            {"Alan": "Adi ve Soyadi", "Deger": sb.get("ogrenci_adi", aday.ogrenci_adi)},
            {"Alan": "Sinifi", "Deger": sb.get("ogrenci_sinif", aday.hedef_sinif or "-")},
            {"Alan": "Okula Kayit Tarihi", "Deger": sb.get("ogrenci_kayit_tarihi", "-")},
            {"Alan": "Ev Adresi", "Deger": sb.get("ogrenci_adres", "-")},
        ]
        pdf.add_table(_pd.DataFrame(ogr_rows))

        # Veli bilgileri
        pdf.add_section("OGRENCININ VELI/VASI BILGILERI")
        veli_rows = [
            {"Alan": "T.C. Kimlik No", "Deger": sb.get("veli_tc", "-")},
            {"Alan": "Adi ve Soyadi", "Deger": sb.get("veli_adi", aday.veli_adi)},
            {"Alan": "Meslegi", "Deger": sb.get("veli_meslek", "-")},
            {"Alan": "Cep Telefonu", "Deger": sb.get("veli_cep", aday.veli_telefon)},
            {"Alan": "Is Telefonu", "Deger": sb.get("veli_is_tel", "-")},
            {"Alan": "e-Posta", "Deger": sb.get("veli_email", aday.veli_email)},
            {"Alan": "Ev Adresi", "Deger": sb.get("veli_ev_adres", "-")},
            {"Alan": "Is Adresi", "Deger": sb.get("veli_is_adres", "-")},
        ]
        pdf.add_table(_pd.DataFrame(veli_rows))

        # Odeme bilgileri
        pdf.add_section(f"ODEME BILGILERI ({sb.get('egitim_yili', '2025-2026')} Egitim Yili)")

        # Ucret kalemleri
        ucret_rows = [
            {"Kalem": "Egitim Ucreti", "Tutar": f'{fb.get("kdv_dahil", 0):,.0f} TL'},
        ]
        # Ek hizmetler
        _ek_map = [("kahvalti", "Kahvalti"), ("ogle_yemegi", "Yemek"), ("servis", "Servis"),
                    ("kiyafet", "Kiyafet"), ("kitap_kirtasiye", "Kitap-Kirtasiye"),
                    ("pansiyon", "Pansiyon/Yatakhane"), ("etut_kurs", "Etut"),
                    ("dijital", "Dijital Kaynaklar"), ("spor_sanat", "Spor/Sanat")]
        for key, label in _ek_map:
            val = eb.get(key, 0)
            if val and val > 0:
                ucret_rows.append({"Kalem": f"* {label}", "Tutar": f"{val:,.0f} TL"})

        ucret_rows.append({"Kalem": "UCRETLER TOPLAMI", "Tutar": f'{fb.get("brut_toplam", fb.get("kdv_dahil", 0)):,.0f} TL'})
        pdf.add_table(_pd.DataFrame(ucret_rows))

        # Odeme sekli
        pdf.add_text(f"Odeme Sekli: {sb.get('odeme_sekli', 'Taksit')}")
        pdf.add_text(f"Pesinat (1. Taksit): {fb.get('toplam_pesinat', fb.get('pesinat', 0)):,.0f} TL")
        pdf.add_text(f"Taksit Sayisi: {fb.get('taksit_sayisi', 0)} x {fb.get('taksit_tutari', 0):,.0f} TL")
        pdf.add_text(f"Odeme Gunu: Her ayin {fb.get('odeme_gunu', '-')}. gunu")

        # Taksit plani varsa
        taksit_plani = fb.get("taksit_plani", [])
        if taksit_plani:
            tp_rows = [{"No": tp["no"], "Tarih": tp["tarih"], "Tip": tp["tip"], "Tutar": f'{tp["tutar"]:,.0f} TL'} for tp in taksit_plani]
            pdf.add_table(_pd.DataFrame(tp_rows))

        # Burs / indirim
        if sb.get("burs_orani", 0) > 0 or sb.get("ucretsiz_okuma", "Yok") != "Yok":
            pdf.add_section("BURS / INDIRIM")
            if sb.get("burs_orani", 0) > 0:
                pdf.add_text(f"Burs Orani: %{sb['burs_orani']}")
            if sb.get("ucretsiz_okuma", "Yok") != "Yok":
                pdf.add_text(f"Ucretsiz Okuma Nedeni: {sb['ucretsiz_okuma']}")
        if fb.get("indirim_detay"):
            pdf.add_text(f"Indirim Detay: {fb['indirim_detay']}")

        # Genel hususlar
        pdf.add_section("GENEL HUSUSLAR")
        for i, husus in enumerate(MEB_GENEL_HUSUSLAR, 1):
            pdf.add_text(f"{i}. {husus}")

        # Ozel hususlar
        if sb.get("ozel_husus_1") or sb.get("ozel_husus_2"):
            pdf.add_section("OZEL HUSUSLAR")
            if sb.get("ozel_husus_1"):
                pdf.add_text(f"1. {sb['ozel_husus_1']}")
            if sb.get("ozel_husus_2"):
                pdf.add_text(f"2. {sb['ozel_husus_2']}")

        # Imza
        pdf.add_spacer(1)
        pdf.add_text(f"Sozlesme Tarihi: {sb.get('sozlesme_tarihi', '-')}")
        pdf.add_text(f"Sozlesme Yeri: {sb.get('sozlesme_yeri', '-')}")
        pdf.add_spacer(0.5)
        pdf.add_text("Ogrenci Veli/Vasi                                              Kurum Temsilcisi")
        pdf.add_text("Adi Soyadi:                                                    Adi Soyadi:")
        pdf.add_text("Imza:                                                          Imza:")

        return pdf.generate()
    except Exception:
        return b""


# ============================================================
# MEB SOZLESME — WORD BELGESININ BIREBIR AYNISI
# ============================================================

# MEB ucret kalemleri (Word belgesindeki sira)
MEB_UCRET_KALEMLERI = [
    ("egitim_ucreti",    "Egitim Ucreti",                                False),
    ("kiyafet",          "Kiyafet Ucreti",                               True),
    ("yemek",            "Yemek Ucreti",                                 True),
    ("kahvalti",         "Kahvalti Ucreti",                              True),
    ("takviye_kursu",    "Takviye Kursu Ucreti",                         True),
    ("yatakhane",        "Yatakhane Ucreti",                             True),
    ("kitap_kirtasiye",  "Kitap-Kirtasiye Ucreti (Ders Kitabi Haric)",   True),
    ("servis",           "Servis Ucreti",                                True),
    ("etut",             "Etut Ucreti",                                  True),
    ("diploma_program",  "Uluslararasi Diploma ve Sertifika Programi",   True),
]


def _render_profil_duzenle(store: KayitDataStore, aday: KayitAday):
    """Veli + Öğrenci profil düzenleme — kayıt sonrası da güncellenebilir."""
    st.markdown(
        '<div style="background:#6366f115;border-left:4px solid #6366f1;border-radius:0 10px 10px 0;'
        'padding:12px 16px;margin-bottom:14px">'
        '<strong style="color:#a5b4fc;font-size:1rem">👤 Veli & Öğrenci Profili</strong><br>'
        '<span style="color:#94a3b8;font-size:.8rem">Profil bilgileri AI analizini güçlendirir — ne kadar detaylı doldurursanız AI o kadar iyi çalışır</span></div>',
        unsafe_allow_html=True)

    vp = aday.veli_profil or {}
    op = aday.ogrenci_profil or {}

    with st.form(f"km_profil_{aday.id}"):
        # ── VELİ PROFİLİ ──
        st.markdown("### 👤 Veli Profili")
        vp1, vp2 = st.columns(2)
        with vp1:
            meslek = st.text_input("Meslek", value=vp.get("meslek", ""), key=f"kp_mes_{aday.id}")
            egitim = st.selectbox("Eğitim Seviyesi",
                                   ["", "İlkokul", "Ortaokul", "Lise", "Üniversite", "Yüksek Lisans/Doktora"],
                                   index=["", "İlkokul", "Ortaokul", "Lise", "Üniversite", "Yüksek Lisans/Doktora"].index(vp.get("egitim", "")) if vp.get("egitim", "") in ["", "İlkokul", "Ortaokul", "Lise", "Üniversite", "Yüksek Lisans/Doktora"] else 0,
                                   key=f"kp_egt_{aday.id}")
            karar = st.selectbox("Karar Verici",
                                  ["", "Anne", "Baba", "İkisi Birlikte", "Büyükanne/Büyükbaba", "Diğer"],
                                  index=["", "Anne", "Baba", "İkisi Birlikte", "Büyükanne/Büyükbaba", "Diğer"].index(vp.get("karar_verici", "")) if vp.get("karar_verici", "") in ["", "Anne", "Baba", "İkisi Birlikte", "Büyükanne/Büyükbaba", "Diğer"] else 0,
                                  key=f"kp_kar_{aday.id}")
            cocuk = st.text_input("Diğer Çocuklar", value=vp.get("diger_cocuklar", ""), key=f"kp_coc_{aday.id}")
            iletisim = st.selectbox("İletişim Tercihi", ["", "Telefon", "WhatsApp", "SMS", "Email"],
                                     key=f"kp_ilt_{aday.id}")
        with vp2:
            neden = st.text_area("Neden Okul Değiştirmek İstiyor?", value=vp.get("neden_degistirmek_istiyor", ""),
                                  key=f"kp_ned_{aday.id}", height=68)
            butce = st.selectbox("Bütçe Beklentisi", ["", "Ekonomik", "Orta", "Yüksek", "Fiyat önemsiz"],
                                  index=["", "Ekonomik", "Orta", "Yüksek", "Fiyat önemsiz"].index(vp.get("butce_beklentisi", "")) if vp.get("butce_beklentisi", "") in ["", "Ekonomik", "Orta", "Yüksek", "Fiyat önemsiz"] else 0,
                                  key=f"kp_but_{aday.id}")
            rakip = st.text_input("Baktığı Diğer Okullar", value=vp.get("rakip_okullar", ""), key=f"kp_rak_{aday.id}")
            zaman = st.selectbox("Ne Zaman Karar Verecek?", ["", "Hemen", "1 Hafta", "1 Ay", "Dönem Sonu", "Belirsiz"],
                                  key=f"kp_zam_{aday.id}")
            duydu = st.text_input("Nasıl Duydu (detay)", value=vp.get("nasil_duydu_detay", ""), key=f"kp_duy_{aday.id}")
        kriter = st.multiselect("Karar Kriterleri", [
            "Akademik başarı", "Öğretmen kalitesi", "Fiziksel ortam", "Ulaşım/servis",
            "Fiyat", "Yabancı dil", "Sosyal etkinlikler", "Spor imkanları",
            "Güvenlik", "Bireysel ilgi", "Teknoloji", "Burs/indirim",
            "Referans/tavsiye", "Okul kültürü", "Üniversiteye hazırlık"
        ], default=vp.get("karar_kriterleri", []), key=f"kp_krt_{aday.id}")

        st.markdown("---")

        # ── ÖĞRENCİ PROFİLİ ──
        st.markdown("### 🎓 Öğrenci Profili")
        op1, op2 = st.columns(2)
        with op1:
            basari = st.selectbox("Akademik Başarı", ["", "Çok Başarılı (90+)", "Başarılı (70-89)", "Orta (50-69)", "Düşük (50 altı)"],
                                   index=["", "Çok Başarılı (90+)", "Başarılı (70-89)", "Orta (50-69)", "Düşük (50 altı)"].index(op.get("akademik_basari", "")) if op.get("akademik_basari", "") in ["", "Çok Başarılı (90+)", "Başarılı (70-89)", "Orta (50-69)", "Düşük (50 altı)"] else 0,
                                   key=f"kp_bas_{aday.id}")
            guclu = st.text_input("Güçlü Dersler", value=op.get("guclu_dersler", ""), key=f"kp_guc_{aday.id}")
            zayif = st.text_input("Zayıf Dersler", value=op.get("zayif_dersler", ""), key=f"kp_zay_{aday.id}")
            davranis = st.selectbox("Davranış Durumu", ["", "Çok İyi", "İyi", "Orta", "Sorunlu"],
                                     key=f"kp_dav_{aday.id}")
            saglik = st.text_input("Sağlık Durumu", value=op.get("saglik_durumu", ""), key=f"kp_sag_{aday.id}")
        with op2:
            ihtiyac = st.selectbox("Özel İhtiyaç", ["", "Yok", "DEHB", "ÖÖG", "Üstün Zeka", "Fiziksel", "Diğer"],
                                    key=f"kp_iht_{aday.id}")
            sosyal = st.selectbox("Sosyal Beceriler", ["", "Çok İyi", "İyi", "Orta", "Zayıf"],
                                   key=f"kp_sos_{aday.id}")
            hobi = st.text_input("Hobiler/İlgi Alanları", value=op.get("hobiler", ""), key=f"kp_hob_{aday.id}")
            memnun = st.selectbox("Önceki Okul Memnuniyeti", ["", "Çok Memnun", "Memnun", "Kısmen", "Memnun Değil"],
                                   key=f"kp_mem_{aday.id}")
            istek = st.text_input("Öğrencinin İsteği", value=op.get("ogrenci_istegi", ""), key=f"kp_ist_{aday.id}")

        if st.form_submit_button("💾 Profili Kaydet", type="primary", use_container_width=True):
            # Veli profil güncelle
            new_vp = {}
            if meslek: new_vp["meslek"] = meslek
            if egitim: new_vp["egitim"] = egitim
            if karar: new_vp["karar_verici"] = karar
            if cocuk: new_vp["diger_cocuklar"] = cocuk
            if neden: new_vp["neden_degistirmek_istiyor"] = neden
            if butce: new_vp["butce_beklentisi"] = butce
            if rakip: new_vp["rakip_okullar"] = rakip
            if zaman: new_vp["karar_zamani"] = zaman
            if kriter: new_vp["karar_kriterleri"] = kriter
            if iletisim: new_vp["iletisim_tercihi"] = iletisim
            if duydu: new_vp["nasil_duydu_detay"] = duydu

            # Öğrenci profil güncelle
            new_op = {}
            if basari: new_op["akademik_basari"] = basari
            if guclu: new_op["guclu_dersler"] = guclu
            if zayif: new_op["zayif_dersler"] = zayif
            if davranis: new_op["davranis_durumu"] = davranis
            if ihtiyac: new_op["ozel_ihtiyac"] = ihtiyac
            if sosyal: new_op["sosyal_beceriler"] = sosyal
            if hobi: new_op["hobiler"] = hobi
            if memnun: new_op["onceki_okul_memnuniyet"] = memnun
            if istek: new_op["ogrenci_istegi"] = istek
            if saglik: new_op["saglik_durumu"] = saglik

            tum = store.load_all()
            for a in tum:
                if a.id == aday.id:
                    a.veli_profil = new_vp
                    a.ogrenci_profil = new_op
                    a.son_islem_tarihi = date.today().isoformat()
                    break
            store.save_all(tum)
            st.success("✅ Profil güncellendi!")
            st.rerun()

    # ── Mevcut profil özeti ──
    if vp or op:
        st.markdown("---")
        st.markdown("### 📋 Mevcut Profil Özeti")
        if vp:
            st.markdown("**👤 Veli:**")
            for k, v in vp.items():
                if v:
                    st.markdown(f"- **{k.replace('_', ' ').title()}:** {v}")
        if op:
            st.markdown("**🎓 Öğrenci:**")
            for k, v in op.items():
                if v:
                    st.markdown(f"- **{k.replace('_', ' ').title()}:** {v}")


def _render_meb_sozlesme(store, aday):
    """MEB Ogrenci Kayit Sozlesmesi — Word belgesinin birebir ekran versiyonu."""
    fb = aday.fiyat_bilgi or {}
    eb = aday.ek_hizmetler or {}
    sb = aday.sozlesme_bilgi or {}

    try:
        from utils.shared_data import load_kurum_profili
        kp = load_kurum_profili()
    except Exception:
        kp = {}
    kurum_adi = kp.get("kurum_adi", kp.get("name", ""))
    kdv_orani = fb.get("kdv_orani", 10)

    # ── BASLIK ──
    st.markdown(
        f'<div style="background:#0c4a6e;border:2px solid #38bdf8;border-radius:12px;'
        f'padding:16px;text-align:center;margin-bottom:14px">'
        f'<div style="color:#7dd3fc;font-size:0.85rem">T.C.</div>'
        f'<div style="color:#e0f2fe;font-weight:800;font-size:1.1rem">MILLI EGITIM BAKANLIGI</div>'
        f'<div style="color:#93c5fd;font-size:0.85rem">OZEL OGRETIM KURUMLARI GENEL MUDURLUGU</div>'
        f'<div style="color:#f1f5f9;font-weight:800;font-size:1.15rem;margin-top:6px">OGRENCI KAYIT SOZLESMESI</div>'
        f'<div style="color:#94a3b8;font-size:0.8rem">(Ozel Okullar Icin)</div>'
        f'<div style="color:#94a3b8;font-size:0.85rem;margin-top:6px">Ozel Okul Adi: <strong style="color:#e2e8f0">{kurum_adi}</strong></div>'
        f'</div>',
        unsafe_allow_html=True)

    with st.form(f"km_meb_sozlesme_{aday.id}"):

        # ── TABLO 1: OGRENCI BILGILERI ──
        st.markdown(
            '<div style="background:#1e40af;color:#fff;padding:8px 12px;border-radius:6px 6px 0 0;font-weight:700">OGRENCININ BILGILERI</div>',
            unsafe_allow_html=True)
        m_oc1, m_oc2 = st.columns(2)
        with m_oc1:
            m_ogr_tc = st.text_input("T.C. Kimlik No / Yabanci Kimlik No", value=sb.get("ogrenci_tc", ""), key=f"meb_otc_{aday.id}", max_chars=11)
            m_ogr_adi = st.text_input("Adi ve Soyadi", value=sb.get("ogrenci_adi", aday.ogrenci_adi), key=f"meb_oad_{aday.id}")
            m_ogr_sinif = st.text_input("Sinifi", value=sb.get("ogrenci_sinif", aday.hedef_sinif or ""), key=f"meb_osn_{aday.id}")
        with m_oc2:
            m_ogr_kayit = st.date_input("Okula Kayit Tarihi", key=f"meb_okt_{aday.id}")
            m_ogr_adres = st.text_area("Ev Adresi", value=sb.get("ogrenci_adres", ""), key=f"meb_oadr_{aday.id}", height=68)

        # ── VELI BILGILERI ──
        st.markdown(
            '<div style="background:#1e40af;color:#fff;padding:8px 12px;border-radius:6px;font-weight:700;margin-top:12px">OGRENCININ VELI/VASI BILGILERI</div>',
            unsafe_allow_html=True)
        m_vc1, m_vc2 = st.columns(2)
        with m_vc1:
            m_veli_tc = st.text_input("T.C. Kimlik No", value=sb.get("veli_tc", ""), key=f"meb_vtc_{aday.id}", max_chars=11)
            m_veli_adi = st.text_input("Adi ve Soyadi", value=sb.get("veli_adi", aday.veli_adi), key=f"meb_vad_{aday.id}")
            m_veli_meslek = st.text_input("Meslegi", value=sb.get("veli_meslek", ""), key=f"meb_vms_{aday.id}")
            m_veli_cep = st.text_input("Cep Telefonu", value=sb.get("veli_cep", aday.veli_telefon), key=f"meb_vcp_{aday.id}")
        with m_vc2:
            m_veli_is_tel = st.text_input("Is Telefonu", value=sb.get("veli_is_tel", ""), key=f"meb_vit_{aday.id}")
            m_veli_email = st.text_input("e-Posta Adresi", value=sb.get("veli_email", aday.veli_email), key=f"meb_vem_{aday.id}")
            m_veli_ev = st.text_area("Ev Adresi", value=sb.get("veli_ev_adres", ""), key=f"meb_vea_{aday.id}", height=50)
            m_veli_is = st.text_area("Is Adresi", value=sb.get("veli_is_adres", ""), key=f"meb_via_{aday.id}", height=50)

        # ── TABLO 2: ODEME BILGILERI ──
        m_egitim_yili = st.text_input("Egitim Yili", value=sb.get("egitim_yili", "2025-2026"), key=f"meb_ey_{aday.id}")
        st.markdown(
            f'<div style="background:#1e40af;color:#fff;padding:8px 12px;border-radius:6px;font-weight:700;margin-top:12px">'
            f'ODEME BILGILERI ({m_egitim_yili} Egitim ve Ogretim Yili Icin)</div>',
            unsafe_allow_html=True)

        # 2 sutun: Kurumun Ilan Ettigi | Ogrenci Icin Belirlenen
        st.markdown(
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0">'
            '<div style="background:#172554;border:1px solid #60a5fa30;border-radius:8px;padding:8px;text-align:center;color:#93c5fd;font-weight:700">Kurumun Ilan Ettigi Ucretler</div>'
            '<div style="background:#2e1065;border:1px solid #a78bfa30;border-radius:8px;padding:8px;text-align:center;color:#c4b5fd;font-weight:700">Ogrenci Icin Belirlenen Ucretler</div></div>',
            unsafe_allow_html=True)

        # Ucret kalemleri
        m_ilan = {}
        m_ogrenci = {}
        for key, label, veli_istegi in MEB_UCRET_KALEMLERI:
            prefix = "* " if veli_istegi else ""
            ic1, ic2 = st.columns(2)
            with ic1:
                m_ilan[key] = st.number_input(f"{prefix}{label} (Ilan)", min_value=0.0, step=100.0,
                                               key=f"meb_il_{key}_{aday.id}", label_visibility="visible")
            with ic2:
                # Ogrenci icin: fiyat bilgisinden otomatik doldur
                default_val = 0.0
                if key == "egitim_ucreti":
                    default_val = float(fb.get("kdv_dahil", 0))
                elif key in eb:
                    default_val = float(eb.get(key, 0))
                m_ogrenci[key] = st.number_input(f"{prefix}{label} (Ogrenci)", min_value=0.0, step=100.0,
                                                  value=default_val, key=f"meb_og_{key}_{aday.id}", label_visibility="visible")

        # Toplam
        ilan_toplam = sum(m_ilan.values())
        ogrenci_toplam = sum(m_ogrenci.values())
        st.markdown(
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0">'
            f'<div style="background:#052e16;border:1px solid #4ade8040;border-radius:8px;padding:10px;text-align:center">'
            f'<span style="color:#94a3b8;font-size:0.8rem">UCRETLER TOPLAMI (Ilan)</span><br>'
            f'<strong style="color:#4ade80;font-size:1.1rem">{ilan_toplam:,.0f} TL</strong></div>'
            f'<div style="background:#052e16;border:1px solid #4ade8040;border-radius:8px;padding:10px;text-align:center">'
            f'<span style="color:#94a3b8;font-size:0.8rem">UCRETLER TOPLAMI (Ogrenci)</span><br>'
            f'<strong style="color:#4ade80;font-size:1.1rem">{ogrenci_toplam:,.0f} TL</strong></div></div>',
            unsafe_allow_html=True)

        # Odeme sekli + taksit
        st.markdown("---")
        m_odeme = st.selectbox("Odeme Sekli", ["Pesin", "Taksit"], index=1, key=f"meb_os_{aday.id}")
        mc1, mc2 = st.columns(2)
        with mc1:
            m_taksit_baslangic = st.date_input("Taksit Baslangic Tarihi", key=f"meb_tb_{aday.id}")
            m_pesinat = st.number_input("Pesinat (TL)", min_value=0.0, step=500.0,
                                         value=float(fb.get("toplam_pesinat", fb.get("pesinat", 0))),
                                         key=f"meb_pes_{aday.id}")
        with mc2:
            m_taksit_bitis = st.date_input("Taksit Bitis Tarihi", key=f"meb_tbt_{aday.id}")
            m_taksit_sayisi = st.number_input("Taksit Sayisi", min_value=1, max_value=12,
                                               value=int(fb.get("taksit_sayisi", 9)),
                                               key=f"meb_ts_{aday.id}")
        m_taksit_tutari = (ogrenci_toplam - m_pesinat) / m_taksit_sayisi if m_taksit_sayisi > 0 else 0
        st.markdown(
            f'<div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:8px;margin:6px 0;'
            f'color:#e2e8f0;font-size:0.85rem;text-align:center">'
            f'Taksit: {m_taksit_sayisi} x <strong>{m_taksit_tutari:,.0f} TL</strong></div>',
            unsafe_allow_html=True)

        # Burs
        st.markdown("---")
        m_burs_var = st.checkbox("Burs Aliyor Mu?", key=f"meb_bv_{aday.id}")
        m_burs_oran = 0.0
        if m_burs_var:
            m_burs_oran = st.number_input("Burs Orani (%)", min_value=0.0, max_value=100.0, key=f"meb_bo_{aday.id}")

        # Indirim
        m_indirim_var = st.checkbox("Egitim Ucretinde Indirim Yapildi Mi?", value=bool(fb.get("toplam_indirim", 0) > 0), key=f"meb_iv_{aday.id}")
        m_indirim_oran = 0.0
        m_ind_kardes = 0.0
        m_ind_personel = 0.0
        m_ind_basari = 0.0
        m_ind_sehit = 0.0
        m_ind_diger_text = ""
        if m_indirim_var:
            m_indirim_oran = st.number_input("Toplam Indirim Orani (%)", min_value=0.0, max_value=50.0,
                                              value=float(fb.get("toplam_indirim", 0)), key=f"meb_io_{aday.id}")
            st.markdown('<div style="color:#94a3b8;font-size:0.85rem;margin:4px 0">Indirim Nedeni:</div>', unsafe_allow_html=True)
            mi1, mi2 = st.columns(2)
            with mi1:
                m_ind_kardes = st.number_input("Kardes Indirimi (%)", min_value=0.0, max_value=100.0,
                                                value=float(fb.get("ind_kardes", 0)), key=f"meb_ik_{aday.id}")
                m_ind_basari = st.number_input("Basari Indirimi (%)", min_value=0.0, max_value=50.0,
                                                value=float(fb.get("ind_bursluluk", 0)), key=f"meb_iba_{aday.id}")
            with mi2:
                m_ind_personel = st.number_input("Personel Cocugu Indirimi (%)", min_value=0.0, max_value=50.0, key=f"meb_ip_{aday.id}")
                m_ind_sehit = st.number_input("Sehit/Gazi Cocugu Indirimi (%)", min_value=0.0, max_value=100.0, key=f"meb_is_{aday.id}")
            m_ind_diger_text = st.text_input("Diger Indirimler", value=fb.get("indirim_detay", ""), key=f"meb_idt_{aday.id}")

        # Ucretsiz okuma
        m_ucretsiz = st.selectbox("Ucretsiz Okuma Nedeni",
                                   ["Yok", "Sehit/Gazi Cocugu", "2828/5395 Sayili Kanunlara Tabi", "Diger"],
                                   key=f"meb_un_{aday.id}")

        # Ozel hususlar
        st.markdown("---")
        st.markdown('<div style="color:#e2e8f0;font-weight:700;margin:8px 0">OZEL HUSUSLAR</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#94a3b8;font-size:0.8rem;margin-bottom:6px">(Yururlukteki mevzuata aykiri olmamak kaydiyla)</div>', unsafe_allow_html=True)
        m_ozel1 = st.text_input("1.", value=sb.get("ozel_husus_1", ""), key=f"meb_oh1_{aday.id}")
        m_ozel2 = st.text_input("2.", value=sb.get("ozel_husus_2", ""), key=f"meb_oh2_{aday.id}")

        # Tarih + imza
        st.markdown("---")
        mc_t1, mc_t2 = st.columns(2)
        with mc_t1:
            m_sozlesme_tarihi = st.date_input("Sozlesme Tarihi", key=f"meb_st_{aday.id}")
        with mc_t2:
            st.markdown(
                '<div style="color:#94a3b8;font-size:0.85rem;margin-top:30px">'
                'Ogrenci Veli/Vasi &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Kurumun Temsilcisi</div>',
                unsafe_allow_html=True)

        # Butonlar
        st.markdown("---")
        mb1, mb2, mb3 = st.columns(3)
        with mb1:
            meb_kaydet = st.form_submit_button("💾 MEB Sozlesme Kaydet", use_container_width=True)
        with mb2:
            meb_kesin = st.form_submit_button("✅ Kesin Kayit", type="primary", use_container_width=True)
        with mb3:
            meb_taslak = st.form_submit_button("📝 Taslak", use_container_width=True)

        _meb_data = {
            "meb_format": True,
            "sozlesme_tarihi": str(m_sozlesme_tarihi),
            "egitim_yili": m_egitim_yili,
            "ogrenci_tc": m_ogr_tc, "ogrenci_adi": m_ogr_adi,
            "ogrenci_sinif": m_ogr_sinif, "ogrenci_kayit_tarihi": str(m_ogr_kayit),
            "ogrenci_adres": m_ogr_adres,
            "veli_tc": m_veli_tc, "veli_adi": m_veli_adi,
            "veli_meslek": m_veli_meslek, "veli_cep": m_veli_cep,
            "veli_is_tel": m_veli_is_tel, "veli_email": m_veli_email,
            "veli_ev_adres": m_veli_ev, "veli_is_adres": m_veli_is,
            "ilan_ucretler": m_ilan, "ogrenci_ucretler": m_ogrenci,
            "ilan_toplam": ilan_toplam, "ogrenci_toplam": ogrenci_toplam,
            "odeme_sekli": m_odeme, "pesinat": m_pesinat,
            "taksit_baslangic": str(m_taksit_baslangic), "taksit_bitis": str(m_taksit_bitis),
            "taksit_sayisi": m_taksit_sayisi, "taksit_tutari": m_taksit_tutari,
            "burs_orani": m_burs_oran,
            "indirim_toplam": m_indirim_oran,
            "ind_kardes": m_ind_kardes, "ind_personel": m_ind_personel,
            "ind_basari": m_ind_basari, "ind_sehit": m_ind_sehit,
            "ind_diger": m_ind_diger_text,
            "ucretsiz_okuma": m_ucretsiz,
            "ozel_husus_1": m_ozel1, "ozel_husus_2": m_ozel2,
            "toplam_ucret": ogrenci_toplam,
            "tarih": datetime.now().isoformat(),
        }

        if meb_kaydet:
            sozlesme_kaydet(store, aday.id, _meb_data)
            st.success("MEB Sozlesme kaydedildi!")
            st.rerun()
        if meb_kesin:
            _meb_data["kayit_sonucu"] = "Kesin Kayit"
            sozlesme_kaydet(store, aday.id, _meb_data)
            kesin_kayit_yap(store, aday.id)
            st.session_state[f"_km_sonuc_{aday.id}"] = {
                "tip": "kesin_kayit", "no": 0, "sonuc": "Kesin Kayıt Tamamlandı! (MEB Sözleşme)",
                "not": "MEB sözleşme imzalandı.",
                "mesaj": "Hoş geldin süreci otomatik başlatılıyor...",
                "aday_label": aday.label, "tarih": date.today().isoformat(), "takip": "",
            }
            try:
                from models.kayit_ai_engine import ai_hosgeldin_sureci
                hg = ai_hosgeldin_sureci(aday)
                if hg:
                    st.session_state[f"_km_hg_{aday.id}"] = hg
            except Exception:
                pass
            st.balloons()
            st.rerun()
        if meb_taslak:
            _meb_data["kayit_sonucu"] = "Taslak"
            sozlesme_kaydet(store, aday.id, _meb_data)
            st.success("Taslak kaydedildi.")
            st.rerun()

    # PDF indir
    if aday.sozlesme_bilgi and aday.sozlesme_bilgi.get("meb_format"):
        st.markdown("---")
        _pdf_meb = _generate_meb_sozlesme_pdf(aday)
        if _pdf_meb:
            st.download_button("📄 MEB Sozlesme PDF Indir", data=_pdf_meb,
                               file_name=f"MEB_Sozlesme_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                               mime="application/pdf", key=f"km_meb_pdf_{aday.id}", use_container_width=True)


def _generate_meb_sozlesme_pdf(aday) -> bytes | None:
    """MEB Ogrenci Kayit Sozlesmesi — Word belgesinin birebir resmi evrak PDF'i."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm, mm
        from reportlab.lib.colors import HexColor, black, white
        from reportlab.pdfgen import canvas
        import io

        from utils.shared_data import load_kurum_profili
        kp = load_kurum_profili()
        k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")
        sb = aday.sozlesme_bilgi or {}
        fb = aday.fiyat_bilgi or {}

        buf = io.BytesIO()
        w, h = A4
        c = canvas.Canvas(buf, pagesize=A4)
        margin_l = 2 * cm
        margin_r = 1.3 * cm
        pw = w - margin_l - margin_r

        # Font — Times New Roman (resmi evrak)
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os as _os
            _win_fonts = _os.path.join(_os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
            _tnr = _os.path.join(_win_fonts, "times.ttf")
            _tnrb = _os.path.join(_win_fonts, "timesbd.ttf")
            if _os.path.exists(_tnr):
                pdfmetrics.registerFont(TTFont("TNR", _tnr))
                pdfmetrics.registerFont(TTFont("TNRB", _tnrb))
                font = "TNR"
                fontB = "TNRB"
            else:
                font = "Helvetica"
                fontB = "Helvetica-Bold"
        except Exception:
            font = "Helvetica"
            fontB = "Helvetica-Bold"

        page_num = [1]

        def safe(v):
            if v is None: return "-"
            s = str(v).strip()
            return s if s else "-"

        def _footer():
            c.saveState()
            c.setStrokeColor(HexColor("#cccccc"))
            c.setLineWidth(0.3)
            c.line(margin_l, 1.5*cm, w-margin, 1.5*cm)
            c.setFont(font, 6)
            c.setFillColor(HexColor("#999999"))
            c.drawString(margin_l, 1.0*cm, f"MEB Ozel Ogretim Kurumlari Yonetmeligi kapsaminda duzenlenmistir. | {k_adi}")
            c.drawRightString(w-margin_r, 1.0*cm, f"Sayfa {page_num[0]}")
            c.restoreState()

        def new_page():
            _footer()
            c.showPage()
            page_num[0] += 1
            return h - 2*cm

        def check(y, need=1*cm):
            if y < need + 2*cm:
                return new_page()
            return y

        def draw_cell(x, y, width, height, text, bold=False, bg=None, align="left", fsize=7.5):
            if bg:
                c.setFillColor(bg)
                c.rect(x, y, width, height, fill=True, stroke=0)
            c.setStrokeColor(HexColor("#333333"))
            c.setLineWidth(0.4)
            c.rect(x, y, width, height, fill=False, stroke=True)
            c.setFillColor(black if not bg else (white if bg != HexColor("#f0f0f0") else black))
            c.setFont(fontB if bold else font, fsize)
            tx = x + 2*mm
            if align == "center":
                tx = x + width/2
                c.drawCentredString(tx, y + height/2 - fsize/3, safe(text)[:50])
            elif align == "right":
                c.drawRightString(x + width - 3*mm, y + height/2 - fsize/3, safe(text)[:50])
            else:
                c.drawString(tx, y + height/2 - fsize/3, safe(text)[:50])

        y = h - 2*cm

        # ═══════════════ BASLIK ═══════════════
        c.setFont(fontB, 9)
        c.drawCentredString(w/2, y, "T.C.")
        y -= 0.4*cm
        c.setFont(fontB, 11)
        c.drawCentredString(w/2, y, "MILLI EGITIM BAKANLIGI")
        y -= 0.45*cm
        c.setFont(font, 9)
        c.drawCentredString(w/2, y, "OZEL OGRETIM KURUMLARI GENEL MUDURLUGU")
        y -= 0.45*cm
        c.setFont(fontB, 12)
        c.drawCentredString(w/2, y, "OGRENCI KAYIT SOZLESMESI")
        y -= 0.4*cm
        c.setFont(font, 8)
        c.drawCentredString(w/2, y, "(Ozel Okullar Icin)")
        y -= 0.6*cm
        c.setFont(font, 9)
        c.drawString(margin_l, y, f"Ozel Okul Adi: {k_adi}")
        y -= 0.8*cm

        # ═══════════════ TABLO 1: OGRENCI + VELI ═══════════════
        rh = 0.55*cm  # row height
        lw = 5.5*cm   # label width
        vw = pw - lw  # value width

        # Ogrenci basligi
        draw_cell(margin_l, y-rh, pw, rh, "OGRENCININ BILGILERI", bold=True, bg=HexColor("#d0d0d0"), align="center")
        y -= rh

        ogr_fields = [
            ("T.C. Kimlik No / Yabanci Kimlik No", sb.get("ogrenci_tc")),
            ("Adi ve Soyadi", sb.get("ogrenci_adi", aday.ogrenci_adi)),
            ("Sinifi", sb.get("ogrenci_sinif")),
            ("Okula Kayit Tarihi", sb.get("ogrenci_kayit_tarihi")),
            ("Ev Adresi", sb.get("ogrenci_adres")),
        ]
        for label, val in ogr_fields:
            y = check(y)
            draw_cell(margin_l, y-rh, lw, rh, label, bold=True)
            draw_cell(margin_l+lw, y-rh, vw, rh, val)
            y -= rh

        y -= 0.3*cm

        # Veli basligi
        y = check(y, 2*cm)
        draw_cell(margin_l, y-rh, pw, rh, "OGRENCININ VELI/VASI BILGILERI", bold=True, bg=HexColor("#d0d0d0"), align="center")
        y -= rh

        veli_fields = [
            ("T.C. Kimlik No / Yabanci Kimlik No", sb.get("veli_tc")),
            ("Adi ve Soyadi", sb.get("veli_adi", aday.veli_adi)),
            ("Meslegi", sb.get("veli_meslek")),
            ("Cep Telefonu", sb.get("veli_cep", aday.veli_telefon)),
            ("Is Telefonu", sb.get("veli_is_tel")),
            ("e-Posta Adresi", sb.get("veli_email")),
            ("Ev Adresi", sb.get("veli_ev_adres")),
            ("Is Adresi", sb.get("veli_is_adres")),
        ]
        for label, val in veli_fields:
            y = check(y)
            draw_cell(margin_l, y-rh, lw, rh, label, bold=True)
            draw_cell(margin_l+lw, y-rh, vw, rh, val)
            y -= rh

        y -= 0.5*cm

        # ═══════════════ TABLO 2: ODEME BILGILERI ═══════════════
        y = check(y, 3*cm)
        ey = sb.get("egitim_yili", "2025-2026")
        draw_cell(margin_l, y-rh, pw, rh, f"ODEME BILGILERI ({ey} Egitim ve Ogretim Yili Icin)", bold=True, bg=HexColor("#c0c0c0"), align="center")
        y -= rh

        # 7 sutunlu ucret tablosu (Word birebir)
        # Sutunlar: Kalem | Ilan Ucret | Ilan KDV% | Ilan Ucret+KDV | Ogr Ucret | Ogr KDV% | Ogr Ucret+KDV
        ck = 4.5*cm    # kalem
        cu = 2.0*cm    # ucret
        cv = 1.2*cm    # kdv orani
        ct = 2.3*cm    # ucret+kdv
        # Ilan grubu = cu + cv + ct = 5.5cm | Ogrenci grubu = cu + cv + ct = 5.5cm | Toplam = ck + 5.5 + 5.5 = 15.5
        # pw ~17cm, kalan bosluk kalem genisligine eklenir
        _kalan = pw - (cu*2 + cv*2 + ct*2)
        ck = _kalan  # kalem otomatik

        kdv_oran = fb.get("kdv_orani", 10)

        # Baslik satiri 1: bos | Kurumun Ilan | Ogrenci Icin
        ilan_w = cu + cv + ct
        ogr_w = cu + cv + ct
        draw_cell(margin_l, y-rh, ck, rh, "", bg=HexColor("#e0e0e0"))
        draw_cell(margin_l+ck, y-rh, ilan_w, rh, "Kurumun Ilan Ettigi Ucretler", bold=True, bg=HexColor("#e0e0e0"), align="center", fsize=7)
        draw_cell(margin_l+ck+ilan_w, y-rh, ogr_w, rh, "Ogrenci Icin Belirlenen Ucretler", bold=True, bg=HexColor("#e0e0e0"), align="center", fsize=7)
        y -= rh

        # Baslik satiri 2: bos | Ucret | KDV% | Ucret+KDV | Ucret | KDV% | Ucret+KDV
        draw_cell(margin_l, y-rh, ck, rh, "", bg=HexColor("#f0f0f0"))
        x0 = margin_l + ck
        for lbl, cw in [("Ucret", cu), ("KDV %", cv), ("Ucret+KDV", ct), ("Ucret", cu), ("KDV %", cv), ("Ucret+KDV", ct)]:
            draw_cell(x0, y-rh, cw, rh, lbl, bold=True, bg=HexColor("#f0f0f0"), align="center", fsize=6)
            x0 += cw
        y -= rh

        # Ucret kalemleri
        ilan_ucr = sb.get("ilan_ucretler", {})
        ogr_ucr = sb.get("ogrenci_ucretler", {})

        for key, label, veli in MEB_UCRET_KALEMLERI:
            y = check(y)
            prefix = "* " if veli else ""
            draw_cell(margin_l, y-rh, ck, rh, f"{prefix}{label}", fsize=6.5)
            iv = float(ilan_ucr.get(key, 0) or 0)
            ov = float(ogr_ucr.get(key, 0) or 0)
            iv_kdv = iv * kdv_oran / 100
            ov_kdv = ov * kdv_oran / 100
            x0 = margin_l + ck
            # Ilan: ucret | kdv% | ucret+kdv
            draw_cell(x0, y-rh, cu, rh, f"{iv:,.0f}" if iv else "", align="right", fsize=6.5); x0 += cu
            draw_cell(x0, y-rh, cv, rh, f"%{kdv_oran:.0f}" if iv else "", align="center", fsize=6.5); x0 += cv
            draw_cell(x0, y-rh, ct, rh, f"{iv + iv_kdv:,.0f}" if iv else "", align="right", fsize=6.5); x0 += ct
            # Ogrenci: ucret | kdv% | ucret+kdv
            draw_cell(x0, y-rh, cu, rh, f"{ov:,.0f}" if ov else "", align="right", fsize=6.5); x0 += cu
            draw_cell(x0, y-rh, cv, rh, f"%{kdv_oran:.0f}" if ov else "", align="center", fsize=6.5); x0 += cv
            draw_cell(x0, y-rh, ct, rh, f"{ov + ov_kdv:,.0f}" if ov else "", align="right", fsize=6.5)
            y -= rh

        # Toplam
        y = check(y)
        ilan_top = float(sb.get("ilan_toplam", 0) or 0)
        ogr_top = float(sb.get("ogrenci_toplam", 0) or 0)
        draw_cell(margin_l, y-rh, ck, rh, "UCRETLER TOPLAMI", bold=True, bg=HexColor("#d4edda"), fsize=7)
        x0 = margin_l + ck
        draw_cell(x0, y-rh, cu, rh, f"{ilan_top:,.0f}", bold=True, bg=HexColor("#d4edda"), align="right", fsize=7); x0 += cu
        draw_cell(x0, y-rh, cv, rh, f"%{kdv_oran:.0f}", bold=True, bg=HexColor("#d4edda"), align="center", fsize=7); x0 += cv
        draw_cell(x0, y-rh, ct, rh, f"{ilan_top*(1+kdv_oran/100):,.0f}", bold=True, bg=HexColor("#d4edda"), align="right", fsize=7); x0 += ct
        draw_cell(x0, y-rh, cu, rh, f"{ogr_top:,.0f}", bold=True, bg=HexColor("#d4edda"), align="right", fsize=7); x0 += cu
        draw_cell(x0, y-rh, cv, rh, f"%{kdv_oran:.0f}", bold=True, bg=HexColor("#d4edda"), align="center", fsize=7); x0 += cv
        draw_cell(x0, y-rh, ct, rh, f"{ogr_top*(1+kdv_oran/100):,.0f}", bold=True, bg=HexColor("#d4edda"), align="right", fsize=7)
        y -= rh

        # Odeme sekli
        y = check(y)
        _pesin_check = "(X)" if sb.get("odeme_sekli") == "Pesin" else "(  )"
        _taksit_check = "(X)" if sb.get("odeme_sekli") == "Taksit" else "(  )"
        draw_cell(margin_l, y-rh, ck, rh, "Odeme Sekli", bold=True)
        draw_cell(margin_l+ck, y-rh, pw-ck, rh, f"{_pesin_check} Pesin          {_taksit_check} Taksit")
        y -= rh

        # Taksit tarihleri
        y = check(y)
        draw_cell(margin_l, y-rh, ck, rh, "Taksit Baslangic/Bitis", bold=True)
        draw_cell(margin_l+ck, y-rh, pw-ck, rh, f'{sb.get("taksit_baslangic", "-")}  —  {sb.get("taksit_bitis", "-")}')
        y -= rh

        # Pesinat
        y = check(y)
        draw_cell(margin_l, y-rh, ck, rh, "Pesinat", bold=True)
        draw_cell(margin_l+ck, y-rh, pw-ck, rh, f'{sb.get("pesinat", 0):,.0f} TL')
        y -= rh

        # Taksit sayisi
        y = check(y)
        draw_cell(margin_l, y-rh, ck, rh, "Taksit Sayisi ve Tutari", bold=True)
        draw_cell(margin_l+ck, y-rh, pw-ck, rh, f'{sb.get("taksit_sayisi", 0)} x {sb.get("taksit_tutari", 0):,.0f} TL')
        y -= rh

        # Burs
        y = check(y)
        burs_text = f"(X) Evet — burs orani %{sb.get('burs_orani', 0)}" if sb.get("burs_orani", 0) > 0 else "(  ) Evet       (X) Hayir"
        draw_cell(margin_l, y-rh, ck, rh, "Burs Aliyor Mu?", bold=True)
        draw_cell(margin_l+ck, y-rh, pw-ck, rh, burs_text)
        y -= rh

        # Indirim
        y = check(y)
        ind_t = sb.get("indirim_toplam", 0)
        ind_text = f"(X) Evet — toplam indirim orani %{ind_t}" if ind_t > 0 else "(  ) Evet       (X) Hayir"
        draw_cell(margin_l, y-rh, ck, rh, "Indirim Yapildi Mi?", bold=True)
        draw_cell(margin_l+ck, y-rh, pw-ck, rh, ind_text)
        y -= rh

        # Indirim nedeni — Word formatinda ayri satirlar
        if ind_t > 0:
            # Satir 1: Kardes | Personel
            y = check(y)
            half_w = (pw - ck) / 2
            draw_cell(margin_l, y-rh, ck, rh, "Indirim Nedeni", bold=True)
            _ik = sb.get("ind_kardes", 0)
            _ip = sb.get("ind_personel", 0)
            draw_cell(margin_l+ck, y-rh, half_w, rh,
                      f"({'X' if _ik else '  '}) Kardes Indirimi %{_ik:.0f}" if _ik else "(  ) Kardes Indirimi %...", fsize=6.5)
            draw_cell(margin_l+ck+half_w, y-rh, half_w, rh,
                      f"({'X' if _ip else '  '}) Personel Cocugu Indirimi %{_ip:.0f}" if _ip else "(  ) Personel Cocugu %...", fsize=6.5)
            y -= rh
            # Satir 2: Basari | Sehit/Gazi
            y = check(y)
            _iba = sb.get("ind_basari", 0)
            _is = sb.get("ind_sehit", 0)
            draw_cell(margin_l, y-rh, ck, rh, "", bold=True)
            draw_cell(margin_l+ck, y-rh, half_w, rh,
                      f"({'X' if _iba else '  '}) Basari Indirimi %{_iba:.0f}" if _iba else "(  ) Basari Indirimi %...", fsize=6.5)
            draw_cell(margin_l+ck+half_w, y-rh, half_w, rh,
                      f"({'X' if _is else '  '}) Sehit/Gazi Cocugu %{_is:.0f}" if _is else "(  ) Sehit/Gazi Cocugu %...", fsize=6.5)
            y -= rh
            # Satir 3: Diger indirimler
            y = check(y)
            _id_text = sb.get("ind_diger", "")
            draw_cell(margin_l, y-rh, ck, rh, "Diger Indirimler", bold=True)
            draw_cell(margin_l+ck, y-rh, pw-ck, rh, _id_text if _id_text else "(1)          (2)          ...", fsize=6.5)
            y -= rh

        # Ucretsiz okuma
        y = check(y)
        ucr_neden = sb.get("ucretsiz_okuma", "Yok")
        draw_cell(margin_l, y-rh, ck, rh, "Ucretsiz Okuma Nedeni", bold=True)
        draw_cell(margin_l+ck, y-rh, pw-ck, rh, ucr_neden if ucr_neden != "Yok" else "-")
        y -= rh

        y -= 0.5*cm

        # ═══════════════ DIPNOT ═══════════════
        y = check(y, 1*cm)
        c.setFont(font, 6)
        c.setFillColor(HexColor("#666666"))
        c.drawString(margin_l, y, "*MEB Ozel Ogretim Kurumlari Yonetmeliginin 53. maddesinin 5. fikrasinda yer alan hukum geregi.")
        y -= 0.3*cm
        c.drawString(margin_l, y, "**Kanunun 13. maddesinde belirtilen (sehit, gazi, korunma/bakim karari verilen cocuklar) disinda ucretsiz okutulan ogrenci burs orani %100'dur.")
        y -= 0.6*cm

        # ═══════════════ GENEL HUSUSLAR ═══════════════
        y = check(y, 2*cm)
        c.setFont(fontB, 11)
        c.setFillColor(black)
        c.drawCentredString(w/2, y, "GENEL HUSUSLAR")
        y -= 0.6*cm

        c.setFont(font, 7)
        c.setFillColor(HexColor("#222222"))
        for i, husus in enumerate(MEB_GENEL_HUSUSLAR, 1):
            y = check(y, 0.8*cm)
            # Numarayi bold yaz
            c.setFont(fontB, 7)
            c.drawString(margin_l, y, f"{i}.")
            c.setFont(font, 7)
            # Metni satirlara bol
            text = husus
            max_chars = 110
            x_start = margin + 0.5*cm
            while text:
                line = text[:max_chars]
                # Kelime bolunmesini onle
                if len(text) > max_chars:
                    last_space = line.rfind(" ")
                    if last_space > 60:
                        line = text[:last_space]
                c.drawString(x_start, y, line)
                text = text[len(line):].strip()
                y -= 0.32*cm
                y = check(y, 0.5*cm)
            y -= 0.15*cm

        # ═══════════════ OZEL HUSUSLAR ═══════════════
        y = check(y, 2*cm)
        c.setFont(fontB, 10)
        c.drawString(margin_l, y, "Ozel Hususlar")
        y -= 0.35*cm
        c.setFont(font, 7)
        c.setFillColor(HexColor("#666666"))
        c.drawString(margin_l, y, "(Yururlukteki mevzuata ve bu sozlesmede yer alan sartlara aykiri olmamak kaydiyla ozel sartlar belirlenebilir)")
        y -= 0.5*cm
        c.setFillColor(black)
        c.setFont(font, 8)
        oh1 = sb.get("ozel_husus_1", "")
        oh2 = sb.get("ozel_husus_2", "")
        c.drawString(margin_l, y, f"1. {oh1}" if oh1 else "1. ............................................................................................................................")
        y -= 0.4*cm
        c.drawString(margin_l, y, f"2. {oh2}" if oh2 else "2. ............................................................................................................................")
        y -= 0.4*cm
        c.drawString(margin_l, y, "3. ............................................................................................................................")
        y -= 1*cm

        # ═══════════════ TARIH + IMZA ═══════════════
        y = check(y, 2.5*cm)
        # Tarih sag ust
        c.setFont(font, 9)
        sozl_tarih = sb.get("sozlesme_tarihi", "-")
        c.drawRightString(w-margin_r, y, f"... / ... / 202...     ({sozl_tarih})")
        y -= 1.2*cm

        # Imza alanlari
        c.setFont(font, 9)
        sol_x = margin + 1*cm
        sag_x = w - margin - 6*cm

        c.drawString(sol_x, y, "Ogrenci Veli/Vasi")
        c.drawString(sag_x, y, "Kurumun Temsilcisi")
        y -= 0.5*cm
        c.drawString(sol_x, y, "Adi Soyadi: ........................")
        c.drawString(sag_x, y, "Adi Soyadi: ........................")
        y -= 0.5*cm
        c.drawString(sol_x, y, "Imza:")
        c.drawString(sag_x, y, "Imza:")

        _footer()
        c.save()
        buf.seek(0)
        return buf.read()
    except Exception:
        return b""


# ============================================================
# TESTLER SEKMESI
# ============================================================

def _aday_secici(adaylar: list[KayitAday], prefix: str) -> KayitAday | None:
    """Ortak aday secici — aktif adaylar listesi."""
    aktif = [a for a in adaylar if a.aktif]
    if not aktif:
        styled_info_banner("Aktif aday yok.", "info")
        return None
    options = ["-- Aday Sec --"] + [
        f"{a.pipeline_info['emoji']} {a.label} [{a.pipeline_info['label']}]" for a in aktif
    ]
    sec = st.selectbox("Aday", options, key=f"{prefix}_aday_sec")
    if sec == "-- Aday Sec --":
        return None
    idx = options.index(sec) - 1
    return aktif[idx]


def _render_testler(store: KayitDataStore, adaylar: list[KayitAday]):
    st.markdown(
        '<div style="background:#6366f115;border-left:4px solid #6366f1;border-radius:0 10px 10px 0;'
        'padding:12px 16px;margin-bottom:14px">'
        '<strong style="color:#a5b4fc;font-size:1rem">🧪 Test Uygula + Sonuc Kaydet + PDF Rapor</strong></div>',
        unsafe_allow_html=True)

    aday = _aday_secici(adaylar, "test")
    if not aday:
        st.info("Test uygulamak icin bir aday secin.")
        return

    # Mevcut testler
    if aday.testler:
        st.markdown(
            f'<div style="color:#a5b4fc;font-weight:700;margin:8px 0">Uygulanan Testler ({len(aday.testler)})</div>',
            unsafe_allow_html=True)
        for ti, test in enumerate(aday.testler):
            clrs = ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd"]
            clr = clrs[ti % len(clrs)]
            skorlar = test.get("skorlar", {})
            skor_text = ""
            if skorlar:
                top3 = sorted(skorlar.items(), key=lambda x: x[1], reverse=True)[:3]
                skor_text = " | ".join(f"{k}: {v}/10" for k, v in top3)
            st.markdown(
                f'<div style="padding:8px 12px;margin:4px 0;'
                f'background:{clr}12;border:1px solid {clr}30;border-radius:8px;border-left:3px solid {clr}">'
                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'<span style="font-weight:700;color:{clr}">🧪 {test.get("test_adi", "-")}</span>'
                f'<span style="font-size:0.8rem;color:#94a3b8">{str(test.get("tarih", ""))[:10]}</span></div>'
                f'{f"<div style=\'font-size:0.8rem;color:#94a3b8;margin-top:4px\'>Top 3: {skor_text}</div>" if skor_text else ""}'
                f'{"<div style=\'font-size:0.8rem;color:#64748b;margin-top:2px\'>Not: " + str(test.get("notlar", ""))[:80] + "</div>" if test.get("notlar") else ""}'
                f'</div>',
                unsafe_allow_html=True)

    # AI Tum Testler Butunsel Analiz
    if aday.testler:
        _render_ai_tum_testler(aday)

    # Test secimi
    st.markdown("---")
    test_sec = st.selectbox("Test Sec", TEST_TURLERI, key=f"km_t_sec_{aday.id}")

    # Tum testler PR modulundeki birebir icerikle render edilir
    _render_genel_test(store, aday, test_sec)


# ============================================================
# GENEL TEST YONLENDIRICI + TUM TEST TURLERI
# (PR modulundeki birebir sinav icerikleri kullanilir)
# ============================================================

def _render_genel_test(store, aday, test_adi):
    if "Coklu Zeka" in test_adi:
        _render_coklu_zeka_testi(store, aday, test_adi)
    elif "VARK" in test_adi or "Ogrenme Stili" in test_adi:
        _render_vark_testi(store, aday, test_adi)
    elif "Seviye Tespit" in test_adi:
        kademe = "Lise" if "Lise" in test_adi else "Ortaokul"
        _render_seviye_tespit(store, aday, test_adi, kademe)
    elif "CEFR" in test_adi or "Yabanci Dil" in test_adi:
        _render_cefr_testi(store, aday, test_adi)
    elif "HHT" in test_adi or "Hazirlik" in test_adi:
        _render_hht1_testi(store, aday, test_adi)
    elif "Checkup" in test_adi:
        _render_checkup_testi(store, aday, test_adi)
    else:
        st.warning(f"'{test_adi}' icin icerikli form henuz tanimlanmamis.")


def _save_test_result(store, aday, data):
    tum = store.load_all()
    for a in tum:
        if a.id == aday.id:
            a.testler.append(data)
            a.son_islem_tarihi = date.today().isoformat()
            break
    store.save_all(tum)


# ────────────────────────────────────────────────────────────
# COKLU ZEKA TESTI — PR modulundeki birebir icerik
# ────────────────────────────────────────────────────────────

def _render_coklu_zeka_testi(store, aday, test_adi):
    """Coklu Zeka Testi — PR modulundeki 9 alan x 5 soru tam sinav."""
    try:
        from views.halkla_iliskiler_module import render_multi_intelligence_test
        prefix = f"km_cz_{aday.id}"
        pdf_bytes = render_multi_intelligence_test(prefix, lead_label=aday.label)

        if pdf_bytes:
            _save_test_result(store, aday, {
                "test_adi": test_adi,
                "tarih": datetime.now().isoformat(),
                "sonuc": "Tamamlandi",
                "skorlar": {},
                "notlar": "Coklu Zeka Testi tamamlandi — detay icin PDF rapor",
            })
            st.download_button("📄 Coklu Zeka Raporu PDF", data=pdf_bytes,
                               file_name=f"CokluZeka_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                               mime="application/pdf", key=f"km_cz_pdf_{aday.id}", use_container_width=True)
    except ImportError:
        st.error("Halkla Iliskiler modulu yuklenemedi.")
    except Exception as e:
        st.error(f"Test yuklenirken hata: {e}")
    _show_previous(aday, test_adi)


# ────────────────────────────────────────────────────────────
# VARK OGRENME STILI TESTI — PR modulundeki birebir icerik
# ────────────────────────────────────────────────────────────

def _render_vark_testi(store, aday, test_adi):
    """VARK Ogrenme Stili Testi — PR modulundeki tam sinav (yas grubuna gore)."""
    try:
        from views.halkla_iliskiler_module import render_vark_learning_style_test
        prefix = f"km_vark_{aday.id}"

        # Yas grubuna gore baslik ve soru bankasi sec
        if "13+" in test_adi or "13" in test_adi:
            from views.halkla_iliskiler_module import _vark_test_bank_13_plus
            title = "Ogrenme Stili Testi (13+ Yas) - VARK"
            questions = _vark_test_bank_13_plus()
        elif "10-12" in test_adi or "10" in test_adi:
            from views.halkla_iliskiler_module import _vark_test_bank_10_12
            title = "Ogrenme Stili Testi (10-12 Yas) - VARK"
            questions = _vark_test_bank_10_12()
        else:
            title = "Ogrenme Stili Testi (7-9 Yas) - VARK"
            questions = None  # default bank

        render_vark_learning_style_test(prefix, lead_label=aday.label, title=title, questions=questions)

        # VARK test sonucu session state'ten alip kaydedelim
        # (VARK testi return None yapar, sonuc ekranda gosterilir)
    except ImportError:
        st.error("Halkla Iliskiler modulu yuklenemedi.")
    except Exception as e:
        st.error(f"Test yuklenirken hata: {e}")
    _show_previous(aday, test_adi)


# ────────────────────────────────────────────────────────────
# SEVIYE TESPIT SINAVI — PR modulundeki birebir icerik
# ────────────────────────────────────────────────────────────

def _render_seviye_tespit(store, aday, test_adi, kademe):
    """Seviye Tespit Sinavi — PR modulundeki tam sinav (sorulu, sureli, PDF raporlu)."""
    try:
        prefix = f"km_sv_{aday.id}_{kademe}"
        if kademe == "Lise":
            from views.halkla_iliskiler_module import render_high_school_exam_test
            pdf_bytes = render_high_school_exam_test(prefix, lead_label=aday.label)
        else:
            from views.halkla_iliskiler_module import render_middle_school_exam_test
            pdf_bytes = render_middle_school_exam_test(prefix, lead_label=aday.label)

        if pdf_bytes:
            _save_test_result(store, aday, {
                "test_adi": test_adi,
                "tarih": datetime.now().isoformat(),
                "sonuc": "Tamamlandi",
                "skorlar": {},
                "notlar": f"{test_adi} tamamlandi — detay icin PDF rapor",
            })
            st.download_button(f"📄 {test_adi} PDF", data=pdf_bytes,
                               file_name=f"SeviyeTespit_{kademe}_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                               mime="application/pdf", key=f"km_sv_pdf_{aday.id}_{kademe}", use_container_width=True)
    except ImportError:
        st.error("Halkla Iliskiler modulu yuklenemedi.")
    except Exception as e:
        st.error(f"Test yuklenirken hata: {e}")
    _show_previous(aday, test_adi)


# ────────────────────────────────────────────────────────────
# CEFR YABANCI DIL YERLESTIRME — PR modulundeki birebir icerik
# ────────────────────────────────────────────────────────────

def _render_cefr_testi(store, aday, test_adi):
    """CEFR Yabanci Dil Yerlestirme — PR modulundeki tam sinav (listening, reading, grammar + PDF)."""
    try:
        from views.halkla_iliskiler_module import render_language_placement_exam_test
        prefix = f"km_cefr_{aday.id}"
        pdf_bytes = render_language_placement_exam_test(prefix, lead_label=aday.label)

        if pdf_bytes:
            _save_test_result(store, aday, {
                "test_adi": test_adi,
                "tarih": datetime.now().isoformat(),
                "sonuc": "Tamamlandi",
                "skorlar": {},
                "notlar": "CEFR Yabanci Dil sinavi tamamlandi — detay icin PDF rapor",
            })
            st.download_button("📄 CEFR Sinav Raporu PDF", data=pdf_bytes,
                               file_name=f"CEFR_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                               mime="application/pdf", key=f"km_cefr_pdf_{aday.id}", use_container_width=True)
    except ImportError:
        st.error("Halkla Iliskiler modulu yuklenemedi.")
    except Exception as e:
        st.error(f"Test yuklenirken hata: {e}")
    _show_previous(aday, test_adi)


# ────────────────────────────────────────────────────────────
# HHT-1 OKULA HAZIRLIK TESTI — PR modulundeki birebir icerik
# ────────────────────────────────────────────────────────────

def _render_hht1_testi(store, aday, test_adi):
    """HHT-1 Okula Hazirlik — PR modulundeki tam sinav (ogrenci 25 soru + veli 15 soru + PDF)."""
    try:
        from views.halkla_iliskiler_module import render_hht1_test
        prefix = f"km_hht_{aday.id}"
        pdf_bytes = render_hht1_test(prefix, lead_label=aday.label)

        if pdf_bytes:
            _save_test_result(store, aday, {
                "test_adi": test_adi,
                "tarih": datetime.now().isoformat(),
                "sonuc": "Tamamlandi",
                "skorlar": {},
                "notlar": "HHT-1 testi tamamlandi — detay icin PDF rapor",
            })
            st.download_button("📄 HHT-1 Raporu PDF", data=pdf_bytes,
                               file_name=f"HHT1_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                               mime="application/pdf", key=f"km_hht_pdf_{aday.id}", use_container_width=True)
    except ImportError:
        st.error("Halkla Iliskiler modulu yuklenemedi.")
    except Exception as e:
        st.error(f"Test yuklenirken hata: {e}")
    _show_previous(aday, test_adi)


def _render_checkup_testi(store, aday, test_adi):
    """Ortaokul Check-Up — birebir sinav (kayit modulu icinde)."""
    prefix = f"km_oc_{aday.id}"
    pdf_bytes = _km_render_ortaokul_checkup(prefix, store, aday, test_adi, lead_label=aday.label)

    if pdf_bytes:
        st.download_button("📄 Ortaokul Check-Up Raporu PDF", data=pdf_bytes,
                           file_name=f"OrtaokulCheckup_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                           mime="application/pdf", key=f"km_oc_pdf_{aday.id}", use_container_width=True)

    _show_previous(aday, test_adi)


# ────────────────────────────────────────────────────────────
# ORTAOKUL CHECK-UP — SORU BANKALARI & YARDIMCI FONKSIYONLAR
# ────────────────────────────────────────────────────────────

def _km_oc_turkce_sorulari() -> list[tuple[str, str, str, str, str, str]]:
    """Turkce Hazirbulunusluk Sorulari (10 soru - max 50 puan)"""
    return [
        ("'Kitap okumak, hayal gücünü geliştirir.' cümlesinde ana fikir nedir?",
         "Kitaplar pahalıdır", "Okumak hayal gücünü geliştirir", "Kitaplar ağırdır", "Okumak zordur", "B"),
        ("'Ali çok çalıştığı için sınavı geçti.' cümlesinde neden-sonuç ilişkisi hangisidir?",
         "Ali sınavı geçti çünkü şanslıydı", "Ali çalıştı, bu yüzden geçti", "Ali sınavı sevdi", "Ali yorgundu", "B"),
        ("'Hava çok sıcak olmasına rağmen dışarı çıktık.' cümlesindeki zıtlık ilişkisi nedir?",
         "Sıcak hava - dışarı çıkmak", "Soğuk - sıcak", "İçeri - dışarı", "Gece - gündüz", "A"),
        ("'Kapkara bulutlar gökyüzünü kapladı.' cümlesinde altı çizili sözcüğün anlamı nedir?",
         "Çok beyaz", "Çok siyah/koyu", "Çok büyük", "Çok küçük", "B"),
        ("Metinde 'Çocuk üzgün görünüyordu' yazıyorsa, çocuğun duygusu hakkında ne çıkarım yapabiliriz?",
         "Mutlu", "Kızgın", "Mutsuz/üzgün", "Heyecanlı", "C"),
        ("'Bahçedeki çiçekler rengarenk açmıştı.' cümlesinde 'rengarenk' sözcüğünün yerine hangisi kullanılabilir?",
         "Solgun", "Çeşitli renklerde", "Tek renkli", "Gri", "B"),
        ("Bir hikayenin sonunda 'Böylece herkes mutlu oldu.' yazıyorsa, bu ne anlama gelir?",
         "Hikaye devam edecek", "Sorun çözüldü", "Herkes üzgün", "Hikaye başlıyor", "B"),
        ("'Kediler süt sever.' cümlesinde özne hangisidir?",
         "Süt", "Sever", "Kediler", "Cümlenin tamamı", "C"),
        ("'Annem bana güzel bir hediye aldı.' cümlesinde nesne hangisidir?",
         "Annem", "Bana", "Güzel bir hediye", "Aldı", "C"),
        ("Bir paragrafta tekrar tekrar 'doğa' kelimesi geçiyorsa, paragrafın konusu ne olabilir?",
         "Teknoloji", "Çevre/doğa", "Spor", "Müzik", "B"),
    ]


def _km_oc_mat_sorulari() -> list[tuple[str, str, str, str, str, str]]:
    """Matematik Hazirbulunusluk Sorulari (10 soru - max 50 puan)"""
    return [
        ("456 sayısında 5'in basamak değeri kaçtır?",
         "5", "50", "500", "56", "B"),
        ("125 × 4 işleminin sonucu kaçtır?",
         "500", "400", "520", "450", "A"),
        ("720 ÷ 8 işleminin sonucu kaçtır?",
         "80", "90", "85", "95", "B"),
        ("1/2 kesrinin 4/8 kesrine eşit olup olmadığını belirleyin:",
         "Eşit değil", "Eşit", "1/2 daha büyük", "4/8 daha büyük", "B"),
        ("3/4 kesrinin okunuşu hangisidir?",
         "Üç bölü dört", "Dörtte üç", "Üç çarpı dört", "Dört bölü üç", "B"),
        ("Bir karenin bir kenarı 6 cm ise çevresi kaç cm'dir?",
         "12 cm", "18 cm", "24 cm", "36 cm", "C"),
        ("Saat 14:30'u 12'li sistemde nasıl gösteririz?",
         "2:30", "14:30", "4:30", "12:30", "A"),
        ("Bir markette 3 elma 15 TL ise 5 elma kaç TL'dir?",
         "20 TL", "25 TL", "30 TL", "18 TL", "B"),
        ("45 + 37 - 22 işleminin sonucu kaçtır?",
         "60", "55", "65", "50", "A"),
        ("Bir dikdörtgenin kısa kenarı 4 cm, uzun kenarı 7 cm ise çevresi kaç cm'dir?",
         "11 cm", "22 cm", "28 cm", "18 cm", "B"),
    ]


def _km_oc_ogrenme_profili() -> list[tuple[str, list[str]]]:
    """Ogrenme Profili Sorulari - Tercih belirleme"""
    return [
        ("Yeni bir konu öğrenirken en çok hangisini tercih edersiniz?",
         ["Resim/şema/grafik görmek (Görsel)", "Birinin anlatmasını dinlemek (İşitsel)",
          "Not alıp yazmak (Okuma-Yazma)", "Uygulama/deneme yapmak (Uygulamalı)"]),
        ("Ders çalışırken en verimli olduğunuz ortam hangisidir?",
         ["Renkli notlar ve görsellerle (Görsel)", "Sessiz ortamda sesli okuyarak (İşitsel)",
          "Özet çıkararak (Okuma-Yazma)", "Pratik yaparak (Uygulamalı)"]),
        ("Bir konuyu en iyi nasıl hatırlarsınız?",
         ["Zihnimde resimleyerek (Görsel)", "Birinin sesini hatırlayarak (İşitsel)",
          "Yazdıklarımı okuyarak (Okuma-Yazma)", "Yaptığım uygulamayı düşünerek (Uygulamalı)"]),
        ("Sınavlara nasıl hazırlanırsınız?",
         ["Şema/harita çizerek (Görsel)", "Konuyu sesli tekrar ederek (İşitsel)",
          "Özet ve not çıkararak (Okuma-Yazma)", "Çok soru çözerek (Uygulamalı)"]),
    ]


def _km_oc_aliskanlik_sorulari() -> list[tuple[str, list[str], list[int]]]:
    """Calisma Aliskanliklari Sorulari (max 60 puan)"""
    return [
        ("Günde telefon/tablet kullanım süreniz ne kadar?",
         ["1 saatten az", "1-2 saat", "2-3 saat", "3 saatten fazla"], [5, 4, 2, 0]),
        ("Haftalık ders programınız var mı?",
         ["Evet, düzenli uyguluyorum", "Var ama bazen uyguluyorum", "Ara sıra yapıyorum", "Hayır, yok"], [5, 3, 2, 0]),
        ("Bir konuya ne kadar süre odaklanabilirsiniz?",
         ["25 dakikadan fazla", "15-25 dakika", "10-15 dakika", "10 dakikadan az"], [5, 4, 2, 0]),
        ("Yanlış yaptığınız soruları tekrar çözüyor musunuz?",
         ["Her zaman", "Çoğunlukla", "Bazen", "Hiç"], [5, 4, 2, 0]),
        ("Ödevlerinizi ne zaman yaparsınız?",
         ["Hemen/aynı gün", "1-2 gün içinde", "Son güne yakın", "Son dakikada"], [5, 3, 2, 0]),
        ("Düzenli tekrar yapıyor musunuz?",
         ["Her gün", "Haftada 2-3 kez", "Haftada 1 kez", "Sınav öncesi"], [5, 4, 2, 0]),
        ("Ders çalışırken mola veriyor musunuz?",
         ["25 dk çalış, 5 dk mola", "Düzensiz mola", "Uzun aralar", "Mola vermiyorum"], [5, 3, 2, 0]),
        ("Defter ve kitaplarınız düzenli mi?",
         ["Çok düzenli", "Genelde düzenli", "Biraz dağınık", "Çok dağınık"], [5, 4, 2, 0]),
        ("Sabah mı akşam mı daha verimli çalışırsınız?",
         ["Sabah erken", "Öğleden sonra", "Akşam", "Gece geç"], [5, 4, 3, 2]),
        ("Hedef koyar mısınız?",
         ["Evet, yazılı hedeflerim var", "Kafamda var", "Bazen", "Hayır"], [5, 3, 2, 0]),
        ("Zorlandığınızda ne yaparsınız?",
         ["Yardım isterim", "Tekrar denerim", "Atlarım", "Bırakırım"], [5, 4, 2, 0]),
        ("Test/sınav öncesi stres yaşar mısınız?",
         ["Hayır, hazır hissederim", "Biraz", "Orta düzeyde", "Çok stresli olurum"], [5, 4, 2, 0]),
    ]


def _km_oc_uyum_sorulari() -> list[tuple[str, list[str], list[int]]]:
    """Uyum & Motivasyon Sorulari (max 20 puan)"""
    return [
        ("Sınıfta öğretmenin yönergelerini takip etmekte zorlanır mısınız?",
         ["Hiç zorlanmam", "Nadiren", "Bazen", "Sık sık"], [5, 4, 2, 0]),
        ("Derste soru sormaktan çekinir misiniz?",
         ["Hiç çekinmem", "Nadiren", "Bazen", "Çok çekinirim"], [5, 4, 2, 0]),
        ("Yeni arkadaşlıklar kurmakta zorlanır mısınız?",
         ["Hiç zorlanmam", "Biraz", "Orta düzeyde", "Çok zorlanırım"], [5, 4, 2, 0]),
        ("Hata yaptığınızda moraliniz bozulur mu?",
         ["Hayır, tekrar denerim", "Biraz üzülürüm", "Orta düzeyde", "Çok bozulur"], [5, 4, 2, 0]),
    ]


def _km_oc_renk_bandi_bolum(puan: int) -> tuple[str, str]:
    """Bolum puani icin renk bandi (0-50)"""
    if puan >= 43:
        return "YEŞİL", "#10b981"
    elif puan >= 33:
        return "MAVİ", "#3b82f6"
    elif puan >= 23:
        return "SARI", "#f59e0b"
    else:
        return "KIRMIZI", "#ef4444"


def _km_oc_renk_bandi_toplam(puan: int) -> tuple[str, str]:
    """Toplam puan icin renk bandi (0-100)"""
    if puan >= 85:
        return "YEŞİL", "#10b981"
    elif puan >= 65:
        return "MAVİ", "#3b82f6"
    elif puan >= 45:
        return "SARI", "#f59e0b"
    else:
        return "KIRMIZI", "#ef4444"


def _km_oc_renk_bandi_uyum(puan: int) -> tuple[str, str]:
    """Uyum puani icin renk bandi (0-20)"""
    if puan >= 16:
        return "YEŞİL", "#10b981"
    elif puan >= 11:
        return "MAVİ", "#3b82f6"
    elif puan >= 6:
        return "SARI", "#f59e0b"
    else:
        return "KIRMIZI", "#ef4444"


def _km_oc_renk_bandi_aliskanlik(puan: int) -> tuple[str, str]:
    """Aliskanlik puani icin renk bandi (0-60)"""
    if puan >= 48:
        return "YEŞİL", "#10b981"
    elif puan >= 36:
        return "MAVİ", "#3b82f6"
    elif puan >= 24:
        return "SARI", "#f59e0b"
    else:
        return "KIRMIZI", "#ef4444"


def _km_oc_toplam_yorum(renk: str, zayif1: str, zayif2: str) -> str:
    """Toplam puana gore otomatik yorum"""
    yorumlar = {
        "YEŞİL": "Çocuğunuzun 5. sınıfa akademik başlangıcı güçlü. Hem okuduğunu anlama hem matematik önkoşullarda sağlam bir taban var. Bu seviyede hedefimiz 'hızlandırma + zenginleştirme': doğru alışkanlıkla çok hızlı ilerler.",
        "MAVİ": f"Genel başlangıç seviyesi iyi. Çocuğunuzun güçlü bir temeli var. Rapor şu iki alanda destekle çok hızlı yukarı çıkar: {zayif1}, {zayif2}. 2 haftalık mini planı uygularsak kısa sürede net fark görürüz.",
        "SARI": f"Başlangıçta bazı temel boşluklar var; bu çok normal çünkü geçiş dönemindeyiz. İyi haber: Bu boşluklar planlı çalışmayla hızlı kapanır. Öncelik vereceğimiz iki konu: {zayif1}, {zayif2}. 4 haftalık destekle belirgin toparlanma bekleriz.",
        "KIRMIZI": f"Şu an başlangıç seviyesinde belirgin destek ihtiyacı görünüyor. Bu 'yapamaz' demek değil; 'doğru plan + yakın takip' demek. Biz önce temeli güçlendirip özgüveni yükseltiriz. İlk hedef: {zayif1} ve {zayif2}. 2-4 haftada görünür ilerleme almayı hedefliyoruz."
    }
    return yorumlar.get(renk, "")


# ────────────────────────────────────────────────────────────
# ORTAOKUL CHECK-UP — ANA RENDER FONKSİYONU
# ────────────────────────────────────────────────────────────

def _km_render_ortaokul_checkup(prefix: str, store, aday, test_adi: str, *, lead_label: str = "") -> bytes | None:
    """4→5 Gecis Ortaokula Baslangic Raporu Testi (kayit modulu icinde)"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
        <h3 style="color: white; margin: 0;">🎓 Ortaokul Check-Up Testi</h3>
        <p style="color: #e9d5ff; margin: 0.5rem 0 0 0;">5. Sınıfa Başlayacaklar İçin Kapsamlı Değerlendirme (60 dk)</p>
    </div>
    """, unsafe_allow_html=True)

    if lead_label:
        st.caption(f"Aday: {lead_label}")

    # Ogrenci bilgileri
    from utils.shared_data import get_student_display_options as _km_stu_opts
    _stu_opts_oc = _km_stu_opts()
    if len(_stu_opts_oc) > 1:
        _stu_sel_oc = st.selectbox("Kayıtli ogrenci sec", list(_stu_opts_oc.keys()), key=f"{prefix}_oc_stu_sel")
        _stu_data_oc = _stu_opts_oc.get(_stu_sel_oc, {})
    else:
        _stu_sel_oc = None
        _stu_data_oc = {}
    _oc_veli = ""
    if _stu_data_oc:
        _oc_veli = _stu_data_oc.get("veli_adi", "")
        if not _oc_veli:
            _oc_veli = f'{_stu_data_oc.get("anne_adi", "")} {_stu_data_oc.get("anne_soyadi", "")}'.strip()
        if not _oc_veli:
            _oc_veli = f'{_stu_data_oc.get("baba_adi", "")} {_stu_data_oc.get("baba_soyadi", "")}'.strip()
    info_cols = st.columns(3)
    with info_cols[0]:
        student_name = st.text_input("Öğrenci Ad Soyad", value=f'{_stu_data_oc.get("ad", "")} {_stu_data_oc.get("soyad", "")}'.strip() if _stu_data_oc else "", key=f"{prefix}_oc_student_name")
    with info_cols[1]:
        veli_adi = st.text_input("Veli Adi", value=_oc_veli, key=f"{prefix}_oc_veli_name")
    with info_cols[2]:
        test_tarihi = st.date_input("Test Tarihi", value=datetime.now().date(), key=f"{prefix}_oc_date")

    # ==================== TEST-1: HAZIR BULUNUSLUK ====================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 10px; padding: 1rem; margin: 1.5rem 0 1rem 0;">
        <h4 style="color: white; margin: 0;">📚 Test-1: Hazırbulunuşluk (Türkçe + Matematik)</h4>
        <p style="color: #d1fae5; margin: 0.3rem 0 0 0; font-size: 0.9rem;">Toplam: 100 puan (Türkçe 50 + Matematik 50)</p>
    </div>
    """, unsafe_allow_html=True)

    turkce_sorulari = _km_oc_turkce_sorulari()
    mat_sorulari = _km_oc_mat_sorulari()
    options = ["Seçiniz", "A", "B", "C", "D"]

    turkce_cevaplar: list[tuple[str, str]] = []
    mat_cevaplar: list[tuple[str, str]] = []

    with st.expander("📖 Türkçe Soruları (10 Soru - 50 Puan)", expanded=True):
        for idx, (soru, a, b, c, d, cevap) in enumerate(turkce_sorulari, 1):
            st.markdown(f"**{idx}.** {soru}")
            st.caption(f"A) {a}  |  B) {b}  |  C) {c}  |  D) {d}")
            secim = st.selectbox("Cevap", options, key=f"{prefix}_tr_{idx}", label_visibility="collapsed")
            turkce_cevaplar.append((secim, cevap))

    with st.expander("🔢 Matematik Soruları (10 Soru - 50 Puan)", expanded=False):
        for idx, (soru, a, b, c, d, cevap) in enumerate(mat_sorulari, 1):
            st.markdown(f"**{idx}.** {soru}")
            st.caption(f"A) {a}  |  B) {b}  |  C) {c}  |  D) {d}")
            secim = st.selectbox("Cevap", options, key=f"{prefix}_mat_{idx}", label_visibility="collapsed")
            mat_cevaplar.append((secim, cevap))

    # ==================== TEST-2: OGRENME PROFILI ====================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 10px; padding: 1rem; margin: 1.5rem 0 1rem 0;">
        <h4 style="color: white; margin: 0;">🧠 Test-2: Öğrenme Profili</h4>
        <p style="color: #bfdbfe; margin: 0.3rem 0 0 0; font-size: 0.9rem;">Tercihler + Çalışma Alışkanlıkları (60 puan)</p>
    </div>
    """, unsafe_allow_html=True)

    ogrenme_profili = _km_oc_ogrenme_profili()
    aliskanlik_sorulari = _km_oc_aliskanlik_sorulari()

    tercih_secimler: list[int] = []
    with st.expander("🎯 Öğrenme Tercihi (4 Soru)", expanded=True):
        for idx, (soru, secenekler) in enumerate(ogrenme_profili, 1):
            st.markdown(f"**{idx}.** {soru}")
            secim = st.radio("Seçim", secenekler, key=f"{prefix}_tercih_{idx}", label_visibility="collapsed")
            tercih_secimler.append(secenekler.index(secim))

    aliskanlik_puanlari: list[int] = []
    with st.expander("📋 Çalışma Alışkanlıkları (12 Soru - 60 Puan)", expanded=False):
        for idx, (soru, secenekler, puanlar) in enumerate(aliskanlik_sorulari, 1):
            st.markdown(f"**{idx}.** {soru}")
            secim = st.radio("Seçim", secenekler, key=f"{prefix}_alis_{idx}", label_visibility="collapsed")
            secim_idx = secenekler.index(secim)
            aliskanlik_puanlari.append(puanlar[secim_idx])

    # ==================== TEST-3: UYUM & MOTIVASYON ====================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); border-radius: 10px; padding: 1rem; margin: 1.5rem 0 1rem 0;">
        <h4 style="color: white; margin: 0;">❤️ Test-3: Uyum & Motivasyon</h4>
        <p style="color: #fef3c7; margin: 0.3rem 0 0 0; font-size: 0.9rem;">Okul adaptasyonu (20 puan)</p>
    </div>
    """, unsafe_allow_html=True)

    uyum_sorulari = _km_oc_uyum_sorulari()
    uyum_puanlari: list[int] = []

    with st.expander("🤝 Uyum Soruları (4 Soru - 20 Puan)", expanded=True):
        for idx, (soru, secenekler, puanlar) in enumerate(uyum_sorulari, 1):
            st.markdown(f"**{idx}.** {soru}")
            secim = st.radio("Seçim", secenekler, key=f"{prefix}_uyum_{idx}", label_visibility="collapsed")
            secim_idx = secenekler.index(secim)
            uyum_puanlari.append(puanlar[secim_idx])

    # ==================== SONUC HESAPLAMA ====================
    if st.button("📊 Raporu Oluştur", key=f"{prefix}_calc", use_container_width=True):
        tr_dogru = sum(1 for secim, cevap in turkce_cevaplar if secim == cevap)
        tr_puan = tr_dogru * 5

        mat_dogru = sum(1 for secim, cevap in mat_cevaplar if secim == cevap)
        mat_puan = mat_dogru * 5

        toplam_puan = tr_puan + mat_puan

        aliskanlik_puan = sum(aliskanlik_puanlari)
        uyum_puan = sum(uyum_puanlari)

        tr_renk, tr_color = _km_oc_renk_bandi_bolum(tr_puan)
        mat_renk, mat_color = _km_oc_renk_bandi_bolum(mat_puan)
        toplam_renk, toplam_color = _km_oc_renk_bandi_toplam(toplam_puan)
        alis_renk, alis_color = _km_oc_renk_bandi_aliskanlik(aliskanlik_puan)
        uyum_renk, uyum_color = _km_oc_renk_bandi_uyum(uyum_puan)

        tercih_labels = ["Görsel", "İşitsel", "Okuma-Yazma", "Uygulamalı"]
        tercih_counter = Counter(tercih_secimler)
        en_cok_tercihler = tercih_counter.most_common(2)
        tercih1 = tercih_labels[en_cok_tercihler[0][0]] if en_cok_tercihler else "Görsel"
        tercih2 = tercih_labels[en_cok_tercihler[1][0]] if len(en_cok_tercihler) > 1 else tercih1

        zayif_alanlar = []
        if tr_puan < mat_puan:
            zayif_alanlar.append("Türkçe/Okuma Anlama")
        else:
            zayif_alanlar.append("Matematik")
        if aliskanlik_puan < 36:
            zayif_alanlar.append("Çalışma Alışkanlıkları")
        if uyum_puan < 11:
            zayif_alanlar.append("Uyum/Motivasyon")

        zayif1 = zayif_alanlar[0] if zayif_alanlar else "Genel"
        zayif2 = zayif_alanlar[1] if len(zayif_alanlar) > 1 else zayif1

        toplam_yorum = _km_oc_toplam_yorum(toplam_renk, zayif1, zayif2)

        # ==================== SONUC GOSTERIMI ====================
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #eef2ff 0%, #1e1b4b 100%); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid #c7d2fe;">
            <h3 style="color: #94A3B8; margin: 0; text-align: center;">📋 Ortaokula Başlangıç Raporu</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.8rem; margin: 1rem 0;">
            <div style="background: {tr_color}; border-radius: 10px; padding: 1rem; text-align: center; color: white;">
                <div style="font-size: 0.8rem;">📖 Türkçe</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{tr_puan}/50</div>
                <div style="font-size: 0.75rem; background: rgba(255,255,255,0.2); border-radius: 8px; padding: 0.2rem;">{tr_renk}</div>
            </div>
            <div style="background: {mat_color}; border-radius: 10px; padding: 1rem; text-align: center; color: white;">
                <div style="font-size: 0.8rem;">🔢 Matematik</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{mat_puan}/50</div>
                <div style="font-size: 0.75rem; background: rgba(255,255,255,0.2); border-radius: 8px; padding: 0.2rem;">{mat_renk}</div>
            </div>
            <div style="background: {toplam_color}; border-radius: 10px; padding: 1rem; text-align: center; color: white;">
                <div style="font-size: 0.8rem;">📊 TOPLAM</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{toplam_puan}/100</div>
                <div style="font-size: 0.75rem; background: rgba(255,255,255,0.2); border-radius: 8px; padding: 0.2rem;">{toplam_renk}</div>
            </div>
            <div style="background: {alis_color}; border-radius: 10px; padding: 1rem; text-align: center; color: white;">
                <div style="font-size: 0.8rem;">📋 Alışkanlık</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{aliskanlik_puan}/60</div>
                <div style="font-size: 0.75rem; background: rgba(255,255,255,0.2); border-radius: 8px; padding: 0.2rem;">{alis_renk}</div>
            </div>
            <div style="background: {uyum_color}; border-radius: 10px; padding: 1rem; text-align: center; color: white;">
                <div style="font-size: 0.8rem;">❤️ Uyum</div>
                <div style="font-size: 1.8rem; font-weight: 700;">{uyum_puan}/20</div>
                <div style="font-size: 0.75rem; background: rgba(255,255,255,0.2); border-radius: 8px; padding: 0.2rem;">{uyum_renk}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: #172554; border-radius: 10px; padding: 1rem; margin: 1rem 0; border: 2px solid #3b82f6;">
            <h4 style="color: #93c5fd; margin: 0 0 0.5rem 0;">🧠 Öğrenme Profili</h4>
            <p style="margin: 0;"><strong>Tercih:</strong> {tercih1} + {tercih2}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: {toplam_color}22; border-radius: 10px; padding: 1rem; margin: 1rem 0; border-left: 4px solid {toplam_color};">
            <h4 style="color: #1f2937; margin: 0 0 0.5rem 0;">💬 Değerlendirme</h4>
            <p style="color: #94A3B8; margin: 0;">{toplam_yorum}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: #052e16; border-radius: 10px; padding: 1rem; margin: 1rem 0; border: 2px solid #10b981;">
            <h4 style="color: #4ade80; margin: 0 0 0.5rem 0;">📅 2 Haftalık Mini Plan</h4>
            <ul style="color: #065f46; margin: 0; padding-left: 1.5rem;">
                <li><strong>Pzt-Çrş-Cum:</strong> 15 dk konu + 10 dk mini test</li>
                <li><strong>Salı-Perş:</strong> 10 dk okuma + 10 dk özet + 5 dk yanlış analizi</li>
                <li><strong>Cts:</strong> 20 dk kısa deneme + 10 dk yanlışlar</li>
                <li><strong>Paz:</strong> 20 dk serbest okuma</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #78350f 0%, #f59e0b40 100%); border-radius: 10px; padding: 1rem; margin: 1rem 0; border: 2px solid #f59e0b;">
            <h4 style="color: #b45309; margin: 0 0 0.5rem 0;">🎤 Veliye Sunum Metni (60 saniye)</h4>
            <p style="color: #fbbf24; margin: 0; font-style: italic;">
            "{veli_adi or 'Sayın Veli'} Hanım/Bey, 60 dakikalık taramamızın sonucunda çocuğunuzun 5. sınıfa başlangıç seviyesini net görüyoruz.
            Toplam puanımız {toplam_puan}/100 ve renk bandı {toplam_renk}.
            Türkçe {tr_puan}/50, Matematik {mat_puan}/50.
            Öğrenme profili {tercih1}+{tercih2}; yani en hızlı bu yöntemlerle öğreniyor.
            Bu rapora göre iki önceliğimiz var: {zayif1} ve {zayif2}.
            İyi haber: 2 haftalık mini planla hızlı gelişim görürüz.
            İsterseniz bir sonraki adım olarak 'deneme ders + kampüs deneyimi' randevusunu netleştirelim."
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Sonucu kaydet
        skorlar = {
            "Turkce": tr_puan,
            "Matematik": mat_puan,
            "Toplam": toplam_puan,
            "Aliskanlik": aliskanlik_puan,
            "Uyum": uyum_puan,
        }
        _save_test_result(store, aday, {
            "test_adi": test_adi,
            "tarih": datetime.now().isoformat(),
            "sonuc": f"{toplam_puan}/100 ({toplam_renk})",
            "puan": toplam_puan,
            "skorlar": skorlar,
            "notlar": f"Turkce:{tr_puan}/50({tr_renk}) Mat:{mat_puan}/50({mat_renk}) Alis:{aliskanlik_puan}/60({alis_renk}) Uyum:{uyum_puan}/20({uyum_renk}) Tercih:{tercih1}+{tercih2}",
        })

        # PDF olustur
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import cm
            from reportlab.lib.colors import HexColor
            from utils.shared_data import ensure_turkish_pdf_fonts
            import io

            font_name, font_bold = ensure_turkish_pdf_fonts()

            buffer = io.BytesIO()
            width, height = A4
            c = canvas.Canvas(buffer, pagesize=A4)

            def safe_text(val):
                if val is None:
                    return ""
                return str(val)

            y = height - 2*cm

            # Baslik
            c.setFillColor(HexColor("#7c3aed"))
            c.roundRect(1.5*cm, y - 1.2*cm, width - 3*cm, 1.5*cm, 8, fill=1, stroke=0)
            c.setFillColor(HexColor("#ffffff"))
            c.setFont(font_bold, 14)
            c.drawCentredString(width/2, y - 0.6*cm, "ORTAOKULA BASLANGIC RAPORU - 5. SINIFA GECIS")
            y -= 2.2*cm

            # Ogrenci bilgileri
            c.setFillColor(HexColor("#1f2937"))
            c.setFont(font_bold, 10)
            c.drawString(2*cm, y, f"Öğrenci: {safe_text(student_name)}")
            c.drawString(10*cm, y, f"Tarih: {test_tarihi}")
            y -= 0.6*cm
            c.drawString(2*cm, y, f"Veli: {safe_text(veli_adi)}")
            c.drawString(10*cm, y, "Sure: 60 dk")
            y -= 1*cm

            # A) Hazirbulunusluk
            c.setFillColor(HexColor("#10b981"))
            c.roundRect(1.5*cm, y - 0.8*cm, width - 3*cm, 1*cm, 5, fill=1, stroke=0)
            c.setFillColor(HexColor("#ffffff"))
            c.setFont(font_bold, 11)
            c.drawString(2*cm, y - 0.5*cm, "A) HAZIR BULUNUSLUK")
            y -= 1.5*cm

            c.setFillColor(HexColor("#1f2937"))
            c.setFont(font_name, 10)
            c.drawString(2*cm, y, f"Turkce: {tr_puan}/50  [{tr_renk}]")
            c.drawString(10*cm, y, f"Matematik: {mat_puan}/50  [{mat_renk}]")
            y -= 0.5*cm
            c.setFont(font_bold, 11)
            c.drawString(2*cm, y, f"TOPLAM: {toplam_puan}/100  [{toplam_renk}]")
            y -= 1*cm

            # B) Kisa Yorum
            c.setFillColor(HexColor("#3b82f6"))
            c.roundRect(1.5*cm, y - 0.8*cm, width - 3*cm, 1*cm, 5, fill=1, stroke=0)
            c.setFillColor(HexColor("#ffffff"))
            c.setFont(font_bold, 11)
            c.drawString(2*cm, y - 0.5*cm, "B) DEGERLENDIRME")
            y -= 1.5*cm

            c.setFillColor(HexColor("#1f2937"))
            c.setFont(font_name, 9)
            yorum_lines = safe_text(toplam_yorum)
            max_chars = 90
            for i in range(0, len(yorum_lines), max_chars):
                line = yorum_lines[i:i+max_chars]
                c.drawString(2*cm, y, line)
                y -= 0.4*cm
            y -= 0.5*cm

            # C) Ogrenme Profili
            c.setFillColor(HexColor("#f59e0b"))
            c.roundRect(1.5*cm, y - 0.8*cm, width - 3*cm, 1*cm, 5, fill=1, stroke=0)
            c.setFillColor(HexColor("#ffffff"))
            c.setFont(font_bold, 11)
            c.drawString(2*cm, y - 0.5*cm, "C) OGRENME PROFILI")
            y -= 1.5*cm

            c.setFillColor(HexColor("#1f2937"))
            c.setFont(font_name, 10)
            c.drawString(2*cm, y, f"Tercih: {safe_text(tercih1)} + {safe_text(tercih2)}")
            y -= 0.5*cm
            c.drawString(2*cm, y, f"Calisma Aliskanligi: {aliskanlik_puan}/60  [{alis_renk}]")
            y -= 1*cm

            # D) Uyum
            c.setFillColor(HexColor("#ef4444"))
            c.roundRect(1.5*cm, y - 0.8*cm, width - 3*cm, 1*cm, 5, fill=1, stroke=0)
            c.setFillColor(HexColor("#ffffff"))
            c.setFont(font_bold, 11)
            c.drawString(2*cm, y - 0.5*cm, "D) UYUM & MOTIVASYON")
            y -= 1.5*cm

            c.setFillColor(HexColor("#1f2937"))
            c.setFont(font_name, 10)
            c.drawString(2*cm, y, f"Uyum Skoru: {uyum_puan}/20  [{uyum_renk}]")
            y -= 1*cm

            # E) 2 Haftalik Plan
            c.setFillColor(HexColor("#10b981"))
            c.roundRect(1.5*cm, y - 0.8*cm, width - 3*cm, 1*cm, 5, fill=1, stroke=0)
            c.setFillColor(HexColor("#ffffff"))
            c.setFont(font_bold, 11)
            c.drawString(2*cm, y - 0.5*cm, "E) 2 HAFTALIK MINI PLAN")
            y -= 1.5*cm

            c.setFillColor(HexColor("#1f2937"))
            c.setFont(font_name, 9)
            c.drawString(2*cm, y, "- Pzt-Crs-Cum: 15 dk konu + 10 dk mini test")
            y -= 0.4*cm
            c.drawString(2*cm, y, "- Sali-Pers: 10 dk okuma + 10 dk ozet + 5 dk yanlis analizi")
            y -= 0.4*cm
            c.drawString(2*cm, y, "- Cts: 20 dk kisa deneme + 10 dk yanlislar")
            y -= 0.4*cm
            c.drawString(2*cm, y, "- Paz: 20 dk serbest okuma")
            y -= 1*cm

            # Footer
            c.setFont(font_name, 8)
            c.setFillColor(HexColor("#6b7280"))
            c.drawCentredString(width/2, 1.5*cm, "SmartCampus AI - Ortaokul Check-Up Raporu")

            c.save()
            pdf_bytes = buffer.getvalue()

            st.download_button(
                "📥 PDF Raporu İndir",
                pdf_bytes,
                file_name=f"ortaokul_checkup_{safe_text(student_name).replace(' ', '_')}_{test_tarihi}.pdf",
                mime="application/pdf",
                key=f"{prefix}_pdf_dl",
                use_container_width=True
            )
            return pdf_bytes

        except Exception as e:
            st.error(f"PDF oluşturma hatası: {e}")
            return None

    return None


def _show_previous(aday, test_adi):
    onceki = [t for t in aday.testler if t.get("test_adi") == test_adi and t.get("skorlar")]
    if not onceki:
        return
    son = onceki[-1]
    skorlar = son.get("skorlar", {})
    if not skorlar:
        return
    st.markdown("---")
    st.markdown(f'<div style="color:#a5b4fc;font-weight:700;margin:8px 0">📊 Son Sonuc ({str(son.get("tarih", ""))[:10]}): {son.get("sonuc", "")}</div>', unsafe_allow_html=True)
    max_val = max((v for v in skorlar.values() if isinstance(v, (int, float))), default=1)
    if isinstance(max_val, str):
        for alan, skor in skorlar.items():
            st.markdown(f'<div style="display:flex;align-items:center;gap:8px;margin:3px 0"><span style="min-width:130px;font-size:0.8rem;color:#94a3b8">{alan}</span><span style="background:#6366f1;color:#fff;padding:2px 10px;border-radius:10px;font-size:0.8rem;font-weight:700">{skor}</span></div>', unsafe_allow_html=True)
    else:
        for alan, skor in sorted(skorlar.items(), key=lambda x: x[1] if isinstance(x[1], (int, float)) else 0, reverse=True):
            if not isinstance(skor, (int, float)):
                continue
            pct = int(skor / max_val * 100) if max_val > 0 else 0
            clr = "#10b981" if pct >= 70 else ("#3b82f6" if pct >= 40 else "#f59e0b")
            st.markdown(f'<div style="display:flex;align-items:center;gap:8px;margin:3px 0"><span style="min-width:130px;font-size:0.8rem;color:#94a3b8">{alan}</span><div style="flex:1;background:#1e293b;border-radius:6px;height:18px;overflow:hidden"><div style="width:{pct}%;height:100%;background:{clr};border-radius:6px;display:flex;align-items:center;justify-content:flex-end;padding-right:4px"><span style="font-size:0.6rem;font-weight:700;color:#fff">{skor}</span></div></div></div>', unsafe_allow_html=True)

    # AI Analiz + Tavsiye + Yol Haritasi
    _render_ai_test_analiz(aday, son)


# ────────────────────────────────────────────────────────────
# AI TEST ANALIZI — Tum testler icin ortak
# ────────────────────────────────────────────────────────────

def _render_ai_test_analiz(aday, test_data: dict):
    """Tek bir test sonucu icin AI analizi, tavsiyesi ve yol haritasi."""
    test_adi = test_data.get("test_adi", "")
    ai_key = f"km_ai_test_{aday.id}_{test_adi.replace(' ', '_')}"
    result_key = f"{ai_key}_result"

    st.markdown("")
    if st.button("🤖 AI Analiz + Tavsiye + Yol Haritasi", key=ai_key, type="primary", use_container_width=True):
        with st.spinner("AI analiz hazirlaniyor..."):
            ai_result = _call_ai_test_analiz(aday, test_data)
            if ai_result:
                st.session_state[result_key] = ai_result

    ai_result = st.session_state.get(result_key, "")
    if ai_result:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#7c3aed20,#4f46e510);'
            'border:1px solid #7c3aed40;border-radius:12px;padding:1rem;margin:0.8rem 0">'
            '<strong style="color:#a78bfa;font-size:1rem">🤖 AI Analiz Raporu</strong></div>',
            unsafe_allow_html=True)
        _render_ai_result(ai_result)


def _render_ai_tum_testler(aday):
    """Adayin tum test sonuclarini topluca AI'ya gonderip genel analiz al."""
    if not aday.testler:
        return

    ai_key = f"km_ai_tum_test_{aday.id}"
    result_key = f"{ai_key}_result"

    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed,#4f46e5);border-radius:12px;'
        'padding:1rem 1.5rem;margin:1rem 0">'
        '<h4 style="color:#fff;margin:0">🤖 AI Genel Degerlendirme</h4>'
        '<p style="color:#c7d2fe;margin:0.3rem 0 0 0;font-size:0.85rem">'
        'Tum test sonuclarini analiz et — bütünsel yol haritasi olustur</p></div>',
        unsafe_allow_html=True)

    if st.button("🤖 Tum Testleri Analiz Et + Genel Yol Haritasi", key=ai_key, type="primary", use_container_width=True):
        with st.spinner("AI tum testleri analiz ediyor..."):
            ai_result = _call_ai_tum_testler_analiz(aday)
            if ai_result:
                st.session_state[result_key] = ai_result

    ai_result = st.session_state.get(result_key, "")
    if ai_result:
        st.markdown(
            '<div style="background:linear-gradient(135deg,#7c3aed20,#4f46e510);'
            'border:1px solid #7c3aed40;border-radius:12px;padding:1rem;margin:0.8rem 0">'
            '<strong style="color:#a78bfa;font-size:1rem">🤖 Butunsel AI Degerlendirme Raporu</strong></div>',
            unsafe_allow_html=True)
        _render_ai_result(ai_result)


def _call_ai_test_analiz(aday, test_data: dict) -> str:
    """Tek test sonucu icin AI analizi."""
    try:
        from utils.smarti_helper import _ensure_env, _get_client
        _ensure_env()
        client = _get_client()
        if not client:
            return ""

        test_adi = test_data.get("test_adi", "")
        sonuc = test_data.get("sonuc", "")
        skorlar = test_data.get("skorlar", {})
        notlar = test_data.get("notlar", "")
        top3 = test_data.get("top3", [])

        skor_text = "\n".join(f"- {k}: {v}" for k, v in skorlar.items()) if skorlar else "Skor detayi yok"
        top3_text = "\n".join(f"- {t.get('alan', '')}: {t.get('skor', '')} ({t.get('seviye', '')})" for t in top3) if top3 else ""

        from utils.ai_rules import inject_rules as _air2
        system_prompt = _air2("""Sen uzman bir egitim psikoloğu ve ogrenci degerlendirme uzmanisin. Turkiye'deki ozel okullarda calisiyorsun.

Gorevlerin:
1. Test sonuclarini profesyonelce analiz et
2. Guclu ve zayif alanlari tespit et
3. Somut, uygulanabilir tavsiyeler ver
4. Haftalik/aylik yol haritasi olustur
5. Veliye sunum icin hazir konusma metni yaz

YANITINI su formatta ver:

## 📊 SONUC ANALIZI
(Test sonuclarinin profesyonel yorumu — guclu/zayif alanlar, dikkat ceken noktalar)

## 💡 GUCLU ALANLAR
(Ogrencinin one cikan yetenekleri ve bunlarin nasil desteklenecegi)

## ⚠️ GELISIM ALANLARI
(Zayif alanlar ve bunlarin neden onemli oldugu)

## 📋 TAVSIYELER
(Her alan icin somut, uygulanabilir 3-5 tavsiye)

## 🗺️ 4 HAFTALIK YOL HARITASI
### Hafta 1: ...
### Hafta 2: ...
### Hafta 3: ...
### Hafta 4: ...

## 🎤 VELIYE SUNUM METNI (60 saniye)
(Hazir konusma — sonuclari veliye nasil anlatacaginiz)

## 🎯 KAYIT SENARYOSU
(Bu test sonuclarina gore veli ikna senaryosu olustur. Su basliklarda yaz:)
### Acilis Cumlesi
(Test sonucuna referansla guven veren 1-2 cumle)
### Ana Mesaj
(Sonuca gore okulun bu ogrenciye ne katacagi — 3-4 cumle)
### Kritik Ikna Noktasi
(Zayif alanlari firsata ceviren 2-3 cumle — "Biz tam da bunu yapiyoruz")
### Itiraz Karsilama
(Veli "dusunecegim" derse hazir 2 cevap)
### Kapatis ve Aksiyon
(Kayit yonlendirme cumlesi + sonraki adim onerisi)
### Aciliyet Yaratan Cumle
(Neden simdi kayit olmali — 1 cumle)

## 📌 SONRAKI ADIMLAR
(Siradaki test onerileri, takip plani, hedefler)

Turkce yaz. Profesyonel ama anlasilir ol. Her oneri somut ve olculebilir olsun.""")

        # Fiyat bilgisi
        fiyat_ozet = ""
        fb = aday.fiyat_bilgi or {}
        if fb:
            gt = fb.get("genel_toplam_final", fb.get("brut_toplam", 0))
            fiyat_ozet = f"\nFIYAT: {float(gt or 0):,.0f} TL | Indirim: %{fb.get('toplam_indirim', 0):.0f}"

        # Ihtiyac analizi
        ihtiyac_ozet = ""
        if aday.ihtiyaclar:
            ihtiyac_ozet = "\nVELI IHTIYACLARI: " + ", ".join(ih.get("kategori", "") for ih in aday.ihtiyaclar[:5])

        user_prompt = f"""OGRENCI: {aday.ogrenci_adi}
KADEME: {aday.kademe} | SINIF: {aday.hedef_sinif or aday.mevcut_sinif}
MEVCUT OKUL: {aday.mevcut_okul} ({aday.okul_turu})
PIPELINE: {aday.asama} | ARAMA: {aday.arama_sayisi} | GORUSME: {aday.gorusme_sayisi}

TEST: {test_adi}
SONUC: {sonuc}

SKORLAR:
{skor_text}

{f"TOP 3 ALAN:{chr(10)}{top3_text}" if top3_text else ""}

{f"NOTLAR: {notlar}" if notlar else ""}{fiyat_ozet}{ihtiyac_ozet}

Bu test sonucunu detayli analiz et, tavsiye ver, 4 haftalik yol haritasi olustur ve kayit senaryosu hazirla."""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=2500,
            temperature=0.7,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        st.error(f"AI analiz hatasi: {e}")
        return ""


def _call_ai_tum_testler_analiz(aday) -> str:
    """Tum test sonuclari icin butunsel AI analizi."""
    try:
        from utils.smarti_helper import _ensure_env, _get_client
        _ensure_env()
        client = _get_client()
        if not client:
            return ""

        # Tum testleri derle
        test_ozet = ""
        for t in aday.testler:
            test_ozet += f"\n### {t.get('test_adi', '')}\n"
            test_ozet += f"Tarih: {str(t.get('tarih', ''))[:10]} | Sonuc: {t.get('sonuc', '')}\n"
            skorlar = t.get("skorlar", {})
            if skorlar:
                for k, v in skorlar.items():
                    test_ozet += f"- {k}: {v}\n"
            top3 = t.get("top3", [])
            if top3:
                test_ozet += "Top 3: " + ", ".join(f'{x.get("alan", "")}: {x.get("skor", "")}' for x in top3) + "\n"
            notlar = t.get("notlar", "")
            if notlar:
                test_ozet += f"Not: {notlar}\n"

        # Ihtiyac analizi
        ihtiyac_ozet = ""
        if aday.ihtiyaclar:
            ihtiyac_ozet = "\n".join(f"- [{ih.get('oncelik', '')}] {ih.get('kategori', '')}: {ih.get('aciklama', '')}" for ih in aday.ihtiyaclar)

        from utils.ai_rules import inject_rules as _air3
        system_prompt = _air3("""Sen uzman bir egitim danismani ve ogrenci degerlendirme uzmanisin. Turkiye'deki ozel okullarda calisiyorsun.

Bir ogrencinin TUM test sonuclarini butunsel olarak analiz edeceksin.

YANITINI su formatta ver:

## 🎯 BUTUNSEL PROFIL ANALIZI
(Ogrencinin genel yetenek profili — testler arasi korelasyon ve oruntu)

## 📊 TEST KARSILASTIRMASI
(Testler arasi guclu/zayif alan karsilastirmasi — tutarlilik analizi)

## 💡 ONE CIKAN YETENEKLER
(Tum testlerde tutarli olan guclu alanlar ve bunlarin anlami)

## ⚠️ ONCELIKLI GELISIM ALANLARI
(En kritik 3-5 gelisim alani — testler arasi ortak zayifliklar)

## 📋 KISISELLESTIRILMIS TAVSIYELER
(Ogrencinin profiline ozel 7-10 somut tavsiye — oncelik sirasina gore)

## 🗺️ 8 HAFTALIK YOL HARITASI
### Hafta 1-2: Temel (...)
### Hafta 3-4: Gelisim (...)
### Hafta 5-6: Pekistirme (...)
### Hafta 7-8: Degerlendirme (...)

## 🎓 EGITIM PROGRAMI ONERISI
(Ogrenci icin ideal ders/aktivite programi — gunluk/haftalik)

## 🎤 VELIYE SUNUM METNI (90 saniye)
(Tum test sonuclarini ozetleyen hazir konusma — guclu/zayif + plan + motivasyon)

## 🎯 KAYIT SENARYOSU (Tam Senaryo)
(Tum test sonuclarina dayali kapsamli kayit ikna senaryosu:)

### 1. GORUSME ACILIS (ilk 2 dakika)
(Test sonuclarina referansla guvenlı acilis — "Testlerimizi tamamladik, cok degerli bilgiler elde ettik" tarzi baslangic + ogrenciye ozel 1-2 pozitif vurgu)

### 2. SONUC SUNUMU (3 dakika)
(Guclu alanlari vurgulayarak sonuclari anlatma — her test icin 1-2 cumle — velinin gurur duyacagi noktalar one ciksin)

### 3. GELISIM FIRSATI (2 dakika)
(Zayif alanlari "firsat" olarak sunma — "Iste tam da burada devreye giriyoruz" mesaji — okulun bu alanlardaki programlari)

### 4. YOL HARITASI SUNUMU (2 dakika)
(8 haftalik plani ozet olarak veliye sunma — somut hedefler ve kontrol noktalari — "ilk 2 haftada su, 4. haftada bu sonuclari gorecegiz")

### 5. KAYIT YONLENDIRME (2 dakika)
(Neden simdi kayit olmali — fiyat/kampanya avantaji varsa vurgula — erken baslamanin onemi — "yerimiz sinirli" aciliyeti)

### 6. ITIRAZ KARSILAMA
- **"Dusunecegiz"** → (hazir cevap)
- **"Baska okullara da bakiyoruz"** → (hazir cevap)
- **"Fiyat yuksek"** → (hazir cevap)
- **"Cocuk istemiyor"** → (hazir cevap)

### 7. KAPATIS CUMLESI
(Son sozu soyleyen cumle — karari kolaylastiran, sıcak ama kararlı kapatis)

## 📌 TAKIP PLANI
(Siradaki olcum tarihleri, hedef metrikler, kontrol noktalari)

Turkce yaz. Profesyonel, butunsel ve somut ol. Kayit senaryosu gercekci, ikna edici ve samimi olsun.""")

        # Fiyat bilgisi
        fiyat_ozet = ""
        fb = aday.fiyat_bilgi or {}
        if fb:
            gt = fb.get("genel_toplam_final", fb.get("brut_toplam", 0))
            fiyat_ozet = f"\nFIYAT BILGISI: Toplam {float(gt or 0):,.0f} TL | Indirim: %{fb.get('toplam_indirim', 0):.0f}"
            taksit_s = fb.get("taksit_sayisi", 0)
            if taksit_s:
                fiyat_ozet += f" | {taksit_s} taksit"

        # Gorusme gecmisi
        gorusme_ozet = ""
        if aday.gorusmeler:
            for gr in aday.gorusmeler[-2:]:
                gorusme_ozet += f"\n- {str(gr.get('tarih', ''))[:10]}: {gr.get('sonuc', '')}"

        user_prompt = f"""OGRENCI: {aday.ogrenci_adi}
KADEME: {aday.kademe} | SINIF: {aday.hedef_sinif or aday.mevcut_sinif}
MEVCUT OKUL: {aday.mevcut_okul} ({aday.okul_turu})
CINSIYET: {aday.cinsiyet}
PIPELINE: {aday.asama} | ARAMA: {aday.arama_sayisi} | GORUSME: {aday.gorusme_sayisi}

UYGULANAN TESTLER ({len(aday.testler)} adet):
{test_ozet}

{f"VELI IHTIYAC ANALIZI:{chr(10)}{ihtiyac_ozet}" if ihtiyac_ozet else "Ihtiyac analizi yapilmamis."}{fiyat_ozet}
{f"SON GORUSMELER:{gorusme_ozet}" if gorusme_ozet else ""}

Tum test sonuclarini butunsel olarak analiz et. Testler arasi korelasyonlari bul. Kisisellestirilmis 8 haftalik yol haritasi olustur. Test sonuclarina dayali kapsamli KAYIT SENARYOSU hazirla.
ONEMLI: Sadece yukaridaki verilere dayan. Veride olmayan bilgi icin yorum YAPMA."""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=3500,
            temperature=0.7,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        st.error(f"AI analiz hatasi: {e}")
        return ""


# ============================================================
# IHTIYAC ANALIZI SEKMESI
# ============================================================

def _render_ihtiyac_analizi(store: KayitDataStore, adaylar: list[KayitAday]):
    """Veli Ihtiyac Analizi — PR modulundeki 32 kategori + Ikna Plani + Belge Onerileri."""
    st.markdown(
        '<div style="background:linear-gradient(135deg,#10b981,#059669);border-radius:12px;'
        'padding:1.2rem 1.5rem;margin-bottom:1rem">'
        '<h3 style="color:#fff;margin:0">🎯 Veli Ihtiyac Analizi</h3>'
        '<p style="color:#d1fae5;margin:0.3rem 0 0 0;font-size:0.9rem">'
        '32 kategoride velinin beklenti ve onceliklerini belirleyin + Ikna Plani + Belge Onerileri</p></div>',
        unsafe_allow_html=True)

    aday = _aday_secici(adaylar, "ihtiyac")
    if not aday:
        st.info("Ihtiyac analizi icin bir aday secin.")
        return

    # PR modulunden veri yapilarini import et
    try:
        from views.halkla_iliskiler_module import (
            NEEDS_CATEGORY_MAP as _NCM,
            IKNA_PLANI_MAP as _IPM,
            SOMUT_BELGELER_ONERILER as _SBO,
        )
    except ImportError:
        _NCM = {}
        _IPM = {}
        _SBO = {}

    # ── Mevcut ihtiyaclar ──
    if aday.ihtiyaclar:
        with st.expander(f"📋 Kayitli Ihtiyaclar ({len(aday.ihtiyaclar)})", expanded=False):
            kat_sayac = Counter(ih.get("kategori", "") for ih in aday.ihtiyaclar)
            for ih in aday.ihtiyaclar:
                onc = ih.get("oncelik", "Orta")
                onc_renk = {"Yuksek": "#f87171", "Orta": "#fbbf24", "Dusuk": "#4ade80"}.get(onc, "#94a3b8")
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:8px;padding:6px 10px;margin:3px 0;'
                    f'background:#10b98108;border:1px solid #10b98120;border-radius:6px;border-left:3px solid {onc_renk}">'
                    f'<span style="color:{onc_renk};font-weight:700;min-width:60px;font-size:0.75rem">{onc}</span>'
                    f'<span style="color:#6ee7b7;font-weight:600;min-width:120px">{ih.get("kategori", "")}</span>'
                    f'<span style="color:#e2e8f0;flex:1;font-size:0.85rem">{ih.get("aciklama", "")}</span>'
                    f'</div>',
                    unsafe_allow_html=True)
            if len(kat_sayac) > 1:
                st.markdown("")
                st.markdown('<div style="color:#94a3b8;font-weight:600;margin:8px 0">Ihtiyac Dagilimi</div>',
                            unsafe_allow_html=True)
                max_v = max(kat_sayac.values())
                for kat, cnt in kat_sayac.most_common(10):
                    pct = int(cnt / max_v * 100)
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:8px;margin:3px 0">'
                        f'<span style="min-width:140px;font-size:0.8rem;color:#94a3b8">{kat}</span>'
                        f'<div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden">'
                        f'<div style="width:{pct}%;height:100%;background:#10b981;border-radius:4px"></div></div>'
                        f'<span style="min-width:20px;font-size:0.75rem;color:#6ee7b7;font-weight:700">{cnt}</span></div>',
                        unsafe_allow_html=True)

    # ── 32 Kategori Secimi (Gruplu Checkbox) ──
    st.markdown("---")
    ihtiyac_items = list(_NCM.keys()) if _NCM else list(IHTIYAC_KATEGORILERI)
    candidate_key = f"km_ih_{aday.id}"

    # Kategorilere gore grupla
    _seen_cats: list[str] = []
    _cat_items: dict[str, list[tuple[int, str]]] = {}
    for idx, item in enumerate(ihtiyac_items):
        cat = _NCM.get(item, "Diger") if _NCM else item
        if cat not in _cat_items:
            _seen_cats.append(cat)
            _cat_items[cat] = []
        _cat_items[cat].append((idx, item))

    selected_ihtiyac_labels: list[str] = []

    with st.expander("📝 Ihtiyac Konularini Sec (32 Kategori)", expanded=True):
        _iht_colors = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#3b82f6", "#ec4899", "#6366f1"]
        for cat_idx, cat_name in enumerate(_seen_cats):
            _c = _iht_colors[cat_idx % len(_iht_colors)]
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{_c}18,{_c}08);border-left:4px solid {_c};'
                f'border-radius:8px;padding:.6rem 1rem;margin:.8rem 0 .4rem 0;">'
                f'<span style="font-weight:800;font-size:.95rem;color:{_c};">{cat_name}</span>'
                f'<span style="font-size:.78rem;color:#94a3b8;margin-left:.5rem;">({len(_cat_items[cat_name])})</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            _iht_cols = st.columns(2)
            for ci, (idx, item) in enumerate(_cat_items[cat_name]):
                checkbox_key = f"{candidate_key}_ihtiyac_{idx}"
                with _iht_cols[ci % 2]:
                    if st.checkbox(item, key=checkbox_key):
                        selected_ihtiyac_labels.append(item)

        if selected_ihtiyac_labels:
            _sel_cats = list(dict.fromkeys(_NCM.get(l, "Diger") for l in selected_ihtiyac_labels))
            _pills = " ".join(
                f'<span style="background:linear-gradient(135deg,#059669,#047857);color:#fff;'
                f'padding:4px 12px;border-radius:20px;font-size:.82rem;font-weight:600;">{c}</span>'
                for c in _sel_cats
            )
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#052e16,#052e16);border-radius:10px;'
                f'padding:.8rem 1rem;margin-top:.8rem;border:1px solid #6ee7b7;'
                f'display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;">'
                f'<strong style="color:#6ee7b7;font-size:.9rem;">✅ Seçilen:</strong> {_pills}'
                f'</div>',
                unsafe_allow_html=True,
            )

        ihtiyac_note = st.text_area(
            "Ek Not",
            key=f"{candidate_key}_ihtiyac_note",
            placeholder="Velinin ozellikle belirttigi konular...",
            height=60,
        )

    # ── Kaydet butonu ──
    if selected_ihtiyac_labels:
        if st.button("💾 Secilen Ihtiyaclari Kaydet", type="primary", key=f"{candidate_key}_save", use_container_width=True):
            tum = store.load_all()
            for a in tum:
                if a.id == aday.id:
                    for label in selected_ihtiyac_labels:
                        cat = _NCM.get(label, label) if _NCM else label
                        a.ihtiyaclar.append({
                            "kategori": cat,
                            "aciklama": label,
                            "oncelik": "Yuksek",
                            "tarih": datetime.now().isoformat(),
                        })
                    if ihtiyac_note:
                        a.ihtiyaclar.append({
                            "kategori": "Genel Not",
                            "aciklama": ihtiyac_note,
                            "oncelik": "Orta",
                            "tarih": datetime.now().isoformat(),
                        })
                    a.son_islem_tarihi = date.today().isoformat()
                    break
            store.save_all(tum)
            st.success(f"{len(selected_ihtiyac_labels)} ihtiyac kaydedildi!")
            st.rerun()

    # ── Veli Ikna Plani ──
    if selected_ihtiyac_labels and _IPM:
        with st.expander("🎯 Veli Ikna Plani", expanded=False):

            selected_categories_for_plan = [_NCM.get(label, "Diger") for label in selected_ihtiyac_labels]

            # Profil ozeti
            st.markdown(
                f'<div style="background:#0f172a;border:1px solid #14b8a6;border-radius:10px;padding:1rem;margin-bottom:1rem">'
                f'<strong style="color:#5eead4;font-size:1rem">📊 Veli Profili — Oncelikli {len(selected_categories_for_plan)} konu</strong></div>',
                unsafe_allow_html=True)
            _plan_pills = " ".join(
                f'<span style="background:linear-gradient(135deg,#0d9488,#14b8a6);color:#fff;'
                f'padding:4px 14px;border-radius:20px;font-size:.85rem;font-weight:600;">{c}</span>'
                for c in selected_categories_for_plan
            )
            st.markdown(f'<div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:1rem;">{_plan_pills}</div>',
                        unsafe_allow_html=True)

            st.markdown(
                '<div style="background:#172554;border-left:4px solid #3b82f6;border-radius:0 10px 10px 0;'
                'padding:10px 14px;margin-bottom:1rem"><strong style="color:#93c5fd">🗣️ Konusma Plani</strong>'
                '<span style="color:#94a3b8;font-size:0.8rem;margin-left:8px">Kategori bazli ikna stratejileri</span></div>',
                unsafe_allow_html=True)

            _ikna_colors = ["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#3b82f6"]
            for idx, label in enumerate(selected_ihtiyac_labels, 1):
                category = _NCM.get(label, "Diger")
                plan = _IPM.get(category, {})
                if not plan:
                    continue

                baslik = plan.get("baslik", f"📌 {category}")
                ana_mesaj = plan.get("ana_mesaj", "")
                konusma_noktalari = plan.get("konusma_noktalari", [])
                sorular = plan.get("sorular", [])
                itiraz_cevaplari = plan.get("itiraz_cevaplari", {})

                _ikna_c = _ikna_colors[(idx - 1) % len(_ikna_colors)]
                st.markdown(
                    f'<div style="background:#0f172a;color:#e2e8f0;border:1px solid #e2e8f0;border-left:5px solid {_ikna_c};'
                    f'border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1rem;'
                    f'box-shadow:0 4px 12px rgba(0,0,0,.06);">'
                    f'<div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.6rem;">'
                    f'<span style="background:{_ikna_c};color:#fff;width:30px;height:30px;border-radius:50%;'
                    f'display:inline-flex;align-items:center;justify-content:center;font-size:.85rem;font-weight:800;">{idx}</span>'
                    f'<strong style="font-size:1.05rem;color:#94A3B8;">{baslik}</strong></div>'
                    f'<div style="padding:.6rem .8rem;background:linear-gradient(135deg,{_ikna_c}08,{_ikna_c}15);'
                    f'border-radius:8px;font-style:italic;color:#7dd3fc;font-size:.92rem;'
                    f'border-left:3px solid {_ikna_c};">'
                    f'💬 "{ana_mesaj}"</div></div>',
                    unsafe_allow_html=True,
                )

                if konusma_noktalari:
                    st.markdown("**✅ Konusulacak Noktalar:**")
                    for nokta in konusma_noktalari:
                        st.markdown(f"- {nokta}")

                if sorular:
                    st.markdown("**❓ Veliye Sorulacak:**")
                    for soru in sorular:
                        st.markdown(f"- *{soru}*")

                if itiraz_cevaplari:
                    with st.expander(f"🛡️ Olasi Itirazlar ve Cevaplar", expanded=False):
                        for itiraz, cevap in itiraz_cevaplari.items():
                            st.markdown(f"**Itiraz:** *\"{itiraz}\"*")
                            st.markdown(f"**Cevap:** {cevap}")
                            st.markdown("---")

                st.markdown("---")

            # Genel tavsiyeler
            st.markdown(
                '<div style="background:#422006;border-left:4px solid #f59e0b;border-radius:0 10px 10px 0;'
                'padding:10px 14px;margin-bottom:1rem"><strong style="color:#fbbf24">💎 Genel Tavsiyeler</strong></div>',
                unsafe_allow_html=True)
            _tavsiye_items = [
                ("Dinleyin", "Velinin endiselerini tam olarak anlamadan cevap vermeyin", "#f59e0b"),
                ("Odaklanin", "Sadece secilen konularda derinlesin, digerlerini atlayin", "#3b82f6"),
                ("Somutlastirin", "Ornekler ve basari hikayeleri paylasin", "#10b981"),
                ("Sorular sorun", "Velinin gercek ihtiyacini kesfedin", "#8b5cf6"),
                ("Not alin", "Velinin soylediklerini kaydedin", "#3b82f6"),
            ]
            _tavsiye_html = '<div style="display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:1rem;">'
            for _tv_baslik, _tv_aciklama, _tv_renk in _tavsiye_items:
                _tavsiye_html += (
                    f'<div style="flex:1;min-width:180px;background:#0f172a;color:#e2e8f0;border:1px solid #e2e8f0;'
                    f'border-top:3px solid {_tv_renk};border-radius:10px;padding:.8rem;'
                    f'box-shadow:0 2px 8px rgba(0,0,0,.04);">'
                    f'<strong style="color:{_tv_renk};font-size:.9rem;">{_tv_baslik}</strong>'
                    f'<div style="font-size:.82rem;color:#94a3b8;margin-top:.3rem;">{_tv_aciklama}</div></div>'
                )
            _tavsiye_html += '</div>'
            st.markdown(_tavsiye_html, unsafe_allow_html=True)

            # Atlanacak konular
            tum_kategoriler = set(_NCM.values())
            secilen_kategoriler_set = set(selected_categories_for_plan)
            atlanacak = tum_kategoriler - secilen_kategoriler_set

            st.markdown(
                '<div style="background:#450a0a;border-left:4px solid #ef4444;border-radius:0 10px 10px 0;'
                'padding:10px 14px;margin-bottom:1rem"><strong style="color:#f87171">🚫 Bu Gorusmede Atlanacak Konular</strong></div>',
                unsafe_allow_html=True)
            if atlanacak:
                _atl_pills = " ".join(
                    f'<span style="background:rgba(239,68,68,.1);color:#dc2626;padding:4px 12px;'
                    f'border-radius:20px;font-size:.82rem;font-weight:600;border:1px solid rgba(239,68,68,.2);">{k}</span>'
                    for k in sorted(atlanacak)
                )
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,#fef2f2,#450a0a);border:1px solid #ef444440;'
                    f'border-left:5px solid #ef4444;border-radius:12px;padding:1rem 1.2rem;">'
                    f'<strong style="color:#f87171;font-size:.92rem;">Bu konular velinin oncelikleri arasinda degil:</strong>'
                    f'<div style="display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.5rem;">{_atl_pills}</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.success("Tum konular velinin oncelikleri arasinda.")

    elif not selected_ihtiyac_labels:
        st.info("💡 Ihtiyac Analizi yapildiginda kisisellestirilmis **Veli Ikna Plani** burada gorunecektir.")

    # ── Belge Onerileri ──
    if selected_ihtiyac_labels and _SBO:
        with st.expander("📂 Somut Belge Onerileri", expanded=False):
            st.markdown(
                '<div style="background:#172554;border-left:4px solid #3b82f6;border-radius:0 10px 10px 0;'
                'padding:10px 14px;margin-bottom:1rem"><strong style="color:#93c5fd">📋 Onerilen Belgeler</strong>'
                '<span style="color:#94a3b8;font-size:0.8rem;margin-left:8px">Velinin ihtiyaclarina gore hazirlama onerileri</span></div>',
                unsafe_allow_html=True)

            for label in selected_ihtiyac_labels:
                category = _NCM.get(label, "Diger")
                belgeler = _SBO.get(category, [])
                if belgeler:
                    st.markdown(f"**{category}:**")
                    for belge in belgeler:
                        belge_adi = belge.get("belge", "")
                        aciklama = belge.get("aciklama", "")
                        st.markdown(
                            f'<div style="display:flex;align-items:center;gap:8px;padding:6px 10px;margin:3px 0;'
                            f'background:#1e293b;border:1px solid #334155;border-radius:6px">'
                            f'<span style="color:#60a5fa;font-weight:600;min-width:180px">📄 {belge_adi}</span>'
                            f'<span style="color:#94a3b8;font-size:0.85rem">{aciklama}</span></div>',
                            unsafe_allow_html=True)

    # ── AI Destekli Gorusme Sureci ──
    if selected_ihtiyac_labels and aday:
        _render_ai_gorusme_sureci(aday, selected_ihtiyac_labels, _NCM)
    elif aday.ihtiyaclar and not selected_ihtiyac_labels:
        # Kayitli ihtiyaclar varsa, onlarla AI calistir
        kayitli_labels = [ih.get("aciklama", ih.get("kategori", "")) for ih in aday.ihtiyaclar]
        _render_ai_gorusme_sureci(aday, kayitli_labels, _NCM)


def _render_ai_gorusme_sureci(aday: KayitAday, selected_labels: list[str], ncm: dict):
    """AI destekli gorusme sureci tasarimi — ihtiyac analizine gore kisisellestirilmis."""

    st.markdown("---")
    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed 0%,#4f46e5 50%,#2563eb 100%);'
        'border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1rem">'
        '<h3 style="color:#fff;margin:0">🤖 AI Destekli Gorusme Sureci</h3>'
        '<p style="color:#c7d2fe;margin:0.3rem 0 0 0;font-size:0.9rem">'
        'Ihtiyac analizine gore kisisellestirilmis gorusme stratejisi, konusma plani ve AI tavsiyeleri</p></div>',
        unsafe_allow_html=True)

    # Kategori ozeti
    kategoriler = [ncm.get(l, l) for l in selected_labels]
    kat_text = ", ".join(kategoriler)
    st.markdown(
        f'<div style="background:#1e1b4b;border:1px solid #6366f1;border-radius:10px;padding:1rem;margin-bottom:1rem">'
        f'<strong style="color:#a5b4fc">Veli Oncelikleri:</strong> '
        f'<span style="color:#e2e8f0">{kat_text}</span></div>',
        unsafe_allow_html=True)

    ai_key = f"km_ai_gorusme_{aday.id}"
    result_key = f"{ai_key}_result"

    if st.button("🤖 AI ile Gorusme Sureci Olustur", type="primary", key=ai_key, use_container_width=True):
        with st.spinner("AI gorusme sureci hazirlaniyor..."):
            ai_result = _call_ai_gorusme_plani(aday, selected_labels, kategoriler)
            if ai_result:
                st.session_state[result_key] = ai_result

    # Sonuc goster
    ai_result = st.session_state.get(result_key, "")
    if ai_result:
        # Bolum bolum render et
        _render_ai_result(ai_result)


def _call_ai_gorusme_plani(aday: KayitAday, selected_labels: list[str], kategoriler: list[str]) -> str:
    """OpenAI GPT-4o-mini ile kisisellestirilmis gorusme plani olustur."""
    try:
        from utils.smarti_helper import _ensure_env, _get_client
        _ensure_env()
        client = _get_client()
        if not client:
            return ""

        # Test bilgisi ozeti
        test_ozet = ""
        if aday.testler:
            for t in aday.testler:
                test_ozet += f"- {t.get('test_adi', '')}: {t.get('sonuc', '')} ({str(t.get('tarih', ''))[:10]})\n"

        # Arama gecmisi ozeti
        arama_ozet = ""
        if aday.aramalar:
            for ar in aday.aramalar[-3:]:
                arama_ozet += f"- {str(ar.get('tarih', ''))[:10]}: {ar.get('sonuc', '')}\n"

        # Gorusme gecmisi
        gorusme_ozet = ""
        if aday.gorusmeler:
            for gr in aday.gorusmeler[-3:]:
                gorusme_ozet += f"- {str(gr.get('tarih', ''))[:10]}: {gr.get('sonuc', '')}\n"

        # Ihtiyac detaylari
        ihtiyac_detay = "\n".join(f"- {l}" for l in selected_labels)

        # Fiyat bilgisi
        fiyat_ozet = ""
        fb = aday.fiyat_bilgi or {}
        if fb:
            gt = fb.get("genel_toplam_final", fb.get("brut_toplam", 0))
            fiyat_ozet = f"Genel Toplam: {float(gt or 0):,.0f} TL, Indirim: %{fb.get('toplam_indirim', 0):.0f}"

        system_prompt = """Sen bir ozel okul kayit danismanisin. Turkiye'deki ozel okullarda veli gorusmesi yapan uzman bir egitim danismanisin.

Gorevlerin:
1. Velinin ihtiyac analizine gore kisisellestirilmis bir GORUSME SURECI tasarla
2. Adim adim konusma plani hazirla (acilis, ihtiyac derinlestirme, cozum sunumu, ikna, kapatis)
3. Her ihtiyac kategorisi icin spesifik konusma noktalari belirle
4. Olasi itirazlara hazirlikli cevaplar olustur
5. Gorusmenin her asamasi icin sure tavsiyesi ver
6. Velinin profiline ozel taktiksel tavsiyeler sun

YANITINI su formatta ver:

## 🎯 GORUSME STRATEJISI
(Velinin profil ozeti ve genel strateji — 2-3 cumle)

## 📋 GORUSME AKIS PLANI

### 1. ACILIS (5 dk)
(Karsilama, buzkirma, guven olusturma — spesifik cumleler)

### 2. IHTIYAC DERINLESTIRME (10 dk)
(Her kategori icin sorulacak sorular ve dinleme noktalari)

### 3. COZUM SUNUMU (15 dk)
(Her ihtiyaca karsilik okulun sunacagi cozumler — somut ve ikna edici)

### 4. TEST/DEGERLENDIRME SONUCLARI (5 dk)
(Varsa test sonuclarini nasil sunacaginiz)

### 5. FIYAT VE DEGER (5 dk)
(Fiyat sunumu stratejisi — ihtiyaclara gore deger vurgusu)

### 6. ITIRAZ YONETIMI (5 dk)
(Olasi itirazlar ve hazir cevaplar — en az 3 itiraz)

### 7. KAPATIS VE AKSIYON (5 dk)
(Gorusmeyi nasil kapatacaginiz, sonraki adim, randevu/kayit yonlendirme)

## 🎤 60 SANIYE ASANSOR KONUSMASI
(Gorusmenin en kritik aninda kullanilacak 60 saniyelik ikna metni — hazir konusma)

## ⚡ TAKTİKSEL TAVSIYELER
(Bu veliye ozel 5 pratik tavsiye — madde madde)

## ⚠️ DIKKAT EDILECEK NOKTALAR
(Bu gorusmede kacınılmasi gereken 3 hata)

Turkce yaz. Samimi ama profesyonel ol. Somut ve uygulanabilir ol."""

        user_prompt = f"""ADAY BILGILERI:
- Ogrenci: {aday.ogrenci_adi}
- Veli: {aday.veli_adi}
- Kademe: {aday.kademe}
- Mevcut Sinif: {aday.mevcut_sinif}
- Hedef Sinif: {aday.hedef_sinif}
- Mevcut Okul: {aday.mevcut_okul} ({aday.okul_turu})
- Kanal: {aday.kanal}
- Pipeline Asama: {aday.asama}
- Toplam Arama: {aday.arama_sayisi}
- Toplam Gorusme: {aday.gorusme_sayisi}

VELININ IHTIYAC KATEGORILERI ({len(kategoriler)} konu):
{ihtiyac_detay}

KISA KATEGORI ADLARI: {', '.join(kategoriler)}

{"ARAMA GECMISI (son 3):" + chr(10) + arama_ozet if arama_ozet else "Henuz arama yapilmamis."}

{"GORUSME GECMISI (son 3):" + chr(10) + gorusme_ozet if gorusme_ozet else "Henuz gorusme yapilmamis."}

{"TEST SONUCLARI:" + chr(10) + test_ozet if test_ozet else "Henuz test uygulanmamis."}

{"FIYAT BILGISI: " + fiyat_ozet if fiyat_ozet else "Henuz fiyat verilmemis."}

{"GENEL NOTLAR: " + aday.notlar if aday.notlar else ""}

Lutfen bu velinin ihtiyac profiline ozel, adim adim bir gorusme sureci tasarla."""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=3000,
            temperature=0.7,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        import streamlit as _st
        _st.error(f"AI gorusme plani olusturulurken hata: {e}")
        return ""


def _render_ai_result(ai_result: str):
    """AI sonucunu bolum bolum stilize ederek goster."""
    # Bolumleri parcala ve renklendir
    _section_styles = {
        "GORUSME STRATEJISI": ("#7c3aed", "🎯"),
        "GORUSME AKIS PLANI": ("#3b82f6", "📋"),
        "ACILIS": ("#10b981", "👋"),
        "IHTIYAC DERINLESTIRME": ("#0ea5e9", "🔍"),
        "COZUM SUNUMU": ("#8b5cf6", "💡"),
        "TEST": ("#ec4899", "📊"),
        "FIYAT": ("#f59e0b", "💰"),
        "ITIRAZ": ("#ef4444", "🛡️"),
        "KAPATIS": ("#10b981", "🎯"),
        "ASANSOR KONUSMASI": ("#7c3aed", "🎤"),
        "TAKTIKSEL": ("#3b82f6", "⚡"),
        "DIKKAT": ("#ef4444", "⚠️"),
    }

    lines = ai_result.split("\n")
    current_section = ""
    section_content: list[str] = []

    def flush_section():
        nonlocal section_content, current_section
        if not current_section or not section_content:
            section_content = []
            return
        content = "\n".join(section_content)

        # Renk ve ikon bul
        color = "#6366f1"
        icon = "📌"
        for key, (c, i) in _section_styles.items():
            if key in current_section.upper():
                color = c
                icon = i
                break

        is_h2 = current_section.startswith("## ")
        clean_title = current_section.lstrip("#").strip()

        if is_h2:
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{color}20,{color}08);'
                f'border-left:5px solid {color};border-radius:0 12px 12px 0;'
                f'padding:1rem 1.2rem;margin:1.2rem 0 0.6rem 0">'
                f'<strong style="color:{color};font-size:1.1rem">{clean_title}</strong></div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="background:{color}10;border-left:3px solid {color};'
                f'border-radius:0 8px 8px 0;padding:0.6rem 1rem;margin:0.8rem 0 0.4rem 0">'
                f'<strong style="color:{color};font-size:0.95rem">{clean_title}</strong></div>',
                unsafe_allow_html=True)

        # Icerigi render et
        st.markdown(content)
        section_content = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("### "):
            flush_section()
            current_section = stripped
        else:
            section_content.append(line)

    flush_section()


# ============================================================
# ARAMA DESTEK — SORU CEVAP REHBERI
# ============================================================

ARAMA_DESTEK_SORULAR = {
    "numara": {
        "soru": "Telefonumu nereden buldunuz?",
        "cevaplar": [
            "Numaraniz okulumuza daha once yaptiginiz basvuru formundan alinmistir.",
            "Egitim fuari/tanitim etkinliginde doldurdugunuz bilgi formundan gelmektedir.",
            "Web sitemiz uzerinden bilgi talebi formu doldurmusstunuz.",
            "Referans velilerimiz tarafindan tavsiye edildiniz.",
        ],
    },
    "izin": {
        "soru": "Size izin vermedim, neden ariyorsunuz?",
        "cevaplar": [
            "Haklisiniz, rahatsiz ettiysem ozur dilerim. Bilgi formunda iletisim izni onayi vardi, ancak sizi listeden cikarabilirim.",
            "Anliyorum, numaranizi 'aramayin' listesine ekleyebilirim. Bir daha rahatsiz etmeyecegiz.",
        ],
    },
    "ucret": {
        "soru": "Ucretler ne kadar?",
        "cevaplar": [
            "Ucretlerimiz kademe ve secilen ek hizmetlere gore degismektedir. Size ozel bir teklif hazirlamak icin randevu olusturabilir miyim?",
            "Fiyatlarimizi yuz yuze gorusmede detayli olarak acikliyoruz. Boylece ihtiyaclariniza uygun paketi birlikte belirleyebiliriz.",
        ],
    },
    "indirim": {
        "soru": "Indirim var mi? / Burs imkani nedir?",
        "cevaplar": [
            "Erken kayit, kardes, basari ve bursluluk sinavi indirimimiz bulunmaktadir.",
            "Bursluluk sinavimiz ile %100'e varan burs imkani sunuyoruz. Sinav tarihleri icin sizi bilgilendirebilirim.",
            "Kampanya donemlerimizde ozel indirimler uygulanmaktadir. Detaylari gorusmede paylasabilirim.",
        ],
    },
    "fark": {
        "soru": "Sizi diger okullardan farkli kilan ne?",
        "cevaplar": [
            "Sinif mevcutlarimiz dusuk tutularak bireysel ilgi saglanmaktadir.",
            "Deneyimli kadromuz, modern altyapimiz ve guclu akademik programimiz ile fark yaratiyoruz.",
            "Velilerimizle surekli iletisim halindeyiz — duzenli raporlama ve gorusme sistemi uyguluyoruz.",
            "Ogrencilerimizin kisisel gelisimine yonelik rehberlik ve danismanlik hizmeti sunuyoruz.",
        ],
    },
    "akademik": {
        "soru": "Akademik basari durumunuz nedir?",
        "cevaplar": [
            "LGS/YKS sonuclarimiz il ortalamasinin uzerindedir. Detaylari gorusmede paylasiriz.",
            "Ogrencilerimiz ulusal ve uluslararasi yarismalardu duzenli olarak basari elde etmektedir.",
            "Bireysel takip sistemi ile her ogrencinin gelisimini yakindan izliyoruz.",
        ],
    },
    "ogretmen": {
        "soru": "Ogretmenleriniz kimler? Tecrubeli mi?",
        "cevaplar": [
            "Kadromuz alaninda uzman, en az 5+ yil deneyimli ogretmenlerden olusmaktadir.",
            "Ogretmenlerimiz duzenli olarak mesleki gelisim egitimlerine katilmaktadir.",
            "Ogretmen kadromuzu gorusme sirasinda detayli olarak tanitmaktayiz.",
        ],
    },
    "sinif": {
        "soru": "Sinif mevcutlari kac kisi?",
        "cevaplar": [
            "Siniflarimiz en fazla 24 ogrenci ile sinirlidir (kademeye gore degisir).",
            "Dusuk sinif mevcudu ile bireysel ilgi saglamaktayiz.",
        ],
    },
    "servis": {
        "soru": "Servis var mi? Guzergahlar nereler?",
        "cevaplar": [
            "Servis hizmetimiz mevcuttur. Guzergah bilgisini adresinize gore kontrolle paylasiriz.",
            "Servis ucretleri guzergaha gore degismektedir. Detaylari gorusmede aktarabilirim.",
        ],
    },
    "yemek": {
        "soru": "Yemek veriliyor mu? Menu nasil?",
        "cevaplar": [
            "Kahvalti, ogle yemegi ve ara ogun seceneklerimiz mevcuttur.",
            "Diyetisyen kontrolunde, saglikli ve dengeli menu uygulamaktayiz.",
            "Alerjik durumlar icin ozel menu secenegi sunuyoruz.",
        ],
    },
    "guvenlik": {
        "soru": "Guvenlik onlemleriniz nedir?",
        "cevaplar": [
            "7/24 kamera sistemi, giris-cikis kontrolu ve profesyonel guvenlik ekibi bulunmaktadir.",
            "Ziyaretci giris-cikis kayit sistemi uygulanmaktadir.",
            "Acil durum tatbikatlarimiz duzenli olarak yapilmaktadir.",
        ],
    },
    "kayit": {
        "soru": "Kayit icin ne gerekiyor?",
        "cevaplar": [
            "Nufus cuzdani fotokopisi, 2 adet vesikalik fotograf, ogrenim belgesi ve saglik raporu gerekmektedir.",
            "Online on kayit formumuzu doldurabilir, ardindan yuz yuze gorusme ile sureci tamamlayabiliriz.",
        ],
    },
    "gelmek": {
        "soru": "Okulu gezmek istiyorum / Randevu almak istiyorum",
        "cevaplar": [
            "Harika! Size uygun bir gun ve saat belirleyelim. Hangi gunler musait olursunuz?",
            "Okul turumuza katilabilirsiniz. Bu hafta Cumartesi 10:00-12:00 arasi tur duzenliyoruz.",
            "Bireysel gorusme icin randevu olusturuyorum. Adiniz ve iletisim bilgilerinizi alabilir miyim?",
        ],
    },
    "dusunme": {
        "soru": "Dusunecegim / Esimle konusacagim",
        "cevaplar": [
            "Tabii ki, bu onemli bir karar. Size bilgi dosyamizi gondereyim, inceleyin.",
            "Anliyorum. Isterseniz esiginizle birlikte okulu ziyaret edebilirsiniz.",
            "Sizi bilgilendirmek icin birKac gun sonra tekrar arayabilir miyim?",
        ],
    },
    "red": {
        "soru": "Ilgilenmiyorum / Baska okula karar verdik",
        "cevaplar": [
            "Anliyorum, saygiyla karsiliyorum. Ileride fikriniz degisirse bize ulasabilirsiniz.",
            "Tercihlerinize saygi duyuyoruz. Iyi gunler dilerim.",
        ],
    },
}


# ============================================================
# OGRENCI KAYIT TAKIP RAPORU PDF
# ============================================================

def _generate_kayit_takip_raporu_pdf(aday: KayitAday) -> bytes | None:
    """Adayin tum asamalarini iceren kapsamli Kayit Takip Raporu PDF."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor
        from utils.shared_data import ensure_turkish_pdf_fonts, load_kurum_profili
        import io

        font_name, font_bold = ensure_turkish_pdf_fonts()
        kp = load_kurum_profili()
        k_adi = kp.get("kurum_adi", "") or kp.get("name", "Kurum")

        buffer = io.BytesIO()
        width, height = A4
        c = canvas.Canvas(buffer, pagesize=A4)

        def safe(val):
            if val is None:
                return "-"
            s = str(val).strip()
            return s if s else "-"

        def new_page():
            c.showPage()
            c.setFont(font_name, 8)
            c.setFillColor(HexColor("#6b7280"))
            c.drawString(2 * cm, height - 1 * cm, f"{k_adi} — Ogrenci Kayit Takip Raporu")
            c.drawRightString(width - 2 * cm, height - 1 * cm, safe(aday.ogrenci_adi))
            return height - 1.8 * cm

        def check_page(y_pos, needed=2.0):
            if y_pos < needed * cm:
                return new_page()
            return y_pos

        def section_header(y_pos, title, color="#7c3aed"):
            y_pos = check_page(y_pos, 2.5)
            c.setFillColor(HexColor(color))
            c.roundRect(1.5 * cm, y_pos - 0.8 * cm, width - 3 * cm, 1 * cm, 5, fill=1, stroke=0)
            c.setFillColor(HexColor("#ffffff"))
            c.setFont(font_bold, 11)
            c.drawString(2 * cm, y_pos - 0.5 * cm, title)
            return y_pos - 1.5 * cm

        def text_line(y_pos, label, value, bold_label=True):
            y_pos = check_page(y_pos)
            if bold_label:
                c.setFont(font_bold, 9)
                c.setFillColor(HexColor("#374151"))
                c.drawString(2 * cm, y_pos, f"{label}:")
                c.setFont(font_name, 9)
                c.drawString(6.5 * cm, y_pos, safe(value))
            else:
                c.setFont(font_name, 9)
                c.setFillColor(HexColor("#374151"))
                c.drawString(2 * cm, y_pos, f"{label}: {safe(value)}")
            return y_pos - 0.45 * cm

        def small_text(y_pos, text, indent=2):
            y_pos = check_page(y_pos)
            c.setFont(font_name, 8)
            c.setFillColor(HexColor("#6b7280"))
            c.drawString(indent * cm, y_pos, safe(text))
            return y_pos - 0.38 * cm

        # ══════════ SAYFA 1 — KAPAK + OGRENCI BILGILERI ══════════
        y = height - 2 * cm

        # Baslik
        c.setFillColor(HexColor("#10b981"))
        c.roundRect(1.5 * cm, y - 1.5 * cm, width - 3 * cm, 2 * cm, 8, fill=1, stroke=0)
        c.setFillColor(HexColor("#ffffff"))
        c.setFont(font_bold, 16)
        c.drawCentredString(width / 2, y - 0.5 * cm, "OGRENCI KAYIT TAKIP RAPORU")
        c.setFont(font_name, 10)
        c.drawCentredString(width / 2, y - 1.1 * cm, k_adi)
        y -= 2.8 * cm

        # Rapor tarihi + durum
        pi = aday.pipeline_info
        c.setFont(font_name, 9)
        c.setFillColor(HexColor("#6b7280"))
        c.drawString(2 * cm, y, f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        c.drawRightString(width - 2 * cm, y, f"Son Durum: {pi.get('label', aday.asama)}")
        y -= 0.8 * cm

        # ── A) Ogrenci ve Veli Bilgileri ──
        y = section_header(y, "A) OGRENCI VE VELI BILGILERI", "#3b82f6")
        y = text_line(y, "Ogrenci Adi", aday.ogrenci_adi)
        y = text_line(y, "Veli Adi", aday.veli_adi)
        y = text_line(y, "Telefon", aday.veli_telefon)
        y = text_line(y, "E-posta", aday.veli_email)
        y = text_line(y, "Kademe", aday.kademe)
        y = text_line(y, "Mevcut Sinif", aday.mevcut_sinif)
        y = text_line(y, "Hedef Sinif", aday.hedef_sinif)
        y = text_line(y, "Cinsiyet", aday.cinsiyet)
        y = text_line(y, "Mevcut Okul", f"{aday.mevcut_okul} ({aday.okul_turu})")
        y = text_line(y, "Kanal", aday.kanal)
        y = text_line(y, "Kampanya", aday.kampanya)
        y -= 0.3 * cm

        # ── B) Pipeline / Surec Ozeti ──
        y = section_header(y, "B) SUREC OZETI", "#8b5cf6")
        y = text_line(y, "Ilk Kayit Tarihi", aday.olusturma_tarihi)
        y = text_line(y, "Son Islem Tarihi", aday.son_islem_tarihi)
        y = text_line(y, "Kapanma Tarihi", aday.kapanma_tarihi)
        y = text_line(y, "Son Durum", pi.get("label", aday.asama))
        y = text_line(y, "Toplam Arama", str(aday.arama_sayisi))
        y = text_line(y, "Toplam Gorusme", str(aday.gorusme_sayisi))
        y = text_line(y, "Toplam Test", str(len(aday.testler)))
        y = text_line(y, "Ihtiyac Kategorisi", str(len(aday.ihtiyaclar)))

        # Surec gunu hesapla
        try:
            d1 = date.fromisoformat(aday.olusturma_tarihi[:10])
            d2 = date.fromisoformat((aday.kapanma_tarihi or aday.son_islem_tarihi)[:10])
            surec_gun = (d2 - d1).days
            y = text_line(y, "Surec Suresi", f"{surec_gun} gun")
        except (ValueError, TypeError):
            pass
        y -= 0.3 * cm

        # ── C) Arama Gecmisi ──
        y = section_header(y, "C) ARAMA GECMISI", "#f59e0b")
        if aday.aramalar:
            for idx, ar in enumerate(aday.aramalar, 1):
                y = check_page(y, 1.2)
                c.setFont(font_bold, 8)
                c.setFillColor(HexColor("#374151"))
                c.drawString(2 * cm, y, f"Arama #{idx}")
                c.setFont(font_name, 8)
                c.drawString(4.5 * cm, y, f"Tarih: {safe(ar.get('tarih', ''))[:16]}")
                c.drawString(10 * cm, y, f"Sonuc: {safe(ar.get('sonuc', ''))}")
                y -= 0.38 * cm
                ar_not = ar.get("not", "") or ar.get("notlar", "")
                if ar_not:
                    y = small_text(y, f"  Not: {str(ar_not)[:100]}", 2.5)
        else:
            y = small_text(y, "Arama kaydi yok.")
        y -= 0.3 * cm

        # ── D) Gorusme Gecmisi ──
        y = section_header(y, "D) GORUSME GECMISI", "#0ea5e9")
        if aday.gorusmeler:
            for idx, gr in enumerate(aday.gorusmeler, 1):
                y = check_page(y, 1.2)
                c.setFont(font_bold, 8)
                c.setFillColor(HexColor("#374151"))
                c.drawString(2 * cm, y, f"Gorusme #{idx}")
                c.setFont(font_name, 8)
                c.drawString(4.5 * cm, y, f"Tarih: {safe(gr.get('tarih', ''))[:16]}")
                c.drawString(10 * cm, y, f"Sonuc: {safe(gr.get('sonuc', ''))}")
                y -= 0.38 * cm
                gr_not = gr.get("not", "") or gr.get("notlar", "")
                if gr_not:
                    y = small_text(y, f"  Not: {str(gr_not)[:100]}", 2.5)
        else:
            y = small_text(y, "Gorusme kaydi yok.")
        y -= 0.3 * cm

        # ── E) Randevu Bilgisi ──
        if aday.randevu_tarihi:
            y = section_header(y, "E) RANDEVU BILGISI", "#14b8a6")
            y = text_line(y, "Randevu Tarihi", aday.randevu_tarihi)
            y = text_line(y, "Randevu Saati", aday.randevu_saati)
            y -= 0.3 * cm

        # ── F) Test Sonuclari ──
        y = section_header(y, "F) TEST SONUCLARI", "#ec4899")
        if aday.testler:
            for idx, test in enumerate(aday.testler, 1):
                y = check_page(y, 1.5)
                c.setFont(font_bold, 9)
                c.setFillColor(HexColor("#374151"))
                c.drawString(2 * cm, y, f"{idx}. {safe(test.get('test_adi', ''))}")
                y -= 0.4 * cm
                c.setFont(font_name, 8)
                c.drawString(2.5 * cm, y, f"Tarih: {safe(test.get('tarih', ''))[:10]}  |  Sonuc: {safe(test.get('sonuc', ''))}")
                y -= 0.38 * cm
                # Skorlar
                skorlar = test.get("skorlar", {})
                if skorlar:
                    skor_text = " | ".join(f"{k}: {v}" for k, v in skorlar.items())
                    # Wrap long text
                    max_chars = 95
                    for i in range(0, len(skor_text), max_chars):
                        y = small_text(y, f"  {skor_text[i:i+max_chars]}", 2.5)
                # Top3
                top3 = test.get("top3", [])
                if top3:
                    t3_text = " | ".join(f'{t.get("alan", "")}: {t.get("skor", "")} ({t.get("seviye", "")})' for t in top3)
                    y = small_text(y, f"  Top 3: {t3_text}", 2.5)
                # Notlar
                notlar = test.get("notlar", "")
                if notlar:
                    for i in range(0, len(str(notlar)), 95):
                        y = small_text(y, f"  Not: {str(notlar)[i:i+95]}", 2.5)
                y -= 0.15 * cm
        else:
            y = small_text(y, "Test kaydi yok.")
        y -= 0.3 * cm

        # ── G) Ihtiyac Analizi ──
        y = section_header(y, "G) VELI IHTIYAC ANALIZI", "#10b981")
        if aday.ihtiyaclar:
            for ih in aday.ihtiyaclar:
                y = check_page(y, 0.8)
                onc = ih.get("oncelik", "Orta")
                kat = ih.get("kategori", "")
                aciklama = ih.get("aciklama", "")
                c.setFont(font_name, 8)
                c.setFillColor(HexColor("#374151"))
                text = f"[{onc}] {kat}"
                if aciklama:
                    text += f" — {aciklama[:80]}"
                c.drawString(2 * cm, y, text)
                y -= 0.38 * cm
        else:
            y = small_text(y, "Ihtiyac analizi yapilmamis.")
        y -= 0.3 * cm

        # ── H) Fiyat Bilgisi ──
        fb = aday.fiyat_bilgi or {}
        if fb:
            y = section_header(y, "H) FIYAT BILGISI", "#a78bfa")
            y = text_line(y, "Liste Fiyati", f'{fb.get("liste_fiyati", 0):,.0f} TL')
            y = text_line(y, "Toplam Indirim", f'%{fb.get("toplam_indirim", 0):.0f}')
            ind_detay = fb.get("indirim_detay", "")
            if ind_detay:
                y = text_line(y, "Indirim Detay", str(ind_detay)[:80])
            y = text_line(y, "KDV Dahil", f'{fb.get("kdv_dahil", 0):,.0f} TL')
            y = text_line(y, "Pesinat", f'{fb.get("pesinat", 0):,.0f} TL')
            taksit_s = fb.get("taksit_sayisi", 0)
            taksit_t = fb.get("taksit_tutari", 0)
            if taksit_s:
                y = text_line(y, "Taksit", f'{taksit_s} x {taksit_t:,.0f} TL/ay')
            # Ek hizmetler
            ek = aday.ek_hizmetler or {}
            if ek and ek.get("toplam", 0) > 0:
                y = text_line(y, "Ek Hizmetler", f'{ek.get("kdv_dahil", ek.get("toplam", 0)):,.0f} TL')
            # Genel toplam
            gt = fb.get("genel_toplam_final", fb.get("brut_toplam", 0))
            if gt:
                y = check_page(y, 1)
                c.setFont(font_bold, 10)
                c.setFillColor(HexColor("#10b981"))
                c.drawString(2 * cm, y, f"GENEL TOPLAM: {float(gt):,.0f} TL")
                y -= 0.6 * cm
            y -= 0.3 * cm

        # ── I) Sozlesme Bilgisi ──
        sb = aday.sozlesme_bilgi or {}
        if sb:
            y = section_header(y, "I) SOZLESME BILGISI", "#38bdf8")
            y = text_line(y, "Sozlesme Tarihi", sb.get("sozlesme_tarihi", ""))
            y = text_line(y, "Toplam Ucret", f'{float(sb.get("toplam_ucret", 0)):,.0f} TL' if sb.get("toplam_ucret") else "-")
            y = text_line(y, "Odeme Sekli", sb.get("odeme_sekli", ""))
            y = text_line(y, "Kayit Sonucu", sb.get("kayit_sonucu", ""))
            y -= 0.3 * cm

        # ── J) Notlar ──
        if aday.notlar:
            y = section_header(y, "J) GENEL NOTLAR", "#6b7280")
            for i in range(0, len(aday.notlar), 95):
                y = small_text(y, aday.notlar[i:i + 95])
            y -= 0.3 * cm

        # ── Footer ──
        y = check_page(y, 2)
        c.setFillColor(HexColor("#d1d5db"))
        c.line(2 * cm, y, width - 2 * cm, y)
        y -= 0.6 * cm
        c.setFont(font_name, 8)
        c.setFillColor(HexColor("#6b7280"))
        c.drawCentredString(width / 2, y, f"SmartCampus AI — Ogrenci Kayit Takip Raporu — {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        y -= 0.4 * cm
        c.drawCentredString(width / 2, y, "Bu rapor adayin sisteme kayit oldugu andaki son durumu yansitmaktadir.")

        c.save()
        return buffer.getvalue()

    except Exception:
        return None


# ============================================================
# SINIF LISTESINE AKTARIM
# ============================================================

def _sinif_listesine_aktar(aday: KayitAday, sinif: str, sube: str, numara: str):
    """Kayit olan ogrenciyi KOI > Iletisim > Sinif Listelerine (students.json) aktarir."""
    import json
    import os
    import uuid as _uuid
    from utils.tenant import get_data_path
    from utils.shared_data import load_shared_students

    stu_path = get_data_path("akademik", "students.json")
    os.makedirs(os.path.dirname(stu_path), exist_ok=True)

    # Mevcut ogrencileri yukle
    try:
        with open(stu_path, "r", encoding="utf-8") as f:
            stu_data = json.load(f)
        if not isinstance(stu_data, list):
            stu_data = stu_data.get("students", stu_data.get("records", []))
    except Exception:
        stu_data = []

    # Tekrar kontrolu: ayni sinif/sube/numara var mi?
    for s in stu_data:
        if (s.get("sinif") == sinif and s.get("sube") == sube
                and str(s.get("numara", "")) == numara):
            return  # Zaten kayitli

    # Ad/soyad ayir
    name_parts = aday.ogrenci_adi.strip().rsplit(" ", 1)
    ad = name_parts[0] if len(name_parts) > 1 else aday.ogrenci_adi
    soyad = name_parts[-1] if len(name_parts) > 1 else ""

    # Cinsiyet normalize
    cin_raw = (aday.cinsiyet or "").lower()
    cinsiyet = ""
    if cin_raw in ("kiz", "kız"):
        cinsiyet = "kiz"
    elif cin_raw == "erkek":
        cinsiyet = "erkek"

    yeni_ogr = {
        "id": f"stu_{_uuid.uuid4().hex[:8]}",
        "tc_no": "",
        "ad": ad,
        "soyad": soyad,
        "sinif": sinif,
        "sube": sube,
        "numara": numara,
        "cinsiyet": cinsiyet,
        "dogum_tarihi": "",
        "dogum_yeri": "",
        "uyruk": "T.C.",
        "anne_adi": "", "anne_soyadi": "",
        "anne_telefon": "", "anne_email": "",
        "anne_meslek": "",
        "baba_adi": "", "baba_soyadi": "",
        "baba_telefon": "", "baba_email": "",
        "baba_meslek": "",
        "veli_adi": aday.veli_adi,
        "veli_cinsiyet": "",
        "veli_telefon": aday.veli_telefon,
        "veli_email": aday.veli_email,
        "adres": "",
        "il": "", "ilce": "",
        "ogrenci_telefon": "",
        "ogrenci_email": "",
        "geldigi_okul": aday.mevcut_okul,
        "kan_grubu": "", "saglik_notu": "",
        "durum": "aktif",
        "kaynak": "kayit_modulu",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }

    stu_data.append(yeni_ogr)
    with open(stu_path, "w", encoding="utf-8") as f:
        json.dump(stu_data, f, ensure_ascii=False, indent=2)


# ============================================================
# KAYIT OLANLAR
# ============================================================

def _render_kayit_olanlar(store: KayitDataStore, adaylar: list[KayitAday]):
    kayitlilar = [a for a in adaylar if a.asama == "kesin_kayit"]

    st.markdown(
        f'<div style="background:#052e16;border-left:4px solid #4ade80;border-radius:0 10px 10px 0;'
        f'padding:12px 16px;margin-bottom:14px">'
        f'<strong style="color:#4ade80;font-size:1rem">✅ Kesin Kayit Olan Ogrenciler ({len(kayitlilar)})</strong></div>',
        unsafe_allow_html=True)

    if not kayitlilar:
        styled_info_banner("Henuz kesin kayit olan ogrenci yok.", "info")
        return

    # Ozet metrikler
    toplam_ucret = sum(float(a.fiyat_bilgi.get("genel_toplam_final", a.fiyat_bilgi.get("brut_toplam", 0)) or 0) for a in kayitlilar)
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(
            f'<div style="background:#052e16;border:1px solid #4ade8040;border-radius:10px;padding:12px;text-align:center">'
            f'<div style="font-size:1.8rem;font-weight:800;color:#4ade80">{len(kayitlilar)}</div>'
            f'<div style="font-size:0.75rem;color:#94a3b8">Toplam Kayit</div></div>',
            unsafe_allow_html=True)
    with mc2:
        st.markdown(
            f'<div style="background:#172554;border:1px solid #60a5fa40;border-radius:10px;padding:12px;text-align:center">'
            f'<div style="font-size:1.4rem;font-weight:800;color:#60a5fa">{toplam_ucret:,.0f} TL</div>'
            f'<div style="font-size:0.75rem;color:#94a3b8">Toplam Ucret</div></div>',
            unsafe_allow_html=True)
    with mc3:
        bu_ay = sum(1 for a in kayitlilar if a.kapanma_tarihi and a.kapanma_tarihi[:7] == date.today().strftime("%Y-%m"))
        st.markdown(
            f'<div style="background:#422006;border:1px solid #fbbf2440;border-radius:10px;padding:12px;text-align:center">'
            f'<div style="font-size:1.8rem;font-weight:800;color:#fbbf24">{bu_ay}</div>'
            f'<div style="font-size:0.75rem;color:#94a3b8">Bu Ay Kayit</div></div>',
            unsafe_allow_html=True)

    st.markdown("")

    # Kayitli ogrenci listesi
    for a in sorted(kayitlilar, key=lambda x: x.kapanma_tarihi or "", reverse=True):
        fb = a.fiyat_bilgi or {}
        sb = a.sozlesme_bilgi or {}
        ucret = float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0)

        st.markdown(
            f'<div style="background:#052e16;border:1px solid #4ade8030;border-left:4px solid #4ade80;'
            f'border-radius:0 10px 10px 0;padding:12px 16px;margin:6px 0">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'
            f'<div>'
            f'<div style="font-weight:800;color:#f1f5f9;font-size:1rem">✅ {a.ogrenci_adi}</div>'
            f'<div style="font-size:0.85rem;color:#94a3b8;margin-top:2px">'
            f'👤 {a.veli_adi} | 📞 {a.veli_telefon or "-"} | 🎓 {a.kademe or "-"} {a.hedef_sinif or ""}</div></div>'
            f'<div style="text-align:right">'
            f'<div style="color:#4ade80;font-weight:700">💰 {ucret:,.0f} TL</div>'
            f'<div style="font-size:0.8rem;color:#94a3b8">📅 {a.kapanma_tarihi or "-"}</div></div>'
            f'</div>'
            # Detaylar
            f'<div style="margin-top:8px;padding-top:8px;border-top:1px solid #4ade8020;'
            f'font-size:0.8rem;color:#94a3b8">'
            f'Arama: {a.arama_sayisi} | Gorusme: {a.gorusme_sayisi} | '
            f'Test: {len(a.testler)} | Kampanya: {a.kampanya or "-"} | Kanal: {a.kanal or "-"}'
            f'</div></div>',
            unsafe_allow_html=True)

        # Sinif / Sube / Ogrenci No atama
        with st.expander(f"🎓 {a.ogrenci_adi} — Sinif & Sube & Ogrenci No", expanded=not bool(a.ogrenci_no)):
            if a.kayit_sinif and a.kayit_sube and a.ogrenci_no:
                st.markdown(
                    f'<div style="background:#052e16;border:1px solid #4ade8040;border-radius:8px;'
                    f'padding:10px;margin-bottom:8px">'
                    f'<span style="color:#4ade80;font-weight:700;font-size:1rem">'
                    f'🎓 {a.kayit_sinif}-{a.kayit_sube}</span>'
                    f'<span style="color:#94a3b8;margin:0 12px">|</span>'
                    f'<span style="color:#fbbf24;font-weight:700">No: {a.ogrenci_no}</span></div>',
                    unsafe_allow_html=True)
            with st.form(f"km_sinif_{a.id}"):
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    _sinif_val = a.kayit_sinif or a.hedef_sinif or ""
                    sinif_opts = [""] + SINIF_SECENEKLERI
                    sinif_idx = sinif_opts.index(_sinif_val) if _sinif_val in sinif_opts else 0
                    yeni_sinif = st.selectbox("Sinif", sinif_opts, index=sinif_idx, key=f"km_ks_{a.id}")
                with sc2:
                    sube_opts = ["A", "B", "C", "D", "E", "F"]
                    sube_idx = sube_opts.index(a.kayit_sube) if a.kayit_sube in sube_opts else 0
                    yeni_sube = st.selectbox("Sube", sube_opts, index=sube_idx, key=f"km_kb_{a.id}")
                with sc3:
                    yeni_no = st.text_input("Ogrenci No", value=a.ogrenci_no, key=f"km_kn_{a.id}",
                                             placeholder="Orn: 2026001")
                if st.form_submit_button("Kaydet", type="primary", use_container_width=True):
                    if not yeni_sinif or not yeni_sube or not yeni_no.strip():
                        st.error("Sinif, sube ve ogrenci numarasi zorunludur.")
                    else:
                        store.update(a.id, {
                            "kayit_sinif": yeni_sinif,
                            "kayit_sube": yeni_sube,
                            "ogrenci_no": yeni_no,
                        })

                        # --- Sinif Listesine otomatik aktar ---
                        _sinif_listesine_aktar(a, yeni_sinif, yeni_sube, yeni_no.strip())

                        st.success(f"✅ {a.ogrenci_adi}: {yeni_sinif}-{yeni_sube} No:{yeni_no} — Sinif listesine aktarildi!")
                        st.rerun()

        # PDF butonlari
        with st.expander(f"📄 {a.ogrenci_adi} — Belge Indir", expanded=False):
            pc1, pc2, pc3, pc4 = st.columns(4)
            with pc1:
                if a.sozlesme_bilgi:
                    _pdf_s = _generate_meb_sozlesme_pdf(a)
                    if _pdf_s:
                        st.download_button("📄 Sozlesme PDF", data=_pdf_s,
                                           file_name=f"Sozlesme_{a.ogrenci_adi.replace(' ', '_')}.pdf",
                                           mime="application/pdf", key=f"km_ko_spdf_{a.id}", use_container_width=True)
            with pc2:
                if a.fiyat_bilgi:
                    _pdf_f = _generate_fiyat_pdf(a, "tam")
                    if _pdf_f:
                        st.download_button("📄 Fiyat PDF", data=_pdf_f,
                                           file_name=f"Fiyat_{a.ogrenci_adi.replace(' ', '_')}.pdf",
                                           mime="application/pdf", key=f"km_ko_fpdf_{a.id}", use_container_width=True)
            with pc3:
                _pdf_takip = _generate_kayit_takip_raporu_pdf(a)
                if _pdf_takip:
                    st.download_button("📊 Kayit Takip Raporu", data=_pdf_takip,
                                       file_name=f"KayitTakipRaporu_{a.ogrenci_adi.replace(' ', '_')}.pdf",
                                       mime="application/pdf", key=f"km_ko_takip_{a.id}", use_container_width=True)
            with pc4:
                st.markdown(
                    f'<div style="background:#111827;border-radius:6px;padding:8px;font-size:0.8rem;color:#94a3b8">'
                    f'<strong style="color:#e2e8f0">Surec Ozeti:</strong><br>'
                    f'{a.arama_sayisi} arama → {a.gorusme_sayisi} gorusme → Kayit ✅</div>',
                    unsafe_allow_html=True)


# ============================================================
# OGRENCI BILGI ISLEM
# ============================================================

def _render_ogrenci_bilgi_islem(store: KayitDataStore, adaylar: list[KayitAday]):
    """Ogrenci Bilgi Islem — Kademe>Sinif>Sube hiyerarsik secim, 3 bolum: Kimlik + Kayit Surec + Okul Surec."""
    kayitlilar = [a for a in adaylar if a.asama == "kesin_kayit"]

    st.markdown(
        '<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);border-radius:12px;'
        'padding:1.2rem 1.5rem;margin-bottom:1rem">'
        '<h3 style="color:#fff;margin:0">🎓 Ogrenci Bilgi Islem</h3>'
        '<p style="color:#c7d2fe;margin:0.3rem 0 0 0;font-size:0.9rem">'
        'Kademe → Sinif → Sube secimi | Kimlik Bilgileri + Kayit Surecleri + Okul Surecleri + AI Erken Uyari</p></div>',
        unsafe_allow_html=True)

    if not kayitlilar:
        styled_info_banner("Henuz kesin kayit olan ogrenci yok.", "info")
        return

    # Kademe sayilari
    kademe_sayac = Counter(a.kademe or "(Bilinmiyor)" for a in kayitlilar)
    atanmis = sum(1 for a in kayitlilar if a.ogrenci_no)
    mc = st.columns(6)
    _s = [
        (mc[0], "Toplam", len(kayitlilar), "#6366f1"),
        (mc[1], "Anaokulu", kademe_sayac.get("Anaokulu", 0), "#ec4899"),
        (mc[2], "Ilkokul", kademe_sayac.get("Ilkokul", 0), "#f59e0b"),
        (mc[3], "Ortaokul", kademe_sayac.get("Ortaokul", 0), "#3b82f6"),
        (mc[4], "Lise", kademe_sayac.get("Lise", 0), "#8b5cf6"),
        (mc[5], "Atanmis", atanmis, "#10b981"),
    ]
    for col, lbl, val, clr in _s:
        with col:
            st.markdown(
                f'<div style="background:{clr}12;border:2px solid {clr}30;border-radius:10px;'
                f'padding:8px;text-align:center">'
                f'<div style="font-size:1.3rem;font-weight:800;color:{clr}">{val}</div>'
                f'<div style="font-size:0.6rem;color:#94a3b8">{lbl}</div></div>',
                unsafe_allow_html=True)

    # ── KADEME → SINIF → SUBE hiyerarsik secim ──
    st.markdown("")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        sec_kademe = st.selectbox("Kademe", ["Tumu"] + KADEME_SECENEKLERI, key="obi_kademe")
    # Kademeye gore filtrele
    if sec_kademe == "Tumu":
        kademe_filtreli = kayitlilar
    else:
        kademe_filtreli = [a for a in kayitlilar if a.kademe == sec_kademe]

    # Sinif secenekleri (mevcut ogrencilerin siniflarindan)
    sinif_set = sorted(set((a.kayit_sinif or a.hedef_sinif or "") for a in kademe_filtreli if (a.kayit_sinif or a.hedef_sinif)))
    with fc2:
        sec_sinif = st.selectbox("Sinif", ["Tumu"] + sinif_set, key="obi_sinif")
    if sec_sinif != "Tumu":
        sinif_filtreli = [a for a in kademe_filtreli if (a.kayit_sinif or a.hedef_sinif) == sec_sinif]
    else:
        sinif_filtreli = kademe_filtreli

    # Sube secenekleri
    sube_set = sorted(set(a.kayit_sube for a in sinif_filtreli if a.kayit_sube))
    with fc3:
        sec_sube = st.selectbox("Sube", ["Tumu"] + sube_set, key="obi_sube")
    if sec_sube != "Tumu":
        sube_filtreli = [a for a in sinif_filtreli if a.kayit_sube == sec_sube]
    else:
        sube_filtreli = sinif_filtreli

    # Filtrelenmis ogrenci listesi
    filtre_text = f"{sec_kademe}" + (f" > {sec_sinif}" if sec_sinif != "Tumu" else "") + (f" > {sec_sube}" if sec_sube != "Tumu" else "")
    st.caption(f"{filtre_text} — {len(sube_filtreli)} ogrenci")

    if not sube_filtreli:
        styled_info_banner("Bu filtreye uygun ogrenci yok.", "info")
        return

    # Ogrenci listesi + secim
    for a in sorted(sube_filtreli, key=lambda x: x.ogrenci_adi):
        fb_o = a.fiyat_bilgi or {}
        ucret_o = float(fb_o.get("genel_toplam_final", fb_o.get("brut_toplam", 0)) or 0)
        sinif_badge_o = (
            f'<span style="background:#10b981;color:#fff;padding:2px 8px;border-radius:10px;'
            f'font-size:0.7rem;font-weight:700">{a.kayit_sinif}-{a.kayit_sube} No:{a.ogrenci_no}</span>'
            if a.ogrenci_no else
            '<span style="background:#f59e0b;color:#fff;padding:2px 8px;border-radius:10px;'
            'font-size:0.7rem;font-weight:700">Atama Bekliyor</span>'
        )
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;padding:6px 10px;margin:2px 0;'
            f'background:#111827;border:1px solid #1e293b;border-radius:6px;border-left:3px solid #6366f1">'
            f'<span style="color:#e2e8f0;font-weight:700;min-width:140px">{a.ogrenci_adi}</span>'
            f'{sinif_badge_o}'
            f'<span style="color:#94a3b8;font-size:0.78rem">👤 {a.veli_adi} | {a.cinsiyet or "-"} | {a.kademe}</span>'
            f'<span style="color:#64748b;font-size:0.75rem;margin-left:auto">💰 {ucret_o:,.0f} TL</span></div>',
            unsafe_allow_html=True)

    # Ogrenci sec
    ogr_options = ["-- Ogrenci Sec --"] + [
        f"{a.ogrenci_adi} — {a.kayit_sinif or a.hedef_sinif or '?'}{('-' + a.kayit_sube) if a.kayit_sube else ''}"
        for a in sorted(sube_filtreli, key=lambda x: x.ogrenci_adi)
    ]
    sec_ogr = st.selectbox("Ogrenci Detay", ogr_options, key="obi_ogr_sec")
    if sec_ogr == "-- Ogrenci Sec --":
        return

    idx = ogr_options.index(sec_ogr) - 1
    aday = sorted(sube_filtreli, key=lambda x: x.ogrenci_adi)[idx]
    fb = aday.fiyat_bilgi or {}
    toplam_ucret = float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0)

    # ══════════════════════════════════════════════════
    # BASLIK 1: KIMLIK BILGILERI
    # ══════════════════════════════════════════════════
    st.markdown(
        '<div style="background:linear-gradient(135deg,#6366f1,#4f46e5);border-radius:12px;'
        'padding:0.8rem 1.2rem;margin:10px 0">'
        '<h4 style="color:#fff;margin:0">👤 Kimlik Bilgileri</h4></div>',
        unsafe_allow_html=True)

    # Mini sinif/no badge
    sinif_text = f"{aday.kayit_sinif}-{aday.kayit_sube} No:{aday.ogrenci_no}" if aday.ogrenci_no else "Atama Bekliyor"
    sinif_clr = "#10b981" if aday.ogrenci_no else "#f59e0b"

    # Duzenleme formu — Yeni Aday formundaki tum alanlar
    with st.expander("✏️ Bilgileri Duzenle", expanded=not bool(aday.ogrenci_no)):
        with st.form(f"km_obi_edit_{aday.id}"):
            # Sinif / Sube / No
            st.markdown(
                '<div style="background:#10b98110;border-left:3px solid #10b981;border-radius:0 6px 6px 0;'
                'padding:6px 10px;margin:4px 0"><strong style="color:#6ee7b7;font-size:0.9rem">🎓 Sinif Atama</strong></div>',
                unsafe_allow_html=True)
            kc1, kc2, kc3 = st.columns(3)
            with kc1:
                sinif_opts = [""] + SINIF_SECENEKLERI
                _sv = aday.kayit_sinif or aday.hedef_sinif or ""
                e_sinif = st.selectbox("Sinif", sinif_opts, index=sinif_opts.index(_sv) if _sv in sinif_opts else 0,
                                        key=f"obi_sinif_{aday.id}")
            with kc2:
                sube_opts = ["A", "B", "C", "D", "E", "F"]
                e_sube = st.selectbox("Sube", sube_opts,
                                       index=sube_opts.index(aday.kayit_sube) if aday.kayit_sube in sube_opts else 0,
                                       key=f"obi_sube_{aday.id}")
            with kc3:
                e_no = st.text_input("Ogrenci No", value=aday.ogrenci_no, key=f"obi_no_{aday.id}",
                                      placeholder="Orn: 2026001")

            # Veli Bilgileri
            st.markdown(
                '<div style="background:#6366f110;border-left:3px solid #6366f1;border-radius:0 6px 6px 0;'
                'padding:6px 10px;margin:8px 0"><strong style="color:#a5b4fc;font-size:0.9rem">👤 Veli Bilgileri</strong></div>',
                unsafe_allow_html=True)
            vc1, vc2, vc3 = st.columns(3)
            with vc1:
                e_veli = st.text_input("Veli Adi Soyadi", value=aday.veli_adi, key=f"obi_va_{aday.id}")
            with vc2:
                e_tel = st.text_input("Telefon", value=aday.veli_telefon, key=f"obi_vt_{aday.id}")
            with vc3:
                e_email = st.text_input("E-posta", value=aday.veli_email, key=f"obi_ve_{aday.id}")

            # Ogrenci Bilgileri
            st.markdown(
                '<div style="background:#10b98110;border-left:3px solid #10b981;border-radius:0 6px 6px 0;'
                'padding:6px 10px;margin:8px 0"><strong style="color:#6ee7b7;font-size:0.9rem">🎓 Ogrenci Bilgileri</strong></div>',
                unsafe_allow_html=True)
            oc1, oc2, oc3 = st.columns(3)
            with oc1:
                e_ogr = st.text_input("Ogrenci Adi", value=aday.ogrenci_adi, key=f"obi_oa_{aday.id}")
            with oc2:
                cin_opts = [""] + CINSIYET_SECENEKLERI
                e_cin = st.selectbox("Cinsiyet", cin_opts,
                                      index=cin_opts.index(aday.cinsiyet) if aday.cinsiyet in cin_opts else 0,
                                      key=f"obi_cin_{aday.id}")
            with oc3:
                kad_opts = KADEME_SECENEKLERI
                e_kad = st.selectbox("Kademe", kad_opts,
                                      index=kad_opts.index(aday.kademe) if aday.kademe in kad_opts else 0,
                                      key=f"obi_kad_{aday.id}")
            oc4, oc5, oc6 = st.columns(3)
            with oc4:
                ms_opts = [""] + SINIF_SECENEKLERI
                e_ms = st.selectbox("Mevcut Sinif", ms_opts,
                                     index=ms_opts.index(aday.mevcut_sinif) if aday.mevcut_sinif in ms_opts else 0,
                                     key=f"obi_ms_{aday.id}")
            with oc5:
                hs_opts = [""] + SINIF_SECENEKLERI
                e_hs = st.selectbox("Hedef Sinif", hs_opts,
                                     index=hs_opts.index(aday.hedef_sinif) if aday.hedef_sinif in hs_opts else 0,
                                     key=f"obi_hs_{aday.id}")
            with oc6:
                ot_opts = [""] + OKUL_TURU_SECENEKLERI
                e_ot = st.selectbox("Okul Turu", ot_opts,
                                     index=ot_opts.index(aday.okul_turu) if aday.okul_turu in ot_opts else 0,
                                     key=f"obi_ot_{aday.id}")
            e_mokul = st.text_input("Mevcut Okul", value=aday.mevcut_okul, key=f"obi_mo_{aday.id}")

            # Kampanya & Kaynak
            st.markdown(
                '<div style="background:#f59e0b10;border-left:3px solid #f59e0b;border-radius:0 6px 6px 0;'
                'padding:6px 10px;margin:8px 0"><strong style="color:#fde68a;font-size:0.9rem">📢 Kampanya & Kaynak</strong></div>',
                unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            with cc1:
                e_kamp = st.text_input("Kampanya", value=aday.kampanya, key=f"obi_kamp_{aday.id}")
            with cc2:
                kan_opts = KANAL_SECENEKLERI
                e_kanal = st.selectbox("Kanal", kan_opts,
                                        index=kan_opts.index(aday.kanal) if aday.kanal in kan_opts else 0,
                                        key=f"obi_kan_{aday.id}")

            e_notlar = st.text_area("Notlar", value=aday.notlar, key=f"obi_not_{aday.id}", height=68)

            if st.form_submit_button("💾 Bilgileri Kaydet", type="primary", use_container_width=True):
                store.update(aday.id, {
                    "kayit_sinif": e_sinif, "kayit_sube": e_sube, "ogrenci_no": e_no,
                    "veli_adi": e_veli, "veli_telefon": e_tel, "veli_email": e_email,
                    "ogrenci_adi": e_ogr, "cinsiyet": e_cin, "kademe": e_kad,
                    "mevcut_sinif": e_ms, "hedef_sinif": e_hs, "okul_turu": e_ot,
                    "mevcut_okul": e_mokul, "kampanya": e_kamp, "kanal": e_kanal,
                    "notlar": e_notlar,
                })
                st.success("Bilgiler guncellendi!")
                st.rerun()

    # Ozet kimlik karti (salt okunur)
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);border:2px solid #6366f1;'
        f'border-radius:14px;padding:20px;margin:6px 0">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px">'
        f'<div>'
        f'<div style="font-size:1.3rem;font-weight:800;color:#e2e8f0">🎓 {aday.ogrenci_adi}</div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:8px;font-size:0.85rem;color:#94a3b8">'
        f'<span>👤 Veli: <strong style="color:#e2e8f0">{aday.veli_adi}</strong></span>'
        f'<span>📞 {aday.veli_telefon or "-"}</span>'
        f'<span>📧 {aday.veli_email or "-"}</span></div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:6px;font-size:0.85rem;color:#94a3b8">'
        f'<span>🎓 {aday.kademe or "-"}</span>'
        f'<span>📚 {aday.mevcut_sinif or "-"} → {aday.hedef_sinif or "-"}</span>'
        f'<span>{aday.cinsiyet or "-"}</span>'
        f'<span>🏫 {aday.mevcut_okul or "-"} ({aday.okul_turu or "-"})</span>'
        f'<span>📢 {aday.kanal or "-"}</span>'
        f'<span>🏷️ {aday.kampanya or "-"}</span>'
        f'<span>📅 {aday.kapanma_tarihi or "-"}</span>'
        f'<span>💰 {toplam_ucret:,.0f} TL</span></div></div>'
        f'<div style="text-align:center;background:{sinif_clr}18;border:2px solid {sinif_clr};'
        f'border-radius:12px;padding:12px 20px;min-width:140px">'
        f'<div style="font-size:0.7rem;color:{sinif_clr};font-weight:600">SINIF / NO</div>'
        f'<div style="font-size:1.2rem;font-weight:800;color:{sinif_clr};margin-top:4px">{sinif_text}</div>'
        f'</div></div></div>',
        unsafe_allow_html=True)

    # ══════════════════════════════════════════════════
    # BASLIK 2: KAYIT SURECLERI
    # ══════════════════════════════════════════════════
    st.markdown(
        '<div style="background:linear-gradient(135deg,#10b981,#059669);border-radius:12px;'
        'padding:0.8rem 1.2rem;margin:14px 0 10px">'
        '<h4 style="color:#fff;margin:0">📋 Kayit Surecleri</h4></div>',
        unsafe_allow_html=True)

    # ── SUREC METRIK KARTLARI ──
    try:
        surec_gun = (date.today() - date.fromisoformat(aday.olusturma_tarihi[:10])).days
    except (ValueError, TypeError):
        surec_gun = 0

    sm = st.columns(6)
    _mk = [
        (sm[0], "📞 Arama", str(aday.arama_sayisi), "#facc15"),
        (sm[1], "🤝 Gorusme", str(aday.gorusme_sayisi), "#60a5fa"),
        (sm[2], "🧪 Test", str(len(aday.testler)), "#a78bfa"),
        (sm[3], "🎯 Ihtiyac", str(len(aday.ihtiyaclar)), "#10b981"),
        (sm[4], "📅 Surec", f"{surec_gun}g", "#f59e0b"),
        (sm[5], "💰 Ucret", f"{toplam_ucret / 1000:.0f}K", "#ec4899"),
    ]
    for col, lbl, val, clr in _mk:
        with col:
            st.markdown(
                f'<div style="background:{clr}12;border:1px solid {clr}25;border-radius:8px;padding:8px;text-align:center">'
                f'<div style="font-size:1.2rem;font-weight:800;color:{clr}">{val}</div>'
                f'<div style="font-size:0.6rem;color:#94a3b8">{lbl}</div></div>',
                unsafe_allow_html=True)

    # ── TUM SUREC GECMISI (kronolojik) ──
    events: list[dict] = []
    events.append({"tarih": aday.olusturma_tarihi, "tip": "sistem", "emoji": "➕", "renk": "#6366f1",
                   "baslik": "Aday Olarak Kaydedildi", "not": f"Kademe: {aday.kademe} | Kanal: {aday.kanal}"})
    for ar in aday.aramalar:
        events.append({"tarih": ar.get("tarih", ""), "tip": "arama", "emoji": "📞", "renk": "#facc15",
                       "baslik": f'{ar.get("arama_no", "")}. Arama — {ar.get("sonuc", "")}',
                       "not": ar.get("not", "") or ar.get("notlar", "")})
    for gr in aday.gorusmeler:
        events.append({"tarih": gr.get("tarih", ""), "tip": "gorusme", "emoji": "🤝", "renk": "#60a5fa",
                       "baslik": f'{gr.get("gorusme_no", "")}. Gorusme — {gr.get("sonuc", "")}',
                       "not": gr.get("not", "") or gr.get("notlar", "")})
    for t in aday.testler:
        skor_text = " | ".join(f"{k}:{v}" for k, v in t.get("skorlar", {}).items()) if t.get("skorlar") else ""
        events.append({"tarih": t.get("tarih", ""), "tip": "test", "emoji": "🧪", "renk": "#a78bfa",
                       "baslik": f'{t.get("test_adi", "")} — {t.get("sonuc", "")}',
                       "not": f"{skor_text}\n{t.get('notlar', '')}" if skor_text else t.get("notlar", "")})
    if aday.fiyat_bilgi:
        events.append({"tarih": aday.fiyat_bilgi.get("tarih", ""), "tip": "fiyat", "emoji": "💰", "renk": "#a78bfa",
                       "baslik": f"Fiyat Verildi — {toplam_ucret:,.0f} TL",
                       "not": f"Indirim: %{fb.get('toplam_indirim', 0):.0f}"})
    if aday.sozlesme_bilgi:
        events.append({"tarih": aday.sozlesme_bilgi.get("tarih", ""), "tip": "sozlesme", "emoji": "📄", "renk": "#38bdf8",
                       "baslik": "Sozlesme Imzalandi", "not": ""})
    events.append({"tarih": aday.kapanma_tarihi or "", "tip": "kayit", "emoji": "✅", "renk": "#4ade80",
                   "baslik": "KESIN KAYIT TAMAMLANDI", "not": ""})
    events.sort(key=lambda x: x.get("tarih", "") or "0")

    with st.expander(f"📜 Tam Kayit Sureci ({len(events)} adim)", expanded=True):
        for ev in events:
            tarih_str = str(ev["tarih"])[:16].replace("T", " ") if ev["tarih"] else "-"
            not_text = (ev.get("not", "") or "").strip()
            not_html = (
                f'<div style="color:#e2e8f0;font-size:0.8rem;margin-top:3px;padding-left:12px;'
                f'border-left:2px solid {ev["renk"]}30">{not_text}</div>'
                if not_text else ""
            )
            st.markdown(
                f'<div style="padding:8px 12px;margin:3px 0;background:#111827;border:1px solid #1e293b;'
                f'border-radius:8px;border-left:4px solid {ev["renk"]}">'
                f'<div style="display:flex;justify-content:space-between;align-items:center">'
                f'<span style="color:{ev["renk"]};font-weight:700;font-size:0.85rem">{ev["emoji"]} {ev["baslik"]}</span>'
                f'<span style="color:#64748b;font-size:0.72rem">{tarih_str}</span></div>'
                f'{not_html}</div>',
                unsafe_allow_html=True)

    # ── IHTIYAC ANALIZI ──
    if aday.ihtiyaclar:
        with st.expander(f"🎯 Ihtiyac Analizi ({len(aday.ihtiyaclar)})", expanded=False):
            for ih in aday.ihtiyaclar:
                onc = ih.get("oncelik", "Orta")
                onc_clr = {"Yuksek": "#f87171", "Orta": "#fbbf24", "Dusuk": "#4ade80"}.get(onc, "#94a3b8")
                st.markdown(
                    f'<div style="padding:6px 10px;margin:3px 0;background:#111827;border-radius:6px;'
                    f'border-left:3px solid {onc_clr}">'
                    f'<span style="color:{onc_clr};font-weight:700;font-size:0.8rem">[{onc}]</span> '
                    f'<span style="color:#e2e8f0">{ih.get("kategori", "")}</span>'
                    f' — <span style="color:#94a3b8;font-size:0.82rem">{ih.get("aciklama", "")}</span></div>',
                    unsafe_allow_html=True)

    # ── NOTLAR ──
    if aday.notlar:
        with st.expander("📝 Genel Notlar", expanded=False):
            st.markdown(f'<div style="color:#94a3b8;font-size:0.85rem;white-space:pre-wrap">{aday.notlar}</div>',
                        unsafe_allow_html=True)

    # ── AI DESTEKLI KAYIT SUREC ANALIZI (Kayit Surecleri icinde) ──
    st.markdown("")
    ai_key = f"km_obi_ai_{aday.id}"
    result_key = f"{ai_key}_result"

    if st.button("🤖 AI Destekli Kayit Surec Analizi", key=ai_key, type="primary", use_container_width=True):
        with st.spinner("AI tum kayit surecini analiz ediyor..."):
            result = _call_ai_son_analiz(aday)
            if result:
                st.session_state[result_key] = result

    result = st.session_state.get(result_key, "")
    if result:
        _render_ai_result(result)
        pdf_bytes = _generate_ai_analiz_pdf(aday, result)
        if pdf_bytes:
            st.download_button("📥 AI Analiz Raporu PDF", data=pdf_bytes,
                               file_name=f"OgrenciBilgiIslem_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                               mime="application/pdf", key=f"{ai_key}_pdf", use_container_width=True)

    # ══════════════════════════════════════════════════
    # BASLIK 3: OKUL SURECLERI
    # ══════════════════════════════════════════════════
    st.markdown(
        '<div style="background:linear-gradient(135deg,#f59e0b,#d97706);border-radius:12px;'
        'padding:0.8rem 1.2rem;margin:14px 0 10px">'
        '<h4 style="color:#fff;margin:0">🏫 Okul Surecleri</h4>'
        '<p style="color:#fef3c7;margin:2px 0 0;font-size:0.8rem">'
        'Notlar, devamsizlik, sinavlar, rehberlik, kulupler, erken uyari — diger modullerden canli veri</p></div>',
        unsafe_allow_html=True)

    _render_okul_surecleri(aday)

    # ══════════════════════════════════════════════════
    # EN SON: GENEL OGRENCI AI DEGERLENDIRMESI
    # ══════════════════════════════════════════════════
    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed 0%,#4f46e5 40%,#0ea5e9 100%);border-radius:12px;'
        'padding:0.8rem 1.2rem;margin:14px 0 10px">'
        '<h4 style="color:#fff;margin:0">🤖 Genel Ogrenci AI Degerlendirmesi</h4>'
        '<p style="color:#c7d2fe;margin:2px 0 0;font-size:0.8rem">'
        'Kimlik + Kayit Sureci + Okul Surecleri — tum verilerin butunsel AI analizi</p></div>',
        unsafe_allow_html=True)

    genel_ai_key = f"km_obi_genel_ai_{aday.id}"
    genel_result_key = f"{genel_ai_key}_result"

    if st.button("🤖 Genel AI Degerlendirme Olustur", key=genel_ai_key, type="primary", use_container_width=True):
        with st.spinner("AI tum ogrenci verilerini butunsel olarak analiz ediyor..."):
            genel_result = _call_ai_genel_ogrenci_degerlendirme(aday)
            if genel_result:
                st.session_state[genel_result_key] = genel_result

    genel_result = st.session_state.get(genel_result_key, "")
    if genel_result:
        _render_ai_result(genel_result)
        genel_pdf = _generate_ai_analiz_pdf(aday, genel_result)
        if genel_pdf:
            st.download_button("📥 Genel AI Degerlendirme PDF", data=genel_pdf,
                               file_name=f"GenelDegerlendirme_{aday.ogrenci_adi.replace(' ', '_')}.pdf",
                               mime="application/pdf", key=f"{genel_ai_key}_pdf", use_container_width=True)


def _call_ai_genel_ogrenci_degerlendirme(aday: KayitAday) -> str:
    """Kimlik + Kayit Sureci + Okul Surecleri — tum verilerle butunsel AI degerlendirme."""
    try:
        from utils.smarti_helper import _ensure_env, _get_client
        _ensure_env()
        client = _get_client()
        if not client:
            return ""

        ogr_adi = aday.ogrenci_adi or ""

        # ── KIMLIK BILGILERI ──
        kimlik = (
            f"Ogrenci: {aday.ogrenci_adi} | Veli: {aday.veli_adi} | Tel: {aday.veli_telefon}\n"
            f"Kademe: {aday.kademe} | Sinif: {aday.kayit_sinif or aday.hedef_sinif}-{aday.kayit_sube} | No: {aday.ogrenci_no}\n"
            f"Cinsiyet: {aday.cinsiyet} | Mevcut Okul: {aday.mevcut_okul} ({aday.okul_turu})\n"
            f"Kanal: {aday.kanal} | Kampanya: {aday.kampanya}"
        )

        # ── KAYIT SURECI ──
        arama_ozet = ""
        for ar in aday.aramalar:
            not_t = ar.get("not", "") or ""
            arama_ozet += f"- {ar.get('arama_no', '')}. Arama ({str(ar.get('tarih', ''))[:10]}): {ar.get('sonuc', '')}{f' | Not: {not_t}' if not_t else ''}\n"

        gorusme_ozet = ""
        for gr in aday.gorusmeler:
            not_t = gr.get("not", "") or ""
            gorusme_ozet += f"- {gr.get('gorusme_no', '')}. Gorusme ({str(gr.get('tarih', ''))[:10]}): {gr.get('sonuc', '')}{f' | Not: {not_t}' if not_t else ''}\n"

        test_ozet = ""
        for t in aday.testler:
            skorlar = t.get("skorlar", {})
            skor_text = ", ".join(f"{k}:{v}" for k, v in skorlar.items()) if skorlar else ""
            test_ozet += f"- {t.get('test_adi', '')}: {t.get('sonuc', '')} | {skor_text}\n"
            if t.get("notlar"):
                test_ozet += f"  Not: {t['notlar']}\n"

        ihtiyac_ozet = ""
        for ih in aday.ihtiyaclar:
            ihtiyac_ozet += f"- [{ih.get('oncelik', '')}] {ih.get('kategori', '')}: {ih.get('aciklama', '')}\n"

        fb = aday.fiyat_bilgi or {}
        toplam_ucret = float(fb.get("genel_toplam_final", fb.get("brut_toplam", 0)) or 0)
        fiyat_ozet = f"Toplam: {toplam_ucret:,.0f} TL | Indirim: %{fb.get('toplam_indirim', 0):.0f}" if fb else "Fiyat yok"

        ek = aday.ek_hizmetler or {}
        ek_ozet = ""
        if ek:
            ek_items = []
            if ek.get("ogle_yemegi", 0) > 0: ek_items.append(f"Yemek:{ek['ogle_yemegi']:,.0f}")
            if ek.get("kahvalti", 0) > 0: ek_items.append(f"Kahvalti:{ek['kahvalti']:,.0f}")
            if ek.get("servis", 0) > 0: ek_items.append(f"Servis:{ek['servis']:,.0f}")
            if ek.get("dijital", 0) > 0: ek_items.append(f"Dijital:{ek['dijital']:,.0f}")
            ek_ozet = " | ".join(ek_items)

        try:
            surec_gun = (date.today() - date.fromisoformat(aday.olusturma_tarihi[:10])).days
        except (ValueError, TypeError):
            surec_gun = 0

        # ── OKUL SURECLERI (diger modullerden) ──
        okul_veri = ""

        # Notlar
        try:
            from models.akademik_takip import AkademikDataStore
            _ak = AkademikDataStore()
            notlar = [n if isinstance(n, dict) else (n.to_dict() if hasattr(n, "to_dict") else {})
                      for n in (_ak.load_objects("grades") if hasattr(_ak, "load_objects") else [])]
            ogr_notlar = [n for n in notlar if ogr_adi.upper() in (n.get("ogrenci_adi", "") or n.get("student_name", "")).upper()]
            if ogr_notlar:
                okul_veri += "YAZILI NOTLAR:\n"
                for n in ogr_notlar[:10]:
                    okul_veri += f"- {n.get('ders', '-')}: {n.get('puan', '-')} ({n.get('not_turu', '')})\n"
        except Exception:
            pass

        # Devamsizlik
        try:
            devler = [d if isinstance(d, dict) else (d.to_dict() if hasattr(d, "to_dict") else {})
                      for d in (_ak.load_objects("attendance") if hasattr(_ak, "load_objects") else [])]
            ogr_dev = [d for d in devler if ogr_adi.upper() in (d.get("ogrenci_adi", "") or d.get("student_name", "")).upper()]
            if ogr_dev:
                ozursuz = sum(1 for d in ogr_dev if "ozursuz" in str(d.get("turu", "")).lower())
                okul_veri += f"\nDEVAMSIZLIK: Toplam {len(ogr_dev)} gun ({ozursuz} ozursuz)\n"
        except Exception:
            pass

        # Erken uyari
        try:
            from models.erken_uyari import ErkenUyariStore
            _eu = ErkenUyariStore()
            risks = [r if isinstance(r, dict) else (r.to_dict() if hasattr(r, "to_dict") else {})
                     for r in (_eu.load_risks() if hasattr(_eu, "load_risks") else [])]
            ogr_risk = [r for r in risks if ogr_adi.upper() in (r.get("ogrenci_adi", "") or r.get("student_name", "")).upper()]
            if ogr_risk:
                son = ogr_risk[-1]
                okul_veri += f"\nERKEN UYARI: Risk Skoru {son.get('risk_skoru', son.get('risk_score', '-'))}/100 | Seviye: {son.get('risk_level', '-')}\n"
        except Exception:
            pass

        # Egitim koclugu
        try:
            from models.egitim_koclugu import get_ek_store
            _ek = get_ek_store()
            for o in (_ek.load_objects("ogrenciler") if hasattr(_ek, "load_objects") else []):
                od = o if isinstance(o, dict) else (o.to_dict() if hasattr(o, "to_dict") else {})
                if ogr_adi.upper() in (od.get("ad", "") + " " + od.get("soyad", "")).upper():
                    okul_veri += f"\nEGITIM KOCLUGU: Koc: {od.get('koc_adi', '-')} | Motivasyon: {od.get('motivasyon_seviyesi', '-')}/5 | Hedef: {od.get('hedef_sinav', '-')} {od.get('hedef_puan', '')}\n"
                    okul_veri += f"Guclu: {od.get('guclu_dersler', '-')} | Zayif: {od.get('zayif_dersler', '-')}\n"
        except Exception:
            pass

        # Rehberlik
        try:
            from models.erken_uyari import CrossModuleLoader
            vakalar = CrossModuleLoader.load_rehberlik_vakalar()
            ogr_vaka = [v if isinstance(v, dict) else (v.to_dict() if hasattr(v, "to_dict") else {})
                        for v in vakalar if ogr_adi.upper() in (
                            (v if isinstance(v, dict) else {}).get("ogrenci_adi", "") or
                            (v.to_dict() if hasattr(v, "to_dict") else {}).get("ogrenci_adi", "")
                        ).upper()]
            if ogr_vaka:
                okul_veri += f"\nREHBERLIK: {len(ogr_vaka)} vaka kaydi\n"
                for v in ogr_vaka[:3]:
                    okul_veri += f"- {v.get('konu', '-')} ({v.get('durum', '')})\n"
        except Exception:
            pass

        # MEB Dijital Formlar
        try:
            from models.erken_uyari import CrossModuleLoader as _CML_MEB_KM
            _meb_all_km = _CML_MEB_KM.load_all_meb_forms()
            _meb_items = []
            for _sk, _flist in _meb_all_km.items():
                for _f in _flist:
                    _f_adi = _f.get("ogrenci_adi_soyadi", "")
                    if _f_adi and ogr_adi and ogr_adi.upper() in _f_adi.upper():
                        _meb_items.append((_sk, _f))
            if _meb_items:
                from models.meb_formlar import MEB_FORM_SCHEMAS
                okul_veri += f"\nMEB DIJITAL FORMLAR: {len(_meb_items)} kayit\n"
                for _sk, _f in _meb_items[:5]:
                    _sch = next((s for s in MEB_FORM_SCHEMAS.values() if s["store_key"] == _sk), None)
                    _fname = _sch["title"] if _sch else _sk
                    okul_veri += f"- {_fname} ({_f.get('tarih', '')})\n"
                    # Kritik bilgiler
                    if _sk == "dehb_gozlem_formlari" and _f.get("yonlendirme_onerisi"):
                        okul_veri += f"  DEHB Yonlendirme: {_f['yonlendirme_onerisi']}\n"
                    if _sk == "psikolojik_yonlendirme_formlari":
                        okul_veri += f"  Psikolojik: {_f.get('yonlendirme_nedeni', '')} — Siddet: {_f.get('belirti_siddeti', '')}\n"
                    if _sk == "disiplin_gorusme_formlari":
                        okul_veri += f"  Disiplin: {_f.get('olay_aciklamasi', '')[:80]}\n"
        except Exception:
            pass

        from utils.ai_rules import inject_rules as _air
        system_prompt = _air("""Sen Turkiye'nin en deneyimli egitim uzmani ve ogrenci degerlendirme uzmanisin.
Bir ogrencinin TUM verilerini — kimlik bilgileri, kayit sureci (aramalar, gorusmeler, testler, ihtiyac analizi), okul surecleri (notlar, devamsizlik, sinavlar, rehberlik, egitim koclugu, erken uyari) — butunsel olarak analiz edeceksin.

YANITINI su formatta ver:

## 🎓 OGRENCI GENEL PROFILI
(Kim bu ogrenci, ailesi, akademik gecmisi, okul ortami — 3-4 cumle butunsel ozet)

## 📊 AKADEMIK DURUM ANALIZI
### Guclu Alanlar
(Test sonuclari + notlar + koçluk verilerine dayali guclu yonler — somut veriyle)
### Gelistirilecek Alanlar
(Zayif noktalar, dusuk skorlar, devamsizlik etkisi — somut oneriyle)
### Akademik Basari Tahmini
(Mevcut verilere gore donem sonu / yil sonu basari tahmini — yuzde olarak)

## 🧠 SOSYAL-DUYGUSAL DEGERLENDIRME
(Rehberlik verileri, motivasyon puani, sosyal etkinlikler, davranis — ne gosteriyor)

## ⚠️ RISK DEGERLENDIRMESI
(Erken uyari skorlari, devamsizlik trendi, dusuk notlar, rehberlik uyarilari — risk seviyesi)
Risk Seviyesi: DUSUK / ORTA / YUKSEK / KRITIK

## 🎯 BIREYSEL GELISIM PLANI
### Kisa Vadeli Hedefler (1 ay)
(3 somut, olculebilir hedef)
### Orta Vadeli Hedefler (1 donem)
(3 somut, olculebilir hedef)
### Uzun Vadeli Hedefler (1 yil)
(3 somut, olculebilir hedef)

## 👨‍👩‍👧 VELI ILETISIM STRATEJISI
(Veliye nasil geri bildirim verilmeli, hangi konularda bilgilendirilmeli, gorusme onerileri)

## 📋 OGRETMEN/KOC ICIN ONERILER
(Sinif ici stratejiler, bireysel destek onerileri, ders bazli aksiyon plani — 5 madde)

## 💎 OZET KARAR
(Bu ogrenci icin tek cumlelik genel degerlendirme + en kritik aksiyon)

KURALLAR:
- Her oneriyi somut veriye dayandır
- Ogrencinin ve velinin adini kullan
- Turkce yaz, profesyonel ama sicak ton
- Olculebilir hedefler koy (yuzde, puan, gun)
- Riskleri gizleme ama cozum odakli yaz""")

        user_prompt = f"""=== KIMLIK BILGILERI ===
{kimlik}

=== KAYIT SURECI ===
Surec: {surec_gun} gun | Arama: {aday.arama_sayisi} | Gorusme: {aday.gorusme_sayisi} | Test: {len(aday.testler)}
Fiyat: {fiyat_ozet}
Ek Hizmetler: {ek_ozet or 'Yok'}

ARAMALAR ({aday.arama_sayisi}):
{arama_ozet or 'Yok'}

GORUSMELER ({aday.gorusme_sayisi}):
{gorusme_ozet or 'Yok'}

TESTLER ({len(aday.testler)}):
{test_ozet or 'Yok'}

IHTIYAC ANALIZI ({len(aday.ihtiyaclar)}):
{ihtiyac_ozet or 'Yapilmamis'}

GENEL NOTLAR: {aday.notlar or 'Yok'}

=== OKUL SURECLERI ===
{okul_veri or 'Henuz okul sureci verisi yok (yeni kayit).'}

Bu ogrencinin TUM verilerini butunsel olarak degerlendir. Kimlik + kayit sureci + okul surecleri birlikte analiz et."""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=4000,
            temperature=0.7,
        )
        return resp.choices[0].message.content or ""
    except Exception as e:
        st.error(f"AI genel degerlendirme hatasi: {e}")
        return ""


def _render_okul_surecleri(aday: KayitAday):
    """Tum modullerden ogrenciye ait okul sureclerini gosteren profesyonel bilgi karti."""

    ogr_adi = aday.ogrenci_adi or ""
    ogr_sinif = aday.kayit_sinif or aday.hedef_sinif or ""
    ogr_sube = aday.kayit_sube or ""

    def _match(name_field: str) -> bool:
        """Ogrenci adi eslesme kontrolu."""
        return bool(ogr_adi and ogr_adi.upper() in str(name_field).upper())

    def _to_d(obj) -> dict:
        if isinstance(obj, dict):
            return obj
        return obj.to_dict() if hasattr(obj, "to_dict") else {}

    def _section(icon: str, title: str, items: list[dict], renk: str):
        cnt = len(items)
        badge_clr = "#4ade80" if cnt > 0 else "#64748b"
        with st.expander(f"{icon} {title} ({cnt})", expanded=False):
            if not items:
                st.caption("Henuz veri yok — ilgili modulde kayit olusturulunca burada gorunecektir.")
                return
            for it in items:
                c = it.get("renk", renk)
                det = f'<div style="color:#94a3b8;font-size:0.76rem;margin-top:2px">{it["detay"]}</div>' if it.get("detay") else ""
                st.markdown(
                    f'<div style="padding:6px 10px;margin:2px 0;background:#111827;border-radius:6px;border-left:3px solid {c}">'
                    f'<span style="color:#e2e8f0;font-weight:600;font-size:0.83rem">{it["baslik"]}</span>{det}</div>',
                    unsafe_allow_html=True)

    # ── 1) YAZILI NOTLAR (Akademik Takip) ──
    items1 = []
    try:
        from models.akademik_takip import AkademikDataStore
        _ak = AkademikDataStore()
        for n in (_ak.load_objects("grades") if hasattr(_ak, "load_objects") else []):
            nd = _to_d(n)
            if _match(nd.get("ogrenci_adi", nd.get("student_name", ""))):
                puan = nd.get("puan", nd.get("score", "-"))
                items1.append({"baslik": f'{nd.get("ders", "-")} — {nd.get("not_turu", "")}: {puan}',
                               "detay": f'Donem: {nd.get("donem", "")} | Yil: {nd.get("akademik_yil", "")}'})
    except Exception:
        pass
    _section("📝", "Yazili Notlar & Puan Kayitlari", items1, "#3b82f6")

    # ── 2) DEVAMSIZLIK (Akademik Takip) ──
    items2 = []
    try:
        from models.akademik_takip import AkademikDataStore
        _ak2 = AkademikDataStore()
        for d in (_ak2.load_objects("attendance") if hasattr(_ak2, "load_objects") else []):
            dd = _to_d(d)
            if _match(dd.get("ogrenci_adi", dd.get("student_name", ""))):
                tur = str(dd.get("turu", dd.get("type", "-")))
                items2.append({"baslik": f'{dd.get("tarih", "-")} — {tur}',
                               "detay": f'Ders: {dd.get("ders", "")}' if dd.get("ders") else "",
                               "renk": "#ef4444" if "ozursuz" in tur.lower() else "#f59e0b"})
    except Exception:
        pass
    _section("📅", "Devamsizlik Kayitlari", items2, "#f59e0b")

    # ── 3) OLCME & DEGERLENDIRME SINAVLARI ──
    items3 = []
    try:
        from models.olcme_degerlendirme import DataStore as _OD
        _ol = _OD()
        for r in (_ol.load_objects("results") if hasattr(_ol, "load_objects") else []):
            rd = _to_d(r)
            if _match(rd.get("student_name", rd.get("ogrenci_adi", ""))):
                items3.append({"baslik": f'{rd.get("exam_title", rd.get("sinav_adi", "-"))} — {rd.get("score", rd.get("puan", "-"))} puan',
                               "detay": f'Tarih: {str(rd.get("date", rd.get("tarih", "")))[:10]}'})
    except Exception:
        pass
    _section("📊", "Olcme & Degerlendirme Sinavlari", items3, "#a78bfa")

    # ── 4) YABANCI DIL SEVIYESI (CEFR) ──
    items4 = []
    try:
        from utils.tenant import get_data_path as _gdp
        from models.cefr_exam import CEFRExamStore
        _cefr = CEFRExamStore(data_dir=f"{_gdp('')}/english/cefr_exams")
        for r in (_cefr.list_results() if hasattr(_cefr, "list_results") else []):
            rd = _to_d(r)
            if _match(rd.get("student_name", "")):
                items4.append({"baslik": f'CEFR: {rd.get("achieved_cefr", rd.get("cefr", "-"))} — %{rd.get("percentage", 0):.0f}',
                               "detay": f'L:{rd.get("listening_score", "-")} R:{rd.get("reading_score", "-")} W:{rd.get("writing_score", "-")} S:{rd.get("speaking_score", "-")}',
                               "renk": "#10b981"})
    except Exception:
        pass
    try:
        from utils.tenant import get_data_path as _gdp2
        from models.yd_assessment import YdAssessmentStore
        _yd = YdAssessmentStore(base_path=f"{_gdp2('')}/yabanci_dil")
        for r in (_yd.get_results() if hasattr(_yd, "get_results") else []):
            rd = _to_d(r)
            if _match(rd.get("student_name", "")):
                _u_num = rd.get("unit", 0) or 0
                _u_label = f" | Ünite {_u_num}" if _u_num > 0 else ""
                items4.append({"baslik": f'YD {rd.get("exam_category", "-").title()}: {rd.get("exam_name", "-")}',
                               "detay": f'Puan: {rd.get("score", "-")} | Dogru: {rd.get("correct_count", rd.get("correct", "-"))} | Yanlis: {rd.get("wrong_count", rd.get("wrong", "-"))}{_u_label}'})
    except Exception:
        pass
    # CEFR Placement (Seviye Tespit) sonuclari
    try:
        from models.cefr_exam import CEFRPlacementStore
        _cp = CEFRPlacementStore()
        for rd in _cp._load(_cp._results_path):
            if _match(rd.get("student_name", "")):
                _period = "Sene Basi" if rd.get("period") == "sene_basi" else "Sene Sonu"
                items4.append({
                    "baslik": f'CEFR Seviye Tespit ({_period} {rd.get("academic_year", "")}): '
                              f'{rd.get("placed_cefr", "-")} — %{rd.get("percentage", 0):.0f}',
                    "detay": f'Hedef: {rd.get("target_cefr", "-")} | '
                             f'L:{rd.get("listening_score", 0):.0f} R:{rd.get("reading_score", 0):.0f} '
                             f'G:{rd.get("use_of_english_score", 0):.0f} W:{rd.get("writing_score", 0):.0f}',
                    "renk": "#6366f1",
                })
    except Exception:
        pass
    _section("🌍", "Yabanci Dil Seviyesi", items4, "#14b8a6")

    # ── 5) REHBERLIK & PDR ──
    items5 = []
    try:
        from models.erken_uyari import CrossModuleLoader as _CML
        for v in _CML.load_rehberlik_vakalar():
            vd = _to_d(v)
            if _match(vd.get("ogrenci_adi", vd.get("student_name", ""))):
                items5.append({"baslik": f'Vaka: {vd.get("konu", vd.get("subject", "-"))}',
                               "detay": f'Durum: {vd.get("durum", "")} | {str(vd.get("tarih", ""))[:10]}',
                               "renk": "#ef4444" if "acil" in str(vd.get("oncelik", "")).lower() else "#0ea5e9"})
        for g in _CML.load_rehberlik_gorusmeler():
            gd = _to_d(g)
            if _match(gd.get("ogrenci_adi", gd.get("student_name", ""))):
                items5.append({"baslik": f'Gorusme: {gd.get("konu", gd.get("topic", "-"))}',
                               "detay": str(gd.get("tarih", ""))[:10]})
    except Exception:
        pass
    _section("🧠", "Rehberlik & PDR", items5, "#0ea5e9")

    # ── 5b) REHBERLİK TEST & ENVANTER ──
    items5b = []
    try:
        from models.erken_uyari import CrossModuleLoader as _CML_RT2
        _rt_oturumlar = _CML_RT2.load_rehberlik_test_oturumlari()
        _rt_testler = _CML_RT2.load_rehberlik_testler()
        _rt_cevaplar = _CML_RT2.load_rehberlik_test_cevaplari()
        _test_map = {t.get("id", ""): t for t in _rt_testler}
        for o in _rt_oturumlar:
            if _match(o.get("ogrenci_adi", "")):
                test = _test_map.get(o.get("test_id", ""), {})
                test_adi = test.get("test_adi", "-")
                durum = o.get("durum", "-")
                renk = "#22c55e" if durum == "TAMAMLANDI" else "#f59e0b" if durum == "DEVAM_EDIYOR" else "#64748b"
                # Cevap puanları
                ogr_cevap = [c for c in _rt_cevaplar if c.get("oturum_id") == o.get("id")]
                puan_text = ""
                if ogr_cevap:
                    puanlar = [float(c.get("puan", 0)) for c in ogr_cevap if c.get("puan")]
                    if puanlar:
                        puan_text = f" | Ort Puan: {sum(puanlar)/len(puanlar):.1f}"
                items5b.append({
                    "baslik": f'{test_adi} — {durum}',
                    "detay": f'Tarih: {str(o.get("bitis_zamani", o.get("baslangic_zamani", "")))[:10]}{puan_text}',
                    "renk": renk,
                })
    except Exception:
        pass
    _section("📝", "Rehberlik Test & Envanter Sonuclari", items5b, "#8b5cf6")

    # ── 6) EGITIM KOCLUGU ──
    items6 = []
    try:
        from models.egitim_koclugu import get_ek_store
        _ek = get_ek_store()
        for o in (_ek.load_objects("ogrenciler") if hasattr(_ek, "load_objects") else []):
            od = _to_d(o)
            if _match(od.get("ad", "") + " " + od.get("soyad", "")):
                items6.append({"baslik": f'Koc: {od.get("koc_adi", "-")} | Hedef: {od.get("hedef_sinav", "-")} {od.get("hedef_puan", "")}',
                               "detay": f'Motivasyon: {od.get("motivasyon_seviyesi", "-")}/5 | Guclu: {od.get("guclu_dersler", "-")} | Zayif: {od.get("zayif_dersler", "-")}',
                               "renk": "#8b5cf6"})
        for g in (_ek.load_objects("gorusmeler") if hasattr(_ek, "load_objects") else []):
            gd = _to_d(g)
            if _match(gd.get("ogrenci_adi", "")):
                items6.append({"baslik": f'Kocluk Gorusme: {gd.get("konu", gd.get("kocluk_alani", "-"))} ({gd.get("durum", "")})',
                               "detay": f'{str(gd.get("tarih", ""))[:10]} | {gd.get("sure_dk", "-")} dk | Motivasyon: {gd.get("motivasyon_puani", "-")}/5'})
    except Exception:
        pass
    _section("🎯", "Egitim Koclugu", items6, "#8b5cf6")

    # ── 7) KULUPLER & SOSYAL ETKINLIKLER ──
    items7 = []
    try:
        from utils.tenant import get_data_path as _gdp3
        from models.sosyal_etkinlik import SosyalEtkinlikDataStore
        _se = SosyalEtkinlikDataStore(_gdp3("sosyal_etkinlik"))
        for k in (_se.load_objects("kulupler") if hasattr(_se, "load_objects") else []):
            kd = _to_d(k)
            uyeler = " ".join(str(u) for u in kd.get("ogrenciler", kd.get("uyeler", []))).upper()
            if ogr_adi and ogr_adi.upper() in uyeler:
                items7.append({"baslik": f'Kulup: {kd.get("ad", kd.get("name", "-"))}',
                               "detay": f'Danisman: {kd.get("danisman", kd.get("advisor", "-"))}'})
        for e in (_se.load_objects("etkinlikler") if hasattr(_se, "load_objects") else []):
            ed = _to_d(e)
            katilimci = " ".join(str(x) for x in ed.get("katilimcilar", [])).upper()
            if ogr_adi and ogr_adi.upper() in katilimci:
                items7.append({"baslik": f'Etkinlik: {ed.get("ad", ed.get("name", "-"))}',
                               "detay": str(ed.get("tarih", ""))[:10], "renk": "#10b981"})
    except Exception:
        pass
    _section("🎭", "Kulupler & Sosyal Etkinlikler", items7, "#10b981")

    # ── 8) KUTUPHANE & DIJITAL KUTUPHANE ──
    items8 = []
    try:
        from utils.tenant import get_data_path as _gdp4
        from models.kutuphane import KutuphaneDataStore
        _kt = KutuphaneDataStore(f"{_gdp4('')}/kutuphane")
        for o in (_kt.load_objects("odunc_islemleri") if hasattr(_kt, "load_objects") else []):
            od = _to_d(o)
            if _match(od.get("odunc_alan_adi", "")):
                durum = od.get("durum", "-")
                renk = "#ef4444" if durum in ("Gecikti", "Kayip") else ("#f59e0b" if durum == "Odunc" else "#4ade80")
                items8.append({"baslik": f'{od.get("materyal_adi", "-")} — {durum}',
                               "detay": f'Odunc: {str(od.get("odunc_tarihi", ""))[:10]} | Iade: {str(od.get("gercek_iade_tarihi", od.get("iade_tarihi", "")))[:10]}',
                               "renk": renk})
    except Exception:
        pass
    try:
        from utils.tenant import get_data_path as _gdp5
        from models.dijital_kutuphane import DijitalKutuphaneDataStore
        _dk = DijitalKutuphaneDataStore(f"{_gdp5('')}/dijital_kutuphane")
        usage = _dk.load_usage_logs() if hasattr(_dk, "load_usage_logs") else []
        ogr_usage = [u for u in usage if isinstance(u, dict) and _match(u.get("user", u.get("ogrenci_adi", "")))]
        if ogr_usage:
            items8.append({"baslik": f"Dijital Kutuphane: {len(ogr_usage)} kullanim kaydi",
                           "detay": f'Son erisim: {str(ogr_usage[-1].get("tarih", ""))[:10]}' if ogr_usage else "",
                           "renk": "#6366f1"})
    except Exception:
        pass
    _section("📚", "Kutuphane & Dijital Kutuphane", items8, "#6366f1")

    # ── 9) SERVIS & YEMEK (Kurum Hizmetleri) ──
    items9 = []
    try:
        from utils.tenant import get_data_path as _gdp6
        from models.servis_yonetimi import get_servis_store
        _sv = get_servis_store(f"{_gdp6('')}/servis")
        hatlar = _sv.load_objects("hatlar") if hasattr(_sv, "load_objects") else []
        for h in hatlar:
            hd = _to_d(h)
            ogrenci_ids = hd.get("ogrenci_ids", [])
            ogrenci_str = " ".join(str(x) for x in ogrenci_ids).upper()
            if ogr_adi and ogr_adi.upper() in ogrenci_str:
                items9.append({"baslik": f'Servis Hatti: {hd.get("hat_adi", "-")}',
                               "detay": f'Plaka: {hd.get("plaka", "-")} | Sofor: {hd.get("sofor_adi", "-")} | Sabah: {hd.get("sabah_saat", "-")}',
                               "renk": "#0ea5e9"})
    except Exception:
        pass
    # Yemek — kayit ek_hizmetler'den
    ek = aday.ek_hizmetler or {}
    if ek:
        yemek_items = []
        if ek.get("ogle_yemegi", 0) > 0:
            yemek_items.append(f"Ogle Yemegi: {ek['ogle_yemegi']:,.0f} TL")
        if ek.get("kahvalti", 0) > 0:
            yemek_items.append(f"Kahvalti: {ek['kahvalti']:,.0f} TL")
        if ek.get("ara_ogun", 0) > 0:
            yemek_items.append(f"Ara Ogun: {ek['ara_ogun']:,.0f} TL")
        if ek.get("servis", 0) > 0:
            yemek_items.append(f"Servis: {ek['servis']:,.0f} TL")
        if yemek_items:
            items9.append({"baslik": "Ek Hizmetler: " + " | ".join(yemek_items),
                           "detay": f"Toplam: {ek.get('kdv_dahil', ek.get('toplam', 0)):,.0f} TL (KDV dahil)",
                           "renk": "#f59e0b"})
    _section("🚌", "Servis & Yemek Hizmetleri", items9, "#0ea5e9")

    # ── 10) ERKEN UYARI SISTEMI ──
    items10 = []
    try:
        from models.erken_uyari import ErkenUyariStore
        _eu = ErkenUyariStore()
        for r in (_eu.load_risks() if hasattr(_eu, "load_risks") else []):
            rd = _to_d(r)
            if _match(rd.get("ogrenci_adi", rd.get("student_name", ""))):
                skor = rd.get("risk_skoru", rd.get("risk_score", 0))
                renk = "#ef4444" if skor >= 70 else ("#f59e0b" if skor >= 40 else "#4ade80")
                kategori = rd.get("kategori", rd.get("category", rd.get("risk_level", "-")))
                items10.append({"baslik": f"Risk: {kategori} — Skor: {skor}/100",
                                "detay": f'Tarih: {str(rd.get("tarih", rd.get("calculated_at", "")))[:10]}',
                                "renk": renk})
        for al in (_eu.load_alerts() if hasattr(_eu, "load_alerts") else []):
            ald = _to_d(al)
            if _match(ald.get("ogrenci_adi", ald.get("student_name", ""))):
                durum = ald.get("durum", ald.get("status", "aktif"))
                items10.append({"baslik": f'Uyari: {str(ald.get("mesaj", ald.get("message", "-")))[:60]}',
                                "detay": f'Durum: {durum} | {str(ald.get("tarih", ""))[:10]}',
                                "renk": "#ef4444" if durum in ("aktif", "acik") else "#64748b"})
    except Exception:
        pass
    # Kayit testlerinden risk tahmini (erken uyari verisi yoksa)
    if not items10 and aday.testler:
        for t in aday.testler:
            for alan, skor in t.get("skorlar", {}).items():
                if isinstance(skor, (int, float)):
                    if skor < 40:
                        items10.append({"baslik": f"Dusuk Skor: {alan} = {skor}", "detay": f'Test: {t.get("test_adi", "")}', "renk": "#ef4444"})
                    elif skor < 60:
                        items10.append({"baslik": f"Takip: {alan} = {skor}", "detay": f'Test: {t.get("test_adi", "")}', "renk": "#f59e0b"})
    _section("⚠️", "Yapay Zeka Erken Uyari Sistemi", items10, "#ef4444")

    # ── 11) AİLE BİLGİ FORMU (Rehberlik) ──
    items11 = []
    try:
        from models.rehberlik import RehberlikDataStore as _RhbStore
        from utils.tenant import get_tenant_dir as _gtd
        _rhb = _RhbStore(_gtd() + "/rehberlik")
        for f in _rhb.load_list("aile_bilgi_formlari"):
            if _match(f.get("ogrenci_adi_soyadi", "")):
                # Kritik bilgiler
                _kritik = []
                if f.get("anne_birlikte_bosanmis") in ("Boşanmış", "Ayrı"):
                    _kritik.append("⚠ Anne-Baba Boşanmış/Ayrı")
                if f.get("baba_birlikte_bosanmis") in ("Boşanmış", "Ayrı"):
                    _kritik.append("⚠ Anne-Baba Boşanmış/Ayrı")
                if f.get("anne_sag_olu") == "Ölü":
                    _kritik.append("⚠ Anne vefat etmiş")
                if f.get("baba_sag_olu") == "Ölü":
                    _kritik.append("⚠ Baba vefat etmiş")
                if f.get("suregen_hastalik"):
                    _kritik.append(f"🏥 Süreğen hastalık: {f['suregen_hastalik']}")
                if f.get("etkisindeki_olay"):
                    _kritik.append(f"⚠ Travmatik olay: {f['etkisindeki_olay']}")
                if f.get("bagimllik_durumu"):
                    _kritik.append(f"⚠ Ailede bağımlılık: {f['bagimllik_durumu']}")
                if f.get("suca_karismis_birey"):
                    _kritik.append(f"⚠ Ailede suç: {f['suca_karismis_birey']}")
                if f.get("yetersizlik_suregen_hastalik"):
                    _kritik.append(f"🏥 Ailede yetersizlik: {f['yetersizlik_suregen_hastalik']}")
                if f.get("kiminle_nerede_yasiyor") not in ("Aile", "", None):
                    _kritik.append(f"🏠 Yaşam: {f['kiminle_nerede_yasiyor']}")

                # Ana kart
                items11.append({
                    "baslik": f'Aile Bilgi Formu — {f.get("tarih", "")}',
                    "detay": (
                        f'Anne: {f.get("anne_adi_soyadi", "-")} | Baba: {f.get("baba_adi_soyadi", "-")} | '
                        f'Kardeş: Öz:{f.get("kardes_oz_sayisi", 0)} Üvey:{f.get("kardes_uvey_sayisi", 0)} | '
                        f'Yaşam: {f.get("kiminle_nerede_yasiyor", "-")} | '
                        f'Gelir: {f.get("ortalama_gelir", "-")} | Ev: {f.get("ev_sahipligi", "-")}'
                    ),
                    "renk": "#0d9488",
                })
                # Kritik uyarılar ayrı satırlar
                for k in _kritik:
                    _k_renk = "#ef4444" if "⚠" in k else "#f59e0b"
                    items11.append({"baslik": k, "detay": "", "renk": _k_renk})

                # Eğitim bilgileri
                _egitim_items = []
                if f.get("okula_tutum"):
                    _egitim_items.append(f'Okula tutum: {f["okula_tutum"]}')
                if f.get("ogretmenlere_tutum"):
                    _egitim_items.append(f'Öğretmenlere tutum: {f["ogretmenlere_tutum"]}')
                if f.get("ders_calisma_alani"):
                    _egitim_items.append(f'Çalışma alanı: {f["ders_calisma_alani"]}')
                if f.get("ders_destegi"):
                    _egitim_items.append(f'Ders desteği: {f["ders_destegi"]}')
                if _egitim_items:
                    items11.append({"baslik": "Eğitim: " + " | ".join(_egitim_items), "detay": "", "renk": "#3b82f6"})

                # Aile iletişim
                if f.get("aile_ici_kurallar"):
                    items11.append({"baslik": f'Aile kuralları: {f["aile_ici_kurallar"]}', "detay": "", "renk": "#8b5cf6"})
    except Exception:
        pass
    _section("📋", "Aile Bilgi Formu (MEB B.K.G.1.c)", items11, "#0d9488")


def _render_arama_destek():
    st.markdown(
        '<div style="background:linear-gradient(135deg,#7c3aed,#5b21b6);border-radius:12px;'
        'padding:16px 20px;margin-bottom:14px">'
        '<div style="color:#fff;font-size:1.1rem;font-weight:800">📞 Telefon Arama Destek Rehberi</div>'
        '<div style="color:#ddd6fe;font-size:0.85rem;margin-top:4px">'
        'Sik sorulan sorular ve hazir cevaplar — arama sirasinda kullanin</div></div>',
        unsafe_allow_html=True)

    # Arama kutusu
    arama = st.text_input("🔍 Soru veya anahtar kelime ara", key="km_destek_ara",
                           placeholder="Orn: ucret, indirim, servis, guvenlik...")

    # Filtreleme
    if arama and len(arama) >= 2:
        q = arama.lower()
        filtreli = {k: v for k, v in ARAMA_DESTEK_SORULAR.items()
                    if q in v["soru"].lower() or q in k.lower()
                    or any(q in c.lower() for c in v["cevaplar"])}
    else:
        filtreli = ARAMA_DESTEK_SORULAR

    if not filtreli:
        styled_info_banner("Aramaniza uygun soru bulunamadi.", "info")
        return

    st.caption(f"{len(filtreli)} soru listeleniyor")

    # Soru-cevap kartlari
    _renk_listesi = ["#6366f1", "#8b5cf6", "#ec4899", "#0ea5e9", "#10b981", "#f59e0b", "#ea580c",
                      "#ef4444", "#14b8a6", "#d946ef", "#3b82f6", "#22c55e", "#f97316", "#a855f7", "#06b6d4"]

    for idx, (key, item) in enumerate(filtreli.items()):
        clr = _renk_listesi[idx % len(_renk_listesi)]
        with st.expander(f"❓ {item['soru']}", expanded=False):
            for ci, cevap in enumerate(item["cevaplar"], 1):
                st.markdown(
                    f'<div style="display:flex;align-items:flex-start;gap:8px;padding:8px 10px;margin:4px 0;'
                    f'background:{clr}08;border:1px solid {clr}20;border-radius:6px;border-left:3px solid {clr}">'
                    f'<div style="background:{clr};color:#fff;min-width:22px;height:22px;border-radius:50%;'
                    f'display:flex;align-items:center;justify-content:center;font-weight:800;font-size:0.65rem;flex-shrink:0">{ci}</div>'
                    f'<div style="color:#e2e8f0;font-size:0.88rem">{cevap}</div></div>',
                    unsafe_allow_html=True)

    # Hizli erisim kartlari
    st.markdown("---")
    st.markdown('<div style="color:#94a3b8;font-weight:600;margin:8px 0">⚡ Hizli Erisim</div>',
                unsafe_allow_html=True)
    hc = st.columns(4)
    _hizli = [
        (hc[0], "💰 Ucret", "ucret"), (hc[1], "🎓 Indirim/Burs", "indirim"),
        (hc[2], "📅 Randevu", "gelmek"), (hc[3], "🤔 Dusunuyor", "dusunme"),
    ]
    for col, label, key in _hizli:
        with col:
            item = ARAMA_DESTEK_SORULAR.get(key, {})
            if item:
                st.markdown(
                    f'<div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:8px;text-align:center">'
                    f'<div style="font-weight:700;color:#e2e8f0;font-size:0.85rem;margin-bottom:4px">{label}</div>'
                    f'<div style="font-size:0.75rem;color:#94a3b8">{item["cevaplar"][0][:60]}...</div></div>',
                    unsafe_allow_html=True)


# ============================================================
# KAPANIS SILAHLARI — 3 MODUL
# 1) Gelecegin Mini Kitabi (PDF)
# 2) AI Korku Yikici (Itiraz cevap raporu)
# 3) Kisisel URL + Sube Hold + Tek-Tik Kayit
# ============================================================

def _aday_secici(adaylar: list[KayitAday], key_prefix: str) -> KayitAday | None:
    """Yeniden kullanilan aday secici bileseni."""
    aktif = [a for a in adaylar if a.aktif]
    if not aktif:
        st.info("Henüz aktif aday yok. Önce 'Yeni Aday' sekmesinden aday ekleyin.")
        return None
    secenekler = {f"{a.veli_adi} — {a.ogrenci_adi} ({a.kademe or '-'})": a for a in aktif}
    sec = st.selectbox(
        "Aday Seç",
        options=list(secenekler.keys()),
        key=f"{key_prefix}_aday_sec",
    )
    return secenekler.get(sec)


def _kurum_adi_getir() -> str:
    try:
        from utils.shared_data import load_kurum_profili
        kp = load_kurum_profili() or {}
        return kp.get("kurum_adi", kp.get("name", "")) or ""
    except Exception:
        return ""


def _render_kapanis_silahlari(store: KayitDataStore, adaylar: list[KayitAday]):
    """Ana giris — 3 kapanis silahi alt sekmeleri."""
    st.markdown(
        '<div style="background:linear-gradient(135deg,#0B1E3F 0%,#1e293b 50%,#0B1E3F 100%);'
        'border:1px solid #C8952E40;border-radius:14px;padding:16px 20px;margin-bottom:12px;'
        'box-shadow:0 4px 20px #C8952E15">'
        '<div style="display:flex;align-items:center;gap:10px">'
        '<div style="font-size:1.6rem">✨</div>'
        '<div>'
        '<div style="color:#C8952E;font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase">PREMIUM KAPANIS SILAHLARI</div>'
        '<div style="color:#fff;font-size:1.2rem;font-weight:700">Kayıt Dönüşümünü Uçuracak 3 Araç</div>'
        '<div style="color:#94a3b8;font-size:0.8rem;margin-top:2px">Her aday için özel — AI destekli, PDF çıktılı, veriye dayalı</div>'
        '</div></div></div>',
        unsafe_allow_html=True
    )

    alt = st.tabs([
        "🎁 Geleceğin Mini Kitabı",
        "🛡️ Korku Yıkıcı",
        "🔗 Kişisel URL + Hold",
    ])

    with alt[0]:
        _render_gelecek_kitabi(adaylar)

    with alt[1]:
        _render_korku_yikici(adaylar)

    with alt[2]:
        _render_kisisel_url(adaylar)


# ------------------------------------------------------------
# 1) GELECEGIN MINI KITABI
# ------------------------------------------------------------

def _render_gelecek_kitabi(adaylar: list[KayitAday]):
    """Aday icin kisisellestirilmis 10-12 sayfalik premium PDF kitap."""
    try:
        from models.kayit_gelecek_kitabi import (
            uret_ve_kaydet, uret_tum_bolumler, generate_gelecek_kitabi_pdf,
            BOLUM_BASLIKLARI, get_gelecek_kitabi_store,
        )
    except Exception as e:
        st.error(f"Modül yuklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#0B1E3F;border-left:4px solid #C8952E;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#C8952E;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        '1) Aday seç → 2) AI 5 bölüm üretir (Süper Güçler, 10 Yıl Sonra, Kariyer, Üniversite, Müdür Mektubu) → '
        '3) Premium PDF kitap hazır → 4) WhatsApp/email ile veliye gönder'
        '</div></div>',
        unsafe_allow_html=True
    )

    aday = _aday_secici(adaylar, "gk")
    if not aday:
        return

    kurum_adi = _kurum_adi_getir()
    store = get_gelecek_kitabi_store()
    gecmis = store.aday_gecmisi(aday.id)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.markdown(
            f'<div style="background:#131825;border:1px solid #334155;border-radius:8px;padding:10px 14px">'
            f'<div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase">Seçili Aday</div>'
            f'<div style="color:#e2e8f0;font-size:1rem;font-weight:700">{aday.ogrenci_adi}</div>'
            f'<div style="color:#64748b;font-size:0.8rem">{aday.veli_adi} • {aday.kademe or "-"} • {aday.hedef_sinif or "-"}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div style="background:#131825;border:1px solid #334155;border-radius:8px;padding:10px 14px;text-align:center">'
            f'<div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase">Önceki Üretim</div>'
            f'<div style="color:#C8952E;font-size:1.5rem;font-weight:800">{len(gecmis)}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c3:
        stats = store.istatistik()
        st.markdown(
            f'<div style="background:#131825;border:1px solid #334155;border-radius:8px;padding:10px 14px;text-align:center">'
            f'<div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase">Toplam</div>'
            f'<div style="color:#C8952E;font-size:1.5rem;font-weight:800">{stats.get("toplam_uretim", 0)}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Profil kontrol
    ogr = aday.ogrenci_profil or {}
    profil_dolu = bool(ogr.get("guclu_dersler") or ogr.get("hobiler") or ogr.get("ogrenci_istegi"))
    if not profil_dolu:
        st.warning(
            "💡 Daha iyi sonuç için Pipeline'dan adayın **Öğrenci Profili** kısmını doldurun "
            "(güçlü dersler, hobiler, öğrenci isteği). Bos ise AI genel bir sablon uretecek."
        )

    st.markdown("---")

    # AI kontrol
    _ai_var = bool(_os_env("OPENAI_API_KEY"))
    if not _ai_var:
        st.info("ℹ️ OPENAI_API_KEY tanımlı değil — sablon metinlerle PDF üretilecek.")

    cbtn1, cbtn2 = st.columns([1, 1])
    with cbtn1:
        uret_btn = st.button(
            "🎁 AI İle Kitap Üret",
            key="gk_uret_btn",
            type="primary",
            use_container_width=True,
        )
    with cbtn2:
        onizle_btn = st.button(
            "👁️ Bölüm Önizle (AI)",
            key="gk_onizle_btn",
            use_container_width=True,
        )

    # Önizleme
    if onizle_btn:
        with st.spinner("AI bölümleri üretiyor..."):
            bolumler = uret_tum_bolumler(aday, kurum_adi)
            st.session_state["_gk_son_bolumler"] = bolumler
            st.session_state["_gk_son_aday_id"] = aday.id

    if st.session_state.get("_gk_son_aday_id") == aday.id and st.session_state.get("_gk_son_bolumler"):
        st.markdown("#### 📖 Üretilen Bölümler")
        for key, baslik in BOLUM_BASLIKLARI:
            with st.expander(f"◆ {baslik}", expanded=False):
                metin = st.session_state["_gk_son_bolumler"].get(key, "")
                st.markdown(metin or "_Metin üretilemedi._")

    # PDF uret + indir
    if uret_btn:
        with st.spinner("Kitap hazırlanıyor (AI + PDF)..."):
            try:
                pdf_bytes, log = uret_ve_kaydet(aday, kurum_adi)
                if pdf_bytes:
                    st.session_state["_gk_son_pdf"] = pdf_bytes
                    st.session_state["_gk_son_pdf_ad"] = f"{aday.ogrenci_adi}_Yolculugu.pdf"
                    st.session_state["_gk_son_log"] = log.to_dict()
                    st.success(f"✅ Kitap hazır! {len(pdf_bytes) / 1024:.1f} KB • "
                               f"{'AI' if log.ai_kullanildi else 'Sablon'} kullanildi.")
                else:
                    st.error("PDF üretilemedi (ReportLab kurulu mu?).")
            except Exception as e:
                st.error(f"Hata: {e}")
                import traceback
                st.code(traceback.format_exc())

    if st.session_state.get("_gk_son_pdf"):
        st.download_button(
            label="📥 Kitabı İndir (PDF)",
            data=st.session_state["_gk_son_pdf"],
            file_name=st.session_state.get("_gk_son_pdf_ad", "gelecegin_kitabi.pdf"),
            mime="application/pdf",
            key="gk_download",
            use_container_width=True,
        )

    # Gecmis
    if gecmis:
        st.markdown("---")
        with st.expander(f"📚 Bu Aday İçin Önceki Üretimler ({len(gecmis)})", expanded=False):
            for lg in reversed(gecmis[-10:]):
                st.markdown(
                    f'<div style="background:#131825;border:1px solid #334155;border-radius:6px;'
                    f'padding:8px 12px;margin:4px 0">'
                    f'<div style="color:#e2e8f0;font-size:0.85rem">'
                    f'🗓️ {lg.olusturma_tarihi[:19]} • '
                    f'{"🤖 AI" if lg.ai_kullanildi else "📋 Sablon"} • '
                    f'{lg.pdf_byte_boyut / 1024:.1f} KB</div></div>',
                    unsafe_allow_html=True,
                )


# ------------------------------------------------------------
# 2) AI KORKU YIKICI
# ------------------------------------------------------------

def _render_korku_yikici(adaylar: list[KayitAday]):
    """Adayin itirazlarini bul + her birine AI cevap + PDF rapor."""
    try:
        from models.kayit_korku_yikici import (
            itirazlari_tespit_et, uret_tum_cevaplar, uret_ve_kaydet,
            get_korku_yikici_store, SABLON_CEVAPLAR,
        )
    except Exception as e:
        st.error(f"Modül yuklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#0B1E3F;border-left:4px solid #DC2626;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#DC2626;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        '1) Aday seç → 2) Notlarındaki tüm itirazlar otomatik bulunur → '
        '3) Her itiraz için AI empatik cevap üretir → 4) Premium PDF hazır → 5) Veliye gönder'
        '</div></div>',
        unsafe_allow_html=True
    )

    aday = _aday_secici(adaylar, "ky")
    if not aday:
        return

    kurum_adi = _kurum_adi_getir()
    store = get_korku_yikici_store()
    gecmis = store.aday_gecmisi(aday.id)

    # Onizleme: Tespit edilen itirazlar
    itirazlar = itirazlari_tespit_et(aday)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.markdown(
            f'<div style="background:#131825;border:1px solid #334155;border-radius:8px;padding:10px 14px">'
            f'<div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase">Seçili Aday</div>'
            f'<div style="color:#e2e8f0;font-size:1rem;font-weight:700">{aday.veli_adi}</div>'
            f'<div style="color:#64748b;font-size:0.8rem">{aday.ogrenci_adi} • {len(aday.aramalar)} arama • {len(aday.gorusmeler)} görüşme</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c2:
        _clr = "#DC2626" if itirazlar else "#16A34A"
        st.markdown(
            f'<div style="background:#131825;border:1px solid #334155;border-radius:8px;padding:10px 14px;text-align:center">'
            f'<div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase">Tespit Edilen İtiraz</div>'
            f'<div style="color:{_clr};font-size:1.8rem;font-weight:800">{len(itirazlar)}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div style="background:#131825;border:1px solid #334155;border-radius:8px;padding:10px 14px;text-align:center">'
            f'<div style="color:#94a3b8;font-size:0.7rem;text-transform:uppercase">Önceki Rapor</div>'
            f'<div style="color:#C8952E;font-size:1.8rem;font-weight:800">{len(gecmis)}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    if not itirazlar:
        st.info("ℹ️ Bu adayın notlarında itiraz tespit edilmedi. Görüşme/arama notlarını zenginleştirin.")
        with st.expander("📋 Desteklenen Itiraz Kategorileri", expanded=False):
            for kat in SABLON_CEVAPLAR.keys():
                st.markdown(f"- {kat}")
        return

    # Tespit edilen itirazlari listele
    st.markdown("#### 🎯 Tespit Edilen İtirazlar")
    for i, it in enumerate(itirazlar, 1):
        st.markdown(
            f'<div style="background:linear-gradient(90deg,#450a0a 0%,#1a0606 100%);'
            f'border-left:3px solid #DC2626;border-radius:6px;padding:8px 12px;margin:6px 0">'
            f'<div style="color:#fca5a5;font-size:0.7rem;font-weight:700">#{i:02d} • {it["kategori"]}</div>'
            f'<div style="color:#fecaca;font-size:0.82rem;margin-top:2px;font-style:italic">"{it["kaynak_metin"]}"</div>'
            f'<div style="color:#64748b;font-size:0.65rem;margin-top:2px">Eşleşme: {it["esleme"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    _ai_var = bool(_os_env("OPENAI_API_KEY"))
    if not _ai_var:
        st.info("ℹ️ OPENAI_API_KEY tanımlı değil — sablon cevaplarla PDF üretilecek.")

    cbtn1, cbtn2 = st.columns([1, 1])
    with cbtn1:
        uret_btn = st.button(
            "🛡️ AI İle Rapor Üret",
            key="ky_uret_btn",
            type="primary",
            use_container_width=True,
        )
    with cbtn2:
        onizle_btn = st.button(
            "👁️ Cevapları Önizle (AI)",
            key="ky_onizle_btn",
            use_container_width=True,
        )

    if onizle_btn:
        with st.spinner("AI cevaplari uretiyor..."):
            cevaplar = uret_tum_cevaplar(aday, kurum_adi)
            st.session_state["_ky_son_cevaplar"] = cevaplar
            st.session_state["_ky_son_aday_id"] = aday.id

    if st.session_state.get("_ky_son_aday_id") == aday.id and st.session_state.get("_ky_son_cevaplar"):
        st.markdown("#### 💬 AI Cevapları")
        for cv in st.session_state["_ky_son_cevaplar"]:
            with st.expander(f"🛡️ {cv['kategori']} → {cv.get('baslik', '')}", expanded=False):
                st.markdown(
                    f'<div style="background:#1a0606;border-left:3px solid #DC2626;border-radius:4px;padding:6px 10px;margin-bottom:8px">'
                    f'<div style="color:#fca5a5;font-size:0.75rem;font-weight:700">İtiraz:</div>'
                    f'<div style="color:#fecaca;font-size:0.82rem;font-style:italic">"{cv.get("kaynak_metin", "")}"</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"**{cv.get('baslik', '')}**")
                st.markdown(cv.get("govde", ""))
                st.markdown(
                    f'<div style="background:#C8952E20;border-left:3px solid #C8952E;border-radius:4px;padding:6px 10px;margin-top:6px">'
                    f'<div style="color:#C8952E;font-size:0.75rem;font-weight:700">➜ SONRAKİ ADIM</div>'
                    f'<div style="color:#e2e8f0;font-size:0.85rem">{cv.get("aksiyon", "")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    if uret_btn:
        with st.spinner("Rapor hazırlanıyor (AI + PDF)..."):
            try:
                pdf_bytes, log = uret_ve_kaydet(aday, kurum_adi)
                if pdf_bytes:
                    st.session_state["_ky_son_pdf"] = pdf_bytes
                    st.session_state["_ky_son_pdf_ad"] = f"{aday.veli_adi}_Endiselerinize_Cevap.pdf"
                    st.success(f"✅ Rapor hazır! {log.itiraz_sayisi} itiraz • {len(pdf_bytes) / 1024:.1f} KB")
                else:
                    st.error("PDF üretilemedi.")
            except Exception as e:
                st.error(f"Hata: {e}")

    if st.session_state.get("_ky_son_pdf"):
        st.download_button(
            label="📥 Korku Yıkıcı Raporunu İndir (PDF)",
            data=st.session_state["_ky_son_pdf"],
            file_name=st.session_state.get("_ky_son_pdf_ad", "korku_yikici.pdf"),
            mime="application/pdf",
            key="ky_download",
            use_container_width=True,
        )

    # Genel istatistik — en sik itirazlar
    _en_sik = store.en_sik_itirazlar(limit=5)
    if _en_sik:
        st.markdown("---")
        with st.expander("📊 Tüm Adaylarda En Sık İtirazlar", expanded=False):
            for item in _en_sik:
                st.markdown(f"- **{item['kategori']}** — {item['sayi']} kez")


# ------------------------------------------------------------
# 3) KISISEL URL + SUBE HOLD + TEK-TIK KAYIT
# ------------------------------------------------------------

def _render_kisisel_url(adaylar: list[KayitAday]):
    """Aday icin unique URL, sube hold ve tek-tik kayit paneli."""
    try:
        from models.kayit_kisisel_url import (
            aday_icin_url_olustur, url_hold_baslat, url_hold_iptal,
            tek_tik_kayit_tamamla, public_url_olustur, qr_kod_veri,
            get_kisisel_url_store, sube_varsayilan_olustur, istatistikler,
            SubeKapasite, HOLD_SURESI_SAAT,
        )
    except Exception as e:
        st.error(f"Modül yuklenemedi: {e}")
        return

    # Varsayilan subeleri hazirla
    sube_varsayilan_olustur()
    store = get_kisisel_url_store()

    st.markdown(
        '<div style="background:#0B1E3F;border-left:4px solid #3B82F6;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#3B82F6;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        '1) Aday seç → 2) Kişisel URL oluştur (otomatik slug) → 3) Veli kendi sayfasından şube seçer → '
        '4) 24 saat hold butonu → 5) Tek-tık kayıt. QR kod ile elden teslim hazır.'
        '</div></div>',
        unsafe_allow_html=True
    )

    # Genel istatistikler
    stats = istatistikler()
    sc = st.columns(5)
    _metrikler = [
        (sc[0], "Toplam URL", str(stats["toplam_url"]), "#3B82F6"),
        (sc[1], "Aktif Hold", str(stats["aktif_hold"]), "#C8952E"),
        (sc[2], "Tamamlanan", str(stats["tamamlanan_kayit"]), "#16A34A"),
        (sc[3], "Görüntülenme", str(stats["toplam_goruntulenme"]), "#8B5CF6"),
        (sc[4], "Dönüşüm %", f"%{stats['donusum_orani']}", "#EF4444"),
    ]
    for col, lbl, val, clr in _metrikler:
        with col:
            st.markdown(
                f'<div style="background:#131825;border:1px solid {clr}40;border-radius:8px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.4rem;font-weight:800">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    _ust_alt = st.tabs(["🔗 Aday URL Yönetimi", "🏫 Şube Kapasite", "📋 Tüm URL'ler"])

    # ── ALT: Aday URL yonetimi ──
    with _ust_alt[0]:
        aday = _aday_secici(adaylar, "ku")
        if aday:
            url = aday_icin_url_olustur(aday, olusturan="koordinator")
            # goruntulenme arttirma (koordinator bakiyor)
            # store.increment_goruntulenme(url.slug)   # koordinator icin saymiyoruz

            # Public URL
            try:
                _qp_base = _os_env("SMARTCAMPUS_PUBLIC_URL", "")
            except Exception:
                _qp_base = ""
            public_link = public_url_olustur(url.slug, _qp_base)

            # Kart
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#0B1E3F 0%,#1e293b 100%);'
                f'border:2px solid #3B82F640;border-radius:12px;padding:14px 18px;margin:8px 0">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">'
                f'<div>'
                f'<div style="color:#3B82F6;font-size:0.7rem;font-weight:700;letter-spacing:1px">KİŞİSEL URL SLUG</div>'
                f'<div style="color:#fff;font-size:1.4rem;font-weight:800;font-family:monospace">{url.slug}</div>'
                f'<div style="color:#94a3b8;font-size:0.75rem;margin-top:2px">{public_link}</div>'
                f'</div>'
                f'<div style="text-align:right">'
                f'<div style="color:#94a3b8;font-size:0.65rem">Görüntülenme</div>'
                f'<div style="color:#8B5CF6;font-size:1.4rem;font-weight:800">{url.goruntulenme_sayisi}</div>'
                f'</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

            # Kopyalanabilir link
            st.code(public_link, language="text")

            # QR kod
            try:
                import qrcode
                from io import BytesIO
                qr = qrcode.QRCode(version=1, box_size=8, border=3)
                qr.add_data(public_link)
                qr.make(fit=True)
                img = qr.make_image(fill_color="#0B1E3F", back_color="white")
                buf = BytesIO()
                img.save(buf, format="PNG")
                st.image(buf.getvalue(), caption=f"QR Kod — {url.slug}", width=220)
            except ImportError:
                st.info("📱 QR kod için `qrcode` paketi kurulu değil. Slug'ı manuel paylaşabilirsiniz.")
            except Exception as _qe:
                st.caption(f"QR kod üretilemedi: {_qe}")

            st.markdown("---")
            st.markdown("#### 🏫 Sınıf Seç & Hold Başlat")

            # Hedef sinif/kademe bazli sube gosterimi
            hedef = aday.hedef_sinif or ""
            tum_sinif = sorted({s.sinif for s in store.load_all_sube()})

            sec_sinif = st.selectbox(
                "Sınıf",
                options=tum_sinif or [""],
                index=tum_sinif.index(hedef) if hedef in tum_sinif else 0,
                key="ku_sec_sinif",
            )

            if sec_sinif:
                subeler = store.sinif_subeleri(sec_sinif)

                if not subeler:
                    st.warning(f"'{sec_sinif}' için şube tanımlı değil. Şube Kapasite sekmesinden ekleyin.")
                else:
                    # Sube kartlari
                    sb_cols = st.columns(min(len(subeler), 4))
                    for i, sb in enumerate(subeler):
                        with sb_cols[i % len(sb_cols)]:
                            kalan = sb.kalan()
                            clr = "#16A34A" if kalan > 5 else ("#C8952E" if kalan > 0 else "#DC2626")
                            durum = "MÜSAİT" if kalan > 5 else ("KRİTİK" if kalan > 0 else "DOLU")
                            st.markdown(
                                f'<div style="background:#131825;border:2px solid {clr}40;border-radius:10px;'
                                f'padding:12px;text-align:center;margin-bottom:8px">'
                                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">Şube</div>'
                                f'<div style="color:#fff;font-size:1.6rem;font-weight:800">{sb.sube}</div>'
                                f'<div style="color:{clr};font-size:0.7rem;font-weight:700">{durum}</div>'
                                f'<div style="margin:6px 0;height:6px;background:#0f172a;border-radius:3px;overflow:hidden">'
                                f'<div style="height:100%;width:{(sb.kayitli + sb.hold_sayisi) / max(sb.kapasite, 1) * 100:.0f}%;background:{clr}"></div>'
                                f'</div>'
                                f'<div style="color:#e2e8f0;font-size:0.75rem">{sb.kayitli}+{sb.hold_sayisi}/{sb.kapasite}</div>'
                                f'<div style="color:{clr};font-size:1rem;font-weight:800;margin-top:2px">{kalan} yer</div>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
                            if kalan > 0 and not url.hold_aktif and not url.kayit_tamamlandi:
                                if st.button(f"🔒 Hold ({HOLD_SURESI_SAAT}h)",
                                             key=f"ku_hold_{sb.id}",
                                             use_container_width=True):
                                    ok, msg = url_hold_baslat(url.slug, sb.id)
                                    if ok:
                                        st.success(msg)
                                        st.rerun()
                                    else:
                                        st.error(msg)

            st.markdown("---")

            # Aktif hold durumu
            if url.kayit_tamamlandi:
                st.success(
                    f"✅ **KAYIT TAMAMLANDI** • {url.hold_sinif} - {url.hold_sube} şubesine "
                    f"{url.kayit_tamamlanma_tarihi[:19]} tarihinde • Onay Kodu: `{url.kayit_onay_kodu}`"
                )
            elif url.hold_aktif:
                saat, dk, sn = url.hold_kalan_saat_dakika()
                st.markdown(
                    f'<div style="background:linear-gradient(90deg,#C8952E20,#0B1E3F);'
                    f'border:2px solid #C8952E;border-radius:10px;padding:14px 18px;margin:8px 0">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">'
                    f'<div>'
                    f'<div style="color:#C8952E;font-size:0.75rem;font-weight:700">🔒 AKTİF HOLD</div>'
                    f'<div style="color:#fff;font-size:1.2rem;font-weight:800">{url.hold_sinif} - {url.hold_sube}</div>'
                    f'<div style="color:#94a3b8;font-size:0.7rem">Başlangıç: {url.hold_baslangic[:19]}</div>'
                    f'</div>'
                    f'<div style="text-align:right">'
                    f'<div style="color:#94a3b8;font-size:0.65rem">Kalan Süre</div>'
                    f'<div style="color:#C8952E;font-size:1.8rem;font-weight:800;font-family:monospace">'
                    f'{saat:02d}:{dk:02d}:{sn:02d}</div>'
                    f'</div></div></div>',
                    unsafe_allow_html=True,
                )
                iptal_col, tamamla_col = st.columns(2)
                with iptal_col:
                    if st.button("❌ Hold İptal", key="ku_hold_iptal", use_container_width=True):
                        ok, msg = url_hold_iptal(url.slug)
                        if ok:
                            st.success(msg)
                            st.rerun()
                with tamamla_col:
                    if st.button("✅ TEK-TIK KAYIT TAMAMLA", key="ku_kayit_tamamla",
                                 type="primary", use_container_width=True):
                        ok, msg = tek_tik_kayit_tamamla(url.slug)
                        if ok:
                            st.success(msg)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(msg)
            else:
                st.info("💡 Bir şube seçip **Hold** butonuna basın — 24 saat rezervasyon başlayacak.")

    # ── ALT: Sube Kapasite ──
    with _ust_alt[1]:
        st.markdown("#### 🏫 Şube Kapasite Yönetimi")
        tum_sube = store.load_all_sube()

        if tum_sube:
            for sb in tum_sube:
                canli = next(iter(store.sinif_subeleri(sb.sinif) or []), sb)
                hld = next((x for x in store.sinif_subeleri(sb.sinif) if x.id == sb.id), sb)
                co1, co2, co3, co4, co5 = st.columns([2, 1, 1, 1, 1])
                with co1:
                    st.markdown(f"**{sb.sinif} - {sb.sube}**")
                with co2:
                    st.caption(f"Kapasite: {sb.kapasite}")
                with co3:
                    st.caption(f"Kayıtlı: {sb.kayitli}")
                with co4:
                    st.caption(f"Hold: {hld.hold_sayisi}")
                with co5:
                    st.caption(f"**Kalan: {hld.kalan()}**")

        with st.expander("➕ Yeni Şube Ekle", expanded=False):
            with st.form("ku_yeni_sube", clear_on_submit=True):
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    sinif = st.text_input("Sınıf (ör. 5. Sinif)", key="ku_sube_sinif")
                with c2:
                    sube = st.text_input("Şube", value="A", key="ku_sube_sube")
                with c3:
                    kapasite = st.number_input("Kapasite", min_value=1, max_value=60, value=24, key="ku_sube_kap")
                kayitli = st.number_input("Mevcut Kayıtlı Sayısı", min_value=0, max_value=60, value=0, key="ku_sube_kayitli")
                if st.form_submit_button("Kaydet", type="primary", use_container_width=True):
                    if sinif and sube:
                        store.add_sube(SubeKapasite(sinif=sinif, sube=sube, kapasite=int(kapasite), kayitli=int(kayitli)))
                        st.success("Şube eklendi.")
                        st.rerun()
                    else:
                        st.error("Sınıf ve Şube alanları zorunlu.")

    # ── ALT: Tum URL listesi ──
    with _ust_alt[2]:
        st.markdown("#### 📋 Tüm Kişisel URL'ler")
        tum_url = store.load_all_urls()
        if not tum_url:
            st.info("Henüz kişisel URL üretilmedi. Aday seçip URL oluşturun.")
        else:
            # Durum gore siralama
            def _sira(u):
                if u.kayit_tamamlandi:
                    return 3
                if u.hold_aktif:
                    return 0  # en ust
                return 1
            tum_url_srt = sorted(tum_url, key=_sira)
            for u in tum_url_srt:
                if u.kayit_tamamlandi:
                    clr = "#16A34A"
                    durum = f"✅ KAYIT TAMAM ({u.hold_sinif}-{u.hold_sube})"
                elif u.hold_aktif:
                    sa, dk, _sn = u.hold_kalan_saat_dakika()
                    clr = "#C8952E"
                    durum = f"🔒 HOLD {sa}s {dk}dk ({u.hold_sinif}-{u.hold_sube})"
                else:
                    clr = "#64748B"
                    durum = "○ Pasif"
                st.markdown(
                    f'<div style="background:#131825;border-left:3px solid {clr};border-radius:6px;'
                    f'padding:8px 12px;margin:4px 0">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap">'
                    f'<div>'
                    f'<div style="color:#e2e8f0;font-size:0.88rem;font-weight:700">{u.veli_adi} — {u.ogrenci_adi}</div>'
                    f'<div style="color:#64748b;font-size:0.7rem">slug: <code>{u.slug}</code> • '
                    f'{u.goruntulenme_sayisi} görüntülenme • oluşturulma: {u.olusturma_tarihi[:10]}</div>'
                    f'</div>'
                    f'<div style="color:{clr};font-size:0.78rem;font-weight:700">{durum}</div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )


# ------------------------------------------------------------
# Yardimci (os.environ access without top-level import)
# ------------------------------------------------------------

def _os_env(key: str, default: str = "") -> str:
    import os
    return os.environ.get(key, default)


# ============================================================
# ZEKI MOTORLAR — 3 MODUL
# 1) Pişmanlık Motoru (kayip adaylari zamanla geri kazanma)
# 2) Çocuğun İç Sesi (cocuga ozel mini anket + duygu analizi)
# 3) Sessiz Red Dedektörü (gizli kaybi onceden sezme)
# ============================================================

def _render_zeki_motorlar(store: KayitDataStore, adaylar: list[KayitAday]):
    """Ana giris — 3 zeki motor alt sekmesi."""
    st.markdown(
        '<div style="background:linear-gradient(135deg,#1a0b3d 0%,#0f172a 50%,#1a0b3d 100%);'
        'border:1px solid #8b5cf640;border-radius:14px;padding:16px 20px;margin-bottom:12px;'
        'box-shadow:0 4px 20px #8b5cf615">'
        '<div style="display:flex;align-items:center;gap:10px">'
        '<div style="font-size:1.6rem">🧠</div>'
        '<div>'
        '<div style="color:#a78bfa;font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase">PREMIUM ZEKI MOTORLAR</div>'
        '<div style="color:#fff;font-size:1.2rem;font-weight:700">Diğer Sistemlerin Göremediği 3 Silah</div>'
        '<div style="color:#94a3b8;font-size:0.8rem;margin-top:2px">Zamana karşı savaş • Gerçek karar vericiye ulaşma • Gizli kaybı önceden sezme</div>'
        '</div></div></div>',
        unsafe_allow_html=True
    )

    alt = st.tabs([
        "🕰️ Pişmanlık Madenciliği",
        "🎙️ Çocuğun İç Sesi",
        "🔮 Sessiz Red Dedektörü",
    ])

    with alt[0]:
        _render_pismanlik_motoru(adaylar)

    with alt[1]:
        _render_cocuk_sesi(adaylar)

    with alt[2]:
        _render_sessiz_red(adaylar)


# ------------------------------------------------------------
# 1) PISMANLIK MOTORU
# ------------------------------------------------------------

def _render_pismanlik_motoru(adaylar: list[KayitAday]):
    """Olumsuz adaylari 3/6/12 ay zincirinde yeniden dogurma."""
    try:
        from models.kayit_pismanlik_motoru import (
            pismanlik_tarama, dokunma_tetikle, geri_donus_kaydet,
            istatistikler, DOKUNMA_ESIKLERI, OLUMSUZ_NEDEN_KATEGORI,
        )
    except Exception as e:
        st.error(f"Modül yuklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#1a0b3d;border-left:4px solid #a78bfa;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#a78bfa;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        'Olumsuz olmuş adaylar silinmez — zaman makinesine girer. '
        '90/180/365 günde otomatik olarak AI kişisel mesaj üretilir. '
        'Rakip unuttu, biz unutmadık.'
        '</div></div>',
        unsafe_allow_html=True
    )

    kurum_adi = _kurum_adi_getir()
    taranan = pismanlik_tarama(adaylar)
    stats = istatistikler()

    # Ust stat kartlari
    sc = st.columns(5)
    _stats = [
        (sc[0], "Takipte", str(len(taranan)), "#a78bfa"),
        (sc[1], "Hazır Dokunma", str(sum(1 for x in taranan if x["hazir"])), "#C8952E"),
        (sc[2], "Geri Dönüş", str(stats["geri_donus_sayisi"]), "#16A34A"),
        (sc[3], "Dönüşüm", str(stats["donusum_sayisi"]), "#22c55e"),
        (sc[4], "Geri Dön %", f"%{stats['geri_donus_orani']}", "#EF4444"),
    ]
    for col, lbl, val, clr in _stats:
        with col:
            st.markdown(
                f'<div style="background:#131825;border:1px solid {clr}40;border-radius:8px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.4rem;font-weight:800">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    if not taranan:
        st.info("ℹ️ Henüz 'olumsuz' aşamasında aday yok. Bu motor olumsuz olan adaylar üzerinde çalışır.")
        return

    # Filtreleme
    fc1, fc2 = st.columns([2, 1])
    with fc1:
        filt = st.radio(
            "Göster",
            options=["Hazır Olanlar (Dokunma Zamanı)", "Tümü"],
            horizontal=True,
            key="pm_filt",
        )
    with fc2:
        neden_filt = st.selectbox(
            "Neden",
            options=["Tümü"] + list(OLUMSUZ_NEDEN_KATEGORI.keys()),
            key="pm_neden",
        )

    filtrelenmis = taranan
    if filt == "Hazır Olanlar (Dokunma Zamanı)":
        filtrelenmis = [x for x in filtrelenmis if x["hazir"]]
    if neden_filt != "Tümü":
        filtrelenmis = [x for x in filtrelenmis if x["olumsuz_neden"] == neden_filt]

    st.markdown(f"#### 🕰️ {len(filtrelenmis)} Aday Listelendi")

    for idx, item in enumerate(filtrelenmis[:30]):
        aday = item["aday"]
        gun = item["gun_gecti"]
        neden = item["olumsuz_neden"]
        esik = item["sonraki_esik"]
        hazir = item["hazir"]

        clr = "#C8952E" if hazir else "#64748B"
        sembol = "🔥" if hazir else "⏳"

        with st.container():
            st.markdown(
                f'<div style="background:linear-gradient(90deg,#1a0b3d20,#131825);'
                f'border-left:3px solid {clr};border-radius:8px;padding:10px 14px;margin:6px 0">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'
                f'<div>'
                f'<div style="color:#e2e8f0;font-size:0.95rem;font-weight:700">{sembol} {item["veli_adi"]} — {item["ogrenci_adi"]}</div>'
                f'<div style="color:#94a3b8;font-size:0.75rem">'
                f'Olumsuz: <b style="color:#fca5a5">{gun} gün önce</b> • '
                f'Neden: <b style="color:#{clr[1:]}">{neden}</b>'
                f'</div>'
                f'</div>'
                f'<div style="color:{clr};font-size:0.8rem;font-weight:700">'
                f'{"➜ " + esik["etiket"] + " dokunması hazır" if esik else "Zincir tamamlandi"}'
                f'</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

            if hazir:
                cb1, cb2, cb3 = st.columns([1, 1, 1])
                with cb1:
                    if st.button(f"🤖 AI Mesaj Üret", key=f"pm_uret_{idx}", use_container_width=True):
                        with st.spinner("AI mesaj hazırlıyor..."):
                            mesaj = dokunma_tetikle(aday, esik, "whatsapp", kurum_adi)
                            st.session_state[f"_pm_son_mesaj_{idx}"] = mesaj

                son_mesaj = st.session_state.get(f"_pm_son_mesaj_{idx}")
                if son_mesaj:
                    with st.expander(f"📬 Üretilen Mesaj — {son_mesaj['etiket']}", expanded=True):
                        st.markdown(f"**Konu:** {son_mesaj['konu']}")
                        st.markdown(f"**Mesaj:**")
                        st.text_area(
                            "Kopyalanabilir",
                            value=son_mesaj["govde"],
                            height=120,
                            key=f"pm_text_{idx}",
                            label_visibility="collapsed",
                        )
                        st.caption(
                            f"{'🤖 AI üretti' if son_mesaj['ai_kullanildi'] else '📋 Şablon'} • "
                            f"Tarih: {son_mesaj['tarih'][:16]}"
                        )
                        if st.button(f"✅ Geri Dönüş Aldım (kaydet)", key=f"pm_geri_{idx}"):
                            geri_donus_kaydet(item["aday_id"], "Koordinator geri dönüş bildirdi")
                            st.success("Geri dönüş kaydedildi.")
                            st.rerun()

            st.markdown("")

    if len(filtrelenmis) > 30:
        st.caption(f"... ve {len(filtrelenmis) - 30} aday daha")


# ------------------------------------------------------------
# 2) COCUGUN IC SESI
# ------------------------------------------------------------

def _render_cocuk_sesi(adaylar: list[KayitAday]):
    """8+ yas cocuga 4 mini soru + AI analiz."""
    try:
        from models.kayit_cocuk_sesi import (
            COCUK_SORULARI, kaydet_ve_analiz, get_cocuk_sesi_store,
            istatistikler,
        )
    except Exception as e:
        st.error(f"Modül yuklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#1a0b3d;border-left:4px solid #ec4899;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#ec4899;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        'Çocuk, veliden <b>ayrı</b> bir odada 4 soruya cevap verir. '
        'AI duygu analizi yapar + en çarpıcı alıntıları çıkarır. '
        'Velinin paneline "Çocuğunuzun Sesi" kartı düşer → karar anında veliyi ikna eder.'
        '</div></div>',
        unsafe_allow_html=True
    )

    store = get_cocuk_sesi_store()
    stats = istatistikler()

    # Ust stat
    sc = st.columns(5)
    _s = [
        (sc[0], "Toplam Kayıt", str(stats["toplam"]), "#ec4899"),
        (sc[1], "Çok Olumlu", str(stats.get("cok_olumlu_sayi", 0)), "#22c55e"),
        (sc[2], "Gelmek İsteyen", str(stats.get("gelmek_isteyen", 0)), "#10b981"),
        (sc[3], "Olumsuz", str(stats.get("olumsuz_sayi", 0)), "#ef4444"),
        (sc[4], "Ortalama Duygu", f"{stats.get('ortalama_duygu', 0):+.2f}", "#a78bfa"),
    ]
    for col, lbl, val, clr in _s:
        with col:
            st.markdown(
                f'<div style="background:#131825;border:1px solid {clr}40;border-radius:8px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.4rem;font-weight:800">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    _ust = st.tabs(["➕ Yeni Kayıt", "📋 Geçmiş Kayıtlar"])

    with _ust[0]:
        aday = _aday_secici(adaylar, "cs")
        if not aday:
            return

        mevcut = store.get_by_aday(aday.id)
        if mevcut:
            st.info(
                f"ℹ️ Bu aday için son kayıt: {mevcut.kayit_tarihi[:16]} — "
                f"Duygu: **{mevcut.duygu_etiket}** ({mevcut.duygu_skoru:+.2f})"
            )

        st.markdown("#### 🎙️ 4 Soru — Çocuğa Sor")
        st.caption("Çocuk rehber odasında, velisi olmadan cevap verir. Koordinatör cevapları yazar.")

        cevaplar = {}
        with st.form("cs_form", clear_on_submit=False):
            for soru in COCUK_SORULARI:
                st.markdown(f"**{soru['soru']}**")
                st.caption(f"💡 {soru['ipucu']}")
                cevaplar[soru["id"]] = st.text_area(
                    f"Cevap",
                    key=f"cs_{soru['id']}",
                    height=80,
                    label_visibility="collapsed",
                )
                st.markdown("")

            kayit_alan = st.text_input("Kaydı Alan (Rehber/Koordinator)", key="cs_kayit_alan")

            submit = st.form_submit_button(
                "🎙️ Kaydet ve AI Analiz Et",
                type="primary",
                use_container_width=True,
            )

        if submit:
            if not any(v.strip() for v in cevaplar.values()):
                st.error("En az bir cevap girmelisiniz.")
            else:
                with st.spinner("AI cocugun sesini analiz ediyor..."):
                    sesi = kaydet_ve_analiz(aday, cevaplar, kayit_alan)
                    st.session_state["_cs_son_sesi"] = sesi.id
                    st.success("✅ Kayıt ve analiz tamamlandı.")
                    st.rerun()

        # Son kayit analizini goster
        if st.session_state.get("_cs_son_sesi"):
            son = next((x for x in store.load_all() if x.id == st.session_state["_cs_son_sesi"]), None)
            if son:
                _cs_goster_analiz(son)

    with _ust[1]:
        tum = store.load_all()
        if not tum:
            st.info("Henüz çocuk sesi kaydı yok.")
        else:
            secenekler = {
                f"{x.ogrenci_adi} ({x.duygu_etiket}) — {x.kayit_tarihi[:10]}": x
                for x in sorted(tum, key=lambda x: x.kayit_tarihi, reverse=True)
            }
            secili = st.selectbox("Kayıt Seç", options=list(secenekler.keys()), key="cs_gecmis_sec")
            if secili:
                _cs_goster_analiz(secenekler[secili])


def _cs_goster_analiz(sesi):
    """Bir CocukSesi kaydinin analizini gorsel olarak goster."""
    skor = sesi.duygu_skoru
    etiket = sesi.duygu_etiket

    # Duygu rengi
    if skor >= 0.5:
        clr = "#22c55e"
    elif skor >= 0.15:
        clr = "#84cc16"
    elif skor >= -0.15:
        clr = "#a78bfa"
    elif skor >= -0.5:
        clr = "#f97316"
    else:
        clr = "#ef4444"

    st.markdown("---")
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{clr}15,#131825);'
        f'border:2px solid {clr}60;border-radius:12px;padding:16px 20px;margin:10px 0">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">'
        f'<div>'
        f'<div style="color:{clr};font-size:0.75rem;font-weight:700;letter-spacing:1px">ÇOCUĞUN İÇ SESİ</div>'
        f'<div style="color:#fff;font-size:1.3rem;font-weight:800">{sesi.ogrenci_adi}</div>'
        f'<div style="color:#94a3b8;font-size:0.75rem">Kayıt: {sesi.kayit_tarihi[:16]} • {sesi.kayit_alan or "—"}</div>'
        f'</div>'
        f'<div style="text-align:right">'
        f'<div style="color:{clr};font-size:2rem;font-weight:800">{skor:+.2f}</div>'
        f'<div style="color:{clr};font-size:0.85rem;font-weight:700">{etiket}</div>'
        f'</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.metric("Mevcut Okul", sesi.mevcut_okul_memnuniyet)
    with mc2:
        st.metric("Gelmek İstiyor", sesi.gelmek_istiyor)
    with mc3:
        st.metric("İlgi Alanı", str(len(sesi.ilgi_alanlari)))

    if sesi.ilgi_alanlari:
        st.markdown("##### 🎯 İlgi Alanları")
        chip_html = ""
        for ilgi in sesi.ilgi_alanlari:
            chip_html += (
                f'<span style="display:inline-block;background:#1a0b3d;border:1px solid #ec489940;'
                f'color:#fbcfe8;padding:4px 10px;border-radius:12px;font-size:0.75rem;'
                f'font-weight:600;margin:2px">{ilgi}</span>'
            )
        st.markdown(chip_html, unsafe_allow_html=True)

    if sesi.carpici_alintilar:
        st.markdown("##### 💬 Velinin Panelinde Görecek Alıntılar")
        for al in sesi.carpici_alintilar:
            st.markdown(
                f'<div style="background:#0f172a;border-left:3px solid #ec4899;'
                f'border-radius:6px;padding:10px 14px;margin:6px 0">'
                f'<div style="color:#fbcfe8;font-size:0.95rem;font-style:italic">'
                f'"{al.get("alinti", "")}"</div>'
                f'<div style="color:#94a3b8;font-size:0.7rem;margin-top:4px">'
                f'💡 {al.get("vurgu", "")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if sesi.aksiyon_onerileri:
        st.markdown("##### 🎯 Koordinatöre Öneriler")
        for i, ak in enumerate(sesi.aksiyon_onerileri, 1):
            st.markdown(f"{i}. {ak}")

    with st.expander("📋 Ham Cevaplar", expanded=False):
        try:
            from models.kayit_cocuk_sesi import COCUK_SORULARI
            for soru in COCUK_SORULARI:
                cvp = sesi.cevaplar.get(soru["id"], "")
                if cvp:
                    st.markdown(f"**{soru['soru']}**")
                    st.markdown(f"> {cvp}")
        except Exception:
            st.json(sesi.cevaplar)


# ------------------------------------------------------------
# 3) SESSIZ RED DEDEKTORU
# ------------------------------------------------------------

def _render_sessiz_red(adaylar: list[KayitAday]):
    """Pipeline'da duran adaylarin sessiz red tahmini."""
    try:
        from models.kayit_sessiz_red import (
            toplu_tarama, tarama_ozet, gecmis_kayip_pattern,
        )
    except Exception as e:
        st.error(f"Modül yuklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#1a0b3d;border-left:4px solid #06b6d4;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#06b6d4;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        'Pipeline\'da duran adayın %40\'ı sessizce red veriyor ama söylemiyor. '
        'Sistem geçmiş kayıpların pattern\'ını öğrenir ve <b>"72 saat içinde ölecek"</b> diyen adayları '
        'kırmızı alarmla işaretler + 3 kurtarma aksiyonu önerir.'
        '</div></div>',
        unsafe_allow_html=True
    )

    # Taramayi yap
    with st.spinner("Davranis pattern'i analiz ediliyor..."):
        risk_listesi = toplu_tarama(adaylar)
        ozet = tarama_ozet(adaylar)

    # Ust stat
    sc = st.columns(5)
    _s = [
        (sc[0], "Taranan", str(ozet["toplam_taranan"]), "#06b6d4"),
        (sc[1], "🚨 KRİTİK", str(ozet["kritik_sayi"]), "#ef4444"),
        (sc[2], "⚠️ Yüksek", str(ozet["yuksek_sayi"]), "#f97316"),
        (sc[3], "👁️ İzle", str(ozet["izle_sayi"]), "#facc15"),
        (sc[4], "Öğrenilen", str(ozet["pattern_ornek_sayi"]), "#a78bfa"),
    ]
    for col, lbl, val, clr in _s:
        with col:
            st.markdown(
                f'<div style="background:#131825;border:1px solid {clr}40;border-radius:8px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.4rem;font-weight:800">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if ozet["pattern_ornek_sayi"] == 0:
        st.warning(
            "⚠️ Henüz 'olumsuz' olmuş aday yok — sistem varsayılan pattern kullanıyor. "
            "İlk kayıplar olduğunda doğruluk dramatik şekilde artacak."
        )
    else:
        st.caption(
            f"📊 Öğrenilen pattern: {ozet['pattern_ornek_sayi']} olumsuz adaydan • "
            f"Ort. son temas: {ozet['ortalama_son_temas_gun']} gün • "
            f"Ort. arama: {ozet['ortalama_arama']} • "
            f"Ort. görüşme: {ozet['ortalama_gorusme']}"
        )

    st.markdown("---")

    if not risk_listesi:
        st.success("✅ Harika! Şu an hiçbir aday sessiz red riski altında değil.")
        return

    # Kritik alarm banner'i
    if ozet["kritik_sayi"] > 0:
        st.markdown(
            f'<div style="background:linear-gradient(90deg,#450a0a,#7f1d1d);'
            f'border:2px solid #ef4444;border-radius:10px;padding:14px 18px;margin:8px 0;'
            f'box-shadow:0 0 20px #ef444440">'
            f'<div style="color:#fecaca;font-size:0.8rem;font-weight:700;letter-spacing:1px">🚨 KRİTİK ALARM</div>'
            f'<div style="color:#fff;font-size:1.1rem;font-weight:800;margin-top:4px">'
            f'{ozet["kritik_sayi"]} aday 72 saat içinde sessizce red verebilir</div>'
            f'<div style="color:#fca5a5;font-size:0.8rem;margin-top:2px">'
            f'SON ŞANS — aşağıdaki aksiyonları bugün yap.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Risk listesi
    filt_secim = st.radio(
        "Göster",
        options=["Sadece Kritik", "Kritik + Yüksek", "Tümü"],
        horizontal=True,
        index=1,
        key="sr_filt",
    )

    if filt_secim == "Sadece Kritik":
        gosterilen = [x for x in risk_listesi if x["seviye"] == "KRITIK"]
    elif filt_secim == "Kritik + Yüksek":
        gosterilen = [x for x in risk_listesi if x["seviye"] in ("KRITIK", "Yuksek")]
    else:
        gosterilen = risk_listesi

    st.markdown(f"#### 🔮 {len(gosterilen)} Aday Risk Altında")

    for idx, item in enumerate(gosterilen[:20]):
        skor = item["skor"]
        seviye = item["seviye"]
        tahmini = item["tahmini_olum_gun"]

        if seviye == "KRITIK":
            clr = "#ef4444"
            bg = "#450a0a"
            emoji = "🚨"
        elif seviye == "Yuksek":
            clr = "#f97316"
            bg = "#431407"
            emoji = "⚠️"
        else:
            clr = "#facc15"
            bg = "#422006"
            emoji = "👁️"

        with st.expander(
            f"{emoji} {item['veli_adi']} — {item['ogrenci_adi']} • "
            f"SKOR: {skor}/100 • TAHMİNİ: {tahmini} gün",
            expanded=(seviye == "KRITIK" and idx < 3),
        ):
            # Kart ust
            st.markdown(
                f'<div style="background:linear-gradient(135deg,{bg},#0f172a);'
                f'border-left:4px solid {clr};border-radius:8px;padding:12px 16px;margin:6px 0">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">'
                f'<div>'
                f'<div style="color:{clr};font-size:0.7rem;font-weight:700">{seviye}</div>'
                f'<div style="color:#fff;font-size:1rem;font-weight:800">{item["veli_adi"]}</div>'
                f'<div style="color:#94a3b8;font-size:0.78rem">{item["ogrenci_adi"]} • Aşama: {item["asama"]}</div>'
                f'</div>'
                f'<div style="text-align:right">'
                f'<div style="color:#94a3b8;font-size:0.65rem">Sessiz Red Skoru</div>'
                f'<div style="color:{clr};font-size:2rem;font-weight:800;line-height:1">{skor}</div>'
                f'<div style="color:{clr};font-size:0.7rem">⏳ ~{tahmini} gün</div>'
                f'</div></div></div>',
                unsafe_allow_html=True,
            )

            # Kritik mesaj
            if item.get("kritik_mesaj"):
                st.markdown(
                    f'<div style="background:#7f1d1d;color:#fff;padding:8px 12px;'
                    f'border-radius:6px;margin:6px 0;font-size:0.85rem;font-weight:700">'
                    f'{item["kritik_mesaj"]}</div>',
                    unsafe_allow_html=True,
                )

            # Tetiklenen sinyaller
            if item.get("sinyaller"):
                st.markdown("**📡 Tetiklenen Sinyaller:**")
                for s in item["sinyaller"]:
                    st.markdown(
                        f'<div style="color:#cbd5e1;font-size:0.82rem;padding:3px 8px;'
                        f'background:#0f172a;border-left:2px solid {clr};margin:3px 0;border-radius:4px">'
                        f'<b style="color:{clr}">+{s["katki"]}</b> • {s["aciklama"]}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            # Kurtarma aksiyonlari
            if item.get("kurtarma_onerileri"):
                st.markdown("**🛡️ 3 Kurtarma Aksiyonu:**")
                for i, aksi in enumerate(item["kurtarma_onerileri"], 1):
                    st.markdown(
                        f'<div style="color:#e2e8f0;font-size:0.85rem;padding:6px 10px;'
                        f'background:#0f172a;border-left:2px solid #16a34a;margin:3px 0;'
                        f'border-radius:4px">'
                        f'<b style="color:#22c55e">{i}.</b> {aksi}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

    if len(gosterilen) > 20:
        st.caption(f"... ve {len(gosterilen) - 20} aday daha")


# ============================================================
# UST DUZEY — 3 STRATEJIK MODUL
# 1) Gelir Optimizasyon (Dynamic Personalized Pricing)
# 2) Kurumsal Kanal (B2B Pipeline)
# 3) CEO Command Center (Executive Cockpit)
# ============================================================

def _render_ust_duzey(store: KayitDataStore, adaylar: list[KayitAday]):
    """Ust Duzey modulun ana render fonksiyonu — 3 alt sekme."""
    st.markdown(
        '<div style="background:linear-gradient(135deg,#0B1E3F 0%,#1e1065 50%,#0B1E3F 100%);'
        'border:2px solid #C8952E60;border-radius:14px;padding:16px 20px;margin-bottom:12px;'
        'box-shadow:0 4px 30px #C8952E20">'
        '<div style="display:flex;align-items:center;gap:12px">'
        '<div style="font-size:1.8rem">👑</div>'
        '<div>'
        '<div style="color:#C8952E;font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase">EXECUTIVE STRATEJIK KATMAN</div>'
        '<div style="color:#fff;font-size:1.3rem;font-weight:800">Üst Düzey Kontrol Merkezi</div>'
        '<div style="color:#cbd5e1;font-size:0.82rem;margin-top:2px">Revenue Management • B2B Satış Kanalı • CEO Command Center</div>'
        '</div></div></div>',
        unsafe_allow_html=True
    )

    alt = st.tabs([
        "🎯 CEO Command Center",
        "💎 Gelir Optimizasyon",
        "🏢 Kurumsal Kanal (B2B)",
    ])

    with alt[0]:
        _render_ceo_cockpit(adaylar)

    with alt[1]:
        _render_gelir_optimizasyon(adaylar)

    with alt[2]:
        _render_kurumsal_kanal()


# ------------------------------------------------------------
# 1) CEO COMMAND CENTER
# ------------------------------------------------------------

def _render_ceo_cockpit(adaylar: list[KayitAday]):
    """Executive cockpit — morning briefing + metrikler."""
    try:
        from models.kayit_ceo_cockpit import morning_briefing, hizli_metrik_ozeti
    except Exception as e:
        st.error(f"CEO Cockpit yuklenemedi: {e}")
        return

    kurum_adi = _kurum_adi_getir()

    # Ust hero — saat + tarih + selamlama
    from datetime import datetime as _dt
    now = _dt.now()
    saat = now.hour
    selam = "Günaydın" if saat < 12 else ("İyi öğlenler" if saat < 18 else "İyi akşamlar")

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0B1E3F 0%,#1e293b 100%);'
        f'border-left:4px solid #C8952E;border-radius:12px;padding:20px 24px;margin:10px 0">'
        f'<div style="color:#C8952E;font-size:0.72rem;font-weight:700;letter-spacing:2px">'
        f'{now.strftime("%d %B %Y").upper()} • {now.strftime("%H:%M")}</div>'
        f'<div style="color:#fff;font-size:1.8rem;font-weight:800;margin-top:6px">'
        f'🌅 {selam}, {kurum_adi or "Müdürüm"}</div>'
        f'<div style="color:#94a3b8;font-size:0.85rem;margin-top:4px">'
        f'Bugünün stratejik brifingi hazır. 3 karar — 1 tehlike — 1 fırsat.</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Cache kontrol
    cache_key = f"_ceo_briefing_{date.today().isoformat()}"
    cached = st.session_state.get(cache_key)

    bc1, bc2 = st.columns([3, 1])
    with bc1:
        if cached:
            st.caption(f"✓ Cached briefing — {cached.get('tarih', '')}")
        else:
            st.caption("Briefing henüz üretilmedi")
    with bc2:
        if st.button("🔄 Yeni Briefing", key="ceo_refresh", use_container_width=True):
            with st.spinner("AI stratejik analiz yapıyor..."):
                cached = morning_briefing(adaylar, kurum_adi)
                st.session_state[cache_key] = cached
                st.rerun()

    if not cached:
        if st.button("🎯 Sabah Brifingi Oluştur", key="ceo_create", type="primary", use_container_width=True):
            with st.spinner("AI tüm modüllerden veri topluyor..."):
                cached = morning_briefing(adaylar, kurum_adi)
                st.session_state[cache_key] = cached
                st.rerun()
        return

    st.markdown("---")

    # Brifing kartları
    briefing = cached

    # 1. KRİTİK KARAR
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#7f1d1d 0%,#1a0606 100%);'
        f'border:2px solid #DC2626;border-radius:12px;padding:14px 18px;margin:10px 0;'
        f'box-shadow:0 0 25px #DC262640">'
        f'<div style="color:#fca5a5;font-size:0.72rem;font-weight:700;letter-spacing:2px">🚨 BUGÜNÜN EN KRİTİK KARARI</div>'
        f'<div style="color:#fff;font-size:1.05rem;font-weight:700;margin-top:6px;line-height:1.5">'
        f'{briefing["kritik_karar"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 2. FİNANSAL RADAR
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);'
        f'border-left:4px solid #22c55e;border-radius:8px;padding:14px 18px;margin:10px 0">'
        f'<div style="color:#86efac;font-size:0.72rem;font-weight:700;letter-spacing:2px">💰 FİNANSAL RADAR</div>'
        f'<div style="color:#e2e8f0;font-size:0.95rem;margin-top:6px;line-height:1.5">'
        f'{briefing["finansal_radar"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 3. TEHLIKE + FIRSAT (yan yana)
    tc1, tc2 = st.columns(2)
    with tc1:
        st.markdown(
            f'<div style="background:#1a0606;border-left:4px solid #F97316;'
            f'border-radius:8px;padding:14px 18px;margin:6px 0;height:140px;overflow:hidden">'
            f'<div style="color:#fed7aa;font-size:0.72rem;font-weight:700;letter-spacing:2px">⚠️ TEHLİKE</div>'
            f'<div style="color:#e2e8f0;font-size:0.88rem;margin-top:6px;line-height:1.5">'
            f'{briefing["tehlike"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with tc2:
        st.markdown(
            f'<div style="background:#1a1b0b;border-left:4px solid #C8952E;'
            f'border-radius:8px;padding:14px 18px;margin:6px 0;height:140px;overflow:hidden">'
            f'<div style="color:#fde68a;font-size:0.72rem;font-weight:700;letter-spacing:2px">🎁 FIRSAT</div>'
            f'<div style="color:#e2e8f0;font-size:0.88rem;margin-top:6px;line-height:1.5">'
            f'{briefing["firsat"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # 4. GÜN ÖZETİ (AI)
    if briefing.get("gun_ozeti"):
        st.markdown(
            f'<div style="background:#131825;border:1px dashed #C8952E60;'
            f'border-radius:8px;padding:10px 14px;margin:10px 0;text-align:center">'
            f'<div style="color:#C8952E;font-size:0.68rem;font-weight:700;letter-spacing:2px">GÜNÜN ÖZETİ</div>'
            f'<div style="color:#cbd5e1;font-size:0.85rem;margin-top:4px;font-style:italic">'
            f'"{briefing["gun_ozeti"]}"</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # 5. ANA METRİKLER
    st.markdown("---")
    st.markdown("#### 📊 Ana Metrikler")
    metrikler = briefing.get("metrikler", [])
    if metrikler:
        cols = st.columns(len(metrikler))
        for i, (lbl, val, clr) in enumerate(metrikler):
            with cols[i]:
                st.markdown(
                    f'<div style="background:#131825;border:1px solid {clr}40;border-radius:10px;'
                    f'padding:12px 8px;text-align:center">'
                    f'<div style="color:#94a3b8;font-size:0.62rem;text-transform:uppercase;letter-spacing:1px">{lbl}</div>'
                    f'<div style="color:{clr};font-size:1.6rem;font-weight:800;margin-top:2px">{val}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # 6. AI kullanildi mi?
    st.caption(
        f"{'🤖 AI stratejik analizi' if briefing.get('ai_kullanildi') else '📋 Rule-based analiz'} • "
        f"Veri kaynagi: 9 modul"
    )

    # Alt: Detaylı gorunum (expandable)
    with st.expander("📂 Ham Veri + Tüm Modül Sinyalleri", expanded=False):
        md = briefing.get("master_data", {})
        j1, j2 = st.columns(2)
        with j1:
            st.markdown("**Pipeline**")
            st.json(md.get("pipeline", {}))
            st.markdown("**Isi Haritasi**")
            st.json(md.get("isi_haritasi", {}))
            st.markdown("**Sessiz Red**")
            st.json(md.get("sessiz_red", {}))
        with j2:
            st.markdown("**Pismanlik Motoru**")
            st.json(md.get("pismanlik", {}))
            st.markdown("**Gelir Optimizasyon**")
            st.json(md.get("gelir_optim", {}))
            st.markdown("**Kurumsal Kanal**")
            st.json(md.get("kurumsal", {}))


# ------------------------------------------------------------
# 2) GELIR OPTIMIZASYON
# ------------------------------------------------------------

def _render_gelir_optimizasyon(adaylar: list[KayitAday]):
    """Dinamik fiyat onerisi — her aday icin ayri."""
    try:
        from models.kayit_gelir_optimizasyon import (
            fiyat_optimize_et, uret_ve_kaydet, get_fiyat_onerisi_store,
            willingness_to_pay_skor, ltv_tahmin, pazarlik_elastikiyeti,
        )
    except Exception as e:
        st.error(f"Gelir Optimizasyon yuklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#0B1E3F;border-left:4px solid #C8952E;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#C8952E;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        'Havayolları gibi: her aday için ayrı optimal fiyat. '
        '<b>WTP</b> (ödeme kapasitesi) + <b>LTV</b> (yaşam değeri) + <b>Elastikiyet</b> → '
        'Savunmacı / Dengeli / Agresif 3 paket üretilir. Beklenen gelir artışı: %15-25.'
        '</div></div>',
        unsafe_allow_html=True
    )

    store = get_fiyat_onerisi_store()
    stats = store.istatistikler()

    # Ust metrik
    sc = st.columns(5)
    _s = [
        (sc[0], "Toplam Öneri", str(stats["toplam_oneri"]), "#C8952E"),
        (sc[1], "Ort. WTP", f"{stats['ortalama_wtp']:.0f}/100", "#6366f1"),
        (sc[2], "Ort. Burs", f"%{stats['ortalama_burs']:.0f}", "#f59e0b"),
        (sc[3], "Ort. LTV", f"{stats['ortalama_ltv']:,.0f}", "#22c55e"),
        (sc[4], "Potansiyel", f"{stats['toplam_potansiyel_gelir']:,.0f}", "#ec4899"),
    ]
    for col, lbl, val, clr in _s:
        with col:
            st.markdown(
                f'<div style="background:#131825;border:1px solid {clr}40;border-radius:8px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.2rem;font-weight:800">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    aday = _aday_secici(adaylar, "go")
    if not aday:
        return

    kurum_adi = _kurum_adi_getir()

    # Liste fiyat girisi
    c1, c2 = st.columns([2, 1])
    with c1:
        liste_fiyat = st.number_input(
            "Liste Fiyatı (TL/yıl)",
            min_value=10000,
            max_value=500000,
            value=int(st.session_state.get("_go_liste_fiyat", 100000)),
            step=5000,
            key="go_liste",
        )
        st.session_state["_go_liste_fiyat"] = liste_fiyat
    with c2:
        st.markdown("")
        st.markdown("")
        uret_btn = st.button(
            "💎 Optimal Fiyat Üret",
            key="go_uret",
            type="primary",
            use_container_width=True,
        )

    # Onizleme: Hesaplama mantığı
    wtp, wtp_gerekce = willingness_to_pay_skor(aday)
    ltv, ltv_detay = ltv_tahmin(aday, liste_fiyat)
    elastikiyet, el_gerekce = pazarlik_elastikiyeti(aday)

    # Skor kartlari
    sk1, sk2, sk3 = st.columns(3)
    with sk1:
        _clr = "#22c55e" if wtp >= 70 else ("#f59e0b" if wtp >= 40 else "#ef4444")
        st.markdown(
            f'<div style="background:#131825;border:2px solid {_clr}60;border-radius:10px;padding:12px;text-align:center">'
            f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">WTP (Ödeme Kapasitesi)</div>'
            f'<div style="color:{_clr};font-size:2rem;font-weight:800">{wtp:.0f}<span style="font-size:0.8rem;color:#64748b">/100</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if wtp_gerekce:
            for g in wtp_gerekce[:3]:
                st.caption(f"• {g}")

    with sk2:
        st.markdown(
            f'<div style="background:#131825;border:2px solid #6366f160;border-radius:10px;padding:12px;text-align:center">'
            f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">LTV (Yaşam Değeri)</div>'
            f'<div style="color:#6366f1;font-size:1.6rem;font-weight:800">{ltv:,.0f}<span style="font-size:0.7rem;color:#64748b"> TL</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.caption(f"• Kalış: {ltv_detay['efektif_kalis']} yıl")
        st.caption(f"• Kardeş katsayısı: {ltv_detay['kardes_katsayi']}x")
        st.caption(f"• Referans katsayısı: {ltv_detay['referans_katsayi']}x")

    with sk3:
        _clr = "#ef4444" if elastikiyet >= 0.6 else ("#f59e0b" if elastikiyet >= 0.4 else "#22c55e")
        st.markdown(
            f'<div style="background:#131825;border:2px solid {_clr}60;border-radius:10px;padding:12px;text-align:center">'
            f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">Pazarlık Elastikiyeti</div>'
            f'<div style="color:{_clr};font-size:2rem;font-weight:800">%{elastikiyet*100:.0f}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.caption(f"• {el_gerekce}")

    if uret_btn:
        with st.spinner("Optimal fiyat hesaplanıyor..."):
            oneri = uret_ve_kaydet(aday, float(liste_fiyat), kurum_adi)
            st.session_state["_go_son_oneri"] = oneri.to_dict()
            st.rerun()

    # Son oneriyi goster
    if st.session_state.get("_go_son_oneri"):
        oneri = st.session_state["_go_son_oneri"]

        st.markdown("---")
        st.markdown("### 💎 Optimal Fiyat Paketi")

        # Ana oneri kart
        st.markdown(
            f'<div style="background:linear-gradient(135deg,#0B1E3F 0%,#1e293b 100%);'
            f'border:2px solid #C8952E;border-radius:12px;padding:16px 20px;margin:10px 0">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">'
            f'<div>'
            f'<div style="color:#C8952E;font-size:0.72rem;font-weight:700;letter-spacing:2px">OPTIMAL FIYAT</div>'
            f'<div style="color:#fff;font-size:2rem;font-weight:800">{oneri["fiyat_optimal"]:,.0f} TL</div>'
            f'<div style="color:#94a3b8;font-size:0.78rem">Taban: {oneri["fiyat_taban"]:,.0f} • Maks: {oneri["fiyat_maks"]:,.0f}</div>'
            f'</div>'
            f'<div style="text-align:right">'
            f'<div style="color:#94a3b8;font-size:0.65rem">Güven Skoru</div>'
            f'<div style="color:#22c55e;font-size:1.8rem;font-weight:800">{oneri["guven_skoru"]}<span style="font-size:0.7rem;color:#64748b">/100</span></div>'
            f'<div style="color:#94a3b8;font-size:0.72rem">Burs: <b>%{oneri["burs_yuzde"]}</b></div>'
            f'<div style="color:#94a3b8;font-size:0.72rem">Taksit: <b>{oneri["taksit_sayi"]}x</b></div>'
            f'</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        # 3 Paket
        st.markdown("#### 📦 3 Alternatif Paket")
        paketler = oneri.get("paketler", [])
        p_cols = st.columns(3)
        paket_renkler = {"Savunmaci": "#6366f1", "Dengeli": "#C8952E", "Agresif": "#ef4444"}
        for i, pk in enumerate(paketler):
            with p_cols[i]:
                clr = paket_renkler.get(pk["ad"], "#C8952E")
                st.markdown(
                    f'<div style="background:#131825;border:2px solid {clr}60;border-radius:10px;'
                    f'padding:14px;margin:4px 0">'
                    f'<div style="color:{clr};font-size:0.75rem;font-weight:700;text-transform:uppercase">{pk["ad"]}</div>'
                    f'<div style="color:#fff;font-size:1.5rem;font-weight:800;margin:4px 0">{pk["fiyat"]:,.0f} TL</div>'
                    f'<div style="color:#94a3b8;font-size:0.72rem">'
                    f'Burs: <b style="color:#e2e8f0">%{pk["burs_yuzde"]}</b> • '
                    f'Taksit: <b style="color:#e2e8f0">{pk["taksit"]}x</b>'
                    f'</div>'
                    f'<div style="color:#64748b;font-size:0.68rem;margin-top:6px;font-style:italic">{pk["aciklama"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        # Gerekce
        with st.expander("🧠 AI Gerekce + Metrik Detay", expanded=False):
            st.markdown(oneri.get("gerekce", ""))


# ------------------------------------------------------------
# 3) KURUMSAL KANAL (B2B)
# ------------------------------------------------------------

def _render_kurumsal_kanal():
    """B2B kurumsal musteri pipeline."""
    try:
        from models.kayit_kurumsal_kanal import (
            get_kurumsal_store, KurumMusteri, SEKTORLER, ANLASMA_TIPLERI,
            B2B_ASAMALARI, B2B_ASAMA_INFO, pipeline_saglik,
            uret_teklif_mektubu,
        )
    except Exception as e:
        st.error(f"Kurumsal Kanal yuklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#0B1E3F;border-left:4px solid #3B82F6;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#3B82F6;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        '1 kurumsal anlaşma = <b>20-50 potansiyel aday</b>. CAC %90 daha düşük, churn neredeyse sıfır. '
        'Şirket, banka, belediye... kurumsal müşteri pipeline\'ı yönetir.'
        '</div></div>',
        unsafe_allow_html=True
    )

    store = get_kurumsal_store()
    stats = store.istatistikler()
    kurumlar = store.load_all()
    saglik = pipeline_saglik(kurumlar)

    # Ust metrik
    sc = st.columns(5)
    _s = [
        (sc[0], "Toplam Kurum", str(stats["toplam_kurum"]), "#3B82F6"),
        (sc[1], "Aktif Anlaşma", str(stats["anlasmali"]), "#22c55e"),
        (sc[2], "Potansiyel Aday", str(stats["toplam_aday_potansiyel"]), "#C8952E"),
        (sc[3], "Gerçek Kayıt", str(stats["toplam_kayit"]), "#ec4899"),
        (sc[4], "Yıllık Potansiyel", f"{stats['yillik_toplam_potansiyel']:,.0f}", "#06b6d4"),
    ]
    for col, lbl, val, clr in _s:
        with col:
            st.markdown(
                f'<div style="background:#131825;border:1px solid {clr}40;border-radius:8px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.2rem;font-weight:800">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Pipeline saglik banner
    saglik_clr = "#22c55e" if saglik["skor"] >= 70 else ("#f59e0b" if saglik["skor"] >= 50 else "#ef4444")
    st.markdown(
        f'<div style="background:{saglik_clr}15;border-left:4px solid {saglik_clr};'
        f'border-radius:6px;padding:8px 12px;margin:10px 0">'
        f'<b style="color:{saglik_clr}">Pipeline Sağlığı: {saglik["saglik"]} ({saglik["skor"]}/100)</b>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if saglik.get("oneriler"):
        for o in saglik["oneriler"]:
            st.caption(f"💡 {o}")

    st.markdown("---")

    _alt = st.tabs(["📋 Kurum Listesi", "➕ Yeni Kurum", "📊 Pipeline Akışı"])

    # ── Tab: Kurum listesi ──
    with _alt[0]:
        if not kurumlar:
            st.info("Henüz kurumsal müşteri yok. 'Yeni Kurum' sekmesinden başlayın.")
        else:
            filt = st.radio(
                "Filtre",
                options=["Aktif", "Hepsi", "Kapalı"],
                horizontal=True,
                key="kk_filt",
            )
            if filt == "Aktif":
                gost = [k for k in kurumlar if k.aktif]
            elif filt == "Kapalı":
                gost = [k for k in kurumlar if not k.aktif]
            else:
                gost = kurumlar

            for kurum in gost:
                asama_info = kurum.asama_info
                with st.expander(
                    f"{asama_info['emoji']} {kurum.kurum_adi} — {asama_info['label']} • "
                    f"Potansiyel: {kurum.tahmini_aday_potansiyel} aday",
                    expanded=False,
                ):
                    kc1, kc2, kc3 = st.columns([2, 1, 1])
                    with kc1:
                        st.markdown(f"**Sektör:** {kurum.sektor or '-'}")
                        st.markdown(f"**Çalışan:** {kurum.calisan_sayisi:,}")
                        st.markdown(f"**İrtibat:** {kurum.irtibat_ad} ({kurum.irtibat_unvan})")
                        st.markdown(f"**Tel:** {kurum.irtibat_telefon} • **Email:** {kurum.irtibat_email}")
                    with kc2:
                        st.metric("Potansiyel Aday", kurum.tahmini_aday_potansiyel)
                        st.metric("Gerçek Aday", kurum.aday_sayisi)
                    with kc3:
                        st.metric("Kayıt", kurum.kayit_sayisi)
                        st.metric("Dönüşüm", f"%{kurum.donusum_orani}")

                    # Asama degistir
                    st.markdown("---")
                    aac1, aac2 = st.columns([2, 1])
                    with aac1:
                        yeni_asama = st.selectbox(
                            "Pipeline Aşaması",
                            options=B2B_ASAMALARI,
                            index=B2B_ASAMALARI.index(kurum.asama) if kurum.asama in B2B_ASAMALARI else 0,
                            key=f"kk_asama_{kurum.id}",
                        )
                    with aac2:
                        st.markdown("")
                        st.markdown("")
                        if st.button("Güncelle", key=f"kk_guncelle_{kurum.id}", use_container_width=True):
                            if yeni_asama != kurum.asama:
                                store.asama_degistir(kurum.id, yeni_asama)
                                st.success(f"Aşama güncellendi: {yeni_asama}")
                                st.rerun()

                    # Teklif mektubu uret
                    if st.button("📄 AI Teklif Mektubu Üret", key=f"kk_teklif_{kurum.id}"):
                        with st.spinner("Teklif hazırlanıyor..."):
                            mektup = uret_teklif_mektubu(
                                kurum,
                                okul_adi=_kurum_adi_getir(),
                                yillik_fiyat=st.session_state.get("_go_liste_fiyat", 100000),
                            )
                            st.text_area("Teklif Mektubu", value=mektup, height=300, key=f"kk_mek_{kurum.id}")
                            st.download_button(
                                label="📥 Mektubu İndir (.txt)",
                                data=mektup,
                                file_name=f"{kurum.kurum_adi}_teklif.txt",
                                mime="text/plain",
                                key=f"kk_dl_{kurum.id}",
                            )

                    if kurum.notlar:
                        st.caption(f"📝 {kurum.notlar}")
                    if kurum.aktiviteler:
                        st.caption(f"🗓️ {len(kurum.aktiviteler)} aktivite kayıtlı")

    # ── Tab: Yeni kurum ──
    with _alt[1]:
        st.markdown("#### ➕ Yeni Kurumsal Müşteri Ekle")
        with st.form("kk_yeni_form", clear_on_submit=True):
            f1, f2 = st.columns(2)
            with f1:
                k_ad = st.text_input("Kurum Adı *", key="kk_n_ad")
                k_sektor = st.selectbox("Sektör", options=SEKTORLER, key="kk_n_sektor")
                k_calisan = st.number_input("Çalışan Sayısı", min_value=0, max_value=100000, value=100, key="kk_n_cal")
                k_sehir = st.text_input("Şehir", key="kk_n_sehir")
                k_web = st.text_input("Web Sitesi", key="kk_n_web")
            with f2:
                k_irtibat = st.text_input("İrtibat Kişi *", key="kk_n_irt")
                k_unvan = st.text_input("Unvanı (ör. IK Direktörü)", key="kk_n_unvan")
                k_tel = st.text_input("Telefon", key="kk_n_tel")
                k_email = st.text_input("Email", key="kk_n_email")
                k_anlasma = st.selectbox("Anlaşma Tipi", options=[""] + ANLASMA_TIPLERI, key="kk_n_anlasma")

            k_indirim = st.slider("İndirim Yüzdesi", 0, 40, 15, key="kk_n_indirim")
            k_notlar = st.text_area("Notlar", key="kk_n_notlar")

            submit = st.form_submit_button("✅ Kaydet", type="primary", use_container_width=True)

        if submit:
            if not k_ad or not k_irtibat:
                st.error("Kurum adı ve irtibat kişi zorunlu.")
            else:
                yeni = KurumMusteri(
                    kurum_adi=k_ad,
                    sektor=k_sektor,
                    calisan_sayisi=int(k_calisan),
                    sehir=k_sehir,
                    web_sitesi=k_web,
                    irtibat_ad=k_irtibat,
                    irtibat_unvan=k_unvan,
                    irtibat_telefon=k_tel,
                    irtibat_email=k_email,
                    anlasma_tipi=k_anlasma,
                    indirim_yuzde=float(k_indirim),
                    notlar=k_notlar,
                    ilk_temas_tarihi=datetime.now().isoformat(timespec="seconds"),
                    asama="tanisma",
                )
                store.add(yeni)
                st.success(f"✅ {k_ad} eklendi ({yeni.tahmini_aday_potansiyel} potansiyel aday)")
                st.rerun()

    # ── Tab: Pipeline akışı ──
    with _alt[2]:
        st.markdown("#### 📊 B2B Pipeline Akışı")
        sayac = store.asama_sayac()

        for asama in B2B_ASAMALARI:
            info = B2B_ASAMA_INFO[asama]
            sayi = sayac.get(asama, 0)
            toplam = max(sum(sayac.values()), 1)
            yuzde = sayi / toplam * 100

            st.markdown(
                f'<div style="display:flex;align-items:center;gap:10px;margin:6px 0">'
                f'<div style="min-width:120px;color:#cbd5e1;font-size:0.85rem">'
                f'{info["emoji"]} {info["label"]}</div>'
                f'<div style="flex:1;background:#0f172a;border-radius:6px;height:22px;position:relative;overflow:hidden">'
                f'<div style="background:{info["color"]};height:100%;width:{yuzde:.0f}%;transition:width 0.3s"></div>'
                f'<div style="position:absolute;top:0;left:8px;right:8px;line-height:22px;color:#fff;font-size:0.78rem;font-weight:700">{sayi}</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )


# ============================================================
# KAYIP KALKANI — 3 SAVUNMA MOTORU
# 1) 5 Dakika Kuralı (Response Time War Room)
# 2) Veli Dijital Parmak İzi (Unified Identity)
# 3) Son Mil Gümrük Memuru (Last-Mile Guard)
# ============================================================

def _render_kayip_kalkani(store: KayitDataStore, adaylar: list[KayitAday]):
    """Üç savunma motorunu alt sekmelerde render eder."""
    st.markdown(
        '<div style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f172a 100%);'
        'border:2px solid #22c55e60;border-radius:14px;padding:16px 20px;margin-bottom:12px;'
        'box-shadow:0 4px 30px #22c55e15">'
        '<div style="display:flex;align-items:center;gap:12px">'
        '<div style="font-size:1.8rem">🛡️</div>'
        '<div>'
        '<div style="color:#22c55e;font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase">PROAKTIF SAVUNMA SISTEMI</div>'
        '<div style="color:#fff;font-size:1.3rem;font-weight:700">Kayıp Kalkanı — 3 Zaman Diliminde Kaçışı Engeller</div>'
        '<div style="color:#94a3b8;font-size:0.82rem;margin-top:2px">İlk 5 dakika • Pipeline boyunca • Son mil</div>'
        '</div></div></div>',
        unsafe_allow_html=True
    )

    alt = st.tabs([
        "⚡ 5 Dakika Kuralı",
        "🔍 Veli Parmak İzi",
        "🛃 Son Mil Gümrük",
    ])

    with alt[0]:
        _render_5dk_kurali()

    with alt[1]:
        _render_veli_parmak_izi(adaylar)

    with alt[2]:
        _render_son_mil_gardiyan(adaylar)


# ------------------------------------------------------------
# 1) 5 DAKIKA KURALI
# ------------------------------------------------------------

def _render_5dk_kurali():
    """Lead yanıt süresi war room."""
    try:
        from models.kayit_5dk_kurali import (
            get_lead_response_store, yeni_lead_kaydet, yanit_kaydet, iptal_et,
            yanit_bekleyenleri_tara, gunluk_ozet, koordinator_performans,
            kanal_analiz, sure_formatla, LEAD_KANALLARI, ESKALASYON_SEVIYELERI,
            UYARI_ESIGI_SN, ESKALASYON_ESIGI_SN,
        )
    except Exception as e:
        st.error(f"5 Dakika Kuralı yüklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#0f172a;border-left:4px solid #ef4444;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#ef4444;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        'Sektör araştırması: İlk 5 dakikada yanıtlanan lead\'lerin dönüşümü <b>%400 daha fazla</b>. '
        'Sistem her yeni lead için sayaç başlatır, 5 dakika dolunca otomatik eskalasyon + müdür uyarısı.'
        '</div></div>',
        unsafe_allow_html=True
    )

    # Gunluk ozet
    ozet = gunluk_ozet()
    sc = st.columns(5)
    _m = [
        (sc[0], "Bugün Lead", str(ozet["toplam_lead"]), "#6366f1"),
        (sc[1], "Yanıtlanan", str(ozet["yanitlanan"]), "#22c55e"),
        (sc[2], "Bekleyen", str(ozet["bekleyen"]), "#f59e0b"),
        (sc[3], "5dk İçinde", f"%{ozet['5dk_icinde_oran']:.0f}", "#ef4444"),
        (sc[4], "Ort. Süre", sure_formatla(ozet["ortalama_yanit_sn"]), "#a78bfa"),
    ]
    for col, lbl, val, clr in _m:
        with col:
            st.markdown(
                f'<div style="background:#131825;border:1px solid {clr}40;border-radius:8px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.3rem;font-weight:800">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    _tab = st.tabs(["🚨 War Room (Bekleyenler)", "➕ Manuel Lead", "📊 Performans"])

    # ── War Room ──
    with _tab[0]:
        tarama = yanit_bekleyenleri_tara()

        # Canli alarm banner
        if tarama["kayip_riski"] or tarama["kritik"]:
            toplam_tehlike = len(tarama["kayip_riski"]) + len(tarama["kritik"])
            st.markdown(
                f'<div style="background:linear-gradient(90deg,#450a0a,#7f1d1d);'
                f'border:2px solid #ef4444;border-radius:10px;padding:14px 18px;margin:8px 0;'
                f'box-shadow:0 0 25px #ef444440;animation:pulse 2s infinite">'
                f'<div style="color:#fecaca;font-size:0.8rem;font-weight:700;letter-spacing:1px">🚨 ACİL MÜDAHALE GEREKLİ</div>'
                f'<div style="color:#fff;font-size:1.1rem;font-weight:800;margin-top:4px">'
                f'{toplam_tehlike} lead 5 dakikayı aştı — hemen yanıtlayın</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if tarama["toplam_bekleyen"] == 0:
            st.success("✅ Harika! Şu an bekleyen lead yok. Tüm yanıt süreleri sağlıklı.")
        else:
            st.markdown(f"#### ⚡ {tarama['toplam_bekleyen']} Aktif Lead Takipte")

            # Tum bekleyenleri birlestir ve skora gore sirala (kritik once)
            tum_bekleyen = (
                tarama["kayip_riski"] + tarama["kritik"]
                + tarama["eskalasyon_gereken"] + tarama["uyari_gereken"]
            )
            tum_bekleyen_sirali = sorted(tum_bekleyen, key=lambda t: -t.gecen_saniye)

            # Henuz sayac sinirina gelmemisleri de ekle (saglikli olanlar)
            tum_bekleyen_ids = {t.id for t in tum_bekleyen}
            store_inner = get_lead_response_store()
            for t in store_inner.aktif_bekleyenler():
                if t.id not in tum_bekleyen_ids:
                    tum_bekleyen_sirali.append(t)

            for t in tum_bekleyen_sirali:
                info = t.seviye_info()
                gecen = sure_formatla(t.gecen_saniye)
                kalan = t.kalan_saniye

                st.markdown(
                    f'<div style="background:linear-gradient(90deg,{info["color"]}15,#131825);'
                    f'border-left:4px solid {info["color"]};border-radius:8px;padding:10px 14px;margin:6px 0">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">'
                    f'<div style="flex:1">'
                    f'<div style="color:{info["color"]};font-size:0.7rem;font-weight:700;letter-spacing:1px">'
                    f'{info["emoji"]} {info["label"]}</div>'
                    f'<div style="color:#fff;font-size:1rem;font-weight:700">{t.veli_adi or "(Bilinmeyen)"}'
                    f'{" — " + t.ogrenci_adi if t.ogrenci_adi else ""}</div>'
                    f'<div style="color:#94a3b8;font-size:0.75rem">'
                    f'Kanal: <b style="color:#cbd5e1">{t.kanal}</b> • '
                    f'Koordinatör: <b style="color:#cbd5e1">{t.atanan_koordinator or "—"}</b>'
                    f'</div>'
                    f'</div>'
                    f'<div style="text-align:right">'
                    f'<div style="color:#94a3b8;font-size:0.65rem">GEÇEN SÜRE</div>'
                    f'<div style="color:{info["color"]};font-size:1.6rem;font-weight:800;font-family:monospace">{gecen}</div>'
                    f'<div style="color:#64748b;font-size:0.65rem">Sınır: 05:00</div>'
                    f'</div></div></div>',
                    unsafe_allow_html=True,
                )

                bc1, bc2, bc3 = st.columns([2, 1, 1])
                with bc1:
                    yanit_kanal = st.selectbox(
                        "Yanıt Kanalı",
                        options=LEAD_KANALLARI,
                        index=LEAD_KANALLARI.index(t.kanal) if t.kanal in LEAD_KANALLARI else 0,
                        key=f"5dk_kanal_{t.id}",
                        label_visibility="collapsed",
                    )
                with bc2:
                    if st.button("✅ Yanıtladım", key=f"5dk_yanit_{t.id}", type="primary", use_container_width=True):
                        yanit_kaydet(t.id, yanit_kanal)
                        st.success(f"✅ Kaydedildi ({sure_formatla(t.gecen_saniye)})")
                        st.rerun()
                with bc3:
                    if st.button("❌ İptal", key=f"5dk_iptal_{t.id}", use_container_width=True):
                        iptal_et(t.id)
                        st.rerun()

    # ── Manuel Lead ──
    with _tab[1]:
        st.markdown("#### ➕ Yeni Lead Gir (Sayaç Başlasın)")
        st.caption("Gerçek entegrasyonda web formu / WhatsApp webhook otomatik doldurur.")

        with st.form("5dk_yeni_lead", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                v_ad = st.text_input("Veli Adı *", key="5dk_yl_ad")
                v_tel = st.text_input("Telefon", key="5dk_yl_tel")
                o_ad = st.text_input("Öğrenci Adı", key="5dk_yl_ogr")
            with c2:
                kanal = st.selectbox("Kanal", options=LEAD_KANALLARI, key="5dk_yl_kanal")
                koor = st.text_input("Atanan Koordinatör", key="5dk_yl_koor")
                detay = st.text_input("Kaynak Detay", key="5dk_yl_detay")

            submit = st.form_submit_button("⚡ Sayacı Başlat", type="primary", use_container_width=True)

        if submit:
            if not v_ad:
                st.error("Veli adı zorunlu.")
            else:
                t = yeni_lead_kaydet(
                    veli_adi=v_ad,
                    veli_telefon=v_tel,
                    ogrenci_adi=o_ad,
                    kanal=kanal,
                    kaynak_detay=detay,
                    atanan_koordinator=koor,
                )
                st.success(f"✅ Sayaç başladı! {v_ad} için 5 dakika var.")
                st.rerun()

    # ── Performans ──
    with _tab[2]:
        st.markdown("#### 📊 Koordinatör Performansı (Son 7 Gün)")
        performans = koordinator_performans(7)

        if not performans:
            st.info("Henüz veri yok.")
        else:
            for p in performans:
                skor_clr = "#22c55e" if p["skor"] >= 80 else ("#f59e0b" if p["skor"] >= 50 else "#ef4444")
                st.markdown(
                    f'<div style="background:#131825;border-left:3px solid {skor_clr};'
                    f'border-radius:6px;padding:10px 14px;margin:4px 0">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">'
                    f'<div>'
                    f'<div style="color:#e2e8f0;font-size:0.95rem;font-weight:700">{p["koordinator"]}</div>'
                    f'<div style="color:#94a3b8;font-size:0.72rem">'
                    f'{p["yanitlanan"]}/{p["toplam"]} yanıtlandı • '
                    f'Ort: <b style="color:{skor_clr}">{p["ortalama_dk"]}dk</b> • '
                    f'5dk: <b>%{p["5dk_oran"]:.0f}</b></div>'
                    f'</div>'
                    f'<div style="text-align:right">'
                    f'<div style="color:#94a3b8;font-size:0.6rem">SKOR</div>'
                    f'<div style="color:{skor_clr};font-size:1.8rem;font-weight:800">{p["skor"]}</div>'
                    f'</div></div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("#### 📡 Kanal Bazlı Yanıt Süreleri")
        kanallar = kanal_analiz()
        if kanallar:
            for k in kanallar:
                st.caption(f"**{k['kanal']}** — {k['toplam']} lead, ortalama {k['ortalama_dk']}dk")


# ------------------------------------------------------------
# 2) VELI DIJITAL PARMAK IZI
# ------------------------------------------------------------

def _render_veli_parmak_izi(adaylar: list[KayitAday]):
    """Omnikanalli duplicat/birlestirme paneli."""
    try:
        from models.kayit_veli_parmak_izi import (
            cakisma_tarama, benzer_adaylar_bul, eslesme_skoru,
            merge_onerisi, birlesik_timeline, parmak_izi_hash,
            parmak_izi_bilesenleri,
        )
    except Exception as e:
        st.error(f"Veli Parmak İzi yüklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#0f172a;border-left:4px solid #06b6d4;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#06b6d4;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        'Aynı veli 4 farklı kanaldan (Instagram, WhatsApp, Telefon, Form) gelince sistem 4 aday oluşturuyor. '
        '3 koordinatör aynı veliyi arıyor → veli rahatsız → kayıp. Bu motor duplicate\'leri <b>fuzzy match</b> ile '
        'tespit edip tek profile birleştirir.'
        '</div></div>',
        unsafe_allow_html=True
    )

    if not adaylar:
        st.info("Henüz aday yok.")
        return

    # Tum cakismalari tara
    with st.spinner("Veli parmak izleri taranıyor..."):
        cakismalar = cakisma_tarama(adaylar)

    # Ust metrik
    sc = st.columns(4)
    _m = [
        (sc[0], "Toplam Aday", str(len(adaylar)), "#6366f1"),
        (sc[1], "Çakışma Çifti", str(len(cakismalar)), "#ef4444"),
        (sc[2], "Kesin Aynı", str(sum(1 for c in cakismalar if c["karar"] == "ayni")), "#dc2626"),
        (sc[3], "Muhtemel", str(sum(1 for c in cakismalar if c["karar"] == "muhtemel")), "#f59e0b"),
    ]
    for col, lbl, val, clr in _m:
        with col:
            st.markdown(
                f'<div style="background:#131825;border:1px solid {clr}40;border-radius:8px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.4rem;font-weight:800">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    _tab = st.tabs(["🔴 Çakışmalar", "🔎 Aday Ara & Parmak İzi", "🌐 Birleşik Timeline"])

    # ── Cakismalar ──
    with _tab[0]:
        if not cakismalar:
            st.success("✅ Harika! Hiç duplicate/çakışma tespit edilmedi.")
        else:
            st.markdown(f"#### 🔴 {len(cakismalar)} Potansiyel Çakışma")

            for idx, c in enumerate(cakismalar[:15]):
                a = c["aday_a"]
                b = c["aday_b"]
                skor = c["skor"]
                karar = c["karar"]

                clr = "#dc2626" if karar == "ayni" else "#f59e0b"
                sembol = "🚨" if karar == "ayni" else "⚠️"

                with st.expander(
                    f"{sembol} {a.veli_adi} ↔ {b.veli_adi} • Benzerlik: %{skor:.0f} ({karar.upper()})",
                    expanded=(idx < 3),
                ):
                    # Karsilastirma
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown("**🅰️ Aday A**")
                        st.caption(f"ID: `{a.id}`")
                        st.markdown(f"- Veli: {a.veli_adi}")
                        st.markdown(f"- Öğrenci: {a.ogrenci_adi}")
                        st.markdown(f"- Tel: {a.veli_telefon or '—'}")
                        st.markdown(f"- Email: {a.veli_email or '—'}")
                        st.markdown(f"- Kanal: {a.kanal or '—'}")
                        st.markdown(f"- Aşama: {a.asama}")
                        st.caption(f"{len(a.aramalar)} arama, {len(a.gorusmeler)} görüşme")
                    with cc2:
                        st.markdown("**🅱️ Aday B**")
                        st.caption(f"ID: `{b.id}`")
                        st.markdown(f"- Veli: {b.veli_adi}")
                        st.markdown(f"- Öğrenci: {b.ogrenci_adi}")
                        st.markdown(f"- Tel: {b.veli_telefon or '—'}")
                        st.markdown(f"- Email: {b.veli_email or '—'}")
                        st.markdown(f"- Kanal: {b.kanal or '—'}")
                        st.markdown(f"- Aşama: {b.asama}")
                        st.caption(f"{len(b.aramalar)} arama, {len(b.gorusmeler)} görüşme")

                    # Gerekce
                    st.markdown("**📋 Eşleşme Gerekçeleri:**")
                    for g in c["gerekceler"]:
                        st.markdown(f"- {g}")

                    # Merge onerisi (read-only goster)
                    if st.button(f"🔗 Merge Önerisi Gör", key=f"pi_merge_{idx}"):
                        merge = merge_onerisi(a, b)
                        st.markdown("#### 🔗 Birleştirme Önerisi")
                        st.info(
                            f"**Ana kaynak:** {merge['birlestirme_ozet']['ana_kaynak']}  \n"
                            f"**Kanallar:** {', '.join(merge['birlestirme_ozet']['kanallar']) or '—'}  \n"
                            f"**Birleşik arama:** {merge['birlestirme_ozet']['toplam_arama']}  \n"
                            f"**Birleşik görüşme:** {merge['birlestirme_ozet']['toplam_gorusme']}"
                        )
                        # Timeline
                        if merge["birlesik_timeline"]:
                            st.markdown("**🌐 Birleşik Zaman Çizelgesi:**")
                            for olay in merge["birlesik_timeline"][:10]:
                                st.caption(
                                    f"• `{olay.get('tarih', '')[:16]}` • "
                                    f"**{olay.get('kanal', '')}** • {olay.get('aciklama', '')}"
                                )
                        st.warning(
                            "⚠️ Gerçek merge operasyonu (KayitDataStore üzerinde silme/birleştirme) "
                            "bu panelde yapılmaz — önce koordinatör/yönetici onayı gerekir. "
                            "Manuel olarak Pipeline sekmesinden adayları kontrol edin."
                        )

    # ── Aday Ara ──
    with _tab[1]:
        st.markdown("#### 🔎 Bir Aday İçin Benzerleri Bul")
        aday = _aday_secici(adaylar, "pi_sec")
        if aday:
            b = parmak_izi_bilesenleri(aday)
            hash_val = parmak_izi_hash(aday)

            st.markdown("##### 🆔 Parmak İzi Bileşenleri")
            ic1, ic2 = st.columns(2)
            with ic1:
                st.code(f"Telefon (norm): {b['telefon'] or '—'}")
                st.code(f"Veli (norm):    {b['veli_adi'] or '—'}")
            with ic2:
                st.code(f"Öğrenci (norm): {b['ogrenci_adi'] or '—'}")
                st.code(f"Hash:           {hash_val}")

            st.markdown("##### 🔍 Benzer Adaylar")
            benzerler = benzer_adaylar_bul(aday, adaylar, esik=40.0)
            if not benzerler:
                st.success("Bu adaya benzer başka bir profil bulunamadı.")
            else:
                for bnz in benzerler[:10]:
                    diger = bnz["aday"]
                    st.markdown(
                        f"**%{bnz['skor']:.0f}** — {diger.veli_adi} / {diger.ogrenci_adi} — "
                        f"({bnz['karar'].upper()})"
                    )
                    for g in bnz["gerekceler"]:
                        st.caption(f"  {g}")

    # ── Birlesik Timeline ──
    with _tab[2]:
        st.markdown("#### 🌐 Aday İçin Tüm Kanallar Zaman Çizelgesi")
        aday = _aday_secici(adaylar, "pi_tl")
        if aday:
            timeline = birlesik_timeline([aday])
            if not timeline:
                st.info("Bu aday için henüz olay yok.")
            else:
                for olay in timeline[:30]:
                    tip_renk = {
                        "olusturma": "#6366f1",
                        "arama": "#f59e0b",
                        "gorusme": "#22c55e",
                    }.get(olay.get("tip", ""), "#64748b")
                    st.markdown(
                        f'<div style="background:#131825;border-left:3px solid {tip_renk};'
                        f'border-radius:6px;padding:8px 12px;margin:4px 0">'
                        f'<div style="color:#94a3b8;font-size:0.7rem">{olay.get("tarih", "")[:16]} • '
                        f'<b style="color:{tip_renk}">{olay.get("kanal", "")}</b></div>'
                        f'<div style="color:#e2e8f0;font-size:0.85rem;margin-top:2px">{olay.get("aciklama", "")}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )


# ------------------------------------------------------------
# 3) SON MIL GUMRUK MEMURU
# ------------------------------------------------------------

def _render_son_mil_gardiyan(adaylar: list[KayitAday]):
    """Son mil checklist motoru."""
    try:
        from models.kayit_son_mil_gardiyan import (
            get_son_mil_store, aday_icin_checklist_olustur,
            kalem_tamamla, kalem_takildi, otomatik_hatirlatma,
            riskli_adaylari_tara, ai_engel_cozum_onerisi,
            KALEM_KATEGORILERI, KALEM_DURUMLARI,
        )
    except Exception as e:
        st.error(f"Son Mil Gardiyan yüklenemedi: {e}")
        return

    st.markdown(
        '<div style="background:#0f172a;border-left:4px solid #8b5cf6;border-radius:6px;'
        'padding:10px 14px;margin:8px 0">'
        '<div style="color:#8b5cf6;font-size:0.75rem;font-weight:700;letter-spacing:1px">NASIL CALISIR?</div>'
        '<div style="color:#e2e8f0;font-size:0.85rem;margin-top:4px">'
        'Sözleşme aşamasına gelmiş aday = %80 kayıt olmuş. Ama evrak eksik, peşinat gecikiyor, '
        'imza atılmadı... Bu motor her kalemi otomatik checklist\'e koyar, son tarihleri takip eder, '
        'takıldığında AI çözüm önerisi üretir.'
        '</div></div>',
        unsafe_allow_html=True
    )

    store = get_son_mil_store()
    stats = store.istatistikler()
    riskli = riskli_adaylari_tara()

    # Ust metrik
    sc = st.columns(5)
    _m = [
        (sc[0], "Toplam Checklist", str(stats["toplam_checklist"]), "#8b5cf6"),
        (sc[1], "Aktif", str(stats["aktif"]), "#6366f1"),
        (sc[2], "Tamamlanan", str(stats["tamamlanan"]), "#22c55e"),
        (sc[3], "🚨 Kritik", str(stats["kritik_takili_aday"]), "#ef4444"),
        (sc[4], "Ort. Tamamlanma", f"%{stats['ortalama_tamamlanma']:.0f}", "#f59e0b"),
    ]
    for col, lbl, val, clr in _m:
        with col:
            st.markdown(
                f'<div style="background:#131825;border:1px solid {clr}40;border-radius:8px;'
                f'padding:10px;text-align:center">'
                f'<div style="color:#94a3b8;font-size:0.65rem;text-transform:uppercase">{lbl}</div>'
                f'<div style="color:{clr};font-size:1.4rem;font-weight:800">{val}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Kritik alarm
    if riskli["toplam_riskli"] > 0:
        st.markdown(
            f'<div style="background:linear-gradient(90deg,#450a0a,#7f1d1d);'
            f'border:2px solid #ef4444;border-radius:10px;padding:12px 16px;margin:8px 0">'
            f'<div style="color:#fecaca;font-size:0.8rem;font-weight:700">🚨 SON MIL ALARMI</div>'
            f'<div style="color:#fff;font-size:1rem;margin-top:4px">'
            f'{len(riskli["kritik_adaylar"])} kritik (süre geçti) • '
            f'{len(riskli["takili_adaylar"])} takılmış • '
            f'{len(riskli["yaklasan"])} yaklaşan</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    _tab = st.tabs(["🎯 Aktif Checklist'ler", "➕ Yeni Checklist", "🚨 Riskli"])

    # ── Aktif Checklists ──
    with _tab[0]:
        tum = store.load_all()
        aktif = [x for x in tum if not x.tamamlandi]

        if not aktif:
            st.info("Henüz aktif son mil checklist yok.")
        else:
            for cl in aktif:
                tamam_orani = cl.tamamlanma_orani
                kritik = cl.kritik_sayisi

                # Expander baslık
                emoji = "🚨" if kritik > 0 else ("✅" if tamam_orani == 100 else "🎯")
                baslik = (
                    f"{emoji} {cl.veli_adi} — {cl.ogrenci_adi} • "
                    f"Tamamlanma: %{tamam_orani:.0f}"
                    + (f" • 🚨 {kritik} kritik" if kritik else "")
                )

                with st.expander(baslik, expanded=(kritik > 0)):
                    # Progress bar
                    st.progress(tamam_orani / 100)

                    # Kalemler
                    for k in cl.kalemler:
                        durum = k.get("durum", "bekliyor")
                        info = KALEM_DURUMLARI.get(durum, KALEM_DURUMLARI["bekliyor"])
                        son_tarih = k.get("son_tarih", "")

                        gun_kaldi = 999
                        if son_tarih and durum not in ("tamam", "iptal"):
                            try:
                                gun_kaldi = (date.fromisoformat(son_tarih[:10]) - date.today()).days
                            except (ValueError, TypeError):
                                pass

                        if durum == "tamam":
                            gun_metin = "✅ Tamam"
                            gun_clr = "#22c55e"
                        elif gun_kaldi < 0:
                            gun_metin = f"⏰ {abs(gun_kaldi)} gün GEÇTİ"
                            gun_clr = "#ef4444"
                        elif gun_kaldi == 0:
                            gun_metin = "⏰ BUGÜN"
                            gun_clr = "#f59e0b"
                        elif gun_kaldi <= 2:
                            gun_metin = f"⏳ {gun_kaldi} gün kaldı"
                            gun_clr = "#f59e0b"
                        else:
                            gun_metin = f"📅 {gun_kaldi} gün"
                            gun_clr = "#64748b"

                        kc1, kc2, kc3, kc4 = st.columns([3, 1, 1, 1])
                        with kc1:
                            st.markdown(
                                f'<div style="background:#131825;border-left:3px solid {info["color"]};'
                                f'border-radius:6px;padding:8px 12px;margin:4px 0">'
                                f'<div style="color:#e2e8f0;font-size:0.88rem;font-weight:700">'
                                f'{info["emoji"]} {k["ad"]}</div>'
                                f'<div style="color:#94a3b8;font-size:0.7rem">'
                                f'Kategori: <b>{k["kategori"]}</b> • '
                                f'<span style="color:{gun_clr}">{gun_metin}</span></div>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
                            if k.get("notlar"):
                                st.caption(f"📝 {k['notlar'][:100]}")

                        with kc2:
                            if durum != "tamam" and st.button(
                                "✅ Tamam", key=f"sm_tam_{cl.id}_{k['id']}", use_container_width=True
                            ):
                                kalem_tamamla(cl.id, k["id"])
                                st.rerun()
                        with kc3:
                            if durum not in ("tamam", "takildi") and st.button(
                                "⚠️ Takıldı", key=f"sm_tak_{cl.id}_{k['id']}", use_container_width=True
                            ):
                                kalem_takildi(cl.id, k["id"], "Koordinatör işaretledi")
                                st.rerun()
                        with kc4:
                            if durum != "tamam" and st.button(
                                "📱 Hatırlat", key=f"sm_hat_{cl.id}_{k['id']}", use_container_width=True
                            ):
                                hatirla = otomatik_hatirlatma(cl.id, k["id"], "whatsapp")
                                if hatirla:
                                    st.session_state[f"_sm_son_mesaj_{cl.id}_{k['id']}"] = hatirla

                        # Son gonderilen mesaj
                        son_msj_key = f"_sm_son_mesaj_{cl.id}_{k['id']}"
                        if st.session_state.get(son_msj_key):
                            msj = st.session_state[son_msj_key]
                            with st.container():
                                st.text_area(
                                    "Hatırlatma Mesajı (kopyala, gönder)",
                                    value=msj["mesaj"],
                                    height=140,
                                    key=f"sm_msj_ta_{cl.id}_{k['id']}",
                                )

                        # Takili ise AI cozum onerisi
                        if durum == "takildi":
                            if st.button(
                                "🤖 AI Çözüm Önerisi", key=f"sm_ai_{cl.id}_{k['id']}"
                            ):
                                with st.spinner("AI çözüm hazırlıyor..."):
                                    cozum = ai_engel_cozum_onerisi(k["ad"], k.get("notlar", ""))
                                    st.info(cozum)

    # ── Yeni Checklist ──
    with _tab[1]:
        st.markdown("#### ➕ Bir Aday İçin Son Mil Checklist Oluştur")
        st.caption(
            "Normalde aday 'sözleşme' aşamasına geçince OTOMATIK oluşur. "
            "Burada manuel başlatabilirsin."
        )

        aday = _aday_secici(adaylar, "sm_yeni")
        if aday:
            mevcut = store.get_by_aday(aday.id)
            if mevcut:
                st.warning(
                    f"⚠️ Bu aday için zaten checklist var "
                    f"({len(mevcut.kalemler)} kalem, %{mevcut.tamamlanma_orani:.0f} tamamlandı)"
                )
            else:
                st.markdown("##### Hangi Kalemler?")
                secili_kalemler = []
                ko = st.columns(2)
                keys = list(KALEM_KATEGORILERI.keys())
                for i, k_key in enumerate(keys):
                    tanim = KALEM_KATEGORILERI[k_key]
                    col = ko[i % 2]
                    with col:
                        varsayilan = tanim["zorunlu"]
                        if st.checkbox(
                            f"{tanim['ad']} ({tanim['varsayilan_sure_gun']}g)",
                            value=varsayilan,
                            key=f"sm_k_{k_key}",
                            help=tanim["ipucu"],
                        ):
                            secili_kalemler.append(k_key)

                if st.button(
                    "🎯 Checklist Oluştur",
                    type="primary",
                    use_container_width=True,
                    disabled=not secili_kalemler,
                ):
                    cl = aday_icin_checklist_olustur(aday, ozel_kalemler=secili_kalemler)
                    st.success(f"✅ Checklist oluşturuldu ({len(cl.kalemler)} kalem)")
                    st.rerun()

    # ── Riskli ──
    with _tab[2]:
        st.markdown(f"#### 🚨 Riskli Adaylar ({riskli['toplam_riskli']})")

        if riskli["kritik_adaylar"]:
            st.markdown("##### ⏰ Süresi Geçmiş")
            for r in riskli["kritik_adaylar"]:
                cl = r["checklist"]
                st.error(f"**{cl.veli_adi} — {cl.ogrenci_adi}**")
                for kk in r["kritik_kalemler"]:
                    st.caption(f"  • {kk['ad']}: {abs(kk['gun_kaldi'])} gün geçti")

        if riskli["takili_adaylar"]:
            st.markdown("##### ⚠️ Takılmış")
            for r in riskli["takili_adaylar"]:
                cl = r["checklist"]
                st.warning(f"**{cl.veli_adi} — {cl.ogrenci_adi}**")
                for tk in r["takili_kalemler"]:
                    st.caption(f"  • {tk['ad']}")

        if riskli["yaklasan"]:
            st.markdown("##### ⏳ Yaklaşan (2 gün içinde)")
            for r in riskli["yaklasan"]:
                cl = r["checklist"]
                st.info(f"**{cl.veli_adi} — {cl.ogrenci_adi}**")
                for yk in r["yaklasan_kalemler"]:
                    st.caption(f"  • {yk['ad']}: {yk['gun_kaldi']} gün kaldı")

        if not any([riskli["kritik_adaylar"], riskli["takili_adaylar"], riskli["yaklasan"]]):
            st.success("✅ Harika! Şu an riskli aday yok.")


# ============================================================
# ZİRVE 1: VELİ ISI HARİTASI + ANLIK MÜDAHALE PANELİ
# ============================================================

def _son_temas_gunu(aday: KayitAday) -> int:
    """Adayin son temas tarihinden buyana gecen gun sayisi."""
    tarihler: list[str] = []
    for ar in aday.aramalar:
        t = ar.get("tarih", "")
        if t:
            tarihler.append(t[:10])
    for gr in aday.gorusmeler:
        t = gr.get("tarih", "")
        if t:
            tarihler.append(t[:10])
    if aday.fiyat_bilgi and aday.fiyat_bilgi.get("tarih"):
        tarihler.append(aday.fiyat_bilgi["tarih"][:10])
    if aday.son_islem_tarihi:
        tarihler.append(aday.son_islem_tarihi[:10])
    if not tarihler:
        return 999
    try:
        en_son = max(tarihler)
        dt = date.fromisoformat(en_son)
        return (date.today() - dt).days
    except (ValueError, TypeError):
        return 999


def _isi_rengi(gun: int) -> tuple[str, str, str]:
    """Sogukluk seviyesine gore (renk, bg, etiket) dondurur."""
    if gun <= 1:
        return "#10b981", "#064e3b", "🔥 Sıcak"
    elif gun <= 3:
        return "#22c55e", "#14532d", "🟢 İlgili"
    elif gun <= 7:
        return "#f59e0b", "#78350f", "🟡 Ilık"
    elif gun <= 14:
        return "#f97316", "#7c2d12", "🟠 Soğuyor"
    elif gun <= 30:
        return "#ef4444", "#7f1d1d", "🔴 Soğuk"
    else:
        return "#64748b", "#1e293b", "⚫ Kayıp"


def _render_isi_haritasi(store: KayitDataStore, adaylar: list[KayitAday]):
    """Veli Isı Haritası — tüm aktif adayların temas sıcaklığı + anlık müdahale."""
    from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

    styled_section("Veli Isı Haritası", "#ef4444")
    styled_info_banner(
        "Tüm aktif adayların son temas tarihine göre sıcaklık analizi. "
        "Soğuyan veliler anında tespit edilir — kaybetmeden müdahale edin.",
        banner_type="warning", icon="🌡️")

    aktifler = [a for a in adaylar if a.aktif]
    if not aktifler:
        styled_info_banner("Aktif aday bulunamadı.", banner_type="info", icon="📭")
        return

    # Her adaya isi skoru hesapla
    isi_data: list[tuple[KayitAday, int, str, str, str]] = []
    for a in aktifler:
        gun = _son_temas_gunu(a)
        renk, bg, etiket = _isi_rengi(gun)
        isi_data.append((a, gun, renk, bg, etiket))

    # Soguktan sicaga sirala (en soguk basta = acil mudahale)
    isi_data.sort(key=lambda x: -x[1])

    # ── İstatistik kartları ──
    sicak = sum(1 for _, g, *_ in isi_data if g <= 3)
    ilik = sum(1 for _, g, *_ in isi_data if 4 <= g <= 7)
    soguyor = sum(1 for _, g, *_ in isi_data if 8 <= g <= 14)
    soguk = sum(1 for _, g, *_ in isi_data if 15 <= g <= 30)
    kayip = sum(1 for _, g, *_ in isi_data if g > 30)
    ort_gun = round(sum(g for _, g, *_ in isi_data) / max(len(isi_data), 1), 1)

    styled_stat_row([
        ("🔥 Sıcak (0-3g)", str(sicak), "#10b981", "🔥"),
        ("🟡 Ilık (4-7g)", str(ilik), "#f59e0b", "🟡"),
        ("🟠 Soğuyor (8-14g)", str(soguyor), "#f97316", "🟠"),
        ("🔴 Soğuk (15-30g)", str(soguk), "#ef4444", "🔴"),
        ("⚫ Kayıp (30g+)", str(kayip), "#64748b", "⚫"),
        ("Ort. Sessizlik", f"{ort_gun}g", "#7c3aed", "📊"),
    ])

    # ── HERO GAUGE — genel sıcaklık skoru ──
    toplam = len(isi_data)
    sicaklik_puani = round((sicak * 100 + ilik * 70 + soguyor * 40 + soguk * 15 + kayip * 0) / max(toplam, 1), 1)
    gauge_renk = "#10b981" if sicaklik_puani >= 70 else "#f59e0b" if sicaklik_puani >= 45 else "#ef4444"
    st.markdown(f"""
    <div style="text-align:center;background:#0f172a;border:1px solid {gauge_renk}40;
                border-radius:16px;padding:20px;margin:12px 0;">
        <div style="font-size:60px;font-weight:900;color:{gauge_renk};
                    font-family:Playfair Display,Georgia,serif;">{sicaklik_puani}</div>
        <div style="font-size:11px;color:#94a3b8;letter-spacing:2px;text-transform:uppercase;">
            Pipeline Sıcaklık Skoru (0-100)</div>
        <div style="font-size:12px;color:{gauge_renk};margin-top:4px;font-weight:600;">
            {toplam} aktif aday · Ortalama {ort_gun} gün sessizlik</div>
    </div>""", unsafe_allow_html=True)

    # ── ACIL MÜDAHALE LİSTESİ (soğuyanlar) ──
    acil = [(a, g, r, bg, et) for a, g, r, bg, et in isi_data if g >= 5]
    if acil:
        styled_section(f"⚠️ Acil Müdahale — {len(acil)} Aday Soğuyor")
        for a, gun, renk, bg, etiket in acil[:30]:
            temas_sayisi = a.arama_sayisi + a.gorusme_sayisi
            asama_info = a.pipeline_info
            son_sonuc = a.son_arama_sonucu or "-"
            # Isı çubuğu (0-30 gün → 100-0%)
            isi_pct = max(0, min(100, 100 - (gun / 30 * 100)))
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {renk}40;border-left:5px solid {renk};
                        border-radius:0 14px 14px 0;padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                    <div>
                        <span style="font-weight:800;color:#fff;font-size:14px;">
                            {a.veli_adi}</span>
                        <span style="color:#94a3b8;font-size:12px;margin-left:8px;">
                            — {a.ogrenci_adi} ({a.kademe} {a.hedef_sinif})</span>
                    </div>
                    <div style="display:flex;gap:6px;align-items:center;">
                        <span style="background:{renk};color:#fff;padding:3px 10px;border-radius:8px;
                                    font-size:11px;font-weight:700;">{etiket}</span>
                        <span style="background:{asama_info['color']}20;color:{asama_info['color']};
                                    padding:3px 8px;border-radius:6px;font-size:10px;font-weight:600;">
                            {asama_info['emoji']} {asama_info['label']}</span>
                    </div>
                </div>
                <div style="display:flex;gap:16px;margin-top:8px;font-size:11px;color:#94a3b8;">
                    <span>📞 {temas_sayisi} temas</span>
                    <span>🕐 {gun} gün sessiz</span>
                    <span>📋 Son: {son_sonuc}</span>
                    <span>📅 Kayıt: {a.olusturma_tarihi[:10]}</span>
                </div>
                <div style="margin-top:8px;background:#1e293b;border-radius:4px;height:6px;overflow:hidden;">
                    <div style="width:{isi_pct}%;height:100%;background:linear-gradient(90deg,{renk},{renk}80);
                                border-radius:4px;transition:width 0.3s;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # ── TÜM ADAY ISI TABLOSU ──
    styled_section("Tüm Adaylar — Isı Haritası")
    # Filtre
    fil_col1, fil_col2 = st.columns(2)
    with fil_col1:
        isi_filtre = st.selectbox("Sıcaklık Filtresi", [
            "Tümü", "🔥 Sıcak (0-3g)", "🟡 Ilık (4-7g)",
            "🟠 Soğuyor (8-14g)", "🔴 Soğuk (15-30g)", "⚫ Kayıp (30g+)"
        ], key="km_isi_filtre")
    with fil_col2:
        asama_filtre = st.selectbox("Aşama", ["Tümü"] + PIPELINE_ASAMALARI, key="km_isi_asama")

    filtered = isi_data
    if isi_filtre.startswith("🔥"):
        filtered = [(a, g, r, bg, et) for a, g, r, bg, et in filtered if g <= 3]
    elif isi_filtre.startswith("🟡"):
        filtered = [(a, g, r, bg, et) for a, g, r, bg, et in filtered if 4 <= g <= 7]
    elif isi_filtre.startswith("🟠"):
        filtered = [(a, g, r, bg, et) for a, g, r, bg, et in filtered if 8 <= g <= 14]
    elif isi_filtre.startswith("🔴"):
        filtered = [(a, g, r, bg, et) for a, g, r, bg, et in filtered if 15 <= g <= 30]
    elif isi_filtre.startswith("⚫"):
        filtered = [(a, g, r, bg, et) for a, g, r, bg, et in filtered if g > 30]
    if asama_filtre != "Tümü":
        filtered = [(a, g, r, bg, et) for a, g, r, bg, et in filtered if a.asama == asama_filtre]

    st.caption(f"📋 {len(filtered)} aday listeleniyor")

    rows_html = ""
    for a, gun, renk, bg, etiket in filtered[:50]:
        rows_html += f"""<tr>
            <td style="padding:6px 10px;font-weight:600;color:#e2e8f0;">{a.veli_adi}</td>
            <td style="padding:6px 10px;color:#94a3b8;">{a.ogrenci_adi}</td>
            <td style="padding:6px 10px;"><span style="background:{a.pipeline_info['color']}20;color:{a.pipeline_info['color']};
                padding:2px 8px;border-radius:6px;font-size:10px;font-weight:600;">
                {a.pipeline_info['emoji']} {a.pipeline_info['label']}</span></td>
            <td style="padding:6px 10px;text-align:center;font-weight:700;color:{renk};">{gun}g</td>
            <td style="padding:6px 10px;"><span style="background:{renk};color:#fff;padding:2px 8px;
                border-radius:6px;font-size:10px;font-weight:700;">{etiket}</span></td>
            <td style="padding:6px 10px;color:#94a3b8;font-size:11px;">{a.arama_sayisi}A / {a.gorusme_sayisi}G</td>
        </tr>"""

    if rows_html:
        st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead><tr style="background:#1e293b;">
            <th style="padding:8px 10px;text-align:left;color:#64748b;">Veli</th>
            <th style="padding:8px 10px;text-align:left;color:#64748b;">Öğrenci</th>
            <th style="padding:8px 10px;text-align:left;color:#64748b;">Aşama</th>
            <th style="padding:8px 10px;text-align:center;color:#64748b;">Sessizlik</th>
            <th style="padding:8px 10px;text-align:left;color:#64748b;">Sıcaklık</th>
            <th style="padding:8px 10px;text-align:left;color:#64748b;">Temas</th>
        </tr></thead><tbody>{rows_html}</tbody></table></div>""", unsafe_allow_html=True)


# ============================================================
# ZİRVE 2: BİR ADIM KALDI — AKILLI KAPANIŞ RADAR
# ============================================================

def _render_kapanis_radar(store: KayitDataStore, adaylar: list[KayitAday]):
    """Fiyat verildi + Sözleşme aşamasındaki adaylar — akıllı kapanış önerileri."""
    from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

    styled_section("Kapanış Radarı — Bir Adım Kaldı", "#f59e0b")
    styled_info_banner(
        "Fiyat verilmiş veya sözleşme aşamasındaki adaylar. Her biri için AI kapanış hamlesi. "
        "Bu adaylar kaybedilirse tüm emek boşa gider — bugün kapatın.",
        banner_type="warning", icon="🎯")

    # Hedef adaylar: fiyat_verildi + sozlesme aşamasında olanlar
    hedefler = [a for a in adaylar if a.aktif and a.asama in ("fiyat_verildi", "sozlesme")]
    if not hedefler:
        styled_info_banner("Fiyat verilmiş / sözleşme aşamasında aktif aday yok.", banner_type="info", icon="✅")
        return

    # Sırala: en çok bekleyen önce
    hedefler.sort(key=lambda a: _son_temas_gunu(a), reverse=True)

    # Kategorize
    fiyat_adaylar = [a for a in hedefler if a.asama == "fiyat_verildi"]
    sozlesme_adaylar = [a for a in hedefler if a.asama == "sozlesme"]
    krizde = [a for a in hedefler if _son_temas_gunu(a) >= 3]

    toplam_gelir = sum(
        float(a.fiyat_bilgi.get("kdv_dahil", a.fiyat_bilgi.get("toplam", 0)) or 0)
        for a in hedefler
    )

    styled_stat_row([
        ("Fiyat Verildi", str(len(fiyat_adaylar)), "#f59e0b", "💰"),
        ("Sözleşme Bekliyor", str(len(sozlesme_adaylar)), "#3b82f6", "📄"),
        ("⏰ Krizde (3g+)", str(len(krizde)), "#ef4444", "🚨"),
        ("Potansiyel Gelir", f"₺{toplam_gelir:,.0f}", "#10b981", "💎"),
    ])

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#78350f 0%,#92400e 100%);border:2px solid #f59e0b;
                border-radius:18px;padding:22px 28px;margin:14px 0;text-align:center;
                box-shadow:0 6px 24px rgba(245,158,11,0.25);">
        <div style="font-size:48px;font-weight:900;color:#fbbf24;font-family:Playfair Display,Georgia,serif;">
            {len(hedefler)}</div>
        <div style="font-size:12px;color:#fde68a;letter-spacing:3px;text-transform:uppercase;margin-top:4px;">
            Kapanışa Hazır Aday</div>
        <div style="font-size:14px;color:#fbbf24;margin-top:8px;font-weight:600;">
            Hepsi tek hamle ile kesin kayıt olabilir · Toplam ₺{toplam_gelir:,.0f} potansiyel gelir</div>
    </div>""", unsafe_allow_html=True)

    # ── KAPANIS STRATEJISI BELIRLEYICI ──
    def _kapanis_onerileri(a: KayitAday) -> list[dict]:
        """Adaya ozel kapanış hamleleri olustur."""
        gun = _son_temas_gunu(a)
        onerileri = []

        # 1. Aciliyet
        if gun >= 7:
            onerileri.append({"ikon": "🚨", "hamle": "Müdür/Kurucu Arama",
                              "aciklama": f"{gun} gün sessiz — üst düzey ilgi gösterin. Müdür bizzat arasın.",
                              "oncelik": "Kritik"})
        elif gun >= 3:
            onerileri.append({"ikon": "📞", "hamle": "Kişisel Arama",
                              "aciklama": "Veliye özel ilgi gösterin. 'Sadece sizi düşündük' mesajı.",
                              "oncelik": "Yüksek"})

        # 2. Fiyat aşamasındaysa
        if a.asama == "fiyat_verildi":
            fiyat = float(a.fiyat_bilgi.get("kdv_dahil", a.fiyat_bilgi.get("toplam", 0)) or 0)
            if fiyat > 0:
                onerileri.append({"ikon": "💎", "hamle": "Sınırlı Süreli İndirim",
                                  "aciklama": f"₺{fiyat:,.0f} üzerinde %5 erken kayıt indirimi teklif edin. 48 saat geçerli.",
                                  "oncelik": "Yüksek"})
            onerileri.append({"ikon": "🏫", "hamle": "Deneme Günü Daveti",
                              "aciklama": "Çocuğu 1 günlük ücretsiz deneme dersine davet edin. Çocuk isterse veli kabul eder.",
                              "oncelik": "Normal"})

        # 3. Sözleşme aşamasındaysa
        if a.asama == "sozlesme":
            onerileri.append({"ikon": "📋", "hamle": "Sözleşme Kolaylığı",
                              "aciklama": "E-imza linki gönderin + taksit planı önerisi yapın. Bürokratik engelleri kaldırın.",
                              "oncelik": "Yüksek"})
            onerileri.append({"ikon": "🎁", "hamle": "Kayıt Hediyesi",
                              "aciklama": "Bu hafta kayıt olursa okul çantası/kit hediye. Anlık karar tetikleyici.",
                              "oncelik": "Normal"})

        # 4. Genel
        onerileri.append({"ikon": "💬", "hamle": "WhatsApp Mesajı",
                          "aciklama": "Kişisel, sıcak bir mesaj gönderin. 'Kontenjanlar dolmadan...' aciliyeti ekleyin.",
                          "oncelik": "Normal"})

        return onerileri[:4]

    # ── ADAY KARTLARI ──
    styled_section("Aday Bazlı Kapanış Planı")
    for a in hedefler:
        gun = _son_temas_gunu(a)
        renk, bg, etiket = _isi_rengi(gun)
        asama = a.pipeline_info
        onerileri = _kapanis_onerileri(a)
        fiyat = float(a.fiyat_bilgi.get("kdv_dahil", a.fiyat_bilgi.get("toplam", 0)) or 0)
        fiyat_str = f"₺{fiyat:,.0f}" if fiyat > 0 else "Belirtilmedi"

        # Oneri HTML
        oneri_html = ""
        for on in onerileri:
            on_renk = "#ef4444" if on["oncelik"] == "Kritik" else "#f59e0b" if on["oncelik"] == "Yüksek" else "#64748b"
            oneri_html += (
                f'<div style="display:flex;gap:8px;align-items:flex-start;padding:4px 0;">'
                f'<span style="font-size:14px;">{on["ikon"]}</span>'
                f'<div><span style="font-size:12px;font-weight:700;color:#e2e8f0;">{on["hamle"]}</span>'
                f'<span style="background:{on_renk}20;color:{on_renk};padding:1px 6px;border-radius:4px;'
                f'font-size:9px;font-weight:700;margin-left:6px;">{on["oncelik"]}</span>'
                f'<div style="font-size:11px;color:#94a3b8;margin-top:2px;">{on["aciklama"]}</div></div></div>')

        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid {renk}30;border-left:5px solid {asama['color']};
                    border-radius:0 16px 16px 0;padding:16px 20px;margin-bottom:12px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.15);">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                    <span style="font-weight:800;color:#fff;font-size:15px;">{a.veli_adi}</span>
                    <span style="color:#94a3b8;font-size:12px;margin-left:8px;">— {a.ogrenci_adi} ({a.kademe} {a.hedef_sinif})</span>
                </div>
                <div style="display:flex;gap:6px;">
                    <span style="background:{renk};color:#fff;padding:3px 10px;border-radius:8px;font-size:11px;font-weight:700;">{etiket} · {gun}g</span>
                    <span style="background:{asama['color']};color:#fff;padding:3px 10px;border-radius:8px;font-size:11px;font-weight:700;">{asama['emoji']} {asama['label']}</span>
                </div>
            </div>
            <div style="display:flex;gap:20px;margin:10px 0;font-size:11px;color:#94a3b8;">
                <span>💰 {fiyat_str}</span>
                <span>📞 {a.arama_sayisi} arama · {a.gorusme_sayisi} görüşme</span>
                <span>📅 Kayıt: {a.olusturma_tarihi[:10]}</span>
                <span>🏫 {a.kanal or '-'}</span>
            </div>
            <div style="background:#1e293b;border-radius:10px;padding:10px 14px;margin-top:8px;">
                <div style="font-size:11px;color:#f59e0b;font-weight:700;margin-bottom:6px;letter-spacing:1px;text-transform:uppercase;">
                    Önerilen Kapanış Hamleleri</div>
                {oneri_html}
            </div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# ZİRVE 3: VELİDEN VELİYE REFERANS ZİNCİRİ (VİRAL LOOP)
# ============================================================

def _render_referans_zinciri(store: KayitDataStore, adaylar: list[KayitAday]):
    """Kesin kayıt velilerine referans linki + referans takip dashboard."""
    from utils.ui_common import styled_section, styled_stat_row, styled_info_banner

    styled_section("Referans Zinciri — Viral Kayıt", "#7c3aed")
    styled_info_banner(
        "Kesin kayıt olan her veli, arkadaşlarını getirecek kişisel referans linkine sahip olur. "
        "Referansla gelen her yeni kayıt, hem getireni hem geleni ödüllendirir.",
        banner_type="info", icon="🔗")

    kesin_kayitlar = [a for a in adaylar if a.asama == "kesin_kayit"]
    tum_adaylar = adaylar

    # Referans istatistikleri
    referansli_adaylar = [a for a in tum_adaylar if a.referans_veli]
    referansli_kesin = [a for a in referansli_adaylar if a.asama == "kesin_kayit"]
    toplam_referans_gelir = sum(
        float(a.fiyat_bilgi.get("kdv_dahil", a.fiyat_bilgi.get("toplam", 0)) or 0)
        for a in referansli_kesin
    )

    # Referans veren veliler — en cok getiren
    referans_verenler = Counter(a.referans_veli for a in referansli_adaylar if a.referans_veli)

    styled_stat_row([
        ("Kesin Kayıt", str(len(kesin_kayitlar)), "#10b981", "✅"),
        ("Referansla Gelen", str(len(referansli_adaylar)), "#7c3aed", "🔗"),
        ("Ref. → Kesin Kayıt", str(len(referansli_kesin)), "#2563eb", "🎯"),
        ("Ref. Geliri", f"₺{toplam_referans_gelir:,.0f}", "#f59e0b", "💎"),
        ("Aktif Referansçı", str(len(referans_verenler)), "#0891b2", "👥"),
    ])

    # ── HERO ──
    donusum = round(len(referansli_kesin) / max(len(referansli_adaylar), 1) * 100, 1)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#312e81 0%,#4c1d95 50%,#6d28d9 100%);
                border:2px solid #a78bfa;border-radius:18px;padding:22px 28px;margin:14px 0;
                box-shadow:0 6px 24px rgba(167,139,250,0.25);text-align:center;">
        <div style="font-size:11px;color:#c4b5fd;letter-spacing:3px;text-transform:uppercase;">
            Referans Dönüşüm Oranı</div>
        <div style="font-size:56px;font-weight:900;color:#a78bfa;font-family:Playfair Display,Georgia,serif;
                    margin:6px 0;">%{donusum}</div>
        <div style="font-size:13px;color:#ddd6fe;font-weight:600;">
            {len(referansli_adaylar)} referans aday → {len(referansli_kesin)} kesin kayıt
            · ₺{toplam_referans_gelir:,.0f} organik gelir</div>
    </div>""", unsafe_allow_html=True)

    # ── ALT SEKMELER ──
    ref_sub = st.tabs(["🏆 Liderlik Tablosu", "🔗 Referans Link Üretici", "📊 Referans Analiz"])

    # ═══ SEKME 1: Liderlik Tablosu ═══
    with ref_sub[0]:
        styled_section("Referans Şampiyonları")
        if not referans_verenler:
            styled_info_banner(
                "Henüz referans kaydı yok. 'Referans Link Üretici' sekmesinden velilere link gönderin.",
                banner_type="info", icon="🔗")
        else:
            for sira, (veli_adi, sayi) in enumerate(referans_verenler.most_common(20), 1):
                # Bu velinin getirdikleri
                getirdikleri = [a for a in referansli_adaylar if a.referans_veli == veli_adi]
                kesin = sum(1 for a in getirdikleri if a.asama == "kesin_kayit")
                gelir = sum(
                    float(a.fiyat_bilgi.get("kdv_dahil", a.fiyat_bilgi.get("toplam", 0)) or 0)
                    for a in getirdikleri if a.asama == "kesin_kayit"
                )
                # Madalya
                madalya = "🥇" if sira == 1 else "🥈" if sira == 2 else "🥉" if sira == 3 else f"#{sira}"
                bar_pct = min(100, sayi / max(referans_verenler.most_common(1)[0][1], 1) * 100)
                renk = "#f59e0b" if sira <= 3 else "#7c3aed"

                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {renk}30;border-radius:12px;
                            padding:12px 16px;margin-bottom:6px;display:flex;align-items:center;gap:14px;">
                    <div style="font-size:20px;min-width:36px;text-align:center;">{madalya}</div>
                    <div style="flex:1;">
                        <div style="font-weight:700;color:#e2e8f0;font-size:13px;">{veli_adi}</div>
                        <div style="display:flex;gap:12px;font-size:10px;color:#94a3b8;margin-top:3px;">
                            <span>🔗 {sayi} referans</span>
                            <span>✅ {kesin} kesin kayıt</span>
                            <span>💰 ₺{gelir:,.0f}</span>
                        </div>
                        <div style="margin-top:6px;background:#1e293b;border-radius:3px;height:4px;overflow:hidden;">
                            <div style="width:{bar_pct}%;height:100%;background:{renk};border-radius:3px;"></div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    # ═══ SEKME 2: Referans Link Üretici ═══
    with ref_sub[1]:
        styled_section("Kişisel Referans Linki Üretici")
        styled_info_banner(
            "Kesin kayıt olan veliler için kişisel referans linki oluşturun. "
            "Link paylaşıldığında, gelen aday otomatik olarak referans verenle eşleşir.",
            banner_type="info", icon="🔗")

        if not kesin_kayitlar:
            styled_info_banner("Henüz kesin kayıt yok.", banner_type="warning", icon="📭")
        else:
            sec_veli = st.selectbox(
                "Referans Linki Oluşturulacak Veli",
                [""] + [f"{a.veli_adi} — {a.ogrenci_adi}" for a in kesin_kayitlar],
                key="km_ref_veli_sec")

            if sec_veli:
                secilen = next((a for a in kesin_kayitlar if f"{a.veli_adi} — {a.ogrenci_adi}" == sec_veli), None)
                if secilen:
                    # Referans kodu: ilk 8 karakter ID
                    ref_kod = secilen.id.replace("aday_", "")[:8].upper()
                    ref_url = f"https://okuladi.smartcampus.ai/?ref={ref_kod}"

                    # Bu velinin mevcut referansları
                    mevcut_ref = [a for a in tum_adaylar if a.referans_veli == secilen.veli_adi]

                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#312e81,#4c1d95);border:2px solid #a78bfa;
                                border-radius:16px;padding:20px 24px;margin:12px 0;text-align:center;">
                        <div style="font-size:12px;color:#c4b5fd;font-weight:600;letter-spacing:2px;text-transform:uppercase;">
                            {secilen.veli_adi} İçin Kişisel Referans Linki</div>
                        <div style="background:#1e1b4b;border:1px dashed #a78bfa;border-radius:10px;
                                    padding:12px 20px;margin:12px 0;font-family:monospace;font-size:14px;
                                    color:#e0e7ff;letter-spacing:0.5px;">{ref_url}</div>
                        <div style="font-size:11px;color:#94a3b8;">
                            Referans Kodu: <b style="color:#fbbf24;">{ref_kod}</b> ·
                            Mevcut Referans: <b style="color:#a78bfa;">{len(mevcut_ref)}</b> aday</div>
                    </div>""", unsafe_allow_html=True)

                    # WhatsApp mesaj şablonu
                    wp_mesaj = (
                        f"Merhaba! 🎓\n\n"
                        f"Çocuğumuz okulumuzda çok mutlu. "
                        f"Siz de ailemize katılmak isterseniz aşağıdaki linkten bize ulaşabilirsiniz:\n\n"
                        f"{ref_url}\n\n"
                        f"Referans kodunuz: {ref_kod}\n"
                        f"Bu kodla kayıt olanlara özel indirim uygulanır! 🎁"
                    )
                    st.text_area("WhatsApp Mesaj Şablonu", value=wp_mesaj, height=150, key="km_ref_wp")
                    st.caption("Kopyalayıp veliye gönderin. Link tıklandığında referans otomatik atanır.")

    # ═══ SEKME 3: Referans Analiz ═══
    with ref_sub[2]:
        styled_section("Referans Kanal Analizi")

        if not referansli_adaylar:
            styled_info_banner("Henüz referans verisi yok.", banner_type="info", icon="📊")
        else:
            # Referans tipi dağılımı
            tip_dagilim = Counter(a.referans_tipi or "Belirtilmedi" for a in referansli_adaylar)
            st.markdown("##### Referans Tipi Dağılımı")
            for tip, sayi in tip_dagilim.most_common():
                pct = round(sayi / len(referansli_adaylar) * 100, 1)
                renk = "#10b981" if tip == "mevcut_veli" else "#7c3aed" if tip == "mezun" else "#f59e0b"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    <span style="min-width:120px;font-size:12px;color:#e2e8f0;font-weight:600;">{tip.replace('_',' ').title()}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:16px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">{sayi} (%{pct})</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # Referans → Pipeline funnel
            st.markdown("##### Referans Pipeline Dönüşümü")
            ref_pipeline = Counter(a.asama for a in referansli_adaylar)
            for asama_key in PIPELINE_ASAMALARI:
                sayi = ref_pipeline.get(asama_key, 0)
                info = PIPELINE_INFO.get(asama_key, {})
                pct = round(sayi / max(len(referansli_adaylar), 1) * 100, 1)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                    <span style="min-width:120px;font-size:11px;color:#94a3b8;">
                        {info.get('emoji','')} {info.get('label', asama_key)}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:14px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{info.get('color','#64748b')};border-radius:4px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:8px;color:#fff;font-weight:700;">{sayi}</span>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

# --- ZİRVE 4,5,6 fonksiyonları ---
from views._kayit_zirve_456 import _render_kayip_analizi, _render_yoy_sezon, _render_kontenjan_yonetimi