"""
RZY-01 Randevu ve Ziyaretci Yonetimi Modulu - Streamlit UI
============================================================
Dashboard, randevu yonetimi, ziyaretci giris/cikis,
ziyaretci rehberi, raporlar, ayarlar.
"""

from __future__ import annotations

import os
from datetime import datetime, date, timedelta


import streamlit as st
import pandas as pd

from utils.tenant import get_tenant_dir
from utils.shared_data import (
    get_ik_employee_name_with_position,
    get_tum_modul_randevulari,
)

from utils.auth import AuthManager
from utils.smarti_helper import render_smarti_chat, render_smarti_welcome
from utils.ui_kit import confirm_action
from utils.ui_common import inject_common_css, styled_header, styled_section, styled_stat_row, styled_info_banner
try:
    from utils.ui_common import ultra_premium_baslat
    ultra_premium_baslat("randevu")
except Exception:
    pass
try:
    from utils.ui_common import modul_hosgeldin, bildirim_cani
    bildirim_cani(0)
    modul_hosgeldin("randevu",
        "Randevu yonetimi, ziyaretci giris/cikis, ziyaretci rehberi, raporlar",
        [("6", "Sekme"), ("QR", "Giris"), ("PDF", "Rapor")])
except Exception:
    pass

from models.randevu_ziyaretci import (
    Ziyaretci, Randevu, ZiyaretKaydi, GorusmeNotu,
    RZYDataStore, RandevuAnalizcisi,
    RANDEVU_DURUMLARI, RANDEVU_TURLERI,
    ZIYARETCI_TIPLERI, GORUSME_ALANLARI,
    GORUSULECEK_UNVANLAR,
    _now,
)


# ============================================================
# YARDIMCI FONKSIYONLAR
# ============================================================

def _get_rzy_store() -> RZYDataStore:
    base = os.path.join(get_tenant_dir(), "randevu")
    return RZYDataStore(base)


def _today_str() -> str:
    return date.today().isoformat()


def _gorusulen_bilgi(obj) -> str:
    """Unvan + Kisi bilgisini birlestirerek dondurur."""
    unvan = getattr(obj, "gorusulecek_unvan", "") or ""
    kisi = getattr(obj, "gorusulecek_kisi", "") or ""
    if unvan and kisi:
        return f"{unvan} - {kisi}"
    return unvan or kisi or "-"


# Diger modullerin kaynak renkleri (badge icin)
_KAYNAK_RENK = {
    "Halkla Iliskiler": "#e11d48",
    "Insan Kaynaklari": "#7c3aed",
    "Okul Sagligi": "#059669",
}


def _durum_renk(durum: str) -> str:
    return {
        "Beklemede": "#f59e0b",
        "Onaylandi": "#2563eb",
        "Iptal": "#ef4444",
        "Tamamlandı": "#10b981",
        "Gelmedi": "#64748b",
    }.get(durum, "#64748b")


def _durum_ikon(durum: str) -> str:
    return {
        "Beklemede": "🕐",
        "Onaylandi": "✅",
        "Iptal": "❌",
        "Tamamlandı": "🎯",
        "Gelmedi": "🚫",
    }.get(durum, "📌")


# ============================================================
# CSS STILLERI
# ============================================================

def _inject_rzy_css():
    inject_common_css("rzy")
    st.markdown("""<style>
    :root {
        --rzy-primary: #2563eb;
        --rzy-secondary: #ea580c;
        --rzy-success: #10b981;
        --rzy-warning: #f59e0b;
        --rzy-danger: #ef4444;
        --rzy-purple: #8b5cf6;
        --rzy-dark: #0B0F19;
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

def _render_modul_randevu_karti(rnd: dict):
    """Diger modullerden gelen birlesik randevu kartini render eder."""
    renk = rnd["kaynak_renk"]
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;padding:10px 14px;'
        f'background:{renk}10;border-left:3px solid {renk};border-radius:8px;margin:5px 0;font-size:13px;">'
        f'<span style="font-weight:700;color:{renk};min-width:55px;">{rnd["saat"] or "-"}</span>'
        f'<span style="font-weight:600;color:#94A3B8;">{rnd["kisi"] or "-"}</span>'
        f'<span style="color:#64748b;font-size:12px;">{rnd["tur"]}</span>'
        f'<span style="color:#64748b;margin-left:auto;font-size:12px;">{rnd["detay"]}</span>'
        f'<span style="background:{renk};color:#fff;padding:2px 8px;border-radius:10px;'
        f'font-size:11px;font-weight:600;">{rnd["kaynak_kisa"]} - {rnd["durum"]}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_rzy_randevu_karti(r):
    """Kendi modulumuzun (RZY) randevu kartini render eder."""
    renk = _durum_renk(r.durum)
    ikon = _durum_ikon(r.durum)
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;padding:10px 14px;'
        f'background:{renk}10;border-left:3px solid {renk};border-radius:8px;margin:5px 0;font-size:13px;">'
        f'<span style="font-weight:700;color:{renk};min-width:90px;">'
        f'{ikon} {r.saat_baslangic}-{r.saat_bitis}</span>'
        f'<span style="font-weight:600;color:#94A3B8;">{r.ziyaretci_adi}</span>'
        f'<span style="color:#64748b;margin-left:auto;font-size:12px;">{_gorusulen_bilgi(r)}</span>'
        f'<span style="background:{renk};color:#fff;padding:2px 8px;border-radius:10px;'
        f'font-size:11px;font-weight:600;">{r.durum}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _tarih_aralik_hesapla(filtre: str, ozel_bas=None, ozel_bit=None):
    """Filtre secenerine gore (baslangic, bitis) tarih ciftini dondurur."""
    bugun = date.today()
    if filtre == "Bugün":
        return bugun.isoformat(), bugun.isoformat()
    if filtre == "Bu Hafta":
        bas = bugun - timedelta(days=bugun.weekday())
        bit = bas + timedelta(days=6)
        return bas.isoformat(), bit.isoformat()
    if filtre == "Bu Ay":
        bas = bugun.replace(day=1)
        if bugun.month == 12:
            bit = bugun.replace(year=bugun.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            bit = bugun.replace(month=bugun.month + 1, day=1) - timedelta(days=1)
        return bas.isoformat(), bit.isoformat()
    if filtre == "Bu Yil":
        return f"{bugun.year}-01-01", f"{bugun.year}-12-31"
    if filtre == "Tarih Aralığı" and ozel_bas and ozel_bit:
        return ozel_bas.isoformat(), ozel_bit.isoformat()
    return bugun.isoformat(), bugun.isoformat()


def _render_dashboard(store: RZYDataStore):
    styled_header("Dashboard", "Anlik durum, randevu takibi ve ziyaretciler", icon="📅")

    bugun = _today_str()

    # ── Filtre secimi ──
    styled_section("Randevu Filtresi")
    fc1, fc2, fc3 = st.columns([2, 2, 2])
    with fc1:
        filtre_secim = st.selectbox(
            "Donem",
            ["Bugün", "Bu Hafta", "Bu Ay", "Bu Yil", "Tarih Aralığı"],
            key="rzy_dash_filtre",
        )
    ozel_bas, ozel_bit = None, None
    if filtre_secim == "Tarih Aralığı":
        with fc2:
            ozel_bas = st.date_input("Başlangıç", value=date.today() - timedelta(days=30), key="rzy_dash_bas")
        with fc3:
            ozel_bit = st.date_input("Bitis", value=date.today(), key="rzy_dash_bit")

    filtre_bas, filtre_bit = _tarih_aralik_hesapla(filtre_secim, ozel_bas, ozel_bit)

    # ── KPI - Kendi modulu (RZY) ──
    randevular = store.load_objects("randevular")
    filtre_rnd = [r for r in randevular if filtre_bas <= r.tarih <= filtre_bit]
    bekleyen = sum(1 for r in filtre_rnd if r.durum == "Beklemede")
    tamamlanan = sum(1 for r in filtre_rnd if r.durum == "Tamamlandı")
    gelmedi_s = sum(1 for r in filtre_rnd if r.durum == "Gelmedi")

    # Diger modullerin randevulari
    diger_rnd = get_tum_modul_randevulari(filtre_bas, filtre_bit)
    toplam = len(filtre_rnd) + len(diger_rnd)

    # Aktif ziyaretci (icerde)
    kayitlar = store.load_objects("ziyaret_kayitlari")
    aktif_ziyaretci = sum(1 for k in kayitlar if k.aktif)

    # Gelmeme orani
    biten = tamamlanan + gelmedi_s
    gelmeme_orani = (gelmedi_s / biten * 100) if biten > 0 else 0

    styled_stat_row([
        ("Toplam Randevu", str(toplam), "#2563eb", "📅"),
        ("RZY Randevu", str(len(filtre_rnd)), "#0ea5e9", "🗓️"),
        ("Bekleyen", str(bekleyen), "#f59e0b", "🕐"),
        ("Tamamlanan", str(tamamlanan), "#10b981", "🎯"),
        ("Diger Modul", str(len(diger_rnd)), "#e11d48", "📢"),
        ("Aktif Ziyaretci", str(aktif_ziyaretci), "#8b5cf6", "🏢"),
    ])

    # ── Kaynak dagilimi mini badge ──
    kaynak_sayilari: dict[str, int] = {}
    for d in diger_rnd:
        k_ad = d["kaynak"]
        kaynak_sayilari[k_ad] = kaynak_sayilari.get(k_ad, 0) + 1
    if kaynak_sayilari:
        badge_html = "".join(
            f'<span style="background:{_KAYNAK_RENK.get(k, "#64748b")}18;color:{_KAYNAK_RENK.get(k, "#64748b")};'
            f'padding:4px 12px;border-radius:12px;font-size:12px;font-weight:600;'
            f'border:1px solid {_KAYNAK_RENK.get(k, "#64748b")}30;">{k}: {v}</span>'
            for k, v in kaynak_sayilari.items()
        )
        st.markdown(
            f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin:4px 0 12px;">{badge_html}</div>',
            unsafe_allow_html=True,
        )

    # ── Gecmis / Gelecek / Aktif Ziyaretci ──
    bugun_rnd = [r for r in filtre_rnd if r.tarih == bugun]
    gecmis_rnd = [r for r in filtre_rnd if r.tarih < bugun]
    gelecek_rnd = [r for r in filtre_rnd if r.tarih > bugun]

    gecmis_diger = [d for d in diger_rnd if d["tarih"] < bugun]
    gelecek_diger = [d for d in diger_rnd if d["tarih"] > bugun]
    bugun_diger = [d for d in diger_rnd if d["tarih"] == bugun]

    sub_tabs = st.tabs([
        f"📋 Bugünün Randevuları ({len(bugun_rnd) + len(bugun_diger)})",
        f"📅 Gelecek Randevular ({len(gelecek_rnd) + len(gelecek_diger)})",
        f"📜 Geçmiş Randevular ({len(gecmis_rnd) + len(gecmis_diger)})",
        f"📋 Diğer Rnd ({aktif_ziyaretci})",
    ])

    # ── Tab 1: Bugünün Randevuları ──
    with sub_tabs[0]:
        bugun_rnd_sirali = sorted(bugun_rnd, key=lambda r: r.saat_baslangic)
        bugun_diger_sirali = sorted(bugun_diger, key=lambda d: d["saat"])
        if bugun_rnd_sirali or bugun_diger_sirali:
            if bugun_rnd_sirali:
                st.markdown(
                    '<div style="font-size:12px;font-weight:700;color:#0ea5e9;margin:6px 0 4px;">Randevu ve Ziyaretci</div>',
                    unsafe_allow_html=True,
                )
                for r in bugun_rnd_sirali:
                    _render_rzy_randevu_karti(r)
            if bugun_diger_sirali:
                st.markdown(
                    '<div style="border-top:1px dashed #e2e8f0;margin:8px 0;"></div>'
                    '<div style="font-size:12px;font-weight:700;color:#e11d48;margin:6px 0 4px;">Diger Moduller</div>',
                    unsafe_allow_html=True,
                )
                for d in bugun_diger_sirali:
                    _render_modul_randevu_karti(d)
        else:
            styled_info_banner("Bugüne ait randevu bulunmuyor.", "info", "📅")

    # ── Tab 2: Gelecek Randevular ──
    with sub_tabs[1]:
        gelecek_rzy_sirali = sorted(gelecek_rnd, key=lambda r: (r.tarih, r.saat_baslangic))
        gelecek_diger_sirali = sorted(gelecek_diger, key=lambda d: (d["tarih"], d["saat"]))
        if gelecek_rzy_sirali or gelecek_diger_sirali:
            if gelecek_rzy_sirali:
                st.markdown(
                    '<div style="font-size:12px;font-weight:700;color:#0ea5e9;margin:6px 0 4px;">Randevu ve Ziyaretci</div>',
                    unsafe_allow_html=True,
                )
                _prev_tarih = ""
                for r in gelecek_rzy_sirali:
                    if r.tarih != _prev_tarih:
                        st.markdown(
                            f'<div style="font-size:11px;font-weight:600;color:#64748b;margin:8px 0 2px;'
                            f'padding:2px 8px;background:#0B0F19;border-radius:4px;display:inline-block;">'
                            f'📆 {r.tarih}</div>',
                            unsafe_allow_html=True,
                        )
                        _prev_tarih = r.tarih
                    _render_rzy_randevu_karti(r)
            if gelecek_diger_sirali:
                st.markdown(
                    '<div style="border-top:1px dashed #e2e8f0;margin:8px 0;"></div>'
                    '<div style="font-size:12px;font-weight:700;color:#e11d48;margin:6px 0 4px;">Diger Moduller</div>',
                    unsafe_allow_html=True,
                )
                _prev_tarih = ""
                for d in gelecek_diger_sirali:
                    if d["tarih"] != _prev_tarih:
                        st.markdown(
                            f'<div style="font-size:11px;font-weight:600;color:#64748b;margin:8px 0 2px;'
                            f'padding:2px 8px;background:#0B0F19;border-radius:4px;display:inline-block;">'
                            f'📆 {d["tarih"]}</div>',
                            unsafe_allow_html=True,
                        )
                        _prev_tarih = d["tarih"]
                    _render_modul_randevu_karti(d)
        else:
            styled_info_banner("Secilen donemde gelecek randevu bulunmuyor.", "info", "🔮")

    # ── Tab 3: Geçmiş Randevular ──
    with sub_tabs[2]:
        gecmis_rzy_sirali = sorted(gecmis_rnd, key=lambda r: (r.tarih, r.saat_baslangic), reverse=True)
        gecmis_diger_sirali = sorted(gecmis_diger, key=lambda d: (d["tarih"], d["saat"]), reverse=True)
        if gecmis_rzy_sirali or gecmis_diger_sirali:
            # Tablo gorunumu
            rows = []
            for r in gecmis_rzy_sirali:
                rows.append({
                    "Kaynak": "RZY",
                    "Tarih": r.tarih,
                    "Saat": f"{r.saat_baslangic}-{r.saat_bitis}",
                    "Kisi": r.ziyaretci_adi,
                    "Tur": r.randevu_turu,
                    "Gorusulen": _gorusulen_bilgi(r),
                    "Durum": r.durum,
                })
            for d in gecmis_diger_sirali:
                rows.append({
                    "Kaynak": d["kaynak_kisa"],
                    "Tarih": d["tarih"],
                    "Saat": d["saat"] or "-",
                    "Kisi": d["kisi"],
                    "Tur": d["tur"],
                    "Gorusulen": d["detay"],
                    "Durum": d["durum"],
                })
            rows.sort(key=lambda x: x["Tarih"], reverse=True)
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.caption(f"Toplam: {len(rows)} gecmis randevu")
        else:
            styled_info_banner("Secilen donemde gecmis randevu bulunmuyor.", "info", "📜")

    # ── Tab 4: Aktif Ziyaretçiler (Binada) ──
    with sub_tabs[3]:
        aktif_kayitlar = [k for k in kayitlar if k.aktif]
        if aktif_kayitlar:
            for k in aktif_kayitlar:
                try:
                    giris_saat = k.giris_zamani[11:16]
                except (IndexError, TypeError):
                    giris_saat = "-"
                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:10px;padding:10px 14px;'
                    f'background:#8b5cf610;border-left:3px solid #8b5cf6;border-radius:8px;margin:5px 0;font-size:13px;">'
                    f'<span style="font-weight:700;color:#8b5cf6;">🟢</span>'
                    f'<span style="font-weight:600;color:#94A3B8;">{k.ziyaretci_adi}</span>'
                    f'<span style="color:#64748b;font-size:12px;">Giriş: {giris_saat}</span>'
                    f'<span style="color:#64748b;margin-left:auto;font-size:12px;">{_gorusulen_bilgi(k)}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            styled_info_banner("Su an binada aktif ziyaretci bulunmuyor.", "success", "✅")

    # ── Son 7 gun trendi ──
    styled_section("Son 7 Gün Trendi")
    trend = RandevuAnalizcisi.gunluk_trend(store, 7)
    if any(v["randevu"] > 0 or v["ziyaret"] > 0 for v in trend.values()):
        from utils.report_utils import ReportStyler
        c1b, c2b = st.columns(2)
        with c1b:
            bar_rnd = {t[-5:]: v["randevu"] for t, v in trend.items()}
            st.markdown(ReportStyler.horizontal_bar_html(bar_rnd, "#4472C4"), unsafe_allow_html=True)
            st.caption("Randevular")
        with c2b:
            bar_ziy = {t[-5:]: v["ziyaret"] for t, v in trend.items()}
            st.markdown(ReportStyler.horizontal_bar_html(bar_ziy, "#ED7D31"), unsafe_allow_html=True)
            st.caption("Ziyaretler")
    else:
        styled_info_banner("Henuz veri bulunmuyor.", "info", "📊")

    # ── Son islemler ──
    styled_section("Son İşlemler")
    son_kayitlar = sorted(kayitlar, key=lambda k: k.created_at, reverse=True)[:10]
    if son_kayitlar:
        rows = []
        for k in son_kayitlar:
            durum = "🟢 Icerde" if k.aktif else "🔴 Çıkış Yapti"
            try:
                giris_saat = k.giris_zamani[11:16]
                giris_tarih = k.giris_zamani[:10]
            except (IndexError, TypeError):
                giris_saat = "-"
                giris_tarih = "-"
            try:
                cikis_saat = k.cikis_zamani[11:16] if k.cikis_zamani else "-"
            except (IndexError, TypeError):
                cikis_saat = "-"
            rows.append({
                "Ziyaretci": k.ziyaretci_adi,
                "Tarih": giris_tarih,
                "Giriş": giris_saat,
                "Çıkış": cikis_saat,
                "Gorusulen Unvan": k.gorusulecek_unvan or "-",
                "Gorusulen Kisi": k.gorusulecek_kisi or "-",
                "Alan": k.gorusme_alani,
                "Durum": durum,
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        styled_info_banner("Henuz ziyaret kaydi bulunmuyor.", "info", "📝")


# ============================================================
# SEKME 2: RANDEVU YONETIMI
# ============================================================

def _render_randevu_yonetimi(store: RZYDataStore):
    styled_header("Randevu Yönetimi", "Randevu olusturma, takip ve takvim")

    sub = st.tabs(["➕ Yeni Randevu", "📋 Bugünün Randevuları", "📅 Takvim Görünümü", "📋 Tüm Randevular"])

    # ---- Yeni Randevu ----
    with sub[0]:
        styled_section("Yeni Randevu Oluştur")

        # Mevcut ziyaretciler
        ziyaretciler = store.load_objects("ziyaretciler")
        ziy_secenekler = {"-- Yeni Ziyaretci --": None}
        for z in sorted(ziyaretciler, key=lambda x: x.tam_ad):
            if z.tam_ad:
                label = f"{z.tam_ad} ({z.ziyaretci_tipi})" if z.ziyaretci_tipi else z.tam_ad
                ziy_secenekler[label] = z

        c1, c2 = st.columns(2)
        with c1:
            secilen_ziy_label = st.selectbox("Ziyaretci", list(ziy_secenekler.keys()), key="rzy_yeni_ziy")
            secilen_ziy = ziy_secenekler.get(secilen_ziy_label)

            if secilen_ziy is None:
                st.info("Yeni ziyaretci bilgilerini asagida girin:")
                yeni_ad = st.text_input("Ad", key="rzy_yeni_ad")
                yeni_soyad = st.text_input("Soyad", key="rzy_yeni_soyad")
                yeni_tel = st.text_input("Telefon", key="rzy_yeni_tel")
                yeni_tip = st.selectbox("Ziyaretci Tipi", ZIYARETCI_TIPLERI, key="rzy_yeni_tip")
            else:
                st.success(f"Secilen: {secilen_ziy.tam_ad} - {secilen_ziy.telefon}")

            randevu_turu = st.selectbox("Randevu Turu", RANDEVU_TURLERI, key="rzy_yeni_tur")

        with c2:
            tarih = st.date_input("Tarih", value=date.today(), key="rzy_yeni_tarih")
            saat_bas = st.time_input("Başlangıç Saati", value=datetime.strptime("09:00", "%H:%M").time(), key="rzy_yeni_sbas")
            saat_bit = st.time_input("Bitis Saati", value=datetime.strptime("09:30", "%H:%M").time(), key="rzy_yeni_sbit")

            # Gorusulecek unvan (dropdown)
            unvan_secenekler = ["-- Secim yapin --"] + list(GORUSULECEK_UNVANLAR) + ["+ Yeni Unvan Ekle"]
            gorusulecek_unvan = st.selectbox("Gorusulecek Unvan", unvan_secenekler, key="rzy_yeni_unvan")
            if gorusulecek_unvan == "+ Yeni Unvan Ekle":
                gorusulecek_unvan = st.text_input("Yeni Unvan Girin", key="rzy_yeni_unvan_custom")

            # Gorusulecek kisi (IK calisan listesi)
            ik_isimler = get_ik_employee_name_with_position()
            kisi_secenekler = ["-- Secim yapin --"] + ik_isimler + ["+ Yeni Kisi Ekle"]
            gorusulecek_kisi = st.selectbox("Gorusulecek Kisi", kisi_secenekler, key="rzy_yeni_kisi")
            if gorusulecek_kisi == "+ Yeni Kisi Ekle":
                gorusulecek_kisi = st.text_input("Kisi Adi Girin", key="rzy_yeni_kisi_custom")

            gorusme_alani = st.selectbox("Görüşme Alani", GORUSME_ALANLARI, key="rzy_yeni_alan")

        konu = st.text_input("Konu", key="rzy_yeni_konu")
        notlar = st.text_area("Notlar", key="rzy_yeni_not", height=80)

        if st.button("Randevu Oluştur", type="primary", key="rzy_btn_olustur"):
            # Ziyaretci olustur veya mevcut
            if secilen_ziy is None:
                if not yeni_ad or not yeni_soyad:
                    st.error("Ad ve Soyad zorunludur!")
                    return
                yeni_z = Ziyaretci(
                    ad=yeni_ad, soyad=yeni_soyad,
                    telefon=yeni_tel, ziyaretci_tipi=yeni_tip,
                )
                store.upsert("ziyaretciler", yeni_z)
                ziy_id = yeni_z.id
                ziy_adi = yeni_z.tam_ad
            else:
                ziy_id = secilen_ziy.id
                ziy_adi = secilen_ziy.tam_ad

            unvan_val = gorusulecek_unvan if gorusulecek_unvan != "-- Secim yapin --" else ""
            kisi_val = gorusulecek_kisi.strip() if gorusulecek_kisi not in ("-- Secim yapin --", "+ Yeni Kisi Ekle") else ""

            rnd = Randevu(
                randevu_kodu=store.next_randevu_code(),
                ziyaretci_id=ziy_id,
                ziyaretci_adi=ziy_adi,
                randevu_turu=randevu_turu,
                tarih=tarih.isoformat(),
                saat_baslangic=saat_bas.strftime("%H:%M"),
                saat_bitis=saat_bit.strftime("%H:%M"),
                gorusulecek_unvan=unvan_val,
                gorusulecek_kisi=kisi_val,
                gorusme_alani=gorusme_alani,
                konu=konu,
                notlar=notlar,
                durum="Beklemede",
            )
            store.upsert("randevular", rnd)
            st.success(f"Randevu oluşturuldu: {rnd.randevu_kodu}")
            st.rerun()

    # ---- Bugünün Randevuları ----
    with sub[1]:
        styled_section("Bugünün Randevuları")
        bugun = _today_str()
        randevular = store.load_objects("randevular")
        bugun_rnd = sorted(
            [r for r in randevular if r.tarih == bugun],
            key=lambda r: r.saat_baslangic,
        )

        if not bugun_rnd:
            styled_info_banner("Bugüne ait randevu bulunmuyor.", "info", "📅")
        else:
            for r in bugun_rnd:
                renk = _durum_renk(r.durum)
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{renk}08,{renk}03);'
                    f'border:1px solid {renk}30;border-left:4px solid {renk};'
                    f'border-radius:12px;padding:16px 20px;margin:8px 0;">'
                    f'<div style="display:flex;align-items:center;justify-content:space-between;">'
                    f'<div>'
                    f'<span style="font-weight:700;color:#94A3B8;font-size:15px;">'
                    f'{_durum_ikon(r.durum)} {r.saat_baslangic}-{r.saat_bitis}</span>'
                    f'<span style="margin-left:12px;font-weight:600;color:#94A3B8;">{r.ziyaretci_adi}</span>'
                    f'</div>'
                    f'<span style="background:{renk};color:#fff;padding:4px 12px;border-radius:12px;'
                    f'font-size:12px;font-weight:600;">{r.durum}</span>'
                    f'</div>'
                    f'<div style="margin-top:8px;font-size:13px;color:#64748b;">'
                    f'<b>Tur:</b> {r.randevu_turu} | '
                    f'<b>Gorusulen:</b> {_gorusulen_bilgi(r)} | '
                    f'<b>Alan:</b> {r.gorusme_alani or "-"} | '
                    f'<b>Konu:</b> {r.konu or "-"}'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

                # Durum degistirme butonlari
                if r.durum in ("Beklemede", "Onaylandi"):
                    bcols = st.columns(4)
                    if r.durum == "Beklemede":
                        if bcols[0].button("Onayla", key=f"rzy_onayla_{r.id}"):
                            r.durum = "Onaylandi"
                            r.updated_at = _now()
                            store.upsert("randevular", r)
                            st.rerun()
                    if bcols[1].button("Tamamla", key=f"rzy_tamam_{r.id}"):
                        r.durum = "Tamamlandı"
                        r.updated_at = _now()
                        store.upsert("randevular", r)
                        st.rerun()
                    if bcols[2].button("Gelmedi", key=f"rzy_gelmedi_{r.id}"):
                        r.durum = "Gelmedi"
                        r.updated_at = _now()
                        store.upsert("randevular", r)
                        st.rerun()
                    if bcols[3].button("Iptal", key=f"rzy_iptal_{r.id}"):
                        r.durum = "Iptal"
                        r.updated_at = _now()
                        store.upsert("randevular", r)
                        st.rerun()

    # ---- Takvim Görünümü ----
    with sub[2]:
        styled_section("Haftalık Takvim")
        bugun = date.today()
        hafta_bas = bugun - timedelta(days=bugun.weekday())
        gun_adlari = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"]

        randevular = store.load_objects("randevular")

        # Saat dilimleri
        ayarlar = store.get_ayarlar()
        try:
            bas_saat = int(ayarlar.calisma_baslangic.split(":")[0])
            bit_saat = int(ayarlar.calisma_bitis.split(":")[0])
        except (ValueError, IndexError):
            bas_saat, bit_saat = 8, 17

        # Takvim tablosu
        takvim_rows = []
        for saat in range(bas_saat, bit_saat):
            row = {"Saat": f"{str(saat).zfill(2)}:00"}
            for g_idx, gun_adi in enumerate(gun_adlari):
                gun_tarih = (hafta_bas + timedelta(days=g_idx)).isoformat()
                saat_str = f"{str(saat).zfill(2)}:"
                gun_rnd = [r for r in randevular if r.tarih == gun_tarih and r.saat_baslangic.startswith(saat_str)]
                if gun_rnd:
                    row[gun_adi] = ", ".join(f"{r.ziyaretci_adi} ({r.durum})" for r in gun_rnd)
                else:
                    row[gun_adi] = ""
            takvim_rows.append(row)

        if takvim_rows:
            st.info(f"Hafta: {hafta_bas.isoformat()} - {(hafta_bas + timedelta(days=4)).isoformat()}")
            st.dataframe(pd.DataFrame(takvim_rows), use_container_width=True, hide_index=True)

    # ---- Tüm Randevular ----
    with sub[3]:
        styled_section("Tüm Randevular")

        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            filtre_tarih_bas = st.date_input("Başlangıç", value=date.today() - timedelta(days=30), key="rzy_ft_bas")
        with fc2:
            filtre_tarih_bit = st.date_input("Bitis", value=date.today(), key="rzy_ft_bit")
        with fc3:
            filtre_durum = st.selectbox("Durum", ["Tümü"] + RANDEVU_DURUMLARI, key="rzy_ft_durum")

        randevular = store.load_objects("randevular")
        filtreli = [r for r in randevular
                     if filtre_tarih_bas.isoformat() <= r.tarih <= filtre_tarih_bit.isoformat()]
        if filtre_durum != "Tümü":
            filtreli = [r for r in filtreli if r.durum == filtre_durum]

        filtreli.sort(key=lambda r: (r.tarih, r.saat_baslangic), reverse=True)

        if filtreli:
            rows = []
            for r in filtreli:
                rows.append({
                    "Kod": r.randevu_kodu,
                    "Tarih": r.tarih,
                    "Saat": f"{r.saat_baslangic}-{r.saat_bitis}",
                    "Ziyaretci": r.ziyaretci_adi,
                    "Tur": r.randevu_turu,
                    "Gorusulen Unvan": r.gorusulecek_unvan or "-",
                    "Gorusulen Kisi": r.gorusulecek_kisi or "-",
                    "Alan": r.gorusme_alani or "-",
                    "Durum": f"{_durum_ikon(r.durum)} {r.durum}",
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.caption(f"Toplam: {len(filtreli)} randevu")
        else:
            styled_info_banner("Filtreye uyan randevu bulunamadı.", "info", "📅")

        # Duzenle/Sil
        if filtreli:
            styled_section("Randevu İşlemleri")
            rnd_secenekler = {f"{r.randevu_kodu} - {r.ziyaretci_adi} ({r.tarih})": r for r in filtreli}
            secilen_rnd_label = st.selectbox("Randevu Sec", ["-- Secim yapin --"] + list(rnd_secenekler.keys()), key="rzy_islem_sec")

            if secilen_rnd_label != "-- Secim yapin --":
                secilen_rnd = rnd_secenekler[secilen_rnd_label]
                dc1, dc2 = st.columns(2)
                with dc1:
                    yeni_durum = st.selectbox("Durum Degistir", RANDEVU_DURUMLARI,
                                              index=RANDEVU_DURUMLARI.index(secilen_rnd.durum), key="rzy_islem_durum")
                    if st.button("Durumu Güncelle", key="rzy_btn_durum"):
                        secilen_rnd.durum = yeni_durum
                        secilen_rnd.updated_at = _now()
                        store.upsert("randevular", secilen_rnd)
                        st.success("Durum güncellendi!")
                        st.rerun()
                with dc2:
                    if confirm_action("Randevuyu Sil", "Bu randevuyu silmek istediğinize emin misiniz?", key="rzy_btn_sil"):
                        store.delete_by_id("randevular", secilen_rnd.id)
                        st.success("Randevu silindi!")
                        st.rerun()


# ============================================================
# SEKME 3: ZIYARETCI GIRIS/CIKIS
# ============================================================

def _render_ziyaretci_giris_cikis(store: RZYDataStore):
    styled_header("Ziyaretçi Giriş/Çıkış", "Hızlı giris/cikis kaydi ve aktif ziyaretci takibi")

    sub = st.tabs(["🚶 Giriş Kaydı", "🚪 Çıkış Kaydı", "👥 Aktif Ziyaretçiler"])

    # ---- Giris Kaydi ----
    with sub[0]:
        styled_section("Ziyaretçi Giriş Kaydı")

        ziyaretciler = store.load_objects("ziyaretciler")
        ziy_secenekler = {"-- Yeni Ziyaretci --": None}
        for z in sorted(ziyaretciler, key=lambda x: x.tam_ad):
            if z.tam_ad:
                ziy_secenekler[z.tam_ad] = z

        # Bugun randevusu olanlar
        bugun = _today_str()
        bugun_rnd = [r for r in store.load_objects("randevular")
                      if r.tarih == bugun and r.durum in ("Beklemede", "Onaylandi")]
        if bugun_rnd:
            styled_info_banner(
                f"Bugüne ait <b>{len(bugun_rnd)}</b> bekleyen/onaylanan randevu var.",
                "info", "📅",
            )

        c1, c2 = st.columns(2)
        with c1:
            secilen_label = st.selectbox("Ziyaretci", list(ziy_secenekler.keys()), key="rzy_giris_ziy")
            secilen_z = ziy_secenekler.get(secilen_label)

            if secilen_z is None:
                ad = st.text_input("Ad", key="rzy_giris_ad")
                soyad = st.text_input("Soyad", key="rzy_giris_soyad")
                telefon = st.text_input("Telefon", key="rzy_giris_tel")
                tip = st.selectbox("Ziyaretci Tipi", ZIYARETCI_TIPLERI, key="rzy_giris_tip")

            # Randevu eslestirme
            rnd_opts = {"-- Randevusuz --": None}
            for r in bugun_rnd:
                rnd_opts[f"{r.randevu_kodu} - {r.ziyaretci_adi} ({r.saat_baslangic})"] = r
            secilen_rnd_label = st.selectbox("Randevu Eslestir", list(rnd_opts.keys()), key="rzy_giris_rnd")
            secilen_rnd = rnd_opts.get(secilen_rnd_label)

        with c2:
            neden = st.text_input("Ziyaret Nedeni", key="rzy_giris_neden")

            unvan_secenekler_g = ["-- Secim yapin --"] + list(GORUSULECEK_UNVANLAR) + ["+ Yeni Unvan Ekle"]
            gorusulecek_unvan = st.selectbox("Gorusulecek Unvan", unvan_secenekler_g, key="rzy_giris_unvan")
            if gorusulecek_unvan == "+ Yeni Unvan Ekle":
                gorusulecek_unvan = st.text_input("Yeni Unvan Girin", key="rzy_giris_unvan_custom")

            ik_isimler_g = get_ik_employee_name_with_position()
            kisi_secenekler_g = ["-- Secim yapin --"] + ik_isimler_g + ["+ Yeni Kisi Ekle"]
            gorusulecek_kisi = st.selectbox("Gorusulecek Kisi", kisi_secenekler_g, key="rzy_giris_kisi")
            if gorusulecek_kisi == "+ Yeni Kisi Ekle":
                gorusulecek_kisi = st.text_input("Kisi Adi Girin", key="rzy_giris_kisi_custom")

            gorusme_alani = st.selectbox("Görüşme Alani", GORUSME_ALANLARI, key="rzy_giris_alan")

            kart_no = st.text_input("Ziyaretci Kart No", key="rzy_giris_kart")
            plaka = st.text_input("Arac Plaka", key="rzy_giris_plaka")

        # Randevudan otomatik doldurma
        if secilen_rnd:
            if not neden:
                neden = secilen_rnd.konu
            giris_unvan = secilen_rnd.gorusulecek_unvan
            giris_kisi = secilen_rnd.gorusulecek_kisi
        else:
            giris_unvan = gorusulecek_unvan if gorusulecek_unvan != "-- Secim yapin --" else ""
            giris_kisi = gorusulecek_kisi.strip() if gorusulecek_kisi not in ("-- Secim yapin --", "+ Yeni Kisi Ekle") else ""

        notlar = st.text_area("Notlar", key="rzy_giris_not", height=60)

        if st.button("Giriş Kaydi Oluştur", type="primary", key="rzy_btn_giris"):
            if secilen_z is None:
                if not ad or not soyad:
                    st.error("Ad ve Soyad zorunludur!")
                    return
                yeni_z = Ziyaretci(ad=ad, soyad=soyad, telefon=telefon, ziyaretci_tipi=tip)
                store.upsert("ziyaretciler", yeni_z)
                ziy_id = yeni_z.id
                ziy_adi = yeni_z.tam_ad
            else:
                ziy_id = secilen_z.id
                ziy_adi = secilen_z.tam_ad

            zk = ZiyaretKaydi(
                ziyaret_kodu=store.next_ziyaret_code(),
                ziyaretci_id=ziy_id,
                ziyaretci_adi=ziy_adi,
                randevu_id=secilen_rnd.id if secilen_rnd else "",
                giris_zamani=_now(),
                ziyaret_nedeni=neden,
                gorusulecek_unvan=giris_unvan,
                gorusulecek_kisi=giris_kisi,
                gorusme_alani=gorusme_alani,
                kart_no=kart_no,
                arac_plaka=plaka,
                notlar=notlar,
            )
            store.upsert("ziyaret_kayitlari", zk)

            # Randevu durumunu guncelle
            if secilen_rnd:
                secilen_rnd.durum = "Tamamlandı"
                secilen_rnd.updated_at = _now()
                store.upsert("randevular", secilen_rnd)

            st.success(f"Giriş kaydi oluşturuldu: {zk.ziyaret_kodu} - {ziy_adi}")
            st.rerun()

    # ---- Cikis Kaydi ----
    with sub[1]:
        styled_section("Ziyaretci Çıkış Kaydi")

        kayitlar = store.load_objects("ziyaret_kayitlari")
        aktif_kayitlar = [k for k in kayitlar if k.aktif]

        if not aktif_kayitlar:
            styled_info_banner("Çıkış bekleyen ziyaretci bulunmuyor.", "success", "✅")
        else:
            st.info(f"{len(aktif_kayitlar)} ziyaretci binada")
            for k in aktif_kayitlar:
                try:
                    giris_saat = k.giris_zamani[11:16]
                except (IndexError, TypeError):
                    giris_saat = "-"

                st.markdown(
                    f'<div style="display:flex;align-items:center;gap:10px;padding:12px 16px;'
                    f'background:#8b5cf610;border-left:3px solid #8b5cf6;border-radius:8px;margin:6px 0;">'
                    f'<span style="font-weight:700;color:#8b5cf6;">🟢</span>'
                    f'<span style="font-weight:600;color:#94A3B8;font-size:14px;">{k.ziyaretci_adi}</span>'
                    f'<span style="color:#64748b;font-size:13px;">Giriş: {giris_saat}</span>'
                    f'<span style="color:#64748b;font-size:13px;margin-left:auto;">{_gorusulen_bilgi(k)}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                if st.button(f"Çıkış Yap - {k.ziyaretci_adi}", key=f"rzy_cikis_{k.id}"):
                    k.cikis_zamani = _now()
                    store.upsert("ziyaret_kayitlari", k)
                    st.success(f"{k.ziyaretci_adi} cikis yapti! (Sure: {k.sure_dk:.0f} dk)")
                    st.rerun()

    # ---- Aktif Ziyaretçiler ----
    with sub[2]:
        styled_section("Aktif Ziyaretçiler (Binada)")

        kayitlar = store.load_objects("ziyaret_kayitlari")
        aktif = [k for k in kayitlar if k.aktif]

        styled_stat_row([
            ("Binada", str(len(aktif)), "#8b5cf6", "🏢"),
            ("Bugün Toplam", str(sum(1 for k in kayitlar if k.giris_zamani[:10] == _today_str())), "#2563eb", "📊"),
        ])

        if aktif:
            rows = []
            for k in aktif:
                try:
                    giris = k.giris_zamani[11:16]
                    giris_dt = datetime.fromisoformat(k.giris_zamani)
                    bekleme = int((datetime.now() - giris_dt).total_seconds() / 60)
                except (ValueError, TypeError, IndexError):
                    giris = "-"
                    bekleme = 0
                rows.append({
                    "Ziyaretci": k.ziyaretci_adi,
                    "Giriş Saati": giris,
                    "Bekleme (dk)": bekleme,
                    "Gorusulen Unvan": k.gorusulecek_unvan or "-",
                    "Gorusulen Kisi": k.gorusulecek_kisi or "-",
                    "Alan": k.gorusme_alani or "-",
                    "Neden": k.ziyaret_nedeni or "-",
                    "Kart No": k.kart_no or "-",
                    "Plaka": k.arac_plaka or "-",
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner("Su an binada aktif ziyaretci bulunmuyor.", "success", "✅")


# ============================================================
# SEKME 4: ZIYARETCI REHBERI
# ============================================================

def _render_ziyaretci_rehberi(store: RZYDataStore):
    styled_header("Ziyaretçi Rehberi", "Kayıtli ziyaretciler ve gecmis bilgileri")

    sub = st.tabs(["📋 Ziyaretçi Listesi", "➕ Yeni Ziyaretçi Ekle"])

    # ---- Ziyaretçi Listesi ----
    with sub[0]:
        styled_section("Kayıtlı Ziyaretçiler")
        ziyaretciler = store.load_objects("ziyaretciler")

        if not ziyaretciler:
            styled_info_banner("Henuz kayitli ziyaretci bulunmuyor.", "info", "👤")
        else:
            # Ziyaret gecmisi istatistikleri
            kayitlar = store.load_objects("ziyaret_kayitlari")
            ziy_ziyaret_sayisi: dict[str, int] = {}
            ziy_son_ziyaret: dict[str, str] = {}
            for k in kayitlar:
                zid = k.ziyaretci_id
                ziy_ziyaret_sayisi[zid] = ziy_ziyaret_sayisi.get(zid, 0) + 1
                mevcut = ziy_son_ziyaret.get(zid, "")
                if k.giris_zamani > mevcut:
                    ziy_son_ziyaret[zid] = k.giris_zamani

            rows = []
            for z in sorted(ziyaretciler, key=lambda x: x.tam_ad):
                son = ziy_son_ziyaret.get(z.id, "")[:10] or "-"
                rows.append({
                    "Ad Soyad": z.tam_ad,
                    "Tipi": z.ziyaretci_tipi or "-",
                    "Telefon": z.telefon or "-",
                    "Email": z.email or "-",
                    "Kurum": z.kurum or "-",
                    "Ziyaret Sayısı": ziy_ziyaret_sayisi.get(z.id, 0),
                    "Son Ziyaret": son,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.caption(f"Toplam: {len(ziyaretciler)} kayitli ziyaretci")

            # Detay / Sil
            styled_section("Ziyaretci İşlemleri")
            z_opts = {f"{z.tam_ad} ({z.ziyaretci_tipi})": z for z in ziyaretciler if z.tam_ad}
            z_sec = st.selectbox("Ziyaretci Sec", ["-- Secim yapin --"] + list(z_opts.keys()), key="rzy_rehber_sec")

            if z_sec != "-- Secim yapin --":
                z_obj = z_opts[z_sec]

                ec1, ec2 = st.columns(2)
                with ec1:
                    styled_section("Bilgileri Düzenle")
                    yeni_ad = st.text_input("Ad", value=z_obj.ad, key="rzy_duz_ad")
                    yeni_soyad = st.text_input("Soyad", value=z_obj.soyad, key="rzy_duz_soyad")
                    yeni_tel = st.text_input("Telefon", value=z_obj.telefon, key="rzy_duz_tel")
                    yeni_email = st.text_input("Email", value=z_obj.email, key="rzy_duz_email")
                    yeni_kurum = st.text_input("Kurum", value=z_obj.kurum, key="rzy_duz_kurum")
                    yeni_tip = st.selectbox("Tip", ZIYARETCI_TIPLERI,
                                             index=ZIYARETCI_TIPLERI.index(z_obj.ziyaretci_tipi) if z_obj.ziyaretci_tipi in ZIYARETCI_TIPLERI else 0,
                                             key="rzy_duz_tip")

                    if st.button("Güncelle", key="rzy_btn_guncelle"):
                        z_obj.ad = yeni_ad
                        z_obj.soyad = yeni_soyad
                        z_obj.telefon = yeni_tel
                        z_obj.email = yeni_email
                        z_obj.kurum = yeni_kurum
                        z_obj.ziyaretci_tipi = yeni_tip
                        z_obj.updated_at = _now()
                        store.upsert("ziyaretciler", z_obj)
                        st.success("Ziyaretci güncellendi!")
                        st.rerun()

                with ec2:
                    styled_section("Ziyaret Geçmişi")
                    z_kayitlar = [k for k in kayitlar if k.ziyaretci_id == z_obj.id]
                    z_kayitlar.sort(key=lambda k: k.giris_zamani, reverse=True)
                    if z_kayitlar:
                        for k in z_kayitlar[:10]:
                            try:
                                tarih = k.giris_zamani[:10]
                                saat = k.giris_zamani[11:16]
                            except (IndexError, TypeError):
                                tarih, saat = "-", "-"
                            sure = f"{k.sure_dk:.0f} dk" if k.sure_dk > 0 else "Devam ediyor"
                            st.markdown(
                                f'<div style="padding:6px 10px;background:#0B0F19;border-radius:6px;margin:3px 0;font-size:13px;">'
                                f'<b>{tarih}</b> {saat} - {_gorusulen_bilgi(k)} ({sure})'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.info("Ziyaret gecmisi yok.")

                    if confirm_action("Ziyaretçiyi Sil", "Bu ziyaretçiyi kayıtlardan silmek istediğinize emin misiniz?", key="rzy_btn_ziy_sil"):
                        store.delete_by_id("ziyaretciler", z_obj.id)
                        st.success("Ziyaretçi silindi!")
                        st.rerun()

    # ---- Yeni Ziyaretçi Ekle ----
    with sub[1]:
        styled_section("Yeni Ziyaretci Kaydi")

        c1, c2 = st.columns(2)
        with c1:
            ad = st.text_input("Ad", key="rzy_ekle_ad")
            soyad = st.text_input("Soyad", key="rzy_ekle_soyad")
            telefon = st.text_input("Telefon", key="rzy_ekle_tel")
            email = st.text_input("Email", key="rzy_ekle_email")
        with c2:
            tc = st.text_input("TC Kimlik No", key="rzy_ekle_tc")
            kurum = st.text_input("Kurum", key="rzy_ekle_kurum")
            tip = st.selectbox("Ziyaretci Tipi", ZIYARETCI_TIPLERI, key="rzy_ekle_tip")
            notlar = st.text_area("Notlar", key="rzy_ekle_not", height=80)

        if st.button("Ziyaretci Ekle", type="primary", key="rzy_btn_ekle"):
            if not ad or not soyad:
                st.error("Ad ve Soyad zorunludur!")
            else:
                z = Ziyaretci(
                    ad=ad, soyad=soyad, telefon=telefon, email=email,
                    tc_kimlik=tc, kurum=kurum, ziyaretci_tipi=tip, notlar=notlar,
                )
                store.upsert("ziyaretciler", z)
                st.success(f"Ziyaretci eklendi: {z.tam_ad}")
                st.rerun()


# ============================================================
# SEKME 5: RAPORLAR
# ============================================================

def _render_raporlar(store: RZYDataStore):
    styled_header("Raporlar", "Günlük, haftalik, aylik, yillik ve karsilastirmali raporlar")

    sub = st.tabs(["📅 Günlük", "📅 Haftalık", "📅 Aylık", "📅 Yıllık", "📅 Tarih Aralığı", "📊 Karşılaştırma"])

    # ---- Günlük ----
    with sub[0]:
        styled_section("Günlük Rapor")
        secilen = st.date_input("Tarih", value=date.today(), key="rzy_rap_gun")
        tarih_str = secilen.isoformat()

        ozet = RandevuAnalizcisi.donem_ozet(store, tarih_str, tarih_str)
        ziy_ozet = RandevuAnalizcisi.ziyaret_ozet(store, tarih_str, tarih_str)

        styled_stat_row([
            ("Randevu", str(ozet["toplam_randevu"]), "#2563eb", "📅"),
            ("Tamamlanan", str(ozet["tamamlanan"]), "#10b981", "🎯"),
            ("Iptal", str(ozet["iptal"]), "#ef4444", "❌"),
            ("Gelmedi", str(ozet["gelmedi"]), "#64748b", "🚫"),
            ("Ziyaret", str(ziy_ozet["toplam_ziyaret"]), "#8b5cf6", "🏢"),
            ("Ort. Sure", f"{ziy_ozet['ortalama_sure_dk']:.0f} dk", "#ea580c", "⏱️"),
        ])

        if ozet["tur_dagilimi"] or ziy_ozet["saat_dagilimi"]:
            from utils.report_utils import ReportStyler
            col1, col2 = st.columns(2)
            with col1:
                if ozet["tur_dagilimi"]:
                    styled_section("Randevu Tur Dagilimi")
                    tur_data = {k: float(v) for k, v in ozet["tur_dagilimi"].items() if v > 0}
                    if tur_data:
                        st.markdown(ReportStyler.sunburst_chart_svg(tur_data, size=175), unsafe_allow_html=True)
            with col2:
                if ziy_ozet["saat_dagilimi"]:
                    styled_section("Saat Bazli Yogunluk")
                    st.markdown(
                        ReportStyler.horizontal_bar_html(ziy_ozet["saat_dagilimi"], "#4472C4"),
                        unsafe_allow_html=True,
                    )

        if ozet["en_cok_gorusen"]:
            styled_section("En Çok Gorusen Kisiler")
            rows = [{"Kisi": k, "Randevu Sayısı": s} for k, s in ozet["en_cok_gorusen"]]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ---- Haftalık ----
    with sub[1]:
        styled_section("Haftalık Rapor")
        bugun = date.today()
        hafta_bas = (bugun - timedelta(days=bugun.weekday())).isoformat()
        hafta_bit = bugun.isoformat()
        st.info(f"Bu hafta: {hafta_bas} - {hafta_bit}")

        ozet = RandevuAnalizcisi.donem_ozet(store, hafta_bas, hafta_bit)
        ziy_ozet = RandevuAnalizcisi.ziyaret_ozet(store, hafta_bas, hafta_bit)

        styled_stat_row([
            ("Randevu", str(ozet["toplam_randevu"]), "#2563eb", "📅"),
            ("Tamamlanan", str(ozet["tamamlanan"]), "#10b981", "🎯"),
            ("Gelmedi", str(ozet["gelmedi"]), "#64748b", "🚫"),
            ("Ziyaret", str(ziy_ozet["toplam_ziyaret"]), "#8b5cf6", "🏢"),
        ])

        trend = RandevuAnalizcisi.gunluk_trend(store, 7)
        if any(v["randevu"] > 0 for v in trend.values()):
            from utils.report_utils import ReportStyler
            col1, col2 = st.columns(2)
            with col1:
                styled_section("Gün Bazli Randevular")
                gun_adlari = ["Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz"]
                bar_data = {}
                for t, v in trend.items():
                    try:
                        d = date.fromisoformat(t)
                        gun_adi = gun_adlari[d.weekday()]
                        bar_data[f"{gun_adi} ({t[-5:]})"] = v["randevu"]
                    except (ValueError, IndexError):
                        bar_data[t] = v["randevu"]
                st.markdown(ReportStyler.horizontal_bar_html(bar_data, "#4472C4"), unsafe_allow_html=True)
            with col2:
                if ozet["tur_dagilimi"]:
                    styled_section("Randevu Tur Dagilimi")
                    tur_data = {k: float(v) for k, v in ozet["tur_dagilimi"].items() if v > 0}
                    if tur_data:
                        st.markdown(ReportStyler.sunburst_chart_svg(tur_data, size=175), unsafe_allow_html=True)

    # ---- Aylık ----
    with sub[2]:
        styled_section("Aylık Rapor")
        bugun = date.today()
        ay_bas = bugun.replace(day=1).isoformat()
        ay_bit = bugun.isoformat()
        st.info(f"Bu ay: {ay_bas} - {ay_bit}")

        ozet = RandevuAnalizcisi.donem_ozet(store, ay_bas, ay_bit)
        ziy_ozet = RandevuAnalizcisi.ziyaret_ozet(store, ay_bas, ay_bit)

        styled_stat_row([
            ("Randevu", str(ozet["toplam_randevu"]), "#2563eb", "📅"),
            ("Tamamlanan", str(ozet["tamamlanan"]), "#10b981", "🎯"),
            ("Iptal", str(ozet["iptal"]), "#ef4444", "❌"),
            ("Ziyaret", str(ziy_ozet["toplam_ziyaret"]), "#8b5cf6", "🏢"),
            ("Ort. Sure", f"{ziy_ozet['ortalama_sure_dk']:.0f} dk", "#ea580c", "⏱️"),
        ])

        # Onceki ayla karsilastirma
        onceki_ay_bit = (bugun.replace(day=1) - timedelta(days=1))
        onceki_ay_bas = onceki_ay_bit.replace(day=1).isoformat()
        onceki_ay_bit_str = onceki_ay_bit.isoformat()

        kars = RandevuAnalizcisi.karsilastir(store, onceki_ay_bas, onceki_ay_bit_str, ay_bas, ay_bit)
        degisim = kars["randevu_degisim"]
        ok = "📈" if degisim > 0 else "📉" if degisim < 0 else "➡️"
        renk = "#ef4444" if degisim > 0 else "#10b981" if degisim < 0 else "#64748b"
        _btype = "error" if degisim > 0 else "success" if degisim < 0 else "info"
        styled_info_banner(
            f"Önceki aya gore randevu degisimi: <b style='color:{renk};'>%{degisim:+.1f} {ok}</b>",
            _btype, "📊",
        )

        if ozet["tur_dagilimi"]:
            from utils.report_utils import ReportStyler
            col1, col2 = st.columns(2)
            with col1:
                styled_section("Randevu Tur Dagilimi")
                tur_data = {k: float(v) for k, v in ozet["tur_dagilimi"].items() if v > 0}
                if tur_data:
                    st.markdown(ReportStyler.sunburst_chart_svg(tur_data, size=175), unsafe_allow_html=True)
            with col2:
                if ozet["alan_dagilimi"]:
                    styled_section("Görüşme Alani Dagilimi")
                    alan_data = {k: float(v) for k, v in ozet["alan_dagilimi"].items() if v > 0}
                    if alan_data:
                        st.markdown(ReportStyler.horizontal_bar_html(alan_data, "#ED7D31"), unsafe_allow_html=True)

    # ---- Yıllık ----
    with sub[3]:
        styled_section("Yıllık Rapor")
        bugun = date.today()
        yil_bas = bugun.replace(month=1, day=1).isoformat()
        yil_bit = bugun.isoformat()
        st.info(f"Bu yil: {yil_bas} - {yil_bit}")

        ozet = RandevuAnalizcisi.donem_ozet(store, yil_bas, yil_bit)
        ziy_ozet = RandevuAnalizcisi.ziyaret_ozet(store, yil_bas, yil_bit)

        styled_stat_row([
            ("Toplam Randevu", str(ozet["toplam_randevu"]), "#2563eb", "📅"),
            ("Tamamlanan", str(ozet["tamamlanan"]), "#10b981", "🎯"),
            ("Iptal", str(ozet["iptal"]), "#ef4444", "❌"),
            ("Gelmedi", str(ozet["gelmedi"]), "#64748b", "🚫"),
            ("Toplam Ziyaret", str(ziy_ozet["toplam_ziyaret"]), "#8b5cf6", "🏢"),
            ("Ort. Sure", f"{ziy_ozet['ortalama_sure_dk']:.0f} dk", "#ea580c", "⏱️"),
        ])

        # Ay bazli trend
        ay_adlari = ["Oca", "Sub", "Mar", "Nis", "May", "Haz", "Tem", "Agu", "Eyl", "Eki", "Kas", "Ara"]
        ay_verileri: dict[str, int] = {}
        for ay in range(1, bugun.month + 1):
            ay_bas_t = bugun.replace(month=ay, day=1).isoformat()
            if ay < 12:
                ay_bit_t = (bugun.replace(month=ay + 1, day=1) - timedelta(days=1)).isoformat()
            else:
                ay_bit_t = bugun.replace(month=12, day=31).isoformat()
            if ay == bugun.month:
                ay_bit_t = bugun.isoformat()
            ay_ozet = RandevuAnalizcisi.donem_ozet(store, ay_bas_t, ay_bit_t)
            ay_verileri[ay_adlari[ay - 1]] = ay_ozet["toplam_randevu"]

        if any(v > 0 for v in ay_verileri.values()):
            from utils.report_utils import ReportStyler
            styled_section("Ay Bazli Randevu Trendi")
            st.markdown(
                ReportStyler.horizontal_bar_html(ay_verileri, "#4472C4"),
                unsafe_allow_html=True,
            )

        if ozet["tur_dagilimi"]:
            from utils.report_utils import ReportStyler
            col1, col2 = st.columns(2)
            with col1:
                styled_section("Randevu Tur Dagilimi")
                tur_data = {k: float(v) for k, v in ozet["tur_dagilimi"].items() if v > 0}
                if tur_data:
                    st.markdown(ReportStyler.sunburst_chart_svg(tur_data, size=175), unsafe_allow_html=True)
            with col2:
                if ozet["en_cok_gorusen"]:
                    styled_section("En Çok Gorusen Kisiler")
                    rows = [{"Kisi": k, "Randevu": s} for k, s in ozet["en_cok_gorusen"]]
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ---- Tarih Aralığı ----
    with sub[4]:
        styled_section("Tarih Aralığı Raporu")
        tc1, tc2 = st.columns(2)
        with tc1:
            ta_bas = st.date_input("Başlangıç", value=date.today() - timedelta(days=30), key="rzy_ta_bas")
        with tc2:
            ta_bit = st.date_input("Bitis", value=date.today(), key="rzy_ta_bit")

        ozet = RandevuAnalizcisi.donem_ozet(store, ta_bas.isoformat(), ta_bit.isoformat())
        ziy_ozet = RandevuAnalizcisi.ziyaret_ozet(store, ta_bas.isoformat(), ta_bit.isoformat())

        styled_stat_row([
            ("Randevu", str(ozet["toplam_randevu"]), "#2563eb", "📅"),
            ("Tamamlanan", str(ozet["tamamlanan"]), "#10b981", "🎯"),
            ("Iptal", str(ozet["iptal"]), "#ef4444", "❌"),
            ("Gelmedi", str(ozet["gelmedi"]), "#64748b", "🚫"),
            ("Ziyaret", str(ziy_ozet["toplam_ziyaret"]), "#8b5cf6", "🏢"),
            ("Ort. Sure", f"{ziy_ozet['ortalama_sure_dk']:.0f} dk", "#ea580c", "⏱️"),
        ])

        if ozet["tur_dagilimi"] or ozet["alan_dagilimi"]:
            from utils.report_utils import ReportStyler
            col1, col2 = st.columns(2)
            with col1:
                if ozet["tur_dagilimi"]:
                    styled_section("Randevu Tur Dagilimi")
                    tur_data = {k: float(v) for k, v in ozet["tur_dagilimi"].items() if v > 0}
                    if tur_data:
                        st.markdown(ReportStyler.sunburst_chart_svg(tur_data, size=175), unsafe_allow_html=True)
            with col2:
                if ozet["alan_dagilimi"]:
                    styled_section("Görüşme Alani Dagilimi")
                    alan_data = {k: float(v) for k, v in ozet["alan_dagilimi"].items() if v > 0}
                    if alan_data:
                        st.markdown(ReportStyler.horizontal_bar_html(alan_data, "#ED7D31"), unsafe_allow_html=True)

        if ziy_ozet["tip_dagilimi"]:
            from utils.report_utils import ReportStyler
            styled_section("Ziyaretci Tipi Dagilimi")
            tip_data = {k: float(v) for k, v in ziy_ozet["tip_dagilimi"].items() if v > 0}
            if tip_data:
                st.markdown(ReportStyler.sunburst_chart_svg(tip_data, size=300, title="Ziyaretci Tipi"), unsafe_allow_html=True)

        if ozet["en_cok_gorusen"]:
            styled_section("En Çok Gorusen Kisiler")
            rows = [{"Kisi": k, "Randevu Sayısı": s} for k, s in ozet["en_cok_gorusen"]]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ---- Karşılaştırma ----
    with sub[5]:
        styled_section("Donem Karşılaştırma")

        kc1, kc2, kc3, kc4 = st.columns(4)
        with kc1:
            d1_bas = st.date_input("Donem 1 Bas", value=date.today() - timedelta(days=60), key="rzy_k_d1b")
        with kc2:
            d1_bit = st.date_input("Donem 1 Bit", value=date.today() - timedelta(days=31), key="rzy_k_d1e")
        with kc3:
            d2_bas = st.date_input("Donem 2 Bas", value=date.today() - timedelta(days=30), key="rzy_k_d2b")
        with kc4:
            d2_bit = st.date_input("Donem 2 Bit", value=date.today(), key="rzy_k_d2e")

        kars = RandevuAnalizcisi.karsilastir(
            store, d1_bas.isoformat(), d1_bit.isoformat(),
            d2_bas.isoformat(), d2_bit.isoformat(),
        )

        # Degisim bilgileri
        def _degisim_banner(baslik: str, deger: float):
            ok = "📈" if deger > 0 else "📉" if deger < 0 else "➡️"
            renk = "#ef4444" if deger > 0 else "#10b981" if deger < 0 else "#64748b"
            _btype = "error" if deger > 0 else "success" if deger < 0 else "info"
            styled_info_banner(
                f"{baslik}: <b style='color:{renk};'>%{deger:+.1f} {ok}</b>",
                _btype, "📊",
            )

        _degisim_banner("Randevu Degisimi", kars["randevu_degisim"])
        _degisim_banner("Tamamlanan Degisimi", kars["tamamlanan_degisim"])
        _degisim_banner("Ziyaret Degisimi", kars["ziyaret_degisim"])

        # Yan yana karsilastirma
        col1, col2 = st.columns(2)
        with col1:
            styled_section("Donem 1")
            o1 = kars["donem1_randevu"]
            styled_stat_row([
                ("Randevu", str(o1["toplam_randevu"]), "#4472C4", "📅"),
                ("Tamamlanan", str(o1["tamamlanan"]), "#10b981", "🎯"),
                ("Gelmedi", str(o1["gelmedi"]), "#64748b", "🚫"),
            ])
            if o1["tur_dagilimi"]:
                from utils.report_utils import ReportStyler
                tur_data = {k: float(v) for k, v in o1["tur_dagilimi"].items() if v > 0}
                if tur_data:
                    st.markdown(ReportStyler.sunburst_chart_svg(tur_data, size=175), unsafe_allow_html=True)

        with col2:
            styled_section("Donem 2")
            o2 = kars["donem2_randevu"]
            styled_stat_row([
                ("Randevu", str(o2["toplam_randevu"]), "#4472C4", "📅"),
                ("Tamamlanan", str(o2["tamamlanan"]), "#10b981", "🎯"),
                ("Gelmedi", str(o2["gelmedi"]), "#64748b", "🚫"),
            ])
            if o2["tur_dagilimi"]:
                from utils.report_utils import ReportStyler
                tur_data = {k: float(v) for k, v in o2["tur_dagilimi"].items() if v > 0}
                if tur_data:
                    st.markdown(ReportStyler.sunburst_chart_svg(tur_data, size=175), unsafe_allow_html=True)

    # ============================================================
    # PERFORMANS KARSILASTIRMA, AI ONERILERI, PDF, KUNYE
    # ============================================================
    try:
        from utils.report_utils import (
            ai_recommendations_html, period_comparison_row_html,
            generate_module_pdf, render_pdf_download_button,
            render_report_kunye_html, ReportStyler as _RS,
        )

        st.markdown(_RS.section_divider_html("Performans Karşılaştırma", "#0d9488"), unsafe_allow_html=True)

        now = datetime.now()
        current_month_start = now.replace(day=1).isoformat()[:10]
        current_month_end = now.isoformat()[:10]
        prev_month_end_dt = now.replace(day=1) - timedelta(days=1)
        prev_month_start = prev_month_end_dt.replace(day=1).isoformat()[:10]
        prev_month_end = prev_month_end_dt.isoformat()[:10]

        cur_ozet = RandevuAnalizcisi.donem_ozet(store, current_month_start, current_month_end)
        prev_ozet = RandevuAnalizcisi.donem_ozet(store, prev_month_start, prev_month_end)
        cur_ziy = RandevuAnalizcisi.ziyaret_ozet(store, current_month_start, current_month_end)
        prev_ziy = RandevuAnalizcisi.ziyaret_ozet(store, prev_month_start, prev_month_end)

        cur_iptal_rate = (cur_ozet["iptal"] / cur_ozet["toplam_randevu"] * 100) if cur_ozet["toplam_randevu"] > 0 else 0
        prev_iptal_rate = (prev_ozet["iptal"] / prev_ozet["toplam_randevu"] * 100) if prev_ozet["toplam_randevu"] > 0 else 0

        comparisons = [
            {"label": "Aylık Randevu", "current": cur_ozet["toplam_randevu"], "previous": prev_ozet["toplam_randevu"]},
            {"label": "Aylık Ziyaret", "current": cur_ziy["toplam_ziyaret"], "previous": prev_ziy["toplam_ziyaret"]},
            {"label": "Iptal Orani (%)", "current": cur_iptal_rate, "previous": prev_iptal_rate, "unit": "%"},
            {"label": "Ort. Sure (dk)", "current": cur_ziy["ortalama_sure_dk"], "previous": prev_ziy["ortalama_sure_dk"]},
        ]
        st.markdown(period_comparison_row_html(comparisons), unsafe_allow_html=True)

        # ---- AI Onerileri ----
        insights = []

        # 1) Yogun saat analizi
        saat_dag = cur_ziy.get("saat_dagilimi", {})
        if saat_dag:
            en_yogun_saat = max(saat_dag, key=saat_dag.get)
            insights.append({
                "icon": "🕐", "title": "Yogun Saat Analizi",
                "text": f"Bu ay en yogun ziyaretci saati <b>{en_yogun_saat}</b> ({saat_dag[en_yogun_saat]} ziyaret). "
                        f"Bu saatlerde ek personel veya bekleme alani duzenlenmesi oneriliyor.",
                "color": "#2563eb",
            })

        # 2) No-show / gelmedi uyarisi
        gelmedi_rate = (cur_ozet["gelmedi"] / cur_ozet["toplam_randevu"] * 100) if cur_ozet["toplam_randevu"] > 0 else 0
        if gelmedi_rate > 15:
            insights.append({
                "icon": "⚠️", "title": "Yuksek Gelmeme Orani",
                "text": f"Bu ay gelmeme orani <b>%{gelmedi_rate:.1f}</b>. "
                        f"Randevu hatirlatma SMS/email sistemi aktif edilmesi onerilir.",
                "color": "#ef4444",
            })
        elif gelmedi_rate > 0:
            insights.append({
                "icon": "✅", "title": "Gelmeme Orani Normal",
                "text": f"Gelmeme orani <b>%{gelmedi_rate:.1f}</b> seviyesinde, kabul edilebilir aralikta.",
                "color": "#10b981",
            })

        # 3) Iptal orani
        if cur_iptal_rate > 20:
            insights.append({
                "icon": "🚫", "title": "Yuksek Iptal Orani",
                "text": f"Iptal orani <b>%{cur_iptal_rate:.1f}</b>. Randevu surelerini veya "
                        f"slotlari gozden gecirmeniz onerilir.",
                "color": "#f59e0b",
            })

        # 4) Kapasite onerisi
        ayar = store.get_ayarlar()
        if cur_ozet["toplam_randevu"] > 0:
            gun_sayisi = max(1, (now - now.replace(day=1)).days + 1)
            gunluk_ort = cur_ozet["toplam_randevu"] / gun_sayisi
            if gunluk_ort > ayar.max_gunluk_randevu * 0.85:
                insights.append({
                    "icon": "📈", "title": "Kapasite Uyarisi",
                    "text": f"Günlük ortalama <b>{gunluk_ort:.1f}</b> randevu ile kapasitenin "
                            f"<b>%{gunluk_ort / ayar.max_gunluk_randevu * 100:.0f}</b>'ine ulasildi. "
                            f"Kapasite artirimi dusunulebilir.",
                    "color": "#8b5cf6",
                })

        # 5) Ziyaretci tipi onerisi
        tip_dag = cur_ziy.get("tip_dagilimi", {})
        if tip_dag:
            en_cok_tip = max(tip_dag, key=tip_dag.get)
            insights.append({
                "icon": "👥", "title": "Ziyaretci Profili",
                "text": f"En sik ziyaretci tipi: <b>{en_cok_tip}</b> ({tip_dag[en_cok_tip]} ziyaret). "
                        f"Bu gruba yonelik hizmet iyilestirmesi oneriliyor.",
                "color": "#0d9488",
            })

        if insights:
            st.markdown(ai_recommendations_html(insights), unsafe_allow_html=True)

        # ---- Kurumsal Kunye ----
        st.markdown(render_report_kunye_html(), unsafe_allow_html=True)

        # ---- PDF Export ----
        st.markdown(_RS.section_divider_html("PDF Rapor", "#1e40af"), unsafe_allow_html=True)
        if st.button("📥 Randevu & Ziyaretci Raporu (PDF)", key="rz_pdf_export_btn", use_container_width=True):
            try:
                sections = [
                    {
                        "title": "Bu Ay Genel Özet",
                        "metrics": [
                            ("Randevu", str(cur_ozet["toplam_randevu"]), "#2563eb"),
                            ("Tamamlanan", str(cur_ozet["tamamlanan"]), "#10b981"),
                            ("Iptal", str(cur_ozet["iptal"]), "#ef4444"),
                            ("Ziyaret", str(cur_ziy["toplam_ziyaret"]), "#8b5cf6"),
                        ],
                        "text": f"Iptal Orani: %{cur_iptal_rate:.1f} | Ort. Sure: {cur_ziy['ortalama_sure_dk']:.0f} dk",
                    },
                ]
                tur_dag = cur_ozet.get("tur_dagilimi", {})
                if tur_dag:
                    tur_items = {k: float(v) for k, v in tur_dag.items() if v > 0}
                    if tur_items:
                        sections.append({
                            "title": "Randevu Tur Dagilimi",
                            "donut_data": tur_items,
                            "donut_title": "Tur Dagilimi",
                        })
                if insights:
                    oneri_text = "\n".join([f"- {i['title']}: {i['text']}" for i in insights])
                    import re as _re
                    oneri_text = _re.sub(r"<[^>]+>", "", oneri_text)
                    sections.append({"title": "AI Onerileri", "text": oneri_text})

                pdf_bytes = generate_module_pdf("Randevu & Ziyaretci Raporu", sections)
                render_pdf_download_button(pdf_bytes, "rz_raporu.pdf", "Randevu & Ziyaretci Raporu", "rz_dl")
            except Exception as e:
                st.error(f"PDF olusturma hatasi: {e}")
    except Exception:
        pass  # report_utils yuklenemezse sessizce gec


# ============================================================
# SEKME 6: AYARLAR
# ============================================================

def _render_ayarlar(store: RZYDataStore):
    styled_header("Ayarlar", "Randevu ve ziyaretci sistemi yaplandirmasi")

    ayar = store.get_ayarlar()

    styled_section("Calisma Saatleri ve Randevu Ayarlari")

    c1, c2 = st.columns(2)
    with c1:
        calisma_bas = st.text_input("Calisma Başlangıç (HH:MM)", value=ayar.calisma_baslangic, key="rzy_ayar_bas")
        calisma_bit = st.text_input("Calisma Bitis (HH:MM)", value=ayar.calisma_bitis, key="rzy_ayar_bit")
    with c2:
        randevu_sure = st.number_input("Randevu Suresi (dk)", value=ayar.randevu_suresi_dk, min_value=10, max_value=120, step=5, key="rzy_ayar_sure")
        max_gunluk = st.number_input("Max Günlük Randevu", value=ayar.max_gunluk_randevu, min_value=1, max_value=100, step=1, key="rzy_ayar_max")

    bildirim = st.checkbox("Bildirim Aktif", value=ayar.bildirim_aktif, key="rzy_ayar_bild")

    if st.button("Ayarlari Kaydet", type="primary", key="rzy_btn_ayar"):
        ayar.calisma_baslangic = calisma_bas
        ayar.calisma_bitis = calisma_bit
        ayar.randevu_suresi_dk = randevu_sure
        ayar.max_gunluk_randevu = max_gunluk
        ayar.bildirim_aktif = bildirim
        ayar.updated_at = _now()
        store.upsert("rzy_ayarlar", ayar)
        st.success("Ayarlar kaydedildi!")
        st.rerun()

    # Istatistikler
    styled_section("Sistem İstatistikleri")
    ziy_count = len(store.load_list("ziyaretciler"))
    rnd_count = len(store.load_list("randevular"))
    zk_count = len(store.load_list("ziyaret_kayitlari"))

    styled_stat_row([
        ("Kayıtli Ziyaretci", str(ziy_count), "#8b5cf6", "👤"),
        ("Toplam Randevu", str(rnd_count), "#2563eb", "📅"),
        ("Toplam Ziyaret", str(zk_count), "#10b981", "🏢"),
    ])


# ============================================================
# SEKME 7: RANDEVULARIM (KISI BAZLI GORUNUM)
# ============================================================

def _get_current_user_info() -> dict:
    """Oturum acan kullanicinin bilgilerini dondurur."""
    return AuthManager.get_current_user()


def _kullanici_kurucu_mu(user: dict) -> bool:
    """Kullanicinin Kurucu (Genel Kurucu / en ust yetki) olup olmadigini kontrol eder."""
    role = user.get("role", "")
    name = user.get("name", "")
    # Yonetici rolu + "Kurucu" iceren isim veya ozel 'kurucu' rolu
    if role == "Yonetici" and ("kurucu" in name.lower() or "genel kurucu" in name.lower()):
        return True
    # username "kurucu" ise
    if user.get("username", "").lower() in ("kurucu", "kurucuadmin", "admin"):
        return True
    return False


def _not_gorunur_mu(not_obj: GorusmeNotu, user: dict) -> bool:
    """Bir gorusme notunun mevcut kullaniciya gorunur olup olmadigini kontrol eder.

    Kurallar:
        - gizli=True -> sadece Kurucu gorebilir
        - gorebilecekler bos -> herkes gorebilir
        - gorebilecekler dolu -> listede olan + Kurucu gorebilir
        - Notu yazan kisi her zaman kendi notunu gorebilir
    """
    username = user.get("username", "")
    kisi_adi = user.get("name", "")

    # Notu yazan her zaman gorebilir
    if not_obj.yazan_kullanici == username:
        return True

    # Kurucu her zaman gorebilir (gizli dahil)
    if _kullanici_kurucu_mu(user):
        return True

    # Gizli ise sadece kurucu gorebilir (yukarida kontrol edildi)
    if not_obj.gizli:
        return False

    # Gorebilecekler bos -> herkes gorebilir
    if not not_obj.gorebilecekler:
        return True

    # Gorebilecekler listesinde mi?
    if kisi_adi in not_obj.gorebilecekler:
        return True

    return False


def _render_randevularim(store: RZYDataStore):
    user = _get_current_user_info()
    kisi_adi = user.get("name", "")
    username = user.get("username", "")
    styled_header("Randevularım", f"{kisi_adi} - Kisiye tanimli randevular ve gorusme notlari")

    randevular = store.load_objects("randevular")

    # Kisi bazli filtreleme: gorusulecek_kisi veya olusturan alanina gore
    benim_rnd = [
        r for r in randevular
        if r.gorusulecek_kisi == kisi_adi or r.olusturan == username
    ]

    bugun = _today_str()
    bugun_rnd = [r for r in benim_rnd if r.tarih == bugun]
    gelecek_rnd = sorted(
        [r for r in benim_rnd if r.tarih > bugun],
        key=lambda r: (r.tarih, r.saat_baslangic),
    )
    gecmis_rnd = sorted(
        [r for r in benim_rnd if r.tarih < bugun],
        key=lambda r: (r.tarih, r.saat_baslangic),
        reverse=True,
    )

    styled_stat_row([
        ("Bugün", str(len(bugun_rnd)), "#2563eb", "📅"),
        ("Gelecek", str(len(gelecek_rnd)), "#10b981", "🔮"),
        ("Geçmiş", str(len(gecmis_rnd)), "#64748b", "📜"),
        ("Toplam", str(len(benim_rnd)), "#8b5cf6", "📊"),
    ])

    sub_tabs = st.tabs(["📋 Bugün", "📅 Gelecek", "📜 Geçmiş", "📝 Not Yaz"])

    # ── Bugun ──
    with sub_tabs[0]:
        if bugun_rnd:
            for r in sorted(bugun_rnd, key=lambda r: r.saat_baslangic):
                _render_rzy_randevu_karti(r)
                # Bu randevunun notlari
                _render_randevu_not_listesi(store, r, user)
        else:
            styled_info_banner("Bugün size tanimli randevu yok.", "info", "📅")

    # ── Gelecek ──
    with sub_tabs[1]:
        if gelecek_rnd:
            _prev = ""
            for r in gelecek_rnd:
                if r.tarih != _prev:
                    st.markdown(
                        f'<div style="font-size:11px;font-weight:600;color:#64748b;margin:8px 0 2px;'
                        f'padding:2px 8px;background:#0B0F19;border-radius:4px;display:inline-block;">'
                        f'📆 {r.tarih}</div>',
                        unsafe_allow_html=True,
                    )
                    _prev = r.tarih
                _render_rzy_randevu_karti(r)
        else:
            styled_info_banner("Gelecek randevunuz bulunmuyor.", "info", "🔮")

    # ── Gecmis ──
    with sub_tabs[2]:
        if gecmis_rnd:
            rows = []
            for r in gecmis_rnd:
                rows.append({
                    "Kod": r.randevu_kodu,
                    "Tarih": r.tarih,
                    "Saat": f"{r.saat_baslangic}-{r.saat_bitis}",
                    "Ziyaretci": r.ziyaretci_adi,
                    "Tur": r.randevu_turu,
                    "Durum": r.durum,
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            styled_info_banner("Geçmiş randevunuz bulunmuyor.", "info", "📜")

    # ── Not Yaz ──
    with sub_tabs[3]:
        _render_not_yaz_formu(store, benim_rnd, user)


def _render_randevu_not_listesi(store: RZYDataStore, randevu, user: dict):
    """Bir randevuya ait gorusme notlarini gosterir (yetki kontrollu)."""
    notlar = store.load_objects("gorusme_notlari")
    rnd_notlari = [n for n in notlar if n.randevu_id == randevu.id]
    rnd_notlari = [n for n in rnd_notlari if _not_gorunur_mu(n, user)]

    if not rnd_notlari:
        return

    rnd_notlari.sort(key=lambda n: n.created_at, reverse=True)
    st.markdown(
        '<div style="margin:4px 0 4px 20px;padding-left:12px;border-left:2px solid #e2e8f0;">',
        unsafe_allow_html=True,
    )
    for n in rnd_notlari:
        gizli_badge = ""
        if n.gizli:
            gizli_badge = ' <span style="background:#ef4444;color:#fff;padding:1px 6px;border-radius:6px;font-size:10px;">GIZLI</span>'
        gorebilecek_badge = ""
        if n.gorebilecekler:
            gorebilecek_badge = f' <span style="background:#f59e0b20;color:#f59e0b;padding:1px 6px;border-radius:6px;font-size:10px;">Kisitli</span>'
        st.markdown(
            f'<div style="background:#111827;border-radius:8px;padding:8px 12px;margin:4px 0;font-size:13px;">'
            f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">'
            f'<span style="font-weight:700;color:#94A3B8;font-size:12px;">✏️ {n.yazan_kisi_adi}</span>'
            f'<span style="color:#94a3b8;font-size:11px;">{n.created_at[:16]}</span>'
            f'{gizli_badge}{gorebilecek_badge}'
            f'</div>'
            f'<div style="color:#94A3B8;">{n.not_metni}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def _render_not_yaz_formu(store: RZYDataStore, randevular: list, user: dict):
    """Gorusme notu yazma formu."""
    styled_section("Görüşme Notu Yaz")

    if not randevular:
        styled_info_banner("Not yazabilmek için size tanimli randevu olmalidir.", "info", "📝")
        return

    # Randevu sec
    rnd_opts = {"-- Randevu secin --": None}
    for r in sorted(randevular, key=lambda x: x.tarih, reverse=True):
        label = f"{r.randevu_kodu} - {r.ziyaretci_adi} ({r.tarih} {r.saat_baslangic})"
        rnd_opts[label] = r
    secilen_label = st.selectbox("Randevu", list(rnd_opts.keys()), key="rzy_not_rnd_sec")
    secilen_rnd = rnd_opts.get(secilen_label)

    if not secilen_rnd:
        return

    not_metni = st.text_area("Görüşme Notu", key="rzy_not_metin", height=120,
                              placeholder="Görüşme notlarinizi buraya yazin...")

    c1, c2 = st.columns(2)
    with c1:
        gizli = st.checkbox("Gizle (Sadece Kurucu Gorebilir)", key="rzy_not_gizli")

    with c2:
        ik_isimler = get_ik_employee_name_with_position()
        gorebilecekler = st.multiselect(
            "Kimler Gorebilir? (Bos = Herkes)",
            ik_isimler,
            key="rzy_not_gorebilir",
            help="Bos birakirsaniz herkes gorebilir. Secim yaparsaniz sadece secilen kisiler ve Kurucu gorebilir.",
        )

    if st.button("Notu Kaydet", type="primary", key="rzy_btn_not_kaydet"):
        if not not_metni.strip():
            st.error("Not metni bos olamaz!")
            return

        yeni_not = GorusmeNotu(
            randevu_id=secilen_rnd.id,
            randevu_kodu=secilen_rnd.randevu_kodu,
            yazan_kullanici=user.get("username", ""),
            yazan_kisi_adi=user.get("name", ""),
            not_metni=not_metni.strip(),
            gizli=gizli,
            gorebilecekler=gorebilecekler,
        )
        store.upsert("gorusme_notlari", yeni_not)
        st.success("Görüşme notu kaydedildi!")
        st.rerun()


# ============================================================
# SEKME 8: GORUSME NOTLARI (FILTRELI GORUNUM)
# ============================================================

def _render_gorusme_notlari(store: RZYDataStore):
    user = _get_current_user_info()
    kurucu = _kullanici_kurucu_mu(user)
    styled_header("Görüşme Notları", "Randevu gorusme notlari - filtreleme ve goruntulem")

    tum_notlar = store.load_objects("gorusme_notlari")
    # Yetki filtresi
    gorunur_notlar = [n for n in tum_notlar if _not_gorunur_mu(n, user)]
    gorunur_notlar.sort(key=lambda n: n.created_at, reverse=True)

    # KPI
    toplam = len(gorunur_notlar)
    gizli_s = sum(1 for n in gorunur_notlar if n.gizli)
    kisitli_s = sum(1 for n in gorunur_notlar if n.gorebilecekler and not n.gizli)
    acik_s = toplam - gizli_s - kisitli_s

    styled_stat_row([
        ("Gorunur Not", str(toplam), "#2563eb", "📝"),
        ("Açık", str(acik_s), "#10b981", "🌐"),
        ("Kisitli", str(kisitli_s), "#f59e0b", "🔒"),
        ("Gizli", str(gizli_s), "#ef4444", "🚫"),
    ])

    # Filtre
    styled_section("Filtreler")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        # Randevu koduna gore filtre
        rnd_kodlari = sorted(set(n.randevu_kodu for n in gorunur_notlar if n.randevu_kodu))
        rnd_filtre = st.selectbox("Randevu Kodu", ["Tümü"] + rnd_kodlari, key="rzy_gn_rnd_filtre")
    with fc2:
        # Yazan kisiye gore filtre
        yazanlar = sorted(set(n.yazan_kisi_adi for n in gorunur_notlar if n.yazan_kisi_adi))
        yazan_filtre = st.selectbox("Yazan Kisi", ["Tümü"] + yazanlar, key="rzy_gn_yazan_filtre")
    with fc3:
        gizlilik_filtre = st.selectbox("Gizlilik", ["Tümü", "Açık", "Kisitli", "Gizli"], key="rzy_gn_gizli_filtre")

    # Filtre uygula
    filtreli = gorunur_notlar
    if rnd_filtre != "Tümü":
        filtreli = [n for n in filtreli if n.randevu_kodu == rnd_filtre]
    if yazan_filtre != "Tümü":
        filtreli = [n for n in filtreli if n.yazan_kisi_adi == yazan_filtre]
    if gizlilik_filtre == "Gizli":
        filtreli = [n for n in filtreli if n.gizli]
    elif gizlilik_filtre == "Kisitli":
        filtreli = [n for n in filtreli if n.gorebilecekler and not n.gizli]
    elif gizlilik_filtre == "Açık":
        filtreli = [n for n in filtreli if not n.gizli and not n.gorebilecekler]

    st.caption(f"Gösterilen: {len(filtreli)} / {toplam} not")

    if filtreli:
        for n in filtreli:
            # Randevu bilgisi
            rnd_obj = store.get_by_id("randevular", n.randevu_id) if n.randevu_id else None
            rnd_bilgi = ""
            if rnd_obj:
                rnd_bilgi = (
                    f'<span style="color:#64748b;font-size:11px;">'
                    f'{rnd_obj.tarih} {rnd_obj.saat_baslangic} - {rnd_obj.ziyaretci_adi} | '
                    f'{_gorusulen_bilgi(rnd_obj)}</span>'
                )

            # Badge'ler
            badges = ""
            if n.gizli:
                badges += ' <span style="background:#ef4444;color:#fff;padding:2px 8px;border-radius:8px;font-size:10px;font-weight:600;">GIZLI</span>'
            elif n.gorebilecekler:
                gorebilir_str = ", ".join(n.gorebilecekler[:3])
                if len(n.gorebilecekler) > 3:
                    gorebilir_str += f" +{len(n.gorebilecekler) - 3}"
                badges += (
                    f' <span style="background:#f59e0b20;color:#f59e0b;padding:2px 8px;'
                    f'border-radius:8px;font-size:10px;font-weight:600;">'
                    f'Gorebilir: {gorebilir_str}</span>'
                )
            else:
                badges += ' <span style="background:#10b98120;color:#10b981;padding:2px 8px;border-radius:8px;font-size:10px;font-weight:600;">Herkes</span>'

            st.markdown(
                f'<div style="background:#111827;border:1px solid #e2e8f0;border-radius:10px;'
                f'padding:12px 16px;margin:8px 0;">'
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
                f'<span style="font-weight:700;color:#2563eb;font-size:12px;">{n.randevu_kodu}</span>'
                f'<span style="font-weight:600;color:#94A3B8;font-size:13px;">✏️ {n.yazan_kisi_adi}</span>'
                f'<span style="color:#94a3b8;font-size:11px;margin-left:auto;">{n.created_at[:16]}</span>'
                f'{badges}'
                f'</div>'
                f'{rnd_bilgi}'
                f'<div style="color:#94A3B8;font-size:14px;margin-top:6px;padding:8px;'
                f'background:#fff;border-radius:6px;border:1px solid #0B0F19;">{n.not_metni}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Kurucu: Sil butonu
            if kurucu or n.yazan_kullanici == user.get("username", ""):
                if confirm_action("Notu Sil", "Bu görüşme notunu silmek istediğinize emin misiniz?", key=f"rzy_gn_sil_{n.id}"):
                    store.delete_by_id("gorusme_notlari", n.id)
                    st.success("Not silindi!")
                    st.rerun()
    else:
        styled_info_banner("Filtreye uyan gorusme notu bulunmuyor.", "info", "📝")


# ============================================================
# ANA GIRIS NOKTASI
# ============================================================

def render_randevu_ziyaretci():
    """RZY-01 modulu ana giris noktasi."""
    _inject_rzy_css()

    store = _get_rzy_store()

    tab_names = [
        "📊 Dashboard",
        "📅 Randevu Yönetimi",
        "🚶 Ziyaretçi Giriş/Çıkış",
        "📋 Ziyaretçi Rehberi",
        "🗺️ AR Kampüs Haritası",
        "📅 Randevularım",
        "📝 Görüşme Notları",
        "📈 Raporlar",
        "⚙️ Ayarlar",
        "🛡️ Güvenlik Merkezi",
        "🧠 AI Randevu",
        "🔍 Görüşme 360",
        "✨ Deneyim Motoru",
        "👤 Ziyaretçi CRM",
        "📊 Appointment BI",
        "🤖 Smarti",
    ]

    render_smarti_welcome("randevu_ziyaretci")

    from utils.shared_data import render_egitim_yili_secici
    selected_egitim_yili = render_egitim_yili_secici("randevu_ziyaretci_egitim_yili")

    tabs = st.tabs(tab_names)

    with tabs[0]:
        _render_dashboard(store)
    with tabs[1]:
        _render_randevu_yonetimi(store)
    with tabs[2]:
        _render_ziyaretci_giris_cikis(store)
    with tabs[3]:
        _render_ziyaretci_rehberi(store)
    # YENİ: AR Kampüs Haritası (tab index 4)
    with tabs[4]:
        try:
            from views._ar_kampus_haritasi import render_ar_kampus_haritasi
            render_ar_kampus_haritasi()
        except ImportError:
            st.info("AR Kampüs Haritası modülü yüklü değil.")
        except Exception as _e:
            st.error(f"AR Kampüs Haritası yüklenemedi: {_e}")

    with tabs[5]:
        _render_randevularim(store)
    with tabs[6]:
        _render_gorusme_notlari(store)
    with tabs[7]:
        _render_raporlar(store)
    with tabs[8]:
        _render_ayarlar(store)

    # MEGA: Guvenlik Merkezi
    with tabs[9]:
        try:
            from views._rzy_mega import render_guvenlik_merkezi
            render_guvenlik_merkezi(store)
        except Exception as _e:
            st.error(f"Guvenlik Merkezi yuklenemedi: {_e}")

    # MEGA: AI Randevu Optimizasyon
    with tabs[10]:
        try:
            from views._rzy_mega import render_ai_randevu
            render_ai_randevu(store)
        except Exception as _e:
            st.error(f"AI Randevu yuklenemedi: {_e}")

    # MEGA: 360 Gorusme Takip
    with tabs[11]:
        try:
            from views._rzy_mega import render_gorusme_360
            render_gorusme_360(store)
        except Exception as _e:
            st.error(f"Gorusme 360 yuklenemedi: {_e}")

    # ULTRA MEGA: Deneyim Motoru
    with tabs[12]:
        try:
            from views._rzy_ultra import render_deneyim_motoru
            render_deneyim_motoru(store)
        except Exception as _e:
            st.error(f"Deneyim Motoru yuklenemedi: {_e}")

    # ULTRA MEGA: Ziyaretci CRM
    with tabs[13]:
        try:
            from views._rzy_ultra import render_ziyaretci_crm
            render_ziyaretci_crm(store)
        except Exception as _e:
            st.error(f"Ziyaretci CRM yuklenemedi: {_e}")

    # ULTRA MEGA: Appointment BI
    with tabs[14]:
        try:
            from views._rzy_ultra import render_appointment_bi
            render_appointment_bi(store)
        except Exception as _e:
            st.error(f"Appointment BI yuklenemedi: {_e}")

    with tabs[15]:
        def _rzy_data_context():
            try:
                randevular = store.load_objects("randevular")
                ziyaretciler = store.load_objects("ziyaretciler")
                return (
                    f"Toplam randevu sayisi: {len(randevular)}\n"
                    f"Toplam ziyaretci sayisi: {len(ziyaretciler)}"
                )
            except Exception:
                return ""
        render_smarti_chat("randevu_ziyaretci", _rzy_data_context)
