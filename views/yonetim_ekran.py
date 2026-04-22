"""
YTE-01 Yonetim Tek Ekran - Streamlit UI
=========================================
Tum modullerin gunluk planlama ve raporlama merkezi.
Otomatik veri toplama: Diger modullerde girilen tarihli islemler
gunu geldiginde bu ekrana otomatik duser.
"""

from __future__ import annotations

import os
from datetime import date, datetime, timedelta
from collections import Counter

import streamlit as st
import pandas as pd  # plotly 6.x requires pandas fully loaded before use
import plotly.graph_objects as go

from utils.chart_utils import SC_COLORS, sc_pie, sc_bar, SC_CHART_CFG
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner


def _init_premium_widgets():
    """Premium widget'ları render_yonetim_ekran içinde lazy-load et (dosya seviyesinde değil)."""
    try:
        from utils.ui_common import ultra_premium_baslat
        ultra_premium_baslat("yonetim_ekran")
    except Exception:
        pass
    try:
        from utils.ui_common import (modul_hosgeldin, bildirim_cani, kisisel_karsilama,
                                      canli_aktivite_akisi, turkiye_haritasi_widget)
        _user = st.session_state.get("auth_user", {})
        kisisel_karsilama(_user.get("name", "Yonetici"), _user.get("role", ""),
                          ["4 randevu bugun", "2 risk uyarisi", "8 sicak aday"])
        bildirim_cani(3)
        turkiye_haritasi_widget()
        canli_aktivite_akisi([
            {"mesaj": "Sistem baslatildi", "zaman": "08:00", "ikon": "\U0001f7e2", "renk": "#10B981"},
            {"mesaj": "Gunluk rapor olusturuldu", "zaman": "08:05", "ikon": "\U0001f4ca", "renk": "#6366F1"},
        ])
    except Exception:
        pass
    try:
        from utils.ui_common import canli_yoklama_haritasi
        canli_yoklama_haritasi()
    except Exception:
        pass

from models.yonetim_ekran import (
    YTEDataStore, GunlukToplayici, GunlukIslemToplayici,
    RaporUreticisi, ModulOzetleyici, ModulRaporToplayici,
    PlanlanmisGorev, GunlukRapor, EpostaAlici, YTEAyar,
    GOREV_DURUMLARI, GOREV_DURUM_RENK, GOREV_DURUM_IKON,
    ONCELIK_SEVIYELERI, ONCELIK_RENK, MODUL_RENK, MODUL_IKON,
)
from utils.tenant import get_tenant_dir
from utils.auth import AuthManager
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome

# Sozlesme raporlari için HI modulu fonksiyonlari
try:
    from views.halkla_iliskiler_module import load_sozlesmeler, _generate_sozlesme_pdf
except ImportError:
    load_sozlesmeler = None
    _generate_sozlesme_pdf = None

# Personel Bilgi Karti icin IK modulu fonksiyonlari
try:
    from views.insan_kaynaklari import (
        _collect_personel_data, _render_personel_bilgi_karti,
        _generate_personel_bilgi_karti_pdf, _get_akademik_store,
        DEVAMSIZLIK_TURLERI,
    )
    from models.insan_kaynaklari import IKDataStore
    _IK_AVAILABLE = True
except ImportError:
    _IK_AVAILABLE = False

# ============================================================
# RENK PALETI
# ============================================================
_CLR_PRIMARY = "#0B0F19"
_CLR_BLUE = "#4472C4"
_CLR_ORANGE = "#ED7D31"
_CLR_GREEN = "#70AD47"
_CLR_GOLD = "#FFC000"
_CLR_GRAY = "#A5A5A5"
_CLR_RED = "#ef4444"

_CHART_COLORS = [
    "#2563eb", "#7c3aed", "#8b5cf6", "#059669", "#ea580c",
    "#dc2626", "#6366f1", "#0891b2", "#4472C4", "#b91c1c",
    "#0d9488", "#f59e0b", "#64748b",
]


# ============================================================
# CSS
# ============================================================

def _inject_css():
    inject_common_css("yte")
    st.markdown("""<style>
    :root{--yte-primary:#0B0F19;--yte-blue:#4472C4;--yte-orange:#ED7D31;--yte-green:#70AD47;--yte-gold:#FFC000;}
    </style>""", unsafe_allow_html=True)


def _durum_badge(durum: str) -> str:
    renk = GOREV_DURUM_RENK.get(durum, "#94a3b8")
    ikon = GOREV_DURUM_IKON.get(durum, "")
    return (f'<span style="background:{renk}18;color:{renk};padding:3px 10px;border-radius:8px;'
            f'font-size:11px;font-weight:700;">{ikon} {durum}</span>')


def _modul_badge(modul: str) -> str:
    renk = MODUL_RENK.get(modul, "#64748b")
    ikon = MODUL_IKON.get(modul, "📋")
    return (f'<span style="background:{renk}15;color:{renk};padding:2px 8px;border-radius:6px;'
            f'font-size:10px;font-weight:600;">{ikon} {modul}</span>')


# ============================================================
# STORE & SYNC HELPERS
# ============================================================

def _get_store() -> YTEDataStore:
    base = os.path.join(get_tenant_dir(), "yte")
    store = YTEDataStore(base)
    if "yte_defaults" not in st.session_state:
        store.auto_populate_defaults()
        st.session_state["yte_defaults"] = True
    return store


def _otomatik_senkronize(tarih_str: str, store: YTEDataStore) -> list[PlanlanmisGorev]:
    """Tarih için canli veriyi tum modullerden topla, kayitli durumlarla birlestir."""
    cache_key = f"yte_sync_{tarih_str}"
    if cache_key in st.session_state:
        # Cache'den yukle (bu session icinde zaten senkronize edildi)
        gorevler_raw = store.find_by_field("gorevler", "tarih", tarih_str)
        return [PlanlanmisGorev.from_dict(g) if isinstance(g, dict) else g for g in gorevler_raw]

    # Canli senkronizasyon
    toplayici = GunlukToplayici(tarih_str)
    merged = toplayici.senkronize(store)
    st.session_state[cache_key] = True
    return merged


def _force_senkronize(tarih_str: str, store: YTEDataStore) -> list[PlanlanmisGorev]:
    """Cache'i temizle ve yeniden senkronize et."""
    cache_key = f"yte_sync_{tarih_str}"
    if cache_key in st.session_state:
        del st.session_state[cache_key]
    return _otomatik_senkronize(tarih_str, store)


def _load_gorevler_for_date(tarih_str: str, store: YTEDataStore) -> list[PlanlanmisGorev]:
    """Belirli bir tarih için görevleri yükle (tekrar eden kalıp için yardımcı)."""
    gorevler_raw = store.find_by_field("gorevler", "tarih", tarih_str)
    return [PlanlanmisGorev.from_dict(g) if isinstance(g, dict) else g for g in gorevler_raw]


def _gorev_timeline_html(gorevler: list[PlanlanmisGorev]) -> None:
    """Görevleri timeline görünümünde göster."""
    for g in sorted(gorevler, key=lambda x: x.saat or "99:99"):
        renk = MODUL_RENK.get(g.kaynak_modul, "#64748b")
        saat_str = g.saat or "--:--"
        bitis = f" - {g.bitis_saati}" if g.bitis_saati else ""
        sorumlu_str = f' | <span style="color:#64748b;">{g.sorumlu}</span>' if g.sorumlu else ""
        konum_str = f' | 📍 {g.konum}' if g.konum else ""
        oncelik_badge = ""
        if g.oncelik in ("Kritik", "Yuksek"):
            o_renk = ONCELIK_RENK.get(g.oncelik, "#94a3b8")
            oncelik_badge = (f'<span style="background:{o_renk}18;color:{o_renk};padding:1px 6px;'
                             f'border-radius:4px;font-size:9px;font-weight:700;">{g.oncelik}</span>')
        st.markdown(f"""<div style="display:flex;gap:12px;align-items:stretch;margin-bottom:8px;">
        <div style="width:4px;background:{renk};border-radius:2px;flex-shrink:0;"></div>
        <div style="flex:1;background:#111827;border-radius:10px;padding:10px 14px;border:1px solid #e2e8f0;">
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            <span style="font-weight:700;color:{_CLR_PRIMARY};font-size:13px;">{saat_str}{bitis}</span>
            {_modul_badge(g.kaynak_modul)}
            {_durum_badge(g.durum)}
            {oncelik_badge}
        </div>
        <div style="font-size:13px;font-weight:600;color:#94A3B8;margin-top:4px;">{g.baslik}</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:2px;">{g.kaynak_tipi}{sorumlu_str}{konum_str}</div>
        </div></div>""", unsafe_allow_html=True)


def _modul_mini_istatistik(gorevler: list[PlanlanmisGorev]) -> None:
    """Modul bazli mini istatistik kartlari."""
    modul_counts = Counter(g.kaynak_modul for g in gorevler)
    mini_html = ""
    for modul, sayi in sorted(modul_counts.items(), key=lambda x: -x[1]):
        renk = MODUL_RENK.get(modul, "#64748b")
        ikon = MODUL_IKON.get(modul, "📋")
        mini_html += (f'<div style="background:{renk}12;border:1px solid {renk}30;border-radius:10px;'
                      f'padding:8px 14px;text-align:center;min-width:100px;">'
                      f'<div style="font-size:20px;font-weight:800;color:{renk};">{sayi}</div>'
                      f'<div style="font-size:10px;color:#64748b;">{ikon} {modul}</div></div>')
    if mini_html:
        st.markdown(f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0;">{mini_html}</div>',
                    unsafe_allow_html=True)


# ============================================================
# TAB 1: DASHBOARD
# ============================================================

def _render_dashboard(store: YTEDataStore):
    styled_section("Genel Bakış", "#0B0F19")

    # ── ZİRVE: Sabah Brifing (gömülü — tıkla aç/kapa) ──
    with st.expander("📅 Bugün Okulda Ne Var? — Sabah Brifing", expanded=False):
        try:
            from views._yte_zirve_features import render_sabah_brifing
            render_sabah_brifing(store)
        except ImportError:
            st.info("Sabah brifing modülü yüklü değil.")
        except Exception as _e:
            st.caption(f"Sabah brifing yüklenemedi: {_e}")

    # ── ZİRVE: Okul Sağlık Puanı ──
    try:
        from views._yte_zirve_features import render_okul_saglik_puani
        render_okul_saglik_puani()
    except ImportError:
        pass
    except Exception as _e:
        st.caption(f"Sağlık puanı yüklenemedi: {_e}")

    # ── ZİRVE: Hızlı İşlem Paneli ──
    try:
        from views._yte_zirve_features import render_quick_actions
        render_quick_actions(store)
    except ImportError:
        pass
    except Exception as _e:
        st.caption(f"Hızlı işlem paneli yüklenemedi: {_e}")

    today = date.today().isoformat()

    # Otomatik senkronizasyon - diger modullerden canli veri toplama
    gorevler = _otomatik_senkronize(today, store)

    toplam = len(gorevler)
    tamamlanan = sum(1 for g in gorevler if g.durum == "Tamamlandı")
    iptal = sum(1 for g in gorevler if g.durum == "Iptal")
    ertelenen = sum(1 for g in gorevler if g.durum == "Ertelendi")
    gelmeyen = sum(1 for g in gorevler if g.durum == "Gelmedi")
    oran = round(tamamlanan / toplam * 100, 1) if toplam > 0 else 0

    styled_stat_row([
        ("Planlanan", str(toplam), _CLR_BLUE, "📋"),
        ("Tamamlanan", str(tamamlanan), _CLR_GREEN, "✅"),
        ("İptal/Gelmeyen", str(iptal + gelmeyen), _CLR_RED, "❌"),
        ("Gerçekleşme", f"%{oran}", _CLR_GOLD, "📊"),
    ])

    # Gauge charts row - her zaman goster
    bekleyen = sum(1 for g in gorevler if g.durum == "Bekliyor")
    ertelenen_pct = round(ertelenen / toplam * 100, 1) if toplam > 0 else 0
    iptal_pct = round((iptal + gelmeyen) / toplam * 100, 1) if toplam > 0 else 0
    bekleyen_pct = round(bekleyen / toplam * 100, 1) if toplam > 0 else 0
    def _yte_gauge(val, mx, lbl, clr):
        pct = min(val / mx * 100, 100) if mx > 0 else 0
        arc = 141.37 * pct / 100
        return (f'<div style="background:#1e293b;border:1px solid {clr}30;border-radius:14px;'
                f'padding:18px 22px;margin:8px 0;box-shadow:0 2px 10px rgba(0,0,0,0.15);text-align:center">'
                f'<svg width="130" height="85" viewBox="0 0 110 85">'
                f'<path d="M 10 55 A 45 45 0 0 1 100 55" fill="none" stroke="#e2e8f0" stroke-width="8" stroke-linecap="round"/>'
                f'<path d="M 10 55 A 45 45 0 0 1 100 55" fill="none" stroke="{clr}" stroke-width="8" '
                f'stroke-linecap="round" stroke-dasharray="{arc} 141.37"/>'
                f'<text x="55" y="50" text-anchor="middle" font-size="18" font-weight="800" fill="#94A3B8">%{val}</text>'
                f'<text x="55" y="66" text-anchor="middle" font-size="8" fill="#64748b" font-weight="600">{lbl}</text>'
                f'<text x="10" y="75" text-anchor="middle" font-size="6" fill="#94a3b8">0</text>'
                f'<text x="100" y="75" text-anchor="middle" font-size="6" fill="#94a3b8">100</text>'
                f'</svg></div>')
    _gc1, _gc2, _gc3, _gc4 = st.columns(4)
    with _gc1:
        st.markdown(_yte_gauge(oran, 100, "Gerçekleşme", _CLR_GREEN), unsafe_allow_html=True)
    with _gc2:
        st.markdown(_yte_gauge(bekleyen_pct, 100, "Bekleyen", _CLR_BLUE), unsafe_allow_html=True)
    with _gc3:
        st.markdown(_yte_gauge(ertelenen_pct, 100, "Ertelenen", _CLR_ORANGE), unsafe_allow_html=True)
    with _gc4:
        st.markdown(_yte_gauge(iptal_pct, 100, "İptal", _CLR_RED), unsafe_allow_html=True)

    # Widget panel ayarlari
    try:
        from utils.ui_common import widget_paneli
        with st.expander("⚙️ Dashboard Widget Ayarları", expanded=False):
            widget_paneli()
    except Exception:
        pass

    if not gorevler:
        styled_info_banner("Bugün için modüllerden herhangi bir planlanan işlem bulunamadı.", banner_type="warning", icon="⚠️")
        return

    col1, col2 = st.columns(2)

    with col1:
        styled_section("Durum Dagilimi", _CLR_BLUE)
        durum_counts = Counter(g.durum for g in gorevler)
        labels = list(durum_counts.keys())
        values = list(durum_counts.values())
        colors = [GOREV_DURUM_RENK.get(l, "#94a3b8") for l in labels]
        fig = go.Figure(go.Pie(
            labels=labels, values=values,
            marker=dict(colors=colors, line=dict(color="#fff", width=2)),
            textinfo="label+value", textfont=dict(size=11),
        ))
        sc_pie(fig, height=300)
        st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)

    with col2:
        styled_section("Modül Dağılımı", _CLR_ORANGE)
        modul_counts = Counter(g.kaynak_modul for g in gorevler)
        m_labels = list(modul_counts.keys())
        m_values = list(modul_counts.values())
        m_colors = [MODUL_RENK.get(m, "#64748b") for m in m_labels]
        fig2 = go.Figure(go.Pie(
            labels=m_labels, values=m_values,
            marker=dict(colors=m_colors, line=dict(color="#fff", width=2)),
            textinfo="label+value", textfont=dict(size=11),
        ))
        sc_pie(fig2, height=300)
        st.plotly_chart(fig2, use_container_width=True, config=SC_CHART_CFG)

    # Haftalik trend (session-state cache, günde 1 kez yüklenir)
    styled_section("Haftalık Trend", _CLR_GREEN)
    _trend_key = f"yte_trend_{date.today().isoformat()}"
    if _trend_key not in st.session_state:
        tarihler = []
        oranlar = []
        for i in range(6, -1, -1):
            d = (date.today() - timedelta(days=i)).isoformat()
            r = store.find_by_field("raporlar", "tarih", d)
            tarihler.append(d[5:])
            if r:
                rapor = r[0] if isinstance(r[0], dict) else r[0].to_dict()
                oranlar.append(rapor.get("gerceklesme_orani", 0))
            else:
                oranlar.append(0)
        st.session_state[_trend_key] = (tarihler, oranlar)
    tarihler, oranlar = st.session_state[_trend_key]

    fig3 = go.Figure(go.Scatter(
        x=tarihler, y=oranlar, mode="lines+markers+text",
        text=[f"%{v}" for v in oranlar], textposition="top center",
        line=dict(color=_CLR_BLUE, width=3),
        marker=dict(size=10, color=_CLR_BLUE),
        textfont=dict(size=10, color=_CLR_BLUE),
    ))
    fig3.update_layout(
        height=250, margin=dict(t=20, b=30, l=40, r=20),
        yaxis=dict(range=[0, 105], title="Gerçekleşme %"),
        xaxis=dict(title=""),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Son gorevler tablosu
    styled_section("Bugünün Görevleri")
    rows = ""
    for g in sorted(gorevler, key=lambda x: x.saat or "99:99")[:20]:
        rows += f"""<tr>
        <td style="padding:6px 10px;font-weight:600;color:{_CLR_PRIMARY};">{g.saat or '-'}</td>
        <td style="padding:6px 10px;">{g.baslik}</td>
        <td style="padding:6px 10px;">{_modul_badge(g.kaynak_modul)}</td>
        <td style="padding:6px 10px;">{g.sorumlu or '-'}</td>
        <td style="padding:6px 10px;">{_durum_badge(g.durum)}</td></tr>"""
    if rows:
        st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead><tr style="background:#1A2035;">
        <th style="padding:8px 10px;text-align:left;color:#64748b;font-weight:600;">Saat</th>
        <th style="padding:8px 10px;text-align:left;color:#64748b;font-weight:600;">Baslik</th>
        <th style="padding:8px 10px;text-align:left;color:#64748b;font-weight:600;">Modul</th>
        <th style="padding:8px 10px;text-align:left;color:#64748b;font-weight:600;">Sorumlu</th>
        <th style="padding:8px 10px;text-align:left;color:#64748b;font-weight:600;">Durum</th>
        </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)


# ============================================================
# TAB 2: GUN BASI RAPORU
# ============================================================

def _render_gun_basi(store: YTEDataStore):
    """Ultra Premium Gun Basi Raporu — 33 modul kapsami + altın hero kart + canli timeline."""
    styled_section("Gün Başı Raporu", _CLR_BLUE)
    styled_info_banner(
        "Tum 33 modulden bugune ait planlanan tum islemler (randevu, sinav, toplanti, gorusme, "
        "etkinlik, post yayini, kocluk seansı, CEFR sinavi, SWOT olcumu, anket donemi vb.) "
        "otomatik toplanir. Saat 00:01'de yeni gunun calisma programi hazirdir.",
        banner_type="info", icon="📅")

    col1, col2 = st.columns([2, 1])
    with col1:
        secili_tarih = st.date_input("Tarih", value=date.today(), key="yte_gb_tarih")
    with col2:
        st.write("")
        st.write("")
        if st.button("Yenile", use_container_width=True, key="yte_gb_yenile"):
            _force_senkronize(secili_tarih.isoformat(), store)
            st.rerun()

    tarih_str = secili_tarih.isoformat()
    gorevler = _otomatik_senkronize(tarih_str, store)

    # ── ULTRA PREMIUM HERO KART ──
    try:
        dt = datetime.strptime(tarih_str, "%Y-%m-%d")
        from models.yonetim_ekran import _GUN_ADLARI
        gun_adi = _GUN_ADLARI.get(dt.weekday(), "")
        tarih_pretty = f"{dt.day:02d}.{dt.month:02d}.{dt.year}"
    except ValueError:
        gun_adi = ""
        tarih_pretty = tarih_str

    aktif_modul_set = set(g.kaynak_modul for g in gorevler) if gorevler else set()
    _TOPLAM_MODUL = 33
    aktif_modul_sayisi = len(aktif_modul_set)
    kapsama_yuzde = round(aktif_modul_sayisi / _TOPLAM_MODUL * 100, 1)
    kritik = sum(1 for g in gorevler if g.oncelik == "Kritik")
    yuksek = sum(1 for g in gorevler if g.oncelik == "Yuksek")
    erken_saat = next((g.saat for g in sorted(gorevler, key=lambda x: x.saat or "99:99") if g.saat), "—")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);
                border:2px solid #c9a84c;border-radius:20px;padding:24px 32px;margin:14px 0;
                box-shadow:0 8px 32px rgba(201,168,76,0.25),inset 0 1px 0 rgba(255,255,255,0.05);
                position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#6d4c41,#c9a84c,#e8d48b,#c9a84c,#6d4c41);"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px;">
            <div>
                <div style="font-size:11px;color:#c9a84c;font-weight:700;letter-spacing:3px;
                            text-transform:uppercase;margin-bottom:4px;">SmartCampus AI · Yönetim Tek Ekran</div>
                <div style="font-size:32px;font-weight:900;color:#fff;
                            font-family:Playfair Display,Georgia,serif;letter-spacing:-0.5px;">
                    Gün Başı Çalışma Programı</div>
                <div style="font-size:14px;color:#e8d48b;margin-top:6px;font-weight:600;">
                    📅 {tarih_pretty} · {gun_adi} &nbsp;|&nbsp; ⏰ İlk işlem: {erken_saat}</div>
            </div>
            <div style="text-align:center;background:rgba(201,168,76,0.12);border:1px solid #c9a84c;
                        border-radius:16px;padding:14px 26px;min-width:140px;">
                <div style="font-size:48px;font-weight:900;color:#c9a84c;
                            font-family:Playfair Display,Georgia,serif;line-height:1;">{len(gorevler)}</div>
                <div style="font-size:10px;color:#e8d48b;letter-spacing:2px;
                            text-transform:uppercase;margin-top:4px;">Toplam İş</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px;
                    padding-top:18px;border-top:1px solid rgba(201,168,76,0.2);">
            <div style="text-align:center;">
                <div style="font-size:24px;font-weight:800;color:#c9a84c;">{aktif_modul_sayisi}/{_TOPLAM_MODUL}</div>
                <div style="font-size:9px;color:#a1887f;text-transform:uppercase;letter-spacing:1.5px;margin-top:2px;">Aktif Modül</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:24px;font-weight:800;color:#10b981;">%{kapsama_yuzde}</div>
                <div style="font-size:9px;color:#a1887f;text-transform:uppercase;letter-spacing:1.5px;margin-top:2px;">Kapsama</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:24px;font-weight:800;color:#ef4444;">{kritik}</div>
                <div style="font-size:9px;color:#a1887f;text-transform:uppercase;letter-spacing:1.5px;margin-top:2px;">Kritik İş</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:24px;font-weight:800;color:#f97316;">{yuksek}</div>
                <div style="font-size:9px;color:#a1887f;text-transform:uppercase;letter-spacing:1.5px;margin-top:2px;">Yüksek Öncelik</div>
            </div>
        </div>
        <div style="position:absolute;bottom:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#6d4c41,#c9a84c,#e8d48b,#c9a84c,#6d4c41);"></div>
    </div>
    """, unsafe_allow_html=True)

    if not gorevler:
        styled_info_banner(
            "Bu tarih için 33 modülün hiçbirinden planlanan işlem bulunamadı. "
            "Diğer modüllerden tarihli görev/etkinlik ekleyince burada otomatik görünür.",
            banner_type="warning", icon="📭")
        return

    # Modul mini istatistik
    _modul_mini_istatistik(gorevler)

    # Timeline gorunumu
    styled_section(f"Günlük Çalışma Programı — {len(gorevler)} işlem · {aktif_modul_sayisi} modül")
    _gorev_timeline_html(gorevler)

    # Gün Başı PDF
    st.divider()
    rapor_engine = RaporUreticisi(store)
    pdf_bytes = rapor_engine.gun_basi_pdf_olustur(tarih_str, gorevler)
    if pdf_bytes:
        st.download_button(
            "📄 Gün Başı Raporu PDF İndir", pdf_bytes,
            file_name=f"gun_basi_raporu_{tarih_str}.pdf",
            mime="application/pdf", use_container_width=True, key="yte_gb_pdf")


# ============================================================
# TAB 3: GUN SONU RAPORU
# ============================================================

def _render_modul_islemleri_html(modul_islemler: dict[str, list[dict]]) -> None:
    """Modul bazli gunluk islemleri gorsel kartlarla goster."""
    if not modul_islemler:
        styled_info_banner("Bu tarih için modullerde islem bulunamadı.", banner_type="warning", icon="⚠️")
        return

    # 33 modul kapsami — GunlukIslemToplayici cikti anahtarlari ile birebir
    modul_sira = [
        # Akademik (9)
        "Akademik Takip", "Olcme Degerlendirme", "Rehberlik",
        "Okul Sagligi", "Yabanci Dil", "Kisisel Dil Gelisimi",
        "AI Bireysel Egitim", "Erken Uyari", "Egitim Koclugu",
        # Kurum & Operasyon (9)
        "Insan Kaynaklari", "Halkla Iliskiler", "Sosyal Medya",
        "Butce Gelir Gider", "Toplanti ve Kurullar", "Randevu ve Ziyaretci",
        "Kayit Modulu", "Kurum Hizmetleri", "KOI",
        # Etkinlik & Destek (8)
        "Sosyal Etkinlik", "Kutuphane", "Dijital Kutuphane",
        "Destek Hizmetleri", "Tuketim Demirbas", "Sivil Savunma",
        "Mezunlar", "SWOT Analizi",
        # Analiz (1)
        "Veli Memnuniyet",
    ]
    for modul in modul_sira:
        items = modul_islemler.get(modul)
        if not items:
            continue
        renk = MODUL_RENK.get(modul, "#64748b")
        ikon = MODUL_IKON.get(modul, "📋")
        modul_toplam = sum(i["sayi"] for i in items)
        items_html = ""
        for item in items:
            detay_str = ""
            if item.get("detaylar"):
                detay_parts = [f'<span style="color:#94a3b8;font-size:10px;">• {d}</span>' for d in item["detaylar"][:4]]
                detay_str = '<div style="margin-left:8px;">' + ''.join(detay_parts) + '</div>'
            items_html += (
                f'<div style="display:flex;align-items:center;gap:8px;padding:4px 0;">'
                f'<span style="background:{renk};color:#fff;padding:2px 8px;border-radius:6px;'
                f'font-size:12px;font-weight:700;min-width:32px;text-align:center;">{item["sayi"]}</span>'
                f'<span style="font-size:12px;font-weight:600;color:#94A3B8;">{item["baslik"]}</span>'
                f'</div>{detay_str}')
        st.markdown(
            f'<div style="background:#111827;border-left:4px solid {renk};border-radius:0 12px 12px 0;'
            f'padding:12px 16px;margin-bottom:10px;">'
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
            f'<span style="font-size:16px;">{ikon}</span>'
            f'<span style="font-size:14px;font-weight:700;color:{renk};">{modul}</span>'
            f'<span style="background:{renk}18;color:{renk};padding:2px 10px;border-radius:8px;'
            f'font-size:11px;font-weight:700;">{modul_toplam} islem</span></div>'
            f'{items_html}</div>', unsafe_allow_html=True)


def _render_gun_sonu(store: YTEDataStore):
    """Ultra Premium Gun Sonu Raporu — 33 modul kapsami + altın hero kart + tum islem ozeti."""
    styled_section("Gün Sonu Raporu", _CLR_ORANGE)
    styled_info_banner(
        "Tum 33 modulde gun icinde yapilan tum islemler (not girisi, odunc, gider, revir ziyareti, "
        "post yayini, kocluk gorusmesi, anket cevabi, SWOT madde, CEFR sonucu, adaptif tekrar vb.) "
        "otomatik toplanir. Kurumsal formatta PDF rapor + AI degerlendirme + e-posta gonderimi yapilir.",
        banner_type="warning", icon="📊")

    secili_tarih = st.date_input("Tarih", value=date.today(), key="yte_gs_tarih")
    tarih_str = secili_tarih.isoformat()

    # Otomatik senkronize - planlanan gorevler
    gorevler = _otomatik_senkronize(tarih_str, store)

    # Modul islemlerini topla
    islem_cache_key = f"yte_islem_{tarih_str}"
    if islem_cache_key not in st.session_state:
        islem_toplayici = GunlukIslemToplayici(tarih_str)
        st.session_state[islem_cache_key] = islem_toplayici.topla()
    modul_islemler = st.session_state[islem_cache_key]
    toplam_islem = sum(i["sayi"] for items in modul_islemler.values() for i in items)

    # ── ULTRA PREMIUM HERO KART (Gun Sonu) ──
    try:
        dt = datetime.strptime(tarih_str, "%Y-%m-%d")
        from models.yonetim_ekran import _GUN_ADLARI
        gun_adi = _GUN_ADLARI.get(dt.weekday(), "")
        tarih_pretty = f"{dt.day:02d}.{dt.month:02d}.{dt.year}"
    except ValueError:
        gun_adi = ""
        tarih_pretty = tarih_str

    _TOPLAM_MODUL = 33
    aktif_modul_islem = len(modul_islemler)
    aktif_modul_plan = len(set(g.kaynak_modul for g in gorevler)) if gorevler else 0
    aktif_modul_set = set(modul_islemler.keys()) | set(g.kaynak_modul for g in gorevler)
    kapsama_yuzde = round(len(aktif_modul_set) / _TOPLAM_MODUL * 100, 1)

    tamam = sum(1 for g in gorevler if g.durum == "Tamamlandi")
    iptal = sum(1 for g in gorevler if g.durum == "Iptal")
    gerceklesme = round(tamam / max(len(gorevler), 1) * 100, 1) if gorevler else 0

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#3e1f1c 0%,#5d2d27 50%,#7a3a32 100%);
                border:2px solid #c9a84c;border-radius:20px;padding:24px 32px;margin:14px 0;
                box-shadow:0 8px 32px rgba(201,168,76,0.25),inset 0 1px 0 rgba(255,255,255,0.05);
                position:relative;overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#6d4c41,#c9a84c,#e8d48b,#c9a84c,#6d4c41);"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px;">
            <div>
                <div style="font-size:11px;color:#c9a84c;font-weight:700;letter-spacing:3px;
                            text-transform:uppercase;margin-bottom:4px;">SmartCampus AI · Yönetim Tek Ekran</div>
                <div style="font-size:32px;font-weight:900;color:#fff;
                            font-family:Playfair Display,Georgia,serif;letter-spacing:-0.5px;">
                    Gün Sonu Faaliyet Raporu</div>
                <div style="font-size:14px;color:#e8d48b;margin-top:6px;font-weight:600;">
                    📅 {tarih_pretty} · {gun_adi} &nbsp;|&nbsp; 📦 Toplam: {toplam_islem} işlem · {len(gorevler)} planlanan</div>
            </div>
            <div style="text-align:center;background:rgba(201,168,76,0.12);border:1px solid #c9a84c;
                        border-radius:16px;padding:14px 26px;min-width:140px;">
                <div style="font-size:48px;font-weight:900;color:#c9a84c;
                            font-family:Playfair Display,Georgia,serif;line-height:1;">%{gerceklesme}</div>
                <div style="font-size:10px;color:#e8d48b;letter-spacing:2px;
                            text-transform:uppercase;margin-top:4px;">Gerçekleşme</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:20px;
                    padding-top:18px;border-top:1px solid rgba(201,168,76,0.2);">
            <div style="text-align:center;">
                <div style="font-size:24px;font-weight:800;color:#c9a84c;">{len(aktif_modul_set)}/{_TOPLAM_MODUL}</div>
                <div style="font-size:9px;color:#a1887f;text-transform:uppercase;letter-spacing:1.5px;margin-top:2px;">Aktif Modül</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:24px;font-weight:800;color:#10b981;">%{kapsama_yuzde}</div>
                <div style="font-size:9px;color:#a1887f;text-transform:uppercase;letter-spacing:1.5px;margin-top:2px;">Kapsama</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:24px;font-weight:800;color:#3b82f6;">{toplam_islem}</div>
                <div style="font-size:9px;color:#a1887f;text-transform:uppercase;letter-spacing:1.5px;margin-top:2px;">Modül İşlem</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:24px;font-weight:800;color:#10b981;">{tamam}</div>
                <div style="font-size:9px;color:#a1887f;text-transform:uppercase;letter-spacing:1.5px;margin-top:2px;">Tamamlanan</div>
            </div>
            <div style="text-align:center;">
                <div style="font-size:24px;font-weight:800;color:#ef4444;">{iptal}</div>
                <div style="font-size:9px;color:#a1887f;text-transform:uppercase;letter-spacing:1.5px;margin-top:2px;">İptal/Gelmedi</div>
            </div>
        </div>
        <div style="position:absolute;bottom:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#6d4c41,#c9a84c,#e8d48b,#c9a84c,#6d4c41);"></div>
    </div>
    """, unsafe_allow_html=True)

    # Klasik ozet stat (alt destek)
    styled_stat_row([
        ("Planlanan Görev", str(len(gorevler)), _CLR_BLUE, "📋"),
        ("Modül İşlemi", str(toplam_islem), "#7c3aed", "📦"),
        ("Aktif Modul (33'ten)", f"{len(aktif_modul_set)}/{_TOPLAM_MODUL}", _CLR_GREEN, "✅"),
        ("Kapsama", f"%{kapsama_yuzde}", "#c9a84c", "🎯"),
    ])

    # Alt sekmeler: Planlanan Gorevler | Modul Islemleri | Rapor & PDF
    sub = st.tabs(["📋 Planlanan Görev Durumları", "📦 Modül Bazlı İşlemler", "📄 Rapor Oluştur & Gönder"])

    # --- Alt Sekme 1: Planlanan Gorev Durumlari ---
    with sub[0]:
        if not gorevler:
            styled_info_banner("Bu tarih için planlanan gorev bulunamadı.", banner_type="warning", icon="⚠️")
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Tümü Tamamlandı", key="yte_hepsi_tamam"):
                    for g in gorevler:
                        g.durum = "Tamamlandı"
                        g.updated_at = datetime.now().isoformat()
                        store.upsert("gorevler", g)
                    st.rerun()
            with col_b:
                if st.button("Durumlari Kaydet", key="yte_durum_kaydet", type="primary"):
                    for g in gorevler:
                        key = f"yte_d_{g.id}"
                        nkey = f"yte_n_{g.id}"
                        if key in st.session_state:
                            g.durum = st.session_state[key]
                        if nkey in st.session_state:
                            g.gerceklesme_notu = st.session_state[nkey]
                        g.updated_at = datetime.now().isoformat()
                        store.upsert("gorevler", g)
                    st.success("Durumlar kaydedildi!")
                    st.rerun()

            for g in sorted(gorevler, key=lambda x: x.saat or "99:99"):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    renk = MODUL_RENK.get(g.kaynak_modul, "#64748b")
                    saat = g.saat or "--:--"
                    st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;">
                    <span style="color:{renk};font-weight:700;">{saat}</span>
                    <span style="font-size:12px;">{g.baslik}</span>
                    {_modul_badge(g.kaynak_modul)}</div>""", unsafe_allow_html=True)
                with col2:
                    idx = GOREV_DURUMLARI.index(g.durum) if g.durum in GOREV_DURUMLARI else 0
                    st.selectbox("Durum", GOREV_DURUMLARI, index=idx,
                                 key=f"yte_d_{g.id}", label_visibility="collapsed")
                with col3:
                    st.text_input("Not", value=g.gerceklesme_notu, key=f"yte_n_{g.id}",
                                  label_visibility="collapsed", placeholder="Not...")

    # --- Alt Sekme 2: Modul Bazli Islemler ---
    with sub[1]:
        styled_section("Gün İçinde Yapılan Tüm İşlemler", "#7c3aed")
        styled_info_banner(
            f"Tüm modullerde {tarih_str} tarihinde kaydedilen islemler otomatik olarak toplanmistir. "
            f"Toplam {toplam_islem} islem, {len(modul_islemler)} modulde.",
            banner_type="info", icon="📦")

        if st.button("İşlemleri Yenile", key="yte_islem_yenile"):
            if islem_cache_key in st.session_state:
                del st.session_state[islem_cache_key]
            st.rerun()

        _render_modul_islemleri_html(modul_islemler)

    # --- Alt Sekme 3: Rapor Olustur & Gonder ---
    with sub[2]:
        styled_section("Rapor Oluştur ve Gönder")

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            rapor_olustur = st.button("Rapor Oluştur", use_container_width=True,
                                       type="primary", key="yte_rapor_btn")
        with col_r2:
            ai_degerlendirme_btn = st.button("AI Değerlendirme", use_container_width=True, key="yte_ai_btn")
        with col_r3:
            eposta_btn = st.button("E-posta Gönder", use_container_width=True, key="yte_eposta_btn")

        rapor_engine = RaporUreticisi(store)

        if rapor_olustur:
            gorevler_r = _load_gorevler_for_date(tarih_str, store)

            rapor = rapor_engine.gunluk_rapor_olustur(tarih_str, gorevler_r, "gun_sonu")
            store.upsert("raporlar", rapor)
            st.success(f"Kurumsal gun sonu raporu oluşturuldu! "
                       f"Görev gerceklesme: %{rapor.gerceklesme_orani} | "
                       f"Modul islemleri: {toplam_islem}")

            # Grafikler
            col1, col2 = st.columns(2)
            with col1:
                durum_counts = Counter(g.durum for g in gorevler_r)
                if durum_counts:
                    labels = list(durum_counts.keys())
                    values = list(durum_counts.values())
                    colors = [GOREV_DURUM_RENK.get(l, "#94a3b8") for l in labels]
                    fig = go.Figure(go.Pie(labels=labels, values=values,
                                           marker=dict(colors=colors, line=dict(color="#fff", width=2)),
                                           textinfo="label+percent"))
                    sc_pie(fig, height=300)
                    st.plotly_chart(fig, use_container_width=True, config=SC_CHART_CFG)

            with col2:
                if modul_islemler:
                    m_names = list(modul_islemler.keys())[:10]
                    m_counts = [sum(i["sayi"] for i in modul_islemler[m]) for m in m_names]
                    m_colors = [MODUL_RENK.get(m, "#64748b") for m in m_names]
                    fig2 = go.Figure(go.Bar(
                        y=m_names, x=m_counts, orientation="h",
                        marker_color=SC_COLORS[0],
                        text=m_counts, textposition="outside",
                    ))
                    sc_bar(fig2, height=300, horizontal=True)
                    st.plotly_chart(fig2, use_container_width=True, config=SC_CHART_CFG)

            # Kurumsal PDF indirme
            pdf_bytes = rapor_engine.gun_sonu_pdf_olustur(rapor, gorevler_r)
            if pdf_bytes:
                st.download_button("Kurumsal Gün Sonu Raporu PDF Indir", pdf_bytes,
                                   file_name=f"gun_sonu_raporu_{tarih_str}.pdf",
                                   mime="application/pdf", use_container_width=True)

        if ai_degerlendirme_btn:
            gorevler_r = _load_gorevler_for_date(tarih_str, store)
            rapor_list = store.find_by_field("raporlar", "tarih", tarih_str)
            if rapor_list:
                rapor_obj = GunlukRapor.from_dict(rapor_list[-1]) if isinstance(rapor_list[-1], dict) else rapor_list[-1]
            else:
                rapor_obj = rapor_engine.gunluk_rapor_olustur(tarih_str, gorevler_r, "gun_sonu")

            with st.spinner("AI degerlendirme hazirlaniyor..."):
                degerlendirme = rapor_engine.ai_degerlendirme(rapor_obj, gorevler_r)

            if degerlendirme:
                rapor_obj.ai_degerlendirme = degerlendirme
                store.upsert("raporlar", rapor_obj)
                try:
                    from utils.report_utils import ai_recommendations_html
                    st.markdown(ai_recommendations_html([
                        {"icon": "🤖", "title": "AI Günlük Değerlendirme",
                         "text": degerlendirme.replace("\n", "<br>"), "color": "#7c3aed"},
                    ]), unsafe_allow_html=True)
                except Exception:
                    st.info(degerlendirme)
            else:
                st.warning("AI degerlendirme olusturulamadi. OpenAI API anahtarini kontrol edin.")

        if eposta_btn:
            gorevler_r = _load_gorevler_for_date(tarih_str, store)
            rapor_list = store.find_by_field("raporlar", "tarih", tarih_str)
            if not rapor_list:
                st.warning("Önce rapor olusturun.")
            else:
                rapor_obj = GunlukRapor.from_dict(rapor_list[-1]) if isinstance(rapor_list[-1], dict) else rapor_list[-1]
                pdf_bytes = rapor_engine.gun_sonu_pdf_olustur(rapor_obj, gorevler_r)
                with st.spinner("E-postalar gonderiliyor..."):
                    sonuclar = rapor_engine.eposta_gonder(rapor_obj, pdf_bytes)
                if sonuclar:
                    for eposta, ok, msg in sonuclar:
                        if ok:
                            st.success(f"{eposta}: Gonderildi")
                        else:
                            st.error(f"{eposta}: {msg}")
                    rapor_obj.eposta_gonderildi = True
                    rapor_obj.eposta_gonderim_zamani = datetime.now().isoformat()
                    store.upsert("raporlar", rapor_obj)
                else:
                    st.warning("Aktif e-posta alicisi bulunamadı. E-posta Ayarları sekmesinden alici ekleyin.")

    # --- AI Önerileri (tüm alt sekmelerin altında) ---
    st.divider()
    styled_section("AI Önerileri", "#8b5cf6")

    # Kayıtlı raporu kontrol et
    rapor_list = store.find_by_field("raporlar", "tarih", tarih_str)
    kayitli_ai = ""
    if rapor_list:
        rapor_obj = GunlukRapor.from_dict(rapor_list[-1]) if isinstance(rapor_list[-1], dict) else rapor_list[-1]
        kayitli_ai = rapor_obj.ai_degerlendirme or ""

    # Session-state ile AI sonucu cache
    ai_cache_key = f"yte_ai_oneri_{tarih_str}"
    if kayitli_ai:
        st.session_state[ai_cache_key] = kayitli_ai

    if ai_cache_key in st.session_state and st.session_state[ai_cache_key]:
        try:
            from utils.report_utils import ai_recommendations_html
            ai_text = st.session_state[ai_cache_key]
            st.markdown(ai_recommendations_html([
                {"icon": "🤖", "title": "Günün Genel Değerlendirmesi",
                 "text": ai_text.replace("\n", "<br>"), "color": "#7c3aed"},
            ]), unsafe_allow_html=True)
        except Exception:
            st.info(st.session_state[ai_cache_key])
    else:
        styled_info_banner(
            "AI değerlendirmesi henüz oluşturulmadı. Aşağıdaki buton ile oluşturabilirsiniz.", banner_type="info", icon="🤖")
        if st.button("AI Önerileri Oluştur", key="yte_ai_oneri_btn", type="primary"):
            rapor_engine = RaporUreticisi(store)
            gorevler_r = _load_gorevler_for_date(tarih_str, store)
            if rapor_list:
                rapor_obj = GunlukRapor.from_dict(rapor_list[-1]) if isinstance(rapor_list[-1], dict) else rapor_list[-1]
            else:
                rapor_obj = rapor_engine.gunluk_rapor_olustur(tarih_str, gorevler_r, "gun_sonu")
                store.upsert("raporlar", rapor_obj)

            with st.spinner("AI önerileri hazırlanıyor..."):
                degerlendirme = rapor_engine.ai_degerlendirme(rapor_obj, gorevler_r)

            if degerlendirme:
                rapor_obj.ai_degerlendirme = degerlendirme
                store.upsert("raporlar", rapor_obj)
                st.session_state[ai_cache_key] = degerlendirme
                st.rerun()
            else:
                st.warning("AI değerlendirme oluşturulamadı. OpenAI API anahtarını kontrol edin.")


# ============================================================
# TAB 4: PERFORMANS OLCUMLERI
# ============================================================

def _render_performans(store: YTEDataStore):
    styled_section("Performans Olcumleri", _CLR_GREEN)

    donem = st.radio("Donem", ["Son 7 Gün", "Son 30 Gün", "Son 90 Gün", "Tarih Araligi"],
                     horizontal=True, key="yte_perf_donem")

    raporlar_raw = store.load_objects("raporlar")

    if donem == "Tarih Araligi":
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            baslangic = st.date_input("Başlangıç Tarihi", value=date.today() - timedelta(days=30),
                                       key="yte_perf_bas")
        with col_t2:
            bitis = st.date_input("Bitis Tarihi", value=date.today(), key="yte_perf_bit")
        bas_str = baslangic.isoformat()
        bit_str = bitis.isoformat()
        raporlar = [r for r in raporlar_raw if bas_str <= getattr(r, "tarih", "") <= bit_str]
    else:
        gun_sayisi = {"Son 7 Gün": 7, "Son 30 Gün": 30, "Son 90 Gün": 90}[donem]
        cutoff = (date.today() - timedelta(days=gun_sayisi)).isoformat()
        raporlar = [r for r in raporlar_raw if getattr(r, "tarih", "") >= cutoff]

    if not raporlar:
        styled_info_banner("Secili donemde rapor bulunamadı.", banner_type="warning", icon="⚠️")
        return

    ort_oran = sum(r.gerceklesme_orani for r in raporlar) / len(raporlar)
    toplam_plan = sum(r.planlanan_sayi for r in raporlar)
    toplam_gercek = sum(r.gerceklesen_sayi for r in raporlar)
    toplam_iptal = sum(r.iptal_sayi for r in raporlar)

    styled_stat_row([
        ("Ortalama Oran", f"%{ort_oran:.1f}", _CLR_GREEN, "📊"),
        ("Toplam Planlanan", str(toplam_plan), _CLR_BLUE, "📋"),
        ("Toplam Gerçekleşen", str(toplam_gercek), _CLR_GREEN, "✅"),
        ("Toplam İptal", str(toplam_iptal), _CLR_RED, "❌"),
    ])

    styled_section("Gerçekleşme Oranı Trendi")
    raporlar_sorted = sorted(raporlar, key=lambda r: r.tarih)
    fig = go.Figure(go.Scatter(
        x=[r.tarih[5:] for r in raporlar_sorted],
        y=[r.gerceklesme_orani for r in raporlar_sorted],
        mode="lines+markers", line=dict(color=_CLR_BLUE, width=3),
        marker=dict(size=8, color=_CLR_BLUE),
    ))
    fig.update_layout(height=300, margin=dict(t=10, b=30, l=40, r=10),
                      yaxis=dict(range=[0, 105], title="Gerçekleşme %"),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    styled_section("Modul Performans Sıralamasi")
    modul_stats: dict[str, dict] = {}
    for r in raporlar:
        for modul, ozet in (r.modul_ozet or {}).items():
            if modul not in modul_stats:
                modul_stats[modul] = {"planlanan": 0, "tamamlanan": 0}
            modul_stats[modul]["planlanan"] += ozet.get("planlanan", 0)
            modul_stats[modul]["tamamlanan"] += ozet.get("tamamlanan", 0)

    if modul_stats:
        sirali = sorted(modul_stats.items(), key=lambda x: x[1]["tamamlanan"], reverse=True)
        m_names = [s[0] for s in sirali]
        m_plan = [s[1]["planlanan"] for s in sirali]
        m_done = [s[1]["tamamlanan"] for s in sirali]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Planlanan", y=m_names, x=m_plan, orientation="h",
                              marker_color=SC_COLORS[0], text=m_plan, textposition="outside"))
        fig2.add_trace(go.Bar(name="Tamamlanan", y=m_names, x=m_done, orientation="h",
                              marker_color=SC_COLORS[1], text=m_done, textposition="outside"))
        fig2.update_layout(barmode="group", legend=dict(orientation="h", y=-0.15))
        sc_bar(fig2, height=max(250, len(m_names) * 40), horizontal=True)
        st.plotly_chart(fig2, use_container_width=True, config=SC_CHART_CFG)


# ============================================================
# TAB 5: MODUL OZETLERI
# ============================================================

@st.fragment
def _render_modul_ozetleri():
    styled_section("Modül Özetleri", _CLR_BLUE)
    styled_info_banner(
        "SmartCampus AI yazilimindaki tum modullerin guncel anahtar metrikleri. "
        "Her modul otomatik olarak kendi DataStore'undan veri ceker.", banner_type="info", icon="📋")

    # Session-state cache: 66 JSON yüklemesi sadece ilk açılışta
    _kpi_cache = "yte_modul_kpis"
    if _kpi_cache not in st.session_state:
        with st.spinner("Modül verileri yükleniyor..."):
            st.session_state[_kpi_cache] = ModulOzetleyici().tum_modul_kpi()
    kpis = st.session_state[_kpi_cache]

    if st.button("Verileri Yenile", key="yte_kpi_yenile"):
        st.session_state.pop(_kpi_cache, None)
        st.rerun(scope="fragment")

    # Tum modullerin sabit sirasi (33 modul kapsami)
    MODUL_SIRA = [
        # Akademik (9)
        "Akademik Takip", "Olcme Degerlendirme", "Rehberlik",
        "Okul Sagligi", "Yabanci Dil", "Kisisel Dil Gelisimi",
        "AI Bireysel Egitim", "Erken Uyari", "Egitim Koclugu",
        # Kurumsal (9)
        "KOI", "Halkla Iliskiler", "Sosyal Medya",
        "Insan Kaynaklari", "Butce Gelir Gider", "Toplanti ve Kurullar",
        "Randevu ve Ziyaretci", "Kayit Modulu", "Kurum Hizmetleri",
        # Operasyon & Etkinlik (8)
        "Sosyal Etkinlik", "Kutuphane", "Dijital Kutuphane",
        "Tuketim Demirbas", "Destek Hizmetleri", "Sivil Savunma",
        "Mezunlar", "Akademik Takvim",
        # Analiz (2)
        "SWOT Analizi", "Veli Memnuniyet",
        # Icerik Platformlari (5)
        "AI Treni", "STEAM Merkezi", "Matematik Koyu", "Sanat Sokagi", "Bilisim Vadisi",
    ]

    # Ozet istatistikler
    veri_olan = sum(1 for m in MODUL_SIRA if kpis.get(m))
    toplam_modul = len(MODUL_SIRA)
    toplam_kayit = sum(
        sum(v for v in d.values() if isinstance(v, (int, float)))
        for d in kpis.values()
    )
    styled_stat_row([
        ("Toplam Modul", str(toplam_modul), _CLR_BLUE, "📦"),
        ("Aktif Veri", str(veri_olan), _CLR_GREEN, "✅"),
        ("Veri Yok", str(toplam_modul - veri_olan), _CLR_GRAY, "⚪"),
        ("Toplam Kayit", f"{toplam_kayit:,}", "#7c3aed", "📊"),
    ])

    # Donut grafik (tek, kompakt)
    modul_kayit = {}
    for modul in MODUL_SIRA:
        data = kpis.get(modul)
        if data:
            toplam = sum(v for v in data.values() if isinstance(v, (int, float)))
            if toplam > 0:
                modul_kayit[modul] = toplam
    if modul_kayit:
        m_labels = list(modul_kayit.keys())
        m_values = list(modul_kayit.values())
        fig_kayit = go.Figure(go.Pie(
            labels=m_labels, values=m_values,
            marker=dict(colors=SC_COLORS[:len(m_labels)], line=dict(color="#fff", width=1)),
            textinfo="label+percent", textfont=dict(size=9), hole=0.4,
        ))
        fig_kayit.update_layout(
            title=dict(text="Modul Bazli Kayit Dagilimi", font=dict(size=13)),
            height=320, margin=dict(t=40, b=10, l=10, r=10),
            legend=dict(font=dict(size=9), orientation="h", y=-0.15),
        )
        sc_pie(fig_kayit, height=320)
        st.plotly_chart(fig_kayit, use_container_width=True, config=SC_CHART_CFG)

    st.divider()

    # Kompakt 3-sutun grid kartlar
    _mo_cols = st.columns(3)
    for _mo_idx, modul in enumerate(MODUL_SIRA):
        renk = MODUL_RENK.get(modul, "#64748b")
        ikon = MODUL_IKON.get(modul, "📋")
        data = kpis.get(modul)

        with _mo_cols[_mo_idx % 3]:
            if not data:
                st.markdown(
                    f'<div style="background:#94A3B8;border:1px solid rgba(255,255,255,.06);'
                    f'border-radius:12px;padding:14px;margin-bottom:10px;border-left:3px solid #475569;'
                    f'opacity:.6">'
                    f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">'
                    f'<span style="font-size:1.1rem">{ikon}</span>'
                    f'<span style="font-size:.82rem;font-weight:700;color:#94a3b8">{modul}</span>'
                    f'</div>'
                    f'<div style="font-size:.7rem;color:#64748b">Veri yok</div></div>',
                    unsafe_allow_html=True)
                continue

            metrik_items = []
            for key, val in data.items():
                label = key.replace("_", " ").title()
                if isinstance(val, float):
                    val_str = f"{val:,.0f}" if val >= 1000 else f"{val:,.1f}"
                elif isinstance(val, int) and val >= 1000:
                    val_str = f"{val:,}"
                else:
                    val_str = str(val)
                metrik_items.append(
                    f'<div style="display:flex;justify-content:space-between;padding:2px 0">'
                    f'<span style="font-size:.7rem;color:#94a3b8">{label}</span>'
                    f'<span style="font-size:.75rem;font-weight:700;color:#e2e8f0">{val_str}</span></div>'
                )
            metrik_html = "".join(metrik_items)
            toplam_val = sum(v for v in data.values() if isinstance(v, (int, float)))

            st.markdown(
                f'<div style="background:linear-gradient(160deg,#94A3B8,#0B0F19);'
                f'border:1px solid rgba(255,255,255,.06);border-radius:12px;'
                f'padding:14px;margin-bottom:10px;border-left:3px solid {renk}">'
                f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:8px">'
                f'<span style="font-size:1.1rem">{ikon}</span>'
                f'<span style="font-size:.82rem;font-weight:700;color:#1A2035">{modul}</span>'
                f'<span style="margin-left:auto;background:{renk}20;color:{renk};'
                f'padding:1px 7px;border-radius:6px;font-size:.65rem;font-weight:700">'
                f'{toplam_val:,.0f}</span>'
                f'</div>{metrik_html}</div>',
                unsafe_allow_html=True)


# ============================================================
# TAB 6: E-POSTA AYARLARI
# ============================================================

def _render_eposta_ayarlari(store: YTEDataStore):
    styled_section("E-posta Alicilari", _CLR_BLUE)
    styled_info_banner(
        "Gün sonu raporlari saat 19:00'da tanimli e-posta adreslerine PDF olarak gonderilir. "
        "Otomatik zamanlama için Windows Görev Zamanlayici veya cron kullanabilirsiniz.", banner_type="info", icon="📧")

    alicilar = store.load_objects("eposta_alicilari")
    if alicilar:
        rows = ""
        for a in alicilar:
            aktif_badge = ('<span style="color:#10b981;font-weight:700;">Aktif</span>'
                           if a.aktif else '<span style="color:#94a3b8;">Pasif</span>')
            rows += f"""<tr>
            <td style="padding:6px 10px;">{a.ad_soyad}</td>
            <td style="padding:6px 10px;">{a.eposta}</td>
            <td style="padding:6px 10px;">{a.rol}</td>
            <td style="padding:6px 10px;">{aktif_badge}</td></tr>"""
        st.markdown(f"""<table style="width:100%;border-collapse:collapse;font-size:12px;">
        <thead><tr style="background:#1A2035;">
        <th style="padding:8px 10px;text-align:left;color:#64748b;">Ad Soyad</th>
        <th style="padding:8px 10px;text-align:left;color:#64748b;">E-posta</th>
        <th style="padding:8px 10px;text-align:left;color:#64748b;">Rol</th>
        <th style="padding:8px 10px;text-align:left;color:#64748b;">Durum</th>
        </tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)

        sil_sec = st.selectbox("Alici Sil", [""] + [a.ad_soyad for a in alicilar], key="yte_ea_sil")
        if sil_sec and st.button("Sil", key="yte_ea_sil_btn"):
            for a in alicilar:
                if a.ad_soyad == sil_sec:
                    store.delete_by_id("eposta_alicilari", a.id)
                    st.success(f"{sil_sec} silindi.")
                    st.rerun()

    styled_section("Yeni Alici Ekle")
    with st.form("yte_yeni_alici"):
        c1, c2 = st.columns(2)
        with c1:
            ad = st.text_input("Ad Soyad")

            rol = st.text_input("Rol", placeholder="Orn: Mudur, Yonetici")

        with c2:
            eposta = st.text_input("E-posta")

            aktif = st.checkbox("Aktif", value=True)

        submitted = st.form_submit_button("Ekle", use_container_width=True)

    if submitted and ad and eposta:
        yeni = EpostaAlici(ad_soyad=ad, eposta=eposta, aktif=aktif, rol=rol)
        store.upsert("eposta_alicilari", yeni)
        st.success(f"{ad} eklendi!")
        st.rerun()

    styled_section("Test")
    if st.button("Test E-postasi Gonder", key="yte_test_email"):
        alicilar = store.load_objects("eposta_alicilari")
        aktif_alicilar = [a for a in alicilar if a.aktif]
        if not aktif_alicilar:
            st.warning("Aktif alici yok.")
        else:
            try:
                from utils.messaging import send_email
                for a in aktif_alicilar:
                    ok, msg = send_email(a.eposta, "SmartCampus AI - Test", "Bu bir test e-postasıdır.")
                    if ok:
                        st.success(f"{a.eposta}: OK")
                    else:
                        st.error(f"{a.eposta}: {msg}")
            except Exception as e:
                st.error(f"Hata: {e}")


# ============================================================
# TAB 7: RAPORLAR (GECMIS)
# ============================================================

@st.fragment
def _render_raporlar(store: YTEDataStore):
    styled_section("Raporlar", _CLR_BLUE)
    styled_info_banner(
        "Tüm modullerin rapor ozetlerini tek ekrandan goruntuleyebilir, "
        "gun basi/gun sonu gecmis raporlarinizi inceleyebilir ve PDF olarak indirebilirsiniz.", banner_type="info", icon="📄")

    try:
        from utils.ui_common import sesli_rapor_okuma
        sesli_rapor_okuma("Yonetim rapor ozeti: Tum modullerin guncel durumu normal. Gorev tamamlanma oranlari yuzde seksen.", "yte_rapor")
    except ImportError:
        pass
    except Exception as _e:
        st.caption(f"Sesli rapor yüklenemedi: {_e}")

    try:
        from utils.ui_common import ai_haftalik_bulten
        ai_haftalik_bulten()
    except ImportError:
        pass

    sub = st.tabs(["📋 Modül Raporları", "📜 Geçmiş Günlük Raporlar", "📝 Sözleşme Raporları"])

    # --- Alt Sekme 1: Modul Raporlari ---
    with sub[0]:
        _render_modul_raporlari()

    # --- Alt Sekme 2: Gecmis Gunluk Raporlar ---
    with sub[1]:
        _render_gecmis_raporlar(store)

    # --- Alt Sekme 3: Sozlesme Raporlari ---
    with sub[2]:
        _render_sozlesme_raporlari()


def _render_modul_raporlari():
    """Tum modullerin rapor ozetlerini alt alta goster."""
    styled_section("Tüm Modul Rapor Özetleri", "#7c3aed")
    styled_info_banner(
        "SmartCampus AI yazilimindaki tum modullerin guncel rapor verileri "
        "asagida modul basliklari altinda listelenmektedir.", banner_type="info", icon="📊")

    cache_key = "yte_modul_raporlari"
    if cache_key not in st.session_state:
        toplayici = ModulRaporToplayici()
        st.session_state[cache_key] = toplayici.tum_modul_raporlari()
    modul_raporlari = st.session_state[cache_key]

    if st.button("Verileri Yenile", key="yte_mrap_yenile"):
        if cache_key in st.session_state:
            del st.session_state[cache_key]
        st.rerun(scope="fragment")

    # 33 modul kapsami (ModulRaporToplayici cikti anahtarlari ile birebir)
    MODUL_SIRA = [
        # Akademik (9)
        "Akademik Takip", "Olcme Degerlendirme", "Rehberlik",
        "Okul Sagligi", "Yabanci Dil", "Kisisel Dil Gelisimi",
        "AI Bireysel Egitim", "Erken Uyari", "Egitim Koclugu",
        # Kurumsal (9)
        "Insan Kaynaklari", "Halkla Iliskiler", "Sosyal Medya",
        "Butce Gelir Gider", "Toplanti ve Kurullar", "Randevu ve Ziyaretci",
        "Kayit Modulu", "Kurum Hizmetleri", "KOI",
        # Operasyon & Etkinlik (8)
        "Sosyal Etkinlik", "Kutuphane", "Dijital Kutuphane",
        "Destek Hizmetleri", "Tuketim Demirbas", "Sivil Savunma",
        "Mezunlar", "Akademik Takvim",
        # Analiz (2)
        "SWOT Analizi", "Veli Memnuniyet",
    ]

    # Ozet stat
    veri_olan = sum(1 for m in MODUL_SIRA if m in modul_raporlari)
    toplam_kayit = 0
    for data in modul_raporlari.values():
        for satir in data.get("satirlar", []):
            val = satir.get("Kayit Sayisi", 0)
            if isinstance(val, (int, float)):
                toplam_kayit += val
    styled_stat_row([
        ("Toplam Modul", str(len(MODUL_SIRA)), _CLR_BLUE, "📦"),
        ("Veri Olan Modul", str(veri_olan), _CLR_GREEN, "✅"),
        ("Toplam Kayit", str(toplam_kayit), "#7c3aed", "📊"),
    ])

    # Her modul için rapor karti
    for modul in MODUL_SIRA:
        renk = MODUL_RENK.get(modul, "#64748b")
        ikon = MODUL_IKON.get(modul, "📋")
        data = modul_raporlari.get(modul)

        if not data:
            st.markdown(
                f'<div style="background:#111827;border-left:4px solid #cbd5e1;border-radius:0 10px 10px 0;'
                f'padding:10px 16px;margin-bottom:6px;display:flex;align-items:center;gap:8px;">'
                f'<span style="font-size:14px;">{ikon}</span>'
                f'<span style="font-size:13px;font-weight:600;color:#94a3b8;">{modul}</span>'
                f'<span style="font-size:10px;color:#cbd5e1;margin-left:auto;">Veri Yok</span></div>',
                unsafe_allow_html=True)
            continue

        with st.expander(f"{ikon} {modul}  —  {data.get('baslik', '')}", expanded=False):
            # Metrik kartlari
            metriks = data.get("metriks", [])
            if metriks:
                m_html = ""
                for label, val, clr in metriks:
                    m_html += (
                        f'<div style="display:inline-block;background:{clr}10;border:1px solid {clr}25;'
                        f'border-radius:12px;padding:10px 18px;margin:3px;min-width:110px;text-align:center;">'
                        f'<div style="font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:.5px;">'
                        f'{label}</div>'
                        f'<div style="font-size:20px;font-weight:800;color:{clr};margin-top:2px;">'
                        f'{val}</div></div>')
                st.markdown(
                    f'<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:10px;">{m_html}</div>',
                    unsafe_allow_html=True)

            # Detay tablosu
            satirlar = data.get("satirlar", [])
            if satirlar:
                rows_html = ""
                for satir in satirlar:
                    alan = satir.get("Rapor Alani", "")
                    kayit = satir.get("Kayit Sayisi", satir.get("Kayıt Sayısı", 0))
                    rows_html += (
                        f'<tr><td style="padding:5px 10px;font-size:12px;color:#94A3B8;">{alan}</td>'
                        f'<td style="padding:5px 10px;font-size:12px;font-weight:700;color:{renk};'
                        f'text-align:right;">{kayit}</td></tr>')
                st.markdown(
                    f'<table style="width:100%;border-collapse:collapse;">'
                    f'<thead><tr style="background:{renk}08;">'
                    f'<th style="padding:6px 10px;text-align:left;color:#64748b;font-size:11px;">Rapor Alani</th>'
                    f'<th style="padding:6px 10px;text-align:right;color:#64748b;font-size:11px;">Kayıt Sayısı</th>'
                    f'</tr></thead><tbody>{rows_html}</tbody></table>',
                    unsafe_allow_html=True)


def _render_gecmis_raporlar(store: YTEDataStore):
    """Gecmis gun basi/gun sonu raporlarini listele."""
    styled_section("Geçmiş Günlük Raporlar", _CLR_BLUE)

    # Tarih filtre
    col1, col2 = st.columns(2)
    with col1:
        bas_tarih = st.date_input("Başlangıç", value=date.today() - timedelta(days=30), key="yte_rap_bas")
    with col2:
        bit_tarih = st.date_input("Bitis", value=date.today(), key="yte_rap_bit")

    bas_str = bas_tarih.isoformat()
    bit_str = bit_tarih.isoformat()

    raporlar = sorted(
        [r for r in store.load_objects("raporlar") if bas_str <= r.tarih <= bit_str],
        key=lambda r: r.tarih, reverse=True)

    if not raporlar:
        styled_info_banner("Secili tarih araliginda rapor bulunamadı.", banner_type="warning", icon="⚠️")
        return

    # Rapor listesi
    rows = ""
    for r in raporlar[:50]:
        tur_badge = '<span style="color:#3b82f6;font-size:10px;">Gün Sonu</span>'
        if r.rapor_turu == "gun_basi":
            tur_badge = '<span style="color:#059669;font-size:10px;">Gün Başı</span>'
        rows += f"""<tr>
        <td style="padding:6px 10px;font-weight:600;">{r.tarih}</td>
        <td style="padding:6px 10px;">{tur_badge}</td>
        <td style="padding:6px 10px;">{r.planlanan_sayi}</td>
        <td style="padding:6px 10px;color:#10b981;font-weight:600;">{r.gerceklesen_sayi}</td>
        <td style="padding:6px 10px;color:#ef4444;">{r.iptal_sayi}</td>
        <td style="padding:6px 10px;font-weight:700;color:{_CLR_BLUE};">%{r.gerceklesme_orani}</td>
        <td style="padding:6px 10px;">{'✅' if r.eposta_gonderildi else '—'}</td></tr>"""
    st.markdown(f"""<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:12px;">
    <thead><tr style="background:#1A2035;">
    <th style="padding:8px 10px;text-align:left;color:#64748b;">Tarih</th>
    <th style="padding:8px 10px;text-align:left;color:#64748b;">Tur</th>
    <th style="padding:8px 10px;text-align:left;color:#64748b;">Planlanan</th>
    <th style="padding:8px 10px;text-align:left;color:#64748b;">Gerçekleşen</th>
    <th style="padding:8px 10px;text-align:left;color:#64748b;">İptal</th>
    <th style="padding:8px 10px;text-align:left;color:#64748b;">Oran</th>
    <th style="padding:8px 10px;text-align:left;color:#64748b;">E-posta</th>
    </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)

    # Detay goruntuleme + PDF indirme
    st.divider()
    tarih_secenekleri = sorted(set(r.tarih for r in raporlar), reverse=True)
    secili = st.selectbox("Rapor Detayi ve PDF Indirme", [""] + tarih_secenekleri, key="yte_rapor_detay")
    if secili:
        rapor = next((r for r in raporlar if r.tarih == secili), None)
        if rapor:
            styled_stat_row([
                ("Planlanan", str(rapor.planlanan_sayi), _CLR_BLUE, "📋"),
                ("Gerçekleşen", str(rapor.gerceklesen_sayi), _CLR_GREEN, "✅"),
                ("İptal", str(rapor.iptal_sayi), _CLR_RED, "❌"),
                ("Oran", f"%{rapor.gerceklesme_orani}", _CLR_GOLD, "📊"),
            ])

            if rapor.ai_degerlendirme:
                styled_section("AI Değerlendirme")
                st.markdown(rapor.ai_degerlendirme)

            # PDF indirme - hem gun basi hem gun sonu
            gorevler_raw = store.find_by_field("gorevler", "tarih", secili)
            gorevler = [PlanlanmisGorev.from_dict(g) if isinstance(g, dict) else g for g in gorevler_raw]
            engine = RaporUreticisi(store)

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                gb_pdf = engine.gun_basi_pdf_olustur(secili, gorevler)
                if gb_pdf:
                    st.download_button("Gün Başı PDF Indir", gb_pdf,
                                       file_name=f"gun_basi_{secili}.pdf",
                                       mime="application/pdf", use_container_width=True, key=f"yte_gbpdf_{secili}")
            with col_p2:
                gs_pdf = engine.gun_sonu_pdf_olustur(rapor, gorevler)
                if gs_pdf:
                    st.download_button("Gün Sonu PDF Indir", gs_pdf,
                                       file_name=f"gun_sonu_{secili}.pdf",
                                       mime="application/pdf", use_container_width=True, key=f"yte_gspdf_{secili}")


def _render_sozlesme_raporlari():
    """Sozlesme raporlarini filtrele ve PDF olarak indir."""
    styled_section("Sözleşme Raporları", "#7c3aed")
    styled_info_banner(
        "Halkla Iliskiler modulunde kaydedilen sozlesmeleri tarih ve isme gore "
        "filtreleyebilir, PDF olarak indirebilirsiniz.", banner_type="info", icon="📄")

    if load_sozlesmeler is None:
        styled_info_banner(
            "Halkla Iliskiler modulu yuklenemedi. Sozlesme raporlari kullanilamaz.", banner_type="error", icon="⚠️")
        return

    sozlesmeler = load_sozlesmeler()
    if not sozlesmeler:
        styled_info_banner("Henuz kaydedilmis sozlesme bulunmuyor.", banner_type="warning", icon="📭")
        return

    # --- Filtreler ---
    fc1, fc2, fc3 = st.columns([2, 2, 1])
    with fc1:
        _yte_sf_arama = st.text_input(
            "Öğrenci / Veli Adi Ara",
            key="yte_sozl_arama",
            placeholder="Isim ile arayin...",
        )
    with fc2:
        _yte_sf_tarih = st.selectbox(
            "Tarih Filtresi",
            ["Tümü", "Bu Ay", "Son 3 Ay", "Son 6 Ay", "Tarih Araligi"],
            key="yte_sozl_tarih_filtre",
        )
    with fc3:
        _yte_sf_sonuc = st.selectbox(
            "Sonuc",
            ["Tümü", "Kesin Kayıt", "Kayıt Iptal", "Bekliyor"],
            key="yte_sozl_sonuc_filtre",
        )

    # Tarih araligi
    _yte_sf_start = None
    _yte_sf_end = None
    if _yte_sf_tarih == "Tarih Araligi":
        _d1, _d2 = st.columns(2)
        with _d1:
            _yte_sf_start = st.date_input(
                "Başlangıç", value=date.today() - timedelta(days=90), key="yte_sozl_start")
        with _d2:
            _yte_sf_end = st.date_input(
                "Bitis", value=date.today(), key="yte_sozl_end")
    elif _yte_sf_tarih == "Bu Ay":
        _yte_sf_start = date.today().replace(day=1)
        _yte_sf_end = date.today()
    elif _yte_sf_tarih == "Son 3 Ay":
        _yte_sf_start = date.today() - timedelta(days=90)
        _yte_sf_end = date.today()
    elif _yte_sf_tarih == "Son 6 Ay":
        _yte_sf_start = date.today() - timedelta(days=180)
        _yte_sf_end = date.today()

    # Filtreleme uygula
    filtered = sozlesmeler
    if _yte_sf_arama:
        q = _yte_sf_arama.lower()
        filtered = [
            s for s in filtered
            if q in s.get("ogrenci_adi", "").lower()
            or q in s.get("veli_adi", "").lower()
            or q in s.get("ogrenci_label", "").lower()
        ]
    if _yte_sf_sonuc == "Kesin Kayıt":
        filtered = [s for s in filtered if s.get("kayit_sonucu") == "Kesin Kayıt"]
    elif _yte_sf_sonuc == "Kayıt Iptal":
        filtered = [s for s in filtered if s.get("kayit_sonucu") == "Kayıt İptal"]
    elif _yte_sf_sonuc == "Bekliyor":
        filtered = [s for s in filtered if not s.get("kayit_sonucu")]

    if _yte_sf_start and _yte_sf_end:
        date_filtered = []
        for s in filtered:
            s_tarih = s.get("sozlesme_tarihi", "") or s.get("kayit_tarihi", "")
            if s_tarih:
                try:
                    s_date = date.fromisoformat(str(s_tarih)[:10])
                    if _yte_sf_start <= s_date <= _yte_sf_end:
                        date_filtered.append(s)
                except (ValueError, TypeError):
                    date_filtered.append(s)
            else:
                date_filtered.append(s)
        filtered = date_filtered

    # Istatistik kartlari
    kesin = len([s for s in filtered if s.get("kayit_sonucu") == "Kesin Kayıt"])
    iptal = len([s for s in filtered if s.get("kayit_sonucu") == "Kayıt İptal"])
    bekl = len(filtered) - kesin - iptal
    styled_stat_row([
        ("Toplam Sozlesme", str(len(filtered)), "#7c3aed", "📄"),
        ("Kesin Kayıt", str(kesin), _CLR_GREEN, "✅"),
        ("Kayıt Iptal", str(iptal), _CLR_RED, "❌"),
        ("Bekliyor", str(bekl), _CLR_GOLD, "⏳"),
    ])

    # Sozlesme listesi
    if not filtered:
        styled_info_banner("Filtrelere uygun sozlesme bulunamadı.", banner_type="info", icon="🔍")
        return

    for si, sozl in enumerate(filtered):
        s_sonuc = sozl.get("kayit_sonucu", "")
        if s_sonuc == "Kesin Kayıt":
            s_renk, s_bg, s_icon = "#22c55e", "#dcfce7", "✅"
        elif s_sonuc == "Kayıt İptal":
            s_renk, s_bg, s_icon = "#ef4444", "#fee2e2", "❌"
        else:
            s_renk, s_bg, s_icon = "#f59e0b", "#fef3c7", "⏳"

        s_tarih_str = str(sozl.get("sozlesme_tarihi", ""))[:10]
        s_toplam = float(sozl.get("toplam_kdv_dahil", 0) or 0)

        st.markdown(
            f'<div style="background:{s_bg};border:1px solid {s_renk};border-left:5px solid {s_renk};'
            f'border-radius:12px;padding:.8rem 1.2rem;margin-bottom:.5rem;'
            f'box-shadow:0 2px 8px rgba(0,0,0,.04);">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">'
            f'<div>'
            f'<strong style="font-size:1rem;color:#94A3B8;">'
            f'🎓 {sozl.get("ogrenci_adi", "-")}</strong>'
            f' <span style="color:#64748b;font-size:.88rem;">'
            f'({sozl.get("ogrenci_sinif", "-")})</span><br>'
            f'<span style="font-size:.85rem;color:#64748b;">'
            f'👤 {sozl.get("veli_adi", "-")} | '
            f'📅 {s_tarih_str} | '
            f'💰 ₺{s_toplam:,.0f}'
            f'</span></div>'
            f'<span style="background:{s_renk};color:#fff;padding:4px 12px;border-radius:20px;'
            f'font-size:.82rem;font-weight:700;">{s_icon} {s_sonuc or "Bekliyor"}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        # PDF indirme butonu
        if _generate_sozlesme_pdf is not None:
            pdf_data = _generate_sozlesme_pdf(sozl)
            if pdf_data:
                ogr_name = sozl.get("ogrenci_adi", "ogrenci").replace(" ", "_")
                st.download_button(
                    f"📥 {sozl.get('ogrenci_adi', 'Öğrenci')} - Sozlesme PDF Indir",
                    pdf_data,
                    file_name=f"sozlesme_{ogr_name}.pdf",
                    mime="application/pdf",
                    key=f"yte_sozl_pdf_{si}",
                )


# ============================================================
# TAB 8: AYARLAR
# ============================================================

def _render_ayarlar(store: YTEDataStore):
    styled_section("Genel Ayarlar", _CLR_BLUE)

    ayarlar = {a.ayar_adi: a for a in store.load_objects("yte_ayarlar")}

    rapor_saati = st.text_input("Rapor Saati (HH:MM)", value=ayarlar.get("rapor_saati", YTEAyar()).deger or "19:00",
                                key="yte_ay_rapor_saati")
    ai_aktif = st.checkbox("AI Değerlendirme Aktif",
                           value=ayarlar.get("ai_degerlendirme", YTEAyar()).deger == "true",
                           key="yte_ay_ai")

    if st.button("Ayarlari Kaydet", key="yte_ay_kaydet", type="primary"):
        a_rapor = ayarlar.get("rapor_saati", YTEAyar(ayar_adi="rapor_saati"))
        a_rapor.deger = rapor_saati
        store.upsert("yte_ayarlar", a_rapor)

        a_ai = ayarlar.get("ai_degerlendirme", YTEAyar(ayar_adi="ai_degerlendirme"))
        a_ai.deger = "true" if ai_aktif else "false"
        store.upsert("yte_ayarlar", a_ai)

        st.success("Ayarlar kaydedildi!")

    st.divider()
    styled_info_banner(
        "Otomatik e-posta gonderimi icin: Saat 19:00'da "
        "Windows Görev Zamanlayici veya Linux cron ile "
        "'streamlit run app.py -- --send-report' komutu planlayin.", banner_type="warning", icon="⏰")


# ============================================================
# TAB: PERSONEL BILGI KARTI (IK ENTEGRASYON)
# ============================================================

def _render_sinif_veli_listesi():
    """Sınıf & Veli Listesi — shared_data + Halkla İlişkiler verilerinden."""
    styled_section("Sınıf & Veli Listesi", "#6366f1")
    styled_info_banner(
        "Kurumsal Organizasyon > İletişim > Sınıf Listeleri'nden ve "
        "Halkla İlişkiler > Aday Yönetimi'nden gelen güncel öğrenci ve veli verileri.",
        banner_type="info", icon="📋")

    from utils.shared_data import load_shared_students
    students = load_shared_students()

    if not students:
        styled_info_banner("Henüz öğrenci verisi bulunamadı. Kurumsal Org. > İletişim > Sınıf Listeleri'nden ekleyin.", banner_type="warning", icon="⚠️")
        return

    # İstatistikler
    siniflar = sorted(set(str(s.get("sinif", "")) for s in students if s.get("sinif")))
    subeler = sorted(set(s.get("sube", "") for s in students if s.get("sube")))
    veli_olan = sum(1 for s in students if s.get("veli_ad") or s.get("veli_adi"))
    styled_stat_row([
        ("Toplam Öğrenci", str(len(students)), "#2563eb", "👨‍🎓"),
        ("Sınıf Sayısı", str(len(siniflar)), "#059669", "🏫"),
        ("Şube Sayısı", str(len(subeler)), "#7c3aed", "📂"),
        ("Veli Kayıtlı", str(veli_olan), "#ea580c", "👪"),
    ])

    # Filtre
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        fil_sinif = st.selectbox("Sınıf", ["Tümü"] + siniflar, key="yte_svl_sinif")
    with col_f2:
        fil_sube = st.selectbox("Şube", ["Tümü"] + subeler, key="yte_svl_sube")
    with col_f3:
        fil_ara = st.text_input("Ara (öğrenci/veli)", key="yte_svl_ara", placeholder="Ad ara...")

    filtered = students
    if fil_sinif != "Tümü":
        filtered = [s for s in filtered if str(s.get("sinif", "")) == fil_sinif]
    if fil_sube != "Tümü":
        filtered = [s for s in filtered if s.get("sube", "") == fil_sube]
    if fil_ara:
        q = fil_ara.lower()
        filtered = [s for s in filtered if
                    q in (s.get("ad", "") + " " + s.get("soyad", "")).lower() or
                    q in (s.get("veli_ad", s.get("veli_adi", ""))).lower()]

    st.caption(f"📋 {len(filtered)} öğrenci listeleniyor")

    # Alt sekmeler: Sınıf Listesi | Veli Listesi
    sub_t1, sub_t2 = st.tabs(["📋 Sınıf Listesi", "👪 Veli Listesi"])

    with sub_t1:
        if not filtered:
            st.info("Filtreye uyan öğrenci yok.")
        else:
            import pandas as pd
            sorted_students = sorted(filtered, key=lambda x: (str(x.get("sinif", "")), x.get("sube", ""), x.get("numara", 0)))
            rows = []
            for s in sorted_students:
                rows.append({
                    "Sınıf": str(s.get("sinif", "")),
                    "Şube": s.get("sube", ""),
                    "No": s.get("numara", ""),
                    "Ad": s.get("ad", ""),
                    "Soyad": s.get("soyad", ""),
                    "Cinsiyet": s.get("cinsiyet", ""),
                    "TC": str(s.get("tc", ""))[-4:] + "****" if s.get("tc") else "",
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, height=400)

            # ── PDF İndir ──
            sinif_label = fil_sinif if fil_sinif != "Tümü" else "Tum"
            sube_label = fil_sube if fil_sube != "Tümü" else "Tum"
            if st.button("📄 Sınıf Listesi PDF İndir", key="yte_sinif_pdf_btn", type="primary"):
                pdf_bytes = _generate_sinif_listesi_pdf(sorted_students, fil_sinif, fil_sube)
                st.download_button(
                    "📥 PDF İndir",
                    data=pdf_bytes,
                    file_name=f"sinif_listesi_{sinif_label}_{sube_label}.pdf",
                    mime="application/pdf",
                    key="yte_sinif_pdf_dl",
                )

    with sub_t2:
        if not filtered:
            st.info("Filtreye uyan veli yok.")
        else:
            import pandas as pd
            rows_v = []
            for s in sorted(filtered, key=lambda x: (str(x.get("sinif", "")), x.get("sube", ""), x.get("ad", ""))):
                veli_ad = s.get("veli_ad", s.get("veli_adi", ""))
                veli_tel = s.get("veli_tel", s.get("veli_telefon", ""))
                veli_email = s.get("veli_email", s.get("veli_eposta", ""))
                if not veli_ad and not veli_tel:
                    continue
                rows_v.append({
                    "Öğrenci": f"{s.get('ad', '')} {s.get('soyad', '')}",
                    "Sınıf/Şube": f"{s.get('sinif', '')}/{s.get('sube', '')}",
                    "Veli Adı": veli_ad,
                    "Veli Tel": veli_tel,
                    "Veli E-posta": veli_email,
                })
            if rows_v:
                df_v = pd.DataFrame(rows_v)
                st.dataframe(df_v, use_container_width=True, height=400)
            else:
                st.info("Veli bilgisi bulunan öğrenci yok.")


def _generate_sinif_listesi_pdf(students: list, sinif_filtre: str, sube_filtre: str) -> bytes:
    """Sınıf listesini baskıya hazır premium PDF olarak üretir."""
    import io
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_CENTER
    except ImportError:
        return b"reportlab yuklu degil"

    from utils.shared_data import ensure_turkish_pdf_fonts, load_kurum_profili
    font_name, font_bold = ensure_turkish_pdf_fonts()
    kurum = load_kurum_profili()
    kurum_adi = kurum.get("kurum_adi", kurum.get("okul_adi", ""))

    NAVY = colors.HexColor('#1a1a2e')
    GOLD = colors.HexColor('#c9a84c')

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=1.5*cm, rightMargin=1.5*cm)

    elements = []

    # Başlık
    baslik = f"Sınıf Listesi"
    if sinif_filtre and sinif_filtre != "Tümü":
        baslik += f" — {sinif_filtre}. Sınıf"
    if sube_filtre and sube_filtre != "Tümü":
        baslik += f" / {sube_filtre} Şubesi"

    elements.append(Paragraph(
        kurum_adi if kurum_adi else "SmartCampus AI",
        ParagraphStyle('kurum', fontSize=14, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY, spaceAfter=4)
    ))
    elements.append(Paragraph(
        baslik,
        ParagraphStyle('baslik', fontSize=12, fontName=font_bold, alignment=TA_CENTER, textColor=GOLD, spaceAfter=4)
    ))
    from datetime import datetime
    elements.append(Paragraph(
        datetime.now().strftime("%d.%m.%Y"),
        ParagraphStyle('tarih', fontSize=9, fontName=font_name, alignment=TA_CENTER, textColor=colors.grey, spaceAfter=12)
    ))

    # Tablo
    header = ["No", "Sınıf", "Şube", "Öğrenci No", "Ad", "Soyad", "Cinsiyet"]
    rows = [header]
    for i, s in enumerate(students, 1):
        rows.append([
            str(i),
            str(s.get("sinif", "")),
            s.get("sube", ""),
            str(s.get("numara", "")),
            s.get("ad", ""),
            s.get("soyad", ""),
            s.get("cinsiyet", ""),
        ])

    col_widths = [1*cm, 1.5*cm, 1.5*cm, 2*cm, 4*cm, 4*cm, 2*cm]
    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (4, 1), (5, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('BOX', (0, 0), (-1, -1), 1.5, NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('LINEBELOW', (0, 0), (-1, 0), 2, GOLD),
    ]))
    elements.append(tbl)
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(
        f"Toplam: {len(students)} öğrenci",
        ParagraphStyle('toplam', fontSize=9, fontName=font_bold, alignment=TA_CENTER, textColor=NAVY)
    ))

    doc.build(elements)
    return buf.getvalue()


def _render_yte_personel_bilgi_karti():
    """Yonetim Ekranı'ndan Personel Bilgi Kartı — IK modulunden veri cekilir."""
    if not _IK_AVAILABLE:
        styled_info_banner("IK modülü yüklenemedi. Personel Bilgi Kartı kullanılamıyor.", banner_type="error", icon="⚠️")
        return

    ik_base = os.path.join(get_tenant_dir(), "ik")
    ik_store = IKDataStore(ik_base)
    _render_personel_bilgi_karti(ik_store)


# ============================================================
# TAB 9: SMARTI
# ============================================================

def _render_smarti(store: YTEDataStore):
    def _data_context():
        today = date.today().isoformat()
        gorevler = store.find_by_field("gorevler", "tarih", today)
        toplam = len(gorevler)
        tamamlanan = sum(1 for g in gorevler if (g.get("durum") if isinstance(g, dict) else g.durum) == "Tamamlandı")
        oran = round(tamamlanan / toplam * 100, 1) if toplam > 0 else 0

        raporlar = store.load_objects("raporlar")
        son_rapor = max(raporlar, key=lambda r: r.tarih) if raporlar else None

        ctx = f"Bugün ({today}): {toplam} planlanan gorev, {tamamlanan} tamamlanan, %{oran} gerceklesme.\n"
        if son_rapor:
            ctx += f"Son rapor ({son_rapor.tarih}): %{son_rapor.gerceklesme_orani} gerceklesme.\n"
        return ctx

    render_smarti_chat("yonetim_ekran", _data_context)


# ============================================================
# TAB: KULLANIM KILAVUZU
# ============================================================

def _render_veli_ogrenci_veri_akisi():
    """Veli/Öğrenci ekranlarına veri sağlayan tüm kaynakların detaylı akış şeması."""
    styled_section("Veli / Öğrenci Paneli — Veri Akış Haritası", "#6366f1")
    st.caption("Her sekmeye hangi modülden, hangi işlemle, nasıl veri geliyor — detaylı kaynak haritası.")

    # ── Veri Akış Tablosu ──
    VERI_AKISI = [
        # (Sekme, Veri, Kaynak Modül, Giriş Yapan, Yöntem, Veri Dosyası, Kademe)
        ("📋 Günlük Bülten", "Günlük etkinlik, yemek, uyku, davranış, duygu durumu",
         "Akademik Takip → Okul Öncesi/İlkokul", "Öğretmen", "Manuel",
         "data/akademik/gunluk_bultenler.json", "Okul Öncesi, İlkokul"),

        ("📝 Veli Geri Bildirim", "Evdeki çocuğun durumu (yemek, uyku, ruh hali, sağlık)",
         "Veli Paneli (doğrudan)", "Veli", "Manuel",
         "data/akademik/veli_geri_bildirimler.json", "Tüm Kademeler"),

        ("📊 Notlarım", "Ders notları, sınav puanları, dönem ortalaması",
         "Akademik Takip → Not Girişi", "Öğretmen", "Manuel",
         "data/akademik/grades.json", "İlkokul 3+, Ortaokul, Lise"),

        ("📅 Devamsızlık", "Günlük/ders bazlı devamsızlık kaydı",
         "Akademik Takip → Yoklama", "Öğretmen", "Manuel",
         "data/akademik/attendance.json", "Tüm Kademeler"),

        ("📝 Ödevler", "Ödev başlığı, açıklama, son tarih, teslim durumu",
         "Akademik Takip → Ödev Yönetimi", "Öğretmen", "Manuel",
         "data/akademik/odevler.json", "Tüm Kademeler"),

        ("📥 Ödev Teslim", "Öğrencinin ödev teslim durumu ve puanı",
         "Öğrenci Paneli (doğrudan)", "Öğrenci", "Manuel/Online",
         "data/akademik/odev_teslimleri.json", "Tüm Kademeler"),

        ("📖 Kazanım İşleme", "İşlenen kazanımlar, tarih, ders",
         "Akademik Takip → Uygulama Takibi", "Öğretmen", "Manuel",
         "data/akademik/kazanim_isleme.json", "Tüm Kademeler"),

        ("📚 Kazanım Borçları", "Öğrencinin eksik kazanımları",
         "Sistem (Otomatik)", "Sistem", "Otomatik (devamsızlık/eksik ödevden)",
         "data/akademik/kazanim_borclari.json", "Ortaokul, Lise"),

        ("🎯 KYT Soruları", "Kazanım Yoklama Testi soruları",
         "Akademik Takip → Sınav & KYT", "Öğretmen", "Manuel",
         "data/akademik/kyt_sorular.json", "Tüm Kademeler"),

        ("🎯 KYT Cevapları", "Öğrencinin KYT yanıtları ve analizi",
         "Öğrenci Paneli (doğrudan)", "Öğrenci", "Online Test",
         "data/akademik/kyt_cevaplar.json", "Tüm Kademeler"),

        ("📊 Sınav Sonuçları", "Sınav puanı, doğru/yanlış, kazanım analizi",
         "Ölçme ve Değerlendirme → Sonuçlar", "Öğretmen/Sistem", "Manuel + Otomatik Puanlama",
         "data/olcme/results.json", "Tüm Kademeler"),

        ("🔄 Telafi Görevleri", "Düşük başarıdan kaynaklanan telafi (RED/YELLOW/GREEN/BLUE)",
         "Ölçme ve Değerlendirme (Otomatik)", "Sistem", "Otomatik (sınav sonrası)",
         "data/olcme/telafi_tasks.json", "Tüm Kademeler"),

        ("📅 Ders Programı", "Haftalık ders çizelgesi, öğretmen bilgileri",
         "Akademik Takip → Ders Programı", "Müdür/Müdür Yrd.", "Manuel",
         "data/akademik/schedule.json", "Tüm Kademeler"),

        ("💬 Mesajlar", "Öğretmen-veli karşılıklı mesajlaşma",
         "Kurumsal Org. → İletişim / Akademik Takip", "Öğretmen/Veli", "Manuel",
         "data/akademik/mesajlar.json", "Tüm Kademeler"),

        ("🏥 Revir Kayıtları", "Revir ziyaretleri, şikayet, müdahale",
         "Okul Sağlığı Takip → Revir Ziyareti", "Revir Görevlisi", "Manuel",
         "data/okul_sagligi/revir_ziyaretleri.json", "Tüm Kademeler"),

        ("🧑‍⚕️ Rehberlik Vakaları", "Rehberlik vakaları, görüşmeler, risk seviyesi",
         "Rehberlik → Vaka Takibi / Görüşmeler", "Rehber Öğretmen", "Manuel",
         "data/rehberlik/vakalar.json, gorusmeler.json", "Tüm Kademeler"),

        ("📋 Rehberlik Testleri", "Psikolojik test sonuçları",
         "Rehberlik → Test & Envanter", "Rehber Öğretmen", "Manuel + Online Test",
         "data/rehberlik/test_sonuclari.json", "Tüm Kademeler"),

        ("🚨 Risk Uyarıları", "Akademik risk tespiti, erken uyarı",
         "Erken Uyarı Sistemi (Otomatik)", "Sistem", "Otomatik (9 bileşenli hesaplama)",
         "data/akademik/risk_alerts.json", "Tüm Kademeler"),

        ("📋 Destek Planları", "Müdahale ve destek planları",
         "Erken Uyarı / Akademik Takip", "Öğretmen/Rehber", "Manuel",
         "data/akademik/destek_planlari.json", "Tüm Kademeler"),

        ("📎 Belgeler", "Öğretmen tarafından paylaşılan dosyalar/linkler",
         "Akademik Takip → Ders Defteri", "Öğretmen", "Dosya Yükleme",
         "data/akademik/ogretmen_belgeleri.json", "Tüm Kademeler"),

        ("🎉 Etkinlik & Duyurular", "Okul etkinlikleri, duyurular",
         "Kurum Hizmetleri", "Okul İdaresi", "Manuel",
         "data/akademik/duyurular.json", "Tüm Kademeler"),

        ("🍽️ Yemek Menüsü", "Günlük/haftalık yemek listesi",
         "Kurum Hizmetleri → Yemek Menüsü", "Kurum Hizmetleri Sorumlusu", "Manuel/Excel",
         "data/kurum_hizmetleri/yemek_menu.json", "Tüm Kademeler"),

        ("📅 Randevu", "Öğretmen randevu talebi",
         "Randevu ve Ziyaretçi", "Veli talep / Öğretmen onay", "Manuel",
         "data/randevu_ziyaretci/randevular.json", "Tüm Kademeler"),

        ("📄 Belge Talep", "Karne, öğrenci belgesi talepleri",
         "Akademik Takip", "Veli talep / İdare karşılık", "Manuel",
         "data/akademik/belge_talepleri.json", "Tüm Kademeler"),

        ("📊 Memnuniyet Anketi", "Veli memnuniyet değerlendirmesi",
         "Veli Memnuniyet Modülü", "Veli", "Online Anket",
         "data/veli_memnuniyet/anket_cevaplar.json", "Tüm Kademeler"),

        ("📓 Öğrenci Defteri", "Kişisel notlar, öğretmen yorumları",
         "Akademik Takip → Öğrenci Defteri", "Öğrenci + Öğretmen", "Manuel",
         "data/akademik/ogrenci_defteri.json", "İlkokul 3+, Ortaokul, Lise"),

        ("🤖 Smarti AI", "Kişiselleştirilmiş AI sohbet",
         "AI Destek + Tüm Akademik Veriler", "Sistem (AI)", "Otomatik (GPT-4o-mini)",
         "Canlı — prompt + akademik veriler", "Tüm Kademeler"),
    ]

    # Kademe filtresi
    _fil_kademe = st.selectbox("Kademe Filtresi", ["Tümü", "Okul Öncesi", "İlkokul", "Ortaokul", "Lise"], key="yte_veri_kademe")

    # Tablo göster
    import pandas as pd
    rows = []
    for sekme, veri, kaynak, giren, yontem, dosya, kademe in VERI_AKISI:
        if _fil_kademe != "Tümü" and _fil_kademe not in kademe and "Tüm" not in kademe:
            continue
        rows.append({
            "Sekme": sekme,
            "Gösterilen Veri": veri,
            "Kaynak Modül": kaynak,
            "Veriyi Giren": giren,
            "Giriş Yöntemi": yontem,
            "Veri Dosyası": dosya,
            "Kademe": kademe,
        })

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, height=600)
        st.caption(f"Toplam: {len(rows)} veri kaynağı")
    else:
        st.info("Bu kademe için veri kaynağı bulunamadı.")

    # ── PDF Rapor ──
    st.markdown("---")
    if st.button("📄 Veri Akış Raporunu PDF Olarak İndir", key="yte_veri_pdf", type="primary"):
        pdf_bytes = _generate_veri_akisi_pdf(VERI_AKISI, _fil_kademe)
        if pdf_bytes:
            st.download_button(
                "⬇️ PDF İndir",
                data=pdf_bytes,
                file_name=f"veli_ogrenci_veri_akisi_{_fil_kademe}.pdf",
                mime="application/pdf",
                key="yte_veri_pdf_dl",
            )


def _generate_veri_akisi_pdf(veri_akisi: list, kademe_filtre: str) -> bytes | None:
    """Veli/Öğrenci veri akış raporunu PDF olarak üret."""
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from utils.shared_data import ensure_turkish_pdf_fonts
        import io

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=landscape(A4), topMargin=1.5*cm, bottomMargin=1*cm,
                                leftMargin=1*cm, rightMargin=1*cm)

        # Türkçe font
        try:
            normal_font, bold_font = ensure_turkish_pdf_fonts()
        except Exception:
            normal_font, bold_font = "Helvetica", "Helvetica-Bold"

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("TitleTR", parent=styles["Title"], fontName=bold_font,
                                     fontSize=16, spaceAfter=12)
        subtitle_style = ParagraphStyle("SubTR", parent=styles["Normal"], fontName=normal_font,
                                        fontSize=10, spaceAfter=6, textColor=colors.gray)
        cell_style = ParagraphStyle("CellTR", parent=styles["Normal"], fontName=normal_font,
                                     fontSize=7, leading=9)
        header_style = ParagraphStyle("HeaderTR", parent=styles["Normal"], fontName=bold_font,
                                       fontSize=8, leading=10, textColor=colors.white)

        elements = []
        elements.append(Paragraph("SmartCampusAI — Veli/Öğrenci Paneli Veri Akış Raporu", title_style))
        elements.append(Paragraph(f"Kademe: {kademe_filtre} | Oluşturma: {datetime.now().strftime('%d.%m.%Y %H:%M')}", subtitle_style))
        elements.append(Spacer(1, 0.5*cm))

        # Tablo başlıkları
        headers = ["Sekme", "Gösterilen Veri", "Kaynak Modül", "Veriyi Giren", "Giriş Yöntemi", "Veri Dosyası", "Kademe"]
        header_row = [Paragraph(h, header_style) for h in headers]

        data = [header_row]
        for sekme, veri, kaynak, giren, yontem, dosya, kademe in veri_akisi:
            if kademe_filtre != "Tümü" and kademe_filtre not in kademe and "Tüm" not in kademe:
                continue
            data.append([
                Paragraph(sekme, cell_style),
                Paragraph(veri, cell_style),
                Paragraph(kaynak, cell_style),
                Paragraph(giren, cell_style),
                Paragraph(yontem, cell_style),
                Paragraph(dosya, cell_style),
                Paragraph(kademe, cell_style),
            ])

        col_widths = [2.2*cm, 4.5*cm, 4.5*cm, 2.5*cm, 3*cm, 4.5*cm, 3*cm]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#94A3B8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), bold_font),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("FONTNAME", (0, 1), (-1, -1), normal_font),
            ("FONTSIZE", (0, 1), (-1, -1), 7),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#111827")]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.5*cm))

        # Özet bilgi
        elements.append(Paragraph(f"Toplam: {len(data)-1} veri kaynağı", subtitle_style))
        elements.append(Paragraph(
            "Manuel: Öğretmen/Veli/İdare tarafından elle girilir. "
            "Otomatik: Sistem tarafından hesaplanır/oluşturulur. "
            "Online: Öğrenci/Veli tarafından çevrimiçi yapılır.",
            cell_style,
        ))

        doc.build(elements)
        return buf.getvalue()
    except Exception as e:
        st.error(f"PDF oluşturulamadı: {e}")
        return None


# ============================================================

def _render_kullanim_kilavuzu():
    """Tüm modüllerin detaylı kullanım kılavuzu."""
    from utils.kilavuz_data import get_modul_listesi, get_modul_kilavuz

    styled_header("Kullanım Kılavuzu", "Tüm modüllerin detaylı kullanım rehberi", icon="📖")

    modul_listesi = get_modul_listesi()
    modul_secimi = st.selectbox(
        "Modül Seçin",
        modul_listesi,
        key="kilavuz_modul_secimi",
        help="Kılavuzunu görmek istediğiniz modülü seçin",
    )

    kilavuz = get_modul_kilavuz(modul_secimi)
    if not kilavuz:
        styled_info_banner("Seçili modül için kılavuz verisi bulunamadı.", "warning")
        return

    # Modül başlık kartı
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1e3a8a 0%,#2563eb 100%);
        padding:20px 24px;border-radius:14px;margin:12px 0 18px 0;
        box-shadow:0 6px 20px rgba(30,30,80,.18)">
        <div style="display:flex;align-items:center;gap:12px">
            <span style="font-size:2.2rem">{kilavuz.get('icon','📋')}</span>
            <div>
                <div style="font-size:1.3rem;font-weight:800;color:#fff">{modul_secimi}</div>
                <div style="font-size:.88rem;color:#93c5fd;margin-top:2px">{kilavuz.get('aciklama','')}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Alt sekmeler
    k_tabs = st.tabs([
        "📑 Sekmeler",
        "🔧 Manuel İşlemler",
        "⚡ Otomatik İşlemler",
        "🤖 AI Özellikleri",
        "📄 Çıktılar & Entegrasyon",
    ])

    # ---- Sekmeler ----
    with k_tabs[0]:
        sekmeler = kilavuz.get("sekmeler", [])
        if sekmeler:
            for i, sekme in enumerate(sekmeler):
                ad = sekme.get("ad", "")
                aciklama = sekme.get("aciklama", "")
                alt_sekmeler = sekme.get("alt_sekmeler", [])
                st.markdown(f"""<div style="background:#111827;border:1px solid #e2e8f0;
                    border-radius:10px;padding:12px 16px;margin-bottom:8px;
                    border-left:4px solid #2563eb">
                    <div style="font-weight:700;color:#94A3B8;font-size:.95rem">{ad}</div>
                    <div style="font-size:.82rem;color:#64748b;margin-top:2px">{aciklama}</div>
                </div>""", unsafe_allow_html=True)
                if alt_sekmeler:
                    for alt in alt_sekmeler:
                        st.markdown(f"""<div style="background:#f0f4ff;border:1px solid #dbeafe;
                            border-radius:8px;padding:8px 14px;margin:4px 0 4px 24px;
                            border-left:3px solid #60a5fa">
                            <div style="font-weight:600;color:#1e40af;font-size:.85rem">{alt.get('ad','')}</div>
                            <div style="font-size:.78rem;color:#64748b;margin-top:1px">{alt.get('aciklama','')}</div>
                        </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Bu modül için sekme bilgisi bulunmuyor.", "info")

    # ---- Manuel İşlemler (Nasıl Yapılır?) ----
    with k_tabs[1]:
        manuel = kilavuz.get("manuel_islemler", [])
        if manuel:
            for idx, islem in enumerate(manuel):
                baslik = islem.get("baslik", "")
                adimlar = islem.get("adimlar", [])
                with st.expander(f"📌 {baslik}", expanded=(idx == 0)):
                    for step_no, adim in enumerate(adimlar, 1):
                        renk = "#059669" if step_no == len(adimlar) else "#2563eb"
                        st.markdown(f"""<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px">
                            <div style="min-width:26px;height:26px;background:{renk};color:#fff;
                                border-radius:50%;display:flex;align-items:center;justify-content:center;
                                font-size:.75rem;font-weight:800;flex-shrink:0">{step_no}</div>
                            <div style="font-size:.85rem;color:#94A3B8;padding-top:3px">{adim}</div>
                        </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Bu modülde manuel işlem tanımı bulunmuyor.", "info")

    # ---- Otomatik İşlemler ----
    with k_tabs[2]:
        otomatik = kilavuz.get("otomatik_islemler", [])
        if otomatik:
            for item in otomatik:
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;
                    background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:8px 12px">
                    <span style="color:#059669;font-size:1rem">⚡</span>
                    <span style="font-size:.85rem;color:#166534">{item}</span>
                </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Bu modülde otomatik işlem bulunmuyor.", "info")

    # ---- AI Özellikleri ----
    with k_tabs[3]:
        ai = kilavuz.get("ai_ozellikleri", [])
        if ai:
            for item in ai:
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;
                    background:#f5f3ff;border:1px solid #ddd6fe;border-radius:8px;padding:8px 12px">
                    <span style="color:#7c3aed;font-size:1rem">🤖</span>
                    <span style="font-size:.85rem;color:#5b21b6">{item}</span>
                </div>""", unsafe_allow_html=True)
        else:
            styled_info_banner("Bu modülde AI özelliği bulunmuyor.", "info")

    # ---- Çıktılar & Entegrasyon ----
    with k_tabs[4]:
        pdf_list = kilavuz.get("pdf_ciktilari", [])
        veri = kilavuz.get("veri_yonetimi", "")
        enteg = kilavuz.get("entegrasyonlar", [])

        if pdf_list:
            styled_section("PDF / Excel Çıktıları", "#dc2626")
            for item in pdf_list:
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
                    <span style="color:#dc2626">📄</span>
                    <span style="font-size:.85rem;color:#94A3B8">{item}</span>
                </div>""", unsafe_allow_html=True)

        if veri:
            styled_section("Veri Yönetimi", "#0d9488")
            st.markdown(f"""<div style="background:#f0fdfa;border:1px solid #99f6e4;
                border-radius:8px;padding:10px 14px">
                <code style="font-size:.82rem;color:#0f766e">{veri}</code>
            </div>""", unsafe_allow_html=True)

        if enteg:
            styled_section("Entegrasyonlar", "#7c3aed")
            for item in enteg:
                st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
                    <span style="color:#7c3aed">🔗</span>
                    <span style="font-size:.85rem;color:#94A3B8">{item}</span>
                </div>""", unsafe_allow_html=True)


# ============================================================
# GÜNÜN BİLGİSİ KİTAP
# ============================================================

def _render_gunun_bilgisi_kitap():
    """Günün Bilgisi 365 günlük PDF kitap indirme ekranı."""
    from models.gunun_bilgisi_kitap import (
        BASLANGIC, BITIS, KATEGORILER, _AY_ADLARI,
        get_gecmis_bilgiler, get_gunun_bilgisi, generate_pdf_kitap,
    )

    styled_header("Günün Bilgisi — 365 Günlük Bilgi Kitabı", "Eğitim öğretim yılı boyunca her gün farklı bir bilgi", icon="💡")

    bugun = date.today()
    bilgiler = get_gecmis_bilgiler(bugun)
    toplam_gun = (min(bugun, BITIS) - BASLANGIC).days + 1 if bugun >= BASLANGIC else 0
    kalan = (BITIS - bugun).days if bugun < BITIS else 0

    # Üst istatistikler
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Toplam Bilgi", f"{len(bilgiler)} gün")
    with c2:
        st.metric("Başlangıç", f"1 Eylül 2025")
    with c3:
        st.metric("Bitiş", f"31 Ağustos 2026")
    with c4:
        st.metric("Kalan", f"{max(kalan, 0)} gün")

    # İlerleme çubuğu
    if toplam_gun > 0:
        ilerleme = min(len(bilgiler) / 365, 1.0)
        st.progress(ilerleme, text=f"İlerleme: {len(bilgiler)}/365 gün (%{int(ilerleme*100)})")

    st.divider()

    # Bugünün bilgisi
    bugunun_bilgisi = get_gunun_bilgisi(bugun)
    if bugunun_bilgisi:
        kat_info = KATEGORILER.get(bugunun_bilgisi["kategori"], {})
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e3a5f,#2563eb);border-radius:12px;padding:20px;margin-bottom:16px">
            <div style="font-size:11px;color:rgba(255,255,255,.6);margin-bottom:4px">
                {kat_info.get('icon','')} {kat_info.get('baslik','')} — {bugun.strftime('%d.%m.%Y')}
            </div>
            <div style="font-size:18px;font-weight:700;color:#fff;margin-bottom:8px">
                {bugunun_bilgisi['baslik']}
            </div>
            <div style="font-size:13px;color:rgba(255,255,255,.85);line-height:1.7">
                {bugunun_bilgisi['icerik']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Kurum adı
    try:
        from utils.shared_data import load_kurum_profili
        profil = load_kurum_profili()
        kurum_adi = profil.get("kurum_adi", "SmartCampus AI") if profil else "SmartCampus AI"
    except Exception:
        kurum_adi = "SmartCampus AI"

    # PDF İndirme
    styled_section("PDF Kitap İndir", "#1e3a5f")

    if bugun < BASLANGIC:
        st.warning("Günün Bilgisi kitabı 1 Eylül 2025'te başlayacak.")
    elif not bilgiler:
        st.info("Henüz gösterilecek bilgi yok.")
    else:
        st.info(f"📖 **{len(bilgiler)} gün**lük bilgi içeren profesyonel PDF kitap oluşturulacak. "
                f"Her gün için ayrı sayfa.")

        if st.button("📄 PDF Kitap Oluştur ve İndir", key="gunun_bilgisi_pdf_btn", type="primary"):
            with st.spinner("PDF kitap oluşturuluyor..."):
                pdf_data = generate_pdf_kitap(bugun, kurum_adi)
            if pdf_data:
                dosya_adi = f"Gunun_Bilgisi_{BASLANGIC.strftime('%Y%m%d')}_{bugun.strftime('%Y%m%d')}.pdf"
                st.download_button(
                    label="⬇️ PDF Kitabı İndir",
                    data=pdf_data,
                    file_name=dosya_adi,
                    mime="application/pdf",
                    key="gunun_bilgisi_pdf_download",
                )
                st.success(f"✅ {len(bilgiler)} günlük kitap hazır! ({len(pdf_data)//1024} KB)")
            else:
                st.error("PDF oluşturulamadı. ReportLab kütüphanesi yüklü mü?")

    # Kategori dağılımı
    st.divider()
    styled_section("Kategori Dağılımı", "#7c3aed")

    kat_sayac: dict[str, int] = {}
    for _, b in bilgiler:
        k = b["kategori"]
        kat_sayac[k] = kat_sayac.get(k, 0) + 1

    if kat_sayac:
        cols = st.columns(4)
        for i, (kat, info) in enumerate(KATEGORILER.items()):
            sayi = kat_sayac.get(kat, 0)
            with cols[i % 4]:
                st.markdown(f"""
                <div style="background:#1e293b;border:1px solid {info['renk']}30;
                border-radius:10px;padding:12px;text-align:center;margin-bottom:8px">
                    <div style="font-size:24px">{info['icon']}</div>
                    <div style="font-size:11px;font-weight:700;color:{info['renk']}">{info['baslik']}</div>
                    <div style="font-size:16px;font-weight:800;color:#e2e8f0">{sayi}</div>
                </div>
                """, unsafe_allow_html=True)


# ============================================================
# ANA RENDER FONKSIYONU
# ============================================================

def render_yonetim_ekran():
    _inject_css()
    _init_premium_widgets()

    styled_header("Yönetim Tek Ekran", "Tüm Modüllerin Günlük Planlama ve Raporlama Merkezi", icon="🎯")
    render_smarti_welcome("yonetim_ekran")

    store = _get_store()

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("yonetim_ekran_egitim_yili")

    try:
        from utils.ui_common import zaman_yolculugu_slider
        _secilen_tarih = zaman_yolculugu_slider("yonetim")
    except ImportError:
        pass

    # -- Tab Gruplama (10 -> 2 grup) --
    _G_30983 = {
        "Grup A": [("📊 Dashboard", 0), ("📋 Günlük İşlemler", 1), ("📇 Yönetim", 2), ("📈 Raporlar", 3), ("📚 Kazanımlar", 4), ("🏗️ Kontrol Merkezi", 5), ("🧠 AI Danışman", 6)],
        "Grup B": [("⚖️ Karşılaştır", 7), ("⚙️ Ayarlar", 8), ("📌 Görev Atama", 9)],
    }
    _r_30983 = st.radio("", list(_G_30983.keys()), horizontal=True, label_visibility="collapsed", key="r_30983")
    _a_30983 = set(t[1] for t in _G_30983[_r_30983])
    tabs = st.tabs([t[0] for t in _G_30983[_r_30983]])
    _m_30983 = {idx: t for idx, t in zip((t[1] for t in _G_30983[_r_30983]), tabs)}

    if 0 in _a_30983:
      with _m_30983[0]:
        _render_dashboard(store)
        # ZIRVE: Ders Programi Heatmap — gömülü (tıkla aç/kapa)
        with st.expander("📅 Okul Genel Ders Programı", expanded=False):
            try:
                from utils.schedule_heatmap import render_schedule_heatmap
                render_schedule_heatmap(baslik="Okul Genel Ders Programi")
            except ImportError:
                st.info("Ders programı heatmap modülü yüklü değil.")
            except Exception as _e:
                st.caption(f"Ders programı heatmap yüklenemedi: {_e}")
        with st.expander("🏫 Okul Genel Dashboard", expanded=False):
            try:
                from views.okul_dashboard import render_okul_dashboard
                render_okul_dashboard()
            except ImportError:
                st.info("Okul Dashboard modülü yüklü değil.")
            except Exception as _e:
                st.info(f"Okul Dashboard yüklenemedi: {_e}")

    if 1 in _a_30983:
      with _m_30983[1]:
        sub_gun = st.tabs(["🌅 Gün Başı", "🌆 Gün Sonu", "⭐ Performans", "📅 Haftalık Takvim", "📊 Haftalık Trend", "📝 Ajanda"])
        with sub_gun[0]:
            _render_gun_basi(store)
        with sub_gun[1]:
            _render_gun_sonu(store)
        with sub_gun[2]:
            _render_performans(store)
        with sub_gun[3]:
            try:
                from views._yte_zirve_features import render_haftalik_takvim
                render_haftalik_takvim(store)
            except Exception as _e:
                st.error(f"Haftalık takvim yüklenemedi: {_e}")
        with sub_gun[4]:
            try:
                from views._yte_zirve_features import render_haftalik_trend
                render_haftalik_trend(store)
            except Exception as _e:
                st.error(f"Haftalık trend yüklenemedi: {_e}")
        with sub_gun[5]:
            try:
                from views._yte_zirve_features import render_yonetici_ajanda
                render_yonetici_ajanda(store)
            except Exception as _e:
                st.error(f"Ajanda yüklenemedi: {_e}")

    if 2 in _a_30983:
      with _m_30983[2]:
        sub_yon = st.tabs(["📋 Modüller", "📇 Personel", "👨‍👩‍👧 Sınıf & Veli", "📧 E-posta"])
        with sub_yon[0]:
            _render_modul_ozetleri()
        with sub_yon[1]:
            _render_yte_personel_bilgi_karti()
        with sub_yon[2]:
            _render_sinif_veli_listesi()
        with sub_yon[3]:
            _render_eposta_ayarlari(store)

    if 3 in _a_30983:
      with _m_30983[3]:
        sub_rap = st.tabs(["📈 Raporlar", "💡 Günün Bilgisi", "📖 Kılavuz", "🔀 Veri Akışı", "📚 Kampüs Wiki"])
        with sub_rap[0]:
            _render_raporlar(store)
        with sub_rap[1]:
            _render_gunun_bilgisi_kitap()
        with sub_rap[2]:
            _render_kullanim_kilavuzu()
        with sub_rap[3]:
            st.markdown(
                '<div style="font-size:1.1rem;font-weight:700;color:#6366f1;margin-bottom:12px;">'
                '👨‍👩‍👧 Veli / Öğrenci Paneli — Veri Akış Haritası</div>',
                unsafe_allow_html=True,
            )
            _va_c1, _va_c2, _va_c3 = st.columns(3)
            with _va_c1:
                if st.button("📋 Veri Akış Tablosu", key="va_tablo_btn", use_container_width=True):
                    st.session_state["_va_panel"] = "tablo" if st.session_state.get("_va_panel") != "tablo" else None
                    st.rerun()
            with _va_c2:
                if st.button("📊 İnteraktif Diyagram", key="va_diyagram_btn", use_container_width=True):
                    st.session_state["_va_panel"] = "diyagram" if st.session_state.get("_va_panel") != "diyagram" else None
                    st.rerun()
            with _va_c3:
                if st.button("📄 PDF Rapor İndir", key="va_pdf_btn", use_container_width=True):
                    st.session_state["_va_panel"] = "pdf" if st.session_state.get("_va_panel") != "pdf" else None
                    st.rerun()

            _va_active = st.session_state.get("_va_panel")
            if _va_active == "tablo":
                _render_veli_ogrenci_veri_akisi()
            elif _va_active == "diyagram":
                try:
                    from views._veri_akis_diyagrami import render_veri_akis_diyagrami
                    render_veri_akis_diyagrami()
                except ImportError:
                    st.info("Veri akış diyagramı modülü yüklü değil.")
                except Exception as _e:
                    st.error(f"Diyagram yüklenemedi: {_e}")
            elif _va_active == "pdf":
                # Veri akışı verisini topla ve PDF üret
                try:
                    from utils.shared_data import load_shared_students
                    students = load_shared_students() or []
                    veri_akisi = []
                    for s in students:
                        veri_akisi.append({
                            "Öğrenci": f"{s.get('ad','')} {s.get('soyad','')}",
                            "Sınıf": f"{s.get('sinif','')}/{s.get('sube','')}",
                            "Veli": s.get("veli_adi", "-"),
                            "Telefon": s.get("veli_telefon", "-"),
                        })
                    pdf_bytes = _generate_veri_akisi_pdf(veri_akisi, "Tümü")
                    if pdf_bytes:
                        st.download_button(
                            "📥 Veri Akışı PDF İndir", data=pdf_bytes,
                            file_name="veli_ogrenci_veri_akisi.pdf",
                            mime="application/pdf", key="va_pdf_dl",
                        )
                    else:
                        st.warning("PDF oluşturulamadı. ReportLab kurulu mu kontrol edin.")
                except Exception as _e:
                    st.error(f"PDF oluşturma hatası: {_e}")
        with sub_rap[4]:
            try:
                from views._kampus_wiki import render_kampus_wiki
                render_kampus_wiki()
            except ImportError:
                st.info("Kampüs Wiki modülü yüklü değil.")
            except Exception as _e:
                st.error(f"Kampüs Wiki yüklenemedi: {_e}")

    if 4 in _a_30983:
      with _m_30983[4]:
        _render_kazanim_yonetimi()

    # ZİRVE: Canlı Kontrol Merkezi
    if 5 in _a_30983:
      with _m_30983[5]:
        try:
            from views._yte_zirve_features import render_canli_kontrol_merkezi
            render_canli_kontrol_merkezi(store)
        except Exception as _e:
            st.error(f"Kontrol merkezi yüklenemedi: {_e}")

    # ZİRVE: AI Çapraz Modül Danışman
    if 6 in _a_30983:
      with _m_30983[6]:
        try:
            from views._yte_zirve_features import render_ai_capraz_danisman
            render_ai_capraz_danisman(store)
        except Exception as _e:
            st.error(f"AI danışman yüklenemedi: {_e}")

    # ZİRVE: Karşılaştırma Cockpit
    if 7 in _a_30983:
      with _m_30983[7]:
        try:
            from views._yte_zirve_features import render_karsilastirma_cockpit
            render_karsilastirma_cockpit(store)
        except Exception as _e:
            st.error(f"Karşılaştırma cockpit yüklenemedi: {_e}")

    if 8 in _a_30983:
      with _m_30983[8]:
        sub_ayar = st.tabs(["⚙️ Ayarlar", "🤖 Smarti"])
        with sub_ayar[0]:
            _render_ayarlar(store)
        with sub_ayar[1]:
            _render_smarti(store)

    if 9 in _a_30983:
      with _m_30983[9]:
        try:
            from views.modul_gorev_atama import render_modul_gorev_atama
            render_modul_gorev_atama()
        except Exception as _e:
            st.info(f"Görev Atama yüklenemedi: {_e}")


# ══════════════════════════════════════════════════════════════
# KAZANIM YÖNETİMİ — Merkezi Veri Kaynağı (TEK YÖNETİM NOKTASI)
# Buraya yüklenen kazanımlar otomatik olarak şu modüllere yansır:
# OD, Akademik Takip, Erken Uyarı, Öğrenci/Veli Paneli, MEB Sınav,
# Soru Oluşturucu, Dijital Kütüphane, Matematik Dünyası, AI Destek,
# AI Premium, Öğrenci Defteri, Yabancı Dil, Rehberlik
# ══════════════════════════════════════════════════════════════

def _render_kazanim_yonetimi():
    """Merkezi Kazanım Yönetimi — kademe bazlı yükleme, güncelleme, görüntüleme."""
    from utils.shared_data import (
        KAZANIM_KADEMELERI, KAZANIM_KADEME_DERSLER,
        load_all_kazanimlar, save_all_kazanimlar,
        get_kazanimlar_by_grade_subject,
        get_kazanim_dersleri,
        import_kazanimlar_batch,
    )
    from utils.ui_common import styled_section, styled_stat_row

    styled_section("Kazanım Yönetimi — Merkezi Veri Kaynağı", "#7c3aed")

    st.markdown("""<div style="background:linear-gradient(135deg,#4c1d95,#7c3aed);
        padding:14px 20px;border-radius:12px;color:white;margin:0 0 16px 0;">
        <b>Bu ekran tüm kazanımların TEK yönetim noktasıdır.</b><br/>
        <span style="opacity:0.85;font-size:0.85rem;">
        Buraya yüklenen/güncellenen kazanımlar otomatik olarak 13 modüle yansır:
        Ölçme & Değerlendirme, Akademik Takip, Erken Uyarı, Dijital Kütüphane,
        Matematik Dünyası, Öğrenci/Veli Paneli, AI Destek ve diğerleri.
        </span></div>""", unsafe_allow_html=True)

    all_plans = load_all_kazanimlar()

    # ── ÖZET KPI ──
    kademe_sayac = Counter()
    ders_sayac = Counter()
    for p in all_plans:
        g = p.get("grade", 0)
        for kademe_adi, siniflar in KAZANIM_KADEMELERI.items():
            if g in siniflar:
                kademe_sayac[kademe_adi] += 1
                break
        ders_sayac[p.get("subject", "?")] += 1

    styled_stat_row([
        ("Toplam Plan", f"{len(all_plans):,}", "#7c3aed", "📚"),
        ("Okul Öncesi", str(kademe_sayac.get("Okul Öncesi", 0)), "#f59e0b", "🌈"),
        ("İlkokul", str(kademe_sayac.get("İlkokul", 0)), "#2563eb", "📖"),
        ("Ortaokul", str(kademe_sayac.get("Ortaokul", 0)), "#10b981", "📗"),
        ("Lise", str(kademe_sayac.get("Lise", 0)), "#ef4444", "🎓"),
        ("Ders Sayısı", str(len(ders_sayac)), "#6366f1", "📋"),
    ])

    # ── ALT SEKMELER ──
    sub1, sub2, sub3 = st.tabs(["📊 Görüntüle & Yönet", "📤 Toplu Yükleme", "🗑️ Temizlik"])

    # ═══════════════════════════════════════════════
    # ALT SEKME 1: Görüntüle & Yönet
    # ═══════════════════════════════════════════════
    with sub1:
        col_k, col_s, col_d = st.columns(3)
        with col_k:
            kademe = st.selectbox("Kademe", list(KAZANIM_KADEMELERI.keys()), key="kzy_kademe")
        with col_s:
            siniflar = KAZANIM_KADEMELERI[kademe]
            sinif = st.selectbox("Sınıf", siniflar, key="kzy_sinif")
        with col_d:
            mevcut_dersler = get_kazanim_dersleri(sinif)
            beklenen_dersler = KAZANIM_KADEME_DERSLER.get(kademe, [])
            tum_dersler = sorted(set(mevcut_dersler + beklenen_dersler))
            ders = st.selectbox("Ders", ["Tümü"] + tum_dersler, key="kzy_ders")

        if ders == "Tümü":
            filtered = [p for p in all_plans if p.get("grade") == sinif]
        else:
            filtered = get_kazanimlar_by_grade_subject(sinif, ders)

        st.caption(f"**{len(filtered)}** kayıt bulundu | {kademe} > {sinif}. Sınıf > {ders}")

        if filtered:
            unite_groups = {}
            for p in filtered:
                u = p.get("unit", "Genel")
                unite_groups.setdefault(u, []).append(p)

            for unite_name, plans_in_unite in sorted(unite_groups.items()):
                kaz_count = sum(len(p.get("learning_outcomes", [])) for p in plans_in_unite)
                with st.expander(f"📁 {unite_name} ({len(plans_in_unite)} hafta, {kaz_count} kazanım)"):
                    for p in plans_in_unite:
                        topic = p.get("topic", "")
                        week = p.get("week", "")
                        outcomes = p.get("learning_outcomes", [])
                        hours = p.get("hours", "")

                        st.markdown(f"**{week}** — {topic}" + (f" ({hours} saat)" if hours else ""))
                        for o in outcomes:
                            st.markdown(
                                f"<span style='color:#6d28d9;font-size:0.85rem;'>• {o}</span>",
                                unsafe_allow_html=True,
                            )
                        st.markdown("---")

            eksik_dersler = [d for d in beklenen_dersler if d not in mevcut_dersler]
            if eksik_dersler:
                st.warning(f"⚠️ Bu sınıf için eksik dersler: **{', '.join(eksik_dersler)}**")
        else:
            st.info("Bu filtre için kazanım bulunamadı. Toplu Yükleme sekmesinden ekleyebilirsiniz.")

    # ═══════════════════════════════════════════════
    # ALT SEKME 2: Toplu Yükleme
    # ═══════════════════════════════════════════════
    with sub2:
        st.markdown("#### JSON Dosyası ile Toplu Yükleme")
        st.markdown("""
JSON dosyası formatı:
```json
[
    {
        "grade": 9,
        "subject": "Fizik",
        "unit": "OPTİK",
        "week": "NİSAN - 1. Hafta",
        "topic": "Işık ve Aydınlanma",
        "learning_outcomes": ["FİZ.9.4.1 Kazanım açıklaması..."],
        "hours": "4"
    }
]
```
        """)

        col_up1, col_up2 = st.columns(2)
        with col_up1:
            overwrite = st.checkbox(
                "Mevcut kayıtları güncelle (aynı sınıf+ders+ünite+konu)",
                key="kzy_overwrite",
            )
        with col_up2:
            source_label = st.text_input("Kaynak", value="MEB", key="kzy_source")

        uploaded = st.file_uploader("JSON dosyası yükleyin", type=["json"], key="kzy_upload")

        if uploaded:
            try:
                import json as _json_mod
                content = _json_mod.loads(uploaded.read().decode("utf-8"))
                if not isinstance(content, list):
                    content = [content]

                st.info(f"📋 {len(content)} kayıt bulundu. Önizleme:")

                preview_data = []
                for c in content[:10]:
                    preview_data.append({
                        "Sınıf": c.get("grade", "?"),
                        "Ders": c.get("subject", "?"),
                        "Ünite": str(c.get("unit", "?"))[:30],
                        "Konu": str(c.get("topic", "?"))[:30],
                        "Kazanım #": len(c.get("learning_outcomes", [])),
                    })
                st.dataframe(preview_data, use_container_width=True, hide_index=True)
                if len(content) > 10:
                    st.caption(f"... ve {len(content) - 10} kayıt daha")

                for c in content:
                    c["source"] = source_label

                if st.button("Yükle ve Kaydet", type="primary", key="kzy_import_btn"):
                    result = import_kazanimlar_batch(content, overwrite_existing=overwrite)
                    st.success(
                        f"✅ İşlem tamamlandı!\n\n"
                        f"**Eklenen:** {result['added']} | "
                        f"**Güncellenen:** {result['updated']} | "
                        f"**Atlanan:** {result['skipped']} | "
                        f"**Toplam:** {result['total']}"
                    )
                    st.balloons()
                    st.rerun()
            except Exception as e:
                st.error(f"JSON okuma hatası: {e}")

        st.markdown("---")
        st.markdown("#### Tekli Kazanım Ekleme")

        with st.form("kzy_tekli_form"):
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                f_kademe = st.selectbox("Kademe", list(KAZANIM_KADEMELERI.keys()), key="kzy_f_kademe")
            with fc2:
                f_sinif = st.selectbox("Sınıf", KAZANIM_KADEMELERI[f_kademe], key="kzy_f_sinif")
            with fc3:
                f_ders = st.selectbox(
                    "Ders", KAZANIM_KADEME_DERSLER.get(f_kademe, []), key="kzy_f_ders",
                )

            fc4, fc5 = st.columns(2)
            with fc4:
                f_unite = st.text_input("Ünite", key="kzy_f_unite")
            with fc5:
                f_topic = st.text_input("Konu", key="kzy_f_topic")

            f_outcomes = st.text_area(
                "Kazanımlar (her satır bir kazanım)", height=120, key="kzy_f_outcomes",
            )
            f_hours = st.text_input("Saat", value="2", key="kzy_f_hours")

            if st.form_submit_button("Kaydet", type="primary"):
                if f_unite and f_outcomes.strip():
                    outcomes_list = [o.strip() for o in f_outcomes.strip().split("\n") if o.strip()]
                    result = import_kazanimlar_batch([{
                        "grade": f_sinif,
                        "subject": f_ders,
                        "unit": f_unite,
                        "topic": f_topic,
                        "learning_outcomes": outcomes_list,
                        "hours": f_hours,
                        "source": "Manuel",
                    }])
                    st.success(f"✅ {result['added']} kazanım eklendi!")
                    st.rerun()
                else:
                    st.warning("Ünite ve kazanım alanları zorunludur.")

    # ═══════════════════════════════════════════════
    # ALT SEKME 3: Temizlik
    # ═══════════════════════════════════════════════
    with sub3:
        st.markdown("#### Veri Temizliği ve İstatistikler")

        ders_stats = {}
        for p in all_plans:
            g = p.get("grade", 0)
            s = p.get("subject", "?")
            key = f"{g}. Sınıf - {s}"
            if key not in ders_stats:
                ders_stats[key] = {"plan": 0, "kazanim": 0}
            ders_stats[key]["plan"] += 1
            ders_stats[key]["kazanim"] += len(p.get("learning_outcomes", []))

        if ders_stats:
            df = pd.DataFrame([
                {"Sınıf-Ders": k, "Plan Sayısı": v["plan"], "Kazanım Sayısı": v["kazanim"]}
                for k, v in sorted(ders_stats.items())
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(
                f"Toplam: {len(all_plans)} plan, "
                f"{sum(v['kazanim'] for v in ders_stats.values())} kazanım"
            )

        st.markdown("---")
        st.markdown("#### Belirli Sınıf+Ders Silme")
        dc1, dc2 = st.columns(2)
        with dc1:
            del_sinif = st.number_input("Sınıf", 0, 12, 9, key="kzy_del_sinif")
        with dc2:
            del_ders = st.text_input("Ders (tam isim)", key="kzy_del_ders")

        if del_ders:
            matching = [
                p for p in all_plans
                if p.get("grade") == del_sinif and p.get("subject") == del_ders
            ]
            st.warning(f"⚠️ {len(matching)} kayıt silinecek: {del_sinif}. Sınıf - {del_ders}")

            if st.button("Sil", type="secondary", key="kzy_del_btn"):
                remaining = [
                    p for p in all_plans
                    if not (p.get("grade") == del_sinif and p.get("subject") == del_ders)
                ]
                save_all_kazanimlar(remaining)
                st.success(f"✅ {len(matching)} kayıt silindi. Kalan: {len(remaining)}")
                st.rerun()
