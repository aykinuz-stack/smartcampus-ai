"""
Veli Memnuniyet Anketi Modulu - Streamlit UI
=============================================
Anket donemi yonetimi, anket doldurma, degerlendirme, karsilastirma,
AI analiz, trafik isigi raporlama, PDF export.
"""
from __future__ import annotations

import io
import os
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
from models.veli_memnuniyet import (
    VeliAnketDataStore, AnketDonemi, AnketSoru, AnketCevap, AnketYorum,
    ANKET_KATEGORILERI, KATEGORI_IKONLARI, KATEGORI_RENKLER,
    LIKERT_OLCEK, LIKERT_RENKLER, DONEM_DURUMLARI,
    _now, _today,
)


# ============================================================
# STORE FACTORY
# ============================================================

def _get_anket_store() -> VeliAnketDataStore:
    base = os.path.join(get_tenant_dir(), "veli_anket")
    store = VeliAnketDataStore(base)
    store.seed_defaults()
    return store


# ============================================================
# TRAFIK ISIGI ESIKLERI
# ============================================================

ESIK_KIRMIZI = 2.5   # < 2.5  Basarisiz (Kirmizi)
ESIK_SARI = 3.5      # 2.5 - 3.49  Kritik (Sari)
                      # >= 3.5  Memnun (Yesil)


def _trafik_renk(ort: float) -> tuple[str, str, str]:
    """Ortalamaya gore (renk_hex, etiket, emoji) dondur."""
    if ort < ESIK_KIRMIZI:
        return "#ef4444", "Başarısız", "🔴"
    if ort < ESIK_SARI:
        return "#f59e0b", "Kritik", "🟡"
    return "#10b981", "Memnun", "🟢"


def _memnuniyet_badge(ort: float) -> tuple[str, str]:
    """Ortalamaya gore renk ve etiket."""
    if ort >= 4.5:
        return "#10b981", "Çok Iyi"
    if ort >= 3.5:
        return "#22c55e", "Iyi"
    if ort >= 2.5:
        return "#eab308", "Orta"
    if ort >= 1.5:
        return "#f97316", "Dusuk"
    return "#ef4444", "Çok Dusuk"


# ============================================================
# CSS ENJEKSIYON
# ============================================================

def _inject_css():
    """Modul icin premium CSS enjekte et."""
    inject_common_css("veli")


def _trafik_bar_html(kat_ort: dict[str, float]) -> str:
    """Kategori bazli trafik isigi renkli yatay bar chart."""
    if not kat_ort:
        return ""
    sorted_items = sorted(kat_ort.items(), key=lambda x: x[1])
    bars = []
    for label, ort in sorted_items:
        renk, etiket, emoji = _trafik_renk(ort)
        pct = (ort / 5.0) * 100
        ikon = KATEGORI_IKONLARI.get(label, "")
        bars.append(f"""
        <div style="display:flex;align-items:center;margin-bottom:6px;">
          <div style="width:200px;text-align:right;padding-right:12px;font-size:12px;
          font-weight:600;color:#94A3B8;white-space:nowrap;overflow:hidden;
          text-overflow:ellipsis;" title="{label}">{ikon} {label}</div>
          <div style="flex:1;display:flex;align-items:center;">
            <div style="flex:1;background:#e8ecf1;border-radius:4px;height:30px;overflow:hidden;position:relative">
              <div style="width:{pct:.1f}%;height:100%;background:linear-gradient(90deg,{renk}cc,{renk});
              border-radius:4px;min-width:24px;transition:width 0.4s ease;position:relative">
              <span style="position:absolute;right:8px;top:50%;transform:translateY(-50%);
              color:#fff;font-size:11px;font-weight:700;">{ort:.2f}</span></div>
            </div>
            <span style="min-width:70px;margin-left:8px;font-size:12px;font-weight:700;color:{renk};
            display:flex;align-items:center;gap:3px">{emoji} {etiket}</span>
          </div>
        </div>""")
    return f'<div style="margin:10px 0;">{"".join(bars)}</div>'


def _trafik_kart(items: list[dict], renk: str, baslik: str, emoji: str) -> str:
    """Trafik isigi grubu için kart HTML'i."""
    kat_items = [i for i in items if i["tip"] == "kategori"]
    soru_items = [i for i in items if i["tip"] == "soru"]
    html = f"""<div style="background:{renk}08;border:2px solid {renk}40;border-radius:14px;
    padding:16px;margin:8px 0">
    <div style="font-size:1.1rem;font-weight:800;color:{renk};margin-bottom:10px;
    display:flex;align-items:center;gap:8px">
    <span style="font-size:1.4rem">{emoji}</span> {baslik} ({len(items)} bulgu)</div>"""

    if kat_items:
        html += '<div style="margin-bottom:8px;font-size:0.8rem;font-weight:700;color:#64748b;text-transform:uppercase">Kategoriler</div>'
        for item in kat_items:
            html += f"""<div style="background:{renk}10;border-left:3px solid {renk};
            border-radius:0 8px 8px 0;padding:8px 12px;margin:4px 0;
            display:flex;justify-content:space-between;align-items:center">
            <span style="font-weight:600;color:#94A3B8">{KATEGORI_IKONLARI.get(item['ad'], '')} {item['ad']}</span>
            <span style="background:{renk}20;color:{renk};padding:2px 10px;border-radius:6px;
            font-weight:800;font-size:0.9rem">{item['ortalama']:.2f}</span>
            </div>"""

    if soru_items:
        html += '<div style="margin:10px 0 8px 0;font-size:0.8rem;font-weight:700;color:#64748b;text-transform:uppercase">Sorular</div>'
        for item in soru_items[:10]:
            kat_label = item.get("kategori", "")
            html += f"""<div style="background:#1e293b;border:1px solid #334155;border-left:3px solid {renk};
            border-radius:0 8px 8px 0;padding:7px 12px;margin:3px 0;
            display:flex;justify-content:space-between;align-items:center">
            <div style="flex:1">
            <div style="font-size:0.78rem;color:#94a3b8">{kat_label}</div>
            <div style="font-size:0.82rem;color:#e2e8f0">{item['ad'][:80]}</div>
            </div>
            <span style="background:{renk}20;color:{renk};padding:2px 8px;border-radius:6px;
            font-weight:700;font-size:0.8rem;min-width:40px;text-align:center">{item['ortalama']:.2f}</span>
            </div>"""
        if len(soru_items) > 10:
            html += f'<div style="font-size:0.75rem;color:#94a3b8;text-align:center;margin-top:6px">+{len(soru_items) - 10} daha...</div>'

    html += '</div>'
    return html


# ============================================================
# ALT SEKME 1: DASHBOARD
# ============================================================

def _render_dashboard(store: VeliAnketDataStore):
    styled_header("Veli Memnuniyet Dashboard", "Anket sonuc ozeti ve analizler", icon="📋")

    aktif = store.get_aktif_donem()
    donemler = store.load_objects("donemler")
    son_kilitli = None
    kapali = [d for d in donemler if d.durum in ("Kilitli", "Kapali")]
    if kapali:
        kapali.sort(key=lambda x: x.updated_at or x.created_at, reverse=True)
        son_kilitli = kapali[0]

    hedef = aktif or son_kilitli
    if not hedef:
        styled_info_banner(
            "Henuz anket donemi olusturulmadi. 'Donem Yönetimi' sekmesinden yeni donem olusturun.", banner_type="info", icon="📋")
        return

    durum_renk = "#10b981" if hedef.durum == "Açık" else "#ef4444" if hedef.durum == "Kilitli" else "#f59e0b"
    styled_info_banner(
        f"<b>{hedef.donem_adi}</b> | Durum: <b style='color:{durum_renk}'>{hedef.durum}</b> | "
        f"Başlangıç: {hedef.baslangic} | Bitis: {hedef.bitis or '-'}", banner_type="info", icon="📊")

    ist = store.donem_istatistik(hedef.id)
    if ist["toplam_cevap"] == 0:
        styled_info_banner("Henuz cevap girilmedi.", banner_type="info", icon="📋")
        return

    renk_g, etiket_g = _memnuniyet_badge(ist["genel_ortalama"])
    trafik_r, trafik_e, trafik_emoji = _trafik_renk(ist["genel_ortalama"])

    # Trafik isigi sayilari
    rapor = store.trafik_isigi_raporu(hedef.id)
    k_kat = len([i for i in rapor["kirmizi"] if i["tip"] == "kategori"])
    s_kat = len([i for i in rapor["sari"] if i["tip"] == "kategori"])
    y_kat = len([i for i in rapor["yesil"] if i["tip"] == "kategori"])

    styled_stat_row([
        ("Katilimci", str(ist["toplam_katilimci"]), "#2563eb", "👥"),
        ("Genel Ortalama", f"{ist['genel_ortalama']:.2f}", trafik_r, "⭐"),
        ("Kirmizi Alan", str(k_kat), "#ef4444", "🔴"),
        ("Sari Alan", str(s_kat), "#f59e0b", "🟡"),
        ("Yesil Alan", str(y_kat), "#10b981", "🟢"),
    ])

    from utils.report_utils import ReportStyler

    # Trafik isigi renkli kategori bar chart
    col_a, col_b = st.columns(2)
    with col_a:
        styled_section("Kategori Bazli Memnuniyet (Trafik Isigi)")
        if ist["kategori_ortalama"]:
            st.markdown(_trafik_bar_html(ist["kategori_ortalama"]), unsafe_allow_html=True)

    with col_b:
        styled_section("Puan Dagilimi")
        puan_data = {}
        for p in range(5, 0, -1):
            puan_data[f"{p} - {LIKERT_OLCEK[p]}"] = float(ist["puan_dagilimi"].get(p, 0))
        if any(v > 0 for v in puan_data.values()):
            st.markdown(
                ReportStyler.sunburst_chart_svg(puan_data, title="Likert Dagilimi"),
                unsafe_allow_html=True,
            )

    # Sinif bazli
    if ist["sinif_ortalama"]:
        styled_section("Sınıf Bazlı Ortalamalar")
        sinif_sorted = dict(sorted(ist["sinif_ortalama"].items()))
        sinif_data = {f"{k}. Sınıf": v for k, v in sinif_sorted.items()}
        st.markdown(
            ReportStyler.horizontal_bar_html(sinif_data, "#4472C4", max_val=5.0),
            unsafe_allow_html=True,
        )

    # Kirmizi ve Yesil alanlar yan yana
    soru_ist = store.soru_bazli_istatistik(hedef.id)
    if soru_ist:
        col_c, col_d = st.columns(2)
        with col_c:
            styled_section("En Dusuk Puanli Sorular", "#ef4444")
            dusuk = soru_ist[:5]
            for i, s in enumerate(dusuk, 1):
                r, _, _ = _trafik_renk(s["ortalama"])
                st.markdown(
                    f"""<div style="background:{r}08;border-left:3px solid {r};
                    border-radius:0 8px 8px 0;padding:8px 12px;margin:4px 0">
                    <div style="font-size:0.8rem;color:#64748b">{s['kategori']}</div>
                    <div style="font-size:0.85rem;font-weight:600;color:#94A3B8">{i}. {s['soru'][:80]}</div>
                    <div style="font-size:0.8rem;color:{r};font-weight:700">
                    Ort: {s['ortalama']:.2f} | {s['katilim']} cevap</div>
                    </div>""", unsafe_allow_html=True
                )

        with col_d:
            styled_section("En Yuksek Puanli Sorular", "#10b981")
            yuksek = list(reversed(soru_ist[-5:]))
            for i, s in enumerate(yuksek, 1):
                r, _, _ = _trafik_renk(s["ortalama"])
                st.markdown(
                    f"""<div style="background:{r}08;border-left:3px solid {r};
                    border-radius:0 8px 8px 0;padding:8px 12px;margin:4px 0">
                    <div style="font-size:0.8rem;color:#64748b">{s['kategori']}</div>
                    <div style="font-size:0.85rem;font-weight:600;color:#94A3B8">{i}. {s['soru'][:80]}</div>
                    <div style="font-size:0.8rem;color:{r};font-weight:700">
                    Ort: {s['ortalama']:.2f} | {s['katilim']} cevap</div>
                    </div>""", unsafe_allow_html=True
                )


# ============================================================
# ALT SEKME 2: DONEM YONETIMI
# ============================================================

def _render_donem_yonetimi(store: VeliAnketDataStore):
    from utils.shared_data import SINIF_LISTESI

    styled_section("Donem Yönetimi", "#2563eb")

    user = AuthManager.get_current_user()
    if user.get("role") not in ("Yonetici",):
        styled_info_banner("Bu alana sadece Yonetici rolundeki kullanicilar erisebilir.", banner_type="error", icon="🔒")
        return

    # --- Tüm dönemleri yükle ---
    donemler = store.load_objects("donemler")
    aktif = store.get_aktif_donem()

    # --- Dönem Seç ---
    styled_section("Dönem Seç", "#8b5cf6")

    if not donemler:
        styled_info_banner(
            "Henüz hiç anket dönemi oluşturulmamış. Aşağıdan yeni dönem oluşturabilirsiniz.", banner_type="info", icon="📋")
    else:
        _DURUM_RENK = {
            "Acik": ("#10b981", "🟢"), "Açık": ("#10b981", "🟢"),
            "Taslak": ("#64748b", "📝"), "Kapali": ("#f59e0b", "🟡"),
            "Kilitli": ("#ef4444", "🔒"),
        }

        donemler_sorted = sorted(donemler, key=lambda x: x.created_at, reverse=True)
        donem_secenekler = {
            f"{d.donem_adi}  ({d.baslangic} ~ {d.bitis or '-'})  [{d.durum}]": d
            for d in donemler_sorted
        }

        secilen_label = st.selectbox(
            "Dönem",
            list(donem_secenekler.keys()),
            key="dy_donem_sec",
        )
        secilen: AnketDonemi = donem_secenekler[secilen_label]
        katilimci = store.donem_katilimci_sayisi(secilen.id)
        renk, ikon = _DURUM_RENK.get(secilen.durum, ("#64748b", "📋"))

        # --- Dönem Detay Kartı ---
        _ekler = ""
        if secilen.hedef_siniflar:
            _ekler += f"<div style='margin-top:10px;font-size:0.85rem;color:#94a3b8'><b style=\"color:#e2e8f0\">Hedef Siniflar:</b> {', '.join(secilen.hedef_siniflar)}</div>"
        if secilen.aciklama:
            _ekler += f"<div style='margin-top:6px;font-size:0.85rem;color:#94a3b8'><b style=\"color:#e2e8f0\">Aciklama:</b> {secilen.aciklama}</div>"
        if secilen.olusturan:
            _ekler += f"<div style='margin-top:6px;font-size:0.8rem;color:#64748b'>Olusturan: {secilen.olusturan}</div>"

        st.markdown(
            f"""<div style="background:linear-gradient(135deg,{renk}12 0%,{renk}05 100%);border:1px solid {renk}30;border-radius:14px;padding:20px 24px;margin:10px 0 16px 0">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
<div style="font-size:1.2rem;font-weight:800;color:#94A3B8">{ikon} {secilen.donem_adi}</div>
<span style="background:{renk}20;color:{renk};padding:4px 14px;border-radius:20px;font-size:0.8rem;font-weight:700">{secilen.durum}</span>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">
<div style="background:#1e293b;border-radius:10px;padding:10px 14px;text-align:center;border:1px solid #334155">
<div style="font-size:0.7rem;color:#94a3b8;text-transform:uppercase;font-weight:600">Başlangıç</div>
<div style="font-size:0.95rem;font-weight:700;color:#e2e8f0">{secilen.baslangic}</div>
</div>
<div style="background:#1e293b;border-radius:10px;padding:10px 14px;text-align:center;border:1px solid #334155">
<div style="font-size:0.7rem;color:#94a3b8;text-transform:uppercase;font-weight:600">Bitiş</div>
<div style="font-size:0.95rem;font-weight:700;color:#e2e8f0">{secilen.bitis or '-'}</div>
</div>
<div style="background:#1e293b;border-radius:10px;padding:10px 14px;text-align:center;border:1px solid #334155">
<div style="font-size:0.7rem;color:#94a3b8;text-transform:uppercase;font-weight:600">Katılımcı</div>
<div style="font-size:0.95rem;font-weight:700;color:#e2e8f0">{katilimci}</div>
</div>
</div>{_ekler}</div>""", unsafe_allow_html=True
        )

        # --- İşlem Butonları ---
        b1, b2, b3 = st.columns(3)

        if secilen.durum in ("Acik", "Açık"):
            with b1:
                if st.button("Dönemi Kapat ve Kilitle", type="primary", key="anket_kapat_btn"):
                    secilen.durum = "Kilitli"
                    secilen.updated_at = _now()
                    secilen.toplam_katilimci = katilimci
                    store.upsert("donemler", secilen)
                    st.success("Anket dönemi kilitlendi!")
                    st.rerun()
        elif secilen.durum in ("Taslak", "Kapali", "Kilitli"):
            acik_donem_var = aktif is not None
            with b1:
                if st.button("Anketi Aç", type="primary", key="anket_ac_btn",
                             disabled=acik_donem_var):
                    secilen.durum = "Acik"
                    secilen.baslangic = _today()
                    secilen.updated_at = _now()
                    store.upsert("donemler", secilen)
                    st.success(f"'{secilen.donem_adi}' anketi açıldı!")
                    st.rerun()
            if acik_donem_var:
                styled_info_banner(
                    f"Zaten açık bir dönem var (<b>{aktif.donem_adi}</b>). Önce mevcut dönemi kapatmalısınız.",
                    banner_type="warning", icon="⚠️"
                )

    # --- Yeni Dönem Oluştur ---
    styled_section("Yeni Anket Dönemi Oluştur", "#10b981")
    with st.form("anket_yeni_donem", clear_on_submit=True):
        k1, k2 = st.columns(2)
        with k1:
            donem_adi = st.selectbox(
                "Donem Adi *",
                ["1. Donem", "2. Donem", "Tüm Yil"],
                key="anket_donem_adi_sec",
            )
        with k2:
            sure_gun = st.number_input("Açık Kalma Suresi (gun)",
                                        min_value=1, max_value=60, value=7)

        k3, k4 = st.columns(2)
        with k3:
            bas_tarih = st.date_input("Başlangıç", value=date.today(), key="anket_bas")
        with k4:
            bit_tarih = st.date_input("Bitis",
                                       value=date.today() + timedelta(days=7),
                                       key="anket_bit")

        hedef_siniflar = st.multiselect("Hedef Sınıflar", SINIF_LISTESI,
                                         default=SINIF_LISTESI, key="anket_siniflar")
        aciklama = st.text_area("Açıklama", key="anket_aciklama",
                                 placeholder="Anket hakkinda kisa bilgi...")

        if st.form_submit_button("Donem Oluştur ve Ac", type="primary"):
            if not donem_adi:
                st.error("Donem adi zorunludur.")
            elif aktif:
                st.error("Zaten acik bir donem var. Önce mevcut donemi kapatmalisiniz.")
            else:
                yeni = AnketDonemi(
                    donem_adi=donem_adi,
                    aciklama=aciklama,
                    durum="Açık",
                    baslangic=bas_tarih.isoformat(),
                    bitis=bit_tarih.isoformat(),
                    hedef_siniflar=hedef_siniflar,
                    olusturan=user.get("name", ""),
                )
                store.upsert("donemler", yeni)
                st.success(f"'{donem_adi}' donemi oluşturuldu ve acildi!")
                st.rerun()


# ============================================================
# ALT SEKME 3: ANKETE KATIL
# ============================================================

def _render_ankete_katil(store: VeliAnketDataStore):
    styled_header("Veli Memnuniyet Anketi", "Degerli velimiz, gorusleriniz bizim için onemlidir")

    user = AuthManager.get_current_user()
    if user.get("role") not in ("Veli", "Yonetici"):
        styled_info_banner(
            "Bu anket yalnizca veli hesaplari için aktiftir. Veli hesabinizla giris yapin.", banner_type="error", icon="🔒")
        return

    aktif = store.get_aktif_donem()
    if not aktif:
        styled_info_banner("Su anda aktif bir anket donemi bulunmamaktadir.", banner_type="info", icon="📋")
        return

    styled_info_banner(
        f"<b>{aktif.donem_adi}</b> | Son tarih: <b>{aktif.bitis}</b>", banner_type="success", icon="🟢")

    if "veli_anket_token" not in st.session_state:
        import uuid
        st.session_state["veli_anket_token"] = uuid.uuid4().hex[:12]

    token = st.session_state["veli_anket_token"]

    mevcut = store.katilimci_cevaplari(aktif.id, token)
    if mevcut:
        styled_info_banner(
            f"Bu anket donemi için zaten katilim sagladiniz ({len(mevcut)} cevap). Tesekkur ederiz!",
            banner_type="success", icon="✅"
        )
        return

    from utils.shared_data import SINIF_LISTESI
    sinif = st.selectbox("Cocugunuzun sinifi *", ["Seciniz"] + SINIF_LISTESI,
                          key="anket_sinif_sec")
    if sinif == "Seciniz":
        styled_info_banner("Devam etmek için cocugunuzun sinifini seciniz.", banner_type="warning", icon="⚠️")
        return

    st.markdown("---")

    sorular_by_kat = store.get_sorular_by_kategori()
    cevaplar: dict[str, int] = {}

    for kat in ANKET_KATEGORILERI:
        kat_sorular = sorular_by_kat.get(kat, [])
        if not kat_sorular:
            continue

        ikon = KATEGORI_IKONLARI.get(kat, "")
        renk = KATEGORI_RENKLER.get(kat, "#2563eb")

        st.markdown(
            f"""<div style="background:linear-gradient(135deg,{renk}15 0%,{renk}05 100%);
            border-left:4px solid {renk};border-radius:0 12px 12px 0;
            padding:14px 18px;margin:20px 0 10px 0">
            <span style="font-size:1.3rem">{ikon}</span>
            <span style="font-size:1.1rem;font-weight:700;color:{renk};margin-left:8px">{kat}</span>
            <span style="font-size:0.8rem;color:#64748b;margin-left:8px">({len(kat_sorular)} soru)</span>
            </div>""", unsafe_allow_html=True
        )

        for soru in kat_sorular:
            st.markdown(
                f"""<div style="font-size:0.9rem;font-weight:500;color:#94A3B8;margin:8px 0 4px 8px">
                {soru.sira}. {soru.soru}</div>""", unsafe_allow_html=True
            )
            secim = st.radio(
                f"s_{soru.id}",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} - {LIKERT_OLCEK[x]}",
                horizontal=True,
                key=f"anket_q_{soru.id}",
                label_visibility="collapsed",
            )
            cevaplar[soru.id] = secim

    st.markdown("---")
    styled_section("Görüşleriniz (Opsiyonel)")
    genel_yorum = st.text_area(
        "Eklemek istediginiz goruslerinizi yazabilirsiniz:",
        key="anket_genel_yorum",
        placeholder="Okul hakkindaki genel degerlendimeniz, onerileriniz veya sikayetleriniz...",
        height=100,
    )

    st.markdown("")
    if st.button("Anketi Gonder", type="primary", use_container_width=True,
                  key="anket_gonder_btn"):
        toplam = 0
        for soru_id, puan in cevaplar.items():
            soru = store.get_by_id("sorular", soru_id)
            cevap = AnketCevap(
                donem_id=aktif.id,
                soru_id=soru_id,
                kategori=soru.kategori if soru else "",
                puan=puan,
                anonim_token=token,
                sinif=sinif,
            )
            store.upsert("cevaplar", cevap)
            toplam += 1

        if genel_yorum.strip():
            yorum = AnketYorum(
                donem_id=aktif.id,
                yorum=genel_yorum.strip(),
                anonim_token=token,
                sinif=sinif,
            )
            store.upsert("yorumlar", yorum)

        st.success(f"Anketiniz basariyla kaydedildi! ({toplam} cevap) Katiliminiz için tesekkur ederiz.")
        st.balloons()
        st.rerun()


# ============================================================
# ALT SEKME 4: DEGERLENDIRME (Trafik Isigi)
# ============================================================

def _render_degerlendirme(store: VeliAnketDataStore):
    styled_header("Memnuniyet Değerlendirmesi",
                    "Trafik isigi sistemi: Kirmizi (< 2.5) | Sari (2.5-3.49) | Yesil (>= 3.5)")

    user = AuthManager.get_current_user()
    if user.get("role") not in ("Yonetici", "Öğretmen"):
        styled_info_banner("Bu alana sadece Yonetici ve Öğretmen rolleri erisebilir.", banner_type="error", icon="🔒")
        return

    donemler = store.load_objects("donemler")
    if not donemler:
        styled_info_banner("Henuz anket donemi olusturulmadi.", banner_type="info", icon="📋")
        return

    donem_opt = {d.id: f"{d.donem_adi} ({d.durum})" for d in donemler}
    secili_id = st.selectbox("Donem Sec", list(donem_opt.keys()),
                              format_func=lambda x: donem_opt[x],
                              key="anket_deger_donem")

    ist = store.donem_istatistik(secili_id)
    if ist["toplam_cevap"] == 0:
        styled_info_banner("Bu donem için henuz cevap girilmedi.", banner_type="info", icon="📋")
        return

    rapor = store.trafik_isigi_raporu(secili_id)
    trafik_r, trafik_e, trafik_emoji = _trafik_renk(ist["genel_ortalama"])

    # Ozet istatistikler
    k_kat = len([i for i in rapor["kirmizi"] if i["tip"] == "kategori"])
    s_kat = len([i for i in rapor["sari"] if i["tip"] == "kategori"])
    y_kat = len([i for i in rapor["yesil"] if i["tip"] == "kategori"])
    k_soru = len([i for i in rapor["kirmizi"] if i["tip"] == "soru"])
    s_soru = len([i for i in rapor["sari"] if i["tip"] == "soru"])
    y_soru = len([i for i in rapor["yesil"] if i["tip"] == "soru"])

    styled_stat_row([
        ("Genel Ort.", f"{ist['genel_ortalama']:.2f}", trafik_r, trafik_emoji),
        ("Kirmizi Kat.", str(k_kat), "#ef4444", "🔴"),
        ("Sari Kat.", str(s_kat), "#f59e0b", "🟡"),
        ("Yesil Kat.", str(y_kat), "#10b981", "🟢"),
    ])

    # Esik bilgisi
    st.markdown(
        """<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;padding:12px 16px;
        margin:10px 0;display:flex;gap:24px;justify-content:center;flex-wrap:wrap">
        <span style="display:flex;align-items:center;gap:6px">
        <span style="width:14px;height:14px;border-radius:50%;background:#ef4444;display:inline-block"></span>
        <span style="font-size:0.82rem;color:#334155"><b>Kirmizi:</b> Ort < 2.50 (Basarisiz - Acil Aksiyon)</span></span>
        <span style="display:flex;align-items:center;gap:6px">
        <span style="width:14px;height:14px;border-radius:50%;background:#f59e0b;display:inline-block"></span>
        <span style="font-size:0.82rem;color:#334155"><b>Sari:</b> 2.50 - 3.49 (Kritik - Iyilestirme)</span></span>
        <span style="display:flex;align-items:center;gap:6px">
        <span style="width:14px;height:14px;border-radius:50%;background:#10b981;display:inline-block"></span>
        <span style="font-size:0.82rem;color:#334155"><b>Yesil:</b> Ort >= 3.50 (Memnun)</span></span>
        </div>""", unsafe_allow_html=True
    )

    # Trafik isigi bar chart
    styled_section("Kategori Bazli Trafik Isigi Haritasi")
    if ist["kategori_ortalama"]:
        st.markdown(_trafik_bar_html(ist["kategori_ortalama"]), unsafe_allow_html=True)

    from utils.report_utils import ReportStyler

    # Sunburst chart - trafik isigi dagilimi
    styled_section("Durum Dagilimi")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        durum_data = {}
        if k_kat > 0:
            durum_data["Kirmizi Kategoriler"] = float(k_kat)
        if s_kat > 0:
            durum_data["Sari Kategoriler"] = float(s_kat)
        if y_kat > 0:
            durum_data["Yesil Kategoriler"] = float(y_kat)
        if durum_data:
            st.markdown(
                ReportStyler.sunburst_chart_svg(
                    durum_data, title="Kategori Trafik Dagilimi",
                    inner_colors=["#ef4444", "#f59e0b", "#10b981"],
                ),
                unsafe_allow_html=True,
            )

    with col_sb2:
        durum_soru = {}
        if k_soru > 0:
            durum_soru["Kirmizi Sorular"] = float(k_soru)
        if s_soru > 0:
            durum_soru["Sari Sorular"] = float(s_soru)
        if y_soru > 0:
            durum_soru["Yesil Sorular"] = float(y_soru)
        if durum_soru:
            st.markdown(
                ReportStyler.sunburst_chart_svg(
                    durum_soru, title="Soru Trafik Dagilimi",
                    inner_colors=["#ef4444", "#f59e0b", "#10b981"],
                ),
                unsafe_allow_html=True,
            )

    # 3 trafik isigi grubu kartlari
    if rapor["kirmizi"]:
        st.markdown(
            _trafik_kart(rapor["kirmizi"], "#ef4444", "KIRMIZI - Acil Aksiyon Gereken Alanlar", "🔴"),
            unsafe_allow_html=True,
        )

    if rapor["sari"]:
        st.markdown(
            _trafik_kart(rapor["sari"], "#f59e0b", "SARI - Iyilestirme Gereken Alanlar", "🟡"),
            unsafe_allow_html=True,
        )

    if rapor["yesil"]:
        st.markdown(
            _trafik_kart(rapor["yesil"], "#10b981", "YESIL - Memnuniyet Saglanan Alanlar", "🟢"),
            unsafe_allow_html=True,
        )


# ============================================================
# ALT SEKME 5: DONEM KARSILASTIRMA
# ============================================================

def _render_karsilastirma(store: VeliAnketDataStore):
    styled_header("Dönem Karşılaştırma", "Önceki dönemlerle karşılaştırmalı analiz")

    user = AuthManager.get_current_user()
    if user.get("role") not in ("Yonetici", "Öğretmen"):
        styled_info_banner("Bu alana sadece Yonetici ve Öğretmen rolleri erisebilir.", banner_type="error", icon="🔒")
        return

    donemler = store.load_objects("donemler")
    verili = [d for d in donemler if store.donem_katilimci_sayisi(d.id) > 0]

    if len(verili) < 2:
        styled_info_banner(
            "Karşılaştırma için en az 2 dönem verisi gereklidir. Daha fazla anket dönemi oluşturun.", banner_type="info", icon="📋")
        return

    verili.sort(key=lambda x: x.created_at)
    donem_opt = {d.id: d.donem_adi for d in verili}

    col1, col2 = st.columns(2)
    with col1:
        onceki_id = st.selectbox("Önceki Donem", list(donem_opt.keys()),
                                  format_func=lambda x: donem_opt[x],
                                  key="anket_karsi_onceki")
    with col2:
        sonraki_id = st.selectbox("Sonraki Donem", list(donem_opt.keys()),
                                   format_func=lambda x: donem_opt[x],
                                   index=min(1, len(donem_opt) - 1),
                                   key="anket_karsi_sonraki")

    if onceki_id == sonraki_id:
        styled_info_banner("Farkli iki donem secmelisiniz.", banner_type="warning", icon="⚠️")
        return

    karsi = store.donem_karsilastirma(onceki_id, sonraki_id)

    # Genel degisim
    fark = karsi["genel_fark"]
    fark_renk = "#10b981" if fark > 0.1 else "#ef4444" if fark < -0.1 else "#f59e0b"
    fark_ok = "↑" if fark > 0.1 else "↓" if fark < -0.1 else "→"

    styled_stat_row([
        ("Önceki Ort.", f"{karsi['genel_onceki']:.2f}", "#64748b", "📊"),
        ("Sonraki Ort.", f"{karsi['genel_sonraki']:.2f}", "#2563eb", "📊"),
        ("Degisim", f"{fark:+.2f} {fark_ok}", fark_renk, "📈" if fark > 0 else "📉"),
        ("Katilimci", f"{karsi['katilimci_onceki']}→{karsi['katilimci_sonraki']}", "#8b5cf6", "👥"),
    ])

    from utils.report_utils import ReportStyler

    # Kategori bazli karsilastirma tablosu
    styled_section("Kategori Bazlı Karşılaştırma")
    rows = []
    for kat, data in sorted(karsi["kategori_karsilastirma"].items(),
                             key=lambda x: x[1]["fark"]):
        trend_emoji = "🔼" if data["trend"] == "yukselis" else "🔽" if data["trend"] == "dusus" else "➡️"
        fark_r = "#10b981" if data["fark"] > 0.1 else "#ef4444" if data["fark"] < -0.1 else "#64748b"
        ikon = KATEGORI_IKONLARI.get(kat, "")

        st.markdown(
            f"""<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;
            padding:12px 16px;margin:5px 0;display:flex;align-items:center;justify-content:space-between">
            <div style="display:flex;align-items:center;gap:8px;flex:1">
            <span style="font-size:1.2rem">{ikon}</span>
            <span style="font-weight:700;color:#94A3B8">{kat}</span></div>
            <div style="display:flex;align-items:center;gap:16px">
            <div style="text-align:center;min-width:60px">
            <div style="font-size:0.7rem;color:#94a3b8">Onceki</div>
            <div style="font-weight:700;color:#64748b">{data['onceki']:.2f}</div></div>
            <span style="font-size:1.2rem">{trend_emoji}</span>
            <div style="text-align:center;min-width:60px">
            <div style="font-size:0.7rem;color:#94a3b8">Sonraki</div>
            <div style="font-weight:700;color:#94A3B8">{data['sonraki']:.2f}</div></div>
            <span style="background:{fark_r}15;color:{fark_r};padding:3px 10px;border-radius:8px;
            font-weight:800;font-size:0.85rem;min-width:60px;text-align:center">
            {data['fark']:+.2f}</span>
            </div></div>""", unsafe_allow_html=True
        )

    # Grafik karsilastirma
    styled_section("Görsel Karşılaştırma")
    tum_kat = sorted(karsi["kategori_karsilastirma"].keys())
    if tum_kat:
        onceki_data = {k: karsi["kategori_karsilastirma"][k]["onceki"] for k in tum_kat}
        sonraki_data = {k: karsi["kategori_karsilastirma"][k]["sonraki"] for k in tum_kat}

        col_a, col_b = st.columns(2)
        with col_a:
            styled_section(f"{donem_opt[onceki_id]}", "#64748b")
            st.markdown(
                ReportStyler.horizontal_bar_html(onceki_data, "#94a3b8", max_val=5.0),
                unsafe_allow_html=True,
            )
        with col_b:
            styled_section(f"{donem_opt[sonraki_id]}", "#2563eb")
            st.markdown(
                ReportStyler.horizontal_bar_html(sonraki_data, "#2563eb", max_val=5.0),
                unsafe_allow_html=True,
            )


# ============================================================
# ALT SEKME 6: AI ANALIZ & TAVSIYE
# ============================================================

def _render_ai_analiz(store: VeliAnketDataStore):
    styled_header("AI Analiz & Tavsiyeler", "Yapay zeka destekli degerlendirme ve oneriler")

    user = AuthManager.get_current_user()
    if user.get("role") not in ("Yonetici",):
        styled_info_banner("Bu alana sadece Yonetici rolundeki kullanicilar erisebilir.", banner_type="error", icon="🔒")
        return

    donemler = store.load_objects("donemler")
    if not donemler:
        styled_info_banner("Henuz anket donemi olusturulmadi.", banner_type="info", icon="📋")
        return

    donem_opt = {d.id: f"{d.donem_adi} ({d.durum})" for d in donemler}
    secili_id = st.selectbox("Donem Sec", list(donem_opt.keys()),
                              format_func=lambda x: donem_opt[x],
                              key="anket_ai_donem")

    ist = store.donem_istatistik(secili_id)
    if ist["toplam_cevap"] == 0:
        styled_info_banner("Bu donem için henuz cevap girilmedi.", banner_type="info", icon="📋")
        return

    rapor = store.trafik_isigi_raporu(secili_id)
    yorumlar = store.donem_yorumlar(secili_id)

    if st.button("AI Analiz Raporu Oluştur", type="primary", key="anket_ai_btn",
                  use_container_width=True):
        # Veri ozetini hazirla
        kat_ozet = ""
        for kat, ort in sorted(ist["kategori_ortalama"].items(), key=lambda x: x[1]):
            renk, etiket, _ = _trafik_renk(ort)
            kat_ozet += f"- {kat}: {ort:.2f}/5 ({etiket})\n"

        soru_ist = store.soru_bazli_istatistik(secili_id)
        dusuk_sorular = ""
        for s in soru_ist[:5]:
            dusuk_sorular += f"- [{s['kategori']}] {s['soru']}: {s['ortalama']:.2f}/5\n"
        yuksek_sorular = ""
        for s in reversed(soru_ist[-5:]):
            yuksek_sorular += f"- [{s['kategori']}] {s['soru']}: {s['ortalama']:.2f}/5\n"

        yorum_metni = ""
        for y in yorumlar[:15]:
            yorum_metni += f"- ({y.sinif}. sinif velisi): {y.yorum[:150]}\n"

        kirmizi_kat = [i["ad"] for i in rapor["kirmizi"] if i["tip"] == "kategori"]
        sari_kat = [i["ad"] for i in rapor["sari"] if i["tip"] == "kategori"]

        prompt = f"""Bir okul yoneticisi olarak asagidaki veli memnuniyet anketi verilerini analiz et ve detayli rapor olustur.

GENEL ORTALAMA: {ist['genel_ortalama']:.2f}/5 ({ist['toplam_katilimci']} katilimci)

KATEGORI BAZLI SONUCLAR:
{kat_ozet}

EN DUSUK PUANLI SORULAR:
{dusuk_sorular}

EN YUKSEK PUANLI SORULAR:
{yuksek_sorular}

KIRMIZI KATEGORILER (Acil Aksiyon): {', '.join(kirmizi_kat) if kirmizi_kat else 'Yok'}
SARI KATEGORILER (Iyilestirme): {', '.join(sari_kat) if sari_kat else 'Yok'}

VELI YORUMLARI:
{yorum_metni if yorum_metni else 'Yorum girilmemiş.'}

Lutfen su basliklarda detayli analiz yap:

1. GENEL DEGERLENDIRME: Genel memnuniyet durumu hakkinda kisa analiz.

2. GUCLU YONLER: Yuksek puan alan kategoriler ve sorularin analizi.

3. IYILESTIRILMESI GEREKEN ALANLAR: Dusuk puan alan kategorilerin detayli analizi.

4. ACIL AKSIYON PLANI: Kirmizi bolgede olan kategoriler için somut adimlar.

5. ORTA VADELI ONERILER: Sari bolgede olan kategoriler için iyilestirme onerileri.

6. VELI YORUMLARI ANALIZI: Ortak temalar ve onemli noktalar.

7. STRATEJIK ONERILER: Uzun vadeli iyilestirme stratejisi.

Yaniti Turkce yaz. Her baslik için 3-5 cumle olmali."""

        with st.spinner("AI analiz raporu olusturuluyor..."):
            try:
                from openai import OpenAI
                client = OpenAI()
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Sen bir egitim uzmani ve okul danismanisin. Veli memnuniyet anketlerini analiz edip somut oneriler sunuyorsun."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=2500,
                )
                ai_text = response.choices[0].message.content or ""
                st.session_state["anket_ai_rapor"] = ai_text
            except Exception as e:
                st.error(f"AI analiz olusturulamadi: {e}")
                st.info("OpenAI API anahtarinin dogru ayarlandigindan emin olun.")

    # Kayitli raporu goster
    if "anket_ai_rapor" in st.session_state and st.session_state["anket_ai_rapor"]:
        styled_section("AI Analiz Raporu", "#8b5cf6")
        ai_text = st.session_state["anket_ai_rapor"]
        st.markdown(ai_text)

        # Kopyala butonu
        st.download_button(
            "AI Raporu Indir (TXT)",
            ai_text,
            file_name="veli_memnuniyet_ai_rapor.txt",
            mime="text/plain",
            key="anket_ai_dl",
        )


# ============================================================
# ALT SEKME 7: SONUCLAR & RAPORLAR (Detay + PDF)
# ============================================================

def _render_sonuclar(store: VeliAnketDataStore):
    styled_header("Sonuclar & Raporlar", "Detayli analiz, grafikler ve PDF export")

    user = AuthManager.get_current_user()
    if user.get("role") not in ("Yonetici", "Öğretmen"):
        styled_info_banner("Bu alana sadece Yonetici ve Öğretmen rolleri erisebilir.", banner_type="error", icon="🔒")
        return

    donemler = store.load_objects("donemler")
    if not donemler:
        styled_info_banner("Henuz anket donemi olusturulmadi.", banner_type="info", icon="📋")
        return

    donem_opt = {d.id: f"{d.donem_adi} ({d.durum})" for d in donemler}
    secili_id = st.selectbox("Donem Sec", list(donem_opt.keys()),
                              format_func=lambda x: donem_opt[x],
                              key="anket_sonuc_donem")

    ist = store.donem_istatistik(secili_id)
    if ist["toplam_cevap"] == 0:
        styled_info_banner("Bu donem için henuz cevap girilmedi.", banner_type="info", icon="📋")
        return

    from utils.report_utils import ReportStyler

    s_tab1, s_tab2, s_tab3, s_tab4, s_tab5 = st.tabs([
        "📊 Genel Analiz", "📂 Kategori Detay", "❓ Soru Bazli", "💬 Yorumlar", "📥 PDF Rapor"
    ])

    # ---- GENEL ANALIZ ----
    with s_tab1:
        trafik_r, trafik_e, trafik_emoji = _trafik_renk(ist["genel_ortalama"])
        renk, etiket = _memnuniyet_badge(ist["genel_ortalama"])

        styled_stat_row([
            ("Katilimci", str(ist["toplam_katilimci"]), "#2563eb", "👥"),
            ("Cevap Sayısı", str(ist["toplam_cevap"]), "#8b5cf6", "📝"),
            ("Genel Ort.", f"{ist['genel_ortalama']:.2f}", trafik_r, trafik_emoji),
            ("Durum", trafik_e, trafik_r, "📊"),
        ])

        col1, col2 = st.columns(2)
        with col1:
            styled_section("Kategori Ortalamalari")
            if ist["kategori_ortalama"]:
                sorted_kat = dict(sorted(ist["kategori_ortalama"].items(),
                                         key=lambda x: x[1], reverse=True))
                rows = []
                for kat, ort in sorted_kat.items():
                    tr, te, temoji = _trafik_renk(ort)
                    rows.append({
                        "Kategori": f"{KATEGORI_IKONLARI.get(kat, '')} {kat}",
                        "Ortalama": f"{ort:.2f}",
                        "Durum": f"{temoji} {te}",
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        with col2:
            styled_section("Memnuniyet Haritasi")
            if ist["kategori_ortalama"]:
                st.markdown(
                    _trafik_bar_html(ist["kategori_ortalama"]),
                    unsafe_allow_html=True,
                )

        # Puan dagilimi
        styled_section("Likert Olcek Dagilimi")
        puan_data = {}
        for p in range(5, 0, -1):
            puan_data[f"{p} - {LIKERT_OLCEK[p]}"] = float(ist["puan_dagilimi"].get(p, 0))
        if any(v > 0 for v in puan_data.values()):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown(
                    ReportStyler.sunburst_chart_svg(puan_data, title="Puan Dagilimi"),
                    unsafe_allow_html=True,
                )
            with col_p2:
                toplam_c = sum(ist["puan_dagilimi"].values())
                if toplam_c > 0:
                    for p in range(5, 0, -1):
                        sayi = ist["puan_dagilimi"].get(p, 0)
                        yuzde = sayi / toplam_c * 100
                        st.markdown(
                            f"""<div style="display:flex;align-items:center;gap:8px;margin:4px 0">
                            <span style="min-width:30px;font-weight:700;color:{LIKERT_RENKLER[p]}">{p}</span>
                            <div style="flex:1;background:#e2e8f0;border-radius:8px;height:20px;overflow:hidden">
                            <div style="width:{yuzde:.0f}%;background:{LIKERT_RENKLER[p]};height:100%;
                            border-radius:8px;transition:width 0.3s"></div>
                            </div>
                            <span style="min-width:60px;font-size:0.8rem;color:#64748b;text-align:right">
                            {sayi} (%{yuzde:.0f})</span>
                            </div>""", unsafe_allow_html=True
                        )

    # ---- KATEGORI DETAY ----
    with s_tab2:
        soru_ist = store.soru_bazli_istatistik(secili_id)
        if not soru_ist:
            styled_info_banner("Soru bazli veri yok.", banner_type="info", icon="📋")
        else:
            for kat in ANKET_KATEGORILERI:
                kat_sorulari = [s for s in soru_ist if s["kategori"] == kat]
                if not kat_sorulari:
                    continue

                ikon = KATEGORI_IKONLARI.get(kat, "")
                kat_ort = sum(s["ortalama"] for s in kat_sorulari) / len(kat_sorulari)
                tr, te, temoji = _trafik_renk(kat_ort)

                st.markdown(
                    f"""<div style="background:{tr}08;border:2px solid {tr}30;
                    border-radius:12px;padding:14px 18px;margin:12px 0 8px 0;
                    display:flex;justify-content:space-between;align-items:center">
                    <div><span style="font-size:1.2rem">{ikon}</span>
                    <span style="font-size:1rem;font-weight:700;color:#94A3B8;margin-left:8px">{kat}</span></div>
                    <div style="display:flex;align-items:center;gap:12px">
                    <span style="font-size:1.1rem">{temoji}</span>
                    <span style="background:{tr}20;color:{tr};padding:3px 10px;border-radius:6px;
                    font-size:0.8rem;font-weight:700">{te}</span>
                    <span style="font-size:1.1rem;font-weight:800;color:{tr}">{kat_ort:.2f}</span>
                    </div></div>""", unsafe_allow_html=True
                )

                for s in sorted(kat_sorulari, key=lambda x: x["ortalama"]):
                    sr, se, semoji = _trafik_renk(s["ortalama"])
                    st.markdown(
                        f"""<div style="background:#1e293b;border:1px solid #334155;border-radius:8px;
                        padding:10px 14px;margin:3px 0 3px 20px;display:flex;justify-content:space-between;
                        align-items:center">
                        <div style="flex:1;font-size:0.85rem;color:#e2e8f0">{s['soru']}</div>
                        <div style="display:flex;align-items:center;gap:8px;min-width:140px;justify-content:flex-end">
                        <span style="font-size:0.75rem;color:#64748b">{s['katilim']} cevap</span>
                        <span>{semoji}</span>
                        <span style="background:{sr}20;color:{sr};padding:2px 8px;border-radius:6px;
                        font-weight:700;font-size:0.85rem">{s['ortalama']:.2f}</span>
                        </div></div>""", unsafe_allow_html=True
                    )

    # ---- SORU BAZLI ----
    with s_tab3:
        soru_ist = store.soru_bazli_istatistik(secili_id)
        if soru_ist:
            styled_section("Tüm Sorular (Ortalama Sirasina Gore)")
            rows = []
            for i, s in enumerate(soru_ist, 1):
                tr, te, temoji = _trafik_renk(s["ortalama"])
                rows.append({
                    "#": i,
                    "Kategori": s["kategori"],
                    "Soru": s["soru"][:80],
                    "Ort.": round(s["ortalama"], 2),
                    "Min": s["min"],
                    "Max": s["max"],
                    "Katilim": s["katilim"],
                    "Durum": f"{temoji} {te}",
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)

            csv_buf = io.StringIO()
            df.to_csv(csv_buf, index=False)
            st.download_button(
                "CSV Indir",
                csv_buf.getvalue(),
                file_name="anket_soru_bazli.csv",
                mime="text/csv",
                key="anket_csv_dl",
            )
        else:
            styled_info_banner("Soru bazli veri yok.", banner_type="info", icon="📋")

    # ---- YORUMLAR ----
    with s_tab4:
        yorumlar = store.donem_yorumlar(secili_id)
        if not yorumlar:
            styled_info_banner("Bu donem için yorum girilmedi.", banner_type="info", icon="📋")
        else:
            styled_section(f"Veli Yorumlari ({len(yorumlar)} yorum)")
            for y in yorumlar:
                st.markdown(
                    f"""<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;
                    padding:12px 16px;margin:6px 0;border-left:3px solid #8b5cf6">
                    <div style="font-size:0.85rem;color:#334155;line-height:1.5">{y.yorum}</div>
                    <div style="font-size:0.75rem;color:#94a3b8;margin-top:6px;text-align:right">
                    {y.sinif}. sinif velisi | {y.created_at[:10]}</div>
                    </div>""", unsafe_allow_html=True
                )

    # ---- PDF RAPOR ----
    with s_tab5:
        styled_section("PDF Rapor Oluştur")
        if st.button("Veli Memnuniyet Raporu Oluştur (PDF)", type="primary",
                      key="anket_pdf_btn"):
            try:
                from utils.report_utils import ReportPDFGenerator, get_institution_info
                info = get_institution_info()

                donem = store.get_by_id("donemler", secili_id)
                donem_adi = donem.donem_adi if donem else "Bilinmeyen Donem"
                rapor = store.trafik_isigi_raporu(secili_id)

                pdf = ReportPDFGenerator(
                    title=f"Veli Memnuniyet Anketi Raporu - {donem_adi}",
                    institution_info=info,
                )

                # Ozet
                trafik_r, trafik_e, _ = _trafik_renk(ist["genel_ortalama"])
                pdf.add_header("Genel Özet")
                pdf.add_metrics([
                    ("Katilimci Sayısı", str(ist["toplam_katilimci"])),
                    ("Toplam Cevap", str(ist["toplam_cevap"])),
                    ("Genel Ortalama", f"{ist['genel_ortalama']:.2f} / 5.00"),
                    ("Genel Değerlendirme", trafik_e),
                ])

                # Trafik isigi ozeti
                k_items = [i for i in rapor["kirmizi"] if i["tip"] == "kategori"]
                s_items = [i for i in rapor["sari"] if i["tip"] == "kategori"]
                y_items = [i for i in rapor["yesil"] if i["tip"] == "kategori"]

                pdf.add_header("Trafik Isigi Değerlendirmesi")
                pdf.add_metrics([
                    ("Kirmizi (Başarısız)", f"{len(k_items)} kategori"),
                    ("Sari (Kritik)", f"{len(s_items)} kategori"),
                    ("Yesil (Memnun)", f"{len(y_items)} kategori"),
                ])

                # Kategori bazli sonuclar
                pdf.add_header("Kategori Bazli Sonuclar")
                if ist["kategori_ortalama"]:
                    kat_rows = []
                    sorted_kat = dict(sorted(ist["kategori_ortalama"].items(),
                                             key=lambda x: x[1], reverse=True))
                    for kat, ort in sorted_kat.items():
                        _, e, _ = _trafik_renk(ort)
                        kat_rows.append([kat, f"{ort:.2f}", e])
                    pdf.add_table(
                        headers=["Kategori", "Ortalama", "Durum"],
                        rows=kat_rows,
                    )

                # Kirmizi alanlar detay
                if k_items:
                    pdf.add_header("KIRMIZI ALAN - Acil Aksiyon Gereken Kategoriler")
                    for item in k_items:
                        pdf.add_section(item["ad"], f"Ortalama: {item['ortalama']:.2f}/5 - BASARISIZ")

                if s_items:
                    pdf.add_header("SARI ALAN - Iyilestirme Gereken Kategoriler")
                    for item in s_items:
                        pdf.add_section(item["ad"], f"Ortalama: {item['ortalama']:.2f}/5 - KRITIK")

                # Soru bazli sonuclar
                soru_ist2 = store.soru_bazli_istatistik(secili_id)
                if soru_ist2:
                    pdf.add_header("Soru Bazli Sonuclar")
                    soru_rows = []
                    for s in soru_ist2:
                        _, e, _ = _trafik_renk(s["ortalama"])
                        soru_rows.append([
                            s["kategori"], s["soru"][:55],
                            f"{s['ortalama']:.2f}", str(s["katilim"]), e,
                        ])
                    pdf.add_table(
                        headers=["Kategori", "Soru", "Ort.", "Katilim", "Durum"],
                        rows=soru_rows,
                    )

                # Grafik
                if ist["kategori_ortalama"]:
                    pdf.add_header("Memnuniyet Grafigi")
                    pdf.add_bar_chart(
                        ist["kategori_ortalama"],
                        title="Kategori Bazli Memnuniyet (5 uzerinden)",
                    )

                # Yorumlar
                yorumlar_pdf = store.donem_yorumlar(secili_id)
                if yorumlar_pdf:
                    pdf.add_header("Veli Yorumlari")
                    for y in yorumlar_pdf[:20]:
                        pdf.add_section(
                            f"[{y.sinif}. sinif - {y.created_at[:10]}]",
                            y.yorum[:200],
                        )

                # AI raporu varsa ekle
                if st.session_state.get("anket_ai_rapor"):
                    pdf.add_header("AI Analiz Raporu")
                    ai_text = st.session_state["anket_ai_rapor"]
                    for para in ai_text.split("\n\n"):
                        if para.strip():
                            pdf.add_section("", para.strip()[:300])

                pdf_bytes = pdf.generate()
                st.download_button(
                    "PDF Indir",
                    pdf_bytes,
                    file_name=f"veli_memnuniyet_{donem_adi.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    key="anket_pdf_dl",
                )
                st.success("PDF rapor oluşturuldu!")
            except Exception as e:
                st.error(f"PDF olusturulurken hata: {e}")


# ============================================================
# ALT SEKME 8: SORU YONETIMI
# ============================================================

def _render_soru_yonetimi(store: VeliAnketDataStore):
    styled_section("Soru Yönetimi", "#2563eb")

    user = AuthManager.get_current_user()
    if user.get("role") not in ("Yonetici",):
        styled_info_banner("Bu alana sadece Yonetici rolundeki kullanicilar erisebilir.", banner_type="error", icon="🔒")
        return

    sorular = store.load_objects("sorular")
    aktif_sorular = [s for s in sorular if s.aktif]
    pasif_sorular = [s for s in sorular if not s.aktif]

    styled_stat_row([
        ("Toplam Soru", str(len(sorular)), "#2563eb", "📝"),
        ("Aktif", str(len(aktif_sorular)), "#10b981", "✅"),
        ("Pasif", str(len(pasif_sorular)), "#ef4444", "⛔"),
        ("Kategori", str(len(set(s.kategori for s in aktif_sorular))), "#8b5cf6", "📂"),
    ])

    styled_section("Yeni Soru Ekle", "#10b981")
    with st.form("anket_yeni_soru", clear_on_submit=True):
        k1, k2 = st.columns([2, 1])
        with k1:
            soru_text = st.text_input("Soru Metni *", placeholder="Soru yazin...")
        with k2:
            kategori = st.selectbox("Kategori", ANKET_KATEGORILERI, key="yeni_soru_kat")

        if st.form_submit_button("Soru Ekle", type="primary"):
            if not soru_text:
                st.error("Soru metni zorunludur.")
            else:
                mevcut_kat = [s for s in aktif_sorular if s.kategori == kategori]
                yeni_sira = max((s.sira for s in mevcut_kat), default=0) + 1
                yeni_soru = AnketSoru(
                    kategori=kategori,
                    soru=soru_text,
                    sira=yeni_sira,
                    aktif=True,
                )
                store.upsert("sorular", yeni_soru)
                st.success(f"Soru eklendi: {kategori} / {soru_text[:50]}")
                st.rerun()

    styled_section("Mevcut Sorular")
    for kat in ANKET_KATEGORILERI:
        kat_sorular = [s for s in sorular if s.kategori == kat]
        if not kat_sorular:
            continue
        kat_sorular.sort(key=lambda x: x.sira)

        ikon = KATEGORI_IKONLARI.get(kat, "")

        with st.expander(f"{ikon} {kat} ({len(kat_sorular)} soru)"):
            for s in kat_sorular:
                c1, c2, c3 = st.columns([5, 1, 1])
                with c1:
                    durum_icon = "✅" if s.aktif else "⛔"
                    st.markdown(f"{durum_icon} **{s.sira}.** {s.soru}")
                with c2:
                    btn_label = "Pasif Yap" if s.aktif else "Aktif Yap"
                    if st.button(btn_label, key=f"toggle_{s.id}", use_container_width=True):
                        s.aktif = not s.aktif
                        store.upsert("sorular", s)
                        st.rerun()
                with c3:
                    if st.button("Sil", key=f"del_{s.id}", use_container_width=True):
                        store.delete_by_id("sorular", s.id)
                        st.rerun()


# ============================================================
# ANA RENDER FONKSIYONU
# ============================================================

def render_veli_memnuniyet():
    """Veli Memnuniyet Anketi ana giriş noktası (Yönetim & Sonuçlar)."""
    _inject_css()
    store = _get_anket_store()

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("veli_memnuniyet_egitim_yili")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab_smarti = st.tabs([
        " 📊 Dashboard ", " 📅 Donem Yönetimi ", " 👁️ Anket Onizleme ",
        " ✅ Değerlendirme ", " 🔄 Dönem Karşılaştırma ", " 🤖 AI Analiz ",
        " 📈 Sonuclar & Raporlar ", " ❓ Soru Yönetimi ", " 🤖 Smarti ",
    ])

    with tab1:
        _render_dashboard(store)
    with tab2:
        _render_donem_yonetimi(store)
    with tab3:
        _render_ankete_katil(store)
    with tab4:
        _render_degerlendirme(store)
    with tab5:
        _render_karsilastirma(store)
    with tab6:
        _render_ai_analiz(store)
    with tab7:
        _render_sonuclar(store)
    with tab8:
        _render_soru_yonetimi(store)
    with tab_smarti:
        try:
            from views.ai_destek import render_smarti_chat
            render_smarti_chat(modul="veli_memnuniyet")
        except Exception:
            st.markdown(
                '<div style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;'
                'padding:20px;border-radius:12px;text-align:center;margin:20px 0">'
                '<h3 style="margin:0">🤖 Smarti AI</h3>'
                '<p style="margin:8px 0 0;opacity:.85">Smarti AI asistanı bu modülde aktif. '
                'Sorularınızı yazın, AI destekli yanıtlar alın.</p></div>',
                unsafe_allow_html=True)
            user_q = st.text_area("Smarti'ye sorunuzu yazın:", key="smarti_q_veli_memnuniyet")
            if st.button("Gönder", key="smarti_send_veli_memnuniyet"):
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
                                    {"role": "system", "content": "Sen SmartCampus AI'nin Smarti asistanısın. veli_memnuniyet modülü hakkında Türkçe yardım et."},
                                    {"role": "user", "content": user_q}
                                ],
                                temperature=0.7, max_tokens=500)
                            st.markdown(resp.choices[0].message.content)
                        else:
                            st.warning("API anahtarı tanımlı değil.")
                    except Exception as e:
                        st.error(f"Hata: {e}")
