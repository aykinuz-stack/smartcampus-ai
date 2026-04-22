"""
Randevu & Ziyaretci — ULTRA MEGA Ozellikleri
===============================================
1. Ziyaretci Deneyim Motoru (Visitor Experience Engine)
2. Akilli Ziyaretci CRM (Visitor Relationship Manager)
3. Randevu Performans Zekasi + Tahmin Paneli (Appointment BI)
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
# 1. ZİYARETÇİ DENEYİM MOTORU
# ============================================================

_DENEYIM_SORULARI = [
    {"id": "karsilama", "soru": "Karsilama nasil?", "ikon": "🤝"},
    {"id": "bekleme", "soru": "Bekleme suresi?", "ikon": "⏰"},
    {"id": "gorusme", "soru": "Gorusme kalitesi?", "ikon": "💬"},
]


def _deneyim_path() -> str:
    return os.path.join(_td(), "randevu", "deneyim_anket.json")


def render_deneyim_motoru(store):
    """Ziyaretci deneyim motoru — yolculuk + anket + skor."""
    styled_section("Ziyaretci Deneyim Motoru", "#8b5cf6")
    styled_info_banner(
        "Ziyaretcinin okula gelistiginden cikisina kadar tum deneyimini olcun. "
        "30 saniyelik anket + deneyim skoru + mesaj sablonlari.",
        banner_type="info", icon="✨")

    randevular = store.load_list("randevular") if hasattr(store, "load_list") else []
    ziyaret_kayitlari = store.load_list("ziyaret_kayitlari") if hasattr(store, "load_list") else []
    anketler = _lj(_deneyim_path())

    # Deneyim skoru
    if anketler:
        tum_p = []
        for a in anketler:
            for s in _DENEYIM_SORULARI:
                p = a.get("cevaplar", {}).get(s["id"], 0)
                if p > 0:
                    tum_p.append(p)
        deneyim_ort = round(sum(tum_p) / max(len(tum_p), 1) / 5 * 100, 1) if tum_p else 0
    else:
        deneyim_ort = 0

    # Bekleme suresi ortalamasi
    bekleme_sureleri = []
    for z in ziyaret_kayitlari:
        if z.get("giris_zamani") and z.get("cikis_zamani"):
            try:
                giris = datetime.fromisoformat(z["giris_zamani"][:19])
                cikis = datetime.fromisoformat(z["cikis_zamani"][:19])
                dk = (cikis - giris).total_seconds() / 60
                if 0 < dk < 300:
                    bekleme_sureleri.append(dk)
            except Exception:
                pass
    ort_bekleme = round(sum(bekleme_sureleri) / max(len(bekleme_sureleri), 1)) if bekleme_sureleri else 0

    gelmeme = sum(1 for r in randevular if r.get("durum") == "Gelmedi")
    gelmeme_oran = round(gelmeme / max(len(randevular), 1) * 100, 1)
    tekrar_gelenler = sum(1 for z, s in Counter(r.get("ziyaretci_adi", "") for r in randevular).items() if s >= 2)

    d_renk = "#10b981" if deneyim_ort >= 70 else "#f59e0b" if deneyim_ort >= 50 else "#ef4444"

    styled_stat_row([
        ("Deneyim Skoru", f"{deneyim_ort}" if deneyim_ort else "—", d_renk, "⭐"),
        ("Ort. Bekleme", f"{ort_bekleme} dk", "#f59e0b", "⏰"),
        ("Gelmeme", f"%{gelmeme_oran}", "#ef4444", "❌"),
        ("Tekrar Gelen", str(tekrar_gelenler), "#10b981", "🔄"),
        ("Anket Sayisi", str(len(anketler)), "#7c3aed", "📋"),
    ])

    # ── HERO ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#3b0764 0%,#581c87 100%);
                border:2px solid {d_renk};border-radius:20px;padding:24px;margin:0 0 16px 0;
                box-shadow:0 8px 32px {d_renk}30;text-align:center;">
        <div style="font-size:10px;color:#c4b5fd;letter-spacing:3px;text-transform:uppercase;">Ziyaretci Deneyim Endeksi</div>
        <div style="font-size:64px;font-weight:900;color:{d_renk};
                    font-family:Playfair Display,Georgia,serif;line-height:1;margin:8px 0;">{deneyim_ort or '—'}</div>
        <div style="font-size:12px;color:#c4b5fd;">{len(anketler)} anket · Ort. bekleme: {ort_bekleme} dk</div>
    </div>""", unsafe_allow_html=True)

    sub = st.tabs(["📋 Deneyim Anketi", "💬 Mesaj Sablonlari", "📊 Sonuclar"])

    # ═══ ANKET ═══
    with sub[0]:
        styled_section("Hizli Deneyim Anketi (Cikista)")
        with st.form("deneyim_form"):
            st.caption("Ziyaretci cikisinda 30 saniyelik hizli anket")
            ziyaretci_ad = st.text_input("Ziyaretci Adi", key="dx_ad")
            cevaplar = {}
            for s in _DENEYIM_SORULARI:
                cevaplar[s["id"]] = st.slider(f"{s['ikon']} {s['soru']}", 1, 5, 3, key=f"dx_{s['id']}")
            yorum = st.text_input("Ek yorum (istege bagli)", key="dx_yorum")

            if st.form_submit_button("Kaydet", type="primary"):
                if ziyaretci_ad:
                    anketler.append({
                        "id": f"dx_{uuid.uuid4().hex[:8]}",
                        "ziyaretci": ziyaretci_ad, "cevaplar": cevaplar,
                        "yorum": yorum, "tarih": date.today().isoformat(),
                    })
                    _sj(_deneyim_path(), anketler)
                    st.success("Deneyim anketi kaydedildi!")
                    st.rerun()

    # ═══ MESAJ ŞABLONLARI ═══
    with sub[1]:
        styled_section("WhatsApp Mesaj Sablonlari")
        sablonlar = {
            "hos_geldin": "Merhaba! Okulumuza hosgeldiniz. Randevunuz {tarih} {saat} icin planlanmistir. Gorusme yeriniz: {alan}. Iyi gunler dileriz.",
            "yol_tarifi": "Okulumuza ulasim: {adres}\nOtopark: Ziyaretci otoparkini kullanabilirsiniz.\nKapida guvenlik gorevlisine randevu kodunuzu gostermeniz yeterlidir.",
            "hatirlatma": "Hatirlatma: Yarin saat {saat}'da randevunuz var. Gorusulecek kisi: {kisi}. Sizi bekliyoruz!",
            "gelmedi": "Bugunku randevunuza katilamamissiniz. Yeni bir randevu almak icin bizimle iletisime gecebilirsiniz.",
            "tesekkur": "Ziyaretiniz icin tesekkur ederiz! Gorusmemizin faydali olmasini umuyoruz. Herhangi bir sorunuz olursa bize ulasabilirsiniz.",
        }
        for key, sablon in sablonlar.items():
            label = key.replace("_", " ").title()
            with st.expander(f"💬 {label}"):
                st.text_area(f"Sablon — {label}", value=sablon, height=80, key=f"dx_sab_{key}")
                st.caption("Kopyalayip WhatsApp'ta gonderebilirsiniz.")

    # ═══ SONUÇLAR ═══
    with sub[2]:
        styled_section("Deneyim Anket Sonuclari")
        if not anketler:
            styled_info_banner("Henuz anket yok.", banner_type="info", icon="📋")
        else:
            for s in _DENEYIM_SORULARI:
                puanlar = [a.get("cevaplar", {}).get(s["id"], 0) for a in anketler if a.get("cevaplar", {}).get(s["id"], 0) > 0]
                ort = round(sum(puanlar) / max(len(puanlar), 1), 1) if puanlar else 0
                bar_w = round(ort / 5 * 100)
                renk = "#10b981" if ort >= 4 else "#f59e0b" if ort >= 3 else "#ef4444"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                    <span style="font-size:14px;">{s['ikon']}</span>
                    <span style="min-width:140px;font-size:12px;color:#e2e8f0;font-weight:600;">{s['soru']}</span>
                    <div style="flex:1;background:#1e293b;border-radius:4px;height:18px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:4px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">{ort}/5</span></div></div>
                </div>""", unsafe_allow_html=True)

            # Yorumlar
            yorumlar = [a.get("yorum", "") for a in anketler if a.get("yorum", "").strip()]
            if yorumlar:
                styled_section("Ziyaretci Yorumlari")
                for y in yorumlar[-10:]:
                    st.markdown(f'<div style="background:#0f172a;border-left:3px solid #8b5cf6;border-radius:0 8px 8px 0;padding:6px 12px;margin-bottom:4px;font-size:11px;color:#c4b5fd;font-style:italic;">"{y}"</div>', unsafe_allow_html=True)


# ============================================================
# 2. AKILLI ZİYARETÇİ CRM
# ============================================================

def render_ziyaretci_crm(store):
    """Ziyaretci CRM — kisi bazli tum gecmis tek ekranda."""
    styled_section("Ziyaretci CRM", "#0891b2")
    styled_info_banner(
        "Her ziyaretcinin tum gecmisini tek ekranda gorun. "
        "Randevu + giris-cikis + not + sikayet + memnuniyet.",
        banner_type="info", icon="👤")

    randevular = store.load_list("randevular") if hasattr(store, "load_list") else []
    ziyaret_kayitlari = store.load_list("ziyaret_kayitlari") if hasattr(store, "load_list") else []
    gorusme_notlari = store.load_list("gorusme_notlari") if hasattr(store, "load_list") else []
    ziyaretciler = store.load_list("ziyaretciler") if hasattr(store, "load_list") else []
    anketler = _lj(os.path.join(_td(), "randevu", "deneyim_anket.json"))

    # Benzersiz ziyaretci listesi
    isimler = set()
    for r in randevular:
        if r.get("ziyaretci_adi"):
            isimler.add(r["ziyaretci_adi"])
    for z in ziyaret_kayitlari:
        if z.get("ziyaretci_adi"):
            isimler.add(z["ziyaretci_adi"])
    for zc in ziyaretciler:
        ad = f"{zc.get('ad', '')} {zc.get('soyad', '')}".strip()
        if ad:
            isimler.add(ad)

    styled_stat_row([
        ("Toplam Ziyaretci", str(len(isimler)), "#0891b2", "👤"),
        ("Toplam Randevu", str(len(randevular)), "#2563eb", "📅"),
        ("Toplam Ziyaret", str(len(ziyaret_kayitlari)), "#10b981", "🚶"),
    ])

    # Arama
    arama = st.text_input("Ziyaretci Ara", key="zcrm_ara", placeholder="Isim yazin...")

    if not arama or len(arama) < 2:
        # En sik gelen 10 ziyaretci
        styled_section("Sik Gelen Ziyaretciler")
        sik = Counter(r.get("ziyaretci_adi", "") for r in randevular if r.get("ziyaretci_adi")).most_common(10)
        for z, sayi in sik:
            gelmedi = sum(1 for r in randevular if r.get("ziyaretci_adi") == z and r.get("durum") == "Gelmedi")
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:4px 0;">
                <span style="flex:1;font-size:12px;color:#e2e8f0;font-weight:600;">{z}</span>
                <span style="font-size:10px;color:#0891b2;">{sayi} randevu</span>
                <span style="font-size:10px;color:{'#ef4444' if gelmedi > 0 else '#10b981'};">{gelmedi} gelmedi</span>
            </div>""", unsafe_allow_html=True)
        return

    q = arama.strip().lower()
    eslesen = sorted([i for i in isimler if q in i.lower()])

    if not eslesen:
        styled_info_banner(f'"{arama}" ile eslesen ziyaretci bulunamadi.', banner_type="warning", icon="🔍")
        return

    st.caption(f"{len(eslesen)} sonuc")

    for ziyaretci in eslesen[:5]:
        # Randevu gecmisi
        kisi_randevu = sorted([r for r in randevular if r.get("ziyaretci_adi") == ziyaretci],
                                key=lambda x: x.get("tarih", ""), reverse=True)
        kisi_ziyaret = [z for z in ziyaret_kayitlari if z.get("ziyaretci_adi") == ziyaretci]
        kisi_not = []
        for r in kisi_randevu:
            kisi_not.extend([n for n in gorusme_notlari if n.get("randevu_id") == r.get("id")])
        kisi_anket = [a for a in anketler if a.get("ziyaretci", "").lower() == ziyaretci.lower()]

        # Sikayet (KOI)
        sikayetler = _lj(os.path.join(_td(), "kim01_sikayet_oneri.json"))
        kisi_sikayet = [s for s in sikayetler if ziyaretci.lower() in (s.get("bildiren", "") or "").lower()]

        # Iliski skoru
        skor = 50
        skor += min(len(kisi_randevu) * 3, 15)
        skor += min(len(kisi_ziyaret) * 2, 10)
        gelmedi = sum(1 for r in kisi_randevu if r.get("durum") == "Gelmedi")
        skor -= min(gelmedi * 8, 20)
        skor -= min(len(kisi_sikayet) * 5, 15)
        if kisi_anket:
            ort = sum(sum(a.get("cevaplar", {}).values()) for a in kisi_anket) / max(len(kisi_anket) * 3, 1)
            skor += round((ort - 3) * 5)
        skor = max(0, min(100, skor))
        s_renk = "#10b981" if skor >= 70 else "#f59e0b" if skor >= 45 else "#ef4444"

        with st.expander(f"👤 {ziyaretci} — Skor: {skor}/100 · {len(kisi_randevu)} randevu", expanded=len(eslesen) == 1):
            # Hero
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {s_renk}40;border-radius:14px;
                        padding:16px;margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-size:18px;font-weight:900;color:#fff;">{ziyaretci}</div>
                    <div style="text-align:center;">
                        <div style="font-size:32px;font-weight:900;color:{s_renk};">{skor}</div>
                        <div style="font-size:8px;color:#94a3b8;">ILISKI SKORU</div>
                    </div>
                </div>
                <div style="display:flex;gap:12px;margin-top:8px;font-size:10px;color:#94a3b8;">
                    <span>{len(kisi_randevu)} randevu</span>
                    <span>{len(kisi_ziyaret)} ziyaret</span>
                    <span>{gelmedi} gelmedi</span>
                    <span>{len(kisi_sikayet)} sikayet</span>
                    <span>{len(kisi_anket)} anket</span>
                </div>
            </div>""", unsafe_allow_html=True)

            # Timeline
            timeline = []
            for r in kisi_randevu[:10]:
                durum_renk = {"Tamamlandi": "#10b981", "Gelmedi": "#ef4444", "Iptal": "#94a3b8"}.get(r.get("durum", ""), "#3b82f6")
                timeline.append({
                    "tarih": r.get("tarih", "")[:10], "tip": f"📅 {r.get('randevu_turu', 'Randevu')}",
                    "detay": f"{r.get('konu', '-')} → {r.get('gorusulecek_kisi', '-')} [{r.get('durum', '')}]",
                    "renk": durum_renk,
                })
            for n in kisi_not[:5]:
                timeline.append({
                    "tarih": (n.get("created_at", "") or "")[:10], "tip": "📝 Gorusme Notu",
                    "detay": (n.get("not_metni", "") or "")[:100], "renk": "#7c3aed",
                })
            for s in kisi_sikayet[:3]:
                timeline.append({
                    "tarih": (s.get("created_at", "") or "")[:10], "tip": "📝 Sikayet",
                    "detay": s.get("konu", ""), "renk": "#ef4444",
                })
            timeline.sort(key=lambda x: x["tarih"], reverse=True)

            if timeline:
                st.markdown("**Etkilesim Gecmisi:**")
                for t in timeline[:12]:
                    st.markdown(f"""
                    <div style="display:flex;gap:8px;padding:3px 0;border-left:3px solid {t['renk']};padding-left:10px;margin-bottom:3px;">
                        <span style="min-width:65px;font-size:9px;color:#64748b;">{t['tarih']}</span>
                        <span style="font-size:10px;font-weight:700;color:{t['renk']};">{t['tip']}</span>
                        <span style="font-size:10px;color:#94a3b8;flex:1;">{t['detay']}</span>
                    </div>""", unsafe_allow_html=True)


# ============================================================
# 3. APPOINTMENT BI (RANDEVU İŞ ZEKASI)
# ============================================================

def render_appointment_bi(store):
    """Randevu performans zekasi + tahmin paneli."""
    styled_section("Appointment BI", "#f59e0b")
    styled_info_banner(
        "Randevu verilerinden stratejik is zekasi. "
        "Verimlilik + tahmin + korelasyon analizi.",
        banner_type="info", icon="📊")

    randevular = store.load_list("randevular") if hasattr(store, "load_list") else []
    ziyaret_kayitlari = store.load_list("ziyaret_kayitlari") if hasattr(store, "load_list") else []

    toplam = len(randevular)
    tamamlandi = sum(1 for r in randevular if r.get("durum") == "Tamamlandi")
    gelmedi = sum(1 for r in randevular if r.get("durum") == "Gelmedi")
    iptal = sum(1 for r in randevular if r.get("durum") == "Iptal")
    donusum = round(tamamlandi / max(toplam, 1) * 100, 1)

    styled_stat_row([
        ("Toplam Randevu", str(toplam), "#f59e0b", "📅"),
        ("Tamamlandi", str(tamamlandi), "#10b981", "✅"),
        ("Gelmedi", str(gelmedi), "#ef4444", "❌"),
        ("Donusum", f"%{donusum}", "#2563eb", "📊"),
    ])

    sub = st.tabs(["📊 Verimlilik", "🔮 Tahmin", "🔗 Korelasyon"])

    # ═══ VERİMLİLİK ═══
    with sub[0]:
        styled_section("Gorusulecek Kisi Bazli Verimlilik")

        kisi_stats: dict[str, dict] = {}
        for r in randevular:
            kisi = r.get("gorusulecek_kisi", "Belirtilmedi")
            if kisi not in kisi_stats:
                kisi_stats[kisi] = {"toplam": 0, "tamamlandi": 0, "gelmedi": 0}
            kisi_stats[kisi]["toplam"] += 1
            if r.get("durum") == "Tamamlandi":
                kisi_stats[kisi]["tamamlandi"] += 1
            elif r.get("durum") == "Gelmedi":
                kisi_stats[kisi]["gelmedi"] += 1

        if kisi_stats:
            sirali = sorted(kisi_stats.items(), key=lambda x: -x[1]["tamamlandi"])
            for kisi, stats in sirali[:15]:
                oran = round(stats["tamamlandi"] / max(stats["toplam"], 1) * 100)
                bar_w = min(oran, 100)
                renk = "#10b981" if oran >= 80 else "#f59e0b" if oran >= 60 else "#ef4444"
                st.markdown(f"""
                <div style="background:#0f172a;border:1px solid #1e293b;border-left:4px solid {renk};
                            border-radius:0 10px 10px 0;padding:8px 14px;margin-bottom:6px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                        <span style="font-weight:700;color:#e2e8f0;font-size:12px;">{kisi}</span>
                        <div style="display:flex;gap:8px;font-size:10px;">
                            <span style="color:#10b981;">{stats['tamamlandi']} tamam</span>
                            <span style="color:#ef4444;">{stats['gelmedi']} gelmedi</span>
                            <span style="color:{renk};font-weight:700;">%{oran}</span>
                        </div>
                    </div>
                    <div style="background:#1e293b;border-radius:3px;height:6px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{renk};border-radius:3px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

        # Randevu turu verimlilik
        styled_section("Randevu Turu Verimlilik")
        tur_stats = Counter()
        tur_tamam = Counter()
        for r in randevular:
            tur = r.get("randevu_turu", "Diger")
            tur_stats[tur] += 1
            if r.get("durum") == "Tamamlandi":
                tur_tamam[tur] += 1

        for tur, toplam_t in tur_stats.most_common():
            tamam_t = tur_tamam.get(tur, 0)
            oran = round(tamam_t / max(toplam_t, 1) * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="min-width:140px;font-size:11px;color:#e2e8f0;font-weight:600;">{tur}</span>
                <span style="font-size:10px;color:#94a3b8;min-width:60px;">{toplam_t} randevu</span>
                <span style="font-size:10px;color:#10b981;font-weight:700;">%{oran} basari</span>
            </div>""", unsafe_allow_html=True)

    # ═══ TAHMİN ═══
    with sub[1]:
        styled_section("Haftalik Tahmin")

        # Mevsimsellik — ay bazli randevu sayilari
        ay_sayac = Counter()
        for r in randevular:
            ay = r.get("tarih", "")[:7]
            if ay:
                ay_sayac[ay] += 1

        if ay_sayac:
            styled_section("Aylik Randevu Trendi (Mevsimsellik)")
            en_cok = max(ay_sayac.values())
            for ay, sayi in sorted(ay_sayac.items()):
                bar_w = round(sayi / max(en_cok, 1) * 100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                    <span style="min-width:60px;font-size:10px;color:#94a3b8;">{ay}</span>
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:12px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#f59e0b;border-radius:3px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:8px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                </div>""", unsafe_allow_html=True)

        # Bu hafta tahmini
        bugun = date.today()
        bu_hafta = bugun - timedelta(days=bugun.weekday())
        bu_hafta_rnd = sum(1 for r in randevular if r.get("tarih", "")[:10] >= bu_hafta.isoformat())

        # Gecen hafta
        gecen_hafta = bu_hafta - timedelta(weeks=1)
        gecen_hafta_rnd = sum(1 for r in randevular
                               if gecen_hafta.isoformat() <= r.get("tarih", "")[:10] < bu_hafta.isoformat())

        tahmini_gelmeme = round(bu_hafta_rnd * gelmedi / max(toplam, 1))

        st.markdown(f"""
        <div style="background:#0f172a;border:2px solid #f59e0b;border-radius:16px;
                    padding:16px;text-align:center;margin:12px 0;">
            <div style="font-size:10px;color:#94a3b8;">Bu Hafta Tahmini</div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:8px;">
                <div><div style="font-size:28px;font-weight:900;color:#f59e0b;">{bu_hafta_rnd}</div>
                    <div style="font-size:9px;color:#64748b;">Randevu</div></div>
                <div><div style="font-size:28px;font-weight:900;color:#ef4444;">{tahmini_gelmeme}</div>
                    <div style="font-size:9px;color:#64748b;">Tahmini Gelmeme</div></div>
                <div><div style="font-size:28px;font-weight:900;color:#64748b;">{gecen_hafta_rnd}</div>
                    <div style="font-size:9px;color:#64748b;">Gecen Hafta</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Gun bazli yogunluk
        styled_section("Gun Bazli Yogunluk")
        gun_adlari = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
        gun_sayac = Counter()
        for r in randevular:
            try:
                dt = date.fromisoformat(r["tarih"][:10])
                gun_sayac[gun_adlari[dt.weekday()]] += 1
            except Exception:
                pass

        if gun_sayac:
            en_yogun = gun_sayac.most_common(1)[0]
            for gun in gun_adlari[:5]:
                sayi = gun_sayac.get(gun, 0)
                bar_w = round(sayi / max(en_yogun[1], 1) * 100)
                is_best = gun == en_yogun[0]
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                    <span style="min-width:70px;font-size:11px;color:{'#f59e0b' if is_best else '#94a3b8'};
                                font-weight:{'800' if is_best else '400'};">{'⭐ ' if is_best else ''}{gun}</span>
                    <div style="flex:1;background:#1e293b;border-radius:3px;height:14px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:#f59e0b;border-radius:3px;
                                    display:flex;align-items:center;padding-left:6px;">
                            <span style="font-size:9px;color:#fff;font-weight:700;">{sayi}</span></div></div>
                </div>""", unsafe_allow_html=True)

    # ═══ KORELASYON ═══
    with sub[2]:
        styled_section("Korelasyon Analizi")

        # Kayit modulu baglantisi
        kayit_aday = 0
        try:
            from models.kayit_modulu import get_kayit_store
            adaylar = get_kayit_store().load_all()
            kayit_gorusme = [r for r in randevular if r.get("randevu_turu") in ("Kayit Gorusmesi", "Kayıt Görüşmesi")]
            kayit_kesin = sum(1 for a in adaylar if a.asama == "kesin_kayit")
            kayit_aday = len(adaylar)
        except Exception:
            kayit_gorusme = []
            kayit_kesin = 0

        korelasyonlar = [
            {"kaynak": "Toplam Randevu", "hedef": "Tamamlanan", "k_val": toplam, "h_val": tamamlandi,
             "yorum": "Randevu sayisi artinca tamamlanma artiyor mu?", "renk": "#2563eb"},
            {"kaynak": "Kayit Gorusmesi", "hedef": "Kesin Kayit", "k_val": len(kayit_gorusme), "h_val": kayit_kesin,
             "yorum": "Kayit gorusmeleri kayita donusuyor mu?", "renk": "#10b981"},
            {"kaynak": "Gelmeme Sayisi", "hedef": "Iptal", "k_val": gelmedi, "h_val": iptal,
             "yorum": "Gelmeme artinca iptal de artiyor mu?", "renk": "#ef4444"},
        ]

        for kor in korelasyonlar:
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid {kor['renk']}30;border-left:4px solid {kor['renk']};
                        border-radius:0 12px 12px 0;padding:12px 16px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-weight:700;color:#e2e8f0;font-size:12px;">
                            {kor['kaynak']} → {kor['hedef']}</span>
                        <div style="font-size:10px;color:#64748b;margin-top:2px;">{kor['yorum']}</div>
                    </div>
                    <div style="display:flex;gap:10px;align-items:center;">
                        <div style="text-align:center;">
                            <div style="font-size:18px;font-weight:800;color:{kor['renk']};">{kor['k_val']}</div>
                            <div style="font-size:8px;color:#64748b;">Kaynak</div></div>
                        <div style="font-size:14px;color:#64748b;">→</div>
                        <div style="text-align:center;">
                            <div style="font-size:18px;font-weight:800;color:#10b981;">{kor['h_val']}</div>
                            <div style="font-size:8px;color:#64748b;">Hedef</div></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # AI Insight
        st.divider()
        if st.button("AI Randevu Analizi", key="abi_ai", type="primary"):
            try:
                from utils.smarti_helper import _get_client
                client = _get_client()
                if client:
                    veri = (f"Toplam: {toplam}, Tamamlanan: {tamamlandi}, Gelmedi: {gelmedi}, Iptal: {iptal}, "
                            f"Donusum: %{donusum}, Kayit Gorusme: {len(kayit_gorusme)}, Kesin Kayit: {kayit_kesin}")
                    with st.spinner("AI analiz ediyor..."):
                        resp = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "Sen bir okul randevu analisti. Verilen verileri analiz et. Verimlilik, tahmin, korelasyon onerileri sun. Turkce, somut."},
                                {"role": "user", "content": veri},
                            ],
                            max_tokens=500, temperature=0.7,
                        )
                        ai = resp.choices[0].message.content or ""
                    if ai:
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#78350f,#92400e);border:1px solid #f59e0b;
                                    border-radius:14px;padding:16px 20px;">
                            <div style="font-size:12px;color:#fde68a;font-weight:700;margin-bottom:6px;">AI Randevu Insight</div>
                            <div style="font-size:12px;color:#fef3c7;line-height:1.8;">{ai.replace(chr(10), '<br>')}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.warning("OpenAI API bulunamadi.")
            except Exception as e:
                st.error(f"Hata: {e}")
