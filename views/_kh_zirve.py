"""
Kurum Hizmetleri — Zirve Ozellikleri
======================================
1. AI Akilli Menu Planlama + Beslenme Analizi
2. Kurum Hizmetleri Komuta Merkezi
3. Servis Akilli Takip + Guvenlik Sistemi
"""
from __future__ import annotations

import json
import os
from collections import Counter
from datetime import date, datetime, timedelta

import streamlit as st

from utils.ui_common import styled_section, styled_stat_row, styled_info_banner


def _td() -> str:
    try:
        from utils.tenant import get_tenant_dir
        return get_tenant_dir()
    except Exception:
        return os.path.join("data", "tenants", "uz_koleji")


def _lj(path: str) -> list:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, list) else []
    except Exception:
        return []


def _ak_dir() -> str:
    try:
        from utils.tenant import get_data_path
        return get_data_path("akademik")
    except Exception:
        return "data/akademik"


_GUN_ADLARI = {0: "Pazartesi", 1: "Sali", 2: "Carsamba", 3: "Persembe", 4: "Cuma"}


# ============================================================
# 1. AI AKILLI MENÜ PLANLAMA + BESLENME ANALİZİ
# ============================================================

_YEMEK_KATEGORILERI = {
    "protein": {"label": "Protein", "ikon": "🥩", "renk": "#ef4444", "hedef_pct": 25},
    "karbonhidrat": {"label": "Karbonhidrat", "ikon": "🍚", "renk": "#f59e0b", "hedef_pct": 40},
    "sebze": {"label": "Sebze/Salata", "ikon": "🥗", "renk": "#10b981", "hedef_pct": 25},
    "tatli": {"label": "Tatli/Meyve", "ikon": "🍎", "renk": "#7c3aed", "hedef_pct": 10},
}


def render_ai_menu_planlama():
    """AI ile otomatik menu planlama + beslenme analizi."""
    styled_section("AI Akilli Menu Planlama", "#f59e0b")
    styled_info_banner(
        "Aylik menu planini AI ile olusturun. Beslenme dengesi, "
        "tekrar kontrolu, maliyet tahmini — hepsi otomatik.",
        banner_type="info", icon="🤖")

    td = _td()
    ak = _ak_dir()

    # Mevcut menuler
    menuler = _lj(os.path.join(td, "kurum_hizmetleri", "yemek_menu.json"))
    if not menuler:
        menuler = _lj(os.path.join(ak, "yemek_menusu.json"))

    # Ogrenci sayisi
    ogrenciler = _lj(os.path.join(ak, "students.json"))
    aktif_ogr = sum(1 for s in ogrenciler if s.get("durum", "aktif") == "aktif")

    styled_stat_row([
        ("Kayitli Menu", str(len(menuler)), "#f59e0b", "🍽️"),
        ("Aktif Ogrenci", str(aktif_ogr), "#2563eb", "🎓"),
    ])

    sub = st.tabs(["🤖 AI Menu Uret", "📊 Beslenme Analizi", "📋 Mevcut Menuler"])

    # ═══ AI MENÜ ÜRET ═══
    with sub[0]:
        styled_section("AI ile Aylik Menu Olustur")
        col1, col2 = st.columns(2)
        with col1:
            ay = st.selectbox("Ay", list(range(1, 13)),
                                format_func=lambda x: ["Ocak", "Subat", "Mart", "Nisan", "Mayis", "Haziran",
                                                         "Temmuz", "Agustos", "Eylul", "Ekim", "Kasim", "Aralik"][x-1],
                                index=date.today().month - 1, key="aim_ay")
            porsiyon_fiyat = st.number_input("Porsiyon Maliyeti (TL)", 5, 100, 25, key="aim_fiyat")
        with col2:
            gun_sayisi = st.number_input("Is Gunu Sayisi", 15, 25, 20, key="aim_gun")
            ozel_diyet = st.multiselect("Dikkat Edilecek", ["Glutensiz", "Laktozsuz", "Vejetaryen", "Dusuk Seker"], key="aim_diyet")

        if st.button("AI ile Menu Olustur", key="aim_btn", type="primary", use_container_width=True):
            try:
                from utils.smarti_helper import _get_client
                client = _get_client()
                if client:
                    diyet_txt = ", ".join(ozel_diyet) if ozel_diyet else "Standart"
                    with st.spinner("AI menu planliyor..."):
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "Sen bir okul beslenme uzmanisin. Verilen parametrelerle aylik yemek menusu olustur. Her gun: Kahvalti + Ogle + Ikindi. Ayni yemek haftada 2 kez olmasin. Protein/karbonhidrat/sebze dengeli. Turkce."},
                                {"role": "user", "content": f"Ay: {ay}, Gun: {gun_sayisi}, Diyet: {diyet_txt}, Ogrenci: {aktif_ogr}. {gun_sayisi} gunluk menu olustur."},
                            ],
                            max_tokens=1500, temperature=0.8,
                        )
                        ai = resp.choices[0].message.content or ""
                    if ai:
                        # Maliyet
                        toplam_maliyet = gun_sayisi * aktif_ogr * porsiyon_fiyat
                        st.markdown(f"""
                        <div style="background:#0f172a;border:2px solid #f59e0b;border-radius:14px;
                                    padding:14px 18px;margin-bottom:12px;text-align:center;">
                            <span style="font-size:12px;color:#fde68a;">Tahmini Aylik Maliyet:</span>
                            <span style="font-size:20px;font-weight:900;color:#fbbf24;margin-left:8px;">
                                {toplam_maliyet:,.0f} TL</span>
                            <span style="font-size:10px;color:#94a3b8;margin-left:8px;">
                                ({gun_sayisi} gun x {aktif_ogr} ogrenci x {porsiyon_fiyat} TL)</span>
                        </div>""", unsafe_allow_html=True)

                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#78350f,#92400e);border:1px solid #f59e0b;
                                    border-radius:14px;padding:16px 20px;">
                            <div style="font-size:12px;color:#fde68a;font-weight:700;margin-bottom:8px;">AI Aylik Menu Plani</div>
                            <div style="font-size:12px;color:#fef3c7;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.warning("OpenAI API bulunamadi.")
            except Exception as e:
                st.error(f"Hata: {e}")

    # ═══ BESLENME ANALİZİ ═══
    with sub[1]:
        styled_section("Beslenme Denge Analizi")
        if not menuler:
            styled_info_banner("Analiz icin menu verisi gerekli.", banner_type="warning", icon="📊")
        else:
            # Basit kelime bazli kategori analizi
            protein_kw = ["et", "tavuk", "balik", "kofte", "sosis", "yumurta", "peynir", "yogurt", "mercimek"]
            karb_kw = ["pilav", "makarna", "ekmek", "borek", "pogaca", "bulgur", "patates", "eriste"]
            sebze_kw = ["salata", "cacik", "sebze", "domates", "biber", "havuc", "brokoli", "ispanak"]
            tatli_kw = ["meyve", "komposto", "tatli", "puding", "sutlac", "kek", "biskuvi"]

            kat_sayac = {"protein": 0, "karbonhidrat": 0, "sebze": 0, "tatli": 0}
            for m in menuler:
                metin = " ".join([
                    m.get("kahvalti", ""), m.get("ogle", m.get("ana_yemek", "")),
                    m.get("ikindi", ""), m.get("menu", "")
                ]).lower()
                for kw in protein_kw:
                    if kw in metin:
                        kat_sayac["protein"] += 1
                for kw in karb_kw:
                    if kw in metin:
                        kat_sayac["karbonhidrat"] += 1
                for kw in sebze_kw:
                    if kw in metin:
                        kat_sayac["sebze"] += 1
                for kw in tatli_kw:
                    if kw in metin:
                        kat_sayac["tatli"] += 1

            toplam = max(sum(kat_sayac.values()), 1)
            for kat_key, kat_info in _YEMEK_KATEGORILERI.items():
                sayi = kat_sayac.get(kat_key, 0)
                pct = round(sayi / toplam * 100)
                hedef = kat_info["hedef_pct"]
                fark = pct - hedef
                fark_renk = "#10b981" if abs(fark) <= 5 else "#f59e0b" if abs(fark) <= 15 else "#ef4444"
                bar_w = min(pct, 100)

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                    <span style="font-size:18px;min-width:28px;">{kat_info['ikon']}</span>
                    <span style="min-width:100px;font-size:12px;color:#e2e8f0;font-weight:700;">{kat_info['label']}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:20px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{kat_info['renk']};border-radius:4px;
                                    display:flex;align-items:center;padding-left:8px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">%{pct}</span></div></div>
                    <span style="min-width:80px;font-size:10px;color:{fark_renk};font-weight:600;">
                        Hedef: %{hedef} ({'+' if fark > 0 else ''}{fark})</span>
                </div>""", unsafe_allow_html=True)

    # ═══ MEVCUT MENÜLER ═══
    with sub[2]:
        styled_section("Kayitli Menuler")
        if not menuler:
            st.info("Henuz menu girisi yok.")
        else:
            for m in sorted(menuler, key=lambda x: x.get("tarih", ""), reverse=True)[:20]:
                tarih = m.get("tarih", "?")[:10]
                kahvalti = m.get("kahvalti", "-")[:60]
                ogle = m.get("ogle", m.get("ana_yemek", m.get("menu", "-")))[:60]
                ikindi = m.get("ikindi", "-")[:40]
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;
                            padding:8px 12px;margin-bottom:4px;font-size:11px;">
                    <span style="color:#f59e0b;font-weight:700;min-width:70px;">{tarih}</span>
                    <span style="color:#94a3b8;margin-left:8px;">K: {kahvalti} · O: {ogle} · I: {ikindi}</span>
                </div>""", unsafe_allow_html=True)


# ============================================================
# 2. KURUM HİZMETLERİ KOMUTA MERKEZİ
# ============================================================

def render_hizmet_komuta():
    """Tum kurum hizmetlerinin canli durumu tek ekranda."""
    styled_section("Kurum Hizmetleri Komuta Merkezi", "#0891b2")
    styled_info_banner(
        "Servis, yemek, nobet, duyuru, veli talebi, mesaj — "
        "tum hizmetlerin anlık durumu tek bakista.",
        banner_type="info", icon="🎛️")

    td = _td()
    ak = _ak_dir()
    bugun = date.today().isoformat()
    simdi = datetime.now()

    # Veri toplama
    # 1. Nobet
    nobet = _lj(os.path.join(ak, "nobet_kayitlar.json"))
    bugun_nobet = [n for n in nobet if n.get("tarih", "") == bugun]

    # 2. Yemek
    menuler = _lj(os.path.join(td, "kurum_hizmetleri", "yemek_menu.json"))
    if not menuler:
        menuler = _lj(os.path.join(ak, "yemek_menusu.json"))
    bugun_menu = next((m for m in menuler if m.get("tarih", "") == bugun), None)

    # 3. Duyuru
    duyurular = _lj(os.path.join(ak, "duyurular.json"))
    if not duyurular:
        duyurular = _lj(os.path.join(td, "akademik", "duyurular.json"))
    son_24s = (date.today() - timedelta(days=1)).isoformat()
    yeni_duyuru = sum(1 for d in duyurular if (d.get("tarih", d.get("created_at", "")) or "")[:10] >= son_24s)

    # 4. Veli talep
    randevular = _lj(os.path.join(ak, "veli_randevular.json"))
    belge_talep = _lj(os.path.join(ak, "veli_belge_talepleri.json"))
    bekleyen_randevu = sum(1 for r in randevular if r.get("durum") in ("Beklemede", "beklemede"))
    bekleyen_belge = sum(1 for b in belge_talep if b.get("durum") in ("Beklemede", "beklemede"))

    # 5. Mesaj
    mesajlar = _lj(os.path.join(ak, "veli_mesajlar.json"))
    cevapsiz = sum(1 for m in mesajlar if not m.get("cevaplandi") and m.get("yon", m.get("direction", "")) == "gelen")

    # 6. Servis
    try:
        from models.servis_yonetimi import ServisDataStore
        servis_store = ServisDataStore(os.path.join(td, "servis"))
        hatlar = servis_store.load_list("hatlar") if hasattr(servis_store, "load_list") else []
        olaylar = servis_store.load_list("olaylar") if hasattr(servis_store, "load_list") else []
        bugun_olay = sum(1 for o in olaylar if (o.get("tarih", "") or "")[:10] == bugun)
    except Exception:
        hatlar = []
        bugun_olay = 0

    # 7. Zaman cizelgesi — su anki ders
    from views._yte_zirve_features import _aktif_ders_saati
    aktif_ders = _aktif_ders_saati()

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0c4a6e 0%,#155e75 100%);
                border:2px solid #0891b2;border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px rgba(8,145,178,0.25);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <div>
                <div style="font-size:10px;color:#67e8f9;letter-spacing:3px;text-transform:uppercase;">Kurum Hizmetleri</div>
                <div style="font-size:24px;font-weight:900;color:#fff;font-family:Playfair Display,Georgia,serif;">
                    Komuta Merkezi</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:24px;font-weight:900;color:#67e8f9;font-family:monospace;">{simdi.strftime('%H:%M')}</div>
                <div style="font-size:10px;color:#a5f3fc;">
                    {aktif_ders}. Ders{'  Devam Ediyor' if aktif_ders > 0 else ' yok'}</div>
            </div>
        </div>

        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#f59e0b;">{len(bugun_nobet)}</div>
                <div style="font-size:9px;color:#67e8f9;">Bugun Nobet</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:{'#10b981' if bugun_menu else '#ef4444'};">
                    {'Var' if bugun_menu else 'Yok'}</div>
                <div style="font-size:9px;color:#67e8f9;">Bugun Menu</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:#2563eb;">{yeni_duyuru}</div>
                <div style="font-size:9px;color:#67e8f9;">Yeni Duyuru</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:{'#ef4444' if bugun_olay > 0 else '#10b981'};">{bugun_olay}</div>
                <div style="font-size:9px;color:#67e8f9;">Servis Olay</div></div>
        </div>

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:10px;">
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:{'#f59e0b' if bekleyen_randevu > 0 else '#10b981'};">{bekleyen_randevu}</div>
                <div style="font-size:9px;color:#67e8f9;">Bekleyen Randevu</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:{'#f59e0b' if bekleyen_belge > 0 else '#10b981'};">{bekleyen_belge}</div>
                <div style="font-size:9px;color:#67e8f9;">Bekleyen Belge</div></div>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:12px;text-align:center;">
                <div style="font-size:22px;font-weight:900;color:{'#ef4444' if cevapsiz > 3 else '#f59e0b' if cevapsiz > 0 else '#10b981'};">{cevapsiz}</div>
                <div style="font-size:9px;color:#67e8f9;">Cevapsiz Mesaj</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Bugunun menusu
    if bugun_menu:
        kahvalti = bugun_menu.get("kahvalti", "-")
        ogle = bugun_menu.get("ogle", bugun_menu.get("ana_yemek", bugun_menu.get("menu", "-")))
        ikindi = bugun_menu.get("ikindi", "-")
        st.markdown(f"""
        <div style="background:#0f172a;border:1px solid #f59e0b30;border-left:4px solid #f59e0b;
                    border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:8px;">
            <div style="font-size:12px;font-weight:700;color:#fbbf24;margin-bottom:4px;">Bugunun Menusu</div>
            <div style="font-size:10px;color:#94a3b8;">
                Kahvalti: {kahvalti[:50]} · Ogle: {ogle[:50]} · Ikindi: {ikindi[:30]}</div>
        </div>""", unsafe_allow_html=True)


# ============================================================
# 3. SERVİS AKILLI TAKİP + GÜVENLİK
# ============================================================

def render_servis_guvenlik():
    """Servis guvenlik skoru + analitik + tahmin."""
    styled_section("Servis Guvenlik & Analitik", "#dc2626")
    styled_info_banner(
        "Her servis hatti icin guvenlik skoru. "
        "Olay gecmisi, sofor performansi, kapasite analizi, bakim takvimi.",
        banner_type="warning", icon="🛡️")

    td = _td()

    # Servis verisi
    try:
        from models.servis_yonetimi import ServisDataStore
        servis_store = ServisDataStore(os.path.join(td, "servis"))
        hatlar = servis_store.load_list("hatlar") if hasattr(servis_store, "load_list") else []
        soforler = servis_store.load_list("soforler") if hasattr(servis_store, "load_list") else []
        araclar = servis_store.load_list("araclar") if hasattr(servis_store, "load_list") else []
        olaylar = servis_store.load_list("olaylar") if hasattr(servis_store, "load_list") else []
        binis = servis_store.load_list("binis_kayitlari") if hasattr(servis_store, "load_list") else []
        bakimlar = servis_store.load_list("bakim_kayitlari") if hasattr(servis_store, "load_list") else []
    except Exception:
        hatlar, soforler, araclar, olaylar, binis, bakimlar = [], [], [], [], [], []

    styled_stat_row([
        ("Hat Sayisi", str(len(hatlar)), "#dc2626", "🚌"),
        ("Sofor", str(len(soforler)), "#2563eb", "👤"),
        ("Arac", str(len(araclar)), "#059669", "🚗"),
        ("Olay (toplam)", str(len(olaylar)), "#ef4444", "⚠️"),
        ("Binis Kaydi", str(len(binis)), "#7c3aed", "📋"),
    ])

    if not hatlar and not soforler:
        styled_info_banner(
            "Servis verisi bulunamadi. Servis Yonetimi sekmesinden hat/arac/sofor ekleyin.",
            banner_type="warning", icon="🚌")
        return

    sub = st.tabs(["🛡️ Guvenlik Skoru", "📊 Kapasite Analizi", "🔧 Bakim Takibi"])

    # ═══ GÜVENLİK SKORU ═══
    with sub[0]:
        styled_section("Hat Bazli Guvenlik Skoru")
        for h in hatlar:
            hid = h.get("id", "")
            h_ad = h.get("hat_adi", h.get("ad", f"Hat {hid}"))

            # Olay sayisi
            h_olay = sum(1 for o in olaylar if o.get("hat_id") == hid)
            # Bakim durumu
            h_bakim = [b for b in bakimlar if b.get("arac_id") in [a.get("id") for a in araclar if a.get("hat_id") == hid]]
            geciken_bakim = sum(1 for b in h_bakim if b.get("sonraki_bakim", "") and b["sonraki_bakim"] < date.today().isoformat())

            # Guvenlik skoru
            skor = 100
            skor -= min(h_olay * 10, 40)
            skor -= min(geciken_bakim * 15, 30)
            skor = max(0, skor)

            s_renk = "#10b981" if skor >= 80 else "#f59e0b" if skor >= 60 else "#ef4444"
            bar_w = min(skor, 100)

            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {s_renk}30;border-left:5px solid {s_renk};
                        border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <span style="font-weight:800;color:#e2e8f0;font-size:14px;">🚌 {h_ad}</span>
                    <span style="font-size:22px;font-weight:900;color:{s_renk};">{skor}</span>
                </div>
                <div style="background:#1e293b;border-radius:4px;height:8px;overflow:hidden;margin-bottom:6px;">
                    <div style="width:{bar_w}%;height:100%;background:{s_renk};border-radius:4px;"></div>
                </div>
                <div style="display:flex;gap:12px;font-size:10px;color:#94a3b8;">
                    <span>Olay: <b style="color:{'#ef4444' if h_olay > 0 else '#10b981'};">{h_olay}</b></span>
                    <span>Geciken Bakim: <b style="color:{'#ef4444' if geciken_bakim > 0 else '#10b981'};">{geciken_bakim}</b></span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ KAPASİTE ANALİZİ ═══
    with sub[1]:
        styled_section("Hat Kapasite Analizi")
        for h in hatlar:
            kapasite = h.get("kapasite", h.get("max_ogrenci", 30))
            kayitli = h.get("kayitli_ogrenci", h.get("ogrenci_sayisi", 0))
            doluluk = round(kayitli / max(kapasite, 1) * 100)
            renk = "#ef4444" if doluluk >= 95 else "#f59e0b" if doluluk >= 80 else "#10b981"

            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                <span style="min-width:120px;font-size:12px;color:#e2e8f0;font-weight:600;">
                    🚌 {h.get('hat_adi', h.get('ad', '?'))}</span>
                <div style="flex:1;background:#1e293b;border-radius:4px;height:18px;overflow:hidden;">
                    <div style="width:{min(doluluk, 100)}%;height:100%;background:{renk};border-radius:4px;
                                display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:9px;color:#fff;font-weight:700;">{kayitli}/{kapasite}</span></div></div>
                <span style="min-width:40px;font-size:10px;color:{renk};font-weight:700;">%{doluluk}</span>
            </div>""", unsafe_allow_html=True)

    # ═══ BAKIM TAKİBİ ═══
    with sub[2]:
        styled_section("Arac Bakim Durumu")
        if not araclar:
            st.info("Arac kaydi yok.")
        else:
            for a in araclar:
                plaka = a.get("plaka", a.get("ad", "?"))
                son_bakim = a.get("son_bakim_tarihi", "")
                sonraki = a.get("sonraki_bakim", "")

                if sonraki and sonraki < date.today().isoformat():
                    durum = "GECIKTI"
                    d_renk = "#ef4444"
                elif sonraki and sonraki <= (date.today() + timedelta(days=30)).isoformat():
                    durum = "YAKLASAN"
                    d_renk = "#f59e0b"
                else:
                    durum = "NORMAL"
                    d_renk = "#10b981"

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
                    <span style="min-width:100px;font-size:12px;color:#e2e8f0;font-weight:600;">🚗 {plaka}</span>
                    <span style="font-size:10px;color:#94a3b8;">Son: {son_bakim or '-'}</span>
                    <span style="font-size:10px;color:#94a3b8;">Sonraki: {sonraki or '-'}</span>
                    <span style="background:{d_renk}20;color:{d_renk};padding:2px 8px;border-radius:6px;
                                font-size:9px;font-weight:700;">{durum}</span>
                </div>""", unsafe_allow_html=True)
