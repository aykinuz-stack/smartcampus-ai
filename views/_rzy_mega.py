"""
Randevu & Ziyaretci — MEGA Ozellikleri
========================================
1. Ziyaretci Akilli Guvenlik Merkezi
2. Randevu AI Optimizasyon Motoru
3. 360 Gorusme Takip Sistemi
"""
from __future__ import annotations

import json
import os
import uuid
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


def _sj(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# 1. ZİYARETÇİ AKILLI GÜVENLİK MERKEZİ
# ============================================================

def _kara_liste_path() -> str:
    return os.path.join(_td(), "randevu", "kara_liste.json")


def render_guvenlik_merkezi(store):
    """Ziyaretci guvenlik merkezi — kara liste + canli izleme + rozet."""
    styled_section("Ziyaretci Guvenlik Merkezi", "#dc2626")
    styled_info_banner(
        "Okul binasinin fiziksel guvenligini dijitallestirin. "
        "Kara liste + canli ziyaretci takibi + dijital rozet + alarm.",
        banner_type="warning", icon="🛡️")

    bugun = date.today().isoformat()
    simdi = datetime.now()

    ziyaret_kayitlari = store.load_list("ziyaret_kayitlari") if hasattr(store, "load_list") else []
    randevular = store.load_list("randevular") if hasattr(store, "load_list") else []
    kara_liste = _lj(_kara_liste_path())

    # Bugun girisler
    bugun_giris = [z for z in ziyaret_kayitlari if (z.get("giris_zamani", "") or "")[:10] == bugun]
    aktif_ziyaretci = [z for z in bugun_giris if not z.get("cikis_zamani")]
    cikis_yapan = [z for z in bugun_giris if z.get("cikis_zamani")]

    # Uzun sure binada (2+ saat)
    uzun_sure = []
    for z in aktif_ziyaretci:
        try:
            giris = datetime.fromisoformat(z["giris_zamani"][:19])
            dakika = (simdi - giris).total_seconds() / 60
            if dakika > 120:
                uzun_sure.append({**z, "dakika": round(dakika)})
        except Exception:
            pass

    styled_stat_row([
        ("Bugun Giris", str(len(bugun_giris)), "#2563eb", "🚶"),
        ("Su An Binada", str(len(aktif_ziyaretci)), "#f59e0b", "🏢"),
        ("Cikis Yapan", str(len(cikis_yapan)), "#10b981", "✅"),
        ("Uzun Sure (2s+)", str(len(uzun_sure)), "#ef4444", "⏰"),
        ("Kara Liste", str(len(kara_liste)), "#dc2626", "🚫"),
    ])

    # ── CANLI DURUM HERO ──
    binada_renk = "#10b981" if len(aktif_ziyaretci) < 5 else "#f59e0b" if len(aktif_ziyaretci) < 15 else "#ef4444"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#450a0a 0%,#7f1d1d 100%);
                border:2px solid {binada_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {binada_renk}30;text-align:center;">
        <div style="font-size:10px;color:#fca5a5;letter-spacing:3px;text-transform:uppercase;">Canli Bina Durumu</div>
        <div style="font-size:56px;font-weight:900;color:{binada_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{len(aktif_ziyaretci)}</div>
        <div style="font-size:12px;color:#fca5a5;">Ziyaretci Su An Binada · {simdi.strftime('%H:%M')}</div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["🏢 Aktif Ziyaretciler", "🚫 Kara Liste", "🪪 Rozet Uretici", "📊 Trafik"])

    # ═══ AKTİF ZİYARETÇİLER ═══
    with sub[0]:
        styled_section("Su An Binada Olanlar")
        if not aktif_ziyaretci:
            st.success("Binada aktif ziyaretci yok.")
        else:
            for z in aktif_ziyaretci:
                try:
                    giris = datetime.fromisoformat(z["giris_zamani"][:19])
                    dk = round((simdi - giris).total_seconds() / 60)
                except Exception:
                    dk = 0
                dk_renk = "#ef4444" if dk > 120 else "#f59e0b" if dk > 60 else "#10b981"
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {dk_renk}30;border-left:4px solid {dk_renk};
                            border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-weight:700;color:#e2e8f0;font-size:13px;">{z.get('ziyaretci_adi', '?')}</span>
                            <span style="color:#94a3b8;font-size:11px;margin-left:8px;">
                                → {z.get('gorusulecek_kisi', z.get('gorusulecek_unvan', '-'))}</span>
                        </div>
                        <div style="display:flex;gap:8px;align-items:center;">
                            <span style="background:{dk_renk}20;color:{dk_renk};padding:2px 10px;
                                        border-radius:6px;font-size:10px;font-weight:700;">{dk} dk</span>
                            <span style="font-size:10px;color:#64748b;">Giris: {z.get('giris_zamani', '')[-8:-3]}</span>
                        </div>
                    </div>
                    <div style="font-size:10px;color:#64748b;margin-top:3px;">
                        Neden: {z.get('ziyaret_nedeni', '-')} · Kart: {z.get('kart_no', '-')} · Plaka: {z.get('arac_plaka', '-')}</div>
                </div>""", unsafe_allow_html=True)

        # Uzun sure uyari
        if uzun_sure:
            styled_section("Uzun Sure Uyarisi (2+ saat)", "#ef4444")
            for z in uzun_sure:
                st.error(f"⏰ **{z.get('ziyaretci_adi', '?')}** — {z['dakika']} dakikadir binada! Cikis yapilmamis.")

    # ═══ KARA LİSTE ═══
    with sub[1]:
        styled_section("Kara Liste Yonetimi")
        if kara_liste:
            for kl in kara_liste:
                st.markdown(f"""
                <div style="background:#450a0a;border:1px solid #ef4444;border-radius:10px;
                            padding:10px 14px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:700;color:#fca5a5;">{kl.get('ad', '')} {kl.get('soyad', '')}</span>
                        <span style="font-size:10px;color:#94a3b8;">{kl.get('tarih', '')}</span>
                    </div>
                    <div style="font-size:11px;color:#fca5a5;margin-top:3px;">
                        Neden: {kl.get('neden', '-')} · Ekleyen: {kl.get('ekleyen', '-')}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Kara listede kimse yok.")

        # Yeni kara liste ekle
        styled_section("Kara Listeye Ekle")
        with st.form("kara_liste_form"):
            kl_c1, kl_c2 = st.columns(2)
            with kl_c1:
                kl_ad = st.text_input("Ad", key="kl_ad")
                kl_neden = st.text_input("Neden", key="kl_neden")
            with kl_c2:
                kl_soyad = st.text_input("Soyad", key="kl_soyad")
                kl_tc = st.text_input("TC (istege bagli)", key="kl_tc")
            if st.form_submit_button("Kara Listeye Ekle", type="primary"):
                if kl_ad:
                    kara_liste.append({
                        "id": f"kl_{uuid.uuid4().hex[:8]}",
                        "ad": kl_ad, "soyad": kl_soyad, "tc": kl_tc,
                        "neden": kl_neden, "ekleyen": "Yonetim",
                        "tarih": date.today().isoformat(),
                    })
                    _sj(_kara_liste_path(), kara_liste)
                    st.success(f"Kara listeye eklendi: {kl_ad} {kl_soyad}")
                    st.rerun()

    # ═══ ROZET ÜRETİCİ ═══
    with sub[2]:
        styled_section("Dijital Ziyaretci Rozeti")
        styled_info_banner("Ziyaretci icin aninda dijital kimlik rozeti olusturun.", banner_type="info", icon="🪪")

        rz_c1, rz_c2 = st.columns(2)
        with rz_c1:
            rz_ad = st.text_input("Ziyaretci Adi", key="rz_ad")
            rz_kisi = st.text_input("Gorusulecek Kisi", key="rz_kisi")
        with rz_c2:
            rz_kurum = st.text_input("Kurum", key="rz_kurum")
            rz_neden = st.text_input("Ziyaret Nedeni", key="rz_neden")

        if rz_ad:
            rz_saat = simdi.strftime("%H:%M")
            rz_kod = uuid.uuid4().hex[:8].upper()
            st.markdown(f"""
            <div style="max-width:380px;margin:12px auto;background:linear-gradient(135deg,#0B0F19,#1a237e);
                        border:3px solid #c9a84c;border-radius:16px;overflow:hidden;">
                <div style="background:linear-gradient(90deg,#c9a84c,#e8d48b,#c9a84c);padding:6px;text-align:center;">
                    <span style="font-size:10px;font-weight:800;color:#1a1a2e;letter-spacing:2px;">ZIYARETCI KARTI</span>
                </div>
                <div style="padding:16px 20px;text-align:center;">
                    <div style="font-size:20px;font-weight:900;color:#fff;">{rz_ad}</div>
                    <div style="font-size:11px;color:#c9a84c;margin:4px 0;">{rz_kurum or '-'}</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;text-align:left;">
                        <div><div style="font-size:8px;color:#64748b;">Gorusulecek</div>
                            <div style="font-size:12px;color:#e2e8f0;font-weight:600;">{rz_kisi or '-'}</div></div>
                        <div><div style="font-size:8px;color:#64748b;">Neden</div>
                            <div style="font-size:12px;color:#e2e8f0;font-weight:600;">{rz_neden or '-'}</div></div>
                        <div><div style="font-size:8px;color:#64748b;">Giris Saati</div>
                            <div style="font-size:12px;color:#e2e8f0;font-weight:600;">{rz_saat}</div></div>
                        <div><div style="font-size:8px;color:#64748b;">Rozet Kodu</div>
                            <div style="font-size:12px;color:#c9a84c;font-weight:800;font-family:monospace;">{rz_kod}</div></div>
                    </div>
                    <div style="font-size:9px;color:#64748b;">{date.today().strftime('%d.%m.%Y')} · SmartCampus AI</div>
                </div>
                <div style="background:linear-gradient(90deg,#c9a84c,#e8d48b,#c9a84c);padding:4px;text-align:center;">
                    <span style="font-size:8px;color:#1a1a2e;font-weight:600;">Cikista bu karti gosteriniz</span>
                </div>
            </div>""", unsafe_allow_html=True)

    # ═══ TRAFİK ANALİZİ ═══
    with sub[3]:
        styled_section("Ziyaretci Trafik Analizi")
        # Son 7 gun trafik
        for i in range(6, -1, -1):
            gun = (date.today() - timedelta(days=i)).isoformat()
            gun_kisa = gun[5:]
            gun_giris = sum(1 for z in ziyaret_kayitlari if (z.get("giris_zamani", "") or "")[:10] == gun)
            is_bugun = i == 0
            bar_w = min(gun_giris * 10, 100)
            renk = "#c9a84c" if is_bugun else "#2563eb"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="min-width:50px;font-size:10px;color:{'#c9a84c' if is_bugun else '#94a3b8'};
                            font-weight:{'800' if is_bugun else '400'};">{gun_kisa}</span>
                <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;
                                display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:9px;color:#fff;font-weight:700;">{gun_giris}</span></div></div>
            </div>""", unsafe_allow_html=True)

        # Saat bazli yogunluk
        styled_section("Saat Bazli Yogunluk (Bugun)")
        saat_sayac = Counter()
        for z in bugun_giris:
            saat = (z.get("giris_zamani", "") or "")[11:13]
            if saat:
                saat_sayac[saat] += 1
        if saat_sayac:
            en_cok = max(saat_sayac.values())
            for s in sorted(saat_sayac.keys()):
                sayi = saat_sayac[s]
                bar_w = round(sayi / max(en_cok, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:6px;margin-bottom:2px;">
                    <span style="min-width:40px;font-size:10px;color:#94a3b8;">{s}:00</span>
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:10px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#f59e0b;border-radius:3px;"></div></div>
                    <span style="font-size:9px;color:#e2e8f0;font-weight:700;min-width:20px;">{sayi}</span>
                </div>""", unsafe_allow_html=True)


# ============================================================
# 2. RANDEVU AI OPTİMİZASYON MOTORU
# ============================================================

def render_ai_randevu(store):
    """AI ile randevu optimizasyonu — no-show tahmini + akilli slot."""
    styled_section("AI Randevu Optimizasyon", "#7c3aed")
    styled_info_banner(
        "Gelmeme riskini tahmin edin, akilli slot onerin, "
        "bekleme listesi yonetin. AI ile randevu surecini optimize edin.",
        banner_type="info", icon="🧠")

    randevular = store.load_list("randevular") if hasattr(store, "load_list") else []
    bugun = date.today().isoformat()

    # Gelmeme orani hesapla
    toplam = len(randevular)
    gelmedi = sum(1 for r in randevular if r.get("durum") == "Gelmedi")
    tamamlandi = sum(1 for r in randevular if r.get("durum") == "Tamamlandi")
    gelmeme_oran = round(gelmedi / max(toplam, 1) * 100, 1)

    styled_stat_row([
        ("Toplam Randevu", str(toplam), "#7c3aed", "📅"),
        ("Tamamlandi", str(tamamlandi), "#10b981", "✅"),
        ("Gelmedi", str(gelmedi), "#ef4444", "❌"),
        ("Gelmeme Orani", f"%{gelmeme_oran}", "#f59e0b", "📊"),
    ])

    sub = st.tabs(["🔮 No-Show Tahmin", "📅 Akilli Slot", "📋 Bekleme Listesi"])

    # ═══ NO-SHOW TAHMİN ═══
    with sub[0]:
        styled_section("Gelmeme Risk Tahmini")

        # Gelecek randevular
        gelecek = [r for r in randevular if r.get("tarih", "") >= bugun
                    and r.get("durum") in ("Beklemede", "Onaylandi")]

        if not gelecek:
            styled_info_banner("Gelecek randevu yok.", banner_type="info", icon="📅")
        else:
            # Ziyaretci bazli gelmeme gecmisi
            ziyaretci_gelmeme: dict[str, dict] = {}
            for r in randevular:
                zid = r.get("ziyaretci_adi", "?")
                if zid not in ziyaretci_gelmeme:
                    ziyaretci_gelmeme[zid] = {"toplam": 0, "gelmedi": 0}
                ziyaretci_gelmeme[zid]["toplam"] += 1
                if r.get("durum") == "Gelmedi":
                    ziyaretci_gelmeme[zid]["gelmedi"] += 1

            for r in sorted(gelecek, key=lambda x: x.get("tarih", "")):
                zid = r.get("ziyaretci_adi", "?")
                gecmis = ziyaretci_gelmeme.get(zid, {"toplam": 0, "gelmedi": 0})

                # Risk hesapla
                risk = 15  # baz risk
                if gecmis["toplam"] > 0:
                    kisisel_oran = gecmis["gelmedi"] / gecmis["toplam"]
                    risk += round(kisisel_oran * 50)
                # Pazartesi/Cuma riski
                try:
                    gun = date.fromisoformat(r["tarih"][:10]).weekday()
                    if gun == 0 or gun == 4:
                        risk += 10
                except Exception:
                    pass
                risk = min(risk, 100)

                r_renk = "#ef4444" if risk >= 60 else "#f59e0b" if risk >= 35 else "#10b981"
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid {r_renk}30;border-left:4px solid {r_renk};
                            border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-weight:700;color:#e2e8f0;font-size:12px;">{zid}</span>
                            <span style="color:#94a3b8;font-size:10px;margin-left:8px;">
                                {r.get('tarih', '')[:10]} {r.get('saat_baslangic', '')} · {r.get('randevu_turu', '')}</span>
                        </div>
                        <span style="background:{r_renk}20;color:{r_renk};padding:3px 10px;border-radius:6px;
                                    font-size:10px;font-weight:700;">%{risk} risk</span>
                    </div>
                    <div style="font-size:9px;color:#64748b;margin-top:2px;">
                        Gecmis: {gecmis['toplam']} randevu, {gecmis['gelmedi']} gelmedi · → {r.get('gorusulecek_kisi', '-')}</div>
                </div>""", unsafe_allow_html=True)

    # ═══ AKILLI SLOT ═══
    with sub[1]:
        styled_section("Akilli Slot Onerisi")
        styled_info_banner(
            "Yogunluk analizine gore en uygun randevu saatlerini onerin.",
            banner_type="info", icon="📅")

        # Saat bazli yogunluk (tum randevular)
        saat_yogunluk = Counter()
        for r in randevular:
            saat = r.get("saat_baslangic", "")[:2]
            if saat:
                saat_yogunluk[saat] += 1

        # Ayarlardan calisma saatleri
        ayarlar = store.load_list("rzy_ayarlar") if hasattr(store, "load_list") else []
        ayar = ayarlar[0] if ayarlar else {}
        bas_saat = int(ayar.get("calisma_baslangic", "08")[:2]) if ayar.get("calisma_baslangic") else 8
        bit_saat = int(ayar.get("calisma_bitis", "17")[:2]) if ayar.get("calisma_bitis") else 17

        styled_section("Saat Bazli Yogunluk + Oneri")
        en_cok = max(saat_yogunluk.values()) if saat_yogunluk else 1
        for s in range(bas_saat, bit_saat + 1):
            saat_key = f"{s:02d}"
            sayi = saat_yogunluk.get(saat_key, 0)
            yogunluk_pct = round(sayi / max(en_cok, 1) * 100)
            renk = "#ef4444" if yogunluk_pct > 70 else "#f59e0b" if yogunluk_pct > 40 else "#10b981"
            oneri = "Yogun — kacinilmali" if yogunluk_pct > 70 else "Orta" if yogunluk_pct > 40 else "Ideal — onerin!"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="min-width:50px;font-size:11px;color:#e2e8f0;font-weight:600;">{saat_key}:00</span>
                <div style="flex:1;background:#1e293b;border-radius:3px;height:18px;overflow:hidden;">
                    <div style="width:{yogunluk_pct}%;height:100%;background:{renk};border-radius:3px;
                                display:flex;align-items:center;padding-left:6px;">
                        <span style="font-size:8px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                <span style="min-width:120px;font-size:9px;color:{renk};font-weight:600;">{oneri}</span>
            </div>""", unsafe_allow_html=True)

    # ═══ BEKLEME LİSTESİ ═══
    with sub[2]:
        styled_section("Bekleme Listesi")
        bekleme_path = os.path.join(_td(), "randevu", "bekleme_listesi.json")
        bekleme = _lj(bekleme_path)

        if bekleme:
            for b in bekleme:
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #7c3aed30;border-radius:10px;
                            padding:8px 14px;margin-bottom:4px;">
                    <span style="font-weight:600;color:#e2e8f0;font-size:12px;">{b.get('ad', '')}</span>
                    <span style="color:#94a3b8;font-size:10px;margin-left:8px;">
                        {b.get('konu', '')} · {b.get('tercih_gun', 'Herhangi gun')}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Bekleme listesi bos.")

        # Yeni bekleme kaydi
        with st.form("bekleme_form"):
            bc1, bc2 = st.columns(2)
            with bc1:
                b_ad = st.text_input("Ad Soyad", key="bk_ad")
                b_konu = st.text_input("Konu", key="bk_konu")
            with bc2:
                b_tel = st.text_input("Telefon", key="bk_tel")
                b_gun = st.selectbox("Tercih Gunu", ["Herhangi", "Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma"], key="bk_gun")
            if st.form_submit_button("Bekleme Listesine Ekle", type="primary"):
                if b_ad:
                    bekleme.append({
                        "id": f"bk_{uuid.uuid4().hex[:8]}",
                        "ad": b_ad, "telefon": b_tel, "konu": b_konu,
                        "tercih_gun": b_gun, "tarih": date.today().isoformat(),
                    })
                    _sj(bekleme_path, bekleme)
                    st.success(f"Bekleme listesine eklendi: {b_ad}")
                    st.rerun()


# ============================================================
# 3. 360° GÖRÜŞME TAKİP SİSTEMİ
# ============================================================

def render_gorusme_360(store):
    """Gorusmenin tam yasam dongusu — oncesi/sirasi/sonrasi."""
    styled_section("360 Gorusme Takip", "#059669")
    styled_info_banner(
        "Gorusme oncesi hazirlik + gorusme sirasi not alma + sonrasi aksiyon takibi. "
        "Veli profilini bilerek gorusmeye girin.",
        banner_type="info", icon="🔍")

    randevular = store.load_list("randevular") if hasattr(store, "load_list") else []
    gorusme_notlari = store.load_list("gorusme_notlari") if hasattr(store, "load_list") else []
    bugun = date.today().isoformat()

    # Bugunun randevulari
    bugun_randevular = [r for r in randevular if r.get("tarih", "")[:10] == bugun
                         and r.get("durum") in ("Beklemede", "Onaylandi")]

    styled_stat_row([
        ("Bugun Randevu", str(len(bugun_randevular)), "#059669", "📅"),
        ("Toplam Not", str(len(gorusme_notlari)), "#2563eb", "📝"),
    ])

    sub = st.tabs(["📋 Bugun Hazirlik", "📊 Konu Trendi", "🤖 AI Gorusme Asistan"])

    # ═══ BUGÜN HAZIRLIK ═══
    with sub[0]:
        styled_section("Bugunun Gorusmeleri — Hazirlik Kartlari")

        if not bugun_randevular:
            styled_info_banner("Bugun randevu yok.", banner_type="info", icon="📅")
        else:
            for r in sorted(bugun_randevular, key=lambda x: x.get("saat_baslangic", "")):
                ziyaretci = r.get("ziyaretci_adi", "?")
                saat = r.get("saat_baslangic", "--:--")
                konu = r.get("konu", "-")
                tur = r.get("randevu_turu", "-")
                kisi = r.get("gorusulecek_kisi", "-")
                alan = r.get("gorusme_alani", "-")

                # Onceki gorusmeler
                onceki = [rr for rr in randevular if rr.get("ziyaretci_adi") == ziyaretci
                           and rr.get("durum") == "Tamamlandi" and rr.get("tarih", "") < bugun]
                onceki_not = [n for n in gorusme_notlari
                               if n.get("randevu_id") in [rr.get("id") for rr in onceki]]

                # Sikayet gecmisi
                td = _td()
                sikayetler = _lj(os.path.join(td, "kim01_sikayet_oneri.json"))
                kisi_sikayet = [s for s in sikayetler if ziyaretci.lower() in (s.get("bildiren", "") or "").lower()]

                with st.expander(f"📅 {saat} — {ziyaretci} ({tur})", expanded=len(bugun_randevular) <= 3):
                    # Hazirlik karti
                    st.markdown(f"""
                    <div style="background:#0f172a;border:1px solid #05966940;border-radius:12px;
                                padding:14px 18px;margin-bottom:8px;">
                        <div style="font-size:14px;font-weight:800;color:#6ee7b7;margin-bottom:8px;">
                            Hazirlik Karti — {ziyaretci}</div>
                        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:11px;color:#94a3b8;">
                            <div>Saat: <b style="color:#e2e8f0;">{saat}</b></div>
                            <div>Tur: <b style="color:#e2e8f0;">{tur}</b></div>
                            <div>Gorusulecek: <b style="color:#e2e8f0;">{kisi}</b></div>
                            <div>Alan: <b style="color:#e2e8f0;">{alan}</b></div>
                            <div>Konu: <b style="color:#e2e8f0;">{konu}</b></div>
                            <div>Onceki Gorusme: <b style="color:#e2e8f0;">{len(onceki)}</b></div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                    # Gecmis notlar
                    if onceki_not:
                        st.markdown("**Onceki Gorusme Notlari:**")
                        for n in onceki_not[-3:]:
                            st.caption(f"- {n.get('not_metni', '')[:150]} ({n.get('created_at', '')[:10]})")

                    # Sikayet gecmisi
                    if kisi_sikayet:
                        st.markdown(f"**Sikayet Gecmisi ({len(kisi_sikayet)}):**")
                        for s in kisi_sikayet[-2:]:
                            st.caption(f"- {s.get('konu', '')} ({s.get('durum', '')})")

                    # Hizli not ekleme
                    not_txt = st.text_area(f"Gorusme Notu — {ziyaretci}", key=f"g360_not_{r.get('id', '')}", height=60)
                    aksiyon = st.text_input(f"Aksiyon — {ziyaretci}", key=f"g360_aks_{r.get('id', '')}",
                                             placeholder="Ornek: Rehberlige yonlendir")
                    memnuniyet = st.slider(f"Memnuniyet — {ziyaretci}", 1, 5, 3, key=f"g360_mem_{r.get('id', '')}")

                    if st.button(f"Kaydet", key=f"g360_btn_{r.get('id', '')}", type="primary"):
                        if not_txt:
                            yeni_not = {
                                "id": f"gn_{uuid.uuid4().hex[:8]}",
                                "randevu_id": r.get("id", ""),
                                "randevu_kodu": r.get("randevu_kodu", ""),
                                "yazan_kisi_adi": "Gorusmeci",
                                "not_metni": not_txt,
                                "aksiyon": aksiyon,
                                "memnuniyet": memnuniyet,
                                "gizli": False,
                                "created_at": datetime.now().isoformat(),
                            }
                            gorusme_notlari.append(yeni_not)
                            store.save_list("gorusme_notlari", [n if isinstance(n, dict) else n.to_dict() for n in gorusme_notlari])
                            st.success(f"Not kaydedildi: {ziyaretci}")
                            st.rerun()

    # ═══ KONU TRENDİ ═══
    with sub[1]:
        styled_section("Gorusme Konu Trendi")
        tur_sayac = Counter(r.get("randevu_turu", "Diger") for r in randevular)
        konu_sayac = Counter()
        for n in gorusme_notlari:
            metin = (n.get("not_metni", "") or "").lower()
            if "sikayet" in metin or "sorun" in metin:
                konu_sayac["Sikayet/Sorun"] += 1
            elif "bilgi" in metin or "soru" in metin:
                konu_sayac["Bilgi/Soru"] += 1
            elif "tesekk" in metin or "memnun" in metin:
                konu_sayac["Tessekkur/Memnuniyet"] += 1
            elif "kayit" in metin or "ucret" in metin:
                konu_sayac["Kayit/Ucret"] += 1
            else:
                konu_sayac["Genel"] += 1

        if tur_sayac:
            styled_section("Randevu Turu Dagilimi")
            en_cok = tur_sayac.most_common(1)[0][1]
            for tur, sayi in tur_sayac.most_common():
                bar_w = round(sayi / max(en_cok, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <span style="min-width:140px;font-size:11px;color:#e2e8f0;font-weight:600;">{tur}</span>
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#059669;border-radius:3px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                </div>""", unsafe_allow_html=True)

        if konu_sayac:
            styled_section("Not Icerigi Analizi")
            for konu, sayi in konu_sayac.most_common():
                st.markdown(f"- **{konu}:** {sayi} gorusme")

        # Tekrar eden ziyaretciler
        styled_section("Sik Gelen Ziyaretciler")
        ziyaretci_sayac = Counter(r.get("ziyaretci_adi", "?") for r in randevular if r.get("ziyaretci_adi"))
        sik_gelenler = [(z, s) for z, s in ziyaretci_sayac.most_common(10) if s >= 2]
        if sik_gelenler:
            for z, s in sik_gelenler:
                gelmedi_s = sum(1 for r in randevular if r.get("ziyaretci_adi") == z and r.get("durum") == "Gelmedi")
                renk = "#ef4444" if gelmedi_s > 1 else "#f59e0b" if gelmedi_s > 0 else "#10b981"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;padding:3px 0;">
                    <span style="font-size:12px;color:#e2e8f0;font-weight:600;flex:1;">{z}</span>
                    <span style="font-size:10px;color:#2563eb;">{s} randevu</span>
                    <span style="font-size:10px;color:{renk};">{gelmedi_s} gelmedi</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.caption("Tekrar eden ziyaretci yok.")

    # ═══ AI GÖRÜŞME ASİSTAN ═══
    with sub[2]:
        styled_section("AI Gorusme Asistani")
        soru = st.text_area("Gorusme hakkinda soru sorun...", key="g360_ai", height=80,
                             placeholder="Ornek: Bu veli ile onceki gorusmede ne konusulmustu?")
        if st.button("AI'ya Sor", key="g360_ai_btn", type="primary"):
            if soru:
                try:
                    from utils.smarti_helper import _get_client
                    client = _get_client()
                    if client:
                        notlar_ozet = "\n".join(f"- {n.get('not_metni', '')[:100]}" for n in gorusme_notlari[-20:])
                        with st.spinner("AI dusunuyor..."):
                            resp = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "Sen bir okul randevu/gorusme yonetim uzmanisin. Verilen gorusme notlarina dayanarak soruyu cevapla. Turkce."},
                                    {"role": "user", "content": f"Soru: {soru}\n\nGorusme Notlari:\n{notlar_ozet or 'Not yok'}"},
                                ],
                                max_tokens=400, temperature=0.6,
                            )
                            ai = resp.choices[0].message.content or ""
                        if ai:
                            st.markdown(f"""
                            <div style="background:linear-gradient(135deg,#052e16,#065f46);border:1px solid #059669;
                                        border-radius:14px;padding:16px 20px;">
                                <div style="font-size:12px;color:#6ee7b7;font-weight:700;margin-bottom:6px;">AI Cevap</div>
                                <div style="font-size:12px;color:#d1fae5;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.warning("OpenAI API bulunamadi.")
                except Exception as e:
                    st.error(f"Hata: {e}")
