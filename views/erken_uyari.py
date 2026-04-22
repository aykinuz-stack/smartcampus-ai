"""
Yapay Zeka Erken Uyarı & Öğrenci 360° Profil Sistemi — Streamlit UI
====================================================================
9 modülden cross-module veri entegrasyonu ile kapsamlı öğrenci takibi.
"""

from __future__ import annotations

import streamlit as st
from datetime import datetime

from models.erken_uyari import (
    RiskCalculator,
    ErkenUyariStore,
    CrossModuleLoader,
    Intervention,
    RISK_WEIGHTS,
    risk_level_for,
    PredictiveRiskEngine,
    AIProfileSummarizer,
    AnomalyDetector,
    AIParentReportGenerator,
    AIInterventionPlanner,
)
from views._eu_common import COMP_LABELS, risk_color, grade_color, PRIORITY_COLORS
from utils.ui_common import (
    inject_common_css,
    styled_header,
    styled_section,
    styled_stat_row,
    styled_info_banner,
)
from views.eu_charts import (
    risk_distribution_3d_pie, component_bar_3d, bell_curve,
    student_radar, risk_gauge, class_comparison_bar,
    risk_trend_line, period_comparison_butterfly,
    heatmap_3d_surface, risk_sunburst, premium_stat_card,
)


def _inject_css():
    inject_common_css()
    try:
        from utils.ui_common import ultra_premium_baslat
        ultra_premium_baslat("erken_uyari")
    except Exception:
        pass
    try:
        from utils.ui_common import modul_hosgeldin, bildirim_cani
        bildirim_cani(0)
        modul_hosgeldin("erken_uyari",
            "43 kaynaktan 10 bilesikli AI risk skoru — proaktif mudahale",
            [("43", "Kaynak"), ("10", "Risk"), ("AI", "Tahmin")])
    except Exception:
        pass
    st.markdown("""<style>
    .eu-card{background:linear-gradient(135deg,#0B0F19,#94A3B8);border-radius:16px;
    padding:16px;margin-bottom:10px;border-left:4px solid #3b82f6;color:#e2e8f0}
    .eu-card h4{margin:0 0 6px;font-size:14px;color:#111827}
    .eu-card .score{font-size:26px;font-weight:800}
    .eu-card .meta{font-size:11px;color:#94a3b8;margin-top:3px}
    .eu-bar{height:7px;border-radius:4px;background:#94A3B8;overflow:hidden;margin:3px 0}
    .eu-fill{height:100%;border-radius:4px;transition:width .4s}
    .eu-alert{background:#1e1a2e;border-radius:12px;padding:12px;margin-bottom:8px;
    border-left:4px solid #f59e0b;color:#e2e8f0}
    .eu-alert.critical{border-left-color:#ef4444;background:#1e1418}
    .eu-alert.high{border-left-color:#f97316}
    .eu-alert .t{font-weight:700;font-size:13px}
    .eu-alert .m{font-size:11px;color:#94a3b8;margin-top:3px}
    .eu-sec{background:linear-gradient(135deg,#0c1322,#162033);border-radius:14px;
    padding:14px;margin-bottom:10px;border:1px solid rgba(59,130,246,.12)}
    .eu-sec h5{color:#60a5fa;margin:0 0 8px;font-size:13px;font-weight:700}
    .eu-rec{background:rgba(59,130,246,.07);border-radius:8px;padding:7px 11px;
    margin-bottom:5px;font-size:11px;color:#cbd5e1;border-left:3px solid #3b82f6}
    .eu-src{display:inline-block;padding:2px 8px;border-radius:10px;font-size:9px;
    background:rgba(99,102,241,.12);color:#818cf8;margin:2px;font-weight:600}
    .eu-module-badge{display:inline-block;padding:3px 10px;border-radius:12px;font-size:10px;
    font-weight:600;margin:2px}
    .eu-row{display:flex;justify-content:space-between;padding:3px 0;font-size:12px;
    border-bottom:1px solid rgba(255,255,255,.03)}

    /* ═══ SEKME SARIM DUZELTMESI — 32 sekme cok satira ayrilsin ═══ */
    /* Ana erken uyari sekmelerini cok satirlik flex yap */
    div[data-testid="stTabs"] > div[role="tablist"],
    .stTabs > div[data-baseweb="tab-list"],
    .stTabs [data-baseweb="tab-list"] {
        flex-wrap: wrap !important;
        row-gap: 6px !important;
        column-gap: 4px !important;
        overflow-x: visible !important;
        overflow-y: visible !important;
        scrollbar-width: none;
        padding-bottom: 8px;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none !important;
    }
    /* Her sekme kucuk ve kendi satirina cekilebilecek sekilde */
    .stTabs [data-baseweb="tab"],
    div[data-testid="stTabs"] button[role="tab"] {
        flex: 0 0 auto !important;
        min-width: auto !important;
        padding: 6px 12px !important;
        font-size: 12px !important;
        border-radius: 8px !important;
        white-space: nowrap;
    }
    /* Tablet/masaustu: 4-6 satir olabilir, sorun degil */
    @media (max-width: 900px) {
        .stTabs [data-baseweb="tab"],
        div[data-testid="stTabs"] button[role="tab"] {
            font-size: 11px !important;
            padding: 5px 9px !important;
        }
    }
    /* Tab alt cizgisini sekme alanlarina hizala */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    /* Secilen sekme belirgin olsun */
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99,102,241,.2), rgba(139,92,246,.15)) !important;
        border: 1px solid rgba(139,92,246,.4) !important;
        color: #fff !important;
    }
    </style>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
def render_erken_uyari():
    _inject_css()
    styled_header(
        "Yapay Zeka Erken Uyarı Sistemi",
        "9 Modülden Cross-Module Öğrenci 360° Takip & Risk Analizi",
        icon="🧠",
    )

    store = ErkenUyariStore()
    loader = CrossModuleLoader()
    calc = RiskCalculator()

    # Hizli Erisim Dropdown — 32 sekme arasinda hizli gezinmek icin
    _TAB_LABELS = [
        "📊 Dashboard", "🎯 360° Profil", "🔴 Erken Uyarı", "📈 Risk Skoru",
        "🗺️ Kazanım Haritası", "👨‍👩‍👧 Veli Raporu", "🧭 Rehberlik", "📉 Kohort Analizi",
        "🤖 AI Merkezi", "🔥 Isı Haritası", "📊 Dönem Karşılaştırma", "🔄 Müdahale Takip",
        "📋 Kurum Karnesi", "🚨 Escalation", "🛡️ Koruyucu Faktör", "🔮 Dropout Tahmin",
        "🛡️ Zorbalık Tespit", "🔀 Geçiş Dönemi", "📊 Davranış Tarama", "🌐 Risk Füzyon",
        "📱 Bildirim Merkezi", "🏅 Pozitif Davranış", "🧬 Risk DNA", "📡 Komuta Merkezi",
        "🔮 Kaynak Optimizasyon", "🏛️ MEB Uyumluluk", "🎭 Senaryo Planlama",
        "📖 Başarı Arşivi", "🗺️ Mezun Başarı Haritası", "🏥 Cross-Alert",
        "🧭 Kariyer Pusula", "🛡️ Bütüncül Risk 20-Boyut",
    ]
    with st.expander(f"🔍 Hızlı Erişim — 32 sekme arasında arama ve filtreleme", expanded=False):
        col_a, col_b = st.columns([3, 1])
        with col_a:
            arama = st.text_input("Sekme ara (kelime yaz, ornegin 'risk' veya 'aile')",
                                  key="eu_tab_search", placeholder="örn: zorbalık, protokol, 360...")
        with col_b:
            st.caption(" ")
            if st.button("🔄 Temizle", key="eu_tab_search_clear"):
                st.session_state["eu_tab_search"] = ""
                st.rerun()
        if arama.strip():
            q = arama.strip().lower()
            eslesen = [(i, lbl) for i, lbl in enumerate(_TAB_LABELS) if q in lbl.lower()]
            if eslesen:
                st.success(f"**{len(eslesen)} sekme eşleşti** — aşağıdaki sekme listesinde bu sekmeleri bulup tıkla:")
                cols = st.columns(min(len(eslesen), 4))
                for idx, (i, lbl) in enumerate(eslesen):
                    with cols[idx % len(cols)]:
                        st.markdown(
                            f"<div style='background:rgba(99,102,241,.15); border:1px solid #6366f1; "
                            f"border-radius:6px; padding:6px 10px; margin:3px 0; font-size:12px;'>"
                            f"<b>#{i+1}</b>  {lbl}</div>",
                            unsafe_allow_html=True,
                        )
            else:
                st.warning("Eşleşen sekme yok. Farklı kelime dene.")

    # -- Tab Gruplama (32 tab -> 5 grup) --
    _GRP_38508 = {
        "📋 Grup A": [("📊 Dashboard", 0), ("🎯 360° Profil", 1), ("🔴 Erken Uyarı", 2), ("📈 Risk Skoru", 3), ("🗺️ Kazanım Haritası", 4), ("👨‍👩‍👧 Veli Raporu", 5), ("🧭 Rehberlik", 6)],
        "📊 Grup B": [("📉 Kohort Analizi", 7), ("🤖 AI Merkezi", 8), ("🔥 Isı Haritası", 9), ("📊 Dönem Karşılaştırma", 10), ("🔄 Müdahale Takip", 11), ("📋 Kurum Karnesi", 12), ("🚨 Escalation", 13)],
        "🔧 Grup C": [("🛡️ Koruyucu Faktör", 14), ("🔮 Dropout Tahmin", 15), ("🛡️ Zorbalık Tespit", 16), ("🔀 Geçiş Dönemi", 17), ("📊 Davranış Tarama", 18), ("🌐 Risk Füzyon", 19), ("📱 Bildirim Merkezi", 20)],
        "📈 Grup D": [("🏅 Pozitif Davranış", 21), ("🧬 Risk DNA", 22), ("📡 Komuta Merkezi", 23), ("🔮 Kaynak Optimizasyon", 24), ("🏛️ MEB Uyumluluk", 25), ("🎭 Senaryo Planlama", 26), ("📖 Başarı Arşivi", 27)],
        "🎯 Grup E": [("🗺️ Mezun Başarı Haritası", 28), ("🏥 Cross-Alert", 29), ("🧭 Kariyer Pusula", 30), ("🛡️ Bütüncül Risk 20-Boyut", 31)],
    }
    _sg_38508 = st.radio("", list(_GRP_38508.keys()), horizontal=True, label_visibility="collapsed", key="rg_38508")
    _gt_38508 = _GRP_38508[_sg_38508]
    _aktif_idx_38508 = set(t[1] for t in _gt_38508)
    _tab_names_38508 = [t[0] for t in _gt_38508]
    tabs = st.tabs(_tab_names_38508)
    _tab_real_38508 = {idx: t for idx, t in zip((t[1] for t in _gt_38508), tabs)}

    if 0 in _aktif_idx_38508:
      with _tab_real_38508[0]:
        _tab_dashboard(store, loader, calc)
    if 1 in _aktif_idx_38508:
      with _tab_real_38508[1]:
        _tab_360(store, loader)
    if 2 in _aktif_idx_38508:
      with _tab_real_38508[2]:
        _tab_alerts(store)
    if 3 in _aktif_idx_38508:
      with _tab_real_38508[3]:
        _tab_risk(store, calc)
    if 4 in _aktif_idx_38508:
      with _tab_real_38508[4]:
        _tab_kazanim(store, loader)
    if 5 in _aktif_idx_38508:
      with _tab_real_38508[5]:
        _tab_veli(store, loader)
    if 6 in _aktif_idx_38508:
      with _tab_real_38508[6]:
        _tab_rehberlik(store, loader)
    if 7 in _aktif_idx_38508:
      with _tab_real_38508[7]:
        _tab_kohort(store, loader)
    if 8 in _aktif_idx_38508:
      with _tab_real_38508[8]:
        _tab_ai_center(store, loader)
    if 9 in _aktif_idx_38508:
      with _tab_real_38508[9]:
        _tab_heatmap(store, loader)
    if 10 in _aktif_idx_38508:
      with _tab_real_38508[10]:
        _tab_donem_karsilastirma(store, loader)
    if 11 in _aktif_idx_38508:
      with _tab_real_38508[11]:
        _tab_mudahale_takip(store)
    if 12 in _aktif_idx_38508:
      with _tab_real_38508[12]:
        _tab_kurum_karnesi(store, loader)
    if 13 in _aktif_idx_38508:
      with _tab_real_38508[13]:
        try:
            from views._eu_yeni_ozellikler import render_escalation_motoru
            render_escalation_motoru(store, loader)
        except Exception as _e:
            st.error(f"Escalation yuklenemedi: {_e}")
    if 14 in _aktif_idx_38508:
      with _tab_real_38508[14]:
        try:
            from views._eu_yeni_ozellikler import render_koruyucu_faktor
            render_koruyucu_faktor(store, loader)
        except Exception as _e:
            st.error(f"Koruyucu Faktor yuklenemedi: {_e}")
    if 15 in _aktif_idx_38508:
      with _tab_real_38508[15]:
        try:
            from views._eu_yeni_ozellikler import render_dropout_tahmin
            render_dropout_tahmin(store, loader)
        except Exception as _e:
            st.error(f"Dropout Tahmin yuklenemedi: {_e}")
    if 16 in _aktif_idx_38508:
      with _tab_real_38508[16]:
        try:
            from views._eu_super_features import render_zorbalik_tespit
            render_zorbalik_tespit(store, loader)
        except Exception as _e:
            st.error(f"Zorbalik Tespit yuklenemedi: {_e}")
    if 17 in _aktif_idx_38508:
      with _tab_real_38508[17]:
        try:
            from views._eu_super_features import render_gecis_donemi
            render_gecis_donemi(store, loader)
        except Exception as _e:
            st.error(f"Gecis Donemi yuklenemedi: {_e}")
    if 18 in _aktif_idx_38508:
      with _tab_real_38508[18]:
        try:
            from views._eu_super_features import render_davranis_tarama
            render_davranis_tarama(store, loader)
        except Exception as _e:
            st.error(f"Davranis Tarama yuklenemedi: {_e}")
    if 19 in _aktif_idx_38508:
      with _tab_real_38508[19]:
        try:
            from views._eu_mega_features import render_fuzyon_motoru
            render_fuzyon_motoru(store, loader)
        except Exception as _e:
            st.error(f"Risk Fuzyon yuklenemedi: {_e}")
    if 20 in _aktif_idx_38508:
      with _tab_real_38508[20]:
        try:
            from views._eu_mega_features import render_bildirim_merkezi
            render_bildirim_merkezi(store, loader)
        except Exception as _e:
            st.error(f"Bildirim Merkezi yuklenemedi: {_e}")
    if 21 in _aktif_idx_38508:
      with _tab_real_38508[21]:
        try:
            from views._eu_mega_features import render_pozitif_davranis
            render_pozitif_davranis(store, loader)
        except Exception as _e:
            st.error(f"Pozitif Davranis yuklenemedi: {_e}")
    if 22 in _aktif_idx_38508:
      with _tab_real_38508[22]:
        try:
            from views._eu_zirve_features import render_risk_dna
            render_risk_dna(store, loader)
        except Exception as _e:
            st.error(f"Risk DNA yuklenemedi: {_e}")
    if 23 in _aktif_idx_38508:
      with _tab_real_38508[23]:
        try:
            from views._eu_zirve_features import render_komuta_merkezi
            render_komuta_merkezi(store, loader)
        except Exception as _e:
            st.error(f"Komuta Merkezi yuklenemedi: {_e}")
    if 24 in _aktif_idx_38508:
      with _tab_real_38508[24]:
        try:
            from views._eu_zirve_features import render_kaynak_optimizasyon
            render_kaynak_optimizasyon(store, loader)
        except Exception as _e:
            st.error(f"Kaynak Optimizasyon yuklenemedi: {_e}")
    if 25 in _aktif_idx_38508:
      with _tab_real_38508[25]:
        try:
            from views._eu_final_features import render_meb_uyumluluk
            render_meb_uyumluluk(store, loader)
        except Exception as _e:
            st.error(f"MEB Uyumluluk yuklenemedi: {_e}")
    if 26 in _aktif_idx_38508:
      with _tab_real_38508[26]:
        try:
            from views._eu_final_features import render_senaryo_planlama
            render_senaryo_planlama(store, loader)
        except Exception as _e:
            st.error(f"Senaryo Planlama yuklenemedi: {_e}")
    if 27 in _aktif_idx_38508:
      with _tab_real_38508[27]:
        try:
            from views._eu_final_features import render_basari_arsivi
            render_basari_arsivi(store, loader)
        except Exception as _e:
            st.error(f"Basari Arsivi yuklenemedi: {_e}")
    if 28 in _aktif_idx_38508:
      with _tab_real_38508[28]:
        try:
            from views._eu_cross_module import render_basari_haritasi
            render_basari_haritasi(store, loader)
        except Exception as _e:
            st.error(f"Mezun Basari Haritasi yuklenemedi: {_e}")
    if 29 in _aktif_idx_38508:
      with _tab_real_38508[29]:
        try:
            from views._eu_cross_module import render_cross_alert
            render_cross_alert(store, loader)
        except Exception as _e:
            st.error(f"Cross-Alert yuklenemedi: {_e}")
    if 30 in _aktif_idx_38508:
      with _tab_real_38508[30]:
        try:
            from views._eu_cross_module import render_kariyer_pusula
            render_kariyer_pusula(store, loader)
        except Exception as _e:
            st.error(f"Kariyer Pusula yuklenemedi: {_e}")
    if 31 in _aktif_idx_38508:
      with _tab_real_38508[31]:
        try:
            from views._eu_butuncul_risk import render_butuncul_panel
            render_butuncul_panel(store, loader)
        except Exception as _e:
            st.error(f"Butuncul Risk Paneli yuklenemedi: {_e}")
            import traceback
            with st.expander("Hata detayi"):
                st.code(traceback.format_exc())


# ═══════════════════════════════════════════════════════════════
# TAB 1: DASHBOARD
# ═══════════════════════════════════════════════════════════════
def _tab_dashboard(store, loader, calc):
    styled_section("📊 Veri Kaynakları & Genel Bakış")

    # Duygu Check-in widget — riskli öğrenciler varsa gösterir
    try:
        from views._mood_checkin import render_mood_erken_uyari_widget
        render_mood_erken_uyari_widget()
    except Exception:
        pass

    # Veri özeti
    summary = loader.get_data_summary()
    students = loader.load_students()
    aktif = sum(1 for s in students if s.get("durum") == "aktif")
    risks = store.get_latest_risks()
    alerts = store.get_active_alerts()

    # Üst istatistikler
    styled_stat_row([
        ("Aktif Öğrenci", str(aktif), "#3b82f6", "👥"),
        ("Analiz Edilen", str(len(risks)), "#8b5cf6", "📊"),
        ("Aktif Uyarı", str(len(alerts)), "#ef4444", "🔔"),
        ("Veri Kaynağı", str(sum(1 for v in summary.values() if v > 0)), "#6366f1", "🔗"),
    ])

    # Modül bazlı veri sayıları — gömülü expander (aç/kapa)
    aktif_kaynak = sum(1 for v in summary.values() if v > 0)
    toplam_kayit = sum(summary.values())
    with st.expander(f"🔗 Cross-Module Veri Kaynakları — {aktif_kaynak} aktif kaynak, {toplam_kayit} kayıt", expanded=False):
        modules = [
            ("📚 Akademik Takip / Notlar", summary.get("Not Kaydı", 0), "#3b82f6"),
            ("📅 Akademik Takip / Devamsızlık", summary.get("Devamsızlık", 0), "#f59e0b"),
            ("📝 Ölçme & Değerlendirme / Sınav", summary.get("Sınav Sonucu", 0), "#8b5cf6"),
            ("📋 Akademik Takip / Ödev", summary.get("Ödev", 0), "#06b6d4"),
            ("📤 Akademik Takip / Ödev Teslim", summary.get("Ödev Teslim", 0), "#14b8a6"),
            ("🎯 Akademik Takip / Kazanım Borcu", summary.get("Kazanım Borcu", 0), "#f97316"),
            ("🔄 Ölçme / Telafi Görevi", summary.get("Telafi Görevi", 0), "#ec4899"),
            ("🧭 Rehberlik / Vaka", summary.get("Rehberlik Vaka", 0), "#e11d48"),
            ("💬 Rehberlik / Görüşme", summary.get("Rehberlik Görüşme", 0), "#be185d"),
            ("🏥 Okul Sağlığı", summary.get("Sağlık Ziyareti", 0), "#22c55e"),
            ("📊 KYT Kazanım Yoklama", summary.get("KYT Cevap", 0), "#a855f7"),
            ("📱 Veli Mesajları", summary.get("Veli Mesaj", 0), "#0ea5e9"),
        ]
        for name, count, color in modules:
            status = "✅" if count > 0 else "⬜"
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;padding:4px 8px;'
                f'font-size:12px;color:#cbd5e1;border-bottom:1px solid rgba(255,255,255,.03)">'
                f'<span>{status} {name}</span>'
                f'<span style="color:{color};font-weight:700">{count} kayıt</span></div>',
                unsafe_allow_html=True,
            )

    # Hesapla butonu
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧠 Tüm Öğrencileri Analiz Et (9 Modül)", type="primary", use_container_width=True):

            with st.spinner("Cross-module veri analizi yapılıyor... 9 modülden veri çekiliyor..."):
                results = calc.calculate_all()
                crit = sum(1 for r in results if r.risk_level == "CRITICAL")
                high = sum(1 for r in results if r.risk_level == "HIGH")
                st.success(f"✅ {len(results)} öğrenci analiz edildi! | 🔴 Kritik: {crit} | 🟠 Yüksek: {high}")
                st.rerun()
    with c2:
        if st.button("🔄 Verileri Yenile", use_container_width=True):

            st.rerun()

    # Risk dağılımı — Ultra Premium Grafikler
    if risks:
        st.markdown("---")
        dist = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        for r in risks:
            lv = r.get("risk_level", "LOW")
            if lv in dist:
                dist[lv] += 1

        # Premium stat kartları
        all_scores = [r.get("risk_score", 0) for r in risks]
        _avg_sc = sum(all_scores) / len(all_scores) if all_scores else 0
        _cards = st.columns(6)
        _card_data = [
            ("Toplam Öğrenci", str(len(risks)), "", "#6366f1", "👥"),
            ("Risk Ortalaması", f"{_avg_sc:.1f}", "", "#3b82f6", "📊"),
            ("🟢 Düşük", str(dist["LOW"]), "", "#22c55e", "✅"),
            ("🟡 Orta", str(dist["MEDIUM"]), "", "#f59e0b", "⚠️"),
            ("🟠 Yüksek", str(dist["HIGH"]), "", "#f97316", "🔶"),
            ("🔴 Kritik", str(dist["CRITICAL"]), "", "#ef4444", "🚨"),
        ]
        for i, (lb, vl, dt, clr, ic) in enumerate(_card_data):
            with _cards[i]:
                st.markdown(premium_stat_card(lb, vl, dt, clr, ic), unsafe_allow_html=True)

        # 3 kolon: Pasta + Çan Eğrisi + Gauge
        gc1, gc2, gc3 = st.columns(3)
        with gc1:
            risk_distribution_3d_pie(dist["LOW"], dist["MEDIUM"], dist["HIGH"], dist["CRITICAL"])
        with gc2:
            bell_curve(all_scores, "Risk Puanı Çan Eğrisi")
        with gc3:
            risk_gauge(_avg_sc, "Kurum Risk Ortalaması")

        # Bileşen Ortalamaları — 3D Bar
        _comp_labels = {
            "grade_risk": "Not", "attendance_risk": "Devam.", "exam_risk": "Sınav",
            "homework_risk": "Ödev", "outcome_debt_risk": "Kaz.Borç", "counseling_risk": "Rehber.",
            "health_risk": "Sağlık", "trend_risk": "Trend", "behavior_risk": "Davranış",
            "foreign_lang_risk": "Yab.Dil",
        }
        _comp_avgs = {}
        for ck, cl in _comp_labels.items():
            vals = [r.get(ck, 0) for r in risks]
            _comp_avgs[cl] = sum(vals) / len(vals) if vals else 0
        component_bar_3d(_comp_avgs)

        # Sınıf Karşılaştırma + Sunburst
        _class_scores: dict[str, list] = {}
        for r in risks:
            k = f"{r.get('sinif', '?')}/{r.get('sube', '?')}"
            _class_scores.setdefault(k, []).append(r.get("risk_score", 0))

        sc1, sc2 = st.columns(2)
        with sc1:
            class_comparison_bar(_class_scores)
        with sc2:
            risk_sunburst(risks)

        # En riskli 5
        styled_section("🚨 En Riskli 5 Öğrenci")
        for r in sorted(risks, key=lambda x: x.get("risk_score", 0), reverse=True)[:5]:
            lv = risk_level_for(r.get("risk_score", 0))
            sources = r.get("data_sources_used", [])
            src_html = "".join(f'<span class="eu-src">{s}</span>' for s in sources[:4])
            st.markdown(f"""
            <div class="eu-alert {'critical' if r.get('risk_level')=='CRITICAL' else 'high' if r.get('risk_level')=='HIGH' else ''}">
                <div class="t">{lv['icon']} {r.get('student_name','')} — {r.get('sinif','')}/{r.get('sube','')}</div>
                <div class="m">
                    Risk: <b style="color:{lv['color']}">{r.get('risk_score',0)}</b> |
                    Not: {r.get('grade_avg',0)} | Devam: {r.get('attendance_total',0)}g |
                    Sınav: {r.get('exam_avg',0)} | Ödev: {r.get('homework_submitted',0)}/{r.get('homework_total',0)} |
                    Rehberlik: {r.get('counseling_open_cases',0)} vaka
                </div>
                <div style="margin-top:4px">{src_html}</div>
            </div>""", unsafe_allow_html=True)

    # ═══ SINIF BAZLI RISK ANALIZI ═══
    if risks:
        st.markdown("---")
        styled_section("📊 Sınıf Bazlı Risk Analizi & Yorum")

        sinif_risk: dict[str, dict] = {}
        for r in risks:
            key = f"{r.get('sinif', '?')}/{r.get('sube', '?')}"
            if key not in sinif_risk:
                sinif_risk[key] = {"scores": [], "high": 0, "critical": 0, "names": []}
            sinif_risk[key]["scores"].append(r.get("risk_score", 0))
            sinif_risk[key]["names"].append(r.get("student_name", ""))
            if r.get("risk_level") == "HIGH":
                sinif_risk[key]["high"] += 1
            elif r.get("risk_level") == "CRITICAL":
                sinif_risk[key]["critical"] += 1

        for key in sorted(sinif_risk.keys()):
            info = sinif_risk[key]
            avg = round(sum(info["scores"]) / len(info["scores"]), 1)
            stu_cnt = len(info["scores"])
            risk_cnt = info["high"] + info["critical"]

            # Yorum
            if info["critical"] > 0:
                yorum = f"🚨 KRİTİK — {info['critical']} öğrenci acil müdahale bekliyor"
                y_clr = "#ef4444"
            elif info["high"] > 0:
                yorum = f"🟠 DİKKAT — {info['high']} öğrenci yüksek riskte"
                y_clr = "#f97316"
            elif avg > 40:
                yorum = f"🟡 TAKİP — Ortalama risk ortanın üstünde"
                y_clr = "#f59e0b"
            else:
                yorum = f"🟢 İYİ — Risk kontrol altında"
                y_clr = "#22c55e"

            # Aksiyon
            if risk_cnt > 0:
                aksiyon = f"Bu sınıfta {risk_cnt} riskli öğrenci var → Rehberlik yönlendirmesi + veli görüşmesi yapın"
            elif avg > 30:
                aksiyon = "Haftalık takip rutini oluşturun — ödev + devamsızlık kontrolü"
            else:
                aksiyon = "Koruyucu takip yeterli — aylık kontrol"

            st.markdown(f"""<div style="background:#0f172a;border-radius:12px;padding:12px 16px;
            margin:6px 0;border-left:4px solid {y_clr};">
            <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
            <div style="font-size:.92rem;font-weight:700;color:#e2e8f0;">{key} — {stu_cnt} öğrenci</div>
            <div style="font-size:.8rem;color:{y_clr};margin-top:2px;">{yorum}</div>
            </div>
            <div style="text-align:right;">
            <div style="font-size:1.3rem;font-weight:900;color:{y_clr};">{avg}</div>
            <div style="font-size:.6rem;color:#475569;">ort risk</div>
            </div></div>
            <div style="font-size:.75rem;color:#818cf8;margin-top:6px;padding:4px 8px;
            background:rgba(99,102,241,0.08);border-radius:6px;">💡 {aksiyon}</div>
            </div>""", unsafe_allow_html=True)

        # Toplu yorum
        total_high = sum(info["high"] + info["critical"] for info in sinif_risk.values())
        overall_avg = round(sum(r.get("risk_score", 0) for r in risks) / len(risks), 1) if risks else 0
        en_riskli = max(sinif_risk.items(), key=lambda x: sum(x[1]["scores"])/len(x[1]["scores"])) if sinif_risk else None
        en_guvenli = min(sinif_risk.items(), key=lambda x: sum(x[1]["scores"])/len(x[1]["scores"])) if sinif_risk else None

        st.markdown(f"""<div style="background:linear-gradient(135deg,#0c1929,#1e3a5f);
        border-radius:12px;padding:14px 18px;margin:8px 0;border:1px solid rgba(59,130,246,0.2);">
        <div style="font-size:.88rem;font-weight:700;color:#93c5fd;margin-bottom:6px;">
        📊 Toplu Değerlendirme</div>
        <div style="font-size:.82rem;color:#cbd5e1;line-height:1.6;">
        • Kurum geneli ortalama risk: <b>{overall_avg}</b>/100<br>
        • Toplam yüksek/kritik riskli öğrenci: <b>{total_high}</b><br>
        {f'• En riskli sınıf: <b>{en_riskli[0]}</b> (ort {sum(en_riskli[1]["scores"])/len(en_riskli[1]["scores"]):.0f})' if en_riskli else ''}
        <br>
        {f'• En güvenli sınıf: <b>{en_guvenli[0]}</b> (ort {sum(en_guvenli[1]["scores"])/len(en_guvenli[1]["scores"]):.0f})' if en_guvenli else ''}
        </div></div>""", unsafe_allow_html=True)

    # ═══ ERKEN UYARI VIZYON ═══
    st.markdown("---")
    _render_erken_uyari_vizyon(risks, aktif)


def _render_erken_uyari_vizyon(risks, aktif):
    """Erken Uyari sistemi vizyonu — mevcut durum + ideal durum + yol haritasi + AI vizyon."""

    # Mevcut durum analizi
    if not risks:
        risk_high = 0
        risk_crit = 0
        avg_score = 0
    else:
        risk_high = sum(1 for r in risks if r.get("risk_level") == "HIGH")
        risk_crit = sum(1 for r in risks if r.get("risk_level") == "CRITICAL")
        avg_score = round(sum(r.get("risk_score", 0) for r in risks) / len(risks), 1)

    # Risk faktor dagilimi
    faktor_avgs = {}
    if risks:
        for key in ["grade_risk", "attendance_risk", "exam_risk", "homework_risk",
                     "outcome_debt_risk", "counseling_risk", "health_risk", "trend_risk", "behavior_risk"]:
            vals = [r.get(key, 0) for r in risks]
            faktor_avgs[key] = round(sum(vals) / len(vals), 1)

    # Ideal vs mevcut
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#312e81 100%);
    border-radius:18px;padding:24px;margin:16px 0;border:1.5px solid rgba(99,102,241,0.25);">
    <div style="font-size:1.1rem;font-weight:900;color:#c7d2fe;letter-spacing:.3px;">
    🔮 Erken Uyarı Sistemi — Vizyon & Yol Haritası</div>
    <div style="font-size:.82rem;color:#818cf8;margin-top:4px;">
    Mevcut durumdan ideale — her öğrenci güvende, her risk kontrol altında</div>
    </div>""", unsafe_allow_html=True)

    # Gap kartlari
    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        st.markdown(f"""<div style="background:#052e16;border:1px solid #22c55e40;
        border-radius:12px;padding:14px;text-align:center;">
        <div style="font-size:.7rem;color:#86efac;text-transform:uppercase;">Ideal Durum</div>
        <div style="color:#e2e8f0;font-size:.85rem;margin-top:6px;">
        Sıfır kritik/yüksek risk<br>Ort risk skoru &lt;25<br>
        Tüm modüller veri besliyor<br>Haftalık otomatik tarama</div>
        </div>""", unsafe_allow_html=True)
    with gc2:
        mev_clr = "#22c55e" if risk_crit + risk_high == 0 else ("#f59e0b" if risk_crit == 0 else "#ef4444")
        st.markdown(f"""<div style="background:#1c0505;border:1px solid {mev_clr}40;
        border-radius:12px;padding:14px;text-align:center;">
        <div style="font-size:.7rem;color:{mev_clr};text-transform:uppercase;">Mevcut Durum</div>
        <div style="color:#e2e8f0;font-size:.85rem;margin-top:6px;">
        {risk_crit} kritik + {risk_high} yüksek risk<br>
        Ort risk skoru: {avg_score}<br>
        {len(risks)} öğrenci analiz edildi<br>
        {'Tarama yapıldı' if risks else 'Henüz tarama yok'}</div>
        </div>""", unsafe_allow_html=True)
    with gc3:
        gap = max(0, avg_score - 25) if avg_score > 25 else 0
        gap_clr = "#22c55e" if gap == 0 else ("#f59e0b" if gap < 15 else "#ef4444")
        st.markdown(f"""<div style="background:#0f172a;border:1px solid {gap_clr}40;
        border-radius:12px;padding:14px;text-align:center;">
        <div style="font-size:.7rem;color:{gap_clr};text-transform:uppercase;">Gap</div>
        <div style="font-size:2rem;font-weight:900;color:{gap_clr};margin:6px 0;">
        {'✅ 0' if gap == 0 else f'{gap:.0f} puan'}</div>
        <div style="font-size:.75rem;color:#64748b;">
        {'Hedefte!' if gap == 0 else 'Kapanması gereken fark'}</div>
        </div>""", unsafe_allow_html=True)

    # Yol haritasi
    if risks:
        st.markdown("#### Erken Uyarı İyileştirme Yol Haritası")
        roadmap = []

        if risk_crit > 0:
            roadmap.append(("🔴", "ACİL", "1 Gün",
                            f"{risk_crit} kritik riskli öğrenci için acil müdahale planı",
                            "Rehberlik yönlendirmesi + veli görüşmesi + bireysel destek"))
        if risk_high > 0:
            roadmap.append(("🟠", "YÜKSEK", "1 Hafta",
                            f"{risk_high} yüksek riskli öğrenci için takip programı",
                            "Haftalık kontrol + ödev desteği + etüt planlaması"))
        if faktor_avgs:
            en_yuksek = max(faktor_avgs.items(), key=lambda x: x[1])
            faktor_labels = {
                "grade_risk": "Not", "attendance_risk": "Devamsızlık", "exam_risk": "Sınav",
                "homework_risk": "Ödev", "outcome_debt_risk": "Kazanım Borcu",
                "counseling_risk": "Rehberlik", "health_risk": "Sağlık",
                "trend_risk": "Trend", "behavior_risk": "Davranış",
            }
            roadmap.append(("🎯", "ORTA", "2 Hafta",
                            f"En yüksek risk faktörü: {faktor_labels.get(en_yuksek[0], en_yuksek[0])} (%{en_yuksek[1]:.0f})",
                            "Bu alanda hedefli iyileştirme programı başlatın"))

        roadmap.append(("📊", "SÜREKLI", "Haftalık",
                        "Düzenli risk taraması rutini oluşturun",
                        "Her Pazartesi otomatik tarama + Cuma rapor kontrolü"))
        roadmap.append(("🔮", "VIZYON", "6 Ay",
                        "Sıfır kritik risk hedefi — tüm öğrenciler güvende",
                        "Proaktif müdahale kültürü + veri odaklı karar verme"))

        for icon, pri, sure, baslik, detay in roadmap:
            pri_clr = {"ACİL": "#ef4444", "YÜKSEK": "#f97316", "ORTA": "#f59e0b",
                       "SÜREKLI": "#6366f1", "VIZYON": "#8b5cf6"}.get(pri, "#64748b")
            st.markdown(f"""<div style="display:flex;gap:12px;align-items:flex-start;padding:8px 0;
            border-bottom:1px solid #1e293b;">
            <div style="min-width:70px;text-align:center;">
            <div style="font-size:1.3rem;">{icon}</div>
            <div style="font-size:.6rem;color:{pri_clr};font-weight:700;">{pri}</div>
            <div style="font-size:.55rem;color:#475569;">{sure}</div>
            </div>
            <div style="flex:1;">
            <div style="font-size:.88rem;font-weight:700;color:#e2e8f0;">{baslik}</div>
            <div style="font-size:.78rem;color:#94a3b8;margin-top:2px;">{detay}</div>
            </div></div>""", unsafe_allow_html=True)

    # AI Vizyon butonu
    st.markdown("---")
    _vizyon_key = "_eu_vizyon_text"
    if st.session_state.get(_vizyon_key):
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f172a,#1e1b4b,#4c1d95);
        border-radius:16px;padding:24px;margin:8px 0;border:1.5px solid rgba(139,92,246,0.3);">
        <div style="font-size:.9rem;font-weight:800;color:#c4b5fd;margin-bottom:10px;">
        🔮 AI Erken Uyarı Vizyonu</div>
        <div style="color:#e2e8f0;font-size:.88rem;line-height:1.7;">
        {st.session_state[_vizyon_key]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        if st.button("🔮 AI Erken Uyarı Vizyonu Oluştur", key="eu_vizyon_btn",
                       type="primary", use_container_width=True):
            try:
                from utils.smarti_helper import _get_client, _get_ai_response
                client = _get_client()
                if client:
                    with st.spinner("AI erken uyarı vizyonu oluşturuyor..."):
                        context = (
                            f"{aktif} aktif öğrenci, {len(risks)} analiz edildi. "
                            f"Ortalama risk: {avg_score}. Kritik: {risk_crit}, Yüksek: {risk_high}. "
                            f"Risk faktörleri: {', '.join(f'{k}:%{v:.0f}' for k, v in faktor_avgs.items()) if faktor_avgs else 'veri yok'}. "
                            f"Bu veriye göre 3 yıllık erken uyarı vizyon stratejisi yaz. "
                            f"Her yıl için somut hedef + ogrenci odaklı + veli katılımlı + veri odaklı. "
                            f"Motivasyonel ve cesur. 300 kelime. Türkçe."
                        )
                        messages = [
                            {"role": "system", "content": "Eğitim risk yönetimi uzmanı. Cesur, ilham verici, somut."},
                            {"role": "user", "content": context},
                        ]
                        result = _get_ai_response(client, messages)
                        if result:
                            st.session_state[_vizyon_key] = result
                            st.rerun()
            except Exception:
                pass


# ═══════════════════════════════════════════════════════════════
# TAB 2: 360° PROFİL
# ═══════════════════════════════════════════════════════════════
def _tab_360(store, loader):
    styled_section("🎯 Öğrenci 360° Komple Takip Kartı")

    students = loader.load_students()
    aktif = [s for s in students if s.get("durum") == "aktif"]
    if not aktif:
        styled_info_banner("Aktif öğrenci bulunamadı.", "warning")
        return

    opts = {f"{s.get('ad','')} {s.get('soyad','')} — {s.get('sinif','')}/{s.get('sube','')}": s for s in aktif}
    selected = st.selectbox("Öğrenci Seç", [""] + list(opts.keys()))

    if not selected:
        styled_info_banner("Bir öğrenci seçin → 9 modülden toplanan verileri tek ekranda görün.", "info")
        return

    stu = opts[selected]
    sid = stu.get("id", "")

    # Tüm verileri çek
    risk_hist = store.get_student_risk_history(sid)
    latest = risk_hist[-1] if risk_hist else None
    grades = [g for g in loader.load_grades() if g.get("student_id") == sid]
    attendance = [a for a in loader.load_attendance() if a.get("student_id") == sid]
    exams = [e for e in loader.load_exam_results() if e.get("student_id") == sid]
    hw_subs = [h for h in loader.load_homework_submissions() if h.get("student_id") == sid]
    borc = [b for b in loader.load_kazanim_borclari() if b.get("student_id") == sid]
    telafi = [t for t in loader.load_telafi_tasks() if t.get("student_id") == sid]
    vakalar = [v for v in loader.load_rehberlik_vakalar() if v.get("ogrenci_id") == sid]
    gorusmeler = [g2 for g2 in loader.load_rehberlik_gorusmeler() if g2.get("ogrenci_id") == sid]
    saglik = [s2 for s2 in loader.load_saglik_ziyaretleri() if s2.get("ogrenci_id") == sid]
    kyt = [k for k in loader.load_kyt_answers() if k.get("student_id") == sid]
    # MEB Dijital Formlar
    meb_ogr: dict[str, list] = {}
    try:
        _meb_all_eu = loader.load_all_meb_forms()
        for _sk, _fl in _meb_all_eu.items():
            for _f in _fl:
                if _f.get("ogrenci_id") == sid:
                    meb_ogr.setdefault(_sk, []).append(_f)
    except Exception:
        pass

    # ── Üst Risk Kartı ──
    if latest:
        lv = risk_level_for(latest.get("risk_score", 0))
        sources = latest.get("data_sources_used", [])
        src_html = "".join(f'<span class="eu-src">{s}</span>' for s in sources)
        st.markdown(f"""
        <div class="eu-card" style="border-left-color:{lv['color']}">
            <h4>{lv['icon']} {stu.get('ad','')} {stu.get('soyad','')}</h4>
            <div style="display:flex;gap:25px;align-items:center">
                <div>
                    <div class="score" style="color:{lv['color']}">{latest.get('risk_score',0)}</div>
                    <div class="meta">Risk / 100</div>
                </div>
                <div style="flex:1">
                    <div class="meta">
                        Sınıf: {stu.get('sinif','')}/{stu.get('sube','')} |
                        No: {stu.get('numara','')} |
                        <b style="color:{lv['color']}">{lv['label']}</b>
                    </div>
                    <div class="eu-bar"><div class="eu-fill" style="width:{latest.get('risk_score',0)}%;background:{lv['color']}"></div></div>
                    <div style="margin-top:4px">{src_html}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Risk Trend Sparkline ──
    if risk_hist and len(risk_hist) >= 2:
        _spark_scores = [r.get("risk_score", 0) for r in risk_hist[-12:]]
        _spark_dates = [r.get("calculated_at", "")[:10] for r in risk_hist[-12:]]
        _spark_max = max(_spark_scores) if _spark_scores else 100
        _spark_min = min(_spark_scores) if _spark_scores else 0
        _spark_range = max(_spark_max - _spark_min, 1)
        _spark_w = 300
        _spark_h = 50
        _spark_points = []
        for i, s in enumerate(_spark_scores):
            x = int(i / max(len(_spark_scores) - 1, 1) * (_spark_w - 20)) + 10
            y = int(_spark_h - 8 - ((s - _spark_min) / _spark_range) * (_spark_h - 16))
            _spark_points.append((x, y))
        _spark_line = " ".join(f"{x},{y}" for x, y in _spark_points)
        _spark_last = _spark_scores[-1]
        _spark_first = _spark_scores[0]
        _spark_delta = _spark_last - _spark_first
        _sp_clr = "#ef4444" if _spark_delta > 5 else "#22c55e" if _spark_delta < -5 else "#f59e0b"
        _sp_arrow = "↑" if _spark_delta > 5 else "↓" if _spark_delta < -5 else "→"
        _sp_dots = "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{_sp_clr}"/>' for x, y in _spark_points)
        st.markdown(f"""
        <div style="background:#0f172a;border-radius:10px;padding:10px 14px;margin:8px 0;
        border:1px solid {_sp_clr}30;display:flex;align-items:center;gap:14px;">
        <div>
            <div style="color:#94a3b8;font-size:.72rem;">Risk Trendi (Son {len(_spark_scores)} Analiz)</div>
            <svg width="{_spark_w}" height="{_spark_h}" viewBox="0 0 {_spark_w} {_spark_h}">
            <polyline points="{_spark_line}" fill="none" stroke="{_sp_clr}" stroke-width="2" stroke-linejoin="round"/>
            {_sp_dots}
            <line x1="0" y1="{int(_spark_h/2)}" x2="{_spark_w}" y2="{int(_spark_h/2)}" stroke="#334155" stroke-width="0.5" stroke-dasharray="4,4"/>
            </svg>
        </div>
        <div style="text-align:center;">
            <div style="font-size:1.5rem;font-weight:800;color:{_sp_clr};">{_sp_arrow} {_spark_delta:+.1f}</div>
            <div style="color:#64748b;font-size:.7rem;">{_spark_first:.0f} → {_spark_last:.0f}</div>
        </div>
        </div>""", unsafe_allow_html=True)

    # ── Radar Grafik + Gauge + Trend ──
    if latest:
        _rc1, _rc2 = st.columns(2)
        with _rc1:
            _radar_data = {
                "Not": latest.get("grade_risk", 0), "Devam.": latest.get("attendance_risk", 0),
                "Sınav": latest.get("exam_risk", 0), "Ödev": latest.get("homework_risk", 0),
                "Kaz.Borç": latest.get("outcome_debt_risk", 0), "Rehber.": latest.get("counseling_risk", 0),
                "Sağlık": latest.get("health_risk", 0), "Trend": latest.get("trend_risk", 0),
                "Davranış": latest.get("behavior_risk", 0), "Yab.Dil": latest.get("foreign_lang_risk", 0),
            }
            student_radar(_radar_data, f"{stu.get('ad','')} {stu.get('soyad','')}")
        with _rc2:
            risk_gauge(latest.get("risk_score", 0), f"{stu.get('ad','')} Risk Skoru")
            if risk_hist and len(risk_hist) >= 2:
                _t_dates = [r.get("calculated_at", "")[:10] for r in risk_hist[-12:]]
                _t_scores = [r.get("risk_score", 0) for r in risk_hist[-12:]]
                risk_trend_line(_t_dates, _t_scores, f"{stu.get('ad','')}")

    # ── 10 Bileşen Grid ──
    if latest:
        styled_section("📊 Risk Bileşenleri (10 Modül)")
        components = [
            ("📚 Not", "grade_risk", RISK_WEIGHTS["grade"]),
            ("📅 Devamsızlık", "attendance_risk", RISK_WEIGHTS["attendance"]),
            ("📝 Sınav", "exam_risk", RISK_WEIGHTS["exam"]),
            ("📋 Ödev", "homework_risk", RISK_WEIGHTS["homework"]),
            ("🎯 Kazanım Borcu", "outcome_debt_risk", RISK_WEIGHTS["outcome_debt"]),
            ("🧭 Rehberlik", "counseling_risk", RISK_WEIGHTS["counseling"]),
            ("🏥 Sağlık", "health_risk", RISK_WEIGHTS["health"]),
            ("📈 Trend", "trend_risk", RISK_WEIGHTS["trend"]),
            ("🔄 Davranış/KYT", "behavior_risk", RISK_WEIGHTS["behavior"]),
            ("🌍 Yabancı Dil", "foreign_lang_risk", RISK_WEIGHTS.get("foreign_lang", 0.09)),
        ]
        for label, key, weight in components:
            val = latest.get(key, 0)
            color = "#22c55e" if val < 30 else "#f59e0b" if val < 55 else "#f97316" if val < 75 else "#ef4444"
            st.markdown(
                f'<div class="eu-row"><span style="color:#cbd5e1">{label} <span style="color:#64748b;font-size:10px">(%{int(weight*100)})</span></span>'
                f'<span style="color:{color};font-weight:700">{val}</span></div>'
                f'<div class="eu-bar"><div class="eu-fill" style="width:{val}%;background:{color}"></div></div>',
                unsafe_allow_html=True,
            )

    # ── Detay Kolonları ──
    c1, c2 = st.columns(2)

    with c1:
        # Notlar
        st.markdown('<div class="eu-sec"><h5>📚 Not Durumu (Akademik Takip)</h5>', unsafe_allow_html=True)
        if grades:
            subj: dict[str, list] = {}
            for g in grades:
                subj.setdefault(g.get("ders", "?"), []).append(g.get("puan", 0))
            for s, scores in sorted(subj.items()):
                avg = sum(scores) / len(scores) if scores else 0
                c = "#22c55e" if avg >= 70 else "#f59e0b" if avg >= 50 else "#ef4444"
                st.markdown(f'<div class="eu-row"><span>{s}</span><span style="color:{c};font-weight:700">{avg:.0f}</span></div>', unsafe_allow_html=True)
        else:
            st.caption("Not verisi yok")
        st.markdown('</div>', unsafe_allow_html=True)

        # Sınav Sonuçları
        st.markdown('<div class="eu-sec"><h5>📝 Sınav Sonuçları (Ölçme & Değerlendirme)</h5>', unsafe_allow_html=True)
        if exams:
            for e in exams[-5:]:
                sc = e.get("score", 0)
                c = "#22c55e" if sc >= 70 else "#f59e0b" if sc >= 50 else "#ef4444"
                st.markdown(f'<div class="eu-row"><span style="color:#94a3b8">{e.get("graded_at","")[:10]}</span><span style="color:{c};font-weight:700">{sc:.0f}/100</span></div>', unsafe_allow_html=True)
        else:
            st.caption("Sınav verisi yok")
        st.markdown('</div>', unsafe_allow_html=True)

        # Ödev
        st.markdown('<div class="eu-sec"><h5>📋 Ödev Performansı</h5>', unsafe_allow_html=True)
        if hw_subs:
            teslim = sum(1 for h in hw_subs if h.get("durum") == "teslim_edildi")
            puanlar = [h.get("puan", 0) for h in hw_subs if h.get("puan")]
            avg_p = sum(puanlar) / len(puanlar) if puanlar else 0
            st.markdown(f'<div class="eu-row"><span>Teslim Edilen</span><span class="v">{teslim}/{len(hw_subs)}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="eu-row"><span>Ortalama Puan</span><span style="font-weight:700">{avg_p:.0f}</span></div>', unsafe_allow_html=True)
        else:
            st.caption("Ödev teslim verisi yok")
        st.markdown('</div>', unsafe_allow_html=True)

        # KYT
        st.markdown('<div class="eu-sec"><h5>📊 Kazanım Yoklama Testi (KYT)</h5>', unsafe_allow_html=True)
        if kyt:
            correct = sum(1 for k2 in kyt if k2.get("dogru_mu"))
            ratio = correct / len(kyt) * 100
            c = "#22c55e" if ratio >= 70 else "#f59e0b" if ratio >= 50 else "#ef4444"
            st.markdown(f'<div class="eu-row"><span>Toplam Soru</span><span>{len(kyt)}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="eu-row"><span>Doğru Oranı</span><span style="color:{c};font-weight:700">%{ratio:.0f}</span></div>', unsafe_allow_html=True)
        else:
            st.caption("KYT verisi yok")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        # Devamsızlık
        st.markdown('<div class="eu-sec"><h5>📅 Devamsızlık (Akademik Takip)</h5>', unsafe_allow_html=True)
        if attendance:
            ozurlu = sum(1 for a in attendance if a.get("turu") == "ozurlu")
            ozursuz = sum(1 for a in attendance if a.get("turu") == "ozursuz")
            st.markdown(
                f'<div style="font-size:12px;color:#cbd5e1">'
                f'Toplam: <b>{len(attendance)}</b> | '
                f'<span style="color:#ef4444">Özürsüz: {ozursuz}</span> | '
                f'<span style="color:#f59e0b">Özürlü: {ozurlu}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption("Devamsızlık yok")
        st.markdown('</div>', unsafe_allow_html=True)

        # Rehberlik
        st.markdown('<div class="eu-sec"><h5>🧭 Rehberlik (Vaka & Görüşme)</h5>', unsafe_allow_html=True)
        if vakalar:
            for v in vakalar:
                dur = v.get("durum", "?")
                risk = v.get("risk_seviyesi", "?")
                dc = "#ef4444" if risk == "ACİL" else "#f97316" if risk == "YUKSEK" else "#f59e0b" if risk == "ORTA" else "#22c55e"
                st.markdown(f'<div class="eu-row"><span>{v.get("vaka_basligi","Vaka")[:30]}</span><span style="color:{dc};font-weight:600">{dur} / {risk}</span></div>', unsafe_allow_html=True)
        if gorusmeler:
            st.markdown(f'<div class="eu-row"><span>Toplam Görüşme</span><span>{len(gorusmeler)}</span></div>', unsafe_allow_html=True)
            last = sorted(gorusmeler, key=lambda x: x.get("tarih", ""), reverse=True)[0]
            st.markdown(f'<div class="eu-row"><span>Son Görüşme</span><span>{last.get("tarih","")}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="eu-row"><span>Konu</span><span>{last.get("gorusme_konusu","")}</span></div>', unsafe_allow_html=True)
        if not vakalar and not gorusmeler:
            st.caption("Rehberlik kaydı yok")
        # MEB Dijital Formlar
        if meb_ogr:
            try:
                from models.meb_formlar import MEB_FORM_SCHEMAS
                st.markdown(f'<div class="eu-row"><span style="font-weight:700;">📄 MEB Formlar</span><span>{sum(len(v) for v in meb_ogr.values())} kayıt</span></div>', unsafe_allow_html=True)
                for _sk, _fms in meb_ogr.items():
                    _sch = next((s for s in MEB_FORM_SCHEMAS.values() if s["store_key"] == _sk), None)
                    _fn = _sch["title"] if _sch else _sk
                    _ic = _sch.get("icon", "📄") if _sch else "📄"
                    _clr = "#3b82f6"
                    if _sk in ("dehb_gozlem_formlari", "ozel_ogrenme_guclugu_formlari", "psikolojik_yonlendirme_formlari"):
                        _clr = "#ef4444"
                    elif _sk in ("disiplin_gorusme_formlari", "ev_ziyareti_formlari"):
                        _clr = "#f59e0b"
                    st.markdown(f'<div class="eu-row"><span>{_ic} {_fn}</span><span style="color:{_clr};font-weight:600">{len(_fms)}</span></div>', unsafe_allow_html=True)
            except Exception:
                pass
        st.markdown('</div>', unsafe_allow_html=True)

        # Sağlık
        st.markdown('<div class="eu-sec"><h5>🏥 Okul Sağlığı (Revir)</h5>', unsafe_allow_html=True)
        if saglik:
            st.markdown(f'<div class="eu-row"><span>Ziyaret Sayısı</span><span>{len(saglik)}</span></div>', unsafe_allow_html=True)
            takip = sum(1 for s3 in saglik if s3.get("takip_gerekiyor"))
            if takip:
                st.markdown(f'<div class="eu-row"><span style="color:#f59e0b">Takip Gereken</span><span style="color:#f59e0b;font-weight:700">{takip}</span></div>', unsafe_allow_html=True)
            last_s = sorted(saglik, key=lambda x: x.get("basvuru_tarihi", ""), reverse=True)[0]
            st.markdown(f'<div class="eu-row"><span>Son Şikayet</span><span>{last_s.get("sikayet_kategorisi","?")}</span></div>', unsafe_allow_html=True)
        else:
            st.caption("Sağlık kaydı yok")
        st.markdown('</div>', unsafe_allow_html=True)

        # Kazanım Borcu
        st.markdown('<div class="eu-sec"><h5>🎯 Kazanım Borçları</h5>', unsafe_allow_html=True)
        if borc:
            open_b = [b2 for b2 in borc if b2.get("durum") == "borc_var"]
            closed = len(borc) - len(open_b)
            st.markdown(f'<div class="eu-row"><span style="color:#ef4444">Açık Borç</span><span style="color:#ef4444;font-weight:700">{len(open_b)}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="eu-row"><span style="color:#22c55e">Kapatılan</span><span>{closed}</span></div>', unsafe_allow_html=True)
            for b3 in open_b[:3]:
                st.markdown(f'<div style="font-size:10px;color:#94a3b8;padding:2px 0">• {b3.get("ders","")} — {b3.get("kazanim_kodu","")}</div>', unsafe_allow_html=True)
        else:
            st.caption("Kazanım borcu yok")
        st.markdown('</div>', unsafe_allow_html=True)

        # Telafi
        st.markdown('<div class="eu-sec"><h5>🔄 Telafi Görevleri (Ölçme)</h5>', unsafe_allow_html=True)
        if telafi:
            comp = sum(1 for t2 in telafi if t2.get("status") == "completed")
            bands = {}
            for t3 in telafi:
                cb = t3.get("color_band", "?")
                bands[cb] = bands.get(cb, 0) + 1
            st.markdown(f'<div class="eu-row"><span>Toplam</span><span>{len(telafi)}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="eu-row"><span>Tamamlanan</span><span style="color:#22c55e">{comp}</span></div>', unsafe_allow_html=True)
            band_str = " | ".join(f'{k}: {v}' for k, v in bands.items())
            st.markdown(f'<div style="font-size:10px;color:#94a3b8">{band_str}</div>', unsafe_allow_html=True)
        else:
            st.caption("Telafi görevi yok")
        st.markdown('</div>', unsafe_allow_html=True)

        # Yabancı Dil Değerlendirmesi
        st.markdown('<div class="eu-sec"><h5>🌍 Yabancı Dil Değerlendirmesi</h5>', unsafe_allow_html=True)
        fl_perf = latest.get("foreign_lang_performance", {}) if latest else {}
        fl_risk_val = latest.get("foreign_lang_risk", 0) if latest else 0
        if fl_perf:
            # Quiz durumu
            if fl_perf.get("quiz_avg"):
                qc = "#22c55e" if fl_perf["quiz_avg"] >= 70 else "#f59e0b" if fl_perf["quiz_avg"] >= 50 else "#ef4444"
                st.markdown(f'<div class="eu-row"><span>Quiz Ort.</span>'
                            f'<span style="color:{qc};font-weight:700">{fl_perf["quiz_avg"]:.0f}</span></div>',
                            unsafe_allow_html=True)
                st.markdown(f'<div class="eu-row"><span>Quiz Sayısı</span>'
                            f'<span>{fl_perf.get("quiz_count", 0)}</span></div>',
                            unsafe_allow_html=True)
            # CEFR Seviye Tespit
            if fl_perf.get("placed_cefr"):
                below = fl_perf.get("is_below", False)
                cefr_clr = "#ef4444" if below else "#22c55e"
                st.markdown(f'<div class="eu-row"><span>CEFR Tespit</span>'
                            f'<span style="color:{cefr_clr};font-weight:700">{fl_perf["placed_cefr"]}</span></div>',
                            unsafe_allow_html=True)
                st.markdown(f'<div class="eu-row"><span>Hedef CEFR</span>'
                            f'<span>{fl_perf.get("target_cefr", "?")}</span></div>',
                            unsafe_allow_html=True)
            # Mock Exam
            if fl_perf.get("mock_achieved_cefr"):
                st.markdown(f'<div class="eu-row"><span>Mock Exam</span>'
                            f'<span style="color:#8b5cf6;font-weight:700">'
                            f'{fl_perf["mock_achieved_cefr"]} (%{fl_perf.get("mock_percentage", 0):.0f})</span></div>',
                            unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:10px;color:#94a3b8;padding:2px 0">'
                            f'L:{fl_perf.get("mock_listening", 0):.0f} '
                            f'R:{fl_perf.get("mock_reading", 0):.0f} '
                            f'W:{fl_perf.get("mock_writing", 0):.0f} '
                            f'S:{fl_perf.get("mock_speaking", 0):.0f}</div>',
                            unsafe_allow_html=True)
            # Durum tespiti + tavsiye
            _fl_color = "#22c55e" if fl_risk_val < 30 else "#f59e0b" if fl_risk_val < 55 else "#f97316" if fl_risk_val < 75 else "#ef4444"
            _fl_durum = "İyi" if fl_risk_val < 30 else "Gelişmeli" if fl_risk_val < 55 else "Riskli" if fl_risk_val < 75 else "Kritik"
            st.markdown(f'<div style="margin-top:6px;padding:6px 8px;background:{_fl_color}10;border-left:3px solid {_fl_color};border-radius:4px;">'
                        f'<span style="color:{_fl_color};font-weight:700;font-size:.82rem;">Durum: {_fl_durum} (Risk: {fl_risk_val:.0f})</span></div>',
                        unsafe_allow_html=True)
            _fl_tvs = []
            if fl_perf.get("is_below"):
                _fl_tvs.append("CEFR hedef altı — seviye programı")
            if fl_perf.get("quiz_avg", 100) < 50:
                _fl_tvs.append("Quiz ort. düşük — pekiştirme quizi")
            if fl_perf.get("mock_percentage", 100) < 50:
                _fl_tvs.append("Mock düşük — beceri çalışması")
            if not fl_perf.get("mock_achieved_cefr"):
                _fl_tvs.append("Mock Exam yapılmalı")
            if not fl_perf.get("placed_cefr"):
                _fl_tvs.append("CEFR tespiti yapılmalı")
            if _fl_tvs:
                st.markdown('<div style="font-size:10px;color:#a5b4fc;margin-top:4px;">'
                            + " · ".join(_fl_tvs) + '</div>', unsafe_allow_html=True)
        else:
            st.caption("YD verisi yok — Quiz/CEFR uygulanmalı")
        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ AI MEB FORM DEĞERLENDİRME ═══
    if meb_ogr:
        try:
            from views.meb_formlar import render_ai_ogrenci_panel
            render_ai_ogrenci_panel(None, sid, f"{stu.get('ad','')} {stu.get('soyad','')}")
        except Exception:
            pass

    # ═══ AKILLI YORUM & AKSIYON MOTORU ═══
    if latest:
        styled_section("🧠 Akıllı Yorum & Aksiyon Planı")

        score = latest.get("risk_score", 0)
        level = latest.get("risk_level", "LOW")
        gr = latest.get("grade_risk", 0)
        att = latest.get("attendance_risk", 0)
        ex = latest.get("exam_risk", 0)
        hw = latest.get("homework_risk", 0)
        ob = latest.get("outcome_debt_risk", 0)
        co = latest.get("counseling_risk", 0)
        he = latest.get("health_risk", 0)
        tr = latest.get("trend_risk", 0)
        bh = latest.get("behavior_risk", 0)
        fl = latest.get("foreign_lang_risk", 0)

        # 1. Genel durum yorumu
        if level == "CRITICAL":
            yorum = "Bu öğrenci ACİL müdahale gerektiriyor. Birden fazla alanda ciddi risk var."
            y_clr, y_icon = "#ef4444", "🚨"
        elif level == "HIGH":
            yorum = "Yüksek risk — yakın takip ve müdahale planı gerekli."
            y_clr, y_icon = "#f97316", "🟠"
        elif level == "MEDIUM":
            yorum = "Orta risk — bazı alanlarda dikkat gerektiriyor, önleyici tedbirler alınmalı."
            y_clr, y_icon = "#f59e0b", "🟡"
        else:
            yorum = "Düşük risk — genel durum iyi. Koruyucu takibe devam."
            y_clr, y_icon = "#22c55e", "🟢"

        st.markdown(f"""<div style="background:linear-gradient(135deg,#0f172a,#1e293b);
        border-radius:14px;padding:16px;border-left:4px solid {y_clr};margin:8px 0;">
        <div style="font-size:1rem;font-weight:700;color:{y_clr};">{y_icon} {yorum}</div>
        <div style="font-size:.8rem;color:#94a3b8;margin-top:4px;">
        Risk Skoru: {score:.0f}/100 | Seviye: {level}</div>
        </div>""", unsafe_allow_html=True)

        # 2. Faktor bazli yorum — en yuksek 3 risk faktoru
        faktorler = [
            ("Not Riski", gr, "Ders başarısı düşük — etüt + bireysel destek", "📝"),
            ("Devamsızlık", att, "Devamsızlık yüksek — veli görüşmesi + takip", "📋"),
            ("Sınav Riski", ex, "Sınav performansı düşük — deneme sınavı + tekrar", "📊"),
            ("Ödev Riski", hw, "Ödev teslim oranı düşük — günlük takip + hatırlatma", "📓"),
            ("Kazanım Borcu", ob, "Eksik kazanımlar var — telafi programı", "🎯"),
            ("Rehberlik", co, "Rehberlik vakası var — görüşme takibi", "🧭"),
            ("Sağlık", he, "Sağlık takibi gereken durum — revir koordinasyonu", "🏥"),
            ("Trend", tr, "Performans düşüş trendi — erken müdahale", "📉"),
            ("Davranış", bh, "KYT/telafi performansı düşük — motivasyon desteği", "⚡"),
            ("Yabancı Dil", fl, "Yabancı dil quiz/CEFR performansı düşük — pekiştirme gerekli", "🌍"),
        ]
        en_yuksek = sorted(faktorler, key=lambda x: -x[1])[:3]

        st.markdown("**En Kritik 3 Risk Faktörü:**")
        for label, val, action, icon in en_yuksek:
            if val > 0:
                f_clr = "#ef4444" if val >= 60 else ("#f59e0b" if val >= 30 else "#22c55e")
                st.markdown(f"""<div style="display:flex;gap:10px;align-items:center;padding:6px 0;
                border-bottom:1px solid #1e293b;">
                <span style="font-size:1.1rem;">{icon}</span>
                <div style="flex:1;">
                <div style="color:#e2e8f0;font-weight:600;font-size:.85rem;">{label}: <span style="color:{f_clr}">%{val:.0f}</span></div>
                <div style="color:#94a3b8;font-size:.78rem;">{action}</div>
                </div>
                <div style="width:80px;background:#1e293b;border-radius:4px;height:8px;overflow:hidden;">
                <div style="width:{min(100,val)}%;height:100%;background:{f_clr};border-radius:4px;"></div></div>
                </div>""", unsafe_allow_html=True)

        # 3. Kisisel aksiyon plani
        st.markdown("**📋 Kişisel Aksiyon Planı:**")
        actions = []
        if gr >= 40:
            actions.append(("ACİL", "📝", "Düşük notlu derslere haftalık etüt planı oluştur",
                            "Akademik Takip > Etüt sekmesinden"))
        if att >= 30:
            actions.append(("ACİL", "📋", "Velisiyle devamsızlık görüşmesi yap",
                            "KOİ > İletişim > Mesaj Gönder"))
        if hw >= 30:
            actions.append(("YÜKSEK", "📓", "Ödev takibini sıkılaştır — günlük kontrol",
                            "Akademik Takip > Ödev Takip"))
        if ob >= 30:
            actions.append(("YÜKSEK", "🎯", "Kazanım borçları için telafi programı başlat",
                            "Ölçme & Değerlendirme > Telafi"))
        if co >= 30:
            actions.append(("ORTA", "🧭", "Rehberlik görüşmesi planla",
                            "Rehberlik > Görüşme Kayıtları"))
        if he >= 30:
            actions.append(("ORTA", "🏥", "Sağlık takibi — revir ile koordine ol",
                            "Okul Sağlığı > Revir Ziyareti"))
        if not actions:
            actions.append(("DÜŞÜK", "✅", "Koruyucu takibe devam — ayda 1 kontrol",
                            "Erken Uyarı > 360° Profil"))

        pri_colors = {"ACİL": "#ef4444", "YÜKSEK": "#f97316", "ORTA": "#f59e0b", "DÜŞÜK": "#22c55e"}
        for pri, icon, gorev, modul in actions:
            clr = pri_colors.get(pri, "#64748b")
            st.markdown(f"""<div style="display:flex;gap:8px;align-items:center;padding:6px 0;
            border-bottom:1px solid #1e293b;">
            <span style="font-size:1rem;">{icon}</span>
            <div style="flex:1;">
            <div style="color:#e2e8f0;font-weight:600;font-size:.85rem;">{gorev}</div>
            <div style="color:#475569;font-size:.72rem;">{modul}</div>
            </div>
            <span style="font-size:.6rem;color:{clr};font-weight:700;background:{clr}15;
            padding:2px 8px;border-radius:4px;">{pri}</span>
            </div>""", unsafe_allow_html=True)

    # AI Öneriler (rule-based)
    if latest and latest.get("recommendations"):
        styled_section("💡 🤖 Sistem Önerileri")
        for rec in latest["recommendations"]:
            st.markdown(f'<div class="eu-rec">{rec}</div>', unsafe_allow_html=True)

    # ── AI Doğal Dil 360° Özet ──
    if latest:
        st.markdown("---")
        styled_section("🧠 AI 360° Profil Analizi (GPT-4o)")
        if st.button("🤖 AI ile Analiz Et", key="ai_360_btn", type="primary"):
            with st.spinner("GPT-4o-mini profil analizi yapıyor..."):
                summary_text = AIProfileSummarizer.generate_summary(
                    f"{stu.get('ad','')} {stu.get('soyad','')}",
                    latest,
                )
            if summary_text:
                st.markdown(f"""<div class="eu-sec" style="border:1px solid rgba(139,92,246,.3)">
                    <h5>🧠 AI Profil Özeti</h5>
                    <div style="font-size:12px;color:#e2e8f0;line-height:1.7;white-space:pre-wrap">{summary_text}</div>
                </div>""", unsafe_allow_html=True)
            else:
                styled_info_banner("AI analizi yapılamadı. OPENAI_API_KEY kontrol edin.", "warning")

    # ── AI Risk Tahmini ──
    if risk_hist:
        styled_section("🔮 AI 30 Gün Risk Tahmini")
        if st.button("🔮 Tahmin Oluştur", key="ai_pred_btn"):
            with st.spinner("Trend analizi + AI tahmin yapılıyor..."):
                prediction = PredictiveRiskEngine.predict_risk(
                    sid, f"{stu.get('ad','')} {stu.get('soyad','')}",
                    risk_hist, latest,
                )
            trend_icon = {"rising": "📈🔴", "falling": "📉🟢", "stable": "➡️🟡"}.get(prediction["trend"], "➡️")
            st.markdown(f"""<div class="eu-card" style="border-left-color:#8b5cf6">
                <h4>🔮 30 Günlük Tahmin — {prediction['student_name']}</h4>
                <div style="display:flex;gap:20px;margin-top:8px">
                    <div><div class="score" style="color:#60a5fa">{prediction['current_score']}</div><div class="meta">Şu An</div></div>
                    <div style="font-size:24px;align-self:center">→</div>
                    <div><div class="score" style="color:#a78bfa">{prediction['predicted_score']}</div><div class="meta">Tahmin</div></div>
                </div>
                <div class="meta" style="margin-top:8px">
                    Trend: {trend_icon} {prediction['trend'].upper()} | Güven: %{prediction['confidence']*100:.0f} | Eğim: {prediction['slope']}
                </div>
            </div>""", unsafe_allow_html=True)
            if prediction.get("ai_analysis"):
                st.markdown(f"""<div class="eu-sec" style="border:1px solid rgba(139,92,246,.2)">
                    <h5>🧠 AI Tahmin Analizi</h5>
                    <div style="font-size:12px;color:#e2e8f0;line-height:1.7;white-space:pre-wrap">{prediction['ai_analysis']}</div>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 3: ERKEN UYARI
# ═══════════════════════════════════════════════════════════════
def _tab_alerts(store):
    styled_section("🔴 Erken Uyarı Merkezi")
    alerts = store.load_alerts()
    active = [a for a in alerts if not a.get("is_resolved")]
    resolved = [a for a in alerts if a.get("is_resolved")]

    styled_stat_row([
        ("Aktif", str(len(active)), "#ef4444", "🔔"),
        ("Çözülen", str(len(resolved)), "#22c55e", "✅"),
        ("Kritik", str(sum(1 for a in active if a.get("severity") == "CRITICAL")), "#ef4444", "🚨"),
        ("Toplam", str(len(alerts)), "#6366f1", "📊"),
    ])

    if not active:
        styled_info_banner("Aktif uyarı yok. Sistem temiz! ✅", "info")
        return

    sev_f = st.selectbox("Filtre", ["Tümü", "CRITICAL", "HIGH", "MEDIUM", "LOW"])

    mod_f = st.selectbox("Kaynak Modül", ["Tümü"] + list(set(a.get("source_module", "") for a in active if a.get("source_module"))))


    filtered = active
    if sev_f != "Tümü":
        filtered = [a for a in filtered if a.get("severity") == sev_f]
    if mod_f != "Tümü":
        filtered = [a for a in filtered if a.get("source_module") == mod_f]

    for a in sorted(filtered, key=lambda x: x.get("created_at", ""), reverse=True):
        sev = a.get("severity", "MEDIUM")
        cls = "critical" if sev == "CRITICAL" else "high" if sev == "HIGH" else ""
        icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(sev, "🟢")
        src = a.get("source_module", "")
        st.markdown(f"""
        <div class="eu-alert {cls}">
            <div class="t">{icon} {a.get('title','')}</div>
            <div class="m">{a.get('message','')}</div>
            <div style="margin-top:4px"><span class="eu-src">{src}</span>
            <span style="font-size:10px;color:#64748b;margin-left:8px">{a.get('created_at','')[:16]}</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button("✅ Çözüldü", key=f"res_{a.get('id','')}"):
            store.resolve_alert(a.get("id", ""))
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# TAB 4: RİSK SKORU
# ═══════════════════════════════════════════════════════════════
def _tab_risk(store, calc):
    styled_section("📈 Risk Skoru Tablosu")
    risks = store.get_latest_risks()
    if not risks:
        styled_info_banner("Risk verisi yok. Dashboard'dan analiz çalıştırın.", "warning")
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        sinif_f = st.selectbox("Sınıf", ["Tümü"] + sorted(set(str(r.get("sinif","")) for r in risks if r.get("sinif"))))

    with c2:
        sube_f = st.selectbox("Şube", ["Tümü"] + sorted(set(r.get("sube","") for r in risks if r.get("sube"))))

    with c3:
        risk_f = st.selectbox("Risk", ["Tümü", "CRITICAL", "HIGH", "MEDIUM", "LOW"])


    filtered = risks
    if sinif_f != "Tümü":
        filtered = [r for r in filtered if str(r.get("sinif","")) == sinif_f]
    if sube_f != "Tümü":
        filtered = [r for r in filtered if r.get("sube") == sube_f]
    if risk_f != "Tümü":
        filtered = [r for r in filtered if r.get("risk_level") == risk_f]

    filtered = sorted(filtered, key=lambda x: x.get("risk_score", 0), reverse=True)
    st.markdown(f"**{len(filtered)}** öğrenci")

    for r in filtered:
        lv = risk_level_for(r.get("risk_score", 0))
        st.markdown(f"""
        <div class="eu-card" style="border-left-color:{lv['color']};padding:10px 14px">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                    <b style="color:#111827;font-size:12px">{lv['icon']} {r.get('student_name','')}</b>
                    <span style="color:#64748b;font-size:10px;margin-left:6px">{r.get('sinif','')}/{r.get('sube','')}</span>
                </div>
                <div class="score" style="color:{lv['color']};font-size:20px">{r.get('risk_score',0)}</div>
            </div>
            <div style="display:flex;gap:12px;margin-top:4px;font-size:10px;color:#94a3b8;flex-wrap:wrap">
                <span>📚{r.get('grade_avg',0)}</span>
                <span>📅{r.get('attendance_total',0)}g/{r.get('attendance_ozursuz',0)}öz</span>
                <span>📝{r.get('exam_avg',0)}</span>
                <span>📋{r.get('homework_submitted',0)}/{r.get('homework_total',0)}öd</span>
                <span>🎯{r.get('outcome_debts',0)}borç</span>
                <span>🧭{r.get('counseling_open_cases',0)}vaka</span>
                <span>🏥{r.get('health_visits',0)}rev</span>
            </div>
            <div class="eu-bar" style="margin-top:4px"><div class="eu-fill" style="width:{r.get('risk_score',0)}%;background:{lv['color']}"></div></div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 5: KAZANIM HARİTASI
# ═══════════════════════════════════════════════════════════════
def _tab_kazanim(store, loader):
    styled_section("🗺️ Kazanım Hakimiyet Haritası")

    students = loader.load_students()
    aktif = [s for s in students if s.get("durum") == "aktif"]
    if not aktif:
        styled_info_banner("Aktif öğrenci bulunamadı.", "warning")
        return

    opts = {f"{s.get('ad','')} {s.get('soyad','')} — {s.get('sinif','')}/{s.get('sube','')}": s for s in aktif}
    selected = st.selectbox("Öğrenci Seç", [""] + list(opts.keys()), key="kaz_stu")
    if not selected:
        return

    stu = opts[selected]
    sid = stu.get("id", "")

    # KYT cevapları — ders bazlı kazanım performansı
    kyt = [k for k in loader.load_kyt_answers() if k.get("student_id") == sid]
    borc = [b for b in loader.load_kazanim_borclari() if b.get("student_id") == sid]
    exams = [e for e in loader.load_exam_results() if e.get("student_id") == sid]

    if kyt:
        styled_section("📊 KYT Kazanım Bazlı Performans")
        ders_perf: dict[str, dict] = {}
        for k2 in kyt:
            ders = k2.get("ders", "?")
            if ders not in ders_perf:
                ders_perf[ders] = {"total": 0, "correct": 0}
            ders_perf[ders]["total"] += 1
            if k2.get("dogru_mu"):
                ders_perf[ders]["correct"] += 1

        for ders, data in sorted(ders_perf.items()):
            ratio = data["correct"] / data["total"] * 100 if data["total"] > 0 else 0
            color = "#22c55e" if ratio >= 70 else "#f59e0b" if ratio >= 50 else "#ef4444"
            st.markdown(f"""
            <div style="margin-bottom:5px">
                <div class="eu-row"><span>{ders}</span>
                <span style="color:{color};font-weight:700">{ratio:.0f}% ({data['correct']}/{data['total']})</span></div>
                <div class="eu-bar"><div class="eu-fill" style="width:{ratio}%;background:{color}"></div></div>
            </div>""", unsafe_allow_html=True)

    if borc:
        styled_section("🎯 Kazanım Borçları")
        open_b = [b2 for b2 in borc if b2.get("durum") == "borc_var"]
        for b3 in open_b:
            st.markdown(
                f'<div class="eu-rec" style="border-left-color:#ef4444">'
                f'<b>{b3.get("ders","")}</b> — {b3.get("kazanim_kodu","")}: {b3.get("kazanim_metni","")[:60]}'
                f'<br><span style="color:#94a3b8;font-size:10px">Neden: {b3.get("borc_nedeni","")}</span></div>',
                unsafe_allow_html=True,
            )

    if exams:
        # outcome_breakdown
        outcomes: dict[str, list] = {}
        for e in exams:
            ob = e.get("outcome_breakdown", {})
            if isinstance(ob, dict):
                for oid, val in ob.items():
                    score = val.get("score", val) if isinstance(val, dict) else val
                    try:
                        outcomes.setdefault(oid, []).append(float(score))
                    except (ValueError, TypeError):
                        pass
        if outcomes:
            styled_section("📝 Sınav Kazanım Performansı")
            for oid, scores in sorted(outcomes.items()):
                avg = sum(scores) / len(scores) * 100
                color = "#22c55e" if avg >= 70 else "#f59e0b" if avg >= 50 else "#ef4444"
                st.markdown(f"""
                <div style="margin-bottom:3px">
                    <div class="eu-row"><span style="font-size:10px">{oid[:35]}</span>
                    <span style="color:{color};font-weight:700;font-size:11px">{avg:.0f}%</span></div>
                    <div class="eu-bar"><div class="eu-fill" style="width:{avg}%;background:{color}"></div></div>
                </div>""", unsafe_allow_html=True)

    if not kyt and not borc and not exams:
        styled_info_banner("Kazanım bazlı veri henüz oluşmadı.", "info")


# ═══════════════════════════════════════════════════════════════
# TAB 6: VELİ RAPORU
# ═══════════════════════════════════════════════════════════════
def _tab_veli(store, loader):
    styled_section("👨‍👩‍👧 Veli Rapor Kartı")

    students = loader.load_students()
    aktif = [s for s in students if s.get("durum") == "aktif"]
    if not aktif:
        return

    opts = {f"{s.get('ad','')} {s.get('soyad','')} — {s.get('sinif','')}/{s.get('sube','')}": s for s in aktif}
    selected = st.selectbox("Öğrenci Seç", [""] + list(opts.keys()), key="veli_stu")
    if not selected:
        return

    stu = opts[selected]
    sid = stu.get("id", "")
    latest = None
    hist = store.get_student_risk_history(sid)
    if hist:
        latest = hist[-1]

    grades = [g for g in loader.load_grades() if g.get("student_id") == sid]
    attendance = [a for a in loader.load_attendance() if a.get("student_id") == sid]

    st.markdown(f"### 📋 Haftalık Veli Bilgilendirme Raporu")
    st.markdown(f"**Öğrenci:** {stu.get('ad','')} {stu.get('soyad','')} | **Sınıf:** {stu.get('sinif','')}/{stu.get('sube','')} | **Tarih:** {datetime.now().strftime('%d.%m.%Y')}")
    st.markdown(f"**Veli:** {stu.get('veli_adi','')} | **Tel:** {stu.get('veli_telefon','')}")
    st.markdown("---")

    if grades:
        subj_avgs: dict[str, list] = {}
        for g in grades:
            subj_avgs.setdefault(g.get("ders", ""), []).append(g.get("puan", 0))
        st.markdown("**📚 Ders Durumu:**")
        for subj, scores in sorted(subj_avgs.items()):
            avg = sum(scores) / len(scores) if scores else 0
            emoji = "🟢" if avg >= 70 else "🟡" if avg >= 50 else "🔴"
            st.markdown(f"- {emoji} **{subj}**: Ortalama **{avg:.0f}**")

    ozursuz = sum(1 for a in attendance if a.get("turu") == "ozursuz")
    st.markdown(f"**📅 Devamsızlık:** Toplam **{len(attendance)}** gün | Özürsüz: **{ozursuz}**")
    if ozursuz >= 5:
        st.error(f"⚠️ Özürsüz devamsızlık kritik seviyede!")

    if latest:
        lv = risk_level_for(latest.get("risk_score", 0))
        st.markdown(f"**🎯 Genel Değerlendirme:** {lv['icon']} {lv['label']} ({latest.get('risk_score',0)}/100)")
        if latest.get("recommendations"):
            st.markdown("**🤖 Öneriler:**")
            for rec in latest["recommendations"]:
                st.markdown(f"- {rec}")

        # ── AI Veli Raporu Üretimi ──
        st.markdown("---")
        styled_section("🤖 AI Veli Bilgilendirme Mektubu (GPT-4o)")
        period = st.text_input("Dönem", value=datetime.now().strftime("%B %Y"), key="veli_period")
        if st.button("✉️ AI ile Veli Mektubu Oluştur", key="ai_veli_btn", type="primary"):
            with st.spinner("GPT-4o-mini veli mektubu hazırlıyor..."):
                letter = AIParentReportGenerator.generate_report(
                    f"{stu.get('ad','')} {stu.get('soyad','')}",
                    latest, period,
                )
            if letter and not letter.startswith("[AI Hata"):
                st.markdown(f"""<div style="background:#fff;color:#1a1a2e;border-radius:12px;padding:24px;
                    font-family:'Segoe UI',sans-serif;line-height:1.8;font-size:13px;
                    border:1px solid #e2e8f0;white-space:pre-wrap">{letter}</div>""",
                    unsafe_allow_html=True,
                )
                st.download_button(
                    "📥 Mektubu İndir (TXT)", letter,
                    file_name=f"veli_rapor_{stu.get('ad','')}_{stu.get('soyad','')}.txt",
                    mime="text/plain",
                )
            else:
                styled_info_banner("AI raporu oluşturulamadı. OPENAI_API_KEY kontrol edin.", "warning")


# ═══════════════════════════════════════════════════════════════
# TAB 7: REHBERLİK PANELİ
# ═══════════════════════════════════════════════════════════════
def _tab_rehberlik(store, loader):
    styled_section("🧭 Rehberlik Entegre Paneli")

    risks = store.get_latest_risks()
    interventions = store.load_interventions()
    vakalar = loader.load_rehberlik_vakalar()
    gorusmeler = loader.load_rehberlik_gorusmeler()

    critical = [r for r in risks if r.get("risk_level") == "CRITICAL"]
    high = [r for r in risks if r.get("risk_level") == "HIGH"]
    open_cases = [v for v in vakalar if v.get("durum") in ("ACIK", "TAKIPTE")]

    # MEB form istatistikleri
    try:
        _meb_risk_eu = loader.get_meb_risk_factors()
        _meb_toplam = _meb_risk_eu.get("toplam_kayit", 0)
        _meb_acil = _meb_risk_eu.get("risk", {}).get("acil_mudahale", 0)
    except Exception:
        _meb_toplam, _meb_acil = 0, 0

    styled_stat_row([
        ("Kritik Öğrenci", str(len(critical)), "#ef4444", "🔴"),
        ("Yüksek Risk", str(len(high)), "#f97316", "🟠"),
        ("Açık Vaka", str(len(open_cases)), "#e11d48", "📋"),
        ("Toplam Görüşme", str(len(gorusmeler)), "#8b5cf6", "💬"),
    ])
    styled_stat_row([
        ("MEB Form Kayıt", str(_meb_toplam), "#3b82f6", "📄"),
        ("Acil Müdahale", str(_meb_acil), "#ef4444" if _meb_acil > 0 else "#22c55e", "🚨"),
    ])

    # Riskli öğrenciler + rehberlik durumu
    if critical or high:
        styled_section("🚨 Acil Müdahale Listesi")
        for r in sorted(critical + high, key=lambda x: x.get("risk_score", 0), reverse=True):
            lv = risk_level_for(r.get("risk_score", 0))
            co_info = ""
            if r.get("counseling_open_cases", 0) > 0:
                co_info = f' | 🧭 {r.get("counseling_open_cases")} açık vaka ({r.get("counseling_risk_level","")})'
            recs = r.get("recommendations", [])[:2]
            rec_html = "".join(f'<div class="eu-rec">{rc}</div>' for rc in recs)
            st.markdown(f"""
            <div class="eu-card" style="border-left-color:{lv['color']}">
                <h4>{lv['icon']} {r.get('student_name','')} — {r.get('sinif','')}/{r.get('sube','')}</h4>
                <div class="meta">Risk: <b style="color:{lv['color']}">{r.get('risk_score',0)}</b> |
                Not: {r.get('grade_avg',0)} | Devam: {r.get('attendance_total',0)}g{co_info}</div>
                {rec_html}
            </div>""", unsafe_allow_html=True)

    # ── AI Müdahale Planlayıcı ──
    if critical or high:
        st.markdown("---")
        styled_section("🤖 AI Müdahale Planlayıcı (GPT-4o)")
        ai_target_opts = {
            f"{r.get('student_name','')} — Risk: {r.get('risk_score',0)}": r
            for r in sorted(critical + high, key=lambda x: x.get("risk_score", 0), reverse=True)
        }
        ai_target = st.selectbox("Öğrenci Seç", [""] + list(ai_target_opts.keys()), key="ai_intv_stu")
        if ai_target and st.button("🤖 AI Müdahale Planı Oluştur", key="ai_intv_btn", type="primary"):
            target_rec = ai_target_opts[ai_target]
            with st.spinner("GPT-4o-mini müdahale planı hazırlıyor..."):
                plan = AIInterventionPlanner.plan_intervention(
                    target_rec.get("student_name", ""), target_rec,
                )
            priority_colors = {"ACİL": "#ef4444", "YÜKSEK": "#f97316", "ORTA": "#f59e0b", "DÜŞÜK": "#22c55e"}
            pc = priority_colors.get(plan["priority"], "#6366f1")
            st.markdown(f"""<div class="eu-card" style="border-left-color:{pc}">
                <h4>📋 AI Müdahale Planı — {plan['student_name']}</h4>
                <div class="meta">Öncelik: <b style="color:{pc}">{plan['priority']}</b> | Risk: {plan['risk_score']:.1f}</div>
                <div style="margin-top:8px">
                    <b style="color:#60a5fa;font-size:11px">Stratejiler:</b><br>
                    {''.join(f'<span class="eu-module-badge" style="background:rgba(59,130,246,.12);color:#60a5fa">{s}</span>' for s in plan['strategies'])}
                </div>
                <div style="margin-top:6px">
                    <b style="color:#60a5fa;font-size:11px">Paydaşlar:</b><br>
                    {''.join(f'<span class="eu-module-badge" style="background:rgba(34,197,94,.12);color:#22c55e">{s}</span>' for s in plan['stakeholders'])}
                </div>
            </div>""", unsafe_allow_html=True)
            if plan.get("ai_plan_text") and not plan["ai_plan_text"].startswith("[AI Hata"):
                st.markdown(f"""<div class="eu-sec" style="border:1px solid rgba(139,92,246,.3)">
                    <h5>🧠 Detaylı AI Müdahale Planı</h5>
                    <div style="font-size:12px;color:#e2e8f0;line-height:1.8;white-space:pre-wrap">{plan['ai_plan_text']}</div>
                </div>""", unsafe_allow_html=True)

    # Yeni müdahale
    st.markdown("---")
    styled_section("📋 Yeni Müdahale Planı")
    with st.form("new_intv"):
        c1, c2 = st.columns(2)
        with c1:
            target = st.text_input("Öğrenci Adı")

            plan_type = st.selectbox("Müdahale Türü", ["telafi", "etut", "veli_gorusme", "rehberlik", "ozel_ders", "destek_programi"])

        with c2:
            assigned = st.text_input("Sorumlu")

            start = st.date_input("Başlangıç")

        desc = st.text_area("Açıklama")

        if st.form_submit_button("Oluştur", type="primary"):
            store.save_intervention(Intervention(
                student_name=target, plan_type=plan_type,
                description=desc, assigned_to=assigned,
                start_date=start.strftime("%Y-%m-%d"),
            ))
            st.success("Müdahale planı oluşturuldu!")
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# TAB 8: KOHORT ANALİZİ
# ═══════════════════════════════════════════════════════════════
def _tab_kohort(store, loader):
    styled_section("📉 Kohort — Sınıf/Şube Karşılaştırma")

    risks = store.get_latest_risks()
    if not risks:
        styled_info_banner("Risk verisi yok. Dashboard'dan analiz çalıştırın.", "warning")
        return

    groups: dict[str, list] = {}
    for r in risks:
        key = f"{r.get('sinif','?')}/{r.get('sube','?')}"
        groups.setdefault(key, []).append(r)

    import pandas as pd
    rows = []
    for key, members in sorted(groups.items()):
        n = len(members)
        rows.append({
            "Sınıf/Şube": key,
            "Öğrenci": n,
            "Ort. Risk": round(sum(m.get("risk_score", 0) for m in members) / n, 1),
            "Ort. Not": round(sum(m.get("grade_avg", 0) for m in members) / n, 1),
            "Ort. Devam": round(sum(m.get("attendance_total", 0) for m in members) / n, 1),
            "Ort. Sınav": round(sum(m.get("exam_avg", 0) for m in members) / n, 1),
            "Ödev Teslim%": round(sum(m.get("homework_submitted", 0) for m in members) / max(1, sum(m.get("homework_total", 1) for m in members)) * 100, 0),
            "Kritik": sum(1 for m in members if m.get("risk_level") == "CRITICAL"),
            "Yüksek": sum(1 for m in members if m.get("risk_level") == "HIGH"),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return

    st.dataframe(df.sort_values("Ort. Risk", ascending=False), use_container_width=True, hide_index=True)

    worst = df.loc[df["Ort. Risk"].idxmax()]
    best = df.loc[df["Ort. Risk"].idxmin()]
    c1, c2 = st.columns(2)
    with c1:
        st.error(f"🔴 En Riskli: **{worst['Sınıf/Şube']}** — Risk: {worst['Ort. Risk']}")
    with c2:
        st.success(f"🟢 En İyi: **{best['Sınıf/Şube']}** — Risk: {best['Ort. Risk']}")

    st.markdown("---")
    st.bar_chart(df.set_index("Sınıf/Şube")[["Ort. Risk", "Ort. Not", "Ort. Sınav"]])

    # ── Anomali Tespiti (İstatistiksel + AI) ──
    styled_section("🔍 Anomali Tespiti")
    all_avgs = [row["Ort. Risk"] for _, row in df.iterrows()]
    school_avg = sum(all_avgs) / len(all_avgs) if all_avgs else 0
    for _, row in df.iterrows():
        diff = row["Ort. Risk"] - school_avg
        if abs(diff) > 10:
            d = "üstünde" if diff > 0 else "altında"
            e = "🔺" if diff > 0 else "🔽"
            st.markdown(f"- {e} **{row['Sınıf/Şube']}** okul ortalamasının **{abs(diff):.0f} puan {d}**")

    # Öğrenci bazlı anomali
    st.markdown("---")
    styled_section("🔬 AI Öğrenci Anomali Analizi")
    anomalies = AnomalyDetector.detect_anomalies(risks)
    if anomalies:
        st.markdown(f"**{len(anomalies)}** öğrencide anomali tespit edildi (Z-score ≥ 1.8)")
        for a in anomalies[:8]:
            z_color = "#ef4444" if a["anomaly_type"] == "high" else "#22c55e"
            z_icon = "🔺" if a["anomaly_type"] == "high" else "🔽"
            comp_html = " ".join(
                f'<span class="eu-src" style="background:rgba(239,68,68,.15);color:#ef4444">{k.replace("_risk","")}: {v}</span>'
                for k, v in a["components"].items()
            )
            st.markdown(f"""<div class="eu-alert {'critical' if a['z_score'] > 2.5 else ''}">
                <div class="t">{z_icon} {a['student_name']} — {a['sinif']}/{a['sube']}</div>
                <div class="m">Risk: <b style="color:{z_color}">{a['risk_score']}</b> |
                Z-score: <b style="color:{z_color}">{a['z_score']}</b> |
                Ortalama: {a['mean']} ± {a['std']}</div>
                <div style="margin-top:4px">{comp_html}</div>
            </div>""", unsafe_allow_html=True)

        if st.button("🧠 AI Anomali Yorumu", key="ai_anomaly_btn"):
            with st.spinner("GPT-4o-mini anomali yorumluyor..."):
                analysis = AnomalyDetector.get_ai_anomaly_analysis(anomalies)
            st.markdown(f"""<div class="eu-sec" style="border:1px solid rgba(239,68,68,.2)">
                <h5>🧠 AI Anomali Analizi</h5>
                <div style="font-size:12px;color:#e2e8f0;line-height:1.7;white-space:pre-wrap">{analysis}</div>
            </div>""", unsafe_allow_html=True)
    else:
        styled_info_banner("Anomali tespit edilmedi. Tüm öğrenciler beklenen aralıkta. ✅", "info")


# ═══════════════════════════════════════════════════════════════
# TAB 9: AI MERKEZİ — Tüm AI Motorları Tek Panelde
# ═══════════════════════════════════════════════════════════════
def _tab_ai_center(store, loader):
    styled_section("🤖 Yapay Zeka Komuta Merkezi")

    styled_info_banner(
        "5 AI motoru aktif: Risk Tahmini, Profil Özeti, Anomali Tespiti, Veli Raporu, Müdahale Planı. "
        "Tüm motorlar GPT-4o-mini ile çalışır.", "info",
    )

    risks = store.get_latest_risks()
    students = loader.load_students()
    aktif = [s for s in students if s.get("durum") == "aktif"]

    styled_stat_row([
        ("Aktif Öğrenci", str(len(aktif)), "#3b82f6", "👥"),
        ("Risk Kaydı", str(len(risks)), "#8b5cf6", "📊"),
        ("AI Motor", "5", "#f59e0b", "🤖"),
        ("Model", "GPT-4o", "#22c55e", "🧠"),
    ])

    # ── Öğrenci seçimi ──
    risk_map = {r.get("student_id"): r for r in risks}
    opts = {}
    for s in aktif:
        sid = s.get("id", "")
        name = f"{s.get('ad', '')} {s.get('soyad', '')}".strip()
        risk_val = risk_map.get(sid, {}).get("risk_score", "-")
        opts[f"{name} — {s.get('sinif','')}/{s.get('sube','')} (Risk: {risk_val})"] = s

    selected = st.selectbox("🎯 Öğrenci Seç", [""] + list(opts.keys()), key="ai_center_stu")
    if not selected:
        styled_info_banner("AI analizi başlatmak için bir öğrenci seçin.", "info")
        _render_bulk_ai(risks, store)
        return

    stu = opts[selected]
    sid = stu.get("id", "")
    name = f"{stu.get('ad', '')} {stu.get('soyad', '')}".strip()
    record = risk_map.get(sid)
    risk_hist = store.get_student_risk_history(sid)

    if not record:
        styled_info_banner("Bu öğrenci için risk analizi yok. Dashboard'dan analiz çalıştırın.", "warning")
        return

    # ── 5 AI Motor Butonları ──
    st.markdown("---")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        btn_profile = st.button("🧠 Profil", key="aic_profile", use_container_width=True)
    with c2:
        btn_predict = st.button("🔮 Tahmin", key="aic_predict", use_container_width=True)
    with c3:
        btn_veli = st.button("✉️ Veli", key="aic_veli", use_container_width=True)
    with c4:
        btn_intv = st.button("📋 Müdahale", key="aic_intv", use_container_width=True)
    with c5:
        btn_all = st.button("⚡ Hepsi", key="aic_all", type="primary", use_container_width=True)

    run_profile = btn_profile or btn_all
    run_predict = btn_predict or btn_all
    run_veli = btn_veli or btn_all
    run_intv = btn_intv or btn_all

    # ── 1. AI Profil Özeti ──
    if run_profile:
        with st.spinner("🧠 AI Profil Özeti oluşturuluyor..."):
            summary = AIProfileSummarizer.generate_summary(name, record)
        styled_section("🧠 AI 360° Profil Özeti")
        if summary and not summary.startswith("[AI Hata"):
            st.markdown(f"""<div class="eu-sec" style="border:1px solid rgba(59,130,246,.3)">
                <h5>🧠 {name} — Profil Analizi</h5>
                <div style="font-size:12px;color:#e2e8f0;line-height:1.8;white-space:pre-wrap">{summary}</div>
            </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner(f"Profil özeti oluşturulamadı: {summary}", "warning")

    # ── 2. AI Risk Tahmini ──
    if run_predict:
        with st.spinner("🔮 30 Gün Risk Tahmini hesaplanıyor..."):
            prediction = PredictiveRiskEngine.predict_risk(sid, name, risk_hist, record)
        styled_section("🔮 30 Günlük Risk Tahmini")
        trend_icon = {"rising": "📈 Artıyor", "falling": "📉 Düşüyor", "stable": "➡️ Stabil"}.get(prediction["trend"], "?")
        pred_lv = risk_level_for(prediction["predicted_score"])
        curr_lv = risk_level_for(prediction["current_score"])
        st.markdown(f"""<div class="eu-card" style="border-left-color:#a78bfa">
            <h4>🔮 {name} — 30 Gün Projeksiyonu</h4>
            <div style="display:flex;gap:30px;margin:10px 0;align-items:center">
                <div style="text-align:center">
                    <div class="score" style="color:{curr_lv['color']}">{prediction['current_score']}</div>
                    <div class="meta">Mevcut</div>
                </div>
                <div style="font-size:28px;color:#64748b">→</div>
                <div style="text-align:center">
                    <div class="score" style="color:{pred_lv['color']}">{prediction['predicted_score']}</div>
                    <div class="meta">30 Gün Sonra</div>
                </div>
                <div style="flex:1;text-align:right">
                    <div style="font-size:14px;font-weight:700;color:#a78bfa">{trend_icon}</div>
                    <div class="meta">Güven: %{prediction['confidence']*100:.0f}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
        if prediction.get("ai_analysis") and not prediction["ai_analysis"].startswith("[AI Hata"):
            st.markdown(f"""<div class="eu-sec" style="border:1px solid rgba(167,139,250,.2)">
                <h5>🧠 AI Tahmin Yorumu</h5>
                <div style="font-size:12px;color:#e2e8f0;line-height:1.7;white-space:pre-wrap">{prediction['ai_analysis']}</div>
            </div>""", unsafe_allow_html=True)

    # ── 3. AI Veli Raporu ──
    if run_veli:
        with st.spinner("✉️ AI Veli Mektubu hazırlanıyor..."):
            letter = AIParentReportGenerator.generate_report(name, record)
        styled_section("✉️ AI Veli Bilgilendirme Mektubu")
        if letter and not letter.startswith("[AI Hata"):
            st.markdown(f"""<div style="background:#fff;color:#1a1a2e;border-radius:12px;padding:24px;
                font-family:'Segoe UI',sans-serif;line-height:1.8;font-size:13px;
                border:1px solid #e2e8f0;white-space:pre-wrap">{letter}</div>""",
                unsafe_allow_html=True,
            )
            st.download_button(
                "📥 Mektubu İndir", letter,
                file_name=f"veli_rapor_{name.replace(' ','_')}.txt",
                mime="text/plain", key="aic_dl_veli",
            )
        else:
            styled_info_banner(f"Veli mektubu oluşturulamadı: {letter}", "warning")

    # ── 4. AI Müdahale Planı ──
    if run_intv:
        with st.spinner("📋 AI Müdahale Planı oluşturuluyor..."):
            plan = AIInterventionPlanner.plan_intervention(name, record)
        styled_section("📋 AI Müdahale Stratejisi")
        pc = {"ACİL": "#ef4444", "YÜKSEK": "#f97316", "ORTA": "#f59e0b", "DÜŞÜK": "#22c55e"}.get(plan["priority"], "#6366f1")
        st.markdown(f"""<div class="eu-card" style="border-left-color:{pc}">
            <h4>📋 {name} — Müdahale Planı</h4>
            <div class="meta">Öncelik: <b style="color:{pc}">{plan['priority']}</b> | Risk: {plan['risk_score']:.1f}</div>
            <div style="margin-top:8px">
                <b style="color:#60a5fa;font-size:11px">Stratejiler:</b><br>
                {''.join(f"<span class='eu-module-badge' style='background:rgba(59,130,246,.12);color:#60a5fa'>{s}</span>" for s in plan['strategies'])}
            </div>
            <div style="margin-top:6px">
                <b style="color:#22c55e;font-size:11px">Paydaşlar:</b><br>
                {''.join(f"<span class='eu-module-badge' style='background:rgba(34,197,94,.12);color:#22c55e'>{s}</span>" for s in plan['stakeholders'])}
            </div>
        </div>""", unsafe_allow_html=True)
        if plan.get("ai_plan_text") and not plan["ai_plan_text"].startswith("[AI Hata"):
            st.markdown(f"""<div class="eu-sec" style="border:1px solid rgba(139,92,246,.3)">
                <h5>🧠 Detaylı Müdahale Planı</h5>
                <div style="font-size:12px;color:#e2e8f0;line-height:1.8;white-space:pre-wrap">{plan['ai_plan_text']}</div>
            </div>""", unsafe_allow_html=True)

    # ── Alt: Toplu AI ──
    st.markdown("---")
    _render_bulk_ai(risks, store)


def _render_bulk_ai(risks, store):
    """Toplu anomali tarama ve riskli öğrenci AI analizi."""
    styled_section("⚡ Toplu AI Analiz")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔬 Anomali Tara (Tüm Okul)", key="aic_bulk_anomaly", use_container_width=True):
            anomalies = AnomalyDetector.detect_anomalies(risks)
            if anomalies:
                st.warning(f"⚠️ {len(anomalies)} öğrencide anomali tespit edildi!")
                for a in anomalies[:5]:
                    z_icon = "🔺" if a["anomaly_type"] == "high" else "🔽"
                    st.markdown(f"- {z_icon} **{a['student_name']}** ({a['sinif']}/{a['sube']}) — Risk: {a['risk_score']}, Z: {a['z_score']}")
                with st.spinner("AI anomali yorumu..."):
                    analysis = AnomalyDetector.get_ai_anomaly_analysis(anomalies)
                if analysis and not analysis.startswith("[AI Hata"):
                    st.markdown(f"""<div class="eu-sec" style="border:1px solid rgba(239,68,68,.2)">
                        <h5>🧠 AI Anomali Raporu</h5>
                        <div style="font-size:12px;color:#e2e8f0;line-height:1.7;white-space:pre-wrap">{analysis}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                styled_info_banner("Anomali tespit edilmedi. Tüm öğrenciler normal aralıkta. ✅", "info")

    with c2:
        if st.button("📊 En Riskli 5 için AI Rapor", key="aic_bulk_top5", use_container_width=True):
            top5 = sorted(risks, key=lambda x: x.get("risk_score", 0), reverse=True)[:5]
            if not top5:
                styled_info_banner("Risk verisi yok.", "warning")
                return
            for r in top5:
                rname = r.get("student_name", "?")
                with st.spinner(f"🧠 {rname} analiz ediliyor..."):
                    summary = AIProfileSummarizer.generate_summary(rname, r)
                lv = risk_level_for(r.get("risk_score", 0))
                if summary and not summary.startswith("[AI Hata"):
                    st.markdown(f"""<div class="eu-sec" style="border-left:3px solid {lv['color']}">
                        <h5>{lv['icon']} {rname} — {r.get('sinif','')}/{r.get('sube','')} (Risk: {r.get('risk_score',0)})</h5>
                        <div style="font-size:11px;color:#e2e8f0;line-height:1.6;white-space:pre-wrap">{summary}</div>
                    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 10: ISI HARİTASI (HEATMAP) + KORELASYON MATRİSİ
# ═══════════════════════════════════════════════════════════════

def _tab_heatmap(store, loader):
    styled_section("🔥 Risk Isı Haritası — Sınıf × Bileşen Matrisi")

    risks = store.get_latest_risks()
    if not risks:
        styled_info_banner("Risk verisi yok. Önce Dashboard'dan analiz çalıştırın.", "warning")
        return

    comp_labels = {
        "grade_risk": "Not", "attendance_risk": "Devam.", "exam_risk": "Sınav",
        "homework_risk": "Ödev", "outcome_debt_risk": "Kaz.Borç", "counseling_risk": "Rehber.",
        "health_risk": "Sağlık", "trend_risk": "Trend", "behavior_risk": "Davranış",
        "foreign_lang_risk": "Yab.Dil",
    }
    comp_keys = list(comp_labels.keys())

    # 3D Surface Plot
    _cls_map: dict[str, dict] = {}
    for r in risks:
        k = f"{r.get('sinif', '?')}/{r.get('sube', '?')}"
        if k not in _cls_map:
            _cls_map[k] = {ck: [] for ck in comp_keys}
        for ck in comp_keys:
            _cls_map[k][ck].append(r.get(ck, 0))
    _cls_names = sorted(_cls_map.keys())
    _comp_names = [comp_labels[ck] for ck in comp_keys]
    _z = [[sum(_cls_map[c][ck]) / max(len(_cls_map[c][ck]), 1) for ck in comp_keys] for c in _cls_names]
    if _cls_names and _z:
        heatmap_3d_surface(_cls_names, _comp_names, _z)

    # Sınıf gruplama
    class_data: dict[str, dict] = {}
    for r in risks:
        key = f"{r.get('sinif', '?')}/{r.get('sube', '?')}"
        if key not in class_data:
            class_data[key] = {"count": 0, "components": {}}
        class_data[key]["count"] += 1
        for comp in comp_keys:
            class_data[key]["components"].setdefault(comp, []).append(r.get(comp, 0))

    # Heatmap table
    th = "<th style='padding:8px 4px;background:#1e1b4b;color:#a5b4fc;font-size:.7rem;'>Sınıf</th>"
    for ck in comp_keys:
        th += f"<th style='padding:8px 2px;background:#1e1b4b;color:#a5b4fc;font-size:.6rem;text-align:center;writing-mode:vertical-rl;min-width:28px;'>{comp_labels[ck]}</th>"
    th += "<th style='padding:8px 4px;background:#1e1b4b;color:#a5b4fc;font-size:.7rem;text-align:center;'>Ort</th>"

    rows = ""
    for cls in sorted(class_data.keys()):
        cd = class_data[cls]
        cells = ""
        total = 0
        for ck in comp_keys:
            vals = cd["components"].get(ck, [0])
            avg = sum(vals) / len(vals) if vals else 0
            total += avg
            bg = "#064e3b" if avg < 25 else "#166534" if avg < 40 else "#854d0e" if avg < 55 else "#9a3412" if avg < 70 else "#7f1d1d"
            cells += f"<td style='padding:6px 2px;text-align:center;background:{bg};color:#fff;font-size:.75rem;font-weight:700;border:1px solid #0f172a;'>{avg:.0f}</td>"
        ov = total / len(comp_keys)
        ov_c = "#22c55e" if ov < 30 else "#f59e0b" if ov < 55 else "#f97316" if ov < 75 else "#ef4444"
        cells += f"<td style='padding:6px;text-align:center;color:{ov_c};font-weight:800;background:#0f172a;border:1px solid #1e293b;'>{ov:.0f}</td>"
        rows += f"<tr><td style='padding:6px 8px;font-weight:700;color:#c7d2fe;font-size:.82rem;background:#0f172a;border:1px solid #1e293b;'>{cls} <span style='color:#64748b;font-size:.65rem;'>({cd['count']})</span></td>{cells}</tr>"

    st.markdown(f"""<div style="overflow-x:auto;border-radius:12px;border:2px solid rgba(99,102,241,.2);">
    <table style="width:100%;border-collapse:collapse;"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>
    <div style="display:flex;gap:6px;margin-top:8px;justify-content:center;">
    <span style="font-size:.7rem;color:#94a3b8;">Renk:</span>
    <span style="background:#064e3b;color:#fff;padding:2px 8px;border-radius:4px;font-size:.65rem;">0-24</span>
    <span style="background:#166534;color:#fff;padding:2px 8px;border-radius:4px;font-size:.65rem;">25-39</span>
    <span style="background:#854d0e;color:#fff;padding:2px 8px;border-radius:4px;font-size:.65rem;">40-54</span>
    <span style="background:#9a3412;color:#fff;padding:2px 8px;border-radius:4px;font-size:.65rem;">55-69</span>
    <span style="background:#7f1d1d;color:#fff;padding:2px 8px;border-radius:4px;font-size:.65rem;">70+</span>
    </div>""", unsafe_allow_html=True)

    # Korelasyon Matrisi
    st.markdown("---")
    styled_section("🔗 Bileşen Korelasyon Matrisi")
    import math

    comp_vals = {ck: [r.get(ck, 0) for r in risks] for ck in comp_keys}

    def _pearson(xs, ys):
        n = len(xs)
        if n < 3: return 0
        mx, my = sum(xs) / n, sum(ys) / n
        sx = math.sqrt(max(0, sum((x - mx) ** 2 for x in xs) / n))
        sy = math.sqrt(max(0, sum((y - my) ** 2 for y in ys) / n))
        if sx == 0 or sy == 0: return 0
        return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n * sx * sy)

    cor_th = "<th style='padding:4px;background:#1e1b4b;'></th>"
    for ck in comp_keys:
        cor_th += f"<th style='padding:4px 2px;background:#1e1b4b;color:#a5b4fc;font-size:.55rem;text-align:center;writing-mode:vertical-rl;'>{comp_labels[ck]}</th>"
    cor_rows = ""
    for ck1 in comp_keys:
        cells = ""
        for ck2 in comp_keys:
            if ck1 == ck2:
                cells += "<td style='padding:4px;text-align:center;background:#312e81;color:#818cf8;font-size:.6rem;font-weight:700;border:1px solid #0f172a;'>1.00</td>"
            else:
                corr = _pearson(comp_vals[ck1], comp_vals[ck2])
                bg = "#7f1d1d" if corr >= 0.7 else "#854d0e" if corr >= 0.4 else "#1e3a5f" if corr <= -0.4 else "#0f172a"
                cells += f"<td style='padding:4px;text-align:center;background:{bg};color:#e2e8f0;font-size:.6rem;border:1px solid #0f172a;'>{corr:.2f}</td>"
        cor_rows += f"<tr><td style='padding:4px 6px;background:#0f172a;color:#a5b4fc;font-size:.65rem;font-weight:600;border:1px solid #1e293b;'>{comp_labels[ck1]}</td>{cells}</tr>"

    st.markdown(f"""<div style="overflow-x:auto;border-radius:10px;"><table style="border-collapse:collapse;">
    <thead><tr>{cor_th}</tr></thead><tbody>{cor_rows}</tbody></table></div>
    <div style="font-size:.7rem;color:#64748b;margin-top:6px;">Yüksek pozitif (≥0.7): birlikte kötüleşiyor | Negatif: ters yönlü</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 11: DÖNEM KARŞILAŞTIRMA
# ═══════════════════════════════════════════════════════════════

def _tab_donem_karsilastirma(store, loader):
    styled_section("📊 Dönem Karşılaştırma — İyileşen / Kötüleşen / Stabil")

    risks = store.load_risks()
    if not risks:
        styled_info_banner("Risk verisi yok.", "warning")
        return

    student_map: dict[str, dict] = {}
    for r in risks:
        sid = r.get("student_id", "")
        if not sid: continue
        if sid not in student_map:
            student_map[sid] = {"first": r, "last": r, "name": r.get("student_name", ""), "sinif": r.get("sinif", ""), "sube": r.get("sube", "")}
        else:
            if r.get("calculated_at", "") < student_map[sid]["first"].get("calculated_at", ""):
                student_map[sid]["first"] = r
            if r.get("calculated_at", "") > student_map[sid]["last"].get("calculated_at", ""):
                student_map[sid]["last"] = r

    iyilesen, kotulesen, stabil = [], [], []
    for sid, d in student_map.items():
        delta = d["last"].get("risk_score", 0) - d["first"].get("risk_score", 0)
        entry = {"name": d["name"], "sinif": d["sinif"], "sube": d["sube"],
                 "first": round(d["first"].get("risk_score", 0), 1),
                 "last": round(d["last"].get("risk_score", 0), 1),
                 "delta": round(delta, 1), "level": d["last"].get("risk_level", "LOW")}
        if delta < -5: iyilesen.append(entry)
        elif delta > 5: kotulesen.append(entry)
        else: stabil.append(entry)

    styled_stat_row([
        ("İyileşen", str(len(iyilesen)), "#22c55e", "📈"),
        ("Kötüleşen", str(len(kotulesen)), "#ef4444", "📉"),
        ("Stabil", str(len(stabil)), "#f59e0b", "➡️"),
        ("Toplam", str(len(student_map)), "#6366f1", "👥"),
    ])

    c1, c2, c3 = st.columns(3)

    def _list(items, color, icon, title, col):
        with col:
            st.markdown(f"<h4 style='color:{color};font-size:14px;'>{icon} {title} ({len(items)})</h4>", unsafe_allow_html=True)
            for s in sorted(items, key=lambda x: abs(x["delta"]), reverse=True)[:15]:
                arr = "↓" if s["delta"] < 0 else "↑"
                lv = risk_level_for(s["last"])
                st.markdown(f"""<div style="background:#0f172a;border-left:3px solid {color};border-radius:0 8px 8px 0;padding:6px 10px;margin:3px 0;">
                <div style="font-size:.82rem;font-weight:700;color:#e2e8f0;">{s['name']}</div>
                <div style="font-size:.72rem;color:#94a3b8;">{s['sinif']}/{s['sube']} | {s['first']} {arr} {s['last']} <span style="color:{color};font-weight:700;">({s['delta']:+.1f})</span> | {lv['icon']}</div>
                </div>""", unsafe_allow_html=True)

    _list(iyilesen, "#22c55e", "📈", "İyileşen", c1)
    _list(kotulesen, "#ef4444", "📉", "Kötüleşen", c2)
    _list(stabil, "#f59e0b", "➡️", "Stabil", c3)

    # Bileşen bazlı değişim
    st.markdown("---")
    styled_section("🔬 Bileşen Bazlı Kurum Değişimi")
    # Butterfly chart
    _bf_labels = {"grade_risk": "Not", "attendance_risk": "Devam.", "exam_risk": "Sınav",
                  "homework_risk": "Ödev", "outcome_debt_risk": "Kaz.Borç", "counseling_risk": "Rehber.",
                  "health_risk": "Sağlık", "trend_risk": "Trend", "behavior_risk": "Davranış",
                  "foreign_lang_risk": "Yab.Dil"}
    _bf_first = {ck: sum(d["first"].get(ck, 0) for d in student_map.values()) / max(len(student_map), 1) for ck in _bf_labels}
    _bf_last = {ck: sum(d["last"].get(ck, 0) for d in student_map.values()) / max(len(student_map), 1) for ck in _bf_labels}
    period_comparison_butterfly(_bf_labels, _bf_first, _bf_last)
    cl = {"grade_risk": "Not", "attendance_risk": "Devamsızlık", "exam_risk": "Sınav", "homework_risk": "Ödev",
          "outcome_debt_risk": "Kaz.Borç", "counseling_risk": "Rehberlik", "health_risk": "Sağlık",
          "trend_risk": "Trend", "behavior_risk": "Davranış", "foreign_lang_risk": "Yab.Dil"}
    for comp, label in cl.items():
        f_vals = [d["first"].get(comp, 0) for d in student_map.values()]
        l_vals = [d["last"].get(comp, 0) for d in student_map.values()]
        af = sum(f_vals) / len(f_vals) if f_vals else 0
        al = sum(l_vals) / len(l_vals) if l_vals else 0
        dt = al - af
        clr = "#22c55e" if dt < -3 else "#ef4444" if dt > 3 else "#f59e0b"
        arr = "↓" if dt < -3 else "↑" if dt > 3 else "→"
        st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;padding:3px 0;">
        <span style="min-width:90px;color:#cbd5e1;font-size:.82rem;">{label}</span>
        <span style="color:#64748b;font-size:.75rem;min-width:40px;">{af:.1f}</span>
        <span style="color:{clr};font-weight:700;">{arr}</span>
        <span style="color:{clr};font-weight:700;font-size:.82rem;min-width:40px;">{al:.1f}</span>
        <span style="color:{clr};font-size:.72rem;">({dt:+.1f})</span></div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 12: MÜDAHALE TAKİP DÖNGÜSÜ + BİLDİRİM
# ═══════════════════════════════════════════════════════════════

def _tab_mudahale_takip(store):
    styled_section("🔄 Müdahale Takip — Plan → Uygulama → Sonuç")

    interventions = store.load_interventions()
    planned = [i for i in interventions if i.get("status") == "planned"]
    in_prog = [i for i in interventions if i.get("status") == "in_progress"]
    done = [i for i in interventions if i.get("status") == "completed"]
    unresolved = [a for a in store.load_alerts() if not a.get("is_resolved")]

    styled_stat_row([
        ("Planlanan", str(len(planned)), "#3b82f6", "📋"),
        ("Devam Eden", str(len(in_prog)), "#f59e0b", "🔄"),
        ("Tamamlanan", str(len(done)), "#22c55e", "✅"),
        ("Çözülmemiş Uyarı", str(len(unresolved)), "#ef4444", "🔴"),
    ])

    # Yeni müdahale
    st.markdown("---")
    st.markdown("#### ➕ Yeni Müdahale Planı")
    high_risk = [r for r in (store.get_latest_risks() or []) if r.get("risk_level") in ("HIGH", "CRITICAL")]
    if high_risk:
        opts = {f"{r.get('student_name','?')} ({r.get('sinif','')}/{r.get('sube','')}) — {r.get('risk_score',0):.0f}": r for r in high_risk}
        sel = st.selectbox("Öğrenci:", list(opts.keys()), key="mt_sel")
        mc1, mc2 = st.columns(2)
        with mc1:
            ptype = st.selectbox("Tür:", ["Akademik Destek", "Devamsızlık Takip", "Veli Görüşmesi",
                "Rehberlik Yönlendirme", "Yabancı Dil Destek", "Kapsamlı", "Diğer"], key="mt_type")
        with mc2:
            assigned = st.text_input("Sorumlu:", key="mt_assigned", placeholder="Sınıf öğretmeni")
        desc = st.text_area("Plan Detayı:", key="mt_desc", height=80)
        if st.button("📋 Oluştur", key="mt_create", type="primary"):
            if sel and desc:
                r = opts[sel]
                store.save_intervention(Intervention(
                    student_id=r.get("student_id", ""), student_name=r.get("student_name", ""),
                    plan_type=ptype, description=desc, assigned_to=assigned or "-",
                    status="planned", start_date=datetime.now().strftime("%Y-%m-%d")))
                st.success("Plan oluşturuldu!")
                st.rerun()
    else:
        styled_info_banner("Yüksek/Kritik öğrenci yok. ✅", "info")

    # Mevcut müdahaleler
    if interventions:
        st.markdown("---")
        st.markdown("#### 📋 Müdahale Kayıtları")
        flt = st.radio("Filtre:", ["Tümü", "Planlanan", "Devam Eden", "Tamamlanan"], horizontal=True, key="mt_flt")
        show = {"Planlanan": planned, "Devam Eden": in_prog, "Tamamlanan": done}.get(flt, interventions)
        for iv in sorted(show, key=lambda x: x.get("created_at", ""), reverse=True):
            st_lbl, st_clr = {"planned": ("📋 Plan", "#3b82f6"), "in_progress": ("🔄 Devam", "#f59e0b"),
                              "completed": ("✅ Tamam", "#22c55e")}.get(iv.get("status", ""), ("?", "#64748b"))
            with st.expander(f"{st_lbl} | {iv.get('student_name','?')} — {iv.get('plan_type','')}", expanded=(iv.get("status") != "completed")):
                st.markdown(f"""<div style="background:#0f172a;border-left:4px solid {st_clr};border-radius:0 10px 10px 0;padding:10px 14px;">
                <b>{iv.get('plan_type','')}</b> | Sorumlu: {iv.get('assigned_to','-')}<br>
                <span style="color:#cbd5e1;font-size:.82rem;">{iv.get('description','')}</span><br>
                <span style="color:#64748b;font-size:.72rem;">Başlangıç: {iv.get('start_date','-')}</span></div>""", unsafe_allow_html=True)
                if iv.get("status") == "planned":
                    if st.button("▶️ Başlat", key=f"mt_s_{iv.get('id','')}"):
                        store.update_intervention_status(iv["id"], "in_progress", "")
                        st.rerun()
                elif iv.get("status") == "in_progress":
                    outcome = st.text_input("Sonuç:", key=f"mt_o_{iv.get('id','')}")
                    if st.button("✅ Tamamla", key=f"mt_d_{iv.get('id','')}"):
                        store.update_intervention_status(iv["id"], "completed", outcome)
                        st.rerun()

    # Bildirim sistemi
    st.markdown("---")
    styled_section("📨 Otomatik Bildirim")
    critical = [r for r in (store.get_latest_risks() or []) if r.get("risk_level") == "CRITICAL"]
    if critical:
        st.warning(f"⚠️ {len(critical)} kritik öğrenci!")
        if st.button("📨 Kritik Velilere Mesaj Gönder", key="mt_notify", type="primary"):
            sent = 0
            for cr in critical:
                try:
                    from models.akademik_takip import AkademikDataStore
                    ak = AkademikDataStore()
                    msgs = ak._load_json(ak._paths.get("veli_mesajlar", ""))
                    if isinstance(msgs, list):
                        msgs.append({
                            "student_id": cr.get("student_id", ""),
                            "konu": f"Erken Uyarı: {cr.get('student_name', '')}",
                            "mesaj": f"Sayın Veli, {cr.get('student_name','')} öğrencimizin risk skoru "
                                     f"{cr.get('risk_score',0):.0f}/100. Rehberlik ile görüşmenizi rica ederiz.",
                            "gonderen": "Erken Uyarı", "tarih": datetime.now().strftime("%Y-%m-%d"), "okundu": False,
                        })
                        ak._save_json(ak._paths.get("veli_mesajlar", ""), msgs)
                        sent += 1
                except Exception:
                    pass
            st.success(f"✅ {sent} veliye mesaj gönderildi!")
    else:
        styled_info_banner("Kritik öğrenci yok. ✅", "info")


# ═══════════════════════════════════════════════════════════════
# TAB 13: KURUM RİSK KARNESİ + HAFTALIK PDF
# ═══════════════════════════════════════════════════════════════

def _tab_kurum_karnesi(store, loader):
    styled_section("📋 Kurum Risk Karnesi")

    risks = store.get_latest_risks()
    if not risks:
        styled_info_banner("Risk verisi yok.", "warning")
        return

    scores = [r.get("risk_score", 0) for r in risks]
    avg = sum(scores) / len(scores)
    low = sum(1 for r in risks if r.get("risk_level") == "LOW")
    med = sum(1 for r in risks if r.get("risk_level") == "MEDIUM")
    high = sum(1 for r in risks if r.get("risk_level") == "HIGH")
    crit = sum(1 for r in risks if r.get("risk_level") == "CRITICAL")
    lv = risk_level_for(avg)

    # Ana karne
    st.markdown(f"""<div style="background:linear-gradient(135deg,#0f172a,#1e1b4b);border-radius:16px;
    padding:24px;margin:12px 0;border:2px solid {lv['color']}40;text-align:center;">
    <div style="color:#94a3b8;font-size:.9rem;">Kurum Risk Ortalaması</div>
    <div style="font-size:3rem;font-weight:900;color:{lv['color']};margin:8px 0;">{avg:.1f}</div>
    <div style="font-size:1.1rem;font-weight:700;color:{lv['color']};">{lv['icon']} {lv['label']}</div>
    <div style="display:flex;justify-content:center;gap:20px;margin-top:14px;">
    <span style="color:#22c55e;">🟢 {low}</span><span style="color:#f59e0b;">🟡 {med}</span>
    <span style="color:#f97316;">🟠 {high}</span><span style="color:#ef4444;">🔴 {crit}</span>
    </div><div style="color:#64748b;font-size:.78rem;margin-top:8px;">{len(risks)} öğrenci</div>
    </div>""", unsafe_allow_html=True)

    # Bileşen ortalamaları
    st.markdown("---")
    styled_section("Bileşen Ortalamaları")
    cl = {"grade_risk": ("📚", "Not"), "attendance_risk": ("📅", "Devam."), "exam_risk": ("📝", "Sınav"),
          "homework_risk": ("📋", "Ödev"), "outcome_debt_risk": ("🎯", "Kaz.Borç"),
          "counseling_risk": ("🧭", "Rehber."), "health_risk": ("🏥", "Sağlık"),
          "trend_risk": ("📈", "Trend"), "behavior_risk": ("⚡", "Davranış"),
          "foreign_lang_risk": ("🌍", "Yab.Dil")}
    for ck, (ic, lb) in cl.items():
        vs = [r.get(ck, 0) for r in risks]
        a = sum(vs) / len(vs) if vs else 0
        c = "#22c55e" if a < 30 else "#f59e0b" if a < 55 else "#f97316" if a < 75 else "#ef4444"
        w = RISK_WEIGHTS.get(ck.replace("_risk", ""), 0) * 100
        st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;padding:3px 0;">
        <span>{ic}</span><span style="min-width:80px;color:#cbd5e1;font-size:.82rem;">{lb} <span style="color:#64748b;font-size:.6rem;">%{w:.0f}</span></span>
        <div style="flex:1;background:rgba(99,102,241,.08);border-radius:4px;height:16px;overflow:hidden;">
        <div style="width:{a}%;height:100%;background:{c};border-radius:4px;"></div></div>
        <span style="color:{c};font-weight:700;font-size:.85rem;">{a:.1f}</span></div>""", unsafe_allow_html=True)

    # Sınıf sıralaması
    st.markdown("---")
    styled_section("Sınıf Sıralaması")
    class_r: dict[str, list] = {}
    for r in risks:
        k = f"{r.get('sinif','?')}/{r.get('sube','?')}"
        class_r.setdefault(k, []).append(r.get("risk_score", 0))
    sorted_c = sorted(class_r.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True)
    for i, (cls, sc) in enumerate(sorted_c):
        a = sum(sc) / len(sc)
        l2 = risk_level_for(a)
        medal = "🥇" if i == len(sorted_c) - 1 else ""
        st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;padding:3px 0;">
        <span style="min-width:20px;">{medal}</span>
        <span style="min-width:55px;color:#e2e8f0;font-weight:700;font-size:.85rem;">{cls}</span>
        <div style="flex:1;background:rgba(99,102,241,.08);border-radius:4px;height:14px;overflow:hidden;">
        <div style="width:{a}%;height:100%;background:{l2['color']};border-radius:4px;"></div></div>
        <span style="color:{l2['color']};font-weight:700;font-size:.82rem;">{a:.1f}</span>
        <span style="color:#64748b;font-size:.7rem;">({len(sc)})</span></div>""", unsafe_allow_html=True)

    # PDF üretimi
    st.markdown("---")
    styled_section("📄 Haftalık Risk Raporu PDF")
    if st.button("📄 PDF Oluştur & İndir", key="kk_pdf", type="primary", use_container_width=True):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import cm
            from reportlab.pdfgen import canvas as _cv
            from reportlab.lib.colors import HexColor
            import io
            buf = io.BytesIO()
            c = _cv.Canvas(buf, pagesize=A4)
            w, h = A4
            # Başlık
            c.setFillColor(HexColor("#1e1b4b"))
            c.rect(0, h - 80, w, 80, fill=1, stroke=0)
            c.setFillColor(HexColor("#ffffff"))
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(w / 2, h - 35, "KURUM RISK KARNESI")
            c.setFont("Helvetica", 10)
            c.drawCentredString(w / 2, h - 55, f"Haftalik Ozet - {datetime.now().strftime('%d.%m.%Y')}")
            c.drawCentredString(w / 2, h - 70, f"{len(risks)} ogrenci | Ort: {avg:.1f} | {lv['label']}")
            y = h - 110
            c.setFillColor(HexColor("#1e293b"))
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, y, "Risk Dagilimi:")
            y -= 16
            c.setFont("Helvetica", 10)
            for lb, cnt in [("Dusuk", low), ("Orta", med), ("Yuksek", high), ("Kritik", crit)]:
                c.drawString(2 * cm, y, f"  {lb}: {cnt}")
                y -= 14
            y -= 10
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, y, "En Riskli 10:")
            y -= 16
            c.setFont("Helvetica", 9)
            for r in sorted(risks, key=lambda x: x.get("risk_score", 0), reverse=True)[:10]:
                c.drawString(2 * cm, y, f"- {r.get('student_name','?')} ({r.get('sinif','')}/{r.get('sube','')}) Risk: {r.get('risk_score',0):.0f}")
                y -= 13
                if y < 3 * cm: c.showPage(); y = h - 3 * cm
            y -= 10
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, y, "Bilesen Ortalamalari:")
            y -= 16
            c.setFont("Helvetica", 9)
            for ck, (ic, lb) in cl.items():
                vs = [r.get(ck, 0) for r in risks]
                a = sum(vs) / len(vs) if vs else 0
                c.drawString(2 * cm, y, f"  {lb}: {a:.1f}")
                y -= 13
            c.save()
            buf.seek(0)
            st.download_button("📥 PDF İndir", data=buf.getvalue(),
                               file_name=f"risk_karnesi_{datetime.now().strftime('%Y%m%d')}.pdf",
                               mime="application/pdf")
            st.success("PDF hazır!")
        except ImportError:
            styled_info_banner("pip install reportlab gerekli.", "warning")
